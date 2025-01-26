from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        # Ваша кастомная логика для аутентификации
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
