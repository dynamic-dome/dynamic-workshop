# -*- coding: utf-8 -*-
"""Cockpit build: chapter HTML (sanitised, links rewritten) and the single-file cockpit artefact.

The artefact resources/claude-code-workshop-ui.html = tools/cockpit/template.html with the library data injected into
the one inline script. Constraints (spec section 8): exactly one <script>, no inline event handlers, no inline style
attributes, no external references, no confirm().
"""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import sys

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import markdown  # noqa: E402  (maintainer dependency)

ROOT = TOOLS.parent
TEMPLATE = TOOLS / "cockpit" / "template.html"
ARTEFACT = ROOT / "resources" / "claude-code-workshop-ui.html"
REPO_URL = "https://github.com/dynamic-dome/dynamic-workshop/blob/main/"
DATA_MARKER = "/*@@LIBRARY_DATA@@*/"
MAX_BYTES = 1_500_000
CHAPTER_FILE = re.compile(r"^(?:s[0-4]-\d{2}|x-\d{2})-[a-z0-9-]+\.md$")

ALLOWED = {
    "p": set(), "h2": {"id"}, "h3": {"id"}, "h4": {"id"}, "h5": set(), "h6": set(), "ul": set(), "ol": set(),
    "li": set(), "pre": {"class"}, "code": {"class"}, "blockquote": set(), "table": set(), "thead": set(),
    "tbody": set(), "tr": set(), "th": {"class"}, "td": {"class"}, "strong": set(), "em": set(), "a": {"href"},
    "details": set(), "summary": set(), "br": set(), "hr": set(), "kbd": set(), "sup": set(), "sub": set(),
    "del": set(), "div": {"class", "data-diagram"}, "span": {"class"},
}
VOID = {"br", "hr"}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "svg", "math", "template", "noscript"}


class _Sanitizer(HTMLParser):
    def __init__(self, rewrite):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip, self.rewrite = [], [], 0, rewrite

    def handle_starttag(self, tag, attrs):
        if self.skip or tag in DROP_WITH_CONTENT:
            if tag in DROP_WITH_CONTENT and tag not in VOID:
                self.skip += 1
            return
        if tag not in ALLOWED:
            return
        kept = []
        for name, value in attrs:
            value = value or ""
            if name == "style" and tag in ("th", "td"):
                match = re.search(r"text-align:\s*(left|right|center)", value)
                if match:
                    kept.append(("class", f"align-{match.group(1)}"))
                continue
            if name not in ALLOWED[tag]:
                continue
            if name == "class" and not re.fullmatch(r"[A-Za-z0-9 _-]*", value):
                continue
            if name == "id" and not re.fullmatch(r"[A-Za-z0-9_-]*", value):
                continue
            kept.append((name, value))
        if tag == "a":
            kept = self.rewrite(dict(kept).get("href", ""))
        attr_text = "".join(f' {n}="{escape(v, quote=True)}"' for n, v in kept)
        self.out.append(f"<{tag}{attr_text}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()
            self.out.append(f"</{tag}>")

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in ALLOWED or tag in VOID:
            return
        if tag in self.stack:
            while self.stack:
                top = self.stack.pop()
                self.out.append(f"</{top}>")
                if top == tag:
                    break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(escape(data, quote=False))

    def handle_comment(self, data):
        return

    def close(self):
        super().close()
        while self.stack:
            self.out.append(f"</{self.stack.pop()}>")
        return "".join(self.out)


def link_rewriter(ids_by_file, chapter_rel_dir="resources/library/"):
    """Returns a function href -> list of attributes for the cockpit (spec section 7, links)."""

    def rewrite(href):
        href = (href or "").strip()
        if not href:
            return []
        if href.startswith("#"):
            return [("href", href)]
        if re.match(r"^https?://", href):
            return [("href", href), ("target", "_blank"), ("rel", "noopener noreferrer")]
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):  # mailto:, javascript:, data: ...
            return []
        file_part, _, anchor = href.partition("#")
        name = file_part.rsplit("/", 1)[-1]
        if file_part == name and name in ids_by_file:
            cid = ids_by_file[name]
            return [("href", f"?run={cid}"), ("data-chapter", cid)]
        resolved = _resolve(chapter_rel_dir, file_part)
        url = REPO_URL + resolved + (f"#{anchor}" if anchor else "")
        return [("href", url), ("target", "_blank"), ("rel", "noopener noreferrer")]

    return rewrite


def _resolve(base_dir, rel):
    parts = [p for p in base_dir.strip("/").split("/") if p]
    for piece in rel.split("/"):
        if piece in ("", "."):
            continue
        if piece == "..":
            if parts:
                parts.pop()
        else:
            parts.append(piece)
    return "/".join(parts)


DETAILS_OPEN = re.compile(r"^<details>(\s*<summary>)", re.M)
QUIZ_BLOCK = re.compile(r"<details><summary>Quizfrage</summary>.*?</details>\s*", re.S)
META_BLOCK = re.compile(r"<!-- meta:start -->.*?<!-- meta:end -->\s*", re.S)
FENCE_MERMAID = re.compile(r"^```mermaid\n(.*?)^```\s*$", re.S | re.M)


def diagram_key(source):
    return hashlib.sha256(source.strip().encode("utf-8")).hexdigest()[:8]


def chapter_markdown_for_cockpit(text):
    """Strip front matter, H1, meta block and the quiz (the cockpit renders the quiz itself)."""
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        text = text[end + 5:] if end >= 0 else text
    text = META_BLOCK.sub("", text)
    text = re.sub(r"^# .*\n", "", text, count=1, flags=re.M)
    text = QUIZ_BLOCK.sub("", text)
    text = text.replace("<!-- cockpit:example -->\n", "")
    return text


def chapter_html(text, ids_by_file, diagrams=None):
    """Markdown chapter text -> sanitised HTML fragment for the cockpit."""
    diagrams = diagrams or {}
    md = chapter_markdown_for_cockpit(text)

    def mermaid(match):
        source = match.group(1)
        key = diagram_key(source)
        if key in diagrams:
            return f'\n<div class="diagram" data-diagram="{key}"></div>\n'
        return f'\n<pre class="diagram-source"><code>{escape(source)}</code></pre>\n'

    md = FENCE_MERMAID.sub(mermaid, md)
    md = DETAILS_OPEN.sub(r'<details markdown="1">\1', md)
    html = markdown.markdown(md, extensions=["fenced_code", "tables", "md_in_html", "sane_lists"],
                             output_format="html")
    parser = _Sanitizer(link_rewriter(ids_by_file))
    parser.feed(html)
    return parser.close()


def script_safe_json(data):
    """JSON that can sit inside a <script> element: no '</' and no U+2028/2029 surprises."""
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return text.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
