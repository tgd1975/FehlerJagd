# Phase 0 — Kernrisiko absichern (vor allem anderen)

Das ganze Projekt hängt an einer Frage: **Ist die phonetische Bewertung bei der
Stimme deiner Tochter zuverlässig genug?** Diese Phase ist das *De-Risking-
Experiment*, kein Produktionscode — aber sie ist getestet, weil sie das einzige
GO/NO-GO-Werkzeug ist.

> **Wichtige Entscheidungen & Abweichungen vom Konzept:** siehe
> [`DECISIONS.md`](DECISIONS.md). Die größte: echte Kinder-Aufnahmen lassen sich
> hier nicht erzeugen — es gibt darum einen **synthetischen Selbsttest**, der die
> Pipeline beweist, das De-Risking an echter Stimme aber nicht ersetzt.

## Was geprüft wird

1. **Flüssigkeit (Nähe):** Trennen die Wort-Scores „flüssig gelesen" sauber von
   „gestockt"? → legt die grün/gelb/rot-Schwellen fest. **Harte Bedingung.**
2. **Lautgetreue Fehlerprüfung (Distanz, nur hörbare Fehler):** Erkennt die
   akustische **Distanz zum richtigen Wort** zuverlässig, ob eine Falschschreibung
   (z. B. „Tihsc") literal gelesen oder still zu „Tisch" auto-korrigiert wurde?
   → legt fest, welche Fehler *vorlesend* und welche *nur durch Markieren* laufen.
   **Degradierbar** — fällt sie aus, greift überall das Markieren.

Das **Markieren** der Fehler braucht keine Validierung (deterministisch).

## Schnellstart — ohne Installation, ohne Aufnahme

Der Kern läuft mit reiner Python-Stdlib. So beweist du, dass das Harness rechnet:

```bash
cd phase0
python -m fjp0 selftest            # synthetischer End-to-End-GO/NO-GO-Lauf
```

Das erzeugt gelabelte Kunst-Clips, fährt die volle Pipeline und schreibt einen
Report (`data/selftest/report.md` + `.json`). Erwartetes Verdikt: **GO**.

Tests:

```bash
cd phase0
pip install -r requirements-dev.txt
pytest                              # 47 Tests; torch-Smoke-Test wird ohne Modell übersprungen
```

## Echtes GO/NO-GO — mit Aufnahmen deiner Tochter

1. **Aufnehmen:** 5–10 kurze Clips mit dem geplanten Headset, **16 kHz Mono WAV**.
   - ein paar flüssige und ein paar bewusst gestockte Vorlese-Sätze;
   - für die Fehlerprüfung **hörbare** Falschschreibungen (z. B. „Tihsc"/„Tisch"),
     je einmal *literal* gelesen und einmal *normal* (auto-korrigiert).
   - Dateien nach `phase0/data/audio/` legen (per `.gitignore` geschützt).
2. **Manifest füllen:** `manifest.example.csv` nach `data/manifest.csv` kopieren
   und Pfade/Labels eintragen (Format unten).
3. **torch installieren** (echtes akustisches Backend):
   ```bash
   pip install -r requirements.txt   # oder: torch torchaudio --index-url .../whl/cpu
   ```
4. **Auswerten:**
   ```bash
   python -m fjp0 run --manifest data/manifest.csv
   ```
   → Report mit Schwellen, Trennschärfe und **GO / GO-MIT-EINSCHRÄNKUNG / NO-GO**.
5. **Schwellen nachziehen**, bis die Trennung Antonias Stimme abbildet.

Einzelnen Clip schnell anschauen (wie das alte Skript):

```bash
python -m fjp0 score --audio data/audio/satz.wav --text "im regal stehen viele buecher"
python -m fjp0 score --audio data/audio/tisch.wav --text "tisch" --shown Tihsc --correct Tisch
```

## Manifest-Format (CSV)

| Spalte | `vorlesen` | `fehlerjagd` |
|---|---|---|
| `clip`  | WAV-Pfad (relativ zum Manifest) | dito |
| `kind`  | `vorlesen` | `fehlerjagd` |
| `text`  | erwarteter Satz | **richtiges** Wort (Distanz-Referenz) |
| `shown` | — | gezeigte Falschschreibung, z. B. `Tihsc` |
| `label` | `fluent` \| `stocked` | `literal` \| `autocorrected` |
| `note`  | optional | optional |

`#` am Zeilenanfang ist ein Kommentar. Siehe `manifest.example.csv`.

## Report lesen

- **balancierte Genauigkeit ≥ 0.80** und **Margin ≥ 0.10** ⇒ Mechanik validiert.
- **Margin** = Abstand der Klassen-Mediane (>0 = richtig geordnet).
- **Verdikt:**
  - **GO** — beide Mechaniken trennen sauber.
  - **GO-MIT-EINSCHRÄNKUNG** — Flüssigkeit ok, lautgetreue Prüfung nicht; hörbare
    Fehler laufen vorerst nur über Markieren.
  - **NO-GO** — Flüssigkeit trennt nicht; Modellwahl/Headset/Schwellen prüfen.

## Wichtiger Hinweis (Konzept-Risiko 2)

Die lautgetreue Prüfung läuft über **akustische Distanz / Forced-Alignment gegen
die Lautfolge des richtigen Worts** — **niemals** über ASR-Transkription
(Whisper & Co. „reparieren" `Tihsc` still zu `Tisch`). Genau so ist
`fjp0.aligner.TorchAudioAligner` gebaut.

## Aufbau

```
phase0/
├── fjp0/                  # das Paket
│   ├── normalize.py       # dt. Textnormalisierung/Romanisierung für MMS_FA
│   ├── audio.py           # WAV-I/O, RMS, Testton-Erzeugung (Stdlib)
│   ├── gating.py          # Energie-/Dauer-Gate (Stille-Schutz)
│   ├── scoring.py         # Flüssigkeit: Score→Farbe, Clip-Kennzahl
│   ├── literal.py         # lautgetreue Prüfung (nur Klasse 'hoerbar')
│   ├── aligner.py         # Aligner-Interface + Scripted + TorchAudio
│   ├── manifest.py        # CSV-Datensatz laden/validieren
│   ├── calibrate.py       # Schwellensuche + Trennschärfe
│   ├── report.py          # GO/NO-GO-Auswertung (JSON + Markdown)
│   ├── pipeline.py        # verdrahtet alles
│   ├── selftest.py        # synthetischer End-to-End-Beweis
│   └── cli.py             # selftest | run | score | smoke
├── tests/                 # 47 Tests (dependency-frei; torch-Smoke optional)
├── manifest.example.csv   # Vorlage (committet)
├── validate_scoring.py    # Kompatibilitäts-Shim → fjp0.cli
├── requirements.txt       # torch/torchaudio (nur echtes Backend)
├── requirements-dev.txt   # pytest
└── DECISIONS.md           # Entscheidungen & Abweichungen vom Konzept
```
