# Phase 2 — Aktualhaltung: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Der Kurs meldet Drift gegenüber der offiziellen Doku binnen eines Monats selbst, und Modellgenerationen
stehen nur noch im Kanon.

**Architecture:** Reine Parser/Extraktoren (`tools/currency_extract.py`) + ein Ablauf-Skript mit injiziertem Fetcher
(`tools/currency_check.py`, Exit 0/1/2, `SUMMARY`-Zeile) + erweiterter Lint (`tools/lint_currency.py`:
Generationsregel, Stale-Gate, gemeinsame Dateimenge). Ein privater Wrapper außerhalb des Repos startet den Check
monatlich und legt Todos an.

**Tech Stack:** Python 3.12 Standardbibliothek (`urllib`, `re`, `json`, `dataclasses`), pytest, node (nur
`node --check` im Test), Windows-Aufgabenplanung.

**Spec:** `docs/plans/2026-09-29-phase2-aktualhaltung-design.md`

## Global Constraints

- Nur Standardbibliothek; keine neue Abhängigkeit. Tests: `python -m pytest tools -q` aus dem Repo-Root (Baseline 109 grün).
- Tests offline und zeitunabhängig: jedes Datum wird als Parameter übergeben, kein Netzzugriff in pytest.
- Dateien UTF-8 mit LF. Code, Bezeichner, Commit-Messages Englisch; Kursprosa und Berichte Deutsch.
- Öffentliches Repo: keine privaten Pfade, Hostnamen, Namen oder Secrets in Dateien und Commits.
- Commit-Trailer (jeder Commit):
  `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`
- Schwellen (aus der Spec, wörtlich): Lint WARNUNG > 45 Tage, rot > 90 Tage; Retirement rot < 60 Tage;
  Bestätigungs-Todo > 60 Tage; Timeout 30 s je Quelle; Mindestgröße 5 KB je Doku-Seite; Mindestmengen
  Flags 80, Env 150, Deprecations 10, Aliase 3.
- Exit-Codes Check: 0 sauber · 1 rot oder gelb · 2 Quelle/Kanon unbrauchbar. Letzte stdout-Zeile `SUMMARY {json}`.
- Repo-Regel: jede Inhaltsänderung an Modulen/Demos/Exercises zieht `agents/workshop-mentor.md` nach.
- Kein Push, kein Cockpit-Re-Export ohne ausdrückliche Owner-Freigabe (Task 11).
- Keine `\uXXXX`-Escapes in Tool-Aufrufen schreiben (die Harness wandelt sie still in Zeichen um); Umlaute direkt.

## Review Focus

1. **Cockpit-Skript bricht nach dem Sweep** (ein Kommentar oder Anführungszeichen in einem JS-String) → Lernende
   sehen ein leeres Cockpit. Erwartet: Skript parst weiter. Test: `node --check` auf das Inline-Skript (Task 7).
2. **Umlaute im Todo-Text unter der Windows-Aufgabe** → `UnicodeEncodeError` im Kindprozess, kein Todo, still.
   Erwartet: Todo entsteht. Test: Wrapper setzt `PYTHONIOENCODING=utf-8` für `add_todo` (Task 9, privater Teil).
3. **Absturz des Checks ohne `SUMMARY`** endet mit Exit 1 wie „Befunde". Erwartet: Wrapper wertet das als
   Fehlschlag. Test: `decide()` mit Exit 1 ohne Summary (Task 9) und `main()` fängt `OSError` als Exit 2 (Task 4).
4. **Instabile Befund-Schlüssel** erzeugen jeden Monat „neue" Befunde und damit doppelte Todos. Erwartet: gleicher
   Befund → „weiterhin offen". Test: zweiter identischer Lauf hat `new_red == 0` (Task 4).
5. **Doku liefert HTML statt Markdown mit Status 200** (Fehler- oder Challenge-Seite). Erwartet: Exit 2, nicht
   „Flag fehlt". Test: HTML-Body → `SourceError` (Task 4).

---

## File Structure

| Datei | Verantwortung | Task |
|---|---|---|
| `tools/lint_currency.py` | Dateimenge (`live_files`), Generationsregel, Stale-Gate, CLI | 1, 6 |
| `tools/currency_extract.py` | Reine Funktionen: Kurs-Bezeichner, Quellen-Parser, Kanon-Parser | 2, 3 |
| `tools/currency_check.py` | Prüfungen, `run()` mit injiziertem Fetcher, Bericht, Zustand, CLI | 4 |
| `tools/currency_exceptions.txt` | Ausnahmen `bezeichner \| grund` (darf nur schrumpfen) | 4, 8 |
| `tools/test_lint_currency.py` | Tests Dateimenge + Lint | 1, 6 |
| `tools/test_currency_extract.py` | Tests Extraktion + Parser + Gegenprobe | 2, 3 |
| `tools/test_currency_check.py` | Tests Ablauf, Stufen, Fail-closed, Zustand, CLI, Kanon-Struktur, Ausnahme-Ratchet | 4, 5, 8 |
| `tools/fixtures/currency/*.md` | Gegenprobe-Auszüge aus Vorher-Fassungen | 3 |
| `resources/_canonical.md` | Kanon: Prüfdatum, Modelltabelle, Aliase, Effort, Quellen | 5 |
| Kursdateien (12) | Sweep auf Aliase/Kanon-Verweise | 7 |
| `.gitignore` | `.currency/` | 1 |
| Privater Wrapper (außerhalb des Repos) | Monatslauf, Todos, Windows-Aufgabe | 9 |

---

### Task 1: Gemeinsame Dateimenge für Lint und Check

**Files:**
- Modify: `tools/lint_currency.py` (Konstanten `EXCLUDE_DIRS`/`EXCLUDE_FILES`, neue `live_files()`, `main()` nutzt sie)
- Modify: `.gitignore`
- Create: `tools/test_lint_currency.py`

**Interfaces:**
- Produces: `lint_currency.live_files(root: str = ROOT) -> Iterator[tuple[str, str]]` liefert `(rel_posix, full_path)`
  sortiert; `lint_currency.read_lines(full: str) -> list[str]`; `lint_currency.is_excluded(rel: str) -> bool`.

- [ ] **Step 1: Write the failing test**

`tools/test_lint_currency.py`:

```python
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
        "workshop-playground/node_modules/pkg/readme.md": "x",
        "resources/demo.py": "x",
    })

    rels = [rel for rel, _full in lint.live_files(str(root))]

    assert rels == ["README.md", "agents/mentor.md", "resources/modules/m.md"]


def test_currency_state_dir_is_git_ignored():
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".currency/" in lines
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tools/test_lint_currency.py -q`
Expected: FAIL — `AttributeError: module 'lint_currency' has no attribute 'live_files'` und `.currency/` fehlt.

- [ ] **Step 3: Write minimal implementation**

In `tools/lint_currency.py` die beiden Tupel `EXCLUDE_DIRS` und `EXCLUDE_FILES` ersetzen und `live_files()` nach
`is_excluded()` einfügen:

```python
# Ausgeklammerte Ordner relativ zum Repo-Root (Historie, Archiv, Meta, Werkzeuge, lokaler Zustand)
EXCLUDE_DIRS = (
    ".agent-memory",
    ".codegraph",
    ".currency",
    ".pi-glla",
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
```

```python
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
```

In `main()` den `os.walk`-Block ersetzen durch:

```python
    for rel, full in live_files():
        try:
            for i, line in enumerate(read_lines(full), 1):
                for label, rx in patterns:
                    if rx.search(line):
                        hits.append((rel, i, label, line.strip()[:120]))
        except OSError:
            continue
```

In `.gitignore` nach dem Block `# Local agent/tool state` ergänzen:

```
.currency/
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tools -q` → Expected: 111 passed.
Run: `python tools/lint_currency.py` → Expected: `OK — keine veralteten Model-IDs/Generationen in Live-Content.`

- [ ] **Step 5: Commit**

```bash
git add tools/lint_currency.py tools/test_lint_currency.py .gitignore
git commit -m "refactor(tools): share one live-content file set for currency checks"
```

---

### Task 2: Kurs-Bezeichner extrahieren

**Files:**
- Create: `tools/currency_extract.py`
- Create: `tools/test_currency_extract.py`

**Interfaces:**
- Produces:
  - `Hit(kind: str, value: str, path: str, line: int)` (frozen dataclass); `kind` ∈ `flag`, `env`, `hook_event`,
    `model_id`, `alias`, `permission_mode`.
  - `extract_course_hits(path: str, text: str) -> tuple[list[Hit], int]` — Treffer und Zahl nicht parsebarer
    ```` ```json ````-Blöcke.
  - `logical_lines(text) -> Iterator[tuple[int, str]]`, `command_segments(line) -> list[str]`.
  - Regexe `FLAG`, `ENV`, `MODEL_ID` (von Task 3/4 wiederverwendet).

- [ ] **Step 1: Write the failing tests**

`tools/test_currency_extract.py`:

```python
"""Extraction and parsing for the currency check (design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md)."""
import datetime as dt
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FENCE = "`" * 3


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cx = _load("currency_extract")


def values(text, kind):
    hits, _unparsed = cx.extract_course_hits("x.md", text)
    return sorted({h.value for h in hits if h.kind == kind})


def test_flags_after_a_claude_call_are_collected():
    assert values("claude -p --max-turns 3 --output-format json", "flag") == ["--max-turns", "--output-format"]


def test_shell_continuation_lines_are_joined():
    text = "claude --bare -p \"x\" \\\n  --max-budget-usd 0.50 \\\n  --output-format json\n"
    assert values(text, "flag") == ["--bare", "--max-budget-usd", "--output-format"]


def test_js_string_continuation_in_the_cockpit_is_joined():
    line = 'example: "claude --bare -p \\"x\\" \\\\\\n  --output-format json \\\\\\n  < diff.patch\\n\\n# B\\ngit log --oneline"'
    assert values(line, "flag") == ["--bare", "--output-format"]


def test_inline_code_starting_with_a_flag_is_collected():
    assert values("Pass `--metadata '{\"a\":1}'` to tag runs.", "flag") == ["--metadata"]


def test_foreign_flags_in_prose_css_and_pipes_are_ignored():
    text = (
        "Use git checkout --orphan here.\n"
        "  --accent-glow: #fff; color: var(--accent-glow);\n"
        "claude -p x | jq --raw-output .result\n"
        "cp ~/.claude/settings.json --target backup\n"
        "npx @anthropic-ai/claude-code --version-check\n"
    )
    assert values(text, "flag") == []


def test_camel_case_and_single_letter_flags_are_kept_whole():
    assert values("claude -p --allowedTools Read --x", "flag") == ["--allowedTools", "--x"]
    assert values("Use `--disallowedTools` and `--x`.", "flag") == ["--disallowedTools", "--x"]


def test_env_model_ids_aliases_and_modes():
    text = (
        "export ANTHROPIC_MODEL=x CLAUDE_CODE_OAUTH_TOKEN=y SLACK_BOT_TOKEN=z\n"
        "claude --model opus --permission-mode acceptEdits\n"
        "claude --model claude-opus-4-8 -p x\n"
        "model: sonnet\n"
        '{"model": "haiku", "defaultMode": "plan"}\n'
        "permissionMode: dontAsk\n"
        "Default model: the best one\n"
    )
    assert values(text, "env") == ["ANTHROPIC_MODEL", "CLAUDE_CODE_OAUTH_TOKEN"]
    assert values(text, "model_id") == ["claude-opus-4-8"]
    assert values(text, "alias") == ["haiku", "opus", "sonnet"]
    assert values(text, "permission_mode") == ["acceptEdits", "dontAsk", "plan"]


def test_hook_events_come_from_parsable_json_fences():
    text = (
        f"{FENCE}json\n"
        '{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command"}]}], "Stop": []}}\n'
        f"{FENCE}\n\n"
        f"{FENCE}json\n"
        "{ this is not json }\n"
        f"{FENCE}\n"
    )
    hits, unparsed = cx.extract_course_hits("x.md", text)
    assert sorted(h.value for h in hits if h.kind == "hook_event") == ["PreToolUse", "Stop"]
    assert unparsed == 1
    assert {h.line for h in hits if h.kind == "hook_event"} == {1}


