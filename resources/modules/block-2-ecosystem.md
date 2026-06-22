# Block 2: The Claude Code Ecosystem

**Target audience:** Experienced programmers. Security analogies used throughout — especially relevant for the CySec engineer in the group.
**Duration:** ~90 minutes
**Goal:** Understand and use Skills, Hooks, Plugins, MCP, and RAG/NotebookLM to extend Claude Code

---

## Module 2.1: Skills & Commands

**Learning Objectives:** After this module, you can:
- Author a SKILL.md with the right frontmatter fields (`name`, `description`, `when_to_use`, `arguments`, `disable-model-invocation`, `paths`) so Claude picks it up reliably or only on manual invocation.
- Use dynamic context injection (`` !`<command>` ``) and argument substitution (`$1`, `$mode`, `${CLAUDE_SESSION_ID}`) to turn static skills into living prompts.
- Distinguish bundled skills (`/batch`, `/debug`, `/loop`, `/simplify`, `/verify`, `/run`, `/run-skill-generator`, `/fewer-permission-prompts`) and know which problem each one solves.

### The Core Idea

When you work with Claude Code repeatedly, you notice patterns: you always start sessions the same way, you always ask for commits in the same format, you always want tests written before implementation. Writing these instructions from scratch every time is wasteful and error-prone.

**Skills** solve this. A skill is a reusable prompt template — a set of instructions stored in a file that gets loaded into Claude's context when invoked. Instead of typing "follow TDD, write the failing test first, then implement..." every session, you type `/tdd` and Claude already knows exactly what to do.

**Commands** are the entry points — what the user types. A command can load a skill, pass arguments to it, or trigger a workflow. Think of it as the button on the wall vs. the procedure it triggers.

### Security Analogy: SOPs and Alarm Buttons

In physical security, you have **Standard Operating Procedures (SOPs)** — laminated documents in the control room that tell guards exactly what to do when a specific alarm fires. The SOP for "motion detected in Server Room A" might be: check CCTV feed, call supervisor, dispatch patrol, log incident.

The alarm button itself is just a trigger. The SOP is the intelligence behind it.

- **Skills = SOPs.** Detailed, reusable instructions. The "what to do."
- **Commands = Alarm buttons.** What the operator presses. The "how to trigger it."

A command `/tdd` is the button. The SKILL.md file for TDD is the SOP that Claude reads and follows.

### Anatomy of a Skill

Skills live in `skills/*/SKILL.md` inside a plugin, or in `~/.claude/skills/*/SKILL.md` for user-level skills. The file has two parts:

**YAML Frontmatter** (the header):
```yaml
---
name: tdd
description: >
  Test-Driven Development workflow. Use when user wants to write tests first,
  implement after, or says "write tests before code", "TDD", "red-green-refactor".
when_to_use: >
  TDD, test first, write tests, red-green-refactor, failing test,
  or any request where implementation should wait for a failing test.
argument-hint: "[target]"
arguments: [target]
model: sonnet
effort: high
paths: ["src/**", "tests/**"]
---
```

Key frontmatter fields (official schema):
- `name` - the identifier for this skill
- `description` - short summary for humans and discovery
- `when_to_use` - explicit activation guidance. Prefer this for trigger conditions instead of overloading `description`.
- `argument-hint` / `arguments` - user-facing hint plus named argument mapping.
- `model`, `effort`, `paths` - execution and scoping controls.

### Official Frontmatter Fields (2026 Reference)

Beyond `name` and `description`, the official skill schema supports a richer set of fields. These actually influence how Claude Code loads, scopes, and executes the skill:

```yaml
---
name: tdd
description: Test-Driven Development workflow. Use when writing tests before code.
when_to_use: >
  Triggers on TDD, test-first, red-green-refactor, "write tests before code"
argument-hint: "[guide|learn] [module]"
arguments: [mode, module]
model: sonnet
effort: high
paths: ["src/**/*.ts", "tests/**/*.ts"]
shell: powershell
hooks:
  PreToolUse:
    - matcher: Bash
      type: command
      command: ./pre-test-check.sh
---
```

| Field | What it does |
|-------|--------------|
| `argument-hint` | UI hint shown when the user types the slash command (e.g. `/tdd [guide|learn] [module]`) |
| `arguments` | Named positional argument list. Maps to `$mode`, `$module`, ... in the body |
| `when_to_use` | Modern alternative to stuffing trigger phrases into `description`. Read by Claude as activation signal |
| `model` | `haiku` / `sonnet` / `opus` — which model handles the skill's forked context |
| `effort` | `low` / `high` / `xhigh` / `max` — default thinking effort for this skill |
| `paths` | Glob patterns. Skill is path-scoped — only auto-activates when matching files are in context |
| `shell` | `powershell` / `bash` — override the shell used for skill-executed commands. Critical on Windows |
| `hooks` | Component-scoped hooks. Only run while this skill is active (see Module 2.2 for hook details) |

### Argument Substitution

When a skill receives arguments, Claude Code substitutes them into the body at execution time. The substitutions match the `arguments:` frontmatter:

| Token | Meaning |
|-------|---------|
| `$ARGUMENTS` | All arguments as a single string |
| `$1`, `$2`, ..., `$N` | Positional arguments by index |
| `$mode`, `$module`, ... | Named arguments (matches the `arguments:` frontmatter list) |
| `${CLAUDE_SESSION_ID}` | Current session UUID |
| `${CLAUDE_EFFORT}` | Current effort level (`low`/`high`/`xhigh`/`max`) |
| `${CLAUDE_SKILL_DIR}` | Absolute path to this skill's directory |

**Example** — combining positional and named arguments:

```markdown
---
name: review
description: Run a review against a target module
argument-hint: "[mode] [module]"
arguments: [mode, module]
---

# Review Skill

You are running the **$mode** review on module **$module**.

Session: ${CLAUDE_SESSION_ID}
Effort: ${CLAUDE_EFFORT}

Raw input: $ARGUMENTS
First positional: $1
```

Invoked as `/review strict auth-service`, the body sees `$mode = strict`, `$module = auth-service`, `$1 = strict`, `$ARGUMENTS = "strict auth-service"`.

### Dynamic Context Injection — Live Prompts

Skills are no longer static markdown. The `` !`<command>` `` syntax runs a shell command at skill-load time and inlines the command's stdout directly into the prompt.

```markdown
# Pre-Commit Skill

Current git diff:
!`git diff HEAD`

Current branch:
!`git branch --show-current`

Failing tests:
!`pytest --tb=no -q 2>&1 | tail -20`

Now review the diff and propose a commit message.
```

When Claude loads the skill, the backtick blocks are replaced by live command output **before** the prompt reaches the model. This transforms skills from static markdown into **living prompts** that auto-collect real-time context.

**Security analogy:** This is like a security checkpoint that pulls fresh badge data from the directory on every scan, rather than relying on a printout from this morning. Powerful — but also a new attack surface.

**Enterprise hardening:** Managed environments can disable this feature globally:

```json
{
  "disableSkillShellExecution": true
}
```

Set via managed settings — admins can lock skill bodies down to pure text, preventing any shell execution on skill load.

