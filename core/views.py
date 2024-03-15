import os.path

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
    "https://www.googleapis.com/auth/calendar",
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
    config = get_secret("staging/google/calendar")
    creds = CredentialsService.init_for(request.user, scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(config, SCOPES)
            flow.redirect_uri = REDIRECT_URL

            authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
            request.session["state"] = state

            return redirect(authorization_url)

    return render(request, "core/success.html", {})


def google_calendar_redirect_view(request):
    state = request.session["state"]
    if state is None:
        return render(request, "core/success.html", {"error": "Algo de errado aconteceu."})

    config = get_secret("staging/google/calendar")
    flow = google_auth_oauthlib.flow.Flow.from_client_config(config, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = Credentials.from_flow(flow.credentials)

    userinfo_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = userinfo_service.userinfo().get().execute()

    email = user_info.get("email")
    User = get_user_model()
    user, created = User.objects.get_or_create(username=email, email=email)
    if created:
        user.set_unusable_password()
        user.save()

    if not CredentialsService.get_for(user):
        saved_credentials = CredentialsService.create_for(user, credentials)
    else:
        saved_credentials = CredentialsService.update_for(user, credentials)
    if not saved_credentials:
        return redirect("/calendar/init")

    saved_credentials.user = user
    saved_credentials.save(update_fields=["user"])

    user = authenticate(request, username=email)
    if user:
        login(request, user)

    try:
        service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        calendar_list = service.calendarList().list().execute()
        calendar_id = calendar_list["items"][0]["id"]
        service.events().list(calendarId=calendar_id).execute()
    except:
        return render(request, "core/error.html")
    else:
        return render(request, "core/success.html")
