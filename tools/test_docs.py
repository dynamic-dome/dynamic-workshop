"""Root documents and live material: one set of rules, no links to retired files."""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
RETIRED = [
    "resources/modules/", "resources/exercises/", "resources/demos/block-", "resources/session-plan.md",
    "resources/prerequisites.md", "resources/cheatsheet.md", "resources/quick-reference.md", "resources/faq.md",
    "resources/troubleshooting.md", "resources/glossary.md", "resources/security-analogies.md",
    "resources/trainer-notes.md", "resources/live-3-person-mode.md", "resources/retrieval-recap-bridges.md",
    "resources/transfer-retention-plan.md", "resources/capstone-exit-assessment.md", "resources/workshop-guide.md",
    "WORKSHOP_EINFUEHRUNG.md", "claude-code-workshop.pptx", "claude-code-workshop-4session.pptx",
]
LIVE_DIRS = ["resources/library", "resources/reference", "resources/moderation", "resources/paths", "skills", "agents"]
LIVE_ROOT = ["README.md", "HOW-TO-USE.md", "CLAUDE.md", "AGENTS.md"]


def live_markdown():
    files = [ROOT / f for f in LIVE_ROOT]
    for rel in LIVE_DIRS:
        for dirpath, _, names in os.walk(ROOT / rel):
            files += [Path(dirpath) / n for n in names if n.endswith(".md")]
    return files


def test_agents_md_mirrors_claude_md():
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8").replace("\r\n", "\n").split("\n", 1)[1]
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").replace("\r\n", "\n").split("\n", 1)[1]
    assert claude == agents, "AGENTS.md (Codex) und CLAUDE.md (Claude) müssen dieselben Regeln tragen"


def test_claude_md_stays_short():
    assert len((ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines()) <= 40


def _repo_path(base: Path, target: str):
    try:
        return os.path.relpath(os.path.normpath(base / target), ROOT).replace("\\", "/")
    except ValueError:  # other drive
        return None


def retired_references(path: Path, text: str) -> list:
    """Links resolve relative to the file; code mentions (`resources/x.md`) may also be repo-relative."""
    found = []
    links = [(t, False) for t in re.findall(r"\]\(([^)\s]+)\)", text)]
    codes = [(t, True) for t in re.findall(r"`([^`\s]+\.(?:md|pptx))`", text)]
    for target, is_code in links + codes:
        clean = target.split("#", 1)[0].replace("\\", "/")
        if not clean or "://" in clean or clean.startswith("mailto:"):
            continue
        bases = [path.parent, ROOT] if is_code else [path.parent]
        for rel in filter(None, (_repo_path(b, clean) for b in bases)):
            if any(rel == old.rstrip("/") or rel.startswith(old) for old in RETIRED):
                found.append(f"{path.relative_to(ROOT).as_posix()}: {target}")
                break
    return found


def test_retired_reference_guard_resolves_relative_to_the_file():
    lib = ROOT / "resources" / "library" / "x.md"
    ref = ROOT / "resources" / "reference" / "README.md"
    assert retired_references(lib, "[alt](../cheatsheet.md) und `resources/modules/block-1-foundations.md`")
    assert retired_references(ROOT / "README.md", "[alt](WORKSHOP_EINFUEHRUNG.md)")
    assert retired_references(ref, "[FAQ](faq.md), `faq.md`, [Karte](karte-hooks.md#x)") == []


def test_no_links_to_retired_files():
    offenders = []
    for path in live_markdown():
        offenders += retired_references(path, path.read_text(encoding="utf-8"))
    assert not offenders, "\n".join(offenders)
