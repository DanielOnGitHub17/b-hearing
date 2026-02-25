"""
Docstring for selection.populate_verses
"""

import json
from importlib import reload
import re

from .models import Book, Chapter, Verse
from .consts import BOOKS, FULL_TO_ABBR

# Note: \b-hearing\bible-data\corpus\eng-engkjv.txt for kjv
# kjv verses = 31170

# Get chapter endings of all bible chapters. Then split the text and create database rows as needed.


SPLIT_VERSE = re.compile("[0-9]+:[0-9]+")


def process_pg_json():
    """
    kjv: 31,102
    Used this to get the json after deleting some element nodes
    JSON.stringify($$(".chapter").map(
    i=>[...i.getElementsByTagName("p")].map(
    j=>j.textContent.trim().replaceAll('\n',' '))))
    "5:6 And Seth lived an hundred and five years, and begat Enos: 5:7 And Seth lived after he begat Enos eight hundred and seven years, and begat sons and daughters: 5:8 And all the days of Seth were nine hundred and twelve years: and he died.",
    note how verses are spread accross. take note of that to make more verses.
    Output:
    [
        [ # book
            ["verse"], # chapters
        ],
        [
            [],
        ],
    ]
    """
    bible = []
    verse_counts = {}
    with open(r"..\b-hearing\bible-data\kjv.json") as bible_file:
        data = json.load(bible_file)

    for book_index, book in enumerate(data):
        bible.append([])
        verse_counts[BOOKS[book_index]] = []
        chapter_no = 0
        verse_no = 0
        for verse in book:
            first_space = verse.find(" ")
            ch_v = verse[:first_space].split(":")
            if not all(map(str.isdecimal, ch_v)):
                continue

            for ch_v, verse in zip(
                re.findall(SPLIT_VERSE, verse), re.split(SPLIT_VERSE, verse)[1:]
            ):
                new_chapter_no, new_verse_no = [*map(int, ch_v.split(":"))]
                if chapter_no != new_chapter_no:
                    bible[-1].append([])
                    chapter_no = new_chapter_no
                    verse_counts[BOOKS[book_index]].append(verse_no)

                bible[-1][-1].append(verse.strip())
                verse_no = new_verse_no

        verse_counts[BOOKS[book_index]].append(verse_no)

    with open(r"..\b-hearing\bible-data\kjv_curated.json", "w") as bible_file:
        print(len(bible), len(bible[0]))
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

        Book(
            number=book_no,
            name=BOOKS[book_no],
            abbreviation=FULL_TO_ABBR[BOOKS[book_no]],
            start=Verse.objects.get(number=start_book_verse),
            end=verse_obj,
            start_chapter=Chapter.objects.get(number=start_chapter),
            end_chapter=chapter_obj,
        ).save()

    print(book_no, chapter_no, verse_no)


if __name__ == "__main__":
    process_pg_json()
    # init_bible_db("kjv", r"C:\Users\enesi\Code\b-hearing\bible-data\kjv_curated.json")
    # start 2:58, end = 3:02:53
    # 65 1189 31081 - should be 31102! missing 21
