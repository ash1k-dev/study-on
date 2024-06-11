from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOrTeacherOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import ListQuestionSerializer, QuestionAnswerSerializer
from study_on.courses.models import Question
from study_on.services.views import BaseModelViewSet


class QuestionFilter(filters.FilterSet):
    """Фильтр для вопросов курса"""

    class Meta:
        model = Question
        fields = ("survey",)


class QuestionViewSet(BaseModelViewSet):
    """Вопрос урока"""

    queryset = Question.objects.all()
    serializer_class = ListQuestionSerializer
    permission_classes = (IsStudentOrTeacherOnCourse,)
    filterset_class = QuestionFilter
    filter_backends = [SearchFilter]
    search_fields = ["title", "question_text"]

    def create(self, request, *args, **kwargs):
        """Создания вопроса"""
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=True,
        methods=["post"],
        url_path="send-answer",
        serializer_class=QuestionAnswerSerializer,
        permission_classes=[IsAdminOrStuff],
    )
    def send_answer(self, request, *args, **kwargs):
        """Отправка ответа на вопрос"""
        question = self.get_object()
        question.answer_text = request.data["answer_text"]
        question.save()
        return Response({"answer": True})

    @action(
        detail=True,
        methods=["post"],
        url_path="check-answer",
        serializer_class=QuestionAnswerSerializer,
        permission_classes=[IsTeacherOnCourse, IsAdminOrStuff],
    )
    def check_answer(self, request, *args, **kwargs):
        """Проверка ответа на вопрос"""
        question = self.get_object()
        question.answer_check = True
        question.save()
        return Response({"answer_check": True})
