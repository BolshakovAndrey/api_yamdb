from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import generate_confirmation_code
from django.core.validators import MaxValueValidator, MinValueValidator
from collections import Counter


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.CharField(
        max_length=4000, null=True, verbose_name='Информация о себе')
    confirmation_code = models.CharField(
        max_length=100, null=True, verbose_name='Код подтверждения',
        default=generate_confirmation_code())
    role = models.CharField(
        max_length=50, choices=Roles.choices, verbose_name='Роль')
    username = models.CharField(
        max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(
        max_length=255, unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name=('Автор'),
        on_delete=models.CASCADE
    )
    scope = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=False
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        unique_together = ['author', 'scope']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

