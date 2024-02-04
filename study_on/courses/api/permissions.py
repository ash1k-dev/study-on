from rest_framework.permissions import BasePermission


class IsAdminOrStuff(BasePermission):
    """Проверка является ли пользователь администратором или персоналом"""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsStudentOnCourse(BasePermission):
    """Проверка является ли пользователь студентом на курсе"""

    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()


class IsTeacherOnCourse(BasePermission):
    """Проверка является ли пользователь преподавателем на курсе"""

    def has_object_permission(self, request, view, obj):
        return obj.teachers.filter(id=request.user.id).exists()
