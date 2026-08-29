import { VerseRangeForm } from "./selections.js";

function populate() {
    const data = [
        [{ book: "Genesis", chapter: 1, verse: 1 }, { book: "Genesis", chapter: 3, verse: 8 }],
        [{ book: "John", chapter: 2, verse: 2 }, { book: "John", chapter: 3, verse: 9 }],
    ];
    for (const input of data) {
        for (let i = 0; i < 2; i++) {
            for (let prop in input[i]) {
                VerseRangeForm.forms[i][prop].value = input[i][prop];
            }
        }
        get("create-verse-range").click();
    }
}

export { populate };