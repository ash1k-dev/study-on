from datetime import datetime
from os import getenv

from django.db.models import Count, F
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOrTeacherOnCourse
from study_on.courses.api.serializers import (
    BookmarkSerializer,
    CourseInfoSerializer,
    CourseParticipantsAmountSerializer,
    CourseWithContentsSerializer,
    CurrentCourseInfoSerializer,
    ListCourseSerializer,
    ReviewSerializer,
)
from study_on.courses.models import AvailableLessons, Bookmark, Completion, Course, Review
from study_on.services.views import BaseModelViewSet
from study_on.services.work_with_docx import create_file, upload_file

TEMPLATE_PATH = getenv("CERTIFICATE_TEMPLATE_PATH", default="study_on/courses/api/templates/certificate.docx")
FILE_PATH = getenv("CERTIFICATE_FILE_PATH", default="study_on/courses/api/templates")


class CourseFilter(filters.FilterSet):
    """Фильтр для курсов"""

    class Meta:
        model = Course
        fields = ("subject", "teachers", "students", "slug")


class CourseViewSet(BaseModelViewSet):
    """Курс"""

    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer
    filterset_class = CourseFilter
    filter_backends = [SearchFilter]
    search_fields = [
        "slug",
        "title",
        "description",
        "subject__title",
        "teachers__username",
        "students__username",
    ]

    def create(self, request, *args, **kwargs):
        """Создание курса"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        """Список курсов"""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related("subject").prefetch_related("teachers", "students", "lessons")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="register-student-on-course",
        permission_classes=[IsAuthenticated],
    )
    def register_student_on_course(self, request, *args, **kwargs):
        """Регистрация студента на курс"""
        course = self.get_object()
        if course.students.filter(id=request.user.id).exists():
            return Response({"registration": False})
        else:
            AvailableLessons.objects.create(course=course, student=request.user)
            course.students.add(request.user)
            return Response({"registration": True})

    @action(
        detail=True,
        methods=["post"],
        url_path="register-teacher-on-course",
        permission_classes=[IsAuthenticated],
    )
    def register_teacher_on_course(self, request, *args, **kwargs):
        """Регистрация учителя на курс"""
        course = self.get_object()
        if course.teachers.filter(id=request.data["teachers"]).exists():
            print(request.data)
            return Response({"registration": False})
        else:
            print(request.data)
            course.teachers.add(request.data["teachers"])
            return Response({"registration": True})

    @action(
        detail=True,
        methods=["get"],
        url_path="get-contents",
        serializer_class=CourseWithContentsSerializer,
        permission_classes=[IsStudentOrTeacherOnCourse],
    )
    def get_contents(self, request, *args, **kwargs):
        """Получение содержимого курса"""
        course = self.get_object()
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-participants",
        serializer_class=CourseParticipantsAmountSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_participants(self, request, *args, **kwargs):
        """Получение количества участников курса"""
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(
            teachers_count=Count(F("teachers"), distinct=True),
            students_count=Count(F("students"), distinct=True),
            lessons_count=Count(F("lessons"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="get-courses-info",
        serializer_class=CourseInfoSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_courses_info(self, request, *args, **kwargs):
        """Получение информации о курсах(автор, название, кол-во участников)"""
        annotated_results = self.filter_queryset(self.get_queryset()).annotate(
            students_count=Count(F("students"), distinct=True),
        )
        serializer = self.get_serializer(annotated_results, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="get-current-course-info",
        serializer_class=CurrentCourseInfoSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def get_current_course_info(self, request, *args, **kwargs):
        """Получение информации о курсе (название, описание, преподаватели, уроки, кол-во тестов)"""
        uinited_results = (
            self.filter_queryset(self.get_queryset())
            .prefetch_related("teachers")
            .prefetch_related(
                "lessons",
                "lessons__tests",
            )
            .annotate(tests_count=Count("lessons__tests"))
        )
        serializer = self.get_serializer(uinited_results)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="post-review",
        permission_classes=[IsAuthenticated],
        serializer_class=ReviewSerializer,
    )
    def post_review(self, request, *args, **kwargs):
        """Создание отзыва"""
        if Review.objects.filter(student=request.user, course=self.get_object()).exists():
            return Response({"review": "already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Review.objects.create(student=request.user, course=self.get_object(), text=request.data["text"])
            return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        url_path="post-bookmark",
        permission_classes=[IsAuthenticated],
        serializer_class=BookmarkSerializer,
    )
    def post_bookmark(self, request, *args, **kwargs):
        """Создание записи в закладках"""
        if Bookmark.objects.filter(student=request.user, course=self.get_object()).exists():
            return Response({"bookmark": "already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Bookmark.objects.create(student=request.user, course=self.get_object())
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="get-certificate")
    def get_certificate(self, request, *args, **kwargs):
        """Получение сертификата о прохождении курса"""
        user = request.user
        course = self.get_object()
        if not Completion.objects.filter(student=user, course=course).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        context = {"user": user, "course": course, "date": datetime.now().strftime("%Y-%m-%d")}
        template_path = TEMPLATE_PATH
        file_path = f"{FILE_PATH}/{user.username}"
        create_file(context, template_path, file_path)
        return upload_file(file_path, request.user)
