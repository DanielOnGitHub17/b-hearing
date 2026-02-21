"""
Docstring for selection.populate_verses
"""

import json
from importlib import reload

from .models import Book, Chapter, Verse

# Note: \b-hearing\bible-data\corpus\eng-engkjv.txt for kjv
# kjv verses = 31170

# Get chapter endings of all bible chapters. Then split the text and create database rows as needed.

books = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Songs of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corintians",
    "2 Corintians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]


def process_pg_json():
    """
    kjv: 31,102
    Used this to get the json after deleting some element nodes
    JSON.stringify($$(".chapter").map(
    i=>[...i.getElementsByTagName("p")].map(
    j=>j.textContent.trim().replaceAll('\n',' '))))
    "5:6 And Seth lived an hundred and five years, and begat Enos: 5:7 And Seth lived after he begat Enos eight hundred and seven years, and begat sons and daughters: 5:8 And all the days of Seth were nine hundred and twelve years: and he died.",
    note how verses are spread accross. take note of that to make more verses.
    Regex?
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
    with open(r"..\b-hearing\bible-data\kjv.json") as bible_file:
        data = json.load(bible_file)
        bible = []
        for book in data:
            bible.append([])
            chapter_no = 0
            for verse in book:
                first_space = verse.find(" ")
                ch_v = verse[:first_space].split(":")
                if not all(map(str.isdecimal, ch_v)):
                    continue

                new_chapter_no = int(ch_v[0])
                if chapter_no != new_chapter_no:
                    bible[-1].append([])
                    chapter_no = new_chapter_no

                bible[-1][-1].append(verse[first_space + 1 :])

    with open(r"..\b-hearing\bible-data\kjv_curated.json", "w") as bible_file:
        print(len(bible), len(bible[0]))
        json.dump(bible, bible_file)


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
            ).save()
            chapter_no += 1

        Book(
            number=book_no,
            name=books[book_no],
            start=Verse.objects.get(number=start_book_verse),
            end=verse_obj,
            start_chapter=Chapter.objects.get(number=start_chapter),
            end_chapter=chapter_obj,
        ).save()

    print(book_no, chapter_no, verse_no)


if __name__ == "__main__":
    # process_pg_json()
    init_bible_db("kjv", r"C:\Users\enesi\Code\b-hearing\bible-data\kjv_curated.json")
