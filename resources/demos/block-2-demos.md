# Block 2: Demo Scripts — Ecosystem

**For the moderator.** Each demo has exact commands, expected output, recovery steps, and talking points.
Audience: experienced programmers from physical security.
Total demo time budget: ~35 minutes across 5 demos.

---

## Demo 2.1: Skills in Action (~8 minutes)

### Goal
Show what skills look like, how they're invoked, and why they're more powerful than typing instructions every time.

### Setup (before demo)
- Have a terminal open in any project directory
- Have `~/.claude/skills/` available (even if empty)
- Optionally: have a simple `email-validator.js` stub ready but NOT tested

### Step-by-Step Script

**Step 1: Show available commands (1 min)**

In Claude Code, type:
```
/help
```

Walk through the output. Point out:
- Built-in commands (like `/compact`, `/clear`)
- Custom commands from installed plugins
- Say: *"These are the alarm buttons. Each one triggers a specific SOP."*

**Step 2: List user skills (1 min)**

In your terminal:
```bash
ls ~/.claude/skills/
```

Or in Claude Code:
```
list my skills
```

Show whatever is there. If the audience has `agent-orchestrator` or `tdd` installed, highlight one. Say: *"These are my personal SOPs — available in every project on this machine."*

**Step 3: Invoke TDD skill to build an email validator (5 min)**

In Claude Code:
```
/tdd
```

If `/tdd` is not installed as a command, type:
```
Use TDD to implement an email validator function. Start with the failing test.
```

Walk through what happens:
1. Claude asks what to implement (or starts directly)
2. Claude writes the test FIRST — show it to the audience
3. Claude runs the test → it FAILS (red) — show the red output
4. Claude writes minimal implementation
5. Claude runs the test → it PASSES (green) — show the green output

Say: *"I didn't tell Claude to do TDD. I invoked the skill — or used the trigger phrase — and Claude followed the entire SOP automatically. No reminder, no repetition."*

**Step 4: Show the SKILL.md file (1 min)**

```bash
cat ~/.claude/skills/tdd/SKILL.md
# Or if it's a plugin skill:
cat ~/.claude/plugins/cache/superpowers-marketplace/skills/test-driven-development/SKILL.md
```

Point out:
- YAML frontmatter with trigger phrases
- The actual workflow steps in the body
- Say: *"This is the SOP. A text file. You can edit it, version it, share it with your team."*

### Talking Points
- "Skills are SOPs — standard operating procedures stored as text files."
- "Commands are the alarm buttons that trigger them."
- "User skills in `~/.claude/skills/` follow you across every project."
- "You can write your own skills for any repetitive workflow — your team's code review checklist, your deployment procedure, your incident response steps."

### Recovery if TDD skill is not installed
```
Let's implement an email validator with tests. Write the failing test first, then implement, then verify the test passes. Follow strict red-green-refactor — no implementation before a failing test exists.
```
This manually triggers the TDD workflow. Then say: *"I just did this manually. With a skill, I'd type `/tdd` and Claude already knows all of this."*

---

## Demo 2.2: Hooks — The Alarm System (~7 minutes)

### Goal
Show that hooks fire automatically in response to Claude's actions, can block dangerous operations, and require zero user intervention once configured.

### Setup (before demo)
- Have `~/.claude/settings.json` with at least one hook configured
- Ideally: have the innerHTML security hook active (warns on `innerHTML` in JS files)
- Alternatively: have a simple echo hook that logs tool calls

### Step-by-Step Script

**Step 1: Show the hooks configuration (2 min)**

```bash
cat ~/.claude/settings.json | jq '.hooks'
# If jq not available:
cat ~/.claude/settings.json
```

