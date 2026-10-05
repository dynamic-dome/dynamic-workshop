# Durchsicht 2026-10-05: Einteilung, Lernbogen, Fakten

> Auftrag des Owners: den Workshop einmal komplett ansehen und zurückmelden, wie er als Selbstlern-Material wirkt
> (Einteilung, Richtigkeit, Lernbogen, eigene Kriterien). Stand des Materials: `main` = `e693038`.
> Diese Datei ist die Befundliste; die DCO-Todos verweisen mit der Befund-Nummer (R1 …) hierher.
> Ergänzt den Cockpit-Durchgang vom 2026-10-02 (B1 … B12), ersetzt ihn nicht.

## Vorgehen

- **Selbst gelesen (Claude Code, Fable):** Spec, `_shelves.yaml`, `_placement.yaml`, alle fertigen Pfade, `einstufung.md`,
  Tutor-Skill, README, HOW-TO-USE, S1.1, S2.6, S1.20, S4.8 (Aufgabe und Rubrik), Stellen aus rund 25 weiteren Kapiteln
  zur Gegenprobe; Cockpit im Browser (Start, Kapitel, Bibliothek, schmale Breite).
- **Selbst gemessen:** `measure.py`, `measure2.py`, `tally.py` (Übungsdichte, Zeitangaben, Moderationsanteil,
  Lesestrecken, Nachzählung der Leser-Zahlen).
- **Selbst ausgeführt:** die beiden Gate-Vorlagen und `safety-check.sh` mit Testeingaben auf stdin (R1).
- **14 Leser auf Sonnet, festes Raster, Berichte mit Zitat und Zeile:** 7 Didaktik-Leser (alle 70 Kapitel in
  Lesereihenfolge), 7 Faktenprüfer gegen die offizielle Doku (66 Seiten, abgerufen 2026-10-05, Changelog bis 2.1.289).
- **Ablage der Rohdaten:** `~/AI/analysis-artifacts/workshop-review-2026-10-05/` (`berichte/` D1–D7 und F1–F7,
  `docs-cache/`, die drei Skripte).

Herkunft je Befund: **[ausgeführt]** = von mir laufen gelassen · **[geprüft]** = von mir an Kapitel und Doku
nachgeschlagen · **[gezählt]** = Skript über alle Kapitel · **[Leser]** = aus einem Leserbericht übernommen, Zitat dort.

## Was trägt

- Eine Quelle je Information, Generator und Validator, Sicherheitsboden als Regel in der Einstufung, Kanon für
  Modelle: Die Bauweise ist die eines gepflegten Produkts.
- Fakten: Die sieben Prüfer haben 925 Aussagen geprüft (889 nachgezählte Tabellenzeilen zu Kapiteln, Karten und
  Community-Kapiteln, dazu 36 Posten des Modell-Kanons). Davon 815 belegt (88 %), 24 Abweichungen, 9 Widersprüche
  zwischen Kapiteln, 73 aus den Quellen nicht belegbar (meist Workshop-eigene Bausteine, Fremdprodukte,
  Rechtsaussagen), 4 ohne Urteil. Der Kanon stimmt in allen Modellen, IDs, Preisen und Kontextgrößen. Die Aussagen
  über fremde Projekte in X.1 bis X.4 halten: 100 geprüft, 99 belegt.
- Eine gemeldete Abweichung habe ich verworfen: `karte-rechte.md`:69 („`auto` in `.claude/settings.json` startet in
  Manual“) deckt sich mit dem Fehlersuche-Abschnitt der Doku (permission-modes.md Z. 313); die Doku sagt an anderer
  Stelle (Z. 72) etwas anderes, das ist ihr Widerspruch, nicht der des Kurses.
- Wo es Übungen gibt, sind sie oft gut gebaut: S1.1 (Übung 1.1), S1.10, S1.16, S2.11, S2.14, S3.4, S3.12, die
  Prüfübung in X.1, die Rubrik in S4.8. Die „Typischen Fallen“ stammen erkennbar aus echten Fehlern.
- `safety-check.sh` fällt geschlossen, auch ohne `jq` (ausgeführt: Exit 2).

## Befunde

Schweregrad: **hoch** = verhindert oder verfälscht das Lernen bzw. hat eine Sicherheitsfolge · **mittel** = kostet
spürbar Zeit oder Verständnis · **klein** = Feinschliff.

