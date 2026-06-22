# Block 3: Advanced & Multi-Agent — Teaching Material

> **Audience:** Experienced programmers. Security analogies used throughout —
> especially relevant for the CySec engineer in the group.

### Feature Maturity Overview

| Symbol | Meaning |
|--------|---------|
| :white_check_mark: | **Stable** — Part of Claude Code, production-ready |
| :test_tube: | **Experimental** — Feature flag required, may change |
| :wrench: | **Custom** — Workshop-specific implementation |

| Feature | Status |
|---------|--------|
| Built-in Subagents (Explore, Plan, general-purpose) | :white_check_mark: |
| Custom Subagents | :white_check_mark: |
| `claude agents` CLI + Background-Sessions | :white_check_mark: |
| Git Worktrees | :white_check_mark: |
| `/loop`, `/goal`, `/schedule`, Routines | :white_check_mark: |
| Permission Modes (6 levels) | :white_check_mark: |
| Protected Paths (unconditional) | :white_check_mark: |
| `/security-review`, `/review`, `/ultrareview` | :white_check_mark: |
| OS-Level Sandboxing | :white_check_mark: |
| `claude remote-control` + `/teleport` | :white_check_mark: |
| `PushNotification` Tool | :white_check_mark: |
| Agent Teams | :test_tube: |
| Channels (MCP-Push) | :test_tube: |
| Codex Swarm (`multi-model-orchestrator`) | :wrench: |
| Devil's Advocate Debate Chain | :wrench: |
| Self-Improve Loop (`agentic-os`) | :wrench: |
| Telegram Bridge | :wrench: |

---

## Module 3.1: Agents & Multi-Agent Orchestration

**Learning Objectives:** After this module, you can:
- Define a custom subagent in YAML frontmatter (`name`, `description`, `tools`, `model`, `permissionMode`, `maxTurns`, `isolation`, `effort`) and explain the security restrictions that apply to plugin-shipped subagents.
- Pick the right orchestration pattern (Fan-Out/Fan-In, Pipeline, Hierarchical) for a given multi-agent task and quantify the speed gain versus sequential execution.
- Distinguish synchronous subagents (`Agent` tool) from background sessions (`claude --bg`, `claude agents`, `attach/logs/stop/respawn`) and know when to use each.

### What Is an Agent?

An agent is an **autonomous Claude instance** with a specific role, a specific set of tools,
and its own context window.  It is not a skill (a skill guides a single Claude instance).
An agent **spawns a separate Claude process** with its own permissions and focus.

Think about your access control infrastructure: you do not have one guard do everything —
monitor cameras, respond to alarms, manage card access, and write incident reports.
You have **specialized roles**.  Agents work the same way.

**Typical agent roles in a software project:**
- **Code Explorer** — reads and analyzes structure, finds patterns, understands the codebase
- **Code Reviewer** — reads changes, finds bugs, security issues, style violations
- **Implementer** — writes code, applies patches, creates files
- **Test Writer** — generates and runs tests, validates behavior
- **Security Auditor** — scans for vulnerabilities, injection flaws, secrets leaks

Each agent is good at its job because it is **not distracted** by anything else.

---

### Why Specialization Matters

A single Claude instance doing everything:
- Has a limited context window — long conversations degrade quality
- Can get confused by contradictory instructions across tasks
- Must context-switch, just like a human multitasking

Multiple specialized agents:
- Each starts fresh with a clean context tailored to its role
- Can work **in parallel** — massively faster on independent subtasks
- Output from one feeds cleanly into the next

**Security analogy:** Your SOC (Security Operations Center) dispatches teams.
Camera operators do not respond to physical intrusions.
Response teams do not configure card readers.
The SOC orchestrates — it does not do everything itself.

---

### The Agent Tool

Claude Code's built-in Agent tool launches subagents.  When Claude uses it:

1. Creates a new Claude instance
2. Passes it a role description, instructions, and tool permissions
3. Waits for results (or fires-and-forgets for parallel work)
4. Receives the output and uses it in the orchestrator's reasoning

Each subagent gets:
- Its own context window (blank slate, purpose-built)
- Specific tool allowances (Read, Write, Bash, or none)
- A focused task description

The orchestrating Claude stays at the top, aggregating results.

---

### Built-in Subagents (Ships with Claude Code)

Before defining custom subagents, Claude Code already provides three built-in ones you can invoke directly:

| Built-in | What it does | Typical Use-Case |
|---|---|---|
| **Explore** | Read-only scout — maps codebases, finds entry points, builds dependency graphs | "Map this repo before I start refactoring" |
| **Plan** | Strategic planner — produces multi-step implementation plans without writing code | "Plan how to migrate from Solid to React in 5 stages" |
| **general-purpose** | Multi-purpose worker — falls back to a balanced toolset when no specialized agent matches | Catch-all when you're not sure which custom agent fits |

Claude routes to these automatically when your prompt matches their job description (e.g., "explore the project structure" → Explore). You can also force one with `Agent(subagent_type="Explore", prompt=...)`. Most workshop demos focus on **custom subagents** below — but knowing the built-ins prevents you from reinventing scouts and planners.

---

### Agent Definition Anatomy

Agents are defined as YAML frontmatter + body text in `.md` files:

```yaml
---
name: code-explorer
description: >
  Analyzes codebases to understand structure, dependencies, and patterns.
  Use when you need: project overview, file map, dependency graph, entry points.
  Examples: "explore this project", "what does this codebase do", "map the architecture"
model: haiku
color: cyan
tools:
  - Read
  - Glob
  - Grep
permissionMode: default
maxTurns: 20
---

You are a code exploration specialist.  Your job is to understand, not to change.

When asked to explore a project:
1. Start with the directory structure
2. Read key files: README, main entry points, config
3. Map the dependency graph
4. Identify architectural patterns
5. Report clearly — structure, purpose, notable patterns, risks

Never modify files.  Never execute code.  Explore only.
```

**Key fields explained:**

- **`description`** — This is how the orchestrator decides *when* to use this agent.
  Write it with trigger phrases and examples.  This is the routing logic.
- **`model`** — Use shorthand `haiku` / `sonnet` / `opus`, or pin to a specific ID like
  `claude-haiku-4-5-20251001`, `claude-sonnet-4-6`, `claude-opus-4-7`. Haiku for quick reads,
  Sonnet for analysis, Opus for architecture decisions.
- **`tools`** — **Security through least privilege.**  An explorer has no Write.
  A reviewer has no Bash.  Lock down to exactly what is needed. (Field was renamed from
  `allowed_tools` — old YAML still parses as legacy alias but `tools` is canonical.)
- **`color`** — Visual differentiation in logs.  Matters for readability during parallel runs.

#### Full Frontmatter Reference (2026 Schema)

| Field | Type | Purpose |
|---|---|---|
| `name` | string | Unique agent identifier (used by orchestrator routing) |
| `description` | string | Trigger description — routing logic. Include examples. |
| `tools` | list | Allowlist of tools the agent may call |
| `disallowedTools` | list | Denylist — alternative to `tools`. Useful when "everything except X" is shorter than the allowlist. |
| `model` | string | `haiku` / `sonnet` / `opus` shorthand or full ID (`claude-opus-4-7`) |
| `permissionMode` | string | `default` / `acceptEdits` / `plan` / `auto` / `dontAsk` / `bypassPermissions` |
| `maxTurns` | int | Hard turn limit for this subagent (cost / runaway guard) |
| `skills` | list | Preload named skills into the subagent's startup context |
| `mcpServers` | list | Allowlist of MCP servers this subagent may connect to |
| `hooks` | object | Component-scoped hooks — only fire while this subagent runs |
| `memory` | string | `user` / `project` / `local` — gives the subagent its own persistent memory directory across sessions |
| `background` | bool | Always run this subagent as a background session |
| `isolation` | string | Set to `worktree` to spawn the subagent inside a temporary git worktree |
| `effort` | string | `low` / `high` / `xhigh` / `max` — reasoning effort cap |
| `color` | string | `cyan` / `magenta` / `yellow` / ... — log differentiation |
| `initialPrompt` | string | Auto-submitted first user turn (useful for `background: true` agents) |

**Plugin-Subagent Security Restriction:** Subagents shipped inside a *plugin* have **`hooks`, `mcpServers`, and `permissionMode` silently ignored**. The host system refuses to let a guest plugin escalate its own permission level, attach hooks the user did not opt into, or pull in undisclosed MCP servers. Security analogy: a contractor walking into your facility cannot set their own badge level or rewrite the standing orders. Plugin authors must request elevated capabilities through the install manifest — not through the agent frontmatter.

#### Inline Subagent Definition via `--agents`

For scripted CI pipelines you can skip the file system entirely and define a subagent inline as JSON:

```bash
claude --agents '[{"name":"reviewer","model":"sonnet","tools":["Read","Grep"],"permissionMode":"default"}]' \
       -p "Review the latest diff and report any security concerns."
```

Useful when the CI runner does not own a persistent `.claude/agents/` directory or when you want to keep the subagent definition versioned alongside the workflow YAML.

---

### Orchestration Patterns

#### Pattern 1: Fan-Out / Fan-In

Launch N agents in parallel, collect all results, synthesize.

```
Orchestrator
  |-> Agent A (Task 1) -> Result A -+
  |-> Agent B (Task 2) -> Result B -+-> Synthesize -> Final Output
  `-> Agent C (Task 3) -> Result C -+
```

**Use when:** Tasks are independent.  Analyzing 3 modules.  Running scans on 5 files simultaneously.

**Speed gain:** Each task takes 60 seconds.  3 sequential = 180s.  3 parallel = ~60s.  **3x faster.**

#### Pattern 2: Pipeline (Sequential)

Output of Agent A becomes input of Agent B.

```
Orchestrator -> Agent A (Explore) -> Agent B (Review) -> Agent C (Fix)
```

**Use when:** Each step depends on the previous.  Plan -> Implement -> Test -> Review.

#### Pattern 3: Hierarchical

Orchestrator spawns sub-orchestrators, each managing their own agents.

```
Master Orchestrator
  |-> Sub-Orchestrator 1 (Security)
  |     |-> Scanner Agent
  |     `-> Validator Agent
  `-> Sub-Orchestrator 2 (Quality)
        |-> Reviewer Agent
        `-> Test Writer Agent
```

**Use when:** Problem requires decomposition at multiple levels.  Enterprise-scale codebases.

---

### Quick-Start: Triggering Multi-Agent Work

Tell Claude:

> "Analyze this project from two angles simultaneously: one agent maps the architecture,
> another finds all TODO and FIXME comments.  Run them in parallel and give me a combined report."

