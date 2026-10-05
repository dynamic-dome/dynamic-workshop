#!/usr/bin/env python
r"""secure-diff-gate.py -- PreToolUse hook (matcher "Write|Edit"): block writes to protected paths.

jq-free variant for machines that have Python but neither jq nor Git Bash.

Contract (official hooks reference):
  - Claude Code sends the event as JSON on stdin; the target is in tool_input.file_path
    (absolute, with backslashes on Windows).
  - Exit 2 = BLOCK: the file is not written, and stderr is shown to Claude as the reason.
  - Exit 0 = no objection: the normal permission flow decides.
  - Any OTHER exit code does NOT block. An uncaught Python error ends with 1, so the write would
    happen anyway. That is why every failure in here ends with 2.
  - Protected: .env / *.pem / secrets/ / credentials, in any letter case (Windows and the default
    macOS file system treat .ENV and .env as the same file).

Limits: the matcher "Write|Edit" does not see shell commands. `echo X > .env` through the Bash or
PowerShell tool goes past this gate. Add deny rules (permissions.deny) or a sandbox for a hard limit.

Register in .claude/settings.json (matcher "Write|Edit"):
  "command": "python \"$HOME/.claude/hooks/secure-diff-gate.py\""
  (macOS / Linux: python3)

$HOME expands in Git Bash and in PowerShell, the two shells Claude Code runs hook commands in on
Windows. The cmd form %USERPROFILE%\... expands in neither: Python then cannot open the file, ends
with 2, and every write is blocked.
"""

import json
import re
import sys

BLOCK = 2
PROTECTED = re.compile(r"(\.env|\.pem|secrets/|credentials)", re.IGNORECASE)


def say(message: str) -> None:
    # Claude Code reads UTF-8; a Windows console stream would write cp1252.
    sys.stderr.buffer.write((message + "\n").encode("utf-8"))


def main() -> int:
    # Read bytes: Claude Code sends UTF-8, while sys.stdin on Windows decodes cp1252.
    payload = json.loads(sys.stdin.buffer.read())
    tool_input = payload.get("tool_input") or {}
    # Newer Claude Code nests the path under tool_input.file_path; older/demo payloads use a top-level
    # file_path or path. First non-empty wins.
    path = tool_input.get("file_path") or payload.get("file_path") or payload.get("path") or ""
    # Windows delivers absolute backslash paths (C:\project\secrets\x): normalise before matching "secrets/".
    path = path.replace("\\", "/")

    if PROTECTED.search(path):
        say(f"BLOCKED: write to protected path: {path}")
        return BLOCK

    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception:  # noqa: BLE001 - fail closed: input that cannot be read must not let the write through
        say("BLOCKED: secure-diff-gate could not read the hook input - blocking to stay safe.")
        code = BLOCK
    sys.exit(code)
