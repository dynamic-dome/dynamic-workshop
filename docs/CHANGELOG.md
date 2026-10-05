# Changelog

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
