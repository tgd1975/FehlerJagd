// Wort-Vorsprechen (Mikro-Lernschleife). Fragt das Backend, wie gesprochen
// werden soll; bei mode 'browser' nutzt es die Web Speech API.

import { api } from "./api.js";

export async function speak(word) {
  try {
    const res = await api.ttsWord(word);
    if (res.mode === "browser" && "speechSynthesis" in window) {
      const u = new SpeechSynthesisUtterance(res.text);
      u.lang = res.lang || "de-AT";
      u.rate = 0.9;
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
    } else if (res.audio_url) {
      new Audio(res.audio_url).play().catch(() => {});
    }
  } catch {
    // Fällt still aus, wenn Backend/TTS nicht verfügbar – kein Blocker.
    if ("speechSynthesis" in window) {
      const u = new SpeechSynthesisUtterance(word);
      u.lang = "de-AT"; u.rate = 0.9;
      speechSynthesis.speak(u);
    }
  }
}
