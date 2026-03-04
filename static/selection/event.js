import { VerseRange } from "./VerseRange.js";
// load voices,
// build versesUI
// Etc.


function buildUI(e) {
    // Add verse ranges, verses.
    const verseRanges = get("verse-ranges");
    const verseRangeObjs = JSON.parse(get("verse-ranges-obj").textContent);
    for (const verseRangeObj of verseRangeObjs) {
        const verseRange = new VerseRange(verseRangeObj, verseRanges);
    }
}

configureEvents({
    "load": [buildUI]
})

