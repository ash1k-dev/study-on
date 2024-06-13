from rest_framework import serializers

from study_on.courses.models import AvailableLessons


class AvailableLessonsSerializer(serializers.ModelSerializer):
    """Список доступных уроков"""

    class Meta:
        model = AvailableLessons
        fields = "__all__"
