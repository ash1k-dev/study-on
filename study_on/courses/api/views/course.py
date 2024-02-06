from typing import Any

from django.db.models import Count, F
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse
from study_on.courses.api.serializers import (
    CourseInfoSerializer,
    CourseParticipantsAmountSerializer,
    CourseWithContentsSerializer,
    CurrentCourseInfoSerializer,
    ListCourseSerializer,
)
from study_on.courses.models import AvailableLessons, Course
from study_on.services.views import BaseModelViewSet


class CourseFilter(filters.FilterSet):
    """Фильтр для курсов"""

    class Meta:
        model = Course
        fields = ("subject", "teachers", "students", "slug")


class CourseViewSet(BaseModelViewSet):
    """Курс"""

    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer
    filterset_class = CourseFilter
    filter_backends = [SearchFilter]
    search_fields = ["slug", "title", "description", "subject__title", "teachers__username", "students__username"]

    @action(
        detail=True,
        methods=["post"],
        url_path="register-user-on-course",
        permission_classes=[IsAuthenticated],
    )
    def register_user_on_course(self, request, *args, **kwargs):
        """Регистрация пользователя на курс"""
        course = self.get_object()
        if course.students.filter(id=request.user.id).exists():
            return Response({"registration": False})
        else:
            AvailableLessons.objects.create(course=course, student=request.user)
            course.students.add(request.user)
            return Response({"registration": True})

    @action(
        detail=True,
        methods=["get"],
        url_path="get-contents",
        serializer_class=CourseWithContentsSerializer,
        permission_classes=[IsStudentOnCourse],
    )
    def get_contents(self, request, *args, **kwargs):
        """Получение содержимого курса"""
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-participants",
        serializer_class=CourseParticipantsAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_participants(self, request, *args, **kwargs):
        """Получение количества участников курса"""
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(
            teachers_count=Count(F("teachers"), distinct=True),
            students_count=Count(F("students"), distinct=True),
            lessons_count=Count(F("lessons"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        """Создание курса"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-courses-info",
        serializer_class=CourseInfoSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_courses_info(self, request, *args, **kwargs):
        """Получение информации о курсах(автор, название, кол-во участников)"""
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(
            students_count=Count(F("students"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="get-current-course-info",
        serializer_class=CurrentCourseInfoSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_current_course_info(self, request, *args, **kwargs):
        """Получение информации о курсe(название, описание, преподаватели, уроки, кол-во тестов)"""
        uinited_results = (
            self.filter_queryset(self.get_queryset())
            .prefetch_related("teachers")
            .prefetch_related(
                "lessons",
                "lessons__tests",
            )
            .annotate(tests_count=Count("lessons__tests"))
        )
        serializer = self.get_serializer(uinited_results, many=True)
        return Response(serializer.data)
