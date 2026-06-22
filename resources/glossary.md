# Glossar — Claude Code Workshop

> Zentrale Begriffsdefinitionen fuer den Dynamic Workshop. Sortiert alphabetisch.
> Begriffsnamen bleiben Englisch (Code-Identifier). Definitionen auf Deutsch.
> Stand: 2026-05-20.

---

## A

### Agent (Built-in Tool)
Eingebautes Tool, das eine neue Subagent-Instanz spawned. Wurde in v2.1.63 von `Task` zu `Agent` umbenannt. Ueber das `Agent`-Tool startet Claude einen Subagent mit isoliertem Kontext und definierten Tool-Permissions.
- **Verwandt:** Sub-Agent, TaskCreate, Built-in Tools
- **Modul:** 3.1 — Agents & Multi-Agent

### AGENTS.md
Convention aus dem OpenAI-/Codex-Oekosystem fuer Cross-Tool-Interop. Ein Markdown-File im Repo-Root mit Anweisungen fuer Coding-Agenten. Claude Code laedt es nicht automatisch, aber via `@AGENTS.md`-Import in `CLAUDE.md` ist Interop moeglich.
- **Verwandt:** CLAUDE.md, `@path` Import
- **Modul:** 1.2 — Context & Memory

### AskUserQuestion (Built-in Tool)
Eingebautes Tool fuer Multiple-Choice-Rueckfragen. Macht interaktive Skills und Agents moeglich, die nicht nur freitext-Antworten verarbeiten, sondern strukturierte User-Auswahl anfordern.
- **Verwandt:** Built-in Tools, Skill, Sub-Agent
- **Modul:** 2.1 — Skills & Commands

### Auto-Memory
Default-on Mechanik seit v2.1.59. Claude legt automatisch Memory-Notes in `~/.claude/projects/<hash>/memory/` an, wenn Themen wiederholt auftauchen oder fuer Bootstrap-Logik. Frueher: User musste "say remember" sagen. Heute: passiert automatisch, Index lebt in `MEMORY.md`.
- **Verwandt:** Memory System, CLAUDE.md, Path-Scoped Rule
- **Modul:** 1.2 — Context & Memory

### Auto-Mode → siehe Permission Mode

---

## B

### Background Agent
Subagent, der detached in einer eigenen Session laeuft. Wird via `claude --bg` oder `/background` gestartet, wird ueber `claude agents` (Live-View), `claude attach <id>`, `claude logs <id>`, `claude stop <id>` verwaltet. Seit v2.1.139.
- **Verwandt:** Sub-Agent, Routine, Channel
- **Modul:** 3.1 — Agents & Multi-Agent

### Built-in Tools
Hardcoded Tools, die Claude Code immer kennt. Die Namen sind die Strings fuer Permission Rules, Hook Matcher und Subagent Tool-Listen.
- **Liste:** `Read`, `Write`, `Edit`, `Bash`, `PowerShell`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `Skill`, `Agent`, `Monitor`, `AskUserQuestion`, `TaskCreate`/`TaskList`/`TaskUpdate`/`TaskGet`/`TaskOutput`/`TaskStop`, `EnterPlanMode`/`ExitPlanMode`, `EnterWorktree`/`ExitWorktree`, `NotebookEdit`, `LSP`, `PushNotification`, `ShareOnboardingGuide`, `TeamCreate`/`SendMessage`, `CronCreate`/`CronList`.
- **Verwandt:** Permission Rule, Skill, Agent
- **Modul:** 1.1 — What is Claude Code?

### Bundled Skills
Prompt-basierte Playbooks, die in jeder Session verfuegbar sind (anders als Built-in Commands, die fixe Logik ausfuehren). Aktuell: `/batch`, `/loop`, `/run`, `/verify`, `/debug`, `/simplify`, `/claude-api`, `/fewer-permission-prompts`, `/run-skill-generator`.
- **Verwandt:** Skill, Slash Command
- **Modul:** 2.1 — Skills & Commands; Cheatsheet

---

## C