Claude will use the Agent tool to do exactly that.
The skill `/agent-orchestrator` automates the full orchestration workflow.

### `/batch` — Multi-Agent Worktree Use-Case (Recap)

`/batch` was introduced in Module 2.1 as a bundled skill — fanning a task across isolated worktrees with one subagent per worktree. Here is one concrete multi-agent application:

```
/batch migrate src/components/* from Solid to React, one module per worktree
```

Five files → five worktrees → five Sonnet subagents in parallel → five PRs at the end. Aggregate runtime: the slowest subagent, not the sum. See Module 2.1 for the full `/batch` mechanics; in Block 3 we treat it as one orchestration primitive among many.

### `/tasks` — Background Task Management

Use `/tasks` (alias `/bashes`) to see all running background tasks in your session. When you spawn parallel agents or long-running operations, this is your dashboard.

### Agent Teams (Experimental)

Beyond subagents (which are one-shot workers), Claude Code supports **Agent Teams** — multi-session coordination where agents can communicate with each other:

```
TeamCreate — create a new teammate agent (e.g., reviewer, QA, docs writer)
SendMessage — send messages between team members
```

Each teammate runs as a **separate session** with its own context window. They can:
- Work on different parts of a task in parallel
- Send findings to each other
- The lead agent synthesizes results

**Cost warning:** Token cost scales linearly per teammate. Each idle teammate still consumes tokens. Use Sonnet for teammates, keep teams small, clean up after completion.

**Security analogy:** A full SOC team — lead operator, camera monitor, patrol dispatcher, incident reporter. Each has their own workstation (context), their own radio channel (SendMessage), and their own access level (tools). The lead operator (orchestrator) coordinates.

---

### Background Agents (`claude agents`)

Since v2.1.139 Claude Code ships a dedicated subsystem for **long-running background sessions**: tasks you fire off and walk away from. Build watchers, CI monitors, generation pipelines that run for hours — your laptop lid can close, the session keeps going server-side.

**Starting a background session:**

```bash
claude --bg "Generate API documentation for every public function in src/api/"
claude --bg --from-pr 1234     # Resume an open PR review in the background
```

The `--bg` flag detaches Claude immediately and returns a session ID. You can also detach a running interactive session with `/background` (alias `/bg`).

**The `claude agents` Live-View:**

```bash
claude agents      # Opens the background-sessions monitor — every active patrol on one screen
```

From inside the live-view you reach each session with these subcommands:

| Subcommand | What it does |
|---|---|
| `claude attach <id>` | Hop into the running session as if it were yours |
| `claude logs <id>` | Stream stdout/stderr from the session |
| `claude stop <id>` | End the session gracefully (saves transcript) |
| `claude respawn <id>` | Restart the session with the same prompt + context |
| `claude rm <id>` | Remove the session record after it has stopped |

Plus `claude daemon status` for a quick health check of the background-session supervisor itself (helpful when sessions appear stuck).

**Security analogy:** Think of `claude agents` as the **watch-commander's shift roster**. Every patrol that is currently out is one line on the board. You can radio in to any of them (`attach`), pull their bodycam stream (`logs`), recall one (`stop`), send the same patrol out again (`respawn`), or strike a finished entry from the roster (`rm`). The board itself never sleeps — that is what `claude daemon status` checks on.

**Typical use-cases:**
- **Build watch:** `claude --bg "Watch for npm test failures and propose minimal patches"` — runs until you stop it.
- **PR babysitter:** `claude --bg --from-pr 1234` — resumes a PR review every time CI re-runs.
- **Doc generation:** `claude --bg "Generate JSDoc for every function in src/, commit per file"` — runs for hours, you check in via `attach` when convenient.

**Comparison with subagents:** A subagent (via `Agent` tool) is *synchronous* inside one orchestrator's turn. A background agent (via `claude --bg`) is a **standalone session** that outlives your terminal. Pick subagents for fan-out within a task, background agents for "fire and forget for the next 4 hours."

---

## Module 3.2: Nested Orchestration & Multi-Model Pipelines

**Learning Objectives:** After this module, you can:
- Map task phases (plan / implement / review) to the right model (Opus / Sonnet / Haiku / Codex) and justify the choice from cost and judgement perspectives.
- Identify the data-flow boundary in a Claude-Codex pipeline (which provider sees which code) and choose between skip-Codex, local-model substitution, or signature-only stripping for sensitive code.
- Use a multi-model pipeline (e.g. Codex Swarm with `--decompose`) for parallel implementation and aggregate the results via Claude review.

### Different Models, Different Strengths

| Model | Strengths | Best Used For |
|---|---|---|
| **Claude Opus** | Deep reasoning, architecture, judgment | Planning, review, quality decisions |
| **Claude Sonnet** | Fast, capable, good at most tasks | General implementation, analysis |
| **Claude Haiku** | Very fast, cheap, focused | Bulk processing, simple reads, brainstorming |
| **Codex (OpenAI)** | Fast code generation, different training | Implementation, second opinion |

Key insight: **Codex generates code fast and cheap.  Claude Opus reviews with high judgment.**
Using both together beats either alone.

---

### Cost Trade-Off — Order-of-Magnitude Multipliers

> Full pricing table and the Plan/Implement/Review cost strategy live in **Module 1.5 (Cost Engineering)** — single source of truth. Rough orientation for this module: Opus ~3x Sonnet, Haiku ~0.2x Sonnet (per MTok).

**Mini-Strategy for a typical Claude → Codex → Claude pipeline:**

- **Plan with Opus** — one expensive call buys a clean spec; bad plans are 10x more costly downstream.
- **Implement with Sonnet** (or Codex when speed beats determinism) — the bulk of the tokens flow here.
- **Review with Haiku first**, escalate disagreements to Opus — Haiku catches 80% of issues at ~7% of Opus cost.

A 1000-token spec reviewed by Opus is ~$0.025. The same review by Haiku is ~$0.005. Across 200 PRs per month, that compounds.

---

### Data Flow — What Goes Where?

> **Important for security-sensitive audiences:** A Codex Swarm sends your source code to **OpenAI**, not Anthropic. Anthropic's data policies (Block 3.3 retention table) cover only the Claude side of the pipeline. OpenAI has its own retention and training policies, governed by your OpenAI Codex agreement.

If your codebase is sensitive (customer PII, proprietary firmware, contracted exclusivity), you have three options:

1. **Skip the Codex step** — let Sonnet handle the bulk implementation; cost goes up slightly, data stays inside Anthropic's contract.
2. **Use a local model** for the Codex slot (Ollama / vLLM with a Code-Llama variant) — same role, no third party.
3. **Strip sensitive parts before sending** — refactor the prompt so Codex only sees skeleton signatures, not identifiers or business logic.

The orchestration patterns in this module are model-agnostic — the same Plan → Implement → Review pipeline works with any pair of providers.

---

### The Claude -> Codex -> Claude Pipeline

**Phase 1: Claude Opus Plans**
- Analyzes requirements, designs architecture
- Breaks task into clear, unambiguous implementation tickets
- Writes detailed specs for each ticket

**Phase 2: Codex Implements (Fast, Parallel)**
- Receives specs from Phase 1
- Generates code — fast, no hesitation
- Multiple Codex agents work on different tickets simultaneously

**Phase 3: Claude Opus Reviews**
- Reads all generated code
- Checks against original requirements
- Finds bugs, security issues, spec violations
- Decides: accept, request changes, or reject

**Why this works:**
- Opus is expensive but used only where judgment matters — plan and review
- Codex handles the mechanical generation — cheap, fast, parallel
- Two AI systems have different blind spots.  What one misses, the other catches.

**Security analogy:** Senior architect writes the spec.
Contractors install hardware in parallel.
Senior engineer inspects every door, every reader, every cable run before sign-off.

---

### Codex Swarm

> **:wrench: Custom Component:** `multi-model-orchestrator` is a custom plugin, not part of Claude Code.

```
/multi-model-orchestrator:codex-swarm --decompose "Build a Python CLI with scan, check, report commands"
```

With `--decompose`:
1. Claude analyzes the task and breaks it into N independent subtasks
2. N Codex agents spawn in parallel, one per subtask
3. All work simultaneously — total time is the slowest agent, not the sum
4. Claude reviews all results together, catches integration issues

**When to use Codex Swarm:**
- Large, parallelizable implementation tasks
- You want a second opinion from a different AI model
- Speed matters more than cost per token
- Tasks are well-specified and mechanical

---

### Practical Example: Security CLI Tool

Task: "Build a Python security CLI with three commands:
- `scan` — lists open ports on a given host
- `check` — verifies a URL returns HTTP 200
- `report` — generates a JSON security report"

With `--decompose`, Claude might decompose into:
1. Agent 1: CLI framework + scan command (socket-based port enumeration)
2. Agent 2: check command (HTTP request, timeout handling, status validation)
3. Agent 3: report command (JSON output, aggregates results)
4. Agent 4: Test suite for all three commands

All 4 Codex agents run simultaneously.  Claude reviews the assembled result.

---

## Module 3.3: Security & Adversarial Testing

**Learning Objectives:** After this module, you can:
- Walk through the 4 stages of a Devil's Advocate pipeline (Scanners → Debate → Consensus → Fixers) and explain why overlap and adversarial debate reduce (but do not eliminate) false positives.
- Compare the built-in review trio (`/security-review`, `/review`, `/ultrareview`) against custom adversarial pipelines and pick the right tool for a given audit scenario.
- Apply the right combination of permission modes, protected paths, sandbox-level network hardening (`sandbox.network.deniedDomains`, `autoMode.hard_deny`), and skill-shell hardening (`disableSkillShellExecution`) for autonomous workflows.

> **Note to moderator:** Frame this as automated penetration testing with a trial system.
> Because that is literally what it is.  The CySec person will feel very at home.

### The Devil's Advocate Swarms Pipeline

A **multi-agent adversarial system** for finding and fixing security and quality issues.
It mirrors real professional security review — with one difference: it runs automatically.

**Four stages:**

---

#### Stage 1: Scanners

Multiple scanner agents analyze code simultaneously from different angles:

- **Security Scanner** — injection flaws, hardcoded credentials, unsafe patterns, missing auth
- **Quality Scanner** — error handling gaps, missing input validation, unsafe type assumptions
- **Architecture Scanner** — trust boundary violations, privilege escalation paths, data flow risks

**Why multiple scanners with overlap?**

Two scanners finding the same issue = high confidence it is real.
One finding something the other misses = investigate carefully.

