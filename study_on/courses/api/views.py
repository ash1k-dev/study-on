from typing import Any

from django.db.models import Count, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from study_on.courses.api.filters import (
    ContentFilter,
    CourseFilter,
    LessonFilter,
    QuestionFilter,
    SubjectFilter,
    TestFilter,
)
from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import CreateCourseSerializer  # noqa
from study_on.courses.api.serializers import CreateLessonSerializer  # noqa
from study_on.courses.api.serializers import CreateQuestionSerializer  # noqa
from study_on.courses.api.serializers import CreateSubjectSerializer  # noqa
from study_on.courses.api.serializers import CreateTestSerializer  # noqa
from study_on.courses.api.serializers import UpdateContentSerializer  # noqa
from study_on.courses.api.serializers import UpdateCourseSerializer  # noqa
from study_on.courses.api.serializers import UpdateLessonSerializer  # noqa
from study_on.courses.api.serializers import UpdateQuestionSerializer  # noqa
from study_on.courses.api.serializers import UpdateSubjectSerializer  # noqa
from study_on.courses.api.serializers import UpdateTestSerializer  # noqa
from study_on.courses.api.serializers import (  # noqa
    CourseParticipantsAmountSerializer,
    CourseWithContentsSerializer,
    CreateContentSerializer,
    ListAvailableLessonsSerializer,
    ListContentSerializer,
    ListCourseSerializer,
    ListLessonSerializer,
    ListQuestionSerializer,
    ListSubjectSerializer,
    ListTestSerializer,
    QuestionAnswerSerializer,
    SubjectAmountSerializer,
    SubjectWithCourseSerializer,
    ViewSetSerializerMixin,
)
from study_on.courses.models import AvailableLessons, Content, Course, Lesson, Question, Subject, Test


class BaseModelViewSet(ModelViewSet, ViewSetSerializerMixin):
    pass


class SubjectViewSet(BaseModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = ListSubjectSerializer
    # list_serializer_class = ListSubjectSerializer
    # create_serializer_class = CreateSubjectSerializer
    # update_serializer_class = UpdateSubjectSerializer
    filterset_class = SubjectFilter

    @action(
        detail=False,
        methods=["get"],
        url_path="subjects-with-courses",
        serializer_class=SubjectWithCourseSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def subjects_with_courses(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(courses__isnull=False).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="courses-amount",
        serializer_class=SubjectAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    @method_decorator(cache_page(60 * 15))
    def courses_amount(self, request, *args, **kwargs):
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(course_count=Count("courses"))
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer
    # list_serializer_class = ListCourseSerializer
    # create_serializer_class = CreateCourseSerializer
    # update_serializer_class = UpdateCourseSerializer
    filterset_class = CourseFilter

    @action(
        detail=True,
        methods=["post"],
        url_path="registration-on-course",
        permission_classes=[IsAuthenticated],
    )
    def registration_on_course(self, request, *args, **kwargs):
        course = self.get_object()
        if course.students.filter(id=request.user.id).exists():
            return Response({"registration": False})
        else:
            AvailableLessons.objects.create(course=course, student=request.user)
            course.students.add(request.user)
            return Response({"registration": True})

    @action(
        detail=True,
        methods=["get"],
        url_path="contents",
        serializer_class=CourseWithContentsSerializer,
        permission_classes=(IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff),
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="participants",
        serializer_class=CourseParticipantsAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def participants(self, request, *args, **kwargs):
        annotated_results = Course.objects.annotate(
            teachers_count=Count(F("teachers"), distinct=True),
            students_count=Count(F("students"), distinct=True),
            lessons_count=Count(F("lessons"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class LessonViewSet(BaseModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = ListLessonSerializer
    # list_serializer_class = ListLessonSerializer
    # create_serializer_class = CreateLessonSerializer
    # update_serializer_class = UpdateLessonSerializer
    filterset_class = LessonFilter
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ContentViewSet(BaseModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ListContentSerializer
    # list_serializer_class = ListContentSerializer
    # create_serializer_class = CreateContentSerializer
    # update_serializer_class = UpdateContentSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
    filterset_class = ContentFilter

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class TestViewSet(BaseModelViewSet):
    queryset = Test.objects.all()
    serializer_class = ListTestSerializer
    # list_serializer_class = ListTestSerializer
    # create_serializer_class = CreateTestSerializer
    # update_serializer_class = UpdateTestSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
    filterset_class = TestFilter

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class QuestionViewSet(BaseModelViewSet):
    queryset = Question.objects.all()
    serializer_class = ListQuestionSerializer
    # list_serializer_class = ListQuestionSerializer
    # create_serializer_class = CreateQuestionSerializer
    # update_serializer_class = UpdateQuestionSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
    filterset_class = QuestionFilter

    @action(
        detail=True,
        methods=["post"],
        url_path="answer",
        serializer_class=QuestionAnswerSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def answer(self, request, *args, **kwargs):
        question = self.get_object()
        question.answer_text = request.data["answer_text"]
        question.save()
        return Response({"answer": True})

    @action(
        detail=True,
        methods=["post"],
        url_path="answer-check",
        serializer_class=QuestionAnswerSerializer,
        permission_classes=[IsTeacherOnCourse, IsAdminOrStuff],
    )
    def answer_check(self, request, *args, **kwargs):
        question = self.get_object()
        question.answer_check = True
        question.save()
        return Response({"answer_check": True})

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AvailableLessonsViewSet(BaseModelViewSet):
    queryset = AvailableLessons.objects.all()
    serializer_class = ListAvailableLessonsSerializer
    # list_serializer_class = ListAvailableLessonsSerializer
    # create_serializer_class = CreateAvailableLessonsSerializer
    # update_serializer_class = UpdateAvailableLessonsSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
