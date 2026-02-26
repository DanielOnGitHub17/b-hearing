from django.contrib import admin

from .models import Book, Hidden, Selection, Verse, VerseRange


for model in Book, Hidden, Selection, Verse, VerseRange:
    admin.site.register(model)