### Inhalt und Richtigkeit

| Nr. | Schwere | Befund | Ort | Herkunft |
|---|---|---|---|---|
| R1 | hoch | **Das Secure Diff Gate fällt offen.** `secure-diff-gate.sh` endet ohne `jq` mit Exit 127, auch bei Ziel `.env`; `secure-diff-gate.py` gibt bei kaputter oder leerer Eingabe 0 zurück (Kommentar im Code: „fail open“) und lässt `.ENV` in Großbuchstaben durch (unter Windows und macOS dieselbe Datei). Der Matcher `Write\|Edit` sieht Bash-Umleitungen (`echo X > .env`) nicht. S2.10 nennt das Gate „harte Sperre“ und „Tresor-Regel“, S2.8 lehrt das Gegenteil („Temposchwelle, keine Mauer“; lieber blocken, wenn die Eingabe nicht lesbar ist). | `resources/demos/assets/hooks/secure-diff-gate.{sh,py}`, S2.10:28, :32, :38, :218 | ausgeführt |
| R2 | mittel | „Blockt **nur** mit `exit 2`“ steht als absolute Regel an mindestens neun Stellen; richtig ist: Über den Exit-Code allein blockt nur 2, daneben blockt JSON mit `permissionDecision: "deny"` (so steht es in S2.10:99 und S4.5:216). Erweitert B5. | S2.6:33, :62, :75, :98, :108 · S2.7:68 · S2.8:33, :297, :590 · S4.10:37 · README:32 · `_shelves.yaml` (Hooks) | geprüft (hooks.md Z. 840) |
| R3 | mittel | Laut Doku feuert PostToolUse nur nach einem **erfolgreichen** Tool-Aufruf; ein fehlgeschlagener `npm test` geht an PostToolUseFailure, das kein `updatedToolOutput` kennt. Token Firewall, Schwärzung und Audit-Log greifen damit gerade bei Fehlschlägen nicht; der Handtest in S2.10:305 zeigt eine Eingabe, die so nicht vorkommt. Nicht live getestet. | S2.10:239–305 · S2.8:547–576 · S2.6:64 | geprüft (hooks.md Z. 2018, 2123 ff.) |
| R4 | mittel | `${VAR:-default}` heißt „die sichere Wahl“ für eine eingecheckte `.mcp.json`; die Beispiele setzen einen Token- und einen Passwort-förmigen Rückfallwert genau dorthin, entgegen Z. 34 desselben Kapitels. | S2.15:142, :150, :162 | geprüft |
| R5 | mittel | Es fehlt die zweite, feste Schwelle: Textergebnisse über 50.000 Zeichen landen unabhängig von `MAX_MCP_OUTPUT_TOKENS` in einer Datei. | S2.16:82–85 · `karte-erweitern.md`:78–81 | geprüft (mcp.md Z. 1287) |
| R6 | mittel | `${CLAUDE_PLUGIN_ROOT}` steht im Hook-Befehl ohne Anführungszeichen (Doku verlangt sie; Pfade mit Leerzeichen brechen). Der Cache-Pfad in S2.2 hat weder Plugin- noch Versionsebene, anders als S2.11:111. | S2.11:115 · S2.2:249 | geprüft / Leser F3 |
| R7 | mittel | Demo „Hooks, die Alarmanlage“: gezeigt wird eine PreToolUse-Konfiguration für Bash, ausgelöst werden soll ein PostToolUse-Hook auf `innerHTML`; das Skript `security-check.sh` liegt nicht bei den Vorlagen. | S2.8:241–297 | Leser F3, D3 |
| R8 | mittel | S0.1 nennt als Prüfstand 2.1.200 und als Minimum 2.1.197; S1.1, S1.5 und S1.6 setzen den Startmodus `auto` ab 2.1.283 voraus. Wer das Minimum nutzt, sieht ein anderes Startverhalten. Dazu Node 22 gegen `setup_20.x` gegen „v18 oder neuer“. | S0.1:87, :97, :197, :296 | Leser F1, D1 |
| R9 | klein bis mittel | Seit dem Prüfdatum veraltet: `claude project purge` heißt seit 2.1.288 `claude purge`; Sonnet 4.5 ist seit 2026-09-30 abgekündigt (Kanon Z. 51); die Doku nennt den Startmodus von `claude -p` bei Drittanbietern jetzt selbst (Kanon Z. 73, 78–79, ebenso S1.6:88); `/hooks` öffnet seit 2.1.286 mit einer Liste je Ereignis. Haiku 4.5: frühestes Abschaltdatum 2026-10-15. Klein: X.1 schreibt dem mattpocock-README einen Marketplace-Befehl zu, den es dort seit August nicht mehr nennt (der Befehl funktioniert weiter). | S1.11:91–95 · `_canonical.md` · `karte-rechte.md`:23 · `karte-start-und-flags.md`:27 · X.1:96 | geprüft (Changelog, permission-modes.md Z. 85) / Leser F2, F7 |
| R10 | mittel | `pip install notebooklm-py` ohne das Extra `[browser]`, das PyPI für den Login nennt. Mit Vorbehalt: PyPI sagt nicht ausdrücklich, dass es ohne scheitert. | S2.18:79, :344 | Leser F4 |
| R11 | klein | `xhigh`/`max` gelten nicht für jedes Modell hinter den Aliasen (S1.7:74, :101) · `Bash(rm *)` trifft auch das nackte `rm` (S1.5:97) · „Stop feuert nach jeder Antwort“: nicht nach Abbruch oder API-Fehler (S2.6:109, S2.7:105), und das Beispiel in S2.8:95 loggt an Stop „Session ended“ · „in jeder Sitzung“ gilt für die meisten mitgelieferten Skills (S2.4:53) · `--bare` „nur“ API-Key gegen Cloud-Anbieter (S4.4:119 gegen :65) · Skill-Aufruf unter `--bare` gilt laut Doku nur für Skills aus `--add-dir` (S4.4:113) · S4.8: 35–45 Minuten angesagt, die Schritte ergeben 45–50. | wie genannt | Leser F1, F3, F6, teils geprüft |
| R12 | mittel | Ohne Quelle: die Regelwerk-Tabelle (EN 50131, DORA, MiFID II, NIS2 „sind Pflicht“) neben dem Satz „keine Rechtsberatung“; „Bedrock-Verkehr bleibt in deiner VPC“; Exit-Code bei erreichter Budgetgrenze; „84 % weniger Rückfragen“. | S3.11:37, :83–88 · S4.5:186 · S4.4:88, :263 · S3.9:99 | Leser F5, F6, F1 |
| R13 | mittel | Playground-Doku passt nicht zum Code: `backup_database()` „~140“ (ist 161), `read_log()` „~127“ (ist 148), `log_event()` „105–113“ (ist 132); „Block 3.3“; „Do NOT fix“ gegen den Fix im Abschlussprojekt. | `workshop-playground/CLAUDE.md`:52–75 | geprüft |

