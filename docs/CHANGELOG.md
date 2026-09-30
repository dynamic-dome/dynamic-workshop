# Changelog

## 2026-09-30 — Praxisbibliothek

Der Kurs wird vom linearen 4-Session-Aufbau zur deutschsprachigen Praxisbibliothek (Branch `praxisbibliothek`).

- **Bibliothek:** 68 Kapitel (65 Lerneinheiten, neu S0.1 Werkstatt einrichten, X.1 Community-Skills, X.2 Mit Claude Code
  lernen) in 19 Regalen, fester Aufbau je Kapiteltyp, Kapitel als einzige Quelle; Modul-, Demo- und Übungsdateien entfallen.
- **Einstufung:** Ziel, Warum, Sitzungslänge, Stand in 14 Bereichen, freiwillige Mini-Szenarien; deterministische Engine
  (`tools/placement.py`, JS-Port im Cockpit, 15 Personas als Vertrag), Sicherheitsboden für neun Kapitel.
- **Cockpit:** neu gebaut (Start, Einstufung, Mein Pfad, Bibliothek als Gebäudeplan, Kapitel, Wiederholen), aus den
  Kapiteln generiert; fail-soft Speicher, keine Inline-Handler, Browser-Verhaltenstests statt Wortlaut-Tests.
- **Tutor:** `/dynamic-workshop:workshop start | next | learn | review | guide` im Stil von Matt Pococks `teach`;
  Mentor ohne Inhaltskopie; überflüssiges `commands/workshop.md` entfernt.
- **Referenz und Moderation:** druckbare Referenzkarten statt Cheatsheet-Nachbau; ein Moderations-Handbuch statt
  sechs Einzeldateien; Review-Archive nach `docs/reviews/`.
- **Deck:** neuer Foliensatz aus dem Katalog mit bearbeitbaren Diagrammen und Sprechernotizen.
- **Korrekturen beim Umzug** (belegt): u. a. `UserPromptSubmit` kann Prompts nicht umschreiben; Hook-Änderungen werden
  ohne Neustart übernommen; Playground hat fünf Schwachstellen; `--plugin-dir` zeigt auf den Plugin-Ordner.
- **Prüfung:** Spec in vier Codex-Runden bis zur Freigabe, Gate-A-Verifier auf die Werkzeuge, Aussagen-Matrix je Kapitel
  durch unabhängige Prüfer, Snippet-Ledger gegen den Basis-Commit `ba222d2`.
