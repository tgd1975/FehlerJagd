---
name: fehlerjagd-story
description: >-
  Erzeugt einen neuen, regeltreuen Fall ("Fall"/Geschichte) für das FehlerJagd-Kinder-Lernspiel
  in diesem Repo — vollständige Szenen-Markdown + graph.yaml unter stories/. Use this skill
  whenever the user wants to add, scaffold, write, generate or extend a FehlerJagd case/story/Fall,
  or says things like "neuen Fall erzeugen", "schreib Fall 10", "neue FehlerJagd-Geschichte",
  "add a case", "noch einen Fall" — auch wenn die Regeln nicht erwähnt werden. Sorgt für:
  Österreichisches Standarddeutsch (Volksschulniveau), die 8 Merkregeln + Drei-Klassen-Fehlermodell,
  Auflösung mit Regel-Bezug, Falschschreibungen NUR in der Fälscher-Notiz, konvergente
  Verzweigungsstruktur und warmen, nie gruseligen Ton. Enthält Gerüst- und Prüfskripte (inkl. Leak-Test).
---

# FehlerJagd — einen neuen Fall erzeugen

FehlerJagd ist ein Detektiv-Lesespiel für ein 10-jähriges Kind. Jeder Fall hat zwei gleichwertige Mechaniken: **korrekt vorlesen** (phonetisch bewertet, „Ampel" grün/gelb/rot) und **Fehler jagen** (Rechtschreibfehler in einer gerahmten „Fälscher-Notiz" markieren).

**Oberste Regel:** Falschschreibungen stehen **ausschließlich** in der Fälscher-Notiz (`szene-05.md`, `mode: fehlerjagd`). In **keinem** Vorlese-Text darf je ein Fehler vorkommen — sonst lernt das Kind den Fehler falsch. Das Prüfskript erzwingt das.

## Schritt 0 — kanonische Regeln lesen (Pflicht, gegen Drift)
Diese Dateien im Repo sind die **Quelle der Wahrheit**. Lies sie zuerst, statt aus dem Gedächtnis zu arbeiten:
- `CLAUDE.md` — alle harten Regeln kompakt (Sprache, Gewichtung, Drei-Klassen-Modell, Schwerpunkte, Auflösungs-Mapping).
- `docs/Konzept.md` — §1 Bewertung, §2 Didaktik + die **8 Merkregeln**, §6e **Story-Format (YAML-Schema)**.
- `docs/Faelle.md` — **Legende** (Fehlerklasse → Merkregel) und die **Abdeckungsmatrix** (welche Regel in welchen Fällen schon geübt wird).
- `docs/Design.md` — nur falls auch Titel-/Szenenbilder geplant sind.

## Ablauf
1. **Fall festlegen.** Wiener Schauplatz; warme Prämisse, deren Auflösung ein **Missverständnis oder Streich** ist (kein echter Bösewicht). Nächste freie Nummer/Slug wählen (`stories/` ansehen).
2. **Schwerpunkt wählen.** In der **Abdeckungsmatrix** (`docs/Faelle.md`) schauen, welche der 8 Merkregeln noch wenig geübt sind, und 1–2 davon zum Schwerpunkt machen (Phonetik-Schwerpunkt erlaubt, aber ausgewogen mischen).
3. **Gerüst anlegen** mit `new_case.py` (siehe Werkzeuge) → erzeugt `graph.yaml` + 10 Szenen mit korrekter Frontmatter und Standardstruktur.
4. **Szenen schreiben** (01–07 + bonus), siehe Struktur unten. Österreichisches Standarddeutsch, Volksschulniveau, warm. **Kein Fehler im Vorlese-Text.**
5. **Fälscher-Notiz + Fehler.** Notiztext in `szene-05.md`; die Fehler als `proofread_errors` in `graph.yaml` (Felder: `shown`, `correct`, `klasse`, `regel`, `tipp`, `method`).
6. **graph.yaml füllen:** echte `choices`-Labels und `target_patterns`.
7. **Prüfen** mit `validate_case.py`, bis **BESTANDEN**. Erst dann ist der Fall fertig.
8. **Bibel aktualisieren (empfohlen):** den Fall in `docs/Faelle.md` ergänzen (Kurzbeschreibung, Fehlerliste, Abdeckungsmatrix). Kein zentrales Manifest nötig — der Fall wird über seinen Ordner erkannt.

## Struktur eines Falls
Dateien: `graph.yaml` + `szene-01, 02a, 02b, 03, 04a, 04b, 05, 06, 07, bonus-01` (`.md`).

```
szene-01 (Hook, vorlesen) ──1. Wahl──► szene-02a ┐
                            └─────────► szene-02b ┴─► szene-03 (Hinweis) ──2. Wahl──► szene-04a ┐
                                                                          └─────────► szene-04b ┴─► szene-05 (FÄLSCHER-NOTIZ, fehlerjagd)
                                                                                                     └─► szene-06 ──3. Wahl (beide Optionen)──► szene-07 (Auflösung) ─► bonus-01 (requires: all_green)
```
Die Szenen sind kurz (Lese-Niveau ~10 J., je ~3–5 Sätze). Skalierung erlaubt: längere Texte oder **mehrere** Notiz-Szenen sind möglich (einfach weitere Nodes ergänzen) — der Validator kommt damit zurecht.