### Channels
MCP-Push-Mechanismus (Research-Preview) fuer asynchrone Nachrichten an Claude-Code-Sessions. Ersatz fuer Custom-Pattern wie die Workshop-Telegram-Bridge.
- **Verwandt:** MCP, Telegram Bridge, Routine
- **Modul:** 3.4 / 3.5

### CLAUDE.md (Project-level)
Markdown-File im Repo-Root mit projekt-spezifischen Anweisungen. Wird beim Session-Start automatisch geladen. Eingecheckt ins Git-Repo — geteilt mit dem Team.
- **Verwandt:** CLAUDE.local.md, AGENTS.md, Path-Scoped Rule
- **Modul:** 1.2 — Context & Memory

### CLAUDE.md (User-level)
`~/.claude/CLAUDE.md` — globale User-Instruktionen, gelten in allen Projekten. Behavior-Shaping der eigenen Session, nicht teamweit.
- **Verwandt:** CLAUDE.md (Project), Memory System
- **Modul:** 1.2 — Context & Memory

### CLAUDE.local.md
Markdown-File im Repo-Root fuer persoenliche Project-Notes, die NICHT eingecheckt werden. Gehoert in `.gitignore`. Ergaenzt `CLAUDE.md` um lokale Praeferenzen.
- **Verwandt:** CLAUDE.md (Project), CLAUDE.md (User)
- **Modul:** 1.2 — Context & Memory

### Command
Slash-Command, der eine bestimmte Action triggert. Seit v2.x technisch mit Skills gemerged: Ein Skill ohne `disable-model-invocation` wirkt als auto-getriggerter Skill, ein Skill mit `disable-model-invocation: true` wirkt als reines Slash-Command (nur manuell).
- **Verwandt:** Slash Command, Skill, Trigger Phrase
- **Modul:** 2.1 — Skills & Commands

### Context Window
Die maximale Token-Menge, die Claude in einer Session "im Kopf" behalten kann. Opus 4.7 und Sonnet 4.6: 1M Token (Sonnet beta), Haiku 4.5: 200K. `/context` zeigt aktuelle Nutzung, `/compact` komprimiert.
- **Verwandt:** Token, Model
- **Modul:** 1.2 — Context & Memory

### Cost-Cap
Maximaler USD-Betrag fuer einen `claude -p`-Run. CLI-Flag `--max-budget-usd <amount>`. Schutz vor Endlos-Loops in CI/Automatisierung. Kombiniert sich gut mit `--max-turns`.
- **Verwandt:** Headless Mode, Routine
- **Modul:** 3.6 (geplant) — CI/CD

### Custom Skill
User- oder Projekt-Skill, NICHT aus Plugin oder Bundled Skills. Liegt unter `~/.claude/skills/<name>/SKILL.md` (User) oder `.claude/skills/<name>/SKILL.md` (Projekt).
- **Verwandt:** Skill, Plugin, Bundled Skills
- **Modul:** 2.1 — Skills & Commands

---

## D

### Dynamic Context Injection
Skill-Feature, das via `` !`command` `` Syntax die Ausgabe eines Shell-Commands direkt in den Skill-Prompt einbettet. Macht Skills aus statischem Markdown zu aktiven Tools, die Live-Daten lesen koennen.
- **Verwandt:** Skill, Skill Frontmatter, `disableSkillShellExecution`
- **Modul:** 2.1 — Skills & Commands

---

## E

### Effort Level
Steuert die Tiefe von Claudes Reasoning. Werte: `low` / `medium` / `high` / `xhigh` / `max`. `xhigh` und `max` sind nur auf Opus 4.7 verfuegbar. CLI: `/effort xhigh` in Session. Trade-off: Tiefe vs. Latenz und Cost.
- **Verwandt:** Model, Cost-Cap
- **Modul:** 1.3 — Effective Prompting

---

## H

