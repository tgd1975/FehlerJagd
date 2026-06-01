// Profil-Auswahl / -Anlage.

import { api } from "../api.js";
import { el, mount } from "../ui.js";

export async function renderProfiles(go) {
  const profiles = await api.listProfiles();

  const list = profiles.map((p) =>
    el("button", { class: "case-card", onClick: () => go.pickProfile(p) }, [
      el("h3", {}, p.name),
      el("div", { class: "place" }, `${p.points} Punkte`),
    ]));

  const nameInput = el("input", { type: "text", placeholder: "Name", class: "name-input" });
  const createBtn = el("button", { class: "btn" }, "Neues Profil");
  createBtn.addEventListener("click", async () => {
    const name = nameInput.value.trim();
    if (!name) return;
    const p = await api.createProfile(name);
    go.pickProfile(p);
  });

  mount(
    el("h2", {}, "Wer ermittelt heute?"),
    el("div", { class: "grid" }, list),
    el("div", { class: "row" }, [nameInput, createBtn]),
  );
}
