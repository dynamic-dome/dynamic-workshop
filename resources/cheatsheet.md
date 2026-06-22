# Claude Code Cheatsheet

> Quick reference for the Claude Code Dynamic Workshop

---

## Installation & Setup

```bash
# Install (macOS/Linux/WSL) — recommended
curl -fsSL https://claude.ai/install.sh | bash

# Install (Windows PowerShell)
irm https://claude.ai/install.ps1 | iex

# Install via npm (alternative, requires Node.js 18+)
npm install -g @anthropic-ai/claude-code

# Homebrew (macOS, no auto-updates)
brew install --cask claude-code

# Update existing installation
claude update

# Verify installation
claude --version

# Authenticate
claude /login

# Desktop App: download from claude.ai/code (Mac/Windows)
# Web App: claude.ai/code (browser-based)
```

**System Requirements:** 4 GB RAM (8 GB recommended), Node.js 18+, Git for Windows (mandatory on Windows)

---

## CLI Flags

| Flag | What it does |
|------|-------------|
| `claude` | Start interactive session |
| `claude "task"` | Start with a specific task |
| `claude -c` / `--continue` | Continue last conversation |
| `claude -r` / `--resume <id>` | Resume a named session |
| `claude -p "prompt"` / `--print` | Non-interactive mode, stdout only (CI/scripts) |
| `claude --output-format json` | JSON output (pairs with --print) |
| `claude --json-schema <schema>` | Validated JSON output (structured outputs) |
| `claude --model sonnet` | Use a specific model (opus, sonnet, haiku) |
| `claude --permission-mode <mode>` | Set permission mode (see Permission System) |
| `claude --dangerously-skip-permissions` | Auto-accept all tool use (use with caution!) |
| `claude --allowedTools "Edit,Read"` | Whitelist specific tools |
| `claude --add-dir /path` | Add additional working directory |
| `claude --verbose` | Show debug output |
| `claude --debug <category>` | Filter debug output by category (more granular than `--verbose`) |
| `claude --worktree <branch>` / `-w` | Auto-create worktree under `<repo>/.claude/worktrees/<name>` |
| `claude --mcp-config <file>` | Load MCP servers from JSON file |
| `claude --strict-mcp-config` | Only use MCP servers from config |
| `claude --plugin-dir <path>` | Load local plugin directory (accepts `.zip`) |
| `claude --plugin-url <url>` | Load remote plugin from URL (v2.1.129+) |
| `claude --bare` | Headless mode without Hooks/Skills/Plugins/MCP/AutoMemory |
| `claude --tools <list>` | Restrict tools (different from `--allowedTools` allowlist) |
| `claude --max-budget-usd <amount>` | Cost cap per `-p` run |
| `claude --append-system-prompt "..."` | Add persona text to system prompt |
| `claude --system-prompt "..."` | Full persona override |
| `claude --system-prompt-file <path>` | Load persona from file |
| `claude --teleport` | Pull Web-Session into local terminal |
| `claude --bg` | Start as background-agent (use with `claude agents`) |
| `claude --from-pr <num>` | Resume session attached to a PR |
| `claude --fork-session` | Generate new session-ID when used with `--resume` |
| `claude --remote-control` / `--rc` | Start remote-control session |
| `claude --tmux` | Spawn tmux session for worktree |
| `claude --agents '<json>'` | Inline subagent definition via JSON |
| `claude --setting-sources <list>` | Override which settings sources to load |
| `claude --permission-mode auto` | Auto-Mode (replaces removed `--enable-auto-mode`; also via Shift+Tab cycle) |

---

## CLI Subcommands

