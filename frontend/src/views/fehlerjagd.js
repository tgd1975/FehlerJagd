// Fehlerjagd-Screen (Mechanik B): Fälscher-Notiz, Wörter UND Lücken markieren.
// Markieren nutzt eine eigene Affordanz (Einkringeln) – NICHT die Ampelfarben.

import { api } from "../api.js";
import { el, mount } from "../ui.js";
import { speak } from "../speak.js";

export function renderFehlerjagd(scene, go, ctx) {
  const markedWords = new Set();
  const markedGaps = new Set();      // Index des Worts VOR der Lücke
  const tokens = scene.tokens || [];
  const text = scene.text;

  const noteBox = el("div", { class: "note scene-text" });

  function buildNote() {
    noteBox.replaceChildren();
    if (tokens.length === 0) { noteBox.append(text); return; }
    // Text vor dem ersten Token.
    noteBox.append(text.slice(0, tokens[0].start));
    tokens.forEach((tok, i) => {
      const span = el("span", { class: "tok" + (markedWords.has(tok.index) ? " marked" : "") },
        tok.text);
      span.addEventListener("click", () => {
        markedWords.has(tok.index) ? markedWords.delete(tok.index) : markedWords.add(tok.index);
        buildNote();
      });
      noteBox.append(span);
      // Zwischenraum bis zum nächsten Token als anklickbare Lücke.
      const nextStart = i + 1 < tokens.length ? tokens[i + 1].start : tok.end;
      const between = text.slice(tok.end, nextStart);
      if (i + 1 < tokens.length) {
        const gap = el("span", { class: "gap" + (markedGaps.has(tok.index) ? " marked" : ""),
          title: "Beistrich-Lücke" }, between || " ");
        gap.addEventListener("click", () => {
          markedGaps.has(tok.index) ? markedGaps.delete(tok.index) : markedGaps.add(tok.index);
          buildNote();
        });
        noteBox.append(gap);
      } else {
        noteBox.append(between);
      }
    });
    noteBox.append(text.slice(tokens[tokens.length - 1].end));
  }
  buildNote();

  const result = el("div", {});
  const submitBtn = el("button", { class: "btn" }, "Fehler prüfen");

  submitBtn.addEventListener("click", async () => {
    submitBtn.disabled = true;
    try {
      const res = await api.proofread({
        case_id: scene.case_id, scene_id: scene.scene_id,
        marked_indices: [...markedWords], marked_gap_indices: [...markedGaps],
        profile_id: ctx.profileId ?? null,
      });
      if (ctx.profileId) {
        api.rewardProofread({ profile_id: ctx.profileId,
          found_count: res.found_count, total: res.total })
          .then((r) => { if (ctx.profile) ctx.profile.points = r.points; })
          .catch(() => {});
      }
      renderResult(res);
    } catch (err) {
      result.replaceChildren(el("p", {}, "Fehler: " + err.message));
      submitBtn.disabled = false;
    }
  });

  function renderResult(res) {
    const items = res.outcomes.map((o) => {
      const correct = el("strong", { class: "speakable", title: "Antippen zum Anhören" }, o.correct);
      correct.addEventListener("click", () => speak(o.correct));
      return el("div", { class: "outcome " + (o.found ? "found" : "missed") }, [
        el("div", {}, `${o.found ? "✓ gefunden" : "✗ übersehen"}: „${o.shown}" → `),
        correct,
        el("div", { class: "regel" },
          (o.regel && o.regel !== "–" ? `Regel ${o.regel}: ` : "") + o.tipp),
      ]);
    });
    result.replaceChildren(
      el("h3", {}, `${res.found_count} von ${res.total} Fehlern gefunden`),
      ...(res.false_positives
        ? [el("p", { class: "regel" }, `${res.false_positives} Markierung(en) zu viel.`)] : []),
      ...items,
      el("div", { class: "row" },
        [el("button", { class: "btn", onClick: () => go.advance(scene, null, ctx.allGreen) },
          "Weiter →")]),
    );
    submitBtn.disabled = true;
  }

  mount(
    el("div", { class: "scene" }, [
      el("div", { class: "mode-badge" }, "Fehlerjagd – Fälscher-Notiz"),
      el("p", {}, "Der Fälscher hat sich verraten! Tippe die falsch geschriebenen Wörter an – bei fehlenden Beistrichen die Lücke zwischen zwei Wörtern."),
      noteBox,
      el("div", { class: "row" }, [submitBtn]),
      result,
    ]),
  );
}
