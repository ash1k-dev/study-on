from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import ListTestSerializer
from study_on.courses.models import Test
from study_on.services.views import BaseModelViewSet


class TestFilter(filters.FilterSet):
    """Фильтр тестов урока"""

    class Meta:
        model = Test
        fields = ("lesson",)


class TestViewSet(BaseModelViewSet):
    """Тест урока"""

    queryset = Test.objects.all()
    serializer_class = ListTestSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
    filterset_class = TestFilter
    filter_backends = [SearchFilter]
    search_fields = ["title", "description", "lesson__title", "lesson__course__title"]

    def create(self, request, *args, **kwargs):
        """Создание теста"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
