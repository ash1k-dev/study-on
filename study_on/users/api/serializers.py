from django.contrib.auth import get_user_model
from rest_framework import serializers

from study_on.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    """Пользователь"""

    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class ListUserSerializer(serializers.ModelSerializer[UserType]):
    """Пользователь"""

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "first_name",
            "last_name",
            "url",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
