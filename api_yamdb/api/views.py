from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from api_yamdb.api.serializers import (CommentSerializer, ReviewSerializer,
                                       CategorySerializer, GenreSerializer,
                                       TitleSerializer)
from api_yamdb.reviews.models import Review, Title, Category, Genre, Title
from api_yamdb.api.viewsets import CreateListDestroyViewSet
from api_yamdb.api.permissions import (AdminModeratorAuthorOrReadOnly,
                                       AdminOnly, AdminOrReadOnly)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # FIXME add "permission_classes = (IsAdmin,)" after they are written 
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # FIXME add "permission_classes = (IsAdminOrReadOnly,)" after they are written 
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # FIXME add "permission_classes = (IsAdminOrReadOnly,)" after they are written 


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
