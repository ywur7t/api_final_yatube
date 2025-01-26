from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermission(BasePermission):
    """
    Разрешает изменения (PUT, PATCH, DELETE) только автору поста.
    Чтение доступно всем.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем
        if request.method in SAFE_METHODS:
            return True
        # Разрешить изменения только автору
        return obj.author == request.user
