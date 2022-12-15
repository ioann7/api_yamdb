from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=(UniqueValidator(queryset=Category.objects.all()),)
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category
