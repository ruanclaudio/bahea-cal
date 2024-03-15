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

from users.services import Credentials
from users.models import UserCredential, UserEvent

API_SERVICE_NAME = "calendar"
API_VERSION = "v3"


def get_service(user_credentials):
    credentials = Credentials.from_user_credentials(user_credentials)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def schedule_for(credential):
    service = get_service(credential)

    events = UserEvent.objects.filter(eid__isnull=True)

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
            event.eid = eventc.get("htmlLink").split("eid=")[1]
            event.save()
            print(f"Event created: {calendar_event.description} {eventc.get('htmlLink')}")
        else:
            event.eid = possible.get("htmlLink").split("eid=")[1]
            event.save()
            print(f"Event already in calendar: {calendar_event.description} {possible.get('htmlLink')}")


def process():
    for credential in UserCredential.objects.all():
        schedule_for(credential)


if __name__ == "__main__":
    process()
