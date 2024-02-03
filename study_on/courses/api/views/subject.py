from typing import Any

from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import (
    ListSubjectSerializer,
    SubjectAmountSerializer,
    SubjectWithCourseSerializer,
)
from study_on.courses.models import Subject
from study_on.services.views import BaseModelViewSet


class SubjectFilter(filters.FilterSet):
    class Meta:
        model = Subject
        fields = ("slug",)


class SubjectViewSet(BaseModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = ListSubjectSerializer
    filterset_class = SubjectFilter

    @action(
        detail=False,
        methods=["get"],
        url_path="subjects-with-courses",
        serializer_class=SubjectWithCourseSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def subjects_with_courses(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(courses__isnull=False).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="courses-amount",
        serializer_class=SubjectAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    @method_decorator(cache_page(60 * 15))
    def courses_amount(self, request, *args, **kwargs):
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(course_count=Count("courses"))
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
