# Block 1: Demo Scripts for Moderator

**Purpose:** Live demonstrations to run during Block 1 teaching segments.
**Format:** Exact commands to type, talking points, expected behavior, recovery notes.
**Audience reminder:** Experienced programmers, physical security domain. Use their terminology where possible.

---

## Pre-Demo Checklist

Before starting Block 1:

- [ ] Terminal open, Claude Code installed and authenticated (`claude --version` to confirm)
- [ ] Working directory set to a neutral location (e.g., `~/cc-workshop/demos/`)
- [ ] No sensitive files open or visible
- [ ] Font size bumped up for screen visibility (terminal font size 16+)
- [ ] `gh` (GitHub CLI) authenticated if Demo 1.4 includes PR creation
- [ ] Python 3 available (`python3 --version`)

---

## Demo 1.1: First Contact

**Teaching point this demo supports:** Module 1.1 — What Claude Code is and what it can do.

**Duration:** ~8 minutes

**What participants see:** Claude Code starting, responding to natural language, creating and running a real Python file — all in one terminal window, no copy-pasting, no switching.

---

### Step 1: Start Claude Code

Type in terminal:
```
claude
```

**Expected behavior:** Claude Code starts, shows a welcome prompt. You are now in the interactive session.

**Talking point while it starts:**
> "This is not a browser. This is not a chat window. Notice we are entirely in the terminal. This is where Claude Code lives. Let me show you what it can do from here."

---

### Step 2: Ask Claude to Describe Itself

Type in Claude Code:
```
Describe yourself in exactly 3 bullet points. Focus on what makes you different from a chat interface.
```

**Expected behavior:** Claude responds with 3 concise bullets. They should cover something like: (1) file system access, (2) command execution, (3) git/tool integration. The exact wording varies but the substance will be there.

**Talking point while Claude responds:**
> "Notice it's not saying 'I am a helpful AI assistant.' It's describing its capabilities accurately. It knows it's an agent, not a chat tool. That framing is important."

**Recovery note:** If Claude gives more than 3 bullets, just say "Good, and you can see it respects constraints in the prompt — I said 3 bullets and it gave me 3."

---

### Step 3: Create a Password Generator

Type in Claude Code:
```
Create a Python script called password_gen.py in the current directory.
It should generate secure random passwords. Requirements:
- Configurable length via command-line argument (default 16)
- Uses uppercase, lowercase, digits, and special characters
- Special characters: !@#$%^&*
- Uses Python's secrets module (not random — this needs to be cryptographically secure)
- Prints the generated password to stdout
```

**Expected behavior:** Claude creates the file. It will show the code it wrote. The file appears in the current directory.

**Talking point while Claude writes:**
> "I did not open an editor. I did not write a single line of code. I wrote a specification — a work order — and Claude is implementing it. Watch the file appear."

**Pause and let participants see the code Claude wrote.** Scroll through it briefly.

**Talking point after code appears:**
> "Notice it used `secrets.choice()` not `random.choice()`. I specified 'cryptographically secure' and it knew which Python module that maps to. This is domain knowledge, not just text generation."

---

### Step 4: Run the Script

Type in Claude Code:
```
Run password_gen.py with length 20
```

**Expected behavior:** Claude executes `python3 password_gen.py 20` (or equivalent) and shows the output — a 20-character password.

**Talking point:**
> "It ran it. In the same session. No switching windows. No copy-pasting. Describe what you want → it writes it → it runs it → you see the result. This is the core loop of Claude Code."

**Optional extension (if time allows):**
```
Run it 5 times in a row and show me the output of each run
```
Expected: Claude runs a loop or runs the command 5 times. Shows 5 different passwords.

**Talking point:**
> "Each run produces a different password. The cryptographic randomness is working. And I didn't write a single line of Python."

---

### Closing Talking Point for Demo 1.1

> "What just happened: I opened a terminal. I described what I wanted. Claude created a file, I reviewed it, Claude ran it. No copy-paste. No editor switch. No separate terminal tab to run the script. The entire development loop happened in one conversation. This is what 'full terminal integration' means."

---

## Demo 1.2: Context & Memory Live

