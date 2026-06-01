// Vorlese-Screen (Mechanik A): laut lesen, Aufnahme, Wort-Einfärbung.

import { api } from "../api.js";
import { el, mount } from "../ui.js";

const COLOR_CLASS = { "grün": "green", "gelb": "yellow", "rot": "red", "ungeprüft": "unrated" };

export function renderVorlesen(scene, go, ctx) {
  let recorder = null;
  let chunks = [];
  let allGreen = false;

  const status = el("span", { class: "mic-status" }, "bereit");
  const wordsBox = el("p", { class: "scene-text read-words" },
    scene.text.split(/\s+/).filter(Boolean).map((w) => el("span", { class: "w unrated" }, w + " ")));

  const recordBtn = el("button", { class: "btn" }, "🎙️ Vorlesen");
  const nav = el("div", { class: "choices" });

  function paint(result) {
    const colored = result.words;
    const spans = scene.text.split(/\s+/).filter(Boolean).map((w, i) => {
      const cls = COLOR_CLASS[colored[i]?.color] || "unrated";
      return el("span", { class: "w " + cls }, w + " ");
    });
    wordsBox.replaceChildren(...spans);
    allGreen = result.all_green;
    renderNav();
  }

  async function toggleRecord() {
    if (recorder && recorder.state === "recording") {
      recorder.stop();
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recorder = new MediaRecorder(stream);
      chunks = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        status.textContent = "wertet aus…";
        status.classList.remove("recording");
        const blob = new Blob(chunks, { type: "audio/webm" });
        try {
          const result = await api.scoreFluency({
            expectedText: scene.text, caseId: scene.case_id,
            sceneId: scene.scene_id, profileId: ctx.profileId, audioBlob: blob,
          });
          paint(result);
          status.textContent = result.calibrated ? "fertig" : "aufgenommen (Bewertung inaktiv)";
        } catch (err) {
          status.textContent = "Fehler: " + err.message;
        }
        recordBtn.textContent = "🎙️ Nochmal";
      };
      recorder.start();
      status.textContent = "hört zu…";
      status.classList.add("recording");
      recordBtn.textContent = "⏹️ Stopp";
    } catch (err) {
      status.textContent = "kein Mikrofon – du kannst trotzdem weiterlesen";
    }
  }
  recordBtn.addEventListener("click", toggleRecord);

  function renderNav() {
    nav.replaceChildren();
    if (scene.choices.length) {
      scene.choices.forEach((c) =>
        nav.append(el("button", { class: "btn ghost", onClick: () => go.advance(scene, c.index, allGreen) }, c.label)));
    } else if (scene.has_goto || scene.next_case) {
      nav.append(el("button", { class: "btn", onClick: () => go.advance(scene, null, allGreen) }, "Weiter →"));
    } else {
      nav.append(el("p", {}, "🎉 Fall abgeschlossen!"),
        el("button", { class: "btn", onClick: () => go.cases() }, "Zur Fallauswahl"));
    }
  }
  renderNav();

  mount(
    el("div", { class: "scene" }, [
      el("div", { class: "mode-badge" }, scene.scoring === "uebung" ? "Stimm-Eichung / Übung" : "Vorlesen"),
      ...(scene.eich_saetze?.length
        ? [el("p", {}, "Sprich diese Sätze nach:"),
           el("ul", {}, scene.eich_saetze.map((s) => el("li", {}, s)))]
        : []),
      wordsBox,
      el("div", { class: "row" }, [recordBtn, status]),
      nav,
    ]),
  );
}
