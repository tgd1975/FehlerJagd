# Backend (FastAPI)

Noch nicht implementiert — geplante Verantwortlichkeiten (siehe `../docs/Konzept.md`, Abschnitt 6):

- **Profile / User** (`/profiles`)
- **Story-Loader** — lädt Fälle aus `../stories/*/graph.yaml` + Szenen-Markdown
- **Scoring (lokal, torchaudio):**
  - `/score/fluency` — Nähe zum *richtigen* Wort (Vorlesen, grün/gelb/rot)
  - `/score/literal` — Distanz zum richtigen Wort (lautgetreue Fehlerprüfung; **nicht** per ASR-Transkription!)
  - `/proofread/check` — deterministischer Abgleich der markierten Fehler (kein ML)
- **Fortschritt / Punkte / Belohnungen** (SQLite)

Provider (Scoring, LLM-Autoren-Tool, TTS) über Config (`.env` / YAML) austauschbar: `local | azure | speechace`.

Setup (später):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
