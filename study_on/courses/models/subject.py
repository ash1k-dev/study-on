from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.models import BaseModel


class Subject(BaseModel):
    """Модель предмета"""

    heading = models.ForeignKey(
        to="courses.Heading", related_name="subjects", on_delete=models.CASCADE, verbose_name=_("Направление")
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(verbose_name=_("Описание"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Ссылка"))
    is_published = models.BooleanField(default=False, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")

    def __str__(self):
        return self.title
