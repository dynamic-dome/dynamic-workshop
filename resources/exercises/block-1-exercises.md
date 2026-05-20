# Block 1: Exercises

**Audience:** Experienced programmers. Security analogies used throughout.
**Time budget:** ~85-90 minutes total for all Block 1 exercises (1.5 optional; without it ~60-65 min)
**Format:** Work individually or in pairs. Facilitator available for questions.

---

## How These Exercises Work

Each exercise has:
- **Goal** — what you are practicing
- **Steps** — numbered, do them in order
- **Success check** — how you know you are done
- **Hints** — if you get stuck

The exercises are designed to be short and hands-on. You are not building a production system. You are building muscle memory.

---

## Exercise 1.1: Your First Claude Code Project

**Goal:** Get comfortable with the core Claude Code loop — describe, implement, run, extend, explain. Build a small tool from scratch without writing any code yourself.

**Time:** ~12-15 minutes

---

### Steps

**1. Open Claude Code in a clean directory**

In your terminal:
```
mkdir -p ~/cc-workshop/exercises/exercise-1.1 && cd ~/cc-workshop/exercises/exercise-1.1
claude
```

**2. Ask Claude to create a small tool**

Give Claude this prompt — do not copy it exactly, adapt it slightly to something that feels relevant to your domain:
```
Create a Python script called event_log_parser.py.
It should read a text file where each line has this format:
  TIMESTAMP DOOR_ID EVENT_TYPE CARD_ID
Example line:
  2024-03-15T09:42:11 DOOR-03 ACCESS_GRANTED CARD-1047

The script should:
- Accept a filename as a command-line argument
- Parse each line
- Count how many ACCESS_GRANTED and ACCESS_DENIED events occurred per door
- Print a summary table to stdout

Create a sample input file called sample_events.txt with 10 test lines covering
at least 3 different doors and both event types.
```

**3. Watch what Claude does**

Observe: Does it read back the requirements? Does it create both files? Does the code look reasonable to you?

**4. Run the tool**

Ask Claude:
```
Run event_log_parser.py on sample_events.txt and show me the output
```

**5. Ask Claude to add a feature**

Once it runs, add a feature:
```
Add a --door flag that filters the output to show only events for a specific door.
Example: python event_log_parser.py sample_events.txt --door DOOR-03
```

**6. Ask Claude to explain what it did**

```
Explain in plain language what changes you made to support the --door flag.
Then show me the diff.
```

---

### Success Check

- [ ] `event_log_parser.py` exists in the directory
- [ ] `sample_events.txt` exists with at least 10 lines
- [ ] Running the script produces a summary table (no crash)
- [ ] The `--door` flag works and filters correctly
- [ ] You understand what Claude changed (from the explanation)

---

### Hints

- If Claude creates a file but you don't see it, ask: "What files did you create? List them."
- If the script crashes with a parsing error on the sample file, say: "The script crashes on line X with this error: [paste error]. Fix it without changing the sample file format."
- If you want to try your own domain-specific tool instead of the log parser, go for it. The goal is the loop, not the specific tool.

---

## Exercise 1.2: Setting Up Your Context

**Goal:** Create a CLAUDE.md for your actual work domain. Test that it persists across a session restart. Create a personal memory item.

**Time:** ~15 minutes

---

### Steps

**1. Create a project directory**

Pick a directory that represents a real (or realistic) project from your work. It can be empty — we just need a home for CLAUDE.md.

```
mkdir -p ~/cc-workshop/exercises/exercise-1.2 && cd ~/cc-workshop/exercises/exercise-1.2
git init
claude
```

**2. Tell Claude about your project and have it write CLAUDE.md**

Think about what you actually work on. Then give Claude a prompt like:

```
Create a CLAUDE.md for this project. It is a [describe your project — e.g.,
Python-based alarm management system for commercial buildings].

Include these conventions:
- [Your language/framework, e.g., Python 3.11, asyncio]
- [Your test framework, e.g., pytest with pytest-asyncio]
- [Any formatting tools you use]
- [A rule about something that must never be changed — e.g., the legacy panel interface]
- [A domain-specific convention — e.g., all alarm codes must be in SCREAMING_SNAKE_CASE]
- [Anything else that's specific to your domain or team]
```

