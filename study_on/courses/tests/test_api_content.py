import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import ContentSerializer
from study_on.courses.models import Content, Lesson, Survey


@pytest.mark.django_db
def test_content_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка контента"""
    baker.make(Content, _quantity=5)
    url = reverse("api:content-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_content_create(admin_api_client, unauthorized_api_client):
    """Проверка создания контента"""
    url = reverse("api:content-list")
    lesson = baker.make(Lesson)
    data = {"lesson": lesson.id, "text": "test", "order": 1, "is_published": True}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Content.objects.count() == 1
    assert Content.objects.first().lesson_id == data["lesson"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_content_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного контента"""
    content = baker.make(Content)
    url = reverse("api:content-detail", args=[content.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == ContentSerializer(content).data
    non_existent_url = reverse("api:survey-detail", args=[content.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_content_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения контента"""
    content = baker.make(Content)
    url = reverse("api:content-detail", args=[content.id])
    data = {"lesson": baker.make(Lesson).id}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["lesson"] == data["lesson"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_content_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления контента"""
    content = baker.make(Content)
    url = reverse("api:content-detail", args=[content.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Survey.objects.count() == 0
    non_existent_url = reverse("api:survey-detail", args=[content.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    content = baker.make(Content)
    url = reverse("api:content-detail", args=[content.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
