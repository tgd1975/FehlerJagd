// Service Worker – cacht nur die App-Shell (same-origin). API-Aufrufe ans
// Backend laufen immer übers Netz (kein Caching von Scores/Inhalten hier).

const CACHE = "fehlerjagd-shell-v2";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon.svg",
  "./src/styles.css",
  "./src/app.js",
  "./src/api.js",
  "./src/ui.js",
  "./src/speak.js",
  "./src/views/cases.js",
  "./src/views/vorlesen.js",
  "./src/views/fehlerjagd.js",
  "./src/views/profiles.js",
  "./src/views/avatar.js",
  "./src/views/dashboard.js",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // Nur same-origin GET aus der Shell bedienen; alles andere (API) direkt.
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  e.respondWith(
    caches.match(e.request).then((hit) => hit || fetch(e.request))
  );
});
