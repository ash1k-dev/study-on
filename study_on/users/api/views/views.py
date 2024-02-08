import random
from os import getenv

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from study_on.services.permissions import IsAdminOrStuff
from study_on.users.api.serializers import (
    ChangePasswordUserSerializer,
    IdentificationCodeValidationError,
    ListUserSerializer,
    RegistrationUserSerializer,
    UserSerializer,
    VerificationUserSerializer,
    VerifyChangePasswordUserSerializer,
)
from study_on.users.tasks import send_email

User = get_user_model()

MAX_INCORRECT_ATTEMPTS = getenv("MAX_INCORRECT_ATTEMPTS", default=5)


class UserFilter(filters.FilterSet):
    """Фильтр для пользователя"""

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """Пользователь"""

    serializer_class = ListUserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAdminOrStuff,)
    filterset_class = UserFilter
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

    @action(detail=False, serializer_class=UserSerializer)
    def me(self, request):
        """Получить информацию о пользователе"""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="register-user",
        serializer_class=RegistrationUserSerializer,
    )
    def register_user(self, request, *args, **kwargs):
        """Регистрация пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random.randint(100000, 999999)
        user = User.objects.create_user(
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
            is_active=False,
            identification_code=code,
        )
        send_email.delay(user.username, user.email, user.identification_code, "confirm")
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["post"],
        url_path="verify-user",
        serializer_class=VerificationUserSerializer,
    )
    def verify_user(self, request, *args, **kwargs):
        """Верификация пользователя"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.validated_data["email"])
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        except IdentificationCodeValidationError as e:
            user = User.objects.get(email=serializer.initial_data["email"])
            user.identification_code_entry_attempts += 1
            user.save()
            if user.identification_code_entry_attempts == MAX_INCORRECT_ATTEMPTS:
                send_email.delay(user.username, user.email, user.identification_code, "confirm_error")
                user.delete()
            return Response(data=e.args[0], status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_path="change-password",
        serializer_class=ChangePasswordUserSerializer,
    )
    def change_password(self, request, *args, **kwargs):
        """Смена пароля"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random.randint(100000, 999999)
        user = User.objects.get(email=serializer.validated_data["email"])
        user.identification_code = code
        user.save()
        send_email.delay(user.username, user.email, user.identification_code, "change_password")
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="verify-password",
        serializer_class=VerifyChangePasswordUserSerializer,
    )
    def verify_password(self, request, *args, **kwargs):
        """Потверждение смены пароля"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(status=status.HTTP_200_OK)
