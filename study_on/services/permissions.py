from rest_framework.permissions import BasePermission


class IsAdminOrStuff(BasePermission):
    """Проверка является ли пользователь администратором или персоналом"""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