**Markdown Body** (the actual instructions Claude follows):
```markdown
# TDD Workflow

You are following strict Test-Driven Development. Follow these steps exactly:

## Phase 1: Red (Write the Failing Test)
1. Ask the user what behavior needs to be implemented
2. Write the test FIRST — before any implementation code
3. Run the test and confirm it FAILS
4. Show the user the red output

## Phase 2: Green (Make It Pass)
1. Write the MINIMUM code needed to pass the test
2. No gold-plating, no extras — just enough to go green
3. Run the tests and confirm they PASS

## Phase 3: Refactor
1. Now clean up the code — remove duplication, improve naming
2. Tests must stay green throughout
3. Commit with a meaningful message

## Rules
- Never write implementation before a test exists
- Never write more code than necessary to pass the current tests
- If the user skips a phase, remind them of the process
```

### Anatomy of a Command

Commands live in `commands/*.md` inside a plugin, or can be defined in settings. They are what the user types directly (e.g., `/tdd`, `/commit`, `/review`):

```yaml
---
name: commit
description: Create a structured git commit with conventional format
user_invocable: true
arguments:
  - name: message
    description: Optional commit message prefix
    required: false
---
```

The command body can be short (just trigger a skill) or contain its own instructions:

```markdown
# Commit Command

When invoked, follow this commit workflow:
1. Run `git status` to see what changed
2. Run `git diff --staged` to review staged changes
3. Write a commit message following Conventional Commits format:
   - feat: new feature
   - fix: bug fix
   - refactor: code restructure without behavior change
   - test: adding tests
   - docs: documentation only
4. Ask for confirmation before committing
5. Create the commit
```

### User Skills: Your Personal Toolkit

User skills live in `~/.claude/skills/` and are available in **every project** on your machine — not just one repo. This is your personal toolkit.

```
~/.claude/skills/
  my-workflow/
    SKILL.md          # your custom instructions
  code-review/
    SKILL.md
  agent-orchestrator/
    SKILL.md
```

To create a user skill:
```bash
mkdir -p ~/.claude/skills/my-workflow
# create SKILL.md with frontmatter + instructions
```

Then in any Claude Code session, you can invoke it: `/my-workflow` or just describe what you want — Claude will match the trigger phrases in the description.

### Skills vs Commands — Same Thing, Different Defaults

**Important didactic clarification.** In earlier versions of Claude Code, commands and skills were two separate categories. **Since v2.x they have been merged into a single concept.**

Both of these produce the exact same `/deploy` slash command:

```
.claude/commands/deploy.md
.claude/skills/deploy/SKILL.md
```

They are loaded by the same machinery, support the same frontmatter, and expose the same interface to the user. The "Command vs Skill" terminology is kept alive in the docs and the community, but the **runtime treats them identically**.

The relevant difference is now a single frontmatter switch:

```yaml
---
name: deploy
disable-model-invocation: true   # Manual /deploy only — never auto-triggered
---
```

- `disable-model-invocation: false` (default) — behaves like a classic **skill**: Claude can auto-invoke it when the description matches user intent.
- `disable-model-invocation: true` — behaves like a classic **command**: only fires when the user explicitly types `/deploy`.

#### Conceptual mapping (legacy terminology vs. current reality)

| Aspect | "Command-style" (manual) | "Skill-style" (auto-detected) |
|--------|--------------------------|-------------------------------|
| Frontmatter switch | `disable-model-invocation: true` | `disable-model-invocation: false` (default) |
| Who triggers it | End user (types `/name`) | User OR Claude (via description match) |
| Typical use | Destructive/critical actions: `/deploy`, `/commit`, `/delete` | Reusable workflows: TDD, code review, formatting |
| Analogy | Alarm button (you must press it) | SOP document (procedure can be invoked by anyone, including by name match) |
| Lives at | `commands/*.md` or `skills/*/SKILL.md` | `commands/*.md` or `skills/*/SKILL.md` |

**Bottom line:** both names live on, but functionally they are merged. Treat `disable-model-invocation` as the real boundary, not the file path.

### Bundled Skills (Built-in, Always Available)

Claude Code ships with **bundled skills** — prompt-based playbooks available in every session without installation. These are different from built-in commands (which execute fixed logic):

| Skill | What it does | Example |
|-------|-------------|---------|
| `/batch <instruction>` | Parallel codebase changes across git worktrees | `/batch migrate src/ from Solid to React` |
| `/claude-api` | Loads API reference + Agent SDK docs for your language | `/claude-api` |
| `/debug [description]` | Activates debug logging and analyzes the log | `/debug failing mcp auth` |
| `/loop [interval] <prompt>` | Executes a prompt periodically | `/loop 5m check deploy status` |
| `/simplify [focus]` | Runs parallel reviews + fixes on recently changed files | `/simplify focus on perf` |
| `/run [skill-name]` | Launch and verify your app (added v2.1.145) | `/run dev-server` |
| `/verify` | Verify recent changes by actually running the app, not just tests (v2.1.145) | `/verify` |
| `/run-skill-generator` | Generate a per-project run-skill that knows how to launch this codebase (v2.1.145) | `/run-skill-generator` |
| `/fewer-permission-prompts` | Scans your transcripts for repeated tool calls and generates a `permissions.allow` allowlist | `/fewer-permission-prompts` |

**Security analogy:** Bundled skills are like the standard operating procedures that come pre-installed with a security system. The `/batch` skill is like running a firmware update across all door controllers simultaneously — each in its own isolated worktree so a failure in one doesn't brick the others. `/verify` is the equivalent of physically opening the door after replacing the lock — it isn't fixed until you've actually used it.

### Authoring Skills with `/run-skill-generator`

The fastest way to create a new project-specific skill is the bundled `/run-skill-generator`:

```
/run-skill-generator
```

It interviews you ("What kind of repeated task do you have? What inputs? What outputs?") and
generates a `SKILL.md` skeleton in `.claude/skills/<skill-name>/SKILL.md` — pre-filled with:
- Sensible `description` and `when_to_use` for trigger detection
- `arguments` placeholders if your task takes inputs
- A starter template with `$ARGUMENTS` substitution
- Recommended `model` and `effort` based on the task type

**Use this when:**
- You've identified a task you do 3+ times per week
- You want to commit the skill into the team repo (`.claude/skills/` is git-tracked)

**Don't use this when:**
- The task is one-off — just write the prompt inline
- You need a deeply custom skill with hooks and tool restrictions — write it by hand

After generation, refine the description (most-important for trigger detection) and test:

```
/<your-new-skill-name>
```

If it doesn't trigger as expected, see Module 3.7 (Troubleshooting) for diagnosis steps.

### Skill Live-Reload

Files in `~/.claude/skills/` and `.claude/skills/` are picked up live — **no Claude Code restart needed**. Edit a `SKILL.md`, save, invoke the skill again. The new content is loaded immediately. This makes skill authoring iterative and fast: edit, test, edit, test.

### Advanced Skill Frontmatter

Beyond `name` and `description`, skills support control fields that matter for security and automation:

```yaml
---
name: deploy
description: Deploy the current branch to staging
disable-model-invocation: true    # ONLY manual /deploy — never auto-triggered
allowed-tools: Read Grep Bash     # Intent scoping (not hard security!)
context: fork                     # Run in isolated subagent context
agent: sonnet                     # Use Sonnet model for the subagent
user-invocable: true              # Show in /skills list (false = background knowledge)
---
```

