// App-Controller: Health-Check, Navigation, View-Dispatch.

import { api } from "./api.js";
import { mount, setStatus, el } from "./ui.js";
import { renderCases } from "./views/cases.js";
import { renderVorlesen } from "./views/vorlesen.js";
import { renderFehlerjagd } from "./views/fehlerjagd.js";

const ctx = { profileId: null, allGreen: false };

const go = {
  cases: () => renderCases(go),
  scene: async (caseId, sceneId) => {
    const scene = await api.getScene(caseId, sceneId);
    renderScene(scene);
  },
  // Übergang anstoßen (Choice oder linear) und Folge-Szene anzeigen.
  advance: async (scene, choiceIndex, allGreen) => {
    ctx.allGreen = !!allGreen;
    const res = await api.next({
      case_id: scene.case_id, scene_id: scene.scene_id,
      choice_index: choiceIndex, all_green: !!allGreen,
    });
    if (res.scene) {
      renderScene(res.scene);
    } else {
      mount(
        el("div", { class: "scene" }, [
          el("h2", {}, res.skipped_bonus ? "Fall gelöst! 🔎" : "Fall abgeschlossen 🎉"),
          el("p", {}, res.skipped_bonus
            ? "Die Bonus-Szene gibt es beim nächsten Mal mit durchgehend grünem Lesen."
            : "Gut gemacht, Spürnase!"),
          el("button", { class: "btn", onClick: () => go.cases() }, "Zur Fallauswahl"),
        ]),
      );
    }
  },
};

function renderScene(scene) {
  if (scene.mode === "fehlerjagd") renderFehlerjagd(scene, go, ctx);
  else renderVorlesen(scene, go, ctx);  // vorlesen + kalibrierung
}

async function boot() {
  try {
    const health = await api.health();
    if (!health.scoring_calibrated) {
      setStatus("Scoring: Stub (Phase 0 offen)", true);
    } else {
      setStatus("Scoring: " + health.scoring_provider);
    }
  } catch (err) {
    mount(el("div", { class: "banner" },
      `Backend nicht erreichbar (${err.message}). Starte das Backend und lade neu, ` +
      `oder gib die API-URL via ?api=http://… an.`));
    return;
  }
  go.cases();
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

boot();
