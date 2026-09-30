"""Validator tests: one broken variant per rule, starting from the valid fixture library."""
from pathlib import Path
import importlib.util
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tools" / "fixtures" / "library"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lm = _load("library_model")
bl = _load("build_library")


@pytest.fixture
def lib_dir(tmp_path):
    target = tmp_path / "library"
    shutil.copytree(FIXTURES, target)
    return target


def rules(lib_dir, complete=False):
    return sorted({p.rule for p in bl.validate(lm.load_library(lib_dir), complete=complete)})


def edit(lib_dir, name, old, new, count=1):
    path = lib_dir / name
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {name}"
    path.write_text(text.replace(old, new, count), encoding="utf-8")


HOOK = "s2-08-demo-hook.md"
EVENTS = "s2-07-demo-events.md"
STATION = "s2-20-demo-station.md"
COMMUNITY = "x-01-demo-community.md"


def test_valid_fixture_library_has_no_problems(lib_dir):
    assert rules(lib_dir) == []


def test_complete_mode_reports_missing_required_ids(lib_dir):
    problems = bl.validate(lm.load_library(lib_dir), complete=True)
    missing = [p for p in problems if p.rule == "required-ids"]
    assert missing and "S1.1" in missing[0].message


@pytest.mark.parametrize("name,old,new,rule", [
    (HOOK, "type: lesson\n", "type: lecture\n", "frontmatter-schema"),
    (HOOK, "level: core\n", "level: basic\n", "frontmatter-schema"),
    (HOOK, "minutes: 15\n", "minutes: fifteen\n", "frontmatter-schema"),
    (HOOK, "safety_floor: true\n", "safety_floor: yes please\n", "frontmatter-schema"),
    (HOOK, "outcome: \"Ich kann", "outcome: \"Man kann", "frontmatter-schema"),
    (HOOK, "title: Einen Hook konfigurieren\n", "", "frontmatter-schema"),
    (COMMUNITY, "after: S2.13\n", "", "frontmatter-schema"),
    (STATION, "offers: [S2.8]\n", "", "frontmatter-schema"),
    (HOOK, "aliases: [\"2.2\"]\n", "aliases: [\"2.2\"]\noffers: [S2.7]\n", "frontmatter-schema"),
    (HOOK, "id: S2.8\n", "id: S2-8\n", "id-format"),
    (EVENTS, "id: S2.7\n", "id: S2.8\n", "id-unique"),
    (EVENTS, "aliases: []\n", "aliases: [\"2.2\"]\n", "alias-unique"),
    (HOOK, "# S2.8 · Einen Hook konfigurieren", "# S2.8 · Anderer Titel", "h1"),
    (HOOK, "shelf: hooks\n", "shelf: unbekannt\n", "shelf-exists"),
    (HOOK, "requires: [S2.7]\n", "requires: [S9.9]\n", "requires-exist"),
    (EVENTS, "requires: []\n", "requires: [S2.8]\n", "requires-backward"),
    (STATION, "offers: [S2.8]\n", "offers: [S3.1]\n", "offers-exist"),
    (STATION, "requires: []\n", "requires: [S2.8]\n", "practice-no-requires"),
    (HOOK, "## Bild im Kopf\n", "## Bildchen\n", "sections-allowed"),
    (HOOK, "## Schnellcheck\n", "## Vorspann\n", "sections-allowed"),
    (STATION, "## Selbst machen\n", "## Im Detail\n", "sections-allowed"),
    (HOOK, "## Weiterlesen\n\n- [Hooks-Referenz](https://code.claude.com/docs/en/hooks)\n", "", "sections-required"),
    (HOOK, "<!-- cockpit:example -->\n", "", "example-count"),
    (HOOK, "<details><summary>Quizfrage</summary>", "<details><summary>Frage</summary>", "quiz-count"),
    (HOOK, "- Falsch: Nur ein Timeout blockt den Aufruf\n", "", "quiz-shape"),
    (HOOK, "- **Richtig:** Exit-Code 2 blockt den Aufruf",
     "- **Richtig:** Exit-Code 2 blockt den Aufruf, weil nur dieser Code laut Hooks-Referenz ein blockierender Fehler ist",
     "quiz-length-tell"),
    (HOOK, "- Weißt du ohne Nachschlagen, welcher Exit-Code blockt?\n", "", "skip-check-count"),
    (HOOK, "[Link](s2-07-demo-events.md)", "[Link](s2-99-gibt-es-nicht.md)", "links-resolve"),
    (EVENTS, "Details.", "Details. <!-- TODO(migration): Quelle prüfen -->", "no-migration-todo"),
    (HOOK, "  - https://code.claude.com/docs/en/hooks\n", "  - http://code.claude.com/docs/en/hooks\n", "sources-https"),
    (EVENTS, "sources:\n  - https://code.claude.com/docs/en/hooks\n", "sources: []\n", "sources-required"),
])
def test_each_rule_fires(lib_dir, name, old, new, rule):
    edit(lib_dir, name, old, new)
    found = rules(lib_dir)
    assert rule in found, found