| Field | Effect | When to use |
|-------|--------|-------------|
| `disable-model-invocation` | Only manual trigger, never auto-detected | Critical actions: deploy, commit, delete |
| `allowed-tools` | Suggests which tools this skill needs | Scoping intent (not a hard security boundary!) |
| `context: fork` | Runs in a separate subagent context | Isolate the skill's context from your main session |
| `agent: <model>` | Specifies which model to use for the forked context | Cost control: use haiku for simple skills |
| `user-invocable: false` | Hides from command list, only auto-triggered | Background knowledge skills that Claude loads silently |

### Skill Discovery: `/skills`

Use `/skills` in any session to see all available skills — bundled, user, project, and plugin skills. Useful for discovering what's installed and available.

---

## Module 2.2: Hooks

**Learning Objectives:** After this module, you can:
- Map the 11 most-used hook events (PreToolUse, PostToolUse, Stop, SessionStart/End, UserPromptSubmit, PreCompact, SubagentStart/Stop, FileChanged, InstructionsLoaded, Notification) to concrete use cases.
- Write a hook entry in `settings.json` with the right matcher syntax (literal vs. regex), the `if` permission-rule filter, and one of the 5 execution types (command / http / prompt / agent / mcp_tool).
- Use advanced hook outputs (`updatedToolOutput`, `continueOnBlock`, `terminalSequence`) and `$CLAUDE_EFFORT` to build effort-aware, soft-blocking, redaction-capable hooks.

### The Core Idea

Hooks are automated actions that run in response to Claude Code events — without you having to remember to ask. They execute shell commands (scripts, binaries, echo statements, curl calls) at specific moments in Claude's workflow.

Think of hooks as **event listeners** for Claude's behavior. When something happens — Claude uses a tool, Claude finishes a response, Claude is about to run a bash command — a hook can fire.

### Hook Types

The official docs currently list **a couple dozen lifecycle events**. We focus on the 11 you will reach for most often:

| Event | When it fires | Typical use case |
|-------|---------------|------------------|
| **PreToolUse** | Before Claude uses a tool (bash, edit, MCP call). **Can block** by exiting non-zero | Prevent dangerous commands, enforce review before deploy, confirm irreversible actions |
| **PostToolUse** | After a tool runs and the result is back. Can react, log, trigger follow-ups | Audit log of every edit, Slack notification when tests pass, dashboard updates |
| **Stop** | Claude finishes a response and is waiting for the next user prompt | End-of-session summaries, cleanup tasks, status updates |
| **SessionStart** | Each time a Claude Code session starts | Briefing hook: print project status, check `git status`, verify dependencies are installed |
| **SessionEnd** | Clean exit (user runs `/exit` or closes the session) | Wrap-up hook: save session summary, archive logs, sync to wiki |
| **UserPromptSubmit** | The user submits a prompt (before Claude sees it) | Prompt validation, auto-append context (current branch, ticket ID), redact secrets |
| **PreCompact** | About to compress context to free tokens | Persist critical state to disk before it gets summarized away |
| **SubagentStart** | A subagent is being spawned | Inject extra instructions, log delegation, attach observers |
| **SubagentStop** | A subagent finishes | Capture the subagent's final report, write to audit log, trigger downstream agent |
| **FileChanged** | A tracked file changes (external editor, git pull, watcher) | React to external edits, re-run tests, invalidate caches |
| **InstructionsLoaded** | After CLAUDE.md / `.claude/rules/` loading finishes | Debug what was actually loaded into context, log effective instructions |
| **Notification** | Claude emits a notification (long task done, permission required) | Push to phone via Pushover, forward to Slack, blink the lights |

**Security analogy:** PreToolUse is the badge reader checking authorization *before* the door unlocks. PostToolUse is the door-open sensor logging the event *after*. SessionStart is the morning shift briefing. PreCompact is the moment before a guard hands off their notes — make sure the important details get written down before they fade.

### The Three Cornerstones in Detail

**PreToolUse — Before, Can Block.** Fires before Claude uses a tool (runs bash, edits a file, calls an MCP server). The hook receives information about what Claude is about to do. It can log the action, warn the user, or **block the action entirely** by exiting with a non-zero code.

**PostToolUse — After, Can React.** Fires after Claude uses a tool and receives the result. It can log what happened, trigger follow-up actions, send notifications, write to audit logs.

**Stop — When Claude Finishes.** Fires when Claude finishes a response and is waiting for the next user input. Use cases: end-of-session summaries, cleanup tasks, status updates.

### Security Analogy: Access Control Sensors

In an access control system:

- The **card reader** fires when someone presents a card. Before the door opens, the system checks: Is this card authorized? Is it within allowed hours? Is the area currently accessible? **This is PreToolUse** — a check that can block the action.

- A **door-open sensor** fires after the door opens and logs: who entered, when, which door. **This is PostToolUse** — reactive logging after the fact.

- An **end-of-shift alarm** fires at 18:00 to remind the control room to check that all zones are secured. **This is Stop** — a scheduled/trigger-based end event.

The sensors don't replace the guards. They automate the repetitive checking so guards can focus on exceptions.

### Hook Configuration

Hooks are configured in `settings.json`. There are two locations:

- `~/.claude/settings.json` — global, applies to all projects
- `.claude/settings.json` — project-level, only for this repo

The structure:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/pre-bash-check.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/audit-log.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Session ended' >> ~/.claude/session.log"
          }
        ]
      }
    ]
  }
}
```

The `matcher` field controls which tool calls the hook reacts to. The matching logic depends on the matcher's contents:

- If the matcher contains **only letters, digits, `_`, and `|`**, it is treated as an exact match or a pipe-separated list. `"Bash"` matches just the Bash tool; `"Bash|Edit|Write"` matches any of those three.
- If the matcher contains **any other special characters**, it is treated as a JavaScript regex. `".*"` matches all tools; `"Bash|^Edit$"` is also regex once `.` or `^`/`$` appear.

You can also add an `if` field for further filtering using **permission-rule syntax**, which is a much more semantic filter than tool-name regex alone:

```json
{
  "matcher": "Bash",
  "if": "Bash(git *)",
  "hooks": [...]
}
```

This hook fires only on Bash invocations that match the permission rule `Bash(git *)` — i.e., only git-related shell commands. The `if` syntax mirrors the same patterns you use in `permissions.allow` / `permissions.deny`.

### A Real Hook Example: Security Warning

This hook warns before any bash command containing `rm -rf` or `git push --force`:

**`~/.claude/hooks/pre-bash-check.sh`:**
```bash
#!/bin/bash

# Claude passes tool input via stdin as JSON
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.command // ""')

# Check for dangerous patterns
if echo "$COMMAND" | grep -qE 'rm\s+-rf|git push.*--force|DROP TABLE|truncate'; then
  echo "WARNING: Potentially destructive command detected: $COMMAND" >&2
  echo "Pausing for confirmation..." >&2
  # Exit 1 to BLOCK the command from running
  exit 1
fi

