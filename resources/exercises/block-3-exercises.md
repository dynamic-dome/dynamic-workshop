# Block 3: Exercises

> These exercises move from guided exploration to open architecture design.
> The final exercise — Architecture Discussion — is the goal of the entire workshop.
> Leave enough time for it.

### Exercise Priority Guide

| Priority | Exercise | Realistic Time |
|----------|----------|---------------|
| **Must-do** | 3.1 Multi-Agent Task | ~15 min |
| **Must-do** | 3.5 Architecture Discussion | ~45 min |
| **Should-do** | 3.3 Security Audit **OR** 3.4 Automation | ~25-30 min / ~20 min |
| **Should-do** | 3.6 Pre-Commit Hook with Claude | ~25 min |
| **Should-do** | 3.7 Debug a Broken Hook | ~20 min |
| **Nice-to-have** | 3.2 Codex Swarm (demo-only) | ~15 min |
| **Nice-to-have** | Bonus 3.8 HIPAA Hook | ~20 min |

> **Realistic total: 110–145 minutes.** Prioritize Must-do exercises first.

---

## Exercise 3.1: Your First Multi-Agent Task

**Type:** Individual, ~15 minutes
**Goal:** Experience the difference between single-instance and multi-agent Claude.

### Task

Think of a task in your current work that has 2-3 clearly independent parts.

Examples:
- "Analyze this config file for security issues AND document what each setting does"
- "Find all hardcoded values in this file AND write unit tests for the main functions"
- "Map the directory structure of this project AND list all external dependencies"

Ask Claude to use **separate agents running in parallel** for each part.
Be explicit:

> "Use separate agents running in parallel for each part.
> Part 1: [describe Part 1]
> Part 2: [describe Part 2]
> Report the results together."

### What to Watch

- The two agent threads appearing in the output
- Each agent having its own context — it does not know what the other is doing
- The orchestrator combining the results
- Total time vs. what it would have been sequentially

### Reflection Questions

1. Were the tasks actually independent?  Did the agents need to coordinate?
2. Did running in parallel introduce any issues?
3. Where in your actual work could you use this pattern?

### Hints

- Tasks must be genuinely independent.  If Agent 2 needs Agent 1's output, it is a pipeline, not fan-out.
- Keep each agent's task focused.  Vague tasks produce vague results.
- Start small.  Two agents is enough to see the pattern.

---

## Exercise 3.2: Watch a Codex Swarm (Group Exercise)

**Type:** Group observation and discussion, ~15 minutes
**Goal:** Understand the multi-model pipeline and when to use it.

### Format

The moderator runs the demo from Demo 3.2.
Everyone watches.

### Discussion Questions (after the demo)

Work in groups of 2-3.  Discuss:

1. **Decomposition quality:** How well did Claude break the task into independent subtasks?
   Were the boundaries clean?  Would you have decomposed differently?

2. **Codex vs. Claude comparison:** Looking at what Codex generated — does it match what Claude would have written?
   Where are the differences?  Does Codex code feel different?

3. **Review effectiveness:** What did the Claude review step catch?
   Were there issues in the generated code that you can see?

4. **Your use case:** Where in your current work would you use a Codex Swarm?
   What task would benefit from the architect-contractor-inspector model?

5. **The cost/speed tradeoff:** This pipeline uses Opus for planning and review, Codex for generation.
   When does the cost make sense?  When would you just use Claude directly?

### Report Back

Each group shares their most interesting answer.  5 minutes total.

---

## Exercise 3.3: Security Audit Your Project

**Type:** Individual or pair, ~25-30 minutes
**Goal:** Run adversarial security testing on real code and see what it finds.

### Setup

Use `workshop-playground/access_control.py`. It already contains three deliberately planted vulnerabilities:
1. Command Injection in `backup_database()`
2. Hardcoded credential `ADMIN_PASSWORD = "admin123"`
3. Path Traversal in `read_log()`

