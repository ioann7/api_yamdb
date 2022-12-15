from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from api.serializers import (CategorySerializer,
                             GenreSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title
from api.viewsets import CreateListDestroyViewSet


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # FIXME add "permission_classes = (IsAdmin,)" after they are written 
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


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