```bash
# Authentication
claude auth login          # Login (OAuth or API key)
claude auth logout         # Logout
claude auth status         # Check auth status

# MCP Server Management
claude mcp add <name> -- <command>              # Add stdio MCP server
claude mcp add --transport http <name> <url>    # Add HTTP MCP server (recommended)
claude mcp add-json <name> '<json>'             # Add via inline JSON config
claude mcp list                                  # List configured servers
claude mcp get <name>                            # Show server details
claude mcp remove <name>                         # Remove server
claude mcp reset-project-choices                 # Reset .mcp.json approval prompts

# Plugin Management
claude plugin install <source>    # Install plugin (marketplace/git/local)
claude plugin uninstall <name>    # Remove plugin
claude plugin enable <name>       # Enable disabled plugin (auto-pulls deps)
claude plugin disable <name>      # Disable plugin (blocked if others depend on it)
claude plugin update <name>       # Update plugin
claude plugin validate            # Local pre-submission check
claude plugin prune               # Cleanup orphaned dependencies
claude plugin marketplace add <owner/repo>  # Add a marketplace

# Background Agents (v2.1.139+)
claude agents                      # Live view of running background sessions
claude attach <id>                 # Attach to background session
claude logs <id>                   # Stream logs from background session
claude stop <id>                   # Stop a background session
claude respawn <id>                # Respawn a stopped session
claude rm <id>                     # Remove a session entry

# Other
claude update                     # Update Claude Code CLI
claude install [version]          # Pin a specific version
claude remote-control             # Start remote control session
claude ultrareview [target]       # Cloud-based multi-agent code review
claude setup-token                # Long-lived OAuth token for CI (~1 year)
claude project purge [path]       # Complete reset of a project
claude auto-mode defaults         # Print auto-mode classifier rules
```

---

## Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Enter` | Send message |
| `Shift+Enter` | Newline in input |
| `Shift+Tab` | Cycle modes: Normal → Auto-accept → Plan |
| `Escape` | Cancel current generation |
| `Ctrl+C` | Interrupt / cancel |
| `Ctrl+L` | Clear screen |
| `Up/Down` | Navigate input history |
| `Tab` | Accept suggestion / autocomplete |

---

## Slash Commands

### Session Management
| Command | What it does |
|---------|-------------|
| `/help` | Show available commands |
| `/status` | Show current session status |
| `/clear` | Reset conversation context (aliases: `/reset`, `/new`) |
| `/compact [focus]` | Compress context to free up tokens |
| `/resume <name>` | Resume a named session |
| `/rename "name"` | Rename current session |
| `/export [file]` | Export conversation to file |
| `/branch` / `/fork` | Branch conversation (experiment safely) |
| `/btw <question>` | Side-question without polluting context |
| `/copy [n]` | Copy last assistant output to clipboard |
| `/exit` | Exit CLI |

### Models & Context
| Command | What it does |
|---------|-------------|
| `/model <name>` | Switch model (opus, sonnet, haiku) |
| `/fast` | Toggle fast output mode |
| `/effort <level>` | Set effort level (low/high/xhigh/max) — controls thinking depth |
| `/context` | Visualize context window usage |
| `/cost` | Show token usage and cost for session |
| `/usage` | Show rate limits and subscription status |
| `/stats` | Show usage streaks and patterns |

### Project & Memory
| Command | What it does |
|---------|-------------|
| `/init` | Initialize/improve project CLAUDE.md |
| `/memory` | Manage auto-memory and CLAUDE.md |
| `/plan [task]` | Enter planning mode (think before acting) |
| `/diff` | Interactive diff viewer |
| `/rewind` | Rewind to checkpoint (undo multiple steps) |

### Configuration
| Command | What it does |
|---------|-------------|
| `/config` | View/change settings (alias: `/settings`) |
| `/permissions` | Change permission mode and rules |
| `/hooks` | View hook configurations |
| `/skills` | List all available skills |
| `/plugin` | Manage plugins |
| `/sandbox` | Toggle OS-level sandbox mode |
| `/keybindings` | Configure keyboard shortcuts |
| `/theme` | Change visual theme |
| `/color <color>` | Change prompt bar color |
| `/statusline` | Configure status line |
| `/output-styles` | Switch persona/output style (Concise/Detailed/JSON) |
| `/terminal-setup` | Optimize terminal for Claude Code |
| `/setup-bedrock` | Cloud provider setup wizard (AWS Bedrock) |
| `/setup-vertex` | Cloud provider setup wizard (Google Vertex) |

### Security & Diagnostics
| Command | What it does |
|---------|-------------|
| `/security-review` | Run security diff review on recent changes |
| `/doctor` | Run diagnostic health check |
| `/bug` / `/feedback` | Create a bug report |
| `/privacy-settings` | Privacy settings (Pro/Max) |
| `/release-notes` | Show recent changelog |
| `/insights` | Session report (patterns, friction points) |

### Integration & Remote
| Command | What it does |
|---------|-------------|
| `/mcp` | Manage MCP servers + OAuth status |
| `/chrome` | Configure Chrome integration |
| `/desktop` | Continue session in Desktop App |
| `/mobile` | QR code for Mobile App |
| `/remote-control` (`/rc`) | Enable remote control session |
| `/ide` | IDE integrations |
| `/install-github-app` | Install GitHub Actions App |
| `/install-slack-app` | Install Slack App |

