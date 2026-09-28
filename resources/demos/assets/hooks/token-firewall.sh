#!/bin/bash
# token-firewall.sh - PostToolUse hook (matcher "Bash"): shrink noisy test output before Claude reads it.
# tested asset: resources/demos/assets/hooks/token-firewall.sh
#
# Replaces tool_response.stdout via hookSpecificOutput.updatedToolOutput (same Bash shape).
# stderr passes through unchanged: stripping error details can mislead Claude.
# Note: suppressOutput has no effect, and systemMessage only reaches the user, not Claude.

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // ""')

# Only touch test runs; everything else passes through untouched.
if ! printf '%s' "$COMMAND" | grep -qE '(npm test|pytest|jest|mocha)'; then
  exit 0
fi

printf '%s' "$INPUT" | jq '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    updatedToolOutput: (.tool_response | .stdout |= (
      [split("\n")[] | select(test("FAIL|ERROR|Error|passed|failed|Summary"))]
      | .[-50:] | join("\n")
      | . + "\n--- [Token Firewall: passing-test lines removed; failures and summary kept] ---"
    ))
  }
}'
exit 0
