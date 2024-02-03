from study_on.courses.api.permissions import IsAdminOrStuff, IsStudentOnCourse, IsTeacherOnCourse
from study_on.courses.api.serializers import ListAvailableLessonsSerializer
from study_on.courses.models import AvailableLessons
from study_on.services.views import BaseModelViewSet


class AvailableLessonsViewSet(BaseModelViewSet):
    queryset = AvailableLessons.objects.all()
    serializer_class = ListAvailableLessonsSerializer
    permission_classes = (IsStudentOnCourse, IsTeacherOnCourse, IsAdminOrStuff)
