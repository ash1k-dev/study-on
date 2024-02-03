from typing import Any

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import ListLessonSerializer
from study_on.courses.models import Lesson
from study_on.services.views import BaseModelViewSet


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ("course",)


class LessonViewSet(BaseModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = ListLessonSerializer
    filterset_class = LessonFilter
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
