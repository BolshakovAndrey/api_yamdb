from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from collections import Counter


User = get_user_model()


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
        verbose_name=('Произведение'),
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name_plural = 'Рецензия'


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

    class Meta:
        verbose_name_plural = 'Комментарии'