### Agents & Automation
| Command | What it does |
|---------|-------------|
| `/add-dir <path>` | Add file access to running session |
| `/agents` | Manage subagent configuration |
| `/autofix-pr` | Spawn web-session that watches PR CI and pushes fixes |
| `/background` / `/bg` | Detach session into background-agent |
| `/bashes` / `/tasks` | Show background tasks |
| `/focus` | Focus view |
| `/goal [condition]` | Work across turns until condition is met (v2.1.139+) |
| `/recap` | One-line session summary |
| `/review [PR]` | Local PR review (vs. cloud-based `/ultrareview`) |
| `/schedule <task>` | Create cloud-scheduled task |
| `/team-onboarding` | Generate onboarding guide from session history |
| `/teleport` / `/tp` | Pull web-session into local terminal |
| `/ultraplan <prompt>` | Browser-based plan + execute |
| `/ultrareview [PR]` | Multi-agent cloud review (vs. local `/review`) |
| `/voice [hold\|tap\|off]` | Voice dictation mode |
| `/web-setup` | GitHub setup for claude-code-on-the-web |
| `/powerup` | Interactive feature lessons |

> **Note:** For PR comments, ask Claude directly (e.g. "show me the PR comments") — the explicit `/pr-comments` command was removed in v2.1.91.

### Workshop-Specific Skills
| Command | What it does |
|---------|-------------|
| `/commit` | Create git commits with structured messages |
| `/tdd` | Enforce red-green-refactor workflow |
| `/workshop guide X.X` | Access workshop module guide (moderator mode) |
| `/workshop learn X.X` | Interactive learning (self-paced mode) |

---

## Bundled Skills

Bundled Skills are prompt-based playbooks available in every session (unlike Built-in Commands, which execute fixed logic).

| Skill | What it does | Example |
|-------|-------------|---------|
| `/batch <instruction>` | Parallel codebase changes via worktrees | `/batch migrate src/ from Solid to React` |
| `/claude-api` | Loads API reference + Agent SDK docs | `/claude-api` |
| `/debug [description]` | Enable debug logging and analyze log | `/debug failing mcp auth` |
| `/loop [interval] <prompt>` | Run prompt periodically | `/loop 5m check deploy status` |
| `/simplify [focus]` | Parallel-Reviews + Fixes auf changed files | `/simplify focus on perf` |
| `/run [skill-name]` | Launch & verify your app (v2.1.145+) | `/run dev-server` |
| `/verify` | Verify recent changes by running the app (v2.1.145+) | `/verify` |
| `/run-skill-generator` | Generate a per-project run-skill (v2.1.145+) | `/run-skill-generator` |
| `/fewer-permission-prompts` | Scan transcripts, generate `permissions.allow` allowlist | `/fewer-permission-prompts` |

---

## Built-in Tools

Tool names are the strings used for permission rules, hook matchers, and subagent tool lists.

| Tool | Function | Permission required? |
|------|----------|---------------------|
| `Read` | Read files | No |
| `Glob` | Find files by pattern | No |
| `Grep` | Search file contents | No |
| `Edit` | Modify files (targeted replacement) | Yes |
| `Write` | Create/overwrite files | Yes |
| `NotebookEdit` | Edit Jupyter notebooks | Yes |
| `Bash` | Execute shell commands | Yes |
| `PowerShell` | Native Windows shell (v2.1.x+) | Yes |
| `WebSearch` | Search the web | Yes |
| `WebFetch` | Fetch URL content | Yes |
| `LSP` | Code intelligence via Language Server | No (setup required) |
| `Skill` | Invoke a skill | Yes |
| `Agent` | Spawn a subagent (was `Task` pre-v2.1.63) | No |
| `Monitor` | Background-watch logs/PRs/files and react in running session | No |
| `AskUserQuestion` | Multiple-choice questions for interactive skills | No |
| `TaskCreate` / `TaskList` / `TaskUpdate` / `TaskGet` / `TaskOutput` / `TaskStop` | Task cluster (replaces `TodoWrite`, v2.1.142) | No |
| `EnterPlanMode` / `ExitPlanMode` | Built-in mode switch | No |
| `EnterWorktree` / `ExitWorktree` | Built-in worktree switch | No |
| `PushNotification` | Desktop/phone push for long-running tasks | No |
| `ShareOnboardingGuide` | Generate team-onboarding guide from history | No |
| `TeamCreate` / `SendMessage` | Agent Teams (experimental) | No |
| `CronCreate` / `CronList` / etc. | Scheduled recurring tasks | No |

