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
