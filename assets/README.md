# assets/ — Bild-Assets

Bildstrategie im Detail: siehe [`../docs/Konzept.md`](../docs/Konzept.md), Abschnitt 5.

## Struktur
```
assets/
├── reference/                 # ZUERST: Stil-Guide + Charakter-Referenzblätter
│   ├── stil-guide.*           # Palette, Linien, Look (eigener Stil, nicht an eine Reihe angelehnt)
│   ├── mia.*                  # Posen/Mienen — Grundlage für Konsistenz
│   ├── ben.*
│   └── frieda.*
├── titles/                    # je 1 Aktendeckel-Bild pro Fall (Fallauswahl)
│   ├── fall-01.png … fall-06.png
└── scenes/                    # OPTIONAL: Comic-Panels, erscheinen erst nach gutem Vorlesen
    └── fall-0X/szene-YY.png
```

## Reihenfolge & Prinzipien
1. **Stil-Guide + Charakter-Referenzblätter** zuerst — sie sind die Grundlage für gleichbleibende Figuren (egal ob KI oder Illustration).
2. **Titelbilder** (6 Stück) — schauplatzbetont, Figuren höchstens klein. Gut mit **Claude Design** zu erstellen.
3. **Szenenbilder** zuletzt und optional — als **Belohnung** (Reveal nach gutem Vorlesen), nie als inhaltsverratendes Beiwerk neben dem Lesetext.

## Verknüpfung (in `stories/<fall>/graph.yaml`)
- `title_image:` pro Fall → Bild in `titles/`.
- `reveal_image:` pro Szene (optional) → Panel in `scenes/<fall>/`, das erst nach gutem Vorlesen erscheint.

## Stil
Flach, freundlich, warm; Palette laut Konzept. **Rot/Gelb/Grün bleibt dem Vorlese-Feedback vorbehalten** — Titel-/Szenenbilder nutzen die übrige Palette. Eigener Stil, bewusst nicht an eine bestehende Reihe angelehnt.
