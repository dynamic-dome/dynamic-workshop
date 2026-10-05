#!/bin/bash
# secure-diff-gate.sh - PreToolUse hook (matcher "Write|Edit"): block writes to protected paths.
#
# Contract (official hooks reference):
#   - Claude Code sends the event as JSON on stdin; the target is in tool_input.file_path
#     (absolute, with backslashes on Windows).
#   - exit 2 = BLOCK: the file is not written, and stderr is shown to Claude as the reason.
#   - exit 0 = no objection: the normal permission flow decides.
#   - Any OTHER exit code (1, 127, ...) does NOT block: the write happens anyway. That is why this
#     script decides every branch itself and never lets a failing tool end it.
#   - Protected: .env / *.pem / secrets/ / credentials, in any letter case (Windows and the default
#     macOS file system treat .ENV and .env as the same file).
#
# Limits: the matcher "Write|Edit" does not see shell commands. `echo X > .env` through the Bash or
# PowerShell tool goes past this gate. Add deny rules (permissions.deny) or a sandbox for a hard limit.
#
# Register in .claude/settings.json (matcher "Write|Edit"):
#   "command": "bash ~/.claude/hooks/secure-diff-gate.sh"
#
# Windows: run via Git Bash (jq required). No jq? Use secure-diff-gate.py instead.

INPUT=$(cat)

# Fail closed: if the input cannot be read (no jq, no JSON, empty, not an object), block instead of allowing
# the write. jq would turn `null.tool_input` into null without complaint, hence the explicit type checks.
READ_PATH='if type != "object" then error("hook input is not a JSON object") else
  (.tool_input.file_path // .file_path // .path // "") | if type == "string" then . else error("path is not a string") end
end'
if ! FILE=$(printf '%s' "$INPUT" | jq -er "$READ_PATH" 2>/dev/null); then
  echo "BLOCKED: secure-diff-gate could not read the hook input (is jq installed?) - blocking to stay safe." >&2
  exit 2
fi

# Windows delivers absolute backslash paths (C:\project\secrets\x): normalise before matching "secrets/".
FILE="${FILE//\\//}"

# Matched by bash itself, so a missing grep cannot turn the gate off either.
shopt -s nocasematch
if [[ "$FILE" =~ (\.env|\.pem|secrets/|credentials) ]]; then
  echo "BLOCKED: write to protected path: $FILE" >&2
  exit 2
fi

exit 0
