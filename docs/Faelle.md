# Die neun Fälle — Mia, Ben & Frieda

Neun ausgearbeitete Detektivfälle für **FehlerJagd**, im **Ton von „Die drei !!!"** (warm, freundschaftlich, mädchengeführt — bewusst leichter als *Die drei ???* oder *TKKG*), mit **eigenem Trio**. Schema je Fall (siehe [`Konzept.md`](Konzept.md), Abschnitt 3 & 4):

**Hook → 2–3 konvergierende Entscheidungen → Fälscher-Notiz (Fehlerjagd) → Auflösung → optionale Bonus-Szene.**

- **Sprache:** österreichisches Standarddeutsch (kein Bundesdeutsch, kein Dialekt).
- **Rollen:** **Mia** trägt die Fehlerjagd; **Ben** hat die Einfälle, spricht Leute an und sorgt für Humor; **Frieda** (Dackel-Dame) erschnüffelt Spuren.
- **Gewichtung:** Die Notizen sind **phonetik-dominant** (Fokus laut Konzept, wegen des erhofften Aha-Effekts); die nicht-phonetischen Punkte sind **eingestreut**, und **Fall 8 & 9** widmen sich ihnen stärker. **Alle Punkte sind gleichwertig** — Fokus betrifft nur die Übungs-Dosis.

## Fehlerklassen & Methode
Alle *audio-blinden* Klassen werden **nur markiert**; nur `hörbar` lässt sich vorlesen **oder** markieren.
- `hörbar` — laut-verändernd (Buchstabendreher) → vorlesen oder markieren
- `vokallänge` — Doppelkonsonant/ck/tz, ß/ss → markieren
- `ie` / `dehnungs-h` / `homophon` — klingt identisch → markieren
- **audio-blind, je Merkblatt:** `großschreibung`, `komma` (Lücken-Modus: zwischen zwei Wörter tippen), `auslaut` (d/t), `v/f`, `das/dass`, `ver/vor` → markieren

**Auflösung mit Regel-Bezug:** In der Auflösung verweist jede Korrektur **direkt auf die passende Merkregel** (1–8): `großschreibung`→1, `komma`→2, `auslaut`→3, `v/f`→4, `ie`→5, `das/dass`→6, `ver/vor`→7, `vokallänge`→8. Phänomene außerhalb der acht Punkte (`dehnungs-h`, `doppelvokal`, reine `hörbar`-Dreher) bekommen eine kurze Klartext-Begründung. Im `graph.yaml` als Feld `regel` (+ `tipp`) hinterlegt.

## Abdeckung der acht Merkblatt-Punkte
| Punkt | Fälle |
|---|---|
| Groß/klein | 1, 6, 8 |
| Beistrich (Komma) | 5, 8 |
| Auslaut (d/t) | 3, 9 |
| v/f | 2, 8 |
| i/ie | 1, 4 |
| das/dass | 4, 8 |
| ver-/vor- | 5, 9 |
| Vokallänge / ß–ss | 1, 3, 5, 6, 7 (+ Dehnungs-h in 2, 6) |

---

## Fall 0 — Tutorial: Willkommen im Detektivklub
**Schauplatz:** Rahmenhandlung (Detektivklub).
**Zweck:** das Trio vorstellen, **beide Mechaniken erklären** und das **Detektiv-Ohr eichen** (Stimm-Eichung = individuelles Training der Phonetikerkennung). Dateien: [`stories/fall-00-tutorial/`](../stories/fall-00-tutorial/).

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 | Mia, Ben & Frieda stellen sich vor, begrüßen die neue Detektivin. | **Vorlesen** |
| 2 | Vorlese-Mechanik erklärt: Ampel **grün/gelb/rot**. | **Vorlesen** |
| 3 — **Stimm-Eichung** | Sechs kurze Eich-Sätze laut lesen; die App lernt die Stimme kennen (Basislinie für die Bewertung, **ohne Wertung**). | **Kalibrierung** |
| 4 | Der Fälscher & die Fälscher-Notiz werden eingeführt: **Fehler antippen**. | **Vorlesen** |
| 5 | Erste, leichte Fehlerjagd mit Tipps (2× hörbar + 1× Groß/klein). | **Fehlerjagd** |
| 6 — Abschluss | „Du bist bereit!" → führt zu **Fall 1**. | **Vorlesen** |

