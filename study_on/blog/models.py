from django.db import models
from django.utils.translation import gettext_lazy as _

from study_on.services.fields import OrderField
from study_on.services.models import BaseModel


class Post(BaseModel):
    """Модель поста"""

    author = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("Автор"))
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Ссылка"))
    image = models.ImageField(upload_to="posts", null=True, blank=True, verbose_name=_("Изображение"))
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликовано"))

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return self.title


class Content(BaseModel):
    """Модель содержания"""

    post = models.ForeignKey(
        "blog.Post",
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name=_("Пост"),
    )
    text = models.TextField(verbose_name=_("Текст"))
    video = models.URLField(blank=True, verbose_name=_("Видео"))
    image = models.FileField(upload_to="images", blank=True, verbose_name=_("Изображение"))
    order = OrderField(blank=True, for_fields=["lesson"], verbose_name=_("Порядок"))
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликовано"))

    class Meta:
        verbose_name = _("Содержание")
        verbose_name_plural = _("Содержание")
