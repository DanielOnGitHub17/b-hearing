function speak(text, voice) {
    const whatToSay = new SpeechSynthesisUtterance(text);
    whatToSay.voice = voice || speak.voice;
    speechSynthesis.speak(whatToSay);
    speak.voice = voice;
}

export { speak };