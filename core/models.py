import uuid

from django.db import models


class Team(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.IntegerField(unique=True)
    popular_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"<Team: {self.popular_name}>"


class Championship(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"<Championship: {self.name}>"


class Location(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    popular_name = models.CharField(max_length=64)

    def __str__(self):
        return f"<MatchLocation: {self.popular_name}>"


class Phase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    phase_type = models.CharField(max_length=64)


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    championship = models.ForeignKey("core.Championship", on_delete=models.SET_NULL, null=True)
    home_team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="away_matches")
    location = models.ForeignKey("core.Location", on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey("core.Phase", on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey("core.Round", on_delete=models.SET_NULL, null=True)
    start_at = models.DateTimeField()


class SoccerEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey("core.Match", on_delete=models.CASCADE, related_name="event")
