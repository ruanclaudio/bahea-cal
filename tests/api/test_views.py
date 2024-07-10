# Python imports
import random
from unittest.mock import patch

# Pip imports
import pytest
from rest_framework.test import APIClient

# Internal imports
from users.models import User, UserCredential


@pytest.fixture
def user():
    yield User.objects.create(username=f"test{random.randint(1, 100)}")


@pytest.fixture
def user_with_credential(user):
    UserCredential.objects.create(user=user)
    yield user


@pytest.fixture
def client():
    yield APIClient()


@pytest.fixture
def authenticated_client(client, user):
    client.force_authenticate(user=user)
    yield client
    client.force_authenticate(user=None)


@pytest.mark.django_db
class TestUserInfoView:

    def test_get_user_info_missing_credential(self, user):
        assert False

    @patch("api.views.UserService.from_credentials")
    def test_get_user_info(self, m_from_crentials, authenticated_client, user_with_credential):
        user = user_with_credential

        m_from_crentials.return_value.remote.return_value = expected_response = {
            "id": "1234567890",
            "email": user.email,
            "verified_email": True,
            "name": user.first_name,
            "given_name": user.first_name,
            "family_name": user.last_name,
            "picture": "https://example.com/picture.jpg",
        }

        response = authenticated_client.get("/api/v1/user/info/")
        assert response.status_code == 200
        assert response.json() == expected_response
        m_from_crentials.return_value.check_calendar.assert_called_once_with(user)
        m_from_crentials.return_value.remote.assert_called_once_with()

    def test_get_user_info_unauthenticated(self, client):
        response = client.get("/api/v1/user/info/")
        assert response.status_code == 403
        assert response.json() == {"error": "User not authenticated"}