### Hook
Automatische Action bei einem Lifecycle-Event in Claude Code (vor/nach Tool-Use, Session-Start, etc.). Definiert in `settings.json` oder Skill/Subagent-Frontmatter. Use-Cases: Security-Block, Audit-Log, Format-on-Save, Inject-Context.
- **Verwandt:** Hook Event, Hook Execution Type
- **Modul:** 2.2 — Hooks

### Hook Event
Der Trigger-Zeitpunkt fuer einen Hook. ~28 Events offiziell. Wichtigste: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `SubagentStart`, `SubagentStop`, `FileChanged`, `InstructionsLoaded`, `Notification`.
- **Verwandt:** Hook, Hook Execution Type
- **Modul:** 2.2 — Hooks

### Hook Execution Type
Wie ein Hook seine Action ausfuehrt. Fuenf Varianten: `command` (Shell), `http` (HTTP-Request), `prompt` (Prompt-Eval durch Claude), `agent` (Subagent fuer komplexe Eval), `mcp_tool` (direkter MCP-Tool-Call, v2.1.119+).
- **Verwandt:** Hook, Hook Event, MCP
- **Modul:** 2.2 — Hooks

---

## M

### Marketplace
Plugin-Registry. Zwei offizielle Anthropic-Marketplaces: **claude-plugins-official** (kuratiert) und **claude-community** (Community-Contributions). Hinzufuegen via `claude plugin marketplace add <owner/repo>`.
- **Verwandt:** Plugin, Plugin Scope
- **Modul:** 2.3 — Plugins

### MCP (Model Context Protocol)
Offenes Protokoll fuer die Verbindung zwischen LLM-Agents und externen Tools/Datenquellen. Anthropic-spezifiziert, aber tool-agnostisch. Ein MCP-Server stellt Tools, Ressourcen und Prompts bereit; Claude Code konsumiert sie als Built-in-Tools mit Namespace.
- **Verwandt:** MCP Server, Scope (MCP)
- **Modul:** 2.4 — MCP

### MCP Server
Ein Prozess, der das MCP-Protokoll implementiert und Tools/Resources bereitstellt. Drei Transports: **HTTP** (remote, empfohlen), **stdio** (lokaler Prozess), **SSE** (deprecated).
- **Verwandt:** MCP, Scope (MCP)
- **Modul:** 2.4 — MCP

### Memory System
Claudes persistenter Speicher zwischen Sessions. Drei Ebenen: (1) `CLAUDE.md` (manuell gepflegt), (2) `MEMORY.md` + Topic-Files (auto-erzeugt via Auto-Memory), (3) Session-State im SQLite-Backend.
- **Verwandt:** Auto-Memory, CLAUDE.md, Path-Scoped Rule
- **Modul:** 1.2 — Context & Memory

### Model
Das LLM hinter Claude Code. Aktuelle Modelle: **Opus 4.7** (Default seit 2026-04-16, 1M Context, fuer Architektur und Reasoning), **Sonnet 4.6** (1M Context beta, fuer Standard-Coding), **Haiku 4.5** (200K Context, fuer Bulk-Reads). Wechsel via `/model` oder `--model`.
- **Verwandt:** Context Window, Effort Level
- **Modul:** 1.1 — What is Claude Code?

### Monitor (Built-in Tool)
Built-in-Tool fuer Background-Watching (Logs/PRs/Files). Reagiert im laufenden Session-Kontext, wenn etwas passiert. Wichtig fuer reaktive Multi-Agent-Patterns.
- **Verwandt:** Built-in Tools, Background Agent, Hook
- **Modul:** 3.1 — Agents & Multi-Agent

---

## P

### Path-Scoped Rule
Markdown-Files in `.claude/rules/` mit `paths:`-Filter im Frontmatter. Werden nur geladen, wenn matching Files im Kontext sind. Skalierungs-Antwort fuer grosse Codebases, wo `CLAUDE.md` zu gross wuerde.
- **Verwandt:** CLAUDE.md, Auto-Memory
- **Modul:** 1.2 — Context & Memory

