from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel
from study_on.users.tasks import send_email


class Answer(BaseModel):
    """Модель ответов на вопросы"""

    survey_student = models.ForeignKey(
        to="courses.SurveyStudent",
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Студент"),
    )
    question = models.ForeignKey(
        to="courses.Question", on_delete=models.CASCADE, related_name="answers", verbose_name=_("Вопрос")
    )
    text = models.TextField(verbose_name=_("Ответ"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Правильность"))

    class Meta:
        verbose_name = _("Ответ")
        verbose_name_plural = _("Ответы")
        constraints = [models.UniqueConstraint(fields=["question"], name="unique_answer")]

    def __str__(self):
        return f"{self.question.title}: {self.is_correct}"


@receiver(post_save, sender=Answer)
def check_survey(sender, instance, created, **kwargs):
    """Проверка теста студента"""
    if not created and instance.is_correct:
        questions = instance.survey_student.survey.questions.all().count()
        answers = Answer.objects.filter(survey_student=instance.survey_student, is_correct=True).count()
        if questions == answers:
            instance.survey_student.is_passed = True
            instance.survey_student.save()


@receiver(post_save, sender=Answer)
def send_email_to_teacher(sender, instance, created, **kwargs):
    """Отправка писем учителям при ответе на все вопросы теста"""
    if created:
        questions = instance.survey_student.survey.questions.all().count()
        answers = Answer.objects.filter(survey_student=instance.survey_student).count()
        if questions == answers:
            teachers = instance.survey_student.survey.lesson.course.teachers.all()
            for teacher in teachers:
                send_email.delay(
                    teacher.username, teacher.email, instance.survey_student.survey.lesson.title, "survey_done"
                )
