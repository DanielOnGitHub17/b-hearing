from django.contrib import admin

from .models import Book, Chapter, Verse

# Register your models here.


for model in Verse, Chapter, Book:
    admin.site.register(model)
