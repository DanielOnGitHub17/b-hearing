class Verse {
    constructor(verseObj, parentElement) {
        for (const prop in verseObj) this[prop] = verseObj[prop];
        this.parentElement = parentElement;
        this.build();
        Verse.verses.push(this);
    }

    build() {
        this.container = add(make("p", { className: "verse-holder" }), this.parentElement);
        for (const prop of Verse.props) {
            this[`${prop}Holder`] =
                add(make("span", { textContent: this[prop], className: prop }), this.container);
        }
    }

    static props = ["book", "chapter", "verse", "text"]
    static verses = [];
}

export { Verse };