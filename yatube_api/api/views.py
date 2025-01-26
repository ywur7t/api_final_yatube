# from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
# from api.permisssions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.permisssions import IsOwner
from posts.models import Follow, Post
from .serializers import FollowSerializer, PostSerializer

from api.serializers import CommentSerializer
from posts.models import Comment
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import AllowAny
from api.serializers import GroupSerializer
from django.contrib.auth.models import Group


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        search_param = self.request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(
                following__username__icontains=search_param)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        following = serializer.validated_data['following']
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя.")
        serializer.save(user=user)


class PostViewSet(viewsets.ModelViewSet):  # Только чтение
    queryset = Post.objects.select_related('author', 'group').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Проверка на авторизацию
        if not self.request.user or not self.request.user.is_authenticated:
            raise PermissionDenied(
                "Вы должны быть авторизованы для создания поста.")
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой пост.")
        super().perform_destroy(instance)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)  # Проверяем права
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # Разрешения на просмотр групп
    permission_classes = [IsAuthenticatedOrReadOnly]

    # permission_classes_by_action = {
    #     'retrieve': [IsAuthenticatedOrReadOnly],
    #     'list': [IsAuthenticatedOrReadOnly],
    #     'create': [IsAuthenticated],
    #     'update': [IsAuthenticated],
    #     'partial_update': [IsAuthenticated],
    #     'destroy': [IsAuthenticated],
    # }

    # def get_permissions(self):
    #     return [permission() for permission in
    #             self.permission_classes_by_action.get(self.action,
    #                                                   self.permission_classes)]
# class GroupViewSet(viewsets.ReadOnlyModelViewSet):

#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     permission_classes_by_action = {
#         'retrieve': [IsAuthenticated],
#         'list': [IsAuthenticatedOrReadOnly],
#         'create': [IsAuthenticated],
#         'update': [IsAuthenticated],
#         'partial_update': [IsAuthenticated],
#         'destroy': [IsAuthenticated],
#     }

#     def get_permissions(self):
#         return [permission() for permission in
#                 self.permission_classes_by_action.get(self.action,
#                                                       self.permission_classes)]
    # permission_classes_by_action = {
    #     'retrieve': [IsAuthenticated],
    #     'list': [IsAuthenticatedOrReadOnly],
    #     'create': [IsAuthenticated],
    #     'update': [IsAuthenticated],
    #     'partial_update': [IsAuthenticated],
    #     'destroy': [IsAuthenticated]
    # }

    # def get_permissions(self):
    #     return [permission() for permission in
    #             self.permission_classes_by_action.get(self.action,
    #                                                   self.permission_classes)]

    # def create(self, request, *args, **kwargs):
    #     raise PermissionDenied("Создание групп через API запрещено.")

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     Обрабатывает запрос GET /api/v1/groups/{group_id}/.
    #     """
    #     group_id = kwargs.get('pk')  # Получаем ID группы из URL
    #     group = self.get_queryset().filter(id=group_id).first()

    #     if not group:
    #         raise NotFound(f"Группа с ID {group_id} не найдена.")

    #     serializer = self.get_serializer(group)
    #     return Response(serializer.data)
