# Block 3: Demo Scripts for Moderator

> Live demos for the afternoon advanced block.
> Each demo has a clear talking point — the security analogy that ties it to the audience's world.

---

## Demo 3.1: Multi-Agent Orchestration

**Goal:** Show two agents running simultaneously on independent tasks.

### Setup

Have a mid-sized project open (the workshop demo project or any real codebase with 10+ files).

### Steps

**Step 1: Ask Claude to analyze from two angles in parallel**

Tell Claude (type this out loud so the audience sees the prompt):

> "Analyze this project using two separate agents running in parallel:
> Agent 1 maps the overall architecture — directory structure, key files, main entry points, technology stack.
> Agent 2 scans for all TODO, FIXME, HACK, and XXX comments and lists them with file and line number.
> Run both agents simultaneously and give me a combined report."

Watch the two agent threads appear in the output.
Point out that both are running at the same time — not waiting for each other.

**Step 2: Show /agent-orchestrator for structured multi-model work**

```
/agent-orchestrator
```

Select: Haiku for brainstorming, Sonnet for analysis.
Task: "Generate 5 architectural improvement ideas for this project, then evaluate each one for feasibility and impact."

Show how Haiku generates ideas quickly (fast, cheap), Sonnet analyzes them with more depth.

### Talking Point

"We just dispatched two security teams to sweep different floors simultaneously.
One team is mapping the building layout, the other is checking for hazards.
They report back independently — we get both reports in parallel, not sequentially.
This is exactly how a well-run SOC operates."

---

## Demo 3.2: Codex Swarm

**Goal:** Show multi-model pipeline — Claude plans, Codex builds in parallel, Claude reviews.

### Prerequisite

Codex CLI must be installed and authenticated.
Verify with: `codex --version`

### Steps

**Step 1: Launch Codex Swarm with decompose**

```
/multi-model-orchestrator:codex-swarm --decompose
```

When prompted for the task, enter:

> "Build a Python CLI security tool with three commands:
> 1. scan: given a hostname, attempt connections to ports 21, 22, 23, 25, 80, 443, 3306, 5432, 8080, 8443 and report which are open
> 2. check: given a URL, make an HTTP GET request with a 5-second timeout and report the status code and response time in milliseconds
> 3. report: run both scan and check on a given target and output a JSON report with timestamp, target, open ports, and HTTP status
> Include a CLI entry point using argparse, proper error handling, and a test file."

**Step 2: Watch decomposition**

Point out that Claude is analyzing the task and breaking it into independent subtasks before spawning any Codex agents.
Name each subtask as Claude identifies it.

**Step 3: Watch parallel execution**

Show the N Codex agents spinning up simultaneously.
Highlight that they are working in parallel — the timer is running for all of them at once.

**Step 4: Claude reviews**

Watch Claude read through all generated files.
Point out what it catches — integration issues, missing error handling, test coverage gaps.

### Talking Point

"This is the architect-contractor-inspector model.
Claude Opus designed the spec.
Codex agents built the components in parallel — like contractors installing readers on different floors at the same time.
Claude Opus is now inspecting each component before sign-off.
Three different intelligence profiles.  One pipeline.  The result is better than any one of them alone."

---

## Demo 3.3: Devil's Advocate — Adversarial Security Testing

**Goal:** Show automated penetration testing pipeline.  This demo is the highlight for the CySec audience.

### Setup

You have already cloned `workshop-playground/` as part of the prerequisites (Step 7).
We use it as-is — it ships with three deliberately planted vulnerabilities in `access_control.py`.

No file creation required for this demo.

> **Windows note for moderators:** The Command Injection vulnerability lives in `backup_database()` and uses the Unix `cp` command (`access_control.py:140`). On a Windows workshop machine, the live `backup` CLI call will fail at runtime (no `cp` on Windows). The **swarm still detects the vulnerability statically** because the dangerous pattern (`subprocess.run` with `shell=True` and unvalidated input) is what matters. If you want to demonstrate live exploitation as well, open a Git Bash or WSL shell — otherwise note the limitation aloud and move on. The static finding is the point of the demo.

### Steps

**Step 1: Move into the playground**

```bash
cd workshop-playground/
```

**Step 2: Launch the adversarial swarm**

