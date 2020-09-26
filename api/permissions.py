from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Редактирование объекта возможно только для Автора.
    """

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and
                obj.author == request.user)


class IsModerator(BasePermission):
    """
    Редактирование объекта возможно только для Модератора.
    """
    message = 'Не хватает прав, нужны права Модератора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Редактирование объекта возможно только для Администратора.
    Для чтения доступно всем.
    """
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(BasePermission):
    """
    Для редактирование объекта необходим статус superuser
    """
    message = 'Не хватает прав, нужны права Администратора Django'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_superuser)
