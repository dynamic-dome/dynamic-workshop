# -*- coding: utf-8 -*-
"""Chapter model of the practice library (resources/library/).

A chapter is a Markdown file with a narrow YAML front matter and fixed H2 sections
(spec docs/plans/2026-09-30-praxisbibliothek-design.md, section 4). This module only
parses; tools/build_library.py validates and generates.

Chapters are written for one person learning alone. The demo and the notes for moderators of a
chapter live in the moderation layer, resources/moderation/vorfuehren/<chapter file>
(design docs/plans/2026-10-05-selbstlern-zuerst-design.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

import yaml

_TOOLS = str(Path(__file__).resolve().parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
import catalog_core as _core  # noqa: E402

SECTION_ORDER = [
    "Schnellcheck", "Auf einen Blick", "Bild im Kopf", "Im Detail",
    "Selbst machen", "Typische Fallen", "Check", "Weiterlesen",
]
DEMO_FOLDER = ("moderation", "vorfuehren")  # next to the library folder
MODERATOR_BLOCK = "<summary>Für Moderierende</summary>"
CHAPTER_TYPES = ("lesson", "setup", "practice", "capstone", "community")
LEVELS = ("core", "deep-dive", "bonus")

SESSION_ID = _core.SESSION_ID
EXTRA_ID = _core.EXTRA_ID
FENCE = re.compile(r"^\s*(```|~~~)")
H2 = re.compile(r"^## (.+?)\s*$")
META_START, META_END = "<!-- meta:start -->", "<!-- meta:end -->"
EXAMPLE_MARKER = "<!-- cockpit:example -->"
GENERATED_NAMES = ("README.md", "einstufung.md")  # generated into the library folder by build_library
LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
QUIZ_BLOCK = re.compile(r"<details><summary>Quizfrage</summary>(.*?)</details>", re.S)
QUIZ_QUESTION = re.compile(r"^\*\*Frage:\*\*\s*(.+?)\s*$", re.M)
QUIZ_RIGHT = re.compile(r"^- \*\*Richtig:\*\*\s*(.+?)\s*$", re.M)
QUIZ_WRONG = re.compile(r"^- Falsch:\s*(.+?)\s*$", re.M)


class ChapterError(Exception):
    def __init__(self, path, message):
        super().__init__(f"{path}: {message}")
        self.path = str(path)
        self.message = message


@dataclass(frozen=True)
class Quiz:
    question: str
    correct: str
    wrong: list
    n_correct: int = 1
    closed: bool = True


@dataclass
class Chapter:
    path: Path
    id: str
    type: str
    title: str
    shelf: str
    level: str
    minutes: int
    requires: list
    safety_floor: bool
    transferable: bool
    outcome: str
    sources: list
    aliases: list
    after: str | None
    offers: list
    front: dict
    h1: str
    preamble: str
    sections: dict
    section_order: list
    quiz: Quiz | None
    example: str | None
    example_lang: str
    skip_check: list
    glance: str
    analogy: str
    checkpoint: str
    mermaid: list
    links: list
    demo: Path | None = None  # file in the moderation layer, if this chapter has a demo

    @property
    def order(self) -> int:
        return order_of(self.id, self.after)

    @property
    def session(self) -> int | None:
        match = SESSION_ID.match(self.id)
        return int(match.group(1)) if match else None


@dataclass
class Library:
    root: Path
    chapters: list
    shelves: list
    placement: dict
    problems: list = field(default_factory=list)

    @property
    def demo_dir(self) -> Path:
        return demo_dir(self.root)

    @property
    def by_id(self) -> dict:
        return {c.id: c for c in self.chapters}


def demo_dir(library_root) -> Path:
    """Folder of the moderation layer that belongs to a library folder."""
    return Path(library_root).parent.joinpath(*DEMO_FOLDER)


def order_of(chapter_id: str, after: str | None) -> int:
    """Teaching order (single definition in catalog_core)."""
    return _core.order_of(chapter_id, after)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def _split_front(path: Path, text: str):
    if not text.startswith("---\n"):
        raise ChapterError(path, "Frontmatter fehlt (Datei muss mit '---' beginnen)")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ChapterError(path, "Frontmatter ist nicht geschlossen")
    try:
        front = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as err:
        raise ChapterError(path, f"Frontmatter ist kein gültiges YAML: {err}") from err
    if not isinstance(front, dict):
        raise ChapterError(path, "Frontmatter muss ein Mapping sein")
    return front, text[end + 5:]


def _strip_meta(body: str) -> str:
    out, inside = [], False
    for line in body.split("\n"):
        if line.strip() == META_START:
            inside = True
            continue
        if line.strip() == META_END:
            inside = False
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def _split_sections(body: str):
    """Split by H2 outside code fences. Returns (h1, preamble, {title: text}, [titles])."""
    h1, pre, sections, order = "", [], {}, []
    current, buf, in_fence = None, [], False

    def flush():
        if current is not None:
            sections[current] = "\n".join(buf).strip("\n")

    for line in body.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence:
            h2 = H2.match(line)
            if h2:
                flush()
                current, buf = h2.group(1), []
                order.append(current)
                continue
            if current is None and not h1 and line.startswith("# "):
                h1 = line[2:].strip()
                continue
        (buf if current is not None else pre).append(line)
    flush()
    return h1, "\n".join(pre).strip("\n"), sections, order


def _paragraphs(text: str) -> list:
    """Top-level paragraphs, skipping code fences, lists, headings, HTML and blockquotes."""
    paras, buf, in_fence = [], [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if stripped.startswith(("- ", "* ", "#", "<", ">", "|")) or re.match(r"^\d+\. ", stripped):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        buf.append(stripped)
    if buf:
        paras.append(" ".join(buf))
    return paras


def _first_paragraph(text: str) -> str:
    paras = _paragraphs(text or "")
    return paras[0] if paras else ""


def _list_items(text: str) -> list:
    return [m.group(1).strip() for m in re.finditer(r"^- (.+)$", text or "", re.M)]


def _fences(text: str):
    """Yield (lang, content, start_index_of_opening_line) for each fenced block."""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        match = FENCE.match(lines[i])
        if match:
            ticks = match.group(1)
            lang = lines[i].strip()[len(ticks):].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(ticks):
                j += 1
            yield lang, "\n".join(lines[i + 1:j]), i
            i = j + 1
        else:
            i += 1


def _example(text: str):
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if line.strip() == EXAMPLE_MARKER:
            rest = "\n".join(lines[idx + 1:])
            for lang, content, _ in _fences(rest):
                return content, lang
            return None, ""
    return None, ""


def _quiz(check_text: str):
    text = check_text or ""
    block = QUIZ_BLOCK.search(text)
    if not block:
        if "<details><summary>Quizfrage</summary>" in text:
            return Quiz("", "", [], 0, closed=False)  # opened but never closed
        return None
    inner = block.group(1)
    question = QUIZ_QUESTION.search(inner)
    rights = QUIZ_RIGHT.findall(inner)
    wrong = QUIZ_WRONG.findall(inner)
    return Quiz(question.group(1) if question else "", rights[0] if rights else "", wrong, len(rights))


def _links(body: str) -> list:
    out, in_fence = [], False
    for line in body.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.extend(LINK.findall(line))
    return out


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def parse_chapter(path) -> Chapter:
    path = Path(path)
    front, body = _split_front(path, _read(path))
    body = _strip_meta(body)
    h1, preamble, sections, order = _split_sections(body)
    example, lang = None, ""
    for title in ("Selbst machen", "Im Detail", "Check"):
        if title in sections:
            example, lang = _example(sections[title])
            if example is not None:
                break
    mermaid = [content for text in sections.values() for fl, content, _ in _fences(text) if fl == "mermaid"]
    minutes = front.get("minutes")
    demo = demo_dir(path.parent) / path.name
    return Chapter(
        path=path,
        id=str(front.get("id", "")),
        type=str(front.get("type", "")),
        title=str(front.get("title", "")),
        shelf=str(front.get("shelf", "")),
        level=str(front.get("level", "")),
        minutes=minutes if isinstance(minutes, int) else 0,
        requires=_as_list(front.get("requires")),
        safety_floor=front.get("safety_floor") is True,
        transferable=front.get("transferable") is True,
        outcome=str(front.get("outcome", "")),
        sources=_as_list(front.get("sources")),
        aliases=_as_list(front.get("aliases")),
        after=front.get("after"),
        offers=_as_list(front.get("offers")),
        front=front,
        h1=h1,
        preamble=preamble,
        sections=sections,
        section_order=order,
        quiz=_quiz(sections.get("Check", "")),
        example=example,
        example_lang=lang,
        skip_check=_list_items(sections.get("Schnellcheck", "")),
        glance=_first_paragraph(sections.get("Auf einen Blick", "")),
        analogy=_first_paragraph(sections.get("Bild im Kopf", "")),
        checkpoint=_first_paragraph(sections.get("Check", "")),
        mermaid=mermaid,
        links=_links(body),
        demo=demo if demo.is_file() else None,
    )


def _load_yaml(path: Path, default):
    if not path.exists():
        return default
    return yaml.safe_load(_read(path)) or default


def load_library(root) -> Library:
    root = Path(root)
    chapters, problems = [], []
    with __import__("os").scandir(root) as entries:
        names = sorted(e.name for e in entries if e.is_file() and e.name.endswith(".md"))
    for name in names:
        if name in GENERATED_NAMES:
            continue
        if not re.match(r"^(s[0-4]-\d{2}|x-\d{2})-", name):
            problems.append(ChapterError(root / name, "Datei gehört nicht in die Bibliothek oder hat einen ungültigen "
                                         "Kapitel-Dateinamen (erwartet s<s>-<nn>-<slug>.md oder x-<nn>-<slug>.md)"))
            continue
        try:
            chapters.append(parse_chapter(root / name))
        except ChapterError as err:
            problems.append(err)

    def sort_key(ch):
        try:
            return (0, ch.order, ch.id)
        except ValueError:
            return (1, 0, ch.id)

    chapters.sort(key=sort_key)
    return Library(root=root, chapters=chapters, shelves=_load_yaml(root / "_shelves.yaml", []),
                   placement=_load_yaml(root / "_placement.yaml", {}), problems=problems)
