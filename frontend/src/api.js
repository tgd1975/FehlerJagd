// API-Client für das FehlerJagd-Backend.
// Basis-URL konfigurierbar via ?api=… (in localStorage gemerkt) oder Default.

const DEFAULT_BASE = "http://localhost:8000";

function resolveBase() {
  const fromQuery = new URLSearchParams(location.search).get("api");
  if (fromQuery) localStorage.setItem("fj_api", fromQuery);
  return localStorage.getItem("fj_api") || DEFAULT_BASE;
}

export const API_BASE = resolveBase();

async function jsonFetch(path, options = {}) {
  const res = await fetch(API_BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export const api = {
  health: () => jsonFetch("/health"),
  listCases: () => jsonFetch("/cases"),
  getScene: (caseId, sceneId) =>
    jsonFetch(`/cases/${caseId}/scene/${sceneId}`),
  next: (body) =>
    jsonFetch("/scene/next", { method: "POST", body: JSON.stringify(body) }),
  proofread: (body) =>
    jsonFetch("/proofread/check", { method: "POST", body: JSON.stringify(body) }),

  // Flüssigkeit: Audio als multipart (optional – Stub ignoriert es).
  async scoreFluency({ expectedText, caseId, sceneId, profileId, audioBlob }) {
    const fd = new FormData();
    fd.append("expected_text", expectedText);
    if (caseId) fd.append("case_id", caseId);
    if (sceneId) fd.append("scene_id", sceneId);
    if (profileId != null) fd.append("profile_id", String(profileId));
    if (audioBlob) fd.append("audio", audioBlob, "aufnahme.webm");
    const res = await fetch(API_BASE + "/score/fluency", { method: "POST", body: fd });
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
    return res.json();
  },
};
