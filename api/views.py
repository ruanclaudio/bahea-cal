import json
import os.path

from django.conf import settings
from django.contrib.auth import login
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from core.views import UserService
from distutils.command import build
from users.services import Credentials, CredentialsService
from webapp.secrets import get_secret
from rest_framework.decorators import api_view
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build as apiClientBuild


FULL_SECRET_PATH = 'C:/Users/ruanc/OneDrive/Documentos/Workspace/bahea-cal/webapp/secrets.json'
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

@api_view(['GET'])
def calendar_init_view(request):
    config = get_secret(f"{settings.ENVIRONMENT}/google/calendar")
    creds = CredentialsService.init_for(request.user, scopes=SCOPES)
    print("cred= ", creds)
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

            return JsonResponse({"authorization_url": authorization_url})

    return JsonResponse({"message": "Sucess"})

@api_view(['POST'])
def calendar_token(request):
    config = get_secret(f"{settings.ENVIRONMENT}/google/calendar")
    flow = Flow.from_client_config(config,scopes=SCOPES,redirect_uri="http://localhost:3000")
    code = request.data['code']
    
    try:
        flow.fetch_token(code=code)
        credentials = Credentials.from_flow(flow.credentials)

        user_service = UserService.from_credentials(credentials)
        user, _ = user_service.update_local(user_service.remote())
        user_service.check_calendar(user)

        login(request, user)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"sucess": True})
    

@api_view(["GET"])
def user_info_view(request):
    user = request.user
    creds = Credentials(
        token=user.social_auth.get(provider='google-oauth2').access_token,
        refresh_token=user.social_auth.get(provider='google-oauth2').refresh_token,
        client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        scopes=SCOPES  
    )
    service_account_info = json.load(open(FULL_SECRET_PATH))
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES) 
    
    print(creds)
    calendar_service = build('calendar', 'v3', credentials=creds)
    choiced_teams = {}
    time_to_match = {}
        
    user_info = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_email': user.email,
        'photo': user.profile.photo,
        'teams': choiced_teams,
        'time_to_match': time_to_match
    }

    return JsonResponse(user_info)