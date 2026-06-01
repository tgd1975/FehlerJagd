# Backend (FastAPI)

Lokale Web-API für FehlerJagd: Story-Engine, deterministische Fehlerjagd und
austauschbares phonetisches Scoring. Siehe `../docs/Konzept.md` Abschnitt 6.

> **GO/NO-GO-unabhängig gebaut.** Das phonetische Scoring steckt hinter einem
> austauschbaren Provider-Interface. Bis zur Phase-0-Freigabe läuft der
> `stub`-Provider (bewertet nicht, markiert die Antwort als `calibrated: false`).
> Nach dem GO: `FJ_SCORING=local` – dann wird die in `phase0/` validierte
> torchaudio-Engine genutzt, ohne dass sich die API ändert.

## Schnellstart

```bash
cd backend
pip install -r requirements.txt          # ohne torch: fastapi sqlmodel pyyaml … reichen für stub
uvicorn app.main:app --reload --port 8000
# API-Doku: http://localhost:8000/docs
```

Tests:

```bash
pip install -r requirements-dev.txt
pytest                                    # 39 Tests, ohne torch, In-Memory-/Temp-DB
```

## Endpunkte

| Methode | Pfad | Zweck |
|---|---|---|
| GET  | `/health` | Status + aktiver Scoring-Provider |
| GET  | `/cases` | alle Fälle (Übersicht) |
| GET  | `/cases/{id}` | ein Fall |
| GET  | `/cases/{id}/scene/{sid}` | Szene (Lösungen ausgeblendet; bei Fehlerjagd inkl. Tokens) |
| POST | `/scene/next` | Navigation (Choices, linear, Bonus-Gate, Fall-Wechsel) |
| POST | `/proofread/check` | **deterministische** Fehlerjagd-Prüfung + Auflösung mit Regel-Bezug |
| POST | `/score/fluency` | Flüssigkeits-Scoring (Mechanik A) + sanftes Gating (`can_continue`, `earned_bonus`) |
| POST | `/score/literal` | lautgetreue Fehlerprüfung (Mechanik B, nur hörbare Fehler) |
| POST | `/tts/word` | Wort-Vorsprechen (pluggable; Default `browser` = Web Speech API) |
| POST/GET/PUT | `/profiles`, `/progress`, `/points` | Persistenz |
| POST/GET | `/rewards/scene-complete`, `/rewards/proofread`, `/rewards/catalog/{id}`, `/avatar/equip` | Punkte, Pinnwand, Avatar |
| GET | `/dashboard/{id}` | Eltern-Dashboard: übersehene Regel-Kategorien + Lese-Überblick |

Zusätzliche Werkzeuge: `python lint_stories.py --coverage` (Validierung + Merkblatt-Abdeckung), CI unter `.github/workflows/ci.yml`.

## Architektur

```
app/
├── main.py            FastAPI-App (CORS, Router, Lifespan: Inhalte laden + DB)
├── config.py          Settings via Env (FJ_SCORING, FJ_DB_URL, Schwellen, CORS)
├── registry.py        einmal geladene Fälle + aktiver Scoring-Provider
├── db.py / models.py  SQLite (SQLModel): profiles, progress, score/proofread_history …
├── schemas.py         Pydantic-Request/Response
├── serialize.py       Domäne → API (versteckt Lösungen, liefert Tokens)
├── story/             Engine: graph (Modell), loader (+Validierung), navigation, regeln
├── proofread/         deterministische Markier-Prüfung (Wörter + Beistrich-Lücken)
├── scoring/           base (Interface) · stub (bis GO) · local_torch (phase0-Engine)
└── routers/           cases · navigation · proofread · scoring · progress
```

## Wichtige Entscheidungen

- **Strenge Inhalts-Validierung beim Laden.** Der Loader prüft jeden Fall gegen
  das Konzept und scheitert laut bei Verstößen: gültige Modi; `proofread_errors`
  **nur** auf `mode: fehlerjagd` (Falschschreibungen nie im Vorlese-Text); jeder
  Fehler regel-/methoden-konsistent (`regeln.py`, Mapping 1–8); alle
  `goto`/`choices`-Ziele und Textdateien existieren. Alle 10 Repo-Fälle bestehen.
- **Beistrich-Lückenmodus** (`method: markieren_luecke`, Klasse `komma`): wird als
  eigener Markier-Kanal behandelt – nicht das Wort, sondern die **Lücke** zwischen
  zwei Wörtern wird markiert (Konzept Abschnitt 2).
- **Lösungen erst nach dem Abschicken.** Szenen-Payloads enthalten nie
  `correct`/`regel`/`tipp`; die Auflösung kommt ausschließlich aus
  `/proofread/check`.
- **Audio wird nie persistiert.** `/score/fluency` schreibt Uploads in eine
  Temp-Datei, bewertet, löscht sie sofort (DSGVO, Konzept-Risiko 6).
- **Scoring delegiert (nach GO) an `phase0/fjp0`** – keine zweite, abweichende
  Scoring-Implementierung.

## Konfiguration (Env)

| Variable | Default | Zweck |
|---|---|---|
| `FJ_SCORING` | `stub` | `stub` \| `local` (azure/speechace folgen) |
| `FJ_STORIES_DIR` | `../stories` | Story-Inhalte |
| `FJ_DB_URL` | `sqlite:///backend/fehlerjagd.db` | SQLite |
| `FJ_GREEN` / `FJ_YELLOW` / `FJ_LITERAL_MAX` | 0.80 / 0.55 / 0.55 | Schwellen (Phase 0 kalibriert) |
| `FJ_CORS` | `http://localhost:5173,…` | erlaubte Frontend-Origins |