exit 0
```

When Claude tries to run `rm -rf /tmp/build`, this hook fires, prints the warning, and exits with code 1 — Claude Code sees the block and stops.

### What Hooks Can Do

1. **Block dangerous operations** — prevent `rm -rf`, force pushes, production deploys without approval
2. **Enforce standards** — require tests to pass before any file edit is committed
3. **Log activity** — write every tool call to an audit file for compliance
4. **Add guardrails** — warn when Claude touches files outside the project directory
5. **Automate workflows** — after a successful test run, automatically open a PR draft
6. **Security scanning** — check for secrets, API keys, or `innerHTML` assignments before committing

Hooks add **automated guards** to Claude Code — shell scripts that fire on specific lifecycle events. They are **best-effort** (a malformed matcher, missing executable bit, or hook timeout silently disables them), not a hard security boundary. Pair Hooks with proper permission rules and sandboxing for real isolation.

### Hook Execution Types

Hooks don't just run shell commands. There are five execution types:

| Type | How it works | Best for |
|------|-------------|----------|
| **command** | Runs a shell command (default) | Simple checks, scripts, logging |
| **http** | Sends HTTP request to a URL | Webhook notifications, external APIs |
| **prompt** | Sends a prompt to Claude for evaluation | Complex, context-aware decisions |
| **agent** | Spawns a subagent for evaluation | Multi-step validation logic |
| **mcp_tool** | Invokes an MCP tool directly | Notification to Slack via MCP, push to monitoring dashboard, structured external action without shelling out |

**Example: prompt hook** that evaluates whether a Bash command is safe:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this command is safe for a production environment. Block if it modifies system files, deletes data, or accesses network resources outside the project scope."
          }
        ]
      }
    ]
  }
}
```

### Component-Scoped Hooks: Hooks in Skill and Subagent Frontmatter

Hooks don't have to live in `settings.json`. They can also be **embedded in the frontmatter of a skill or subagent**, in which case they only run **while that component is active**. Outside the skill or subagent, the hook is silent.

This is a major 2026 feature that lets a skill ship its own pre- and post-checks without polluting global settings.

```yaml
---
name: deploy
description: Deploy the current branch to staging
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: Bash
      type: command
      command: ./pre-deploy-check.sh
  PostToolUse:
    - matcher: Bash
      type: command
      command: ./post-deploy-notify.sh
---
```

The `pre-deploy-check.sh` only fires while the deploy skill's context is active. As soon as the session leaves the skill, the hook is gone — no need to add a matcher that filters by skill name in a global hook.

**Security analogy:** A guard who is patrolling Zone A carries Zone-A-specific sensors. When they move to Zone B, those sensors don't come along — Zone B has its own. Component-scoped hooks are exactly that: localized, contextual, and they retire automatically.

### Advanced Hook Output — Rewriting, Soft-Blocking, Terminal Feedback

Beyond simply exiting 0 (allow) or non-zero (block), hooks can return a **structured JSON object** on stdout to control downstream behavior more precisely. Three fields matter in practice.

#### `updatedToolOutput` — Rewrite What Claude Sees (v2.1.119+)

A `PostToolUse` hook can **replace the tool's output before Claude reads it**. The original output is intercepted; Claude sees only the rewritten version.

```bash
#!/bin/bash
# ~/.claude/hooks/redact-secrets.sh
INPUT=$(cat)
OUTPUT=$(echo "$INPUT" | jq -r '.toolOutput')
REDACTED=$(echo "$OUTPUT" | sed -E 's/(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16})/[REDACTED]/g')
jq -n --arg out "$REDACTED" '{"hookSpecificOutput":{"updatedToolOutput":$out}}'
exit 0
```

**Use case:** Redact API keys, tokens, or PII out of tool output before Claude embeds them into its reasoning (and potentially into future messages). The model never sees the raw secret.

**Security analogy:** A redaction officer between the field operative and the briefing room — the report still reaches the analyst, but with the sensitive identifiers blacked out first.

#### `continueOnBlock: true` — Soft Warnings (v2.1.121+)

By default, a non-zero exit from a hook **stops Claude** in its tracks. With `continueOnBlock: true` on the hook entry, the block degrades to a **warning** — Claude is told what was blocked and why, but the turn continues.

```json
{
  "matcher": "Bash",
  "if": "Bash(git push *)",
  "continueOnBlock": true,
  "hooks": [
    { "type": "command", "command": "./audit-log-push.sh" }
  ]
}
```

**Use case:** Non-fatal audit logs ("we noticed a `git push` — entry written to the audit trail") where you want the action to proceed but want the hook's signal preserved in the transcript.

#### `terminalSequence` — ANSI Output to the User's Terminal (v2.1.139+)

A hook can return a `terminalSequence` field whose value is written **directly to the user's terminal** as raw ANSI escape sequences — independent of the model's reasoning stream.

```bash
#!/bin/bash
# Flash red status line when a destructive command was attempted
jq -n '{"terminalSequence":"[41;97m  DESTRUCTIVE COMMAND BLOCKED [0m\n"}'
exit 1
```

**Use case:** Colored warnings, status-bar updates, audible bells, anything that should reach the human operator's eyes without going through Claude's token budget.

#### `$CLAUDE_EFFORT` — Effort-Aware Hooks (v2.1.119+)

Every hook process gets the current effort level injected as an environment variable. This lets one hook script behave **differently depending on whether the user is on low/high/xhigh/max**.

```bash
#!/bin/bash
# Stricter scanning when the user requested xhigh / max effort
case "$CLAUDE_EFFORT" in
  xhigh|max)
    ./full-security-scan.sh
    ;;
  *)
    ./quick-pattern-check.sh
    ;;
esac
```

**Use case:** A pre-commit hook that runs a lightweight regex scanner during fast iteration but a full SAST sweep when the user explicitly cranked effort up — without registering two separate hooks. Hooks living inside skills can also branch on the *skill's* configured effort via the same variable.

### Circuit Breaker Pattern

> **Note:** Circuit Breaker is a *pattern* (not a built-in Claude Code feature).
> You implement it by writing a hook that tracks repeated identical tool calls.
> The example below shows the pattern; you'd need to write the actual hook script
> (a small shell or Python script that persists call counts in `~/.claude/state/`,
> matches on identical tool + arguments + exit code, and blocks once the threshold is crossed).

A critical hook pattern for preventing runaway token costs. When an agent executes the same command 3 times with the same error result, the hook detects the loop, stops the process, and asks the user for a strategy change.

**Security analogy:** A deadman switch in an alarm system. If the patrol guard stops checking in, the system escalates automatically. The circuit breaker prevents Claude from getting stuck in an "exploration trap" — endlessly retrying the same failing approach.

This is especially important when running autonomous loops or multi-agent workflows where token costs can escalate rapidly without human oversight.

---

## Module 2.3: Plugins

**Learning Objectives:** After this module, you can:
- Scaffold a plugin with the correct directory layout (`.claude-plugin/plugin.json`, `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`) and validate it with `claude plugin validate`.
- Choose the right plugin scope (user / project / local / managed) for a given distribution scenario and use `claude plugin install/enable/disable/uninstall/prune` to manage the lifecycle.
- Identify supply-chain risks of third-party plugins and apply mitigations (review code, pin versions, project scope for team plugins, inspect via `/plugin`).

### The Core Idea

