# Block 1: Foundations — Teaching Content

**Audience:** Experienced programmers who are **new to coding agents**. We assume strong programming background and explain agent concepts from zero. Security analogies used throughout — especially relevant for the CySec engineer in the group.
**Duration:** ~90 minutes
**Goal:** Participants understand what Claude Code is, how context and memory work, how to write effective prompts, and how to use git integration.

---

## Lerneinheiten-Landkarte (Welle F — Session 1)

> Dieser Block speist **Session 1** des 4-Session-/65-LE-Plans (`session-plan.md`). Jede LE ist hier
> auf ihre Quell-Abschnitte und ihr Level abgebildet — adressierbar für den `workshop-mentor`-Agent
> und das `/workshop`-Command. Reihenfolge = Lehr-Reihenfolge laut session-plan, nicht Datei-Reihenfolge.

| LE | Level | Titel | Quell-Abschnitt(e) in diesem Modul |
|---|---|---|---|
| S1.1 | core | Coding Agent vs. Chat — mentales Modell | Module 1.1 → *Overview*, *The Three Consultant Modes*, *Boris Cherny's Philosophy* |
| S1.2 | core | First Contact: bau sofort eine Datei | 1.1 → *First: Hello, Claude Code*, *What Claude Code Can Do*, *What Claude Code Cannot Do* |
| S1.3 | core | Die Oberflächen (CLI/Desktop/IDE/Web/iOS) | 1.1 → *The Five Surfaces*, *Surface-Switching from Inside a Session* |
| S1.4 | core | Built-in Tools & Tool-Namen | 1.1 → *Built-in Tools Reference* |
| S1.5 | core | Permissions Grundlagen: default & acceptEdits | 1.1 → *Permission System* (Alltags-Modi default/acceptEdits/plan + allow/deny) |
| S1.6 | **core** ⭐ | Permission Modes komplett (6 Modi + Cloud) | 1.1 → *Permission System* (auto/dontAsk/bypass + Cloud-2-Modi-Restriktion) |
| S1.7 | core | Modellwahl & Effort-Level | 1.1 → *Model Selection & Cost Awareness*; 1.5 → *Effort Levels as a Strategic Lever* |
| S1.8 | core | Kontextfenster verstehen | 1.2 → *The Context Window*, *The Control Room with Limited Monitors*, *Context Compression* |
| S1.9 | core | `/compact`, `/rewind` & Kontext steuern | 1.2 → *Context Compression: How to Handle It*, *Key Context Commands* |
| S1.10 | core | CLAUDE.md: Projekt-Standing-Orders | 1.2 → *CLAUDE.md: Your Project Access Policy*, *CLAUDE.md as Access Policy* |
| S1.11 | deep-dive | Memory-Layer komplett | 1.2 → *Auto-Memory*, *.claude/rules/*, *CLAUDE.local.md*, *Managed-Policy CLAUDE.md* |
| S1.12 | deep-dive | `@path`-Imports, `--add-dir`, AGENTS.md | 1.2 → *@path Imports and AGENTS.md Interop*, *Multi-Project Setup with --add-dir* |
| S1.13 | core | Vager vs. präziser Prompt | 1.3 → *Clarity Over Cleverness*, *The Contractor Analogy*, *Scope Control* |
| S1.14 | core | Plan Mode & Explain/Propose/Refine/Execute | 1.3 → *Iterative Work Pattern*, *Plan Mode*, *Effective Prompting Patterns*, *Bad vs Good*, *What Not to Do* |
| S1.15 | deep-dive | Output Styles & Personas | 1.3 → *Output Styles*, *`/voice` for Dictation*, *Persona-Switching via System Prompt* |
| S1.16 | core | Git in einem Flow: branch → commit → PR | 1.4 → *Built-in Git Capabilities*, *The Full PR Workflow in One Flow*, *Key Git Commands* |
| S1.17 | deep-dive | Git-Slash-Commands | 1.4 → *Git-Related Slash Commands*, *Resuming a Session at a Specific PR* |
| S1.18 | deep-dive | Worktrees als Test-Labor | 1.4 → *Git Worktrees*, *Worktree as Test Lab*, *The --worktree CLI Flag*, *worktree.baseRef*, *Worktrees in Practice* |
| S1.19 | core | Kosten im Blick: /cost, /usage & Budget-Cap | 1.5 → *Token Tracking — Three Tools*, *Budget Caps for Autonomous Sessions* |
| S1.20 | core | Hands-on Puffer (Exercise 1.x — pick 1) | `exercises/block-1-exercises.md` |

> **💸 Verschoben nach Session 4 (S4.4):** Der Rest von Modul 1.5 — *Pricing Reference*, *Deep Dive: /insights*,
> *Model Choice (Plan/Implement/Review Pipeline)*, *Cost-Reduction Tactics*, *Team Rules of Thumb*,
> *Prompt Caching*, *Anti-Patterns* — wird im Live-Workshop **nicht** in Session 1 gefahren, sondern bei den
> CI-Budget-Caps in **S4.4** praktisch wieder aufgegriffen. Der Text bleibt hier als Referenz/Selbststudium stehen.
>
> **⭐ S1.6 ist `[core]`** (nicht deep-dive): Die Zielgruppe (Physical-Security-Profis) will die vollen 6
> Permission Modes / Clearance-Level früh sehen. Die Lernziele unten sind entsprechend angepasst.

---

## Module 1.1: What is Claude Code?

**Learning Objectives:** After this module, you can:
- **Explain what a coding agent is and how it differs from a chat assistant** — the core mental model everything else builds on.
- Distinguish between Claude Code's five surfaces (CLI, Desktop App, IDE Extension, Web App, iOS App) and pick the right one for a given workflow.
- *(Comes later in the session — builds on the basics above)* Identify when each of the 6 permission modes (default / acceptEdits / plan / auto / dontAsk / bypassPermissions) applies and which restrictions cloud sessions impose. **Core for this security-focused audience** (LE S1.6).
- *(Comes later in the session — builds on the basics above)* Choose the right model (Fable 5 / Opus 4.8 / Sonnet 4.6 / Haiku 4.5) and effort level for a given task based on cost and reasoning depth (LE S1.7).

---

### First: Hello, Claude Code (do this now — ~5 minutes)

Before any theory, get one success under your belt. Three commands, a visible result:

```bash
# macOS / Linux / Git Bash
mkdir -p ~/cc-workshop/hello && cd ~/cc-workshop/hello
claude
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\cc-workshop\hello" | Out-Null
Set-Location "$HOME\cc-workshop\hello"
claude
```

Once Claude Code starts, type a plain-language request and hit enter:

```
Create a file hello.py that prints "Hello from Claude Code" and run it.
```

Watch what happens: Claude proposes the file, asks permission to write it, creates it, then runs it and shows you the output. **That loop — you describe, it acts, you see the result — is the whole game.** Everything in the rest of this module just explains the mechanics behind what you just did.

> New to agents? The key thing you just saw: Claude didn't *tell you how* to write the file — it *wrote and ran it itself*. That's the difference between a chat assistant and a coding agent. We unpack it next.

---

### Overview

Claude Code is not a chat interface. It is a command-line tool that gives an AI agent full, active access to your development environment. A chat assistant answers your question and leaves the doing to you; an **agent** takes actions on your behalf — it reads and writes files, runs commands, and checks the results — inside a permission system you control. Understanding that distinction, and the different surfaces Claude Code runs on, is the first mental model to establish.

---

### The Five Surfaces

**1. claude.ai (Web Chat)**

The browser-based chat you may already know. You type, Claude responds. You can share files by uploading them manually. Claude reads and reasons but has no ability to execute code, write files, or interact with your system directly.

This is a consultation interface. Claude gives you advice and you implement it yourself.

**2. Claude Code CLI**

Installed as a terminal command (`claude`). When you run it, you get an interactive session where Claude has:

- Full read/write access to your filesystem (within your working directory)
- The ability to run shell commands on your behalf
- Git integration (commits, branches, PRs)
- Web search capability
- Access to external tools via MCP (Model Context Protocol)
- The ability to spawn sub-agents for complex parallel tasks
- Persistent memory across sessions

This is not a chat interface. This is an agent operating in your environment.

**3. Desktop App**

Claude Code is also available as a **Desktop App** (Mac/Windows). It provides the same agent capabilities as the CLI — file access, command execution, git integration — but with a graphical interface on top of your local machine. Useful for people who prefer a GUI over a terminal. (The cloud-hosted Web App at claude.ai/code is covered separately in surface 5.)

**4. IDE Extensions (VS Code, JetBrains)**

An IDE extension that runs Claude Code as a sidecar chat panel in your editor. Available as the official **VS Code extension** (installable from the marketplace) and the **JetBrains plugin** (IntelliJ, PyCharm, GoLand, WebStorm, Rider). Both surfaces expose the same agent engine as the CLI, plus a **mode-indicator UI** at the bottom of the prompt box that shows the current permission mode (default / acceptEdits / plan / auto / bypassPermissions) and lets you switch with one click instead of typing `/permissions`.

The extension has access to your open files and project context, and can make edits directly. Think of it as a senior colleague sitting next to you who can see your screen and make changes when you ask — but it's not passively watching everything you type in real time.

This is a pair programming interface.

**5. Web App & iOS App**

Claude Code is also available as a cloud-hosted surface at **claude.ai/code** (Web App) and through the **iOS App** on iPhone/iPad. Both run sessions on Anthropic's infrastructure, connected to a GitHub repository instead of your local filesystem. Useful for: status checks on long-running tasks while away from your laptop, kicking off a PR-review from your phone, and pairing with the same session from multiple devices.

**Important security restriction:** Cloud sessions only support two permission modes — `acceptEdits` and `plan`. The aggressive modes `auto`, `dontAsk`, and `bypassPermissions` are **not available** in the cloud, because cloud sessions don't have a trusted-VM boundary the way your local machine does. If your workflow depends on `auto`, stay local.

### Surface-Switching from Inside a Session

You don't have to pick one surface and stick with it. Claude Code provides three slash commands to teleport an active session between surfaces:

- `/desktop` — push the current conversation to the Desktop App
- `/mobile` — push the current conversation to the iOS App (requires logged-in mobile session)
- `/chrome` — open the current conversation in claude.ai/code in your default browser

Use case: you start a long refactor on the CLI, switch to `/mobile` when you leave the office, check in from your phone, and `/chrome` back into the web app when you sit down at a different machine.

---

### Security Analogy: The Three Consultant Modes

Your participants deal with physical security every day. This analogy maps cleanly onto what they already know.

**claude.ai = Security Consultant on the Phone**

You call a security expert. They listen to your description of the building, the lock placement, the camera angles. They give you advice. They might say "your server room door should have a card reader AND a PIN pad." But they never touch anything. They have no physical access. Whatever they say, you go implement it yourself.

Capability: advice, analysis, review — zero physical footprint.

**Claude Code CLI = Consultant with Badge Access**

Same expert, but now they have a visitor badge and an escort has walked them through the building. They can open doors, physically inspect locks, review wiring in the comms room, pull the access log off the controller, make configuration changes on the panel. They operate in your environment, under your supervision, with real effects.

Capability: reads your files, writes your files, runs your commands, commits your code, creates your branches.

**Desktop App = Consultant in Your Office with a Nice Desk**

Same expert, same badge access, but now sitting at a proper desk with a monitor instead of standing at a terminal. The work is the same — file access, commands, git. The interface is just more comfortable. Some consultants prefer a standing desk (CLI), others prefer a chair (Desktop App). (The cloud-hosted Web App + iOS App map onto a different analogy — "Consultant Reachable from the Road" — and live on Anthropic's infrastructure.)

Capability: identical to CLI — different wrapper, same engine.

**IDE Extension = Consultant Sitting Next to You**

Same expert, at a desk next to yours. They can see your editor, your open files, your project structure. When you ask, they make changes directly. They don't passively watch every keystroke, but they have full context of what you're working on and can jump in when asked.

Capability: file context, direct edits, project-aware suggestions.

---

### Boris Cherny's Philosophy

Boris Cherny is the original creator of Claude Code. His design philosophy is deliberately anti-prescriptive:

> "Claude Code is a power tool. There's no one right way to work with it. Everyone uses it differently for their tasks. You have to figure out what works best for you."

This matters because it sets the right expectation for the workshop: we are not teaching "the correct way to use Claude Code." We are teaching you the mechanics, the mental models, and a range of patterns. What you build from those is yours.

Compare this to a circular saw: the manual tells you how the blade works, the safety features, the feed rate. But how you use it to build your project is your decision. The tool does not constrain your creativity.

---

### What Claude Code Can Do

- **Read codebases**: Traverse directories, read files, understand entire projects at once
- **Write and edit files**: Create new files, modify existing ones, refactor across multiple files
- **Run commands**: Execute shell commands, run test suites, build projects, start services
- **Manage git**: Stage, commit, branch, merge, push, create pull requests — all from conversation
- **Search the web**: Research documentation, find packages, look up error messages
- **Orchestrate agents**: Spawn parallel sub-agents for independent tasks
- **Connect via MCP**: Integrate with external tools — databases, APIs, monitoring systems, GitHub, Slack
- **Remember across sessions**: Persist context using CLAUDE.md and the memory system

### Built-in Tools Reference

Claude Code works through **tools** — each capability has a specific tool name. These names matter for permissions, hooks, and agent configuration:

These are the tools you'll actually see in your first sessions — the everyday core:

| Tool | What it does | Needs permission? |
|------|-------------|-------------------|
| `Read` | Read files | No |
| `Glob` | Find files by pattern | No |
| `Grep` | Search file contents | No |
| `Edit` | Modify files (targeted replacement) | Yes |
| `Write` | Create/overwrite files | Yes |
| `Bash` | Execute shell commands | Yes |

**Security analogy:** Each tool is like a specific card-access zone. `Read` is the lobby — everyone gets in. `Bash` is the server room — you need explicit clearance. When you configure permissions (allow/deny rules) or hook matchers, you use these exact tool names.

> **Full tool reference** — `WebSearch`, `WebFetch`, `LSP`, `Skill`, `Agent`, `Monitor`, `AskUserQuestion`, `TaskCreate`/`TaskList`/`TaskUpdate`, `NotebookEdit`, `PowerShell`, and the rest — lives in [`resources/cheatsheet.md`](../cheatsheet.md#built-in-tools). You don't need them on day one; `Skill` and `Agent` are explored in depth in Block 2.1 (Skills) and Block 3.1 (Agents).

---

### Model Selection & Cost Awareness

Claude Code supports multiple models. Choosing the right one matters for both quality and cost:

| Model | Context | Strengths | Cost |
|-------|---------|-----------|------|
| **Claude Fable 5** (`claude-fable-5`, GA 2026-06-09) | 1M tokens | Anthropic's most capable model — hardest reasoning, long-horizon agentic work. Premium tier. | Premium |
| **Claude Opus 4.8** (current default, model ID `claude-opus-4-8`) | 1M tokens | Deepest Opus-tier reasoning, architecture, complex tasks. Effort defaults to `high`. | High |
| **Claude Sonnet 4.6** | 1M tokens | Fast, capable, everyday coding | Medium |
| **Claude Haiku 4.5** | 200K tokens | Quick tasks, brainstorming, bulk operations | Lowest |

> Model names move fast. The script was written against Opus 4.8 (current default since ~May 2026); Fable 5 went GA on 2026-06-09. Run `/model` to see what your CLI actually offers, and `/release-notes` for the latest.
>
> **Mind Haiku's 200K context** (vs. 1M on the others): it caps *bulk-read* tasks. Use Haiku for small, focused reads and Opus/Fable for whole-codebase analysis — if Haiku seems to "forget" the start of a large file, the 200K limit is why.

**How to switch:**
- At startup: `claude --model sonnet`
- In session: `/model` command
- Effort level: `/effort <low|medium|high|xhigh|max>` — five tiers from cheap-and-fast to deepest analysis. On Opus 4.8 the default is `high`; `xhigh` and `max` (available on Opus 4.7, Opus 4.8, and Fable 5) unlock even deeper reasoning when set explicitly
- Check spend: `/cost` shows token usage and cost for the current session
- Check context: `/context` visualizes how much of the context window is used

**Rule of thumb:** Start with Opus for planning and architecture. Switch to Sonnet for implementation. Use Haiku for bulk reads and simple tasks. Use `/cost` regularly to stay aware of spend.

> **Lean System Prompt (recent default).** On current Opus-4.8+ builds Claude Code ships a **leaner system prompt** by default — less fixed overhead in your context window, so more room for your actual code. You rarely need to touch it; if you want to override or extend it, use `--append-system-prompt` (add to it) or `--system-prompt` / `--system-prompt-file` (replace it).

> Detailed pricing per million tokens, effort multipliers, and the Plan/Implement/Review cost strategy live in **Module 1.5 (Cost Engineering)** — single source of truth.

---

### Permission System

Claude Code has a built-in permission system that controls which tools it can use. This is security through least privilege — a concept your participants already know well.

**Permission modes (6 levels, set via `claude --permission-mode <mode>` or `/permissions`):**

| Mode | Behavior | Analogy |
|------|----------|---------|
| **default** | Only reads allowed, everything else asks for approval | Visitor badge — lobby access only |
| **acceptEdits** | Reads + file edits allowed; bash still asks — **but** common filesystem Bash in the workdir (`mkdir`/`touch`/`rm`/`mv`) is also auto-approved (⚠️ incl. destructive `rm`/`mv`; detail in Modul 3.3) | Maintenance badge — utility rooms too |
| **plan** | Shows full plan upfront, approves all steps at once | Security briefing — approve the mission |
| **auto** | ML classifier decides risk level (Max-Plan with Opus 4.8, plus Team/Enterprise) | Smart badge — system decides per door |
| **dontAsk** | Never prompts — relies entirely on allow/deny rules | Automated system — rules only, no guard |
| **bypassPermissions** | Accepts everything (DANGER — isolated VMs only!) | Master key — no locks at all |

**Allow/deny rules in `settings.json`:**
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(npm test)"],
    "deny": ["Bash(rm *)", "Bash(curl*)"]
  }
}
```

**Allowlists via CLI flag:** `claude --allowedTools "Read,Glob,Grep"` — only these tools are available.

**Security analogy:** This is card access clearance levels. A visitor badge gets you through the lobby but not the server room. A maintenance badge opens utility closets but not the executive floor. Each Claude session has a clearance level — you decide what it can access. The permission mode sets the *default* clearance, and allow/deny rules fine-tune individual doors.

---

### What Claude Code Cannot Do

- **Access your screen directly**: It cannot see your GUI, your browser, your monitor display. Only what it can read from the filesystem or run as commands. *(Note: Since March 2026, Computer Use allows Claude to control the desktop on macOS, Windows, and Linux — mouse, keyboard, screenshots. This is a separate feature and not enabled by default.)*
- **Run persistent services**: It can start a server but does not maintain background processes between sessions.
- **Access private networks without configuration**: VPN, internal APIs, on-prem systems require explicit MCP configuration or tunneling.
- **Make production decisions without approval**: Best practice is always human approval for anything touching production. Claude Code does not push to production by itself.
- **Know what it doesn't know**: Like any LLM, it can be confidently wrong. Always verify critical outputs.

---

### Practical Implication for Physical Security Developers

Your domain involves:
- Firmware for access controllers
- Integration protocols (OSDP, Wiegand, RS-485)
- Event log parsing and alarm correlation
- Configuration management for large panel installations
- Regulatory compliance in safety-critical systems

Claude Code can read your controller configuration files, understand your protocol implementations, write parsers for your event log formats, generate test harnesses for alarm state machines, and help you navigate compliance requirements. But it does not touch your live panels. That boundary is yours to enforce.

---

## Module 1.2: Context & Memory

**Learning Objectives:** After this module, you can:
- Explain how the context window fills, when auto-compression triggers, and use `/context` and `/compact` to manage it deliberately.
- Decide where each piece of project knowledge belongs across the four memory layers (`CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, Auto-Memory) and apply the Managed > User > Project precedence.
- Use `@path` imports, `--add-dir`, and the `InstructionsLoaded` event to debug what is actually loaded into context at session start.

### Overview

Claude Code does not have unlimited awareness of your project. It has a context window — a finite working memory. Understanding how this works, and how to manage it, is essential for reliable sessions.

---

### The Context Window

The context window is Claude's active memory for a session. Everything Claude "knows" during your conversation — your files, your instructions, your conversation history, the results of commands it ran — lives in this window.

**Size:** Up to 1 million tokens for Claude Opus (roughly 750,000 words, or about 5,000 pages of text). This sounds enormous, but a large codebase with many files can fill it quickly.

**What goes in:**
- Your messages and Claude's responses
- Files Claude reads
- Command output (stdout/stderr)
- CLAUDE.md contents
- Memory items loaded at session start

**What happens when it fills:**
Auto-compression. Claude summarizes the oldest parts of the conversation. The summary replaces the full history. Detail is lost. This is why having a persistent external memory (CLAUDE.md, memory files) matters — they are reloaded fresh each session.

---

### Security Analogy: The Control Room with Limited Monitors

Your security operations center has a wall of monitors. Each shows a camera feed. But you have 200 cameras and only 20 monitor slots.

When a new camera feed is critical — say, an active alarm at Door 47 — you bring it up. But you only have 20 slots. One of the older feeds gets archived. The operator can still request the archived feed, but it takes time and effort to pull it back up.

Claude's context window works the same way. Active information is on the monitors. Old information gets archived (compressed). You can reference it again, but with less fidelity than when it was live.

The implication: **don't rely on Claude remembering details from early in a long session.** If something is important, write it down (CLAUDE.md, a file, a note). Make Claude reread it if it's critical.

---

### CLAUDE.md: Your Project Access Policy

CLAUDE.md is a Markdown file that Claude Code reads automatically at the start of every session. Think of it as the standing orders, the briefing document, the project access policy.

**Two levels:**

- `./CLAUDE.md` — project-level, checked into the repo, applies to this project
- `~/.claude/CLAUDE.md` — user-level, applies to all your Claude Code sessions

**What to put in CLAUDE.md:**
- Technology stack and versions
- Coding conventions (naming, formatting, test framework, lint rules)
- Project-specific terminology and domain knowledge
- What not to do (e.g., "never use global state", "never modify the legacy parser")
- Deployment notes, key file locations
- Contact info or escalation notes if relevant

**What not to put in CLAUDE.md:**
- Secrets (API keys, passwords) — these should never be in plaintext files
- Temporary task context — use the conversation for that
- Lengthy documentation — keep it concise, Claude reads it every session

---

### Security Analogy: CLAUDE.md as Access Policy

In physical security, a new contractor arriving on site is handed the site access policy document: which areas are authorized, which are off-limits, what procedures to follow if an alarm triggers, who to contact. They read it before they start work.

CLAUDE.md is exactly this. Every session, Claude reads the policy before doing anything. If the policy says "always run pytest before committing," Claude will always run pytest before committing. If it says "never modify the legacy firmware parser," Claude will treat that as a hard boundary.

You write the policy once. Claude follows it every session, without being reminded.

---

> ### ⏩ Deepening — skippable on a first pass
>
> **Core so far:** the context window fills and auto-compresses, and `./CLAUDE.md` is the standing policy Claude reads every session. That's enough to work productively. If this is your first pass, **jump ahead to "Context Compression" below** (the `/context` and `/compact` commands) and come back to the memory mechanisms here later.
>
> The next sections cover the *advanced* memory machinery — Auto-Memory internals, path-scoped rules, `@path` imports, `CLAUDE.local.md`, managed enterprise policy, and multi-repo `--add-dir`. Useful, but not needed for your first sessions.

### The Memory System: Auto-Memory (Default On)

Beyond CLAUDE.md, Claude Code has a structured memory system stored in `~/.claude/projects/<project>/memory/`. Since **recent releases this Auto-Memory feature is default on** — you don't have to ask Claude to remember anything. Claude automatically captures notes during a session and writes them to disk: build commands that worked, debugging insights, code-style preferences it observed, project-specific gotchas. The next session starts with that knowledge already in context.

**The file layout:**

- `MEMORY.md` — the **index file**. The first 200 lines (or ~25 KB) are loaded at every session start, before Claude reads anything else.
- `debugging.md`, `patterns.md`, `commands.md`, etc. — **topic-files** that the index references. These are loaded on-demand when Claude decides they are relevant (similar to how a librarian pulls a specific book off the shelf instead of carrying the entire library).

This split keeps session bootstrapping fast (always-load is bounded) while still giving Claude access to a deep memory archive when needed.

**Memory types Claude tends to capture automatically:**

- **User preferences**: "I prefer German for communication but English for code." Stored and applied every session.
- **Feedback**: "Last time you refactored the parser this way, it broke the alarm correlation module." Stored as a lesson.
- **Project context**: "This project uses a custom OSDP variant — see osdp-custom-spec.md for deviations." Stored as reference.
- **Working commands**: build invocations, test runners, deploy steps that succeeded.

**Inspect what Claude knows about you:**

Open `~/.claude/projects/<your-project-hash>/memory/MEMORY.md` in your editor. You will likely find that Claude has already started taking notes for you without being told to. On Windows the project-hash directory uses the full path with slashes replaced by hyphens and `C:` rewritten as `C--`.

**Manual triggers still work:**

The old phrase "Remember that..." or "Note for future sessions that..." still works as an explicit hint — Claude will preserve that note with higher priority. But it is no longer required for memory to accumulate. The system runs whether you ask for it or not.

To opt out of Auto-Memory for a single run, use `claude --bare` (skips Hooks, Skills, Plugins, MCP, and Auto-Memory — useful for short scripted invocations).

> **Privacy — the one thing to remember now:** Auto-Memory writes notes to disk and sends them
> to Anthropic as part of each session's context. **Never let secrets (API keys, credentials,
> customer data) end up in it.** Opt out of a single run with `claude --bare`.
>
> The full privacy regime — periodic `MEMORY.md` review, `claude project purge`, and drift-detection
> — is covered in Module 3.7 (Troubleshooting).

---

### `.claude/rules/` — Path-Scoped Rules

A monolithic CLAUDE.md works fine for small projects. For larger codebases with different conventions per subdirectory (e.g., `src/api/` follows REST conventions, `src/firmware/` is C with embedded-style rules), Claude Code offers **path-scoped rules** as a fourth memory mechanism alongside `./CLAUDE.md`, `~/.claude/CLAUDE.md`, and Auto-Memory.

Rules live in `.claude/rules/<name>.md` and use **YAML frontmatter** with a `paths` glob to declare when they apply:

```markdown
---
paths: ["src/api/**/*.ts"]
---

