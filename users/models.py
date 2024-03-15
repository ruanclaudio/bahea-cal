import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserCredential(models.Model):
    client_id = models.CharField(max_length=128, unique=True)
    credentials = models.JSONField(editable=False, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)

    def as_dict(self):
        return {**self.credentials, "client_id": self.client_id}


class UserEvent(models.Model):
    eid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    event = models.ForeignKey("core.SoccerEvent", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "event")


class UserSubscription(models.Model):
    team = models.ForeignKey("core.Team", on_delete=models.CASCADE, related_name="subscriptions")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("team", "user")


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    events = models.ManyToManyField("core.SoccerEvent", through=UserEvent, blank=True)
    subscriptions = models.ManyToManyField("core.Team", through=UserSubscription, blank=True)


user = User
