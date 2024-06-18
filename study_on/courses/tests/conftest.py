import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def admin_api_client():
    """Создание клиента для администратора"""
    admin = baker.make("users.User", is_staff=True, is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def unauthorized_api_client():
    """Создание клиента для неавторизованного пользователя"""
    return APIClient()


@pytest.fixture
def authorized_api_client():
    """Создание клиента для авторизованного пользователя"""
    user = baker.make("users.User")
    client = APIClient()
    client.force_authenticate(user=user)
    return client
