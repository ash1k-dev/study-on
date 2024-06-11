from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers.bookmark import BookmarkSerializer
from study_on.courses.models import Bookmark
from study_on.services.views import BaseModelViewSet


class BookmarkFilter(filters.FilterSet):
    """Фильтр для закладок"""

    class Meta:
        model = Bookmark
        fields = ("course", "student")


class BookmarkViewSet(BaseModelViewSet):
    """Работа с закладками"""

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    filter_class = BookmarkFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "course__title",
        "student__username",
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    @action(
        detail=False,
        methods=["get"],
        url_path="get-bookmark",
    )
    def get_bookmarks(self, request, *args, **kwargs):
        """Получение закладок сделанных конкретным студентом"""
        results = self.filter_queryset(self.get_queryset()).filter(student=request.user)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-course-bookmark-count",
        permission_classes=[IsAuthenticated, IsAdminOrStuff],
    )
    def get_course_bookmark_count(self, request, *args, **kwargs):
        """Получение количества закладок для каждого курса"""
        course_bookmark_count = self.get_queryset().values("course").annotate(count=Count("id")).order_by("course")
        return Response({"course_bookmark_count": course_bookmark_count})
