# Block 2: Exercises — Ecosystem

**For participants.** Each exercise has a Goal, Steps, Success Check, and Hints.
Time estimate per exercise: 25-30 minutes (Exercise 2.5 with NotebookLM setup runs longer, 30-40 min).
Do them in order — each builds on the last.
Audience: experienced programmers. Security analogies used throughout.

---

## Exercise 2.1: Build Your First Skill

### Goal
Turn a workflow you already repeat manually into a reusable skill. After this exercise, you will never have to type the same instructions twice.

### Background
Think of a task you do repeatedly in your projects:
- Code review with a specific checklist
- Setting up a new feature branch with certain steps
- Running through a debugging process in a consistent order
- Writing commit messages in your team's format
- Generating documentation from code

You're about to write the SOP for that task — as a SKILL.md file.

### Steps

**Step 1: Identify your repetitive task**

Pick something specific. The more concrete, the better. Example: "Before every commit, I always check that tests pass, no debug logs are left in, and the commit message follows our format."

Write it down in plain language first. What steps do you always follow? What rules do you always apply?

**Step 2: Create the skill directory**

```bash
# Create a directory for your skill under user skills
mkdir -p ~/.claude/skills/my-first-skill

# Verify it exists
ls ~/.claude/skills/
```

Name it something meaningful — use lowercase and hyphens: `pre-commit-check`, `feature-setup`, `debug-workflow`, etc.

**Step 3: Write the SKILL.md file**

Create `~/.claude/skills/my-first-skill/SKILL.md`:

```bash
# Open in your editor, or create via Claude Code:
# "Create a SKILL.md file in ~/.claude/skills/my-first-skill/ for a pre-commit checklist skill"
```

Your SKILL.md needs:

```markdown
---
name: my-first-skill
description: >
  [One sentence explaining what this skill does].
when_to_use: >
  [List 3-5 trigger situations or phrases that should activate this skill].
argument-hint: "[target]"
arguments: [target]
---

# [Skill Name]

[Detailed instructions for Claude to follow]

## Step 1: [First thing Claude should do]
[Details]

## Step 2: [Second thing]
[Details]

## Rules
- [Non-negotiable rules Claude must follow]
- [Add as many as needed]
```

**Step 4: Test the skill by invoking it**

Open or restart Claude Code. Then trigger your skill:

Option A — direct invocation:
```
/my-first-skill
```

Option B — trigger phrase (Claude matches from description):
```
[use one of the trigger phrases you wrote in the description]
```

Option C — explicit reference:
```
Use the my-first-skill skill to [describe your task]
```

**Step 5: Iterate**

Watch how Claude performs. Does it follow all the steps? Does it miss anything? Is a step too vague?

Edit the SKILL.md to fix it. Test again. Repeat until Claude follows the SOP exactly as you intended.

### Success Check

You've succeeded when:
- [ ] `ls ~/.claude/skills/` shows your new skill directory
- [ ] The SKILL.md has valid YAML frontmatter with `name`, `description`, and `when_to_use`
- [ ] Claude follows your skill's instructions without you repeating them
- [ ] You've edited the skill at least once to improve it
- [ ] The skill works the same way in a new Claude Code session (restart and try)

### Hints

**If Claude doesn't pick up the skill automatically:**
Check that your trigger phrases in the `description` field match what you're typing. The description field uses YAML block scalar (`>`), so make sure it's formatted correctly.

**If the skill is too vague:**
Add concrete examples. Instead of "review the code", write "check for: (1) missing error handling, (2) debug console.log statements, (3) variable names shorter than 3 characters".

**If you're not sure what task to use:**
Use this: "Before every git commit, check that (1) all tests pass, (2) no TODO comments were added without a ticket number, (3) the staged files match what I said I was changing, (4) the commit message follows Conventional Commits format."

**Finding inspiration:**
Look at your chat history with Claude Code — what instructions do you repeat? Those are candidates for skills.

---

## Exercise 2.2: Build a Safety Hook

### Goal
Create a PreToolUse hook that warns (or blocks) before Claude runs potentially dangerous shell commands. After this exercise, you have an automatic safety net that fires every session — no reminder needed.

### Background
In access control terms: you're installing a sensor on the bash tool. Every time Claude runs a bash command, your sensor fires. If the command matches a dangerous pattern, the sensor raises an alarm (warning) or locks the door (block).