**Eich-Sätze (Szene 3):** kurz, sicher lesbar, breite Lautabdeckung (lange/kurze Vokale, Umlaute, Diphthonge ei/au/eu, sch/ch) — die Grundlage für die persönlichen grün/gelb/rot-Schwellen (vgl. [`phase0/`](../phase0/)). Die **Fehlschreibungen** stehen nur in der Fälscher-Notiz (Szene 5): *erwsichen→erwischen*, *Felher→Fehler* (beide hörbar), *fälscher→Fälscher* (Groß/klein).

---

## Fall 1 — Das Geheimnis der Schulbibliothek
**Schauplatz:** Schulbibliothek, erster Schultag nach den Ferien.
**Ziel-Muster:** Doppelkonsonant, ie (+ Groß/klein).
**Prämisse:** Über Nacht stehen die Bücher anders; ein Drohzettel taucht auf. Auflösung: Der pensionierte Schulwart ordnet die Bände heimlich nach einem alten System — als Überraschung zum Jubiläum der Bibliothek.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Mia entdeckt vertauschte Bücher und einen Zettel zwischen zwei Bänden. | **Vorlesen** |
| 2 — Wahl A | *Den Schulwart fragen* **/** *Das Regal untersuchen* → Frieda erschnüffelt eine Spur | **Vorlesen** → Konvergenz |
| 3 | Eine verschlüsselte Notiz: Zahlen = Seite und Zeile. | **Vorlesen** (ie + Doppelkons.) |
| 4 — Wahl B | *Welches Buch zuerst entschlüsseln?* → Hinweis in den Archivraum | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Der „heimliche Umräumer" hinterlässt eine Warnung — voller Fehler. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Der freundliche Schulwart erklärt sein altes Ordnungssystem. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* eine versteckte Dankesbotschaft im ältesten Buch. | **Vorlesen** |

**Beispiel-Vorlesetext (Szene 1):**
> Gleich am ersten Schultag nach den Ferien entdeckte Mia etwas Seltsames. In der Schulbibliothek standen die Bücher anders als sonst — als hätte sie jemand über Nacht vertauscht. Zwischen zwei Bänden steckte ein zusammengefalteter Zettel. „Schaut euch das an", sagte Mia leise zu Ben. Frieda hob die Nase und schnüffelte aufgeregt am Regal. Ben grinste. „Das schreit ja förmlich nach einem Fall für uns drei."

**Fälscher-Notiz (Szene 5):**
> Achtung! Ich räume die Bücehr jede Nacht um, und niemand kann mich aufhalten. Auf dem regal im Lesesaal liegt schon vile durcheinander. Hört auf zu suchen — sonst ist morgen ales anders. Der heimliche Umräumer.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| Bücehr | Bücher | hörbar | lesen_oder_markieren |
| regal | Regal | großschreibung | markieren |
| vile | viele | ie | markieren |
| ales | alles | vokallänge | markieren |

---

## Fall 2 — Der Fall im Wiener Prater
**Schauplatz:** Wiener Prater — Ringelspiel, Riesenrad, Geisterbahn.
**Ziel-Muster:** Dehnungs-h, ck (+ v/f).
**Prämisse:** Beim Ringelspiel verschwinden über Nacht die Hauptgewinne; ein Zettel behauptet, ein Gespenst treibe sein Unwesen. Auflösung: Ein neuer Mitarbeiter hat die Preise nur ins Lager geräumt — ein Missverständnis mit dem Lieferanten.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Beim Ringelspiel fehlen die großen Plüschtiere; daneben klebt ein Zettel. | **Vorlesen** |
| 2 — Wahl A | *Den Schausteller fragen* **/** *Spuren bei der Geisterbahn suchen* → Frieda nimmt eine Schleifspur auf | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis am Riesenrad. | **Vorlesen** (Dehnungs-h + ck) |
| 4 — Wahl B | *Geisterbahn oder Schießbude zuerst?* → Spur zum Lager | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Der „Plagegeist" warnt alle, nach Hause zu gehen — fehlerhaft. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Der neue Mitarbeiter klärt das Lager-Missverständnis auf. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* eine Freifahrt als Dankeschön. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Hört gut zu! In der Geisterban geht ein echtes Gespenst um. Jede Nacht stiehlt es einen Preis fon eurem Riesenrda. Wer noch hierbleibt, hat kein Glük mehr. Geht nach Hause! Euer Plagegeist.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| Geisterban | Geisterbahn | dehnungs-h | markieren |
| fon | von | v/f | markieren |
| Riesenrda | Riesenrad | hörbar | lesen_oder_markieren |
| Glük | Glück | vokallänge | markieren |