```
/devil-advocate-swarms:swarm scan workshop-playground/access_control.py
```

**Step 3: Watch Stage 1 — Scanners**

Two scanners run in parallel.
Name what each is looking for.
Point out: they will both find the planted issues — overlap = validation.

Expected confirmed findings (three planted issues):
- **Command Injection** in `backup_database()` (`access_control.py:~140`) — `subprocess.run(f"cp {DB_FILE} {filename}", shell=True)` with unvalidated CLI input from the `backup` command
- **Hardcoded Credential** `ADMIN_PASSWORD = "admin123"` (`access_control.py:19`) — a literal secret at module scope
- **Path Traversal** in `read_log()` (`access_control.py:~127`) — `open(f"logs/{log_name}")` with no sanitization, reachable via the `read-log` CLI command

There is also a strong chance the scanners surface an **ungeplante bonus finding**: a **Log-Injection / Log-Forging** issue in `log_event()` (`access_control.py:105-113`). The function writes `username` and `action` straight into a line-based log file — a newline-bearing username can forge log entries. If the swarm catches this, celebrate it; if not, mention it after the demo as evidence that no scanner is exhaustive.

**Step 4: Watch Stage 2 — Debate**

This is the most important part.  Slow down and explain what is happening:
- Prosecutor is arguing each finding as if writing an exploit report
- Defender is looking for reasons it is not exploitable
- For the hardcoded credential: Defender has no good argument.  Confirmed.
- For the command injection: same.  Confirmed.
- For the path traversal: Defender may argue "logs/ is a controlled directory" — Prosecutor counters with the `../../etc/passwd` example. Confirmed.
- Point out if any finding gets argued away — that is the system saving engineer time.

**Step 5: Watch Stage 3 — Consensus**

Show the CONFIRMED vs FALSE POSITIVE split.
Each confirmed finding has a full audit trail — the debate transcript is the evidence.

**Step 6: Watch Stage 4 — Fixers**

Show the fixes being applied.
Each fix is minimal and targeted.
Each has a regression test.

**Step 7: Show the planted vulnerabilities were all found**

Scroll through findings. **Three confirmed planted issues + 1 bonus finding (Log-Injection)** is the expected outcome — three of the swarm's confirmations map 1:1 onto the planted vulnerabilities, the fourth (if surfaced) is the un-planted log forging issue.

### Talking Point

"This is an automated penetration test with a built-in legal review.
The Prosecutor is your pentester writing the exploit report.
The Defender is your developer explaining what is and is not actually exploitable.
The Consensus agent is your security manager deciding what gets a CVE.
The Fixers are your patching team.
The entire thing just ran in under 5 minutes.
For the CySec engineers in the room — this is your world applied to code."

---

## Demo 3.3b: Permission Modes — From Visitor to Master Key (~5 minutes)

### Goal
Show the 6 permission modes live. Demonstrate how the same task behaves differently under different clearance levels.

### Steps

**Step 1: Show default mode (1 min)**

Start Claude Code normally (default mode). Ask:
```
Show me the contents of package.json
```
This works without asking — reads are always allowed.

Now ask:
```
Add a comment to the top of README.md
```
Claude asks for permission. Say: *"Default mode. Visitor badge. Reading is free, writing needs approval."*

**Step 2: Switch to acceptEdits (1 min)**

```
/permissions
```

Switch to `acceptEdits`. Now ask:
```
Add a comment to the top of README.md
```
This time it goes through without asking. But:
```
Run npm test
```
Still asks. Say: *"Maintenance badge. You can open office doors but the server room still needs authorization."*

**Step 3: Show plan mode (2 min)**

Start a new session with:
```bash
claude --permission-mode plan
```

Ask:
```
Refactor this file to use async/await instead of callbacks, add error handling, and run tests
```

Claude shows the full plan first. One approval covers all steps.

Say: *"Plan mode is the security briefing. You approve the whole mission, not each step. Useful for complex multi-step tasks where constant approving is exhausting."*

**Step 4: Mention dontAsk and bypass (1 min)**

Don't demo these live (too dangerous for live demo). Just explain:
- `dontAsk` = pre-approved work orders for CI/CD, only allow-listed operations run
- `bypassPermissions` = master key, only inside sealed test facilities (Docker, sandbox)

