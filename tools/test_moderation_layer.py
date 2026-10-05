"""The live course stays out of the chapters: demos and moderator notes are a layer of their own.

Design: docs/plans/2026-10-05-selbstlern-zuerst-design.md. These tests read the real library, not a fixture.
"""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "resources" / "library"
DEMOS = ROOT / "resources" / "moderation" / "vorfuehren"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lm = _load("library_model")


def chapters():
    return [lm.parse_chapter(p) for p in sorted(LIBRARY.glob("*.md")) if p.name not in lm.GENERATED_NAMES]


def test_no_chapter_carries_a_demo_section_or_moderator_block():
    offenders = [ch.id for ch in chapters()
                 if "Vorführen" in ch.sections or "<summary>Für Moderierende</summary>" in ch.path.read_text(encoding="utf-8")]
    assert offenders == []


def test_the_cockpit_does_not_ship_moderator_notes():
    cockpit = (ROOT / "resources" / "claude-code-workshop-ui.html").read_text(encoding="utf-8")
    # Closing tags are escaped in the embedded data, the opening tag is not. Count first: an assert on the
    # 2.6 MB string itself makes pytest render it when the test fails.
    blocks = cockpit.count("<summary>Für Moderierende")
    assert blocks == 0


def test_demos_exist_and_the_live_path_links_every_one_of_them():
    names = sorted(p.name for p in DEMOS.glob("*.md"))
    assert names, "the moderation layer is empty"
    live = (ROOT / "resources" / "paths" / "live-workshop.md").read_text(encoding="utf-8")
    assert [n for n in names if f"(../moderation/vorfuehren/{n})" not in live] == []
