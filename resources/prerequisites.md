# Workshop Prerequisites & Installation Guide

> Complete setup guide for participants of the Claude Code Dynamic Workshop.
> Please complete these steps **before** the workshop begins.

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

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

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

If something isn't working, run the built-in doctor:

```bash
claude /doctor
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

**Last Updated:** 2026-04-03 | **Workshop:** Claude Code Dynamic Workshop

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

Three options:

**Option A (recommended for live workshops): Get them from your workshop moderator.**
The moderator will provide a tarball or shared Drive/Git link with the plugin sources.
Extract each into `~/.claude/plugins/` and run `/reload-plugins` in Claude Code.

**Option B (self-learners): Observation mode only.**
You can read about these plugins in the modules and watch the demos in recorded video form.
The patterns they demonstrate (adversarial swarms, multi-model pipelines, self-improve loops)
are conceptually transferable to plugins you build yourself.

**Option C: Build minimal replacements.**
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

**macOS / Linux / Git Bash** (needs `jq` — see the prerequisites checklist):

```bash
mkdir -p ~/.claude/hooks
cat > ~/.claude/hooks/security-check.sh << 'EOF'
#!/bin/bash
# Workshop demo hook: blocks rm -rf and force-pushes
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+-rf|git push.*--force|DROP TABLE|truncate'; then
  echo "WARNING: Potentially destructive command detected: $COMMAND" >&2
  echo "Pausing for confirmation..." >&2
  exit 1
fi

exit 0
EOF
chmod +x ~/.claude/hooks/security-check.sh
```

**Windows / PowerShell** (no `jq`, no `chmod`, no heredoc — uses `New-Item -Force` and a here-string):

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.claude/hooks" | Out-Null

@'
# Workshop demo hook: blocks rm -rf and force-pushes
$raw = $input | Out-String
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }
$command = [string]$data.command
if ($command -match 'rm\s+-rf|git push.*--force|DROP TABLE|truncate') {
  [Console]::Error.WriteLine("WARNING: Potentially destructive command detected: $command")
  [Console]::Error.WriteLine("Pausing for confirmation...")
  exit 1
}
exit 0
'@ | Set-Content -Path "$HOME/.claude/hooks/security-check.ps1" -Encoding utf8
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
/skills                                 # should show notebooklm (only if you went with Option A above)
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

