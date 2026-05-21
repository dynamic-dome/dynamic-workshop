# Workshop Session Plan

> Zeitlicher Ablauf und didaktischer Aufbau über alle 3 Sessions.
> Stand: 2026-05-21.

## Format-Übersicht

| Session | Block | Thema | Dauer | Termin |
|---|---|---|---|---|
| 1 | Block 1 | Foundations | ~3h | 10. April 2026 (durchgeführt) |
| 2 | Block 2 | Ecosystem | ~3h | TBD |
| 3 | Block 3 | Advanced | ~3h | TBD |

## Session 1 — Foundations (~3h)

**Mission:** Was ist Claude Code, wie steuere ich es — und was kostet es?

| Zeit | Komponente | Inhalt |
|---|---|---|
| 0:00 – 0:15 | Intro + PPT | Welcome, Workshop-Format, PowerPoint-Slides als visueller Einstieg |
| 0:15 – 0:30 | Modul 1.1 | What is Claude Code? — drei Interfaces, Permissions, Models |
| 0:30 – 0:40 | Demo 1.1 | First Contact — Log-Parser in 3 Min |
| 0:40 – 0:55 | Modul 1.2 | Context & Memory — CLAUDE.md, Auto-Memory, Rules |
| 0:55 – 1:05 | Demo 1.2 | CLAUDE.md anlegen, /compact zeigen |
| 1:05 – 1:20 | Exercises 1.1 + 1.2 | Hands-on |
| 1:20 – 1:30 | **Pause** | |
| 1:30 – 1:45 | Modul 1.3 | Effective Prompting — Vager vs. präziser Prompt |
| 1:45 – 1:55 | Demo 1.3 | Good vs Bad Prompting Side-by-Side |
| 1:55 – 2:10 | Modul 1.4 | Git Integration & Worktrees |
| 2:10 – 2:20 | Demo 1.4 | Branch → Feature → Commit → PR Flow |
| 2:20 – 2:35 | Modul 1.5 (NEU) | Cost Engineering & Effort Management — `/cost`, `/usage`, `/insights`, Effort-Level als Kosten-Hebel |
| 2:35 – 2:50 | Exercises 1.3 / 1.4 (pick 1) | Hands-on |
| 2:50 – 3:00 | Q&A + Ausblick Session 2 | |

## Session 2 — Ecosystem (~3h)

**Mission:** Wie erweitert man Claude Code? Skills, Hooks, Plugins, MCP, RAG.

**Wichtig:** Exercises 2.1-2.5 nicht alle als Pflicht — "pick 2-3" reicht, sonst Zeitdruck.

| Zeit | Komponente | Inhalt |
|---|---|---|
| 0:00 – 0:10 | Recap Session 1 + Intro Block 2 | PPT Slides 12-18 als visueller Einstieg |
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
| 0:00 – 0:10 | Recap Session 2 + Intro Block 3 | PPT Slides 19-29 als visueller Einstieg |
| 0:10 – 0:25 | Modul 3.1 | Agents & Multi-Agent + Background-Sessions |
| 0:25 – 0:40 | Demo 3.1 | 2 parallele Agents |
| 0:40 – 0:50 | Modul 3.2 + Demo 3.2 | Multi-Model Pipelines / Codex Swarm |
| 0:50 – 1:10 | Modul 3.3 + Demo 3.3 | Security & Adversarial Testing |
| 1:10 – 1:20 | **Pause** | |
| 1:20 – 1:35 | Modul 3.4 + Demo 3.4 | Scheduled Tasks, Loops, /goal |
| 1:35 – 1:50 | Modul 3.6 + Demo 3.6 (NEU) | CI/CD & Headless Mode |
| 1:50 – 2:05 | Modul 3.7 + Demo 3.7 (NEU) | Troubleshooting & Debugging |
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

## Estimated Cost to Replicate

If you replicate the workshop entirely (all demos + all required exercises) on your own
Claude Code account, expect these costs per block:

| Block | Activities | Estimated Cost |
|---|---|---:|
| Block 1 — Foundations | Demos 1.1-1.5 + 4 Exercises | $1-3 |
| Block 2 — Ecosystem | Demos 2.1-2.5 + 2.2b + 3 Exercises | $5-15 |
| Block 3 — Advanced | Demos 3.1-3.7 + Capstone Exercise + Self-Improve Loop | $15-50 |
| **Workshop total** | | **$20-70** |

**Drivers of the high end:**
- Running `/agentic-os:run-loop` for multiple iterations in Demo 3.4 (Self-Improve)
- Codex Swarm parallel agents in Demo 3.2
- Multi-agent orchestration in Demo 3.1 + Capstone Exercise

**To stay on the low end:**
- Use `claude --bare -p` for batch demos (skip overhead)
- Set `--max-budget-usd 0.50` and `--max-turns 5` for autonomous loops
- Use Haiku for Demo 1.5 baseline runs

**For workshop moderators:** Bring a Pro/Max account with at least $50 of budget for safe live execution.

**For self-learners:** Pro plan ($20/month) is enough for non-multi-agent demos.
A pay-as-you-go API key is recommended for Self-Improve Loop and Codex Swarm experimentation.

---

*Letzter Stand: 2026-05-21*
