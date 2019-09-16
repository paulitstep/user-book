from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['image', 'title', 'author', 'published_year', 'user']
    list_filter = ['created', 'user']