There is also a strong chance the swarm surfaces a fourth, *unplanned* issue (Log-Injection in `log_event()`). Treat that as a bonus.

**No vulnerability planting required** — we use the existing ones.

**Step 1: Open the playground**

```bash
cd workshop-playground/
ls access_control.py     # confirm you have the file
```

**Step 2: Run the swarm against `access_control.py`**

```
/devil-advocate-swarms:swarm scan workshop-playground/access_control.py
```

**Step 3: Wait and watch**

Do not skip ahead.  Watch each stage:
- Scanners: what did each one identify? Did they catch all three planted issues? Anything beyond?
- Debate: which findings are being argued?  Who is winning?
- Consensus: how many CONFIRMED vs FALSE POSITIVE?
- Fixers: what does the fix for each confirmed finding look like?

The swarm should confirm the **three planted issues** (Command Injection, Hardcoded Credential, Path Traversal) — plus potentially find the **Log-Injection bonus** in `log_event()`.

**Step 4: Pick one finding and apply its fix**

Choose **one** of the three confirmed findings and let Claude implement the fix in `access_control.py`. After the fix:

```bash
pytest -v
```

The existing test suite must still pass. The fix is only acceptable if the baseline tests stay green.

### What to Report

1. How many of the three planted vulnerabilities did the swarm confirm? At which stage?
2. Did it find the bonus Log-Injection in `log_event()` — or anything else you had not expected?
3. Were there false positives?  What did the Defender argue for each one?
4. Which finding did you fix, and does the fix break any of the existing tests?

### Hints

- The debate phase is the most interesting part.  Read the Prosecutor and Defender arguments.
- Some findings may end up as false positives — the Defender should win those.
- If the swarm misses one of the three planted issues, that is also interesting — why?
- Pay attention to the regression test the Fixer writes.  Is it testing the right thing?
- After the fix, run `pytest -v` from the playground root to confirm the baseline still passes.

### For the CySec Engineer

Your professional instincts will tell you whether the Prosecutor's arguments are realistic.
Are the attack scenarios in the debate plausible?  Would you write a CVE this way?
Where does the automated analysis fall short of human expert judgment?
Where does it match or exceed it?

---

## Exercise 3.4: Set Up Automation

**Type:** Individual, ~20 minutes
**Goal:** Configure a real automated task that will run without your involvement.

### Task

Choose something you actually want to automate.  Options:

**Option A: Quality Gate on a Schedule**
```
/schedule
```
Task: run the quality gate every day at a time of your choice.
Configure it for your current project.

**Option B: Security Scan on a Schedule**
```
/schedule
```
Task: run a security audit every week on Monday.
Configure it for a project with external input handling.

**Option C: Monitoring Loop**
```
/loop 1m
```
Task: check if a specific file has been modified in the last 60 seconds and report.
(Useful during active development to catch accidental changes.)

**Option D: Your Own Idea**
What would you actually automate at work?
Design it, set it up, verify it triggers at least once.

### Verification

After setting up your automation, verify it runs:
- For `/schedule`: check the schedule list with `/schedule` and confirm your task appears
- For `/loop`: watch it trigger at least twice in your terminal

### Discussion (with the person next to you)

- What did you choose to automate?  Why that task?
- What would break if the automation ran on bad code?  What is your safety net?
- What would you actually automate in your work environment, given 30 minutes to set it up?

---

## Exercise 3.5: Architecture Discussion (Capstone) — Must-do, ~45 min

**Priority:** Must-do — Workshop-Capstone
**Type:** Group, ~30 minutes (Discussion) + optional Capstone Track (homework or bonus time)
**Goal:** Design an ideal Claude Code workflow for a real project.
This is the synthesis exercise — the goal of the entire workshop.

> **Note:** Before starting, review the Use Case Blueprints below for inspiration.

### Format

Groups of 3-4 people.  Each group designs a workflow.

### Your Task

