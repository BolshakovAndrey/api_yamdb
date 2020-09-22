from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.IntegerChoices):
    USER = 1
    MODERATOR = 2
    ADMIN = 3


class User(AbstractUser):
    bio = models.CharField(
        max_length=4000, null=True, verbose_name='Информация о себе')
    confirmation_code = models.CharField(
        max_length=100, null=True, verbose_name='Код подтверждения')
    role = models.IntegerField(
        choices=Roles.choices, default=Roles.USER, verbose_name='Роль')
    username = models.CharField(max_length=30, unique=False, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )
