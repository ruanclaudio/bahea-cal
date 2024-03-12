from django.db import models


class UserCredentials(models.Model):
    client_id = models.CharField(max_length=128, unique=True)
    credentials = models.JSONField(editable=False, blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)

    def as_dict(self):
        return {**self.credentials, "client_id": self.client_id}
