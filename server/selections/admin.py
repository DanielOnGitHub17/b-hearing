from django.contrib import admin

from .models import Book, HiddenRange, Selection, Verse, VerseRange

for model in Book, HiddenRange, Selection, Verse, VerseRange:
    admin.site.register(model)
