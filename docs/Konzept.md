# Konzept: „Club der Spürnasen" — Vorlese-Detektiv als Lern-App

*Interaktive Detektivgeschichte mit phonetischer Vorlese-Bewertung **und** Korrekturlese-Training für eine 10-jährige Leserin (4. Klasse Volksschule).*

> **Update v2 (gegenüber v1):**
> - Korrekturlesen ist jetzt ein **gleichwertiges Kern-Ziel**, nicht mehr ein optionaler Zusatz.
> - Zwei **gekoppelte Mechaniken**: *Vorlesen* (Flüssigkeit) **+** *Fehlerjagd* (die „Fälscher-Notiz").
> - Neu: **Drei-Klassen-Modell der Rechtschreibfehler** — welche Erkennungsmethode funktioniert bei welchem Fehlertyp.
> - Neu: das Implementierungsdetail **„akustische Distanz statt ASR-Transkription"** für die lautgetreue Fehlerprüfung.

---

## 0. Kurzfassung (TL;DR)

Die App verfolgt **zwei Ziele mit zwei gekoppelten Mechaniken**:

1. **Vorlesen → Leseflüssigkeit & Laut-Buchstaben-Bindung.** Korrekt geschriebener Text, sie liest laut, jedes Wort wird grün/gelb/rot bewertet (phonetisch).
2. **Fehlerjagd → Korrekturlesen.** Eine „gefälschte Nachricht" mit eingebauten Rechtschreibfehlern; sie muss die Fehler **finden** (antippen) und ausgewählte sogar **lautgetreu vorlesen**. Sofort danach werden die korrekten Schreibweisen gezeigt.

**Der zentrale Knackpunkt, der das Design bestimmt:** Viele deutsche Rechtschreibfehler **klingen vorgelesen genau wie das richtige Wort**. Deshalb wird jeder Fehler der passenden Methode zugeordnet (Abschnitt 3): laut-verändernde Fehler kann sie *vorlesend* jagen, vokallängen- und stumme Fehler nur durch *Markieren*. Das Markieren ist dabei der **deterministisch prüfbare, regelunabhängige Rückhalt** — kein ML, daher der zuverlässigste Teil des ganzen Systems.

**Technik in einem Satz:** PC-first als lokale **Web-App** (Python/FastAPI-Backend + Browser-Frontend, SQLite), phonetische Bewertung **lokal über `torchaudio`** (CPU genügt, Stimme bleibt am Gerät → DSGVO), **kein Live-LLM für das Kind** — Geschichten als versionierte Markdown-Dateien, LLM nur als dein Autoren-Werkzeug. Wächst ohne Umbau zu *online* (Backend deployen) und *Tablet* (PWA).

**Wichtigster Rat:** Bau zuerst **Phase 0** (Abschnitt 7) — ein Wegwerf-Skript, das prüft, ob (a) die Flüssigkeits-Bewertung bei der Stimme deiner Tochter zuverlässig trennt und (b) die lautgetreue Fehlerprüfung für die *hörbaren* Fehler funktioniert. Das entscheidet, welche Fehler über welche Methode laufen. Das Markieren braucht keine Validierung (deterministisch).

**Hardware:** günstiges USB-Headset (~20–30 €) — wegen konstantem Mund-Mikro-Abstand und wenig Raumlärm, nicht wegen High-End-Klang.

---

## 1. Prinzipielle Bewertung des Konzepts

### Was stark ist
- **Vorlesen + sofortiges Wort-Feedback** ist didaktisch wertvoll und zuhause kaum anders objektiv zu bekommen.
- **Narrative Einbettung** (Detektivfall, Verzweigungen) verwandelt Wiederholung in Spielfortschritt — der Motivations-Hebel von Apps wie Anton.
- **Zwei Skills statt einem:** durch die gekoppelten Mechaniken trifft die App beide Ziele — Leseflüssigkeit *und* Korrekturlesen.

### Der entscheidende Zusammenhang — und seine Grenze
Phonetische Bewertung misst, *wie etwas klingt*, nicht *was geschrieben steht*. Daraus folgt ein differenziertes Bild (kein pauschales „geht nicht"):

- **Lautgetreues Vorlesen einer Falschschreibung kann ein echtes Korrektur-Signal sein** — wenn die Referenz das *richtige* Wort ist und du prüfst „hat sie das *richtige* Wort gesagt? → dann hat sie nicht genau hingeschaut". Liest sie „Tihsc" als irgendetwas, das **nicht** wie „Tisch" klingt, hat sie nachweislich die Buchstaben dekodiert. Das ist ein legitimer, aktiver Korrekturlese-Mechanismus.
- **Aber er funktioniert nur bei einem Teil der Fehler.** Bei vokallängen- und stummen Fehlern (siehe Abschnitt 3) klingt die Falschschreibung **identisch** zum richtigen Wort — da ist Audio prinzipiell blind.

**Fazit:** Das Konzept ist tragfähig und adressiert beide Ziele. Der Schlüssel ist nicht „eine perfekte Bewertung", sondern **jeden Fehlertyp der Methode zuzuordnen, die ihn zuverlässig erkennt** — phonetisch dort, wo es hörbar ist, und durch Markieren überall sonst.

---

## 2. Didaktische Analyse

### Was bei deiner Tochter vermutlich passiert
Geübte Leser lesen **lexikalisch/ganzheitlich**: Das Gehirn erkennt das Wortbild und „repariert" Abweichungen automatisch. Das ist ein **Zeichen von Lesekompetenz**, kein Defizit — es macht schnelles, sinnentnehmendes Lesen erst möglich. Der Preis: Beim *Korrekturlesen* übersieht man Fehler, weil man liest, was gemeint ist, nicht, was dasteht. (Passiert auch Erwachsenen ständig.) Dass keine Legasthenie-Zeichen vorliegen, passt genau dazu. Wichtig: Die Zielwörter („alles", „immer", „Tisch") kann sie ohnehin richtig schreiben — du trainierst also **Aufmerksamkeit**, nicht das Schreiben selbst.

### Was die beiden Mechaniken trainieren
- **Vorlesen (korrekter Text):** Decodier-Genauigkeit, Artikulation, Graphem-Phonem-Korrespondenz (Schrift → Laut), Leseflüssigkeit, Selbstvertrauen. Sie nimmt dabei **richtige Wortbilder** auf.
- **Fehlerjagd (Fälscher-Notiz):** bewusstes Hinschauen auf orthografische Details — genau die Fähigkeit, die fehlt. Das **„lies exakt, was dasteht"** zwingt zu Buchstabe-für-Buchstabe-Decodierung und durchbricht das ganzheitliche Auto-Korrigieren.

### Antonias Schwerpunkte — das Lern-Curriculum
Antonias eigenes Merkblatt ist die **inhaltliche Grundlage** für die Fälle und Fälscher-Notizen. Grundsatz: **alles ist gleichwertig** — Vorlesen und Fehlerjagd ebenso wie die acht Punkte untereinander; keiner steht über dem anderen. Gewichtet wird allein die **Übungs-Dosis**: **Fokus (nicht Exklusivität) auf das Phonetische** — die laut-/lautlängen­bezogenen Punkte und vor allem die lautgetreue „lies genau, was dasteht"-Mechanik. Die nicht-phonetischen Punkte (Groß/klein, Beistrich, v/f, das/dass, ver-/vor-, Auslaut) sind **vollständig dabei** und werden übers **Markieren** geübt.

**Die acht Schwerpunkte:**
1. **Groß oder klein?** — Satzanfang groß; Nomen-Check (Begleiter *der/die/das/ein*? anfassbar/sichtbar?); Endungen *-ung/-heit/-keit/-schaft/-nis* sind immer Nomen (die Übung, die Freiheit). → *Großschreibung, audio-blind → markieren.*
2. **Beistrich-Check** — Aufzählungen (Hunde, Katzen, Mäuse); vor *weil/dass/wenn/aber* fast immer ein Komma. → *Zeichensetzung, audio-blind → markieren (eigene Interaktion, s. u.).*
3. **Ende-Check (verlängern)** — Auslaut hörbar machen über die Mehrzahl: Hund→Hunde (d), Berg→Berge (g). → *Auslautverhärtung, audio-blind (Hund/Hunt klingen gleich) → markieren.*
4. **v oder f?** — Vogel-V-Wörter merken (Vogel, Vater, viel, voll, von, vor, vielleicht, Vorsicht); sonst f. → *audio-blind (v = f-Laut) → markieren.*
5. **i oder ie?** — langes i meist *ie* (Spiel, dies); Tiger-Wörter als Ausnahme (Tiger, Igel, Maschine, Kino, Benzin). → *meist audio-blind → markieren.*
6. **das oder dass?** — Ersatzprobe *dieses/jenes/welches*: passt → *das*; passt nicht → *dass*. → *audio-blind (gleich klingend) → markieren.*
7. **Vorsilben ver-/vor-** — „fer…/for…" am Anfang gibt es nicht; immer mit v (verlaufen, vorlesen). → *audio-blind → markieren.*
8. **Vokal-Check (kurz/lang)** — kurz = Doppel-Bremse (ll, mm, nn, rr, tt, ff, pp; Spezial ck, tz; scharfes *ss*); lang = ein Buchstabe (l, m, n …; summendes *s*; scharfes *ß*). → *Vokallänge — markieren (lautgetreues Lesen nur eingeschränkt, da bloß die Vokaldauer variiert).*

**Leitidee (die Hoffnung dahinter):** Intensives, *exaktes* Vorlesen soll die Gewohnheit aufbauen, genau auf das geschriebene Wort zu schauen — der erhoffte **Aha-Effekt** „Ich muss wirklich lesen, was dasteht", der dann aufs Korrekturlesen allgemein abfärbt. Daher der Phonetik-Fokus. Das ist eine **plausible, aber zu beobachtende Annahme** — ob Antonias Korrekturlesen besser wird, lässt sich im Eltern-Dashboard (Abschnitt 3) verfolgen.

**Interaktions-Erweiterung für Beistriche:** Komma-Fehler markiert man nicht am *Wort*, sondern an der *Lücke*. Die Fehlerjagd braucht dafür zusätzlich zum Wort-Antippen einen kleinen „Komma einsetzen/streichen"-Modus (zwischen zwei Wörter tippen).

### Auflösung mit Regel-Bezug
Sobald die richtige Schreibung erscheint (die **Auflösung** der Fehlerjagd), wird **jeder Fehler direkt mit der passenden Merkregel erklärt** — also nicht nur das richtige Wort gezeigt, sondern das *Warum* aus Antonias Merkblatt benannt: eine kurze, kindgerechte Begründung, die genau auf die zutreffende der acht Regeln verweist. Mapping Fehlerklasse → Merkregel:

| Fehlerklasse | Merkregel |
|---|---|
| `großschreibung` | **1** — Groß oder klein? (Nomen groß) |
| `komma` | **2** — Beistrich-Check |
| `auslaut` | **3** — Ende-Check (verlängern: Hund→Hunde) |
| `v/f` | **4** — v oder f? (Vogel-V-Wörter) |
| `ie` | **5** — i oder ie? (Tiger-Wörter) |
| `das/dass` | **6** — das oder dass? (Ersatzprobe) |
| `ver/vor` | **7** — Vorsilben ver-/vor- |
| `vokallänge` | **8** — Vokal-Check kurz/lang (Doppel-Bremse) |

Phänomene **außerhalb der acht Punkte** — `dehnungs-h` (Lehrer, Uhr), `doppelvokal` (Zoo, Boot) und reine `hörbar`-Buchstabendreher (Bücehr) — bekommen eine kurze **Klartext-Begründung** statt einer (sonst falschen) Regel-Nummer. Technisch trägt dafür jeder Fehler im `graph.yaml` ein Feld **`regel`** (1–8 oder „–") plus einen kindgerechten **`tipp`** (Schema s. Abschnitt 6e). Übersehene Regel-Kategorien landen im Eltern-Dashboard (`proofread_history`).

### Der Umgang mit Falschschreibungen (Interferenz-Sorge — entschärft)
Wiederholte Konfrontation mit Falschschreibungen kann grundsätzlich **orthografische Interferenz** erzeugen (das falsche Wortbild prägt sich mit ein). In *diesem* Design ist das Risiko jedoch klein, weil drei mildernde Bedingungen zusammenkommen:
1. **Aktives Suchen** statt passiven Lesens (sie verarbeitet die Wörter kritisch, nicht als Modelle).
2. **Sofortige Korrektur** (richtige Form direkt nach dem Markieren).
3. **„Fälscher"-Rahmung** — eine *gefälschte* Nachricht signalisiert psychologisch „das ist FALSCH", das Gegenteil davon, Fehler als normalen Text zu zeigen.

Dazu geht es um Wörter, die sie schon korrekt schreiben kann. Null ist das Risiko nie — deshalb die harte Regel: **Falschschreibungen ausschließlich in der klar markierten Fälscher-Notiz, niemals in der Vorlese-Geschichte.**

### Motivation (Selbstbestimmungstheorie)
- **Autonomie** → Verzweigungen/Entscheidungen.
- **Kompetenz** → Wort-Feedback + Punkte + Belohnungen.
- **Zugehörigkeit** → wiederkehrende Figuren.

**Kautelen:** sanftes statt hartes Gating; „Rot" freundlich rahmen („Der Hinweis ist noch verschwommen — lies ihn genau"); Mikro-Lernschleife (rotes Wort antippen → korrekte Aussprache hören → nochmal lesen).

---

## 3. Detailkonzept (die zwei gekoppelten Mechaniken)

### Mechanik A — Vorlesen (Leseflüssigkeit)
1. Szene erscheint, **korrekt geschrieben** (1 kurzer Absatz).
2. Sie tippt „Vorlesen" → Aufnahme.
3. Backend bewertet → **jedes Wort grün/gelb/rot** (Referenz = das angezeigte richtige Wort; Belohnung = akustische Nähe).
4. Gelbe/rote Wörter sind antippbar → korrekte Aussprache hören (TTS).
5. Mindestschwelle erreicht → weiter; sonst die markierten Sätze erneut.

### Mechanik B — Fehlerjagd (Korrekturlesen, die „Fälscher-Notiz")
Eine kurze Notiz **mit eingebauten Fehlern**, klar als Fälschung gerahmt:
1. „Der Fälscher hat sich verraten — finde die falsch geschriebenen Wörter!"
2. **Markieren:** sie tippt die Fehler an → **deterministische Prüfung** gegen die eingebauten Fehler. Funktioniert bei **allen** Fehlertypen.
3. **Optional, nur bei hörbaren Fehlern:** „Sprich aus, was der Fälscher geschrieben hat." → lautgetreue Prüfung (siehe unten). Vertieft die hörbaren Fälle und schlägt die Brücke zwischen beiden Skills.
4. **Korrektur:** nach dem Abschicken werden die richtigen Schreibweisen gezeigt.

### Das Drei-Klassen-Modell der Fehler (das Herzstück der Fehlerauswahl)

| Fehlerklasse | Beispiel (gezeigt → richtig) | Hörbarer Unterschied? | Erkennung |
|---|---|---|---|
| **Hörbar** (laut-verändernd: Dreher, falsche/zusätzliche Konsonanten) | „Tihsc" → Tisch | ja, klar | **Vorlesen *oder* Markieren** |
| **Knifflig** (Doppelkonsonant → Vokallänge) | „ales" → alles, „Sone" → Sonne | nur Vokaldauer (kurz/lang) | **Markieren** (Vorlesen nur eingeschränkt, riskant) |
| **Unhörbar/homophon** (Dehnungs-h, viele ie-Fälle) | „Zal" → Zahl, „Libe" → Liebe | **nein, identisch** | **nur Markieren** |

**Konsequenz für die Inhalte:** Jeder eingebaute Fehler wird nach seiner Klasse mit der passenden Methode getaggt (siehe Story-Format, Abschnitt 6e). Dein ursprüngliches „ales/alles" liegt in der mittleren Klasse — also primär per Markieren. Mehrere Regeln vom Merkblatt (Doppelkonsonant, Dehnungs-h, ie) fallen in die unteren zwei Klassen.

### Score → Farbe & Schwellen (für Mechanik A)
Der lokale Scorer liefert pro Wort 0–100 (Alignment-/Konfidenzwert). Mapping z. B. **grün ≥ 80**, **gelb 55–79**, **rot < 55** — **empirisch zu kalibrieren** (Phase 0) und für Kinder bewusst milder (Microsoft selbst rät dazu). Ausgelassene/zusätzliche Wörter erkennt man über fehlende/zusätzliche Einträge im Alignment.

### Sanftes Gating, Punkte, Dashboard
- **Mindestschwelle** zum Weiterkommen, **Bonus** (Extra-Punkte/Geheimpfad) für sehr gutes Lesen — nicht hart blockieren.
- Punkte → Belohnung: **Detektiv-Avatar ausstatten** oder **Fall-Pinnwand/Puzzle** füllen.
- **Eltern-Dashboard:** Da Wort-Scores *und* Fehlerjagd-Ergebnisse gespeichert werden, lässt sich zeigen, *welche Regel-Kategorien* sie noch oft übersieht (z. B. „Dehnungs-h: 3 von 8 gefunden").

---

## 4. Story-Konzept

### Welt & Ton
Heimeliger Kinder-Krimi im **Ton von „Die drei !!!"** — warmherzig, freundschaftsbetont, mädchengeführt; **neugierig, nie gruselig** und bewusst leichter als die kriminalistischeren *Die drei ???* oder *TKKG*. Verschwundene Gegenstände, geheime Botschaften, gefälschte Nachrichten, Missverständnisse, die sich gut auflösen; keine Gewalt, keine echten Bösewichte. **Eigene Figuren** (kein fremdes Personal), **Schauplätze in Wien und Umgebung** (Schulbibliothek, Prater, Konditorei, Tiergarten Schönbrunn, Schulfest) — vertraut für Antonia.

### Die Ermittlerinnen: Mia, Ben & Frieda (eigenes Trio, „Club der Spürnasen")
Ein **eigenes Detektiv-Trio** im Geist der !!! — Stärken passend zu den zwei Mechaniken:
- **Mia (10)** — Anführerin & Identifikationsfigur, scharfe Beobachterin, führt das **Spürnasen-Logbuch**. → **trägt die Fehlerjagd** (entdeckt, was am Wortbild nicht stimmt).
- **Ben (11)** — der Tüftler: Gadgets, Technik, Humor; öffnet notfalls mit Werkzeug ein Schloss. → **technische Hinweise, Menschen ausfragen, Auflockerung.**
- **Frieda** — clevere Dackel-Dame mit Wundernase; spricht nicht, hält die Welt geerdet. → **Geruchsspuren & körperliche Hinweise; im Tiergarten die Tier-Verbindung.**
- **Erwachsene unterstützen — gelöst wird vom Trio.**

### Sprache: österreichisches Standarddeutsch (verbindlich)
Alle Texte in **österreichischem Standarddeutsch** auf **Volksschulniveau** (wie im österreichischen Lehrplan vorgesehen) — **kein Bundesdeutsch, kein Dialekt/Wienerisch**.
- **Verwenden:** das Cola, einen *Einser*/Zweier (Schulnoten), die Karotte, die Grapefruit, die Semmel, das Sackerl, die Jause, der Bub, die Stiege, der Kasten, der Sessel, Schlagobers, Topfen, Palatschinke, heuer; „es hat *geläutet*"; Perfekt mit *sein*: „ich bin gesessen/gestanden/gelegen"; „schauen" (nie „gucken"); Grüße „Servus" / „Grüß dich", „Grüß Gott" (Erwachsene).
- **Vermeiden:** die Cola, eine Eins, Möhre, Pampelmuse, Brötchen, Tüte, Junge, Treppe, Sahne/Quark, Pfannkuchen, „gucken", „lecker", „klingeln", „Tschüss" — und **kein Artikel vor Vornamen** („die Mia").
- **Nicht** ins Dialektale kippen (kein „leiwand", „Oida", „gschwind"). Standardsprachlich, nur die österreichische Variante.

(Diese Regel gilt für **alle** Inhalte, auch für später vom LLM erzeugte Fälle; sie steht zusätzlich kurz in `CLAUDE.md`.)

### Falllänge & Lesepensum (4. Klasse)
- **Szene:** 3–6 Sätze, ~**40–80 Wörter**.
- **Fall:** **8–12 Szenen**, gesamt ~**350–550 Wörter**.
- **Sitzung:** ~**10–15 Minuten**.

### Pfade & Verzweigung — die wichtigste Struktur-Entscheidung
**Keine Voll-Verzweigung** (2ⁿ Pfade explodieren als Einzelautor). Stattdessen **„Branch & Bottleneck" (string of pearls):** Entscheidungen verzweigen 1–2 Szenen und **laufen wieder zusammen**.

Pro Fall: **8–12 Szenen**, **2–3 binäre Entscheidungspunkte** (konvergierend), **1 Hauptauflösung** + optional **1 Bonus-Szene** (nur bei durchgehend grünem Lesen). Kopplung: Optionen erscheinen ab Mindestschwelle; sehr gutes Lesen schaltet die *bessere* Option frei (sanft).

### Die neun Fälle
Neun ausgearbeitete Fälle — je mit Beat-Sheet, Entscheidungspunkten, **Fälscher-Notiz (mit klassifizierten Fehlern)** und Ziel-Rechtschreibmustern — liegen in **[`docs/Faelle.md`](Faelle.md)**. Die Notizen sind **phonetik-dominant** (Übungs-Fokus), die nicht-phonetischen Punkte sind eingestreut; Fall 8 & 9 widmen sich ihnen stärker. Eine Abdeckungstabelle aller acht Merkblatt-Punkte steht in `Faelle.md`.
1. **Das Geheimnis der Schulbibliothek** — Doppelkonsonant + ie (+ Groß/klein)
2. **Der Fall im Wiener Prater** — Dehnungs-h + ck (+ v/f)
3. **Die verschwundene Mehlspeise** (Konditorei) — ß/ss + tz (+ Auslaut)
4. **Aufregung im Tiergarten Schönbrunn** — ie + Doppelvokal (+ das/dass)
5. **Das Schulfest steht Kopf** — gemischte Wiederholung (+ ver-/vor-, + Komma)
6. **Rätsel am Rainergymnasium** — Großschreibung + Dehnungs-h (Gymnasium-Start, mit Gastfigur Marie)
7. **Trubel am Naschmarkt** — Vokallänge + ß/ss (phonetischer Schwerpunkt)
8. **Aufruhr in der Schülerzeitung** — das/dass + Komma + Groß/klein (+ v/f); nicht-phonetische Punkte gebündelt
9. **Der Kuhschwanz im Klimt-Bild** (Belvedere) — ver-/vor- + Auslaut

Vorangestellt ist **Fall 0 — ein Tutorial** (`stories/fall-00-tutorial/`): Es stellt das Trio vor, erklärt beide Mechaniken und führt die **Stimm-Eichung** durch (individuelles Training der Phonetikerkennung — liefert die persönliche Basislinie für die grün/gelb/rot-Bewertung, vgl. Abschnitt 7 / Phase 0).

Jeder Fall folgt demselben Schema: **Hook → 2–3 konvergierende Entscheidungen → Fälscher-Notiz (Fehlerjagd) → Auflösung → optionale Bonus-Szene.** Die Fälscher-Notiz ist der Ort, an dem beide Mechaniken zusammenkommen.

### Inhaltliche Skalierung
Jede Szene wird mit **Ziel-Mustern** getaggt (z. B. „Szene 3 drillt `ie` + Doppelkonsonant"), Fehlerjagd-Fehler zusätzlich mit ihrer **Erkennungsklasse** und ihrer **Merkregel** (s. „Auflösung mit Regel-Bezug"). So behältst du didaktische Kontrolle.

**Mitwachsen in zwei Richtungen.** Fälle können später (a) **längere Vorlese-Texte** bekommen — mehr Sätze oder ganze Absätze pro Szene, wenn Antonia sicherer liest — und (b) **mehr Schritte**: mehr Szenen, mehr Entscheidungspunkte und **mehr als eine Fälscher-Notiz pro Fall** (mehrere Fehlertexte hintereinander). Das Format trägt beides **ohne Änderung**: einfach weitere Szenen-Dateien anlegen und im `graph.yaml` zusätzliche Knoten ergänzen — längere `mode: vorlesen`-Texte bzw. weitere `mode: fehlerjagd`-Knoten mit jeweils eigenem `proofread_errors`-Block. So lässt sich Länge *und* Schwierigkeitsgrad mit ihr mitsteigern, ohne die Engine anzufassen.

---

## 5. Designkonzept & Bildsprache

### Gesamtanmutung
**Anton-artig:** flach, freundlich, runde Formen, hell aber **ruhig** (nicht grell), viel Weißraum.

### Typografie (entscheidend)
- **Lesetext groß** (~22–26 px), Zeilenabstand ~1.5, kurze Zeilen.
- **Gut lesbare humanistische Schrift** — **Andika** (für Alphabetisierung entworfen), **Lexend** oder **Atkinson Hyperlegible**; OpenDyslexic optional.
- **Cremefarbener Hintergrund** (weniger Blendung), hoher aber nicht harter Kontrast — legasthenie-freundlich = generell gute Praxis.

### Farb- & Interaktionssystem (mit Selbstbeschränkung)
- **Rot/Gelb/Grün NUR für das Vorlese-Feedback** reservieren. UI sonst in **ruhigem Blau/Petrol + warmen Neutraltönen**, damit Feedback „poppt" und nicht mit Deko verwechselt wird.
- **Markieren ≠ Vorlese-Farben:** das Antippen in der Fehlerjagd nutzt eine **andere Affordanz** (z. B. Wort einkringeln/auswählen), damit es nicht mit Grün/Gelb/Rot kollidiert.
- **Fälscher-Notiz visuell abgesetzt** (z. B. „zerknittertes Papier"/anderer Hintergrund), damit klar ist: *Das ist das verdächtige Dokument* — verstärkt das „diese Fehler sind falsch".

### Ikonografie & Metaphern
Lupe, Fußspuren, Notizbuch/Akte, **Korkpinnwand mit roter Schnur** als Fortschritts-/Fallkarte (verbundene Hinweise = gelöste Szenen). „Akten"-Look für die Fallauswahl.

### Belohnung & Sound
Fall-Pinnwand/Puzzle füllt sich (doppelt als Fortschrittsbalken) oder Avatar-Detektiv ausstatten (Hut, Mantel, Lupe). Leiser, freundlicher Erfolgs-Chime; niemals harter „Falsch"-Buzzer.

### Bildstrategie: Titelbilder & Szenenbilder
- **Titelbilder (pro Fall, empfohlen):** je ein Bild für die Fallauswahl, gestaltet als **Aktendeckel**. **Schauplatzbetont** (Bibliothek, Riesenrad, Konditorei, Schönbrunn, Schulfest, Gymnasium), Figuren höchstens klein/silhouettiert — wirkt wie atmosphärische „Fall-Cover" und umgeht die Figuren-Konsistenz. Nur 6 Bilder → gut machbar, ideal für **Claude Design**.
- **Szenenbilder (pro Seite, optional — Belohnung statt Beiwerk):** **kein** inhaltlich verräterisches Bild *neben* dem Lesetext, sonst „liest" das Kind das Bild statt der Wörter (kontraproduktiv, besonders auf der Fehlerjagd-Seite). Stattdessen erscheint das Szenenbild **erst nach gutem Vorlesen** als freigeschaltetes Comic-Panel → Anreiz statt Krücke, fügt sich in die Belohnungsschleife (die Pinnwand füllt sich mit diesen Panels). Während des Lesens höchstens **dekorativ** (Eck-Motiv, „Akten"-Kopfleiste), nie Szeneninhalt.
- **Produktion — Figuren-Konsistenz ist der Knackpunkt:** ~48 Szenenbilder mit gleichbleibenden Mia/Ben/Frieda sind aufwendig (KI driftet ohne Referenz). Grundlage daher: **Stil-Guide + Charakter-Referenzblätter** (einige Posen/Mienen je Figur), egal ob KI oder Illustration. **Eigener Stil**, bewusst nicht an eine bestehende Reihe angelehnt. KI taugt gut für Titel/Atmosphäre, schwieriger für konsistente Figurenszenen (Kuratierung einplanen).
- **Reihenfolge:** Titelbilder zuerst; Szenenbilder als spätere Polish-/Belohnungs-Funktion. **Der Lesekern braucht keine Bilder** → kein Blocker für Phase 0/1.
- **Ablage:** `assets/titles/fall-0X.*` und (optional) `assets/scenes/fall-0X/szene-YY.*`; Verknüpfung über `title_image` (pro Fall) bzw. optional `reveal_image` (pro Szene) in `graph.yaml`.

### Layout pro Bildschirm (mobile-first)
Eine Szene sichtbar; großer „Vorlesen"-Button; klarer **Mikro-Status** (bereit / hört zu / wertet aus); dann Feedback bzw. Markier-Interaktion; dann Entscheidungen.

---

## 6. Implementierungskonzept

### 6a. Grundsatzfrage: Android oder PC?
**Empfehlung: PC-first als lokale *Web-App* (Browser-Frontend + Python-Backend), nicht nativ.** Gründe:
- **Schnellster Bau für dich** (Python ist dein Heimspiel).
- **Browser löst Mikrofon-Aufnahme** plattformübergreifend (`MediaRecorder`/Web Audio).
- **Eine Codebasis, drei Ziele:** dasselbe Frontend wird später *online* (Backend deployen) und *als Tablet-App* (PWA) nutzbar — ohne Neuschrieb.
- **Natives Android (Kotlin/Flutter) erst bei echtem Produkt** (dann nicht Python; On-Device-ML via ONNX/ExecuTorch).

Für ein Kind fühlt sich ein **Tablet** am natürlichsten an — die PWA löst das ohne nativen Aufwand: erst am PC mit Headset entwickeln, später dieselbe App aufs Tablet „installieren".

### 6b. Architektur
```
┌─────────────────────────────┐        ┌──────────────────────────────┐
│  Frontend (Browser, PWA)    │        │  Backend (Python / FastAPI)  │
│  - Szenen rendern           │  HTTP  │  - /profiles  (User)         │
│  - Audio aufnehmen          │ <────> │  - /scene/next               │
│  - Wort-Einfärbung (A)      │  Audio │  - /score/fluency  (A)       │
│  - Markieren (B)            │ ─────> │  - /score/literal  (B)       │
│  - Entscheidungen           │        │  - /proofread/check  (B,det.)│
│  - Belohnung/Avatar         │        │  - /progress, /rewards       │
└─────────────────────────────┘        │   ├─ Scoring (LOKAL, torch)  │
                                        │   ├─ Story-Loader (Markdown) │
                                        │   ├─ TTS (Wort-Wiedergabe)   │
                                        │   └─ SQLite                  │
                                        └──────────────────────────────┘
```

### 6c. Scoring — zwei Verwendungen derselben Engine
- **Mechanik A — Flüssigkeit (Nähe):** Forced-Align gegen das *angezeigte (richtige)* Wort → **hohe** Übereinstimmung = gut (grün). Lokal über `torchaudio.functional.forced_align()` bzw. `torchaudio.pipelines.Wav2Vec2FABundle`. CPU genügt (kurze Clips alignen in ~2 s). **Stimme bleibt am Gerät** (DSGVO).
- **Mechanik B — lautgetreue Fehlerprüfung (Distanz, nur hörbare Fehler):** Hier ist die Logik **umgekehrt**. Du misst die **akustische Distanz zum *richtigen* Wort**:
  - Audio ≈ richtiges Wort („Tisch") → sie hat **auto-korrigiert** → *nicht* genau gelesen.
  - Audio **fern** vom richtigen Wort → literaler Dekodier-Versuch → bestanden.
  - **Wichtig (Stolperfalle):** Das musst du über **akustische Distanz / Forced-Align gegen die Lautfolge des richtigen Worts** bauen, **NICHT über ASR-Transkription** — Whisper & Co. „korrigieren" „Tihsc" beim Transkribieren automatisch zu „Tisch" und liefern ein falsches Ergebnis. Zusätzlich eine **Mindestschwelle**, damit reines Murmeln/Auslassen nicht als „nicht-Tisch" durchrutscht.
- **Markieren (deterministisch, kein ML):** der Rückhalt für *alle* Fehlerklassen — Vergleich der angetippten Wörter mit den eingebauten Fehlern. Zuverlässigster Teil des Systems.
- **Pluggable Scoring-Backend** (`local | azure | speechace`). **Azure** als Alternative: ~33 Sprachen inkl. **Deutsch (de-DE)**, „scripted assessment" = Vorlese-Szenario, ~**1,32 $/Stunde** (5 Gratis-Stunden/Monat) — praktisch gratis für Familiengebrauch. **Aber:** Kinderstimme geht in die Cloud (DSGVO), Prosodie nur en-US. Daher **lokal als Standard**.

### 6d. LLM — bewusst NICHT zur Laufzeit fürs Kind
- **Geschichten = vorgeschriebene, versionierte Markdown-Dateien** (passt zu deiner PartsLedger-/CircuitSmith-Philosophie): keine Latenz/Kosten, **offline**, und **kein unkontrollierter LLM-Output an ein Kind** (Kindersicherheit).
- **LLM = dein Autoren-Werkzeug** (offline): hilft *dir*, Fälle zu schreiben, korrekte Schärfungswörter einzustreuen, Fälscher-Notizen mit passend klassifizierten Fehlern zu generieren, Verzweigungen konsistent zu halten. Provider pluggable per Config.
- **TTS** (Wort vorlesen): pluggable (OS-/Browser-TTS, lokales dt. TTS, oder vorgerendert). Einzelwörter ⇒ billig.

### 6e. Story-Format (Markdown + YAML)
```yaml
# fall-01-bibliothek/graph.yaml
case_id: fall-01
title: "Das Geheimnis der alten Bibliothek"
start: szene-01
scenes:
  szene-01:
    text: szene-01.md
    mode: vorlesen
    target_patterns: ["doppelkonsonant", "ie"]
    choices:
      - { label: "Frau Brandner fragen", goto: szene-02a }
      - { label: "Das Regal untersuchen", goto: szene-02b }
  szene-02a: { text: szene-02a.md, mode: vorlesen, goto: szene-03 }   # Konvergenz
  szene-02b: { text: szene-02b.md, mode: vorlesen, goto: szene-03 }   # Konvergenz
  szene-03:  { text: szene-03.md, mode: vorlesen, target_patterns: ["ie"], ... }

  szene-05:                                   # eine Fälscher-Notiz (mehrere pro Fall möglich)
    text: szene-05.md                         # Notiz-Text mit Fehlern (lautes Vorlesen)
    mode: fehlerjagd
    # regel = passende Merkregel 1–8 für die Auflösung; "–" wenn außerhalb der 8.
    # tipp  = kurze, kindgerechte Begründung, die in der Auflösung erscheint.
    proofread_errors:
      - { shown: "Tihsc", correct: "Tisch", klasse: "hoerbar",     regel: "–", tipp: "Buchstaben vertauscht — genau lesen.", method: "lesen_oder_markieren" }
      - { shown: "ales",  correct: "alles", klasse: "vokallaenge", regel: 8,   tipp: "Kurzer Vokal → Doppel-Bremse (ll).",  method: "markieren" }
      - { shown: "Zal",   correct: "Zahl",  klasse: "dehnungs-h",  regel: "–", tipp: "Langes a mit Dehnungs-h.",           method: "markieren" }
    goto: szene-06

  bonus-01: { text: bonus-01.md, mode: vorlesen, requires: "all_green" }
```
Diff-bar, LLM-freundlich, konsistent mit deinem Markdown-nativen Ansatz. **Mehrere `fehlerjagd`-Knoten pro Fall sind erlaubt** (mehrere Notizen), und `vorlesen`-Texte dürfen beliebig länger werden — das Schema bleibt gleich (s. „Inhaltliche Skalierung").

### 6f. Datenbank (SQLite)
- `profiles` (id, name, avatar_state)
- `cases` (id, title, path) — Metadaten; Inhalt in Markdown
- `progress` (profile_id, case_id, current_scene, completed)
- `score_history` (profile_id, scene_id, word, score, attempt, ts) — Flüssigkeits-Verlauf
- `proofread_history` (profile_id, scene_id, error_id, klasse, gefunden, ts) — **Fehlerjagd-Verlauf fürs Dashboard** (welche Regel-Kategorien werden übersehen?)
- `points`, `unlocked_items`

### 6g. Migrationspfad
- **Online:** dasselbe FastAPI-Backend auf kleinen VPS/Container; Frontend als statische PWA; echte Accounts. Audio dann zum *eigenen* Server (oder reiner Lokal-Modus beibehalten).
- **Tablet/Android:** PWA installieren (sofort) oder mit **Capacitor** verpacken; On-Device-Scoring später via ONNX/ExecuTorch.
- **Nativ (Kotlin):** erst bei Produkt-Ambition.

### 6h. Konkreter Tech-Stack
- **Backend:** Python 3.12, FastAPI + Uvicorn, SQLite (SQLModel/SQLAlchemy), **PyTorch + torchaudio**, `soundfile`/`pydub`.
- **Frontend:** Vite; **vanilla JS** oder leichtgewichtig **Svelte/Preact**; Web-Audio/`MediaRecorder`; PWA-Manifest + Service Worker.
- **LLM-Authoring:** Anthropic/OpenAI SDK (offline), Provider per `.env`.
- **Config:** YAML/`.env` für Provider-Wahl (Scoring, LLM, TTS) + Score-Schwellen.

---

## 7. Roadmap / Phasen

### ⚠️ Phase 0 — Kernrisiken absichern (ein Nachmittag, VOR allem)
Nimm 5–10 echte Vorlese-Clips deiner Tochter auf (geplantes Headset) und prüfe mit einem **Wegwerf-Skript** (`torchaudio`-Forced-Alignment) zwei Dinge:
- **(a) Flüssigkeit:** Trennen die Wort-Scores „flüssig" sauber von „gestockt/falsch"? Schwellen für grün/gelb/rot tunen.
- **(b) Lautgetreue Fehlerprüfung (hörbare Klasse):** Erkennt die **akustische Distanz zum richtigen Wort** zuverlässig, ob sie „Tihsc" literal gelesen oder zu „Tisch" auto-korrigiert hat? Das legt fest, **welche Fehler vorlesend** und **welche nur durch Markieren** laufen.
- **Markieren braucht keine Validierung** (deterministisch) — die Korrekturlese-Funktion steht also auf jeden Fall, unabhängig vom Audio-Ergebnis.

**Ergebnis = GO/NO-GO** und zugleich die Kalibrierung der Methoden-Zuordnung.

### Phase 1 — Vertikaler Durchstich (beide Ziele, minimal)
Eine fest verdrahtete Geschichte, ein Nutzer: **Vorlesen → Wort-Feedback → Re-Read** *plus* eine **Fälscher-Notiz mit Markieren** (deterministisch, kein Extra-ML). Liefert bereits beide Skills.

### Phase 2 — Spiel + lautgetreue Prüfung
Konvergente Verzweigung + sanftes Gating + Belohnung; **lautgetreue Fehlerprüfung** für die hörbare Klasse (braucht die in Phase 0 kalibrierte Distanz-Schwelle).

### Phase 3 — Breite
Mehrbenutzer + mehrere Geschichten + Eltern-Dashboard (Flüssigkeit *und* Fehler-Kategorien) + **Autoren-Workflow** (Markdown + LLM-Assistenz).

### Phase 4 — Online / Tablet
Backend deployen, PWA aufs Tablet.

---

## 8. Werkzeug-Workflow: Claude Design ↔ Claude Code

Beide Werkzeuge ergänzen sich entlang einer klaren Linie: **Claude Design** für *Exploration und visuelle Sprache*, **Claude Code** für den *Bau*. Anthropic hat den Übergang dafür eingebaut — Claude Design bündelt ein fertiges Design in einen **Handoff für Claude Code**.

### Rollenteilung
- **Claude Design** (Research Preview, Canvas + Chat): erkundet Aussehen, Layout und Flow als interaktive Prototypen. Hier entstehen die Bildsprache (Anton-artig + Detektiv), das Farbsystem (Rot/Gelb/Grün nur fürs Feedback), Typografie, Ikonografie (Lupe, Pinnwand + rote Schnur) und ein **Design-System** (Color-Tokens, Schriftgrößen, Spacing, Komponenten). Claude Design kann ein bestehendes Design-System bzw. einen Codebase als Referenz lesen und anwenden.
- **Claude Code** (Terminal, lokales Repo): überführt das Design in den echten **PWA-Frontend + FastAPI-Backend** und verdrahtet die **Logik** — phonetisches Scoring, Story-Engine, Persistenz, lokales Audio/DSGVO.

### Welche Screens in Claude Design entstehen sollten
- **Vorlese-Screen:** Szenentext, Wort-Einfärbung grün/gelb/rot (dezent, z. B. Unterstreichung), Mikro-Status (bereit / hört zu / wertet aus), Re-Read-Aufforderung.
- **Fehlerjagd / Fälscher-Notiz:** Markier-Interaktion (Wörter einkringeln) mit **anderer Affordanz** als die Vorlese-Farben; Notiz visuell abgesetzt (zerknittertes Papier); Korrektur-Anzeige nach dem Abschicken.
- **Belohnung:** Avatar-Ausstattung und/oder Pinnwand-Puzzle.
- **Profil-/Fallauswahl** im „Akten"-Look.
- Querschnitt: lesefreundliche Typografie (groß, Cremehintergrund), **mobile-/Tablet-first** (PWA).

### Der Handoff (der vorgesehene Weg)
Steht ein Screen/Flow in Claude Design, wird er per Befehl als **Handoff-Bundle an Claude Code** übergeben; dort entsteht der Produktionscode, der ans Backend angebunden wird. (Alternativ Export als standalone HTML — als Startgerüst, das Claude Code verfeinert.)

### Single Source of Truth & Synchronität
- Das **Design-System als Datei ins Repo** legen — z. B. `docs/design/` mit `DESIGN.md` + Tokens (CSS-Variablen oder JSON). `CLAUDE.md` darauf verweisen.
- Da Claude Design einen **Codebase als Referenz lesen** kann, bauen spätere Design-Iterationen auf denselben Tokens auf — und Claude Code implementiert gegen dieselben Tokens. So driften Exploration und Implementierung nicht auseinander.

### Iterationsschleife (pro Screen, nicht alles auf einmal)
Design (ein Screen) → Handoff → Code (implementieren + ans echte Scoring anbinden) → im laufenden App testen → fühlt sich etwas falsch an? → zurück zu Claude Design für genau diesen Screen → erneuter Handoff. Klein iterieren.

### Grenzen & Reihenfolge
- Claude Design macht **Aussehen, Layout, Flow, Prototyp** — **nicht** die Kernlogik (phonetisches Scoring, lokales Audio/DSGVO, Story-Engine). Die gehört zu Claude Code.
- **Phase 0 zuerst.** Das phonetische Kernrisiko ist unabhängig vom Design; das Design nicht vor das De-Risking stellen. Design darf parallel laufen, der Build beginnt aber erst nach dem GO.
- Claude Design ist **Research Preview** mit Nutzungslimits; Verfügbarkeit je nach Plan (Pro/Max/Team/Enterprise; bei Enterprise admin-seitig zu aktivieren). Vor Nutzung kurz den aktuellen Stand prüfen.

---

## 9. Offene Risiken / im Auge behalten
1. **Zuverlässigkeit der Kinderstimmen-Bewertung** (Hauptrisiko, betrifft Mechanik A und die lautgetreue Prüfung) — Phase 0 klärt es; milder kalibrieren.
2. **ASR-Auto-Korrektur** — die lautgetreue Fehlerprüfung **darf nicht** über Transkription laufen, sonst „repariert" das Modell die Falschschreibung. Akustische Distanz/Forced-Align verwenden.
3. **Methoden-Zuordnung** — vokallängen- und homophone Fehler **nur** über Markieren; nicht versuchen, sie hörbar zu erkennen.
4. **Schwellen-Kalibrierung & Fairness** — zu streng = Frust; lieber mild + Bonus.
5. **Orthografische Interferenz** — Falschschreibungen ausschließlich in der gerahmten Fälscher-Notiz, mit sofortiger Korrektur; nie in der Vorlese-Geschichte.
6. **Datenschutz** — Audio lokal halten (Standard = lokales Scoring).
7. **Mikro/Lärm-Variabilität** — Headset, ruhige Umgebung, konstante Bedingungen.

---

*Stand der recherchierten technischen Eckdaten: Mai 2026. Azure-Funktionsumfang/Preise und torchaudio-APIs ändern sich — vor dem Bau kurz gegenprüfen.*
