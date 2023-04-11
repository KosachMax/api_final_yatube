from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Follow, Group, User
from rest_framework import serializers

from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        default=CurrentUserDefault(),
        slug_field='username',
        queryset=User.objects.all(),
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Can not follow twice'
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if following == user:
            raise serializers.ValidationError('Can not follow yourself')
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group
