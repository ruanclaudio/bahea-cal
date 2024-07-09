# Python imports
import uuid

# Pip imports
import arrow
from django.db import models
from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.IntegerField(unique=True)
    popular_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"<Team: {self.popular_name}>"


class Championship(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"<Championship: {self.name}>"


class Location(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    popular_name = models.CharField(max_length=64)

    def __str__(self):
        return f"<MatchLocation: {self.popular_name}>"


class Phase(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    phase_type = models.CharField(max_length=64)


class Round(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)


class Match(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    championship = models.ForeignKey("core.Championship", on_delete=models.SET_NULL, null=True)
    home_team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="away_matches")
    location = models.ForeignKey("core.Location", on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey("core.Phase", on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey("core.Round", on_delete=models.SET_NULL, null=True)
    start_at = models.DateTimeField()

    class Meta:
        unique_together = ("championship", "home_team", "away_team", "start_at")
        ordering = ("start_at",)

    def __str__(self):
        if self.championship:
            start_at = arrow.get(self.start_at).to("America/Bahia").strftime("%d/%m/%Y %H:%M")
            return f"{self.championship}: {self.home_team} x {self.away_team} {start_at}"


class SoccerEvent(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey("core.Match", on_delete=models.CASCADE, related_name="event")

    class Meta:
        ordering = ("match__start_at",)

    def __str__(self):
        return f"{self.match}"
