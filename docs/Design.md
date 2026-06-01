# FehlerJagd — Design-Konzept (Visuelle Identität)

> Schwesterdokument zu `Konzept.md` (Inhalt/Pädagogik) und `Faelle.md` (Story-Bibel).
> Dieses Dokument ist die **Quelle der Wahrheit für alles Visuelle** und wird sowohl von
> **Claude Design** (Bild-Exploration) als auch von **Claude Code** (Einbindung in die App) genutzt.
> Der bestehende `assets/titles/cover-team.svg` ist der **visuelle Anker** — neue Designs werden daran angeglichen.

---

## 0. Zweck & Geltung

FehlerJagd ist ein gemütliches **Detektiv-Lesespiel** für ein 10-jähriges Kind (Wien, Schulstart am Gymnasium). Zwei gleichwertige Mechaniken: **korrekt vorlesen** (phonetisch bewertet, „Ampel" grün/gelb/rot) und **Fehler jagen** (Rechtschreibfehler in einer gerahmten „Fälscher-Notiz" markieren). Das Design soll diese zwei Welten optisch tragen, ohne je zu überfordern oder zu erschrecken.

---

## 1. Zielgruppe & Ton

- **Publikum:** ein einzelnes Kind (~10 J.), leseförderndes Setting, österreichischer Alltag.
- **Ton:** warm, **mädchengeführt**, augenzwinkernd, neugierig — **nie gruselig**. Auch der Prater-„Geist" (Fall 2) und die Belvedere-„Fälschung" (Fall 9) bleiben freundlich und harmlos.
- **Haltung:** Auflösungen sind immer ein Missverständnis oder ein Streich — keine echten Bösewichte. Das spiegelt sich in offenen, freundlichen Gesichtern und hellen Bildern.

---

## 2. Visuelle Sprache

### 2.1 Farbpalette
Werte als Referenz — **die exakten Farben aus `cover-team.svg` übernehmen** (Cover = Quelle der Wahrheit).

| Rolle | Farbe | Hex (Richtwert) |
|---|---|---|
| Papier / Hintergrund | Creme | `#FAF3E4` |
| Primär (Figur **Mia**) | Petrol / Teal | `#2A9D8F` |
| Sekundär (Figur **Ben**) | Senf / Ocker | `#E9C46A` |
| Akzent (Friedas Halsband, Warnungen) | Koralle | `#E76F51` |
| Linien & Text | Tinte | `#2B2B2B` |
| *optional, sparsam* | Salbeigrün (Außen/Wiese) | `#A3B18A` |
| *optional, sparsam* | sanftes Blau (Himmel/Wasser) | `#8DA9C4` |

Grundsatz: warme, leicht entsättigte Töne; viel Creme als „Luft"; Koralle nur als Akzent.

### 2.2 Typografie
- **Display / Headlines / Akten-Nummern:** **Baloo 2** (rund, freundlich).
  Fallback: `"Baloo 2", system-ui, sans-serif`.
- **Fließtext / UI / Vorlese-Text:** **Atkinson Hyperlegible** — bewusst gewählt für **maximale Lesbarkeit** (entwickelt für leseschwache/sehbehinderte Menschen, passt perfekt zur Lese-App).
  Fallback: `"Atkinson Hyperlegible", Verdana, sans-serif`.
- Großzügige Zeilenhöhe und Schriftgröße im Vorlese-Modus (das Kind liest hier wirklich).

### 2.3 Illustrationsstil
- **Flache** Farbflächen, warm, aus der Palette.
- **Outline:** gleichmäßige, leicht handgezeichnet wirkende **Tinten-Outline** (`#2B2B2B`), mittlere Strichstärke; Innenlinien sparsam.
- **Schatten:** höchstens **eine** sanfte Schattenfläche (kein Verlauf) — oder ganz weglassen.
- **Gesichter:** bewusst **einfach** (Punktaugen, kleine Brauen, schlichter Mund) → leicht reproduzierbar und on-model.
- **Hintergründe:** reduziert; ein bis zwei Setting-Requisiten genügen.
- *Optional:* feines Papierkorn auf Creme für Buch-Haptik.

