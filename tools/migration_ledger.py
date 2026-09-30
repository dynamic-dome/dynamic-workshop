# -*- coding: utf-8 -*-
"""Snippet ledger for the move to the library: every fenced code block of the old course files (read from the base
commit) must appear unchanged in the new corpus, or be listed with a reason in tools/fixtures/migration-dropped.txt.

  python tools/migration_ledger.py                 # summary over all old files
  python tools/migration_ledger.py --chapter S2.8  # snippets owned by one chapter (docs/migration/ownership.json)
  python tools/migration_ledger.py --missing       # list every missing snippet
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import textwrap
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "ba222d2"
DROPPED = ROOT / "tools" / "fixtures" / "migration-dropped.txt"
OWNERSHIP = ROOT / "docs" / "migration" / "ownership.json"
FENCE = re.compile(r"^\s*(```|~~~)(.*)$")

OLD_FILES = [
    "resources/modules/block-1-foundations.md", "resources/modules/block-2-ecosystem.md",
    "resources/modules/block-3-advanced.md", "resources/demos/block-1-demos.md", "resources/demos/block-2-demos.md",
    "resources/demos/block-3-demos.md", "resources/exercises/block-1-exercises.md",
    "resources/exercises/block-2-exercises.md", "resources/exercises/block-3-exercises.md",
    "resources/cheatsheet.md", "resources/quick-reference.md", "resources/faq.md", "resources/troubleshooting.md",
    "resources/prerequisites.md", "resources/glossary.md", "resources/session-plan.md", "resources/trainer-notes.md",
    "resources/live-3-person-mode.md", "resources/retrieval-recap-bridges.md", "resources/transfer-retention-plan.md",
    "resources/capstone-exit-assessment.md", "resources/security-analogies.md", "resources/workshop-guide.md",
    "WORKSHOP_EINFUEHRUNG.md", "README.md", "HOW-TO-USE.md",
]
NEW_ROOTS = ["resources", "skills", "agents", "commands"]
NEW_FILES = ["README.md", "HOW-TO-USE.md"]


@dataclass(frozen=True)
class Snippet:
    path: str
    line: int
    lang: str
    text: str
    digest: str


def normalize(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    # A fence inside a list item is indented as a whole; moving it to column 0 does not change the snippet.
    return textwrap.dedent("\n".join(lines))


def digest(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()[:16]


def fenced_blocks(text: str):
    """Yield (line_number_of_opening_fence, lang, content). Nested fences of a different marker are content."""
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        match = FENCE.match(lines[i])
        if match:
            marker, lang = match.group(1), match.group(2).strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(marker):
                j += 1
            yield i + 1, lang, "\n".join(lines[i + 1:j])
            i = j + 1
        else:
            i += 1


def git_show(path: str, base: str = BASE) -> str:
    out = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True, text=True,
                         encoding="utf-8", check=False)
    if out.returncode != 0:
        raise FileNotFoundError(f"{base}:{path}: {out.stderr.strip()}")
    return out.stdout


def old_snippets(base: str = BASE) -> list:
    result = []
    for path in OLD_FILES:
        for line, lang, content in fenced_blocks(git_show(path, base)):
            if normalize(content):
                result.append(Snippet(path, line, lang, content, digest(content)))
    return result


def _walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "node_modules")]
        for name in filenames:
            if name.endswith(".md"):
                yield Path(dirpath) / name


def new_digests(root: Path = ROOT, skip_old: bool = True) -> dict:
    """digest -> list of repo-relative files (new corpus: resources/**, skills/**, agents/**, commands/**, root docs)."""
    old = (set(OLD_FILES) - set(NEW_FILES)) if skip_old else set()  # README/HOW-TO-USE are rewritten in place
    found = {}
    files = [root / f for f in NEW_FILES] + [p for r in NEW_ROOTS for p in _walk(root / r)]
    for path in files:
        if not path.exists():
            continue
        rel = path.relative_to(root).as_posix()
        if rel in old:
            continue
        for _, _, content in fenced_blocks(path.read_text(encoding="utf-8")):
            if normalize(content):
                found.setdefault(digest(content), []).append(rel)
    return found


def dropped() -> dict:
    """digest -> reason. Format per line: '<digest> <path>:<line> <reason>' (comments with #)."""
    result = {}
    if DROPPED.exists():
        for raw in DROPPED.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(" ", 2)
            if len(parts) == 3 and parts[2].strip():
                result[parts[0]] = parts[2].strip()
    return result


def ledger(base: str = BASE, root: Path = ROOT):
    snippets = old_snippets(base)
    present = new_digests(root)
    gone = dropped()
    missing = [s for s in snippets if s.digest not in present and s.digest not in gone]
    return snippets, present, gone, missing


def owned_ranges(chapter_id: str):
    packs = json.loads(OWNERSHIP.read_text(encoding="utf-8"))["packs"]
    return packs.get(chapter_id, [])


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--chapter")
    parser.add_argument("--missing", action="store_true")
    args = parser.parse_args(argv)
    snippets, present, gone, missing = ledger()
    if args.chapter:
        ranges = owned_ranges(args.chapter)
        mine = [s for s in snippets if any(r["file"] == s.path and r["start"] <= s.line <= r["end"] for r in ranges)]
        bad = 0
        for s in mine:
            where = present.get(s.digest)
            state = f"ok ({', '.join(sorted(set(where)))})" if where else ("gestrichen: " + gone[s.digest]
                                                                            if s.digest in gone else "FEHLT")
            bad += state == "FEHLT"
            first = normalize(s.text).split("\n", 1)[0][:70]
            print(f"{s.digest} {s.path}:{s.line} [{s.lang or '-'}] {first!r} → {state}")
        print(f"{len(mine)} Snippets im Heimatbereich von {args.chapter}, {bad} fehlen.")
        return 1 if bad else 0
    if args.missing:
        for s in missing:
            print(f"{s.digest} {s.path}:{s.line} {normalize(s.text).split(chr(10), 1)[0][:70]!r}")
    print(f"{len(snippets)} alte Snippets · {len(snippets) - len(missing)} erfasst · {len(missing)} fehlen · "
          f"{len(gone)} begründet gestrichen")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
