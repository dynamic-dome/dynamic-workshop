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
    ("chapter_goals: {}", "chapter_goals: {S2.8: {alltag: true}}", "placement-refs"),
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


def test_order_unique(lib_dir):
    edit(lib_dir, COMMUNITY, "after: S2.13", "after: S2.7")
    (lib_dir / "x-02-zweites.md").write_text((lib_dir / COMMUNITY).read_text(encoding="utf-8")
        .replace("id: X.1", "id: X.2").replace("# X.1 ·", "# X.2 ·"), encoding="utf-8")
    assert "order-unique" in rules(lib_dir)


def test_meta_contract(lib_dir):
    lib = lm.load_library(lib_dir)
    meta = [dict(c.front, file=c.path.name) for c in lib.chapters]
    assert [p for p in bl.validate(lib, complete=False, meta=meta) if p.rule == "meta-contract"] == []
    meta[0]["minutes"] = 99
    found = [p for p in bl.validate(lib, complete=False, meta=meta) if p.rule == "meta-contract"]
    assert found and "minutes" in found[0].message


def test_links_to_planned_chapters_are_ok_during_migration(lib_dir):
    edit(lib_dir, HOOK, "[Link](s2-07-demo-events.md)", "[Link](s2-09-geplant.md)")
    lib = lm.load_library(lib_dir)
    meta = [dict(c.front, file=c.path.name) for c in lib.chapters] + [{"id": "S2.9", "file": "s2-09-geplant.md"}]
    assert "links-resolve" not in {p.rule for p in bl.validate(lib, complete=False, meta=meta)}
    assert "links-resolve" in {p.rule for p in bl.validate(lib, complete=True, meta=meta)}


def test_badly_named_markdown_file_is_reported(lib_dir, capsys):
    (lib_dir / "s2-8-hook.md").write_text((lib_dir / HOOK).read_text(encoding="utf-8"), encoding="utf-8")
    assert "parse" in rules(lib_dir)
    assert bl.main(["validate", "--chapter", str(lib_dir / "s2-8-hook.md")]) == 1


def test_generated_files_in_library_are_not_chapters(lib_dir):
    (lib_dir / "README.md").write_text("# Generiert\n", encoding="utf-8")
    (lib_dir / "einstufung.md").write_text("# Generiert\n", encoding="utf-8")
    assert rules(lib_dir) == []


def test_unclosed_quiz_is_reported(lib_dir):
    edit(lib_dir, HOOK, "- Falsch: Nur ein Timeout blockt den Aufruf\n\n</details>", "- Falsch: Nur ein Timeout blockt den Aufruf\n")
    assert "quiz-shape" in rules(lib_dir)


def test_two_correct_answers_are_reported(lib_dir):
    edit(lib_dir, HOOK, "- Falsch: Exit-Code 1 blockt den Aufruf", "- **Richtig:** Exit-Code 1 blockt den Aufruf")
    assert "quiz-shape" in rules(lib_dir)


def test_broken_anchor_is_reported_and_valid_anchor_passes(lib_dir):
    edit(lib_dir, HOOK, "[Link](s2-07-demo-events.md)", "[Link](s2-07-demo-events.md#selbst-machen)")
    assert "links-resolve" not in rules(lib_dir)
    edit(lib_dir, HOOK, "[Link](s2-07-demo-events.md#selbst-machen)", "[Link](s2-07-demo-events.md#gibt-es-nicht)")
    assert "links-resolve" in rules(lib_dir)


def test_github_slug():
    assert bl.github_slug("Selbst machen") == "selbst-machen"
    assert bl.github_slug("Für Moderierende: `exit 2`!") == "für-moderierende-exit-2"
    assert bl.github_slug("Rechte & Freigaben") == "rechte--freigaben"


def test_requires_on_planned_chapters_are_ok_during_migration(lib_dir):
    edit(lib_dir, EVENTS, "requires: []", "requires: [S1.5]")
    lib = lm.load_library(lib_dir)
    meta = [dict(c.front, file=c.path.name) for c in lib.chapters] + [{"id": "S1.5", "file": "s1-05-x.md"}]
    partial = {p.rule for p in bl.validate(lib, complete=False, meta=meta)}
    assert "requires-exist" not in partial
    assert "requires-exist" in {p.rule for p in bl.validate(lib, complete=True, meta=meta)}


def test_quiz_longest_share_is_checked_library_wide(lib_dir):
    # both fixture quizzes: make the correct answer the longest in each -> 2 of 2 = 100 %
    edit(lib_dir, HOOK, "- **Richtig:** Exit-Code 2 blockt den Aufruf", "- **Richtig:** Exit-Code 2 blockt den Aufruf ganz")
    edit(lib_dir, EVENTS, "- **Richtig:** Bevor ein Werkzeug ausgeführt wird", "- **Richtig:** Bevor ein Werkzeug ausgeführt wird!!")
    found = {p.rule for p in bl.validate(lm.load_library(lib_dir), complete=True)}
    assert "quiz-longest-share" in found


