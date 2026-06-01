// Fallauswahl im „Akten"-Look.

import { api } from "../api.js";
import { el, mount } from "../ui.js";

export async function renderCases(go) {
  const cases = await api.listCases();
  const cards = cases.map((c) =>
    el("button", { class: "case-card", onClick: () => go.scene(c.case_id, c.start) }, [
      el("h3", {}, c.titel),
      el("div", { class: "place" }, c.schauplatz || "—"),
      el("div", { class: "tags" },
        (c.ziel_muster || []).map((t) => el("span", { class: "tag" }, t))),
    ])
  );
  mount(
    el("h2", {}, "Wähle einen Fall"),
    el("p", { class: "place" }, "Mia, Ben & Frieda warten auf dich."),
    el("div", { class: "grid" }, cards),
  );
}
