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

# Ausgeklammerte Pfad-Fragmente (historisch / Archiv / Meta / generiert)
EXCLUDE_DIRS = (
    ".agent-memory",
    "docs",
    ".git",
    ".pytest_cache",
    "node_modules",
    "__pycache__",
)
# Ausgeklammerte einzelne Dateien
EXCLUDE_FILES = (
    os.path.join("resources", "_canonical.md"),  # definiert die Liste absichtlich
    os.path.join("tools", "lint_currency.py"),   # enthaelt die Patterns
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
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # in-place prune fuer Performance
        dirnames[:] = [d for d in dirnames if d not in (".git", ".agent-memory", "docs", "node_modules", "__pycache__", ".pytest_cache")]
        for fn in filenames:
            if not fn.endswith(EXTS):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if is_excluded(rel):
                continue
            try:
                for i, line in enumerate(read_lines(full), 1):
                    for label, rx in patterns:
                        if rx.search(line):
                            hits.append((rel.replace(os.sep, "/"), i, label, line.strip()[:120]))
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
