"""The /workshop tutor, the mentor and the plugin manifest point only at files that exist in the library layout."""
from pathlib import Path
import json
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "workshop" / "SKILL.md"
MENTOR = ROOT / "agents" / "workshop-mentor.md"
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
GENERATED = {"resources/library/catalog.json", "resources/library/README.md", "resources/paths/live-workshop.md"}
REMOVED = ["resources/modules", "resources/demos/block-", "resources/exercises", "session-plan.md", "cheatsheet.md",
           "security-analogies.md", "quick-reference.md", "workshop-guide.md", "prerequisites.md", "trainer-notes.md"]


def front(path):
    text = path.read_text(encoding="utf-8")
    end = text.index("\n---", 4)
    return yaml.safe_load(text[4:end]), text[end + 4:]


def plugin_paths(text):
    return sorted(set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)", text)))


def test_skill_frontmatter_and_modes():
    meta, body = front(SKILL)
    assert meta["name"] == "workshop"
    assert meta["arguments"] == ["mode", "target"]
    assert meta["disable-model-invocation"] is True
    for mode in ("start", "next", "learn", "review", "guide"):
        assert f"`/workshop {mode}" in body, mode
    assert "aus dem Gedächtnis" in body  # no silent fallback to model knowledge


def test_skill_and_mentor_reference_existing_or_generated_files():
    for path in (SKILL, MENTOR):
        for rel in plugin_paths(path.read_text(encoding="utf-8")):
            rel = rel.rstrip("/.")
            if "<" in rel or rel in GENERATED:
                continue
            assert (ROOT / rel).exists(), f"{path.name}: {rel}"


def test_supporting_formats_exist_and_credit_the_source():
    for name in ("MISSION-FORMAT.md", "LEARNING-RECORD-FORMAT.md"):
        text = (SKILL.parent / name).read_text(encoding="utf-8")
        assert "mattpocock/skills" in text and "MIT" in text
        assert f"]({name})" in SKILL.read_text(encoding="utf-8")


def test_no_references_to_removed_course_files():
    for path in (SKILL, MENTOR):
        text = path.read_text(encoding="utf-8")
        for old in REMOVED:
            assert old not in text, f"{path.name} nennt {old}"


def test_placement_cli_named_in_skill_exists_with_the_used_flags():
    text = SKILL.read_text(encoding="utf-8")
    assert "tools/placement.py" in text
    cli = (ROOT / "tools" / "placement.py").read_text(encoding="utf-8")
    for flag in ("--catalog", "--answers", "--format", "--link-base", "--template"):
        assert flag in cli, flag
        if flag != "--template":
            assert flag in text, flag


def test_manifest_describes_the_library():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["name"] == "dynamic-workshop"
    assert "70 Kapitel" in data["description"] and "/workshop start" in data["description"]
    assert "17 modules" not in data["description"]


def test_no_duplicate_command_shadowing_the_skill():
    assert not (ROOT / "commands" / "workshop.md").exists()


def test_tutor_goes_through_the_teaching_text_when_a_chapter_is_to_be_worked_through():
    """Status 'work' means the lesson text itself, not only the summary (design 2026-10-05, package P2)."""
    body = SKILL.read_text(encoding="utf-8")
    section = body.split("## Ein Kapitel durchgehen", 1)[1].split(chr(10) + "## ", 1)[0]
    for step in ("**Schnellcheck**", "**Auf einen Blick + Bild im Kopf**", "**Im Detail**", "**Selbst machen**",
                 "**Check**", "**Abschluss**"):
        assert step in section, step
    assert (section.index("**Auf einen Blick + Bild im Kopf**") < section.index("**Im Detail**")
            < section.index("**Selbst machen**") < section.index("**Check**"))
    assert "`skim` heißt: nur Schritt 2 und 5" in section
    assert "kein „Selbst machen" in section  # a lesson without an exercise still ends in something to do
