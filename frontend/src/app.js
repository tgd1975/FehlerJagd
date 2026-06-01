// App-Controller: Profile, Navigation, Belohnungen, View-Dispatch.

import { api } from "./api.js";
import { mount, setStatus, el } from "./ui.js";
import { renderProfiles } from "./views/profiles.js";
import { renderCases } from "./views/cases.js";
import { renderVorlesen } from "./views/vorlesen.js";
import { renderFehlerjagd } from "./views/fehlerjagd.js";
import { renderAvatar } from "./views/avatar.js";
import { renderDashboard } from "./views/dashboard.js";

const ctx = { profile: null, profileId: null, allGreen: false };

function updateChips() {
  const chip = document.getElementById("status-chip");
  chip.hidden = false;
  chip.classList.toggle("warn", !ctx.calibrated);
  chip.textContent =
    (ctx.profile ? `${ctx.profile.name} · ${ctx.profile.points}P · ` : "") +
    (ctx.calibrated ? "Scoring aktiv" : "Scoring: Stub");
}

const go = {
  profiles: () => renderProfiles(go),
  pickProfile: (p) => {
    ctx.profile = p; ctx.profileId = p.id;
    localStorage.setItem("fj_profile", String(p.id));
    updateChips();
    go.cases();
  },
  cases: () => renderCases(go),
  avatar: () => renderAvatar(go, ctx),
  dashboard: () => renderDashboard(go, ctx),

  scene: async (caseId, sceneId) => {
    const scene = await api.getScene(caseId, sceneId);
    if (ctx.profileId) {
      api.saveProgress({ profile_id: ctx.profileId, case_id: caseId,
        current_scene: sceneId }).catch(() => {});
    }
    renderScene(scene);
  },

  advance: async (scene, choiceIndex, allGreen) => {
    ctx.allGreen = !!allGreen;
    // Szene abgeschlossen → Punkte + Pinnwand-Panel.
    if (ctx.profileId) {
      try {
        const r = await api.rewardScene({
          profile_id: ctx.profileId, case_id: scene.case_id,
          scene_id: scene.scene_id, all_green: !!allGreen,
        });
        if (ctx.profile) { ctx.profile.points = r.points; updateChips(); }
      } catch {}
    }
    const res = await api.next({
      case_id: scene.case_id, scene_id: scene.scene_id,
      choice_index: choiceIndex, all_green: !!allGreen,
    });
    if (res.scene) {
      if (ctx.profileId) {
        api.saveProgress({ profile_id: ctx.profileId, case_id: res.scene.case_id,
          current_scene: res.scene.scene_id }).catch(() => {});
      }
      renderScene(res.scene);
    } else {
      mount(el("div", { class: "scene" }, [
        el("h2", {}, res.skipped_bonus ? "Fall gelöst! 🔎" : "Fall abgeschlossen 🎉"),
        el("p", {}, res.skipped_bonus
          ? "Die Bonus-Szene gibt es beim nächsten Mal mit durchgehend grünem Lesen."
          : "Gut gemacht, Spürnase!"),
        el("div", { class: "row" }, [
          el("button", { class: "btn", onClick: () => go.cases() }, "Zur Fallauswahl"),
          el("button", { class: "btn ghost", onClick: () => go.avatar() }, "Ausrüstung"),
        ]),
      ]));
    }
  },
};

function renderScene(scene) {
  if (scene.mode === "fehlerjagd") renderFehlerjagd(scene, go, ctx);
  else renderVorlesen(scene, go, ctx);
}

async function boot() {
  let health;
  try {
    health = await api.health();
  } catch (err) {
    mount(el("div", { class: "banner" },
      `Backend nicht erreichbar (${err.message}). Starte das Backend und lade neu, ` +
      `oder gib die API-URL via ?api=http://… an.`));
    return;
  }
  ctx.calibrated = !!health.scoring_calibrated;
  updateChips();

  // Profil aus localStorage wiederherstellen, sonst Auswahl zeigen.
  const savedId = Number(localStorage.getItem("fj_profile"));
  if (savedId) {
    const profiles = await api.listProfiles().catch(() => []);
    const found = profiles.find((p) => p.id === savedId);
    if (found) { go.pickProfile(found); return; }
  }
  go.profiles();
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

boot();
export { go, ctx };
