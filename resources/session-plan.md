# Workshop Session Plan

> Zeitlicher Ablauf und didaktischer Aufbau über **4 Sessions** (Welle-F-Restrukturierung).
> Die 17 Module sind in **48 kleine Lerneinheiten (LE)** zerlegt — jede 10–25 Min, mit 1–3 klaren
> Lernzielen und einer natürlichen „ich kann jetzt X"-Grenze.
> Stand: 2026-06-23. Vorgänger-Fassung (3 Sessions, Modul-Ebene) siehe Git-Historie.

## Drei-Schicht-Modell (gilt für jede LE)

| Level | Bedeutung | Im Live-Workshop |
|---|---|---|
| `[core]` | Pflichtpfad. Was jeder Teilnehmer können muss. | Immer gefahren. Der Core-Pfad einer Session zielt auf ≤150 Min. |
| `[deep-dive]` | Optionale Vertiefung **desselben** Themas. | **„Wenn Zeit, dann zeigen"** — eingeplant, wird gefahren solange das Zeitbudget reicht; sonst Lesestoff/Cheatsheet. |
| `[bonus]` | Kür/Showcase, oft `🔧`-Custom-Komponenten & experimentelle Features. | Nur bei Zeitüberschuss oder auf Nachfrage. |

> **deep-dive-Default dieses Workshops: „wenn Zeit, dann zeigen".** Der Trainer streicht deep-dives
> erst, wenn der Core-Pfad sonst nicht in den Termin passt — nicht standardmäßig.

## Format-Übersicht

| Session | Thema | Level-Fokus | Core-Dauer | Termin |
|---|---|---|---|---|
| 1 | Erste Schritte mit dem Agenten (sanfter Einstieg) | Foundations | ~160 Min Core | 10. April 2026 (Erstfassung durchgeführt) |
| 2 | Das Ecosystem (Skills, Hooks, Plugins, MCP, RAG) | Ecosystem | ~145 Min Core | TBD |
| 3 | Advanced Kern (Agents, Security, Automation) | Advanced-Kern | ~148 Min Core | TBD |
| 4 | Advanced Bonus (Multi-Model, CI/CD, Capstone, Troubleshooting) | Advanced-Bonus | ~163 Min | TBD |

> **Warum 4 Sessions?** Block 3 hatte faktisch ~270 Min Inhalt in einem 180-Min-Termin. Der ehrliche
> Schnitt trennt den Pflicht-Kern (Session 3: Agents + Security + Automation) vom Überlauf
> (Session 4: Multi-Model + CI/CD + Capstone + Troubleshooting) in zwei vollwertige Termine.

---

## Session 1 — Erste Schritte mit dem Agenten (~3h)

> **Mission:** „Was ist Claude Code, wie steuere ich es, wie arbeite ich sicher mit Git — und behalte die Kosten im Blick."
> Sanfter Einstieg: In den ersten ~36 Min hat ein Neuling **gebaut**, bevor er über Clearance-Level nachdenkt.

| LE | Titel | Level | Min | aus (alt) |
|---|---|---|---:|---|
| S1.1 | Coding Agent vs. Chat — das mentale Modell | core | 12 | 1.1 Overview + Consultant-Analogie |
| S1.2 | First Contact: bau sofort eine Datei | core | 12 | 1.1 Hello/„What CC can do" + Demo 1.1 |
| S1.3 | Die Oberflächen: CLI, Desktop, IDE, Web, iOS | core | 12 | 1.1 Five Surfaces + Surface-Switching |
| S1.4 | Built-in Tools & die Tool-Namen | core | 12 | 1.1 Built-in Tools Reference |
| S1.5 | Permissions Grundlagen: default & acceptEdits | core | 15 | 1.1 Permission System (Alltags-Modi) |
| **S1.6** | **Permission Modes komplett (6 Modi + Cloud)** | **core** ⭐ | 15 | 1.1 Permission System (auto/dontAsk/bypass) |
| S1.7 | Modellwahl & Effort-Level | core | 15 | 1.1 Model Selection + 1.3 Effort-Hebel |
| S1.8 | Kontextfenster verstehen | core | 15 | 1.2 Context Window + Control-Room-Analogie |
| S1.9 | `/compact`, `/rewind` & Kontext steuern | core | 12 | 1.2 How-to-handle-it + Key Context Commands + Demo 1.2 |
| S1.10 | CLAUDE.md: die Projekt-Standing-Orders | core | 15 | 1.2 CLAUDE.md + Analogien + Demo 1.2 |
| S1.11 | Memory-Layer komplett (Auto-Memory, rules/, local, managed) | deep-dive | 18 | 1.2 Auto-Memory + rules/ + local + Managed |
| S1.12 | `@path`-Imports, `--add-dir`, AGENTS.md-Interop | deep-dive | 12 | 1.2 @path Imports + Multi-Project --add-dir |
| S1.13 | Vager vs. präziser Prompt (Contractor-Analogie) | core | 15 | 1.3 Clarity + Contractor + Scope + Demo 1.3 |
| S1.14 | Plan Mode & Explain/Propose/Refine/Execute | core | 15 | 1.3 Iterative Pattern + Plan Mode + Patterns |
| S1.15 | Output Styles & Personas (system-prompt) | deep-dive | 12 | 1.3 Output Styles + /voice + Persona-Switching |
| S1.16 | Git in einem Flow: branch → commit → PR | core | 18 | 1.4 Built-in Git + Full PR Workflow + Demo 1.4 |
| S1.17 | Git-Slash-Commands: /diff /review /rewind /autofix-pr | deep-dive | 15 | 1.4 Git-Related Slash Commands + --from-pr |
| S1.18 | Worktrees als Test-Labor | deep-dive | 15 | 1.4 Git Worktrees + --worktree + baseRef |
| S1.19 | Kosten im Blick: /cost, /usage & Budget-Cap | core | 15 | 1.5 Token Tracking (core) + Budget Caps |
| S1.20 | Demo + Hands-on Puffer (Exercise 1.x — pick 1) | core | 15 | Exercises 1.1–1.4 |

