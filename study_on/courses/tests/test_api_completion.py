import pytest
from django.urls import reverse
from model_bakery import baker

from study_on.courses.api.serializers import CompletionSerializer
from study_on.courses.models import Completion, Course
from study_on.users.models import Reward, User


@pytest.mark.django_db
def test_completion_list(admin_api_client, unauthorized_api_client):
    """Проверка получения списка отметок о прохождении курсов"""
    baker.make(Reward, title="За прохождение первого курса")
    baker.make(Completion, _quantity=5)
    url = reverse("api:completion-list")
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_completion_create(admin_api_client, unauthorized_api_client):
    """Проверка создания новой отметки о прохождении курса"""
    baker.make(Reward, title="За прохождение первого курса")
    course = baker.make(Course)
    user = baker.make(User)
    url = reverse("api:completion-list")
    # проверка для администраторов
    data = {"course": course.id, "student": user.id}
    response = admin_api_client.post(url, data)
    assert response.status_code == 201
    assert Completion.objects.count() == 1
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_completion_detail(admin_api_client, unauthorized_api_client):
    """Проверка получения конкретной отметки о прохождении курса"""
    baker.make(Reward, title="За прохождение первого курса")
    completion = baker.make(Completion)
    url = reverse("api:completion-detail", args=[completion.id])
    # проверка для администраторов
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == CompletionSerializer(completion).data
    non_existent_url = reverse("api:completion-detail", args=[completion.id + 1])
    response = admin_api_client.get(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_completion_update(admin_api_client, unauthorized_api_client):
    """Проверка изменения отметки о прохождении курса"""
    baker.make(Reward, title="За прохождение первого курса")
    completion = baker.make(Completion)
    url = reverse("api:completion-detail", args=[completion.id])
    data = {"course": completion.course.id, "student": completion.student.id}
    # проверка для администраторов
    response = admin_api_client.patch(url, data)
    assert response.status_code == 200
    assert Completion.objects.first().course.id == data["course"]
    assert Completion.objects.first().student.id == data["student"]
    non_existent_url = reverse("api:completion-detail", args=[completion.id + 1])
    response = admin_api_client.patch(non_existent_url, data)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.patch(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_completion_delete(admin_api_client, unauthorized_api_client):
    """Проверка удаления отметки о прохождении курса"""
    baker.make(Reward, title="За прохождение первого курса")
    completion = baker.make(Completion)
    url = reverse("api:completion-detail", args=[completion.id])
    # проверка для администраторов
    response = admin_api_client.delete(url)
    assert response.status_code == 204
    assert Completion.objects.count() == 0
    non_existent_url = reverse("api:completion-detail", args=[completion.id + 1])
    response = admin_api_client.delete(non_existent_url)
    assert response.status_code == 404
    # проверка для неавторизованных пользователей
    response = unauthorized_api_client.delete(url)
    assert response.status_code == 403
