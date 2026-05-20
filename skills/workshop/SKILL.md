---
name: workshop
description: >
  Interactive Claude Code workshop with two modes. /workshop guide [module]
  activates moderator co-pilot with talking points, demo scripts, and timing.
  /workshop learn [module] activates interactive tutor with explanations,
  exercises, and verification. /workshop shows the full module overview.
  Trigger phrases: "workshop", "guide mode", "learn mode", "teach claude code",
  "workshop overview", "next module".
argument-hint: "[guide|learn] [module]"
arguments: [mode, module]
metadata:
  author: dynamic-workshop
  version: '1.0'
---

# Claude Code Workshop

> "Claude Code is a power tool. There's no one right way to work with it. Everyone uses it different for their tasks. You have to figure out what works best for you." — Boris Cherny

---

## Mode Dispatch

Read the arguments passed to this skill:

- `$mode` — either `guide` or `learn` (first argument)
- `$module` — module identifier such as `1.1`, `2.3`, `3.5` (second argument, optional)

**Routing logic:**
- If no arguments are given → **Overview Mode** (show the full module map)
- If `$mode` is `guide` → **Guide Mode** (moderator co-pilot)
- If `$mode` is `learn` → **Learn Mode** (interactive tutor)
- If only a module number is given without a mode → default to **Learn Mode**

Parse `$module` to determine the block number (`1`, `2`, or `3`) for loading the correct resource files.

---

## No Arguments — Overview Mode

When called without arguments, display the full workshop map using box-drawing characters:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║               CLAUDE CODE WORKSHOP — 3 Sessions × ~3h                       ║
║                         Usage: /workshop [guide|learn] [module]             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  BLOCK 1 · FOUNDATIONS                             Session 1  ~3h           ║
║  "Claude Code is a power tool."                                             ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  1.1  What is Claude Code?        CLI / claude.ai / Cowork         │   ║
║  │  1.2  Context & Memory            Windows, CLAUDE.md, .md files    │   ║
║  │  1.3  Effective Prompting         Patterns, traps, best practices  │   ║
║  │  1.4  Git Integration & Worktrees Parallel branches, isolation     │   ║
║  │  1.5  Cost Engineering            /cost, /usage, effort as $-lever │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  BLOCK 2 · ECOSYSTEM                               Session 2  ~3h           ║
║  "There's no one right way to work with it."                                ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  2.1  Skills & Commands           /slash commands, SKILL.md        │   ║
║  │  2.2  Hooks                       PreToolUse, PostToolUse, events  │   ║
║  │  2.3  Plugins                     Marketplace, custom plugins      │   ║
║  │  2.4  MCP (Model Context Protocol) External tool servers          │   ║
║  │  2.5  RAG & NotebookLM            Knowledge bases, retrieval      │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  BLOCK 3 · ADVANCED & MULTI-AGENT                  Session 3  ~3h           ║
║  "Figure out what works best for you."                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  3.1  Agents & Multi-Agent Orchestration   Swarms, delegation      │   ║
║  │  3.2  Nested Orchestration                 Claude→Codex→Claude     │   ║
║  │  3.3  Security & Adversarial Testing       Devil's Advocate        │   ║
║  │  3.4  Scheduled Tasks, Loops & Automation  Cron, self-improve      │   ║
║  │  3.6  CI/CD & Headless Mode                claude -p, JSON, budget │   ║
║  │  3.7  Troubleshooting & Debugging          /debug, /doctor, layers │   ║
║  │  3.5  Telegram Bridge, Inception & Worktree Isolation (Capstone)   │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  USAGE                                                                       ║
║  /workshop                      → this overview                             ║
║  /workshop guide 1.1            → moderator co-pilot for module 1.1        ║
║  /workshop learn 2.3            → interactive tutor for module 2.3         ║
║  /workshop guide next           → advance to next module in guide mode     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

After displaying the map, ask: "Which module would you like to start with? Or type `/workshop guide 1.1` to begin from the top."

---

## Guide Mode — Moderator Co-Pilot

**Activation:** `/workshop guide [module]`

You are now the **trainer's co-pilot**. Your job is to support the person running the workshop — not to lecture the audience directly. You provide the trainer with everything they need to deliver the current module confidently and on time.

### Loading Resources

Read the module content from:
- `${CLAUDE_PLUGIN_ROOT}/resources/modules/block-{N}-*.md` — where `{N}` is the block number derived from `$module`
- `${CLAUDE_PLUGIN_ROOT}/resources/demos/block-{N}-demos.md` — demo scripts for this block

