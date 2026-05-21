# Final Gap Sweep - 2026-05-21

## Scope

Final consistency sweep after deck update and Session 2/3 dry run.

Checked:

- root onboarding files
- plugin manifest
- workshop command
- workshop skill
- workshop mentor agent
- session plan
- trainer notes
- deck audit
- dry-run report
- main module/demo/exercise files

## Findings Closed

### 1. Plugin manifest still claimed 14 modules

**Status:** fixed.

` .claude-plugin/plugin.json` still described the workshop as `14 modules (4+5+5)`, while the current curriculum is 17 modules across Block 1 = 5, Block 2 = 5, Block 3 = 7.

Changed to `17 modules (5+5+7)`.

### 1b. Plugin manifest used stale component arrays

**Status:** fixed.

`claude plugin validate .` rejected the manifest because `commands`, `agents`, and `skills` arrays were not valid for the current validator shape, and `skills[0]` pointed to `skills/workshop/SKILL.md` instead of the skill directory. The manifest now keeps metadata only; Claude discovers components from the standard `commands/`, `agents/`, and `skills/` directories.

### 2. Workshop skill frontmatter still used trigger phrases inside description

**Status:** fixed.

The main workshop skill now uses `when_to_use` for activation guidance instead of embedding trigger phrases in `description`.

### 3. Workshop skill advertised `/workshop guide next`

**Status:** fixed.

The skill behavior says the trainer can type `next` while already in guide mode. The overview previously advertised `/workshop guide next`, which looks like a real command/module route but is not a module ID. The overview now says: `type "next" in guide mode`.

### 4. Mentor frontmatter used legacy `allowed_tools`

**Status:** fixed during dry run.

`agents/workshop-mentor.md` now uses `tools`.

### 5. Session plan did not mention new slide ranges or Demo 3.6/3.7

**Status:** fixed during dry run.

Session 2 opener references slides 12-18, Session 3 opener references slides 19-29, and Session 3 lists `Module 3.6 + Demo 3.6` plus `Module 3.7 + Demo 3.7`.

## Remaining Non-Blocking Notes

- `resources/deck-audit-2026-05-21.md` intentionally mentions the old 112-slide index as historical context.
- `resources/dry-run-session-2-3-2026-05-21.md` intentionally mentions `allowed_tools` as a before/after finding.
- Some generated/static artifacts such as `resources/workshop-learning-dashboard.html` may still contain older illustrative snippets, but they are not part of the current live trainer path.
- A later polish pass could make the old and new slides visually identical, but the current deck already renders cleanly and covers the missing 17-module visual layer.
- `claude plugin validate .` now passes with a warning that root `CLAUDE.md` is project context, not plugin-shipped context. This is expected for this repo because `CLAUDE.md` is also the local workshop project guide.
- The currently installed Claude plugin copy is stale: `claude plugin details dynamic-workshop` still reports `13 modules` and two `workshop` skill entries. Do not treat that as repo truth; reinstall/update the plugin from the fixed project after commit.

## Recommendation

The remaining work should move from consistency cleanup to operational preflight on the actual moderator machine:

1. verify installed plugins and skills
2. prepare hook scripts as files
3. prepare NotebookLM notebook and Playwright fallback
4. decide which Session 3 advanced demos are live vs. discussion
5. reinstall or update the local `dynamic-workshop` Claude plugin so runtime metadata matches this repo