---

## Fall 3 — Die verschwundene Mehlspeise
**Schauplatz:** eine Wiener Konditorei, kurz vor einem Mehlspeisen-Wettbewerb.
**Ziel-Muster:** ß/ss, tz (+ Auslaut d/t).
**Prämisse:** Das Geheimrezept für die Marillen-Topfentorte ist verschwunden, dazu ein frecher Zettel. Auflösung: Der Lehrling hatte das Rezept nur zum Abschreiben mitgenommen — das Original war hinter den Kasten gerutscht.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Ben entdeckt einen frechen Zettel: Das Geheimrezept ist weg. | **Vorlesen** |
| 2 — Wahl A | *Den Lehrling fragen* **/** *Die Backstube absuchen* → Frieda folgt einer Mehlspur | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis auf einem Bestellzettel. | **Vorlesen** (ß/ss + tz) |
| 4 — Wahl B | *Kühlraum oder Vorratskammer?* → Spur zum Kasten | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Ein „guter Freund" verhöhnt den Konditor — voller Fehler. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Der Lehrling gesteht verlegen; das Original taucht hinter dem Kasten auf. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* ein Stück Torte fürs Trio. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Na, sucht ihr euer Rezept? Eure Torte ist viel zu süs und gewinnt heuer keinen Preis. Nicht einmal euer Brod gelingt euch! Auf dem Plaz vor der Konditorie lacht schon die ganze Stadt. Gebt auf! Ein guter Freund.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| süs | süß | vokallänge | markieren |
| Brod | Brot | auslaut | markieren |
| Plaz | Platz | vokallänge | markieren |
| Konditorie | Konditorei | hörbar | lesen_oder_markieren |

---

## Fall 4 — Aufregung im Tiergarten Schönbrunn
**Schauplatz:** Tiergarten Schönbrunn.
**Ziel-Muster:** ie, Doppelvokal (+ das/dass).
**Prämisse:** Ein Aushang behauptet, gefährliche Tiere seien ausgebrochen. Frieda nimmt sofort eine Fährte auf. Auflösung: Das vermisste Tier war nur bei der Tierärztin zur Untersuchung; der Aushang war ein dummer Scherz.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Ein Aushang sorgt für Aufregung: Ein Tier sei entkommen. Frieda wird unruhig. | **Vorlesen** |
| 2 — Wahl A | *Die Tierpflegerin fragen* **/** *Das Gehege untersuchen* → Frieda nimmt die Fährte auf | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis an der Fütterungstafel. | **Vorlesen** (ie + Doppelvokal) |
| 4 — Wahl B | *Winterhaus oder Tierambulanz?* → Spur zur Tierärztin | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Ein „Tierfreund" warnt alle Besucher — fehlerhaft. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Das Tier war zur Untersuchung; der Aushang war ein Streich. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* ein Blick hinter die Kulissen der Tierpflege. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Achtung, liebe Besucher! Wir haben gehört, das ein wildes Tir aus dem Zo entkommen ist. Sogar der große Tiegr ist nicht mehr in seinem Gehege. Bleibt zu Hause, hier ist es gefährlich! Der Tierfreund.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| das | dass | das/dass | markieren |
| Tir | Tier | ie | markieren |
| Zo | Zoo | doppelvokal | markieren |
| Tiegr | Tiger | hörbar | lesen_oder_markieren |

