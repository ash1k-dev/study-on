from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel

CHOICES = (
    ("course_completion", "Пройдено определенное количество курсов"),
    ("lesson_completion", "Пройдено определенное количество уроков"),
    ("task_completion", "Завершено определенное количество заданий"),
)


class Reward(BaseModel):
    """Модель для награды"""

    title = models.CharField(max_length=200, verbose_name=_("Название награды"))
    reward_type = models.CharField(
        max_length=50,
        choices=CHOICES,
        verbose_name=_("Тип награды"),
    )
    reward_value = models.IntegerField(default=0, verbose_name=_("Количество действий, нужное для получения награды"))
    image = models.ImageField(blank=True, upload_to="images", verbose_name=_("Изображение"))

    class Meta:
        verbose_name = _("Награда")
        verbose_name_plural = _("Награды")

    def __str__(self):
        return self.title