This is one of the highest-value exercises in the workshop. Once configured, this hook protects you silently, forever.

### Steps

**Step 1: Locate or create your settings.json**

```bash
# Global settings (applies to all projects):
cat ~/.claude/settings.json

# If it doesn't exist, create it:
echo '{}' > ~/.claude/settings.json
```

Check if there's already a `hooks` section. If so, you'll add to it. If not, you'll create it.

**Step 2: Create the hook script**

Create `~/.claude/hooks/safety-check.sh`:

```bash
mkdir -p ~/.claude/hooks
```

Write the script:

```bash
#!/bin/bash

# Read the tool input from stdin (Claude passes it as JSON)
INPUT=$(cat)

# Extract the command that Claude wants to run
# The field name depends on the tool — for Bash it's "command"
COMMAND=$(echo "$INPUT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('command', ''))" 2>/dev/null || echo "")

# Define dangerous patterns to check
DANGEROUS_PATTERNS=(
  'rm\s+-rf'
  'git push.*--force'
  'git push.*-f\b'
  'DROP TABLE'
  'truncate.*--yes'
  'mkfs\.'
  'dd\s+if=.*of=/dev/'
  '> /dev/sd'
)

# Check each pattern
for PATTERN in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiE "$PATTERN"; then
    echo "SAFETY HOOK: Potentially destructive command detected!" >&2
    echo "Command: $COMMAND" >&2
    echo "Pattern matched: $PATTERN" >&2
    echo "Hook blocked execution. Review and run manually if intended." >&2
    # Exit 1 to BLOCK the command
    exit 1
  fi
done

# All checks passed — allow the command
exit 0
```

```bash
# Make it executable
chmod +x ~/.claude/hooks/safety-check.sh
```

**Step 3: Register the hook in settings.json**

Edit `~/.claude/settings.json` to add the hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/safety-check.sh"
          }
        ]
      }
    ]
  }
}
```

If settings.json already has content, add the `hooks` section carefully — don't break the JSON structure.

**Step 4: Test it**

Restart Claude Code (hooks are read at startup), then:

```
Run: rm -rf /tmp/test-directory
```

Expected: Claude tries to run it, your hook fires, Claude Code shows the warning/block message, the command does NOT execute.

Try a safe command to verify normal operation:
```
Run: echo "hello world"
```

Expected: no hook message, command runs normally.

**Step 5 (Bonus): Add PostToolUse logging**

Add a second hook that logs all bash commands to a file:

Create `~/.claude/hooks/audit-log.sh`:

```bash
#!/bin/bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('command', ''))" 2>/dev/null || echo "unknown")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] BASH: $COMMAND" >> ~/.claude/audit.log
exit 0
```

```bash
chmod +x ~/.claude/hooks/audit-log.sh
```

Add to settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/safety-check.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/audit-log.sh"
          }
        ]
      }
    ]
  }
}
```

After running some Claude commands, inspect the log:
```bash
cat ~/.claude/audit.log
```

### Success Check

You've succeeded when:
- [ ] `~/.claude/hooks/safety-check.sh` exists and is executable (`chmod +x`)
- [ ] `~/.claude/settings.json` has a valid `hooks.PreToolUse` section pointing to your script
- [ ] Asking Claude to run `rm -rf` is blocked by your hook
- [ ] Asking Claude to run `echo "hello"` succeeds without any hook warning
- [ ] (Bonus) `~/.claude/audit.log` grows with entries as Claude runs commands

### Hints

**If the hook fires but doesn't block:**
Make sure the script exits with `exit 1` for dangerous patterns, not `exit 0`. Exit code 0 = allow, non-zero = block.

**If the JSON parsing fails:**
The `python3 -c` approach is robust. If python3 is not available, try:
```bash
COMMAND=$(echo "$INPUT" | grep -o '"command":"[^"]*"' | cut -d'"' -f4)
```

**If settings.json is invalid JSON after editing:**
Validate it:
```bash
python3 -m json.tool ~/.claude/settings.json
```

**Hook execution order:**
If you have multiple hooks for the same event and tool, they run in array order. The first one to exit non-zero blocks the action.

**What data does the hook receive?**
Claude passes the tool input as JSON to stdin. For the Bash tool, it looks like:
```json
{"command": "rm -rf /tmp/test"}
```
For Edit, it includes `file_path`, `old_string`, `new_string`. You can log the raw input to inspect it: `echo "$INPUT" >> ~/.claude/debug.log`