---

## Models & Context

> Quick-ref snapshot. **Session 1 (LE S1.19)** covers the basics: `/cost`, `/usage`, `--max-budget-usd`. The full cost strategy — effort multipliers, Plan/Implement/Review pipeline, prompt caching, cost-reduction tactics — is taught in **Session 4 (LE S4.4)** alongside CI budget caps (the text still lives in Module 1.5 of `block-1-foundations.md` for reference).

| Model | Context Window | Best for | API Price ($/MTok) |
|-------|---------------|----------|-------------------|
| **Claude Fable 5** | 1M tokens | Most capable model (GA 2026-06-09). Hardest reasoning, long-horizon agentic work. Premium tier. | In: 10 / Out: 50 |
| **Claude Opus 4.8** | 1M tokens | Current default in Claude Code. Complex tasks, architecture, deep reasoning. Effort defaults to `high`. | In: ~5 / Out: ~25 |
| **Claude Sonnet 4.6** | 1M tokens | Fast coding, everyday tasks, cost-effective | In: 3 / Out: 15 |
| **Claude Haiku 4.5** | 200K tokens | Simple tasks, brainstorming, cheapest option | In: 1 / Out: 5 |

- Claude Code defaults to **Opus 4.8** with 1M context (Fable 5 premium tier; Sonnet 4.6 + Haiku 4.5 also current)
- Switch models: `/model` in session (e.g. `/model fable`, `/model opus`) or `claude --model sonnet` at startup
- Fast Mode: `/fast` runs Opus 4.8/4.7 at up to ~2.5x output speed (premium pricing) — toggle on/off
- Use `/compact` when context gets large — compresses older messages
- Use `/context` to visualize how much context you've used
- Use `/cost` to track token spend during a session
- Effort levels: `/effort low|medium|high|xhigh|max` — default `high` on Opus 4.8; `xhigh`/`max` on Opus 4.7 / 4.8 / Fable 5

### Cost Guidance

| Metric | Typical Value |
|--------|--------------|
| Average cost per dev/day | ~$6 (Sonnet 4.6) |
| Monthly per dev | $100-200 (varies heavily) |
| Token reduction strategies | Skills instead of CLAUDE.md bloat, subagents, `/compact`, Sonnet for routine work |

---

## File Locations

| Location | Purpose |
|----------|---------|
| `./CLAUDE.md` | Project-specific instructions (checked into repo) |
| `~/.claude/CLAUDE.md` | Global user instructions (all projects) |
| `~/.claude/settings.json` | Hooks, permissions, and settings |
| `~/.claude/settings.local.json` | Local settings (not shared) |
| `~/.claude/skills/` | Custom user skills directory |
| `~/.claude/plugins/` | Installed plugins directory |
| `~/.claude/plugins/cache/` | Cached marketplace plugins |
| `~/.claude/keybindings.json` | Custom keyboard shortcuts |
| `.claude/settings.json` | Project-level settings |
| `.claude/settings.local.json` | Project-level local settings |
| `.claude/skills/` | Project-level skills |
| `.mcp.json` | MCP config (project-level) |
| `~/.claude/.mcp.json` | MCP config (user-level) |

---

## Permission System

### Permission Modes

| Mode | Behavior | Best for |
|------|----------|----------|
| **default** | Only reads allowed, everything else asks | Beginners, critical systems |
| **acceptEdits** | Reads + file edits + common FS bash (mkdir, touch, rm, mv, cp, sed) auto-approved in working dir | Iterative development |
| **plan** | Shows full plan upfront, approves all at once | Complex refactorings |
| **auto** | ML classifier decides risk level | Power users (see requirements below) |
| **dontAsk** | Never prompts — use with allow/deny rules | CI/CD pipelines |
| **bypassPermissions** | YOLO mode — accepts everything | Sandboxed/isolated VMs only! |

Set via: `claude --permission-mode plan` or `/permissions` in session. Cycle Normal -> acceptEdits -> plan via Shift+Tab.

> **auto mode requirements:** **Max-Plan with Opus 4.8** OR Team/Enterprise (Sonnet 4.6, Opus 4.8). Anthropic API only (not Bedrock/Vertex). Claude Code v2.1.83+. Admins can lock/loosen via managed settings.