As you accumulate skills, hooks, agents, and commands, you want to package them together. A **plugin** is that package — a self-contained, distributable bundle that adds a coherent set of capabilities to Claude Code.

A plugin might contain:
- A set of related skills (e.g., all skills for code review workflows)
- Custom commands (e.g., `/review`, `/security-scan`)
- Agents (autonomous sub-processes that run within Claude)
- Hooks (automated behaviors)
- All wired together with shared context

### Security Analogy: Security Module

Think of a physical security system's **module** — say, a biometric access module. It contains:
- The fingerprint scanner hardware (sensors = hooks)
- The matching algorithm (logic = agents)
- The standard procedures for access granted/denied (procedures = skills)
- The control panel buttons (user interface = commands)
- The wiring diagram and configuration (metadata = plugin.json)

You buy the module, install it, and it integrates with your existing system. It's self-contained. You don't have to build each piece from scratch.

A Claude Code plugin is the same idea: install it once, and you get a coherent set of new capabilities.

### Plugin Structure

```
~/.claude/plugins/cache/my-plugin-marketplace/
  .claude-plugin/
    plugin.json            # MUST be here, not in the plugin root
  skills/
    my-skill/
      SKILL.md             # skill instructions
    another-skill/
      SKILL.md
  commands/
    my-command.md          # command-style entry points (disable-model-invocation: true)
    another-command.md
  agents/
    my-agent.md            # subagent definitions
  hooks/
    hooks.json             # plugin-bundled hook config (JSON schema = settings.json hooks)
  monitors/
    monitors.json          # background-monitor definitions (poll logs, PRs, files)
  scripts/
    setup.sh               # install/setup scripts run on plugin install
    teardown.sh
  bin/                     # PATH-injected executables (HANDLE WITH CARE)
    my-cli
  .mcp.json                # bundled MCP servers (loaded with the plugin)
  .lsp.json                # bundled LSP server configurations
  settings.json            # plugin-default settings (default agent, statusline, etc.)
```

> **Correction vs. earlier versions:** The plugin manifest is **`.claude-plugin/plugin.json`**, not `plugin.json` in the plugin root. Putting `plugin.json` at the root no longer works with the current spec. If you scaffold a plugin and Claude Code "doesn't see it," check this first.

> **`hooks/pre-tool-use.sh` is deprecated.** Earlier workshop materials and older plugins shipped raw shell files under `hooks/`. Current spec is `hooks/hooks.json` with the same JSON schema as the `hooks` block in `settings.json`. The shell file (if you still need one) is referenced from inside the JSON via `"command": "${CLAUDE_PLUGIN_ROOT}/hooks/pre-tool-use.sh"`.

**`.claude-plugin/plugin.json`** — the manifest:
```json
{
  "name": "my-plugin",
  "version": "2.1.0",
  "description": "A plugin for automated code review and security scanning",
  "author": "your-name",
  "dependencies": [],
  "enabled": true
}
```

Most fields (skills, commands, agents, hooks, MCP servers) are now **auto-discovered** from the directory layout — you don't have to repeat them in the manifest. Just put them in the right folder, name them sensibly, and the plugin loader picks them up.

To disable a plugin without deleting it, use `claude plugin disable <name>` rather than renaming files manually.

### Official Marketplaces

Anthropic runs two first-party plugin marketplaces:

- **`claude-plugins-official`** — curated by Anthropic, auto-available to every Claude Code installation. High quality bar, internally reviewed.
- **`claude-community`** — public submissions, lower bar, broader selection. Anthropic does not vet each plugin individually.

Add a marketplace once, then install plugins from it by `<name>@<marketplace>`:

```bash
# Add the community marketplace
/plugin marketplace add anthropics/claude-plugins-community

# Install a specific plugin from a specific marketplace
/plugin install code-review@claude-plugins-official
/plugin install some-niche-plugin@claude-community
```

**Submission flow:** To publish your own plugin, go to `claude.ai/settings/plugins/submit`. The form points to your plugin's git repository, Anthropic runs basic validation, and once approved it lands in `claude-community`. Getting into `claude-plugins-official` is a separate, higher-bar review.

### Notable Plugins in the Ecosystem

> **Custom Components:** The plugins listed below (`agentic-os`, `devil-advocate-swarms`,
> `multi-model-orchestrator`, `superpowers`, `hookify`) are **custom-built extensions**,
> not part of the official Claude Code installation. They demonstrate what's possible
> with the plugin system. The patterns they implement (adversarial testing, multi-model
> pipelines, meta-cognition workflows) are real — the specific implementations are our own.

**agentic-os** — the core orchestration plugin. Contains session bootstrapping, self-improvement loops, quality gates, research pipeline, iteration logging, and wrap-up workflows. Most other plugins depend on it.

**devil-advocate-swarms** — adversarial analysis. Spawns multiple Claude agents that argue against your implementation. Finds flaws through structured disagreement.

**multi-model-orchestrator** — routes tasks between Claude, Codex, and other models. Coordinates parallel agent execution. Contains the codex-swarm command for spawning multiple coding agents simultaneously.

**superpowers** — meta-cognition skills. Teaches Claude Code how to reason about its own workflow: when to brainstorm vs. plan vs. execute, how to do TDD, how to review code systematically.

**hookify** — makes it easy to create and manage hooks through a guided interface instead of editing JSON directly.

### Plugin Scopes

Plugins can be installed at different scopes — controlling who gets them and who controls them:

| Scope | Config Location | Who controls | Use case |
|-------|----------------|-------------|----------|
| **user** | `~/.claude/settings.json` | Individual developer | Personal tools |
| **project** | `.claude/settings.json` | Team (checked into repo) | Shared team tools |
| **local** | `.claude/settings.local.json` | Individual (not shared) | Personal overrides |
| **managed** | Org-managed settings | Enterprise admin | Organization-wide policies |

**Security analogy:** Like access control zones. User scope = your personal locker. Project scope = the team equipment room. Managed scope = the building-wide security policy that nobody except the security manager can change.

### Plugin CLI Management

```bash
# Install from marketplace or git
claude plugin install <source>        # --scope user|project

# Manage installed plugins
claude plugin list                    # Show all plugins
claude plugin enable <name>           # Enable a disabled plugin (pulls transitive deps)
claude plugin disable <name>          # Disable without removing (blocks if others depend on it)
claude plugin uninstall <name>        # Remove completely
claude plugin update <name>           # Update to latest version
claude plugin validate <path>         # Local pre-submission schema/structure check
claude plugin prune                   # Remove orphaned dependencies left over from uninstalls

# Test local plugin during development
claude --plugin-dir ./my-plugin       # Load from local directory
claude --plugin-dir ./my-plugin.zip   # Load directly from a zipped plugin (v2.1.128+)
claude --plugin-url <url>             # Load plugin from remote URL (v2.1.129+)

# In-session management
/plugin                               # Interactive plugin manager
/reload-plugins                       # Hot-reload after changes
```

Since v2.1.128 the `--plugin-dir` flag also accepts a `.zip` archive directly — useful for plugin authors who want to test the **packaged** artifact they will eventually submit to a marketplace, without unzipping it into a working tree first.

### Pinning the Claude Code CLI Version

`claude install` re-installs the CLI. Without an argument it pulls the **latest** stable build (the default behavior most users rely on). With an explicit version, it **pins** to that exact build:

