# CLAUDE.md — Projektkontext für Claude Code

> **Quelle der Wahrheit:** [`docs/Konzept.md`](docs/Konzept.md). Bei Widerspruch gilt das Konzept; diese Datei ist die Kurzfassung + die Regeln, die leicht falsch gemacht werden.

## Was wir bauen

**FehlerJagd** — eine Detektiv-Lern-App für Kinder mit **zwei gekoppelten Mechaniken**:
1. **Vorlesen** — lautes Lesen auf **korrektem** Text, pro Wort phonetisch bewertet (grün/gelb/rot).
2. **Fehlerjagd** — Korrekturlesen: Rechtschreibfehler in einer „Fälscher-Notiz" finden/markieren.

Zielnutzerin: **Antonia** (10, 4. Klasse Volksschule). Ermittlerinnen sind ein **eigenes Trio: Mia, Ben & Frieda** (Ton von „Die drei !!!", aber eigene Figuren). Neun ausgearbeitete Fälle in [`docs/Faelle.md`](docs/Faelle.md).

**Sprache: österreichisches Standarddeutsch** auf Volksschulniveau (österreichischer Lehrplan) — **kein Bundesdeutsch, kein Dialekt**. Wortliste in `docs/Konzept.md`, Abschnitt 4.

## Oberste Priorität: Phase 0 zuerst

**Vor jeder App-Entwicklung** das Kernrisiko absichern (siehe [`phase0/`](phase0/)): Trennt die phonetische Bewertung bei der echten Kinderstimme zuverlässig „flüssig" von „gestockt", und erkennt die lautgetreue Prüfung hörbare Fehler? Erst danach Backend/Frontend bauen. Nicht ungefragt mit dem App-Bau starten.

## Harte Design-Regeln (nicht verletzen)

- **Österreichisches Standarddeutsch** in allen Inhalten: das Cola, einen Einser, Karotte, Grapefruit, Semmel, Sackerl, der Bub, Stiege, Kasten, Schlagobers, Topfen, „es hat geläutet", Perfekt mit *sein* („bin gesessen"), „schauen" (nie „gucken"). **Nicht:** die Cola, eine Eins, Möhre, Brötchen, Tüte, Junge, Treppe, Sahne, „lecker", „Tschüss", Artikel vor Vornamen. Kein Dialekt.
- **Vorlesen und Fehlerjagd sind gleichwertig** — keines dem anderen unterordnen.
- **Antonias Schwerpunkte** (Curriculum, `docs/Konzept.md` Abschnitt 2): Groß/klein, Beistrich, Auslaut (d/t), v/f, i/ie, das/dass, ver-/vor-, Vokallänge. **Alles gleichwertig** — aber **Übungs-Fokus (nicht Exklusivität) auf Phonetik** (Vokallänge/ie/ß/ss + lautgetreues Lesen); Leitidee: exaktes Vorlesen → genaueres Korrekturlesen (Aha-Effekt). Nicht-phonetische Punkte sind **audio-blind → markieren** und durchgehend dabei; Beistriche brauchen einen Lücken-Tipp-Modus.
- **Falschschreibungen NUR in der Fälscher-Notiz** (`mode: fehlerjagd`), **niemals** im Vorlese-Text. Sonst droht orthografische Interferenz.
- **Auflösung mit Regel-Bezug:** Jeder korrigierte Fehler verweist **direkt auf die passende Merkregel (1–8)** — Feld `regel` (+ kindgerechter `tipp`) im `graph.yaml`. Mapping: großschreibung→1, komma→2, auslaut→3, v/f→4, ie→5, das/dass→6, ver/vor→7, vokallänge→8. Außerhalb der 8 (dehnungs-h, doppelvokal, reine hörbar-Dreher): `regel: "–"` + Klartext-`tipp`.
- **Skalierbar (ohne Engine-Änderung):** Fälle dürfen wachsen — **längere `vorlesen`-Texte** und **mehr Schritte**, inkl. **mehrerer `fehlerjagd`-Knoten pro Fall** (mehrere Notizen). Einfach Szenen-Dateien + Knoten ergänzen.
- **Drei-Klassen-Fehlermodell** — jeden Fehler der Methode zuordnen, die ihn erkennt:
  - *hörbar* (laut-verändernd, z. B. „Tihsc") → Vorlesen **oder** Markieren
  - *Vokallänge* (Doppelkonsonant, z. B. „ales"/„alles") → **nur Markieren**
  - *homophon* (Dehnungs-h, viele ie-Fälle, z. B. „Zal"/„Zahl") → **nur Markieren** (Audio ist blind)
- **Lautgetreue Fehlerprüfung über akustische Distanz / Forced-Alignment gegen das richtige Wort — NICHT über ASR-Transkription** (ASR „repariert" die Falschschreibung).
- **Markieren ist deterministisch** (Abgleich mit `proofread_errors`), **kein ML**. Das ist der zuverlässige Rückhalt.
- **Phonetisches Scoring lokal** (torchaudio), Standard. **Kinderstimme/Audio bleibt am Gerät** und wird **nie committet** (siehe `.gitignore`: `*.wav`, `data/`, `*.db`).
- **Kein Live-LLM für das Kind.** Geschichten sind versionierte **Markdown + YAML**; das LLM ist nur ein **Autoren-Werkzeug** (offline).
- **Sanftes Gating, kindgerechtes Feedback.** Mindestschwelle zum Weiterkommen + Bonus für sehr gutes Lesen; „Rot" freundlich rahmen, nie harter „Falsch"-Buzzer.

## Tech-Stack & Konventionen

- **Backend:** Python / FastAPI, SQLite (SQLModel), PyTorch + torchaudio. Scoring-/LLM-/TTS-Provider über Config austauschbar (`local | azure | speechace`).
- **Frontend:** schlanke Web-App (Vite + vanilla JS oder Svelte/Preact), **PWA-fähig**, Audio via `MediaRecorder`/Web Audio.
- **Plattform:** PC-first als lokale Web-App → später online (Backend deployen) und Tablet (PWA), ohne Architektur-Umbau.
- **Geschichten:** ein Ordner pro Fall unter `stories/`, `graph.yaml` (Branch-&-Bottleneck, konvergierende Pfade) + Szenen-Markdown. Fehler in `proofread_errors` mit `klasse` + `method` taggen.
- **Repo-Namen ASCII/PascalCase** (wie `FehlerJagd`), Commits klein und beschreibend.

## Struktur

```
docs/      Konzept.md (Detailkonzept), Faelle.md (9 Fälle)
backend/   FastAPI (folgt)
frontend/  PWA (folgt)
stories/   Fälle als Markdown + YAML (Beispiel: fall-01-bibliothek)
assets/    Bild-Assets (Referenzblätter, Titelbilder, Szenen-Panels)
phase0/    Validierungs-Skript (zuerst!)
```

## Lizenz

Zwei Lizenzen: **Code → MIT** (`LICENSE`) und **kreative Inhalte → CC BY 4.0** (`LICENSE-CONTENT.md`; Geschichten, Fälle, Figuren Mia/Ben/Frieda, Konzept, Bilder). Im Zweifel: ausführbarer Code = MIT, Texte/Geschichten/Bilder = CC BY 4.0. © 2026 tgd1975. Reale Werke/Orte (Klimt „Bauernhaus mit Birken", Belvedere) werden nur referenziert, nicht mitlizenziert (Klimt ist gemeinfrei).
