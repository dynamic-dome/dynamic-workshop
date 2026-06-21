# Neue & 'verrueckte' Uebungen — Welle 2 (Wild-Exercise-Designer)

> Fortsetzung von `05-new-exercises.md` (Welle 1, Nr. 1-8). Diese zweite Welle ergaenzt 10 NEUE Formate, die sich bewusst von Welle 1 unterscheiden. Mischung: 3 Micro-Aufwaermer (easy), 3 mittlere Domaenen-Uebungen (medium), 4 wilde Team-Formate (wild/hard). Verteilt ueber alle drei Bloecke. Nicht-Duplizierung gegen Welle 1 geprueft.

| Nr. | Titel | Block | Schwierigkeit | Geuebtes Konzept |
|----:|---|---|---|---|
| 9 | Das Orakel-Spiel | 1 | easy | Klaerungsverhalten / Frage-vor-Annahme |
| 10 | Tab-Complete-Bingo | 1 | easy | Slash-Commands & CLI-Oberflaeche |
| 11 | Kontext-Streichliste | 1 | easy | Context Window / @-Referenzen |
| 12 | OSDP-Polizist (Frame-Forensik) | 2 | medium | RAG / NotebookLM gegen echte Spec |
| 13 | Der Panel-Migrations-Diff | 2 | medium | Skill + strukturierte Config-Transformation |
| 14 | Alarm-Sturm-Korrelator | 3 | medium | Multi-Agent Fan-out auf Event-Streams |
| 15 | Telefon-Spiel mit Agenten | 3 | wild | Subagent-Isolation / Context-Drift |
| 16 | Saboteur in der Schicht | 2 | wild | Hook-Forensik unter Zeitdruck (sozial) |
| 17 | Blind-Vault (Spec-Diktat) | 1→2 | hard | Prompting blind + Spec-Disziplin |
| 18 | Der Falsche-Tuer-Heist | 3 | wild | Permission Modes / Protected Paths Red-Team |

---

## 9. Das Orakel-Spiel  `[Micro-Warmup ~3 Min | easy]`

- **Thema/Block:** Block 1, Warmup zwischen 1.1 und 1.3 (Prompting)
- **Geuebtes Konzept:** Claudes Klaerungsverhalten provozieren — wann fragt es nach, wann raet es?
- **Didaktischer Wert:** Neulinge denken, der Agent muss alles sofort wissen. Diese Uebung zeigt in 3 Minuten, dass eine bewusst unmoegliche Aufgabe ein GUTES Nachfrage-Verhalten ausloest — und macht aus "Claude hat falsch geraten" das Lernziel "ich war zu vage". Bruecke zu 1.3.
- **Security-Aufhaenger:** Der Wachmann am Tor, der bei unklarem Ausweis NICHT durchwinkt, sondern rueckfragt — Verweis `security-analogies.md` (Claude Code CLI = Consultant with badge access).

**Ablauf:**

1. In leerem Dir `claude` starten.
2. Bewusst unterbestimmt prompten: `Baue mir den Parser.` (nichts weiter).
3. Beobachten: Stellt Claude Rueckfragen (welcher Parser? welches Format?) oder raet es drauflos? Antwort NICHT geben — nur zaehlen, wie viele Annahmen Claude trifft.
4. Jetzt das Gegenteil: `Baue NICHTS. Stelle mir genau 3 Fragen, die du brauchst, um einen OSDP-Frame-Parser zu bauen.`
5. Die 3 Fragen laut vorlesen. Aha-Moment: Das sind exakt die Infos, die ihr beim naechsten Mal gleich in den Prompt schreibt.

---

## 10. Tab-Complete-Bingo  `[Micro-Warmup, Gruppen-Schnitzeljagd ~5 Min | easy]`

- **Thema/Block:** Block 1, ganz zu Beginn (CLI-Oberflaeche, vor 1.1)
- **Geuebtes Konzept:** Existenz und Entdeckbarkeit der Slash-Commands (`/help`, `/cost`, `/hooks`, `/rewind`, `/clear`).
- **Didaktischer Wert:** Spielerisches "Anfassen" der CLI ohne Code-Druck. Wer noch nie ein Slash-Command gesehen hat, hat nach 5 Minuten 5 davon selbst getippt. Senkt die Angst vor der "leeren Eingabezeile".
- **Security-Aufhaenger:** Ein neuer Operator lernt das Bedienpult der Leitstelle kennen, bevor der erste Alarm kommt (Context Window = Control room).

