from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from study_on.courses.models.completion import Completion
from study_on.services.models import BaseModel


class AvailableLessons(BaseModel):
    """Модель доступных для пользователя уроков курса"""

    course = models.ForeignKey(
        to="courses.Course",
        related_name="student",
        on_delete=models.CASCADE,
        verbose_name=_("Курс"),
    )
    student = models.ForeignKey(
        to="users.User",
        related_name="available_lessons",
        on_delete=models.CASCADE,
        verbose_name=_("Студент"),
    )
    max_available_lesson = models.PositiveIntegerField(
        default=0,
        help_text=_(
            "Номер урока",
        ),
        verbose_name=_("Доступный урок"),
    )

    class Meta:
        verbose_name = _("Доступные уроки курса")
        verbose_name_plural = _("Доступные уроки курса")
        unique_together = ["course", "student"]

    def __str__(self):
        return f"Для {self.course.title} доступен урок - {self.max_available_lesson}"


@receiver(post_save, sender=AvailableLessons)
def create_completion_on_max_lesson(sender, instance, created, **kwargs):
    """Создание экземпляра модели Completion при достижении последнего доступного урока"""
    if not created and instance.max_available_lesson == instance.course.lessons.last().order:
        Completion.objects.create(
            course=instance.course,
            student=instance.student,
        )
