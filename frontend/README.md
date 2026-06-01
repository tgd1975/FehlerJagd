# Frontend (PWA)

Schlanke, **build-freie** Progressive Web App (ES-Module, kein Framework, keine
Abhängigkeiten). Spricht das FastAPI-Backend an und setzt die zwei Mechaniken um:
**Vorlesen** (Aufnahme + Wort-Einfärbung) und **Fehlerjagd** (Fälscher-Notiz mit
Markier- und Beistrich-Lückenmodus). Design nach `../docs/Konzept.md` §5.

## Starten

Irgendein Static-Server genügt (Service Worker braucht http, nicht `file://`):

```bash
cd frontend
python3 -m http.server 5173
# Browser: http://localhost:5173
```

Dazu das Backend starten (siehe `../backend/README.md`). Andere API-URL:
`http://localhost:5173/?api=http://192.168.0.10:8000` (wird in localStorage gemerkt).

## Aufbau

```
frontend/
├── index.html              App-Shell
├── manifest.webmanifest    PWA-Manifest (installierbar, Tablet-tauglich)
├── sw.js                   Service Worker (cacht nur die Shell, nie API/Scores)
├── icons/icon.svg          Lupe-Icon
└── src/
    ├── styles.css          Designsystem: Petrol-UI, Creme-BG, Ampel NUR fürs Vorlesen
    ├── api.js              Backend-Client (fetch)
    ├── ui.js               DOM-Helfer
    ├── app.js              Controller: Health-Check, Navigation, View-Dispatch
    └── views/
        ├── cases.js        Fallauswahl (Akten-Look)
        ├── vorlesen.js     Mechanik A: MediaRecorder, Wort-Ampel, Re-Read
        └── fehlerjagd.js   Mechanik B: Wörter + Lücken markieren, Auflösung
```

## Wichtige Entscheidungen

- **Build-frei statt Vite.** Reine ES-Module laufen ohne `npm install`/Build,
  sind sofort verifizierbar und später ohne Bruch auf Vite hebbar (das Konzept
  nennt „Vite + vanilla JS" – vanilla zuerst).
- **Token-Indizes vom Backend.** Die Fehlerjagd rendert die Notiz aus den
  `tokens` des Szenen-Payloads – dieselben Indizes, die `/proofread/check`
  erwartet. Keine doppelte Tokenisierung, kein Drift.
- **Affordanz-Trennung (Konzept §5).** Ampelfarben (rot/gelb/grün) ausschließlich
  fürs Vorlese-Feedback; Markieren nutzt Einkringeln/Lila – nie die Ampel.
- **Solange `stub` aktiv ist** (vor Phase-0-GO), zeigt die Statuszeile „Scoring:
  Stub" und Wörter erscheinen als „ungeprüft"; der Spielfluss funktioniert
  trotzdem komplett (Navigation, Fehlerjagd, Auflösung).

## Später

PWA installieren (Tablet) · Vite-Build · Belohnungen (Avatar/Pinnwand) ·
Szenen-Reveal-Bilder · Eltern-Dashboard.
