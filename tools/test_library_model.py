"""Tests for tools/library_model.py - parsing library chapters."""
from pathlib import Path
import importlib.util
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tools" / "fixtures" / "library"


def _load():
    spec = importlib.util.spec_from_file_location("library_model", ROOT / "tools" / "library_model.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["library_model"] = module
    spec.loader.exec_module(module)
    return module


lm = _load()


def test_order_of_session_ids():
    assert lm.order_of("S2.8", None) == 2080
    assert lm.order_of("S0.1", None) == 10
    assert lm.order_of("S4.10", None) == 4100
    assert lm.order_of("X.1", "S2.13") == 2135


def test_order_of_x_chapter_needs_after():
    with pytest.raises(ValueError):
        lm.order_of("X.1", None)


def test_order_of_rejects_unknown_id():
    with pytest.raises(ValueError):
        lm.order_of("Q1.2", None)


def test_parse_lesson_fixture():
    ch = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md")
    assert ch.id == "S2.8"
    assert ch.type == "lesson"
    assert ch.session == 2
    assert ch.order == 2080
    assert ch.requires == ["S2.7"]
    assert ch.safety_floor is True
    assert ch.aliases == ["2.2"]
    assert ch.section_order == [
        "Schnellcheck", "Auf einen Blick", "Bild im Kopf", "Im Detail", "Selbst machen", "Check", "Weiterlesen",
    ]
    assert ch.skip_check == [
        "Hast du schon einen Hook gebaut, der eine Aktion wirklich blockt?",
        "Weißt du ohne Nachschlagen, welcher Exit-Code blockt?",
    ]
    assert ch.glance == "Ein Hook ist ein Skript, das Claude Code bei einem Ereignis aufruft. Nur `exit 2` blockt."
    assert ch.analogy == "Wie ein Türsensor, der die Tür nur bei einem bestimmten Signal verriegelt."
    assert ch.checkpoint == "Du kannst einen Hook eintragen und seinen Exit-Code begründen."
    assert ch.example == '{"hooks": {"PreToolUse": []}}'
    assert ch.example_lang == "json"
    assert ch.quiz.question == "Welcher Exit-Code blockt einen PreToolUse-Aufruf?"
    assert ch.quiz.correct == "Exit-Code 2 blockt den Aufruf"
    assert len(ch.quiz.wrong) == 3
    assert len(ch.mermaid) == 1 and ch.mermaid[0].startswith("flowchart LR")
    assert "s2-07-demo-events.md" in ch.links
    assert "https://code.claude.com/docs/en/hooks" in ch.links



# --- P10: one reason per quiz answer ("- Warum: ..." indented under the answer) ---------------------------

def test_quiz_reasons_belong_to_their_answers():
    q = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md").quiz
    assert q.why_correct.startswith("Nur Exit-Code 2 ")
    assert len(q.why_wrong) == 3 and all(q.why_wrong)
    assert q.why_wrong[1].startswith("Exit-Code 1 ")  # same order as the wrong answers
    assert q.why_stray == 0


def test_quiz_without_reasons_has_none():
    q = lm.parse_chapter(FIXTURES / "s2-07-demo-events.md").quiz
    assert q.why_correct is None and q.why_wrong == [None, None, None] and q.why_stray == 0
    assert not q.has_why


def test_quiz_reason_without_indent_or_twice_is_stray(tmp_path):
    text = (FIXTURES / "s2-08-demo-hook.md").read_text(encoding="utf-8")
    first = "  - Warum: Nur Exit-Code 2 "
    assert first in text
    path = tmp_path / "s2-08-demo-hook.md"
    path.write_text(text.replace(first, "- Warum: Nur Exit-Code 2 "), encoding="utf-8")
    q = lm.parse_chapter(path).quiz
    assert q.why_correct is None and q.why_stray == 1
    path.write_text(text.replace(first, "  - Warum: doppelt" + chr(10) + first), encoding="utf-8")
    assert lm.parse_chapter(path).quiz.why_stray == 1

def test_h2_inside_code_fence_is_not_a_section():
    ch = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md")
    assert "Das ist kein Abschnitt" not in ch.sections
    assert "## Das ist kein Abschnitt" in ch.sections["Im Detail"]


def test_meta_block_is_ignored_for_sections():
    ch = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md")
    assert all("alter generierter Block" not in body for body in ch.sections.values())
    assert "alter generierter Block" not in ch.preamble


def test_crlf_input_parses_like_lf(tmp_path):
    src = (FIXTURES / "s2-08-demo-hook.md").read_bytes().replace(b"\r\n", b"\n")
    crlf = tmp_path / "s2-08-demo-hook.md"
    crlf.write_bytes(src.replace(b"\n", b"\r\n"))
    a = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md")
    b = lm.parse_chapter(crlf)
    for field in ("id", "sections", "section_order", "quiz", "example", "skip_check", "glance", "analogy",
                  "checkpoint", "mermaid", "links"):
        assert getattr(a, field) == getattr(b, field), field


def test_practice_offers_and_x_after():
    station = lm.parse_chapter(FIXTURES / "s2-20-demo-station.md")
    assert station.type == "practice"
    assert station.offers == ["S2.8"]
    assert station.requires == []
    community = lm.parse_chapter(FIXTURES / "x-01-demo-community.md")
    assert community.session is None
    assert community.order == 2135
    assert community.quiz is None and community.example is None


def test_missing_frontmatter_raises(tmp_path):
    bad = tmp_path / "s1-01-kaputt.md"
    bad.write_text("# S1.1 · Ohne Kopf\n\n## Auf einen Blick\n\nText\n", encoding="utf-8")
    with pytest.raises(lm.ChapterError):
        lm.parse_chapter(bad)


def test_load_library_sorts_by_order(tmp_path):
    lib_dir = tmp_path / "library"
    shutil.copytree(FIXTURES, lib_dir)
    lib = lm.load_library(lib_dir)
    assert [c.id for c in lib.chapters] == ["S2.7", "S2.8", "X.1", "S2.20"]
    assert lib.by_id["S2.8"].title == "Einen Hook konfigurieren"
    assert [s["id"] for s in lib.shelves][:2] == ["hooks", "practice"]
    assert lib.placement["version"] == 1


def test_recall_questions_and_their_answers_are_parsed_from_the_check_section():
    hook = lm.parse_chapter(FIXTURES / "s2-08-demo-hook.md")
    assert hook.recall == ["Welcher Exit-Code blockt einen Aufruf?", "Was passiert bei `exit 1`?"]
    assert hook.answers == ["Von den Exit-Codes blockt nur `2`.",
                            "Der Aufruf läuft weiter, Claude Code meldet nur einen Hook-Fehler."]
    events = lm.parse_chapter(FIXTURES / "s2-07-demo-events.md")
    assert events.recall == [] and events.answers is None  # no questions, no answer block
