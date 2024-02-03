from rest_framework import serializers

from study_on.courses.api.serializers.content import ListContentSerializer
from study_on.courses.models import Lesson


class ListLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class UpdateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonWithContentsSerializer(serializers.ModelSerializer):
    contents = ListContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["order", "title", "description", "contents"]