**Teaching point this demo supports:** Module 1.2 — CLAUDE.md as persistent context, memory across sessions.

**Duration:** ~10 minutes

**What participants see:** CLAUDE.md being created, Claude exiting and restarting, and Claude remembering the project conventions from CLAUDE.md without being told again. Then a memory item being created.

---

### Step 1: Set Up the Demo Project

In terminal (outside Claude Code, or use Claude Code's bash):
```
mkdir -p ~/cc-workshop/demos/demo-1.2 && cd ~/cc-workshop/demos/demo-1.2 && git init
```

Then start Claude Code in that directory:
```
claude
```

**Talking point:**
> "Fresh project. No CLAUDE.md. No memory. Claude knows nothing about this project yet except what I tell it right now."

---

### Step 2: Create CLAUDE.md via Claude Code

Type in Claude Code:
```
Create a CLAUDE.md file for this project. It's a Python CLI tool for access control management.
Include these conventions:
- Python 3.11+
- pytest for all tests (pytest-cov for coverage)
- black for formatting (line length 88)
- Type hints required on all function signatures
- Explicit error handling — never use bare except clauses
- No global state — all configuration passed as parameters
- Log using the standard logging module, not print statements
- The legacy module legacy_panel_parser.py must never be modified
```

**Expected behavior:** Claude creates `./CLAUDE.md` with these conventions written in clean Markdown.

**Talking point:**
> "This is our access policy. Every rule Claude will follow, every session, without being reminded. Think of it as the site security policy document handed to every contractor before they start work."

**Show the file briefly.** You can ask Claude: "Show me the CLAUDE.md you just created."

---

### Step 3: Exit and Restart

Type in Claude Code:
```
exit
```

Then restart:
```
claude
```

**Talking point while restarting:**
> "New session. Clean slate. Claude has no memory of our conversation. Except..."

---

### Step 4: Test That CLAUDE.md Was Loaded

Type in Claude Code:
```
What are the coding conventions for this project?
```

**Expected behavior:** Claude lists all the conventions from CLAUDE.md — pytest, black, type hints, no global state, no bare except, etc. It read CLAUDE.md on startup.

**Talking point:**
> "I told Claude the rules exactly once. I exited, started a new session, and it still knows them. CLAUDE.md is loaded automatically every session. This is how you write the rules once and have Claude follow them indefinitely."

**Follow-up question to reinforce:**
```
If I ask you to modify legacy_panel_parser.py, what would you do?
```

**Expected behavior:** Claude should say it would refuse or flag this, because CLAUDE.md says that file must never be modified.

**Talking point:**
> "That constraint lives in the file, not in my head. I don't have to remember to tell Claude. The policy enforces itself."

---

### Step 5: Create a Memory Item

Type in Claude Code:
```
Remember that I prefer German for communication but all code and file names must be in English.
```

**Expected behavior:** Claude confirms it has stored this as a memory. In future sessions, Claude will communicate in German if you are this user.

**Talking point:**
> "This is different from CLAUDE.md. CLAUDE.md is project-level — it's in the project directory, everyone who uses this project gets these rules. Memory is user-level — it's stored in my home directory and applies to all my sessions across all projects. Use CLAUDE.md for project conventions. Use memory for personal preferences."

**Talking point to close:**
> "CLAUDE.md is your access policy. It lives with the project. Write the rules once. Claude follows every session."

### Recovery Notes

- **If Auto-Memory shows no entries after restart:** Try `cat ~/.claude/projects/<project-hash>/memory/MEMORY.md` manually. Auto-Memory needs ~1 turn before writing.
- **If `claude` restart doesn't reload CLAUDE.md:** Verify the file is in the working directory or `~/.claude/CLAUDE.md`. Use `claude --verbose` to see what was loaded.
- **If memory item drift visible:** Acknowledge as teaching moment — "this is exactly why we need to inspect Auto-Memory periodically (see Module 3.7)."
- **If Claude doesn't remember the conventions in Step 4:** Confirm `CLAUDE.md` exists in cwd with `ls -la CLAUDE.md`, then restart Claude Code and try again — the file may have been written to a different directory.

---

## Demo 1.3: Good vs Bad Prompting

**Teaching point this demo supports:** Module 1.3 — Effective prompting, specificity, scope control.

**Duration:** ~10 minutes

**What participants see:** Two prompts for the same task producing dramatically different results.

---

### Step 1: The Bad Prompt

**Setup talking point:**
> "Same tool. Same capabilities. Let's see what happens with a vague request."

Type in Claude Code:
```
Fix the code
```

**Expected behavior:** Claude will ask for clarification — "Which code? What's the issue?" — or will say it needs more context.

**Talking point:**
> "Claude is doing the right thing. It doesn't guess. But this is a useless prompt. In a real session, if I had just shared some code earlier, Claude might attempt a fix — but with no context, any fix would be a shot in the dark. Let's try the same task properly."

---

### Step 2: The Good Prompt

Type in Claude Code:
```
Write a Python function called validate_ipv4(address: str) -> bool in a new file
called validators.py.

Requirements:
- Returns True for valid IPv4 addresses, False for anything else
- Valid format: four octets separated by dots, e.g. "192.168.1.1"
- Each octet must be an integer 0-255
- No leading zeros allowed (e.g., "192.168.01.1" is invalid)
- Must handle edge cases: empty string, None input, extra whitespace, IPv6 addresses
- Do not use regex — use explicit parsing for clarity

After creating the function, write pytest tests in tests/test_validators.py covering:
- 5 valid addresses
- Leading zeros (invalid)
- Out-of-range octet (256, -1)
- Too few octets
- Too many octets
- Non-numeric characters
- Empty string
- None input
- IPv6 address (should return False)
```

**Expected behavior:** Claude creates `validators.py` with a clean, explicit parsing approach and `tests/test_validators.py` with all the specified cases.

**Talking point while Claude works:**
> "Notice what the prompt does: it specifies the function signature, the file name, the validation rules, the edge cases, the implementation constraint (no regex), and the test requirements. This is a work order, not a wish."

**After Claude finishes, ask:**
```
Run the tests
```

**Expected behavior:** Claude runs `pytest tests/test_validators.py -v` and shows all tests passing.

**Talking point:**
> "First attempt. All tests pass. Because the specification was complete. The tool didn't get smarter between the two prompts. The prompts got smarter. That's the skill."

---

### Comparison Summary for Participants

Write or display this:

| | Bad Prompt | Good Prompt |
|---|---|---|
| **Input** | "Fix the code" | Specific function, file, requirements, edge cases, tests |
| **Claude's response** | Asks for clarification or guesses | Implements exactly what was specified |
| **Result quality** | Unknown | Deterministic, testable |
| **Iterations needed** | Many | One (usually) |

**Closing talking point:**
> "This is the highest-leverage skill in this workshop. Not the git integration, not the memory system — just this. Write prompts like work orders. Specific. Scoped. With success criteria. The tool rewards precision."

### Recovery Notes

- **If Claude asks clarifying questions instead of guessing on the bad prompt:** Acknowledge as positive behavior, redirect: "this is good behavior — Claude refused to guess. But in production it might have just picked an interpretation."
- **If Claude reads files unexpectedly:** Normal for newer versions. Continue and discuss in retro why context-grabbing happens.
- **If the IPv4 validator doesn't pass tests:** Show the failing output as a teaching moment — "see, even with a good prompt, you need to verify."
- **If Claude refuses to run the bad prompt at all:** Skip the bad-prompt step, narrate what *would* have happened, and pivot directly to the good prompt — the contrast still lands.

---

## Demo 1.4: Git Workflow

**Teaching point this demo supports:** Module 1.4 — Git integration and worktrees.

**Duration:** ~10 minutes

**What participants see:** A complete branch → implement → commit → log flow, then worktree creation.

---

### Pre-requisites

This demo builds on the `~/cc-workshop/demos/demo-1.2` directory created in Demo 1.2. Make sure it has the `validators.py` and tests from Demo 1.3, or create them fresh.

---

### Step 1: Create a Feature Branch

Type in Claude Code:
```
What's the current git status?
```

**Expected behavior:** Claude runs `git status` and shows current state.

**Talking point:**
> "Before touching anything, we check what state we're in. Good habit whether you're in Claude Code or not."

Type in Claude Code:
```
Create a new branch called feature/ipv4-validation
```

**Expected behavior:** Claude runs `git checkout -b feature/ipv4-validation` and confirms.

---

### Step 2: Implement a Feature

Type in Claude Code:
```
Add a function validate_ip_range(start: str, end: str) -> bool to validators.py.
It should verify that both addresses are valid IPv4 and that start comes before end
numerically. Use the existing validate_ipv4 function for the per-address check.
Add tests for it in the existing test file.
```

**Expected behavior:** Claude reads the existing file, adds the new function in a compatible style, adds tests.

**Talking point while Claude works:**
> "Notice Claude read the existing file first. It knows the existing function is there. It will use it rather than reimplementing. This is the advantage of giving Claude context — it builds on what exists."

---

### Step 3: Review the Diff

Type in Claude Code:
```
Show me the full diff before we commit. I want to review the changes.
```

**Expected behavior:** Claude runs `git diff` and displays the changes.

**Talking point:**
> "Always review before committing. This is true whether you wrote the code or Claude did. Especially when Claude did."

---

### Step 4: Run Tests and Commit

Type in Claude Code:
```
Run the tests. If they pass, stage everything and commit with message:
"Add IP range validation with tests

Adds validate_ip_range() to validators.py, using existing validate_ipv4()
for per-address validation. Tests cover valid ranges, inverted ranges,
and invalid address inputs."
```

**Expected behavior:** Claude runs tests, shows output, then stages and commits with the provided message.

**Talking point:**
> "That commit message is ready for a PR. Descriptive title, short body explaining the why. I specified it in the prompt so I control the format. You can also ask Claude to generate the message — it's usually quite good at conventional commit style."

---

### Step 5: Show Git Log

Type in Claude Code:
```
Show me git log --oneline -5
```

**Expected behavior:** Shows the recent commits including the one just made.

**Talking point:**
> "Branch → code → test → commit. Entire flow in one conversation. No switching to a git GUI. No separate terminal."

---

### Step 6: Create a Worktree (Bonus — if time allows)

**Setup talking point:**
> "Now let's say I want to experiment with a completely different approach — maybe rewriting this with regex after all, to see if it's actually cleaner. I don't want to mess up my current branch. Worktree."

Type in Claude Code:
```
Create a git worktree at ../validators-experiment on a new branch
called experiment/regex-validators
```

**Expected behavior:** Claude runs `git worktree add ../validators-experiment -b experiment/regex-validators` and confirms.

Type in Claude Code:
```
What worktrees do we have now?
```

**Expected behavior:** Claude runs `git worktree list` and shows both the main working directory and the new experiment worktree.

**Talking point:**
> "Two branches. Two directories. Both pointing to the same repository. I can have Claude work in the experiment directory — try the regex approach — while my main branch is completely untouched. If the experiment works, I merge. If it doesn't, I delete the worktree and walk away. No stashing, no cleanup, no accidental changes to main."

**Security analogy payoff:**
> "Remember the test bench analogy: separate room, same equipment, completely isolated. That's this. Your live system — main branch — is not affected by anything happening in the test lab."

---

### Closing Talking Point for Demo 1.4

> "Branch, implement, test, commit, log. All in conversation. Git becomes something you think about, not something you manage manually. And worktrees give you the test-lab model you already know from physical security: isolated environment, real equipment, no risk to production."

### Recovery Notes

- **If `git worktree add` fails with existing branch:** Remove with `git worktree remove ../<dir>` and retry. If the branch already exists, drop the `-b` flag and let git reuse it.
- **If `gh pr create` fails (auth):** Skip the PR step, demonstrate via `git push` only. Mention "gh auth needed for PR-creation — `gh auth login` before the workshop."
- **If `pytest` not available:** Mention as setup-issue, continue without test-step. Or run via `python -m pytest` as fallback.
- **If `git status` shows unexpected files:** Stage only the validators-related paths explicitly (`git add validators.py tests/`) — don't `git add -A`.

---

## Demo 1.5: Cost-Aware — Same Task, Three Models

**Teaching point this demo supports:** Module 1.5 — model choice and effort levels are cost levers, not just quality levers.

**Duration:** ~6 minutes

**What participants see:** The same realistic coding task run three times with different model + effort combinations, with `/cost` after each one, so they can compare the dollar amounts side by side.

**Setup:**
- Terminal open in a scratch directory (`~/cost-demo/`)
- Claude Code authenticated
- `/cost` is available in this build (confirm before the workshop)

---

### Step 1: Baseline with Opus 4.8 + xhigh

In Claude Code:
```
/model opus
/effort xhigh
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

**Expected behavior:** Claude produces a thorough implementation with several edge cases (leading zeros, out-of-range octets, empty strings, embedded whitespace) and a small test block.

After it finishes, type:
```
/cost
```

**Expected output:** A session cost in the ballpark of ~$0.10–$0.20 for this single turn (numbers vary; the point is the *order of magnitude*).

**Talking point:**
> "That's the most expensive combination Claude Code offers — Opus at the deepest effort level. Look at the cost. Now let's see what we get for less."

---

### Step 2: Same Task with Sonnet 4.6 + medium

Reset the session or just continue:
```
/model sonnet
/effort medium
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

After completion:
```
/cost
```

**Expected output:** Significantly lower — typically around 1/3 to 1/5 of the Opus + xhigh cost.

**Talking point:**
> "Sonnet at default effort. Same code task. Probably similar code quality. Notice how much that costs versus the first one."

---

### Step 3: Same Task with Haiku 4.5 + low

```
/model haiku
/effort low
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

```
/cost
```

**Expected output:** Roughly one order of magnitude cheaper than the Opus baseline.

**Talking point:**
> "Haiku at low effort. The output will be a bit terser, maybe one or two fewer edge cases enumerated. But for validating an IPv4 address — a task with a well-known correct answer — Haiku is plenty."

---

### Step 4: Side-by-Side Comparison

Open all three generated files in your editor or paste them side by side in the terminal. Ask the room:

- Are all three outputs functionally correct? (Usually: yes.)
- Where is the quality difference? (Opus tends to enumerate more edge cases; Haiku is more terse with explanation.)
- The cost spread between cheapest and most expensive is often 10–20x.
- For this specific task — IPv4 validation, well-defined problem, no architectural decisions — is Opus worth 15x the price? Almost never.

**Talking point:**
> "The real question to ask *before* the session is: how important is the quality here? If it's a one-shot utility, Haiku does the job. If you're designing a protocol parser that will live in firmware for ten years, pay for Opus + xhigh. The cost dial and the effort dial are part of your job."

---

### Closing Talking Point for Demo 1.5

> "Cost isn't a sticker you get at the end of the month. It's a knob you turn every session. `/cost` shows you where you are, `/usage` shows you where you've been, `/insights` shows you what to fix. Get into the habit of checking before you scale a workflow up."

**Recovery notes:**
- If `/cost` isn't available in the participant's build (older versions): pivot to the web console at `console.anthropic.com → Usage`, which shows the aggregate. Still gets the point across.
- If two runs return suspiciously identical cost numbers, you've probably hit cache — clear with `/clear` between runs or change the prompt slightly.
- If a participant questions whether Haiku really produces correct code: run their counter-example live. The demo's point survives — and you've just shown adversarial debugging in passing.

---

## Moderator Notes: Handling Common Issues

**Claude gives wrong output:**
Don't hide it. Use it as a teaching moment: "And this is why we review before accepting. Let me show you how to correct course."

Recovery prompt pattern:
```
That's not quite right. The issue is [specific problem]. Fix only that — don't change anything else.
```

**Demo runs slow:**
Keep talking through the concepts while waiting. "While Claude is thinking, let me explain what's happening under the hood..."

**Participant asks about a feature not in the demo:**
"Good question. Let's park that for the exercise section where you'll have time to experiment. If we don't get to it, find me in the break."

**Terminal output is hard to read on screen:**
Before demoing:
```bash
export TERM=xterm-256color          # macOS / Linux / Git Bash
```
```powershell
$env:TERM = "xterm-256color"        # Windows PowerShell
```
And bump font size. If still hard: narrate what's happening and move on.

---

*End of Block 1 Demo Scripts*
