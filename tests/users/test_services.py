# Pip imports
import pytest

# Internal imports
from users.models import User, UserCredential
from users.services import CredentialsService


@pytest.mark.django_db
class TestCredentialsService:

    def test_get_for_existing(self):
        user = User.objects.create(username="test")
        UserCredential.objects.create(user=user)
        service = CredentialsService()

        credential = service.get_for(user)
        assert isinstance(credential, UserCredential)
        assert credential.user == user

    def test_get_for_non_existing(self):
        user = User()
        service = CredentialsService()

        credential = service.get_for(user)
        assert credential is None
