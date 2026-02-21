import { VerseRangeForm } from "./selections.js";

const addVerseRange = get("add-verse-range");
const verseRangeForms = get("verse-range-forms")
const verseRanges = get("verse-ranges")

// Use a field set
// check that verse range doesn't start AND end from the same place
// Maybe also indicate that a particular start or end has already been selected for this particular verse
// User might want
// For elsewhere: Selections should be editted the same way they are created.
// The form will look the same.
// Add validation for chapter based on Book and verse based on chapter.
function buildUI() {
    makeVerseRangeForms();
}

function makeVerseRangeForms() {
    for (let prop of ["start", "end"]) {
        new VerseRangeForm(prop, verseRangeForms);
    }
}

configureEvents({
    "load": [buildUI],
    "change": [VerseRangeForm.event]
});

// build it twice for one and other