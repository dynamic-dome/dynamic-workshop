"""Behaviour tests for every Claude Code hook the course asks learners to copy.

Payloads follow the official hooks reference (code.claude.com/docs/en/hooks, checked 2026-09-28):
- PreToolUse input carries tool_name + tool_input (Bash: tool_input.command; Write: file_path + content;
  Edit: file_path + old_string + new_string). File paths are absolute, with backslashes on Windows.
- PostToolUse input adds tool_response (Bash: stdout, stderr, interrupted, isImage).
- Only exit 2 blocks. Any other non-zero exit is a non-blocking error: the action proceeds.
- PostToolUse replaces what Claude sees via hookSpecificOutput.updatedToolOutput in the tool's own shape.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "resources" / "demos" / "assets" / "hooks"
BASH = shutil.which("bash")
JQ = shutil.which("jq")
POWERSHELL = shutil.which("powershell.exe") or shutil.which("powershell")

needs_bash_jq = pytest.mark.skipif(BASH is None or JQ is None, reason="bash and jq are required")
needs_powershell = pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")

BLOCK = 2  # the only exit code that blocks a PreToolUse call


def pre_bash(command: str) -> dict:
    return {
        "session_id": "test",
        "cwd": "C:\\project",
        "permission_mode": "default",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command, "description": "test", "timeout": 120000},
        "tool_use_id": "toolu_test",
    }


def pre_write(file_path: str, content: str) -> dict:
    return {
        "session_id": "test",
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": content},
        "tool_use_id": "toolu_test",
    }


def pre_edit(file_path: str, old: str, new: str) -> dict:
    return {
        "session_id": "test",
        "hook_event_name": "PreToolUse",
        "tool_name": "Edit",
        "tool_input": {"file_path": file_path, "old_string": old, "new_string": new},
        "tool_use_id": "toolu_test",
    }


def post_bash(command: str, stdout: str, stderr: str = "") -> dict:
    return {
        "session_id": "test",
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "tool_response": {"stdout": stdout, "stderr": stderr, "interrupted": False, "isImage": False},
        "tool_use_id": "toolu_test",
    }


def run(script: Path, payload: dict) -> subprocess.CompletedProcess:
    if script.suffix == ".py":
        cmd = [sys.executable, str(script)]
    elif script.suffix == ".sh":
        cmd = [BASH, str(script)]
    elif script.suffix == ".ps1":
        cmd = [POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)]
    else:
        raise ValueError(script)
    return subprocess.run(
        cmd,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=60,
    )


def updated_output(result: subprocess.CompletedProcess) -> dict:
    data = json.loads(result.stdout)
    specific = data["hookSpecificOutput"]
    assert specific["hookEventName"] == "PostToolUse"
    return specific["updatedToolOutput"]


# --- secure-diff-gate (Demo 2.2b, PreToolUse Write|Edit) -------------------------------------------

SECURE_DIFF_GATE = [HOOKS / "secure-diff-gate.py", pytest.param(HOOKS / "secure-diff-gate.sh", marks=needs_bash_jq)]


@pytest.mark.parametrize("script", SECURE_DIFF_GATE)
def test_secure_diff_gate_blocks_windows_backslash_path_into_secrets(script):
    result = run(script, pre_write("C:\\project\\secrets\\panel-db.json", "{}"))

    assert result.returncode == BLOCK
    assert "BLOCKED" in result.stderr


@pytest.mark.parametrize("script", SECURE_DIFF_GATE)
def test_secure_diff_gate_allows_normal_absolute_windows_path(script):
    result = run(script, pre_write("C:\\project\\src\\access_control.py", "print('ok')"))

    assert result.returncode == 0


# --- safety-check (Exercise 2.2 + Demo 2.2, PreToolUse Bash) ---------------------------------------

SAFETY_CHECK = [
    pytest.param(HOOKS / "safety-check.sh", marks=needs_bash_jq),
    pytest.param(HOOKS / "safety-check.ps1", marks=needs_powershell),
]


@pytest.mark.parametrize("script", SAFETY_CHECK)
@pytest.mark.parametrize(
    "command",
    ["rm -rf /tmp/test-directory", "git push --force origin main", "psql -c 'DROP TABLE users'"],
)
def test_safety_check_blocks_destructive_bash_commands_with_exit_2(script, command):
    result = run(script, pre_bash(command))

    assert result.returncode == BLOCK
    assert "SAFETY HOOK" in result.stderr


@pytest.mark.parametrize("script", SAFETY_CHECK)
def test_safety_check_allows_harmless_command(script):
    result = run(script, pre_bash('echo "hello world"'))

    assert result.returncode == 0
    assert result.stderr.strip() == ""


@pytest.mark.parametrize("script", SAFETY_CHECK)
def test_safety_check_fails_closed_when_input_is_unreadable(script):
    """A safety gate that cannot read its input must not silently wave the call through."""
    cmd_result = subprocess.run(
        [BASH, str(script)] if script.suffix == ".sh"
        else [POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        input="this is not json",
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=60,
    )

    assert cmd_result.returncode == BLOCK


# --- sensitive-data-scanner (Bonus Exercise 3.8, PreToolUse Write|Edit) ----------------------------

SCANNER = pytest.param(HOOKS / "sensitive-data-scanner.sh", marks=needs_bash_jq)


@pytest.mark.parametrize("script", [SCANNER])
def test_scanner_blocks_api_key_in_write_content(script):
    result = run(script, pre_write("C:\\project\\config.py", 'API_KEY = "sk-' + "a" * 24 + '"'))

    assert result.returncode == BLOCK
    assert "BLOCKED" in result.stderr


@pytest.mark.parametrize("script", [SCANNER])
def test_scanner_blocks_card_number_in_edit_new_string(script):
    result = run(script, pre_edit("C:\\project\\notes.md", "card: TBD", "card: 4111 1111 1111 1111"))

    assert result.returncode == BLOCK


@pytest.mark.parametrize("script", [SCANNER])
def test_scanner_allows_clean_write(script):
    result = run(script, pre_write("C:\\project\\README.md", "# Access panel notes\nNothing secret here."))

    assert result.returncode == 0


# --- redact-output (Module 2.2 advanced output, PostToolUse Bash) ----------------------------------

REDACT = pytest.param(HOOKS / "redact-output.sh", marks=needs_bash_jq)


@pytest.mark.parametrize("script", [REDACT])
def test_redact_output_replaces_secret_in_bash_stdout_with_bash_shape(script):
    secret = "sk-" + "b" * 24
    result = run(script, post_bash("cat .env", f"TOKEN={secret}\nMODE=dev\n", "warn: x"))

    assert result.returncode == 0
    replaced = updated_output(result)
    assert set(replaced) == {"stdout", "stderr", "interrupted", "isImage"}
    assert secret not in replaced["stdout"]
    assert "[REDACTED]" in replaced["stdout"]
    assert "MODE=dev" in replaced["stdout"]
    assert replaced["stderr"] == "warn: x"


@pytest.mark.parametrize("script", [REDACT])
def test_redact_output_stays_silent_without_secrets(script):
    result = run(script, post_bash("ls", "a.txt\nb.txt\n"))

    assert result.returncode == 0
    assert result.stdout.strip() == ""


# --- token-firewall (Bonus Exercise 2.6, PostToolUse Bash) -----------------------------------------

FIREWALL = pytest.param(HOOKS / "token-firewall.sh", marks=needs_bash_jq)


@pytest.mark.parametrize("script", [FIREWALL])
def test_token_firewall_keeps_only_failures_and_summary_for_test_runs(script):
    noisy = "\n".join(f"tests/test_{i}.py::test_ok PASSED" for i in range(300))
    stdout = noisy + "\ntests/test_x.py::test_door FAILED\n=== 1 failed, 300 passed in 2.1s ==="
    result = run(script, post_bash("pytest -v", stdout))

    assert result.returncode == 0
    replaced = updated_output(result)
    assert set(replaced) == {"stdout", "stderr", "interrupted", "isImage"}
    assert "test_door FAILED" in replaced["stdout"]
    assert "1 failed, 300 passed" in replaced["stdout"]
    assert "test_0.py::test_ok PASSED" not in replaced["stdout"]
    assert len(replaced["stdout"]) < len(stdout) / 10


@pytest.mark.parametrize("script", [FIREWALL])
def test_token_firewall_leaves_non_test_commands_alone(script):
    result = run(script, post_bash("ls -la", "total 0\n"))

    assert result.returncode == 0
    assert result.stdout.strip() == ""


# --- live course content ----------------------------------------------------------------------------

ASSET_MARKER = re.compile(r"tested asset: (resources/demos/assets/hooks/[\w.-]+)")
FENCE = re.compile(r"^```[\w-]*\n(.*?)^```", re.S | re.M)
LIVE_MD = [
    p for p in (ROOT / "resources").rglob("*.md")
    if not p.relative_to(ROOT).as_posix().startswith("resources/media/")
]


# --- guard: known-wrong hook idioms must not come back ----------------------------------------------

WRONG_IDIOMS = {
    "reads a top-level field instead of tool_input/tool_response":
        re.compile(r"jq -r '?\.(command|content|new_content|toolOutput|file_path|path)\b"),
    "python reads top-level 'command'": re.compile(r"\bd\.get\(['\"]command['\"]"),
    "PowerShell reads top-level command": re.compile(r"\$data\.command\b"),
    "claims any non-zero exit blocks": re.compile(
        r"non-zero = block|non-zero exit code is interpreted as a \*\*block|exit 1\s*#\s*Exit 1 to BLOCK"
        r"|exiting with a non-zero code|first one to exit non-zero blocks|`exit 1` blocks",
        re.I,
    ),
    "uses suppressOutput as if it did something": re.compile(r"\"?suppressOutput\"?\s*:\s*true"),
    "flat skill-frontmatter hook (handler without nested hooks list)":
        re.compile(r"- matcher: \"?\w+\"?\s*\n\s+type: command"),
}
HOOK_GROUP_KEYS = {"matcher", "hooks"}
HOOK_HANDLER_KEYS = {
    "type", "if", "timeout", "statusMessage", "once",                      # common
    "command", "args", "async", "asyncRewake", "shell",                   # command
    "url", "headers", "allowedEnvVars",                                   # http
    "server", "tool", "input",                                            # mcp_tool
    "prompt", "model", "continueOnBlock",                                 # prompt / agent
}
LIVE_FILES = LIVE_MD + [ROOT / "resources" / "claude-code-workshop-ui.html", ROOT / "agents" / "workshop-mentor.md"]


def find_wrong_idioms(text: str) -> list:
    return [label for label, rx in WRONG_IDIOMS.items() if rx.search(text)]


def hook_config_problems(text: str) -> list:
    problems = []
    for block in re.findall(r"^```json\n(.*?)^```", text, re.S | re.M):
        try:
            data = json.loads(block)
        except ValueError:
            continue  # placeholders like [...] - not a full config
        hooks = data.get("hooks") if isinstance(data, dict) else None
        if not isinstance(hooks, dict):
            continue
        for event, groups in hooks.items():
            for group in groups:
                extra = set(group) - HOOK_GROUP_KEYS
                if extra:
                    problems.append(f"{event}: matcher group has {sorted(extra)} (belongs on the handler?)")
                for handler in group.get("hooks", []):
                    unknown = set(handler) - HOOK_HANDLER_KEYS
                    if unknown:
                        problems.append(f"{event}: unknown handler field(s) {sorted(unknown)}")
    return problems


def test_guard_catches_the_old_mistakes():
    """Negative control: the idioms the course taught before 2026-09-28 must be flagged."""
    old = (
        "COMMAND=$(echo \"$INPUT\" | jq -r '.command // \"\"')\n"
        "    exit 1   # Exit 1 to BLOCK the command\n"
        "Exit code 0 = allow, non-zero = block.\n"
        "    - matcher: Bash\n      type: command\n"
        '```json\n{"hooks": {"PreToolUse": [{"matcher": "Bash", "if": "Bash(git *)", "hooks": []}]}}\n```\n'
    )
    assert len(find_wrong_idioms(old)) >= 3
    assert hook_config_problems(old)


@pytest.mark.parametrize("path", LIVE_FILES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_live_course_content_has_no_wrong_hook_idioms(path):
    text = path.read_text(encoding="utf-8")

    assert find_wrong_idioms(text) == []
    assert hook_config_problems(text) == []


# --- course snippets must equal the tested assets ---------------------------------------------------

def _normalise(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


# Copyable assets and the one chapter each lives in (the library keeps every snippet once; secure-diff-gate is
# copied as a file, not pasted, and has its own behaviour tests above).
SNIPPET_HOME = {
    "safety-check.sh": "s2-08-hook-einrichten.md",
    "safety-check.ps1": "s2-08-hook-einrichten.md",
    "redact-output.sh": "s2-10-hook-ausgaben.md",
    "token-firewall.sh": "s2-10-hook-ausgaben.md",
    "sensitive-data-scanner.sh": "s3-11-datenschutz-und-compliance.md",
}


def test_every_marked_course_snippet_matches_its_tested_asset():
    homes = {}
    for md in LIVE_MD:
        for block in FENCE.findall(md.read_text(encoding="utf-8")):
            marker = ASSET_MARKER.search(block)
            if not marker:
                continue
            asset = ROOT / marker.group(1)
            assert asset.exists(), f"{md.name}: marker points to missing asset {marker.group(1)}"
            assert _normalise(block) == _normalise(asset.read_text(encoding="utf-8")), (
                f"{md.relative_to(ROOT)}: snippet drifted from {marker.group(1)}"
            )
            homes.setdefault(asset.name, []).append(md.name)

    assert homes == {name: [home] for name, home in SNIPPET_HOME.items()}, homes
