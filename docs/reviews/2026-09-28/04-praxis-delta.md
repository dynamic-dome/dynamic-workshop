# 04 — Praxis-Delta: was der Autor seit Juli anders macht, als der Kurs lehrt

> Maßstab: die eigene Arbeitspraxis mit Claude Code, Codex und Subagenten zwischen 2026-07 und 2026-09.
> Belege sind datierte Betriebsnotizen und Messungen aus dem eigenen Agenten-Setup (privat, nicht verlinkt)
> sowie Kurs-Fundstellen per `grep`. Format laut `00-SCHEMA.md`. Erstellt 2026-09-28 (Claude, Orchestrator).

Der Kurs versprach auf der Website, „mit echter Engineering-Arbeit mitzuwachsen". Dieses Delta sammelt,
was in dieser Arbeit seit dem letzten Kursstand gelernt wurde und im Kurs noch fehlt. Die meisten Befunde
sind keine Fehler, sondern Lektionen, die erst im Dauerbetrieb sichtbar werden: genau das Material, das
offizielle Einsteigerkurse nicht haben.

## Befunde

### P-01 · fehlt · P1 · Ergebnisse von Agenten prüfen (Selbstbericht ist kein Beweis)
- **Ort:** S3.1–S3.4 (Agents & Orchestrierung), S4.1/S4.2 (Multi-Model); Andockpunkt für das versprochene Eval-Modul.
- **Beleg:** Betriebsnotiz 2026-09-26: sechs Arbeitspakete von Sonnet-Ausführungsagenten, alle mit grünen Tests und
  plausiblen Berichten. Ein unabhängiger Prüfer (Codex, read-only) gab 4 von 6 FAIL mit echten Fehlern, u. a. ein
  Schutztest, der bei Regression in echte Daten geschrieben hätte, und ein nie invalidierter Cache. Browser-QA fand
  zusätzlich einen Layoutfehler, den String-Tests nicht sahen.
  Kurs: `grep -ri "negative control\|mutation"` in modules/demos/exercises = 0 Treffer; „self-report" nur einmal in
  `block-2-ecosystem.md`. Der Kurs lehrt Swarms („Claude reviews the assembled result", `block-3-advanced.md:522`),
  aber nicht, *wie* man einem grünen Agentenergebnis misstraut.
- **Vorschlag:** Eigene LE „Agentenergebnisse prüfen": Stichprobe statt Selbstbericht, unabhängiger Prüfer,
  Negativkontrolle (ein absichtlich kaputter Input muss rot werden), Verdikt-Stufen (selbst geprüft vs. unabhängig
  belegt). Übung mit eingebautem Fehler, bei dem die Agententests grün bleiben. Kern des Eval-Moduls.
- **Aufwand:** M

### P-02 · fehlt · P2 · Auch der Prüfer irrt
- **Ort:** S4.1 (Claude→Codex→Claude), `block-3-advanced.md:422`
- **Beleg:** Betriebsnotiz 2026-09-26: Codex-Prüfer meldete fehlende Anführungszeichen in einem Shell-Skript; Datei und
  Commit waren korrekt gequotet. Ursache sehr wahrscheinlich: Anführungszeichen des inline mitgegebenen Diffs gingen
  auf dem Windows-Weg zum Prüfer verloren. Ein unnötiger „Fix" an korrektem Code wurde nur durch Gegenprobe verhindert.
  Gleiche Runde: ein weiterer Prüferbefund (BOM-Test) war falsch.
- **Vorschlag:** In S4.1 ergänzen: Befunde des Prüfers gegen Datei/Commit verifizieren, bevor gefixt wird; Prüfer
  den Code selbst lesen lassen statt Diffs inline zu übergeben; nach zwei Prüfrunden Rest als Folgeaufgabe statt Endlosschleife.
- **Aufwand:** S

### P-03 · veraltet · P2 · Claude↔Codex nur in eine Richtung
- **Ort:** `block-3-advanced.md:422` („Codex generates code fast and cheap. Claude Opus reviews with high judgment.")
- **Beleg:** Arbeitsteilungs-Richtlinie des Autors (Stand 2026-07): „Claude denkt breit, Codex setzt eng um …
  Beide prüfen einander dort, wo der jeweils andere blinde Flecken hat." In der Praxis prüft Codex regelmäßig
  Claude-/Sonnet-Ergebnisse (siehe P-01), nicht nur umgekehrt.
- **Vorschlag:** Die Multi-Model-LE auf gegenseitige Prüfung umstellen: Rollen nach Stärke, Prüfung jeweils durch
  das andere Modell; Beispiel aus P-01 als Fallstudie.
- **Aufwand:** S

### P-04 · fehlt · P2 · Tests, die ein Agent startet, dürfen keine echten Daten treffen
- **Ort:** S3.13 (Autonome Loops absichern) oder Sicherheitsblock S3.6–S3.9; Übungsanschluss Playground.
- **Beleg:** Zwei reale Vorfälle im eigenen Setup (2026-04-29, 2026-05-29): Eine von Agenten gestartete Testsuite
  leerte echte SQLite-Datenbanken. Ursache beim zweiten Mal: Der DB-Pfad war eine Modul-Konstante, zur Import-Zeit
  eingefroren; Test-Overrides per Umgebungsvariable griffen deshalb nicht. Seither Regel: DB-Pfad als Funktion,
  zwei harte Guards, Zeilenzahl-Schnappschuss vor/nach dem Lauf. Kurs: einziger Treffer zu Produktionsdaten ist
  `autoMode.hard_deny` (`block-3-advanced.md:797`); Testisolation wird nicht gelehrt.
- **Vorschlag:** Fallstudie + Übung „Beweise die Isolation": Playground bekommt ein kleines Datenmodul mit
  eingefrorenem Pfad; Aufgabe ist, das Risiko zu finden, auf lazy umzubauen und per Schnappschuss zu belegen.
  Passt zur Security-Zielgruppe (Fail-safe-Denken) und zum Versprechen „Production-Operations".
- **Aufwand:** M

### P-05 · fehlt · P2 · Headless `claude -p` als Unterprozess härten
- **Ort:** S4.3 (Headless Mode), S4.4/S4.5 (CI)
- **Beleg:** Betriebsnotiz 2026-05-31 (sechs Funde im Echtbetrieb): Headless-Aufrufe erben Hooks aus den
  Nutzer-Settings; ohne Tool-/Permission-Vorgaben hängt der Prozess an einer Rückfrage; lange Prompts als
  Argument werden unter Windows vom `.cmd`-Wrapper zerlegt (stdin nutzen); eine gesetzte `ANTHROPIC_API_KEY` in
  der Umgebung schaltet unbemerkt von Abo auf API-Abrechnung; Ausgabe zuerst parsen, dann Exit-Code werten.
  Kurs: `grep -- "--settings\|disableAllHooks"` in modules/cheatsheet = 0 Treffer. `claude --help` (2.1.283)
  bietet dafür heute u. a. `--bare` (überspringt Hooks, Plugins, Auto-Memory, CLAUDE.md-Suche), `--settings`,
  `--tools`, `--permission-mode`.
- **Vorschlag:** Checkliste „Headless sicher aufrufen" in S4.3, mit `--bare` als neuer Standardempfehlung für
  Pipelines (Faktencheck der Flags vorausgesetzt).
- **Aufwand:** S

### P-06 · unklar · P2 · `--max-turns`: Kurs sagt „existiert nicht", eigene Produktion nutzt es
- **Ort:** Kursweit entfernt in Welle A/B (Juni, Begründung „Flag existiert nicht in CLI v2.1.185").
- **Beleg:** `claude --help` 2.1.283 listet `--max-turns` nicht. Eigene Werkzeuge rufen `claude -p` aber mit
  `--max-turns 1` auf (laufendes Tool im Orchestrator, Stand 2026-09), laut Betriebsnotiz 2026-05-31 gegen das
  echte Binary getestet. Möglich: verstecktes, aber funktionierendes Flag. `claude --max-turns 1 --version` ist
  kein Beweis (`--version` bricht vor der Optionsprüfung ab; ein erfundenes Flag verhält sich gleich).
- **Vorschlag:** Einmal real testen (`claude -p --max-turns 1 "…"` gegen ein erfundenes Flag als Gegenprobe) und
  danach Kurs oder eigene Regel korrigieren. Wer sich irrt, ist offen.
- **Aufwand:** S

### P-07 · fehlt · P2 · Hooks kosten Zeit bei jedem Tool-Aufruf
- **Ort:** S2.8 ff. (Hooks), Andockpunkt für das Versprechen „Token-Ökonomie und Kosten-Patterns".
- **Beleg:** Messung 2026-07-28 im eigenen Setup: vier Hooks mit `matcher=*` kosten zusammen rund 232 ms pro
  Tool-Aufruf (~46 s auf 200 Aufrufe); der größte Teil ist Interpreter-Start (~43 ms je Python-Hook), nicht
  Skriptlogik. Kurs lehrt viele Hooks, aber kein Hook-Budget.
- **Vorschlag:** Kasten „Hook-Budget": Matcher eng fassen, Hooks bündeln, Startzeit messen; Messrezept als Mini-Übung.
- **Aufwand:** S

### P-08 · fehlt · P2 · Kosten messen statt schätzen
- **Ort:** S1.19 (Cost-Basics), S4.4 (Cost-Engineering); Versprechen „Token-Ökonomie".
- **Beleg:** Eigenes Token-Dashboard (2026-08): Nur die Auswertung mit `ccusage` stimmte mit der Abrechnung überein;
  ein naiver Walk über Session-Transkripte zählte zu hoch. Kurs: `grep -r ccusage` in modules/cheatsheet = 0 Treffer.
- **Vorschlag:** Token-Ökonomie-Modul mit echten, eigenen Messdaten (Subagent vs. langer Hauptlauf, Caching-Effekt,
  Hook-Kosten aus P-07), Messwerkzeug benennen, Zählfallen zeigen.
- **Aufwand:** M

### P-09 · fehlt · P2 · Unbeaufsichtigte Läufe betreiben (Not-Aus, Bericht, Überspringen)
- **Ort:** S3.12/S3.13 (Scheduling, abgesicherte Loops); Versprechen „Production-Operations".
- **Beleg:** Nächtlicher Konsolidierungslauf seit 2026-09-24: geplanter Task, Not-Aus-Datei, JSONL-Bericht je Lauf,
  überspringt aktive Sitzungen und zu alte Arbeit, erntet headless nur mechanische Daten und lässt Urteilsfragen
  (Learnings, Entscheidungen) bewusst liegen. Kurs lehrt `/schedule`, Routines und Budget-Caps, aber nicht
  Not-Aus, Laufbericht und die Grenze „was darf ein Agent unbeaufsichtigt entscheiden".
- **Vorschlag:** Production-Ops-LE mit diesem Lauf als Fallstudie: Not-Aus, Idempotenz, Bericht, Alarm,
  Urteils-Grenze. Security-Analogie liegt nahe (Nachtwache mit Wachbuch und Notschalter).
- **Aufwand:** M

### P-10 · fehlt · P2 · Arbeitsprozess nach Größe (Spec → Plan → Umsetzung → Beleg)
- **Ort:** S1.x (Prompting/Plan Mode) und Capstone S4.8.
- **Beleg:** Seit 2026-08 eigener Prozess: Größe S/M/L entscheidet das Prozessgewicht (S: drei Sätze Design;
  M: Spec + Plan; L: Spec + Tickets, eine frische Sitzung je Ticket), Belegpflicht vor jeder Erfolgsmeldung.
  Kurs erwähnt Superpowers (`block-2-ecosystem.md`, `block-2-demos.md`), lehrt aber keinen durchgängigen,
  größenabhängigen Ablauf; der Capstone bewertet das Ergebnis, nicht den Prozess.
- **Vorschlag:** Kurze LE „Wie viel Prozess braucht diese Aufgabe?" vor dem Capstone; Capstone-Rubrik um
  Prozess-Kriterien (Plan vorhanden, Beleg vor Erfolgsmeldung) ergänzen.
- **Aufwand:** M

### P-11 · fehlt · P2 · Lese-Tools können Geheimnisse mitlesen
- **Ort:** MCP-Sicherheit in Block 2 (S2.x MCP), Browser-MCP-Übung 2.4.
- **Beleg:** Betriebsnotiz 2026-09: Browser-Tools zum Finden/Auslesen von Seitenelementen lieferten auf einer
  Token-Seite Nachbartext mit, also Geheimnisse im Agenten-Kontext. Kurs behandelt Prompt Injection
  (`block-2-ecosystem.md`, `cheatsheet.md`), aber nicht Datenabfluss durch Lese-Tools.
- **Vorschlag:** Einen Absatz plus Regel („auf Seiten mit Geheimnissen nur Screenshot/Klick, nie Text-Extraktion")
  in die MCP-Sicherheits-LE.
- **Aufwand:** S

### P-12 · fehlt · P3 · Parallele Sitzungen im selben Repo
- **Ort:** S1.16 (Git-Workflow), S3.x Worktrees.
- **Beleg:** Wiederholt beobachtet (2026-05 bis 2026-09): zwei Sitzungen arbeiten am selben Repo; frische,
  fremde Änderungen im Arbeitsverzeichnis. Regel seither: vor Übernahme `git status` + Änderungszeiten prüfen,
  bei frischer fremder Drift nur lesen. Kurs hat die Stage-Regel bereits (`demos/block-1-demos.md:489`,
  „don't `git add -A`") — gute Basis.
- **Vorschlag:** Die vorhandene Stage-Regel um „fremde Änderungen erkennen" erweitern.
- **Aufwand:** S

### P-13 · fehlt · P3 · Gedächtnis braucht Pflege, nicht nur Anlegen
- **Ort:** S1.x Context & Memory (Auto-Memory, CLAUDE.md).
- **Beleg:** Eigene Gedächtnis-Analyse 2026-09-24: Ein Abruf-Ledger über 458 gespeicherte Erinnerungen zeigte
  299, die nie abgerufen wurden. Kurs lehrt Anlegen und Scopes von Memory, nicht Messen und Ausdünnen.
- **Vorschlag:** Kurzer Deep-Dive „Memory-Hygiene": messen, was tatsächlich abgerufen wird; Index klein halten.
- **Aufwand:** S

### P-14 · stärke · — · Was der Kurs aus der Praxis schon richtig hat
- Chirurgisches Stagen statt `git add -A` (`demos/block-1-demos.md:489`).
- Budget-Cap vor Loops (`--max-budget-usd`, S3.13) und Worktree-Isolation.
- Modell pro Phase statt ein Modell für alles (S4.1).
- Windows-Tauglichkeit der Hook-Beispiele (Welle C) — im eigenen Alltag weiterhin der häufigste Stolperstein.

## Zählung

| Art | P1 | P2 | P3 | gesamt |
|---|---|---|---|---|
| fehlt | 1 | 8 | 2 | 11 |
| veraltet | 0 | 1 | 0 | 1 |
| unklar | 0 | 1 | 0 | 1 |
| stärke | — | — | — | 1 |

## Was ich nicht prüfen konnte und warum

- P-06 (`--max-turns`) braucht einen echten Headless-Aufruf; bewusst nicht in dieser Bewertung ausgeführt.
- P-05: Die heutige Semantik von `--bare`, `--tools` und `--permission-mode` stammt aus `claude --help` 2.1.283,
  nicht aus einem Lauf. Verifikation gehört in den Faktencheck/Umsetzungsschritt.
- Ob die Fallstudien öffentlich erzählt werden sollen (P-01, P-04, P-09), entscheidet der Autor; die Befunde
  sind so formuliert, dass sie ohne private Pfade und Namen auskommen.
