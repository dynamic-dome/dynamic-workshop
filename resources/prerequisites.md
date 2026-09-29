# Workshop Prerequisites & Installation Guide

> Complete setup guide for participants of the Claude Code Dynamic Workshop.
> Please complete these steps **before** the workshop begins.
>
> **Time budget:** plan ~45 minutes, in the order below. Do not start with optional plugins; get the core CLI, repo, and playground tests green first.

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Windows 10, macOS 12, Ubuntu 20.04 | Latest version |
| **Node.js** | v18.0+ | v20 LTS or v22 LTS |
| **RAM** | 4 GB | 8 GB+ |
| **Disk** | 500 MB free | 2 GB+ |
| **Terminal** | Any modern terminal | Windows Terminal, iTerm2, or Warp |
| **Internet** | Required | Stable connection (API calls) |

---

## Step 1: Install Node.js

Claude Code requires Node.js 18 or higher.

**Check if installed:**
```bash
node --version   # Should show v18+ or v20+
npm --version    # Should show 9+
```

**Install if needed:**
- **Windows:** Download from [nodejs.org](https://nodejs.org/) (LTS version) or use `winget install OpenJS.NodeJS.LTS`
- **macOS:** `brew install node` or download from [nodejs.org](https://nodejs.org/)
- **Linux:** `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs`

---

## Step 2: Install Claude Code

**Recommended installers (official docs):**

```powershell
# Windows
irm https://claude.ai/install.ps1 | iex

# Alternative on Windows
winget install Anthropic.ClaudeCode
```

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Alternative on macOS / Linux
brew install --cask claude-code
```

The old npm install path exists in older material, but the current official docs mark npm as deprecated for new installs.

```bash
# Verify installation
claude --version

# Already installed? Update to a recent build:
claude update
```

### Tested Version Gate

This workshop was refreshed against `claude --version` **2.1.200** on 2026-07-04. Use **2.1.197+** as the tested minimum for the full workshop so the `fable`/`opus`/`sonnet`/`haiku` aliases, workflows fixes, plugin improvements, and current hook behavior are in range. The generations those aliases resolve to today need a newer CLI (Fable 5.1 from 2.1.257, Opus 5.5 from 2.1.280, Sonnet 5.5 from 2.1.284; see the [canon](_canonical.md) and check `claude --version`). <!-- version-pinned: Mindest-CLI je Modellgeneration -->

| Feature used in workshop | Minimum documented version | Verification |
|---|---:|---|
| Plugin init / local plugin improvements | 2.1.157 | `claude plugin init`, `claude --plugin-dir` |
| Fable tier | 2.1.170 | `/model` lists `fable` after update |
| `/workflows` agent detail/status UI | 2.1.186 | `/workflows` available in current CLI builds |
| Hook JSON output (`updatedToolOutput`, `systemMessage`, `terminalSequence`) | Current hook docs | `python -m pytest tools/test_course_hooks.py` in the repo, then Demo 2.2 / Exercise 2.6 |
| Sonnet tier with 1M context | 2.1.197 | `claude --version`, `/model` |

```bash
# Verify feature surface after update
claude --version
claude --print "Say ready"
```

> Always trust `claude --version`, `/model`, `/workflows`, and `/release-notes` over any version number printed in older workshop material.

**Alternative — without global install:**
```bash
npx @anthropic-ai/claude-code
```

**Desktop App (optional):**
- Download from [claude.ai/code](https://claude.ai/code) for Mac or Windows
- Web version also available at the same URL

---

## Step 3: Authenticate

```bash
# Start Claude Code and log in
claude
# Then run:
/login
```

You need one of:
- **Claude Pro/Max subscription** (recommended for workshop)
- **Anthropic API key** — set the `ANTHROPIC_API_KEY` environment variable:
  ```powershell
  # Windows PowerShell — current session only:
  $env:ANTHROPIC_API_KEY = "sk-ant-..."
  # Windows — persist across sessions (re-open the terminal afterwards):
  setx ANTHROPIC_API_KEY "sk-ant-..."
  ```
  ```bash
  # macOS / Linux / Git Bash:
  export ANTHROPIC_API_KEY="sk-ant-..."        # current session
  echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc   # persist
  ```
- **AWS Bedrock** or **Google Vertex** credentials (enterprise setups)

**Verify authentication works:**
```bash
claude --print "Say hello"
# Should return a response without errors
```

---

## Step 4: Install Git

Required for demo repository and version control exercises.

**Check if installed:**
```bash
git --version   # Should show 2.30+
```

**Install if needed:**
- **Windows:** `winget install Git.Git` or download from [git-scm.com](https://git-scm.com/)
- **macOS:** `xcode-select --install` or `brew install git`
- **Linux:** `sudo apt install git`

---

## Step 5: Install Python 3 (for Block 1+)

Required from the very first Block 1 exercise onward (the `event_log_parser.py` task) and for the workshop-playground demo repo (pytest tests, vulnerability demos). Install it before Session 1, not just before Block 2.

**Check if installed** (on Windows the commands are `python`/`pip`, on macOS/Linux `python3`/`pip3`):
```bash
python3 --version   # Windows: python --version    (should show 3.9+)
pip3 --version      # Windows: pip --version
```

**Install if needed:**
- **Windows:** `winget install Python.Python.3.12` or download from [python.org](https://python.org/)
- **macOS:** `brew install python`
- **Linux:** `sudo apt install python3 python3-pip`

---

## Step 6: Install GitHub CLI (optional, for Block 3)

Used in advanced exercises for PR workflows.

```bash
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh

# Then authenticate
gh auth login
```

---

## Step 7: Clone the Workshop Repository

The workshop playground is a subfolder inside the main workshop repository.

```bash
# Variant A: Clone the workshop repo (this contains the playground)
mkdir -p ~/cc-workshop
git clone https://github.com/dynamic-dome/dynamic-workshop.git ~/cc-workshop/dynamic-workshop
cd ~/cc-workshop/dynamic-workshop/workshop-playground

# Variant B: If your workshop moderator provided a different path/URL, use that one instead.

# Install Python dependencies   (Windows: use pip instead of pip3)
pip3 install -r requirements.txt

# Verify tests run   (Windows: use python instead of python3)
python3 -m pytest -v
```

Clone URL verified reachable on 2026-07-04 with `git ls-remote https://github.com/dynamic-dome/dynamic-workshop.git HEAD`.

---

## Pre-Workshop Checklist

Run through this checklist to make sure everything works:

- [ ] `node --version` shows v18+
- [ ] `claude --version` shows current version
- [ ] `claude --print "Hello"` returns a response (authentication works)
- [ ] `git --version` shows 2.30+
- [ ] `python3 --version` (Windows: `python --version`) shows 3.9+
- [ ] Workshop playground repo cloned and tests pass
- [ ] Terminal supports Unicode and ANSI colors
  - macOS / Linux / Git Bash: `echo -e "\033[32mGreen\033[0m"`
  - Windows PowerShell 7+: `Write-Host "`e[32mGreen`e[0m"` (or `"$([char]27)[32mGreen$([char]27)[0m"` in PowerShell 5.1)

---

## Quick Diagnostic

If something isn't working, run the built-in doctor and the workshop doctor:

```bash
claude /doctor
```

```powershell
# From the cloned workshop repo:
powershell -ExecutionPolicy Bypass -File .\tools\workshop_doctor.ps1
```

This checks your environment and reports issues.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npm: command not found` | Install Node.js first (Step 1) |
| `claude: command not found` | Run `npm install -g @anthropic-ai/claude-code` again, check PATH |
| Authentication fails | Check API key or subscription status, try `/login` again |
| `EACCES` permission error | Use `npm config set prefix ~/.npm-global` and add to PATH |
| Python not found on Windows | Use `python` instead of `python3`, or install from Microsoft Store |
| Tests fail in playground | Check Python version, run `pip3 install -r requirements.txt` |
| Slow/no response | Check internet connection, try `claude --verbose` for details |

---

## What to Bring

- Laptop with the above setup completed
- Curiosity and questions
- A project idea you'd like to try with Claude Code (optional but fun)

---

**Questions?** Contact the workshop organizer before the session.

**Last Updated:** 2026-06-23 | **Workshop:** Claude Code Dynamic Workshop (zentraler Stand-Anker: README → „Stand & Versionen")

---

## Workshop-Specific Plugins & Skills

> **About these plugins:** The plugins listed below (`agentic-os`, `devil-advocate-swarms`,
> `multi-model-orchestrator`) and the `notebooklm` user-skill are **workshop-custom plugins**
> built specifically for this workshop. They are not part of the official Claude Code
> installation, not in the public Anthropic marketplaces, and not maintained by Anthropic.
>
> Block 1 and Block 2 (Modules 2.1, 2.2, 2.3, 2.4) work without these plugins.
> Only Block 3 Demos 3.3, 3.4, 3.5 reference them — and observation/web-UI alternatives
> exist for self-learners (see each demo's recovery notes).

Several demos require custom plugins or user-skills that are not part of the default Claude Code installation. Install these **before Session 2** (Block 2 onwards).

### Workshop-Custom Plugins

Several Block 3 demos reference custom plugins built specifically for this workshop:
`agentic-os`, `devil-advocate-swarms`, `multi-model-orchestrator`.

**These are workshop-author plugins, not part of any official marketplace.**

Four options:

**Option A (self-serve workshop plugin): Use the reachable workshop repo.**
The workshop plugin in this repository is available at `https://github.com/dynamic-dome/dynamic-workshop.git`.

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_workshop_plugin.ps1
```

Then start Claude Code with the local plugin source:

```bash
claude --plugin-dir ~/cc-workshop/dynamic-workshop/.claude-plugin
```

**Option B (live workshop extras): Get demo-only custom plugins from your workshop moderator.**
If the moderator wants to run `agentic-os`, `devil-advocate-swarms`, or `multi-model-orchestrator` live, they must provide a real Git/Drive release link before the workshop. Do not depend on an unpublished tarball during participant setup.

**Option C (self-learners): Observation mode only.**
You can read about these plugins in the modules and watch the demos in recorded video form.
The patterns they demonstrate (adversarial swarms, multi-model pipelines, self-improve loops)
are conceptually transferable to plugins you build yourself.

**Option D: Build minimal replacements.**
After completing Modules 2.1 (Skills) and 2.3 (Plugins), you can build your own simplified
versions of these patterns. The workshop modules walk through the structure.

**These plugins are NOT required to complete Block 1 or Block 2.**
Only Block 3 Demos 3.3 (Devil's Advocate), 3.4 (Self-Improve), and 3.5 (Inception) use them.

Used in:
- `agentic-os` — Demo 2.3 (Plugin Anatomy), Demo 3.4 (Self-Improve Loop)
- `devil-advocate-swarms` — Demo 3.3 (Security Audit)
- `multi-model-orchestrator` — Demo 3.2 (Codex Swarm), Demo 3.5 (Inception)

### Custom User-Skills

The `notebooklm` user-skill is a workshop-custom skill (not part of official Claude Code).
It is used in Demo 2.5 and Exercise 2.5.

Two options:

**Option A: Get the skill from your workshop moderator.**
The moderator will provide a tarball or local copy. Extract into `~/.claude/skills/notebooklm/`.

```bash
mkdir -p ~/.claude/skills
# Then place the moderator-provided skill folder at ~/.claude/skills/notebooklm
```

**Option B: Use the official NotebookLM web UI (notebooklm.google.com) instead.**
In this case, you'll use the web interface for Demo 2.5 and Exercise 2.5 instead of the
CLI commands. Recovery steps are documented in the demos.

Verify Option A with `/skills` — `notebooklm` should appear in the list.

### Prepared Hook Files

Demo 2.2 (Hooks — The Alarm System) uses a pre-prepared hook file at `~/.claude/hooks/security-check.sh`. Create it before the demo:

The hook is the tested safety script from the repo (`resources/demos/assets/hooks/safety-check.*`, the same one Exercise 2.2 builds). It reads the command from `tool_input.command` and blocks with **exit 2** — the only exit code that blocks. Copy it instead of retyping it:

**macOS / Linux / Git Bash** (needs `jq` — see the prerequisites checklist):

```bash
mkdir -p ~/.claude/hooks
cp ~/cc-workshop/dynamic-workshop/resources/demos/assets/hooks/safety-check.sh ~/.claude/hooks/security-check.sh
chmod +x ~/.claude/hooks/security-check.sh

# Smoke test with an input in the real format - expect "blocked" and exit=2:
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"}}' | bash ~/.claude/hooks/security-check.sh; echo "exit=$?"
```

**Windows / PowerShell** (no `jq`, no `chmod` needed):

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.claude/hooks" | Out-Null
Copy-Item "$HOME/cc-workshop/dynamic-workshop/resources/demos/assets/hooks/safety-check.ps1" "$HOME/.claude/hooks/security-check.ps1"

# Smoke test with an input in the real format - expect "blocked" and exit=2:
'{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"}}' | powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME/.claude/hooks/security-check.ps1"; "exit=$LASTEXITCODE"
```

Reference this hook in your `~/.claude/settings.json`. Use the `command` that matches the script you created:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash ~/.claude/hooks/security-check.sh" }
        ]
      }
    ]
  }
}
```

> **Windows:** replace the `command` value with `"pwsh -File $HOME/.claude/hooks/security-check.ps1"` (or `powershell -File ...` for Windows PowerShell 5.1). If you prefer the bash variant, install **Git Bash + jq** (see the prerequisites checklist) and keep the `bash ...` command.

### Prepared NotebookLM Notebook

Demo 2.5 (NotebookLM as Knowledge Base) uses a pre-prepared notebook named `claude-code-docs` with the official Claude Code documentation as sources.

Create it before Session 2:

```bash
# CLI variant (if notebooklm CLI is available)
notebooklm create "claude-code-docs"
notebooklm add-source https://code.claude.com/docs/en/overview --notebook claude-code-docs
notebooklm add-source https://code.claude.com/docs/en/skills --notebook claude-code-docs
notebooklm add-source https://code.claude.com/docs/en/hooks --notebook claude-code-docs
```

Alternatively use the NotebookLM web UI: notebooklm.google.com → Create notebook → "claude-code-docs" → Add web sources.

### Pre-pull the Playwright MCP (for Exercise 2.4 / Demo 2.4)

Exercise 2.4 adds the Playwright MCP server, which runs via `npx @playwright/mcp`. On first use, `npx`
downloads the package **and** Playwright downloads a browser binary — that can stall the live session
for a minute or more. Warm the cache **before Session 2** so nothing downloads on stage:

```bash
# Pre-download the MCP package + its browser into the npx/Playwright cache:
npx -y @playwright/mcp@latest --help   # pulls the package
npx -y playwright install chromium     # pulls the browser binary
```

After this, the `claude mcp add` step in Exercise 2.4 starts the server from cache — no live download.

### Codex CLI (optional, for Demo 3.2)

OpenAI Codex CLI is **optional** — required only for Demo 3.2 (Codex Swarm).
If you want to follow Demo 3.2 hands-on:

**Method 1: Official OpenAI Codex CLI (if available in your region)**

See: https://platform.openai.com/docs/codex
Install via your package manager or from GitHub releases.

**Method 2: Skip the install**

Demo 3.2 is also marked as "Nice-to-have, demo-only" in the exercise priority guide.
You can observe the moderator's demo without running it yourself.

**Verify your install (if you went with Method 1):**

```bash
codex --version
codex auth status   # ensure authenticated to your OpenAI account
```

If Codex is not installed, the demo can still be observed but not replicated locally.

### Verification

After all installs, run a quick verification:

```bash
claude plugin list                      # shows installed plugins (0–3 depending on which option you chose)
claude --plugin-dir ~/cc-workshop/dynamic-workshop/.claude-plugin   # verifies local workshop plugin loads
/skills                                 # should show notebooklm (only if you used Custom User-Skills Option A)
ls ~/.claude/hooks/security-check.sh    # macOS/Linux/Git Bash — the hook file should exist
# Windows PowerShell: Test-Path "$HOME/.claude/hooks/security-check.ps1"   # should print True
notebooklm list                         # should show claude-code-docs (only if you used CLI variant)
```

Note: The plugin/skill/notebooklm CLI lines are only relevant if you installed the
optional workshop-custom plugins, the notebooklm user-skill, or the notebooklm CLI.
Block 1 and most of Block 2 work without any of these.

---

## Workdir Convention

Use a single workspace root for all workshop content:

```bash
mkdir -p ~/cc-workshop
```

Inside, this structure:

```
~/cc-workshop/
├── dynamic-workshop/          # git clone of the workshop repo (see clone step above)
│   └── workshop-playground/   #   ← the playground lives HERE: ~/cc-workshop/dynamic-workshop/workshop-playground
├── demos/                     # Live demo workdirs (one per demo: demo-1.1, demo-1.2, ...)
└── exercises/                 # Exercise workdirs (one per exercise: exercise-1.1, ...)
```

> The playground is **inside the cloned repo** (`dynamic-workshop/workshop-playground`), not directly
> under `~/cc-workshop/`. Exercises that reference it use that path; the `demos/` and `exercises/`
> folders above are just scratch workdirs you create by hand.

This way:
- All workshop artifacts in one place
- Easy to clean up after workshop (`rm -rf ~/cc-workshop`)
- Demos and exercises don't pollute your home directory