**Ablauf:**

1. Jede Person bekommt eine Bingo-Karte mit 6 Feldern: `/help`, `/cost`, `/hooks`, `/clear`, ein Slash-Command, den NIEMAND von euch kennt, und "ein Command, der eine Zahl ausgibt".
2. 5-Minuten-Timer. Ziel: jedes Feld durch echtes Eintippen abhaken und in einem Satz notieren, was es tut.
3. Pflicht-Twist fuer das fuenfte Feld: `/help` lesen und EINEN bislang unbekannten Command finden und ausprobieren.
4. Wer zuerst alle 6 hat, ruft "Bingo" und erklaert der Gruppe den unbekanntesten Command.
5. Debrief in einem Satz: "Welcher Command rettet mir wahrscheinlich am haeufigsten den Tag?"

---

## 11. Kontext-Streichliste  `[Micro-Warmup ~4 Min | easy]`

- **Thema/Block:** Block 1, nach 1.2 (Context/CLAUDE.md)
- **Geuebtes Konzept:** Was ist im Kontext? `@`-Datei-Referenzen vs. "Claude raet"; bewusstes Fuellen und Leeren des Fensters.
- **Didaktischer Wert:** "Kontext" ist fuer Neulinge abstrakt. Diese Uebung macht ihn greifbar: derselbe Prompt liefert vor und nach `@datei` sichtbar andere Qualitaet. Bereitet Block 2 (RAG) und Block 3 (Agent-Isolation) vor.
- **Security-Aufhaenger:** Der Leitstand mit begrenzten Monitoren — was nicht auf dem Schirm ist, existiert fuer die Entscheidung nicht (Context Window = Control room with limited monitors).

**Ablauf:**

1. Im Workshop-Playground starten. Ohne Datei-Referenz fragen: `Welche drei Vulnerabilities stecken in der Zutrittssteuerung?`
2. Antwort grob notieren (rateend? konkret?).
3. Kontext fuellen: `@access_control.py Welche drei Vulnerabilities stecken hier drin, mit Zeilennummern?`
4. Differenz beobachten: jetzt mit Zeilen 19, 127, 140.
5. Streichen: `/clear`, dieselbe Frage erneut ohne `@`. Erkenntnis: der Kontext war weg. DU fuellst und leerst das Fenster, nicht der Zufall.

---

## 12. OSDP-Polizist — Frame-Forensik gegen die echte Spec  `[Gefuehrte Domaenen-Uebung ~25 Min | medium]`

- **Thema/Block:** Block 2, Vertiefung zu 2.5 (NotebookLM/RAG)
- **Geuebtes Konzept:** RAG-Grounding — Claude ein echtes OSDP-Spec-Auszug-Notebook geben und falsche Behauptungen gegen geerdetes Wissen pruefen.
- **Didaktischer Wert:** Fuellt die Luecke "RAG nur abstrakt geuebt". Hier wird der Unterschied zwischen Halluzination und Quelle an echten Frame-Bytes spuerbar. Knuepft direkt an `osdp_frame_decoder.c` an.
- **Security-Aufhaenger:** Bauplaene des Gebaeudes statt Allgemeinwissen — der Pruefer entscheidet anhand der Spec, nicht aus dem Bauch (RAG/NotebookLM = Building blueprints).

**Ablauf:**

1. Notebook "OSDP Frame Reference" anlegen (per `/notebooklm create` oder Web-UI), 2-3 Quellen zum OSDP-Frame-Format laden (SOM `0x53`, LEN, ADDR, CMD, DATA, CRC — passend zu `osdp_frame_decoder.c`).
2. OHNE Notebook fragen: `Was bedeutet das erste Byte 0x53 in einem OSDP-Frame und wo sitzt die CRC?` — Antwort notieren.
3. MIT Notebook dieselbe Frage stellen, Quellen-Zitate vergleichen. Stimmt Claudes Bauchantwort?
4. Forensik-Fall: einen Hex-Frame-String vorlegen (z.B. aus dem decoder-`main()`) und fragen: `Ist dieser Frame gueltig laut Spec? Wo waere die Laengen-Pruefung, die der C-Code vergisst?`
5. Aha-Moment-Bruecke: Genau diese fehlende Laengen-Pruefung ist Buffer-Overflow V1 in `osdp_frame_decoder.c:40` — RAG hat die Sicherheitsluecke aus der Spec heraus erklaert.

