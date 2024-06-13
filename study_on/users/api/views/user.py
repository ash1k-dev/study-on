import random
from datetime import datetime
from os import getenv

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from study_on.courses.api.serializers import AvailableLessonsSerializer, QuestionAnswerSerializer
from study_on.courses.models import AvailableLessons, Lesson, Question
from study_on.services.work_with_docx import create_file, upload_file
from study_on.users.api.serializers import (
    ChangePasswordUserSerializer,
    IdentificationCodeValidationError,
    ListUserSerializer,
    RegistrationUserSerializer,
    RewardSerializer,
    UserSerializer,
    VerificationUserSerializer,
    VerifyChangePasswordUserSerializer,
)
from study_on.users.models import Reward
from study_on.users.tasks import send_email

User = get_user_model()

MAX_INCORRECT_ATTEMPTS = getenv("MAX_INCORRECT_ATTEMPTS", default=5)
TEMPLATE_PATH = getenv("PLAN_TEMPLATE_PATH", default="study_on/users/api/templates/plan.docx")
FILE_PATH = getenv("PLAN_FILE_PATH", default="study_on/users/api/templates")


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
    filterset_class = UserFilter
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]
    # permission_classes = [IsAdminOrStuff]

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
        permission_classes=[AllowAny],
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

    @action(
        detail=True,
        methods=["get"],
        url_path="get-plan",
        queryset=AvailableLessons.objects.all(),
        serializer_class=AvailableLessonsSerializer,
    )
    def get_courses_plan(self, request, *args, **kwargs):
        """Получение сводного файла по курсам"""
        available_lessons = AvailableLessons.objects.filter(student=request.user)
        if not available_lessons:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course_progress = []
        for available_lesson in available_lessons:
            course = available_lesson.course
            lessons_before = Lesson.objects.filter(
                course=course, order__lte=available_lesson.max_available_lesson
            ).count()
            lessons_after = Lesson.objects.filter(
                course=course, order__gt=available_lesson.max_available_lesson
            ).count()
            if lessons_before == 0:
                course_progress.append({"course": course, "progress": 0})
            else:
                progress = lessons_before / (lessons_before + lessons_after) * 100
                course_progress.append(
                    f"Курс {course.title}: прогресс {round(progress, 2)}%"
                    f" (пройдено {lessons_before} из {lessons_before + lessons_after} уроков)"
                )
        context = {"data": course_progress, "user": request.user, "date": datetime.now().strftime("%Y-%m-%d")}
        template_path = TEMPLATE_PATH
        file_path = f"{FILE_PATH}/{request.user.username}"
        create_file(context, template_path, file_path)
        return upload_file(file_path, request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-answers-without-check",
        queryset=Question.objects.all(),
        serializer_class=QuestionAnswerSerializer,
    )
    def get_answers_without_check(self, request, *args, **kwargs):
        """Получение списка ответов без проверки (для преподавателя)"""
        questions = (
            self.filter_queryset(self.get_queryset())
            .select_related("survey", "survey__lesson", "survey__lesson__course")
            .filter(answer_check=False, survey__lesson__course__teachers=request.user)
        )
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="get-rewards",
        serializer_class=RewardSerializer,
    )
    def get_rewards(self, request, *args, **kwargs):
        """Получение списка наград пользователя"""
        rewards = Reward.objects.filter(users=request.user)
        serializer = self.get_serializer(rewards, many=True)
        return Response(serializer.data)