def test_hits_carry_path_and_first_line_of_a_logical_line():
    hits, _ = cx.extract_course_hits("m/a.md", "intro\nclaude \\\n  --bare -p x\n")
    assert [(h.path, h.line, h.value) for h in hits] == [("m/a.md", 2, "--bare")]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tools/test_currency_extract.py -q`
Expected: FAIL — `FileNotFoundError` / `No such file` für `currency_extract.py`.

- [ ] **Step 3: Write minimal implementation**

`tools/currency_extract.py`:

```python
# -*- coding: utf-8 -*-
"""Pure extraction and parsing for the currency check: no network, no filesystem.

Consumers: tools/currency_check.py (monthly drift check) and tools/lint_currency.py (canon header).
Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md
"""
import json
import re
from dataclasses import dataclass

FLAG = re.compile(r"(?<![\w-])--[A-Za-z](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?![\w-])")
ENV = re.compile(r"\b(?:ANTHROPIC|CLAUDE)_[A-Z0-9_]*[A-Z0-9]\b")
MODEL_ID = re.compile(r"\bclaude-(?:opus|sonnet|haiku|fable|mythos)-\d+(?:-\d+)*\b")
INLINE_FLAG = re.compile(r"`(--[A-Za-z](?:[A-Za-z0-9-]*[A-Za-z0-9])?)(?![\w-])[^`]*`")
# "claude" as a command word: not ~/.claude/, not claude-code, not @anthropic-ai/claude-...
CLAUDE_CALL = re.compile(r"(?<![\w./@-])claude\b(?![./-])")
MODEL_VALUE = re.compile(
    r"--model[ =]+[\"']?([A-Za-z0-9][A-Za-z0-9.\[\]-]*)"
    r"|^\s*model:\s*[\"']?([A-Za-z0-9][A-Za-z0-9.\[\]-]*)"
    r"|\"model\"\s*:\s*\"([A-Za-z0-9][A-Za-z0-9.\[\]-]*)\""
)
PERMISSION_MODE = re.compile(
    r"--permission-mode[ =]+[\"']?([A-Za-z]+)"
    r"|\"defaultMode\"\s*:\s*\"([A-Za-z]+)\""
    r"|^\s*permissionMode:\s*[\"']?([A-Za-z]+)"
)
JSON_FENCE = re.compile(r"^```json[ \t]*\n(.*?)^```", re.S | re.M)
SEGMENT_BREAK = re.compile(r"\|\||&&|\||;")


@dataclass(frozen=True)
class Hit:
    kind: str
    value: str
    path: str
    line: int


def logical_lines(text):
    """Yield (first_line_no, line) with shell continuations (backslash at line end) joined."""
    start, parts = None, []
    for number, raw in enumerate(text.splitlines(), 1):
        if start is None:
            start = number
        body = raw.rstrip()
        if body.endswith("\\") and not body.endswith("\\\\"):
            parts.append(body[:-1])
            continue
        parts.append(raw)
        yield start, " ".join(parts)
        start, parts = None, []
    if parts:
        yield start, " ".join(parts)


def command_segments(line):
    """Split a logical line into shell commands: JS/JSON "\\n" escapes, pipes, &&, ;."""
    merged, carry = [], ""
    for piece in line.split("\\n"):
        body = piece.rstrip()
        if body.endswith("\\\\"):  # escaped backslash before \n = continuation inside a JS string
            carry += body[:-2] + " "
            continue
        merged.append(carry + piece)
        carry = ""
    if carry:
        merged.append(carry)
    segments = []
    for chunk in merged:
        segments.extend(SEGMENT_BREAK.split(chunk))
    return segments


def _first(groups):
    return next(g for g in groups if g)


