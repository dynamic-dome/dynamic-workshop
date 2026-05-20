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
- **Anthropic API key** (set `ANTHROPIC_API_KEY` environment variable)
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

## Step 5: Install Python 3 (for Block 2+)

Required for the workshop-playground demo repo (pytest tests, vulnerability demos).

**Check if installed:**
```bash
python3 --version   # Should show 3.9+
pip3 --version
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

```bash
# Navigate to your workspace
cd ~/Desktop

# Clone the workshop playground (demo repo with intentional vulnerabilities)
git clone <workshop-playground-url>
cd workshop-playground

# Install Python dependencies
pip3 install -r requirements.txt

# Verify tests run
python3 -m pytest -v
```

---

## Pre-Workshop Checklist

Run through this checklist to make sure everything works:

- [ ] `node --version` shows v18+
- [ ] `claude --version` shows current version
- [ ] `claude --print "Hello"` returns a response (authentication works)
- [ ] `git --version` shows 2.30+
- [ ] `python3 --version` shows 3.9+
- [ ] Workshop playground repo cloned and tests pass
- [ ] Terminal supports Unicode and ANSI colors (try `echo -e "\033[32mGreen\033[0m"`)

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

Several demos require custom plugins or user-skills that are not part of the default Claude Code installation. Install these **before Session 2** (Block 2 onwards).

### Custom Plugins

These plugins are referenced in demos in Block 2 and 3. Install via:

```bash
# Marketplace-add and install
claude plugin marketplace add agentic-os/agentic-os-marketplace
claude plugin install agentic-os --scope user

claude plugin marketplace add devil-advocate-swarms/devil-advocate-swarms-marketplace
claude plugin install devil-advocate-swarms --scope user

claude plugin marketplace add multi-model-orchestrator/multi-model-orchestrator-marketplace
claude plugin install multi-model-orchestrator --scope user
```

Used in:
- `agentic-os` — Demo 2.3 (Plugin Anatomy), Demo 3.4 (Self-Improve Loop)
- `devil-advocate-swarms` — Demo 3.3 (Security Audit)
- `multi-model-orchestrator` — Demo 3.2 (Codex Swarm), Demo 3.5 (Inception)

### Custom User-Skills

The `notebooklm` skill is used in Demo 2.5 and Exercise 2.5. Install:

```bash
# Clone the skill into your user skills directory
mkdir -p ~/.claude/skills
# (Replace with actual source — placeholder until upstream URL)
git clone <notebooklm-skill-repo> ~/.claude/skills/notebooklm
```

Verify with `/skills` — `notebooklm` should appear in the list.

### Prepared Hook Files

Demo 2.2 (Hooks — The Alarm System) uses a pre-prepared hook file at `~/.claude/hooks/security-check.sh`. Create it before the demo:

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

Reference this hook in your `~/.claude/settings.json`:

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

### Codex CLI (optional, for Demo 3.2)

Demo 3.2 (Codex Swarm) optionally requires the OpenAI Codex CLI. Install if you want to follow the live demo hands-on:

```bash
# Install Codex CLI (replace with actual install command for your system)
# Check codex --version after install
codex --version
codex auth status   # ensure authenticated
```

If Codex is not installed, the demo can still be observed but not replicated locally.

### Verification

After all installs, run a quick verification:

```bash
claude plugin list                      # should show 3 plugins
/skills                                 # should show notebooklm
ls ~/.claude/hooks/security-check.sh    # should exist + be executable
notebooklm list                         # should show claude-code-docs
```

---

## Workdir Convention

Use a single workspace root for all workshop content:

```bash
mkdir -p ~/cc-workshop
```

Inside, this structure:

```
~/cc-workshop/
├── demos/              # Live demo workdirs (one per demo: demo-1.1, demo-1.2, ...)
├── exercises/          # Exercise workdirs (one per exercise: exercise-1.1, ...)
└── workshop-playground/   # Cloned from the workshop repo
```

This way:
- All workshop artifacts in one place
- Easy to clean up after workshop (`rm -rf ~/cc-workshop`)
- Demos and exercises don't pollute your home directory