### Lernbogen

| Nr. | Schwere | Befund | Ort | Herkunft |
|---|---|---|---|---|
| R14 | hoch | **34 von 61 Lektionen haben kein „Selbst machen“**, im Kern 17 von 37. Längste Strecke ohne eigenes Tun: S2.3 bis S2.7 (5 Kapitel, 66 Minuten). Im Pfad „Alltag“ sind 17 von 36 Kapiteln reine Lektüre. Mehrere Outcomes versprechen ein Können, das nie geübt wird (u. a. S1.5 Deny-Regel schreiben, S1.14 Plan-Modus, S2.3 `disable-model-invocation`, S3.3 eigener Subagent, S3.9 Isolationsstufe wählen, S3.13 gedeckelter Lauf). | Liste: `measure2.py` | gezählt / Leser D1–D7 |
| R15 | hoch | **207 Abruffragen, eine Auflösung gibt es in zwei Kapiteln** (S1.6, S1.10). Wer allein lernt, kann seine Antwort nicht prüfen. Quiz: häufig erfundene oder offensichtlich falsche Antworten, die richtige ist oft die längste; mehrere Checks prüfen etwas anderes als das Outcome (S2.4, S2.7, S2.8, S2.10, S3.11, S4.4). | alle Kapitel | gezählt / Leser |
| R16 | hoch | **Der Lernweg hat keinen Schluss.** Alle sechs Zielpfade enden mit S4.9 und S4.10 (Fehlersuche). Das Abschlussprojekt S4.8 ist Kür, steht vor der Fehlersuche und kommt nur in zwei Pfaden vor (`agents`, `einschaetzen`). Die Praxis-Stationen sind Auswahlmenüs aus dem Live-Format („Im Workshop hast du dafür 15 Minuten“) und verweisen auf Übungen, die man im Pfad schon hinter sich hat; S2.20 bietet für die Sicherheitsboden-Kapitel S2.13 und S2.17 nichts an, S3.15 nur zwei Kapitel. | `resources/paths/*.md`, S1.20, S2.20, S3.15, S4.8 | geprüft / Leser |
| R17 | hoch | **Der erste Erfolg kommt spät.** Vor der ersten Datei liegen S0.1 (auch Node, `jq`, `gh`, Playground-Klon, die erst später gebraucht werden), das Kür-Kapitel X.2 und in S1.1 der Theorieteil. Die erste Übung verlangt, die Freigabe-Abfrage zu sehen; im Startmodus `auto` bleibt sie aus, wie das Kapitel selbst sagt. | S0.1, X.2, S1.1:33, :60, :168, :198 | geprüft / Leser D1 |
| R18 | hoch | **Der Playground verrät die Lösungen.** Jede Schwachstelle trägt einen `VULNERABILITY`-Kommentar, und die automatisch geladene `CLAUDE.md` listet alle fünf. Damit zeigen die Übung in S1.8 (Kontext leer oder gefüllt), der Scan in S3.6 (Scanner gegen Fachwissen) und das Extra in S2.18 nicht mehr, was sie zeigen sollen. | `workshop-playground/`, S1.8:93–112, S3.6 | geprüft |
| R19 | hoch | **Cockpit und Tutor führen standardmäßig durch die Kurzfassung.** Die Kapitelansicht zeigt Schnellcheck, Auf einen Blick, Bild, ein Beispiel und die Quizfrage; „Im Detail“ und „Selbst machen“ liegen eingeklappt hinter „Ganzes Kapitel lesen“, auch beim Status „durcharbeiten“. Die Abruffragen erscheinen dort nicht, „Als erledigt markieren“ steht oben rechts. Der Tutor fasst in höchstens 150 Wörtern zusammen und geht dann zur Übung; hat das Kapitel keine, folgt direkt der Check. | `tools/cockpit/template.html`:784, `skills/workshop/SKILL.md`:121–138 | geprüft |
| R20 | mittel | **Die Minutenangabe ist die Lesezeit.** Übungen mit eigener Zeitangabe summieren sich auf 542 Minuten zusätzlich; in 15 Kapiteln dauern die Übungen länger als das ganze Kapitel laut Kopfzeile (S3.6: 18 gegen 115, S4.8: 25 gegen 45, S2.8: 15 gegen 25). „17 Stunden“ und die Etappenplanung der Einstufung rechnen ohne das Tun. | Frontmatter `minutes` | gezählt |
| R21 | mittel | **Reste des Live-Formats im Lernweg.** 29 Kapitel haben „Vorführen“ (10 % des Texts). Lehr- und Hilfetext steht in „Für Moderierende“-Blöcken (S2.6: Hooks sind Best-Effort-Wächter; S2.10: Windows-Weg des Gates; S3.8: Fehlerhilfe). Gruppenübungen ohne Einzelfassung (S1.1 Bingo, S3.8 Heist, S4.2, S4.8, S4.10). Nicht beschaffbare Bausteine: `devil-advocate-swarms`, `agentic-os` (`run-loop` gibt es nicht mehr), `multi-model-orchestrator`, Telegram-Bridge, der `notebooklm`-Skill der Moderation. Kürzel wie „W1“, „Übung 3.9“, „Block 3.3“. | wie genannt | gezählt / Leser |
| R22 | mittel | **Baustellenspuren im Lehrtext.** „Der alte Kurs zeigte …“, „frühere Fassungen“, „aus der bisherigen Kursanleitung“ in acht Kapiteln; absichtlich falsche Beispiele, die danach korrigiert werden (S2.3:93, S2.5:89, S3.13:70, :148); Versionsarchäologie und Wartungstabelle in S0.1. | S0.1, S2.3, S2.5, S2.11, S3.13, X.2 u. a. | geprüft |
| R23 | mittel | **Windows-Weg in den Hook-Kapiteln lückenhaft.** S2.8: Sicherung, Ordner, Handtest nur in bash; S2.10: keine `.ps1` für Schwärzung und Token Firewall, Windows-Weg des Gates nur im Moderationsblock; S2.6: Skript mit `jq` ohne Hinweis. Der Schnellcheck von S2.8 fragt den Windows-Matcher nicht ab. | S2.6, S2.8, S2.10 | Leser D3 |
| R24 | mittel | **Ungleiche Last.** Überladen: S1.5, S2.8, S2.10 (sieben Ideen), S3.6 (rund fünf Lerneinheiten), S3.8, S4.4, S4.10. Dünn oder Nachschlagewerk im Kern: S2.4, S2.6/S2.7, S1.6, S3.2. | wie genannt | Leser |
| R25 | mittel | **Bilder wandern.** „Besucherausweis“ meint in S1.2 den Zutritt überhaupt, in S1.5 den Modus `default`; Knopf und Dienstanweisung wechseln zwischen S2.1 und S2.3 die Zuordnung; „Testhalle“ ist in S3.8 der Container, in S3.9 die Sandbox; „Generalschlüssel ohne jedes Schloss“ gegen „Deny-Regeln blocken weiter“; S1.8: das Archiv „kann ihn zurückholen“. | wie genannt | Leser D1, D3, D6 |
| R26 | mittel | **Angesprochen wird ein Fachgebiet, das das README nicht nennt.** „Zu deinem Fachgebiet gehören Firmware für Zutrittscontroller, Integrationsprotokolle (OSDP, Wiegand, RS-485) …“; OSDP-, RS-485- und Panel-Beispiele in mindestens zehn Kapiteln. Laut README richtet sich die Bibliothek an Entwicklerinnen und Entwickler allgemein. | S1.2:76–78 u. a. | geprüft |

