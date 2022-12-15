from django.db import models


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
        vebose_name_plural = 'genres'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        help_text='Введите название произведения',
        max_length=256
    )
    year = models.IntegerField(
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
