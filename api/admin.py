from django.contrib import admin
from api.models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    """
    Администрирование категорий.
    """
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """
    Администрирование жанров.
    """
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    """
    Администрирование произведений.
    """
    list_display = ('id', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)