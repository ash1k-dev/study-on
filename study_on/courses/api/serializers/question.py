from rest_framework import serializers

from study_on.courses.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Список вопросов"""

    class Meta:
        model = Question
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Ответ на вопрос"""

    class Meta:
        model = Question
        fields = "__all__"
        # fields = ("answer_text",)
