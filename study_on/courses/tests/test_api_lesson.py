import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import LessonSerializer
from study_on.courses.models import Course, Lesson


@pytest.mark.django_db
def test_lesson_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка уроков"""
    baker.make(Lesson, _quantity=5)
    url = reverse("api:lesson-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_lesson_create(admin_api_client, unauthorized_api_client):
    """Проверка создания урока"""
    url = reverse("api:lesson-list")
    course = baker.make(Course)
    data = {
        "course": course.id,
        "title": "test",
        "description": "test",
        "order": 1,
        "is_published": True,
    }
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Lesson.objects.count() == 1
    assert Lesson.objects.first().title == data["title"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_lesson_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения урока"""
    lesson = baker.make(Lesson)
    url = reverse("api:lesson-detail", args=[lesson.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == LessonSerializer(lesson).data
    non_existent_url = reverse("api:lesson-detail", args=[lesson.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    url = reverse("api:lesson-detail", args=[lesson.id])
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_lesson_update(admin_api_client, unauthorized_api_client):
    """Проверка обновления урока"""
    lesson = baker.make(Lesson)
    url = reverse("api:lesson-detail", args=[lesson.id])
    data = {"title": "test"}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_lesson_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления урока"""
    lesson = baker.make(Lesson)
    url = reverse("api:lesson-detail", args=[lesson.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Lesson.objects.count() == 0
    non_existent_url = reverse("api:lesson-detail", args=[lesson.id])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    assert Lesson.objects.count() == 0
    # проверка для неавторизованных пользователей
    lesson = baker.make(Lesson)
    url = reverse("api:lesson-detail", args=[lesson.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
