# CLAUDE.md — Dynamic Workshop

## Mission

Einen praxisnahen, demo-lastigen Workshop in 4 aufeinander aufbauenden Sessions entwickeln, der erfahrenen Entwicklern aus dem Bereich Physical Security einen vollumfaenglichen Eindruck von Claude Code vermittelt — von den Grundlagen bis hin zu autonomen Multi-Agent-Systemen.

**Ziel:** Die Teilnehmer sollen nach dem Workshop Claude Code eigenstaendig und produktiv in ihrem Arbeitsalltag einsetzen koennen.

## Workshop-Format

- **4 Sessions à ~3h** (Welle-F-Restrukturierung: 17 Module → 65 Lerneinheiten), jeweils Teaching + Live Demos + optionale Exercises
- **Session 1 — Foundations:** CLI, Context, Prompting, Git, Cost-Basics (Termin: 10. April 2026)
- **Session 2 — Ecosystem:** Skills, Hooks, Plugins, MCP, RAG
- **Session 3 — Advanced Kern:** Agents, adversariale Security, Hardening/Compliance, Automation
- **Session 4 — Advanced Bonus:** Multi-Model, CI/CD & Headless, Capstone-Architektur, Troubleshooting
- Zielgruppe: 3 erfahrene Entwickler aus Physical Security (Zutrittskontrolle, Alarmsysteme)
- Durchgaengige Security-Analogien als didaktisches Mittel
- **Einstieg immer visuell:** Sessions mit PowerPoint-Praesentation (claude-code-workshop.pptx) starten, dann in Text-Module vertiefen. Teilnehmer wollen sich zuerst ein Bild machen, nicht gleich mit Text ueberflutet werden.

## Regeln

- Bei jeder Inhaltsaenderung an Modulen/Demos/Exercises auch `agents/workshop-mentor.md` aktualisieren
- Demos > Slides — lieber zeigen als erklaeren
- Exercises sind optional/Bonus, keine Pflicht-Hausaufgaben
- Sprache: Deutsch fuer Kommunikation, Englisch fuer Code und Dateinamen

## Struktur

- `resources/modules/` — Teaching Content (3 Bloecke)
- `resources/demos/` — Demo-Scripts mit Recovery-Notes
- `resources/exercises/` — Hands-on Uebungen
- `resources/cheatsheet.md` — Referenz-Karte fuer Teilnehmer
- `resources/prerequisites.md` — Setup-Anleitung
- `resources/session-plan.md` — Zeitplan alle 4 Sessions + 65-LE-Landkarte
- `workshop-playground/` — Demo-Repo mit 3 geplanteten Vulnerabilities
- `agents/workshop-mentor.md` — Mentor-Agent fuer guide/learn Modi

## Deep Research Integration (2026-04-05)

- 2 Deep Research Reports integriert (50+ offizielle Commands, 15 Use Case Blueprints, vollstaendige Tool/Permission/MCP-Referenz)
- Cheatsheet ist jetzt die umfassendste Referenz (50+ Commands, 7 neue Sektionen)
- Alle Module enthalten jetzt: Bundled Skills, 6 Permission Modes, Hook-Typen (command/http/prompt/agent), Plugin Scopes, MCP Transports/OAuth/Limits, Agent Teams, OS-Sandboxing, Data Retention, CVE-Beispiele
- 3 neue Demos: Secure Diff Gate (2.2b), Permission Modes (3.3b), CVE-Fix Pipeline (3.3c)
- 2 neue Exercises: Token Firewall (2.6), HIPAA Guardrails (3.3)
- 10 Use-Case-Blueprints als Inspiration fuer Architecture Discussion (Exercise 3.5)