---

## Fall 5 — Das Schulfest steht Kopf
**Schauplatz:** das Schulfest (Volksschule).
**Ziel-Muster:** gemischte Wiederholung (+ ver-/vor-, + Komma).
**Prämisse:** Mitten im Fest verschwindet das Klassenmaskottchen, dazu eine Spottnotiz. Auflösung: Kinder aus der ersten Klasse hatten es „ausgeborgt" und im Turnsaal versteckt — gut gemeint, schlecht erklärt.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Beim Schulfest ist das Klassenmaskottchen weg; eine Notiz liegt da. | **Vorlesen** |
| 2 — Wahl A | *Bei den Ständen fragen* **/** *Im Klassenzimmer suchen* → Frieda schnüffelt eine Spur | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis am Tombola-Stand. | **Vorlesen** (gemischt) |
| 4 — Wahl B | *Turnsaal oder Schulhof?* → Spur in den Turnsaal | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Der „Spielverderber" prahlt mit seinem Streich — voller Fehler. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Die Kleinen geben das Maskottchen lachend zurück. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* ein gemeinsames Foto fürs Logbuch. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Liebe Klasse! Euer Schulfset wird heuer ein Reinfall. Euer Maskottchen ist ferschwunden, und ihr findet es nie. Kein Stük Kuchen kein bisschen Spas — alles umsonst geplant! Der Spielverderber.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| Schulfset | Schulfest | hörbar | lesen_oder_markieren |
| ferschwunden | verschwunden | ver/vor | markieren |
| Stük | Stück | vokallänge | markieren |
| *(Lücke)* „Kuchen ◌ kein" | „Kuchen**,** kein" | komma | markieren (Lücke) |
| Spas | Spaß | vokallänge | markieren |

---

## Fall 6 — Rätsel am Rainergymnasium
**Schauplatz:** Rainergymnasium (BG/BRG Wien 5, Rainergasse 39, 1050 Wien — Margareten), Mias erster Schultag am Gymnasium im September.
**Ziel-Muster:** Großschreibung + Dehnungs-h.
**Gastfigur:** **Marie**, eine freundliche Siebtklässlerin, die Mia das große Schulhaus zeigt und mitermittelt.
**Prämisse:** Am schwarzen Brett hängt eine alarmierende „Mitteilung der Direktion": Das Schulanfangsfest sei abgesagt. Marie wird stutzig — die vielen Rechtschreibfehler verraten die Fälschung. Auflösung: Zwei aufgeregte Erstklässler hatten sich einen Streich erlaubt; das Fest findet statt — und Mia hat schon am ersten Tag Freunde.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Mias erster Tag; am schwarzen Brett hängt eine Mitteilung: Das Fest sei abgesagt. | **Vorlesen** |
| 2 — Wahl A | *Marie, die Siebtklässlerin, fragen* **/** *Im Sekretariat nachschauen* → Marie schließt sich an | **Vorlesen** → Konvergenz |
| 3 | Marie zeigt den Schaukasten mit den echten Aushängen — zum Vergleich. | **Vorlesen** (Großschreibung + Dehnungs-h) |
| 4 — Wahl B | *Musiksaal oder Turnsaal zuerst?* → Frieda erschnüffelt am Pausenhof eine Spur | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Die „Mitteilung" genau prüfen — die Fehler entlarven die Fälschung. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Zwei Erstklässler gestehen kleinlaut den Streich; das Fest findet statt. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* Marie zeigt Mia ihren Lieblingsplatz in der Schulbibliothek. | **Vorlesen** |

**Beispiel-Vorlesetext (Szene 1):**
> Mias erster Tag am Rainergymnasium begann aufregend. So viele Gänge, so viele große Schüler — Mia kam sich richtig winzig vor. Am schwarzen Brett im Eingang blieb sie stehen. Auf einem Zettel stand in dicken Buchstaben, das Schulanfangsfest sei abgesagt. „Das stimmt sicher nicht", sagte eine freundliche Stimme hinter ihr. Es war Marie, eine Siebtklässlerin. „Komm, das schauen wir uns genauer an."

