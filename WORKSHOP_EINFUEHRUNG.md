# Workshop-Einführung

> Dieses Repository ist ein praxisnaher Claude-Code-Workshop für erfahrene Entwickler.
> 4 Sessions à ~3h, 17 Module → 48 Lerneinheiten (Block 3 auf Session 3+4 verteilt), demo-lastig mit optionalen Hands-on-Exercises.

## Einordnung

Dieses Repo ist die Materialbasis zur DoMe-Dynamics-Seite:

- Website-Ueberblick: https://dynamic-dome.com/workshop
- Werkstatt-Kontext: https://dynamic-dome.com/werkstatt
- DCO-Kontext: https://dynamic-dome.com/dco

Die Website ist das kuratierte Schaufenster. Dieses Repository ist der Arbeitsnachweis: Module, Demos, Exercises, Mentor-Agent, Plugin-Struktur und Playground.

## Wie nutze ich dieses Repo?

**Als Selbstlerner:**
1. Lies zuerst `resources/prerequisites.md` (Setup)
2. Dann `resources/workshop-guide.md` (Orientierung)
3. Arbeite Block für Block durch — `resources/modules/`, `resources/demos/`, `resources/exercises/`
4. Nutze `resources/cheatsheet.md` und `resources/quick-reference.md` als Referenz

**Als Workshop-Moderator:**
1. Lies `resources/session-plan.md` für Zeitplan
2. Prüfe `resources/prerequisites.md` und schicke an Teilnehmer min. 1 Woche vorher
3. Demos vorher proben (siehe Recovery-Notes in `resources/demos/`)
4. Nutze `resources/troubleshooting.md` als Notfall-Referenz

**Als Reviewer / Tech Lead:**
1. Lies zuerst die Website-Seite, um die Rolle des Workshops im Gesamtportfolio zu verstehen
2. Pruefe dann `resources/session-plan.md`, `resources/modules/` und `resources/demos/`
3. Fuehre den Playground-Test aus: `cd workshop-playground && python3 -m pytest -v`
4. Pruefe `agents/workshop-mentor.md`, wenn dich der guide/learn-Modus interessiert

## Verzeichnisstruktur

| Ordner / Datei | Zweck |
|---|---|
| `resources/modules/` | Lehrmaterial pro Block (Block 1/2/3) |
| `resources/demos/` | Demo-Scripts mit Recovery-Notes |
| `resources/exercises/` | Hands-on-Übungen |
| `resources/cheatsheet.md` | Vollständige Schnellreferenz (~800 Zeilen) |
| `resources/quick-reference.md` | 1-Pager Quick-Reference (druckbar) |
| `resources/glossary.md` | Begriffsdefinitionen |
| `resources/faq.md` | Häufige Fragen |
| `resources/troubleshooting.md` | Top-Probleme + Lösungen |
| `resources/security-analogies.md` | Single-Source Physical-Security-Mappings |
| `resources/session-plan.md` | Zeitplan pro Session |
| `resources/prerequisites.md` | Setup vor Workshop |
| `workshop-playground/` | Übungsprojekt mit absichtlichen Vulnerabilities |
| `.claude-plugin/` | Plugin-Manifest |
| `agents/workshop-mentor.md` | Mentor-Agent für Fragen |
| `commands/workshop.md` | `/workshop`-Command |
| `skills/workshop/SKILL.md` | Workshop-Skill (guide/learn Modi) |

## Block-Übersicht

- **Block 1 — Foundations** (5 Module): What is Claude Code, Context & Memory, Effective Prompting, Git Integration & Worktrees, Cost Engineering
- **Block 2 — Ecosystem** (5 Module): Skills & Commands, Hooks, Plugins, MCP, RAG & NotebookLM
- **Block 3 — Advanced** (7 Module): Agents & Multi-Agent, Multi-Model Pipelines, Security & Adversarial Testing, Scheduled Tasks, Telegram/Inception/Worktrees, CI/CD & Headless Mode, Troubleshooting & Debugging

## Empfehlung für verschiedene Leser

- **Moderator / Maintainer:** `README.md`, `resources/session-plan.md`, `resources/prerequisites.md`, `resources/troubleshooting.md`
- **Teilnehmer:** `resources/prerequisites.md`, `resources/workshop-guide.md`, `resources/cheatsheet.md`, `resources/quick-reference.md`
- **Selbstlerner ohne Workshop:** `resources/workshop-guide.md`, dann blockweise `modules/`, `demos/`, `exercises/`

Stand: 2026-05-20.