Overlap is validation through consensus.
This is exactly how you run a physical security audit: two independent teams,
compare findings, overlapping results are high-confidence.

---

#### Stage 2: Debate

For each finding, two agents argue:

**Prosecutor** presents the attack scenario:
> "An attacker can inject arbitrary commands through the search parameter.
> The input reaches a shell call with no sanitization.
> Here is a proof-of-concept payload."

**Defender** challenges the finding:
> "Input is validated against a whitelist of allowed characters before it reaches that code path.
> The validation rejects all shell metacharacters.
> This is not exploitable as written."

The debate **reduces** false positives — it does not eliminate them.
Traditional security tooling commonly reports 30-50% false positive rates;
the debate stage is designed to filter many of those before any engineer
looks at them, but the actual reduction depends on prompt quality, scanner
choice, and codebase characteristics. We have not benchmarked it against
a labeled dataset. Treat it as **"a useful adversarial filter, not a
guaranteed false-positive eliminator."**

The Prosecutor's job: argue every finding as if writing an exploit report for a paying client.
The Defender's job: find every reason the finding is not actually exploitable.

A finding survives only if the Prosecutor wins convincingly.

---

#### Stage 3: Consensus

A consensus agent reviews the full debate and decides:
- **CONFIRMED** — real vulnerability, promote to fix queue
- **FALSE POSITIVE** — not exploitable in context, discard with explanation
- **NEEDS INVESTIGATION** — ambiguous, flag for human review

Only CONFIRMED findings proceed.  Everything else is logged — your audit trail.

---

#### Stage 4: Fixers

For each confirmed finding, a fixer agent:
- Reads the exact finding and full debate context
- Implements the **minimal targeted fix** — no refactoring, no scope creep
- Writes a regression test that would have caught the vulnerability
- Documents why the fix is correct

**The security analogy, complete:**
- Prosecutor = pentester writing the exploit report
- Defender = developer explaining what was and was not exploitable
- Consensus = security manager deciding what gets patched
- Fixers = patching team
- The whole process runs autonomously, with full documentation

> **Domain Note:** The workshop has two playgrounds — `access_control.py` (Python, user-management)
> and `osdp_frame_decoder.c` (C, embedded OSDP frame parser). For Physical-Security / Embedded
> audiences, the C playground demonstrates memory-safety vulnerabilities (buffer overflow,
> integer overflow, format string) that are typical of firmware. The Python playground covers
> backend-style vulnerabilities. Use whichever matches the audience.

---

### Security Audit Skill

The `/security-audit` skill provides automated scanning for any project receiving external input.

**What it checks:**

| Check | What It Finds |
|---|---|
| Command injection | Shell calls built from unvalidated external input |
| SQL injection | Queries built by string concatenation with user data |
| Hardcoded credentials | Passwords, API keys, tokens in source files |
| Unsafe deserialization | Loading serialized objects from untrusted sources |
| Open redirects | Redirect targets controlled by user-supplied input |
| Missing authentication | Endpoints reachable without auth check |
| Supply chain risks | Dependencies with known CVEs, unpinned versions |
| Missing input validation | External parameters used without sanitization |

Runs in minutes.  Integrates into CI/CD pipelines.

---

### Permission Modes — Going Deeper

> **See Module 1.1 for the 6 modes overview** — the full table (default / acceptEdits / plan / auto / dontAsk / bypassPermissions) lives there. This module skips the recap and dives only into the **advanced modes** (`auto`, `dontAsk`, `bypassPermissions`) and their CI/CD patterns.

#### `auto` Mode — Plan Availability & Restrictions

`auto` is the ML-classifier-driven mode where Claude itself decides which actions to auto-approve based on per-action risk:

- **Max plan (consumer)** — available **with Opus 4.7 only** (other models locked).
- **Team / Enterprise** — available with Sonnet 4.6 and Opus 4.7.
- **Transport** — Anthropic API only (not yet on Bedrock or Vertex).
- **Version** — requires Claude Code v2.1.83 or later.

Admins on Team/Enterprise can tighten or loosen `auto` via managed settings — see `autoMode.hard_deny` below for the unconditional block-list.

#### `acceptEdits` — Wider Than It Looks

The Block 1 table summarizes `acceptEdits` as "reads + file edits allowed, bash still asks." That is the conservative version of the truth. In current Claude Code releases, `acceptEdits` also **auto-approves the common filesystem Bash commands** that are functionally equivalent to file edits — within the working directory and any `--add-dir` paths:

| Platform | Auto-approved under `acceptEdits` |
|---|---|
| Linux / macOS / WSL | `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed` (in-place) |
| Windows (PowerShell) | `Set-Content`, `Add-Content`, `Clear-Content`, `Remove-Item` |

Anything *outside* the working directory still triggers the normal prompt. Network calls (`curl`, `wget`), package managers (`npm install`, `pip`), and arbitrary shell scripts are **not** auto-approved — they still ask.

**Why this matters:** When you cycle into `acceptEdits` for a long refactor, expect Claude to silently `mv` and `rm` files inside the project as part of normal work. That is by design. If your project has a directory layout that should remain stable (generated artifacts, vendored libraries), put it on the deny list explicitly.

#### CI/CD pattern — Headless `dontAsk`

The `dontAsk` mode is the workhorse for CI runners: Claude works through allow/deny rules without ever prompting.

```bash
claude --permission-mode dontAsk \
  --allowedTools "Read,Glob,Grep,Bash(npm test)" \
  --output-format json \
  -p "Run the test suite and emit a structured failure report."
```

Tips for CI: pair `--permission-mode dontAsk` with `--max-budget-usd` and `--max-turns` as a hard cost/loop cap (see Module 3.4), and use a long-lived OAuth token from `claude setup-token` so the runner never prompts for re-auth.

#### `bypassPermissions` — When You Actually Need It

`bypassPermissions` (via `--dangerously-skip-permissions`) really does mean *everything*. Claude Code refuses to start as root/sudo on Linux/macOS outside a recognized sandbox precisely because this mode is meant for ephemeral throwaway containers. Use it inside Inception/Docker, never on a live workstation.

---

### Protected Paths — What Claude *Refuses* to Touch

Even in `bypassPermissions` Claude Code maintains an **unconditional protection list**. These paths cannot be written to without an explicit override flag, no matter how broad the permission mode:

**Protected Directories:**

- `.git` — your version control state
- `.vscode`, `.idea`, `.husky` — IDE / git-hook configurations
- `.claude` — **except** four allowlisted sub-paths: `.claude/commands`, `.claude/agents`, `.claude/skills`, `.claude/worktrees` (these are user-authored content; the rest of `.claude/` is system state)

**Protected Files:**

- `.gitconfig`, `.gitmodules`
- `.bashrc`, `.zshrc`, `.profile` — your shell startup
- `.ripgreprc`
- `.mcp.json`, `.claude.json` — Claude Code's own configuration

**Why this exists:** Even an `auto`-mode classifier that decides "low-risk Bash command" cannot accidentally trigger a `git config` rewrite, a `.bashrc` poison-pill, or a self-modification of `.mcp.json`. The protection is hard-coded in the host process, not enforced via the permission rules.

**Security analogy:** This is the **vault room the building owner cannot enter on their own keycard**. Even the master key has carve-outs for the data center, the safe deposit boxes, and the IT closet. Protected Paths are Claude Code's hardcoded carve-outs from the master-key.

---

### Built-in Code-Review Trio

Three official slash-commands cover the common review surface — before reaching for the custom Devil's Advocate Swarms:

| Command | Where it runs | What it does |
|---|---|---|
| **`/security-review`** | Local | Scans the current branch diff for vulnerabilities (injection, auth gaps, supply chain). Same scope as the security-audit skill, but built in. |
| **`/review [PR]`** | Local | Pulls an open PR (or current branch) and runs a balanced quality review (correctness, style, tests). |
| **`/ultrareview [PR]`** | Cloud | Spawns a **cloud-based multi-agent review pipeline** (Anthropic-hosted) — multiple reviewers in parallel, consensus aggregation. Anthropic's official answer to the Devil's-Advocate-Swarm pattern. |

**Built-in vs. Custom — Quick comparison:**

