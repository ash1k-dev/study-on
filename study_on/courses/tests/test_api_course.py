import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import CourseSerializer
from study_on.courses.models import Course, Subject
from study_on.users.models import User


@pytest.mark.django_db
def test_course_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка курсов"""
    baker.make(Course, _quantity=5)
    url = reverse("api:course-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_course_create(admin_api_client, unauthorized_api_client):
    """Проверка создания курса"""
    url = reverse("api:course-list")
    user = baker.make(User)
    subject = baker.make(Subject)
    data = {
        "author": user.id,
        "subject": subject.id,
        "title": "test",
        "description": "test",
        "slug": "test",
        "is_published": True,
    }
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.first().title == data["title"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_course_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения курса"""
    course = baker.make(Course)
    url = reverse("api:course-detail", args=[course.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == CourseSerializer(course).data
    non_existent_url = reverse("api:course-detail", args=[course.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    url = reverse("api:course-detail", args=[course.id])
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_course_update(admin_api_client, unauthorized_api_client):
    """Проверка обновления курса"""
    course = baker.make(Course)
    url = reverse("api:course-detail", args=[course.id])
    data = {"title": "test"}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_course_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления курса"""
    course = baker.make(Course)
    url = reverse("api:course-detail", args=[course.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == 0
    non_existent_url = reverse("api:course-detail", args=[course.id])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    assert Course.objects.count() == 0
    # проверка для неавторизованных пользователей
    course = baker.make(Course)
    url = reverse("api:course-detail", args=[course.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
