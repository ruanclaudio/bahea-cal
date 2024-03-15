import os
import pathlib
import sys

import django

project_path = pathlib.Path(__file__).parent.parent
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

django.setup()

import arrow
import attrs

from django.db import transaction

from core.models import Team, Championship, Location, Phase, Round, Match, SoccerEvent


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

        description = f"{match.championship.name}: {match.home_team.popular_name} x {match.away_team.popular_name}"
        if match.location:
            description += f", {match.location.popular_name}"
        return cls(
            summary=f"[{match.championship.name}] {match.home_team.popular_name} x {match.away_team.popular_name}",
            description=description,
            start_datetime=arrow.get(match.start_at),
            start_timezone=timezone,
            end_datetime=arrow.get(match.start_at).shift(minutes=+120),
            end_timezone=timezone,
            location=match.location and match.location.popular_name or "",
        )

    def as_dict(self):
        return {
            "summary": self.summary,
            "location": self.location,
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