| Aspect | Built-in (`/security-review`, `/review`, `/ultrareview`) | Custom (Devil's Advocate Swarms) |
|---|---|---|
| Setup | Zero — ships with Claude Code | :wrench: requires custom plugin install |
| Granularity | Anthropic-tuned defaults | Per-stage agent configuration, model choice, prompts |
| Cost transparency | Wrapped in `/cost` | Visible per-agent in plugin logs |
| Audit trail | Built-in transcript | Custom log files in `.agent-memory/` |
| Best for | "Quick second opinion, low effort" | Tailored audits with domain-specific scanners |

**Recommendation for the workshop audience:** Start with the built-ins (`/security-review` on every branch before merge, `/ultrareview` on high-stakes PRs). Reach for Devil's Advocate Swarms when you need a *specific* combination of scanners, a particular debate model, or domain-tuned prompts.

---

### Permission Rules — Beyond Allow/Deny on Bash

The familiar `Bash(rm *)` pattern is only one rule family. The full permission-rule grammar covers tools, skills, agents, and outbound network reach:

| Rule Pattern | Effect |
|---|---|
| `Bash(rm *)` | Allow/deny matching shell invocations |
| `Skill(<name>)` | Allow or block a named skill (e.g., `Skill(commit)`) |
| `Skill(<name> *)` | Wildcard for a skill family (`Skill(agentic-os *)`) |
| `Agent(<agent-type>)` | Block or allow a specific subagent type — useful for managed environments that want to lock down which agents may be invoked |
| `WebFetch(domain:example.com)` | Restrict outbound web fetches to specific domains (or block specific ones) |
| `permissions.ask` rule | Always prompts the user — even in `auto` or `dontAsk` mode. The hard-stop override for "this one tool really should be human-confirmed." |

Use these in your project `settings.json` to enforce policy without depending on the user picking the right mode at runtime.

---

### Sandbox-Level Network Hardening

Two settings let you tighten the network surface within sandboxed bash:

- **`sandbox.network.deniedDomains`** — Even if the broader allow-list permits outbound traffic, listed domains are blocked outright. Use-case: "Yes, allow network, but never reach `evil.com` or the legacy on-prem corp endpoint that should be retired."
- **`autoMode.hard_deny`** — Unconditional block-list for `auto` mode, overrides Claude's classifier. Use-case: "`auto` mode may never touch the production database tooling, regardless of how confidently the classifier says it is safe."

Both live in `settings.json` (project or managed scope) — perfect for Enterprise admins who want to restrict `auto` without disabling it entirely.

---

### Hardening Skill Execution — `disableSkillShellExecution`

Skills support inline shell execution via `` !`command` `` (dynamic context injection — see Module 2.1). In managed/Enterprise environments this can be undesirable: an attacker who can push a skill could trigger shell commands at skill-load time.

Set `disableSkillShellExecution: true` in your managed settings to **disable the `` !`...` `` syntax globally**. Skills continue to work as static prompts; they just lose the dynamic-injection capability. Pair it with `permissions.allow` for explicitly approved skills if you still want some skill autonomy.

---

### Sandboxing Options

Claude Code offers multiple levels of isolation. Understanding these layers is critical for running autonomous agents safely.

**Level 0: OS-Level Sandbox (Built-in)**

Claude Code has native OS-level sandboxing for shell tools:

| Platform | Tool | Technology | What it restricts |
|----------|---|-----------|------------------|
| macOS | `Bash` | Seatbelt profiles | Filesystem paths, network access |
| Linux/WSL2 | `Bash` | bubblewrap (bwrap) | Filesystem paths, network access |
| Windows | `PowerShell` | Native PowerShell tool — runs with the host permission system + Bash-compatible permission rules. Not a kernel sandbox, but a first-class shell path rather than a fallback. |  |

Toggle with `/sandbox` in session. Applies to `Bash`/`PowerShell` + child processes only (not to Read/Write/Edit tools). Anthropic claims this reduces permission prompts by ~84% — note this is a **vendor figure, not an independent benchmark**. Your mileage will vary by workflow.

**Level 1: Git Worktrees (Lightweight)**

Separate working directory, same filesystem.
Protects main branch from agent mistakes.
Near-zero overhead. Use `claude --worktree` or `/batch`.

**Level 2: Docker / Inception (Full OS-Level)**

Separate filesystem, separate network, separate process space.
Run generated code without risk to host.
`multi-model-orchestrator:inception` (:wrench: custom plugin) automates setup and cleanup.

**Level 3: Remote Sandboxes**

Full VM per agent.  Complete network isolation.
For analyzing genuinely dangerous code samples.

### Data Retention & Privacy

Understanding data handling is essential for enterprise deployment and compliance:

| Plan | Training on your data? | Retention period | Notes |
|------|----------------------|-----------------|-------|
| **Free/Pro/Max** | Opt-in | Opt-in: 5 years, Opt-out: 30 days | Consumer plans |
| **Team/Enterprise** | No (by default) | 30 days | Commercial plans |
| **Enterprise + ZDR** | No | 0 days | Zero Data Retention (some features disabled) |

**Telemetry opt-out:**
```bash
export DISABLE_TELEMETRY=1           # No operational metrics (Statsig)
export DISABLE_ERROR_REPORTING=1     # No error logging (Sentry)
```

**Network:** Prompts and outputs are transmitted via TLS. According to docs, data is "not encrypted at rest."

**Security analogy:** This is like your CCTV retention policy. Consumer = 30-day loop with opt-in archive. Enterprise = 30-day loop, no sharing. ZDR = cameras on but no recording — maximum privacy, but you lose playback capability.

### Regulated Industries: Compliance Notes

Different industries — and different jurisdictions — impose different rules on what you can and cannot automate. The workshop covers HIPAA (US Healthcare) as Bonus Exercise 3.8 because the *mechanism* (regex-based PreToolUse guardrails) generalizes. Here is a quick map of the regulations most relevant to this audience:

| Industry / Region | Key Regulation | Implications for Claude Code |
|---|---|---|
| **EU Physical Security** | EN 50131 (intrusion alarms), EN 50132 (CCTV) | Autonomous firmware updates on alarm/access controllers NOT allowed — require human approval gate + audit trail. Avoid Auto-Memory drift on firmware code (Module 3.7). |
| **EU General** | GDPR | Personal data in access logs / video metadata -> Auto-Memory may pull PII into prompts. Use `--bare` for sensitive runs. ZDR (Enterprise) for production data flows. Disclose Anthropic as a data processor in your DPA. |
| **US Healthcare** | HIPAA | PHI must not leave your control. ZDR strongly recommended. See Bonus Exercise 3.8. BAA with Anthropic required for production PHI use. |
| **US Financial** | PCI-DSS | Card data in test fixtures or logs -> block via PreToolUse hook (same pattern as Exercise 3.8) + `WebFetch(domain:...)` allowlist. |
| **EU Financial** | DORA, MiFID II | Audit trail mandatory. Pair Auto-Memory + transcript export for traceable reasoning. Reject `/autofix-pr` on regulated-system PRs without human review. |
| **EU Industrial / Critical Infrastructure** | NIS2 Directive | Critical infrastructure operators -> require human approval gates in any automation loop. Document the Claude Code data flow in your NIS2 risk assessment. |

**General principles for regulated work:**

1. **Disable Auto-Memory for sensitive sessions** with `--bare` (Module 3.6). No accidental PII persistence.
2. **Use ZDR (Zero Data Retention) plans** where the regulatory text demands no retention by the processor (HIPAA + BAA, some GDPR interpretations, ZDR-bound government contracts).
3. **Audit trail discipline** — Git commits with clear author attribution; never let `/autofix-pr` push to protected branches; archive transcripts for the regulator's retention window.
4. **Data flow disclosure to your DPO** — Anthropic for Claude (`api.anthropic.com` or Bedrock/Vertex tenant), OpenAI for Codex if you wire it in (Module 3.2 data-flow caveat), Google for NotebookLM. Each is a separate processor relationship.
5. **Permission rule `WebFetch(domain:...)`** — restrict outbound HTTP to approved domains. Block accidental egress to scraping-aggregator APIs.
6. **Sandbox network with `sandbox.network.deniedDomains`** — block accidental egress at the sandbox layer (above in this module).

**Caveat:** Each company's interpretation of these regulations varies, and national authorities (BfDI in DE, CNIL in FR, ICO in UK) sometimes diverge from each other. The workshop provides patterns; **your compliance officer interprets them for your context**. When in doubt, opt for the more conservative path — human approval gates, ZDR, `--bare`.

---

### Known Vulnerabilities (Teaching Examples)

Real CVEs relevant to understanding the security model:

- **CVE-2025-53110:** Path traversal in MCP server validation. The `startsWith()` check could be bypassed with `../` sequences. Fixed with strict path normalization. Lesson: never trust simple string matching for path validation.

  > **Currency note (2026-05):** The CVE-2025-53110 record is no longer surfaced as a headline example in the current Claude Code docs in this exact form. The **pattern it teaches** — MCP path validation done by string prefix matching rather than canonicalization — remains directly relevant; see Module 2.4's MCP Security section.

- **Supply chain risk (research paper, March 2026):** Academic analysis of agent skill marketplaces found abandoned repos that could be hijacked, injecting malicious skills into unsuspecting users' environments.

These are excellent teaching examples for your security-focused audience — real-world demonstrations of why the permission system and plugin vetting matter.

---

### Trust Boundaries in Practice

| Boundary | Mechanism | What It Prevents |
|---|---|---|
| Tool permissions | `tools` / `disallowedTools` in agent definition | Explorer cannot modify files |
| Filesystem | Worktree isolation | Agent cannot touch main branch |
| Path protection | Protected Paths (hardcoded) | `.git`, shell configs, `.mcp.json` cannot be rewritten |
| OS-level | Docker / Inception | Agent cannot reach host filesystem |
| Process | Hooks blocking actions | Specific commands blocked entirely |
| Network | Docker network none + `sandbox.network.deniedDomains` | Agent cannot make outbound connections / cannot reach blocked domains |

The principle of least privilege applies to agents exactly as it applies to user accounts.
This is not optional hardening — it is the default design.

---

## Module 3.4: Scheduled Tasks, Loops & Automation

**Learning Objectives:** After this module, you can:
- Distinguish `/loop`, `/goal`, `/schedule`, and routines and pick the right primitive for time-based vs. condition-driven vs. persistent recurring tasks.
- Pair every autonomous loop with `--max-budget-usd` and `--max-turns` and use `--worktree` to scope scheduled tasks to a dedicated branch.
- Explain when to reach for a self-improve loop (with safety mechanisms: quality gates, hooks, max iterations) and recognize the failure modes (cost runaway, false fixes, memory drift).

### Cronjobs with `/schedule`

Remote agents that run on cron schedules — even when your laptop is closed.

The `/schedule` skill walks you through:
1. What task to run (skill, command, or custom prompt)
2. When to run it (cron syntax or natural language: "every day at 8am")
3. What context to pass

**Practical scheduled tasks:**

| Task | Schedule | What It Does |
|---|---|---|
| Quality gate | Daily 06:00 | Test suite and code review on main branch |
| Security scan | Daily 02:00 | Devil's Advocate swarm on changed files |
| Dependency check | Weekly Monday | Scan all dependencies for new CVEs |
| Credential scan | Every commit | Detect accidentally committed secrets |
| Performance regression | After every deploy | Compare response times to baseline |

---

### Loops with `/loop`

Runs a command on a recurring interval in your current session:

```
/loop 5m /quality-gate
```

Runs the quality gate every 5 minutes.  Useful during active development.

**Loops vs. Schedules:**
- **Loops:** live in your terminal, stop when you close the session
- **Schedules:** persist across sessions, fire even when you are offline

---

### `/goal` — Native Condition-Driven Loops

`/goal` is the **native alternative to `/loop`** for tasks that have a clear stop-condition rather than a fixed interval. Claude works across as many turns as needed until the condition is met.

```
/goal Tests grün
/goal All TypeScript errors resolved
/goal No more TODO comments in src/api/
```

While running, a live overlay shows **elapsed time / turns used / tokens spent** — you can abort or adjust in flight. Useful when you want autonomous progress *up to a goal*, not just for a fixed duration.

**`/goal` vs `/loop`:**

| | `/loop` | `/goal` |
|---|---|---|
| Stop condition | Time-based (interval) or manual stop | Logical condition met |
| Use-case | "Re-check every 5 min while I work" | "Get to green tests, then stop" |
| Cost shape | Predictable per interval | Open-ended — pair with `--max-budget-usd` |

---

### Routines — Persistent Scheduled Agents

For recurring tasks that must survive across sessions, **Routines** are the official `/schedule` companion (`code.claude.com/docs/en/routines`). A routine is essentially a saved `/schedule` entry with first-class lifecycle (create, list, pause, resume).

**Typical routine use-cases:**

- **Daily build report** — runs every morning at 06:00, summarizes overnight CI, posts to Slack via MCP.
- **Nightly codebase audit** — Devil's Advocate Swarm on the diff merged that day.
- **Weekly dependency review** — `npm audit` + Claude triage of new CVEs.

Routines vs. ad-hoc `/schedule`: `/schedule` creates one entry; routines are the long-lived management surface around them.

---

### `--max-budget-usd` — Safety Net for Autonomous Loops

Both `/loop` and `/agentic-os:run-loop` can burn tokens in a tight cycle if a tool keeps returning failures and Claude keeps retrying. The **hard cost cap** lives at the CLI level:

```bash
claude --max-budget-usd 5.00 -p "/loop 10m /quality-gate"
claude --max-budget-usd 2.00 --max-turns 20 -p "/goal Tests grün"
```

When the cap is hit, Claude stops gracefully and reports the budget exhaustion. Always pair autonomous loops with a budget — it is the difference between a $5 lesson and a $500 surprise.

---

### Worktree-Scoped Scheduled Tasks

Both `/schedule` and `/loop` accept the `--worktree` flag (see Module 3.5 for the worktree mechanics). The scheduled session then runs in its own branch directory — leaving your main working tree completely untouched.

```bash
# Nightly audit on a dedicated branch; main branch untouched
claude --worktree audit/nightly --max-budget-usd 1.00 -p "/loop 24h /security-audit"

# Routine that lives entirely on its own branch
claude --worktree routines/daily-build-report -p "/schedule daily 06:00 ..."
```

**Use case:** Background-audit loops, scheduled refactoring experiments, or any autonomous job that writes files but should not interrupt your interactive work on `main`. The worktree gives the scheduled session a fresh ref (controlled by `worktree.baseRef`, see Module 3.5), an independent file state, and a clean merge surface.

---

### Channels — Official Push-Inbox into a Live Session

Block 3.5 shows the **Telegram Bridge** as a :wrench: custom pattern: outside world pushes messages into a Claude session. The **official equivalent is Channels** — MCP servers can push messages directly into a running Claude Code session (research-preview status today). Same pattern, no custom bridge code, audit-logged via the MCP layer. We will treat the Telegram Bridge as a teaching example for the pattern, but in production you would reach for Channels first.

---

### Self-Improve Loops

> **:wrench: Custom Component:** `agentic-os` is a custom plugin, not part of Claude Code.

The `/agentic-os:run-loop` skill implements **autonomous self-improvement cycles**.

**Each iteration:**

1. **Analysis** — reads quality metrics, test failures, review findings, iteration history
2. **Planning** — designs a targeted fix for the highest-impact weakness
3. **TDD Implementation** — writes failing test first, then code to pass it
4. **Quality Gate** — tests pass?  Quality above threshold?  No regressions?
5. **Commit (only if gate passes)** — git commit with detailed iteration log
6. **Repeat** — next iteration starts with updated state

**Safety mechanisms:**

| Mechanism | What It Does |
|---|---|
| Quality Gates | Refuses to commit if tests fail or quality drops |
| Git history | Every iteration is a reversible commit |
| Hooks | Block specific dangerous operations |
| Human review gates | Pause and wait for approval before committing |
| Max iterations | Cap autonomous runs per session |

**The Agentic OS memory system records everything:**
- `.agent-memory/iterations/` — full log of every change and decision
- `.agent-memory/quality/` — quality scores over time
- `.agent-memory/learnings/` — patterns identified across runs

**Honest assessment:** In internal testing on small Python projects with
clear test suites, the loop has produced incremental fixes without obvious
regressions over several iterations — but this is anecdotal, not published
benchmark data. Don't take it as a guaranteed productivity gain. Treat the
Self-Improve Loop as **"experimental tool, useful when carefully bounded
with budget caps and quality gates."**

**What can go wrong with Self-Improve Loops:**

- **Cost runaway** — without `--max-budget-usd`, a stuck loop can burn $50+ in an hour
- **False fixes** — Claude can "fix" a test by removing the assertion. Pair with strict pre-commit hooks.
- **Memory drift** — the memory system can persist wrong conclusions; periodic cleanup needed
- **Over-confidence in small samples** — a handful of successful runs on toy code does not generalize to production

**Security analogy:** Your access control system runs overnight diagnostics.
It detects a door reader responding 300ms slower than baseline.
It identifies the cause (outdated firmware).
It applies the update.
It verifies the door responds correctly.
It logs everything.
It continues patrol.
No human involvement.  Full audit trail.

> **Hinweis — Branchen-Realitaet:** In regulierten Physical-Security-Systemen
> (EN 50131 fuer Einbruch-/Ueberfallmeldeanlagen) ist autonomes Firmware-Update
> auf Tuer-Controllern **nicht** zulaessig — Change-Management mit Audit-Trail,
> oft physische Anwesenheit eines Technikers und Replay-Tests sind Pflicht.
> Dieses Beispiel illustriert die Self-Improve-Mechanik von Claude Code, nicht
> die Realitaet konformer Sicherheitsanlagen. Fuer Code-Repos und CI/CD gilt
> die Analogie weiterhin; fuer echte Hardware-Endpunkte waere ein
> Approval-Schritt (Mechanism "Human review gates" oben) Pflicht.

---

## Module 3.5: Telegram Bridge, Inception & Worktree Isolation

**Learning Objectives:** After this module, you can:
- Decide between the built-in mobile workflow (`claude remote-control`, `/teleport`, `--teleport`) and a custom Telegram Bridge based on multi-user, audit, and surface requirements.
- Pick the right isolation level (worktree / Docker via Inception / remote VM) for a given task and configure `worktree.baseRef` and `--tmux` for multi-agent visibility.
- Wire up `PushNotification` and Channels (research preview) to receive task completions without polling, and explain when to reach for the official API versus a custom bridge.

### Built-in Mobile Workflow — `claude remote-control` + `/teleport`

Before showing the custom Telegram Bridge, look at what Claude Code already provides out-of-the-box for mobile/remote use:

**`claude remote-control`** — A CLI subcommand that lets a remote surface (claude.ai web, the iOS app) **drive a session running on your local terminal**. The web session sends prompts, your local Claude executes them, the output streams back. No custom bridge code needed.

You can also invoke this from within a running session:
- **`/remote-control`** / **`/rc`** — Toggles remote control on the current session.
- **`/teleport`** / **`/tp`** — Pulls an existing web session **into your local terminal** (the inverse direction). Useful when you started something on your phone and want to continue at your desk.
- **`--teleport`** CLI flag — Equivalent at startup time.

**Typical use-case:** You are on the train, your phone has the claude.ai app. You ping the work laptop via `remote-control`: "Run a security audit on the checkout service." The local Claude executes, results stream back to your phone. No Telegram, no bridge process — just the official channel.

**Trade-off vs. Telegram Bridge:**

| Aspect | `claude remote-control` (built-in) | Telegram Bridge (:wrench: custom) |
|---|---|---|
| Setup effort | Zero — built in | Telegram bot creation + bridge service + auth wiring |
| Surfaces | Anthropic-hosted (claude.ai web, iOS app) | Any Telegram client |
| Multi-user / group | Single-user (your account) | Group chats, multiple senders, audit per sender |
| Customization | Anthropic's UX | Bot commands, role-based access, custom routing |
| Best for | "I just want my phone to drive my laptop" | "Our team's on-call rotation messages a SOC bot" |

**Recommendation:** Use `remote-control` for personal mobile workflows. Build a Telegram Bridge only when you genuinely need multi-user routing, group-chat semantics, or audit trails per sender.

---

### Telegram Bridge — Group-Chat Coordination (Custom)

> **:wrench: Custom Component:** The Telegram Bridge described below is a workshop teaching example. For most personal mobile use-cases, `claude remote-control` (above) is the simpler path.

1. Send a Telegram message: "Run a security audit on the checkout service"
2. The bridge receives it and dispatches a Claude Code task
3. Claude executes the full workflow — can spawn multiple agents, run scans, write reports
4. Results arrive in the Telegram chat

**When this pattern is worth the custom build:**
- Multi-user / group-chat coordination — multiple operators can dispatch and observe, with per-user audit trail
- On-call rotation that already lives in a Telegram channel — keep the existing surface instead of adding a second one
- Cases where the official `remote-control` surfaces (claude.ai web, iOS app) don't fit the team's existing workflow

For single-user "drive my laptop from my phone" scenarios, `claude remote-control` (above) covers the same need without the bridge service.

**`PushNotification` Tool** — A built-in tool that can emit a desktop or phone push when a task completes (for example, "Build done. 3 PRs ready for review."). Pair it with long-running background agents when you want a notification on completion instead of polling the session.

---

### Inception — Claude Code Inside Docker

`/multi-model-orchestrator:inception` runs Claude Code inside a Docker container with full isolation.

**Why:**

| Scenario | Why Inception |
|---|---|
| Running generated code | Generated code might be dangerous.  Run it inside. |
| Untrusted repositories | Analyze without exposing your host system |
| Parallel isolated tasks | Each instance has its own filesystem, no conflicts |
| Compliance requirements | Full network and filesystem audit logging |
| Destructive operations | Restructure, delete, format — with clean rollback |

**Containment chamber analogy:**
You want to know if this suspicious device is dangerous?
You do not open it in the lobby.
You put it in the containment chamber, examine it remotely.
If it explodes, the lobby is fine.

---

### Worktree Isolation

Git worktrees: separate working directories sharing the same git history,
with independent file states.

```bash
git worktree add ../agent-task-1 -b agent/task-1

# Agent works in ../agent-task-1
# Your main directory is completely untouched
# Changes are in git but isolated to that branch

git merge agent/task-1               # Accept
git worktree remove ../agent-task-1  # Or discard entirely
```

**Benefits:**
- Lightweight — no Docker overhead, instant setup
- Multiple agents work in parallel on the same repo without conflicts
- Each agent has its own branch — clean merge or clean discard

#### `worktree.baseRef` — Where the Worktree Branches From

The `worktree.baseRef` setting controls **which ref a new `claude --worktree` branches from**. Two options:

| Value | Behavior | When to use |
|---|---|---|
| **`fresh`** | Branches from `origin/<default>` — always the latest pushed mainline | Multi-agent fan-out where all agents must start from identical, fresh state |
| **`head`** | Branches from your local `HEAD` — your uncommitted intent goes with it | "I'm mid-refactor, spawn a worktree to try an alternative without losing my current state" |

The default for `worktree.baseRef` changed across CLI versions, so set it explicitly rather than relying on it. For Block 3's multi-agent patterns the answer is almost always `fresh` — five agents starting from five subtly-different bases is a debugging nightmare. The setting lives in `settings.json` (project scope) or via `--worktree-base-ref` per invocation.

#### `--tmux` — Multi-Agent Visibility in One Screen

When you fan out several worktree subagents, `--tmux` opens each session in its own tmux pane so you can watch them all simultaneously:

```bash
claude --worktree feature/api-migration --tmux
claude --worktree feature/db-migration --tmux
claude --worktree feature/ui-migration --tmux
```

Each `--tmux` invocation drops into a labeled pane inside the current tmux window — your three migration agents are visible side-by-side, output streams continuously, you can switch focus with the normal tmux bindings. Without `--tmux` you would either juggle three terminals or read logs after the fact. With `--tmux`, the multi-agent run becomes a live cockpit.

---

### The Full Architecture

```
You (CLI / claude.ai web / iOS app  --  optional: Telegram bridge)
    |
    v
Channel: claude remote-control (default)  --or--  :wrench: Telegram Bridge
    |
    v
Claude Code -- Orchestrator
    |
    +------------------+------------------+
    |                  |                  |
    v                  v                  v
Agent 1 (Explorer)  Agent 2 (Tests)  Agent 3 (Docs)
Worktree A          Worktree B       Worktree C
Read-only           Read+Write       Write only
    |                  |                  |
    +-------results----+------------------+
                       |
                       v
             Agent 4 (Implementer)
             Worktree D
                       |
                       v
        Agent 5 -- Devil's Advocate Swarm
        Worktree E (adversarial)
             +--------+--------+
             v                 v
        Scanner 1         Scanner 2
        Security          Quality
             +--------+--------+
                      |
                      v
               Debate Agents
         Prosecutor vs. Defender
                      |
                      v
              Consensus Agent
                      |
              CONFIRMED only
                      |
                      v
              Fixer Agents
                      |
         +------------+
         v
Orchestrator aggregates all results
         |
         v
Report returned on the same channel (remote-control surface, or Telegram chat if bridged)
```

Every piece of this architecture exists and works today — though several components
(:wrench: marked above) are custom implementations built for this workshop, not
out-of-the-box Claude Code features.

---

### The Security Analogy — Complete Picture

| Claude Code Concept | Physical Security Equivalent |
|---|---|
| Orchestrator | SOC (Security Operations Center) |
| Specialized agents | Teams with defined roles and access |
| Worktrees | Locked rooms within the same building |
| Inception / Docker | Containment / isolation chamber |
| Telegram Bridge | Remote SOC access from mobile device |
| Devil's Advocate Swarms | Automated pentest with built-in tribunal |
| Quality Gates | Compliance checklist before sign-off |
| Self-Improve Loop | Continuous autonomous security hardening (note: for code/CI; in regulated PhySec systems per EN 50131 autonomous endpoint patching is not allowed) |
| Scheduled Tasks | Automated patrol routes |
| Hooks | Standing orders requiring authorization |
| Agent memory | Incident logs and after-action reports |

**The complete picture:**
You have built a Security Operations Center for your software.
It monitors continuously.
It investigates automatically.
It dispatches specialists.
It isolates risky work.
It runs adversarial tests against itself.
It patches confirmed findings.
It keeps a full audit trail.
It surfaces findings on whichever channel you have wired up — terminal, web, push notification, or a custom bridge.

---

## Module 3.6: CI/CD & Headless Mode

**Learning Objectives:** After this module, you can:
- Run Claude headlessly with `claude -p`, `--output-format json`, and `--json-schema` to build deterministic, machine-parseable pipeline stages.
- Set up CI authentication with `claude setup-token` and combine `--max-budget-usd`, `--max-turns`, and `--bare` to bound cost and behavior for unattended runs.
- Build a complete pre-commit hook or GitHub Actions workflow that uses Claude Code as a pipeline stage, and recognize the common CI failure patterns (token expiry, missing budget cap, interactive-mode hang).

### Overview

Up to this point we have used Claude Code interactively — typed prompts, watched output, made decisions in the loop. **This module flips that around: Claude Code as a tool in a pipeline.** Pre-commit hooks, auto-PR reviewers, nightly audit reports, CI gatekeepers. The same model, the same skills, the same agents — but invoked headlessly by a script, with cost caps and structured output instead of a human at the keyboard.

> **Mission hint:** When Claude Code is more than an editor sidekick in your daily work, it is running in CI. This module shows how.

The foundation is four building blocks: **headless invocation (`claude -p`), structured output (`--output-format json`), cost caps (`--max-budget-usd`, `--max-turns`), and CI-grade auth (`claude setup-token`)**. Combine them and Claude becomes a deterministic pipeline stage.

---

### Security Analogy

Think of a physical security operation. **Patrol officers are interactive** — they walk the building, react to what they see, make judgement calls. **The nightly audit is autonomous** — it runs on schedule, follows a fixed protocol, reports exceptions. Both are necessary. Both belong to the same SOC.

Claude Code is the same dual creature: an interactive partner *and* a scriptable tool. CI/CD is the autonomous-audit side of that creature.

---

### Headless Mode — `claude -p`

`claude -p "<prompt>"` runs Claude as a **one-shot command** instead of opening an interactive loop. Default output is plain text on stdout; exit code 0 on success, non-zero on failure.

```bash
claude -p "Review this diff and suggest improvements" < diff.patch
```

Typical use-cases:

- **Pre-commit lint helper** — feed the staged diff in, fail the commit if Claude finds issues.
- **PR description generator** — give Claude the branch diff, generate the PR body.
- **Nightly audit report** — cron job emits a Markdown summary of changes that day.

The headless mode does not load your interactive transcript — every invocation starts fresh. That is a feature, not a bug: CI runs must be reproducible.

---

### Structured Output — `--output-format json` + `--json-schema`

A CI pipeline that parses free-form prose is brittle. The right pattern is to force Claude's output through a schema:

```bash
claude -p "Categorize this issue" \
  --output-format json \
  --json-schema '{
    "type":"object",
    "properties":{
      "category":{"type":"string","enum":["bug","feature","docs"]},
      "severity":{"type":"integer","minimum":1,"maximum":5}
    }
  }'
```

The output is JSON that matches the schema — your downstream `jq` / Python / Node script can consume it with confidence. `--output-format` also accepts `text` (default) and `stream-json` (newline-delimited JSON events, useful for live tailing).

**Security analogy:** A patrol report on a clipboard form, not a free-form story. The form forces consistent fields — incident type, severity, location — so the dispatcher can aggregate across patrols.

---

### CI Auth — `claude setup-token`

Interactive `claude` sessions authenticate through a browser OAuth flow. CI runners do not have a browser. The bridge is **`claude setup-token`**:

```bash
claude setup-token         # interactive once on a workstation
# generates a long-lived OAuth token (1 year)
```

Store the token as a CI secret (GitHub Actions Secret, GitLab CI Variable, etc.). At runtime CI exports it as `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_TOKEN`) and `claude -p` picks it up automatically.

