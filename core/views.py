import os.path

import attrs
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect
from django.shortcuts import render
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from users.services import Credentials
from users.services import CredentialsService
from webapp.secrets import get_secret

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
REDIRECT_URL = f"{settings.BASE_URL}/calendar/redirect/"
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"


def home(request):
    return render(request, "core/home.html")


def google_calendar_init_view(request):
    config = get_secret(f"{settings.ENVIRONMENT}/google/calendar")
    creds = CredentialsService.init_for(request.user, scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(config, SCOPES)
            flow.redirect_uri = REDIRECT_URL

            authorization_url, state = flow.authorization_url(
                access_type="offline",
                prompt="consent", include_granted_scopes="true"
            )
            request.session["state"] = state

            return redirect(authorization_url)

    return render(request, "core/success.html", {})


def get_config():
    return get_secret(f"{settings.ENVIRONMENT}/google/calendar")

def google_calendar_redirect_view(request):
    state = request.session.get("state") or request.GET.get("state")
    if state is None:
        return render(request, "core/success.html", {"error": "Algo de errado aconteceu."})

@attrs.define
class FlowService:
    config: dict
    scopes: list
    state: str
    flow: google_auth_oauthlib.flow.Flow = attrs.field()

    @classmethod
    def from_client_config(cls, config, scopes, state):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(config, scopes, state=state)
        flow.redirect_uri = REDIRECT_URL
        return cls(config, scopes, state, flow)

    def setup(self, redirect_uri, authorization_response):
        self.flow.redirect_uri = redirect_uri
        self.flow.fetch_token(authorization_response=authorization_response)
        return self.flow


@attrs.define
class UserService:
    user_info: googleapiclient.discovery.Resource = attrs.field()
    calendar: googleapiclient.discovery.Resource = attrs.field()
    credentials: Credentials = attrs.field()

    @classmethod
    def from_credentials(cls, credentials):
        userinfo_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
        calendar = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        return cls(userinfo_service, calendar, credentials)

    def remote(self):
        return self.user_info.userinfo().get().execute()

    def update_local(self, user_info):
        email = user_info.get("email")

        User = get_user_model()
        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            user.set_unusable_password()

        user.first_name = user_info.get("given_name")
        user.last_name = user_info.get("family_name")
        user.save()

        self._update_credentials(user, self.credentials)
        self._update_calendar(user)
        return user, created

    def _update_credentials(self, user, credentials):
        if not CredentialsService.get_for(user):
            saved_credentials = CredentialsService.create_for(user, credentials)
        else:
            saved_credentials = CredentialsService.update_for(user, credentials)
        if not saved_credentials:
            return redirect("/calendar/init")

        saved_credentials.user = user
        saved_credentials.save(update_fields=["user"])

    def _update_calendar(self, user):
        if not user.calendar_id:
            calendar = {"summary": f"{settings.CALENDAR_NAME_PREFIX}BaheaCal", "timeZone": "America/Bahia"}
            created_calendar = self.calendar.calendars().insert(body=calendar).execute()
            user.calendar_id = created_calendar["id"]
            user.save(update_fields=["calendar_id"])

    def check_calendar(self, user):
        return self.calendar.events().list(calendarId=user.calendar_id).execute()


def google_calendar_redirect_view(request):
    state = request.session["state"]
    if state is None:
        return render(request, "core/success.html", {"error": "Algo de errado aconteceu."})

    try:
        config = get_config()

        flow = FlowService.from_client_config(config, SCOPES, state).setup(REDIRECT_URL, request.get_full_path())
        credentials = Credentials.from_flow(flow.credentials)

        user_service = UserService.from_credentials(credentials)
        user, _ = user_service.update_local(user_service.remote())
        user_service.check_calendar(user)

        login(request, user)
    except Exception as e:
        return render(request, "core/error.html")
    else:
        return redirect("/calendar/success/")


def google_calendar_success(request):
    return render(request, "core/success.html")