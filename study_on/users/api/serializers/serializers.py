from django.contrib.auth import get_user_model
from rest_framework import serializers

from study_on.users.models import User as UserType

User = get_user_model()


class IdentificationCodeValidationError(serializers.ValidationError):
    pass


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


class RegistrationUserSerializer(serializers.ModelSerializer[UserType]):
    """Верификация пользователя"""

    def is_valid(self, raise_exception=False):
        self._check_email_exists()
        return super().is_valid(raise_exception=raise_exception)

    def _check_email_exists(self):
        """Проверка существования пользователя с таким же email"""
        if User.objects.filter(email=self.initial_data["email"]).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует"})

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "first_name",
            "last_name",
            "email",
            "password",
        ]


class VerificationUserSerializer(serializers.ModelSerializer[UserType]):
    """Верификация пользователя"""

    def is_valid(self, raise_exception=False):
        self._check_email_exists()
        self._check_identification_code_correct()
        return super().is_valid(raise_exception=raise_exception)

    def _check_email_exists(self):
        """Проверка существования пользователя с таким же email"""
        if not User.objects.filter(email=self.initial_data["email"]).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email не существует"})

    def _check_identification_code_correct(self):
        """Проверка идентификационного кода пользователя"""
        user = User.objects.get(email=self.initial_data["email"])
        if user.identification_code != int(self.initial_data["identification_code"]):
            raise IdentificationCodeValidationError(
                {"identification_code": "Неверный код для подтверждения пользователя"}
            )

    class Meta:
        model = User
        fields = [
            "email",
            "identification_code",
        ]


class ChangePasswordUserSerializer(serializers.ModelSerializer[UserType]):
    """Верификация пользователя"""

    def is_valid(self, raise_exception=False):
        self._check_email_exists()
        return super().is_valid(raise_exception=raise_exception)

    def _check_email_exists(self):
        """Проверка существования пользователя с таким же email"""
        if not User.objects.filter(email=self.initial_data["email"]).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email не существует"})

    class Meta:
        model = User
        fields = [
            "email",
        ]


class VerifyChangePasswordUserSerializer(serializers.ModelSerializer[UserType]):
    """Верификация пользователя"""

    def is_valid(self, raise_exception=False):
        self._check_email_exists()
        self._check_identification_code_correct()
        return super().is_valid(raise_exception=raise_exception)

    def _check_email_exists(self):
        """Проверка существования пользователя с таким же email"""
        if not User.objects.filter(email=self.initial_data["email"]).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email не существует"})

    def _check_identification_code_correct(self):
        """Проверка идентификационного кода для пароля"""
        user = User.objects.get(email=self.initial_data["email"])
        if user.identification_code != int(self.initial_data["identification_code"]):
            raise IdentificationCodeValidationError({"identification_code": "Неверный код для подтверждения пароля"})

    class Meta:
        model = User
        fields = [
            "email",
            "identification_code",
            "password",
        ]
