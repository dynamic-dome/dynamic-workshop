#!/bin/bash
# safety-check.sh - PreToolUse hook (matcher "Bash|PowerShell"): block destructive shell commands.
# tested asset: resources/demos/assets/hooks/safety-check.sh
#
# Contract (official hooks reference):
#   - Claude Code sends the event as JSON on stdin; the shell command is in tool_input.command
#     (the Bash and the PowerShell tool use the same field).
#   - exit 2 = BLOCK: the command does not run, and stderr is shown to Claude as the reason.
#   - exit 0 = no objection: the normal permission flow decides.
#   - Any OTHER exit code (1, 127, ...) does NOT block: the command runs anyway.
#   - On Windows, shell commands usually run through the PowerShell tool. A hook with
#     matcher "Bash" alone never fires there, so register it as "Bash|PowerShell".
#   - The patterns are examples, not complete protection: combine hooks with permission
#     rules and a sandbox.

INPUT=$(cat)

# Fail closed: if the input cannot be read, block instead of silently allowing everything.
# Readable means: a JSON object whose command, if present, is a string. jq would turn "null" into an
# empty command without complaint, so the type is checked explicitly.
READ_COMMAND='if type != "object" then error("hook input is not a JSON object") else
  (.tool_input.command // "") | if type == "string" then . else error("command is not a string") end
end'
if ! COMMAND=$(printf '%s' "$INPUT" | jq -er "$READ_COMMAND" 2>/dev/null); then
  echo "SAFETY HOOK: could not read the hook input (is jq installed?) - blocking to stay safe." >&2
  exit 2
fi

# Dangerous patterns (extended regex, case-insensitive); the last four are PowerShell and cmd
DANGEROUS_PATTERNS=(
  'rm[[:space:]]+-rf'
  'git push.*--force'
  'git push.*[[:space:]]-f([[:space:]]|$)'
  'DROP TABLE'
  'truncate.*--yes'
  'mkfs\.'
  'dd[[:space:]]+if=.*of=/dev/'
  '> /dev/sd'
  '(^|[^[:alnum:]-])(Remove-Item|rm|ri|del|erase|rmdir|rd)[[:space:]].*-Recurse'
  '(^|[^[:alnum:]-])(rd|rmdir)[[:space:]]+/s'
  'Format-Volume'
  'Clear-Disk'
)

for PATTERN in "${DANGEROUS_PATTERNS[@]}"; do
  if printf '%s' "$COMMAND" | grep -qiE -- "$PATTERN"; then
    echo "SAFETY HOOK: potentially destructive command blocked." >&2
    echo "Command: $COMMAND" >&2
    echo "Pattern matched: $PATTERN" >&2
    echo "If this was intended, run it yourself outside Claude Code." >&2
    exit 2
  fi
done

# All checks passed - no objection
exit 0
