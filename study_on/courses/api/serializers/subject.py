from rest_framework import serializers

from study_on.courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    """Список предметов"""

    class Meta:
        model = Subject
        fields = "__all__"


class SubjectAmountSerializer(serializers.ModelSerializer):
    """Количество курсов по предмету"""

    course_amount = serializers.IntegerField(source="course_count", read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "title", "course_amount"]


class SubjectWithCourseSerializer(serializers.ModelSerializer):
    """Предметы с курсами"""

    count = serializers.IntegerField(source="course_count", read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "title", "slug", "count"]
