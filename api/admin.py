from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title, User


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


class ReviewAdmin(admin.ModelAdmin):
    """
    Администрирование отзывов.
    """
    list_display = ('id', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """
    Администрирование комментариев.
    """
    list_display = ('id', 'text', 'author', 'pub_date')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    """
    Администрирование ролей пользователей.
    """
    list_display = ("role",)


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
