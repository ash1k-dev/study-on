from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.courses.api.serializers import ListAvailableLessonsSerializer
from study_on.courses.models import AvailableLessons
from study_on.services.views import BaseModelViewSet


class AvailableLessonsViewSet(BaseModelViewSet):
    """Доступные для пользователя уроки"""

    queryset = AvailableLessons.objects.all()
    serializer_class = ListAvailableLessonsSerializer
    permission_classes = (IsAdminOrStuff,)
