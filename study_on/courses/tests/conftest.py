import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def admin_api_client():
    admin = baker.make("users.User", is_staff=True, is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def unauthorized_api_client():
    return APIClient()


@pytest.fixture
def authorized_api_client():
    user = baker.make("users.User")
    client = APIClient()
    client.force_authenticate(user=user)
    return client