> **Security note:** The token grants full Claude Code access for a year. Treat it like an SSH deploy key — never commit it, never log it, rotate on a schedule, revoke if a CI provider is compromised.

---

### Cost Caps — `--max-budget-usd` and `--max-turns`

The single biggest CI risk with autonomous LLMs is a runaway loop: a tool keeps failing, Claude keeps retrying, the bill keeps climbing. Two flags neutralize that risk:

- **`--max-budget-usd 0.50`** — hard dollar cap. Once spend hits the cap, the session exits with a non-zero code. CI fails cleanly instead of bleeding money.
- **`--max-turns 10`** — turn cap. Useful when budget alone is too coarse (one turn can be a tiny tool call or an expensive reasoning step).

```bash
claude -p "Generate release notes" --max-budget-usd 0.20 --max-turns 5
```

The two caps are complementary: budget protects you from expensive *reasoning*, turns protect you from infinite *retry loops*. Set both in CI, always.

**Cross-reference:** Module 3.4 (`/loop`, `/goal`) discusses the same flags as a safety net for autonomous loops in interactive sessions — the CI use-case is the strictest application of that pattern.

---

### `--bare` Mode — Lightweight CI

By default `claude -p` still loads hooks, skills, plugins, MCP servers, and the auto-memory system. For a simple "classify this JSON" call in CI, that is pure overhead. **`--bare` disables all of it:**