---

## 13. Der Panel-Migrations-Diff  `[Domaenen-Uebung, baut einen Skill ~25 Min | medium]`

- **Thema/Block:** Block 2, Vertiefung zu 2.1 (Skills)
- **Geuebtes Konzept:** Einen Skill schreiben, der eine wiederkehrende, fehleranfaellige Config-Transformation kapselt (Panel-A-Format → Panel-B-Format).
- **Didaktischer Wert:** Anders als Welle-1-Skills (Workflow/Checkliste) ist DIES eine Daten-Transformation mit Domaenenregeln — das, was PhySec-Entwickler bei Hersteller-Migrationen real qaelt. Der Skill wird zum wiederverwendbaren Werkzeug.
- **Security-Aufhaenger:** Standard Operating Procedure fuer den Controller-Tausch — eine SOP, die jeder Techniker identisch anwendet (Skill = SOP).

**Ablauf:**

1. Zwei Mini-Config-Beispiele bereitstellen: `panel_old.json` (Door-IDs als `D01`, Zeitprofile in Minuten) und Ziel `panel_new.json` (Door-IDs als `DOOR-01`, Zeitprofile in Sekunden).
2. Erst manuell von Hand prompten: `Konvertiere panel_old.json ins neue Format.` — beobachten, welche Regel Claude rateend falsch macht (Minuten→Sekunden? ID-Padding?).
3. Die Regeln explizit machen und als Skill speichern: `~/.claude/skills/panel-migrate/SKILL.md` mit den Konvertierungsregeln als nicht-verhandelbare Schritte.
4. Skill an einem ZWEITEN, etwas anderen `panel_old_2.json` testen — haelt er die Regeln durch?
5. Erkenntnis: Was bei der Migration von 200 Tueren teuer schiefgeht, ist jetzt eine deterministische SOP. Bonus: einen Edge-Case (fehlendes Zeitprofil) einbauen und pruefen, ob der Skill sauber meldet statt still falsch zu konvertieren.

---

## 14. Alarm-Sturm-Korrelator  `[Multi-Agent Fan-out ~25 Min | medium]`

- **Thema/Block:** Block 3, Domaenen-Variante zu 3.1 (Multi-Agent)
- **Geuebtes Konzept:** Echte Fan-out-Parallelitaet auf unabhaengigen Daten-Shards — drei Agenten analysieren drei Log-Quellen, der Orchestrator korreliert.
- **Didaktischer Wert:** Welle-1/3.1 ist generisch ("zwei unabhaengige Teile"). Hier ist die Unabhaengigkeit echt domaenenmotiviert (drei Sensoren) UND es gibt einen Korrelations-Schritt, der zeigt, wo Fan-out endet und Synthese beginnt.
- **Security-Aufhaenger:** Bei einem Alarmsturm patrouillieren drei Team-Mitglieder parallel verschiedene Zonen, der Leitstand fuehrt die Meldungen zusammen (Subagent = Patrol team member, Agent Teams = Patrol roster).

**Ablauf:**

1. Drei kleine Log-Dateien anlegen: `door_events.log`, `motion_sensors.log`, `card_reader.log` — jeweils mit Zeitstempeln, ein gemeinsamer Vorfall (Tueraufbruch 02:14) ist ueber alle drei verstreut.
2. Explizit fan-out prompten: `Nutze drei parallele Agenten. Agent 1 fasst Auffaelligkeiten in door_events.log zusammen, Agent 2 in motion_sensors.log, Agent 3 in card_reader.log. Jeder kennt nur seine Datei.`
3. Beobachten: Jeder Agent hat eigenen Kontext, keiner sieht die anderen Logs.
4. Korrelations-Schritt im Orchestrator: `Korreliere die drei Berichte zu einer Zeitleiste. Gibt es ein Ereignis, das in allen drei auftaucht?`
5. Aha-Moment: Erst die Synthese deckt den koordinierten Vorfall auf, den keiner der drei Agenten allein sehen konnte. Diskussion: Wann ist eine Aufgabe Fan-out, wann eine Pipeline?

