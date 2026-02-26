"""
Docstring for selection.populate_verses
"""

import json
import re
from importlib import reload

from .consts import BOOKS, FULL_TO_ABBR

from .models import Book, Verse

# Note: \b-hearing\bible-data\corpus\eng-engkjv.txt for kjv
# kjv verses = 31170

# Get chapter endings of all bible chapters. Then split the text and create database rows as needed.


SPLIT_VERSE = re.compile("[0-9]+:[0-9]+")


def process_pg_json():
    bible = {}
    verse_counts = {}
    with open(r"..\b-hearing\bible-data\kjv.json") as bible_file:
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

    with open(r"..\b-hearing\bible-data\kjv_curated.json", "w") as bible_file:
        json.dump(bible, bible_file)

    with open(
        r"..\b-hearing\bible-data\kjv_verse_counts.json", "w"
    ) as verse_count_file:
        json.dump(verse_counts, verse_count_file)


def copy_all_verses(src_path, out_path):
    src_path = r"bible-data\\corpus\\eng-engkjvcpb.txt"
    out_path = r"bible-data\\corpus\\eng-engkjv.txt"
    with open(src_path, "rb") as src:
        with open(out_path, "wb") as out:
            for _ in range(31170):
                out.write(src.readline())


def create_books():
    for book in BOOKS:
        Book()


def init_bible_db(version, src_path):
    with open(src_path) as bible_file:
        bible = json.load(bible_file)

    verse_no, chapter_no = 0, 0
    for book_no, book in enumerate(bible):
        start_chapter, start_book_verse = chapter_no, verse_no
        for chapter in book:
            start_verse = verse_no
            for verse in chapter:
                verse_obj = Verse(number=verse_no)
                setattr(verse_obj, version, verse)
                verse_obj.save()
                verse_no += 1

            chapter_obj = Chapter(
                number=chapter_no,
                start=Verse.objects.get(number=start_verse),
                end=verse_obj,
            )
            chapter_obj.save()
            chapter_no += 1

    print(book_no, chapter_no, verse_no)


if __name__ == "__main__":
    process_pg_json()
    # init_bible_db("kjv", r"C:\Users\enesi\Code\b-hearing\bible-data\kjv_curated.json")
    # start 2:58, end = 3:02:53
    # 65 1189 31081 - should be 31102! missing 21
