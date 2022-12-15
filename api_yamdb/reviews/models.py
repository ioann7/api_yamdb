from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        help_text='Введите название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Slug',
        help_text='Введите slug',
        unique=True
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return f'{self.name} | {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        help_text='Введите название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Slug',
        help_text='Введите slug',
        max_length=50
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
    
    def __str__(self):
        return f'{self.name} | {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        help_text='Введите название произведения',
        max_length=256
    )
    year = models.PositiveIntegerField(
        'Год выпуска произведения',
        help_text='Введите год выпуска произведения'
    )
    description = models.TextField(
        'Описание произведения',
        help_text='Введите описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию для произведения'
    )
    genres = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
    
    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'genre_title'
        verbose_name_plural = 'genres_titles'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'
            ),
        )
    
    def __str__(self):
        return f'{self.genre} | {self.title}'


class Review(models.Model):
    """
    Class representing a review on Title from auth users.
    """
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Опубликовано'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Class representing a comment on Review from auth users.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Опубликовано'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