```bash
# Heavy: loads everything
claude -p "Categorize" --output-format json

# Lightweight: just the model
claude --bare -p "Categorize" --output-format json
```

`--bare` gives you:

- **Faster cold-start** — no skill discovery, no MCP handshake.
- **Deterministic behavior** — no surprise hook intervention.
- **Lower token use** — no skill descriptions injected into the system prompt.

Use `--bare` for any CI step that does not actually need your custom skills or hooks. Reach for full mode only when the pipeline genuinely depends on a plugin or MCP server.

---

### Persona Override — `--append-system-prompt`, `--system-prompt`, `--system-prompt-file`

CI personas are different from interactive ones — terser, more structured, line-number-aware. Three flags shape that:

- **`--append-system-prompt "Always respond in JSON."`** — appends a hint on top of the default system prompt. Good for small tweaks.
- **`--system-prompt "<full text>"`** — replaces the system prompt entirely. Total control, but you lose Claude Code's defaults.
- **`--system-prompt-file <path>`** — same as above but reads from a file. Versioning the persona in git is the recommended pattern.

```bash
claude -p "Review the diff" \
  --system-prompt-file ci/personas/strict-reviewer.md \
  --output-format json
```

---

### `/autofix-pr` — Claude in the PR Loop

`/autofix-pr` is a slash command that **spawns a background web session watching a pull request's CI**. When CI fails, the background session analyzes the failure, pushes a fix commit, and lets CI re-run.

Workflow:

1. Developer pushes a PR.
2. CI fails (test broken, lint error, type error).
3. Developer (or a hook) runs `/autofix-pr`.
4. Anthropic-hosted session picks up the PR, analyzes the failure, pushes a fix.
5. CI re-runs.

> **Safety note:** Use `/autofix-pr` for **test and lint failures**, not for production-deploy failures. A failing deploy step is signal that needs human judgement, not autoreply.

> **When to use `/autofix-pr`:**
> - **Test failures, lint failures, formatting issues** — low-risk fixes
> - **Doc typos, missing imports** — clearly mechanical
> - **NEVER for production-deploy failures** — those need human review
> - **NEVER for security/auth/crypto code** — even a "lint fix" could introduce a bug
> - **NEVER in repos where main branch deploys to prod automatically**
>
> Pair `/autofix-pr` with branch protection rules so the auto-pushed commit still needs
> human PR approval before merge.

---

### GitHub Actions — A Complete Pattern

