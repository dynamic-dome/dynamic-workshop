#!/bin/bash
# redact-output.sh - PostToolUse hook (matcher "Bash"): hide secrets from Claude in command output.
# tested asset: resources/demos/assets/hooks/redact-output.sh
#
# PostToolUse receives the finished result in tool_response (Bash: stdout, stderr, interrupted, isImage).
# To change what Claude sees, print hookSpecificOutput.updatedToolOutput in the SAME shape;
# a plain string is ignored for built-in tools. The command itself has already run.

INPUT=$(cat)
SECRETS='(sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})'

TEXT=$(printf '%s' "$INPUT" | jq -r '.tool_response | (.stdout // "") + "\n" + (.stderr // "")')
if ! printf '%s' "$TEXT" | grep -qE -- "$SECRETS"; then
  exit 0   # nothing to hide: print nothing, Claude sees the original output
fi

printf '%s' "$INPUT" | jq --arg re "$SECRETS" '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    updatedToolOutput: (.tool_response | (.stdout, .stderr) |= gsub($re; "[REDACTED]"))
  }
}'
exit 0
