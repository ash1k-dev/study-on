import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import SubjectSerializer
from study_on.courses.models import Heading, Subject


@pytest.mark.django_db
def test_subject_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка предметов"""
    baker.make(Subject, _quantity=5)
    url = reverse("api:subject-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_subject_create(admin_api_client, unauthorized_api_client):
    """Проверка создания предмета"""
    url = reverse("api:subject-list")
    heading = baker.make(Heading)
    data = {"title": "test", "description": "test", "slug": "test", "is_published": True, "heading": heading.id}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Subject.objects.count() == 1
    assert Subject.objects.first().title == data["title"]
    assert Subject.objects.first().description == data["description"]
    assert Subject.objects.first().is_published == data["is_published"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_subject_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного предмета"""
    subject = baker.make(Subject)
    url = reverse("api:subject-detail", args=[subject.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == SubjectSerializer(subject).data
    non_existent_url = reverse("api:subject-detail", args=[subject.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_subject_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения предмета"""
    subject = baker.make(Subject)
    url = reverse("api:subject-detail", args=[subject.id])
    data = {"title": "test", "description": "test", "slug": "test", "is_published": True}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
    assert response.data["description"] == data["description"]
    assert response.data["is_published"] == data["is_published"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_subject_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления предмета"""
    subject = baker.make(Subject)
    url = reverse("api:subject-detail", args=[subject.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Subject.objects.count() == 0
    non_existent_url = reverse("api:subject-detail", args=[subject.id])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    assert Subject.objects.count() == 0
    # проверка для неавторизованных пользователей
    subject = baker.make(Subject)
    url = reverse("api:subject-detail", args=[subject.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