# API Conventions

- All endpoints use Zod for input validation.
- Error responses follow RFC 7807 (Problem Details for HTTP APIs).
- Never use `any` in request/response types — use `unknown` with a type guard.
```

This rule will be loaded into context **only** when Claude is working on files matching `src/api/**/*.ts`. When the active task touches `src/firmware/`, the API rules stay quiet and a different `firmware-conventions.md` rule could apply instead.

**When to use rules instead of CLAUDE.md:**

- Codebase >50 files with multiple distinct domains
- Different test runners, linters, or naming conventions in different subdirectories
- You want a rule that should *not* leak into Claude's reasoning when working elsewhere

**Security analogy:** Path-scoped rules are zone-specific security policies. The rules for entering the server room are not the same as the rules for the reception lobby — and the guard at reception should not have to memorize server-room policy on every shift. Each zone has its own policy, loaded only when relevant.

---

### `@path` Imports and AGENTS.md Interop

CLAUDE.md supports **modular includes** via the `@path` syntax. Instead of one large file, you can split your project memory across smaller documents and pull them in:

```markdown
# Project: Access Controller Firmware

@./docs/architecture.md
@./docs/coding-conventions.md
@AGENTS.md
```

At session start, Claude expands these imports inline, so the agent sees a single concatenated document. Edits to the included files are picked up automatically on the next session.

**`@AGENTS.md` is a deliberate cross-pollination feature.** AGENTS.md is the convention used by OpenAI Codex and several other AI coding tools. If your repository already has an AGENTS.md (for cross-tool compatibility), import it into CLAUDE.md with `@AGENTS.md` and both tools read the same source of truth. No copy-paste, no drift.

---

### CLAUDE.local.md — Personal Project Notes

`CLAUDE.local.md` lives in the same directory as `CLAUDE.md` but is **gitignored by convention**. Use it for personal setup notes that should not enter the team repo: your local DB connection string, your preferred branch-naming style, a reminder that your laptop has a different Python version installed. Claude reads it together with the shared CLAUDE.md but it never gets committed.

---

### Managed-Policy CLAUDE.md — Enterprise Location

A fourth, **managed** CLAUDE.md exists for enterprise admins who need to push unconditional policies to every Claude Code installation on a machine — security restrictions, compliance notes, mandatory escalation paths. It lives in an OS-specific system location that requires admin rights to write:

| OS | Path |
|---|---|
| macOS | `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| Windows | `%ProgramData%\ClaudeCode\CLAUDE.md` |
| Linux | `/etc/claude-code/CLAUDE.md` |

