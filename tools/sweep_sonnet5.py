# -*- coding: utf-8 -*-
"""Einmaliger, regex-restringierter Currency-Sweep (WP-02).

Rename-only (kein Pricing — Sonnet 5 hat dieselben 3/15 wie 4.6):
  'Sonnet 4.6'        -> 'Sonnet 5'
  'claude-sonnet-4-6' -> 'claude-sonnet-5'
  'claude-opus-4-7'   -> 'claude-opus-4-8'   (verirrte Beispiel-ID)

Byte-sicher (kein BOM, Zeilenenden bleiben erhalten). Klammert Archiv/docs/.agent-memory aus.
Aufruf (Repo-Root):  python tools/sweep_sonnet5.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    (b"claude-sonnet-4-6", b"claude-sonnet-5"),
    (b"Sonnet 4.6", b"Sonnet 5"),
    (b"claude-opus-4-7", b"claude-opus-4-8"),
]

EXTS = (".md", ".html", ".json", ".txt")
PRUNE_DIRS = (".git", ".agent-memory", "docs", "node_modules", "__pycache__", ".pytest_cache")
EXCLUDE_REL = (
    os.path.join("resources", "review-2026-06-21"),
    os.path.join("resources", "review-2026-07-04"),
    os.path.join("resources", "_canonical.md"),
)


def excluded(rel):
    for e in EXCLUDE_REL:
        if rel == e or rel.startswith(e + os.sep):
            return True
    return False


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        for fn in filenames:
            if not fn.endswith(EXTS):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if excluded(rel):
                continue
            with open(full, "rb") as fh:
                data = fh.read()
            orig = data
            n = 0
            for old, new in REPLACEMENTS:
                c = data.count(old)
                if c:
                    data = data.replace(old, new)
                    n += c
            if data != orig:
                with open(full, "wb") as fh:
                    fh.write(data)
                changed.append((rel.replace(os.sep, "/"), n))
    total = sum(n for _, n in changed)
    print("Sweep fertig: {} Ersetzungen in {} Dateien.".format(total, len(changed)))
    for rel, n in changed:
        print("  {}  ({})".format(rel, n))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