## Die Fälscher-Notiz (Herzstück)
4–6 Fehler pro Notiz. **Drei-Klassen-Modell** (Details in `docs/Konzept.md` §1):
- **hörbar** — vertauschte Buchstaben, die den Klang verändern (z. B. `Bücehr`→Bücher). `method: lesen_oder_markieren`.
- **vokallänge** — Doppelkonsonant/ck/tz/ss/ß (z. B. `Glük`→Glück, `süs`→süß). Nur markierbar. `method: markieren`.
- **homophon u. Ä.** — klingt identisch: `ie`, `das/dass`, `v/f`, Dehnungs-h, Doppelvokal (z. B. `vile`→viele). Nur markierbar. `method: markieren`.
- **Komma-Lücke** — fehlender Beistrich zwischen zwei Wörtern: `shown: "ist weil"`, `correct: "ist, weil"`, `method: markieren_luecke`.

**Regel-Bezug (Pflicht)** — jedes Fehler-Mapping bekommt `regel` + kindgerechten `tipp`. Mapping (kanonisch in `docs/Konzept.md` §2):

| klasse | regel | klasse | regel |
|---|---|---|---|
| grossschreibung | 1 | das/dass | 6 |
| komma | 2 | ver/vor | 7 |
| auslaut | 3 | vokallaenge | 8 |
| v/f | 4 | hörbar / dehnungs-h / doppelvokal | „–" |
| ie | 5 | | |

`shown` (das Falschwort) muss **wörtlich in der Notiz** vorkommen und sonst **nirgends**. Die Auflösung in `szene-07` greift die passende Merkregel auf.

## Sprache & Ton
- **Österreichisches Standarddeutsch, Volksschulniveau.** Kurz: *das Cola, Semmel, Sackerl, Jause, der Bub, Stiege, Kasten, Sessel, Schlagobers, Topfen, Palatschinke, heuer, Turnsaal*; „es hat geläutet"; Perfekt mit *sein*; „schauen" (nie „gucken"); Grüße: Servus/Grüß dich. **Meiden:** die Cola, Möhre, Brötchen, Tüte, Junge, Treppe, Sahne/Quark, „gucken", „lecker", „klingeln", „Tschüss", Artikel vor Vornamen, Dialekt. Vollständige Liste in `CLAUDE.md`.
- **Ton:** warm, mädchengeführt, augenzwinkernd, **nie gruselig**. Auflösung freundlich (Missverständnis/Streich).
- **Figuren (on-model):** **Mia** (10, Beobachterin, trägt die Fehlerjagd, Lupe), **Ben** (11, einfallsreich & humorvoll, Ideen-/Plänemacher, Brille, Notizheft), **Frieda** (clevere Dackeldame, schnüffelt). Gast **Marie** (Siebtklässlerin) nur in Fall 6. Details/Charakterköpfe in `docs/Faelle.md` und `docs/Design.md`.

## Werkzeuge
Aus dem Repo-Wurzelverzeichnis ausführen (`${CLAUDE_SKILL_DIR}` zeigt auf diesen Skill-Ordner):

**Gerüst anlegen:**
```bash
python "${CLAUDE_SKILL_DIR}/scripts/new_case.py" \
  --slug fall-10-stephansdom \
  --titel "Geheimnis im Stephansdom" \
  --schauplatz "Stephansdom" \
  --muster "ie,doppelkonsonant"
```

**Prüfen** (führt u. a. den Leak-Test aus; benötigt `pyyaml`):
```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_case.py" fall-10-stephansdom
```

## Abschluss-Checkliste
- [ ] `validate_case.py` meldet **BESTANDEN** (keine offenen TODO-Warnungen mehr).
- [ ] Kein Falschwort im Vorlese-Text; alle `shown` stehen in der Notiz.
- [ ] Jeder Fehler hat `klasse`, `regel` (1–8 oder „–") und einen kindgerechten `tipp`.
- [ ] Auflösung (`szene-07`) freundlich und mit Regel-Bezug.
- [ ] `docs/Faelle.md` (Beschreibung + Abdeckungsmatrix) ergänzt.

## Beispiel
**Eingabe:** „Schreib einen neuen Fall am Stephansdom, Schwerpunkt i/ie und Doppelkonsonanten."
**Vorgehen:** Schritt 0 lesen → Slug `fall-10-stephansdom`, Prämisse mit harmloser Auflösung wählen → `new_case.py` (oben) → Szenen schreiben → Notiz mit z. B. `vile`→viele (ie, Regel 5) und `komt`→kommt (vokallänge, Regel 8) → `graph.yaml` füllen → `validate_case.py` bis BESTANDEN → `docs/Faelle.md` ergänzen.
