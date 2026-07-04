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


if __name__ == "__main__":
    test_quiz_shuffle_uses_real_fisher_yates_permutation()
    print("OK - workshop UI behavior checks passed.")
