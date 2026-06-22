---
name: broken-greeter
# ---- THREE DELIBERATELY PLANTED PROBLEMS (Demo 3.7 — Troubleshooting) ----
# Problem 1: description is generic — no concrete trigger phrases, so the model
#            has nothing to match a user prompt against.
description: A skill for greeting.
# Problem 2: auto-invocation is switched off — the skill is registered and shows
#            up in /skills, but the model will never call it on its own.
disable-model-invocation: true
# Problem 3: paths filter that no real file can ever satisfy — even with the other
#            two fixed, this filter gates the skill out.
paths: ["never-match/**"]
---

# Greeter

Reply with a friendly greeting that uses the user's name.

<!--
The BODY is intentionally correct and functional. Only the metadata above is
broken. The demo fixes the three problems in the order the diagnostic trace
surfaces them:
  1. paths filter (delete the `paths:` line)             -> still does not fire
  2. disable-model-invocation: true -> false             -> still does not fire
  3. generic description -> add real trigger phrases      -> finally fires

For comparison, a FIXED description would read something like:
  description: Use when the user asks to greet someone or say hello by name —
               triggers on "greet", "say hi to", "welcome <name>".
-->