```bash
claude install              # latest stable
claude install 2.1.140      # pin to 2.1.140 exactly
```

**Use case:** Team consistency — every developer on the project runs the same CLI build, so plugin and hook behavior matches. Also valuable in CI, where an automatic upgrade between runs can silently change schema validation or hook semantics. Pin the version your CI tested against; upgrade deliberately.

**Caution:** Plain `claude install` *will* upgrade you. If you specifically want today's pinned version to stay pinned, do not run `claude install` without an argument.

### Plugin Dependencies

Plugins can declare dependencies on other plugins via the `dependencies:` field in `.claude-plugin/plugin.json`. The CLI manages them automatically:

- `claude plugin enable <name>` — pulls in transitive dependencies. Enabling a plugin that depends on `agentic-os` will enable `agentic-os` too if it isn't already.
- `claude plugin disable <name>` — refuses to disable a plugin if other enabled plugins depend on it. You'll see a clear "blocked by: X, Y" message. Disable the dependents first, or use `--force` if you really mean it.
- `claude plugin prune` — sweeps orphaned dependencies that were pulled in transitively but whose dependents have since been uninstalled.

### Plugin Security: Supply Chain Risks

**Important warning from the official Plugin Directory:** Plugin contents (MCP servers, files, executables) are not fully controllable by Anthropic. Only install plugins you trust.

Real supply chain risks:
- Abandoned repos can be hijacked — a new maintainer pushes malicious code
- Plugin `bin/` executables run with your user permissions
- Plugin hooks execute shell commands in your environment
- Plugin MCP servers can access external systems

**Mitigation:** Review plugin code before installing. Pin versions. Use project scope (not user) for team plugins so changes go through code review. Use `/plugin` to inspect what's installed.

---

## Module 2.4: MCP (Model Context Protocol)

**Learning Objectives:** After this module, you can:
- Choose the right MCP transport (HTTP / stdio / SSE) and scope (local / project / user) for a given integration and configure it via `claude mcp add` or `.mcp.json`.
- Configure OAuth-enabled MCP servers with `--callback-port`, `--client-id`, `--client-secret` and use `${VAR:-default}` env-var expansion for safe team-shared `.mcp.json` files.
- Recognize MCP-specific risks (prompt injection from untrusted content, token theft, output flooding) and apply mitigations (output limits, permission rules, trusted-server policy).

### The Core Idea

By default, Claude Code can read files, run bash commands, and search the web. MCP (Model Context Protocol) extends this with **connections to external services** — giving Claude Code access to real browsers, databases, communication platforms, and custom APIs.

MCP is an open standard (developed by Anthropic, now adopted broadly). Any service can implement an MCP server, and Claude Code can connect to it. The protocol defines how tools, resources, and prompts are exposed from external systems to the AI.

### Security Analogy: Integrated Building Management

A modern building management system doesn't just control doors in isolation. It **integrates**:
- Fire alarm system — automatic lockdown on smoke detection
- CCTV — camera feeds accessible from the access control console
- Visitor management — pre-authorized visitors appear in the door system
- HR system — employee terminations automatically revoke card access
- Time & attendance — door logs feed into payroll

Each external system exposes an interface. The central control system connects to all of them. Claude Code + MCP works the same way: Claude is the control system, external services expose MCP interfaces, and you configure the connections.

### Available MCP Servers

**Playwright (Browser Control)**
The most powerful for developers. Gives Claude a real browser it can control:
- Navigate to URLs
- Click buttons and links
- Fill forms
- Take screenshots
- Read page content
- Execute JavaScript

Use cases: automating admin panels, scraping dynamic content, testing UI flows, monitoring dashboards.

**Slack**
Read channels, send messages, search conversations. Use cases: Claude can notify your team when tests fail, post deployment summaries, answer questions by searching Slack history.

**Gmail / Google Calendar**
Read emails, create drafts, manage calendar events. Use cases: Claude can draft responses, schedule meetings, parse meeting notes into tasks.

**Databases (PostgreSQL, SQLite, etc.)**
Query databases directly. Claude can analyze data, generate reports, find anomalies without you writing SQL by hand.

**Context7** (documentation lookup)
Fetches current documentation for any library or framework. Prevents hallucination on API syntax by pulling real, current docs.

**Custom MCP Servers**
Any team can build an MCP server that exposes their internal tools. Deploy pipeline? Monitoring system? Bug tracker? Expose it via MCP and Claude can interact with it directly.

### MCP Transport Types

MCP servers communicate with Claude Code via different transport protocols:

| Transport | How it works | Best for | Status |
|-----------|-------------|----------|--------|
| **HTTP** | Remote server over HTTPS | Cloud services, shared team servers | **Recommended** |
| **stdio** | Local process, communicates via stdin/stdout | Local tools, custom scripts, system access | Good for development |
| **SSE** | Server-Sent Events | (legacy) | **Deprecated** — use HTTP instead |

### MCP Scopes

MCP servers, like plugins, live at different scopes. **The scope names changed in 2026 — beware older documentation.**

| Current name | Was called (old docs) | What it means |
|--------------|----------------------|---------------|
| **local** | `project` | Per-user, per-project. Stored in user config but tied to one project on this machine |
| **project** | (new) | Shared with the team via committed `.mcp.json` in the repo |
| **user** | `global` | Available across all of your projects |

If you read older docs and see "project scope = .mcp.json" — that is now called **project**. If you see "global scope" — that is now called **user**. The mechanics are the same; only the names moved.

### MCP CLI Management

```bash
# Add remote HTTP server (recommended for cloud services)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Add with auth header
claude mcp add --transport http --header "Authorization: Bearer xxx" myapi https://api.example.com/mcp

# Add local stdio server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Add with environment variables
claude mcp add --transport stdio --env GITHUB_TOKEN=xxx github -- npx -y @modelcontextprotocol/server-github

# Add a complex config inline as JSON (skips per-flag bookkeeping)
claude mcp add-json my-server '{"command":"npx","args":["-y","my-package"],"env":{"FOO":"bar"}}'

# Reset stored Approve/Decline choices for project-scope .mcp.json servers
claude mcp reset-project-choices

# Manage servers
claude mcp list                  # List all configured servers
claude mcp get <name>            # Show server details
claude mcp remove <name>         # Remove a server

# Load servers from config file
claude --mcp-config servers.json     # Load additional MCP config
claude --strict-mcp-config           # ONLY use servers from config (no others)

# In-session
/mcp                             # Check status, manage OAuth, troubleshoot
```

### MCP OAuth

Claude Code supports OAuth flows for compatible remote MCP servers. When you connect to an OAuth-enabled server, Claude opens a browser for authentication and listens on a callback port.

For team / enterprise setups, you usually want **pre-configured** credentials so every developer connects to the same OAuth app instead of registering a fresh one each time:

```bash
claude mcp add \
  --transport http \
  --callback-port 9876 \
  --client-id "team-shared-client-id" \
  --client-secret "team-shared-secret" \
  notion https://mcp.notion.com/mcp
```

