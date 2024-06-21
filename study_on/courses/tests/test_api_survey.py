import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import SurveySerializer
from study_on.courses.models import Lesson, Survey


@pytest.mark.django_db
def test_survey_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка опросов"""
    baker.make(Survey, _quantity=5)
    url = reverse("api:survey-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_survey_create(admin_api_client, unauthorized_api_client):
    """Проверка создания опроса"""
    url = reverse("api:survey-list")
    data = {"lesson": baker.make(Lesson).id, "title": "test", "description": "test", "is_published": True}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Survey.objects.count() == 1
    assert Survey.objects.first().lesson_id == data["lesson"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_survey_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного опроса"""
    survey = baker.make(Survey)
    url = reverse("api:survey-detail", args=[survey.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == SurveySerializer(survey).data
    non_existent_url = reverse("api:survey-detail", args=[survey.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_survey_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения опроса"""
    survey = baker.make(Survey)
    url = reverse("api:survey-detail", args=[survey.id])
    data = {"lesson": baker.make(Lesson).id}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["lesson"] == data["lesson"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_survey_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления опроса"""
    survey = baker.make(Survey)
    url = reverse("api:survey-detail", args=[survey.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Survey.objects.count() == 0
    non_existent_url = reverse("api:survey-detail", args=[survey.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    survey = baker.make(Survey)
    url = reverse("api:survey-detail", args=[survey.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
