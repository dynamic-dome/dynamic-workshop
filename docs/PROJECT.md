---
project: dynamic_workshop (Claude Code Praxisbibliothek)
status: active
started: 2026-04
stack: [Markdown, Python, JavaScript (Cockpit), PowerShell]
repo: https://github.com/dynamic-dome/dynamic-workshop.git
---
# dynamic_workshop — Claude Code Praxisbibliothek

## Einzeiler

Deutschsprachige Praxisbibliothek, mit der Entwicklerinnen und Entwickler Claude Code nach ihrem Stand lernen: Einstufung, persönlicher Pfad, Kapitel. Zugleich das Material für einen moderierten Workshop in vier Sessions (Quelle: `README.md`, `CLAUDE.md`).

## Aktueller Stand

- Katalog: 71 Kapitel in 19 Regalen (`resources/library/catalog.json`, Felder `chapters` und `shelves`, Version 1).
- Plugin `dynamic-workshop` Version 2.0.0 (`.claude-plugin/plugin.json`).
- Aktualitätskanon `resources/_canonical.md`, Prüfdatum 2026-10-25, CLI 2.1.310.
- Git: Branch `main`, erster Commit 2026-04-09, 407 Commits (Stand 2026-10-25, `git rev-list --count HEAD`).
- Letzte Änderungen stehen in [CHANGELOG.md](CHANGELOG.md).

## Kernfähigkeiten

Siehe [CAPABILITIES.md](CAPABILITIES.md). Kurzfassung:

- Kapitel mit festem Aufbau, einzige Quelle für Lehrinhalte
- Einstufung mit persönlichem Pfad (Cockpit, Tutor `/dynamic-workshop:workshop`, Markdown)
- Aktualitätsprüfung gegen die offizielle Doku (Kanon, Lint, Monatslauf)
- getestete Hook-Vorlagen und ein Übungs-Playground mit fünf Schwachstellen

## Offene Baustellen

Aus dem Repo nicht belegbar, darum hier nur Verweise:

- Offene Arbeit führt das DCO (Todo-Datenbank), nicht dieses Repo.
- Der Export des Cockpits auf dynamic-dome.com liegt bei der Owner-Seite im Repo der Website (`HOW-TO-USE.md` §3); der Monatslauf meldet Abweichungen.
- Lizenz: Im Repo liegt keine LICENSE-Datei (offen, ob und welche gewollt ist).

## Abhängigkeiten

- Claude Code CLI und die offizielle Doku `code.claude.com/docs` als Primärquelle für alle Fakten (`CLAUDE.md`).
- Pflege: `pyyaml`, `markdown`, `python-pptx`, `playwright`, Node für `node --check` (`HOW-TO-USE.md` §3). Lernende brauchen für den Tutor nur Python (Standardbibliothek).

## Beziehungen zu anderen Projekten

- Schaufenster: Workshop-Seite von DoMe Dynamics, `dynamic-dome.com/systeme/workshop` (`README.md`). Die Website liegt in einem eigenen Repo.
- Einordnung laut `README.md`: Werkstatt (persönlicher Arbeitsmodus), DCO (gebautes agentisches System), Praxisbibliothek (Lernweg für Entwicklerteams).
