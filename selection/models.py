from django.db import models

from users.models import User


class Verse(models.Model):
    number = models.IntegerField(primary_key=True)  # Will start from 1 :)
    kjv = models.CharField(verbose_name="King James Version")
    gnb = models.CharField(verbose_name="Good News Bible")
    # Add more versions as needed (Will require migrations. This is intended)
    # Then run populate_verses with that version.

    # maybe have: embedding = models.vector, etc - will be helpful for search.
    # Switch to Postgres to use vector field
    # Or I wonder if I can cheat mysql/sqlite with a biginteger
    # having base as the length of the vector
    # Might be able to run cosine similarity on that


class Chapter(models.Model):
    number = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    start = models.ForeignKey(to=Verse, unique=True)
    end = models.ForeignKey(to=Verse, unique=True)


class Book(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True)
    abbreviation = models.CharField(unique=True, max_length=10)  # 10?
    description = models.CharField(max_length=2000)

    start = models.ForeignKey(to=Verse, unique=True)
    end = models.ForeignKey(to=Verse, unique=True)
    start_chapter = models.ForeignKey(to=Chapter, unique=True)
    end_chapter = models.ForeignKey(to=Chapter, unique=True)


class Selection(models.Model):
    user = models.ForeignKey(to=User)
    label = models.CharField(unique=True)
    voice = models.CharField()
    repeat = models.IntegerField()
    version = models.CharField()
    read_label = models.BooleanField(default=False)


class VerseRange(models.Model):
    start = models.ForeignKey(to=Verse)
    end = models.ForeignKey(to=Verse)
    selection = models.ForeignKey(unique=True)


class Hidden(models.Model):
    hidden = models.ForeignKey(to=VerseRange)
    start = models.ForeignKey(to=Verse)
    end = models.ForeignKey(to=Verse)