---

## Exercise 2.3: Plugin Exploration

### Goal
Understand the anatomy of a real plugin by reading it. Then scaffold the structure of your own mini plugin. After this exercise, plugins are no longer mysterious — they're just directories of files you can read and modify.

### Background
You already work with systems built from modular components — alarm modules, access control panels, reader modules. Each has a clear structure. You don't need to understand the internal electronics to install and configure them, but you do need to understand the interface.

Claude Code plugins work the same way. Read the structure, understand the interface, and you can extend, modify, or build your own.

### Steps

**Step 1: Explore a plugin**

> **Note:** This exercise uses a workshop-provided plugin. If it's not installed,
> ask the workshop leader or use any plugin you have available under `~/.claude/plugins/cache/`.
> Alternatively, explore the workshop plugin itself at `dynamic_workshop/` (same structure).

```bash
# See what plugins are installed
ls ~/.claude/plugins/cache/

# Pick one and go inside it
ls ~/.claude/plugins/cache/<plugin-name>/
```

Read the manifest:
```bash
cat ~/.claude/plugins/cache/<plugin-name>/.claude-plugin/plugin.json
```

> **Note:** The plugin manifest MUST live at `.claude-plugin/plugin.json` (inside a `.claude-plugin/` subdirectory),
> NOT in the plugin root — common mistake. If `cat` above fails, your plugin
> may use the legacy layout; check both locations.

Answer these questions (write them down):
- What version is this plugin?
- How many skills does it list?
- Does it have commands? If so, which ones?
- Is there a `dependencies` field? What does it say?

**Step 2: Read a Skill in depth**

```bash
# List available skills
ls ~/.claude/plugins/cache/<plugin-name>/skills/

# Pick one and read it fully — look for the SKILL.md file
cat ~/.claude/plugins/cache/<plugin-name>/skills/<skill-name>/SKILL.md
```

Answer:
- What trigger phrases does this skill have?
- What steps does it tell Claude to follow?
- Is there anything surprising — something Claude is told to do that you wouldn't have thought to specify?

**Step 3: Read an Agent definition**

```bash
ls ~/.claude/plugins/cache/<plugin-name>/agents/
cat ~/.claude/plugins/cache/<plugin-name>/agents/*.md | head -60
```

Answer:
- How does an agent differ from a skill? (Hint: look at the role/persona described)
- Is the agent reactive (waits to be called) or proactive (runs autonomously)?

**Step 4: Scaffold your own mini plugin**

Create a minimal plugin structure for a hypothetical plugin relevant to your work. For example: `door-audit-plugin` (checks access logs and generates reports), or `firmware-tracker` (tracks firmware versions across devices), or `incident-checklist` (runs through your incident response SOP).

```bash
# Create the plugin directory
mkdir -p ~/.claude/plugins/cache/my-mini-plugin-marketplace/.claude-plugin
mkdir -p ~/.claude/plugins/cache/my-mini-plugin-marketplace/skills/my-skill
mkdir -p ~/.claude/plugins/cache/my-mini-plugin-marketplace/commands

# Create the manifest at .claude-plugin/plugin.json (NOT in the plugin root)
cat > ~/.claude/plugins/cache/my-mini-plugin-marketplace/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-mini-plugin",
  "version": "0.1.0",
  "description": "My first plugin — [describe what it does]",
  "author": "[your name]",
  "skills": ["my-skill"],
  "commands": ["my-command"],
  "agents": [],
  "enabled": true
}
EOF
```

The resulting layout:

```
my-mini-plugin-marketplace/
  .claude-plugin/
    plugin.json
  skills/
    my-skill/
      SKILL.md
  commands/
    my-command.md
```

> **Important:** The manifest MUST live at `.claude-plugin/plugin.json`, not in the plugin root.
> Module 2.3 covers why — Claude Code's loader only looks at `.claude-plugin/plugin.json`.

Create a skill:
```bash
cat > ~/.claude/plugins/cache/my-mini-plugin-marketplace/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: >
  [What this skill does].
when_to_use: >
  [Your trigger phrases and situations]
---

# My Skill

[Your skill instructions here]
EOF
```

