from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from study_on.courses.api.serializers import HeadingSerializer
from study_on.courses.models import Heading
from study_on.services.views import BaseModelViewSet


class HeadingFilter(filters.FilterSet):
    """Фильтр для направлений"""

    class Meta:
        model = Heading
        fields = ("title",)


class HeadingViewSet(BaseModelViewSet):
    """Направление"""

    queryset = Heading.objects.all()
    serializer_class = HeadingSerializer
    filterset_class = HeadingFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "description",
        "is_published",
    ]
