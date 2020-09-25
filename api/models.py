from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .utils import generate_confirmation_code


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """
    Переопределенный пользователь, дополнен нужныеми полями
    """
    bio = models.CharField(max_length=4000, null=True,
                           verbose_name='Информация о себе')
    confirmation_code = models.CharField(max_length=100, null=True,
                                         verbose_name='Код подтверждения',
                                         default=generate_confirmation_code())
    role = models.CharField(max_length=50, choices=Roles.choices,
                            verbose_name='Роль')
    username = models.CharField(max_length=30, unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True,
                              blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )


class Genre(models.Model):
    """
    Жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(max_length=200, verbose_name="Жанр", unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    """
    name = models.CharField(max_length=200, verbose_name="Категория", unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
    """
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(null=True)
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name="titles")

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """
    Отзывы на произведения
    """
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=False,
        null=False
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        unique_together = ['author', 'title']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'


class Comment(models.Model):
    """
    Комментарии к отзывам
    """
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к {self.review}'
