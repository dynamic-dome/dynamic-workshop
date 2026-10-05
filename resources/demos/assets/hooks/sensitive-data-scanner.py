# sensitive-data-scanner.py - PreToolUse hook (matcher "Write|Edit"): block sensitive data in file writes.
# tested asset: resources/demos/assets/hooks/sensitive-data-scanner.py
#
# Same checks as sensitive-data-scanner.sh, for machines without bash or jq.
# exit 2 blocks the write; any other non-zero exit code would let it through.
import json
import re
import sys

PATTERN = re.compile(
    r"[0-9]{3}-[0-9]{2}-[0-9]{4}"
    r"|[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}"
    r"|(sk-|pk_)[A-Za-z0-9]{20,}"
    r"|AKIA[A-Z0-9]{16}"
    r'|password\s*=\s*"[^"]+"',
    re.IGNORECASE,
)

# Fail closed: if the input cannot be read, block instead of silently allowing the write.
try:
    tool_input = json.load(sys.stdin)["tool_input"]
    content = tool_input.get("content") or tool_input.get("new_string") or ""
    if not isinstance(content, str):
        raise ValueError("content is not a string")
except Exception:
    print("SCANNER: could not read the hook input - blocking to stay safe.", file=sys.stderr)
    sys.exit(2)

if PATTERN.search(content):
    # Do not print the match itself: stderr goes to Claude as the block reason.
    print("BLOCKED: sensitive data pattern detected in the file content.", file=sys.stderr)
    print("Redact or remove it before writing (use an environment variable or a secret store).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
