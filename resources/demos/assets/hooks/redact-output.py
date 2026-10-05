# redact-output.py - PostToolUse hook (matcher "Bash|PowerShell"): hide secrets from Claude in command output.
# tested asset: resources/demos/assets/hooks/redact-output.py
#
# Same behaviour as redact-output.sh, for machines without bash or jq.
# PostToolUse receives the finished result in tool_response (stdout, stderr, interrupted, isImage, ...).
# To change what Claude sees, print hookSpecificOutput.updatedToolOutput in the SAME shape.
# Limits: the command has already run, and PostToolUse fires only after a successful call.
# A command that ends with an error code goes to PostToolUseFailure; Claude sees its output unredacted.
import json
import re
import sys

SECRETS = re.compile(r"sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}")

try:
    # Read bytes: Claude Code sends UTF-8, while sys.stdin on Windows decodes cp1252.
    response = json.loads(sys.stdin.buffer.read())["tool_response"]
    stdout, stderr = response.get("stdout") or "", response.get("stderr") or ""
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        raise ValueError("output is not text")
except Exception:
    sys.exit(0)  # unreadable input: change nothing; a PostToolUse hook cannot block anyway

if not SECRETS.search(stdout + "\n" + stderr):
    sys.exit(0)  # nothing to hide: print nothing, Claude sees the original output

response["stdout"] = SECRETS.sub("[REDACTED]", stdout)
response["stderr"] = SECRETS.sub("[REDACTED]", stderr)
# json.dumps escapes everything outside ASCII, so the console encoding cannot damage the text.
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": response}}))
sys.exit(0)