### 2.4 Wiederkehrende Motive
- **Die Akte** (Fallakte / Aktendeckel) — Leitmetapher für jeden Fall (siehe 4.1).
- **Ampel** grün/gelb/rot für die Vorlese-Bewertung — **immer Farbe + Symbol** (`✓` / `~` / `✗`), damit sie auch für farbenblinde Kinder eindeutig ist.
- **Rote Korrektur-Schlängellinie** unter „falschen" Wörtern — das Signet der Fehlerjagd (taucht schon am Cover auf).
- Dezente **Wien-Cues** (Riesenrad, Gloriette, Marktstände) — stilisiert, nie fotorealistisch.

---

## 3. Figuren (kanonische Designs)

**Farbcodierung** macht die drei sofort erkennbar und hält Bilder konsistent. In **jedem** Bild gelten: gleiche Proportionen, Signatur-Requisite mitführen, einfache Gesichter.

### 3.1 Mia — 10 J., die Beobachterin · **Farbcode TEAL**
- Schmal, aufrechte, neugierige Haltung; etwas kleiner.
- Schulterlanges **dunkelbraunes Haar**, seitlich mit kleiner **teal Spange** (oder kurzer Zopf).
- **Teal Kapuzenjacke** über schlichtem Shirt, bequeme Hose, Sneaker.
- **Signatur-Requisite: runde Lupe.** Trägt die Fehlerjagd.
- Ausdruck: aufmerksam, ruhig, leichtes Lächeln; Kopf beim Beobachten leicht geneigt.

### 3.2 Ben — 11 J., einfallsreich & humorvoll · **Farbcode SENF**
- Etwas größer, lebhaft, offene/dynamische Posen.
- Kurze, leicht **lockige dunkle Haare**; **runde Brille** (wie am Cover).
- **Senf-Shirt/Pulli**, einfacher Rucksack — **normales Detektiv-Kram** (keine Hightech-Gadgets).
- **Signatur-Requisite: Notizheft + Stift** (er kritzelt Einfälle und Hinweise hinein); evtl. eine gewöhnliche Taschenlampe.
- Wesen: der **Ideen- und Plänemacher** — improvisiert, hat schnell einen Einfall, lockert mit einem Spruch die Lage.
- Ausdruck: aufgeweckt, breites Grinsen.

### 3.3 Frieda — die clevere Dackeldame
- **Kurzhaardackel**, rotbraun/tan; langer Körper, kurze Beine, **lange Schlappohren**, wache Augen, ausgeprägte Schnauze.
- **Koralle Halsband** mit kleiner Marke.
- **Signatur-Pose:** Nase am Boden, **schnüffelnd**; Schwanz aufgestellt bei Aufregung.
- Ausdruck: clever, neugierig, freundlich.

### 3.4 Marie — Gast (nur Fall 6), ~12–13 J.
- Freundliche **Siebtklässlerin**, etwas größer/„älter"; hilft Mia am ersten Gymi-Tag.
- Schlichtes, etwas reiferes Outfit; **koralle Akzent** (warme Mentorin).
- Nebenfigur — leichtes Spec, ein Auftritt genügt.

### 3.5 Konsistenz-Regeln
- **Farbcode + Signatur-Requisite** in jedem Auftritt.
- **Ausdrucks-Set** je Figur: neutral, fröhlich, überrascht, nachdenklich.
- **Posen-Set:** stehen, zeigen; Mia zusätzlich „beobachten/Lupe"; Frieda „schnüffeln/sitzen/wach".
- Gesichter simpel halten → wiederholbar. Im Zweifel: am Stilframe (3 Figuren) orientieren.

---

## 4. Bildkategorien & Specs

### 4.1 Titelbilder „Aktendeckel" (pro Fall)
Eine **Fallakte** als Titelschirm jedes Falls. Gemeinsames **Template**, nur Nummer/Titel/Vignette tauschen.
- Inhalte: **Reiter „AKTE Nr. N"**, **Titel** (Baloo 2), kleine **Setting-Vignette**, **Figuren-Cameo**, **Schnipsel der Fälscher-Notiz mit roter Korrektur-Schlängellinie** (nur Andeutung), evtl. Büroklammer/Stempel.
- Format: **Querformat 3:2** (z. B. 1500×1000). Vektor (SVG) bevorzugt.
- Menge: **10** (Tutorial `fall-00` + `fall-01`…`fall-09`).