---

## 15. Telefon-Spiel mit Agenten  `[Spielerisches Experiment ~15 Min | wild]`

- **Thema/Block:** Block 3, spielerische Vertiefung zu 3.1 (Agent-Isolation)
- **Geuebtes Konzept:** Subagent-Kontext-Isolation und Information-Drift erlebbar machen — das Kinderspiel "Stille Post", aber mit Agenten als Kette.
- **Didaktischer Wert:** Die wichtigste, am haeufigsten missverstandene Eigenschaft von Subagenten — sie teilen KEINEN Kontext — wird hier zum Lacher und damit unvergesslich. Erklaert, warum man Agenten praezise briefen muss.
- **Security-Aufhaenger:** Eine Funkmeldung wird ueber drei Patrouillen weitergegeben und verzerrt sich — warum jedes Team ein eigenes, vollstaendiges Briefing braucht (Subagent = Patrol team member with own context).

**Ablauf:**

1. Eine bewusst detailreiche "Original-Meldung" bereitstellen, z.B. eine OSDP-Frame-Spezifikation in 4 Saetzen mit konkreten Byte-Werten.
2. Prompt: `Starte eine Kette von 3 Subagenten. Agent 1 bekommt diese Meldung und fasst sie in EINEM Satz zusammen. Agent 2 bekommt NUR Agent 1s Satz und fasst ihn wieder zusammen. Agent 3 ebenso.` — wichtig: jeder Agent kennt nur den Output des vorigen.
3. Den finalen Satz von Agent 3 mit dem Original vergleichen — was ist verloren gegangen, was verzerrt?
4. Wiederholen, aber diesmal jedem Agenten das VOLLE Original mitgeben. Vergleich: kein Drift.
5. Erkenntnis (und der Lacher): Subagenten erben nicht euren Kopf. Wer schlampig briefed, bekommt Stille Post. Bruecke zum `subagent-briefing`-Prinzip.

---

## 16. Saboteur in der Schicht  `[Soziales Sabotage-Spiel unter Zeitdruck ~20 Min | wild]`

- **Thema/Block:** Block 2/3, wilde Vertiefung zu 2.2 + 3.7 (Hook-Forensik)
- **Geuebtes Konzept:** Hook-Diagnose unter Druck — ein Mitspieler sabotiert heimlich eine `settings.json`, der andere muss mit `/hooks` und `--verbose` finden, WAS und WO kaputt ist.
- **Didaktischer Wert:** Unterscheidet sich von Welle-1 "Hook-Honeypot" (dort baut man Fallen FUER Maschinen) — hier ist der Gegner ein MENSCH, der gemein und kreativ sabotiert. Trainiert exakt den 3.7-Diagnose-Loop, aber als Wettlauf gegen einen denkenden Saboteur.
- **Security-Aufhaenger:** Ein Innentaeter hat ueber Nacht die Zutrittspolitik manipuliert; der Tagschicht-Operator muss die Layer abgehen: Karte → Leser → Controller (Hook = Access control sensor).

**Ablauf:**

1. Paare bilden. Person A verlaesst kurz den Raum.
2. Person B sabotiert die projektlokale `settings.json` mit GENAU EINER fiesen Aenderung — zur Wahl: Matcher zu breit (`".*"`), Hook-Skript-Pfad verbogen, Exit-Code invertiert, oder ein zweiter stiller Hook eingeschmuggelt. WICHTIG: projektlokal, nicht global (Welle-1-Honeypot-Lektion).
3. Person A kommt zurueck, Stoppuhr laeuft. Erlaubt sind NUR `/hooks`, `claude --verbose`, und Lesen der Logs — das Skript erst als letztes oeffnen.
4. A muss laut die Hypothese aussprechen, BEVOR sie das Skript oeffnet (Disziplin aus 3.7).
5. Rollen tauschen. Schnellste saubere Diagnose gewinnt. Debrief: Welche der vier Sabotagen war am schwersten zu finden — und warum war `/hooks` + `--verbose` der entscheidende Hebel?

---

## 17. Blind-Vault — Spec-Diktat ohne Bildschirm  `[Prompting-Disziplin, paarweise ~20 Min | hard]`