**Fälscher-Notiz (Szene 5):**
> Wichtige Mitteilung! Das große fest zum Schulanfang fällt heuer leider aus. Das gilt für das ganze Rainergymansium. Auch der Ausflug komt nicht zustande, und kein Lerer ist heute zu erreichen. Die schule bleibt am Freitag geschlossen. Bitte bleibt zu Hause. Die Direktion.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| fest | Fest | großschreibung | markieren |
| Rainergymansium | Rainergymnasium | hörbar | lesen_oder_markieren |
| komt | kommt | vokallänge | markieren |
| Lerer | Lehrer | dehnungs-h | markieren |
| schule | Schule | großschreibung | markieren |

*Erzählerische Brücke: Dass „die Direktion" den eigenen Schulnamen falsch schreibt und Nomen klein lässt, ist genau der Hinweis, der die Notiz als Fälschung entlarvt.*

---

## Fall 7 — Trubel am Naschmarkt
**Schauplatz:** Wiener Naschmarkt — Marktstände.
**Ziel-Muster:** Vokallänge, ß/ss (phonetischer Schwerpunkt).
**Prämisse:** Am beliebten Standl ist die berühmte Ware durcheinander, dazu ein gehässiger Zettel. Auflösung: eine Verwechslung mit der Lieferung des Nachbarstandes — niemand wollte Böses.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Am Standl ist alles durcheinander; ein Zettel steckt zwischen den Kisten. | **Vorlesen** |
| 2 — Wahl A | *Die Standlbesitzerin fragen* **/** *Den Nachbarstand untersuchen* → Frieda erschnüffelt eine Spur | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis auf einer Preistafel. | **Vorlesen** (Vokallänge + ß/ss) |
| 4 — Wahl B | *Lager oder Lieferwagen?* → Spur zur vertauschten Lieferung | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Ein „ehrlicher Nachbar" macht das Standl schlecht — voller Fehler. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Die Lieferung war vertauscht; die Stände tauschen lachend zurück. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* eine Jause aufs Haus. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Aufgepasst am Naschmarkt! Euer berühmter Käes ist heute schon halb verdorben, weil er viel zu heis gelagert wurde. Eure Nus-Mischung ist viel zu bilig — die kauft niemand. Sucht euch ein neues Standl! Ein ehrlicher Nachbar.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| Käes | Käse | hörbar | lesen_oder_markieren |
| heis | heiß | vokallänge | markieren |
| Nus | Nuss | vokallänge | markieren |
| bilig | billig | vokallänge | markieren |

---

## Fall 8 — Aufruhr in der Schülerzeitung
**Schauplatz:** Redaktion der Schülerzeitung.
**Ziel-Muster:** das/dass, Komma, Groß/klein (+ v/f) — die nicht-phonetischen Punkte gebündelt.
**Prämisse:** Ein gehässiger „Leserbrief" macht die Redaktion fertig und droht, die nächste Ausgabe zu verhindern. Auflösung: Ein schüchterner Schüler wollte eigentlich nur mithelfen und hat sich missverständlich ausgedrückt.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Ben liest einen gehässigen Leserbrief, der die Zeitung schlechtmacht. | **Vorlesen** |
| 2 — Wahl A | *Die Redaktion fragen* **/** *Den Redaktionscomputer prüfen* → Konvergenz | **Vorlesen** |
| 3 | Ein Hinweis im Seitenlayout. | **Vorlesen** (das/dass + Komma) |
| 4 — Wahl B | *Redaktionsraum oder Druckerei?* → Spur zum Absender | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Der „Leserbrief" steckt selbst voller Fehler — das verrät ihn. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Der schüchterne Schüler klärt das Missverständnis auf und darf mitmachen. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* die drei schreiben einen eigenen Artikel. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Liebe Redaktion! Wir glauben das eure zeitung viel zu schlecht ist weil niemand sie liest. Euer letzter artikel war foll Fehler. Hört endlich auf damit! Ein Leser.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| das | dass | das/dass | markieren |
| zeitung | Zeitung | großschreibung | markieren |
| *(Lücke)* „ist ◌ weil" | „ist**,** weil" | komma | markieren (Lücke) |
| artikel | Artikel | großschreibung | markieren |
| foll | voll | v/f | markieren |

