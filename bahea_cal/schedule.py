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

from users.services import Credentials, CredentialsService
from users.models import UserCredential, UserEvent

SCOPES = [
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"


class ScheduleException(Exception):
    pass


def get_service(user_credentials):
    creds = Credentials.from_user_credentials(user_credentials)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            CredentialsService.update_for(user_credentials.user, creds)
        else:
            raise ScheduleException(
                f"Credentials for user %s invalid or expired, and unable to refresh", user_credentials.user.username
            )
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
                calendarId=credential.user.calendar_id,
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
            eventc = service.events().insert(calendarId=credential.user.calendar_id, body=event_dict).execute()
            event.eid = eventc["id"]
            event.save()
            print(f"Event created: {calendar_event.description} {eventc.get('htmlLink')}")
        else:
            event.eid = possible["id"]
            event.save()
            print(f"Event already in calendar: {calendar_event.description} {possible.get('htmlLink')}")


def process():
    exceptions = []
    for credential in UserCredential.objects.all():
        try:
            schedule_for(credential)
        except Exception as e:
            exceptions.append(e)
        else:
            print(f"Successfully processed for user: {credential.user.username}")

    if exceptions:
        raise exceptions[0]


if __name__ == "__main__":
    process()