Create a command:
```bash
cat > ~/.claude/plugins/cache/my-mini-plugin-marketplace/commands/my-command.md << 'EOF'
---
name: my-command
description: [What this command does]
user_invocable: true
---

# My Command

When invoked, execute the my-skill skill.
EOF
```

**Step 5: Verify the plugin loads**

Restart Claude Code and type:
```
/help
```

Look for your new command in the list. Try invoking it.

### Success Check

- [ ] You can navigate the agentic-os plugin structure from the command line
- [ ] You've answered the questions about skill anatomy and agent anatomy
- [ ] `~/.claude/plugins/cache/my-mini-plugin-marketplace/.claude-plugin/plugin.json` exists and is valid JSON
- [ ] Your mini plugin has at least one skill and one command
- [ ] (Stretch) Your new command appears in `/help` and can be invoked

### Hints

**If the plugin doesn't appear after restart:**
Check that `.claude-plugin/plugin.json` is valid JSON (`python3 -m json.tool .claude-plugin/plugin.json`), and that `"enabled": true` is set. The single most common reason a plugin is silently skipped: the manifest sits in the plugin root instead of under `.claude-plugin/`.

**What makes a good plugin?**
Cohesion. A plugin should do one thing well. Don't put your commit workflow and your documentation generator in the same plugin — make two plugins. This way you can enable/disable them independently.

**Team distribution:**
Once you have a working plugin, share it by zipping the directory or putting it in a git repo. Teammates drop the directory into `~/.claude/plugins/cache/` and they have the same capabilities.

**Disabling without deleting:**
```bash
mv .claude-plugin/plugin.json .claude-plugin/plugin.json.disabled
# Re-enable:
mv .claude-plugin/plugin.json.disabled .claude-plugin/plugin.json
```

---

## Exercise 2.4: Connect an MCP Server

### Goal
Configure the Playwright MCP server and use it to automate browser interactions. After this exercise, you will have made Claude control a real browser — and you'll understand what this means for automation in your domain.

### Background
In physical security, you integrate external systems — fire panels, CCTV, intercom — into your central access control platform. Each system exposes an interface, and the platform connects to it.

MCP is that integration protocol for Claude Code. Playwright is one of the most powerful MCP servers: it gives Claude a real browser. Any web interface your team uses manually becomes automatable.

### Steps

**Step 1: Install Playwright MCP**

```bash
# Verify npx is available
npx --version

# Test that Playwright MCP can start
npx @playwright/mcp@latest --help
```

If npx is not available, install Node.js first.

**Step 2: Configure the MCP server**

Create or edit `~/.claude/.mcp.json` (global) or `.mcp.json` in your project root (project-level):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {}
    }
  }
}
```

```bash
# Verify the JSON is valid
python3 -m json.tool ~/.claude/.mcp.json
```

**Step 3: Restart Claude Code and verify**

Restart Claude Code. Then check if the Playwright tools are available:

```
What browser tools do you have available?
```

Claude should list tools like `browser_navigate`, `browser_click`, `browser_take_screenshot`, `browser_snapshot`.

**Step 4: Navigate and screenshot**

```
Navigate to example.com using the browser and take a screenshot
```

Claude should:
1. Call the navigate tool with `https://example.com`
2. Call the screenshot tool
3. Display or describe the screenshot

If a screenshot image appears in the terminal — success.

**Step 5: Interact with a page**

```
Navigate to github.com/anthropics and list the first 5 repositories shown on the page
```

Claude navigates, reads the page, and returns a list. This is real DOM content, not cached data.

**Step 6: Explore automation possibilities**

Think about your work context. Pick a web interface your team uses and describe what Claude could automate. Examples:
- "Our controller management portal — Claude could log in, pull all door event logs for the last 24 hours, and flag any after-hours access."
- "Our firmware update site — Claude could check if new firmware is available for each device model we manage."
- "Our ticketing system — Claude could find all open tickets tagged 'access request' and summarize them."

Discuss with the person next to you: What's the highest-value web automation for your team?

**Step 7 (Bonus): Automate a multi-step workflow**

```
Navigate to [a site you use], [describe a multi-step task], and report back what you found
```

Try a real multi-step sequence. Note any failures (page load timing, authentication, JavaScript challenges) — these are normal and solvable with Playwright's wait commands.

### Success Check

