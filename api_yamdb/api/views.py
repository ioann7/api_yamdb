from rest_framework import filters
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from api.serializers import CategorySerializer
from api.viewsets import CreateListDestroyViewSet
from api_yamdb.api.permissions import (AdminModeratorAuthorOrReadOnly,
                                       AdminOnly, AdminOrReadOnly)
from api_yamdb.api.serializers import CommentSerializer, ReviewSerializer
from api_yamdb.reviews.models import Review, Title, Category


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # FIXME add "permission_classes = (IsAdmin,)" after they are written 
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
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

