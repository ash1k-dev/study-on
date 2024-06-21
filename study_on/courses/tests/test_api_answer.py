import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import AnswerSerializer
from study_on.courses.models import Answer, Question, SurveyStudent


@pytest.mark.django_db
def test_answer_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка ответов"""
    baker.make(Answer, _quantity=5)
    url = reverse("api:answer-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_answer_create(admin_api_client, unauthorized_api_client):
    """Проверка создания ответа"""
    url = reverse("api:answer-list")
    survey_student = baker.make(SurveyStudent)
    question = baker.make(Question)
    data = {"survey_student": survey_student.id, "question": question.id, "text": "text", "is_correct": True}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Answer.objects.count() == 1
    assert Answer.objects.first().question_id == data["question"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_answer_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного ответа"""
    answer = baker.make(Answer)
    url = reverse("api:answer-detail", args=[answer.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == AnswerSerializer(answer).data
    non_existent_url = reverse("api:answer-detail", args=[answer.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_answer_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения ответа"""
    answer = baker.make(Answer)
    url = reverse("api:answer-detail", args=[answer.id])
    data = {"text": "text", "is_correct": True}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert Answer.objects.first().text == data["text"]
    assert Answer.objects.first().is_correct == data["is_correct"]
    non_existent_url = reverse("api:answer-detail", args=[answer.id + 1])
    response = admin_api_client.patch(non_existent_url, data)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_answer_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления ответа"""
    answer = baker.make(Answer)
    url = reverse("api:answer-detail", args=[answer.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Answer.objects.count() == 0
    non_existent_url = reverse("api:answer-detail", args=[answer.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