def _hook_keys(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "hooks" and isinstance(value, dict):
                yield from value.keys()
            yield from _hook_keys(value)
    elif isinstance(node, list):
        for item in node:
            yield from _hook_keys(item)


def hook_events_from_json_fences(text):
    """Return ([(event, fence_line)], unparsed_block_count) for every ```json block in text."""
    events, unparsed = [], 0
    for match in JSON_FENCE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        try:
            data = json.loads(match.group(1))
        except ValueError:
            unparsed += 1
            continue
        events.extend((name, line) for name in _hook_keys(data))
    return events, unparsed


def extract_course_hits(path, text):
    """Identifiers the course teaches, with location. Returns (hits, unparsed_json_blocks)."""
    hits = []
    for number, line in logical_lines(text):
        for segment in command_segments(line):
            call = CLAUDE_CALL.search(segment)
            if call:
                hits.extend(Hit("flag", f, path, number) for f in FLAG.findall(segment[call.end():]))
        hits.extend(Hit("flag", f, path, number) for f in INLINE_FLAG.findall(line))
        hits.extend(Hit("env", e, path, number) for e in ENV.findall(line))
        hits.extend(Hit("model_id", m, path, number) for m in MODEL_ID.findall(line))
        for groups in MODEL_VALUE.findall(line):
            value = _first(groups)
            if not value.startswith("claude-"):
                hits.append(Hit("alias", value, path, number))
        hits.extend(Hit("permission_mode", _first(g), path, number) for g in PERMISSION_MODE.findall(line))
    events, unparsed = hook_events_from_json_fences(text)
    hits.extend(Hit("hook_event", name, path, line) for name, line in events)
    return hits, unparsed
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tools/test_currency_extract.py -q` → Expected: 9 passed.
Falls `test_js_string_continuation_in_the_cockpit_is_joined` scheitert: `repr()` der Testzeile ausgeben und mit einer
echten Cockpit-Zeile vergleichen (`grep -n "claude --bare -p" resources/claude-code-workshop-ui.html`); der Test
muss die echte Dateiform abbilden, nicht umgekehrt.

- [ ] **Step 5: Commit**

```bash
git add tools/currency_extract.py tools/test_currency_extract.py
git commit -m "feat(tools): extract the identifiers the course teaches"
```

---

### Task 3: Quellen- und Kanon-Parser, Gegenprobe

**Files:**
- Modify: `tools/currency_extract.py` (anhängen)
- Modify: `tools/test_currency_extract.py` (anhängen)
- Create: `tools/fixtures/currency/cheatsheet-before-ee52d54.md`, `tools/fixtures/currency/block-1-before-sweep.md`

**Interfaces:**
- Consumes: `FLAG`, `ENV`, `extract_course_hits` aus Task 2.
- Produces:
  - `parse_date(text) -> date | None`
  - `DepRow(model_id, status, retirement)`; `parse_deprecations(text) -> dict[str, DepRow]`
  - `parse_aliases(text) -> set[str]`; `parse_permission_modes(modes_text, cli_text="") -> set[str]`
    (Tabellen in permission-modes.md inkl. verlinkter Zellen + Werte der `--permission-mode`-Zeile in cli-reference.md)
  - `parse_canon_header(text) -> tuple[date, str]` (raises `ValueError`)
  - `CanonModel(name, model_id, alias, tier, status, retirement)`; `parse_canon_models(text) -> list[CanonModel]`
  - `parse_canon_sources(text) -> dict[str, list[str]]` mit Schlüsseln `Doku`, `CLI-Version`, `Changelog`
  - `version_tuple(v: str) -> tuple[int, ...]`; `changelog_since(text, since) -> list[tuple[str, str]]`
  - `model_family_version(model_id) -> tuple[str, tuple[int, ...]]`
  - `doc_identifiers(union) -> dict[str, set[str]]` (`flag`, `env`)
  - `exists_in_docs(kind, value, union, aliases, modes) -> bool`
  - `normalize_cockpit(text) -> str`; `parse_exceptions(text) -> dict[str, str]`

- [ ] **Step 1: Create the Gegenprobe fixtures from git history**

```bash
{ echo "<!-- Auszug aus: git show ee52d54^:resources/cheatsheet.md (Zeile 412; H-14, vor dem CI-Auth-Fix) -->"; git show ee52d54^:resources/cheatsheet.md | sed -n 410,413p; } > tools/fixtures/currency/cheatsheet-before-ee52d54.md
{ echo "<!-- Auszug aus: git show 10c7c96:resources/modules/block-1-foundations.md (Zeilen 243-247; vor dem Modell-Sweep) -->"; git show 10c7c96:resources/modules/block-1-foundations.md | sed -n 243,247p; } > tools/fixtures/currency/block-1-before-sweep.md
grep -c "CLAUDE_MODEL" tools/fixtures/currency/cheatsheet-before-ee52d54.md
grep -c "claude-opus-4-8" tools/fixtures/currency/block-1-before-sweep.md
```

Expected: beide `grep -c` ≥ 1. Wenn nicht: Zeilennummern per `git show … | grep -n` neu bestimmen.

- [ ] **Step 2: Write the failing tests** (an `tools/test_currency_extract.py` anhängen)

```python
DEPRECATIONS = """
## Model status

| API model name             | Current state | Deprecated        | Tentative retirement date          |
| :------------------------- | :------------ | :---------------- | :--------------------------------- |
| claude-opus-5-5            | Active        | N/A               | Not sooner than September 22, 2027 |
| claude-haiku-4-5-20251001  | Active        | N/A               | Not sooner than October 15, 2026   |
| claude-opus-4-1-20250805   | Retired       | June 5, 2026      | August 5, 2026                     |

## History

| Retirement date | Deprecated model | Replacement |
| --- | --- | --- |
| claude-3-opus | x | y |
"""

CANON = """# Kanon

Geprüft: 2026-09-29 · CLI 2.1.284

| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |
|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | `claude-opus-5-5` | `opus` | Opus | Active | Not sooner than September 22, 2027 | 1M | 4 | 20 | Default |

## Quellen

- Doku: https://code.claude.com/docs/en/cli-reference.md
- Doku: https://platform.claude.com/docs/en/about-claude/model-deprecations.md
- CLI-Version: https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- Changelog: https://code.claude.com/docs/en/changelog.md
"""


def test_parse_date_handles_retirement_texts():
    assert cx.parse_date("Not sooner than October 15, 2026") == dt.date(2026, 10, 15)
    assert cx.parse_date("August 5, 2026") == dt.date(2026, 8, 5)
    assert cx.parse_date("To be announced") is None
    assert cx.parse_date("N/A") is None


def test_parse_deprecations_reads_only_the_status_table():
    rows = cx.parse_deprecations(DEPRECATIONS)
    assert sorted(rows) == ["claude-haiku-4-5-20251001", "claude-opus-4-1-20250805", "claude-opus-5-5"]
    assert rows["claude-opus-4-1-20250805"].status == "Retired"
    assert rows["claude-haiku-4-5-20251001"].retirement == "Not sooner than October 15, 2026"


def test_parse_aliases_and_permission_modes():
    aliases = cx.parse_aliases("| Model alias | Behavior |\n| - | - |\n| **`default`** | x |\n| **`sonnet[1m]`** | y |\n")
    assert aliases == {"default", "sonnet[1m]"}
    modes = cx.parse_permission_modes(
        "| Mode | x |\n| - | - |\n| `default` | a |\n| [`plan`](#plan-mode) | b |\n"
        "| `default`, `acceptEdits` | c |\n| `--flag` | d |\n",
        "| `--permission-mode` | Accepts `default`, `plan`, or `manual` | `claude --permission-mode plan` |\n"
        "| `claude` | start |\n",
    )
    assert modes == {"default", "plan", "acceptEdits", "manual"}


def test_canon_header_models_and_sources():
    assert cx.parse_canon_header(CANON) == (dt.date(2026, 9, 29), "2.1.284")
    [model] = cx.parse_canon_models(CANON)
    assert (model.model_id, model.alias, model.tier, model.retirement) == (
        "claude-opus-5-5", "opus", "Opus", "Not sooner than September 22, 2027")
    sources = cx.parse_canon_sources(CANON)
    assert len(sources["Doku"]) == 2 and len(sources["CLI-Version"]) == 1 and len(sources["Changelog"]) == 1


def test_canon_parsers_fail_closed():
    with pytest.raises(ValueError):
        cx.parse_canon_header("# Kanon ohne Prüfdatum\n")
    with pytest.raises(ValueError):
        cx.parse_canon_models("# Kanon ohne Tabelle\n")
    with pytest.raises(ValueError):
        cx.parse_canon_sources(CANON.replace("- Changelog: https://code.claude.com/docs/en/changelog.md\n", ""))


def test_changelog_since_returns_only_newer_entries():
    text = (
        '<Update label="2.1.286" description="a">\n  * Added --foo\n  * Fixed bar\n</Update>\n'
        '<Update label="2.1.285" description="b">\n  * Removed --baz\n</Update>\n'
        '<Update label="2.1.284" description="c">\n  * Old entry\n</Update>\n'
    )
    assert cx.changelog_since(text, "2.1.285") == [("2.1.286", "Added --foo"), ("2.1.286", "Fixed bar")]
    assert cx.changelog_since(text, "2.1.286") == []
    with pytest.raises(ValueError):
        cx.changelog_since(text, "2.1.200")


def test_model_family_version_ignores_date_suffix():
    assert cx.model_family_version("claude-haiku-4-5-20251001") == ("haiku", (4, 5))
    assert cx.model_family_version("claude-opus-5-5") == ("opus", (5, 5))
    assert cx.model_family_version("claude-fable-5") == ("fable", (5,))


def test_exists_in_docs_respects_identifier_boundaries():
    union = "Use `--max-turns-total` or `ANTHROPIC_MODEL`. See claude-haiku-4-5-20251001."
    assert not cx.exists_in_docs("flag", "--max-turns", union, set(), set())
    assert cx.exists_in_docs("env", "ANTHROPIC_MODEL", union, set(), set())
    assert not cx.exists_in_docs("model_id", "claude-haiku-4-5", union, set(), set())
    assert cx.exists_in_docs("alias", "opus", "", {"opus"}, set())
    assert cx.exists_in_docs("permission_mode", "plan", "", set(), {"plan"})


def test_doc_identifiers_collects_flags_and_env():
    ids = cx.doc_identifiers("`--bare` and `--max-turns`; set ANTHROPIC_API_KEY or CLAUDE_CODE_USE_BEDROCK")
    assert ids == {"flag": {"--bare", "--max-turns"}, "env": {"ANTHROPIC_API_KEY", "CLAUDE_CODE_USE_BEDROCK"}}


def test_normalize_cockpit_drops_provenance_and_crlf():
    course = "<!doctype html>\n<p>x</p>\n"
    live = "<!doctype html>\r\n<!-- Quelle: dynamic_workshop/resources/claude-code-workshop-ui.html · Stand 2026-09-29 -->\r\n<p>x</p>\r\n"
    assert cx.normalize_cockpit(course) == cx.normalize_cockpit(live)


def test_parse_exceptions_requires_a_reason():
    assert cx.parse_exceptions("# Kommentar\n\n--orphan | git-Flag in Übung 1.3\n") == {"--orphan": "git-Flag in Übung 1.3"}
    with pytest.raises(ValueError):
        cx.parse_exceptions("--orphan\n")
    with pytest.raises(ValueError):
        cx.parse_exceptions("--orphan | ok\n")


def test_gegenprobe_finds_known_wrong_identifiers_in_old_course_text():
    old_cheatsheet = (ROOT / "tools/fixtures/currency/cheatsheet-before-ee52d54.md").read_text(encoding="utf-8")
    hits, _ = cx.extract_course_hits("cheatsheet.md", old_cheatsheet)
    assert "CLAUDE_MODEL" in {h.value for h in hits if h.kind == "env"}
    assert not cx.exists_in_docs("env", "CLAUDE_MODEL", "| `ANTHROPIC_MODEL` | model |", set(), set())

    old_block1 = (ROOT / "tools/fixtures/currency/block-1-before-sweep.md").read_text(encoding="utf-8")
    hits, _ = cx.extract_course_hits("block-1.md", old_block1)
    assert "claude-opus-4-8" in {h.value for h in hits if h.kind == "model_id"}
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python -m pytest tools/test_currency_extract.py -q`
Expected: FAIL — `AttributeError: module 'currency_extract' has no attribute 'parse_date'` (u. a.).

- [ ] **Step 4: Write minimal implementation** (an `tools/currency_extract.py` anhängen; `import datetime as dt`
  oben zu den Imports)

```python
MONTHS = {
    name: number for number, name in enumerate(
        ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"], 1)
}
DATE_TEXT = re.compile(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})")
CANON_HEADER = re.compile(r"^Geprüft:\s*(\d{4}-\d{2}-\d{2})\s*[·|]\s*CLI\s+(\d+\.\d+\.\d+)\s*$", re.M)
CANON_TABLE_HEAD = re.compile(r"^\|\s*Modell\s*\|\s*ID\s*\|\s*Alias\s*\|\s*Tier\s*\|\s*Status\s*\|\s*Retirement[^|]*\|.*$", re.M)
DEPRECATIONS_HEAD = re.compile(r"^\|\s*API model name\s*\|\s*Current state\s*\|.*$", re.M)
SOURCE_LINE = re.compile(r"^- (Doku|CLI-Version|Changelog):\s*(https://\S+)\s*$", re.M)
ALIAS_ROW = re.compile(r"^\|\s*\*\*`([^`]+)`\*\*\s*\|", re.M)
MODE_ROW = re.compile(r"^\|\s*((?:\[?`[A-Za-z]+`\]?(?:\([^)]*\))?(?:,\s*)?)+)\s*\|", re.M)
MODE_FLAG_ROW = re.compile(r"^\|\s*`--permission-mode`\s*\|(.*)$", re.M)
UPDATE = re.compile(r'^<Update label="(\d+\.\d+\.\d+)"', re.M)
PROVENANCE = re.compile(r"^<!-- Quelle: .*claude-code-workshop-ui\.html.*-->\s*$")


@dataclass(frozen=True)
class DepRow:
    model_id: str
    status: str
    retirement: str


@dataclass(frozen=True)
class CanonModel:
    name: str
    model_id: str
    alias: str
    tier: str
    status: str
    retirement: str


def parse_date(text):
    match = DATE_TEXT.search(text or "")
    if not match or match.group(1) not in MONTHS:
        return None
    return dt.date(int(match.group(3)), MONTHS[match.group(1)], int(match.group(2)))


def _table_rows(text, head_match):
    """Cells of every row after the header and separator line, until the table ends."""
    rows = []
    for line in text[head_match.start():].splitlines()[2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def parse_deprecations(text):
    head = DEPRECATIONS_HEAD.search(text)
    if not head:
        return {}
    rows = {}
    for cells in _table_rows(text, head):
        if len(cells) >= 4 and cells[0].startswith("claude-"):
            rows[cells[0]] = DepRow(cells[0], cells[1], cells[3])
    return rows


def parse_aliases(text):
    return set(ALIAS_ROW.findall(text))


def parse_permission_modes(modes_text, cli_text=""):
    """Mode names from the mode tables (linked cells too) plus every value the --permission-mode row accepts."""
    modes = set()
    for match in MODE_ROW.finditer(modes_text):
        modes.update(re.findall(r"`([A-Za-z]+)`", match.group(1)))
    for match in MODE_FLAG_ROW.finditer(cli_text):
        modes.update(re.findall(r"`([A-Za-z]+)`", match.group(1)))
    return modes


def parse_canon_header(text):
    match = CANON_HEADER.search(text)
    if not match:
        raise ValueError("Kanon: Zeile 'Geprüft: YYYY-MM-DD · CLI X.Y.Z' fehlt oder ist unlesbar")
    return dt.date.fromisoformat(match.group(1)), match.group(2)


def parse_canon_models(text):
    head = CANON_TABLE_HEAD.search(text)
    if not head:
        raise ValueError("Kanon: Modelltabelle fehlt")
    models = []
    for cells in _table_rows(text, head):
        if len(cells) < 6:
            raise ValueError(f"Kanon: Tabellenzeile unvollständig: {cells}")
        models.append(CanonModel(cells[0], cells[1].strip("`"), cells[2].strip("`"), cells[3], cells[4], cells[5]))
    if not models:
        raise ValueError("Kanon: Modelltabelle leer")
    return models


def parse_canon_sources(text):
    sources = {"Doku": [], "CLI-Version": [], "Changelog": []}
    for kind, url in SOURCE_LINE.findall(text):
        sources[kind].append(url)
    if not sources["Doku"] or len(sources["CLI-Version"]) != 1 or len(sources["Changelog"]) != 1:
        raise ValueError("Kanon: Quellenliste unvollständig (Doku, genau eine CLI-Version, genau ein Changelog)")
    return sources


def version_tuple(version):
    return tuple(int(part) for part in version.split("."))


def changelog_since(text, since):
    """Entries (version, line) of every release newer than `since`; ValueError if `since` is not listed."""
    marks = [(m.start(), m.group(1)) for m in UPDATE.finditer(text)]
    since_t = version_tuple(since)
    if since_t not in {version_tuple(v) for _pos, v in marks}:
        raise ValueError(f"Changelog: Version {since} nicht gefunden")
    entries = []
    for index, (pos, version) in enumerate(marks):
        if version_tuple(version) <= since_t:
            continue
        end = marks[index + 1][0] if index + 1 < len(marks) else len(text)
        for line in text[pos:end].splitlines()[1:]:
            stripped = line.strip()
            if stripped.startswith("* "):
                entries.append((version, stripped[2:]))
    return entries


def model_family_version(model_id):
    parts = model_id.split("-")
    return parts[1], tuple(int(p) for p in parts[2:] if p.isdigit() and len(p) < 8)


def doc_identifiers(union):
    return {"flag": set(FLAG.findall(union)), "env": set(ENV.findall(union))}


def exists_in_docs(kind, value, union, aliases, modes):
    if kind == "alias":
        return value in aliases
    if kind == "permission_mode":
        return value in modes
    return re.search(r"(?<![\w-])" + re.escape(value) + r"(?![\w-])", union) is not None


def normalize_cockpit(text):
    lines = text.replace("\r\n", "\n").split("\n")
    return "\n".join(line for line in lines if not PROVENANCE.match(line))


def parse_exceptions(text):
    entries = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        value, sep, reason = line.partition("|")
        if not sep or len(reason.strip()) < 3:
            raise ValueError(f"Ausnahme Zeile {number}: Format 'bezeichner | grund' (Grund mindestens 3 Zeichen)")
        entries[value.strip()] = reason.strip()
    return entries
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tools/test_currency_extract.py -q` → Expected: 21 passed.

- [ ] **Step 6: Commit**

```bash
git add tools/currency_extract.py tools/test_currency_extract.py tools/fixtures/currency/
git commit -m "feat(tools): parse canon, deprecations, aliases and changelog for the currency check"
```

---

### Task 4: Der Check — Prüfungen, Ablauf, Bericht, Zustand

**Files:**
- Create: `tools/currency_check.py`
- Create: `tools/currency_exceptions.txt`
- Create: `tools/test_currency_check.py`

**Interfaces:**
- Consumes: alles aus Task 2/3; `lint_currency.live_files`, `lint_currency.read_lines` (Task 1).
- Produces:
  - `SourceError(Exception)`; `Fetched(url, final_url, text)`; `Finding(level, key, text, where=())`
  - `RunResult` mit `exit_code, findings, state, sources, unparsed_json, canon_checked, canon_age_days, cli_canon, cli_latest`
  - `run(*, canon_text, course, exceptions_text, fetcher, today, previous_state, cockpit_text=None, cockpit_url=None) -> RunResult`
  - `render_report(result, *, today, previous_state) -> str`; `summary(result, previous_state, report_path) -> dict`
  - `main(argv=None) -> int`; CLI `python tools/currency_check.py [--today D] [--cockpit-url U] [--state-dir P]`
  - `SUMMARY`-JSON-Schlüssel: `exit, red, yellow, new_red, new_yellow, canon_checked, canon_age_days, report`
    (bei Exit 2: `exit, error`).

- [ ] **Step 1: Write the failing tests**

`tools/test_currency_check.py`:

```python
"""Currency check flow (design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md). Offline, fixed dates."""
import datetime as dt
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cc = _load("currency_check")
TODAY = dt.date(2026, 9, 29)
BASE = "https://docs.test/"
PAD = "\n" + "lorem ipsum " * 500
DOCS = ["cli-reference.md", "env-vars.md", "model-deprecations.md", "model-config.md", "permission-modes.md"]
OPUS = ("Claude Opus 5.5", "claude-opus-5-5", "opus", "Opus", "Active", "Not sooner than September 22, 2027")


def canon(checked="2026-09-29", cli="2.1.284", rows=(OPUS,), docs=DOCS):
    table = "\n".join(f"| {n} | `{i}` | `{a}` | {t} | {s} | {r} | 1M | 4 | 20 | Rolle |" for n, i, a, t, s, r in rows)
    listed = "\n".join(f"- Doku: {BASE}{d}" for d in docs)
    return (
        f"# Kanon\n\nGeprüft: {checked} · CLI {cli}\n\n"
        "| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n" + table + "\n\n## Quellen\n\n" + listed +
        f"\n- CLI-Version: https://npm.test/latest\n- Changelog: {BASE}changelog.md\n"
    )


def dep_table(extra=()):
    rows = [("claude-opus-5-5", "Active", "N/A", "Not sooner than September 22, 2027")]
    rows += [(f"claude-opus-4-{i}", "Active", "N/A", "Not sooner than May 28, 2027") for i in range(1, 10)]
    rows += list(extra)
    body = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows)
    return "| API model name | Current state | Deprecated | Tentative retirement date |\n| --- | --- | --- | --- |\n" + body + "\n" + PAD


def changelog(entries=("Added foo",)):
    new = "\n".join(f"  * {e}" for e in entries)
    return (f'<Update label="2.1.285" description="x">\n{new}\n</Update>\n'
            '<Update label="2.1.284" description="y">\n  * Old\n</Update>\n' + "z" * 100_000)


def pages(**override):
    result = {
        BASE + "cli-reference.md": "# CLI\n" + "\n".join(f"| `--flag-{i}` | x |" for i in range(90))
        + "\n| `--max-turns` | x |\n| `--model` | x |" + PAD,
        BASE + "env-vars.md": "# Env\n" + "\n".join(f"| `ANTHROPIC_VAR_{i}` | x |" for i in range(160))
        + "\n| `ANTHROPIC_MODEL` | x |" + PAD,
        BASE + "model-deprecations.md": dep_table(),
        BASE + "model-config.md": "| Model alias | Behavior |\n| - | - |\n| **`default`** | x |\n| **`opus`** | x |\n"
        "| **`sonnet`** | x |\n| **`haiku`** | x |\n" + PAD,
        BASE + "permission-modes.md": "| Mode | x |\n| - | - |\n| `default` | x |\n| `acceptEdits` | x |\n"
        "| `plan` | x |\n| `auto` | x |\n| `dontAsk` | x |\n| `bypassPermissions` | x |\n" + PAD + "\nPreToolUse Stop\n",
        "https://npm.test/latest": json.dumps({"version": "2.1.285", "pad": "x" * 300}),
        BASE + "changelog.md": changelog(),
    }
    result.update(override)
    return result


def fetcher_for(available, final=None):
    final = final or {}

    def fetch(url):
        if url not in available:
            raise cc.SourceError(f"{url}: 404")
        return cc.Fetched(url, final.get(url, url), available[url])
    return fetch


COURSE = {"m.md": "Use `--max-turns` with `claude -p --model opus`.\n"}


def run(course=None, canon_text=None, available=None, exceptions="", previous=None, today=TODAY, final=None, **kw):
    return cc.run(canon_text=canon_text or canon(), course=course or COURSE, exceptions_text=exceptions,
                  fetcher=fetcher_for(available or pages(), final), today=today, previous_state=previous, **kw)


def levels(result, level):
    return [f for f in result.findings if f.level == level]


def test_clean_run_exits_0():
    result = run()
    assert result.exit_code == 0
    assert levels(result, "rot") == [] and levels(result, "gelb") == []


def test_undocumented_course_flag_is_red_with_location():
    result = run(course={"b3.md": "intro\nPass `--metadata '{}'` to tag CI runs.\n"})
    [finding] = levels(result, "rot")
    assert finding.key == "missing:flag:--metadata"
    assert finding.where == ("b3.md:2",)
    assert result.exit_code == 1


def test_exception_suppresses_and_orphaned_exception_is_red():
    course = {"x.md": "Run `--door 3` in exercise 1.\n"}
    assert run(course=course, exceptions="--door | Übungsparameter\n").exit_code == 0
    orphan = run(exceptions="--orphan | git-Flag\n")
    assert [f.key for f in levels(orphan, "rot")] == ["orphan-exception:--orphan"]


@pytest.mark.parametrize("body", ["/docs/en/models/overview.md", "<!doctype html><html>" + "x" * 6000])
def test_redirect_stub_or_html_page_is_a_source_error(body):
    with pytest.raises(cc.SourceError):
        run(available=pages(**{BASE + "model-config.md": body}))


def test_missing_source_is_a_source_error():
    available = pages()
    del available[BASE + "env-vars.md"]
    with pytest.raises(cc.SourceError):
        run(available=available)


def test_parser_floor_violation_is_a_source_error():
    short = "| API model name | Current state | Deprecated | Tentative retirement date |\n| --- | --- | --- | --- |\n" \
            "| claude-opus-5-5 | Active | N/A | Not sooner than September 22, 2027 |\n" + PAD
    with pytest.raises(cc.SourceError):
        run(available=pages(**{BASE + "model-deprecations.md": short}))


def test_canon_cli_version_missing_in_changelog_is_a_source_error():
    with pytest.raises(cc.SourceError):
        run(canon_text=canon(cli="2.1.100"))


def test_retiring_canon_model_is_red():
    haiku = ("Claude Haiku 4.5", "claude-haiku-4-5-20251001", "haiku", "Haiku", "Active", "Not sooner than October 15, 2026")
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-haiku-4-5-20251001", "Active", "N/A",
                                                                        "Not sooner than October 15, 2026")])})
    result = run(canon_text=canon(rows=(OPUS, haiku)), available=available)
    assert [f.key for f in levels(result, "rot")] == ["retiring:claude-haiku-4-5-20251001:2026-10-15"]


