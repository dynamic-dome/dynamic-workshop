#!/bin/bash
# secure-diff-gate.sh — PreToolUse hook: block writes to protected paths.
#
# Workshop Demo 2.2b ("Secure Diff Gate"). This is the pre-prepared fallback
# referenced in resources/demos/block-2-demos.md, in case the inline-JSON hook
# quoting breaks live.
#
# Contract:
#   - Reads the PreToolUse hook payload as JSON on stdin.
#   - Exits 1 (BLOCK) if the target path matches a protected pattern
#     (.env / *.pem / secrets/ / credentials).
#   - Exits 0 (ALLOW) for any other path.
#
# Register in .claude/settings.json (matcher "Write|Edit"):
#   "command": "bash ~/.claude/hooks/secure-diff-gate.sh"
#
# Windows: run via Git Bash (jq required). No jq? Use secure-diff-gate.py instead.

set -euo pipefail

INPUT=$(cat)

# Newer Claude Code nests the path under tool_input.file_path; older/demo
# payloads use a top-level file_path or path. Check all three, first non-empty wins.
FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .file_path // .path // ""')

if printf '%s' "$FILE" | grep -qE '(\.env|\.pem|secrets/|credentials)'; then
  echo "BLOCKED: write to protected path: $FILE" >&2
  exit 1
fi

exit 0
