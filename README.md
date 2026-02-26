# B Hearing
### Read slices of Bible, Repeat, Trim, ETC

##### Scheme could be extended for other applications
##### Bible text gotten from: [BibleNLP/eBible](https://github.com/BibleNLP/ebible/tree/main/corpus)

##### Using https://www.gutenberg.org/ebooks/10 KJV from Project Gutenberg

### Notes.
- The bible omits some chapters. It'll be a bit difficult to parse directly

- Found that the ebook is not complete. missing ~22 verses...
- If I find more complete text, I might have to redo everything: JSONs, DB creation, etc.

- Restarted db logic. have better one now
```In [11]: print(time.time()); p.reload(p).init_bible_verses(r"C:\Users\enesi\Code\b-hearing\bible-data\kjv_curated.json"); print(time.time());
1772080225.3040729
1772080405.0799894

In [12]: 1772080405.0799894-1772080225.3040729
Out[12]: 179.7759165763855
```
- 3 minutes. wow. I feel like previous one was faster, but we move.