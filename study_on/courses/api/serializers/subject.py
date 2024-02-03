from rest_framework import serializers

from study_on.courses.models import Subject


class ListSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class CreateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class UpdateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectAmountSerializer(serializers.ModelSerializer):
    course_amount = serializers.IntegerField(source="course_count", read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "title", "course_amount"]


class SubjectWithCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