**Session 1 Core:** S1.1–S1.10, S1.13, S1.14, S1.16, S1.19, S1.20 → **~160 Min** (fullster Termin).
**deep-dive (wenn Zeit):** S1.11 (18) + S1.12 (12) + S1.15 (12) + S1.17 (15) + S1.18 (15) = **72 Min**.

> **⭐ Audience-Fit-Entscheidung:** S1.6 (alle 6 Permission Modes) ist **`[core]`**, nicht deep-dive —
> die Zielgruppe (Physical-Security-Profis) will Clearance-Level früh vollständig sehen. Dadurch ist
> Session 1 der vollste Termin (~160 Min Core). Wenn es eng wird: S1.20-Puffer auf 12 Min kürzen
> ODER eine der weichen Core-LEs (S1.9) straffen — die 6 Modi NICHT opfern.

---

## Session 2 — Das Ecosystem (~3h)

> **Mission:** „Wie erweitert und kontrolliert man Claude Code." Skills, Hooks, Plugins, MCP, RAG.

| LE | Titel | Level | Min | aus (alt) |
|---|---|---|---:|---|
| S2.1 | Skills = SOPs, Commands = Buttons | core | 12 | 2.1 Core Idea + SOPs-Analogie |
| S2.2 | Eine SKILL.md schreiben (Frontmatter-Basics) | core | 18 | 2.1 Anatomy + Frontmatter Fields + Demo 2.1 |
| S2.3 | Skills vs Commands & disable-model-invocation | core | 12 | 2.1 Skills vs Commands |
| S2.4 | Bundled Skills (/batch /debug /loop /verify …) | core | 12 | 2.1 Bundled Skills + /skills |
| S2.5 | Living Prompts: dynamische Injection & Argumente | deep-dive | 15 | 2.1 Argument Substitution + Dynamic Injection + Live-Reload |
| S2.6 | Hooks = Event-Listener (die 3 Eckpfeiler) | core | 15 | 2.2 Core Idea + Three Cornerstones + Sensor-Analogie |
| S2.7 | Die wichtigsten Hook-Events landkarten | core | 12 | 2.2 Hook Types (11er-Tabelle) |
| S2.8 | Einen Hook konfigurieren (settings.json, matcher, if) | core | 15 | 2.2 Hook Configuration + Real Example + Demo 2.2 |
| S2.9 | Hook-Exec-Typen & component-scoped Hooks | deep-dive | 15 | 2.2 Execution Types + Component-Scoped Hooks |
| S2.10 | Advanced Hook-Outputs + Secure Diff Gate | deep-dive | 15 | 2.2 Advanced Output + Circuit Breaker + Demo 2.2b |
| S2.11 | Plugins: ein Bundle schnüren | core | 15 | 2.3 Core Idea + Plugin Structure + Demo 2.3 |
| S2.12 | Plugin-Lifecycle, Scopes & Marketplaces | deep-dive | 15 | 2.3 Marketplaces + Scopes + CLI + Pinning |
| S2.13 | Plugin-Supply-Chain-Risiken | deep-dive | 10 | 2.3 Supply Chain Risks + Notable Plugins |
| S2.14 | MCP: der Integrations-Stecker | core | 15 | 2.4 Core Idea + Building-Management-Analogie + Demo 2.4 |
| S2.15 | MCP konfigurieren: Transports, Scopes, CLI | core | 15 | 2.4 Transport Types + Scopes + CLI + File-Config |
| S2.16 | MCP OAuth, Output-Limits & Protokoll-Details | deep-dive | 15 | 2.4 OAuth + Output Limits + Protocol Details |
| S2.17 | MCP-Security & eigenen Server bauen | deep-dive | 18 | 2.4 MCP Security + Build Your Own + Channels |
| S2.18 | RAG & NotebookLM: dem Agenten Blueprints geben | core | 18 | 2.5 Workflow + Use Cases + Demo 2.5 |
| S2.19 | RAG-Grenzen & Datenschutz-Abwägung | deep-dive | 10 | 2.5 RAG Limitations + Data-Flow-Disclosure |
| S2.20 | Hands-on Puffer (Exercise 2.x — pick 2–3) | core | 18 | Exercises 2.1–2.6 |

