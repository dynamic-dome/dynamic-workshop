"""Guard for the CI-auth lesson (Module 3.6, cockpit S4.4/S4.5).

Source of truth: code.claude.com/docs/en/authentication.md and headless.md (fetched 2026-09-29) plus
`claude --help` 2.1.284. `claude setup-token` prints a subscription token that belongs in
`CLAUDE_CODE_OAUTH_TOKEN`; `--bare` never reads it and authenticates only via `ANTHROPIC_API_KEY` or an
`apiKeyHelper`. Until 2026-09-29 the course combined the two, which does not authenticate (review H-10).
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
COCKPIT = ROOT / "resources" / "claude-code-workshop-ui.html"
LIVE_MD = [
    p for p in (ROOT / "resources").rglob("*.md")
    if not p.relative_to(ROOT).as_posix().startswith("resources/media/")
]
LIVE_FILES = LIVE_MD + [COCKPIT, ROOT / "agents" / "workshop-mentor.md"]

WRONG_CLAIMS = {
    "env var CLAUDE_CODE_TOKEN does not exist (it is CLAUDE_CODE_OAUTH_TOKEN)": re.compile(r"\bCLAUDE_CODE_TOKEN\b"),
    "setup-token output is not an ANTHROPIC_API_KEY": re.compile(r"exports? it as `?ANTHROPIC_API_KEY"),
    "setup-token cannot be combined with --bare": re.compile(r"setup-token`? and combine[^\n]*--bare"),
    "no 'manage tokens' command exists": re.compile(r"manage tokens", re.I),
    "placeholder env names are read by nothing": re.compile(r"\b[A-Z_]*CREDENTIAL_PLACEHOLDER\b"),
    "env var CLAUDE_MODEL does not exist (it is ANTHROPIC_MODEL)": re.compile(r"\bCLAUDE_MODEL\b"),
    # cli-reference.md documents `--max-turns` (print mode only); `claude --help` just does not list it.
    "denies the documented --max-turns flag": re.compile(
        r"no (hard |separate )?turn.?(limit|cap).?flag|keine harte Turn-Grenze|kein Hard-Turn-Limit"
        r"|Turn-Limit-Flag im CLI nicht mehr|einzige[^.]{0,40}Hard-Guard",
        re.I,
    ),
    # authentication.md: bare mode reads no federation profiles, so federation is not a --bare path.
    "claims --bare works with federation (path C)": re.compile(r"--bare` means path A or C|path A \(or C\)"),
}
FENCE = re.compile(r"^```[\w-]*\n(.*?)^```", re.S | re.M)
JS_EXAMPLE = re.compile(r'example:\s*"((?:[^"\\]|\\.)*)"')
BARE_INVOCATION = re.compile(r"\bclaude\b[^\n#]*?--bare\b")  # the flag on a claude call, not in a comment
OAUTH_CREDENTIAL = re.compile(r"CLAUDE_CODE_OAUTH_TOKEN\s*[:=]|claude_code_oauth_token\s*:|setup-token")
API_KEY_CREDENTIAL = re.compile(r"ANTHROPIC_API_KEY|apiKeyHelper|anthropic_api_key")


def find_wrong_claims(text: str) -> list:
    return [label for label, rx in WRONG_CLAIMS.items() if rx.search(text)]


def snippets(path: Path, text: str) -> list:
    if path.suffix == ".html":
        return [raw.encode().decode("unicode_escape", errors="ignore") for raw in JS_EXAMPLE.findall(text)]
    return FENCE.findall(text)


def bare_without_api_key(path: Path, text: str) -> list:
    """Snippets that run `--bare` on the subscription token (or setup-token) with no API key in sight.

    Known limit: an API-key mention anywhere in the same snippet counts as "in sight", so a snippet that
    names the key only in a comment passes. Backslash line continuations are joined first, so a wrapped
    `claude \\` + `--bare` call is still seen as one invocation.
    """
    problems = []
    for snippet in snippets(path, text):
        joined = re.sub(r"\\\n\s*", " ", snippet)
        if BARE_INVOCATION.search(joined) and OAUTH_CREDENTIAL.search(joined) and not API_KEY_CREDENTIAL.search(joined):
            problems.append(snippet[:80])
    return problems


def test_guard_catches_the_old_mistakes():
    """Negative control: the CI-auth text the course taught before 2026-09-29 must be flagged."""
    old_module = (
        "- Set up CI authentication with `claude setup-token` and combine `--max-budget-usd` and `--bare`.\n"
        "At runtime CI exports it as `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_TOKEN`).\n"
        "- **Revoke old tokens** via `claude auth status` -> \"manage tokens\".\n"
        "| `CLAUDE_MODEL` | Set default model |\n"
        "```bash\nclaude --bare -p \"Review\" --max-budget-usd 0.50\n# once on the workstation:\nclaude setup-token\n```\n"
    )
    old_cockpit = (
        'example: "# CI-Runner mit allen 4 Bausteinen kombiniert:\\nclaude --bare -p \\"Review this diff\\" \\\\\\n'
        '  --output-format json\\n# Token-Einrichtung einmalig auf der Workstation:\\nclaude setup-token",\n'
        'example: "env:\\n    CLAUDE_CI_CREDENTIAL_PLACEHOLDER: ${{ secrets.CLAUDE_CI_CREDENTIAL_PLACEHOLDER }}",\n'
    )

    old_turn_limit = (
        "The current CLI offers no hard turn-limit flag anymore.\n"
        "Die aktuelle CLI bietet keine harte Turn-Grenze per Flag mehr.\n"
        "1. **`--bare` means path A or C.**\n"
    )
    wrapped = "```bash\nclaude \\\n  --bare -p \"Review\"\n# token: claude setup-token\n```\n"

    assert len(find_wrong_claims(old_module)) >= 4
    assert bare_without_api_key(Path("x.md"), old_module)
    assert find_wrong_claims(old_cockpit)
    assert bare_without_api_key(COCKPIT, old_cockpit)
    assert len(find_wrong_claims(old_turn_limit)) == 2
    assert bare_without_api_key(Path("x.md"), wrapped)


def test_guard_accepts_the_correct_patterns():
    """Positive control: an API-key --bare job and a subscription job without --bare both pass."""
    good = (
        "```yaml\nenv:\n  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}\nrun: claude --bare -p \"Review\"\n```\n"
        "```bash\nclaude setup-token   # store as CLAUDE_CODE_OAUTH_TOKEN\nclaude -p \"Review\"\n```\n"
        "```bash\nclaude setup-token   # subscription token (not read by --bare)\n```\n"
    )

    assert find_wrong_claims(good) == []
    assert bare_without_api_key(Path("x.md"), good) == []


def test_cockpit_examples_are_found():
    """The HTML extractor must actually see the cockpit examples, or the live check proves nothing."""
    examples = snippets(COCKPIT, COCKPIT.read_text(encoding="utf-8"))

    assert len(examples) >= 50
    assert any(BARE_INVOCATION.search(e) for e in examples)


@pytest.mark.parametrize("path", LIVE_FILES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_live_course_content_teaches_consistent_ci_auth(path):
    text = path.read_text(encoding="utf-8")

    assert find_wrong_claims(text) == []
    assert bare_without_api_key(path, text) == []
