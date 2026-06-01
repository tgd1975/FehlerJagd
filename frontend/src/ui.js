// Kleine DOM-Helfer (kein Framework).

export function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function")
      node.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v === true) node.setAttribute(k, "");
    else if (v !== false && v != null) node.setAttribute(k, v);
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    node.append(c.nodeType ? c : document.createTextNode(String(c)));
  }
  return node;
}

export function mount(...nodes) {
  const app = document.getElementById("app");
  app.replaceChildren(...nodes);
}

export function setStatus(text, warn = false) {
  const chip = document.getElementById("status-chip");
  chip.hidden = !text;
  chip.textContent = text || "";
  chip.classList.toggle("warn", warn);
}

export function backLink(label, onClick) {
  return el("a", { class: "back", onClick }, label);
}
