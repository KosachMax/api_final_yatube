from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    PostSerializer,
    FollowSerializer,
    CommentSerializer,
    GroupSerializer
)
from posts.models import Post, Group


class GroupViewSet(ReadOnlyModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()


class FollowViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    @property
    def get_definite_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_definite_post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_definite_post
        )
        Response(HTTPStatus.OK)