### Permission Rules

Configure in `settings.json`:
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(npm test)", "Skill(my-skill)", "Agent(reviewer)"],
    "deny": ["Bash(rm *)", "Bash(curl*)", "WebFetch(domain:evil.com)"],
    "ask": ["Bash(git push *)"]
  }
}
```

| Rule pattern | Effect |
|--------------|--------|
| `Bash(<cmd> *)` | Match shell commands |
| `Skill(<name>)` | Allow/deny specific skill |
| `Agent(<type>)` | Allow/deny specific subagent |
| `WebFetch(domain:example.com)` | Domain-scoped WebFetch |
| `permissions.ask` | Always prompt, even in auto/dontAsk mode |

> **Security note:** For workshops and production, always use least-privilege. Only whitelist what you need.

---

## Sandboxing (OS-Level)

| Platform | Technology | What it does |
|----------|-----------|-------------|
| macOS | Seatbelt | Restricts filesystem + network for Bash |
| Linux/WSL2 | bubblewrap | Restricts filesystem + network for Bash |
| Windows | (limited) | Relies on permission system |

- Toggle with `/sandbox` in session
- Applies to `Bash` tool + child processes only (not all tools)
- Reduces permission prompts by ~84% (Anthropic claim)
- Two modes: auto-allow sandbox, regular permissions + sandbox

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key for direct Anthropic usage |
| `CLAUDE_MODEL` | Set default model |
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock as backend |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI as backend |
| `AWS_REGION` | Region for Bedrock |
| `CLOUD_ML_REGION` | Region for Vertex AI |
| `DISABLE_TELEMETRY` | Opt out of operational metrics |
| `DISABLE_ERROR_REPORTING` | Opt out of error logging (Sentry) |
| `MAX_MCP_OUTPUT_TOKENS` | Raise MCP per-tool warning threshold |
| `CLAUDE_PROJECT_DIR` | Provided to stdio MCP servers for project resolution |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Load CLAUDE.md from `--add-dir` directories |

---

## Settings (settings.json)

| Setting | Effect |
|---------|--------|
| `worktree.baseRef: "fresh"\|"head"` | `--worktree` branches from `origin/<default>` (fresh) or local HEAD; default changed across CLI versions — set it explicitly (v2.1.133+) |
| `autoMode.hard_deny: [<pattern>]` | Unconditional auto-mode block list (overrides user intent, v2.1.136+) |
| `sandbox.network.deniedDomains: [...]` | Block specific domains despite allowed wildcards (v2.1.113+) |
| `disableSkillShellExecution: true` | Disables `` !`<command>` `` in skills (useful for managed/enterprise) |
| `claudeMdExcludes: [...]` | Glob list to exclude from CLAUDE.md auto-discovery (monorepo filter) |
| `skillOverrides: { ... }` | Per-skill visibility: on / name-only / user-invocable-only / off |
| `skillListingBudgetFraction: 0.1` | Token-budget fraction reserved for skill listings |
| `maxSkillDescriptionChars: 200` | Cap description length used in listings |

---

## Hook Events

| Hook Event | When it fires | Use case |
|-----------|---------------|----------|
| **PreToolUse** | Before tool execution | Block unsafe operations, validate inputs |
| **PostToolUse** | After tool completes | Log results, aggregate data, cleanup |
| **Stop** | Session finishes | Save session, cleanup, final reports |
| **SessionStart** | Session begins | Pre-load context, check inventory, env warmup |
| **SessionEnd** | Session ends (any reason) | Persist state, alert on long sessions |
| **UserPromptSubmit** | User submits a prompt | Inject context, strip secrets, log prompts |
| **PreCompact** | Before context compaction | Save outgoing context, snapshot session |
| **SubagentStart** | Subagent spawns | Audit subagent launches, pass context |
| **SubagentStop** | Subagent finishes | Capture result, aggregate output |
| **FileChanged** | File modified by Claude | Live-lint, format-on-save, mirror to backup |
| **InstructionsLoaded** | CLAUDE.md/rules loaded | Validate or augment instructions |
| **Notification** | Notification is shown | Forward to desktop/phone push |

> Full list with ~28 events: code.claude.com/docs/en/hooks (incl. UserPromptExpansion, PermissionRequest, PermissionDenied, PostToolUseFailure, PostToolBatch, TaskCreated, TaskCompleted, StopFailure, TeammateIdle, ConfigChange, CwdChanged, WorktreeCreate, WorktreeRemove, PostCompact, Elicitation, ElicitationResult).

### Hook Execution Types

| Type | How it works |
|------|-------------|
| **command** | Runs a shell command (default; supports `args: string[]` exec form) |
| **http** | Sends HTTP request to a URL |
| **prompt** | Sends prompt to Claude for evaluation |
| **agent** | Spawns a subagent for complex evaluation |
| **mcp_tool** | Calls an MCP tool directly (v2.1.119+) |

> **Matcher syntax:** Letters/digits/`_`/`|` only = exact or pipe-list. With special chars = JavaScript regex. Add `if`-field for additional filter via permission-rule syntax (e.g. `"if": "Bash(git *)"`). Hooks can also live in **Skill frontmatter** and **Subagent frontmatter** — scoped to that component.

Hook config in `settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to run a command'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node security-check.js"
          }
        ]
      }
    ]
  }
}
```

### Hooks on Windows

The `command` of a hook runs in whatever shell the script needs — script files are **not** cross-platform, so provide the form for the box you run on:

| Platform | Script | `command` value |
|----------|--------|-----------------|
| macOS / Linux / Git Bash | `safety-check.sh` (`#!/bin/bash`, needs `chmod +x`) | `bash ~/.claude/hooks/safety-check.sh` |
| Windows PowerShell | `safety-check.ps1` (no `chmod`) | `pwsh -File $HOME/.claude/hooks/safety-check.ps1` |

