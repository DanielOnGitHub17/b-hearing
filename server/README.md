

TODO: Make more clear

JS that extracts from the https://www.gutenberg.org/ebooks/10 html page

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

AFTER THAT

Then find and replace
",\n *"([a-z .])
with
  $1

on vs code on the connected verses that don't have a label.
There should be 126 of them

The rest are book headers or AKAs

After running populate.py's process_pg_json, you should have a file on vs code kjv_curated.json
It will have 33614 lines

No of books in KJV: 66
No of chapters in KJV: 1189
+ curly braces for json
+ the text

33614 - 66*2 - 1189*2 - 2
31102 - This is the number of verses in the KJV bible.

Then run: to create curated kjv json

```(bash)
python manage.py shell | run -s (windows)
from selections import populate
populate.process_pg_json()
```