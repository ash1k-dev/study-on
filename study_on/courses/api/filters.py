from django_filters import rest_framework as filters

from study_on.courses.models import Content, Course, Lesson, Question, Subject, Test


class SubjectFilter(filters.FilterSet):
    class Meta:
        model = Subject
        fields = ("slug",)


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = ("subject", "teachers", "students", "slug")


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ("course",)


class ContentFilter(filters.FilterSet):
    class Meta:
        model = Content
        fields = ("lesson",)


class TestFilter(filters.FilterSet):
    class Meta:
        model = Test
        fields = ("lesson",)


class QuestionFilter(filters.FilterSet):
    class Meta:
        model = Question
        fields = ("test",)
