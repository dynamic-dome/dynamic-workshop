#!/usr/bin/env python
"""secure-diff-gate.py -- PreToolUse hook: block writes to protected paths.

Workshop Demo 2.2b ("Secure Diff Gate"). jq-free fallback for Windows boxes
that have Python but not jq / Git Bash.

Contract:
  - Reads the PreToolUse hook payload as JSON on stdin.
  - Exits 1 (BLOCK) if the target path matches a protected pattern
    (.env / *.pem / secrets/ / credentials).
  - Exits 0 (ALLOW) for any other path.

Register in .claude/settings.json (matcher "Write|Edit"):
  "command": "python %USERPROFILE%\\.claude\\hooks\\secure-diff-gate.py"
  (Git Bash / macOS / Linux: "python ~/.claude/hooks/secure-diff-gate.py")

Note: use "python" on Windows (python3 usually does not exist there).
"""

import json
import re
import sys

PROTECTED = re.compile(r"(\.env|\.pem|secrets/|credentials)")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Malformed/empty payload: fail open so a parser hiccup never wedges the agent.
        return 0

    # Newer Claude Code nests the path under tool_input.file_path; older/demo
    # payloads use a top-level file_path or path. First non-empty wins.
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or payload.get("file_path") or payload.get("path") or ""

    if PROTECTED.search(path):
        sys.stderr.write(f"BLOCKED: write to protected path: {path}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
