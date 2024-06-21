from study_on.courses.api.views.answer import AnswerViewSet
from study_on.courses.api.views.available_lessons import AvailableLessonsViewSet
from study_on.courses.api.views.bookmark import BookmarkViewSet
from study_on.courses.api.views.complition import CompletionViewSet
from study_on.courses.api.views.content import ContentViewSet
from study_on.courses.api.views.course import CourseViewSet
from study_on.courses.api.views.heading import HeadingViewSet
from study_on.courses.api.views.lesson import LessonViewSet
from study_on.courses.api.views.question import QuestionViewSet
from study_on.courses.api.views.review import ReviewViewSet
from study_on.courses.api.views.subject import SubjectViewSet
from study_on.courses.api.views.survey import SurveyViewSet

__all__ = [
    "SubjectViewSet",
    "CourseViewSet",
    "LessonViewSet",
    "ContentViewSet",
    "SurveyViewSet",
    "QuestionViewSet",
    "AvailableLessonsViewSet",
    "BookmarkViewSet",
    "ReviewViewSet",
    "HeadingViewSet",
    "CompletionViewSet",
    "AnswerViewSet",
]
