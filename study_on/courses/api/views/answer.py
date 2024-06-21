from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import AnswerSerializer
from study_on.courses.models import Answer
from study_on.services.views import BaseModelViewSet


class AnswerFilter(filters.FilterSet):
    """Фильтр для закладок"""

    class Meta:
        model = Answer
        fields = ("survey_student", "question", "is_correct")


class AnswerViewSet(BaseModelViewSet):
    """Ответы на вопросы"""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_class = AnswerFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "survey_student__student__username",
        "survey__title",
    ]
    permission_classes = [
        IsAdminOrStuff,
    ]
