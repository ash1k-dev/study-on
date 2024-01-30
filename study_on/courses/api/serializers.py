from rest_framework import serializers

from ..models import Content, Course, Lesson, Question, Subject, Test


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectAmountSerializer(serializers.ModelSerializer):
    course_amount = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ["id", "title", "course_amount"]

    def get_course_amount(self, obj):
        return obj.courses.count()


class SubjectWithCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("answer_text",)


class LessonWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["order", "title", "description"]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    lessons = LessonWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "subject", "title", "slug", "created", "lessons"]
