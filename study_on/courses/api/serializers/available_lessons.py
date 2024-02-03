from rest_framework import serializers

from study_on.courses.models import AvailableLessons


class ListAvailableLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableLessons
        fields = "__all__"


class CreateAvailableLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableLessons
        fields = "__all__"


class UpdateAvailableLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableLessons
        fields = "__all__"