### Permission Mode
Globaler Sicherheits-Level fuer eine Session. Sechs Modi:
- `default` — fragt bei allem nach (ausser Reads)
- `acceptEdits` — Edits + sichere FS-Bash-Commands auto-akzeptiert
- `plan` — zeigt Gesamtplan vorab, einmal genehmigen
- `auto` — ML-Klassifizierer entscheidet (Max-Plan oder Team/Enterprise)
- `dontAsk` — niemals fragen, nur allow/deny-Rules zaehlen
- `bypassPermissions` — YOLO, akzeptiert alles ausser Protected Paths

Setzen via `claude --permission-mode <mode>` oder `/permissions` in Session. Cycle via Shift+Tab.
- **Verwandt:** Permission Rule, Protected Path, Auto-Mode
- **Modul:** 1.1, 3.3 — Security

### Permission Rule
Feingranulare Regel in `settings.json` unter `permissions.allow` / `permissions.deny` / `permissions.ask`. Patterns: `Bash(<cmd> *)`, `Skill(<name>)`, `Agent(<type>)`, `WebFetch(domain:<host>)`, einfache Tool-Namen.
- **Verwandt:** Permission Mode, Built-in Tools
- **Modul:** 3.3 — Security

### Plugin
Versendbare Bundle-Einheit fuer Claude-Code-Erweiterungen. Enthaelt Skills, Agents, Commands, Hooks, MCP-Configs, Output-Styles. Verteilt via Marketplace, Git-Repo, oder lokal via `claude --plugin-dir`.
- **Verwandt:** Plugin Manifest, Plugin Scope, Marketplace
- **Modul:** 2.3 — Plugins

### Plugin Manifest
`.claude-plugin/plugin.json` im Plugin-Root. Enthaelt Name, Version, Description, Dependencies. **Wichtig:** Manifest liegt im Unterordner `.claude-plugin/`, NICHT im Plugin-Root selbst.
- **Verwandt:** Plugin, Plugin Scope
- **Modul:** 2.3 — Plugins

### Plugin Scope
Wo ein Plugin installiert ist. Vier Werte:
- `user` — `~/.claude/plugins/` (individueller Dev)
- `project` — `.claude/plugins/` (Team, eingecheckt)
- `local` — `.claude/settings.local.json` (individuell, nicht geteilt)
- `managed` — Org-managed Settings (Enterprise-Admin)

Installation: `claude plugin install <source> --scope <scope>`.
- **Verwandt:** Plugin, Scope (MCP)
- **Modul:** 2.3 — Plugins

### Protected Path
Hardcoded geschuetzte Pfade, die selbst in `bypassPermissions` NICHT modifiziert werden: `.git/`, `.claude/`, `.mcp.json`, Shell-Configs (`.bashrc`, `.zshrc`, `.profile`). Sicherheitsnetz gegen Self-Sabotage.
- **Verwandt:** Permission Mode, Permission Rule
- **Modul:** 3.3 — Security

### Prompt-Mode
Aktueller Promptbox-Mode in der CLI. Zwei Werte: **Plan Mode** (zeigt Plan vorab, fuehrt nichts aus) und **Default Mode** (normaler Agent-Loop). Wechsel via Shift+Tab. Plan Mode wird oft mit `/plan <task>` aktiviert.
- **Verwandt:** Permission Mode, Slash Command
- **Modul:** 1.3 — Effective Prompting

---

## R

### RAG (Retrieval-Augmented Generation)
Pattern, bei dem ein LLM nicht aus eigenem Memory antwortet, sondern aus einer externen Wissensquelle (Dokumente, Datenbanken). In Claude Code typischerweise via NotebookLM-MCP oder Custom-MCP-Server mit Vector-Store.
- **Verwandt:** MCP, Notebook (NotebookLM)
- **Modul:** 2.5 — RAG & NotebookLM

### Routine
Offizielle Variante von wiederkehrenden Tasks (Ersatz fuer `/schedule` + `/loop`). Definiert in Settings; laeuft cron-aehnlich im Hintergrund. Nutzt Background-Agents fuer die Ausfuehrung.
- **Verwandt:** Background Agent, Channel, Slash Command
- **Modul:** 3.4 — Scheduled Tasks & Loops