- [ ] `.mcp.json` exists and contains a valid Playwright configuration
- [ ] After restarting, Claude lists browser tools when asked
- [ ] Claude successfully navigated to at least one URL
- [ ] A screenshot was taken and displayed/described
- [ ] Claude listed content from a live web page
- [ ] (Bonus) A multi-step interaction completed successfully

### Hints

**If Claude says Playwright tools are not available:**
Check that `.mcp.json` is valid JSON. Check that `npx @playwright/mcp@latest` runs without error in a terminal. Verify Claude Code was restarted after creating the config.

**If navigation times out:**
Playwright may need a moment to start up the first time. Try again — subsequent calls in the same session are faster.

**Authentication:**
Playwright runs in a browser context. If you need to log into a site, tell Claude:
```
Navigate to [site], fill in username [X] and password [ask me for it], then [task]
```
Claude will ask for the password rather than storing it.

**Headless vs. headed mode:**
By default, Playwright MCP may run headless (no visible window). To see the browser: check `@playwright/mcp` documentation for `--headed` flag.

**Security consideration:**
The Playwright browser runs with your network access. Be thoughtful about which sites you automate, especially in corporate environments with proxies or SSO.

---

## Exercise 2.5: Your Personal Knowledge Base

### Goal
Create a NotebookLM notebook for a domain relevant to your work, add real sources, query it from Claude Code, and experience the difference between "general knowledge" and "your verified sources."

### Background
Every experienced professional has accumulated knowledge that isn't on the general internet: your organization's specific procedures, your product line's quirks, your accumulated troubleshooting experience.

When you ask Claude about your specific access control product line, your proprietary protocol, or your customer's installation standards — Claude is guessing. It doesn't know. This exercise shows you how to fix that.

### Steps

**Step 1: Identify your knowledge domain**

Pick a domain where you often wish Claude had more specific knowledge. Examples:
- A specific access control product line (OSDP protocol, specific panel models)
- Your organization's security standards or installation guidelines
- A regulatory framework your projects must comply with
- A technology you work with that has recent changes (firmware, APIs)
- Your accumulated troubleshooting knowledge for a specific system type

**Step 2: Create a NotebookLM notebook**

1. Go to `notebooklm.google.com`
2. Click "New Notebook"
3. Name it something specific: "OSDP Protocol Reference" or "EN 50132 Standard Notes"

**Step 3: Add at least 3 sources**

Choose sources that contain real, specific knowledge for your domain:

Good source types:
- Product documentation PDFs
- Official standard or regulation pages
- Technical specification URLs
- Your own written documentation (paste as text)
- YouTube tutorials on your specific technology

In the NotebookLM web UI: click "Add sources" and upload/paste/link.

Wait for NotebookLM to process the sources (usually 1–3 minutes for URLs, longer for PDFs).

**Step 4: Query WITHOUT the notebook first**

Open Claude Code in a fresh context and ask a specific question from your domain — something that requires knowledge from your sources:

```
[Ask a specific technical question about your domain]
```

Note the quality of the answer. Is it:
- Correctly specific to your domain?
- Using the right terminology?
- Citing the right standards or specifications?
- Confident when it should be uncertain?

Write down the answer (or at least your assessment of its quality).

**Step 5: Query WITH the notebook**

Now use NotebookLM to get a grounded answer:

1. Ask the same question in the NotebookLM web UI chat
2. Copy the answer (including source citations) into a file: `research-notes.md`
3. In Claude Code, include this context and ask again:

```
@research-notes.md [same question you asked above]
```

Compare the answers:
- Is the second answer more specific?
- Does it cite your actual sources?
- Is it more accurate on the details?
- Does it acknowledge uncertainty where the first answer was falsely confident?

**Step 6: Ask 2–3 more questions**

Explore the boundaries of what your notebook knows:
- Ask something clearly covered by your sources
- Ask something at the edge of what your sources cover
- Ask something your sources definitely don't cover

Notice how NotebookLM handles the third case: it should say it doesn't have enough information, rather than hallucinating.

**Step 7: Reflect and plan**

Answer these questions (discuss with the group if time allows):
1. What's the most valuable knowledge base you could build for your day-to-day work?
2. What sources would you add to it?
3. How would querying this notebook change how you use Claude Code?
4. What's stopping you from building this today?

### Success Check

- [ ] A NotebookLM notebook exists with your chosen domain name
- [ ] At least 3 sources have been added and processed
- [ ] You asked the same question with and without the notebook
- [ ] You noticed a qualitative difference in answer quality or specificity
- [ ] You identified at least one high-value knowledge base you want to build

