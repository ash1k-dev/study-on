from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import ContentSerializer
from study_on.courses.models import Content
from study_on.services.views import BaseModelViewSet


class ContentFilter(filters.FilterSet):
    """Фильтр контента уроков"""

    class Meta:
        model = Content
        fields = ("lesson",)


class ContentViewSet(BaseModelViewSet):
    """Контент урока"""

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (IsAdminOrStuff,)
    filterset_class = ContentFilter
    filter_backends = [SearchFilter]
    search_fields = ["lesson__title", "lesson__course__title"]

    def create(self, request, *args, **kwargs):
        """Создание контента"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
