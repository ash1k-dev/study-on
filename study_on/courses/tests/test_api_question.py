import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import QuestionSerializer
from study_on.courses.models import Question, Survey


@pytest.mark.django_db
def test_question_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка вопросов"""
    baker.make(Question, _quantity=5)
    url = reverse("api:question-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_question_create(admin_api_client, unauthorized_api_client):
    """Проверка создания вопроса"""
    url = reverse("api:question-list")
    survey = baker.make(Survey)
    data = {"survey": survey.id, "title": "Test question", "text": "Test text", "order": 1, "is_published": True}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Question.objects.count() == 1
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_question_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного вопроса"""
    question = baker.make(Question)
    url = reverse("api:question-detail", args=[question.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == QuestionSerializer(question).data
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_question_update(admin_api_client, unauthorized_api_client):
    """Проверка обновления вопроса"""
    question = baker.make(Question)
    url = reverse("api:question-detail", args=[question.id])
    data = {
        "is_published": False,
    }
    # проверка для администраторов
    response = admin_api_client.get(url, data)
    assert response.status_code == 200
    assert Question.objects.count() == 1
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.put(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_question_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления вопроса"""
    question = baker.make(Question)
    url = reverse("api:question-detail", args=[question.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Question.objects.count() == 0
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