- Read stdin in PowerShell with `$input | Out-String | ConvertFrom-Json`; match with `-match` (case-insensitive by default); `exit 1` blocks, `exit 0` allows.
- `pwsh` = PowerShell 7; fall back to `powershell -File ...` for Windows PowerShell 5.1.
- No `jq` on Windows? Parse JSON with `python` (`json.load(sys.stdin)`) instead — see the tested assets in `resources/demos/assets/hooks/` and the bash+PowerShell pair in Exercise 2.2.

### Circuit Breaker Pattern
Hook detects when an agent runs the same command 3x with the same error, stops the process, and forces a strategy change. Prevents token waste from hallucination loops.

---

## Skills (Custom)

### Skill Frontmatter Reference

```yaml
---
name: my-skill              # Defines the /command name
description: What it does   # Used for auto-invocation decisions
when_to_use: "..."          # Plain-language trigger description
argument-hint: "[mode] [target]"  # UI hint for argument completion
arguments: [mode, target]   # Positional named args
disable-model-invocation: true  # Only manual start (critical actions)
user-invocable: true        # Show in command menu (false = background knowledge)
allowed-tools: Read Grep Bash   # Intent scoping (not hard security!)
context: fork               # Run in isolated subagent context
agent: Explore              # Subagent TYPE for context:fork (Explore/Plan/general-purpose/custom) — NOT a model
model: haiku|sonnet|opus    # Model for this skill (incl. the forked context)
effort: low|high|xhigh|max  # Effort level
paths: ["src/**/*.ts"]      # Glob — skill only available when files match
shell: powershell|bash      # Shell for command execution
hooks:                      # Skill-scoped lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks: [...]
# Workshop-Custom (NOT in official schema):
# version, author, tags
---
```

### Argument Substitution & Dynamic Context

| Token | Resolves to |
|-------|-------------|
| `$ARGUMENTS` | Full argument string |
| `$1`, `$N` | Positional argument N |
| `$name` | Named argument by `arguments:` key |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_EFFORT}` | Current effort level |
| `${CLAUDE_SKILL_DIR}` | Skill's own directory (for sibling files) |
| `` !`<command>` `` | Dynamic Context Injection — runs shell command and embeds output in prompt |

### Skill Locations

| Scope | Path |
|-------|------|
| Project | `.claude/skills/<name>/SKILL.md` |
| User | `~/.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` |

---

## Plugin Structure & Scopes

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest (name, version, description)
├── skills/
│   └── hello/SKILL.md       # Skills (invoked as /plugin:skill)
├── agents/*.md              # Subagent definitions
├── commands/*.md            # Slash commands
├── hooks/hooks.json         # Lifecycle hooks
├── .mcp.json                # Bundled MCP servers
├── .lsp.json                # Language server config
├── output-styles/*.md       # Output formatting
├── bin/*                    # Executables (added to PATH)
└── scripts/*                # Helper scripts
```

### Plugin Scopes

