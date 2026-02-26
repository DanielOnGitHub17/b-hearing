import { make } from "../util.js";
import { books } from "./consts.js";

class Verse {
    constructor(book, chapter, verse, rangeType) {
        [this.book, this.chapter, this.verse, this.rangeType] = [book, chapter, verse, rangeType];
    }

    build(parent) {
        this.container = add(make("span", { className: `verse ${this.rangeType}`, obj: this }), parent);
        this.write();

        for (const prop of ["book", "chapter", "verse"]) {
            add(make("input", { name: `${this.rangeType}_${prop}`, hidden: true, value: this[prop] }), this.container);
        }

    }

    write(book, chapter, verse) {
        this.container.textContent = `${this.book = book ?? this.book}
            ${this.chapter = chapter ?? this.chapter}:${this.verse = verse ?? this.verse}`;
    }
}


class VerseRange {
    constructor(start, end, parentElement) {
        [this.start, this.end, this.parentElement] = [start, end, parentElement]
        this.build();
        VerseRange.ranges.push(this)
    }

    build() {
        this.container = add(make("div", { className: "verse-range-spec", obj: this }), this.parentElement);
        this.verseRangeText = add(make("p", { className: "verse-range-text" }), this.container);
        for (const verse of [this.start, this.end]) verse.build(this.verseRangeText);
    }

    static ranges = [];
}


class VerseRangeForm {
    constructor(name, parentElement) {
        [this.name, this.parentElement] = [name, parentElement];
        this.build();
        VerseRangeForm.forms.push(this);
    }

    get verseQuery() {
        if (!this.book.value) return;
        // do checks and throw error if not valid
        return [this.book.value, this.chapter.value, this.verse.value];

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
                verseRange.chapter.max = Object.keys(books[dom.value]).length - 1;
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


export { Verse, VerseRange, VerseRangeForm };
