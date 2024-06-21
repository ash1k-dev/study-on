from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.fields import OrderField
from study_on.services.models import BaseModel


class Question(BaseModel):
    """Модель вопросов для теста"""

    survey = models.ForeignKey(
        to="courses.Survey",
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name=_("Тест"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    text = models.TextField(max_length=400, verbose_name=_("Текст вопроса"))
    order = OrderField(blank=True, for_fields=["survey"], verbose_name=_("Порядок"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def __str__(self):
        return self.title
