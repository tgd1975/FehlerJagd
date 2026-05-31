# Phase 0 — Umsetzungsentscheidungen & Abweichungen vom Konzept

Dieses Dokument hält die wichtigen Entscheidungen der Phase-0-Umsetzung fest —
**besonders die Stellen, an denen vom ursprünglichen Konzept abgewichen wurde.**
Quelle der Wahrheit für das Konzept bleibt [`../docs/Konzept.md`](../docs/Konzept.md).

---

## A. Abweichungen vom Konzept (bewusst, begründet)

### A1. Synthetischer Selbsttest statt echter Kinder-Aufnahmen — **größte Abweichung**
**Konzept (Abschnitt 7):** „Nimm 5–10 echte Vorlese-Clips deiner Tochter auf …
das entscheidet GO/NO-GO."

**Realität:** Diese Umsetzungsumgebung kann keine echten Kinder-Aufnahmen
erzeugen. Ohne Daten wäre Phase 0 weder lauffähig noch nachweisbar.

**Entscheidung:** Phase 0 wird als **vollständiges, getestetes Harness** gebaut,
das mit echten Aufnahmen das echte GO/NO-GO liefert — und zusätzlich einen
**synthetischen Selbsttest** mitbringt (`python -m fjp0 selftest`). Dieser erzeugt
gelabelte Kunst-Clips und schickt sie über **exakt dieselbe Pipeline**
(Manifest → Scoring → Gating → Kalibrierung → GO/NO-GO).

**Was das beweist / was nicht:**
- ✅ Beweist: Die Entscheidungs-, Kalibrierungs- und Report-Logik arbeitet
  end-to-end korrekt und trifft das erwartete Verdikt.
- ❌ Beweist **nicht**: die akustische Modellgüte an echter Kinderstimme. Das
  bleibt dem Lauf mit echten Aufnahmen vorbehalten (`run --manifest …`).
  Der Selbsttest ersetzt **nicht** das eigentliche De-Risking — er stellt sicher,
  dass das Werkzeug bereitsteht und korrekt rechnet, sobald echte Clips da sind.

### A2. Manifest als CSV statt YAML
**Konzept:** Die Story-Engine nutzt YAML (`graph.yaml`).
**Entscheidung:** Das Phase-0-Datensatz-Manifest ist **CSV** (Stdlib `csv`).
**Grund:** Hält das gesamte Harness **dependency-frei** (kein PyYAML nötig) und
damit überall sofort test-/lauffähig; CSV ist diff-freundlich und in jeder
Tabellenkalkulation editierbar. Betrifft nur das Phase-0-Wegwerf-Werkzeug, nicht
das Story-Format der späteren App.

### A3. `validate_scoring.py` refaktoriert statt belassen
**Konzept/CLAUDE.md:** referenzieren `phase0/validate_scoring.py`.
**Entscheidung:** Die Logik wurde in das getestete Paket `fjp0/` überführt;
`validate_scoring.py` bleibt als **dünnes Kompatibilitäts-Shim**, das an die neue
CLI delegiert. So funktioniert der im Konzept benannte Pfad weiter, ohne dass
ungetesteter Monolith-Code stehen bleibt. (Phase 0 ist laut Konzept ein
„Wegwerf-Skript" — hier bewusst etwas solider gebaut, weil es das einzige
GO/NO-GO-Werkzeug ist und Tests den Aussagewert erhöhen.)

---

## B. Wichtige Designentscheidungen (innerhalb des Konzepts)

### B1. Austauschbares Aligner-Backend (Kern-Architektur)
Das akustische Modell steckt hinter dem Protokoll `fjp0.aligner.Aligner`.
- `TorchAudioAligner` — echte `torchaudio.pipelines.MMS_FA`-Forced-Alignment,
  **lazy** importiert (torch wird nur geladen, wenn wirklich gebraucht).
- `ScriptedAligner` — deterministisch, für Selbsttest/Unit-Tests, ohne Modell.
Damit ist die gesamte Logik ohne 200-MB-Download und ohne GPU testbar. Die
torch-Forced-Alignment-Methode aus dem Original-Skript bleibt unverändert
erhalten (längen-gewichteter Token-Score → Wort-Score).

