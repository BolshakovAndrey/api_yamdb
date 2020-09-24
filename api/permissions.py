from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Roles


class IsModerator(BasePermission):
    message = 'Не хватает прав, нужны права Модератора'

    def has_permission(self, request, view):
        return request.user.role == Roles.MODERATOR


class IsAdmin(BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN


class IsAdminOrReadOnly(BasePermission):
    """
    Редактирование объекта возможно только для только для admin.
    Для чтения доступно всем.
    """
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or
                        request.user.role == Roles.ADMIN)


class IsSuperuser(BasePermission):
    message = 'Не хватает прав, нужны права Администратора Django'

    def has_permission(self, request, view):
        return request.user.is_superuser