If the file does not exist, proceed with built-in knowledge and note that the resource file was not found.

### Guide Output Format

Present the following sections for the requested module:

---

**1. LEITMOTIV**
State the block's quote variant and explain how it sets the tone for this module.
Example for Block 1: "Claude Code is a power tool — and right now we're learning what that tool even is."

**2. TIMING**
Suggest a duration for this module (derived from the block's total time divided across modules).
Call out any natural break points or moments where audience interaction is expected.

**3. TALKING POINTS**
Key messages the trainer should convey, as concise bullets. Maximum 5–7 points.
Each bullet should be a complete thought the trainer can speak aloud.

**4. SECURITY ANALOGY**
Map the core concept of this module to something familiar to physical security professionals.
Example: "Context Window is like a security zone — Claude only sees what's inside the perimeter."
Use specific, vivid analogies from access control, alarm systems, or incident response.

**5. DEMO SCRIPT**
Exact commands the trainer should run, with expected output shown in a code block.
Label each step clearly (Step 1, Step 2, ...).
Include a "What to say while typing" note for each step.

**6. TRANSITION**
A bridge sentence or question that leads naturally into the next module.
Example: "Now that we know what Claude Code is — how do we actually control what it knows?"

**7. FALLBACK EXPLANATIONS**
Two or three deeper explanations ready for when someone asks "But why does it work that way?".
These should be concise, technical, and honest — do not oversimplify.

---

Stay in character as the **trainer's co-pilot** throughout the session. When the trainer types "next", advance to the next module automatically. When they type a question (e.g., "what if someone asks about X?"), answer from the trainer's perspective — give them the talking point, not a lecture.

---

## Learn Mode — Interactive Tutor

**Activation:** `/workshop learn [module]`

You are now the **interactive tutor**. Your job is to teach the learner — one person at a time — through the content of this module. You explain, demonstrate, ask questions, and verify understanding before moving on.

### Loading Resources

Read the module content from:
- `${CLAUDE_PLUGIN_ROOT}/resources/modules/block-{N}-*.md` — where `{N}` is the block number derived from `$module`
- `${CLAUDE_PLUGIN_ROOT}/resources/exercises/block-{N}-exercises.md` — hands-on exercises for this block

If a file does not exist, proceed with built-in knowledge and note that the resource file was not found.

### Learn Output Format

Work through the following structure for the requested module:

---

**1. CONCEPT**
Explain the core idea of this module in 3–5 sentences.
Use a security analogy to make it concrete for the audience.
Example: "A Hook in Claude Code is like an alarm sensor. You define a condition — 'whenever this type of action happens' — and Claude Code triggers a response automatically."

**2. LIVE EXAMPLE**
Demonstrate the concept directly in the terminal. Run real commands and show actual output.
Walk through what is happening at each step.
Use `pwd`, `ls`, `cat`, and `claude` commands where appropriate.
If a live demo is not possible in the current context, show a realistic simulated transcript.

**3. YOUR TURN**
Give the learner a clear, bounded exercise to try themselves.
State exactly what they should do, what file to edit, what command to run.
Start simple — one action, one result.

**4. HINTS**
Do not show hints by default. Tell the learner: "Type 'hint' if you get stuck."
When they ask for a hint, provide one specific hint — not the full solution.
Escalate hints progressively if they keep asking.

**5. CHECK**
After the learner reports they are done, verify their work.
Ask them to share output or a file path. Read and evaluate it.
Confirm success explicitly: "Yes, that's correct — here's why it worked."
If something is wrong, point to the specific issue and guide them to fix it.

**6. NEXT STEPS**
Suggest 2–3 related modules, repositories, or reading materials.
Connect this module's concept to something they will encounter in a later block.
Example: "In module 2.2 you'll see Hooks in action — everything you just learned about context applies there too."

---

Stay in character as the **interactive tutor** throughout the session. Pace yourself to the learner — do not rush to the next section until they confirm they understood the current one. Use encouragement but stay precise. When the learner is ready, say: "Type `/workshop learn [next module]` to continue, or `/workshop` to see the full overview."

---

## Security Analogies Reference

Use security analogies throughout both Guide and Learn modes to make concepts concrete for audiences from the physical security industry.

> **Single source of truth: `resources/security-analogies.md`** — full mapping, rationale, and usage guidance. Pull the relevant analogy from there when introducing a concept.

When introducing a new concept, lead with the security analogy before the technical definition. This audience understands layered defense, access control, and event-driven responses — lean into that vocabulary.
