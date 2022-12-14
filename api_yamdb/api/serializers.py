from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author'],
                message='Отзыв можно оставить только один раз!'
            )
        ]

    def validate_score(self, score):
        if 1 > score > 10:
            raise serializers.ValidationError(
                'Допустимые значения оценки - от 1 до 10!'
            )
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
