from posts.models import Group
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

from posts.models import Comment, Post, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        fields = ['id', 'text', 'image', 'group', 'author', 'pub_date']

    def validate(self, data):
        if 'text' not in data or not data['text'].strip():
            raise ValidationError({'text':
                                   'Поле "text" обязательно для заполнения.'})
        return data

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        if 'group' in self.initial_data:
            group = self.initial_data['group']
            post.group = Group.objects.get(pk=group)
            post.save()

        return post

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.author:
            raise PermissionDenied('Вы не можете редактировать этот пост.')
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")
        return value