def test_section_order(lib_dir):
    path = lib_dir / HOOK
    text = path.read_text(encoding="utf-8")
    glance = text[text.index("## Auf einen Blick"):text.index("## Bild im Kopf")]
    text = text.replace(glance, "")
    text = text.replace("## Check\n", glance + "## Check\n")
    path.write_text(text, encoding="utf-8")
    assert "section-order" in rules(lib_dir)


def test_filename_must_match_id(lib_dir):
    (lib_dir / HOOK).rename(lib_dir / "s2-09-demo-hook.md")
    edit(lib_dir, STATION, "(s2-08-demo-hook.md#selbst-machen)", "(s2-09-demo-hook.md#selbst-machen)")
    assert "filename" in rules(lib_dir)


def test_parse_error_is_reported(lib_dir):
    (lib_dir / "s2-09-kaputt.md").write_text("kein Frontmatter\n", encoding="utf-8")
    assert "parse" in rules(lib_dir)


@pytest.mark.parametrize("old,new,rule", [
    ("chapters: [S2.7, S2.8]", "chapters: [S2.7, S2.8, S2.99]", "placement-refs"),
    ("minimum_path: [S2.7, S2.8]", "minimum_path: [S2.8]", "minimum-path-closed"),
    ("focus_shelves: [hooks]", "focus_shelves: [nirgends]", "placement-refs"),
    ("base_shelves: [hooks]", "base_shelves: [nirgends]", "placement-refs"),
])
def test_placement_rules(lib_dir, old, new, rule):
    edit(lib_dir, "_placement.yaml", old, new)
    assert rule in rules(lib_dir)


def test_chapter_in_two_areas(lib_dir):
    edit(lib_dir, "_placement.yaml", "scenarios: []",
         "  - {id: extra, label: Extra, statement: \"Ich habe etwas gemacht.\", chapters: [S2.8]}\nscenarios: []")
    assert "area-unique" in rules(lib_dir)


def test_scenario_correct_must_be_an_option(lib_dir):
    edit(lib_dir, "_placement.yaml", "scenarios: []", (
        "scenarios:\n"
        "  - id: hook-exit\n"
        "    area: hooks\n"
        "    question: Was passiert?\n"
        "    options: [{id: a, text: Eins}, {id: b, text: Zwei}, {id: c, text: Drei}, {id: d, text: Vier}]\n"
        "    correct: e\n"
        "    explanation: Weil.\n"
        "    chapter: S2.8\n"))
    assert "placement-refs" in rules(lib_dir)


def test_cli_single_chapter_exit_codes(lib_dir, capsys):
    assert bl.main(["validate", "--chapter", str(lib_dir / HOOK)]) == 0
    edit(lib_dir, HOOK, "<!-- cockpit:example -->\n", "")
    assert bl.main(["validate", "--chapter", str(lib_dir / HOOK)]) == 1
    assert "example-count" in capsys.readouterr().out
