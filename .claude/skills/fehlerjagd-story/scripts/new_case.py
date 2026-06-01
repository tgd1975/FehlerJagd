#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerüstet einen neuen FehlerJagd-Fall: Ordner stories/<slug>/ mit graph.yaml + 10 Szenen.

Schreibt NUR das Skelett (korrekte Frontmatter + Standardstruktur). Inhalt und Fehler
füllt Claude anschließend von Hand ein. Danach mit validate_case.py prüfen.

Beispiel:
  python new_case.py --slug fall-10-stephansdom \\
      --titel "Geheimnis im Stephansdom" --schauplatz "Stephansdom" \\
      --muster "ie,doppelkonsonant"
"""
import argparse, os, re, sys

SZENEN_VORLESEN = ["szene-01", "szene-02a", "szene-02b", "szene-03",
                   "szene-04a", "szene-04b", "szene-06", "szene-07", "bonus-01"]

HINTS = {
    "szene-01":  "Hook: Schauplatz + Ungereimtheit einführen, Zettel entdecken. Endet mit 1. Entscheidung (A1/A2).",
    "szene-02a": "Verzweigung A1 (läuft mit 02b in szene-03 zusammen).",
    "szene-02b": "Verzweigung A2 (läuft mit 02a in szene-03 zusammen).",
    "szene-03":  "Hinweis/Spur. Endet mit 2. Entscheidung (B1/B2).",
    "szene-04a": "Verzweigung B1 (läuft mit 04b in szene-05 zusammen).",
    "szene-04b": "Verzweigung B2 (läuft mit 04a in szene-05 zusammen).",
    "szene-05":  "FÄLSCHER-NOTIZ (Fehlerjagd). EINZIGER Ort mit Falschschreibungen!",
    "szene-06":  "3. Entscheidung: wen/wie ansprechen. Beide Optionen führen zu szene-07.",
    "szene-07":  "Auflösung MIT Regel-Bezug (Missverständnis/Streich, kein echter Bösewicht).",
    "bonus-01":  "Belohnungsszene, nur bei requires: all_green.",
}


def frontmatter(mode, hint):
    fm = "---\nmode: " + mode + "\n"
    if mode == "fehlerjagd":
        fm += ("# Falschschreibungen NUR hier (Fälscher-Notiz), nie im Vorlese-Text.\n"
               "# Markierbare Fehler + Regel-Bezug: siehe graph.yaml (proofread_errors).\n")
    fm += "---\n\n"
    return (fm
            + "<!-- " + hint + " -->\n"
            + "<!-- TODO: Szene schreiben — Österreichisches Standarddeutsch, "
              "Volksschulniveau, warm, nie gruselig. -->\n")

GRAPH = """# {titel}
case_id: {cid}
titel: "{titel}"
schauplatz: "{schauplatz}"
ziel_muster: {pats}
start: szene-01

nodes:
  szene-01:
    text: szene-01.md
    mode: vorlesen
    target_patterns: {pats}
    choices:
      - {{ label: "TODO Wahl A1", goto: szene-02a }}
      - {{ label: "TODO Wahl A2", goto: szene-02b }}
  szene-02a: {{ text: szene-02a.md, mode: vorlesen, goto: szene-03 }}
  szene-02b: {{ text: szene-02b.md, mode: vorlesen, goto: szene-03 }}
  szene-03:
    text: szene-03.md
    mode: vorlesen
    target_patterns: {pats}
    choices:
      - {{ label: "TODO Wahl B1", goto: szene-04a }}
      - {{ label: "TODO Wahl B2", goto: szene-04b }}
  szene-04a: {{ text: szene-04a.md, mode: vorlesen, goto: szene-05 }}
  szene-04b: {{ text: szene-04b.md, mode: vorlesen, goto: szene-05 }}
  szene-05:
    text: szene-05.md
    mode: fehlerjagd
    # 4–6 Fehler. Pflichtfelder je Eintrag: shown, correct, klasse, regel, tipp, method.
    # klasse: hoerbar | vokallaenge | ie | das/dass | grossschreibung | komma | auslaut | v/f | ver/vor | dehnungs-h | doppelvokal
    # regel:  1=Gross/klein 2=Beistrich 3=Auslaut 4=v/f 5=i/ie 6=das/dass 7=ver-/vor- 8=Vokal-Check ; "–" wenn außerhalb der 8
    # method: markieren | lesen_oder_markieren | markieren_luecke (Komma-Lücke)
    proofread_errors:
      - {{ shown: "FALSCHWORT", correct: "Falschwort", klasse: "hoerbar", regel: "–", tipp: "TODO kindgerechter Hinweis.", method: "lesen_oder_markieren" }}
    goto: szene-06
  szene-06:
    text: szene-06.md
    mode: vorlesen
    choices:
      - {{ label: "TODO Wahl C1", goto: szene-07 }}
      - {{ label: "TODO Wahl C2", goto: szene-07 }}
  szene-07: {{ text: szene-07.md, mode: vorlesen, goto: bonus-01 }}
  bonus-01: {{ text: bonus-01.md, mode: vorlesen, requires: all_green }}
"""


def main():
    ap = argparse.ArgumentParser(description="Gerüstet einen neuen FehlerJagd-Fall.")
    ap.add_argument("--slug", required=True, help='z. B. "fall-10-stephansdom"')
    ap.add_argument("--titel", required=True)
    ap.add_argument("--schauplatz", required=True)
    ap.add_argument("--muster", default="", help='Komma-Liste, z. B. "ie,doppelkonsonant"')
    ap.add_argument("--stories-dir", default="stories")
    a = ap.parse_args()

    if not re.match(r"^fall-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$", a.slug):
        sys.exit("FEHLER: --slug muss die Form 'fall-NN-kebab' haben (bekommen: %r)." % a.slug)

    cid = "-".join(a.slug.split("-")[:2])  # fall-NN
    folder = os.path.join(a.stories_dir, a.slug)
    if os.path.exists(folder):
        sys.exit("FEHLER: %s existiert bereits. (Überschreiben verweigert.)" % folder)

    pats = "[" + ", ".join('"%s"' % m.strip() for m in a.muster.split(",") if m.strip()) + "]"
    os.makedirs(folder)
    with open(os.path.join(folder, "graph.yaml"), "w", encoding="utf-8") as f:
        f.write(GRAPH.format(titel=a.titel, cid=cid, schauplatz=a.schauplatz, pats=pats))
    for s in SZENEN_VORLESEN:
        with open(os.path.join(folder, s + ".md"), "w", encoding="utf-8") as f:
            f.write(frontmatter("vorlesen", HINTS[s]))
    with open(os.path.join(folder, "szene-05.md"), "w", encoding="utf-8") as f:
        f.write(frontmatter("fehlerjagd", HINTS["szene-05"]))

    print("✅ Gerüstet: %s  (graph.yaml + 10 Szenen)" % folder)
    print("Nächste Schritte:")
    print("  1) Szenen 01–07 + bonus schreiben (KEINE Fehler im Vorlese-Text!).")
    print("  2) Fälscher-Notiz in szene-05.md schreiben; Fehler in graph.yaml (proofread_errors) eintragen.")
    print("  3) Prüfen:  python <skill>/scripts/validate_case.py %s" % a.slug)


if __name__ == "__main__":
    main()
