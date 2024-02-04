from rest_framework import serializers

from study_on.courses.models import Subject


class ListSubjectSerializer(serializers.ModelSerializer):
    """Список предметов"""

    class Meta:
        model = Subject
        fields = "__all__"


class CreateSubjectSerializer(serializers.ModelSerializer):
    """Создание предмета"""

    class Meta:
        model = Subject
        fields = "__all__"


class UpdateSubjectSerializer(serializers.ModelSerializer):
    """Обновление предмета"""

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

    class Meta:
        model = Subject
        fields = "__all__"
