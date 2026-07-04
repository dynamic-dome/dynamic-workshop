from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
UI_HTML = ROOT / "resources" / "cloud-code-workshop-ui.html"


def _extract_function(source: str, name: str) -> str:
    match = re.search(rf"function {name}\([^)]*\) \{{(?P<body>.*?)\n    \}}", source, re.S)
    if not match:
        raise AssertionError(f"function {name} not found")
    return match.group("body")


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


if __name__ == "__main__":
    test_quiz_shuffle_uses_real_fisher_yates_permutation()
    test_exercise_scoring_is_feedback_only()
    test_cumulative_quiz_books_the_asked_section()
    test_final_quiz_uses_recall_questions_not_theme_labels()
    test_tactical_theme_has_no_blocking_navigation_effects()
    print("OK - workshop UI behavior checks passed.")
