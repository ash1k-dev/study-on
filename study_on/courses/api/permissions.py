from rest_framework.permissions import BasePermission

from study_on.study_on.courses.models import AvailableLessons


class IsAdminOrStuff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOnCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()


class IsLessonAvailable(BasePermission):
    def has_object_permission(self, request, view, obj):
        available_lesson = AvailableLessons.objects.get(course=obj.course, student=request.user)
        if obj.order <= available_lesson.available:
            return True
        return False