---

## S

### Scope (MCP)
Wo eine MCP-Server-Konfiguration gespeichert ist. Drei Werte (umbenannt aus alten Begriffen):
- `local` — `.claude/.mcp.json` (frueher: `project`)
- `project` — `.mcp.json` im Repo-Root (eingecheckt)
- `user` — `~/.claude/.mcp.json` (frueher: `global`)

CLI: `claude mcp add --scope <local|project|user> ...`.
- **Verwandt:** MCP, MCP Server, Plugin Scope
- **Modul:** 2.4 — MCP

### Session
Eine durchgaengige Claude-Code-Conversation mit eigenem Kontext, eigenem SQLite-State, eigener ID. Persistiert nach Beenden, resume via `claude -c` (letzte) oder `claude -r <name>` (named).
- **Verwandt:** Context Window, Memory System
- **Modul:** 1.2, 1.4

### Skill (SOP)
Wiederverwendbare Anweisung, die Claude bei passenden Trigger-Phrases laedt. "Standard Operating Procedure". Lebt als `SKILL.md` (Markdown + YAML-Frontmatter). Drei Ablage-Scopes: Plugin, User, Projekt.
- **Verwandt:** Command, Skill Frontmatter, Trigger Phrase
- **Modul:** 2.1 — Skills & Commands

### Skill Frontmatter
YAML-Header eines `SKILL.md`-Files. Wichtige Felder: `name`, `description`, `when_to_use`, `arguments`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `model`, `effort`, `paths`, `shell`, `hooks`. (`version`, `author`, `tags` sind Workshop-Custom, kein offizielles Schema.)
- **Verwandt:** Skill, Hook
- **Modul:** 2.1 — Skills & Commands

### Skill Live-Reload
Aenderungen an `SKILL.md` werden ohne Session-Restart wirksam. Live-Reload ist Default seit v2.1.x. Falls Skill alte Version laedt: `/reload-plugins` oder neue Session.
- **Verwandt:** Skill, Plugin
- **Modul:** 2.1 — Skills & Commands

### Slash Command
Befehl in der CLI, beginnend mit `/`. Zwei Typen: (1) Built-in Slash Commands (`/help`, `/clear`, `/cost`, ...) mit fixer Logik; (2) Skill-getriggerte Slash Commands (`/tdd`, `/commit`, ...) — Skills mit `disable-model-invocation`.
- **Verwandt:** Command, Skill, Bundled Skills
- **Modul:** 2.1 — Skills & Commands

### Sub-Agent / Subagent
Eine separate Claude-Instanz mit eigenem Kontext, eigenen Tool-Permissions, eigenem Memory-Scope. Gespawned via `Agent`-Tool oder `--agents`-Flag. Use-Case: isolierte Tasks, parallele Arbeit, Spezialisten-Rollen (Reviewer, Implementer, Verifier).
- **Verwandt:** Agent (Built-in Tool), Subagent Frontmatter, Background Agent
- **Modul:** 3.1 — Agents & Multi-Agent

