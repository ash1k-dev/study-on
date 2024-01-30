from django.db import models

from .fields import OrderField


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subject(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.title


class Course(BaseModel):
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE, verbose_name="Предмет")
    teachers = models.ManyToManyField(
        "users.User", related_name="courses_teachers", blank=True, verbose_name="Преподаватели"
    )
    students = models.ManyToManyField("users.User", related_name="courses_joined", blank=True, verbose_name="Студенты")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    order = OrderField(blank=True, for_fields=["course"], verbose_name="Порядок")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Content(BaseModel):
    lesson = models.ForeignKey(Lesson, related_name="contents", on_delete=models.CASCADE, verbose_name="Урок")
    text = models.TextField(verbose_name="Текст")
    video = models.URLField(verbose_name="Видео", blank=True)
    image = models.FileField(upload_to="images", blank=True, verbose_name="Изображение")
    order = OrderField(blank=True, for_fields=["lesson"], verbose_name="Порядок")

    class Meta:
        verbose_name = "Содержание"
        verbose_name_plural = "Содержание"

    def __str__(self):
        return self.text


class Test(BaseModel):
    lesson = models.ForeignKey(Lesson, related_name="tests", on_delete=models.CASCADE, verbose_name="Урок")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    answer_check = models.BooleanField(verbose_name="Правильность", default=False)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.title


class Question(BaseModel):
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE, verbose_name="Тест")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    question_text = models.TextField(max_length=400, verbose_name="Текст вопроса")
    answer_text = models.TextField(max_length=500, verbose_name="Текст ответа", blank=True)
    order = OrderField(blank=True, for_fields=["test"], verbose_name="Порядок")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title


class AvailableLessons(BaseModel):
    course = models.ForeignKey(Course, related_name="students", on_delete=models.CASCADE, verbose_name="Курс")
    student = models.ForeignKey(
        "users.User", related_name="available_lessons", on_delete=models.CASCADE, verbose_name="Студент"
    )
    available = models.PositiveIntegerField(default=0, verbose_name="Доступный урок", help_text="Номер урока")

    class Meta:
        verbose_name = "Доступные уроки курса"
        verbose_name_plural = "Доступные уроки курса"

    def __str__(self):
        return self.course
