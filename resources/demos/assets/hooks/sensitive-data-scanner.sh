#!/bin/bash
# sensitive-data-scanner.sh - PreToolUse hook (matcher "Write|Edit"): block sensitive data in file writes.
# tested asset: resources/demos/assets/hooks/sensitive-data-scanner.sh
#
# Write sends the new file text as tool_input.content, Edit sends it as tool_input.new_string.
# exit 2 blocks the write; any other non-zero exit code would let it through.

INPUT=$(cat)

# Fail closed: if the input cannot be read, block instead of silently allowing the write.
# Readable means a JSON object: jq would turn "null" into empty content without complaint.
READ_CONTENT='if type != "object" then error("hook input is not a JSON object") else
  .tool_input.content // .tool_input.new_string // ""
end'
if ! CONTENT=$(printf '%s' "$INPUT" | jq -er "$READ_CONTENT" 2>/dev/null); then
  echo "SCANNER: could not read the hook input (is jq installed?) - blocking to stay safe." >&2
  exit 2
fi

# Adapt to your domain (card reader formats, internal IP ranges, ...). grep -E has no \d: use [0-9].
PATTERNS='([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(sk-|pk_)[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|password[[:space:]]*=[[:space:]]*"[^"]+")'

if printf '%s' "$CONTENT" | grep -qiE -- "$PATTERNS"; then
  # Do not echo the match itself: stderr goes to Claude as the block reason.
  echo "BLOCKED: sensitive data pattern detected in the file content." >&2
  echo "Redact or remove it before writing (use an environment variable or a secret store)." >&2
  exit 2
fi

exit 0