**Session 2 Core:** S2.1–S2.4, S2.6–S2.8, S2.11, S2.14, S2.15, S2.18, S2.20 → **~145 Min**.
**deep-dive (wenn Zeit):** S2.5 (15) + S2.9 (15) + S2.10 (15) + S2.12 (15) + S2.13 (10) + S2.16 (15) + S2.17 (18) + S2.19 (10) = **113 Min**.

---

## Session 3 — Advanced Kern (~3h)

> **Mission:** „Spezialisierte Agenten, automatisierte Security-Prüfung, sichere Automation." Der Pflicht-Kern von Block 3.

| LE | Titel | Level | Min | aus (alt) |
|---|---|---|---:|---|
| S3.1 | Was ist ein Agent? (Spezialisierung) | core | 12 | 3.1 What Is an Agent + Why Specialization + SOC-Analogie |
| S3.2 | Built-in Subagents nutzen (Explore/Plan/general) | core | 10 | 3.1 Built-in Subagents |
| S3.3 | Einen Custom Subagent definieren | core | 18 | 3.1 Definition Anatomy + Full Frontmatter + Demo 3.1 |
| S3.4 | Orchestrierungs-Muster (Fan-Out/Pipeline/Hierarchie) | core | 15 | 3.1 Orchestration Patterns + Quick-Start + Demo 3.1 |
| S3.5 | Background-Sessions & Agent Teams | deep-dive | 15 | 3.1 Agent Teams + Background Agents + /tasks |
| S3.6 | Devil's Advocate: adversariale Security-Pipeline | core | 18 | 3.3a Devil's-Advocate-Pipeline (4 Stages) + Demo 3.3 |
| S3.7 | Built-in Review-Trio (/security-review, /review, /ultrareview) | core | 12 | 3.3a Security-Audit-Skill + Code-Review-Trio |
| S3.8 | Permissions für Autonomie (advanced modes) | core | 15 | 3.3b Permission Modes Going Deeper + Beyond Allow/Deny |
| S3.9 | Protected Paths & Sandboxing-Stufen | core | 15 | 3.3b Protected Paths + Sandboxing Options + Trust Boundaries |
| S3.10 | Netzwerk-/Skill-Hardening | deep-dive | 12 | 3.3b Sandbox Network Hardening + disableSkillShellExecution |
| S3.11 | Datenschutz, Retention & regulierte Branchen | deep-dive | 15 | 3.3b Data Retention + Regulated Industries + Known CVEs |
| S3.12 | Scheduling: /loop, /goal, /schedule, Routines | core | 15 | 3.4 /schedule + /loop + /goal + Routines + Demo 3.4 |
| S3.13 | Autonome Loops absichern (Budget + Worktree) | core | 12 | 3.4 --max-budget-usd + Worktree-Scoped + Channels |
| S3.14 | Self-Improve Loop (Showcase + Grenzen) | bonus | 15 | 3.4 Self-Improve Loops (inkl. Branchen-Realität) |
| S3.15 | Hands-on Puffer (Exercise 3.x — pick 1) | core | 15 | Exercises 3.1–3.3 |

**Session 3 Core:** S3.1–S3.4, S3.6–S3.9, S3.12, S3.13, S3.15 → **~148 Min**.
**deep-dive/bonus (wenn Zeit):** S3.5 (15) + S3.10 (12) + S3.11 (15) + S3.14 (15) = **57 Min**.

