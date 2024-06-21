import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import BookmarkSerializer
from study_on.courses.models import Bookmark, Course, Survey
from study_on.users.models import User


@pytest.mark.django_db
def test_bookmark_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка закладок"""
    baker.make(Bookmark, _quantity=5)
    url = reverse("api:bookmark-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_bookmark_create(admin_api_client, unauthorized_api_client):
    """Проверка создания закладки"""
    url = reverse("api:bookmark-list")
    course = baker.make(Course)
    user = baker.make(User)
    data = {"course": course.id, "student": user.id}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Bookmark.objects.count() == 1
    assert Bookmark.objects.first().course_id == data["course"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_bookmark_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретной закладки"""
    bookmark = baker.make(Bookmark)
    url = reverse("api:bookmark-detail", args=[bookmark.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == BookmarkSerializer(bookmark).data
    non_existent_url = reverse("api:survey-detail", args=[bookmark.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_bookmark_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения опроса"""
    bookmark = baker.make(Bookmark)
    url = reverse("api:bookmark-detail", args=[bookmark.id])
    course = baker.make(Course)
    data = {"course": course.id}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["course"] == data["course"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_bookmark_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления опроса"""
    bookmark = baker.make(Bookmark)
    url = reverse("api:bookmark-detail", args=[bookmark.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Bookmark.objects.count() == 0
    non_existent_url = reverse("api:bookmark-detail", args=[bookmark.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    survey = baker.make(Survey)
    url = reverse("api:bookmark-detail", args=[survey.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
