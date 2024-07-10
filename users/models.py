# Python imports
import uuid

# Pip imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel


class UserCredential(TimeStampedModel):
    client_id = models.CharField(max_length=128)
    credentials = models.JSONField(editable=False, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)

    def as_dict(self):
        if not self.credentials:
            return {"token": "", "refresh_token": "", "token_uri": "", "client_id": "", "client_secret": ""}
        return {**self.credentials, "client_id": self.client_id}


class UserEvent(TimeStampedModel):
    eid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    event = models.ForeignKey("core.SoccerEvent", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "event")
        ordering = ("event__match__start_at",)


class UserSubscription(TimeStampedModel):
    team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="subscriptions")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("team", "user")


class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    events = models.ManyToManyField("core.SoccerEvent", through=UserEvent, blank=True)
    subscriptions = models.ManyToManyField("core.Team", through=UserSubscription, blank=True)
    calendar_id = models.CharField(max_length=128, blank=True, null=True)


user = User