Putting it all together — a PR reviewer that runs on every pull request:

```yaml
# .github/workflows/claude-review.yml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Claude Code
        run: |
          curl -fsSL https://code.claude.com/install.sh | bash

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          git diff origin/main...HEAD > /tmp/diff.patch
          claude --bare -p "Review this diff. Find bugs, security issues, style issues. Output JSON." \
            --output-format json \
            --max-budget-usd 0.50 \
            --max-turns 3 \
            < /tmp/diff.patch \
            > /tmp/review.json

      - name: Post Review as PR Comment
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "$(jq -r '.summary' /tmp/review.json)"
```

Every building block from this module is in there: `--bare` for a clean run, JSON output for downstream parsing, budget cap and turn cap as the safety net, OAuth secret for auth.

---

### GitLab CI / Self-Hosted Runners

Mid-sized industrial companies often run **GitLab self-hosted** with private runners
(no direct Internet access from the runner). Here is the equivalent `.gitlab-ci.yml`
for a Claude Code MR review:

```yaml
# .gitlab-ci.yml
stages:
  - review

claude-review:
  stage: review
  image: alpine:latest
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  before_script:
    # Setup Claude Code in a minimal container
    - apk add --no-cache curl git bash
    - curl -fsSL https://code.claude.com/install.sh | bash
    - export PATH="$HOME/.claude/bin:$PATH"
  script:
    - git fetch origin $CI_MERGE_REQUEST_TARGET_BRANCH_NAME
    - git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD > /tmp/diff.patch
    - |
      claude --bare -p "Review this MR diff. Find bugs, security issues. Output JSON." \
        --output-format json \
        --max-budget-usd 0.50 \
        --max-turns 3 \
        < /tmp/diff.patch \
        > /tmp/review.json
    - cat /tmp/review.json
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
```

Same four building blocks as the GitHub Actions example — only the surface (GitLab YAML, MR-specific env vars `CI_MERGE_REQUEST_TARGET_BRANCH_NAME`, `CI_PIPELINE_SOURCE`) changes.

---

### Self-Hosted Runner Without Internet

If your runner has **no direct Internet access** (common in regulated industries — utilities, defense subcontractors, hospitals), `claude` cannot reach `api.anthropic.com` directly. Three patterns cover this case:

**Option A: HTTP Proxy** — Configure Claude Code to use a corporate proxy:

```bash
export HTTPS_PROXY="http://proxy.corp.example:8080"
export HTTP_PROXY="http://proxy.corp.example:8080"
claude -p "Review this diff" < diff.patch
```

The proxy needs an outbound rule for `api.anthropic.com`. Most enterprise proxies already log all traffic — pair this with a `--metadata` tag (Module 3.6 Monitoring section) so corporate SOC can correlate Claude calls with runner jobs.

**Option B: AWS Bedrock in VPC** — Use Claude via Bedrock inside your VPC:

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=eu-central-1
export AWS_PROFILE=ci-bedrock-role
claude -p "Review this diff" < diff.patch
```

No direct call to `api.anthropic.com` — all traffic stays in your VPC, signed with AWS SigV4. The runner needs IAM permissions for `bedrock:InvokeModel` on the Anthropic model IDs only.

**Option C: Vertex AI in GCP** — Same pattern via Google Cloud Vertex AI:

```bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=europe-west1
export ANTHROPIC_VERTEX_PROJECT_ID=my-corp-project
claude -p "Review this diff" < diff.patch
```

Equivalent isolation — Claude runs inside your GCP project boundary. Pick Bedrock vs. Vertex by where the rest of your stack already lives; both bypass the public Anthropic endpoint.

---

### Token Rotation for Long-Lived Runners

`claude setup-token` generates a 1-year OAuth token. For long-lived CI runners (build farms, on-prem GitLab runners, Jenkins agents) the rotation discipline matters:

- **Rotate the token at least quarterly** — never let a runner-resident token live to its 1-year expiry undetected.
- **Store in CI provider's secret store** (GitLab CI/CD Variables marked **Protected** + **Masked**; GitHub Actions Secrets; Jenkins Credentials with masked logging).
- **Revoke old tokens** via `claude auth status` -> "manage tokens" — leftover tokens from previous CI integrations are a long-tail risk surface.
- **For high-security environments:** use Bedrock or Vertex with **short-lived AWS/GCP credentials via OIDC federation**. The runner gets a 1-hour STS token from the CI provider's identity, calls Bedrock with it, never carries a long-lived Anthropic token. Token-leak blast radius drops from 1 year to 1 hour.

---

### Pre-Commit Hook — The Local Equivalent

The same headless pattern works locally as a git pre-commit hook (`.git/hooks/pre-commit`):

```bash
#!/bin/bash
git diff --cached | claude --bare -p \
  "Check this staged diff for obvious bugs. Reply 'OK' or list issues." \
  --max-budget-usd 0.10 \
  --max-turns 2 \
  --output-format json
