# -*- coding: utf-8 -*-
"""Drift-Lint fuer den Dynamic Workshop.

Blockt veraltete Model-IDs/Generationen in learner-facing Live-Content.
Kanonische Quelle: resources/_canonical.md. Historische Kontexte (docs/, review-Archive,
.agent-memory) sind bewusst ausgeklammert. Exit 0 = sauber, Exit 1 = Drift gefunden.

Aufruf (aus dem Repo-Root):  python tools/lint_currency.py
"""
import os
import re
import sys

# Repo-Root = Elternordner von tools/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Verbotene Legacy-Tokens (Vorgaenger-/retired Generationen). Muss zu resources/_canonical.md passen.
# Case-insensitive (siehe re.IGNORECASE unten).
FORBIDDEN = [
    r"claude-sonnet-4-6",
    r"sonnet[ -]4\.6",       # 'Sonnet 4.6' / 'sonnet-4.6' / 'SONNET 4.6'
    r"claude-opus-4-7",
    r"claude-3-5-sonnet",    # retired
    r"claude-3-7-sonnet",    # retired
    r"claude-3-5-haiku",     # retired
]

# Zu scannende Endungen
EXTS = (".md", ".html", ".json", ".txt")

# Ausgeklammerte Ordner relativ zum Repo-Root (Historie, Archiv, Meta, Werkzeuge, lokaler Zustand)
EXCLUDE_DIRS = (
    ".agent-memory",
    ".codegraph",
    ".currency",
    ".pi-glla",
    ".superpowers",
    "docs",
    "tools",
    os.path.join("resources", "archive"),
)
# Ordner, die an jeder Stelle uebersprungen werden
PRUNE_ANYWHERE = (".git", "node_modules", "__pycache__", ".pytest_cache")
# Ausgeklammerte einzelne Dateien
EXCLUDE_FILES = (
    os.path.join("resources", "_canonical.md"),  # definiert die Fakten absichtlich
    "HANDOFF.md",  # datierte Agenten-Uebergabe vom 2026-06-21, kein Kursinhalt
)


# Datierte Review-Archive (resources/review-YYYY-MM-DD/...) sind Befunde, kein Kursinhalt.
REVIEW_ARCHIVE = re.compile(r"^resources/review-[^/]+/")


def is_excluded(rel):
    if REVIEW_ARCHIVE.match(rel.replace(os.sep, "/")):
        return True
    rel_norm = rel.replace("/", os.sep)
    for d in EXCLUDE_DIRS:
        if rel_norm.startswith(d + os.sep) or rel_norm == d:
            return True
    for f in EXCLUDE_FILES:
        if rel_norm == f:
            return True
    return False


def live_files(root=ROOT):
    """Yield (rel_posix, full_path) for every live-content file, sorted; shared by lint and currency check."""
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        kept = []
        for name in dirnames:
            rel = name if rel_dir == "." else os.path.join(rel_dir, name)
            if name in PRUNE_ANYWHERE or is_excluded(rel):
                continue
            kept.append(name)
        dirnames[:] = sorted(kept)
        for name in sorted(filenames):
            if not name.endswith(EXTS):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if is_excluded(rel):
                continue
            yield rel.replace(os.sep, "/"), full


def read_lines(full):
    try:
        with open(full, encoding="utf-8-sig") as fh:
            return list(fh)
    except UnicodeDecodeError:
        with open(full, encoding="cp1252") as fh:
            return list(fh)


def main():
    patterns = [(p, re.compile(p, re.IGNORECASE)) for p in FORBIDDEN]
    hits = []
    for rel, full in live_files():
        try:
            for i, line in enumerate(read_lines(full), 1):
                for label, rx in patterns:
                    if rx.search(line):
                        hits.append((rel, i, label, line.strip()[:120]))
        except OSError:
            continue

    if hits:
        print("DRIFT gefunden — {} veraltete Token-Vorkommen in Live-Content:".format(len(hits)))
        for rel, ln, label, snippet in hits:
            print("  {}:{}  [{}]  {}".format(rel, ln, label, snippet))
        print("\nFix: auf die kanonischen IDs aus resources/_canonical.md aktualisieren.")
        return 1
    print("OK — keine veralteten Model-IDs/Generationen in Live-Content.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
