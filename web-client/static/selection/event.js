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

function editSelectionDetails(e) {
    const dom = e.target;
    if (dom.id != "edit-selection-details") return;
    e.preventDefault();

}

function handleControls(e) {
    const button = e.target;
    if (button.localName == "button" &&
        button.parentElement.id != "edit-selection-details" &&
        !button.disabled) return;

    button.disabled = true;
    switch (button.id) {
        case "restart":

            break;

        case "play-pause":

            break;

        case "stop":

            break;

        default:
            break;
    }
}

configureEvents({
    "load": [buildUI],
    "submit": [editSelectionDetails],
    "click": [handleControls],
    "change": [],
})

