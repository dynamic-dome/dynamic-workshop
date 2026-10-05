"""The playground keeps its solutions outside of itself.

Claude Code loads workshop-playground/CLAUDE.md in every session there and reads the sources on request. A list of
the planted flaws in that folder, or a comment that names one, turns "find the flaw" into "copy the list"
(review 2026-10-05, finding R18). The answer key lives in resources/reference/playground-loesungen.md.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PLAYGROUND = ROOT / "workshop-playground"
KEY = ROOT / "resources" / "reference" / "playground-loesungen.md"

# Words that give a planted flaw away. Lower case; matched case-insensitively against every line.
SPOILERS = re.compile(
    r"vulnerab|intentional|teaching target|teaching vuln|fail[- ]open|fail[- ]secure|injection|traversal|overflow"
    r"|off-by-one|format string|hardcoded secret|no sanitization|no bounds check|should deny|\(wrong\)|must be printf"
    r"|trigger v\d|do not fix", re.I)
FLAWED = ("read_log", "backup_database", "log_event", "check_access_resilient",
          "decode_data_payload", "compute_crc", "log_frame", "read_frame_crc")


def playground_texts():
    for path in sorted(PLAYGROUND.iterdir()):
        if path.is_file() and (path.suffix in {".py", ".c", ".md", ".txt"} or path.name == "Makefile"):
            yield path, path.read_text(encoding="utf-8")


def test_nothing_in_the_playground_names_a_planted_flaw():
    hits = [f"{path.name}:{number}: {line.strip()[:90]}"
            for path, text in playground_texts()
            for number, line in enumerate(text.splitlines(), start=1) if SPOILERS.search(line)]
    assert hits == []


def test_the_answer_key_covers_every_flawed_function_and_names_only_functions_that_exist():
    key = KEY.read_text(encoding="utf-8")
    named = set(re.findall(r"`(\w+)\(\)`", key))
    assert [name for name in FLAWED if name not in named] == []
    source = "".join(text for path, text in playground_texts() if path.suffix in {".py", ".c"})
    assert [name for name in sorted(named) if not re.search(rf"\b{name}\s*\(", source)] == []
    assert "ADMIN_PASSWORD" in key and "ADMIN_PASSWORD" in source


def test_the_answer_key_is_linked_from_the_reference_index():
    index = (ROOT / "resources" / "reference" / "README.md").read_text(encoding="utf-8")
    assert "(playground-loesungen.md)" in index
