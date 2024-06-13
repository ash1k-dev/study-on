from rest_framework import serializers

from study_on.courses.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    """Список тестов"""

    class Meta:
        model = Survey
        fields = "__all__"
