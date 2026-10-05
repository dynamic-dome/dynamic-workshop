# token-firewall.py - PostToolUse hook (matcher "Bash|PowerShell"): shrink noisy test output before Claude reads it.
# tested asset: resources/demos/assets/hooks/token-firewall.py
#
# Same behaviour as token-firewall.sh, for machines without bash or jq.
# Replaces tool_response.stdout via hookSpecificOutput.updatedToolOutput (same shape as the input).
# stderr passes through unchanged: stripping error details can mislead Claude.
# Limit: PostToolUse fires only after a successful call. A test run that ends with an error code
# goes to PostToolUseFailure and reaches Claude at full length.
import json
import re
import sys

TEST_RUN = re.compile(r"npm test|pytest|jest|mocha")
KEEP = re.compile(r"FAIL|ERROR|Error|passed|failed|Summary")
NOTE = "--- [Token Firewall: passing-test lines removed; failures and summary kept] ---"

try:
    # Read bytes: Claude Code sends UTF-8, while sys.stdin on Windows decodes cp1252.
    payload = json.loads(sys.stdin.buffer.read())
    command = payload["tool_input"].get("command") or ""
    response = payload["tool_response"]
    stdout = response.get("stdout") or ""
    if not isinstance(command, str) or not isinstance(stdout, str):
        raise ValueError("command or output is not text")
except Exception:
    sys.exit(0)  # unreadable input: change nothing; a PostToolUse hook cannot block anyway

# Only touch test runs; everything else passes through untouched.
if not TEST_RUN.search(command):
    sys.exit(0)

kept = [line for line in stdout.split("\n") if KEEP.search(line)][-50:]
response["stdout"] = "\n".join(kept) + "\n" + NOTE
# json.dumps escapes everything outside ASCII, so the console encoding cannot damage the text.
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": response}}))
sys.exit(0)
