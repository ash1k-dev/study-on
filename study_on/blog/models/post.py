from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.base import MAX_TITLE_LENGTH
from study_on.services.models import BaseModel


class Post(BaseModel):
    """Модель поста"""

    author = models.ForeignKey(to="users.User", on_delete=models.CASCADE, verbose_name=_("Автор"))
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))
    image = models.ImageField(upload_to="posts", null=True, blank=True, verbose_name=_("Изображение"))
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликовано"))

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return self.title