**3. Review and refine the CLAUDE.md**

Read what Claude created. If anything is wrong or missing, say:
```
Add: [missing rule]
Change the section on [X] to say: [correction]
```

**4. Exit and restart**

```
exit
```

Then:
```
claude
```

**5. Test persistence**

Ask Claude:
```
What are the coding conventions for this project?
```

Does it know? Does it mention the specific rules you put in CLAUDE.md?

**6. Test the "never change" boundary**

Ask Claude:
```
Modify the legacy panel interface module
```

Does Claude push back? It should flag that the CLAUDE.md says not to touch it.

**7. Create a personal memory item**

```
Remember that my primary working language for communication is [your preference].
Also remember that in my projects, door IDs always follow the format SITE-FLOOR-DOOR
(e.g., MAIN-02-EAST).
```

Exit and restart again. Ask Claude: "What door ID format should I use in this project?" — it should know.

---

### Success Check

- [ ] CLAUDE.md exists in the project directory with your real conventions
- [ ] After restart, Claude can recite the conventions without being told
- [ ] Claude pushes back on modifying the protected module
- [ ] Memory item was created and is retrieved after restart

---

### Hints

- If Claude doesn't push back on the protected module, check your CLAUDE.md — the rule needs to be specific: "Never modify [exact filename]" not just "be careful with the legacy module."
- You can ask Claude to show you the current CLAUDE.md at any time: "Show me the contents of CLAUDE.md."
- If you want to add a rule after the fact: "Add this rule to CLAUDE.md: [rule]"
- Memory vs CLAUDE.md: If you want the preference to apply across all your projects, not just this one, use memory ("Remember that..."). If it's project-specific, put it in CLAUDE.md.

---

## Exercise 1.3: The Prompting Challenge

**Goal:** Experience firsthand the difference between vague and specific prompts. Same task, two rounds, compare quality. There is no cheating — the point is to feel the contrast.

**Time:** ~15 minutes

**Note:** Do Round 1 and Round 2 in the same session.

---

### The Task

You are going to ask Claude to write an IPv4 address validator in Python — twice.

---

### Round 1: The Vague Prompt

Type this, exactly as written:
```
Write an IPv4 validator
```

Let Claude respond. Do not add any follow-up prompts. Just observe.

**Write down:**
- Does it ask for clarification, or does it just generate something?
- What language did it use?
- Did it include tests?
- Did it handle edge cases (what edge cases)?
- What did the function signature look like?
- How confident are you this is what you needed?

---

### Round 2: The Specific Prompt

Now give Claude this prompt (or adapt it slightly — the point is specificity):

```
Write a Python function called validate_ipv4(address: str) -> bool
in a new file called validators.py in the current directory.

Requirements:
- Returns True only for valid IPv4 addresses in dotted-decimal notation
- Valid: four octets 0-255 separated by single dots, no leading zeros
- Invalid: leading zeros (e.g., 192.168.01.1)
- Invalid: out-of-range octets (256, -1, or any non-integer)
- Invalid: wrong number of octets (3 or 5)
- Invalid: extra whitespace anywhere
- Invalid: IPv6 addresses
- Invalid: empty string or None
- Do not use regex — parse explicitly for code clarity
- Add a docstring with one valid and one invalid example

Then write pytest tests in tests/test_validators.py covering:
1. Five valid addresses (including 0.0.0.0 and 255.255.255.255)
2. Leading zeros in one octet
3. Octet value 256
4. Octet value -1
5. Only 3 octets
6. 5 octets
7. Non-numeric characters
8. Empty string
9. None input
10. IPv6 address (e.g., "2001:db8::1")
```

Let Claude respond.

**Write down:**
- How does the result compare to Round 1?
- Are all 10 test cases present?
- Does the function handle all the edge cases listed?
- How much rework would Round 1 require to match Round 2?

---

### Round 2b: Run the Tests

```
Run the tests and show me the results
```

How many pass?

---

### Reflection Questions

Think about or discuss with your neighbor:

1. How much time would you spend clarifying and iterating after the Round 1 prompt to reach Round 2 quality?
2. In your actual work, what recurring tasks could you write detailed "work order" prompts for once and reuse?
3. What information do you naturally hold in your head that you would need to make explicit when prompting Claude?

