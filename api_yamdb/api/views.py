from rest_framework import filters

from api.serializers import CategorySerializer
from reviews.models import Category
from api.viewsets import CreateListDestroyViewSet


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # FIXME add "permission_classes = (IsAdmin,)" after they are written 
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
