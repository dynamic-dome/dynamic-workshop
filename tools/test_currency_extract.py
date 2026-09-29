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


DEPRECATIONS = """
## Model status

| API model name             | Current state | Deprecated        | Tentative retirement date          |
| :------------------------- | :------------ | :---------------- | :--------------------------------- |
| claude-opus-5-5            | Active        | N/A               | Not sooner than September 22, 2027 |
| claude-haiku-4-5-20251001  | Active        | N/A               | Not sooner than October 15, 2026   |
| claude-opus-4-1-20250805   | Retired       | June 5, 2026      | August 5, 2026                     |

## History

| Retirement date | Deprecated model | Replacement |
| --- | --- | --- |
| claude-3-opus | x | y |
"""

CANON = """# Kanon

Geprüft: 2026-09-29 · CLI 2.1.284

| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |
|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | `claude-opus-5-5` | `opus` | Opus | Active | Not sooner than September 22, 2027 | 1M | 4 | 20 | Default |

## Quellen

- Doku: https://code.claude.com/docs/en/cli-reference.md
- Doku: https://platform.claude.com/docs/en/about-claude/model-deprecations.md
- CLI-Version: https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- Changelog: https://code.claude.com/docs/en/changelog.md
"""


def test_parse_date_handles_retirement_texts():
    assert cx.parse_date("Not sooner than October 15, 2026") == dt.date(2026, 10, 15)
    assert cx.parse_date("August 5, 2026") == dt.date(2026, 8, 5)
    assert cx.parse_date("To be announced") is None
    assert cx.parse_date("N/A") is None


def test_parse_deprecations_reads_only_the_status_table():
    rows = cx.parse_deprecations(DEPRECATIONS)
    assert sorted(rows) == ["claude-haiku-4-5-20251001", "claude-opus-4-1-20250805", "claude-opus-5-5"]
    assert rows["claude-opus-4-1-20250805"].status == "Retired"
    assert rows["claude-haiku-4-5-20251001"].retirement == "Not sooner than October 15, 2026"


def test_parse_aliases_and_permission_modes():
    aliases = cx.parse_aliases("| Model alias | Behavior |\n| - | - |\n| **`default`** | x |\n| **`sonnet[1m]`** | y |\n")
    assert aliases == {"default", "sonnet[1m]"}
    modes = cx.parse_permission_modes(
        "| Mode | x |\n| - | - |\n| `default` | a |\n| [`plan`](#plan-mode) | b |\n"
        "| `default`, `acceptEdits` | c |\n| `--flag` | d |\n",
        "| `--permission-mode` | Accepts `default`, `plan`, or `manual` | `claude --permission-mode plan` |\n"
        "| `claude` | start |\n",
    )
    assert modes == {"default", "plan", "acceptEdits", "manual"}


def test_canon_header_models_and_sources():
    assert cx.parse_canon_header(CANON) == (dt.date(2026, 9, 29), "2.1.284")
    [model] = cx.parse_canon_models(CANON)
    assert (model.model_id, model.alias, model.tier, model.retirement) == (
        "claude-opus-5-5", "opus", "Opus", "Not sooner than September 22, 2027")
    sources = cx.parse_canon_sources(CANON)
    assert len(sources["Doku"]) == 2 and len(sources["CLI-Version"]) == 1 and len(sources["Changelog"]) == 1


def test_canon_parsers_fail_closed():
    with pytest.raises(ValueError):
        cx.parse_canon_header("# Kanon ohne Prüfdatum\n")
    with pytest.raises(ValueError):
        cx.parse_canon_models("# Kanon ohne Tabelle\n")
    with pytest.raises(ValueError):
        cx.parse_canon_sources(CANON.replace("- Changelog: https://code.claude.com/docs/en/changelog.md\n", ""))


def test_changelog_since_returns_only_newer_entries():
    text = (
        '<Update label="2.1.286" description="a">\n  * Added --foo\n  * Fixed bar\n</Update>\n'
        '<Update label="2.1.285" description="b">\n  * Removed --baz\n</Update>\n'
        '<Update label="2.1.284" description="c">\n  * Old entry\n</Update>\n'
    )
    assert cx.changelog_since(text, "2.1.285") == [("2.1.286", "Added --foo"), ("2.1.286", "Fixed bar")]
    assert cx.changelog_since(text, "2.1.286") == []
    with pytest.raises(ValueError):
        cx.changelog_since(text, "2.1.200")


def test_model_family_version_ignores_date_suffix():
    assert cx.model_family_version("claude-haiku-4-5-20251001") == ("haiku", (4, 5))
    assert cx.model_family_version("claude-opus-5-5") == ("opus", (5, 5))
    assert cx.model_family_version("claude-fable-5") == ("fable", (5,))


def test_exists_in_docs_respects_identifier_boundaries():
    union = "Use `--max-turns-total` or `ANTHROPIC_MODEL`. See claude-haiku-4-5-20251001."
    assert not cx.exists_in_docs("flag", "--max-turns", union, set(), set())
    assert cx.exists_in_docs("env", "ANTHROPIC_MODEL", union, set(), set())
    assert not cx.exists_in_docs("model_id", "claude-haiku-4-5", union, set(), set())
    assert cx.exists_in_docs("alias", "opus", "", {"opus"}, set())
    assert cx.exists_in_docs("permission_mode", "plan", "", set(), {"plan"})


def test_doc_identifiers_collects_flags_and_env():
    ids = cx.doc_identifiers("`--bare` and `--max-turns`; set ANTHROPIC_API_KEY or CLAUDE_CODE_USE_BEDROCK")
    assert ids == {"flag": {"--bare", "--max-turns"}, "env": {"ANTHROPIC_API_KEY", "CLAUDE_CODE_USE_BEDROCK"}}


def test_normalize_cockpit_drops_provenance_and_crlf():
    course = "<!doctype html>\n<p>x</p>\n"
    live = "<!doctype html>\r\n<!-- Quelle: dynamic_workshop/resources/claude-code-workshop-ui.html · Stand 2026-09-29 -->\r\n<p>x</p>\r\n"
    assert cx.normalize_cockpit(course) == cx.normalize_cockpit(live)


def test_parse_exceptions_requires_a_reason():
    assert cx.parse_exceptions("# Kommentar\n\n--orphan | git-Flag in Übung 1.3\n") == {"--orphan": "git-Flag in Übung 1.3"}
    with pytest.raises(ValueError):
        cx.parse_exceptions("--orphan\n")
    with pytest.raises(ValueError):
        cx.parse_exceptions("--orphan | ok\n")


def test_gegenprobe_finds_known_wrong_identifiers_in_old_course_text():
    old_cheatsheet = (ROOT / "tools/fixtures/currency/cheatsheet-before-ee52d54.md").read_text(encoding="utf-8")
    hits, _ = cx.extract_course_hits("cheatsheet.md", old_cheatsheet)
    assert "CLAUDE_MODEL" in {h.value for h in hits if h.kind == "env"}
    assert not cx.exists_in_docs("env", "CLAUDE_MODEL", "| `ANTHROPIC_MODEL` | model |", set(), set())

    old_block1 = (ROOT / "tools/fixtures/currency/block-1-before-sweep.md").read_text(encoding="utf-8")
    hits, _ = cx.extract_course_hits("block-1.md", old_block1)
    assert "claude-opus-4-8" in {h.value for h in hits if h.kind == "model_id"}