def test_newer_active_model_in_a_canon_family_is_red():
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-opus-6", "Active", "N/A", "Not sooner than May 1, 2028")])})
    assert [f.key for f in levels(run(available=available), "rot")] == ["new-model:claude-opus-6"]


def test_active_family_missing_in_canon_is_only_info():
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-mythos-5-1", "Active", "N/A", "Not sooner than May 1, 2028")])})
    result = run(available=available)
    assert levels(result, "rot") == []
    assert any(f.key == "unknown-families" for f in levels(result, "info"))


def test_canon_retirement_text_must_match_the_table():
    changed = ("Claude Opus 5.5", "claude-opus-5-5", "opus", "Opus", "Active", "Not sooner than June 1, 2027")
    assert [f.key.split(":")[0] for f in levels(run(canon_text=canon(rows=(changed,))), "rot")] == ["canon-retirement"]


@pytest.mark.parametrize("checked,level", [("2026-06-30", "rot"), ("2026-08-10", "info")])
def test_canon_age(checked, level):
    result = run(canon_text=canon(checked=checked))
    assert any(f.key.startswith(("canon-stale", "canon-age")) for f in levels(result, level))


def test_changelog_naming_a_course_identifier_is_yellow_keyword_only_is_info():
    available = pages(**{BASE + "changelog.md": changelog(["Fixed --max-turns off by one", "Changed the default theme", "Added foo"])})
    result = run(available=available)
    assert [f.text for f in levels(result, "gelb")] == ["2.1.285: Fixed --max-turns off by one"]
    assert [f.text for f in levels(result, "info") if f.key.startswith("changelog-kw")] == ["2.1.285: Changed the default theme"]
    assert result.exit_code == 1


def test_documented_mode_alias_from_the_cli_reference_is_accepted():
    cli = pages()[BASE + "cli-reference.md"] + "\n| `--permission-mode` | Accepts `default`, `plan`, or `manual` | x |\n"
    result = run(course={"c.md": "claude --permission-mode manual\n"}, available=pages(**{BASE + "cli-reference.md": cli}))
    assert levels(result, "rot") == []


def test_changelog_names_aliases_and_modes_only_in_code_form():
    available = pages(**{BASE + "changelog.md": changelog(["Changed `opus` to resolve differently", "Improved the opus picker"])})
    result = run(available=available)
    assert [f.text for f in levels(result, "gelb")] == ["2.1.285: Changed `opus` to resolve differently"]


def test_cockpit_comparison_ignores_provenance_but_reports_real_differences():
    course_cockpit = "<!doctype html>\n<p>x</p>\n" + "c" * 100_000
    same = course_cockpit.replace("<!doctype html>\n", "<!doctype html>\n<!-- Quelle: dynamic_workshop/resources/claude-code-workshop-ui.html · Stand X -->\n")
    url = "https://site.test/cockpit"
    clean = run(available=pages(**{url: same}), cockpit_text=course_cockpit, cockpit_url=url)
    assert levels(clean, "rot") == []
    differs = run(available=pages(**{url: same.replace("<p>x</p>", "<p>y</p>")}), cockpit_text=course_cockpit, cockpit_url=url)
    assert [f.key.split(":")[0] for f in levels(differs, "rot")] == ["cockpit-differs"]


def test_redirect_is_reported_as_info():
    result = run(final={BASE + "env-vars.md": BASE + "moved/env-vars.md"})
    assert any(f.key == f"redirect:{BASE}env-vars.md" for f in levels(result, "info"))


def test_second_identical_run_marks_findings_as_known():
    course = {"b3.md": "Pass `--metadata` here.\n"}
    first = run(course=course)
    second = run(course=course, previous=first.state)
    report = cc.render_report(second, today=TODAY, previous_state=first.state)
    assert "weiterhin offen" in report and "**neu**" not in report
    assert cc.summary(second, first.state, Path("r.md"))["new_red"] == 0
    assert cc.summary(first, None, Path("r.md"))["new_red"] == 1


def test_new_doc_identifiers_since_last_run_are_info():
    first = run()
    more = pages(**{BASE + "cli-reference.md": pages()[BASE + "cli-reference.md"] + "\n`--brand-new`"})
    second = run(available=more, previous=first.state)
    assert any("--brand-new" in f.text for f in levels(second, "info"))


def _patch_main(monkeypatch, tmp_path, available):
    canon_file = tmp_path / "canon.md"
    canon_file.write_text(canon(), encoding="utf-8")
    exceptions_file = tmp_path / "exceptions.txt"
    exceptions_file.write_text("", encoding="utf-8")
    cockpit_file = tmp_path / "cockpit.html"
    cockpit_file.write_text("<p>x</p>", encoding="utf-8")
    monkeypatch.setattr(cc, "CANON", canon_file)
    monkeypatch.setattr(cc, "EXCEPTIONS", exceptions_file)
    monkeypatch.setattr(cc, "COCKPIT", cockpit_file)
    monkeypatch.setattr(cc, "read_course", lambda root=None: dict(COURSE))
    monkeypatch.setattr(cc, "fetch", fetcher_for(available))


def test_main_writes_report_state_and_summary_as_last_line(monkeypatch, tmp_path, capsys):
    _patch_main(monkeypatch, tmp_path, pages())
    state_dir = tmp_path / "state"
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(state_dir)]) == 0
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert last.startswith("SUMMARY ")
    assert json.loads(last[len("SUMMARY "):])["exit"] == 0
    assert (state_dir / "state.json").exists() and (state_dir / "reports" / "2026-09-29.md").exists()


def test_main_keeps_previous_state_on_source_error(monkeypatch, tmp_path, capsys):
    available = pages()
    del available["https://npm.test/latest"]
    _patch_main(monkeypatch, tmp_path, available)
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "state.json").write_text('{"keep": true}', encoding="utf-8")
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(state_dir)]) == 2
    assert (state_dir / "state.json").read_text(encoding="utf-8") == '{"keep": true}'
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert json.loads(last[len("SUMMARY "):])["exit"] == 2


