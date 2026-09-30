"""Snippet ledger: nothing from the old course files may get lost silently during the move."""
from pathlib import Path
import importlib.util
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("migration_ledger", ROOT / "tools" / "migration_ledger.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["migration_ledger"] = module
    spec.loader.exec_module(module)
    return module


ml = _load()


def test_fence_parser_and_normalization():
    text = "a\n```bash\necho hi   \n\n```\n~~~\n```inner```\n~~~\n"
    blocks = list(ml.fenced_blocks(text))
    assert [(line, lang) for line, lang, _ in blocks] == [(2, "bash"), (6, "")]
    assert ml.normalize("\n  x  \r\ny\n\n") == "  x\ny"
    assert ml.digest("echo hi\n") == ml.digest("echo hi   \r\n")
    # a block that sat in a list item (common indentation) is the same snippet when it moves to column 0
    assert ml.digest("   mkdir x\n     cd x\n") == ml.digest("mkdir x\n  cd x\n")
    assert ml.digest("mkdir x\n  cd x\n") != ml.digest("mkdir x\ncd x\n")


def test_old_snippets_come_from_the_base_commit():
    snippets = ml.old_snippets()
    assert len(snippets) > 250
    assert {s.path for s in snippets} <= set(ml.OLD_FILES)


def test_dropped_entries_have_reasons():
    for raw in ml.DROPPED.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            parts = line.split(" ", 2)
            assert len(parts) == 3 and len(parts[0]) == 16 and parts[2].strip(), line


def test_every_old_snippet_is_kept_or_dropped_with_reason():
    _, _, _, missing = ml.ledger()
    assert not missing, f"{len(missing)} Snippets fehlen, z. B. {missing[0].path}:{missing[0].line}"
