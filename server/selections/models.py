"""Data Entities for Bible Hearing app"""

from django.db import models
from users.models import User


class Book(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True)
    abbreviation = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=2000)


class Verse(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="verses")
    chapter = models.IntegerField(default=0)
    verse = models.IntegerField(default=0)
    kjv = models.CharField(verbose_name="King James Version")
    gnb = models.CharField(verbose_name="Good News Bible", default="")
    # Add more versions as needed (Will require migrations. This is intended)
    # Then run populate_verses with that version.

    # maybe have: embedding = models.vector, etc - will be helpful for search.
    # Switch to Postgres to use vector field
    # Or I wonder if I can cheat mysql/sqlite with a biginteger
    # having base as the length of the vector
    # Might be able to run cosine similarity on that
    def __str__(self):
        return f"{self.book.name} {self.chapter}:{self.verse}"

    def to_dict(self, version: str = "kjv") -> dict[str, int | str]:
        return {
            "book": self.book.name,
            "chapter": self.chapter,
            "verse": self.verse,
            "text": getattr(self, version),
        }


class Selection(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="selections"
    )
    label = models.CharField(unique=True)
    voice = models.CharField(default="default")
    repeat = models.IntegerField()
    version = models.CharField()
    read_label = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "label": self.label,
            "voice": self.voice,
            "repeat": self.repeat,
            "version": self.version,
            "readLabel": self.read_label,
        }


class VerseRange(models.Model):
    selection = models.ForeignKey(
        to=Selection, on_delete=models.CASCADE, related_name="verse_ranges"
    )
    start_verse = models.ForeignKey(
        to=Verse, on_delete=models.CASCADE, related_name="start_verse_ranges"
    )
    end_verse = models.ForeignKey(
        to=Verse, on_delete=models.CASCADE, related_name="end_verse_ranges"
    )


class HiddenRange(models.Model):
    verse_range = models.ForeignKey(
        to=VerseRange, on_delete=models.CASCADE, related_name="hidden_ranges"
    )
    start_verse = models.ForeignKey(
        to=Verse, on_delete=models.CASCADE, related_name="start_hidden_ranges"
    )
    end_verse = models.ForeignKey(
        to=Verse, on_delete=models.CASCADE, related_name="end_hidden_ranges"
    )
