from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.mixins import ListCreateViewSet, PerformCreateUserMixin
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Group, Post


class PostViewSet(PerformCreateUserMixin, viewsets.ModelViewSet):
    """ViewSet для обработки публикаций (Post)."""

    queryset = Post.objects.select_related("author", "group")
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    user_field_name = "author"


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для обработки сообществ (Group). Только чтение."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки комментариев (Comment)."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def get_queryset(self):
        return self.get_post().comments.select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(PerformCreateUserMixin, ListCreateViewSet):
    """ViewSet для обработки подписок (Follow)."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)
    user_field_name = "user"

    def get_queryset(self):
        return self.request.user.follower.select_related("following")
