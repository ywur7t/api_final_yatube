# TODO:  Напишите свой вариант
from .serializers import GroupSerializer
from posts.models import Group, Comment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.models import Post
from api.serializers import PostSerializer
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from api.serializers import FollowSerializer, CommentSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        comment_id = self.kwargs.get('comment_id')
        try:
            comment = queryset.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")
        serializer = self.get_serializer(comment)
        return Response(data=serializer.data)
