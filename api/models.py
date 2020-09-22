from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Genre")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(verbose_name="Creation year", null=True, db_index=True)
    description = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="titles")
    # rating = models.IntegerField(default=None, null=True, blank=True)
