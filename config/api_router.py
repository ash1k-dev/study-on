from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from study_on.blog.api.views.blog import PostViewSet
from study_on.courses.api.views import (
    AvailableLessonsViewSet,
    BookmarkViewSet,
    ContentViewSet,
    CourseViewSet,
    LessonViewSet,
    QuestionViewSet,
    ReviewViewSet,
    SubjectViewSet,
    SurveyViewSet,
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
router.register("surveys", SurveyViewSet)
router.register("questions", QuestionViewSet)
router.register("available-lessons", AvailableLessonsViewSet)
router.register("blog", PostViewSet)
router.register("bookmarks", BookmarkViewSet)
router.register("reviews", ReviewViewSet)


app_name = "api"
urlpatterns = router.urls
