import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import ReviewSerializer
from study_on.courses.models import Course, Review
from study_on.users.admin import User


@pytest.mark.django_db
def test_review_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка отзывов"""
    baker.make(Review, _quantity=5)
    url = reverse("api:review-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_review_create(admin_api_client, unauthorized_api_client):
    """Проверка создания отзыва"""
    url = reverse("api:review-list")
    course = baker.make(Course)
    user = baker.make(User)
    data = {"course": course.id, "student": user.id, "text": "test", "grade": 1}
    # проверка для администраторов
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Review.objects.count() == 1
    assert Review.objects.first().course_id == data["course"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_review_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретного отзыва"""
    review = baker.make(Review)
    url = reverse("api:review-detail", args=[review.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == ReviewSerializer(review).data
    non_existent_url = reverse("api:review-detail", args=[review.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_review_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения отзыва"""
    review = baker.make(Review)
    course = baker.make(Course)
    url = reverse("api:review-detail", args=[review.id])
    data = {"course": course.id}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["course"] == data["course"]
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_review_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления отзыва"""
    review = baker.make(Review)
    url = reverse("api:review-detail", args=[review.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Review.objects.count() == 0
    non_existent_url = reverse("api:review-detail", args=[review.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    review = baker.make(Review)
    url = reverse("api:review-detail", args=[review.id])
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