### B2. Energie-Gate ausimplementiert (Konzept-Risiko 2, war ein `TODO`)
Das Original-Skript hatte nur `# TODO: RMS/VAD`. Ohne dieses Gate hätte die
lautgetreue Prüfung eine gefährliche Lücke: ein **stiller** Clip ist akustisch
fern vom richtigen Wort → niedriger Score → würde fälschlich als „literal
gelesen = erkannt" gewertet. `fjp0.gating` prüft **RMS-Energie** und
**stimmhafte Mindestdauer**; verworfene Clips fließen **nicht** in die
Kalibrierung ein und gelten in der Einzelprüfung als `ungültig`, **nie** als
literal. Bewusst kein ML-VAD (genügt für Phase 0, bleibt dependency-frei).

### B3. Asymmetrisches GO/NO-GO (folgt direkt aus dem Konzept)
- **Flüssigkeit (Mechanik A) = harte Bedingung.** Trennt sie nicht → **NO-GO**.
- **Lautgetreue Prüfung (Mechanik B) = degradierbar.** Markieren ist der
  deterministische Rückhalt für *alle* Fehlerklassen (Konzept-Risiko 3). Trennt
  die akustische Distanz nicht → **GO-MIT-EINSCHRÄNKUNG**: App bauen, aber
  hörbare Fehler vorerst nur über Markieren. Kein Projekt-Stopp.

### B4. Trennschärfe-Metrik: balancierte Genauigkeit + Median-Margin
Beide Phase-0-Fragen sind dasselbe Zwei-Klassen-Trennproblem. Die Kalibrierung
sucht die Schwelle mit maximaler **balancierter Genauigkeit** (klassen-fair bei
ungleicher Clip-Zahl); bei Gleichstand gewinnt die mittiger liegende Schwelle
(robuster). Schwellen für „validiert": balancierte Genauigkeit ≥ 0.80 **und**
Median-Margin ≥ 0.10. Bewusst konservativ, aber für Kinderstimmen mild
(vgl. Konzept Abschnitt 3 / Risiko 4).

### B5. Clip-Flüssigkeit = Mittelwert der Wort-Scores
Aggregation der Wort-Scores zur Clip-Kennzahl über den **Mittelwert** (statt min):
ein einzelnes gestocktes Wort senkt den Schnitt wie gewünscht, ohne dass ein
Ausreißer den ganzen Clip kippt. Die Wort-für-Wort-Farben (grün/gelb/rot) bleiben
für das spätere Feedback/Dashboard erhalten.

### B6. Deutsche Romanisierung für MMS_FA
Der mehrsprachige Aligner kennt ä/ö/ü/ß nicht; `fjp0.normalize` romanisiert sie
(ä→ae, ö→oe, ü→ue, ß→ss). **Phase-0-Annahme**, in der Kalibrierung zu prüfen;
bei Wechsel auf ein dediziertes deutsches wav2vec2-Modell kann sie entfallen.

---

## C. Umgebungs-Grenze (kein Code-Fehler)

Der echte torchaudio-**Smoke-Test** (`python -m fjp0 smoke` bzw.
`tests/test_smoke_torch.py`) lädt das MMS_FA-Modell herunter. In dieser
Umsetzungsumgebung ist der Modell-Host **netzwerkseitig gesperrt**
(`HTTP 403 Forbidden`; PyPI ist erlaubt, der Modell-CDN nicht). Der Test
**überspringt** dann sauber (`pytest.importorskip` + try/skip), statt zu
scheitern. **Lokal beim Nutzer mit freiem Netz läuft er durch.** torch 2.x +
torchaudio sind installiert und importieren fehlerfrei — nur der Modell-Download
ist hier blockiert.

---

## D. Was als Nächstes mit ECHTEN Daten zu tun ist

1. 5–10 Clips von Antonia mit dem geplanten Headset aufnehmen (16 kHz Mono WAV),
   nach `phase0/data/audio/` legen.
2. `phase0/manifest.example.csv` nach `phase0/data/manifest.csv` kopieren und mit
   den echten Pfaden/Labels füllen.
3. `python -m fjp0 run --manifest phase0/data/manifest.csv` ausführen.
4. Schwellen (`fjp0.scoring`, `fjp0.gating`, `fjp0.report`) anhand des Reports
   nachziehen, bis die Trennung Antonias Stimme abbildet → **echtes GO/NO-GO.**

Alle Audio-/Datendateien sind per `.gitignore` vom Commit ausgeschlossen
(Kinderstimme bleibt am Gerät — Konzept-Risiko 6).