- **Thema/Block:** Block 1→2 Bruecke, Vertiefung zu 1.3 (Prompting)
- **Geuebtes Konzept:** Praezises "Work-Order"-Prompting unter erschwerten Bedingungen — der Prompter sieht den Bildschirm NICHT und muss allein durch Sprache eine korrekte Implementierung erzeugen.
- **Didaktischer Wert:** Die haerteste Form von 1.3. Wer blind promptet, lernt, dass jede ungesagte Annahme zu Pfusch wird. Macht den Wert von Spezifikation brutal sichtbar und ist als Paar-Format ein Highlight fuer Fortgeschrittene.
- **Security-Aufhaenger:** Ein Operator dirigiert per Funk einen Techniker, den er nicht sehen kann, durch die Tresorraum-Verkabelung — jede Mehrdeutigkeit kostet (Remote Control = phone-based remote ops).

**Ablauf:**

1. Paare: "Sprecher" und "Tipper". Der Sprecher dreht sich vom Bildschirm WEG und darf ihn nicht ansehen.
2. Ziel (nur der Sprecher kennt die Spec von einem Zettel): eine Funktion `is_valid_access_window(now, start, end)`, die prueft, ob ein Zeitstempel in einem erlaubten Zutrittsfenster liegt — inkl. Mitternachts-Ueberlauf (22:00–06:00).
3. Der Sprecher diktiert AUSSCHLIESSLICH Prompts; der Tipper tippt woertlich und darf nicht "mitdenken" oder korrigieren.
4. Wenn Claude eine Annahme trifft, die der Spec widerspricht, muss der Sprecher das blind aus Claudes Antwort heraushoeren und per Folge-Prompt korrigieren.
5. Tests laufen lassen (Mitternachts-Fall ist die Falle). Erst wenn gruen, darf der Sprecher hinsehen. Debrief: An welcher ungesagten Annahme ist es fast gescheitert?

---

## 18. Der Falsche-Tuer-Heist — Permission-Red-Team  `[Red-Team-Wettbewerb gegen Schutzwall ~25 Min | wild]`

- **Thema/Block:** Block 3, wilde Vertiefung zu 3.3/3.8 + Permission Modes
- **Geuebtes Konzept:** Permission Modes und geschuetzte Pfade verstehen, indem man sie ANGREIFT — und dann den Wall haertet, bis der Angriff scheitert.
- **Didaktischer Wert:** Permission Modes werden meist nur erklaert. Hier wird der Schutz erst durchbrochen (Aha: ein zu lockerer Modus laesst alles durch), dann verteidigt. Verbindet CLAUDE.md-Schutzregeln, PreToolUse-Hooks und Permission-Modi zu einem Bild.
- **Security-Aufhaenger:** Ein Red-Team versucht, ueber eine Nebentuer in den Tresorraum zu kommen; jeder erfolgreiche Versuch fuehrt zu einer haerteren Tuer (Permission Modes = clearance levels, Protected Paths = Vault rooms, uncrackable).

**Ablauf:**

1. Schutzziel definieren: `osdp_frame_decoder.c` und `access_control.py` duerfen NICHT veraendert werden (sie sind die "Tresorraeume" — Verweis CLAUDE.md "do NOT fix").
2. Angriffsrunde (Team Rot): Versucht, Claude zu einer Edit dieser Dateien zu bewegen — direkt, ueber Umweg ("formatiere nur die Kommentare"), oder ueber einen anderen Tool-Pfad. Notiert jeden erfolgreichen Durchbruch.
3. Verteidigungsrunde (Team Blau): Baut den Wall in drei Schichten — (a) eine CLAUDE.md-Regel "Never modify these files", (b) einen PreToolUse-Hook mit Matcher `Edit|Write`, der genau diese Pfade blockt, (c) bewusste Wahl eines restriktiveren Permission-Mode statt `bypassPermissions`.
4. Erneute Angriffsrunde gegen den gehaerteten Wall. Welche Schicht hat welchen Angriff gestoppt?
5. Debrief: Welche Schutzschicht war am robustesten — Sprache (CLAUDE.md), Mechanik (Hook) oder Berechtigung (Mode)? Erkenntnis: Schutz braucht Defense-in-Depth, kein einzelner Layer reicht.

---

*Ende Welle 2 (Nr. 9-18). Anschluss an Welle 1 (Nr. 1-8) in `05-new-exercises.md`.*