Walk through the structure:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/security-check.sh"
          }
        ]
      }
    ]
  }
}
```

Say: *"Three sections: which event (PreToolUse), which tool (Bash), what to run (a shell script). That's it."*

**Step 2: Trigger the innerHTML security hook (3 min)**

In Claude Code:
```
Add a div to the page and set its content to the user's name using innerHTML
```

Watch what happens:
- Claude writes the code with `innerHTML`
- The PostToolUse hook fires
- A warning appears: something like *"Security: innerHTML usage detected. Prefer textContent for user-controlled data."*

Say: *"I didn't ask Claude to check for security issues. The hook fired automatically when Claude wrote that code. It's a sensor on the edit action — not a reminder I have to give every session."*

**Step 3: Show the hook script (1 min)**

```bash
cat ~/.claude/hooks/security-check.sh
# Or wherever the hook is
```

Show that it's just a bash script. It reads JSON from stdin (the tool call data), checks for patterns, and either exits 0 (allow) or exits 1 (block + print warning).

Say: *"This is a motion sensor. It's always on. You configure it once and it watches every action Claude takes."*

**Step 4: Mention blocking (1 min)**

Say: *"PreToolUse hooks can also BLOCK. If this hook exits with code 1, Claude Code stops the action entirely — like a door that won't open. PostToolUse hooks are reactive — they log or notify after the fact, but can't undo the action."*

### Talking Points
- "Hooks are the sensors in your alarm system — they fire on events, not on user requests."
- "PreToolUse = sensor that checks before the door opens. Can lock it."
- "PostToolUse = sensor that logs after someone passes through."
- "Stop = end-of-shift alarm — fires when Claude finishes responding."
- "One hook configuration protects every Claude Code session, every project, every team member using the same config."
- "You can enforce your security standards, your coding conventions, your compliance requirements — automatically."

### Recovery if hooks aren't configured
Live-configure one during the demo:

```bash
# Add a simple logging hook to settings.json
```

Or show the structure conceptually and say: *"We'll configure this in Exercise 2.2 — you'll build a safety hook yourselves."*

---

## Demo 2.2b: Secure Diff Gate — Write Protection via Hook (~5 minutes)

### Goal
Show a PreToolUse hook that **blocks** Claude from writing to sensitive files (`.env`, `secrets/`, `*.pem`). This is the "access control for code" pattern from the deep research.

### Setup (before demo)
Add to `.claude/settings.json` in the demo project:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'INPUT=$(cat); FILE=$(echo \"$INPUT\" | jq -r .file_path // .path // \"\" ); if echo \"$FILE\" | grep -qE \"(\\.env|\\.pem|secrets/|credentials)\"; then echo \"BLOCKED: Write to protected path: $FILE\" >&2; exit 1; fi; exit 0'"
          }
        ]
      }
    ]
  }
}
```

### Steps

**Step 1: Show the hook config (1 min)**

Open the settings file and explain:
- Matcher `Write|Edit` fires on any file modification
- The script checks the target path against a pattern
- If it matches `.env`, `.pem`, `secrets/`, or `credentials` → exit 1 = BLOCK

Say: *"This is a door controller with a deny-list. These paths are like the server room — no entry without explicit override."*

**Step 2: Trigger the block (2 min)**

In Claude Code:
```
Create a .env file with DATABASE_URL=postgres://localhost/mydb
```

Watch Claude attempt the write → hook fires → **BLOCKED** message appears → Claude reports it cannot proceed.

Say: *"Claude didn't decide to skip the .env file. The hook physically blocked the write. It's not a suggestion — it's a locked door."*

**Step 3: Show it allows normal writes (1 min)**

```
Create a file called utils.py with a hello world function
```

This goes through — the hook checks the path, finds no sensitive pattern, exits 0.

Say: *"Normal doors open normally. Only the protected zones are locked. Least privilege in action."*

### Talking Point
*"In your access control world, you have zones. Some doors are always open (lobby), some require a badge (offices), some are permanently locked without explicit authorization (vault). This hook is the vault policy for your code."*

### Recovery Notes

- **If the hook bash-quoting breaks live:** Have a pre-prepared `secure-diff-gate.sh` file ready (in `~/.claude/hooks/`) as fallback. Reference it via `command: bash ~/.claude/hooks/secure-diff-gate.sh`.
- **If `jq` not installed (Windows):** Use a Python alternative: `python3 -c "import sys,json; d=json.load(sys.stdin); ..."` — note that prerequisites.md should list `jq` or `python3` requirement.
- **If the hook fires but doesn't block (exit 0 instead of 1):** Check the bash conditional — `grep -qE` must match. Test the regex outside Claude with `echo ".env" | grep -qE "(\.env|\.pem)"; echo $?`.
- **If `settings.json` parse fails:** Common cause is unescaped quotes in the bash inline command. Move the script to its own file and reference by path.

---

