from rest_framework import serializers

from study_on.courses.models import Test


class ListTestSerializer(serializers.ModelSerializer):
    """Список тестов"""

    class Meta:
        model = Test
        fields = "__all__"


class CreateTestSerializer(serializers.ModelSerializer):
    """Создание теста"""

    class Meta:
        model = Test
        fields = "__all__"


class UpdateTestSerializer(serializers.ModelSerializer):
    """Обновление теста"""

    class Meta:
        model = Test
        fields = "__all__"