### Einteilung

| Nr. | Schwere | Befund | Ort | Herkunft |
|---|---|---|---|---|
| R27 | mittel | **Zwei Ordnungen liegen übereinander.** Die IDs folgen den vier Live-Sessions, die Regale dem Thema. Der Pfad „Alltag“ springt deshalb von S2.20 nach S3.8, S3.9 und dann S4.9. `requires` ist an vielen Stellen zu knapp (u. a. S1.5 ohne S1.4, S1.14 ohne S1.6, S3.4 ohne S3.3, S3.13 ohne S3.8, S4.8, S1.20 mit leerer Liste). | Pfade, Frontmatter | geprüft / Leser |
| R28 | mittel | **Kür-Kapitel stehen in der Kernlinie.** X.2 zwischen Installation und erstem Erfolg, X.1 zwischen S2.13 und S2.14, X.3 zwischen „eingebaute“ und „eigene Subagenten“, X.4 nach S4.6. X.3 und X.2 greifen auf Stoff vor, der erst später kommt. | `after:` der X-Kapitel | geprüft / Leser |
| R29 | mittel | **Die Fehlersuche steht am Ende, gebraucht wird sie ab den ersten Skills und Hooks.** S4.9 verlangt nur S1.4. | S4.9, S4.10 | Leser D7 |
| R30 | mittel | **Sicherheitswissen liegt teils in Vertiefung oder Kür,** Nachschlagewerk teils im Kern. Vertiefung oder Kür: S2.13, S2.17, der Abschnitt zur Angriffsfläche in S2.5, der Datenschutz-Kern von S3.11, die Datenfluss-Grenze in S4.2, Notaus und Prüfliste in X.4, das Gate in S2.10. Kern: S2.4, S2.7, weite Teile von S1.6 und S1.3. | Frontmatter `level` | Leser |
| R31 | klein | **„Du musst nicht alles lesen“:** Die Pfade für Neulinge umfassen 36 bis 53 der 70 Kapitel. (Frage aus dem Durchgang vom 2026-10-02.) | `resources/paths/` | gezählt |