| Scope | Config Location | Who controls |
|-------|----------------|-------------|
| **user** | `~/.claude/settings.json` | Individual developer |
| **project** | `.claude/settings.json` | Team (checked into repo) |
| **local** | `.claude/settings.local.json` | Individual (not shared) |
| **managed** | Org-managed settings | Enterprise admin |

Test local plugins: `claude --plugin-dir ./my-plugin`

---

## MCP Configuration

### Transport Types

| Transport | Use case | Status |
|-----------|----------|--------|
| **HTTP** | Remote servers (recommended) | Current standard |
| **stdio** | Local processes, custom scripts | Good for system access |
| **SSE** | Server-Sent Events | **Deprecated** |

### Setup Examples

```bash
# Remote HTTP server (recommended)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Local stdio server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# With environment variables
claude mcp add --transport stdio --env GITHUB_TOKEN=xxx github -- npx -y @modelcontextprotocol/server-github

# With auth header
claude mcp add --transport http --header "Authorization: Bearer xxx" myserver https://api.example.com/mcp
```

### Project-level `.mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem"]
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

### MCP Output Limits

| Threshold | Value | Note |
|-----------|-------|------|
| Warning | 10k tokens | Claude Code warns about large output |
| Default max | 25k tokens | Truncated beyond this |
| Override max | 500k chars | Via `_meta["anthropic/maxResultSizeChars"]` per tool |

### MCP Security

- Third-party MCP servers: **use at your own risk**
- OAuth flows supported for compatible remote servers
- Beware of prompt injection from untrusted content
- In-session: `/mcp` to check status and manage OAuth

---

## Agent Patterns

| Pattern | When to use | Example |
|---------|------------|---------|
| **Single** | Simple tasks, linear workflows | `/tdd` for one feature |
| **Parallel** | Independent subtasks | `/batch` for multi-file refactor |
| **Pipeline** | Sequential with handoff | Claude -> Codex -> Claude review |
| **Fan-out/Fan-in** | Decompose, parallel execute, aggregate | Self-improve loop iterations |
| **Adversarial** | Validate logic, find edge cases | Devil's Advocate swarm for review |
| **Agent Teams** | Multi-session coordination (experimental) | Lead + Reviewer + QA + Docs |

### Agent Teams (Experimental)

```
TeamCreate  — Create a new teammate agent
SendMessage — Send message between team members
/tasks      — Track team progress
```

Uses `TeamCreate`/`SendMessage` tools. Each teammate runs as separate session with own context. Token cost scales per teammate.

---

## Data Retention & Privacy

| Plan | Training | Retention | Notes |
|------|----------|-----------|-------|
| Free/Pro/Max | Opt-in | Opt-in: 5y, Opt-out: 30d | Consumer plans |
| Team/Enterprise | No (default) | 30 days | Commercial plans |
| Enterprise + ZDR | No | 0 days | Zero Data Retention (some features disabled) |

- Telemetry opt-out: `DISABLE_TELEMETRY=1`, `DISABLE_ERROR_REPORTING=1`
- Network: prompts/outputs via TLS, not encrypted at rest (per docs)

---

## Security Analogies (Quick Reference)

> Full mapping in `resources/security-analogies.md` — the single source of truth. Below are the 7 most-used analogies for quick lookup during the workshop.

| Concept | Security Analogy |
|---------|------------------|
| **Permission Modes** | Security levels — from visitor badge to master key |
| **Permissions (allow/deny)** | Least privilege — only grant what's needed |
| **Hooks** | Alarm sensors — detect and block threats |
| **Sandboxing / Worktrees** | Security airlock — isolate untrusted code |
| **Devil's Advocate / Codex Review** | Penetration test — adversarial verification |
| **CLAUDE.md** | Access policy — controls agent behavior |
| **Agents** | Specialized teams — compartmentalize responsibilities |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"claude: command not found"** | `curl -fsSL https://claude.ai/install.sh \| bash` or check PATH |
| **Authentication failed** | Run `/login` or check `ANTHROPIC_API_KEY` |
| **Context compressed** | Use `/compact` proactively, check `/context`, split into sub-tasks |
| **Hook not firing** | `/hooks` to inspect, verify matcher in `settings.json`, restart session |
| **MCP not connecting** | Check `.mcp.json` config, run `/mcp` in session, try `/doctor` |
| **Agent stuck** | Wait 30s, check `/status`, use Escape to cancel |
| **Permission denied** | `/permissions` to adjust, or use `--permission-mode` flag |
| **High cost** | Switch to `/model sonnet`, check `/cost`, use `/effort low` |
| **Slow response** | Try `/fast` mode or switch to a lighter model |
| **Plugin not loading** | `claude plugin enable <name>`, or `/reload-plugins` |
| **Sandbox blocking** | `/sandbox` to toggle, check OS support |

