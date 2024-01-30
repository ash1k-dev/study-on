from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from study_on.courses.api.views import (
    ContentViewSet,
    CourseViewSet,
    LessonViewSet,
    QuestionViewSet,
    SubjectViewSet,
    TestViewSet,
)
from study_on.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("subjects", SubjectViewSet)
router.register("courses", CourseViewSet)
router.register("contents", ContentViewSet)
router.register("lessons", LessonViewSet)
router.register("tests", TestViewSet)
router.register("questions", QuestionViewSet)


app_name = "api"
urlpatterns = router.urls
