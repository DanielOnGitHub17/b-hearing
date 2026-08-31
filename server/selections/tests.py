from typing import Any, cast

from django.test import TestCase

from users.models import User
from .models import Book, Selection, Verse, VerseRange
from .serializers import SelectionDetailSerializer


class TestInitDB(TestCase):
    def test_selection_serializer_serializes_verse_ranges(self):
        user = User.objects.create_user(  # type: ignore[attr-defined]
            email="owner@example.com", password="secret"
        )
        book = Book.objects.create(
            number=1, name="Genesis", abbreviation="Gen", description="test"
        )
        start_verse = Verse.objects.create(
            book=book,
            chapter=1,
            verse=1,
            kjv="In the beginning.",
            gnb="In the beginning.",
        )
        end_verse = Verse.objects.create(
            book=book,
            chapter=1,
            verse=2,
            kjv="And then.",
            gnb="And then.",
        )
        selection = Selection.objects.create(
            owner=user,
            label="Test selection",
            browser_voice="default",
            repeat=1,
            version="kjv",
        )
        VerseRange.objects.create(
            selection=selection,
            start_verse=start_verse,
            end_verse=end_verse,
        )

        serializer = SelectionDetailSerializer(selection)
        data = cast(dict[str, Any], serializer.data)
        verse_ranges = cast(list[dict[str, Any]], data["verse_ranges"])
        verse_range = verse_ranges[0]

        self.assertEqual(data["label"], "Test selection")
        self.assertEqual(len(verse_ranges), 1)
        self.assertEqual(verse_range["start_verse"], int(start_verse.pk))
        self.assertEqual(verse_range["end_verse"], int(end_verse.pk))