---

### Success Check

- [ ] Round 1 completed (observed the output without follow-up)
- [ ] Round 2 completed with the specific prompt
- [ ] Tests run and pass (or you understand why any fail)
- [ ] You can articulate at least 3 specific differences between the two outputs

---

### Hints

- If Round 2 tests fail, do not manually edit the code. Say: "Test [test name] fails with [error]. Fix the implementation to handle this case." Let Claude fix it.
- If Claude asks clarifying questions in Round 1 — that is good Claude behavior. It means Claude is not guessing. The output it generates after clarification is a data point too.
- The "no regex" constraint is intentional. It shows that you can impose implementation choices, not just functional requirements.

---

## Exercise 1.4: Git Flow with Claude Code

**Goal:** Complete a branch → implement → commit → log cycle using only Claude Code conversation. No manual git commands. Bonus: create a worktree.

**Time:** ~18-20 minutes

---

### Setup

Use the project from Exercise 1.2, or create a new one:
```
mkdir -p ~/cc-workshop/exercises/exercise-1.4-git && cd ~/cc-workshop/exercises/exercise-1.4-git
git init
echo "# Access Control Utilities" > README.md
git add README.md
git commit -m "Initial commit"
claude
```

---

### Steps

**1. Check starting state**

Ask Claude:
```
What is the current git status and which branch are we on?
```

Note the answer.

**2. Create a feature branch**

Ask Claude:
```
Create a new branch called feature/access-log-formatter
```

Confirm it was created: "Which branch are we on now?"

**3. Implement a small feature**

Ask Claude:
```
Create a file called log_formatter.py with a function format_access_event
that takes a dictionary with keys: timestamp, door_id, event_type, card_id
and returns a formatted string like:
  [2024-03-15 09:42:11] DOOR-03 ACCESS_GRANTED (Card: CARD-1047)

Add a small test in tests/test_log_formatter.py that tests:
- Normal case with all fields present
- Event type ACCESS_DENIED
- Missing card_id (should show "Card: UNKNOWN")
```

**4. Review before committing**

Ask Claude:
```
Show me the git diff — what has changed since the last commit?
```

Read through the diff. Do the changes match what you asked for?

**5. Run tests**

Ask Claude:
```
Run the tests. Show me the full output.
```

**6. Stage and commit**

Ask Claude:
```
Stage all new and changed files. Then commit with this message:
"Add access event log formatter

Formats access control events into human-readable log lines.
Handles missing card_id gracefully. Tests cover normal case,
ACCESS_DENIED events, and missing card scenarios."
```

**7. Confirm the commit**

Ask Claude:
```
Show me git log --oneline -5
```

Is your commit there?

---

### Bonus: Create a Worktree

**8. Set up an experiment worktree**

Ask Claude:
```
Create a git worktree at ../log-formatter-experiment on a new branch
called experiment/json-log-format
```

**9. Verify it exists**

Ask Claude:
```
List all git worktrees
```

You should see two: the main directory and the experiment.

**10. Think through the workflow**

Imagine you now want to try a completely different implementation — JSON-formatted logs instead of the human-readable string. How does having a separate worktree help you?

In the experiment worktree, you would:
- Modify `log_formatter.py` to output JSON
- Run tests to see if the approach is viable
- Compare the two approaches side by side
- Decide which to merge and which to discard

You do not have to implement it now. Understanding the model is the goal.

---

### Success Check

- [ ] Feature branch `feature/access-log-formatter` was created via Claude Code
- [ ] `log_formatter.py` and tests exist
- [ ] Tests pass
- [ ] Commit was created with the provided message
- [ ] `git log` shows the commit on the correct branch
- [ ] (Bonus) Worktree was created and appears in `git worktree list`

---

### Hints

- If tests fail: "Test [name] fails with [error message]. Fix the implementation." Do not edit the file manually — let Claude fix it and run again.
- If the commit message is not exactly what you specified, ask: "The commit message is wrong. Amend the last commit with this message: [correct message]"
- If git worktree fails with an error about an existing branch, ask Claude to use `--orphan` or create the worktree on a new branch with a slightly different name.
- If you want to see what's in the worktree directory: ask Claude to "List the files in ../log-formatter-experiment"

