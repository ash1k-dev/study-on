from rest_framework import serializers

from study_on.courses.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Список контента"""

    class Meta:
        model = Content
        fields = "__all__"