### 4.2 Szenen-Belohnungsbilder
Werden **nach gutem Vorlesen als Belohnung** freigeschaltet — **nicht** neben dem Lesetext (der Text bleibt unbebildert, damit das Kind liest).
- Stil: etwas „filmischer"/voller als die Akten; ganze Story-Momente.
- Format: **Querformat 16:9** (z. B. 1600×900), **PNG**.
- Menge: **1–3 pro Fall**, an Höhepunkten (typisch: Auflösung + Bonus).

### 4.3 UI-Motive (leichtgewichtig)
- **Ampel** (3 Kreise grün/gelb/rot, je mit Symbol `✓ ~ ✗`).
- **Rote Korrektur-Schlängellinie** als SVG-Komponente.
- **Akten-Reiter** (Folder-Tab) als wiederverwendbares UI-Element.
- Buttons/Chips: rund, freundlich, Palette-konform (nur Stilhinweis — Feinschliff später).

---

## 5. Dateien & Formate

Erweiterung der bestehenden `assets/`-Struktur (Benennung folgt den Story-Slugs):

```
assets/
  reference/   mia.svg  ben.svg  frieda.svg  marie.svg  style-frame.svg  (Posen/Ausdrücke)
  titles/      cover-team.svg (vorhanden)  fall-00.svg … fall-09.svg     (Aktendeckel)
  scenes/      fall-01-aufloesung.png  fall-01-bonus.png  …              (Belohnungsbilder)
  ui/          ampel.svg  korrektur-schlaengel.svg  akte-reiter.svg
```

- **SVG** für Vektor-Teile (Titel, Figuren, UI); **PNG** für Szenenbilder.
- Hintergrund wahlweise **Creme** (`#FAF3E4`) oder **transparent** (für UI/Cameos transparent bevorzugen).
- Dateinamen **kleingeschrieben**, an `stories/`-Slugs gekoppelt, damit Claude Code sie eindeutig zuordnen kann.

---

## 6. Barrierefreiheit
- Hoher Kontrast von Tinte auf Creme; großzügige Vorlese-Schrift.
- **Ampel & alle Statusfarben zusätzlich mit Symbol/Form** (rot-grün-blind-freundlich).
- Klare, unterscheidbare **Silhouetten** je Figur (auch ohne Farbe erkennbar).
- **Atkinson Hyperlegible** als Lesefont; keine reinen Farbcodes ohne Text-/Symbolstütze.

---

## 7. Inhaltliche & rechtliche Hinweise
- Alles **kindgerecht & nicht gruselig**, auch bei „Geist"- und „Fälschungs"-Fällen.
- **Keine fremden Marken/Logos.**
- **Klimt-Bild (Fall 9):** eigenständige, **stilisierte Hommage** an „Bauernhaus mit Birken" — bewusst **nicht** originalgetreu (gemeinfrei, aber für Kind und Klarheit stilisiert). Frieda wartet im Garten (Hunde nicht im Saal).
- Reale Orte (Prater, Schönbrunn, Naschmarkt, Belvedere, Rainergymnasium) **stilisiert** darstellen, nicht fotorealistisch.

---

## 8. Deliverables-Checkliste für Claude Design
In **Schritten mit Freigabe** dazwischen (siehe `Claude-Design-Prompt.md`):

1. ☐ **Stilframe** — Mia, Ben, Frieda nebeneinander im finalen Stil + Farb-/Typo-Probe. → Freigabe.
2. ☐ **Figuren-Referenzblätter** — Mia, Ben, Frieda (Posen + Ausdrücke + Farbcode-Notiz); leichtes Blatt für Marie.
3. ☐ **Aktendeckel-Template** → dann alle **10 Akten** (`fall-00`…`fall-09`).
4. ☐ *(optional)* **1–2 Beispiel-Szenenbilder** als Stilbeleg.

---

## 9. Workflow-Anschluss
**Claude Design** (Canvas, visuelle Exploration) → Export der Assets nach `assets/` (Benennung wie oben) → **Claude Code** bindet sie in die App ein. Der bestehende `cover-team.svg` wird, falls nötig, an die finalen Figurendesigns **nachgezogen**, damit Cover und App eine Sprache sprechen.
