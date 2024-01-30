from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import AvailableLessons, Content, Course, Lesson, Question, Subject, Test
from .permissions import IsAdminOrStuff, IsLessonAvailable, IsOnCourse
from .serializers import (
    ContentSerializer,
    CourseSerializer,
    CourseWithContentsSerializer,
    LessonSerializer,
    QuestionAnswerSerializer,
    QuestionSerializer,
    SubjectAmountSerializer,
    SubjectSerializer,
    SubjectWithCourseSerializer,
    TestSerializer,
)


class SubjectViewSet(ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(
        detail=False,
        methods=["get"],
        serializer_class=SubjectWithCourseSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsAdminOrStuff],
    )
    def subjects_with_courses(self, request):
        queryset = self.get_queryset().filter(courses__isnull=False).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=SubjectWithCourseSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsAdminOrStuff],
    )
    def amount_courses(self, request, *args, **kwargs):
        # annotated_results = Subject.objects.annotate(course_count=Count('courses'))
        annotated_results = self.get_queryset()
        serializer = SubjectAmountSerializer(annotated_results, many=True)
        return Response(serializer.data)


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
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
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsOnCourse],
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class LessonViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsLessonAvailable)


class ContentViewSet(ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    # permission_classes = (IsAuthenticated, IsLessonAvailable)


class TestViewSet(ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    # permission_classes = (IsAuthenticated, IsLessonAvailable)


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = (IsAuthenticated, IsLessonAvailable)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=QuestionAnswerSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsAdminOrStuff],
    )
    def answer(self, request, *args, **kwargs):
        question = self.get_object()
        question.answer_text = request.data["answer_text"]
        question.save()
        return Response({"answer": True})
