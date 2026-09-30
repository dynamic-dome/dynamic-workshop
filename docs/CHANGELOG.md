# Changelog

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
