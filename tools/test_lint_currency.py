"""Lint scope and rules (design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint = _load("lint_currency")


def _tree(tmp_path, files):
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def test_live_files_skips_history_tooling_and_local_state(tmp_path):
    root = _tree(tmp_path, {
        "README.md": "x",
        "agents/mentor.md": "x",
        "resources/modules/m.md": "x",
        "resources/_canonical.md": "x",
        "HANDOFF.md": "x",
        "resources/archive/old.html": "x",
        "resources/review-2026-09-28/01.md": "x",
        "docs/plans/p.md": "x",
        "tools/fixtures/currency/f.md": "x",
        "tools/currency_exceptions.txt": "x",
        ".currency/reports/2026-10-01.md": "x",
        ".pi-glla/archive/a.md": "x",
        ".codegraph/c.json": "x",
        ".superpowers/sdd/x/brief.md": "x",
        "workshop-playground/node_modules/pkg/readme.md": "x",
        "resources/demo.py": "x",
    })

    rels = [rel for rel, _full in lint.live_files(str(root))]

    assert rels == ["README.md", "agents/mentor.md", "resources/modules/m.md"]


def test_currency_state_dir_is_git_ignored():
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".currency/" in lines


import datetime as dt

import pytest

CANON_OK = "# Kanon\n\nGeprüft: 2026-09-29 · CLI 2.1.284\n"


@pytest.mark.parametrize("line", [
    "Nutze Opus 4.8 für Architektur.", "sonnet-4.6", "--model claude-haiku-4-5-20251001",
    "Claude Fable 5.1 ist neu.", "SONNET 5", "claude-opus-5-5", "the current Opus (4.8) only",
])
def test_generation_mentions_are_found(line):
    assert lint.GENERATION.search(line) and not lint.is_pinned(line)


@pytest.mark.parametrize("line", [
    "Nutze das Opus-Tier.", "--model opus", "model: sonnet[1m]", "seit 2.1.145 verfügbar", "Opus-Modelle und Haiku",
    "Opus (2x cheaper)", "Sonnet (1M context)",
])
def test_aliases_roles_and_cli_versions_are_allowed(line):
    assert not lint.GENERATION.search(line)


LEGACY_FORBIDDEN_SAMPLES = [
    "claude-sonnet-4-6", "Sonnet 4.6", "sonnet-4.6", "SONNET 4.6", "claude-opus-4-7",
    "claude-3-5-sonnet", "claude-3-7-sonnet-latest", "claude-3-5-haiku",
]


def test_generation_rule_covers_every_pattern_of_the_retired_forbidden_list():
    """Guard replacement: every pattern of the old FORBIDDEN list (until 274e244) must stay blocked.

    Accepted difference: glued forms such as `model_claude-3-5-sonnet` are not blocked, because the rule is \b-based.
    """
    for sample in LEGACY_FORBIDDEN_SAMPLES:
        assert lint.GENERATION.search(sample), sample


def test_pin_needs_a_reason_on_the_same_line():
    assert lint.is_pinned("Haiku 4.5 kann abgeschaltet werden. <!-- version-pinned: Retirement-Hinweis -->")
    assert lint.is_pinned('q: "Haiku 4.5 hat 200K", // version-pinned: Quiz zu Kontextgrenzen')
    assert not lint.is_pinned("Haiku 4.5 <!-- version-pinned: -->")
    assert not lint.is_pinned("Haiku 4.5 <!-- version-pinned: ab -->")


@pytest.mark.parametrize("today,level", [
    (dt.date(2026, 11, 12), "ok"), (dt.date(2026, 11, 14), "warn"), (dt.date(2026, 12, 29), "red"),
])
def test_stale_gate(tmp_path, today, level):
    canon = tmp_path / "_canonical.md"
    canon.write_text(CANON_OK, encoding="utf-8")
    assert lint.canon_status(str(canon), today)[0] == level


def test_future_check_date_is_red(tmp_path):
    canon = tmp_path / "_canonical.md"
    canon.write_text("# Kanon\n\nGeprüft: 2027-09-29 · CLI 2.1.284\n", encoding="utf-8")
    level, message = lint.canon_status(str(canon), dt.date(2026, 9, 29))
    assert level == "red" and "Zukunft" in message


@pytest.mark.parametrize("today,level", [
    (dt.date(2026, 11, 13), "ok"), (dt.date(2026, 11, 14), "warn"),
    (dt.date(2026, 12, 28), "warn"), (dt.date(2026, 12, 29), "red"),
])
def test_stale_gate_boundaries(tmp_path, today, level):
    """Rule is age > 45 (warn) and age > 90 (red): 45 days ok, 46 warn, 90 warn, 91 red."""
    canon = tmp_path / "_canonical.md"
    canon.write_text(CANON_OK, encoding="utf-8")
    assert lint.canon_status(str(canon), today)[0] == level


def test_main_warns_at_46_days_but_exits_0(tmp_path, capsys):
    root = _tree(tmp_path, {"resources/_canonical.md": CANON_OK, "resources/modules/m.md": "Nutze das Opus-Tier.\n"})
    assert lint.main(str(root), today=dt.date(2026, 11, 14)) == 0
    assert "WARNUNG" in capsys.readouterr().out


def test_course_has_no_generation_outside_the_canon():
    assert lint.generation_hits(lint.ROOT) == []


def test_missing_or_unreadable_check_date_is_red(tmp_path):
    canon = tmp_path / "_canonical.md"
    canon.write_text("# Kanon ohne Datum\n", encoding="utf-8")
    assert lint.canon_status(str(canon), dt.date(2026, 9, 29))[0] == "red"
    assert lint.canon_status(str(tmp_path / "missing.md"), dt.date(2026, 9, 29))[0] == "red"


def test_main_combines_generation_rule_and_stale_gate(tmp_path, capsys):
    root = _tree(tmp_path, {
        "resources/_canonical.md": CANON_OK + "Claude Opus 5.5 steht hier.\n",
        "resources/modules/m.md": "Nutze das Opus-Tier.\nHaiku 4.5 <!-- version-pinned: Retirement-Hinweis -->\n",
    })
    assert lint.main(str(root), today=dt.date(2026, 9, 29)) == 0
    (root / "resources/modules/m.md").write_text("Nutze Opus 5.5.\n", encoding="utf-8")
    assert lint.main(str(root), today=dt.date(2026, 9, 29)) == 1
    assert "resources/modules/m.md:1" in capsys.readouterr().out
    (root / "resources/modules/m.md").write_text("Nutze das Opus-Tier.\n", encoding="utf-8")
    assert lint.main(str(root), today=dt.date(2027, 1, 1)) == 1
