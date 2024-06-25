import json
import os.path

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from core.views import UserService
from googleapiclient.discovery import build
from users.models import UserCredential
from users.services import Credentials, CredentialsService
from webapp.secrets import get_secret
from rest_framework.decorators import api_view
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build as apiClientBuild
import googleapiclient.discovery
from pathlib import Path



ROOT_FOLDER = Path().resolve().parent
FULL_SECRET_PATH = os.path.join(ROOT_FOLDER, "webapp", "secrets.json")
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
    print('user == ', user.email)
    print('user fname== ', user.first_name)
    print('user lname == ', user.last_name)
    print('user id == ', user.id)
    print('user id == ', user.acessToken)
    # print('locale == ', user.photo)
    # print('locale == ', user.locale)
    # print('user pimage == ', user.picture)
    # print('request == ', request_data)
       
    user_creds = UserCredential.objects.get(user)
    creds = Credentials.from_user_credentials(user_creds)
    
    calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    selected_teams = {}
    notify_before = {}
        
    user_info = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'photo': user.photo,
        'selected_teams': selected_teams,
        'notify_before': notify_before
    }

    return JsonResponse(user_info)

import requests
from google.auth.transport import requests as google_requests
@api_view(["GET"])
def test_return(request):

    CLIENT_SECRETS_FILE = os.path.join(ROOT_FOLDER, "bahea-cal/webapp", "secrets2.json")

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    print(flow)
    creds = flow.run_local_server(port=0)
    def verify_id_token(id_token):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            CLIENT_ID = "600789865643-nh6ss44i17aov60br8fno3hqoihro4uh.apps.googleusercontent.com"
            # Verify the token
            idinfo = id_token.verify_oauth2_token(id_token, google_requests.Request(), CLIENT_ID)
            # ID token is valid
            return idinfo
        except ValueError:
            # Invalid token
            return None


      # Get the ID token from the credentials
    id_token_info = creds.id_token
    # Verify the ID token
    idinfo = verify_id_token(id_token_info)
    
    if idinfo:
        userinfo = {
            'sub': idinfo['sub'],
            'name': idinfo['name'],
            'given_name': idinfo['given_name'],
            'family_name': idinfo['family_name'],
            'picture': idinfo['picture'],
            'email': idinfo['email'],
            'email_verified': idinfo['email_verified'],
            'locale': idinfo['locale']
        }
    
        print("User info:", json.dumps(userinfo, indent=4)) 
        return JsonResponse({ "userInfo":json.dumps(userinfo, indent=4) })

    # url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=access_token"
    # response = requests.get(url)
    
    # data = json.loads(response.text)
    # return JsonResponse(data)