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


def test_no_links_to_retired_files():
    offenders = []
    for path in live_markdown():
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r"`([^`\s]+\.(?:md|pptx))`", text):
            normalized = target.replace("\\", "/").lstrip("./")
            normalized = re.sub(r"^(\.\./)+", "", normalized)
            if any(old in "resources/" + normalized or old in normalized for old in RETIRED):
                offenders.append(f"{path.relative_to(ROOT).as_posix()}: {target}")
    assert not offenders, "\n".join(offenders)
