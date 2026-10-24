# Changelog

## 2026-10-24 — Aktualitätslauf: Haiku 4.5 wieder überwacht, Nachprüf-Hook für `version-pinned`

- **Aktualität (Todo #9957):** Die Regel „retiring“ meldet bei Status `Active` und verstrichenem „Not sooner than“-Datum nicht mehr rot,
  sondern nur Info (`retiring-unannounced:…`): Das Datum ist eine Untergrenze, keine Abschaltankündigung. Eine angekündigte Abschaltung
  ändert den Status auf der Deprecations-Seite und bleibt über `canon-status` rot (Vorlauf mindestens 60 Tage). Haiku 4.5 steht als Legacy-Zeile
  wieder in der überwachten Kanon-Tabelle, dazu Sonnet 4.6 und Opus 4.6 (die Anbieter-Aliase lösen noch darauf auf). Sonnet 4.5 bleibt draußen:
  Es ist seit 30.09.2026 `Deprecated` und würde den Lauf bis zur Abschaltung am 30.11.2026 rot halten.
- **Aktualität (Todo #9518, Rest):** Neuer Nachprüf-Hook: Jede Kurszeile mit `version-pinned: <Grund>` wird im Monatslauf gegen die
  Deprecations-Tabelle gelesen. Modell nicht mehr `Active` oder unbekannt = gelb (`pinned-status:`/`pinned-unknown:`), aktives Modell = Info
  (`pinned-active:`, Liste zum Nachlesen), Grund „histor…“ = Info (`pinned-historical:`). Der Kurs enthält zurzeit keine solche Zeile.
- **Nachtrag (Prüfung):** Auch das Fenster von weniger als 60 Tagen vor dem Frühestdatum ist bei Status `Active` nur Info
  (`retiring-soon-unannounced:…`), sonst wären Opus 4.6 (5.2.2027) und Sonnet 4.6 (17.2.2027) im Januar und Februar 2027 ohne Ereignis rot
  geworden. Rot `retiring:` gilt nur noch bei Status außer `Active`. Der Nachprüf-Hook liest datierte IDs einstelliger Generationen
  (`claude-sonnet-4-20250514`) als Familie plus Version, nicht als Version (4, 20250514).

## 2026-10-24 — Kanon auf CLI 2.1.310: Haiku 5.5, `claude -p` startet in `default`

- **Kanon:** Haiku 5.5 (`claude-haiku-5-5`, Active, frühestens 7.10.2027, 1M Kontext, 0.10 $ / 0.50 $, über 100K Prompt 0.50 $ / 2.50 $,
  Effort `low` bis `max`, Start `medium`, ab CLI 2.1.293) ersetzt Haiku 4.5 in der überwachten Tabelle. Haiku 4.5 ist Legacy:
  Die Deprecations-Seite führt es als Active mit „Not sooner than October 15, 2026", eine Abschaltung ist nicht angekündigt (der
  Monatslauf meldete das Datum zu Recht als Frist, es ist aber keine Abschaltung). Alias-Tabelle um die Spalte `haiku` erweitert, Effort-Tabelle,
  Auto-Modus-Modellliste und die Zeile zu `claude -p` (ab 2.1.302 immer `default`) nachgezogen. Quellen: models/overview.md,
  model-deprecations.md, about-claude/pricing.md, code.claude.com model-config.md und permission-modes.md, Changelog 2.1.293 und 2.1.302. Todo #9946.
- **Kapitel und Karten:** S1.6, S3.8, Karte „Rechte" und Karte „Start und Flags" folgen dem Kanon (Startmodus bei `-p`;
  `auto` ist mit Haiku 5.5 verfügbar, nicht mehr „nie Haiku").
- **Nachtrag (Prüfung):** Auch S4.3 (Startmodus bei `-p`, Abschnitt und Fallen) folgt jetzt dem Kanon. S1.6 formuliert die Ablehnung im Lauf ohne Mensch genauer (Aufrufe, die eine Freigabe bräuchten; Allow-Regel oder Hook). Die Karten „Rechte“ und „Start und Flags“ vermerken, dass nur die `claude -p`-Angaben am 2026-10-24 neu geprüft wurden.
- **Offen:** Die Aussagen „Haiku hat ein kleines Kontextfenster, kennt keinen Effort, kostet ein Viertel von Opus" (S1.7 samt Quiz und
  Diagramm, S1.19 Schritt 3, Moderation S1.19, Glossar, Karte „Kosten") stimmen für `haiku` auf der Anthropic API nicht mehr; Folge-Todo.

## 2026-10-24 — Aktualitätslauf: „Fixed“ zählt als Info

- **Aktualität:** Gelbe Changelog-Befunde vom Typ „Fixed“ (Zeile beginnt mit „Fixed“, auch hinter „[VSCode]“, dem in der Quelle maskierten „\[VSCode]“,
  „**Security:**“ oder „Windows:“; Labels wie „Changed …:“ zählen nicht) sind im Monatslauf jetzt Info (Schlüssel `changelog-fixed:…`), nicht gelb; sie zählen nicht mehr für den
  Exit-Code und `finding_keys`. Anlass: Abschluss-Review, rund 82 Gelb-Befunde je Monat, davon etwa 60 % „Fixed“-Zeilen
  (Todo-Müdigkeit). Owner-Entscheid F9 vom 22.10.2026, gilt vor dem ersten Monatslauf am 01.11. Offen bleibt der
  Nachprüf-Hook für version-pinned-Zeilen.
- **Aktualität:** `changelog_since` liest zusätzlich das Live-Format von code.claude.com (seit Oktober 2026:
  `**2.1.310**`, Datumszeile, Gruppen `**Added**`/`**Changed**`/`**N improvements**`/`**N bug fixes**`); das alte
  `<Update label="x.y.z">` bleibt für Altberichte. Ohne das brach der Monatslauf am 01.11. mit „Changelog: reicht nicht
  bis Version … zurück“ ab. Die Gruppe „bug fixes“/„Fixed“ zählt als Info (F9), auch ohne „Fixed“ am Zeilenanfang;
  `changelog_entries_since` liefert dafür (Version, Gruppe, Zeile). Fixture: `tools/fixtures/currency/changelog-live-2026-10-24.md`
  (gekürzter Auszug). Todo #9942.

## 2026-10-05 — Selbstlernende zuerst (Branch `selbstlern-zuerst`, läuft)

Anlass: Durchsicht vom 2026-10-05 (`docs/reviews/2026-10-05-lernbogen-und-fakten.md`, Befunde R1 bis R31). Entwurf und
Pakete: `docs/plans/2026-10-05-selbstlern-zuerst-design.md`, `…-tickets.md`.

- **Hook-Vorlagen (R1):** `secure-diff-gate.sh` und `.py` blocken jetzt, wenn sie ihre Eingabe nicht lesen können (kein
  `jq`, kein JSON, leer), und erkennen `.ENV` in jeder Schreibweise. Vorher endete die Bash-Fassung ohne `jq` mit 127,
  die Python-Fassung gab bei kaputter Eingabe 0 zurück; beides blockt nicht. Der dokumentierte Windows-Aufruf mit
  `%USERPROFILE%` wurde von keiner Hook-Shell aufgelöst; jetzt `python "$HOME/.claude/hooks/secure-diff-gate.py"`.
  S2.10 nennt die Grenze des Gates (Shell-Befehle) und die Deny-Regel als Ergänzung.
- **Formulierung (R2):** „blockt nur mit `exit 2`“ heißt jetzt überall „von den Exit-Codes blockt nur 2“, mit Verweis auf
  die JSON-Entscheidung.
- **Moderationsschicht (P1):** „Vorführen“ ist kein Abschnitt der Kapitel mehr. Demo und Hinweise für Moderierende
  stehen je Kapitel in `resources/moderation/vorfuehren/` (30 Dateien, per Skript verschoben, 12.884 Wörter vorher wie
  nachher). Der Validator weist „Vorführen“ und Blöcke „Für Moderierende“ im Kapitel ab und prüft die Demo-Dateien;
  der Katalog führt je Kapitel `demo`, der Live-Pfad verlinkt die Demos, der Tutor liest sie nur im Modus `guide`.
  Vier Lektionen, deren Cockpit-Beispiel in der Demo stand (S1.2, S3.13, S3.14, S4.6), haben einen Unterabschnitt
  „Ausprobieren“; S3.14 nutzt dafür `/goal` statt des entfallenen Plugin-Befehls.
- **Cockpit und Tutor (P2):** Sagt die Einstufung „durcharbeiten“, öffnet das Cockpit das Kapitel mit vollem Text und
  Übung statt der Kurzfassung; das Quiz und „Als erledigt markieren“ stehen am Ende. Der Tutor geht bei solchen
  Kapiteln durch „Im Detail“, bevor die Übung kommt.
- **Auflösungen (P3):** Abruffragen können eine Auflösung tragen (eingeklappter Block im Abschnitt „Check“). Der
  Validator prüft, dass je Frage genau eine Antwort dasteht; das Cockpit zeigt die Fragen jetzt auch in der Kurzansicht,
  je Frage mit eigener Auflösung. Erstes Kapitel: S1.1. `validate` meldet den Fortschritt (Übungen, Auflösungen).
- **Playground (P4):** Die Lösungen liegen jetzt in `resources/reference/playground-loesungen.md`. Die `CLAUDE.md` des
  Playgrounds und die Kommentare im Code nennen keine Schwachstelle mehr; vorher las Claude Code die Liste in jeder
  Sitzung mit. Das Verhalten des Codes ist unverändert.

## 2026-10-02 — Einstufung: Sicherheitsboden bei Ziel Sicherheit

- **Einstufung:** Bei Ziel `security` gehören jetzt auch S3.13 (Autonome Loops absichern) und S4.4 (CI-Zugangsdaten) zum
  Pfad. Bisher standen sie unter „später — gehört nicht zu deinem Ziel“, obwohl sie den Sicherheitsboden tragen, weil
  die Schwerpunkt-Regale von `security` `automation` und `headless-ci` nicht enthalten. Umgesetzt als gezielte Ausnahme
  über `chapter_goals` (Lesson-/Setup-Kapitel kommen zusätzlich in die Relevanzmenge, wenn eines der Ziele gewählt ist;
  bei Community-Kapiteln bleibt es die Einschränkung). Die Regale des Ziels bleiben unverändert; `schnellstart` und
  `moderieren` ebenfalls. Python-Engine, JS-Port, Spec §6.3 A und Golden-Datei angepasst.

## 2026-09-30 — Praxisbibliothek

Der Kurs wird vom linearen 4-Session-Aufbau zur deutschsprachigen Praxisbibliothek (Branch `praxisbibliothek`).

- **Bibliothek:** 70 Kapitel (65 Lerneinheiten, neu S0.1 Werkstatt einrichten, X.1 Community-Skills, X.2 Mit Claude Code
  lernen, X.3 Pi als Spiegel, X.4 Agenten im Dauerbetrieb mit OpenClaw) in 19 Regalen, fester Aufbau je Kapiteltyp,
  Kapitel als einzige Quelle; Modul-, Demo- und Übungsdateien entfallen (Snippet-Ledger: 357 von 357 alten Codeblöcken
  erfasst, auch in Blockzitaten; 63 begründet gestrichen).
- **Einstufung:** Ziel, Warum, Sitzungslänge, Stand in 14 Bereichen, freiwillige Mini-Szenarien; deterministische Engine
  (`tools/placement.py`, JS-Port im Cockpit, 17 Personas als Vertrag), Sicherheitsboden für neun Kapitel; X.3/X.4 nur
  für die Ziele Agenten, Sicherheit und Einschätzen (`chapter_goals`).
- **Cockpit:** neu gebaut (Start, Einstufung, Mein Pfad, Bibliothek als Gebäudeplan, Kapitel, Wiederholen), aus den
  Kapiteln generiert, mit Volltext aller Kapitel und 61 Diagrammen offline (2,6 MB, gzip rund 0,5 MB); fail-soft
  Speicher, keine Inline-Handler, Browser-Verhaltenstests statt Wortlaut-Tests.
- **Tutor:** `/dynamic-workshop:workshop start | next | learn | review | guide` im Stil von Matt Pococks `teach`;
  Mentor ohne Inhaltskopie; überflüssiges `commands/workshop.md` entfernt.
- **Referenz und Moderation:** druckbare Referenzkarten statt Cheatsheet-Nachbau; ein Moderations-Handbuch statt
  sechs Einzeldateien; Review-Archive nach `docs/reviews/`.
- **Deck:** neuer Foliensatz aus dem Katalog mit bearbeitbaren Diagrammen und Sprechernotizen, Schrift ab 14 pt.
- **Aktualität:** der Monatslauf beobachtet zusätzlich die Fremdprojekt-Quellen der Community-Kapitel (gelb bei
  Änderung, ohne Einfluss auf die Claude-Code-Bezeichnerprüfung); Mindest-CLI je Modellgeneration steht im Kanon.
- **Korrekturen beim Umzug** (belegt): u. a. `UserPromptSubmit` kann Prompts nicht umschreiben; Hook-Änderungen werden
  ohne Neustart übernommen; Playground hat fünf Schwachstellen; `--plugin-dir` zeigt auf den Plugin-Ordner;
  Shell-Hooks registrieren sich unter Windows mit `matcher: "Bash|PowerShell"` (ein reiner `Bash`-Hook feuert mit dem
  PowerShell-Tool nie), die Schutz-Vorlagen kennen PowerShell-Befehle; CI-Beispiele mit offiziellem Installer und
  minimalen `permissions`; NotebookLM-Befehle der tatsächlich genutzten CLI (`notebooklm-py`).
- **Prüfung:** Spec in vier Codex-Runden bis zur Freigabe, Gate-A-Verifier auf die Werkzeuge, Aussagen-Matrix je Kapitel
  durch unabhängige Prüfer, Snippet-Ledger gegen den Basis-Commit `ba222d2`. Schlussprüfung (Gate B/C) durch drei
  unabhängige Prüfer: Stichprobe von 10 Kapiteln, alle 9 Sicherheitsboden-Kapitel, Werkzeuge; Befunde behoben, alle
  drei am Ende `pass`. Monatslauf live gegen die Doku: nur der bewusste Haiku-4.5-Hinweis bleibt rot.