| Flag | Purpose |
|------|---------|
| `--callback-port <port>` | Pin the OAuth callback to a fixed port. Required when corporate firewalls only allow specific ports |
| `--client-id <id>` | Reuse a pre-registered OAuth app. Important when the MCP server only knows your team's client ID |
| `--client-secret <secret>` | The matching secret. Treat this like any other secret — pass via env var or secret manager, not in shell history |

Use case: an enterprise that has a single Notion OAuth app registered for the company. Every developer's Claude Code uses the same client ID/secret pair and authenticates against that app, instead of each developer triggering a new "Authorize MyApp" dialog in Notion's admin UI.

### MCP Output Limits

Large MCP tool outputs can flood your context window. Claude Code has built-in limits:

| Threshold | Value | What happens |
|-----------|-------|-------------|
| Warning | 10k tokens | Claude warns about large output |
| Default max | 25k tokens | Output truncated beyond this |
| Per-tool override | up to 500k chars | Set via `_meta["anthropic/maxResultSizeChars"]` |

This matters especially for database queries (MCP Postgres) or large file listings. If you need more data, use the `_meta` override on the specific MCP tool — but be aware of the context cost.

### MCP Security

**Official Anthropic warning:** Third-party MCP servers are "use at your own risk." Anthropic does not audit them.

Key risks:
- **Prompt injection** — MCP servers that fetch untrusted content (web pages, tickets, emails) can inject instructions into Claude's context
- **Data exfiltration** — a malicious MCP server could read your project files via tool calls
- **Token theft** — OAuth tokens stored for MCP servers could be compromised

**Mitigation:** Only install trusted servers. Use `/mcp` to inspect what's connected. Use permissions to limit what Claude can do with MCP tools. Consider sandboxing for high-risk integrations.

### MCP Configuration (File-Based)

MCP servers can also be configured in `.mcp.json` (project-level) or `~/.claude/.mcp.json` (user-level):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {}
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN:-default-dev-token}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${PG_URL:-postgresql://user:pass@localhost/mydb}"
      }
    }
  }
}
```

**Environment variable expansion** supports two forms:

- `${VAR}` — substitutes the value of `VAR`. Fails if unset.
- `${VAR:-default}` — substitutes the value of `VAR`, or falls back to `default` if `VAR` is unset or empty.

The `:-default` form is the safe choice for shared `.mcp.json` files committed to a repo: every dev gets a sensible fallback, but production overrides via the real env var.

Claude Code reads this config at startup and connects to each server. The tools then appear in Claude's available tool list automatically.

### Channels (Research Preview)

A traditional MCP server is **pull-only**: Claude calls a tool, the server replies. **Channels** flip that model — they let an MCP server **push** messages into a running Claude Code session asynchronously.

Use cases:
- CI server pushes "build done" into your active session
- A Slack mention shows up as a notification in Claude Code
- An external monitoring system tells Claude that an alert just fired

Status: **research preview**. The documentation lives at `code.claude.com/docs/en/channels`. Treat it as experimental — the API may change before GA. But conceptually it is what replaces the custom "Telegram bridge" pattern many teams build by hand.

### Protocol Details Worth Knowing

A handful of small protocol-level features that rarely make it into headline docs but matter once you build or operate an MCP server:

**`streamable-http` alias for `http`.** Inside `.mcp.json` you may see `"type": "http"` or `"type": "streamable-http"`. Both work identically; `streamable-http` is the explicit name from the MCP spec and tends to appear in official upstream documentation. Either form is fine — pick one for consistency inside a single config file.

**Dynamic tool updates via `list_changed`.** A server is allowed to **add or remove tools during a running session**. After a state change (for example: the user just logged in, unlocking a new tool family) the server emits a `list_changed` notification and Claude Code refreshes the tool catalog without a restart. Useful for OAuth-gated servers that legitimately expose more capability after authentication.

**Automatic reconnection with exponential backoff.** When the transport drops (flaky network, server restart, tunnel rotation), Claude Code retries with backoff: **1s, 2s, 4s, ... capped at 30s**. Calls in flight return a transient error that the model can choose to retry. The `/mcp` panel surfaces reconnect attempts in real time, so you can tell at a glance whether a server is genuinely down or just slow.

**`CLAUDE_PROJECT_DIR` for stdio servers.** When Claude Code launches a stdio MCP server, the child process inherits an env var `CLAUDE_PROJECT_DIR` pointing at the current project root. Use this from inside the server to read project files via stable relative paths rather than relying on the CWD the user happened to launch from.

```python
# In a Python stdio MCP server
project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
config_path = pathlib.Path(project_dir) / ".myteam" / "rules.yaml"
```

This is the canonical way for a server to find the project it is serving — do not parse `argv` or call `git rev-parse`; the env var is authoritative.

### What MCP Changes

Without MCP: Claude is a powerful assistant that works with your local filesystem and terminal.

With MCP: Claude becomes an **orchestrator** that can:
- Control browsers to automate web workflows
- Read Slack and draft responses in your name
- Query your databases and generate reports
- Monitor your CI/CD pipeline and act on failures
- Interact with any system your organization uses

The boundary between "AI assistant" and "automated agent" blurs significantly with MCP. This is why hooks and guardrails (Module 2.2) matter more when MCP is involved.

### Build Your Own MCP Server

When existing MCP servers don't cover your needs (internal APIs, custom databases, proprietary
tools), you write your own. Here's a minimal Python MCP server skeleton using `fastmcp`:

```python
# my_mcp_server.py
from fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def get_user_count(date: str) -> int:
    """Return the number of registered users on a given date."""
    # Your custom logic here — query DB, call API, etc.
    import sqlite3
    conn = sqlite3.connect("users.db")
    cur = conn.execute("SELECT COUNT(*) FROM users WHERE date(created_at) = ?", (date,))
    return cur.fetchone()[0]