## Demo 2.3: Plugin Anatomy (~5 minutes)

### Goal
Show that a plugin is just a directory with well-structured files — not magic, not compiled, fully readable and modifiable.

### Setup (before demo)
- Know the path to `~/.claude/plugins/cache/`
- Have at least one plugin installed (agentic-os is ideal)

### Step-by-Step Script

**Step 1: List installed plugins (1 min)**

```bash
ls ~/.claude/plugins/cache/
```

Show the list. Note the naming convention: `pluginname-marketplace`. Say: *"Each directory is one plugin. Let's open one."*

**Step 2: Explore the plugin structure (2 min)**

```bash
ls ~/.claude/plugins/cache/agentic-os-marketplace/
# Expected: plugin.json  skills/  commands/  agents/  hooks/ (varies)

cat ~/.claude/plugins/cache/agentic-os-marketplace/plugin.json
```

Walk through plugin.json:
- `name`, `version`, `description`
- `skills` array — lists what skills this plugin provides
- `commands` array — what slash commands get added
- `agents` array — autonomous sub-processes
- `enabled: true` — can be set to false to disable without deleting

Say: *"This is the wiring diagram — the manifest. Everything in this plugin is listed here."*

**Step 3: Read one skill and one agent (2 min)**

```bash
ls ~/.claude/plugins/cache/agentic-os-marketplace/skills/
cat ~/.claude/plugins/cache/agentic-os-marketplace/skills/wrap-up/SKILL.md | head -30
```

Point out the YAML frontmatter and the markdown body.

```bash
ls ~/.claude/plugins/cache/agentic-os-marketplace/agents/
cat ~/.claude/plugins/cache/agentic-os-marketplace/agents/quality-reviewer.md | head -20
```

Say: *"Agents are like specialized team members — each has a role, a set of responsibilities, and instructions for how to operate."*

### Talking Points
- "A plugin is a self-contained security module — sensors (hooks), procedures (skills), team roles (agents), and control buttons (commands) — all in one package."
- "It's just files. You can read every line, modify every instruction, fork it for your team's specific needs."
- "Install once, available everywhere. Update via git pull."
- "Disable without deleting: rename plugin.json to plugin.json.disabled."
- "Your team can build plugins for your specific workflows and distribute them internally."

### Recovery Notes

- **If agentic-os plugin not installed:** Any installed plugin works. Run `claude plugin list` to find one, then `cat ~/.claude/plugins/cache/<plugin-name>/.claude-plugin/plugin.json`.
- **If no plugins installed at all:** Live-clone the workshop-mentor plugin from this repo: `cp -r .claude-plugin/ /tmp/demo-plugin/.claude-plugin/` and inspect.
- **If the plugin's cache path differs (newer Claude Code versions):** Try `~/.claude/plugins/installed/<plugin-name>/` or run `claude plugin path <plugin-name>` to locate.
- **If `plugin.json` is in `.claude-plugin/` subdirectory:** That's the newer schema — show `~/.claude/plugins/cache/<plugin>/.claude-plugin/plugin.json` instead of the root.

---

## Demo 2.4: MCP — Browser Control (~8 minutes)

### Goal
Show that Claude can control a real browser — not simulate it, not scrape static HTML, but actually navigate, click, and interact with live web pages.

### Setup (before demo)
- Playwright MCP server must be configured in `.mcp.json` or `~/.claude/.mcp.json`
- Internet access required
- Configuration:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### Step-by-Step Script

**Step 1: Set the stage (1 min)**

Say: *"MCP connects Claude Code to external systems. The most visceral example is browser control via Playwright. Watch — Claude is about to control a real browser."*

**Step 2: Navigate to GitHub (1 min)**

In Claude Code:
```
Navigate to github.com/anthropics/claude-code using the browser
```

Claude calls the Playwright MCP tool. A browser window opens (or headless, depending on config) and navigates to the URL.

Take a screenshot:
```
Take a screenshot of the current page
```

Show the screenshot in the terminal output.

**Step 3: Interact with the page (3 min)**

```
Click on the Issues tab
```

Claude clicks the Issues tab. Show the result.

```
List the titles of the first 5 open issues
```

Claude reads the page and extracts the issue titles. Show the list.