### Subagent Frontmatter
YAML-Header eines `.md`-Files im `agents/`-Ordner. Wichtige Felder: `name`, `description`, `tools` (NICHT mehr `allowed_tools`), `disallowedTools`, `model`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`, `initialPrompt`, `permissionMode`, `maxTurns`.
- **Verwandt:** Sub-Agent, Skill Frontmatter
- **Modul:** 3.1 — Agents & Multi-Agent

### Surface
Eine der Interaktions-Oberflaechen fuer Claude Code. Fuenf Surfaces: CLI, Desktop App, Web App (claude.ai/code), IDE Extension (VS Code, JetBrains), iOS App. Alle teilen den gleichen Agent-Engine; Permission-Modes koennen unterscheiden (Cloud-Surfaces nur `acceptEdits`/`plan`).
- **Verwandt:** Permission Mode, Model
- **Modul:** 1.1 — What is Claude Code?

---

## T

### Task Tool
Cluster von Built-in-Tools fuer Task-Tracking (ersetzt das alte `TodoWrite` seit v2.1.142): `TaskCreate`, `TaskList`, `TaskUpdate`, `TaskGet`, `TaskOutput`, `TaskStop`. Genutzt fuer To-Do-Listen in Sessions und Subagent-Koordination.
- **Verwandt:** Built-in Tools, Sub-Agent
- **Modul:** 3.1 — Agents & Multi-Agent

### Telegram Bridge (Custom)
Workshop-Custom-Pattern: Ein Bot, der Claude-Code-Sessions ueber Telegram-Messages steuert. Eigenes Pattern, NICHT Anthropic-offiziell. Offizielle Alternative: Channels (MCP-Push) oder `claude remote-control` + `/teleport`.
- **Verwandt:** Channels, Remote Control
- **Modul:** 3.5 — Telegram & Inception

### Token
Die Abrechnungseinheit fuer LLM-Inputs und -Outputs. ~4 Zeichen Englisch = 1 Token. Pricing nach Input/Output und Modell. `/cost` zeigt Session-Verbrauch.
- **Verwandt:** Context Window, Cost-Cap, Model
- **Modul:** 1.1, 3.6

### Trigger Phrase
Worte oder Saetze in der `description:` eines Skills, die Claude beim Auto-Invoke nutzt. Beispiele: "TDD", "write tests first", "red-green-refactor". Praezise Trigger-Phrases reduzieren False-Positives.
- **Verwandt:** Skill, Skill Frontmatter, Command
- **Modul:** 2.1 — Skills & Commands

---

## W

### Worktree
Git-Feature: zusaetzlicher Working-Tree auf demselben Repository, andere Branch. Erlaubt parallele Subagents in isolierten Filesystem-Bereichen. Claude Code unterstuetzt `--worktree <branch>` Flag (legt auto unter `<repo>/.claude/worktrees/<name>` an).
- **Verwandt:** Worktree Base Ref, Sub-Agent
- **Modul:** 1.4 — Git Integration & Worktrees

### Worktree Base Ref
Settings-Wert in `worktree.baseRef`: `fresh` (`--worktree` branched von `origin/<default>`) oder `head` (vom lokalen HEAD). Der Default hat sich zwischen CLI-Versionen geaendert (fruehe Versionen `head`, neuere `fresh`) — explizit setzen statt auf den Default verlassen. Wichtig fuer Multi-Agent-Setups, wo der Base-Branch sauber sein soll.
- **Verwandt:** Worktree, Settings
- **Modul:** 1.4, 3.5

---

## Begriffliche Drift

Aktualisierungen, die in aelteren Workshops, Doku oder Tutorials noch anders heissen:

| Alter Begriff | Aktueller Begriff | Kontext |
|---|---|---|
| `allowed_tools` | `tools` | Subagent-Frontmatter |
| `Task` (Tool) | `Agent` | Built-in Tool umbenannt v2.1.63 |
| MCP-Scope `project` | `local` | `.claude/.mcp.json` |
| MCP-Scope `global` | `user` | `~/.claude/.mcp.json` |
| `--enable-auto-mode` | `--permission-mode auto` | CLI-Flag entfernt, Auto-Mode jetzt ueber Permission-Mode-Selector |
| `/vim` | entfernt | v2.1.92 — Vim-Mode raus |
| `/pr-comments` | entfernt | v2.1.91 — stattdessen Claude direkt fragen ("zeig mir die PR-Comments") |
| `TodoWrite` | `TaskCreate`/`TaskList`/... | Task-Cluster ersetzt TodoWrite, v2.1.142 |
| `--fast` (CLI-Flag) | `/fast` (Slash-Command) | Toggle nur noch in Session |
| `~/.claude/skills/<name>.md` | `~/.claude/skills/<name>/SKILL.md` | Skill ist immer ein Ordner mit `SKILL.md` |

---

*Siehe auch `resources/faq.md` und `resources/troubleshooting.md`. Vertieftes Material in `resources/modules/`.*
