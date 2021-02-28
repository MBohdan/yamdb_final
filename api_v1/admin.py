from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title_id", "score", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = ("name",)
    list_filter = ("year",)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(User)
