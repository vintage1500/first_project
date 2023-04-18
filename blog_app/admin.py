from django.contrib import admin
from .models import Category, Books


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # Что будет отображаться в категориях
    list_display = ('pk', 'title')
    # Что будет кликабельно
    list_display_links = ('pk', 'title')


class BooksAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'views', 'category', 'author', 'publish')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Books, BooksAdmin)
