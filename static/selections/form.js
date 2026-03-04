import { make } from "../util.js";
import { Verse, VerseRange, VerseRangeForm } from "./selections.js";

const addVerseRange = get("add-verse-range");
const verseRangeForms = get("verse-range-forms");
const verseRanges = get("verse-ranges");
const rangeTypes = ["start", "end"];

// Use a field set
// check that verse range doesn't start AND end from the same place
// Maybe also indicate that a particular start or end has already been selected for this particular verse
// User might want
// For elsewhere: Selections should be editted the same way they are created.
// The form will look the same.
// Add validation for chapter based on Book and verse based on chapter.
function buildUI(e) {
    // make verse range forms
    for (let rangeType of rangeTypes) {
        new VerseRangeForm(rangeType, verseRangeForms);
    }

    // add button to create verse range
    add(make("button", { id: "create-verse-range", textContent: '+', type: "button" }), verseRangeForms);
    speechSynthesis.getVoices();  // Warm up
}

function setVoices(e) {
    if (e.target.id !== "voices") return;
    e.stopPropagation();
    const voices = get("voices");
    if (voices.options.length) return; // has options set
    const voiceObjs = speechSynthesis.getVoices().filter(voice => voice.lang === "en-US").map(voice => voice.voiceURI);
    // if (!voiceObjs.length) setTimeout(() => setVoices(e), 500);  // Run again to add voices
    for (const voiceURI of voiceObjs) {
        voices.options.add(make("option", { textContent: voiceURI }));
    }
}

function testVoice(e) {
    if (e.target.id !== "voices") return;
    const voices = get("voices");
    const voice = speechSynthesis.getVoices().filter(voice => voice.voiceURI === voices.value)[0];
    const utterance = new SpeechSynthesisUtterance(voice.voiceURI);
    utterance.voice = voice;
    speechSynthesis.speak(utterance);

}

function createVerseRange(e) {
    if (e.target.id !== "create-verse-range") return;
    e.preventDefault();

    // wrap in try--catch and update <p.errors>
    const verses = [];
    for (let i = 0; i < rangeTypes.length; i++) {
        verses.push(new Verse(...VerseRangeForm.forms[i].verseQuery, rangeTypes[i]));
    }
    new VerseRange(...verses, verseRanges);
}

configureEvents({
    "change": [VerseRangeForm.event, testVoice],
    "click": [createVerseRange, setVoices],
    "load": [buildUI],
});

// build it twice for one and other