@mcp.tool()
def list_active_features() -> list[str]:
    """Return active feature flags."""
    # Read from your config / feature-flag service
    return ["new_dashboard", "experimental_search"]

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python3",
      "args": ["my_mcp_server.py"]
    }
  }
}
```

Now Claude Code can call `get_user_count` and `list_active_features` as tools. The same pattern
works in Node.js (`@modelcontextprotocol/sdk`) or any language with an MCP SDK.

**For HTTP MCP servers** (recommended for shared team services): swap `transport="stdio"` for
`transport="http"` and run as a regular HTTPS service. Then in `.mcp.json`:

```json
{
  "mcpServers": {
    "my-team-tools": {
      "type": "http",
      "url": "https://mcp.corp.example/tools"
    }
  }
}
```

**Common patterns to expose via MCP:**
- Internal API gateways (Jira, ServiceNow, internal Wiki)
- Database queries (PostgreSQL, Snowflake, ClickHouse)
- Build/CI status (Jenkins, ArgoCD)
- Monitoring (Prometheus, Grafana, Datadog)
- Custom protocol parsers (OSDP, BACnet, Modbus — relevant for Physical Security)

The MCP server becomes the **shared knowledge layer** for your team's Claude Code workflows.

---

## Module 2.5: RAG & NotebookLM

**Learning Objectives:** After this module, you can:
- Explain when RAG beats general-knowledge LLM answers (training cutoff, internal docs, niche domains) and when it doesn't (chunk-boundary issues, retrieval-rank failures).
- Build a NotebookLM-backed knowledge source end-to-end (`notebooklm create` / `add-source` / `use` / `ask`) and route Claude Code queries to it.
- Decide whether a given codebase is suitable for NotebookLM (Google-hosted, source content leaves your perimeter) or whether a local RAG alternative is required.

### The Problem: Training Cutoff and Niche Knowledge

Claude's training data has a cutoff date. Ask about a library released last month and Claude might guess, hallucinate plausible-looking but wrong API calls, or admit uncertainty.

Beyond recency, there's specificity: your internal APIs, your organization's coding standards, your proprietary architecture decisions, your team's accumulated knowledge — none of this is in Claude's training data. It doesn't exist in the general internet either.

**RAG (Retrieval-Augmented Generation)** solves this: instead of relying solely on training data, you give Claude access to a specific, curated knowledge base. When Claude needs to answer a question, it retrieves relevant content from your sources first, then generates an answer grounded in that material.

### Security Analogy: Building Blueprints vs. General Knowledge

Imagine hiring a security consultant. You could say: "We have a 3-story office building, here are the floor plans, here is our current access log format, here is our incident history." The consultant works from *your actual blueprints*.

Or you could say nothing and let them work from "general security knowledge." They'll give reasonable advice — but it won't match your specific door numbering, your particular alarm zones, your actual cable runs.

RAG is giving the consultant your actual blueprints. **Verified, specific, current knowledge — not generalizations.**

### NotebookLM: RAG Without Infrastructure

Building a RAG system from scratch requires: embedding model, vector database, chunking pipeline, retrieval logic, prompt engineering. It's a real engineering project.

**Google NotebookLM** is a hosted RAG system you can use immediately:

1. Create a notebook in NotebookLM
2. Add sources: URLs, PDFs, YouTube videos, text pastes, Google Docs
3. NotebookLM indexes and embeds everything
4. Query it via the web UI or API

> **Data Flow Disclosure:** NotebookLM is hosted by Google. Any source you add to a notebook
> (URLs, PDFs, text pastes, code snippets) is uploaded to Google's servers and indexed by their
> embedding pipeline. Depending on your account type:
> - **Personal NotebookLM (free):** Standard Google data policies apply
> - **Workspace NotebookLM:** Enterprise data policies apply
>
> **Implications for source-code projects:**
> - Do NOT add proprietary source code to a NotebookLM notebook unless your company allows
>   sharing with Google Workspace
> - For sensitive code, use local RAG alternatives (e.g., custom MCP server with local vector DB)
> - For documentation, regulatory texts, or public references — NotebookLM is appropriate

> **Custom Component:** The `notebooklm` user skill shown below is a **custom-built wrapper**,
> not part of the official Claude Code installation. It demonstrates how RAG can be integrated
> via custom skills. Without this skill, use the NotebookLM web UI and bring results into
> Claude Code via `@`-file includes.

> **Setup required:** This demo uses the `notebooklm` user skill, which must be installed
> before the demo runs. See **`prerequisites.md`** for installation instructions. If the
> skill is not installed, the `notebooklm ...` commands below will not be recognized.

### Notation convention

In this module we use two notations:

- `notebooklm <cmd>` — calling the CLI directly. This is what you type in a terminal, or what a skill invokes via `Bash`.
- `/notebooklm <cmd>` — invoking the user skill from within a Claude Code session. The skill internally calls the same CLI.

We use the **CLI form** in the rest of this module, matching the user skill's behavior. If you prefer to invoke it as a slash command, replace `notebooklm` with `/notebooklm` mentally.

### The Full Workflow

Throughout the workflow we use a single example notebook — `claude-code-docs` — so the commands chain together cleanly.

**Step 1: Create a Notebook**
```bash
notebooklm create "Claude Code Docs"
```

**Step 2: Add Sources**
```bash
notebooklm add-source claude-code-docs https://code.claude.com/docs/en/overview
notebooklm add-source claude-code-docs https://code.claude.com/docs/en/hooks
notebooklm add-source claude-code-docs https://code.claude.com/docs/en/skills
# Also accepts PDFs, internal docs, YouTube tutorial transcripts
```

**Step 3: Query from Claude Code**
```bash
notebooklm use claude-code-docs
notebooklm ask "What is the correct format for hook configuration in settings.json?"
```

NotebookLM returns the answer with citations to specific source pages — verifiable, not hallucinated.

### Use Cases

**Internal documentation**
Add your team's Confluence pages, architecture decision records, runbooks. Claude can answer "how do we handle database migrations in this project?" with your actual documented process.

**API documentation (current)**
Add the latest API docs for any library. Claude answers with current syntax, not potentially stale training data.

**Research collections**
Gather papers, articles, blog posts on a topic. Ask Claude to synthesize, compare approaches, identify gaps.

**Curated best practices**
Build a notebook of "how we do things here" — coding standards, review checklist, deployment checklist. Claude follows your actual standards, not generic advice.

**Regulatory / compliance knowledge**
Add the specific regulations your industry operates under. Claude's compliance advice cites your actual regulatory text.

### Why This Matters for Experienced Developers

If you're building anything non-trivial with Claude Code, you will eventually hit the limits of its general knowledge. The pattern that scales is:

1. Identify what Claude needs to know that isn't in its training
2. Build a notebook with those sources
3. Configure Claude Code to check the notebook before answering questions in that domain

This grounds Claude's answers in **your actual documentation** — Claude cites specific sources, you can verify them, and reduce hallucinations on your stack-specific questions. It is not "expertise upgrade" in the deep-learning sense — it is **document retrieval + citation**, with all the limitations that come with it (see below).

### RAG Limitations

NotebookLM (and any RAG system) has known failure modes:

- **Chunk boundary problems:** A relevant answer may be split across two chunks; retrieval misses one
- **Embedding drift:** As the source corpus grows, the most-relevant chunks may shift in surprising ways
- **Citation hallucination:** Claude may cite a real source but paraphrase incorrectly — always click through to verify
- **Stale indexing:** A new source isn't queryable until indexing completes (can take minutes)
- **Retrieval rank failures:** A vital source ranks low and isn't included in the top-K retrieved chunks

For high-stakes answers: ask Claude to **always cite** the specific source page, then verify manually.

---

## Summary: The Ecosystem Stack

```
┌─────────────────────────────────────────────────────┐
│                   Your Workflow                      │
├─────────────────────────────────────────────────────┤
│  Commands (/tdd, /commit)  →  Skills (SKILL.md)     │ ← Module 2.1
├─────────────────────────────────────────────────────┤
│  Hooks (PreToolUse, PostToolUse, Stop)               │ ← Module 2.2
├─────────────────────────────────────────────────────┤
│  Plugins (bundle of skills + commands + agents)      │ ← Module 2.3
├─────────────────────────────────────────────────────┤
│  MCP (Playwright, Slack, DBs, custom services)       │ ← Module 2.4
├─────────────────────────────────────────────────────┤
│  RAG / NotebookLM (your knowledge base)              │ ← Module 2.5
└─────────────────────────────────────────────────────┘
```

Each layer extends Claude Code's reach — from automating your own workflow (skills/commands), to enforcing policies automatically (hooks), to deploying shared team capabilities (plugins), to connecting external systems (MCP), to grounding Claude in your specific knowledge (RAG).
