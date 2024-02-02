from rest_framework import serializers
from rest_framework.serializers import Serializer

from study_on.courses.models import AvailableLessons, Content, Course, Lesson, Question, Subject, Test


class ViewSetSerializerMixin:
    create_serializer_class: Serializer | None = None
    update_serializer_class: Serializer | None = None
    list_serializer_class: Serializer | None = None

    def _get_serializer_class(
        self,
        *args,
        **kwargs,
    ):
        if self.action == "create":  # type: ignore
            return self.create_serializer_class
        if self.action in {"update", "partial_update"}:  # type: ignore
            return self.update_serializer_class or self.create_serializer_class
        if self.action == "list":  # type: ignore
            return self.list_serializer_class
        return None

    def get_serializer_class(self):
        serializer_class = self._get_serializer_class()
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()  # type: ignore


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


class ListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseParticipantsAmountSerializer(serializers.ModelSerializer):
    teachers_amount = serializers.IntegerField(source="teachers_count", read_only=True)
    students_amount = serializers.IntegerField(source="students_count", read_only=True)
    lessons_amount = serializers.IntegerField(source="lessons_count", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "subject", "title", "teachers_amount", "students_amount", "lessons_amount"]


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


class ListContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class CreateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class UpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


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


class ListQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class UpdateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("answer_text",)


class LessonWithContentsSerializer(serializers.ModelSerializer):
    contents = ListContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["order", "title", "description", "contents"]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    lessons = LessonWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "subject", "title", "slug", "created", "lessons"]


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