# --- moderation layer: demos live outside the chapters (design 2026-10-05) ------------------------------

def demo_dir(lib_dir):
    path = lib_dir.parent / "moderation" / "vorfuehren"
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_vorfuehren_section_is_not_allowed_in_a_chapter(lib_dir):
    edit(lib_dir, HOOK, "## Selbst machen", "## Vorführen" + chr(10) * 2 + "Zeig den Hook." + chr(10) * 2 + "## Selbst machen")
    assert "sections-allowed" in rules(lib_dir)


def test_moderation_block_is_not_allowed_in_a_chapter(lib_dir):
    block = "<details><summary>Für Moderierende</summary>" + chr(10) * 2 + "Sagen: …" + chr(10) * 2 + "</details>"
    edit(lib_dir, HOOK, "## Check", block + chr(10) * 2 + "## Check")
    assert "no-moderation-block" in rules(lib_dir)


def test_demo_file_without_a_chapter_is_reported(lib_dir):
    (demo_dir(lib_dir) / "s9-99-ohne-kapitel.md").write_text("# Vorführen: S9.9 · Nichts" + chr(10), encoding="utf-8")
    assert "demo-orphan" in rules(lib_dir)


def test_demo_file_must_name_its_chapter_and_its_links_must_resolve(lib_dir):
    demo = demo_dir(lib_dir) / HOOK
    demo.write_text("# Vorführen: S2.8 · Einen Hook konfigurieren" + chr(10) * 2
                    + "[Kapitel](../../library/s2-08-demo-hook.md)" + chr(10), encoding="utf-8")
    assert rules(lib_dir) == []
    demo.write_text("# Vorführen: S2.8 · Falscher Titel" + chr(10) * 2
                    + "[weg](../../library/gibt-es-nicht.md)" + chr(10), encoding="utf-8")
    assert {"demo-h1", "links-resolve"} <= set(rules(lib_dir))


def test_only_goal_paths_the_generator_writes_may_be_linked_before_they_exist(lib_dir):
    edit(lib_dir, HOOK, "## Weiterlesen", "## Weiterlesen" + chr(10) * 2 + "- [Pfad Alltag](../paths/ziel-alltag.md)")
    assert rules(lib_dir) == []  # goal 'alltag' exists: the file is generated by the build
    edit(lib_dir, HOOK, "(../paths/ziel-alltag.md)", "(../paths/ziel-gibt-es-nicht.md)")
    assert "links-resolve" in rules(lib_dir)


def test_demo_link_to_a_goal_path_that_is_not_generated_is_reported(lib_dir):
    demo = demo_dir(lib_dir) / HOOK
    demo.write_text("# Vorführen: S2.8 · Einen Hook konfigurieren" + chr(10) * 2
                    + "[weg](../../paths/ziel-gibt-es-nicht.md)" + chr(10), encoding="utf-8")
    assert "links-resolve" in rules(lib_dir)


# --- answers to the recall questions (design 2026-10-05, package P3) --------------------------------------

def rules_with_required(lib_dir, required):
    lib = lm.load_library(lib_dir)
    return sorted({p.rule for p in bl.validate(lib, complete=False, answers_required=frozenset(required))})


def test_every_recall_question_needs_exactly_one_answer(lib_dir):
    edit(lib_dir, HOOK, "2. Der Aufruf läuft weiter, Claude Code meldet nur einen Hook-Fehler." + chr(10), "")
    assert "answers-count" in rules(lib_dir)


def test_an_unclosed_answer_block_is_reported(lib_dir):
    edit(lib_dir, HOOK, "meldet nur einen Hook-Fehler." + chr(10) * 2 + "</details>", "meldet nur einen Hook-Fehler.")
    assert "answers-count" in rules(lib_dir)


def test_answers_are_required_only_for_chapters_on_the_list(lib_dir):
    edit(lib_dir, EVENTS, "Du ordnest Events zu.", "Du ordnest Events zu." + chr(10) * 2 + "1. Wann feuert Stop?")
    assert rules_with_required(lib_dir, []) == []
    assert rules_with_required(lib_dir, ["S2.7"]) == ["answers-required"]
    assert rules_with_required(lib_dir, ["S2.8"]) == []  # S2.8 has its answers


def test_validate_reports_how_many_lessons_have_an_exercise_and_answers(lib_dir, capsys):
    assert bl.main(["validate", "--root", str(lib_dir)]) == 0
    out = capsys.readouterr().out
    assert "Lektionen mit Übung: 2 von 2" in out and "mit Auflösung: 1 von 2" in out
