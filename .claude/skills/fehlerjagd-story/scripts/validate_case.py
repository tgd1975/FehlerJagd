#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prüft einen FehlerJagd-Fall auf strukturelle und inhaltliche Regeltreue.

Der wichtigste Test (LECK): Falschschreibungen dürfen NUR in der Fälscher-Notiz
(mode: fehlerjagd) stehen, niemals in einem Vorlese-Text.

Beispiel:
  python validate_case.py fall-10-stephansdom
  python validate_case.py stories/fall-10-stephansdom
"""
import argparse, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("Bitte 'pyyaml' installieren:  pip install pyyaml")

ALLOWED_METHODS = {"markieren", "lesen_oder_markieren", "markieren_luecke"}
ALLOWED_REGEL = {1, 2, 3, 4, 5, 6, 7, 8, "–", "-"}
# Klassen, deren Falschwort selbst ein gültiges Wort sein kann (z. B. "das", "fest")
# -> vom strengen Leak-Test ausgenommen, sonst Fehlalarm im Vorlese-Text:
LEAK_EXEMPT = {"das/dass", "grossschreibung", "großschreibung"}


def split_frontmatter(text):
    """Gibt (meta_dict | None, body) zurück. Erwartet ---...--- am Dateianfang."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, m.group(2)


def has_token(token, text):
    """Ganzwort-Treffer (Unicode-Wortgrenzen), damit z. B. 'Nus' nicht in 'Nuss' anschlägt."""
    return re.search(r"(?<!\w)" + re.escape(token) + r"(?!\w)", text) is not None


def node_targets(nd):
    t = []
    if isinstance(nd, dict):
        if "goto" in nd:
            t.append(nd["goto"])
        for c in nd.get("choices", []) or []:
            if isinstance(c, dict) and "goto" in c:
                t.append(c["goto"])
    return t


def main():
    ap = argparse.ArgumentParser(description="Validiert einen FehlerJagd-Fall.")
    ap.add_argument("case", help="Slug (fall-NN-…) oder Pfad zum Fall-Ordner")
    ap.add_argument("--stories-dir", default="stories")
    a = ap.parse_args()

    folder = a.case if os.path.isdir(a.case) else os.path.join(a.stories_dir, a.case)
    if not os.path.isdir(folder):
        sys.exit("FEHLER: Ordner nicht gefunden: %s" % folder)

    errors, warns = [], []

    gpath = os.path.join(folder, "graph.yaml")
    if not os.path.isfile(gpath):
        sys.exit("FEHLER: graph.yaml fehlt in %s" % folder)
    try:
        graph = yaml.safe_load(open(gpath, encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        sys.exit("FEHLER: graph.yaml ist kein gültiges YAML:\n%s" % e)

    nodes = graph.get("nodes") or {}
    if not nodes:
        errors.append("graph.yaml: 'nodes' fehlt oder ist leer.")
    start = graph.get("start")
    if not start:
        errors.append("graph.yaml: 'start' fehlt.")
    elif start not in nodes:
        errors.append("graph.yaml: start '%s' ist kein Node." % start)

    bodies = {}          # node -> (mode, body)
    fehlerjagd_nodes = []
    for name, nd in nodes.items():
        if not isinstance(nd, dict):
            errors.append("Node '%s': muss ein Mapping sein." % name)
            continue
        fname, mode = nd.get("text"), nd.get("mode")
        if not fname:
            errors.append("Node '%s': 'text' (Dateiname) fehlt." % name)
            continue
        fpath = os.path.join(folder, fname)
        if not os.path.isfile(fpath):
            errors.append("Node '%s': Datei fehlt: %s" % (name, fname))
            continue
        meta, body = split_frontmatter(open(fpath, encoding="utf-8").read())
        if meta is None:
            errors.append("%s: keine ---Frontmatter--- am Anfang." % fname)
        elif meta.get("mode") != mode:
            errors.append("%s: Frontmatter mode='%s' ≠ graph mode='%s'." % (fname, meta.get("mode"), mode))
        bodies[name] = (mode, body)
        if mode == "fehlerjagd":
            fehlerjagd_nodes.append(name)
        for t in node_targets(nd):
            if t not in nodes:
                errors.append("Node '%s': goto '%s' existiert nicht." % (name, t))
        if "TODO" in body or "FALSCHWORT" in body:
            warns.append("%s: enthält noch TODO/Platzhalter." % fname)

    if not fehlerjagd_nodes:
        errors.append("Kein Node mit mode: fehlerjagd (es fehlt die Fälscher-Notiz).")

    shown_strict = []  # (token, quelle) für den strengen Leak-Test
    for fn in fehlerjagd_nodes:
        pe = nodes[fn].get("proofread_errors")
        note_body = bodies.get(fn, ("", ""))[1]
        if not pe:
            errors.append("Node '%s': proofread_errors fehlt." % fn)
            continue
        for i, e in enumerate(pe, 1):
            tag = "%s proofread_errors[%d]" % (fn, i)
            if not isinstance(e, dict):
                errors.append("%s: muss ein Mapping sein." % tag)
                continue
            for key in ("shown", "correct", "klasse", "regel", "tipp", "method"):
                if key not in e or e[key] in (None, ""):
                    errors.append("%s: Feld '%s' fehlt/leer." % (tag, key))
            if e.get("method") not in ALLOWED_METHODS:
                errors.append("%s: method '%s' ungültig (erlaubt: %s)." % (tag, e.get("method"), sorted(ALLOWED_METHODS)))
            if e.get("regel") not in ALLOWED_REGEL:
                errors.append("%s: regel '%s' ungültig (1–8 oder '–')." % (tag, e.get("regel")))
            shown = str(e.get("shown", ""))
            if shown and not has_token(shown, note_body):
                errors.append("%s: shown '%s' kommt im Notiz-Text (%s) nicht vor." % (tag, shown, nodes[fn]["text"]))
            if shown and str(e.get("klasse", "")).lower() not in LEAK_EXEMPT:
                shown_strict.append((shown, fn))

    # Strenger Leak-Test: Falschwort darf in KEINER Vorlese-Szene stehen.
    for shown, src in shown_strict:
        for name, (mode, body) in bodies.items():
            if mode == "fehlerjagd":
                continue
            if has_token(shown, body):
                errors.append("LECK: Falschwort '%s' (aus %s) steht im Vorlese-Text %s!" % (shown, src, nodes[name]["text"]))

    print("Fall: %s" % folder)
    print("  Nodes: %d | Fehlerjagd-Notizen: %d" % (len(nodes), len(fehlerjagd_nodes)))
    if warns:
        print("\n⚠️  Warnungen:")
        for w in warns:
            print("   -", w)
    if errors:
        print("\n❌ FEHLER:")
        for e in errors:
            print("   -", e)
        print("\n%d Fehler. Bitte beheben und erneut prüfen." % len(errors))
        sys.exit(1)
    print("\n✅ BESTANDEN — Struktur, Felder und Leak-Test in Ordnung."
          + ("  (Offene Warnungen siehe oben.)" if warns else ""))


if __name__ == "__main__":
    main()
