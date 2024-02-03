from typing import Any

from django.db.models import Count, F
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import (
    CourseParticipantsAmountSerializer,
    CourseWithContentsSerializer,
    ListCourseSerializer,
)
from study_on.courses.models import AvailableLessons, Course
from study_on.services.views import BaseModelViewSet


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = ("subject", "teachers", "students", "slug")


class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer
    filterset_class = CourseFilter

    @action(
        detail=True,
        methods=["post"],
        url_path="register-user-on-course",
        permission_classes=[IsAuthenticated],
    )
    def register_user_on_course(self, request, *args, **kwargs):
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
        permission_classes=(IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff),
    )
    def get_contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-participants",
        serializer_class=CourseParticipantsAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_participants(self, request, *args, **kwargs):
        annotated_results = Course.objects.annotate(
            teachers_count=Count(F("teachers"), distinct=True),
            students_count=Count(F("students"), distinct=True),
            lessons_count=Count(F("lessons"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
