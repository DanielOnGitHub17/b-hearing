"""
Docstring for selections.populate_verses
"""

import json
import re
from importlib import reload

from .consts import BOOKS, FULL_TO_ABBR

from .models import Book, Verse

# Note: \b-hearing\bible-data\corpus\eng-engkjv.txt for kjv
# kjv verses = 31170

# Get chapter endings of all bible chapters. Then split the text and create database rows as needed.
# pg = project gutenburg


SPLIT_VERSE = re.compile("[0-9]+:[0-9]+")


def process_pg_json():
    bible = {}
    verse_counts = {}
    with open(r"bible-data\kjv.json") as bible_file:
        data = json.load(bible_file)

    for book_index, book in enumerate(data):
        bible[BOOKS[book_index]], verse_counts[BOOKS[book_index]] = {}, {}
        prev_chapter_no, prev_verse_no = 0, 0
        for verse in book:
            first_space = verse.find(" ")
            ch_v = verse[:first_space].split(":")
            if not all(map(str.isdecimal, ch_v)):
                continue

            for ch_v, verse in zip(
                re.findall(SPLIT_VERSE, verse), re.split(SPLIT_VERSE, verse)[1:]
            ):
                chapter_no, verse_no = [*map(int, ch_v.split(":"))]
                if chapter_no != prev_chapter_no:
                    bible[BOOKS[book_index]][chapter_no] = {}
                    verse_counts[BOOKS[book_index]][prev_chapter_no] = prev_verse_no
                    prev_chapter_no = chapter_no

                bible[BOOKS[book_index]][chapter_no][verse_no] = verse.strip()
                prev_chapter_no, prev_verse_no = chapter_no, verse_no

        verse_counts[BOOKS[book_index]][chapter_no] = verse_no

    with open(r"bible-data\kjv_curated.json", "w") as bible_file:
        json.dump(bible, bible_file)

    with open(r"bible-data\kjv_verse_counts.json", "w") as verse_count_file:
        json.dump(verse_counts, verse_count_file)


def copy_all_verses(src_path, out_path):
    src_path = r"bible-data\\corpus\\eng-engkjvcpb.txt"
    out_path = r"bible-data\\corpus\\eng-engkjv.txt"
    with open(src_path, "rb") as src:
        with open(out_path, "wb") as out:
            for _ in range(31170):
                out.write(src.readline())


def create_books():
    for book_no, book in enumerate(BOOKS, start=1):
        Book(
            number=book_no,
            name=book,
            abbreviation=FULL_TO_ABBR[book],
        ).save()


def init_bible_verses(src_path):
    with open(src_path) as bible_file:
        bible = json.load(bible_file)

    for book, chapters in bible.items():
        for ch_no, verses in chapters.items():
            chapter_no = int(ch_no)
            for verse_no, verse in verses.items():
                Verse(
                    book=Book.objects.get(name=book),
                    chapter=chapter_no,
                    verse=int(verse_no),
                    kjv=verse,
                ).save()


if __name__ == "__main__":
    process_pg_json()
    # init_bible_db("kjv", CURATED_JSON_PATH)
    # start 2:58, end = 3:02:53
    # TIme taken for init_bible_db: 124.3229751586914