## Stand der Umsetzung

Branch `selbstlern-zuerst` (ab `e693038`), Owner-Entscheid 2026-10-05: Selbstlernende zuerst, Moderation und
„Vorführen“ als eigene Schicht.

- **R1 umgesetzt.** Beide Gate-Vorlagen blocken jetzt, wenn sie ihre Eingabe nicht lesen können (kein `jq`, kein
  JSON, leer, kein Objekt), erkennen `.ENV` in jeder Schreibweise und melden den Grund lesbar in UTF-8. Die
  Bash-Fassung braucht kein `grep` mehr. Elf neue Tests in `tools/test_course_hooks.py`, neun davon vorher rot.
  S2.10 nennt die Grenze des Gates (Shell-Befehle) und die Deny-Regel als Ergänzung.
- **Dabei gefunden und behoben:** Der dokumentierte Windows-Aufruf `python %USERPROFILE%\.claude\hooks\…` wird weder
  von Git Bash noch von PowerShell aufgelöst. Python findet die Datei nicht und endet mit 2, das Gate hätte jeden
  Schreibzugriff geblockt (ausgeführt). Jetzt `python "$HOME/.claude/hooks/secure-diff-gate.py"`, in beiden Shells geprüft.
- **R2 umgesetzt** in S2.6, S2.7, S2.8, X.3, `karte-hooks.md`, README und `_shelves.yaml`. Unverändert, weil dort
  ausdrücklich von Exit-Codes die Rede ist: S4.10:37, :65, :406, die Szenario-Erklärung in `_placement.yaml` und der
  Code-Kommentar in S2.6:75. Offen: der Beispieltitel „Blockt nur mit exit 2“ in X.2:145 und
  `skills/workshop/LEARNING-RECORD-FORMAT.md`:11.