Say: *"This is a real browser. JavaScript executed, dynamic content loaded, actual DOM elements clicked. Not HTTP requests, not scraping — actual browser automation."*

**Step 4: Connect to the use case (3 min)**

Say: *"Think about what this means for your work."*

Offer examples based on the audience (physical security software):
- *"Your access control admin panel — Claude could log in, pull door event reports, export them, send them to your monitoring system."*
- *"Your manufacturer's firmware update portal — Claude could check for new versions, download, log the update history."*
- *"Your alarm panel web interface — Claude could acknowledge alarms, generate end-of-day reports, check zone status."*

Say: *"Any web interface your team uses manually can be automated with MCP Playwright. And this is just one MCP server — there are servers for Slack, email, databases, and you can build custom ones for your own systems."*

### Talking Points
- "MCP is the access control system connecting to external building systems — fire alarm, CCTV, visitor management. Claude is the central control panel."
- "One protocol, many integrations. Learn it once, connect anything."
- "Playwright MCP turns any web interface into an API that Claude can drive."
- "Security note: MCP servers run with your credentials. This is why hooks and guardrails matter even more here."

### Recovery if Playwright MCP not configured
Show the configuration file and explain what it would do. Say: *"We'll configure this in Exercise 2.4. For now — believe me, it works, and you'll try it yourself."*

Alternatively: show a screenshot taken earlier during prep and describe what happened.

---

## Demo 2.5: NotebookLM as Knowledge Base (~7 minutes)

### Goal
Show that Claude can answer questions from a specific, verifiable knowledge source — not from training data — and that this eliminates hallucination risk for domain-specific queries.

### Setup (before demo)
- `notebooklm` user skill installed (`~/.claude/skills/notebooklm/`)
- A notebook already created with some sources (prepare this before the session — notebook creation and source indexing takes a few minutes)
- Suggested: notebook with Anthropic Claude Code docs, or your own project documentation

### Step-by-Step Script

**Step 1: Explain the problem (1 min)**

Say: *"Claude's training data has a cutoff. For recent APIs, internal tools, or niche topics, it might guess wrong. Let me show you how to give Claude a verified knowledge source."*

**Step 2: Show the notebook workflow (2 min)**

Say: *"I've already created a notebook and added some sources. Here's how that looks."*

Reference a pre-created notebook:
```
notebooklm list
```

Or if using the skill:
```
/notebooklm navigate
```

Show the notebook name and source count. For example: "Claude Code Documentation — 4 sources, 12,000 words indexed."

**Step 3: Query the notebook (3 min)**

In Claude Code:
```
notebooklm use claude-code-docs
notebooklm ask "What is the correct JSON structure for a PreToolUse hook in settings.json?"
```

Watch Claude respond. Key things to point out:
- The answer includes **citations** — which source page it came from
- The answer is specific, not generic
- No hallucination risk because it's retrieval from actual documents

Now ask something Claude would normally struggle with:
```
notebooklm ask "What are the valid matcher patterns for hooks, and what tool names can I match against?"
```

Say: *"This is an exact, specific question. Without the notebook, Claude would either answer from general training data (potentially wrong) or admit uncertainty. With the notebook — it searches the actual documentation and gives you the answer with a citation."*

**Step 4: The contrast (1 min)**

Ask the same question WITHOUT the notebook:
```
(new context) What are the valid matcher patterns for hooks in Claude Code settings.json?
```

Claude gives a reasonable-sounding answer — but it may be outdated, incomplete, or slightly wrong.

Say: *"Same question. Different quality. This is the difference between 'general security knowledge' and 'your actual building blueprints.'"*

### Talking Points
- "RAG = giving Claude your actual blueprints instead of general knowledge."
- "NotebookLM is a hosted RAG system — no ML infrastructure required, works immediately."
- "Answers come with citations — verifiable, not guessed."
- "Use cases: internal docs, current API docs, compliance text, your team's accumulated knowledge."
- "The pattern that scales: identify what Claude needs to know that isn't in its training, build a notebook, configure Claude to check it first."

### Recovery if notebook skill not configured
Demonstrate the concept via the NotebookLM web UI instead:
- Open `notebooklm.google.com`
- Show an existing notebook with sources
- Ask a question in the web UI
- Say: *"The skill wraps this same API so you can query from your terminal. Exercise 2.5 is where you build your own."*
