
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissons import AuthorPermission

from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

from posts.models import Comment, Group, Post
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permisssions import IsOwner
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Список групп.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Список подписок.
    """

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    Список постов.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorPermission,)
    pagination_class = LimitOffsetPagination

    permission_classes_by_action = {

        'create': [IsAuthenticatedOrReadOnly],
    }

    def get_permissions(self):
        return [permission() for permission in
                self.permission_classes_by_action.get(self.action,
                                                      self.permission_classes)]

    def perform_create(self, serializer):
        # Проверка на авторизацию
        if not self.request.user or not self.request.user.is_authenticated:
            raise PermissionDenied(
                "Вы должны быть авторизованы для создания поста.")
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    permission_classes_by_action = {
        'retrieve': [AllowAny],  # Доступ для всех
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        return [permission() for permission in
                self.permission_classes_by_action.get(self.action,
                                                      self.permission_classes)]
