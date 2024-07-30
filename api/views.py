# Python imports
import os.path

# Pip imports
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

# Internal imports
from core.views import UserService
from users.models import UserCredential
from users.serializer import UserInfoSerializer
from users.services import Credentials, CredentialsService
from webapp.secrets import get_secret


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar",
    "openid",
]

REDIRECT_URL = f"{settings.BASE_URL}/calendar/redirect/"
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"


@api_view(["GET"])
def calendar_init_view(request):
    config = get_secret(f"{settings.ENVIRONMENT}/google/calendar")
    creds = CredentialsService.init_for(request.user, scopes=SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(config, SCOPES)
            flow.redirect_uri = REDIRECT_URL

            authorization_url, state = flow.authorization_url(
                access_type="offline", prompt="consent", include_granted_scopes="true"
            )
            request.session["state"] = state

            return JsonResponse({"authorization_url": authorization_url})

    return JsonResponse({"message": "Sucess"})


@api_view(["POST"])
def calendar_token(request):
    config = get_secret(f"{settings.ENVIRONMENT}/google/calendar")
    flow = Flow.from_client_config(config, scopes=SCOPES, redirect_uri="http://localhost:3000")
    code = request.data["code"]

    try:
        flow.fetch_token(code=code)
        credentials = Credentials.from_flow(flow.credentials)

        user_service = UserService.from_credentials(credentials)
        user, _ = user_service.update_local(user_service.remote())
        user_service.check_calendar(user)

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"sucess": True, "token": token.key})


@api_view(["GET"])
def user_info_view(request):
    credential = UserCredential.objects.get(user=request.user)
    creds = Credentials.from_user_credentials(credential)

    user_service = UserService.from_credentials(creds)
    user_service.check_calendar(credential.user)
    serializer = UserInfoSerializer(user_service.remote())
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def user_json_return(request):
    user_info = {
        "send_from": "backend",
        "given_name": "test name",
        "family_name": "family test",
        "email": "example@email.com",
        "photo": "url/path/profile/photo",
        "selected_teams": "Bahia",
        "notify_before": "2 hours",
    }

    return JsonResponse(user_info)
