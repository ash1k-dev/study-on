from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers.review import ReviewSerializer
from study_on.courses.models import Review
from study_on.services.views import BaseModelViewSet


class ReviewFilter(filters.FilterSet):
    """Фильтр для отзывов на курс"""

    class Meta:
        model = Review
        fields = ("course",)


class ReviewViewSet(BaseModelViewSet):
    """Отзывы на курс"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_class = ReviewFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "course__title",
        "student__username",
    ]
    permission_classes = [
        IsAdminOrStuff,
    ]

    @action(
        detail=False,
        methods=["get"],
        url_path="get-course-review-count",
    )
    def get_course_review_count(self, request, *args, **kwargs):
        """Получение количества отзывов для каждого курса"""
        course_review_count = self.get_queryset().values("course").annotate(count=Count("id")).order_by("course")
        return Response({"course_review_count": course_review_count})
