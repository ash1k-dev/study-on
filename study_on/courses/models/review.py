from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Review(BaseModel):
    """Модель отзыва"""

    course = models.ForeignKey(
        to="courses.Course",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Курс"),
    )
    student = models.ForeignKey(
        to="users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Студент"),
    )
    text = models.TextField(blank=True, verbose_name=_("Текст отзыва"))
    grade = models.PositiveIntegerField(
        default=0,
        help_text=_(
            "Оценка от 0 до 5",
        ),
        choices=[(i, i) for i in range(0, 6)],
        verbose_name=_("Оценка"),
    )

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        constraints = [models.UniqueConstraint(fields=["course", "student"], name="unique_review")]

    def __str__(self):
        return f"Отзыв {self.student} на курс {self.course}"
