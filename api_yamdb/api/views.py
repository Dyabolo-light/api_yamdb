# from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import (IsAuthenticated,
#                                         IsAuthenticatedOrReadOnly)

from reviews.models import Category, Genre, Title
# from .permissions import IsAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'yaer', 'genre', 'category')

# class PostViewSet(viewsets.ModelViewSet):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer
    # permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
#    pagination_class = LimitOffsetPagination

#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)


# class CommentViewSet(viewsets.ModelViewSet):
#   serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

#    def get_queryset(self):
#        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
#        return post.comments.all()

#    def perform_create(self, serializer):
#        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
#        serializer.save(author=self.request.user, post=post)


# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer


# class FollowViewSet(viewsets.ModelViewSet):
#    serializer_class = FollowSerializer
    # permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
#    filter_backends = (filters.SearchFilter,)
#    search_fields = ('following__username',)

#    def get_queryset(self):
#        return self.request.user.follower.all()

#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)
