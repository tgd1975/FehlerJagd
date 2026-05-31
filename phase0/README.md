# Phase 0 — Kernrisiko absichern (vor allem anderen)

Das ganze Projekt hängt an einer Frage: **Ist die phonetische Bewertung bei der Stimme deiner Tochter zuverlässig genug?** Diese Phase ist ein *Wegwerf-Experiment*, kein Produktionscode.

## Was geprüft wird

1. **Flüssigkeit (Nähe):** Trennen die Wort-Scores „flüssig gelesen" sauber von „gestockt/falsch"? → legt die grün/gelb/rot-Schwellen fest.
2. **Lautgetreue Fehlerprüfung (Distanz, nur hörbare Fehler):** Erkennt die akustische **Distanz zum richtigen Wort** zuverlässig, ob sie eine Falschschreibung (z. B. „Tihsc") literal gelesen oder zu „Tisch" auto-korrigiert hat? → legt fest, welche Fehler *vorlesend* und welche *nur durch Markieren* laufen.

Das **Markieren** (Antippen der Fehler) braucht keine Validierung — es ist deterministisch und steht unabhängig vom Audio-Ergebnis.

## Vorgehen

1. 5–10 kurze Vorlese-Clips deiner Tochter aufnehmen (geplantes Headset, 16 kHz Mono WAV), je mit bekanntem Soll-Text.
2. Ein paar Clips mit **absichtlichen, hörbaren** Falschschreibungen, jeweils einmal literal gelesen und einmal „normal" (auto-korrigiert).
3. `validate_scoring.py` anpassen (Pfade/Texte) und laufen lassen.
4. Schwellen einstellen, bis die Trennung passt. **Ergebnis = GO/NO-GO.**

## Wichtiger Hinweis

Die lautgetreue Prüfung **darf nicht über ASR-Transkription** laufen (Whisper & Co. „korrigieren" `Tihsc` automatisch zu `Tisch`). Sie muss als **akustische Distanz / Forced-Alignment gegen die Lautfolge des richtigen Worts** gebaut werden — genau das skizziert das Skript.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install torch torchaudio soundfile numpy --index-url https://download.pytorch.org/whl/cpu
python validate_scoring.py --audio meine_aufnahme.wav --text "der erwartete satz"
```

> Der Code ist ein **Ausgangspunkt** und bewusst noch nicht getestet — er zeigt die Struktur und die torchaudio-Forced-Alignment-Logik. Erwarte, an Modellwahl (deutsches/mehrsprachiges Modell) und Schwellen zu feilen.
