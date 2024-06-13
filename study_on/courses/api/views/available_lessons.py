from rest_framework.response import Response

from study_on.courses.api.serializers import AvailableLessonsSerializer
from study_on.courses.models import AvailableLessons
from study_on.services.views import BaseModelViewSet


class AvailableLessonsViewSet(BaseModelViewSet):
    """Доступные для пользователя уроки"""

    queryset = AvailableLessons.objects.all()
    serializer_class = AvailableLessonsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(student=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
