import os
import pathlib
import sys

import django

project_path = pathlib.Path(__file__).parent.parent
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

django.setup()

import googleapiclient.discovery

from bahea_cal.fetch import CalendarEvent
from google.auth.transport.requests import Request

from users.services import CredentialsService
from users.models import UserCredential, UserEvent

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"


def get_service(user_credentials):
    creds = CredentialsService.init_for(user_credentials.user, scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    # credentials = Credentials.from_user_credentials(user_credentials)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def schedule_for(credential):
    service = get_service(credential)

    events = UserEvent.objects.filter(eid__isnull=True, user=credential.user)

    for event in events:
        try:
            calendar_event = CalendarEvent.from_parsed(event.event)
        except:
            print(f"Skipping: {event.match.home_team} x {event.match.away_team}")
            continue

        when = calendar_event.start_datetime

        possible_existing = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=when,
                maxResults=20,
                singleEvents=True,
                orderBy="startTime",
                timeMax=when.shift(minutes=+140),
            )
            .execute()
        )

        existent = False
        for possible in possible_existing.get("items", []):
            if possible["summary"] == calendar_event.summary:
                existent = True
                break

        if not existent:
            event_dict = calendar_event.as_dict()
            eventc = service.events().insert(calendarId="primary", body=event_dict).execute()
            event.eid = eventc["id"]
            event.save()
            print(f"Event created: {calendar_event.description} {eventc.get('htmlLink')}")
        else:
            event.eid = possible["id"]
            event.save()
            print(f"Event already in calendar: {calendar_event.description} {possible.get('htmlLink')}")


def process():
    for credential in UserCredential.objects.all():
        schedule_for(credential)


if __name__ == "__main__":
    process()
