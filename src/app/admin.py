from django.contrib import admin

from .models import Book, Rate

@admin.register(Book)
class Book(admin.ModelAdmin):
    pass

@admin.register(Rate)
class Rate(admin.ModelAdmin):
    pass