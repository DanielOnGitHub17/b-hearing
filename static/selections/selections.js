import { books } from "./books.js";

function make(name = "div", attrs = {}) {
    const dom = document.createElement(name);
    for (const attr in attrs) dom[attr] = attrs[attr];
    return dom;
}

class Verse {
    constructor(book, chapter, verse, number, rangeType, parentElement) {
        for (const prop of arguments) this[prop] = arguments[prop];
        // this.build();
    }

    build() {
        add(this.container = make("span", { className: "verse", obj: this }),
            this.parentElement);
        add(this.input = make("input", { type: "number", name: this.rangeType, hidden: true }),
            this.container);
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
        for (const prop of arguments) this[prop] = arguments[prop];
        this.build();
    }

    build() {
        add(this.container = make("div", { className: "verse-range-spec", obj: this }),
            this.parentElement);

        add(this.verseRangeText = make("p", { className: "verse-range-text" }),
            this.container);
    }
}

class VerseRangeForm {
    constructor(name, parentElement) {
        [this.name, this.parentElement] = arguments;
        this.build();
        VerseRangeForm.forms.push(this);
    }

    build() {
        // It"s funny how the add(what, to) function looks like you"re walking from inside to outside

        // Build elements
        this.container = add(make("fieldset", { id: `${this.name}-verse-form`, className: "verse-form", obj: this }),
            this.parentElement);

        this.legend = add(make("legend", { textContent: `Select ${this.name}ing verse` }),
            this.container);

        add(make("option", { disabled: true, required: true, selected: true, value: "", textContent: "Choose a book from below" }),
            this.book = add(make("select", { required: true }),
                add(make("label", { textContent: "Select Book: " }),
                    this.container
                )
            )
        );

        for (const book in books) add(make("option", { textContent: book }),
            this.book);

        for (const prop of ["chapter", "verse"]) {
            this[prop] = add(make("input", { type: "number", min: 1, required: true }),
                add(make("label", { textContent: `Select ${prop}: ` }),
                    this.container))
        }
    }

    static forms = [];
    static event(e) {
        const dom = e.target;
        let verseRange;
        switch (dom.localName) {
            case "select":
                verseRange = dom.parentElement.parentElement.obj;
                verseRange.chapter.max = books[dom.value].length - 1;
                break;

            case "input":
                if (dom.type !== "number") return;
                verseRange = dom.parentElement.parentElement.obj;
                if (!verseRange.book.value) {
                    verseRange.chapter.value = verseRange.verse.value = 0;
                    break;
                }

                if (verseRange.chapter === dom) verseRange.verse.max = books[verseRange.book.value][+dom.value]
                break;

            default:
                break;
        }
    }
}


export { VerseRangeForm };