Say: *"You would never give a contractor a master key in a live building. Same rule applies here. Bypass mode is for sealed test environments only."*

### Talking Point
*"6 clearance levels. From visitor badge to master key. You pick the right one for the situation — just like you'd never give a delivery driver the same access as the building engineer."*

---

## Demo 3.3c: CVE-Fix Pipeline — From Advisory to PR (~5 minutes)

### Goal
Show Claude fixing a real dependency vulnerability using web search + plan mode + automated PR. This is the "Research-to-Patch" blueprint.

### Steps

**Step 0: Plant a vulnerable dependency (before demo)**

The default `workshop-playground/requirements.txt` only contains unpinned `pytest`. Before the demo, temporarily pin a known-vulnerable older library so the CVE-fix flow has real input.

```bash
# Inside workshop-playground/
# Option A (Python, recommended):
echo "requests==2.5.0" >> requirements.txt    # CVE-2018-18074

# Option B (alternative Python CVE):
# echo "urllib3==1.24.0" >> requirements.txt
```

Important: **bewusst NICHT installieren** — this demo only shows the scan + fix + PR flow, not actual exploitation. We just need the version string in the manifest so Claude can find an advisory for it.

**Step 1: Ask Claude to fix it (3 min)**

```
/plan Find and fix any known CVEs in our dependencies.
Search the web for current advisories, identify the fix version,
update the lockfile, run tests, and create a PR.
```

Walk through what Claude does:
1. **WebSearch** — finds the advisory on NVD/GitHub for the pinned old version
2. **Plan** — identifies the affected package, the fix version, and the migration path
3. **Edit** — updates the version in `requirements.txt`
4. **Bash** — runs `pip install` and tests (skip the install if no internet — Claude can still produce the PR)
5. **Git** — commits and creates a PR with the CVE reference

**Step 2: Show the PR description (1 min)**

Point out that Claude included:
- CVE ID and link to advisory
- What was vulnerable and why
- What was changed
- Test results

Say: *"From 'there's a CVE' to 'here's a PR with tests' — in under 3 minutes. This is vulnerability management at machine speed."*

**Step 3: Clean up after the demo**

```bash
# Remove the planted vulnerable line so the playground does not stay verwundbar by accident:
# Open requirements.txt and delete the requests==2.5.0 (or urllib3==1.24.0) line you added in Step 0.
```

Reverting the planted line keeps the playground in its intended state for later sessions and prevents any participant from accidentally `pip install`-ing a known-vulnerable library on their machine.

### Talking Point
*"In your world, a vulnerability in a door controller firmware means: find the advisory, identify affected units, plan the update path, test on a bench, deploy, verify. Same process here — but Claude does steps 1 through 5 automatically. You review and approve."*

---

## Demo 3.4: Self-Improve Loop

**Goal:** Show a system that analyzes its own weaknesses and fixes them autonomously.

### Setup

Use a project with some test failures or quality issues.
The workshop demo project works well.

### Steps

**Step 1: Show the current state**

Run the quality gate first so the audience sees the baseline:
```
/quality-gate
```
Note the score and any failures.

**Step 2: Start the self-improve loop for 1 iteration**

```
/agentic-os:run-loop
```

When asked for iterations, enter `1`.
Walk through what is happening in each phase:
- Analysis: "Reading the quality gate results and iteration history"
- Planning: "Identifying the highest-impact issue to address"
- TDD: "Writing a failing test — watch, it should fail"
- Implementation: "Writing the minimum code to make the test pass"
- Quality gate: "Running the full check — this is the go/no-go decision"
- Commit: "Only happens if the gate passes — otherwise the iteration is discarded"

**Step 3: Show the iteration log**

```
cat .agent-memory/iterations/iteration-001.md
```

Walk through the log: what it analyzed, what it decided, what it changed, what it verified.

**Step 4: Run the quality gate again**

Show the score improved.

### Talking Point

"The system just improved itself.
It analyzed its own weaknesses, designed a fix, verified the fix with tests, confirmed quality did not regress, and committed the improvement.
To pull the security analogy one more time: this is a security system that ran its own penetration test, found a vulnerability, patched it, tested the patch, and logged the entire operation.
With no human involvement.
This is what continuous security hardening looks like when applied to software."

