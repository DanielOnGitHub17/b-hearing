class Verse {
    constructor(book, chapter, verse, number, rangeType, parentElement) {
        for (let prop of args) this[prop] = args[prop];
        // this
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

class VerseRangeForm {
    constructor(name, parentElement) {
        for (let prop of args) this[prop] = args[prop];
        this.build();
    }

    build() {
        // It's funny how the add(what, to) function looks like you're walking from inside to outside

        // Build elements
        add(this.container = make("fieldset"), to = this.parentElement).id = `${this.name}-verse-form`;

        add(this.legend = make("legend"), to = this.container).legend = `Select ${this.name}ing verse`;

        this.book = add(
            make("select"),
            to = add(make("label"), to = this.container)
        );

        ["chapter", "verse"].forEach(prop => {
            let holder = make("label");
            holder.textContent = `Select ${prop.toUpperCase()}`;
            this[prop] = add(make("input"));
        });

        (this.chapter = add(
            make("input"),
            to = add(make("label"), to = this.container)
        )).type = "number";

        (this.verse = add(
            make("input"),
            to = add(make("label"), to = this.container)
        )).type = "number";
        // Add additional properties.
    }
    static forms = [];
}


