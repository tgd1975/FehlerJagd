// Belohnungen: Detektiv-Avatar ausstatten (Punkte → Items).

import { api } from "../api.js";
import { el, mount } from "../ui.js";

export async function renderAvatar(go, ctx) {
  if (!ctx.profileId) return go.profiles();
  const items = await api.catalog(ctx.profileId);

  const cards = items.map((it) => {
    const btn = el("button", {
      class: "btn" + (it.equipped ? "" : " ghost"),
      disabled: !it.affordable && !it.equipped,
      onClick: async () => {
        await api.equip({ profile_id: ctx.profileId, item_key: it.item_key });
        renderAvatar(go, ctx);
      },
    }, it.equipped ? "angelegt ✓" : (it.affordable ? "anlegen" : `${it.cost} Punkte`));
    return el("div", { class: "case-card" }, [
      el("h3", {}, it.name),
      el("div", { class: "place" }, `${it.cost} Punkte`),
      el("div", { class: "row" }, [btn]),
    ]);
  });

  mount(
    el("h2", {}, "Detektiv-Ausrüstung"),
    el("p", { class: "place" }, "Schalte mit gesammelten Punkten deine Ausrüstung frei."),
    el("div", { class: "grid" }, cards),
    el("div", { class: "row" }, [
      el("button", { class: "btn ghost", onClick: () => go.cases() }, "← Zu den Fällen"),
    ]),
  );
}
