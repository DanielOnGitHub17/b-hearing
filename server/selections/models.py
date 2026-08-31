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


class AudioSource(models.Model):
    """
    https://openbible.com/audio/kjv/KJV_01_Gen_001.mp3 - check and see how to format well
    https://www.wordpocket.org/bibles/app/audio/1/43/14.mp3
    Example url_template
    url_template = "https://somebiblesite.org/audio/moreslug/%(book_name_abbr)s/%(book_no)s/%(chapter_no)s.<ext>"

    For example:
    for the first url it should be
    https::/openbible.com/audio/kjv/KJV_%(book_no)s_%(book_name_abbr)_%(chapter_no)s.mp3
    For the second it would be
    https://www.wordpocket.org/bibles/app/audio/1/%(book_no)s/%(chapter_no)s.mp3
    """

    url_template = models.CharField()
    name = models.CharField(default="")
    default_offset = models.IntegerField(default=0)
    version = models.CharField(default="King James Version")
    version_abbr = models.CharField(default="KJV")

    def form_url(
        self, book_no: str | int, chapter_no: str | int, book_name_abbr: str
    ) -> str:
        return self.url_template % {
            "book_name_abbr": book_name_abbr,
            "book_no": book_no,
            "chapter_no": chapter_no,
        }


class AudioOffset(models.Model):
    source = models.ForeignKey(
        to=AudioSource, on_delete=models.CASCADE, related_name="audio_offsets"
    )
    verse = models.ForeignKey(
        to=Verse, on_delete=models.PROTECT, related_name="audio_offsets"
    )


"""
The API will map to these 
- AudioSourceSuggestion
- AudioOffsetSuggestion

So people can suggest where the verse starts in the audio
Then later on I can take averages, notice outliers, then push an update that is consistent
"""


class AudioSourceSuggestion(AudioSource):
    pass


class AudioOffsetSuggestion(AudioOffset):
    pass


class Selection(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="selections"
    )
    audio_source = models.ForeignKey(
        to=AudioSource, on_delete=models.PROTECT, default=None
    )
    label = models.CharField(unique=True)
    browser_voice = models.CharField(default="default")
    repeat = models.IntegerField()
    version = models.CharField()
    read_label = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


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
    position = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk and not self.position:
            last_position = VerseRange.objects.filter(selection=self.selection).count()
            self.position = last_position + 1
        super().save(*args, **kwargs)


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
