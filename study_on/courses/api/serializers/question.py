from rest_framework import serializers

from study_on.courses.models import Question


class ListQuestionSerializer(serializers.ModelSerializer):
    """Список вопросов"""

    class Meta:
        model = Question
        fields = "__all__"


class CreateQuestionSerializer(serializers.ModelSerializer):
    """Создание вопроса"""

    class Meta:
        model = Question
        fields = "__all__"


class UpdateQuestionSerializer(serializers.ModelSerializer):
    """Обновление вопроса"""

    class Meta:
        model = Question
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Ответ на вопрос"""

    class Meta:
        model = Question
        fields = "__all__"
        # fields = ("answer_text",)
