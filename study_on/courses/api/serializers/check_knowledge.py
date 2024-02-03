from rest_framework import serializers

from study_on.courses.models import Test


class ListTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class CreateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class UpdateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