---

## Exercise 1.5: Get Your Daily Workflow Under $5 (Should-Do, ~25 Min)

**Priority:** Should-do — valuable, but optional if time is short.

**Goal:** Define a cost-optimal Claude Code configuration for three workflows you actually run. Stop treating model and effort as defaults — pick them deliberately.

**Time:** ~25 minutes

---

### Steps

**1. Identify three workflows from your daily work**

Pick three things you do (or expect to do) with Claude Code regularly. Examples — adapt to your domain:

- Code-reviewing a ~100-line pull request
- Bug-fixing in an unfamiliar codebase
- Writing docstrings or short documentation for a function
- Generating a parser for a new event-log format
- Drafting a commit message after a chunky local change

**2. Per workflow, decide model + effort + flags**

Fill in your own table. The columns matter more than the exact values:

| Workflow | Model | Effort | Extra flags | Estimated cost / run |
|---|---|---|---|---:|
| Code-review (~100 lines) | ? | ? | ? | ? |
| Bug-fix in unknown code | ? | ? | ? | ? |
| Doc/comment writing | ? | ? | ? | ? |

**3. Justify each choice**

For each row, ask yourself:
- Why this model? (Depth vs speed vs cost.)
- Why this effort? (Cognitive load of the task.)
- Which flags help? (Especially `--max-budget-usd` as a safety net for unattended runs.)

**4. Verify with one real run**

Pick one workflow from your table. Run it once with your chosen config. Open `/cost`. Does the number match what you estimated? If not — adjust.

**5. Persist your config**

Lock the decision in so you don't re-think it next week. Two reasonable options:

Either a shell alias:
```bash
# ~/.bashrc or ~/.zshrc
alias claude-review='claude --model sonnet --effort medium --max-budget-usd 0.30'
alias claude-deep='claude --model opus --effort xhigh --max-budget-usd 2.00'
alias claude-quick='claude --model haiku --effort low'
```

Or a small user-skill that wraps the right invocation. (Skills are covered in Block 2 — for now an alias is fine.)

---

### Success Check

- [ ] You have a filled-in table with three workflows, each with a model + effort + cost estimate
- [ ] You have a justification one-liner for each row (not just "felt right")
- [ ] At least one workflow has been run live and verified with `/cost`
- [ ] You have either an alias or a note that captures your chosen config for future runs

---

### Reflection

- Which configuration was the cheapest per run? Was the quality acceptable?
- Where was the biggest cost lever — model choice, effort level, or CLAUDE.md length?
- Would you configure differently if the budget came from your employer vs. your own pocket? Why?
- Are any of your workflows candidates for `--max-budget-usd` as a hard safety net? (Hint: anything you run unattended, in CI, or in a loop.)

---

### Hints

- If you're new to the models: start the bug-fix row with Sonnet + medium, the code-review row with Sonnet + low, the doc-writing row with Haiku + low. Then experiment from there.
- `--max-budget-usd` is cheap insurance — even setting it to $1.00 on a routine task catches runaway loops without affecting normal work.
- Don't optimize prematurely. The point isn't to squeeze pennies — it's to make the choice consciously instead of accidentally always paying for Opus + xhigh.

---

## Exercise Debrief Questions

Use these for group discussion or personal reflection after completing the exercises:

**On Claude Code as a tool:**
1. What was surprising about how Claude Code works compared to your expectation?
2. Where did you feel most in control? Where did you feel least in control?
3. What would you need to change about how you currently work to integrate Claude Code effectively?

**On prompting:**
1. What information do you routinely have in your head that you would need to make explicit in prompts?
2. What types of tasks in your domain would benefit most from the "work order" prompting style?
3. When is it appropriate to be less specific and let Claude decide?

**On context and memory:**
1. What conventions or constraints in your current project would you put in CLAUDE.md today?
2. What personal preferences would you store as memories?
3. How would you handle a project where multiple team members use Claude Code — how do you coordinate CLAUDE.md conventions?

**On git integration:**
1. Which part of the git workflow do you find most valuable to do through Claude Code?
2. When would you still prefer to run git commands manually?
3. How does the worktree model change how you think about parallel development work?

---

*End of Block 1 Exercises*
