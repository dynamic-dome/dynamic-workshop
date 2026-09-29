from pathlib import Path
import importlib.util
import re
import tempfile


ROOT = Path(__file__).resolve().parents[1]
UI_HTML = ROOT / "resources" / "claude-code-workshop-ui.html"


def _extract_function(source: str, name: str) -> str:
    match = re.search(rf"function {name}\([^)]*\) \{{(?P<body>.*?)\n    \}}", source, re.S)
    if not match:
        raise AssertionError(f"function {name} not found")
    return match.group("body")


def _load_tool(name: str):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quiz_shuffle_uses_real_fisher_yates_permutation():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "shuffle")

    assert ".sort(" not in body
    assert "Math.random()" in body
    assert "for (let i = copy.length - 1; i > 0; i--)" in body
    assert "[copy[i], copy[j]] = [copy[j], copy[i]];" in body


def test_exercise_scoring_is_feedback_only():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "gradeExercise")

    assert "lengthScore" not in body
    assert "state.done" not in body


def test_cumulative_quiz_books_the_asked_section():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "renderCumulativeQuiz")

    assert "state.quiz[q.id]" in body
    assert "state.done[q.id]" in body
    assert "state.quiz[s.id]" not in body
    assert "state.done[s.id]" not in body


def test_final_quiz_uses_recall_questions_not_theme_labels():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "renderFinalQuiz")

    assert "const qz = sectionQuiz[id];" in body
    assert "${qz.q}" in body
    assert "themeFor(s)" not in body
    assert "Themenfamilie" not in body


def test_tactical_theme_has_no_blocking_navigation_effects():
    source = UI_HTML.read_text(encoding="utf-8")
    forbidden = [
        "amber-flicker",
        "soc-flash",
        "ACCESSING",
        "SECTOR T",
        "scan-line",
        ".main.scanning",
        "blinkInterval",
    ]

    for token in forbidden:
        assert token not in source
    assert "S1.1 STANDBY" in source
    assert "`${activeId} ACCESSED`" in source


def test_route_transparency_shows_budget_and_reference_link():
    source = UI_HTML.read_text(encoding="utf-8")

    assert "48 = Pflicht-Core plus fruehe Vertiefungen; 65 = komplette Landkarte." in source
    assert '["cheatsheet.md", "Cheatsheet"]' in source
    assert "const minutes = items.reduce((sum, item) => sum + item.min, 0);" in source
    assert "S${session}: ${minutes} Min / ~150" in source
    assert "minutes > 150" in source
    assert ".session-budget.over-budget" in source


def test_local_storage_state_load_is_fail_soft():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "loadState")

    assert 'JSON.parse(localStorage.getItem("ccWorkshopUiState") || "{}")' in body
    assert "catch (err)" in body
    assert 'localStorage.removeItem("ccWorkshopUiState")' in body
    assert "return {};" in body


def test_deep_links_validate_route_and_section_before_first_render():
    source = UI_HTML.read_text(encoding="utf-8")
    body = _extract_function(source, "applyDeepLink")

    assert "new URLSearchParams(window.location.search)" in body
    assert 'requestedView === "65" ? "65" : "48"' in body
    assert 'params.get("run") || params.get("section")' in body
    assert "route.some(s => s.id === requestedId)" in body
    assert 'route[0]?.id || "S1.1"' in body
    assert source.rindex("applyDeepLink();") < source.rindex("renderAll();")


def test_currency_sweep_matches_lint_for_sonnet_46_variants():
    sweep = _load_tool("sweep_sonnet5")

    data = b"SONNET 4.6\nsonnet-4.6\nSonnet 4.6\nclaude-sonnet-4-6"
    for rx, new in sweep.REPLACEMENTS:
        data = rx.sub(new, data)

    assert b"SONNET 4.6" not in data
    assert b"sonnet-4.6" not in data
    assert b"Sonnet 4.6" not in data
    assert b"claude-sonnet-4-6" not in data
    assert data.count(b"Sonnet 5") == 3
    assert b"claude-sonnet-5" in data


def test_currency_lint_checks_cp1252_files_instead_of_skipping(tmp_path):
    lint = _load_tool("lint_currency")
    path = tmp_path / "cp1252.md"
    path.write_bytes("Currency: SONNET 4.6 \u20ac".encode("cp1252"))

    lines = lint.read_lines(path)
    assert lint.GENERATION.search(lines[0])


def test_code_example_keeps_line_breaks_so_it_can_be_copied():
    """A <p> with normal white-space collapses newlines; a shebang line would then comment out the whole script."""
    source = UI_HTML.read_text(encoding="utf-8")

    assert re.search(r'<pre id="example"[^>]*>', source)
    rule = re.search(r"#example\s*\{(?P<body>[^}]*)\}", source)
    assert rule and "white-space: pre-wrap" in rule.group("body")
    card = re.search(r"\.mini-code\s*\{(?P<body>[^}]*)\}", source)
    assert card and "grid-column: 1 / -1" in card.group("body")
    assert '<div class="mini mini-code">' in source


def test_currency_lint_excludes_every_dated_review_archive_but_not_live_content():
    lint = _load_tool("lint_currency")

    assert lint.is_excluded("resources/review-2026-09-28/01-welt-delta.md")
    assert lint.is_excluded("resources/review-2031-01-01/00-SCHEMA.md")
    assert not lint.is_excluded("resources/modules/block-1-foundations.md")
    assert not lint.is_excluded("resources/review-notes.md")


if __name__ == "__main__":
    test_quiz_shuffle_uses_real_fisher_yates_permutation()
    test_exercise_scoring_is_feedback_only()
    test_cumulative_quiz_books_the_asked_section()
    test_final_quiz_uses_recall_questions_not_theme_labels()
    test_tactical_theme_has_no_blocking_navigation_effects()
    test_route_transparency_shows_budget_and_reference_link()
    test_local_storage_state_load_is_fail_soft()
    test_deep_links_validate_route_and_section_before_first_render()
    test_currency_sweep_matches_lint_for_sonnet_46_variants()
    with tempfile.TemporaryDirectory() as tmp:
        test_currency_lint_checks_cp1252_files_instead_of_skipping(Path(tmp))
    print("OK - workshop UI behavior checks passed.")
