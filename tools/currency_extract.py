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
