# -*- coding: utf-8 -*-
"""Pure extraction and parsing for the currency check: no network, no filesystem.

Consumers: tools/currency_check.py (monthly drift check) and tools/lint_currency.py (canon header).
Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md
"""
import datetime as dt
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
FOREIGN_LINE = re.compile(r"^- Fremdprojekt:\s*(https://\S+)\s+\((S\d\.\d+|X\.\d+)\)\s*$")
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


def parse_canon_foreign(text):
    """[(url, chapter)] of the `- Fremdprojekt: <url> (<chapter>)` lines; ValueError on a line without a chapter."""
    found = []
    for line in text.splitlines():
        if "Fremdprojekt:" not in line:
            continue  # any spelling that mentions the kind must be the exact form, or the source goes unwatched
        match = FOREIGN_LINE.match(line)
        if not match:
            raise ValueError(f"Kanon: Fremdprojekt-Zeile ohne Kapitel: {line}")
        found.append((match.group(1), match.group(2)))
    return found


def version_tuple(version):
    return tuple(int(part) for part in version.split("."))


def changelog_since(text, since):
    """Entries (version, line) of every release newer than `since`; ValueError if no listed release is <= `since`."""
    marks = [(m.start(), m.group(1)) for m in UPDATE.finditer(text)]
    since_t = version_tuple(since)
    if not any(version_tuple(v) <= since_t for _pos, v in marks):
        raise ValueError(f"Changelog: reicht nicht bis Version {since} zurueck")
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


def denied_in_docs(value, union):
    """First doc line that says `value` does not exist ("There is no `X`") or marks its table row "Removed in"."""
    quoted = re.escape(value)
    negation = re.compile(r"there is no `\$?" + quoted + "`", re.I)
    removed_row = re.compile(r"^\|\s*`" + quoted + r"`\s*\|.*removed in", re.I)
    for line in union.splitlines():
        if negation.search(line) or removed_row.search(line.strip()):
            return line.strip()
    return None


def normalize_cockpit(text):
    lines = text.replace("\r\n", "\n").split("\n")
    return "\n".join(line for line in lines if not PROVENANCE.match(line))


def normalize_foreign(text):
    """Readable text of a third-party page: scripts, styles, comments and tags dropped, whitespace collapsed.

    Build hashes and markup changes of a docs site then do not count as a content change."""
    text = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())


def parse_exceptions(text):
    entries = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|", 2)]
        files = frozenset(f.strip() for f in parts[1].split(",") if f.strip()) if len(parts) == 3 else frozenset()
        if len(parts) != 3 or not files or len(parts[2]) < 3:
            raise ValueError(f"Ausnahme Zeile {number}: Format 'bezeichner | datei[, datei] | grund' "
                             "(mindestens eine Datei, Grund mindestens 3 Zeichen)")
        entries[parts[0]] = {"files": files, "reason": parts[2]}
    return entries