---

## Quick Tips

- **Plan first:** Use `/plan` or `Shift+Tab` before complex tasks
- **Watch costs:** Check `/cost` regularly, use Sonnet for routine work
- **Save context:** Use `/compact` before hitting the limit, check with `/context`
- **Continue sessions:** `claude -c` picks up where you left off, `claude -r <name>` for named sessions
- **CI integration:** `claude -p "task" --output-format json --json-schema schema.json` for pipelines
- **Debug hooks:** `/hooks` to inspect, `--verbose` flag to see execution
- **Reuse skills:** Create custom skills in `~/.claude/skills/` or `.claude/skills/`
- **Validate code:** Run `/security-review` before claiming tasks complete
- **Parallel refactors:** `/batch` for multi-file changes across worktrees
- **Recurring checks:** `/loop 5m check status` for periodic monitoring
- **Side questions:** `/btw what is X?` to ask without polluting context
- **Effort control:** `/effort high` for architecture, `/effort low` for quick fixes
- **Export sessions:** `/export session.md` to save conversation history
- **Undo safely:** `/rewind` to go back multiple steps, not just the last edit

---

## Useful Resources

| Resource | URL |
|----------|-----|
| **Claude Code Docs** | code.claude.com/docs/en/overview |
| **CLI Reference** | code.claude.com/docs/en/cli-reference |
| **Tools Reference** | code.claude.com/docs/en/tools-reference |
| **Skills Docs** | code.claude.com/docs/en/skills |
| **Hooks Docs** | code.claude.com/docs/en/hooks |
| **Plugins Reference** | code.claude.com/docs/en/plugins-reference |
| **Plugins Guide** | code.claude.com/docs/en/plugins |
| **MCP in Claude Code** | code.claude.com/docs/en/mcp |
| **Subagents** | code.claude.com/docs/en/sub-agents |
| **Permissions** | code.claude.com/docs/en/permissions |
| **Permission Modes** | code.claude.com/docs/en/permission-modes |
| **Auto-Mode Config** | code.claude.com/docs/en/auto-mode-config |
| **Sandboxing** | code.claude.com/docs/en/sandboxing |
| **Security** | code.claude.com/docs/en/security |
| **Memory/CLAUDE.md** | code.claude.com/docs/en/memory |
| **Auto-Memory** | code.claude.com/docs/en/memory#auto-memory |
| **Worktrees** | code.claude.com/docs/en/worktrees |
| **Agent-View** | code.claude.com/docs/en/agent-view |
| **Output Styles** | code.claude.com/docs/en/output-styles |
| **Channels** | code.claude.com/docs/en/channels |
| **Routines** | code.claude.com/docs/en/routines |
| **Headless** | code.claude.com/docs/en/headless |
| **Best Practices** | code.claude.com/docs/en/best-practices |
| **Statusline** | code.claude.com/docs/en/statusline |
| **Changelog** | code.claude.com/docs/en/changelog |
| **Claude Code Repo** | github.com/anthropics/claude-code |
| **Awesome Claude Code** | github.com/anthropics/awesome-claude-code |
| **MCP Specification** | modelcontextprotocol.io/specification |
| **Plugin Directory** | github.com/anthropics/claude-code-plugins |
| **Claude Pricing** | claude.com/pricing |

---

## Your First Month with Claude Code

### Day 1: Foundation
- Start Claude Code in an existing project
- Write a `CLAUDE.md` (stack, conventions, no-go zones)
- Solve 3 tasks with specific prompts

### Days 2–3: Automation
- Build a personal skill (your most repeated prompt → `~/.claude/skills/`)
- Set up a safety hook (block `rm -rf`, force push)
- Make `/compact` and `/context` a habit

### Week 2: Integration
- Add an MCP server (GitHub recommended)
- Create a custom subagent (e.g. code reviewer)
- Try `/loop` for simple monitoring

### Weeks 3–4: Advanced (optional)
- Try Agent Teams (experimental)
- Build a NotebookLM knowledge base for your domain
- Structure your own plugin and share with your team

---

**Last Updated:** 2026-05-20 | **Workshop:** Claude Code Dynamic Workshop
