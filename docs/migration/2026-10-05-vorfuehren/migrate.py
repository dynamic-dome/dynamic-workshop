# -*- coding: utf-8 -*-
"""One-off move: every '## Vorführen' section leaves its chapter and becomes a file of the moderation layer.

  python docs/migration/2026-10-05-vorfuehren/migrate.py            # move (run once, on a clean tree)
  python docs/migration/2026-10-05-vorfuehren/migrate.py --check    # prove nothing was lost, against --base

Design: docs/plans/2026-10-05-selbstlern-zuerst-design.md, package P1. The script stays as evidence; after the
move it has nothing left to do. From then on tools/build_library.py keeps the two layers apart.

What it does per chapter with a '## Vorführen' section:
  - cuts the section (boundaries as the project parser sees them: H2 outside code fences),
  - writes it to resources/moderation/vorfuehren/<chapter file> under a header that names the chapter,
  - rewrites relative links for the new folder, drops the chapter-only marker <!-- cockpit:example -->,
  - leaves every other byte of the chapter alone.

--check reads the chapters as they were at --base (git show) and verifies:
  1. each chapter today is exactly the old chapter minus its section,
  2. each demo file carries exactly the words of the old section (link targets and the marker aside),
  3. the word totals match.
Run it directly after the move; later hand edits to chapters are not its business.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import library_model as lm  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

LIBRARY = ROOT / "resources" / "library"
DEMOS = lm.demo_dir(LIBRARY)
SECTION = "Vorführen"
ANCHOR = "vorführen"
LINK = re.compile(r"\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")
DEFAULT_BASE = "991610a"  # last commit before the move


def chapter_files():
    return sorted(p for p in LIBRARY.glob("*.md") if p.name not in lm.GENERATED_NAMES)


def section_span(lines):
    """(start, end) line indices of the section, end exclusive; None if the chapter has none."""
    start, in_fence = None, False
    for i, line in enumerate(lines):
        if lm.FENCE.match(line):
            in_fence = not in_fence
        if in_fence:
            continue
        h2 = lm.H2.match(line)
        if not h2:
            continue
        if start is not None:
            return start, i
        if h2.group(1) == SECTION:
            start = i
    return (start, len(lines)) if start is not None else None


def front_of(text, path):
    front, _ = lm._split_front(path, text)
    return str(front.get("id", "")), str(front.get("title", ""))


def rewrite_links(body, chapter_name, has_demo):
    """Links were written relative to resources/library/; make them work from resources/moderation/vorfuehren/."""
    out, in_fence = [], False

    def fix(match):
        target, title = match.group(1), match.group(2)
        if re.match(r"^[a-z]+:", target):
            return match.group(0)
        file_part, _, fragment = target.partition("#")
        if not file_part:  # anchor inside the chapter the section came from
            return f"](../../library/{chapter_name}#{fragment}{title})"
        if fragment == ANCHOR and file_part in has_demo:  # another chapter's demo: now a sibling file
            return f"]({file_part}{title})"
        new = os.path.relpath(os.path.normpath(LIBRARY / file_part), DEMOS).replace(os.sep, "/")
        return f"]({new}{'#' + fragment if fragment else ''}{title})"

    for line in body.split("\n"):
        if lm.FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append(line if in_fence else LINK.sub(fix, line))
    return "\n".join(out)


def demo_text(chapter_id, title, chapter_name, body, has_demo):
    body = "\n".join(line for line in body.split("\n") if line.strip() != lm.EXAMPLE_MARKER)
    body = re.sub(r"\n{3,}", "\n\n", rewrite_links(body, chapter_name, has_demo)).strip("\n")
    return (f"# Vorführen: {chapter_id} · {title}\n\n"
            f"> Demo und Hinweise für Moderierende zum Kapitel [{chapter_id} · {title}](../../library/{chapter_name}). "
            "Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.\n\n"
            f"{body}\n")


def split_chapter(text):
    """(chapter without the section, section body) or (text, None)."""
    lines = text.split("\n")
    span = section_span(lines)
    if span is None:
        return text, None
    start, end = span
    return "\n".join(lines[:start] + lines[end:]), "\n".join(lines[start + 1:end]).strip("\n")


def move():
    texts = {p: lm._read(p) for p in chapter_files()}
    has_demo = {p.name for p, t in texts.items() if section_span(t.split("\n")) is not None}
    DEMOS.mkdir(parents=True, exist_ok=True)
    for path, text in texts.items():
        rest, body = split_chapter(text)
        if body is None:
            continue
        parsed = lm.parse_chapter(path).sections[SECTION]
        assert parsed == body, f"{path.name}: own cut differs from the project parser"
        chapter_id, title = front_of(text, path)
        (DEMOS / path.name).write_text(demo_text(chapter_id, title, path.name, body, has_demo),
                                       encoding="utf-8", newline="\n")
        path.write_text(rest, encoding="utf-8", newline="\n")
        print(f"verschoben: {path.name} ({len(body.split())} Wörter)")
    print(f"{len(has_demo)} Abschnitte verschoben nach {DEMOS.relative_to(ROOT).as_posix()}/")
    return 0


def words(text):
    """Words of a section, blind to what the move may change: link targets and the chapter-only marker."""
    text = "\n".join(line for line in text.split("\n") if line.strip() != lm.EXAMPLE_MARKER)
    return LINK.sub("]()", text).split()


def check(base):
    problems, total_old, total_new, moved = [], 0, 0, 0
    listing = subprocess.run(["git", "ls-tree", "--name-only", f"{base}:resources/library"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout.split("\n")
    for name in sorted(n for n in listing if n.endswith(".md") and n not in lm.GENERATED_NAMES):
        old = subprocess.run(["git", "show", f"{base}:resources/library/{name}"], cwd=ROOT, capture_output=True,
                             check=True).stdout.decode("utf-8").replace("\r\n", "\n")
        rest, body = split_chapter(old)
        now = lm._read(LIBRARY / name)
        demo = DEMOS / name
        if body is None:
            if now != old:
                problems.append(f"{name}: hatte keinen Abschnitt, ist aber verändert")
            if demo.exists():
                problems.append(f"{name}: Demo-Datei ohne alten Abschnitt")
            continue
        moved += 1
        if now != rest:
            problems.append(f"{name}: Kapitel ist nicht 'alt minus Abschnitt'")
        if not demo.exists():
            problems.append(f"{name}: Demo-Datei fehlt")
            continue
        new_body = lm._read(demo).split("\n", 4)[-1]  # after H1, blank, quote line, blank
        old_words, new_words = words(body), words(new_body)
        total_old += len(old_words)
        total_new += len(new_words)
        if old_words != new_words:
            first = next((i for i, (a, b) in enumerate(zip(old_words, new_words)) if a != b),
                         min(len(old_words), len(new_words)))
            problems.append(f"{name}: Wörter weichen ab bei Wort {first} "
                            f"({old_words[first:first + 4]} gegen {new_words[first:first + 4]})")
    print(f"Basis {base}: {moved} Abschnitte, Wörter alt {total_old}, neu {total_new}")
    for problem in problems:
        print("BEFUND: " + problem)
    print("OK — nichts verloren." if not problems else f"{len(problems)} Befund(e)")
    return 1 if problems else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--base", default=DEFAULT_BASE)
    args = parser.parse_args(argv)
    return check(args.base) if args.check else move()


if __name__ == "__main__":
    sys.exit(main())
