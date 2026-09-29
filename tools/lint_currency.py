# -*- coding: utf-8 -*-
"""Currency-Lint fuer den Dynamic Workshop.

Zwei Regeln (Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md):
1. Generationsregel: Modellgenerationen (etwa "Opus 5.5" oder claude-sonnet-5-5) stehen nur in
   resources/_canonical.md. Ausnahme nur mit `version-pinned: <Grund>` in derselben Zeile.
2. Stale-Gate: das Pruefdatum im Kanon ist hoechstens 90 Tage alt (ab 45 Tagen Warnung).
Ausgeklammert: docs/, review-Archive, resources/archive/, .agent-memory, HANDOFF.md, tools/, lokaler Zustand.
Exit 0 = sauber, Exit 1 = Drift oder Kanon zu alt/unlesbar.

Aufruf (aus dem Repo-Root):  python tools/lint_currency.py
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import currency_extract  # noqa: E402

# Repo-Root = Elternordner von tools/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERATION = re.compile(
    r"\b(?:opus|sonnet|haiku|fable|mythos)[ -]?\d+(?:[.-]\d+)?\b"
    r"|\bclaude-(?:opus|sonnet|haiku|fable|mythos)-\d",
    re.IGNORECASE,
)
PIN = re.compile(r"version-pinned:\s*(.*?)\s*(?:-->|\*/|$)")
STALE_WARN_DAYS = 45
STALE_RED_DAYS = 90

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


def is_pinned(line):
    match = PIN.search(line)
    return bool(match) and len(match.group(1).strip()) >= 3


def generation_hits(root=ROOT):
    hits = []
    for rel, full in live_files(root):
        try:
            lines = read_lines(full)
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            match = GENERATION.search(line)
            if match and not is_pinned(line):
                hits.append((rel, number, match.group(0), line.strip()[:120]))
    return hits


def canon_status(canon_path, today):
    """Return (level, message) with level 'ok' | 'warn' | 'red'."""
    try:
        with open(canon_path, encoding="utf-8") as fh:
            checked, _cli = currency_extract.parse_canon_header(fh.read())
    except (OSError, ValueError) as exc:
        return "red", f"Kanon-Prüfdatum nicht lesbar: {exc}"
    age = (today - checked).days
    if age > STALE_RED_DAYS:
        return "red", (f"Kanon zuletzt geprüft {checked} ({age} Tage > {STALE_RED_DAYS}): "
                       "Monatsbericht abarbeiten und Prüfdatum setzen")
    if age > STALE_WARN_DAYS:
        return "warn", f"WARNUNG: Kanon zuletzt geprüft {checked} ({age} Tage > {STALE_WARN_DAYS})"
    return "ok", f"Kanon geprüft {checked} ({age} Tage)"


def main(root=ROOT, today=None):
    today = today or datetime.date.today()
    level, message = canon_status(os.path.join(root, "resources", "_canonical.md"), today)
    print(message)
    hits = generation_hits(root)
    if hits:
        print("DRIFT gefunden — {} Zeilen nennen eine Modellgeneration außerhalb des Kanons:".format(len(hits)))
        for rel, number, token, snippet in hits:
            print("  {}:{}  [{}]  {}".format(rel, number, token, snippet))
        print("\nFix: Alias oder Rolle nennen und auf resources/_canonical.md verweisen; bewusst versioniert nur mit"
              " `version-pinned: <Grund>` in derselben Zeile.")
    if hits or level == "red":
        return 1
    print("OK — keine Modellgeneration außerhalb des Kanons.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
