from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.blog.api.serializers import PostSerializer
from study_on.blog.models import Post
from study_on.services.views import BaseModelViewSet


class PostFilter(filters.FilterSet):
    """Фильтр для постов"""

    class Meta:
        model = Post
        fields = (
            "title",
            "author",
            "is_published",
        )


class PostViewSet(BaseModelViewSet):
    """Пост"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "author__username",
    ]

    def create(self, request, *args, **kwargs):
        """Создание поста"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """Изменение поста"""
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        """Список постов"""
        queryset = self.filter_queryset(self.get_queryset()).filter(is_published=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