## Noten der Didaktik-Leser (70 Kapitel, Skala 1 bis 5)

| Kriterium | Mittel | Verteilung 1 · 2 · 3 · 4 · 5 |
|---|---:|---|
| Klarheit | 3,3 | 0 · 2 · 42 · 26 · 0 |
| Aktivierung | 2,3 | 24 · 19 · 10 · 17 · 0 |
| Prüfbarkeit | 2,9 | 0 · 13 · 50 · 7 · 0 |
| Selbstlern-Tauglichkeit | 2,9 | 0 · 16 · 43 · 11 · 0 |

Stärkste Kapitel nach Summe: S1.10, S1.16, S2.11, S3.12, dann S1.1, S1.13, S2.14, S3.4. Schwächste: S1.17, S1.20,
S2.10, S2.20, S3.14, S4.7. Die Noten stammen von Sonnet-Lesern mit der Vorgabe, keine 5 ohne Begründung zu geben;
sie taugen zum Vergleich der Kapitel untereinander, nicht als absolute Zensur.

## Empfohlene Reihenfolge

1. **R1** beheben (Gate auf fail-closed, Grenze im Text nennen, Deny-Regel daneben) und **R2** an allen Stellen
   angleichen. Das sind die beiden Stellen, an denen der Kurs seiner eigenen Sicherheitslehre widerspricht.
2. **R15:** zu jeder Abruffrage eine eingeklappte Auflösung. Kleinster Eingriff mit der größten Wirkung fürs Selbstlernen.
3. **R19:** im Cockpit bei „durcharbeiten“ den Lehrtext und die Übung offen zeigen; der Tutor führt bei solchen
   Kapiteln durch „Im Detail“.
4. **R16:** ein kurzer Abschluss in jedem Pfad (Fix, Guardrail, Verifikation, Übergabe im Playground, 25 Minuten,
   Kern), S4.8 dahinter als große Fassung; die Praxis-Stationen zu je einer verbindenden Aufgabe umbauen.
5. **R14:** je Kern-Lektion ohne Übung eine Aufgabe von fünf bis zehn Minuten mit „Geschafft, wenn“.
6. **R17, R18, R28:** X.2 aus der Linie, S0.1 kürzen, in S1.1 die Übung vor die Theorie und mit
   `--permission-mode default`; den Playground in einer Fassung ohne Lösungshinweise ausliefern.
7. **R21, R22, R26:** entscheiden, ob die Selbstlern-Fassung die Hauptfassung ist. Wenn ja: „Vorführen“ und
   Moderation als eigene Schicht, Baustellenspuren raus, Fachgebiet als Beispiel statt als Anrede.
8. Rest der Tabelle Inhalt (R3 bis R13) im nächsten Aktualitätslauf.

## Nicht geprüft

- Keine Übung wurde durchgespielt; Aussagen zur Lösbarkeit beruhen auf Lesen, außer bei den Hook-Vorlagen (R1).
- R3 beruht auf dem Wortlaut der Doku, nicht auf einem Lauf.
- Tutor-Plugin in einer echten Sitzung, Deck, Videos und Moderationsunterlagen wurden nicht bewertet.
- Die Faktenprüfung deckt Aussagen ab, die sich an der Doku messen lassen; Workshop-eigene Bausteine und
  Rechtsaussagen bleiben „nicht belegbar“.