def test_main_turns_an_unreadable_canon_into_exit_2(monkeypatch, tmp_path, capsys):
    _patch_main(monkeypatch, tmp_path, pages())
    monkeypatch.setattr(cc, "CANON", tmp_path / "missing.md")
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(tmp_path / "s")]) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tools/test_currency_check.py -q`
Expected: FAIL — `currency_check.py` existiert nicht.

- [ ] **Step 3: Write minimal implementation**

`tools/currency_exceptions.txt`:

```
# Bezeichner, die der Kurs lehrt, die aber keine Claude-Code-Bezeichner sind (Fremd-Flags, Übungsparameter).
# Format: bezeichner | grund. Die Liste darf nur schrumpfen (tools/test_currency_check.py).
```

`tools/currency_check.py`:

```python
# -*- coding: utf-8 -*-
"""Monthly currency check for the Dynamic Workshop.

Are the identifiers the course teaches still documented, and is the canon still the current model lineup?
Exit 0 = clean, 1 = red or yellow findings, 2 = a source or the canon is unusable (fail-closed).
The last stdout line is 'SUMMARY {json}' for the monthly wrapper.

Aufruf (aus dem Repo-Root):  python tools/currency_check.py [--cockpit-url URL] [--today YYYY-MM-DD]
Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import currency_extract as cx  # noqa: E402
import lint_currency  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "resources" / "_canonical.md"
COCKPIT = ROOT / "resources" / "claude-code-workshop-ui.html"
EXCEPTIONS = ROOT / "tools" / "currency_exceptions.txt"
STATE_DIR = ROOT / ".currency"

TIMEOUT_S = 30
MIN_BYTES = {"doc": 5_000, "cli": 200, "changelog": 100_000, "cockpit": 100_000}
MIN_FLAGS, MIN_ENV, MIN_DEPRECATIONS, MIN_ALIASES, MIN_MODES = 80, 150, 10, 3, 5
RETIREMENT_WARN_DAYS = 60
CANON_INFO_DAYS, CANON_RED_DAYS = 45, 90
REQUIRED_DOCS = ("cli-reference.md", "model-deprecations.md", "model-config.md", "permission-modes.md")
KEYWORDS = re.compile(r"\b(removed|deprecated|renamed|no longer|default)\b", re.I)
SPECIFIC_KINDS = ("flag", "env", "hook_event", "model_id")
KIND_LABEL = {
    "flag": "Flag", "env": "Env-Variable", "hook_event": "Hook-Event",
    "model_id": "Modell-ID", "alias": "Modell-Alias", "permission_mode": "Permission-Modus",
}


class SourceError(Exception):
    """A source or the canon is unusable; the run must end with exit 2, never 'clean'."""


@dataclass(frozen=True)
class Fetched:
    url: str
    final_url: str
    text: str


@dataclass(frozen=True)
class Finding:
    level: str  # "rot" | "gelb" | "info"
    key: str  # stable across runs: decides "neu" vs "weiterhin offen"
    text: str
    where: tuple = ()


@dataclass
class RunResult:
    exit_code: int
    findings: list
    state: dict
    sources: list  # (url, final_url, bytes, sha256, changed)
    unparsed_json: int
    canon_checked: dt.date
    canon_age_days: int
    cli_canon: str
    cli_latest: str


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "dynamic-workshop-currency-check/1"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            return Fetched(url, response.geturl(), response.read().decode("utf-8"))
    except (OSError, ValueError) as exc:  # URLError/HTTPError/timeouts are OSError; bad UTF-8 is ValueError
        raise SourceError(f"{url}: {exc}") from exc


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _short(text):
    return _sha(text)[:10]


def fetch_checked(fetcher, url, kind):
    got = fetcher(url)
    size = len(got.text.encode("utf-8"))
    if size < MIN_BYTES[kind]:
        raise SourceError(f"{url}: nur {size} Bytes (Minimum {MIN_BYTES[kind]})")
    if kind in ("doc", "changelog") and "<html" in got.text[:500].lower():
        raise SourceError(f"{url}: HTML statt Markdown (Fehler- oder Challenge-Seite?)")
    return got


def read_course(root=None):
    root = str(root or ROOT)
    return {rel: "".join(lint_currency.read_lines(full)) for rel, full in lint_currency.live_files(root)}


def _collect_course(course):
    by_value, unparsed = {}, 0
    for path in sorted(course):
        hits, count = cx.extract_course_hits(path, course[path])
        unparsed += count
        for hit in hits:
            by_value.setdefault((hit.kind, hit.value), []).append(f"{hit.path}:{hit.line}")
    return by_value, unparsed


def _check_course(by_value, exceptions, union, aliases, modes):
    findings = []
    for (kind, value), where in sorted(by_value.items()):
        if value in exceptions or cx.exists_in_docs(kind, value, union, aliases, modes):
            continue
        findings.append(Finding("rot", f"missing:{kind}:{value}",
                                f"{KIND_LABEL[kind]} `{value}` steht im Kurs, aber in keiner Doku-Quelle",
                                tuple(sorted(set(where)))))
    taught = {value for _kind, value in by_value}
    for value in sorted(exceptions):
        if value not in taught:
            findings.append(Finding("rot", f"orphan-exception:{value}",
                                    f"Ausnahme `{value}` kommt im Kurs nicht mehr vor: aus currency_exceptions.txt streichen"))
    return findings


def _check_canon_models(canon_models, deprecations, today):
    findings, families = [], {}
    for model in canon_models:
        family, version = cx.model_family_version(model.model_id)
        families[family] = max(families.get(family, ()), version)
        row = deprecations.get(model.model_id)
        if row is None:
            findings.append(Finding("rot", f"canon-unknown:{model.model_id}",
                                    f"Kanon-Modell `{model.model_id}` fehlt in der Deprecations-Tabelle"))
            continue
        if row.status != "Active":
            findings.append(Finding("rot", f"canon-status:{model.model_id}:{row.status}",
                                    f"Kanon-Modell `{model.model_id}` hat Status {row.status}"))
        if row.retirement != model.retirement:
            findings.append(Finding("rot", f"canon-retirement:{model.model_id}:{row.retirement}",
                                    f"Retirement von `{model.model_id}`: Kanon „{model.retirement}“, Doku „{row.retirement}“"))
        earliest = cx.parse_date(row.retirement)
        if earliest and (earliest - today).days < RETIREMENT_WARN_DAYS:
            findings.append(Finding("rot", f"retiring:{model.model_id}:{earliest}",
                                    f"`{model.model_id}` kann ab {earliest} abgeschaltet werden "
                                    f"({(earliest - today).days} Tage)"))
    unknown = set()
    for model_id, row in sorted(deprecations.items()):
        if row.status != "Active":
            continue
        family, version = cx.model_family_version(model_id)
        if family not in families:
            unknown.add(family)
        elif version > families[family]:
            findings.append(Finding("rot", f"new-model:{model_id}",
                                    f"Neues aktives Modell `{model_id}` ist neuer als der Kanon-Stand der Familie {family}"))
    if unknown:
        findings.append(Finding("info", "unknown-families",
                                "Aktive Modellfamilien, die der Kanon nicht führt: " + ", ".join(sorted(unknown))))
    return findings


def _check_changelog(entries, by_value):
    specific = sorted({v for (k, v) in by_value if k in SPECIFIC_KINDS}, key=len, reverse=True)
    # Aliases and modes are ordinary words ("default", "plan"): they count only in code form.
    words = sorted({v for (k, v) in by_value if k not in SPECIFIC_KINDS}, key=len, reverse=True)
    findings = []
    for version, line in entries:
        named = [v for v in specific if re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", line)]
        named += [v for v in words if "`" + v + "`" in line]
        if named:
            findings.append(Finding("gelb", f"changelog:{version}:{_short(line)}", f"{version}: {line}",
                                    tuple(f"nennt {v}" for v in named)))
        elif KEYWORDS.search(line):
            findings.append(Finding("info", f"changelog-kw:{version}:{_short(line)}", f"{version}: {line}"))
    return findings


def run(*, canon_text, course, exceptions_text, fetcher, today, previous_state, cockpit_text=None, cockpit_url=None):
    """Pure orchestration over injected inputs. Raises SourceError for anything unusable."""
    try:
        checked, cli_canon = cx.parse_canon_header(canon_text)
        canon_models = cx.parse_canon_models(canon_text)
        sources = cx.parse_canon_sources(canon_text)
        exceptions = cx.parse_exceptions(exceptions_text)
    except ValueError as exc:
        raise SourceError(str(exc)) from exc

    docs = [fetch_checked(fetcher, url, "doc") for url in sources["Doku"]]
    cli = fetch_checked(fetcher, sources["CLI-Version"][0], "cli")
    changelog = fetch_checked(fetcher, sources["Changelog"][0], "changelog")
    live_cockpit = fetch_checked(fetcher, cockpit_url, "cockpit") if cockpit_url else None

    by_name = {d.url.rsplit("/", 1)[-1]: d for d in docs}
    missing = [name for name in REQUIRED_DOCS if name not in by_name]
    if missing:
        raise SourceError("Kanon-Quellenliste ohne " + ", ".join(missing))
    union = "\n".join(d.text for d in docs)
    doc_ids = cx.doc_identifiers(union)
    deprecations = cx.parse_deprecations(by_name["model-deprecations.md"].text)
    aliases = cx.parse_aliases(by_name["model-config.md"].text)
    modes = cx.parse_permission_modes(by_name["permission-modes.md"].text, by_name["cli-reference.md"].text)
    for label, got, floor in (
        ("Flags in der Doku", len(doc_ids["flag"]), MIN_FLAGS),
        ("Env-Variablen in der Doku", len(doc_ids["env"]), MIN_ENV),
        ("Zeilen der Deprecations-Tabelle", len(deprecations), MIN_DEPRECATIONS),
        ("Aliase in model-config.md", len(aliases), MIN_ALIASES),
        ("Permission-Modi", len(modes), MIN_MODES),
    ):
        if got < floor:
            raise SourceError(f"{label}: {got} < Minimum {floor} (Format geändert?)")
    try:
        cli_latest = json.loads(cli.text)["version"]
        entries = cx.changelog_since(changelog.text, cli_canon)
    except (ValueError, KeyError) as exc:
        raise SourceError(f"CLI-Version/Changelog: {exc}") from exc

    by_value, unparsed = _collect_course(course)
    findings = _check_course(by_value, exceptions, union, aliases, modes)
    findings += _check_canon_models(canon_models, deprecations, today)
    findings += _check_changelog(entries, by_value)

    age = (today - checked).days
    if age > CANON_RED_DAYS:
        findings.append(Finding("rot", f"canon-stale:{checked}",
                                f"Kanon-Prüfdatum {checked} ist {age} Tage alt (> {CANON_RED_DAYS})"))
    elif age > CANON_INFO_DAYS:
        findings.append(Finding("info", f"canon-age:{checked}", f"Kanon-Prüfdatum {checked} ist {age} Tage alt"))

    if live_cockpit is not None:
        mine, theirs = _sha(cx.normalize_cockpit(cockpit_text)), _sha(cx.normalize_cockpit(live_cockpit.text))
        if mine != theirs:
            findings.append(Finding("rot", f"cockpit-differs:{mine[:12]}:{theirs[:12]}",
                                    "Cockpit auf der Website weicht vom Kurs-Cockpit ab (Re-Export fällig)",
                                    (live_cockpit.final_url,)))

    previous = previous_state or {}
    for kind in ("flag", "env"):
        before = set(previous.get("doc_" + kind, []))
        new = sorted(doc_ids[kind] - before) if before else []
        if new:
            findings.append(Finding("info", f"doc-new:{kind}:{_short(' '.join(new))}",
                                    f"Neu in der Doku ({KIND_LABEL[kind]}): " + ", ".join(new)))

    known_sources = previous.get("sources", {})
    rows = []
    for got in docs + [cli, changelog] + ([live_cockpit] if live_cockpit else []):
        sha = _sha(got.text)
        changed = got.url in known_sources and known_sources[got.url]["sha256"] != sha
        rows.append((got.url, got.final_url, len(got.text.encode("utf-8")), sha, changed))
        if got.final_url != got.url:
            findings.append(Finding("info", f"redirect:{got.url}",
                                    f"Quelle umgezogen: {got.url} -> {got.final_url} (Kanon-Quellenliste nachziehen)"))

    exit_code = 1 if any(f.level in ("rot", "gelb") for f in findings) else 0
    state = {
        "version": 1,
        "date": today.isoformat(),
        "cli_latest": cli_latest,
        "doc_flag": sorted(doc_ids["flag"]),
        "doc_env": sorted(doc_ids["env"]),
        "sources": {url: {"sha256": sha, "final_url": final} for url, final, _size, sha, _changed in rows},
        "finding_keys": sorted(f.key for f in findings if f.level in ("rot", "gelb")),
    }
    return RunResult(exit_code, findings, state, rows, unparsed, checked, age, cli_canon, cli_latest)


def render_report(result, *, today, previous_state):
    known = set((previous_state or {}).get("finding_keys", []))
    count = {level: sum(f.level == level for f in result.findings) for level in ("rot", "gelb", "info")}
    lines = [
        f"# Currency-Check {today}",
        "",
        f"- Kanon geprüft: {result.canon_checked} ({result.canon_age_days} Tage) · CLI laut Kanon "
        f"{result.cli_canon} · neueste CLI {result.cli_latest}",
        f"- Befunde: {count['rot']} rot · {count['gelb']} gelb · {count['info']} info",
        f"- Nicht parsebare JSON-Blöcke im Kurs: {result.unparsed_json}",
        "",
    ]
    for level, title in (("rot", "Rot"), ("gelb", "Gelb"), ("info", "Info")):
        items = [f for f in result.findings if f.level == level]
        lines += [f"## {title} ({len(items)})", ""]
        for finding in items:
            tag = "" if level == "info" else (" · weiterhin offen" if finding.key in known else " · **neu**")
            lines.append(f"- {finding.text}{tag}")
            lines += [f"  - {where}" for where in finding.where[:10]]
            if len(finding.where) > 10:
                lines.append(f"  - … {len(finding.where) - 10} weitere")
        lines.append("")
    lines += ["## Quellen", "", "| URL | End-URL | Bytes | sha256 | geändert |", "|---|---|---|---|---|"]
    for url, final, size, sha, changed in result.sources:
        lines.append(f"| {url} | {'' if final == url else final} | {size} | {sha[:12]} | {'ja' if changed else ''} |")
    return "\n".join(lines) + "\n"


def summary(result, previous_state, report_path):
    known = set((previous_state or {}).get("finding_keys", []))
    red = [f for f in result.findings if f.level == "rot"]
    yellow = [f for f in result.findings if f.level == "gelb"]
    return {
        "exit": result.exit_code,
        "red": len(red),
        "yellow": len(yellow),
        "new_red": sum(f.key not in known for f in red),
        "new_yellow": sum(f.key not in known for f in yellow),
        "canon_checked": result.canon_checked.isoformat(),
        "canon_age_days": result.canon_age_days,
        "report": str(report_path),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Monatlicher Currency-Check des Dynamic Workshop")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--cockpit-url")
    parser.add_argument("--state-dir", type=Path, default=STATE_DIR)
    args = parser.parse_args(argv)
    state_path = args.state_dir / "state.json"
    report_path = args.state_dir / "reports" / f"{args.today}.md"
    try:
        previous = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
        result = run(
            canon_text=Path(CANON).read_text(encoding="utf-8"),
            course=read_course(),
            exceptions_text=Path(EXCEPTIONS).read_text(encoding="utf-8"),
            fetcher=fetch,
            today=args.today,
            previous_state=previous,
            cockpit_text=Path(COCKPIT).read_text(encoding="utf-8"),
            cockpit_url=args.cockpit_url,
        )
    except (SourceError, OSError, ValueError) as exc:
        print(f"FEHLER (fail-closed): {exc}")
        print("SUMMARY " + json.dumps({"exit": 2, "error": str(exc)}, ensure_ascii=False))
        return 2
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(result, today=args.today, previous_state=previous), encoding="utf-8")
    state_path.write_text(json.dumps(result.state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Bericht: {report_path}")
    print("SUMMARY " + json.dumps(summary(result, previous, report_path), ensure_ascii=False))
    return result.exit_code


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tools/test_currency_check.py -q` → Expected: 24 passed.
Run: `python -m pytest tools -q` → Expected: alles grün (Baseline + neue Tests).

- [ ] **Step 5: Mutation probe (nicht committen)**

Nacheinander je eine Mutation einbauen, `python -m pytest tools/test_currency_check.py -q` laufen lassen, Rot
notieren, Mutation per `git checkout -- tools/currency_check.py` zurücknehmen:
1. `MIN_DEPRECATIONS = 0` → `test_parser_floor_violation_is_a_source_error` muss rot werden.
2. In `main()` State vor `run()` schreiben (`state_path.write_text("{}")` direkt nach `previous = …`) →
   `test_main_keeps_previous_state_on_source_error` rot.
3. `if value in exceptions or …` → `if … exists_in_docs(…)` (Ausnahmen ignorieren) → Ausnahmetest rot.
4. Den HTML-Check in `fetch_checked` entfernen → HTML-Parametrisierung rot.
Bleibt eine Mutation grün: fehlende Testzelle ergänzen, bevor committet wird.

- [ ] **Step 6: Commit**

```bash
git add tools/currency_check.py tools/currency_exceptions.txt tools/test_currency_check.py
git commit -m "feat(tools): monthly currency check with fail-closed sources and stable findings"
```

---

### Task 5: Kanon neu schreiben

**Files:**
- Modify: `resources/_canonical.md` (vollständig ersetzen)
- Modify: `tools/test_currency_check.py` (Strukturtest am echten Kanon anhängen)

**Interfaces:**
- Consumes: `parse_canon_header`, `parse_canon_models`, `parse_canon_sources` (Task 3).
- Produces: der Kanon, den Task 6 (Stale-Gate) und Task 8 (Live-Lauf) lesen.

- [ ] **Step 1: Write the failing test** (an `tools/test_currency_check.py` anhängen)

```python
def test_real_canon_is_machine_readable():
    cx = _load("currency_extract")
    text = (ROOT / "resources" / "_canonical.md").read_text(encoding="utf-8")
    cx.parse_canon_header(text)
    models = cx.parse_canon_models(text)
    assert {m.tier for m in models} == {"Fable", "Opus", "Sonnet", "Haiku"}
    for model in models:
        assert model.model_id.startswith("claude-") and model.alias in {"fable", "opus", "sonnet", "haiku"}
        assert re.fullmatch(r"(Not sooner than )?[A-Z][a-z]+ \d{1,2}, \d{4}", model.retirement), model.retirement
    sources = cx.parse_canon_sources(text)
    assert len(sources["Doku"]) == 13
    assert all(url.startswith("https://") for urls in sources.values() for url in urls)
    names = {url.rsplit("/", 1)[-1] for url in sources["Doku"]}
    assert {"model-deprecations.md", "model-config.md", "permission-modes.md"} <= names
```

`import re` oben in `tools/test_currency_check.py` ergänzen.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tools/test_currency_check.py::test_real_canon_is_machine_readable -q`
Expected: FAIL — `ValueError: Kanon: Zeile 'Geprüft: …' fehlt`.

- [ ] **Step 3: Fakten an der Quelle bestätigen**

```bash
curl -sL https://platform.claude.com/docs/en/models/overview.md | grep -E "^\| (Claude API ID|\[Pricing\]|\[Context window\]|\[Retirement\])" | cut -c1-400
curl -sL https://platform.claude.com/docs/en/about-claude/model-deprecations.md | grep -E "^\| claude-(fable-5-1|opus-5-5|sonnet-5-5|haiku-4-5-20251001) "
curl -sL https://code.claude.com/docs/en/model-config.md | sed -n '/^### `default` model setting/,/^Before v2/p;/^The version that the `opus`/,/^$/p;/^| Model | Levels |/,/^$/p'
curl -s https://registry.npmjs.org/@anthropic-ai/claude-code/latest | python -c "import json,sys;print(json.load(sys.stdin)['version'])"
```

Expected (Stand 2026-09-29): Fable 5.1 `claude-fable-5-1` 1M $10/$50 „Not sooner than September 1, 2027"; Opus 5.5
`claude-opus-5-5` 1M $4/$20 „Not sooner than September 22, 2027"; Sonnet 5.5 `claude-sonnet-5-5` 1M $2/$10 „Not
sooner than September 28, 2027"; Haiku 4.5 `claude-haiku-4-5-20251001` 200K $1/$5 „Not sooner than October 15, 2026";
`default` = Opus 5.5 (Pro/Max/Team/Enterprise/API); CLI 2.1.284. **Weicht ein Wert ab: den Wert der Quelle nehmen**
und die Abweichung im Commit nennen; `Geprüft:` trägt das Datum dieses Abgleichs und die npm-Version.

- [ ] **Step 4: Kanon ersetzen**

`resources/_canonical.md` (vollständig):

````markdown
<!-- CANONICAL SOURCE OF TRUTH — do not teach anything that contradicts this file.
     Einzige Stelle im Kurs, an der Modellgenerationen und ihre Fakten stehen (Alias-Regel).
     Geprüft von tools/lint_currency.py (Generationsregel + Stale-Gate) und tools/currency_check.py (Monatslauf).
     Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md -->

# Canonical Registry — Dynamic Workshop

Geprüft: 2026-09-29 · CLI 2.1.284

Das Prüfdatum setzt nur eine Session, die diesen Kanon gegen einen Bericht von `tools/currency_check.py` oder direkt
gegen die Quellen unten abgeglichen hat. `tools/lint_currency.py` warnt ab 45 Tagen und wird ab 90 Tagen rot.

## Alias-Regel

- Kursinhalte nennen **keine Modellgeneration** (etwa „Opus 5.5" oder `claude-opus-5-5`). Code und Config nutzen
  Aliase (`opus`, `sonnet`, `haiku`, `fable`), Prosa nennt die Rolle („das Opus-Tier") und verweist hierher.
- Preise, Kontextgrößen, Effort-Defaults und Retirement-Daten stehen nur hier.
- Bewusst versionierte Stellen tragen in derselben Zeile `version-pinned: <Grund>`.
- Immer `claude --version`, `/release-notes` und `/model` über jede hier gedruckte Zahl stellen.

## Aktuelle Claude-Modelle

| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |
|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | `fable` | Fable | Active | Not sooner than September 1, 2027 | 1M | 10 | 50 | Härtestes, langlaufendes Reasoning; nie Account-Default |
| Claude Opus 5.5 | `claude-opus-5-5` | `opus` | Opus | Active | Not sooner than September 22, 2027 | 1M | 4 | 20 | Default in Claude Code; Architektur, tiefes Reasoning |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | `sonnet` | Sonnet | Active | Not sooner than September 28, 2027 | 1M | 2 | 10 | Schnelles Standard-Coding, Alltag |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | `haiku` | Haiku | Active | Not sooner than October 15, 2026 | 200K | 1 | 5 | Bulk-Reads, einfache Suchen, Routine-Reviews |

- **Haiku-Risiko:** Haiku 4.5 kann frühestens am 15.10.2026 abgeschaltet werden. Wer `haiku` für Massenarbeit nutzt,
  prüft vor dem Einsatz mit `/model`, worauf der Alias auflöst.
- API-Alias von Haiku 4.5: `claude-haiku-4-5`.

## Aliase und ihre Auflösung (Quelle: model-config.md)

- `default` löst je Kontotyp auf: Opus 5.5 auf Pro, Max, Team, Enterprise und der Anthropic API sowie auf Claude
  Platform on AWS, Amazon Bedrock und Google Cloud; Sonnet 4.5 auf Microsoft Foundry. Eine Organisations-Vorgabe geht vor.
- `opus` und `sonnet` lösen **je Anbieter** unterschiedlich auf:

| Anbieter | `opus` | `sonnet` |
|---|---|---|
| Anthropic API | Opus 5.5 | Sonnet 5.5 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 |
| Amazon Bedrock, Google Cloud | Opus 5.5 | Sonnet 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 |

- `fable` löst auf Fable 5.1 auf, im Claude-apps-Gateway auf Fable 5; `best` = `fable`, wo Fable verfügbar ist, sonst `opus`.
- Weitere Werte: `opusplan` (Opus im Plan-Modus, dann Sonnet), `sonnet[1m]`, `opus[1m]`.

## Effort (Quelle: model-config.md, „Adjust effort level")

| Modelle | Stufen | Start-Effort in Claude Code |
|---|---|---|
| Fable 5.1 | `low` `medium` `high` `xhigh` `max` | `high` |
| Opus 5.5, Sonnet 5.5 | `low` `medium` `high` `xhigh` `max` | `medium` |
| Haiku 4.5 | kein Effort | — |

- Die Modellübersicht der API nennt für Sonnet 5.5 `high` als Default-Effort; Claude Code startet laut model-config
  mit `medium`. Im Kurs gilt das Claude-Code-Verhalten.
- `max` gilt nur für die laufende Session, außer über `CLAUDE_CODE_EFFORT_LEVEL`.

## Struktur

- **4 Sessions / 65 Lerneinheiten (LE)** — Welle-F-Restrukturierung (`session-plan.md` ist die Ablauf-SSoT).
- Session 1 = Block 1 (Foundations, S1.1–S1.20). Session 2 = Block 2 (Ecosystem, S2.1–S2.20).
  Session 3 = Block 3 Advanced Kern (S3.1–S3.15). Session 4 = Block 3 Advanced Bonus (S4.1–S4.10).
- 17 Module (5+5+7) über 3 Blöcke bleiben die Volltext-Quelle; die 65-LE-Landkarte ist die Navigations-Schicht darüber.

## Quellen

Der Monatslauf (`tools/currency_check.py`) liest genau diese Liste.

- Doku: https://code.claude.com/docs/en/cli-reference.md
- Doku: https://code.claude.com/docs/en/env-vars.md
- Doku: https://code.claude.com/docs/en/hooks.md
- Doku: https://code.claude.com/docs/en/headless.md
- Doku: https://code.claude.com/docs/en/authentication.md
- Doku: https://code.claude.com/docs/en/github-actions.md
- Doku: https://code.claude.com/docs/en/permission-modes.md
- Doku: https://code.claude.com/docs/en/model-config.md
- Doku: https://code.claude.com/docs/en/mcp.md
- Doku: https://code.claude.com/docs/en/skills.md
- Doku: https://code.claude.com/docs/en/settings.md
- Doku: https://platform.claude.com/docs/en/models/overview.md
- Doku: https://platform.claude.com/docs/en/about-claude/model-deprecations.md
- CLI-Version: https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- Changelog: https://code.claude.com/docs/en/changelog.md
````

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tools -q` → Expected: alles grün.
Run: `python tools/lint_currency.py` → Expected: `OK` (die alte Verbotsliste greift im Kanon nicht; er ist ausgeklammert).

- [ ] **Step 6: Commit**

```bash
git add resources/_canonical.md tools/test_currency_check.py
git commit -m "docs(canon): current lineup, alias resolution, effort and source list with check date"
```

---

### Task 6: Lint — Generationsregel, Marker, Stale-Gate

**Files:**
- Modify: `tools/lint_currency.py` (Regeln und `main()` ersetzen; `live_files` etc. bleiben)
- Modify: `tools/test_lint_currency.py` (anhängen)
- Modify: `tools/test_workshop_ui_behavior.py:130-138` (cp1252-Test auf `GENERATION` umstellen)

**Interfaces:**
- Consumes: `currency_extract.parse_canon_header` (Task 3), `live_files`/`read_lines` (Task 1).
- Produces: `GENERATION` (Regex), `is_pinned(line) -> bool`, `generation_hits(root) -> list[tuple]`,
  `canon_status(canon_path, today) -> tuple[str, str]` mit Stufe `ok|warn|red`, `main(root=ROOT, today=None) -> int`.

- [ ] **Step 1: Write the failing tests** (an `tools/test_lint_currency.py` anhängen)

```python
import datetime as dt

import pytest

CANON_OK = "# Kanon\n\nGeprüft: 2026-09-29 · CLI 2.1.284\n"


@pytest.mark.parametrize("line", [
    "Nutze Opus 4.8 für Architektur.", "sonnet-4.6", "--model claude-haiku-4-5-20251001",
    "Claude Fable 5.1 ist neu.", "SONNET 5", "claude-opus-5-5",
])
def test_generation_mentions_are_found(line):
    assert lint.GENERATION.search(line) and not lint.is_pinned(line)


@pytest.mark.parametrize("line", [
    "Nutze das Opus-Tier.", "--model opus", "model: sonnet[1m]", "seit 2.1.145 verfügbar", "Opus-Modelle und Haiku",
])
def test_aliases_roles_and_cli_versions_are_allowed(line):
    assert not lint.GENERATION.search(line)


def test_pin_needs_a_reason_on_the_same_line():
    assert lint.is_pinned("Haiku 4.5 kann abgeschaltet werden. <!-- version-pinned: Retirement-Hinweis -->")
    assert lint.is_pinned('q: "Haiku 4.5 hat 200K", // version-pinned: Quiz zu Kontextgrenzen')
    assert not lint.is_pinned("Haiku 4.5 <!-- version-pinned: -->")
    assert not lint.is_pinned("Haiku 4.5 <!-- version-pinned: ab -->")


@pytest.mark.parametrize("today,level", [
    (dt.date(2026, 11, 12), "ok"), (dt.date(2026, 11, 14), "warn"), (dt.date(2026, 12, 29), "red"),
])
def test_stale_gate(tmp_path, today, level):
    canon = tmp_path / "_canonical.md"
    canon.write_text(CANON_OK, encoding="utf-8")
    assert lint.canon_status(str(canon), today)[0] == level


def test_missing_or_unreadable_check_date_is_red(tmp_path):
    canon = tmp_path / "_canonical.md"
    canon.write_text("# Kanon ohne Datum\n", encoding="utf-8")
    assert lint.canon_status(str(canon), dt.date(2026, 9, 29))[0] == "red"
    assert lint.canon_status(str(tmp_path / "missing.md"), dt.date(2026, 9, 29))[0] == "red"


def test_main_combines_generation_rule_and_stale_gate(tmp_path, capsys):
    root = _tree(tmp_path, {
        "resources/_canonical.md": CANON_OK + "Claude Opus 5.5 steht hier.\n",
        "resources/modules/m.md": "Nutze das Opus-Tier.\nHaiku 4.5 <!-- version-pinned: Retirement-Hinweis -->\n",
    })
    assert lint.main(str(root), today=dt.date(2026, 9, 29)) == 0
    (root / "resources/modules/m.md").write_text("Nutze Opus 5.5.\n", encoding="utf-8")
    assert lint.main(str(root), today=dt.date(2026, 9, 29)) == 1
    assert "resources/modules/m.md:1" in capsys.readouterr().out
    (root / "resources/modules/m.md").write_text("Nutze das Opus-Tier.\n", encoding="utf-8")
    assert lint.main(str(root), today=dt.date(2027, 1, 1)) == 1
```

Grenzfälle Stale-Gate: 2026-09-29 + 44 Tage = 2026-11-12 (ok), + 46 = 2026-11-14 (warn), + 91 = 2026-12-29 (red).

In `tools/test_workshop_ui_behavior.py`, Test `test_currency_lint_checks_cp1252_files_instead_of_skipping`:
**nur** die beiden letzten Zeilen ersetzen (die Zeile `patterns = [re.compile(p, re.IGNORECASE) for p in lint.FORBIDDEN]`
und die Zeile `assert any(rx.search(lines[0]) for rx in patterns)`) durch

```python
    assert lint.GENERATION.search(lines[0])
```

Die `write_bytes`-Zeile darüber bleibt unverändert; sie enthält ein Python-Escape für das Euro-Zeichen, das beim
Neutippen über die Harness still zum Zeichen selbst würde. Nach dem Edit prüfen:

```bash
python -c "import re;s=open('tools/test_workshop_ui_behavior.py',encoding='utf-8').read();print(chr(92)+'u20ac' in s, 'FORBIDDEN' in s)"
```

Expected: `True False`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tools/test_lint_currency.py tools/test_workshop_ui_behavior.py -q`
Expected: FAIL — `AttributeError: … has no attribute 'GENERATION'`.

- [ ] **Step 3: Write minimal implementation**

In `tools/lint_currency.py`: Docstring, `FORBIDDEN` und `main()` ersetzen, Imports ergänzen. Kopf der Datei:

```python
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
```

(`EXTS`, `EXCLUDE_DIRS`, `PRUNE_ANYWHERE`, `EXCLUDE_FILES`, `REVIEW_ARCHIVE`, `is_excluded`, `live_files`,
`read_lines` bleiben unverändert.) Neue Funktionen und neues `main()`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tools -q` → Expected: alles grün.
Run: `python tools/lint_currency.py` → Expected: **Exit 1 mit 58 Treffern in 12 Dateien** (das ist die Arbeitsliste
für Task 7; Zahl notieren und mit der Spec vergleichen — weicht sie ab, die Differenz vor Task 7 erklären).

- [ ] **Step 5: Mutation probe (nicht committen)**

1. `len(match.group(1).strip()) >= 3` → `>= 0` → `test_pin_needs_a_reason_on_the_same_line` rot.
2. `STALE_RED_DAYS = 900` → Stale-Gate-Parametrisierung rot.
3. In `canon_status` `except (OSError, ValueError)` → `return "ok", …` → `test_missing_or_unreadable_check_date_is_red` rot.
Zurücknehmen per `git checkout -- tools/lint_currency.py` nach jeder Probe (vorher committen oder stashen!).
Reihenfolge deshalb: erst Step 6 committen, dann Proben, dann `git checkout -- tools/lint_currency.py`.

- [ ] **Step 6: Commit** (vor den Mutationsproben)

```bash
git add tools/lint_currency.py tools/test_lint_currency.py tools/test_workshop_ui_behavior.py
git commit -m "feat(lint): model generations only in the canon, stale gate on the check date"
```

Hinweis: Ab hier ist `python tools/lint_currency.py` bis zum Ende von Task 7 absichtlich rot. Kein Push, kein Merge
dazwischen.

---

### Task 7: Modell-Sweep in den Kursdateien

**Files:**
- Modify: die Dateien aus der Ausgabe von `python tools/lint_currency.py` (erwartet: `resources/modules/block-1-foundations.md`,
  `resources/cheatsheet.md`, `resources/claude-code-workshop-ui.html`, `resources/quick-reference.md`, `resources/faq.md`,
  `resources/glossary.md`, `resources/prerequisites.md`, `resources/demos/block-1-demos.md`,
  `resources/modules/block-3-advanced.md`, `agents/workshop-mentor.md`, `README.md`, `resources/troubleshooting.md`)
- Modify: `tools/test_workshop_ui_behavior.py` (Guard-Test anhängen)

**Interfaces:**
- Consumes: Kanon (Task 5), Lint (Task 6).
- Produces: Kurs ohne Generationsnennungen außerhalb des Kanons; Lint grün.

- [ ] **Step 1: Guard-Test fürs Cockpit-Skript schreiben** (an `tools/test_workshop_ui_behavior.py` anhängen,
  `import shutil` und `import subprocess` oben ergänzen)

```python
def test_cockpit_inline_script_still_parses(tmp_path):
    """A stray quote or comment in a JS string leaves learners with a blank cockpit."""
    node = shutil.which("node")
    assert node, "node is required to syntax-check the cockpit script"
    source = UI_HTML.read_text(encoding="utf-8")
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", source, re.S)
    assert len(scripts) == 1
    path = tmp_path / "cockpit.js"
    path.write_text(scripts[0], encoding="utf-8")
    proc = subprocess.run([node, "--check", str(path)], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, proc.stderr
```

Run: `python -m pytest tools/test_workshop_ui_behavior.py -q` → Expected: PASS (Guard, am heutigen Cockpit grün).
Probe: in einer Kopie der Datei ein `"` in einen String einfügen, Test gegen die Kopie laufen lassen → rot; Kopie löschen.

- [ ] **Step 2: Arbeitsliste erzeugen**

```bash
python tools/lint_currency.py > "$TEMP/sweep-before.txt"; tail -n +2 "$TEMP/sweep-before.txt" | grep -c ":"
```

- [ ] **Step 3: Jede Zeile nach diesen Regeln umschreiben**

| Fundstelle | Ersetzung |
|---|---|
| `--model claude-opus-4-8` / `claude-sonnet-5` / `claude-haiku-4-5…` / `claude-fable-5` in Code | `--model opus` / `sonnet` / `haiku` / `fable` |
| Modellname in Prosa („Opus 4.8 ist Default") | Rolle ohne Generation („das Opus-Tier, in Claude Code der Default") + beim ersten Vorkommen je Abschnitt Verweis auf den Kanon: Markdown `[Kanon](<relativer Pfad>/_canonical.md)`, Cockpit „siehe Kanon (`resources/_canonical.md`)" |
| Preis, Kontextgröße, Effort-Default in derselben Zeile | streichen und auf den Kanon verweisen; ist die Zahl didaktisch nötig (Quiz zur 200K-Grenze), Zahl gegen den Kanon prüfen und Zeile mit `version-pinned: <Grund>` markieren (Markdown `<!-- … -->`, Cockpit-JS `// …` hinter dem Komma) |
| Modelltabelle im Modul (block-1, S1.7) | Rollentabelle ohne Generationen (Tier · Rolle · wann nehmen) + Verweis auf die Kanon-Tabelle |
| Aussage, die sich inhaltlich geändert hat (z. B. Auto-Modus-Verfügbarkeit, Effort-Default) | an der Quelle (`curl -sL <doku>.md`) prüfen, Zitat in die Commit-Message, dann ohne Generation formulieren |
| Historische Aussage („bis Juli 2026 war …") | darf bleiben, wenn nötig mit `version-pinned: historischer Vergleich` |

Beim Cockpit: nur innerhalb bestehender JS-Strings ändern, keine neuen Anführungszeichen; `// version-pinned: …`
nur hinter dem abschließenden `",` einer Eigenschaft.

- [ ] **Step 4: Mentor nachziehen**

`agents/workshop-mentor.md`: die zwei Treffer umschreiben und im Abschnitt zu Modellwahl einen Satz ergänzen:
„Modellgenerationen, Preise und Retirement-Daten stehen nur in `resources/_canonical.md`; im Gespräch Aliase und
Rollen nennen und für Zahlen auf den Kanon verweisen."

- [ ] **Step 5: Verify**

Run: `python tools/lint_currency.py` → Expected: Exit 0, `OK — keine Modellgeneration außerhalb des Kanons.`
Run: `python -m pytest tools -q` → Expected: alles grün (inkl. `test_cockpit_inline_script_still_parses`, Hook- und
CI-Auth-Wächter).
Run: `git diff --stat` → nur die Dateien der Arbeitsliste plus der Test.
Browser: Cockpit per `file://` in Playwright laden, S1.7 und das Quiz zur Kontextgrenze öffnen, Konsole ohne Fehler
(`browser_console_messages`), Screenshot nicht in `resources/` speichern.

- [ ] **Step 6: Commit**

```bash
git add resources/ agents/workshop-mentor.md README.md tools/test_workshop_ui_behavior.py
git status --short   # nur erwartete Dateien gestaged?
git commit -m "docs(course): teach aliases and roles, keep model generations in the canon"
```

---

### Task 8: Erster Live-Lauf, Ausnahmen, echte Befunde beheben

**Files:**
- Modify: `tools/currency_exceptions.txt`
- Modify: `tools/test_currency_check.py` (Ratchet-Test)
- Modify: Kursdateien laut Befunden (`resources/modules/block-3-advanced.md` für `--metadata`, weitere laut Bericht)

**Interfaces:**
- Consumes: CLI aus Task 4, Kanon aus Task 5.
- Produces: `FROZEN_EXCEPTIONS` im Test; Kurs ohne undokumentierte Bezeichner.

- [ ] **Step 1: Live-Lauf**

```bash
python tools/currency_check.py --cockpit-url https://dynamic-dome.com/workshop-cockpit
```

Expected: Exit 1. Bericht `.currency/reports/<heute>.md` lesen. Erwartete rote Befunde (Messung 2026-09-29):
`--metadata`, `--worktree-base-ref`, `--no-verbose`, `--fast`, Fremd-Flags (`--decompose`, `--door`, `--headed`,
`--notebook`, `--orphan`), `retiring:claude-haiku-4-5-20251001:2026-10-15`, `cockpit-differs` (Sweep ist
noch nicht exportiert). Weitere Befunde einzeln bewerten. **Exit 2:** Fehlermeldung lesen, Quelle/Parser prüfen,
nicht umgehen.

- [ ] **Step 2: Jeden `missing:*`-Befund einordnen**

- **Fremd-Bezeichner** (kein Claude-Code-Flag: Plugin-, Übungs-, git-, Playwright-, NotebookLM-Argument, Prosa-Artefakt)
  → Zeile in `tools/currency_exceptions.txt` mit konkretem Grund (Datei + was es ist).
- **Echter Fehler** → Kurs korrigieren. Vorher an der Quelle prüfen (`curl -sL https://code.claude.com/docs/en/<seite>.md | grep -n -- '<bezeichner>'`
  über cli-reference, settings, commands, monitoring-usage) und das Zitat in die Commit-Message schreiben:
  - `--metadata` (H-13): belegten Ersatz für Kostenzuordnung je CI-Lauf suchen (Kandidaten: `--output-format json`
    mit Kostenfeld laut headless.md; OpenTelemetry-Attribute laut monitoring-usage.md). Ohne belegten Ersatz: Satz
    streichen statt erfinden.
  - `--fast`: ist Fast Mode ein Slash-Command (`/fast`)? Dann Glossar auf `/fast` korrigieren.
  - `--worktree-base-ref`, `--no-verbose`: dokumentierte Entsprechung (Setting `worktree.baseRef`?) oder streichen.
- **H-16 `classification=`** (acht Cockpit-Beispiele): Präfix entfernen; wo die Datenklasse didaktisch zählt, eine
  Kommentarzeile `# Datenklasse: sensitiv — nur Modelle/Anbieter laut Datenhaltungs-Regel` davor setzen.
  Danach `test_cockpit_inline_script_still_parses` laufen lassen.

- [ ] **Step 3: Ratchet-Test schreiben** (an `tools/test_currency_check.py` anhängen; die Menge = genau die Bezeichner
  aus `tools/currency_exceptions.txt` nach Step 2, als Python-Menge ausgeschrieben)

```python
# First live run 2026-09-29: the identifiers recorded in Step 2. The set may only shrink; a swap is caught too.
FROZEN_EXCEPTIONS = frozenset({"--decompose", "--door"})  # replace with the exact Step-2 set


def test_exception_list_only_shrinks():
    cx = _load("currency_extract")
    entries = cx.parse_exceptions((ROOT / "tools" / "currency_exceptions.txt").read_text(encoding="utf-8"))
    assert set(entries) <= FROZEN_EXCEPTIONS, sorted(set(entries) - FROZEN_EXCEPTIONS)
```

- [ ] **Step 4: Erneuter Live-Lauf**

```bash
python tools/currency_check.py --cockpit-url https://dynamic-dome.com/workshop-cockpit
```

Expected: Exit 1 **nur noch** mit `retiring:claude-haiku-4-5-20251001:…` und `cockpit-differs:…` als rot (beide
gewollt bis Haiku-Nachfolger bzw. Re-Export); keine `missing:*`, keine `orphan-exception:*`. Gelbe Changelog-Befunde
lesen und je Zeile entscheiden (Kursänderung nötig → beheben; sonst im Commit „geprüft, keine Kursänderung").

- [ ] **Step 5: Verify**

Run: `python -m pytest tools -q` und `python tools/lint_currency.py` → beide grün.
Mentor: berührte Module in `agents/workshop-mentor.md` nachgezogen (Repo-Regel).

- [ ] **Step 6: Commit** (Kursfixes und Ausnahmen getrennt)

```bash
git add tools/currency_exceptions.txt tools/test_currency_check.py
git commit -m "chore(tools): record foreign identifiers from the first live currency run"
git add resources/ agents/workshop-mentor.md
git status --short
git commit -m "fix(course): drop undocumented flags found by the currency check (H-13, H-16)"
```

---

### Task 9: Privater Monatslauf (außerhalb des Repos)

Der Wrapper, seine Tests und die Windows-Aufgabe liegen bewusst **nicht** in diesem öffentlichen Repo. Vollständiger
Teilplan mit Code: privater Plan des Autors (Pfad im persönlichen Todo „Workshop-Kurs auffrischen", Abschnitt
Phase 2). Vertrag zu diesem Repo:

- Aufruf: `python -X utf8 tools/currency_check.py --cockpit-url https://dynamic-dome.com/workshop-cockpit` mit
  Arbeitsverzeichnis Repo-Root, ohne Konsolenfenster, Timeout 10 min.
- Auswertung nur über die letzte `SUMMARY`-Zeile; fehlt sie, gilt der Lauf als fehlgeschlagen (Review Focus 3).
- Todos: neue rote/gelbe Befunde → Drift-Todo; keine neuen Befunde und `canon_age_days > 60` → Bestätigungs-Todo
  einmal je `canon_checked`; Exit 2, Absturz, Timeout, fehlende `SUMMARY` → Fehlschlag-Todo.
- Live-Abnahme: `.currency/state.json` vorher nach `.currency/state.manual.json` umbenennen (sonst gelten die
  Befunde aus Task 8 als bekannt und es entsteht kein Todo), dann Aufgabe per `schtasks /Run` starten; Bericht,
  Todo und `runs.log` prüfen; kein Fenster sichtbar.

---

### Task 10: Doku und Buchführung

**Files:**
- Modify: `HOW-TO-USE.md` (Zeile „Currency-Checks")
- Modify: `CLAUDE.md`, `AGENTS.md` (Abschnitt „Regeln")
- Modify: `resources/review-2026-09-28/05-bewertung.md` (neuer Abschnitt am Ende)
- Modify: `docs/plans/2026-09-29-phase2-aktualhaltung-design.md` (Cockpit-Vergleich per URL)

- [ ] **Step 1: HOW-TO-USE.md** — die Zeile `- Currency-Checks: …` ersetzen durch:

```markdown
- Currency-Checks: `python tools/lint_currency.py` (Modellgenerationen nur im Kanon, Prüfdatum ≤ 90 Tage) und
  `python tools/currency_check.py [--cockpit-url <Website-Cockpit>]` (Kurs-Bezeichner gegen die Doku, Kanon gegen
  Deprecations/npm; Bericht unter `.currency/reports/`, Exit 0/1/2). Nach dem Abarbeiten eines Berichts
  `Geprüft:` in `resources/_canonical.md` setzen. Details: `docs/plans/2026-09-29-phase2-aktualhaltung-design.md`.
```

- [ ] **Step 2: CLAUDE.md und AGENTS.md** — unter `## Regeln` ergänzen (beide Dateien identisch):

```markdown
- Modellgenerationen, Preise, Kontextgrößen und Retirement-Daten nur in `resources/_canonical.md`; im Kurs Aliase
  (`opus`, `sonnet`, `haiku`, `fable`) und Rollen. Bewusste Ausnahme: `version-pinned: <Grund>` in derselben Zeile.
  `python tools/lint_currency.py` prüft das.
```

- [ ] **Step 3: Spec** — entfällt; der Cockpit-Vergleich per Live-URL wurde am 2026-09-29 zusammen mit
  diesem Plan in die Spec übernommen.

- [ ] **Step 4: Review-Datei** — an `resources/review-2026-09-28/05-bewertung.md` anhängen: Abschnitt
  „## Phase-2-Stand (Datum)" mit: Mechanismus (Lint-Regeln, Monatslauf), Sweep-Umfang (Zeilen/Dateien), Befunde
  des ersten Live-Laufs mit Einordnung (Fremd-Flag vs. Fehler, jeweils mit Beleg), Stand H-13 und H-16, offene
  Punkte (Haiku-Retirement, Cockpit-Re-Export).

- [ ] **Step 5: Verify + Commit**

Run: `python tools/lint_currency.py` und `python -m pytest tools -q` → grün.

```bash
git add HOW-TO-USE.md CLAUDE.md AGENTS.md resources/review-2026-09-28/05-bewertung.md docs/plans/2026-09-29-phase2-aktualhaltung-design.md
git commit -m "docs: currency upkeep workflow, alias rule for agents, phase 2 status"
```

---

### Task 11: Abschluss-Gates

- [ ] **Step 1: Vollständige Verifikation**

```bash
python -m pytest tools -q
python tools/lint_currency.py
cd workshop-playground && python -m pytest -q && cd ..
git status --short
git log --oneline origin/main..HEAD
```

Expected: alles grün, Arbeitsbaum sauber, Commits dieser Phase gelistet.

- [ ] **Step 2: Sweep vor dem Push** (öffentliches Repo)

```bash
git diff origin/main..HEAD | grep -niE "[A-Z]:[\/]Users[\/]|/home/|@gmail|sk-ant|ghp_|api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]" || echo "sweep clean"
```

Zusätzlich die privaten Namensmuster aus dem privaten Teilplan (Abschnitt „Sweep") gegen denselben Diff laufen
lassen. Expected: `sweep clean` in beiden Läufen. Jeder Treffer wird vor dem Push beseitigt.

- [ ] **Step 3: Unabhängiges Review** — ein frischer Reviewer (opus) prüft den ganzen Branch gegen Spec und Plan,
  inklusive Mutationsproben aus Task 4 und 6; danach Codex-Verifier anbieten.

- [ ] **Step 4: Owner-Gates (nur mit ausdrücklicher Freigabe)**
  - Push nach `origin/main`.
  - Cockpit-Re-Export auf die Website nach dem bewährten Verfahren (eigenes Repo, Provenienz-Zeile, Build, Live-sha
    = Commit-sha). Danach `python tools/currency_check.py --cockpit-url https://dynamic-dome.com/workshop-cockpit`:
    `cockpit-differs` ist verschwunden.
