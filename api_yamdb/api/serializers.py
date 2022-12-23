from django.db.models import Avg
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import (Category, Comment, Genre, Review, Title,
                            User)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        required=True,
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):

    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('username', 'email', 'bio', 'role',
                  'first_name', 'last_name')
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError("Username 'me' is not valid")
        return value

    def validate(self, data):
        user_if = User.objects.filter(username=data['username']).exists()
        email_if = User.objects.filter(email=data['email']).exists()
        if user_if:
            if not email_if:
                raise ValidationError('Имя уже использовалось')
        if email_if:
            if not user_if:
                raise ValidationError('Почта уже использовалось')
        if User.objects.filter(username=data['username'], email=data['email']).exists():
            return data
        return data

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ("username", "confirmation_code")
        model = User


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=(UniqueValidator(queryset=Category.objects.all()),)
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=(UniqueValidator(queryset=Genre.objects.all()),)
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        source='genres',
        queryset=Genre.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, year):
        if year > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше чем текущий!'
            )
        return year

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)


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