### Hints

**If you have the custom `notebooklm` skill installed:**
You can also use `/notebooklm create`, `notebooklm add-source`, and `notebooklm ask` directly from Claude Code. This is a custom workshop skill, not a built-in feature.

**If sources take too long to process:**
Add fewer sources (2 is fine) and proceed. Sources index in the background — you can add more later.

**Source quality matters:**
A single well-structured PDF specification is worth more than 10 generic blog posts. Prioritize authoritative sources over volume.

**Discovering trigger phrases:**
When you configure Claude Code to auto-check the notebook (by adding instructions to your CLAUDE.md or a skill), you define which questions should route to NotebookLM. Be specific: "For any question about OSDP protocol, always check the notebook first."

**Taking this further:**
After the workshop, consider:
- Adding your notebook check to a skill's trigger phrases
- Building a weekly-updated notebook for a fast-moving technology
- Creating a shared team notebook for collective knowledge
- Using the `notebooklm` skill's scheduled refresh feature for notebooks with time-sensitive content

---

## Bonus Exercise 2.6: Token Firewall — Hook-Based Output Filtering

**Type:** Individual, ~20 minutes
**Goal:** Build a PreToolUse hook that filters large test outputs before Claude sees them, saving context space and money.

### Background

When Claude runs `npm test` or `pytest` on a large project, the full output can be thousands of lines. Most of that is passing tests — only the failures matter. A "Token Firewall" hook intercepts the Bash output and filters it down to just the failure lines.

This is the equivalent of a CCTV system that only records when motion is detected — instead of recording 24/7 of empty hallways.

### Steps

**Step 1: Create the filter script**

Create `~/.claude/hooks/test-filter.sh`:
```bash
#!/bin/bash
# PostToolUse hook: filters test output AFTER execution to save tokens.
# The hook receives the tool result as JSON on stdin.
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
OUTPUT=$(echo "$INPUT" | jq -r '.output // ""')

# Only filter test command output
if echo "$OUTPUT" | grep -qE '(npm test|pytest|jest|mocha)'; then
  # Show only failures and summary, suppress verbose passing tests
  FILTERED=$(echo "$OUTPUT" | grep -E '(FAIL|ERROR|AssertionError|✗|✘|FAILED|Summary|passed|failed)' | head -50)
  echo "$FILTERED"
  echo "--- [Token Firewall: full output filtered, showing failures only] ---"
fi

exit 0
```

> **Important:** This is a **PostToolUse** hook, not PreToolUse. A PreToolUse hook cannot
> filter tool output — it can only block or allow execution. PostToolUse receives the
> completed tool result and can process it.

**Step 2: Register the hook**

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/test-filter.sh"
          }
        ]
      }
    ]
  }
}
```

**Step 3: Test it**

Ask Claude to run the test suite. Compare the context consumed with and without the filter.

### Success Check

- [ ] The hook fires when Claude runs test commands
- [ ] Only failure lines + summary are shown to Claude
- [ ] Non-test commands are unaffected
- [ ] You measured or estimated the token savings

### Hints

- Add a `--verbose` flag to your hook that lets you bypass the filter when needed
- The `head -50` prevents even filtered output from being too large
- This pattern works for any noisy command: build logs, lint output, dependency installs

---

## Reflection: Block 2 Summary

After completing all exercises, you have:

1. **A skill** that automates your most repetitive instruction pattern
2. **A safety hook** that protects every future Claude Code session automatically
3. **An understanding of plugin anatomy** and your own scaffolded mini plugin
4. **A working MCP connection** to a real browser (and a plan for automation)
5. **A personal knowledge base** that makes Claude an expert in your specific domain
6. **(Bonus) A token firewall** that saves context and money on noisy command outputs

These are not toys. They are infrastructure. Each one you build compounds — your skills accumulate into a toolkit, your hooks enforce standards silently, your plugins distribute team practices, your MCP connections extend Claude's reach into your systems, and your notebooks ground Claude in your real-world knowledge.

The security professionals in this room already think in systems: sensors, procedures, team roles, integrated platforms. You have exactly the mental model needed to build powerful Claude Code setups. The only difference is that the "facility" you're protecting and optimizing is your development workflow.

**Next step:** Block 3 — Building Agents and Multi-Agent Systems.