*Erzählerische Brücke: Ein „Leser", der über Fehler schimpft und selbst voller Fehler schreibt — die Fehlerjagd entlarvt ihn.*

---

## Fall 9 — Der Kuhschwanz im Klimt-Bild
**Schauplatz:** Oberes Belvedere (Klimt-Saal), Klassenausflug.
**Ziel-Muster:** ver-/vor-, Auslaut (d/t).
**Prämisse:** Vor Gustav Klimts „Bauernhaus mit Birken" (1900) — Wiese, ein winziges weißes Haus am Horizont und eine ganz dünne Birke — streiten Mia und Ben: Ist die schmale Form wirklich eine Birke, oder (Bens kühne Theorie) ein Kuhschwanz, der sich ins Bild verirrt hat? Da liegt plötzlich ein Zettel, der behauptet, das ganze Bild sei eine Fälschung. Auflösung: Das Bild ist echt, die „dünne Form" ist Klimts junge Birke (die Museumsführerin erklärt seine Birkenbilder), und der Zettel war ein Scherz aus dem Kinder-Kunstklub des Museums.

| Szene | Inhalt | Mechanik |
|---|---|---|
| 1 — Hook | Im Klimt-Saal streiten Mia & Ben: Birke oder Kuhschwanz? Dann taucht der „Fälschungs"-Zettel auf. | **Vorlesen** |
| 2 — Wahl A | *Die Museumsführerin fragen* **/** *Das Bild ganz genau betrachten* → Konvergenz | **Vorlesen** → Konvergenz |
| 3 | Ein Hinweis auf dem Bildschild neben dem Gemälde. | **Vorlesen** (ver-/vor- + Auslaut) |
| 4 — Wahl B | *Weiter im Klimt-Saal* **/** *Hinaus in den Belvedere-Garten* → Frieda erschnüffelt dort eine Spur | **Vorlesen** → Konvergenz |
| **5 — Fälscher-Notiz** | Der „Unbekannte" behauptet, das Bild sei falsch — voller Fehler. | **Fehlerjagd** |
| 6 — Wahl C | *Wen sprechen wir an?* → Konvergenz | **Vorlesen** |
| 7 — Auflösung | Das Bild ist echt; die schmale Form ist eine junge Birke. Der Zettel war ein Streich aus dem Kunstklub. | **Vorlesen** |
| 8 — Bonus | *(nur bei allem grün)* die drei malen selbst ein „Birke oder Kuhschwanz?"-Bild. | **Vorlesen** |

**Fälscher-Notiz (Szene 5):**
> Aufgepasst im Belvedere! Dieses Bilt von Kilmt ist nur eine Fälschung. Das echte habe ich vor Jahren forne im Lager versteckt — für immer ferloren. Und schaut genau hin: Der Baum ist in Wahrheit ein Kuhschwanz! Ein Unbekannter.

| gezeigt | richtig | Klasse | Methode |
|---|---|---|---|
| Bilt | Bild | auslaut | markieren |
| Kilmt | Klimt | hörbar | lesen_oder_markieren |
| forne | vorne | ver/vor | markieren |
| ferloren | verloren | ver/vor | markieren |

*Sachhinweis: „Bauernhaus mit Birken" (Gustav Klimt, 1900) hängt tatsächlich im Belvedere — schöne Brücke zu echtem Wiener Kulturgut; im selben Haus hängt auch „Der Kuss".*

---

*Hinweis zur Erweiterung: Pro Fall lassen sich die Szenen 2a/2b, 4a/4b usw. als kurze Markdown-Dateien ausschreiben (Schema wie `stories/fall-01-bibliothek/`). Weitere Fälle sind über den Markdown-+-LLM-Autorenweg leicht nachzulegen — die Fälscher-Notizen oben sind bereits einsatzfertig und als `proofread_errors` in `graph.yaml` übertragbar. Bei Komma-Fehlern wird statt eines Wortes die **Lücke** zwischen zwei Wörtern markiert.*
