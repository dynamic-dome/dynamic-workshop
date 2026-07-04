# Capstone Exit Assessment

Purpose: measure whether participants can use Claude Code independently and productively, not whether they remember workshop labels.

Use this as the final S4.8 artifact. The facilitator observes; the participant drives.

---

## Capstone Exit Task

**Mission:** In 35-45 minutes, ship one small improvement in `workshop-playground/` with Claude Code as the main workbench.

The participant must complete all four outputs:

1. **Feature or fix:** implement a small behavior change or bug fix in the playground.
2. **Hook or guardrail:** add one project-specific safety net, such as a pre-commit check, a hook, a permission rule, or a documented allow/deny policy.
3. **Verification:** run the narrow relevant test or manual check and explain why it proves the change.
4. **PR-ready handoff:** produce a branch, commit, and PR description with risks, rollback notes, and the exact checks run.

Allowed support: documentation, local repo files, and Claude Code. Not allowed: facilitator step-by-step driving. The facilitator may answer clarification questions, but should not choose commands or write the implementation.

---

## Observable Rubric

Score each row 0-3. Passing threshold: 12/18 with no zero in safety or verification.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Mission framing | Cannot define a concrete change | Defines a vague task | Defines a small, testable task | Defines scope, risk, and done criteria before coding |
| Claude Code operation | Needs facilitator to choose every command | Uses prompts but loses context often | Drives normal CLI flow with occasional help | Uses context, files, and checkpoints independently |
| Implementation | No working change | Partial change with unclear behavior | Working narrow change | Working change with minimal blast radius and clean handoff |
| Hook / guardrail | No safety net | Generic or non-runnable safety idea | Runnable or clearly installable guardrail | Guardrail is relevant, bounded, and documented |
| Verification | No check | Runs a broad or unrelated check | Runs the relevant narrow check | Explains what the check proves and what it does not prove |
| PR handoff | No handoff | Summary only | Commit plus PR notes | Commit, PR notes, risks, rollback, and checks are explicit |

---

## Session Entry / Exit Self-Efficacy Check

Run this for each session: once before the first slide, once in the final five minutes. Use a 1-5 scale: 1 = not yet, 5 = confident without help.

1. I can explain what Claude Code should and should not be allowed to do in my repo.
2. I can give Claude Code enough project context to work without over-scoping.
3. I can verify a Claude Code change with an appropriate narrow check.
4. I can add or choose a guardrail before automation becomes risky.
5. I can turn a Claude Code result into a clean handoff for another developer.

Facilitator note: compare the entry and exit numbers qualitatively. The goal is visible confidence movement, not grading anxiety.

---

## S4.8 Run Order

1. **5 min:** participant chooses the mission and states done criteria.
2. **25-30 min:** participant drives Claude Code on the playground.
3. **5 min:** participant runs verification and explains evidence.
4. **5 min:** participant drafts PR-ready handoff.
5. **5 min:** facilitator scores rubric and gives one concrete next-step recommendation.

Final handoff: copy the next-step recommendation into `resources/transfer-retention-plan.md`'s take-home adoption plan and schedule the 30-day async follow-up.
