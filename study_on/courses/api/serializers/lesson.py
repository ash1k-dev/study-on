from rest_framework import serializers

from study_on.courses.api.serializers.content import ContentSerializer
from study_on.courses.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonWithContentsSerializer(serializers.ModelSerializer):
    """Урок с содержанием"""

    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["order", "title", "description", "contents"]


class LessonInfoForCourseSerializer(serializers.ModelSerializer):
    """Название урока"""

    class Meta:
        model = Lesson
        fields = ["title"]