**Precedence on conflict:** `Managed > User > Project`. If the managed policy says "never WebFetch from competitor domains" and a project CLAUDE.md tries to override it, the managed rule wins. This is by design — it gives security teams a hard floor that individual developers cannot lift.

**Typical use cases:** mandatory `DISABLE_TELEMETRY=1`, blanket-deny rules for `Bash(curl *)`, compliance reminders for regulated industries (HIPAA, ISO 27001), forbidden tool-categories. The file is loaded silently on every session start, no opt-in needed.

---

### Multi-Project Setup with `--add-dir`

When a session needs file-access to a second repository (cross-repo refactor, shared library extracted into its own repo), launch with `--add-dir`:

```bash
claude --add-dir /path/to/other/project
```

The flagged directory becomes part of Claude's allowed working area for `Read`, `Glob`, `Grep`, `Edit`, and `Write`.

**Default behavior:** Claude **does not** load CLAUDE.md from `--add-dir` paths. Only file-access is granted; the contextual rules of the secondary repo are ignored. This is a deliberate isolation guard — you don't want another project's conventions silently shaping how Claude behaves in your current one.

**Opt-in to CLAUDE.md discovery in additional directories:**

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir /path/to/other/project
```

With the env var set, every `--add-dir` path also contributes its own `CLAUDE.md` (and `.claude/rules/`, AGENTS.md, etc.) to the loaded context.

**Typical use cases:** refactoring a shared utility across two repos, porting a feature from one service to another, working on a frontend repo and the backend repo it consumes in one session.

---

> ### ⏩ End of deepening — back to the core
>
> The rest of the module is core again: how compression behaves and the everyday context commands.

### Context Compression: Why It Happens and How to Handle It

When the context fills, Claude auto-compresses. The compression:
- Summarizes early conversation turns
- Preserves recent turns in full
- Loses fine-grained detail from older parts of the session

**Signs you're hitting compression:**
- Claude starts forgetting things it "knew" earlier
- Responses become slightly less precise about earlier decisions
- You see a "compressing context..." message

**How to handle it:**
1. Use `/compact` proactively before hitting the limit — it compresses with an optional focus hint: `/compact focus on the API changes`
2. Use `/context` to visualize how much context you've consumed
3. Keep important decisions in CLAUDE.md, not just conversation
4. If you notice drift, say "Reread the CLAUDE.md" or paste the key constraint again
5. For very long tasks, consider breaking them into multiple sessions — use `/export` to save conversation history, `claude -r <name>` to resume named sessions
6. Use memory items for things you need persistent across all sessions

### Key Context Commands

| Command | What it does |
|---------|-------------|
| `/context` | Visualize context window usage — shows how full your "monitor wall" is |
| `/compact [focus]` | Compress context proactively (optionally with a focus hint) |
| `/export [file]` | Export conversation to a file for reference |
| `/resume <name>` | Resume a named session with full context |
| `/memory` | Manage auto-memory and CLAUDE.md entries |
| `/init` | Generate or improve project CLAUDE.md (interactive flow) |
| `/rewind` | Rewind to a checkpoint — undo multiple steps at once |

---

### Best Practices Summary

| Practice | Why |
|---|---|
| Keep CLAUDE.md concise | It's read every session; dense docs slow startup |
| Use memory for cross-session info | CLAUDE.md is static; memory is dynamic |
| Reread important files before critical actions | Don't assume Claude remembers from 50 turns ago |
| Break long sessions into focused tasks | Avoids compression drift on complex work |
| Never put secrets in CLAUDE.md | Security hygiene; version control is not a secret store |

---

## Module 1.3: Effective Prompting

**Learning Objectives:** After this module, you can:
- Rewrite a vague prompt into a specific work-order-style prompt with explicit scope, context, and success criteria.
- Apply the Explain / Propose / Refine / Execute pattern and `/plan` mode for multi-file tasks before any code is written.
- Switch output styles and personas using `/output-styles`, `--append-system-prompt`, and `--system-prompt-file` to match the task at hand.

### Overview

Claude Code's capability is constant. The quality of your results varies entirely with how you communicate. This module builds the habits that separate "meh" results from "exactly right" results.

---

### Clarity Over Cleverness

The most common mistake with AI tools is being too vague in an attempt to let the AI "figure it out." This is the wrong mental model. Claude Code is not psychic. It works with what you give it.

**Vague:**
```
Fix the bug.
```

Claude does not know which bug. It might guess, make a change, possibly introduce a new issue, and you have no way to validate whether it fixed the right thing.

**Specific:**
```
Fix the null pointer exception in auth.py at line 45. It occurs when a user account
has no email address set. The function assumes email is always present but new accounts
created via LDAP import can have null email fields. Add a null check before accessing
user.email and return an appropriate error response.
```

Claude now knows: which file, which line, the root cause, the triggering condition, and the expected fix strategy. The output will be dramatically better.

---

### The Contractor Analogy

Prompting Claude Code is like writing a work order for a contractor who has full building access.

You would not hand a contractor a note that says "fix the door." You would write:

> "The card reader on the north server room door (asset ID CR-047) is not triggering the relay after a valid card swipe. The controller log shows the card is being read (event type 0x01) but no relay event (0x04) follows. Check the relay wiring on panel P-03, terminal block TB-6. If the relay tests good, check the controller config for door group assignment. Document findings."

This is how to write prompts. Specific. Contextual. Actionable. Expected output defined.

---

### Scope Control

Smaller, focused requests produce better results than broad ones.

**Too broad:**
```
Refactor the entire alarm processing module.
```

This gives Claude latitude to change things you didn't expect. You lose control of what changes.

**Better:**
```
Refactor the alarm_deduplicator.py file only. Current issue: it uses a list for O(n)
lookups. Replace with a set or dict for O(1) lookups. Do not change the function
signatures or the public interface. Tests are in tests/test_alarm_deduplicator.py —
make sure they still pass.
```

Scope is defined. What not to touch is explicit. Success criterion is stated.

---

### Iterative Work Pattern

For complex tasks, a four-step pattern works well:

1. **Explain**: Give Claude the context. "Here's what we're building, here's the current state, here's the constraint."
2. **Propose**: Ask Claude to propose an approach before implementing. "What's your plan for handling this?"
3. **Refine**: Review the plan. Correct misunderstandings. Add constraints. "Good, but use the existing logger, not print statements."
4. **Execute**: "Go ahead and implement."

This pattern prevents the scenario where Claude writes 300 lines of code in a direction you didn't want.

**Effort as a prompting lever.** Some tasks benefit from `/effort xhigh` (architecture decisions, root-cause analysis of subtle bugs, multi-file refactors with side-effects to reason about). Others are better with `/effort low` (boilerplate, typo fixes, format-only edits). Choosing the right effort level is itself part of prompting — paying for `max` reasoning on a one-line typo wastes tokens; using `low` for an architectural choice produces shallow results. Match the effort to the cognitive load of the task.

---

### Output Styles: Persona-Switching for Different Contexts

Claude Code ships a `/output-styles` command that switches the response persona without changing the underlying model. Three built-in styles cover the common cases:

- **Concise** — minimal prose, bullet points, one-line summaries. Best for brainstorming, status checks, and "just give me the answer" sessions.
- **Detailed** — full explanations, reasoning made explicit, edge cases enumerated. Best for code review, design discussions, and learning sessions.
- **JSON** — structured machine-readable output (paired well with `claude -p --output-format json` for scripting and CI pipelines).

Switch with `/output-styles detailed`. The change persists for the rest of the session. Use Concise when you are deep in flow, Detailed when reviewing a teammate's PR, JSON when the output will be parsed by another tool.

### `/voice` for Dictation

For long prompts where typing is slow, `/voice [hold|tap|off]` enables voice-to-text dictation. `hold` requires holding a key while speaking, `tap` toggles on/off with a single tap. Useful when describing a multi-step refactor verbally is faster than writing it out.

---

### Persona-Switching via System Prompt

Where `/output-styles` switches the *response shape* (Concise/Detailed/JSON), system-prompt flags let you switch the *role* itself — code-reviewer, documentation-writer, tutor, principal engineer. Two CLI flags handle this:

- `--append-system-prompt "<text>"` — **additive**. Your instruction is appended to Claude Code's existing system prompt. Use this for narrow role-tuning that should layer on top of normal behavior.
- `--system-prompt-file <path>` — **complete persona from file**. Replaces the additive section entirely with the contents of a Markdown file. Use this for fully-shaped personas with multiple paragraphs of behavioral guidance.

Examples:

```bash
# Additive: code-review persona that always cites line numbers
claude --append-system-prompt "Always cite line numbers when referring to code. Never propose changes without showing the affected lines first."

