from rest_framework import serializers

from study_on.courses.api.serializers.lesson import LessonInfoForCourseSerializer, LessonWithContentsSerializer
from study_on.courses.models import Course


class ListCourseSerializer(serializers.ModelSerializer):
    """Список курсов"""

    class Meta:
        model = Course
        # fields = "__all__"
        fields = ["id", "title", "slug", "subject", "author", "teachers", "students"]


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курса"""

    class Meta:
        model = Course
        fields = "__all__"


class UpdateCourseSerializer(serializers.ModelSerializer):
    """Обновление курса"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseParticipantsAmountSerializer(serializers.ModelSerializer):
    """Количество участников (студентов и учителей) курса"""

    teachers_amount = serializers.IntegerField(source="teachers_count", read_only=True)
    students_amount = serializers.IntegerField(source="students_count", read_only=True)
    lessons_amount = serializers.IntegerField(source="lessons_count", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "teachers_amount",
            "students_amount",
            "lessons_amount",
        ]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """Курсы с уроками"""

    lessons = LessonWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "subject", "title", "slug", "created", "lessons"]


class CourseInfoSerializer(serializers.ModelSerializer):
    """Курсы с базовой информацией"""

    students_amount = serializers.IntegerField(source="students_count", read_only=True)

    class Meta:
        model = Course
        fields = ["author", "title", "students_amount"]


class CurrentCourseInfoSerializer(serializers.ModelSerializer):
    """Курсы с подробной информацией"""

    lessons = LessonInfoForCourseSerializer(many=True)
    tests_amount = serializers.IntegerField(source="tests_count", read_only=True)

    class Meta:
        model = Course
        fields = ["title", "description", "teachers", "lessons", "tests_amount"]
