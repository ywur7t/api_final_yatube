from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if not request.user or not request.user.is_authenticated:
                raise AuthenticationFailed("Необходима авторизация.")
        return True


class IsAuthenticated(BasePermission):
    """
    Доступ только для авторизованных пользователей.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован
        return request.user and request.user.is_authenticated


class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешает изменение контента только автору.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем только безопасные методы (GET, HEAD, OPTIONS)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Разрешаем изменение только автору поста
        return obj.author == request.user