# Full persona from file: tutor mode for onboarding a new teammate
claude --system-prompt-file ~/.claude/personas/tutor.md
```

Typical persona files: `code-reviewer.md` (no opinions, only flag-and-question), `docs-writer.md` (always produce Markdown, no code unless asked), `tutor.md` (explain at junior-developer level), `architect.md` (always sketch ADR-style trade-offs before deciding).

**Important — keep this out of CI.** Module 3.6 covers CI/CD scenarios where the system prompt is set programmatically per pipeline step. Don't mix interactive persona-switching with CI prompt-engineering — they live in different mental boxes and overloading the same flags causes accidents.

---

### Plan Mode

Claude Code has a built-in planning mode accessible via `/plan` or by pressing `Shift+Tab` before submitting your message.

In plan mode, Claude:
- Reads relevant files first
- Generates a structured implementation plan
- Lists the files it intends to change
- Asks for approval before writing a single line

Use plan mode for:
- Tasks touching more than 2-3 files
- Anything where you need to review the approach before code is written
- Refactors that span a module or subsystem
- Any task where mistakes would be expensive to undo

---

### Effective Prompting Patterns

These are battle-tested patterns to adopt immediately:

**"Read X first, then suggest"**
```
Read src/alarm_correlator.py and src/event_parser.py first. Then suggest
how we should add support for zone-group correlation without breaking
the existing per-zone logic.
```
Forces Claude to ground its suggestions in actual code, not assumptions.

**"Show plan before implementing"**
```
Show me your implementation plan before writing any code. I want to
review the approach and the list of files you'll change.
```
Gives you a checkpoint before any changes happen.

**"Only change X, don't touch Y"**
```
Update the database connection pool settings in config/db.py.
Do not touch any other configuration files or the connection pool
implementation itself — only the settings values.
```
Explicit exclusions prevent unintended scope creep.

**"Test by running Z"**
```
After making changes, run pytest tests/test_auth.py -v and show me
the output before we move on.
```
Embeds verification into the task. You see test results before you commit.

**"Explain what you did"**
```
Explain the changes you made and why, in plain language. Then show
the diff.
```
Forces Claude to articulate its reasoning, making it easier for you to catch misunderstandings.

---

### Bad vs Good: Side-by-Side Examples

| Bad Prompt | Good Prompt |
|---|---|
| "Fix the code" | "Fix the off-by-one error in event_parser.py line 78. The loop should iterate from index 1, not 0, because the first byte is always the sync byte." |
| "Make it faster" | "The alarm_correlator.process() function takes 200ms per call with 1000 events. Profile it and optimize — the bottleneck is probably the nested loop in lines 45-67." |
| "Add tests" | "Write pytest unit tests for the IPv4 validator in validators.py. Cover: valid addresses, leading zeros (invalid), out-of-range octets, too few octets, non-numeric characters, empty string." |
| "Refactor this" | "Refactor the state machine in door_controller.py to use Python's enum module instead of integer constants. Keep all function signatures identical. Run the existing tests to confirm nothing broke." |

---

### What Not to Do

- **Do not chain unrelated tasks in one prompt.** "Fix the bug AND add the feature AND update the docs" splits Claude's focus and makes it hard to verify each piece.
- **Do not rely on Claude's memory for critical constraints.** If "never modify the legacy parser" matters, put it in CLAUDE.md.
- **Do not accept the first output blindly.** Ask Claude to explain its reasoning. Ask it to consider edge cases. Ask "what could go wrong with this approach?"
- **Do not use vague approval.** "That looks good" may cause Claude to proceed to a next step you didn't intend. Be explicit: "Looks good, go ahead and implement" vs "Looks good, stop here."

---

## Module 1.4: Git Integration & Worktrees

**Learning Objectives:** After this module, you can:
- Drive a complete feature-to-PR workflow (branch, commit, push, PR) from inside a single Claude Code conversation.
- Distinguish `/diff`, `/rewind`, `/review`, `/autofix-pr`, `/branch`, `/fork`, and `--fork-session` and pick the right one for a given review or experimentation scenario.
- Set up a git worktree (manual or via `claude --worktree`) and configure `worktree.baseRef` for safe parallel development without stashing.

### Overview

Claude Code has native git integration. This means you can manage your entire version control workflow — branching, committing, pushing, creating pull requests — without leaving the Claude Code session. This module covers the workflow and introduces git worktrees for parallel development.

---

### Built-in Git Capabilities

Claude Code can execute git operations as naturally as it writes code:

- `git status` — check what's changed
- `git diff` — review changes before committing
- `git add` — stage specific files or all changes
- `git commit` — create commits with meaningful messages
- `git branch` / `git checkout -b` — create and switch branches
- `git push` — push to remote
- `git log` — review commit history
- `gh pr create` — create GitHub pull requests (requires GitHub CLI)

You can ask for these in plain language:

```
Create a branch called feature/alarm-dedup, implement the deduplication
change we discussed, commit it with a good message, and push it.
```

Claude handles the git mechanics. You review the diff and approve.

### Git-Related Slash Commands

| Command | What it does |
|---------|-------------|
| `/diff` | Interactive diff viewer — see all changes at a glance |
| `/rewind` | Rewind to a checkpoint — undo multiple steps, not just the last edit |
| `/commit` (skill) | Structured commit with conventional format |
| `/review [pr-num]` | Local PR review — sanity-check the current branch or a specific PR before merging |
| `/autofix-pr` | Spawns a cloud session that watches your PR's CI and pushes fixes automatically |
| `/branch` / `/fork` | Branch the *conversation* (not just the git history) — explore option A and option B in parallel without starting a new session |

`/diff` is especially useful before committing — it gives you a visual overview of everything Claude changed, so you can catch issues before they enter your git history.

`/rewind` is the "undo" for multi-step changes. If Claude made 5 edits and the last 3 went wrong, `/rewind` lets you go back to a specific checkpoint without manually reverting each file.

> **🔭 Outlook — first-pass readers can skim the next three.** `/autofix-pr`, `--fork-session`, and `--from-pr` are *cloud and multi-session* workflows. You don't need them to get value from git integration today — you'll actually drive them in Block 3 (Cloud Sessions & Multi-Agent). Read them now as a preview of where this goes, not as something to master in session 1.

`/autofix-pr` is the modern PR-workflow tool: after you run `gh pr create`, invoke `/autofix-pr` and Claude spawns a web session that monitors the CI checks. If a test fails or the linter complains, Claude pushes a fix commit directly — you don't have to babysit the PR. Example workflow:

```text
1. Implement feature locally.
2. gh pr create --title "Add IPv4 validation"
3. /autofix-pr      # Claude watches CI from the cloud and pushes fixes
4. Review final state and merge.
```

> **When to use `/autofix-pr`:**
> - **Test failures, lint failures, formatting issues** — low-risk fixes
> - **Doc typos, missing imports** — clearly mechanical
> - **NEVER for production-deploy failures** — those need human review
> - **NEVER for security/auth/crypto code** — even a "lint fix" could introduce a bug
> - **NEVER in repos where main branch deploys to prod automatically**
>
> Pair `/autofix-pr` with branch protection rules so the auto-pushed commit still needs
> human PR approval before merge.

`/review` is the **local PR review** — a final sanity-check pass before merge. It differs from `/security-review` (which focuses on the security diff only, covered in Module 3.3): `/review` looks at the full PR scope — correctness, readability, missed edge cases, test coverage, commit-message hygiene. Two invocation styles:

```text
/review        # reviews the current branch against its base (no PR number needed)
/review 1234   # reviews PR #1234 explicitly, even if you're not on that branch
```

Typical placement: after `/autofix-pr` has driven CI green, run `/review` for a last human-readable sanity pass before clicking Merge. The two commands stack — `/autofix-pr` for CI, `/review` for everything CI can't catch.

`/branch` and `/fork` operate on the **conversation tree**, not the git tree. They are the answer to "I want to try approach A *and* approach B without losing context." Combined with git worktrees, you can branch both the conversation and the working tree in parallel for fearless experimentation.

**`--fork-session`** is the session-level sibling of `/branch`: the `claude --fork-session` flag forks the *current* session into a new session-ID, preserving the original. Use it when you want to try something experimental without losing the conversation you're in. Different from `/branch` (which creates a conversation-branch *inside* the same session) — `--fork-session` creates a fully separate session you can later attach back to.

### Resuming a Session at a Specific PR

The `--from-pr <num>` CLI flag resumes a session targeted at a specific pull request:

```bash
claude --from-pr 1234
```

This is useful when you come back to a PR a day later, or when a colleague needs to pick up where you left off — the session opens with the PR diff, comments, and review state already loaded as context.

---

### The Full PR Workflow in One Flow

Here is a complete feature development cycle as a single Claude Code session:

1. **Start with context**: "We're adding IPv4 validation to the access controller API. Read the existing validators.py to understand the current pattern."
2. **Create the branch**: "Create a branch called feature/ipv4-validation."
3. **Implement**: "Implement the IPv4 validator following the existing pattern. Include input sanitization and tests."
4. **Review**: "Show me the diff."
5. **Test**: "Run pytest and show me the results."
6. **Commit**: "Commit with message: 'Add IPv4 validation to access controller API with full test coverage'"
7. **Push and PR**: "Push the branch and create a pull request with a description of what this does and why."

This entire flow happens in conversation. No terminal window switching, no copy-pasting commit messages, no manual `git push` after forgetting to add `-u origin`.

---

### Git Worktrees: Parallel Development Without the Risk

A git worktree is a separate working directory that shares the same git repository. You can have multiple worktrees checked out to different branches simultaneously.

**Why this matters:**

Imagine you are working on a major refactor in branch `refactor/alarm-correlator`. A critical bug is reported in production. Normally you would:
- Stash your refactor changes
- Switch branch
- Fix the bug
- Commit and push
- Unstash
- Continue refactor

With worktrees:
- Your refactor branch stays exactly where it is in its directory
- You create a new worktree for the hotfix
- Fix the bug in the hotfix worktree
- Commit and push from there
- Return to your refactor worktree unchanged

The two branches coexist as separate directories. No stashing. No context switch in your working tree.

---

### Security Analogy: Worktree as Test Lab

In physical security, when you need to test a new firmware version on a controller, you don't flash it on the live system first. You have a test bench — a replica of the production setup in a separate room. You flash the test bench, run your tests, confirm behavior, then schedule the production update.

A git worktree is your software test bench. It's a separate room with the same equipment, completely isolated from the live system. You can break things in the test bench without affecting production. When you're confident, you merge.

```
# Create a worktree for an experiment
git worktree add ../experiment-async-processing feature/async-experiment

