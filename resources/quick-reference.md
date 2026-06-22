# Claude Code Quick Reference

> 1-Pager: druckbare Schnellreferenz für den Workshop-Alltag.

## Start / Auth
| Command | Was |
|---|---|
| `claude` | Interactive session |
| `claude -p "<prompt>"` | One-shot (headless) |
| `claude --bare -p "..."` | Headless, kein Skill/Hook-Overhead |
| `claude -c` | Continue last session |
| `claude --resume <id>` | Resume specific session |
| `claude --from-pr 1234` | Resume at PR |
| `claude --version` | Version check |

## Models & Cost
| Command | Was |
|---|---|
| `/model fable\|opus\|sonnet\|haiku` | Model wechseln (Default: Opus 4.8; Fable 5 = Premium-Tier) |
| `/fast` | Fast Mode an/aus (Opus 4.8/4.7, ~2.5x Output-Speed, Premium-Preis) |
| `/effort low\|medium\|high\|xhigh\|max` | Effort-Level (Default `high` auf Opus 4.8) |
| `/cost` | Aktuelle Session |
| `/usage` | Tagessumme |
| `/insights` | Analytics |
| `--max-budget-usd 0.50` | Kosten-Cap |
| `--max-turns 10` | Turn-Cap |

## Permissions
| Mode | Was |
|---|---|
| `default` | Reads only, Rest fragt |
| `acceptEdits` | + File Edits + FS-Bash |
| `plan` | Plan upfront |
| `auto` | ML decides (Max-Plan/Team) |
| `dontAsk` | No prompts (CI) |
| `bypassPermissions` | ALL (VM only!) |

Wechsel: `Shift+Tab` cycle | `--permission-mode <mode>` | `/permissions`

## Hot Slash-Commands
`/help` `/skills` `/hooks` `/mcp` `/plugin` | `/context` `/compact [focus]` `/rewind` | `/init` `/memory` `/doctor` `/debug` | `/branch` `/diff` `/review` `/security-review` `/ultrareview` | `/goal` `/loop` `/schedule` `/autofix-pr` | `/output-styles` `/voice` `/recap` `/teleport`

## Skills Frontmatter Cheat
```yaml
---
name: my-skill
description: "Trigger when... use this skill"
when_to_use: "Trigger phrases here"
argument-hint: "[mode] [target]"
arguments: [mode, target]
disable-model-invocation: false
allowed-tools: Read Grep Bash
model: sonnet
effort: medium
paths: ["src/**"]
shell: bash
hooks:
  PreToolUse:
    - matcher: Bash
      type: command
      command: ./check.sh
---
```
Substitution: `$ARGUMENTS`, `$1`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `` !`cmd` ``

## Hooks (Top 11 Events)
PreToolUse · PostToolUse · Stop · SessionStart · SessionEnd · UserPromptSubmit · PreCompact · SubagentStart · SubagentStop · FileChanged · InstructionsLoaded

Execution types: `command` `http` `prompt` `agent` `mcp_tool`

## Plugins
```bash
claude plugin marketplace add <owner/repo>
claude plugin install <name>@<marketplace> --scope user
claude plugin list / enable / disable / update / uninstall
claude plugin validate <name>
/reload-plugins
```
Manifest at `.claude-plugin/plugin.json` (NOT root!)

## MCP
```bash
claude mcp add --transport http <name> <url>
claude mcp add <name> -- npx -y @scope/server
claude mcp list / get / remove
/mcp                  # status + OAuth flow
```
Scopes: `local` (was project) · `project` (shared via .mcp.json) · `user` (was global)

## Subagents
```yaml
---
name: my-agent
description: "Use when ..."
tools: Read Grep Bash      # NOT allowed_tools
model: haiku                # or claude-haiku-4-5-20251001
permissionMode: acceptEdits
maxTurns: 5
skills: [test-driven]
isolation: worktree
background: false
---
```
Background: `claude --bg <prompt>` | `claude agents` | `attach` `logs` `stop` `respawn` `rm`

## Worktrees
```bash
git worktree add ../exp feature/x
claude --worktree feature/x
# worktree.baseRef: "fresh" | "head"
```

## Permission Rules
`allow` / `deny` / `ask` mit:
`Bash(npm test*)` · `Skill(<name>)` · `Agent(<type>)` · `WebFetch(domain:example.com)`

## Top URLs
- code.claude.com/docs/en/ — official docs
- code.claude.com/docs/en/changelog — what's new
- claude.com/pricing — costs

---
*Stand 2026-05-20 · Vollversion: `resources/cheatsheet.md`*
