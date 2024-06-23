from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from study_on.services.models import BaseModel


class Subject(BaseModel):
    """Модель предмета"""

    heading = models.ForeignKey(
        to="courses.Heading", related_name="subjects", on_delete=models.CASCADE, verbose_name=_("Направление")
    )
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Заголовок"))
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, verbose_name=_("Описание"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")

    def __str__(self):
        return self.title