# Exit non-zero if issues found
```

Cross-reference: Module 2.2 (Hooks) covers Claude Code's *internal* hook system (PreToolUse, PostToolUse, etc.). The hook above is a **git** hook that *calls* Claude Code from the outside — same word, different layer. Both are legitimate places to invoke Claude in your workflow.

---

### Monitoring CI Costs

`/cost` shows spend for the current interactive session — not aggregated across CI runs. For CI-wide cost visibility you have two paths:

- **Anthropic Console dashboard** — aggregates API spend across all calls under your token.
- **Custom logging** — pipe `--output-format stream-json` to a log aggregator and parse the `usage` events.

**Tag your CI runs** so the aggregation is meaningful. Pass `--metadata '{"ci_run_id":"<id>","repo":"<name>"}'` and you can later slice spend by repo, by workflow, by PR.

---

### Common Failure Patterns

Things that will go wrong in your first CI Claude integration — and how to fix them:

| Symptom | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | OAuth token expired or never set | Re-run `claude setup-token`, rotate the CI secret |
| Unexpected `$10` spend on a single run | Loop without budget cap | Set `--max-budget-usd` and `--max-turns` on **every** CI invocation |
| Downstream `jq` fails on output | Free-form prose, not JSON | Add `--output-format json` and `--json-schema` |
| Inconsistent persona across runs | Default system prompt drifts with skills loaded | Use `--bare` plus `--system-prompt-file` for deterministic persona |
| CI runner stalls waiting for input | Interactive mode invoked instead of `-p` | Always use `claude -p "..."`, never bare `claude` in CI |

---

### Don'ts in CI

A short checklist of mistakes that look fine in a dev environment and bite hard in CI:

- **Do not** use `--dangerously-skip-permissions` on shared CI runners. CI infrastructure is shared — bypassing the permission system can leak secrets across jobs or write to the runner host. Use a sandboxed runner if you need full automation.
- **Do not** start interactive sessions in CI. `claude` without `-p` waits for stdin and hangs the job.
- **Do not** echo the API key in CI logs. Run `set +x` before any step that touches `ANTHROPIC_API_KEY`, and mask the secret in your CI provider's UI.
- **Do not** skip cost caps in autonomous loops. `--max-budget-usd` is one flag — write it on every line.

---

### Cross-References

- **Module 2.2 (Hooks)** — Internal Claude Code hooks vs. external git/CI hooks calling Claude.
- **Module 3.3 (Security)** — Permission rules and `dontAsk` mode for CI; complements this module's auth/budget story.
- **Module 3.4 (Scheduling)** — `/loop` and `/goal` use the same `--max-budget-usd` safety net for interactive autonomous loops.

---

## Module 3.7: Troubleshooting & Debugging Claude Code

**Learning Objectives:** After this module, you can:
- Use `/debug`, `--verbose`, and `/doctor` to diagnose Claude Code issues at the right level (investigative / descriptive / prescriptive).
- Recognize the 4 classic hook failure patterns (overly broad matcher, non-executable script, non-zero exit interpreted as block, script hang) and the 4 classic skill failures (vague description, model-invocation disabled, paths filter mismatch, YAML parse error) and apply the diagnosis sequence for each.
- Walk through the 8-step diagnosis checklist (CLAUDE.md → skills → plugins → hooks → MCP → permissions → `--verbose` → `/doctor`) in order without skipping steps.

### Overview

The workshop so far has shown you how to set Claude Code up, extend it with skills, hooks, plugins, and MCP servers, and run it productively. But every real workflow has a second mode: **diagnosis when things do not behave as expected**.

The skill you wrote does not trigger. The hook you registered blocks all your shell commands. The MCP server times out at first contact. The plugin says it loaded — but the skill inside it is invisible.

In every tooling family this debugging phase shows up around day two. Claude Code reaches it faster than most because so much of its configuration is **distributed across files** — `settings.json`, plugin manifests, skill frontmatter, hook scripts, MCP config blocks, auto-memory directories. A single mismatched field or stale cache can make the whole pipeline behave silently wrong.

This module is your **diagnostic workbench**. It does not teach new features — it teaches the **inspection tools** that turn a black box back into a glass box.

### Security Analogy

Think of a complex access-control installation. A door does not open. There are **five candidate layers**: the card itself, the reader, the controller, the wiring, the power supply. A good technician does not start by replacing the reader — they walk the layers in order, eliminating each one with a quick test.

Claude Code has the same structure. When something does not work, the layers are: **prompt → skill → hook → plugin → permission**. The order of inspection is what separates ten minutes of debugging from two hours.

This module gives you the inspection commands per layer.

---

### `/debug` — The Bundled Debug Skill

`/debug` is a bundled skill that **activates verbose trace logging for the current session**. Once active, Claude reports — in line — which skills it considered, which trigger phrases matched, which hooks fired, which tools were invoked, and which configuration files were consulted.

```
/debug skill-not-triggering
```

The argument focuses the trace on a sub-system (here: skill matching). Other useful focuses:

- `/debug hook-firing` — show every hook event and matcher result
- `/debug mcp-handshake` — surface MCP server connect/disconnect events
- `/debug instructions-loaded` — show which CLAUDE.md / AGENTS.md files were loaded

The typical use-case: *"My skill is installed, but Claude is not picking it up. Why?"* — `/debug` will show you either the failed match (description too generic, paths filter blocked it, model invocation disabled) or that the skill never appeared in the candidate set at all (frontmatter parse error).

See Module 2.1 for the skill frontmatter reference; `/debug` essentially **replays the routing decision** that Module 2.1 describes.

---

### `--verbose` and `/doctor`

Two coarser diagnostic tools that complement `/debug`:

**`claude --verbose`** — Verbose output **at session start**. Restart Claude with this flag and you see the boot sequence: which CLAUDE.md files were merged (project + user + managed + auto-memory), which plugins loaded, which skills are visible, which hooks are armed, which MCP servers responded to their handshake.

Use this when the question is *"What does Claude even think is configured right now?"* — for example after editing settings.json by hand, or after a plugin update.

**`/doctor`** — A **health check** of the current configuration. It walks the layers and reports concrete problems:

- corrupted or unparseable `settings.json`
- plugin manifests that point to missing skill files
- MCP servers configured but not reachable
- expired OAuth tokens
- protected-path permission rules that conflict with each other

`/doctor` is non-interactive — it just prints a report. Use it when *something* is broken but you do not know which layer.

**When `--verbose` vs `/doctor`:**

| Question | Tool |
|---|---|
| "What did Claude load at startup?" | `--verbose` |
| "Is my configuration valid?" | `/doctor` |
| "Why did this specific prompt not trigger my skill?" | `/debug` |
| "Why did this specific hook fire / not fire?" | `/debug hook-firing` |

`--verbose` is **descriptive** (what is configured), `/doctor` is **prescriptive** (what is wrong), `/debug` is **investigative** (what happened on this turn).

---

### Hook-Failure Diagnosis

Hooks are the fastest layer to misconfigure because they are **shell scripts wired to an event matcher**, and either side can be wrong.

**Four classic hook failures:**

1. **Hook blocks everything.** The matcher is too broad — typically `".*"` instead of a specific tool pattern. Every `Bash` invocation triggers the hook; the hook denies; nothing in your terminal works without a prompt.
2. **Hook script does not run at all.** File is not executable (`chmod +x` missing), shebang line absent, or the path in `settings.json` is wrong (typo, relative path that does not resolve, Windows-style backslash).
3. **Hook script errors out.** Any non-zero exit code is interpreted as a **block** by Claude Code. Your script that just wanted to log something is now denying every operation because it has a syntax error on line 12.
4. **Hook script hangs.** No timeout, the script waits for input that never comes, or it shells out to a slow command. Claude Code's default hook timeout is around 5 seconds — past that, the hook is killed and the operation blocked.

**Diagnosis sequence:**

1. **`/hooks`** — Lists active hooks with their matchers. Confirms that your hook is even registered. (Surprisingly often the issue: typo in the JSON key.)
2. **Run the script manually.** `bash ~/.claude/hooks/security-check.sh` — does it execute at all? Does it return 0?
3. **Simulate the JSON input.** Hook scripts receive a JSON payload on stdin. Replay it:

   ```bash
   echo '{"command":"rm -rf /","tool":"Bash"}' | bash ~/.claude/hooks/security-check.sh
   echo $?    # 0 = allow, non-zero = block
   ```

4. **Activate `--verbose`** and re-trigger the action. The hook trace shows match attempts and exit codes inline.

See Module 2.2 for the full hook frontmatter and event reference; this section uses that vocabulary to diagnose mistakes.

---

### "My Skill Does Not Trigger" — Diagnosis

The skill is installed in the right directory, `/skills` lists it, but Claude never invokes it. **Four common causes:**

1. **Description too generic.** The skill description has no concrete trigger phrases. Claude's routing cannot decide that *this* prompt belongs to *this* skill. Fix: rewrite the description with explicit example prompts.
2. **`disable-model-invocation: true`** in frontmatter. The skill is registered but only callable manually via slash-command. Auto-invocation is off by design.
3. **`paths:` filter.** The skill has a paths filter (e.g. `paths: ["src/**/*.py"]`) and the current conversation does not match. The skill is silently inactive.
4. **Frontmatter parse error.** YAML is broken — missing colon, bad indentation, smart-quote that crept in from a paste. The skill loads as an empty stub. `/doctor` catches this; `/skills` may still list the skill but with no description visible.

**Diagnosis sequence:**

1. **`/skills`** — Is the skill in the listing at all? If no → frontmatter parse error or wrong directory.
2. **`cat ~/.claude/skills/<name>/SKILL.md | head -20`** — Inspect the frontmatter. Look for `disable-model-invocation`, `paths`, and the description quality.
3. **Trigger explicitly.** In the prompt write *"Use the `<skill-name>` skill to ..."*. If the skill fires now → routing problem (vague description). If not → frontmatter or path-filter problem.
4. **`/debug`** with skill focus. Run the same prompt again; read the trace.

**Note on caching:** Skills load **live**, no Claude Code restart is needed when you edit a SKILL.md file. The `/skills` listing refreshes on next invocation. If a skill seems "stuck on the old version", you most likely edited a different copy of the file (user-scope vs project-scope, different vault).

---

### Plugin Debugging

Plugins are the next layer up — they contain skills, agents, hooks, and MCP servers. A plugin can be **installed but inert**, or **loaded but with broken contents**.

**Inspection commands:**

- **`claude plugin list`** — Every installed plugin, scope (user/project/local), and load state.
- **`claude plugin validate <name>`** — Schema-checks the plugin manifest. Catches the common mistake of placing `plugin.json` at the root instead of `.claude-plugin/plugin.json` (the correct path since 2025; see Module 2.3).
- **`/reload-plugins`** — Hot-reload after a plugin update. Mostly not necessary (plugin contents load live), but useful when changing the manifest or top-level metadata.

**Common failure: plugin loads, skill inside does not.** Almost always a **relative path issue** in the manifest — the manifest references `skills/my-skill/SKILL.md` but the file actually lives at `my-skill/SKILL.md` (no `skills/` prefix). `claude plugin validate` catches this.

See Module 2.3 for the full plugin layout — this section just gives you the inspection commands for it.

---

### MCP Server Reconnect Problems

MCP servers are subprocesses with their own lifecycle, OAuth state, and timeouts. Diagnosis commands:

- **`/mcp`** — Status table for every configured MCP server: connected / disconnected, OAuth state (authorized / expired / never), last error message.
- **`claude mcp get <name>`** — Detailed configuration for one server (command line, env vars, transport).
- **`claude mcp reset-project-choices`** — Clear the per-project approval cache. Use when Claude keeps re-asking for MCP approval even though you said yes (corrupted approval store).

**Most common MCP problem:** **stale OAuth token.** The server worked yesterday, today it returns 401. Fix: open `/mcp`, find the server with expired status, follow the re-auth link. The browser flow regenerates the token and Claude reconnects.

See Module 2.4 for MCP setup; this section gives you the runtime inspection surface.

---

### `InstructionsLoaded` Event — Inspecting Memory Drift

`InstructionsLoaded` is a hook event (introduced in the 2026 hook expansion — see Module 2.2) that fires **every time Claude loads a CLAUDE.md, AGENTS.md, or auto-memory file**. The hook receives a JSON payload listing the files and (optionally) their content hashes.

**Use-case:** *"I added a new rule to my CLAUDE.md. Is Claude actually loading it?"* — register a tiny logging hook on the event and find out.

```bash
# In ~/.claude/hooks/inspect-instructions.sh
INPUT=$(cat)
echo "$INPUT" | jq '.loadedFiles' >> ~/.claude/loaded-instructions.log
exit 0
```

Register in `settings.json` with the `InstructionsLoaded` event matcher. Now every session start writes the loaded-files manifest into a log you can grep.

This is the single most useful debug hook to keep permanently armed if you maintain a non-trivial CLAUDE.md hierarchy.

---

### Auto-Memory Drift — Recognize and Repair

As covered in Module 1.2, Claude maintains an **auto-memory directory** per project where it records "remembered" facts on its own initiative. Most of the time this is useful — but occasionally Claude records a **false conclusion** ("the user prefers tabs" when really one file had tabs by accident), and that false conclusion then biases all future behavior.

**Symptom:** Claude behaves in a way your CLAUDE.md does not authorize, but consistently across sessions.

**Diagnosis:**

```bash
cat ~/.claude/projects/<hash>/memory/MEMORY.md
# Plus any topic files in the same directory
```

**Repair:** Either delete the offending note from `MEMORY.md` directly, or prompt Claude with *"Forget that I prefer tabs — that was incorrect"*. Auto-memory updates from explicit forget-prompts and from manual edits to the directory.

See Module 1.2 for the full auto-memory mechanics — this section just covers the **drift-detection** angle.

---

### The Diagnosis Checklist

When **anything** is not behaving as expected, walk the layers in this order. Do not skip steps — most problems are found in the first three.

1. **CLAUDE.md loaded?** Ask Claude *"What CLAUDE.md files do you see?"* — first reply tells you. Or use `--verbose` startup.
2. **Skills visible?** `/skills`
3. **Plugins active?** `claude plugin list`
4. **Hooks armed?** `/hooks`
5. **MCP servers connected?** `/mcp`
6. **Permission rules OK?** `/permissions`
7. **Read the verbose log.** Restart with `claude --verbose`, capture the boot output.
8. **Run `/doctor`.** Final pass — catches the leftovers.

If all eight checks pass and the problem persists, the issue is **prompt-shape** (Module 1.3) or **model behavior** rather than configuration.

---

### Anti-Patterns — Don't Do This

- **Do not reinstall the skill / hook / plugin first.** The configuration is almost always the cause, not a corrupted installation. Reinstalling resets your debug state without fixing the bug.
- **Do not "fix" things with `--dangerously-skip-permissions`.** That is symptom suppression, not root-cause analysis. You will reopen the same problem in the next session.
- **Do not ignore the auto-memory directory.** A surprising number of "Claude is weirdly opinionated about X" problems trace back to a single stale auto-memory entry from three weeks ago.
- **Do not edit `.claude.json` or `.mcp.json` manually as your first move.** Both are Protected Paths (see Module 3.3) — Claude refuses to write to them, and for good reason. Use the dedicated CLI commands (`claude plugin`, `claude mcp`) instead.

---

### The Security Analogy — Complete

Your access-control installation has a problem. A door will not open. The technician's playbook is:

1. **Check the card.** Is it the right card? Is it programmed? *(Prompt layer.)*
2. **Check the reader.** Is it powered? Does the LED blink? *(Skill layer.)*
3. **Check the controller.** Is the policy loaded? Does the audit log show a deny? *(Hook layer.)*
4. **Check the wiring and plugins.** Are the modules talking to each other? *(Plugin / MCP layer.)*
5. **Check power and permissions.** Is the whole site authorized for this card class? *(Permission layer.)*

Claude Code's debugging surface — `/debug`, `--verbose`, `/doctor`, `/hooks`, `/mcp`, `claude plugin list`, the `InstructionsLoaded` event, the auto-memory directory — is the same playbook in software form. Use it in order, and most outages collapse in minutes.

---

*End of Block 3 Teaching Material*
