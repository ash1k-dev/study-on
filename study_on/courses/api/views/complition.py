from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import CompletionSerializer
from study_on.courses.models import Completion


class CompletionFilter(filters.FilterSet):
    """Фильтр для отметки о завершении курса"""

    class Meta:
        model = Completion
        fields = ("course", "student")


class CompletionViewSet(viewsets.ModelViewSet):
    """Отметки о завершении курса"""

    queryset = Completion.objects.all()
    serializer_class = CompletionSerializer
    filter_class = CompletionFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "course__title",
        "student__username",
    ]
    permission_classes = [
        IsAdminOrStuff,
    ]
