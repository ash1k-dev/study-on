from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import LessonSerializer
from study_on.courses.models import Lesson
from study_on.services.views import BaseModelViewSet


class LessonFilter(filters.FilterSet):
    """Фильтр для уроков"""

    class Meta:
        model = Lesson
        fields = ("course",)


class LessonViewSet(BaseModelViewSet):
    """Урок"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminOrStuff,)
    filterset_class = LessonFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "course",
        "description",
    ]

    def create(self, request, *args, **kwargs):
        """Создание урока"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
