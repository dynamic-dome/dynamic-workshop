# Dry Run Session 2/3 - 2026-05-21

## Scope

Dry run against the current repo state after the deck refresh:

- `claude-code-workshop.pptx`
- `resources/session-plan.md`
- `resources/modules/block-2-ecosystem.md`
- `resources/modules/block-3-advanced.md`
- `resources/demos/block-2-demos.md`
- `resources/demos/block-3-demos.md`
- `resources/exercises/block-2-exercises.md`
- `resources/exercises/block-3-exercises.md`
- `agents/workshop-mentor.md`

This was a trainer dry run by inspection plus local preflight checks, not a paid live execution of Claude/agent/plugin workflows.

## Preflight

| Check | Result | Note |
|---|---|---|
| Deck render | PASS | PowerPoint exported 30 PNGs; no blank slides found. |
| Slide mapping | PASS | Session 2 uses slides 12-18; Session 3 uses slides 19-29 plus outro 30. |
| `claude --version` | PASS | `2.1.146 (Claude Code)` available. |
| `codex --version` | PASS | `codex-cli 0.128.0` available. |
| Local tools | PASS | `git`, `python`, `node`, `jq` are available. |
| Playground files | PASS | `access_control.py` and `osdp_frame_decoder.c` exist. |
| Playground tests | PASS | `python -m pytest -v`: 18 passed. |

## Session 2 Verdict

**Verdict: GREEN with timing discipline.**

Session 2 is runnable as a 3-hour ecosystem block if the moderator keeps these constraints:

- Use slides 12-18 as the visual opener, not as a full lecture.
- Treat Demo 2.1, Demo 2.2/2.2b, and Demo 2.4 as the live spine.
- Keep Demo 2.3 to show-and-tell unless plugin setup is already open.
- Keep Demo 2.5 as NotebookLM web-UI fallback unless the skill and notebook are prepared before the session.
- Exercises: do 2.1 + 2.2, then pick exactly one from 2.3/2.4/2.5.

### Session 2 Timeline

| Time | Plan | Dry-run decision |
|---|---|---|
| 0:00-0:10 | Recap + Block 2 intro | Use slides 12-18. |
| 0:10-0:35 | Module/Demo 2.1 | Live if `~/.claude/skills/` exists; fallback prompt is documented. |
| 0:35-1:00 | Module/Demo 2.2 + 2.2b | Live only with prebuilt hook file; inline JSON/bash quoting is too risky on Windows. |
| 1:00-1:25 | Exercises 2.1 + 2.2 | Keep paired. These are the highest-value hands-on items. |
| 1:35-1:55 | Module/Demo 2.3 | Show repo plugin anatomy if no installed plugin is available. |
| 1:55-2:25 | Module/Demo 2.4 | Live if Playwright MCP is configured; screenshot/story fallback is acceptable. |
| 2:25-2:40 | Module/Demo 2.5 | Web-UI fallback should be ready. Notebook indexing is not a live-session task. |
| 2:40-3:00 | Pick-one exercise + Q&A | Do not attempt all remaining exercises. |

## Session 3 Verdict

**Verdict: YELLOW/GREEN.** The story is strong, but too many demos depend on plugins, auth, budget, or external services. The dry-run shape should be:

- Must-show live: Demo 3.1 or a prepared parallel-agent example.
- Must-discuss: Demo 3.3 security pipeline, even if plugin fallback is used.
- Should-show live: Demo 3.6 headless CLI, because `claude` is installed locally.
- Should-show live if prepped: Demo 3.7 broken skill.
- Keep Demo 3.2 Codex Swarm, Demo 3.4 self-improve, and Telegram bridge as optional/fallback unless preflight is clean.
- Preserve Exercise 3.5 Capstone. It is the real learning outcome.

### Session 3 Timeline

| Time | Plan | Dry-run decision |
|---|---|---|
| 0:00-0:10 | Recap + Block 3 intro | Use slides 19-29. |
| 0:10-0:40 | Module/Demo 3.1 | Live if agent spawning is available; otherwise show fan-out prompt and expected shape. |
| 0:40-0:50 | Module/Demo 3.2 | Discussion-first unless `multi-model-orchestrator` is confirmed installed. |
| 0:50-1:10 | Module/Demo 3.3 | Highest domain fit. Plugin fallback must be ready. |
| 1:20-1:35 | Module/Demo 3.4 | Keep short; do not run multi-iteration loop live. |
| 1:35-1:50 | Module/Demo 3.6 | Live candidate. Use strict budget cap and harmless file input. |
| 1:50-2:05 | Module/Demo 3.7 | Live candidate if `broken-greeter` is prepared before session. |
| 2:05-2:20 | Module/Demo 3.5 | Worktree + `/remote-control`; Telegram only if already configured. |
| 2:20-3:00 | Exercise 3.5 | Must keep. Whiteboard architecture discussion. |

## Findings Fixed During Dry Run

1. **Skill-frontmatter drift in Module/Exercise 2.1**
   - Before: examples used old `version`, `author`, `tags` style as if it were part of loader behavior.
   - After: examples now use `when_to_use`, `argument-hint`, `arguments`, and related current fields.

2. **Mentor-agent frontmatter drift**
   - Before: `allowed_tools`.
   - After: `tools`.

3. **Session plan missed demos 3.6/3.7**
   - Before: Session 3 listed Module 3.6 and Module 3.7 only.
   - After: Session 3 explicitly lists `Module 3.6 + Demo 3.6` and `Module 3.7 + Demo 3.7`.

4. **Session plan did not reference the new slide ranges**
   - After: Session 2 opener references slides 12-18; Session 3 opener references slides 19-29.

## Moderator Prep Checklist

### Before Session 2

- Prepare `~/.claude/skills/` demo skill or confirm at least one existing skill is available.
- Prepare hook scripts as separate files, not inline shell JSON.
- Confirm `jq` or Python JSON parsing works in the shell used for hooks.
- Prepare Playwright MCP or one screenshot/video fallback.
- Prepare NotebookLM notebook before the session; do not index sources live.

### Before Session 3

- Confirm `claude --version` and login state.
- Confirm `codex --version`; only run Codex Swarm if auth/plugin are verified.
- Confirm `devil-advocate-swarms` plugin or prepare static transcript/screenshot fallback.
- Prepare `~/.claude/skills/broken-greeter/SKILL.md` before Demo 3.7.
- Set explicit budget caps for any headless/autonomous command.
- Do not show `claude setup-token` output on screen.
- Keep Telegram Bridge skipped unless it is pre-configured and already tested.

## Remaining Risks

- Live plugin availability remains the biggest uncertainty. The written fallback path is good enough, but a production workshop should run the plugin preflight on the moderator machine.
- Session 3 still has more possible demos than time. Treat 3.2, 3.4, and Telegram as optional if discussion or debugging runs long.
- Some older resource files outside the main module/demo/exercise path may still contain legacy plugin/skill examples and should be cleaned in a later consistency pass.

## Recommendation

Run Session 2 as a controlled ecosystem lab. Run Session 3 as a curated advanced showcase with one strong security demo and the capstone preserved. Do not try to prove every advanced plugin live in one sitting.
