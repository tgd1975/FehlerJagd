// Eltern-Dashboard: welche Regel-Kategorien werden übersehen? + Lese-Überblick.

import { api } from "../api.js";
import { el, mount } from "../ui.js";

export async function renderDashboard(go, ctx) {
  if (!ctx.profileId) return go.profiles();
  const d = await api.dashboard(ctx.profileId);

  const prRows = d.proofread_by_klasse.map((s) =>
    el("tr", {}, [
      el("td", {}, s.klasse),
      el("td", {}, s.regel === "–" ? "–" : "Regel " + s.regel),
      el("td", {}, `${s.found}/${s.total}`),
      el("td", {}, Math.round(s.found_ratio * 100) + " %"),
    ]));

  const flRows = d.fluency_by_scene.map((s) =>
    el("tr", {}, [
      el("td", {}, `${s.case_id} · ${s.scene_id}`),
      el("td", {}, `${s.green}/${s.yellow}/${s.red}`),
      el("td", {}, s.avg_score == null ? "—" : Math.round(s.avg_score * 100) + " %"),
    ]));

  mount(
    el("h2", {}, "Eltern-Dashboard"),
    ...(d.most_missed.length
      ? [el("div", { class: "banner" },
          "Oft übersehen: " + d.most_missed.join(", "))]
      : []),
    el("h3", {}, "Fehlerjagd nach Regel-Kategorie"),
    d.proofread_by_klasse.length
      ? el("table", { class: "dash" }, [
          el("tr", {}, [el("th", {}, "Klasse"), el("th", {}, "Regel"),
                        el("th", {}, "gefunden"), el("th", {}, "Quote")]),
          ...prRows,
        ])
      : el("p", { class: "place" }, "Noch keine Fehlerjagd-Daten."),
    el("h3", {}, "Vorlesen je Szene (grün/gelb/rot)"),
    d.fluency_by_scene.length
      ? el("table", { class: "dash" }, [
          el("tr", {}, [el("th", {}, "Szene"), el("th", {}, "g/g/r"),
                        el("th", {}, "Ø Score")]),
          ...flRows,
        ])
      : el("p", { class: "place" }, "Noch keine Vorlese-Daten (Scoring evtl. inaktiv)."),
    el("div", { class: "row" }, [
      el("button", { class: "btn ghost", onClick: () => go.cases() }, "← Zu den Fällen"),
    ]),
  );
}
