from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from study_on.courses.api.permissions import IsAdminOrStuff
from study_on.services.views import BaseModelViewSet
from study_on.users.api.serializers import RewardSerializer
from study_on.users.models import Reward


class RewardFilter(filters.FilterSet):
    """Фильтр для курсов"""

    class Meta:
        model = Reward
        fields = ("title", "reward_type", "reward_value")


class RewardViewSet(BaseModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAdminOrStuff]
    filterset_class = RewardFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "reward_type",
        "reward_value",
    ]