---

## Demo 3.5: The Full Stack — Architecture Discussion

**Goal:** Connect all the pieces.  Show the full vision.  Finish with the Telegram demo.

### Steps

**Step 1: Worktree isolation (live)**

```bash
git worktree add ../demo-sandbox -b demo/sandbox
```

Show that `../demo-sandbox` is a clean working copy.
Have an agent do something in the sandbox.
Show the main directory is untouched.
Discard it:
```bash
git worktree remove ../demo-sandbox
```

"The agent worked in a locked room.  We unlocked the door, checked the work, and locked it again."

**Step 2: Whiteboard — the full architecture diagram**

Draw on the whiteboard (or project the ASCII diagram from the module):
- Telegram Bridge -> Orchestrator
- Orchestrator -> specialized agents in worktrees
- One path leads to Devil's Advocate Swarm
- Results aggregate back to orchestrator
- Report sent to Telegram

Walk through each node and explain what it does and what its security boundary is.

**Step 3: Inception (if Docker is available)**

```
/multi-model-orchestrator:inception
```

Task: "List all Python files in /workspace and count the lines of code in each."

Show that Claude runs inside a container.  The container's filesystem is isolated from the host.

**Step 4: Telegram demo (if configured)**

Send a real message from your phone.
Read the response aloud when it arrives.
"I just triggered a full code analysis from my phone.
While I was walking to the coffee machine.
Claude is running agents, which are running tools, which are scanning files — all from that one message."

### Talking Point

"You have an always-available operations center in your pocket.
Every workflow we built today — the multi-agent scans, the adversarial security testing, the self-improving quality checks — all of it can be triggered from a Telegram message and reported back to your phone.
You do not need to be at a laptop.
You do not need to be awake.
Claude is on call."

---

## Demo 3.6: Headless Claude in 5 Minutes

**Goal:** Take the interactive Claude you have used all day and prove it also runs as a one-shot CLI tool — with JSON output, cost caps, and `--bare` mode. Five minutes, four flags, one mindset shift.

### Prerequisite

- `claude` installed and authenticated on the moderator's workstation.
- A small file to feed in. `workshop-playground/access_control.py` works perfectly.
- A terminal where the audience can see both the command and its exit code.

### Steps

**Step 1: Headless basics — one prompt, one answer**

Type at the prompt so the audience watches:

```bash
claude -p "Summarize what this repo does in one sentence."
```

When the single-line answer prints, point out three things:

1. No interactive loop — the prompt returned to the shell.
2. Output went to stdout — pipeable to any other tool.
3. Exit code 0 — the shell would have noticed a failure.

"That is the same Claude you have been talking to all day. Same model, same skills available. The only thing missing is the conversation loop."

**Step 2: Structured output with a schema**

```bash
claude -p "Categorize this file" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"category":{"type":"string"},"language":{"type":"string"}}}' \
  < workshop-playground/access_control.py
```

When the output appears, pipe it through `jq` live to show it really is parseable:

```bash
... | jq '.category'
```

"A CI pipeline can rely on this. Free-form prose breaks parsers — a schema does not."

**Step 3: Demonstrate a cost cap**

```bash
claude -p "Refactor this entire codebase from scratch with full test coverage" \
  --max-budget-usd 0.05 \
  --max-turns 2 \
  < workshop-playground/access_control.py
```

Expectation: Claude starts an ambitious answer, hits the cap, exits cleanly with a budget-exhaustion message. Highlight the exit code (`echo $?`) — non-zero. CI would fail this step instead of running it forever.

"Without that flag this prompt could have spent dollars. With it, the worst case is five cents."

**Step 4: `--bare` mode — show the time difference**

Side-by-side timing:

```bash
time claude -p "Hello"
time claude --bare -p "Hello"
```

`--bare` should return noticeably faster — it skips skill discovery, MCP handshake, hook registration. Call out the delta out loud.

"For a `Hello` you do not need plugins. For a real CI step you might. Pick the right tool."

### Talking Point

"We just turned Claude Code into a Unix-style tool. It takes stdin, produces stdout, returns an exit code, respects flags, and stays within a budget. That is the entry ticket to every CI system on Earth — GitHub Actions, GitLab, Jenkins, your own cron. The interactive Claude is one half of the product. This half is the other."

