"""Extraction and parsing for the currency check (design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md)."""
import datetime as dt
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FENCE = "`" * 3


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cx = _load("currency_extract")


def values(text, kind):
    hits, _unparsed = cx.extract_course_hits("x.md", text)
    return sorted({h.value for h in hits if h.kind == kind})


def test_flags_after_a_claude_call_are_collected():
    assert values("claude -p --max-turns 3 --output-format json", "flag") == ["--max-turns", "--output-format"]


def test_shell_continuation_lines_are_joined():
    text = "claude --bare -p \"x\" \\\n  --max-budget-usd 0.50 \\\n  --output-format json\n"
    assert values(text, "flag") == ["--bare", "--max-budget-usd", "--output-format"]


def test_js_string_continuation_in_the_cockpit_is_joined():
    line = 'example: "claude --bare -p \\"x\\" \\\\\\n  --output-format json \\\\\\n  < diff.patch\\n\\n# B\\ngit log --oneline"'
    assert values(line, "flag") == ["--bare", "--output-format"]


def test_inline_code_starting_with_a_flag_is_collected():
    assert values("Pass `--metadata '{\"a\":1}'` to tag runs.", "flag") == ["--metadata"]


def test_foreign_flags_in_prose_css_and_pipes_are_ignored():
    text = (
        "Use git checkout --orphan here.\n"
        "  --accent-glow: #fff; color: var(--accent-glow);\n"
        "claude -p x | jq --raw-output .result\n"
        "cp ~/.claude/settings.json --target backup\n"
        "npx @anthropic-ai/claude-code --version-check\n"
    )
    assert values(text, "flag") == []


def test_camel_case_and_single_letter_flags_are_kept_whole():
    assert values("claude -p --allowedTools Read --x", "flag") == ["--allowedTools", "--x"]
    assert values("Use `--disallowedTools` and `--x`.", "flag") == ["--disallowedTools", "--x"]


def test_env_model_ids_aliases_and_modes():
    text = (
        "export ANTHROPIC_MODEL=x CLAUDE_CODE_OAUTH_TOKEN=y SLACK_BOT_TOKEN=z\n"
        "claude --model opus --permission-mode acceptEdits\n"
        "claude --model claude-opus-4-8 -p x\n"
        "model: sonnet\n"
        '{"model": "haiku", "defaultMode": "plan"}\n'
        "permissionMode: dontAsk\n"
        "Default model: the best one\n"
    )
    assert values(text, "env") == ["ANTHROPIC_MODEL", "CLAUDE_CODE_OAUTH_TOKEN"]
    assert values(text, "model_id") == ["claude-opus-4-8"]
    assert values(text, "alias") == ["haiku", "opus", "sonnet"]
    assert values(text, "permission_mode") == ["acceptEdits", "dontAsk", "plan"]


def test_hook_events_come_from_parsable_json_fences():
    text = (
        f"{FENCE}json\n"
        '{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command"}]}], "Stop": []}}\n'
        f"{FENCE}\n\n"
        f"{FENCE}json\n"
        "{ this is not json }\n"
        f"{FENCE}\n"
    )
    hits, unparsed = cx.extract_course_hits("x.md", text)
    assert sorted(h.value for h in hits if h.kind == "hook_event") == ["PreToolUse", "Stop"]
    assert unparsed == 1
    assert {h.line for h in hits if h.kind == "hook_event"} == {1}


def test_hits_carry_path_and_first_line_of_a_logical_line():
    hits, _ = cx.extract_course_hits("m/a.md", "intro\nclaude \\\n  --bare -p x\n")
    assert [(h.path, h.line, h.value) for h in hits] == [("m/a.md", 2, "--bare")]
