import json

import arrow
from google.oauth2.credentials import Credentials as GoogleCredentials

from users.models import UserCredential


class Credentials(GoogleCredentials):
    def as_dict(self, strip):
        return json.loads(self.to_json(strip))

    @classmethod
    def from_flow(cls, flow_credentials):
        obj = cls(**json.loads(flow_credentials.to_json()))
        if isinstance(obj.expiry, str):
            obj.expiry = arrow.get(obj.expiry).naive

        return obj

    @classmethod
    def from_user_credentials(cls, user_credentials):
        obj = cls(**user_credentials.as_dict())
        if isinstance(obj.expiry, str):
            obj.expiry = arrow.get(obj.expiry).naive

        return obj


class CredentialsService:
    @staticmethod
    def init_for(client_id, scopes):
        if not (user_credentials := CredentialsService.get_for(client_id)):
            return

        return Credentials.from_authorized_user_info(user_credentials.as_dict(), scopes=scopes)

    @staticmethod
    def get_for(client_id):
        try:
            return UserCredential.objects.get(client_id=client_id)
        except UserCredential.DoesNotExist:
            return

    @staticmethod
    def create_for(client_id, raw_credentials):
        new_credentials = raw_credentials.as_dict(strip=["client_id"])
        return UserCredential.objects.create(client_id=client_id, credentials=new_credentials)

    @staticmethod
    def update_for(client_id, raw_credentials):
        new_credentials = raw_credentials.as_dict(strip=["client_id"])
        credentials, _ = UserCredential.objects.update_or_create(
            client_id=client_id, defaults={"credentials": new_credentials}
        )

        return credentials
