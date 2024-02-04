from rest_framework import serializers

from study_on.courses.models import Content


class ListContentSerializer(serializers.ModelSerializer):
    """Список контента"""

    class Meta:
        model = Content
        fields = "__all__"


class CreateContentSerializer(serializers.ModelSerializer):
    """Создание контента"""

    class Meta:
        model = Content
        fields = "__all__"


class UpdateContentSerializer(serializers.ModelSerializer):
    """Обновление контента"""

    class Meta:
        model = Content
        fields = "__all__"