> **⚓ Live-Anker beibehalten:** Session 3 öffnet nach dem Recap mit **Demo 3.6 Step 1** (`claude -p …`)
> als garantiert-lokalem 60-Sek-Live-Moment, bevor die schwereren Demos kommen (nur lokales `claude`
> nötig — siehe Anker-Notiz in `demos/block-3-demos.md`).

---

## Session 4 — Advanced Bonus (~3h)

> **Mission:** „Multi-Model, CI/CD, die volle Architektur — und souverän debuggen." Der Überlauf aus Block 3,
> jetzt ein vollwertiger Termin. Hier wird auch das **verschobene Cost-Engineering** (Pipeline/Caching/Insights)
> bei den Budget-Caps der CI praktisch wieder aufgegriffen.

| LE | Titel | Level | Min | aus (alt) |
|---|---|---|---:|---|
| S4.1 | Multi-Model: das richtige Modell pro Phase | deep-dive | 15 | 3.2 Different Models + Cost Trade-Off + Claude→Codex→Claude |
| S4.2 | Codex Swarm & Daten-Fluss-Grenze | bonus | 15 | 3.2 Data Flow + Codex Swarm + Demo 3.2 |
| S4.3 | Headless Mode: `claude -p` als Pipeline-Stufe | deep-dive | 15 | 3.6 Headless Mode + Structured Output + Demo 3.6 |
| **S4.4** | **CI-Auth, Cost-Caps & Cost-Engineering-Vertiefung** | deep-dive | 18 | 3.6 CI Auth + Cost Caps + --bare **+ verschobenes 1.5** (Pipeline/Caching/Insights/Taktiken/Anti-Patterns) |
| S4.5 | CI-Pipelines bauen (GitHub Actions / GitLab) | deep-dive | 18 | 3.6 GitHub Actions + GitLab CI + Failure Patterns + Don'ts |
| S4.6 | Mobile/Remote: remote-control & /teleport | bonus | 12 | 3.5 Built-in Mobile Workflow + Telegram Bridge |
| S4.7 | Inception (Docker) & Worktree-Isolation tief | bonus | 15 | 3.5 Inception + Worktree Isolation + baseRef + --tmux |
| S4.8 | Die volle Architektur (Capstone-Diskussion) | bonus | 25 | 3.5 Full Architecture + Complete Analogy + Exercise 3.5 |
| S4.9 | Troubleshooting: /debug, --verbose, /doctor | core* | 15 | 3.7 /debug + --verbose + /doctor |
| S4.10 | Diagnose-Sequenzen (Hook/Skill/Plugin/MCP) | core* | 18 | 3.7 Failure-Diagnosen + 8-Schritt-Checkliste + Demo 3.7 |

**Session 4 (voller Track):** 15+15+15+18+18+12+15+25+15+18 = **~163 Min** (passt in 180 Min mit Pause).

> **`core*` = innerhalb von Session 4 Pflicht.** Troubleshooting (S4.9/S4.10) ist der einzige „jeder braucht
> es"-Teil. **Fallback ohne 4. Termin:** S4.9 + S4.10 (33 Min) ans Ende von Session 3 hängen und die
> Session-3-deep-dives streichen; der Rest von Session 4 wird strukturierter Selbststudien-Track.

> **💸 Cost-Engineering-Verschiebung (Welle-F-Entscheidung):** Vom alten Modul 1.5 bleibt nur S1.19
> (`/cost`, `/usage`, Budget-Cap) als Tag-1-Core. Der Rest — Pipeline-Ökonomie, Prompt-Caching,
> `/insights`-Deep-Dive, Cost-Reduktions-Taktiken, Anti-Patterns — wird in **S4.4 bei den CI-Budget-Caps**
> praktisch wieder aufgegriffen, wo er Hand und Fuß hat. Begründung: Ein Neuling kann am Tag 1 ohne
> Praxisgefühl die Pipeline-Ökonomie nicht einordnen; Budget-Caps werden erst bei autonomen Loops/CI relevant.

---

## Exercise-Mapping (LE ↔ Übung)

| Übungen | Hängen an LE |
|---|---|
| Exercises 1.1–1.4 | S1.20 (Hands-on-Puffer Session 1) |
| Exercises 2.1–2.6 | S2.20 (Hands-on-Puffer Session 2) |
| Exercises 3.1–3.3 | S3.15 (Hands-on-Puffer Session 3) |
| Exercise 3.5 (Capstone / Architecture Discussion) | S4.8 (Die volle Architektur) |

---

## Demo-Zeiten & Bonus-Schritte

