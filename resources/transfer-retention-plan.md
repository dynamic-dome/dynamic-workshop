# Transfer And Retention Plan

Purpose: prevent the workshop from staying inside the synthetic playground. Each participant leaves with one concrete next move for their own work repo.

---

## Bring-Your-Own-Repo Transfer LEs

Each session reserves 10 minutes for a real-work transfer beat. Participants do not need to expose proprietary code on screen; they can use a private repo, a sanitized clone, or a paper inventory if policy blocks live access.

| Transfer LE | Session | Prompt | Output |
|---|---|---|---|
| S1-T | Foundations | Pick one repo and run a context/readiness pass: what files should Claude read first, what must be off-limits, and what narrow check proves a safe first change? | Repo entry map: context files, protected paths, first safe check |
| S2-T | Ecosystem | Choose one repeatable workflow from your repo and decide whether it belongs as a skill, hook, plugin, MCP integration, or RAG source. | One automation candidate with boundary, trigger, and install surface |
| S3-T | Advanced Kern | Pick one risky or repetitive team task and define the safe autonomous shape: agent role, permission mode, worktree, budget cap, and stop condition. | One bounded automation design with explicit safety net |
| S4-T | Advanced Bonus | Turn the capstone into a 30-day adoption slice for your actual team: first PR, first guardrail, first scheduled/routine follow-up. | Adoption plan draft plus owner/date/check |

Facilitator script: "Do not solve the whole repo. Name the next safe slice."

---

## One-Page Take-Home Adoption Plan

Participants fill this out in the final 10 minutes and keep it with the course materials.

### 1. Target Repo

- Repo / system:
- Business context:
- Data sensitivity:
- Protected paths:

### 2. First Useful Claude Code Workflow

- Task:
- Why it matters:
- Claude Code surface: CLI / skill / hook / plugin / MCP / CI / routine:
- Human approval point:

### 3. First 7 Days

- Day 1:
- Day 3:
- Day 7:
- Narrow verification check:
- Rollback path:

### 4. 30-Day Follow-Up

Create one async follow-up using the S3.12 scheduling primitives:

```text
/schedule 30 days from now "Review the adoption plan for <repo>: what shipped, what blocked, what guardrail is missing?"
```

For recurring adoption loops, prefer a Routine over an ad-hoc one-off schedule:

```text
Routine: monthly-claude-code-adoption-review
Cadence: monthly for 3 months
Scope: adoption plan, merged PRs, open risks, next guardrail
Budget cap: set explicitly before unattended runs
Worktree: dedicated review branch if files will be written
```

### 5. Success Signal

One sentence:

> In 30 days, Claude Code adoption is working if...

