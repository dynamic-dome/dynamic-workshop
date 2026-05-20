# Workshop Session Plan

> Zeitlicher Ablauf und didaktischer Aufbau über alle 3 Sessions.
> Stand: 2026-05-20.

## Format-Übersicht

| Session | Block | Thema | Dauer | Termin |
|---|---|---|---|---|
| 1 | Block 1 | Foundations | ~3h | 10. April 2026 (durchgeführt) |
| 2 | Block 2 | Ecosystem | ~3h | TBD |
| 3 | Block 3 | Advanced | ~3h | TBD |

## Session 1 — Foundations (~3h)

**Mission:** Was ist Claude Code und warum ist es anders als ChatGPT?

| Zeit | Komponente | Inhalt |
|---|---|---|
| 0:00 – 0:15 | Intro + PPT | Welcome, Workshop-Format, PowerPoint-Slides als visueller Einstieg |
| 0:15 – 0:30 | Modul 1.1 | What is Claude Code? — drei Interfaces, Permissions, Models |
| 0:30 – 0:40 | Demo 1.1 | First Contact — Log-Parser in 3 Min |
| 0:40 – 0:55 | Modul 1.2 | Context & Memory — CLAUDE.md, Auto-Memory, Rules |
| 0:55 – 1:05 | Demo 1.2 | CLAUDE.md anlegen, /compact zeigen |
| 1:05 – 1:25 | Exercises 1.1 + 1.2 | Hands-on |
| 1:25 – 1:35 | **Pause** | |
| 1:35 – 1:50 | Modul 1.3 | Effective Prompting — Vager vs. präziser Prompt |
| 1:50 – 2:00 | Demo 1.3 | Good vs Bad Prompting Side-by-Side |
| 2:00 – 2:15 | Modul 1.4 | Git Integration & Worktrees |
| 2:15 – 2:25 | Demo 1.4 | Branch → Feature → Commit → PR Flow |
| 2:25 – 2:50 | Exercises 1.3 + 1.4 | Hands-on |
| 2:50 – 3:00 | Q&A + Ausblick Session 2 | |

## Session 2 — Ecosystem (~3h)

**Mission:** Wie erweitert man Claude Code? Skills, Hooks, Plugins, MCP, RAG.

**Wichtig:** Exercises 2.1-2.5 nicht alle als Pflicht — "pick 2-3" reicht, sonst Zeitdruck.

| Zeit | Komponente | Inhalt |
|---|---|---|
| 0:00 – 0:10 | Recap Session 1 + Intro Block 2 | |
| 0:10 – 0:25 | Modul 2.1 | Skills & Commands — Skill-Authoring |
| 0:25 – 0:35 | Demo 2.1 | TDD-Skill in Action |
| 0:35 – 0:50 | Modul 2.2 | Hooks — Event-Listener |
| 0:50 – 1:00 | Demo 2.2 + 2.2b | Security-Hook (rm-rf-Block), Secure Diff Gate |
| 1:00 – 1:25 | Exercises 2.1 + 2.2 | Hands-on |
| 1:25 – 1:35 | **Pause** | |
| 1:35 – 1:45 | Modul 2.3 | Plugins — Packaging |
| 1:45 – 1:55 | Demo 2.3 | Plugin-Anatomie |
| 1:55 – 2:10 | Modul 2.4 | MCP — Browser, DBs, externe Services |
| 2:10 – 2:25 | Demo 2.4 | Playwright MCP live |
| 2:25 – 2:40 | Modul 2.5 + Demo 2.5 | RAG & NotebookLM |
| 2:40 – 2:55 | Exercise (pick 1 von 2.3/2.4/2.5) | Hands-on |
| 2:55 – 3:00 | Q&A + Ausblick Session 3 | |

## Session 3 — Advanced (~3h)

**Mission:** Multi-Agent, Security, Automation, CI/CD, Troubleshooting.

| Zeit | Komponente | Inhalt |
|---|---|---|
| 0:00 – 0:10 | Recap Session 2 + Intro Block 3 | |
| 0:10 – 0:25 | Modul 3.1 | Agents & Multi-Agent + Background-Sessions |
| 0:25 – 0:40 | Demo 3.1 | 2 parallele Agents |
| 0:40 – 0:50 | Modul 3.2 + Demo 3.2 | Multi-Model Pipelines / Codex Swarm |
| 0:50 – 1:10 | Modul 3.3 + Demo 3.3 | Security & Adversarial Testing |
| 1:10 – 1:20 | **Pause** | |
| 1:20 – 1:35 | Modul 3.4 + Demo 3.4 | Scheduled Tasks, Loops, /goal |
| 1:35 – 1:50 | Modul 3.6 (NEU) | CI/CD & Headless Mode |
| 1:50 – 2:05 | Modul 3.7 (NEU) | Troubleshooting & Debugging |
| 2:05 – 2:20 | Modul 3.5 + Demo 3.5 | Telegram-Bridge, Inception, Worktrees |
| 2:20 – 3:00 | Exercise 3.5 | Architecture Discussion (Capstone) |

## Didaktischer Aufbau

Jeder Block folgt demselben Muster:
1. **Konzept verstehen** — Modul lesen
2. **Live-Demo sehen** — Demo nachvollziehen
3. **Selbst ausprobieren** — Exercise lösen
4. **Mit Cheat Sheet absichern** — Quick-Reference

Block 1 ist Pflicht. Block 2 und 3 vertiefen — auch teilweise OK.

## Pausen

Pro Session ~10-15 Min Pause nach ~90 Min. Zusätzlich: Q&A zwischen Modulen.

## Pflicht vs Optional

**Pflicht in jeder Session:** Modul-Inputs + Hauptdemo + mindestens 1 Exercise.

**Optional je nach Zeit:**
- Bonus-Exercises (markiert)
- Sub-Demos (2.2b, 3.3b, 3.3c)
- Advanced-Themen aus Module 3.5 (Telegram/Inception/Channels)

## Materialien pro Session

| Session | Mitbringen | Vorbereitung |
|---|---|---|
| 1 | Laptop, claude installiert, GitHub-Account | `resources/prerequisites.md` durchgearbeitet |
| 2 | Session-1-Setup + Playwright-Browser, NotebookLM-Account | Plugin-Bundle installiert (siehe `prerequisites.md` Sektion "Workshop-Plugins") |
| 3 | Session-2-Setup + Codex-CLI (falls verfügbar) | Workshop-Playground geklont |

---

*Letzter Stand: 2026-05-20*