> **⏱️ Demo-Zeiten realistisch lesen.** Jeder Demo-Slot ist als **Demo + Talking-Points + 2–3 Min Puffer**
> gedacht — Live-Demos laufen IMMER langsamer als das Skript. Faustregel: Die im Demo-Skript genannte
> Dauer (z.B. „~8 minutes") meint den reinen Ablauf OHNE Publikum; plane real ~1,5× ein.
>
> **Bonus-Schritte sind optional — nur bei Zeitüberschuss.** Schritte, die in den Demo-/Exercise-Skripten
> als „Bonus" / „Stretch" / „(if time allows)" markiert sind, zählen NICHT zur Slot-Zeit. Wenn der Slot
> knapp wird, zuerst die Bonus-Schritte streichen — der Kern jeder Demo passt in den Slot, die Boni nicht.

---

## Didaktischer Aufbau

Jede LE folgt demselben Muster:
1. **Konzept verstehen** — LE-Abschnitt im Modul lesen (Anker `<!-- LE: Sx.y -->`)
2. **Live-Demo sehen** — die an die LE gebundene Demo nachvollziehen (Demo > Slides)
3. **Selbst ausprobieren** — Exercise im Hands-on-Puffer lösen
4. **Mit Cheat Sheet absichern** — Quick-Reference

Jede Session startet weiterhin **visuell mit der PPT** (`claude-code-workshop.pptx`), dann Vertiefung in die LEs.
Durchgängige Physical-Security-Analogien und optionale Exercises bleiben erhalten.

## Pausen

Pro Session ~10–15 Min Pause nach ~90 Min. Zusätzlich Q&A zwischen LEs.

## Pflicht vs Optional (auf LE-Ebene)

- **Pflicht je Session:** alle `[core]`-LEs + Hauptdemos + mindestens 1 Exercise (Hands-on-Puffer).
- **„Wenn Zeit, dann zeigen":** `[deep-dive]`-LEs.
- **Nur bei Überschuss / auf Nachfrage:** `[bonus]`-LEs (Self-Improve, Codex Swarm, Capstone, Mobile/Inception).

## Materialien pro Session

| Session | Mitbringen | Vorbereitung |
|---|---|---|
| 1 | Laptop, claude installiert, GitHub-Account | `resources/prerequisites.md` durchgearbeitet |
| 2 | Session-1-Setup + Playwright-Browser, NotebookLM-Account | Plugin-Bundle installiert (siehe `prerequisites.md` „Workshop-Plugins") |
| 3 | Session-2-Setup + Codex-CLI (falls verfügbar) | Workshop-Playground geklont |
| 4 | Session-3-Setup | optional: CI-Repo mit GitHub Actions zum Mitschreiben |
| **Alle** | **Moderator:** vorbereitetes `~/cc-workshop`-Bundle auf USB-Stick | Fallback bei kaputtem Teilnehmer-Setup (vgl. `trainer-notes.md` Pairing-Fallback) |

---

## Estimated Cost to Replicate

If you replicate the workshop entirely (all demos + all required exercises) on your own
Claude Code account, expect these costs per session:

| Session | Activities | Estimated Cost |
|---|---|---:|
| Session 1 — Foundations | Demos 1.1–1.4 + 1 Exercise + `/cost`-Basics | $1–3 |
| Session 2 — Ecosystem | Demos 2.1–2.5 + 2.2b + 2–3 Exercises | $5–15 |
| Session 3 — Advanced Kern | Demos 3.1, 3.3, 3.4 + 1 Exercise + Self-Improve Loop (bonus) | $10–35 |
| Session 4 — Advanced Bonus | Demos 3.2, 3.6, 3.7 + Capstone + CI/Cost-Engineering | $8–25 |
| **Workshop total** | | **$24–78** |

**Drivers of the high end:**
- Running `/agentic-os:run-loop` for multiple iterations in the Self-Improve Loop (S3.14, bonus)
- Codex Swarm parallel agents (S4.2, bonus)
- Multi-agent orchestration in S3.1–S3.4 + Capstone (S4.8)

**To stay on the low end:**
- Use `claude --bare -p` for batch demos (skip overhead)
- Set `--max-budget-usd 0.50` for autonomous loops (current CLI has no hard turn-cap flag anymore — `--max-budget-usd` bounds runaway loops/cost)
- Use Haiku for cost-baseline runs

**For workshop moderators:** Bring a Pro/Max account with at least $50 of budget for safe live execution.

**For self-learners:** Pro plan ($20/month) is enough for non-multi-agent LEs.
A pay-as-you-go API key is recommended for the Self-Improve Loop and Codex Swarm experimentation.

---

*Letzter Stand: 2026-06-23 — Welle F (Restrukturierung), 4 Sessions / 48 Lerneinheiten.*
