class Verse {
    constructor(verseObj, parentElement) {
        for (const prop in verseObj) {
            this[prop] = verseObj[prop];
        }
        this.parentElement = parentElement;
        this.build();
    }

    build() {
        this.container = add(make("p", { className: "verse-holder" }));
        for (const prop of props) {
            this[`${prop}Holder`] = make("span", { textContent: this[prop], className: prop });
        }
    }

    static props = ["book", "chapter", "verse", "text"]
}