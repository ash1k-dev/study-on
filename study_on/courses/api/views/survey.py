from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import SurveySerializer
from study_on.courses.models import Survey
from study_on.services.views import BaseModelViewSet


class SurveyFilter(filters.FilterSet):
    """Фильтр тестов урока"""

    class Meta:
        model = Survey
        fields = ("lesson",)


class SurveyViewSet(BaseModelViewSet):
    """Тест урока"""

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrStuff,)
    filterset_class = SurveyFilter
    filter_backends = [SearchFilter]
    search_fields = ["title", "description", "lesson__title", "lesson__course__title"]

    def create(self, request, *args, **kwargs):
        """Создание теста"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
