class Verse {
    constructor(book, chapter, verse, number, rangeType, parentElement) {
        for (let prop of args) this[prop] = args[prop];
    }

    build() {
        reclass((add(this.container = make("span"), to = this.parentElement).obj = this).container, "verse");
        add(this.input = make("input"), to = this.container).type = "number";
        this.input.name = this.rangeType;
        this.input.hidden = true;
        this.write();
    }

    write(book, chapter, verse, number) {
        this.container.textContent = `${this.book = book ?? this.book}
            ${this.chapter = chapter ?? this.chapter}:${this.verse = verse ?? this.verse}`;
        this.input.value = number;
    }
}
/* 
           <div class="verse-range-spec">
               <p class="verse-range-text">
                   <span class="verse"><input type="number" name="start" hidden></span>
                   <span class="verse"><input type="number" name="end" hidden></span>
               </p>
               
               
               <button type="button" class="remove-verse-range">-</button>
           </div>*/
class VerseRange {
    constructor(start, end, parentElement) {
        /* start and end are Verses*/
        for (let prop of args) this[prop] = args[prop];
        this.build();
    }

    build() {
        reclass((add(this.container = make(), to = this.parentElement).obj = this).container, "verse-range-spec");
        reclass(add(this.verseRangeText = make(), this.parentElement), "verse-range-text");
    }
}
