import datetime
import os
import pathlib
import tempfile

import arrow
import attrs
from apiclient.discovery import build
from django.db import transaction
from httplib2 import Http
from oauth2client import file, client, tools

import sys
import django

# Add the project path to the sys.path
project_path = pathlib.Path(__file__).parent.parent
sys.path.append(str(project_path))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

django.setup()

from core.models import Team, Championship, Location, Phase, Round, Match, SoccerEvent


def get_service():
    SCOPES = "https://www.googleapis.com/auth/calendar"

    # import ipdb; ipdb.set_trace()

    token_name = os.environ.get("TOKEN_NAME")
    store = file.Storage(token_name)
    creds = store.get()
    if not creds or creds.invalid:
        with open(token_name, "w+") as token_file:
            token_file.write(os.environ.get("TOKEN_JSON"))
            with tempfile.NamedTemporaryFile("w+", delete=False) as creds_file:
                flow = client.flow_from_clientsecrets(os.environ.get("CREDENTIALS_JSON"), SCOPES)
        creds = tools.run_flow(flow, store)
        store.put(creds)
    service = build("calendar", "v3", http=creds.authorize(Http()))
    return service


now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time


@attrs.define
class CalendarEvent:
    summary: str
    description: str
    start_datetime: arrow.Arrow
    start_timezone: str
    end_datetime: arrow.Arrow
    end_timezone: str
    location: str = attrs.field(default=None)

    @classmethod
    def from_parsed(cls, event):
        match = event.match

        timezone = "America/Bahia"
        start_date = arrow.get(f"{match.startDate} {match.startHour} {timezone}", "YYYY-MM-DD HH:mm:ss ZZZ")
        return cls(
            summary=f"{match.homeTeam} x {match.awayTeam}",
            description=f"{match.championship}: {match.homeTeam} x {match.awayTeam}, {match.location}",
            start_datetime=start_date,
            start_timezone=timezone,
            end_datetime=start_date.shift(minutes=+110),
            end_timezone=timezone,
            location=match.location,
        )
        # self.__typename = kwargs.pop("__typename")
        # self.awayTeam = kwargs.pop("awayTeam")
        # self.championship = kwargs.pop("championship")
        # self.homeTeam = kwargs.pop("homeTeam")
        # self.liveWatchSources = kwargs.pop("liveWatchSources")
        # self.location = kwargs.pop("location")
        # self.phase = kwargs.pop("phase")
        # self.round = kwargs.pop("round")
        # self.scoreboard = kwargs.pop("scoreboard")
        # self.startDate = kwargs.pop("startDate")
        # self.startHour = kwargs.pop("startHour")
        # self.transmission = kwargs.pop("transmission")
        # self.winner = kwargs.pop("winner")

    def as_dict(self):
        return {
            "summary": self.summary,
            "location": str(self.location),
            "description": self.description,
            "start": {
                "dateTime": self.start_datetime.isoformat(),
                "timeZone": self.start_timezone,
            },
            "end": {
                "dateTime": self.end_datetime.isoformat(),
                "timeZone": self.end_timezone,
            },
        }


def schedule():
    from parse import parse

    service = get_service()

    soccer_events = parse()
    events = soccer_events

    for event in events:
        try:
            event = CalendarEvent.from_parsed(event)
        except:
            print(f"Skipping: {event.match.homeTeam} x {event.match.awayTeam}")
            continue

        when = event.start_datetime

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
            if possible["summary"] == event.summary:
                existent = True
                break

        if not existent:
            event_dict = event.as_dict()
            eventc = service.events().insert(calendarId="primary", body=event_dict).execute()
            print(f"Event created: {event.description} {eventc.get('htmlLink')}")
        else:
            print(f"Event already in calendar: {event.description} {possible.get('htmlLink')}")


def store(event):
    with transaction.atomic():
        home_team = event.match.homeTeam
        home_team_obj = Team.objects.get_or_create(ref=home_team.id, defaults={"popular_name": home_team.popularName})[
            0
        ]

        away_team = event.match.awayTeam
        away_team_obj = Team.objects.get_or_create(ref=away_team.id, defaults={"popular_name": away_team.popularName})[
            0
        ]

        championship = event.match.championship
        championship_obj = Championship.objects.get_or_create(name=championship.name)[0]

        location = event.match.location
        if location:
            location_obj = Location.objects.get_or_create(name=location.name, popular_name=location.popularName)[0]
        else:
            location_obj = None

        phase = event.match.phase
        phase_obj = Phase.objects.get_or_create(name=phase.name, phase_type=phase.type)[0]

        round = event.match.round
        round_obj = Round.objects.get_or_create(name=str(round))[0]

        start_date = event.match.startDate
        start_hour = event.match.startHour
        timezone = "America/Bahia"
        if start_hour:
            start_at = arrow.get(f"{start_date} {start_hour} {timezone}", "YYYY-MM-DD HH:mm:ss ZZZ").datetime
        else:
            start_at = arrow.get(f"{start_date} {timezone}", "YYYY-MM-DD ZZZ").datetime

        match = Match.objects.get_or_create(
            home_team=home_team_obj,
            away_team=away_team_obj,
            championship=championship_obj,
            location=location_obj,
            phase=phase_obj,
            round=round_obj,
            start_at=start_at,
        )[0]
        SoccerEvent.objects.get_or_create(match=match)


def fetch():
    from parse import parse

    events = parse()
    for event in events:
        store(event)


if __name__ == "__main__":
    fetch()
