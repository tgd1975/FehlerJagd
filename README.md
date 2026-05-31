# FehlerJagd

Eine interaktive **Detektiv-Lern-App** für Kinder, die zwei Fähigkeiten in einem Spiel verbindet:

1. **Vorlesen** — lautes, flüssiges Lesen, pro Wort phonetisch bewertet (grün/gelb/rot).
2. **Fehlerjagd** — Korrekturlesen: in einer „gefälschten Nachricht" versteckte Rechtschreibfehler aufspüren und markieren.

> Status: **Konzeptphase / Phase 0.** Das vollständige Konzept liegt unter [`docs/Konzept.md`](docs/Konzept.md).

## Die Idee in Kürze

Geübte Leser lesen ganzheitlich und „reparieren" Rechtschreibfehler automatisch — gut fürs Lesetempo, schlecht fürs Korrekturlesen. FehlerJagd trainiert beides getrennt: Leseflüssigkeit auf korrektem Text und bewusstes Hinschauen auf Fehler in einer klar gerahmten „Fälscher-Notiz".

Zentrale Designregel: Jeder Rechtschreibfehler wird der Methode zugeordnet, die ihn zuverlässig erkennt — laut-verändernde Fehler kann das Kind *vorlesend* jagen, vokallängen- und stumme Fehler (z. B. Dehnungs-h) nur durch *Markieren* (deterministisch geprüft). Details: siehe Drei-Klassen-Modell im Konzept.

## Technik (geplant)

- **Backend:** Python / FastAPI, SQLite, **PyTorch + torchaudio** (phonetisches Scoring lokal, Stimme bleibt am Gerät → DSGVO).
- **Frontend:** Browser-Web-App (PWA-fähig), Audioaufnahme via Web Audio / `MediaRecorder`.
- **Geschichten:** versionierte **Markdown + YAML**-Dateien (kein Live-LLM für das Kind; LLM nur als Autoren-Werkzeug).
- **Plattform:** PC-first als lokale Web-App → wächst ohne Umbau zu online (Backend deployen) und Tablet (PWA).

## Repo-Struktur

```
FehlerJagd/
├── docs/        # Konzept.md — das vollständige Detailkonzept
├── backend/     # FastAPI-Backend (Scoring, Story-Loader, SQLite) — folgt
├── frontend/    # PWA-Web-App — folgt
├── stories/     # Fälle als Markdown + YAML (Beispiel: fall-01-bibliothek)
├── assets/      # Bild-Assets (Referenzblätter, Titelbilder, Szenen-Panels)
└── phase0/      # Wegwerf-Skript zur Validierung der phonetischen Bewertung
```

## Nächster Schritt: Phase 0

Bevor irgendetwas gebaut wird, klärt [`phase0/`](phase0/) das Kernrisiko: Trennt die phonetische Bewertung bei der Stimme des Kindes zuverlässig „flüssig" von „gestockt", und erkennt die lautgetreue Prüfung hörbare Fehler? Das entscheidet, welche Fehler über welche Methode laufen.

## Lizenz

Dieses Repo nutzt **zwei Lizenzen** — eine für Code, eine für die kreativen Inhalte:

- **Code** (`backend/`, `frontend/`, `phase0/` und alle Quelldateien) → **MIT** (siehe [`LICENSE`](LICENSE)).
- **Kreative Inhalte** — die Geschichten und Fälle (`docs/Faelle.md`, `stories/`), das Konzept (`docs/Konzept.md`), die Figuren **Mia, Ben & Frieda** sowie die Bilder (`assets/`, z. B. das Cover) → **Creative Commons Namensnennung 4.0 (CC BY 4.0)** (siehe [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)).

Im Zweifel: **ausführbarer Code = MIT**, **Texte/Geschichten/Bilder = CC BY 4.0**. Namensnennung: „FehlerJagd von tgd1975".