# Now you have:
# ./                          (main branch, ongoing work)
# ../experiment-async-processing   (experiment branch, isolated)
```

### The `--worktree` CLI Flag — One-Step Worktree Sessions

Claude Code can also create a worktree for you in one command, skipping the explicit `git worktree add` step:

```bash
claude --worktree feature/zone-correlation
```

This starts a fresh Claude session inside a worktree at `<repo>/.claude/worktrees/feature-zone-correlation/`. No manual directory creation, no `cd`, and the worktree is automatically grouped under the repo's `.claude/` directory so it's easy to clean up later.

### `worktree.baseRef` — From Where Does the Worktree Branch?

Where `--worktree` branches from is controlled by `worktree.baseRef` — and the **default changed between CLI versions** (early versions branched from local `head`, newer ones default to `fresh`). Don't rely on the default; set it explicitly in `settings.json`:

- `worktree.baseRef: "head"` — branch from local HEAD, including unpushed work
- `worktree.baseRef: "fresh"` — branch from `origin/<default-branch>`, ignoring local state

The `fresh` setting is especially important for **multi-agent worktree setups** in Block 3 — each agent gets a clean starting point that matches what is on the remote, so two parallel agents are not accidentally building on top of each other's uncommitted work.

---

### Key Git Commands in Claude Code

**Check status before anything:**
```
What's the current git status?
```

**Create a branch:**
```
Create a new branch called feature/zone-group-correlation
```

**Stage and commit:**
```
Stage all changed files and commit with message:
"Add zone-group correlation support to alarm correlator"
```

**Review before committing:**
```
Show me the full diff of what would be committed. I want to review before we commit.
```

**Create a worktree:**
```
Create a worktree at ../alarm-refactor-experiment on a new branch
called experiment/alarm-refactor so I can test this approach in isolation
```

**Push and PR:**
```
Push this branch and create a GitHub PR. Title: "Add zone-group correlation".
Description should explain that this adds support for correlating alarms
by zone group, not just individual zones, and that tests cover the
3 new correlation patterns.
```

**The /commit skill:**

If you have the commit skill installed, `/commit` triggers a structured commit workflow: review diff, generate conventional commit message, confirm, commit. Useful for maintaining consistent commit message style.

---

### Worktrees in Practice: When to Use Them

| Scenario | Use Worktree? |
|---|---|
| Hotfix while feature branch is in-progress | Yes — keep feature branch untouched |
| Comparing two approaches side-by-side | Yes — run both simultaneously |
| Risky refactor you might want to abandon | Yes — keep main branch clean |
| Normal feature development | No — a single branch is fine |
| Running two different test configurations | Yes — each worktree has its own working state |

---

## Module 1.5: Cost Engineering & Effort Management

> **⏩ Optional / deepening module.** This is the 5th module of day one, on a topic that only
> matters once you've actually spent something. It's marked optional — exactly like its hands-on
> Exercise 1.5. **The 5-minute core:** `/cost` shows your current-session spend (glance at it
> occasionally); the default model (Opus 4.8) is a fine starting point; for anything unattended,
> cap it with `--max-budget-usd`. That's all you need on day one. Everything below — the pricing
> table, the Plan/Implement/Review pipeline, prompt caching, effort multipliers — is depth for
> when cost becomes a real lever (revisit after Session 1).

**Learning Objectives:** After this module, you can:
- Read `/cost`, `/usage`, and `/insights` and interpret which workflows drive your spend.
- Apply the Plan / Implement / Review pipeline (Opus + Sonnet + Haiku) and the right effort tier (low/medium/high/xhigh/max) per phase to balance quality and cost.
- Set `--max-budget-usd` as a hard guardrail for any unattended or autonomous Claude Code invocation.

### Overview

Claude Code costs money — per session, per day, per team. If you don't know what you're spending, you don't know how to optimize. This module turns cost into a deliberate variable instead of a surprise at the end of the month.

We've already seen models (Module 1.1), effort levels (Module 1.3), tools, and plan mode. Now: what does all of that actually cost in practice — and how do you keep it under control?

---

### Security Analogy: The Guard Roster

Think of a guarding company that runs a site with mixed staff: a seasoned patrol officer, an apprentice, and a specialist for technical alarms. Each one has a different hourly rate. If you put the specialist on lobby duty all night, you burn budget. If you put the apprentice on the alarm panel during an incident, you don't have the right competence on site. The art is matching the right person to the right shift.

Claude Code is the same: Opus is the specialist, Sonnet is the seasoned patrol officer, Haiku is the apprentice. The art is matching the right model to the right task — and knowing when each one is worth its hourly rate.

---

### Pricing Reference (as of 2026-06)

| Model | Input ($/M tokens) | Output ($/M tokens) | Relative cost |
|---|---:|---:|---|
| Claude Fable 5 | $10 | $50 | ~2x |
| Claude Opus 4.8 | $5 | $25 | 1x |
| Claude Sonnet 4.6 | $3 | $15 | ~0.6x |
| Claude Haiku 4.5 | $1 | $5 | ~0.2x |

**Rule of thumb:** Output costs roughly 5x input. Write tight prompts with few pre-loaded files — you pay for input too. A 50 KB CLAUDE.md loaded into every session is a recurring tax on every conversation you have with Claude.

(See **Module 1.1** for the qualitative model overview — context windows, strengths, use cases.)

---

### Token Tracking — Three Tools

Claude Code ships three slash commands for cost observability. Each answers a different question:

1. **`/cost`** — current session: what have I just spent?
2. **`/usage`** — daily/weekly view: what did I run this week?
3. **`/insights`** — analytics: which tools, which models, which sessions were expensive?

| Tool | When to use it |
|---|---|
| `/cost` | During a long session — am I still within budget? |
| `/usage` | Day or week check — did I stay inside my monthly cap? |
| `/insights` | Optimization — which workflows are expensive and why? |

A productive habit: glance at `/cost` whenever you've done something non-trivial (a multi-file refactor, a long planning session, a deep-research detour). It takes two seconds and prevents the "wait, I spent how much today?" moment at the end of the week.

---

### Deep Dive: `/insights`

`/insights` is the analytics dashboard. It shows:

| Metric | Use Case |
|---|---|
| **Cost per project** | Which projects are expensive? Is the team-wide budget concentrated in one repo? |
| **Cost per model** | How much went to Opus vs Sonnet vs Haiku? Are you defaulting to Opus too often? |
| **Cost per tool** | Which tools (Read, Bash, MCP, Subagent) are token-heavy? Often Bash and MCP are surprises. |
| **Cost per skill** | Which skills accumulate the most cost? Often `/loop` or `/agentic-os:run-loop`. |
| **Top expensive sessions** | Hourly histogram — when do costs spike? Is it during business hours or autonomous overnight loops? |

**Weekly review pattern:**

Run `/insights week` and check:
1. Top 3 expensive projects — are they justified?
2. Top 3 expensive sessions — were they intentional?
3. Top 3 expensive skills — should any be moved to Haiku?

This is the difference between **measured cost management** and **shocked-at-month-end** discovery.

**For teams:** Many CI/CD environments don't surface `/insights` data. Use the Anthropic Console
dashboard (https://console.anthropic.com/usage) as the team-aggregate view, and per-developer
`/insights` for individual breakdowns.

---

### Effort Levels as a Strategic Lever

Effort levels are not just a quality dial — they are a cost dial. The relative cost numbers below are approximate (effort-multipliers are not officially published as exact ratios) but the order-of-magnitude is real:

| Effort | Use case | Relative cost |
|---|---|---:|
| `low` | Typo fixes, single-line refactors, quick code reviews | 0.5x |
| `medium` | Standard coding, normal refactors | 1x |
| `high` (default on Opus 4.8) | Architecture decisions, multi-file refactors | 2x |
| `xhigh` | Deep analysis, root-cause debugging (Opus 4.7 / 4.8 / Fable 5) | 4x |
| `max` | Edge cases, "look at everything" — use sparingly | 6x |

**Best practice:** On Opus 4.8 the default is `high`. Downshift to `low`/`medium` for genuinely simple tasks (just as important as upshifting), and escalate to `xhigh`/`max` only when you can clearly identify a need for deep reasoning — otherwise you pay 4x for a 1.2x quality bump.

The reverse is also true: downshifting to `low` for genuinely simple tasks is just as important as upshifting for hard ones. Paying `xhigh` for a one-line typo fix is a small but recurring leak.

---

### Model Choice — The Plan / Implement / Review Pipeline

For demanding tasks, a three-model pipeline often beats a single-model approach on both quality and cost:

| Phase | Model | Effort | Why |
|---|---|---|---|
| **Plan** | Opus 4.8 | xhigh | Architecture is the most expensive phase to get wrong — paying for depth here saves you from rewriting later |
| **Implement** | Sonnet 4.6 | medium | Writing code is routine — Sonnet does it fast and solidly |
| **Review** | Haiku 4.5 | low | Final check, fast pattern-matching, Haiku is enough |

The cost shape is roughly `1x (plan) + 0.6x (implement) + 0.2x (review) ≈ 1.8x`, often producing better outcomes than Opus-only at the same total spend.

When *not* to use this pipeline: small tasks where the planning phase is the trivial part. A one-file utility doesn't need an Opus architect.

---

### Budget Caps for Autonomous Sessions

When you let Claude run for a long time without supervision (`/loop`, `/goal`, subagents, scheduled routines), cost can escape silently. One flag acts as the guardrail:

- `--max-budget-usd 5.00` — hard cap on dollars spent in this `-p` run

The current CLI offers no hard turn-limit flag anymore — `--max-budget-usd` is what caps runaway loops and runaway cost. This flag is essential for CI integration and any unattended workflow. It will be revisited in **Module 3.6 (CI/CD & Headless)** in detail.

Example:
```bash
claude --max-budget-usd 2.00 -p "/loop check deploy status"
```

If the limit is hit, Claude exits cleanly with a status code you can detect from CI.

---

### Cost-Reduction Tactics

Eight habits that compound over the months:

1. **Skills over a long CLAUDE.md** — Skills load on-demand; CLAUDE.md loads every session.
2. **Subagents for isolation** — keeps your main context free of side-quest tokens.
3. **`/compact` proactively** — compress *before* the context fills, with a focus hint so the right detail survives.
4. **Sonnet for routine work** — only reach for Opus when the task actually rewards depth.
5. **Haiku for bulk reads** — file inventory, simple filtering, "find me all files matching X."
6. **Cache reuse** — repeated tasks often land in cache (5-minute TTL on Anthropic's side).
7. **`--bare` mode** for simple invocations — skips Hook/Skill/Plugin/MCP overhead when you don't need them.
8. **Tight prompts** — drop unnecessary "explain your reasoning" when the answer is obvious.

---

### Team Rules of Thumb

- **Solo dev, active use:** $5–10 per working day is normal.
- **Pro Plan:** know your cap, watch the monthly aggregate.
- **Team:** make `--max-budget-usd` a default in shared scripts; review `/insights` weekly.

The dollar figures here are rough — your numbers will depend heavily on context length, model mix, and how often Claude is left running unattended. The point is that there *is* a number, and you should know it.

---

### Prompt Caching — The Biggest Cost Lever

Anthropic caches your prompts for **5 minutes**. If you make the same prompt (or very similar
ones with the same prefix) within that window, the input tokens are **90% cheaper**.

What this means:
- Long CLAUDE.md? Loaded once at session-start, cached. Subsequent turns within 5 min hit cache.
- Subagents spawned in sequence within 5 min reuse cached context.
- `/loop` runs every 30s for 5 min → all input tokens at 0.1x cost.

How to maximize cache hits:
1. **Don't switch models mid-session** — each model has its own cache.
2. **Keep CLAUDE.md stable** — every edit invalidates the cache for that session.
3. **Group related tasks in one session** — within 5 minutes, common context is cached.
4. **For batch CI runs:** use `--exclude-dynamic-system-prompt-sections` to maximize cache reuse
   across runs (this flag is for scripted multi-user workloads).

**What invalidates the cache:**
- Switching model (`/model opus` ↔ `/model sonnet`)
- Editing CLAUDE.md or a loaded skill
- 5-minute idle window (TTL)
- Different `--system-prompt` between runs

**Order of magnitude:** A 100K-token CLAUDE.md costs $0.50 per fresh load with Sonnet. On a
cache hit, it costs $0.05. Over 10 sessions/day, that's $4.50 vs $0.50 — meaningful.

---

### Anti-Patterns

- **Do not** default to Opus + `xhigh` — that's the most expensive combination, rarely justified.
- **Do not** run `/loop` or `/goal` without a budget cap — cost can multiply silently.
- **Do not** let CLAUDE.md grow without limit — every token is paid in every session forever.
- **Do not** rationalize ongoing spend with "I've already burned $20 today, may as well keep going." Treat the early stop signal as a feature.

---

### Summary: Module 1.5

- Cost is a deliberate variable. `/cost`, `/usage`, `/insights` are your dashboard.
- Pick the cheapest model and effort that gets the job done — escalate only when justified.
- For demanding tasks, the Plan/Implement/Review pipeline (Opus + Sonnet + Haiku) often beats Opus-only on both cost and quality.
- Always cap unattended sessions with `--max-budget-usd`.

See `session-plan.md` for workshop-wide cost estimates.

---

### Summary: Block 1 Key Takeaways

1. **Claude Code is an agent, not a chat tool.** It has real access to your filesystem, your git, your commands.
2. **The context window is finite.** CLAUDE.md and memory exist to persist what matters beyond a session.
3. **Specificity is everything in prompts.** Vague in → vague out. Contractor analogy: write a work order, not a wish.
4. **Git is built in.** Branch, commit, push, PR — all from conversation.
5. **Worktrees are your test lab.** Parallel branches, isolated environments, no stashing drama.
6. **Cost is a deliberate variable.** Model, effort, and budget caps decide what you spend — not the calendar.

---

*End of Block 1 Teaching Content*
