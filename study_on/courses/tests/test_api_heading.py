import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import HeadingSerializer
from study_on.courses.models import Heading


@pytest.mark.django_db
def test_heading_list_admin(admin_api_client):
    """Проверка получения списка направлений"""
    baker.make(Heading, _quantity=5)
    url = reverse("api:heading-list")
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_heading_list_unauthorized(unauthorized_api_client):
    """Проверка получения списка направлений неавторизованным пользователем"""
    baker.make(Heading, _quantity=5)
    url = reverse("api:heading-list")
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_heading_create_admin(admin_api_client):
    """Проверка создания направления"""
    url = reverse("api:heading-list")
    data = {"title": "test", "description": "test", "is_published": True}
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Heading.objects.count() == 1
    assert Heading.objects.first().title == data["title"]
    assert Heading.objects.first().description == data["description"]
    assert Heading.objects.first().is_published == data["is_published"]


@pytest.mark.django_db
def test_heading_create_unauthorized(unauthorized_api_client):
    """Проверка создания направления неавторизованным пользователем"""
    url = reverse("api:heading-list")
    data = {"title": "test", "description": "test", "is_published": True}
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_heading_detail_admin(admin_api_client):
    """Проверка получения конкретного направления"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == HeadingSerializer(heading).data
    url = reverse("api:heading-detail", args=[heading.id + 1])
    response = admin_api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_heading_detail_unauthorized(unauthorized_api_client):
    """Проверка получения конкретного направления неавторизованным пользователем"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_heading_update_admin(admin_api_client):
    """Проверка изменения направления"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    data = {"title": "test", "description": "test", "is_published": True}
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
    assert response.data["description"] == data["description"]
    assert response.data["is_published"] == data["is_published"]


@pytest.mark.django_db
def test_heading_update_unauthorized(unauthorized_api_client):
    """Проверка изменения направления неавторизованным пользователем"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    data = {"title": "test", "description": "test", "is_published": True}
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_heading_delete_admin(admin_api_client):
    """Проверка удаления направления"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Heading.objects.count() == 0
    url = reverse("api:heading-detail", args=[heading.id])
    response = admin_api_client.delete(url)
    assert response.status_code == 404
    assert Heading.objects.count() == 0


@pytest.mark.django_db
def test_heading_delete_unauthorized(unauthorized_api_client):
    """Проверка удаления направления неавторизованным пользователем"""
    heading = baker.make(Heading)
    url = reverse("api:heading-detail", args=[heading.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