### Recovery Note

If you also want to show `claude setup-token`, do it **offline before the workshop**, not on the shared screen. The command emits a long-lived OAuth token — treating it carelessly is the same risk class as showing your SSH private key on a projector. Mention the command, point to the docs, move on.

---

## Demo 3.7: Diagnosing a Broken Skill

**Goal:** Walk the audience through the full diagnostic playbook on a skill that fails three different ways in sequence. Each fix reveals the next problem.

### Prerequisite

The moderator has prepared an intentionally broken skill at `~/.claude/skills/broken-greeter/SKILL.md` with **three problems planted** in this order:

1. **Description is generic** — no concrete trigger phrases (just "A skill for greeting").
2. **`disable-model-invocation: true`** in frontmatter — skill is registered but auto-invocation is disabled.
3. **`paths: ["never-match/**"]`** — paths filter that no real file can satisfy.

The body of the skill is functional ("Reply with a friendly greeting that uses the user's name"). Only the metadata is wrong.

### Steps (~7 minutes)

**Step 1: Try to use the skill normally**

User prompt:

> "Greet the user."

Watch the skill not fire. Claude answers with a generic greeting from its base behavior — no sign the skill was even considered.

**Step 2: Confirm the skill is installed**

```
/skills
```

Point out: `broken-greeter` is in the list. So installation is not the problem.

**Step 3: Inspect the frontmatter**

```bash
cat ~/.claude/skills/broken-greeter/SKILL.md | head -20
```

At first glance the frontmatter looks plausible. **Resist the urge to read it carefully.** Instead use the diagnostic tool — that is the lesson.

**Step 4: Activate `/debug` and re-trigger**

```
/debug skill-not-triggering
```

Then repeat the prompt: *"Greet the user."*

Read the trace aloud. Highlight the line:

> *"Skill `broken-greeter` matched paths-filter: NO (filter: `never-match/**`, current files: ...)"*

The first root cause is now visible. Audience reaction: "Oh — the paths filter is wrong."

**Step 5: Fix #1 — remove the paths filter**

Edit the frontmatter, delete the `paths:` line. Re-trigger the prompt. **Skill still does not fire.** Re-read the trace:

> *"Skill `broken-greeter` registered but auto-invocation disabled (`disable-model-invocation: true`). Available only via explicit `/broken-greeter`."*

**Step 6: Verify with manual invocation**

```
/broken-greeter
```

Skill fires — confirms the body works. The block was purely metadata.

**Step 7: Fix #2 — flip `disable-model-invocation` to `false`**

Edit the frontmatter, set `disable-model-invocation: false`. Re-trigger:

> "Greet the user."

**Skill still does not fire** — but the trace now says something different:

> *"Skill `broken-greeter` description too generic for prompt — no candidate match."*

**Step 8: Fix #3 — rewrite the description with trigger phrases**

Edit the description from `"A skill for greeting"` to something like:

```
description: >
  Greets the user warmly by name. Use whenever the prompt is "greet the user",
  "say hello", "welcome me", "hi", or any opening pleasantry.
```

**Step 9: Verify full auto-invocation**

```
"Greet me"
```

Now the skill fires automatically. Three problems, three diagnostic steps, three fixes.

### Talking Point

"Notice that we never **guessed** what was wrong. We let `/debug` and `/skills` tell us each layer's state. We could have stared at the frontmatter for an hour and missed the `paths` filter because it *looked* reasonable. The diagnostic tools turn the black box back into a glass box.

This is the **inspection-driven debugging** loop: ask the tools what they see, fix what they report, ask again. The moment you start guessing is the moment debugging stops being repeatable."

### Recovery Notes

- If `/debug` is not installed in your Claude Code version (older builds): use `claude --verbose` on session restart, and re-trigger the prompts. The trace is less inline but contains the same information.
- If the audience asks "why three problems instead of one?" — the answer is: real-world skills usually have one issue at a time, but **the diagnostic loop is the same regardless of how many issues you stack**. The point is the *method*, not the volume.
- If you want a shorter version (4 min instead of 7): plant only problems #1 and #3, skip the `disable-model-invocation` step.

---

*End of Block 3 Demo Scripts*
