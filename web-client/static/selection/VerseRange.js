import { Verse } from "./Verse.js";

class VerseRange {
    constructor(verseObjs, parentElement) {
        this.verseObjs = verseObjs;
        this.parentElement = parentElement;
        this.verses = [];
        this.build();
        VerseRange.verseRanges.push(this);
    }

    build() {
        this.container = add(make("section", { className: "verse-range" }), this.parentElement);
        for (const verseObj of this.verseObjs) this.verses.push(new Verse(verseObj, this.container));
    }

    static verseRanges = [];
}

export { VerseRange };