# Retrieval And Recap Bridges

Purpose: turn prior sessions into active recall before new material begins. Keep every check short, oral, and ungraded.

---

## 5-Minute Active Recall Openers

Run these before the new session's PPT. Participants answer from memory first; then the facilitator reveals the slide/module anchor.

### Session 2 Opener: Foundations Recall

1. Which permission mode is safe for a first pass in an unfamiliar repo, and why?
2. What belongs in `CLAUDE.md` instead of only in chat?
3. What is one sign that context compression or memory drift may be affecting an answer?
4. Which narrow check would you run before trusting a Claude-generated change?
5. What is the cheapest way to keep a routine task from becoming a cost surprise?

### Session 3 Opener: Ecosystem Recall

1. When is a hook better than a skill?
2. What does `suppressOutput` solve in a PostToolUse hook?
3. What is the difference between a local plugin test with `--plugin-dir` and a team install?
4. When should NotebookLM/RAG be preferred over pasting a large document into chat?
5. What is the first safety question before giving an automation write access?

### Session 4 Opener: Advanced Kern Recall

1. Which tasks benefit from parallel agents, and which tasks should stay single-threaded?
2. What makes an adversarial review more trustworthy than one generic review prompt?
3. Which permission mode or deny rule would you choose before an autonomous loop?
4. What must be capped before `/schedule`, `/loop`, `/goal`, or a Routine runs unattended?
5. What evidence would convince you that a security finding is confirmed, not just plausible?

---

## In-Session Quick Checks

Use after dense analogy clusters. These are 60-90 second checks, not quizzes.

| After | Prompt | Expected signal |
|---|---|---|
| S1.6 Permission Modes | "Name the clearance level you would give Claude for a repo you have never seen." | Participant chooses `default` or `plan` and mentions least privilege. |
| S1.10 `CLAUDE.md` | "Name one standing order that belongs in `CLAUDE.md` for your team." | Participant names a persistent rule, not a one-off prompt. |
| S2.8 Hook Outputs | "Plain stdout or JSON field: which one suppresses noisy output?" | Participant says JSON with `suppressOutput`, not plain stdout. |
| S3.12 Scheduling | "What safety net must every unattended routine carry?" | Participant names budget cap plus stop condition or human review. |
| S4.8 Capstone | "What evidence makes your handoff PR-ready?" | Participant names narrow check, risk, rollback, and exact command run. |

