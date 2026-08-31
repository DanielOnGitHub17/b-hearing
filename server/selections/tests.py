from django.test import TestCase

from users.models import User
from .models import Book, Selection, Verse, VerseRange
from .serializers import SelectionSerializer


class TestInitDB(TestCase):
    def test_selection_serializer_serializes_verse_ranges(self):
        user = User.objects.create_user(email="owner@example.com", password="secret")
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

        serializer = SelectionSerializer(selection)
        data = serializer.data

        self.assertEqual(data["label"], "Test selection")
        self.assertEqual(len(data["verse_ranges"]), 1)
        self.assertEqual(data["verse_ranges"][0]["start_verse"], start_verse.id)
        self.assertEqual(data["verse_ranges"][0]["end_verse"], end_verse.id)
