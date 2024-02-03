from study_on.courses.api.views.available_lessons import AvailableLessonsViewSet
from study_on.courses.api.views.check_knowledge import TestViewSet
from study_on.courses.api.views.content import ContentViewSet
from study_on.courses.api.views.course import CourseViewSet
from study_on.courses.api.views.lesson import LessonViewSet
from study_on.courses.api.views.question import QuestionViewSet
from study_on.courses.api.views.subject import SubjectViewSet

__all__ = [
    "SubjectViewSet",
    "CourseViewSet",
    "LessonViewSet",
    "ContentViewSet",
    "TestViewSet",
    "QuestionViewSet",
    "AvailableLessonsViewSet",
]
