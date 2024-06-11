from rest_framework import serializers

from study_on.users.models import Reward


class RewardSerializer(serializers.ModelSerializer):
    """Награда"""

    class Meta:
        model = Reward
        fields = "__all__"
