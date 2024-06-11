from rest_framework import serializers

from study_on.courses.models import Survey


class ListSurveySerializer(serializers.ModelSerializer):
    """Список тестов"""

    class Meta:
        model = Survey
        fields = "__all__"


class CreateSurveySerializer(serializers.ModelSerializer):
    """Создание теста"""

    class Meta:
        model = Survey
        fields = "__all__"


class UpdateSurveySerializer(serializers.ModelSerializer):
    """Обновление теста"""

    class Meta:
        model = Survey
        fields = "__all__"