Pick a real project (your work, a side project, the workshop demo).
Sketch the ideal Claude Code workflow for that project on the whiteboard or paper.

**Your workflow should address:**

1. **Hooks:**
   What automation happens without being asked?
   (Before commits? After file saves? When tests fail?)

2. **Skills:**
   What workflows are complex enough to formalize as skills?
   (Code review? Deployment? Specific kinds of analysis?)

3. **Scheduled tasks:**
   What runs automatically on a schedule?
   (Daily quality check? Weekly security scan? Dependency monitoring?)

4. **Multi-agent work:**
   Where would parallel agents help?
   (Parallel analysis? Fan-out scanning? Hierarchical review?)

5. **Security integration:**
   Where does adversarial testing fit?
   (Before every PR? Weekly? On-demand when external input changes?)

6. **Telegram triggers (optional):**
   What would you want to trigger from your phone?
   (Incident investigation? Build status? Deployment?)

7. **Continuous improvement:**
   Is there anything you would run the self-improve loop on?
   (Test coverage? Code style? Documentation?)

### Constraints to Consider

- What is the minimum viable workflow?  Not everything at once.
- What is the highest-value first automation to implement?
- What needs human review — where should Claude stop and ask?
- What could go wrong?  Where are the safety nets?

### Presentation

Each group presents their workflow in 5 minutes.
Use the whiteboard or walk through your sketch.

Focus on:
- What problem does this solve?
- What is the highest-value automation?
- What is the first thing you would actually implement this week?

### This Exercise IS the Workshop Goal

The ability to design this workflow is what we came here for.
You now have the vocabulary, the tools, and the mental models.
The workflow you sketch today should be something you can actually start building tomorrow.

### Optional: Capstone Track

If you have time after the discussion (or as homework after the workshop):

**Pick a home project** (your own code, a side project, a repo you use regularly) and build **one** concrete setup element based on workshop content:

- **Variant A — Skill for your workflow:** A skill that addresses a typical concern in your project (e.g., "Code review for firmware PRs", "Generate OSDP frame tests", "Audit access-control configs")
- **Variant B — Hook for your repo:** A hook that enforces a project-specific rule (e.g., "Never commit directly to main", "No edits to firmware/secure-boot.c without confirmation")
- **Variant C — Plugin:** Bundle 2-3 skills/hooks into a plugin and install it locally with `claude --plugin-dir ./my-plugin`
- **Variant D — CI workflow:** GitHub Action YAML that uses Claude Code as a reviewer (see Module 3.6)

**Expectation:** Not production-grade code, but a learning driver. Important: use it in your real workflow, not in the workshop sandbox.

**Optional sharing:** If you want, share your capstone artifact with the workshop community (Slack/Discord/email).

---

## Exercise 3.6: Build a Claude-Backed Pre-Commit Hook

**Type:** Individual, ~25 minutes
**Priority:** Should-do
**Goal:** Wire Claude Code into your local git workflow as a pre-commit lint gate — your first taste of Claude as a CLI tool in a pipeline.

### Background

Module 3.6 introduced the headless mode (`claude -p`, `--bare`, `--max-budget-usd`, `--output-format`). This exercise turns those flags into a real safety net: a git pre-commit hook that blocks dirty diffs before they leave your machine.

You will learn-by-doing four things at once:
- Headless invocation in a real script.
- A hard budget cap on a routine that runs on every commit.
- `--bare` mode to keep the hook fast.
- Reading Claude's structured output to decide pass/fail.

**Security analogy:** Pre-commit hooks are the badge-reader at the building exit — they check what is leaving before it leaves. Adding Claude to that reader gives it a brain instead of a regex.

### Steps

**Step 1: Pick a test repo**

Use the workshop playground or any small repo where you can experiment without worry:

```bash
cd workshop-playground
git init       # if it is not a repo yet
```

**Step 2: Write the hook**

Create `.git/hooks/pre-commit` with the following content:

