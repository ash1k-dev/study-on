from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from study_on.courses.models import AvailableLessons, Lesson
from study_on.services.models import BaseModel
from study_on.users.tasks import send_email_task


class SurveyStudent(BaseModel):
    """Модель записи студента на тест"""

    student = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="survey_students",
        verbose_name=_("Студент"),
    )
    survey = models.ForeignKey(
        to="courses.Survey",
        on_delete=models.CASCADE,
        related_name="survey_students",
        verbose_name=_("Тест"),
    )
    is_passed = models.BooleanField(default=False, verbose_name=_("Пройден"))

    class Meta:
        verbose_name = _("Тест студента")
        verbose_name_plural = _("Тесты студентов")

    def __str__(self):
        return f"{self.student.username}: {self.survey.title}"


@receiver(post_save, sender=SurveyStudent)
def send_email_to_student(sender, instance, created, **kwargs):
    """Отправка письма студенту после проверки теста и объявление следующего урока доступным"""
    if not created and instance.is_passed:
        if instance.student.notification_permission:
            send_email_task.delay(
                username=instance.student.username,
                email=instance.student.email,
                lesson=instance.survey.lesson.title,
                email_type="survey_approve",
            )
        available_lessons = AvailableLessons.objects.filter(
            student=instance.student, course=instance.survey.lesson.course
        )
        after_lesson = Lesson.objects.filter(
            course=instance.survey.lesson.course, order__gt=available_lessons.max_available_lesson
        )
        if after_lesson.exists():
            available_lessons.first().max_available_lesson = after_lesson.first().order
            available_lessons.save()