```bash
#!/bin/bash
STAGED=$(git diff --cached)
if [ -z "$STAGED" ]; then exit 0; fi

RESULT=$(echo "$STAGED" | claude --bare -p \
  "Check this staged diff for obvious bugs, security issues, or leftover debug statements (print, console.log, debugger). Reply with 'OK' if clean, otherwise list the issues one per line." \
  --max-budget-usd 0.10 \
  --max-turns 2 \
  --output-format text)

if [[ "$RESULT" != "OK"* ]]; then
  echo "Pre-commit check failed:"
  echo "$RESULT"
  exit 1
fi
exit 0
```

Notice every flag from Module 3.6 in there:
- `--bare` so the hook starts fast and stays deterministic.
- `--max-budget-usd 0.10` as a hard cap — the worst-case cost of a commit attempt is one dime.
- `--max-turns 2` to prevent runaway loops.
- `--output-format text` because we only need a yes/no answer.

**Step 3: Make it executable**

```bash
chmod +x .git/hooks/pre-commit
```

(On Windows, use Git Bash or WSL — git's hook subsystem looks for executable POSIX scripts.)

**Step 4: Test the happy path**

Make a clean change (a comment, a typo fix, a whitespace tweak), stage it, commit. The hook should pass silently.

**Step 5: Test the unhappy path**

Now intentionally introduce a problem — add a `print("DEBUG")` line, a hardcoded password, or a commented-out test. Stage and try to commit. The hook should block, list the issues it found, and exit non-zero. The commit does not happen.

### Bonus (~5 min): Add a Cost Trace

Log each invocation to a local trace file so you can later audit how much the hook actually costs:

```bash
echo "$(date) | $(basename "$0") | budget=0.10 | result=$(echo "$RESULT" | head -1)" >> ~/.claude/precommit-trace.log
```

Add that line right before `exit 0` (and a similar one before `exit 1`). After a few commits, `tail ~/.claude/precommit-trace.log` shows you the real-world frequency and outcome of every hook run.

### Reflection

After 5+ commits with the hook active, answer these in your notes:

1. **Cost:** Roughly how many tokens did each invocation consume? Check `/usage` in an interactive session, or your Anthropic Console dashboard. Was the $0.10 cap close to being hit, or comfortably over-budget?
2. **Accuracy:** Did the hook catch a problem you would have committed otherwise? Did it cry wolf — false-positives that wasted your time?
3. **Speed:** Did the hook noticeably slow down your commit workflow? If yes, what would you trade off — fewer checks, smaller prompts, a faster model via `--model haiku`?
4. **Production-readiness:** Would you actually enable this hook in a real project? Pro/contra list with three bullets each.

### Success Check

- [ ] The hook is executable and lives at `.git/hooks/pre-commit`.
- [ ] A clean commit passes silently.
- [ ] A commit with an obvious issue is blocked with a readable message.
- [ ] Every Module 3.6 flag (`--bare`, `--max-budget-usd`, `--max-turns`, `--output-format`) appears in your hook.
- [ ] You have an opinion on whether to ship this in a real project.

### Stretch (if time allows)

Convert the hook to use `--output-format json` with a small `--json-schema`, and parse the result with `jq`. The hook decision becomes deterministic Boolean logic instead of string-prefix matching — exactly the pattern a CI runner would use.

---

## Bonus Exercise 3.8: HIPAA-Style Security Guardrails

**Type:** Individual, ~20 minutes
**Goal:** Build a hook that scans every file write for sensitive data patterns — simulating compliance guardrails.

> **For Non-US Audiences:** This bonus exercise uses HIPAA as a concrete example, but the
> pattern (preventing sensitive data from being written to insecure locations via PreToolUse
> hooks) applies equally to GDPR (EU personal data), PCI-DSS (payment cards), and EN 50131
> (Physical Security access logs). Adapt the regex patterns to your regulatory context —
> the hook mechanism is the same. See Module 3.3 "Regulated Industries: Compliance Notes"
> for the regulation-to-mechanism mapping.

### Background

In healthcare (HIPAA), in finance (PCI-DSS), and in physical security (access logs with personal data), there are strict rules about what data can be written to files. This exercise builds a PreToolUse hook that blocks Claude from accidentally writing sensitive patterns into code or config files.

**Security analogy:** This is the equivalent of a scanner at a secure facility exit — checking that nobody carries classified documents out of the building.

### Steps

**Step 1: Define your sensitive patterns**

Choose patterns relevant to your domain:
- Social security numbers: `\d{3}-\d{2}-\d{4}`
- Credit card numbers: `\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}`
- API keys: `(sk-|pk_|AKIA)[A-Za-z0-9]{20,}`
- Access card IDs (your domain!): patterns from your card reader format
- IP addresses of internal infrastructure: `10\.\d+\.\d+\.\d+` or `192\.168\.`

**Step 2: Create the scanner hook**

Create `~/.claude/hooks/sensitive-data-scanner.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
CONTENT=$(echo "$INPUT" | jq -r '.content // .new_content // ""')

# Check for sensitive patterns
PATTERNS='(\d{3}-\d{2}-\d{4}|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|password\s*=\s*["\x27][^"\x27]+)'

if echo "$CONTENT" | grep -qEi "$PATTERNS"; then
  MATCH=$(echo "$CONTENT" | grep -oEi "$PATTERNS" | head -3)
  echo "BLOCKED: Sensitive data pattern detected in file content:" >&2
  echo "$MATCH" >&2
  echo "Redact or remove sensitive data before writing." >&2
  exit 1
fi

exit 0
```

**Step 3: Register and test**

Add to settings.json with matcher `Write|Edit`. Test by asking Claude to create a config file with a hardcoded API key.

### Success Check

- [ ] Hook blocks writes containing sensitive patterns
- [ ] Hook allows normal writes without sensitive data
- [ ] You adapted at least one pattern to your specific domain
- [ ] You understand the difference between blocking (exit 1) and allowing (exit 0)

### Reflection

1. What sensitive data patterns exist in your actual projects?
2. Could you run this as a PostToolUse hook instead (log but don't block)?
3. How would you handle false positives (e.g., test data that looks like real credentials)?

---

## Exercise 3.7: Debug a Broken Hook

**Priority:** Should-do — valuable for self-sufficient productivity. Without this skill you are blocked every time a hook misbehaves.
**Type:** Individual, ~20 minutes (+5 min bonus)
**Goal:** Diagnose and fix a misconfigured hook using only the standard inspection tools — without reading the hook script first.

### Background

The moderator has prepared a mini-setup with a hook in `~/.claude/settings.json` that **blocks every Bash command**, even the harmless ones. Symptom: every `ls`, every `cat`, every `git status` produces a permission prompt or an outright deny. The terminal feels broken.

Your job is **not** to peek at the hook script. The job is to find the problem the way you would find it on a colleague's machine — using only `/hooks`, `claude --verbose`, and the diagnosis playbook from Module 3.7.

**Security analogy:** A new access-control policy was deployed overnight. Every door is now denying every card. The vendor has not returned your call. You walk the layers: card → reader → controller. Same loop, software version.

### Task

**Step 1: Recognize the problem without reading the script**

- Run `/hooks` — what does the matcher look like? Is it suspiciously broad (e.g. `".*"`, `"Bash.*"` without further restriction)?
- Restart Claude with `claude --verbose` — what does the boot log say about the registered hook?

Write down your hypothesis **before** opening the script.

**Step 2: Analyze the hook script**

- Open `~/.claude/hooks/<name>.sh`.
- Read the matcher and the body. What does the matcher actually match? Is it broader than the docstring claims?
- What does the body do? Is it logging, blocking, or both?

**Step 3: Fix the script**

Pick one of two approaches:

- **Tighten the matcher.** Change `".*"` to a specific pattern that matches only what the hook is supposed to scrutinize (e.g. `"Bash(rm *)"` for destructive-command checks, not for `ls`).
- **Temporarily disable the hook** in `settings.json` by removing it from the matcher list (good for unblocking yourself while you reason about the right matcher).

**Step 4: Verify**

- Run a harmless command like `ls` or `git status`.
- It should run **without a permission prompt** this time.
- Run `/hooks` again — confirm the matcher is now what you intended.

### Bonus (~5 minutes)

**Step 5: Write a self-inspecting hook script.**

Modify the (now-fixed) hook so that on every match it appends an entry to `~/.claude/hook-trace.log`:

```bash
TIMESTAMP=$(date -Iseconds)
ACTION=$(echo "$INPUT" | jq -r '.tool // "unknown"')
DECISION="allow"   # or "block" depending on your hook logic
echo "$TIMESTAMP | $ACTION | $DECISION" >> ~/.claude/hook-trace.log
```

Now you have an **audit trail** for hook activity. Later when something feels off ("did my hook fire on that command?"), you `tail -20 ~/.claude/hook-trace.log` and see immediately.

This is the production-grade pattern: every hook should leave a trace, not just a silent block.

### Report

In the discussion afterward, share:

1. **What was the root cause?** Matcher too broad? Exit code wrong? Path wrong?
2. **How would you have found this without `/hooks` and `--verbose`?**
   *(Honest answer: it would have been much harder. Without `/hooks` you would not even know which hook was firing. Without `--verbose` you would not know the matcher was registered too broadly. These two commands are essential.)*
3. **What would you change in the script if it were yours to maintain long-term?**
   *(Tighten the matcher, add the trace log, set an explicit timeout, document the matcher's intent in a comment.)*

### Why This Matters

Hooks are the most powerful Claude Code feature and the easiest to misconfigure. A team that uses hooks heavily will hit this exact scenario every few weeks. The 15 minutes you spent here are the difference between "Claude is broken, give up" and "30-second diagnosis, surgical fix, back to work".

---

## Use Case Blueprints — Inspiration for Exercise 3.5

These blueprints come from deep research into advanced Claude Code workflows. Use them as building blocks for your Architecture Discussion:

| # | Blueprint | Components | Security Relevance |
|---|-----------|-----------|-------------------|
| 1 | **Secure Diff Gate** — Block writes to `.env`, secrets, credentials | PreToolUse Hook + matcher `Write\|Edit` | Prevent accidental secret exposure |
| 2 | **Token Firewall** — Filter noisy test/build output | PreToolUse Hook on Bash + filter script | Cost control, context management |
| 3 | **Circuit Breaker** — Stop agents stuck in retry loops | PostToolUse Hook detecting 3x same error | Prevent runaway token costs |
| 4 | **CVE-Fix Pipeline** — From advisory to PR automatically | WebSearch + Plan Mode + Bash + Git | Vulnerability management |
| 5 | **CI-Locked Agent** — Claude as CI worker with strict rules | `dontAsk` mode + allow rules + `--json-schema` | Deterministic pipeline integration |
| 6 | **Repo Onboarding** — `/init` + Skills + Hooks as team standard | `/init` + Plugin packaging + managed scope | Team standardization |
| 7 | **Autonomous Refactor** — `/batch` across worktrees | `/batch` + subagents + worktrees | Safe large-scale changes |
| 8 | **Living Architecture Map** — Auto-generated Mermaid diagrams | LSP + Skill + PostToolUse hook after merge | Documentation stays current |
| 9 | **Two-Device Debugging** — Remote control from phone/browser | `/remote-control` + local execution | Mobile incident response |
| 10 | **Agent Team as Virtual Dev Org** — Lead + Reviewer + QA + Docs | TeamCreate + SendMessage + Sonnet teammates | Parallel specialized work |

---

*End of Block 3 Exercises*
