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
MAX_BYTES = 3_000_000  # single offline file; gzip on the wire is about a seventh (measured 2026-09-30)
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
EMPTY_ELEMENTS = {"embed", "img", "input", "source", "track", "wbr", "param", "area", "base", "link", "meta", "col"}


class _Sanitizer(HTMLParser):
    def __init__(self, rewrite):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip, self.rewrite = [], [], 0, rewrite

    def handle_starttag(self, tag, attrs):
        if self.skip or tag in DROP_WITH_CONTENT:
            if tag in DROP_WITH_CONTENT and tag not in VOID and tag not in EMPTY_ELEMENTS:
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
        if tag in DROP_WITH_CONTENT:
            return  # <svg/>, <iframe/>: nothing inside to drop, and no end tag will close it
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


def natural_size(svg):
    """Mermaid writes width="100%": a wide flowchart then shrinks to column width and its 15 px labels become
    unreadable. Give the SVG its viewBox size instead; the .diagram box scrolls horizontally when it is wider."""
    match = re.search(r'viewBox="[\d.\s-]*?\s([\d.]+)\s([\d.]+)"', svg)
    if not match:
        return svg
    width, height = (round(float(v)) for v in match.groups())
    svg = re.sub(r'(<svg\b[^>]*?)\swidth="100%"', r"\1", svg, count=1)
    return svg.replace("<svg", f'<svg width="{width}" height="{height}"', 1)


STYLE_BLOCK = re.compile(r"<style>(.*?)</style>", re.S)
GEOMETRY = re.compile(r'(\s(?:d|x|y|x1|x2|y1|y2|cx|cy|r|rx|ry|width|height|transform|points|viewBox)=")([^"]*)(")')
LONG_NUMBER = re.compile(r"(\d+\.\d{2})\d+")


def share_diagram_styles(diagrams):
    """Mermaid repeats an id-scoped <style> block in every SVG (a fifth of its bytes), though there are only a few
    distinct ones. Rescope each block to a class, ship every distinct block once and round geometry to two decimals
    (text such as version numbers stays untouched). Returns ({key: svg}, {class: css})."""
    shared, css = {}, {}
    for key, svg in diagrams.items():
        svg = natural_size(svg)
        match = STYLE_BLOCK.search(svg)
        if match:
            rules = re.sub(rf"#d{key}(?![\w-])", "#MMD", match.group(1))
            # ids with a suffix (url(#d<key>-gradient)) only serve the unused "neo" look; neutral name, same rule
            rules = re.sub(rf"#d{key}(?=[\w-])", "#mmd", rules)
            cls = "mmd-" + hashlib.sha256(rules.encode("utf-8")).hexdigest()[:6]
            css[cls] = rules.replace("#MMD", "." + cls)
            svg = svg[:match.start()] + svg[match.end():]
            if re.search(r'<svg\b[^>]*\sclass="', svg):
                svg = re.sub(r'(<svg\b[^>]*?\sclass=")([^"]*)"', lambda m: f'{m.group(1)}{m.group(2)} {cls}"', svg,
                             count=1)
            else:
                svg = svg.replace("<svg", f'<svg class="{cls}"', 1)
        shared[key] = GEOMETRY.sub(lambda m: m.group(1) + LONG_NUMBER.sub(r"\1", m.group(2)) + m.group(3), svg)
    return shared, css


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


def inline_html(text, ids_by_file):
    """Short Markdown (code spans, bold, links) -> sanitised inline HTML without the outer <p>."""
    if not text:
        return ""
    html = markdown.markdown(text, output_format="html")
    parser = _Sanitizer(link_rewriter(ids_by_file))
    parser.feed(html)
    out = parser.close().strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        out = out[3:-4]
    return out


def script_safe_json(data):
    """JSON that can sit inside a <script> element: no '</', no '<!--' (script data escape state) and no U+2028/2029
    surprises. Both escapes stay valid JSON and JavaScript."""
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    text = text.replace("<!--", "\\u003c!--").replace("</", "<\\/")
    return text.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def cockpit_data(lib, catalog, diagrams=None):
    """Catalog plus sanitised chapter HTML and optional pre-rendered diagrams (spec section 8)."""
    diagrams = diagrams or {}
    ids_by_file = {c.path.name: c.id for c in lib.chapters}
    data = json.loads(json.dumps(catalog))  # deep copy
    for entry in data["chapters"]:
        ch = lib.by_id[entry["id"]]
        entry["html"] = chapter_html(ch.path.read_text(encoding="utf-8"), ids_by_file, diagrams)
        for key in ("glance", "analogy", "checkpoint", "outcome"):
            entry[key + "_html"] = inline_html(entry.get(key) or "", ids_by_file)
        entry["skip_check_html"] = [inline_html(q, ids_by_file) for q in entry.get("skip_check") or []]
        entry["recall_html"] = [inline_html(q, ids_by_file) for q in entry.get("recall") or []]
        entry["answers_html"] = [inline_html(a, ids_by_file) for a in entry.get("answers") or []]
        if entry.get("quiz"):
            q = entry["quiz"]
            entry["quiz_html"] = {"q": inline_html(q["q"], ids_by_file), "correct": inline_html(q["correct"], ids_by_file),
                                  "wrong": [inline_html(w, ids_by_file) for w in q["wrong"]]}
        entry["full_url"] = REPO_URL + "resources/library/" + ch.path.name
    data["diagrams"], data["diagram_css"] = share_diagram_styles(diagrams)
    return data


def render(lib, catalog, template_text=None, diagrams=None):
    """Template + data -> artefact text. Over MAX_BYTES the diagrams go first (Mermaid source instead), then the full
    chapter text (link to the GitHub version instead): reading matters more than pictures."""
    template_text = template_text if template_text is not None else TEMPLATE.read_text(encoding="utf-8")
    if DATA_MARKER not in template_text:
        raise ValueError("Template ohne Datenmarker " + DATA_MARKER)

    def fill(data):
        return template_text.replace(DATA_MARKER + "null", script_safe_json(data), 1)

    text = fill(cockpit_data(lib, catalog, diagrams))
    if len(text.encode("utf-8")) > MAX_BYTES and diagrams:
        text = fill(cockpit_data(lib, catalog, {}))
    if len(text.encode("utf-8")) > MAX_BYTES:
        data = cockpit_data(lib, catalog, {})
        for entry in data["chapters"]:
            entry["html"] = None
        text = fill(data)
    problems = artefact_problems(text)
    if problems:
        raise ValueError("Cockpit-Artefakt verletzt Vorgaben: " + "; ".join(problems))
    return text


def artefact_problems(text):
    problems = []
    if len(re.findall(r"<script\b", text, re.I)) != 1:
        problems.append("nicht genau ein <script>")
    # the embedded JSON writes attribute quotes as \" - look at the markup the browser will actually build
    markup = text.replace('\\"', '"')
    if re.search(r"<(?:link|img|iframe|object|embed|use|image)\b[^>]*(?:src|href)=\"(?:https?:)?//", markup, re.I):
        problems.append("externe Referenz")
    if re.search(r"\son[a-z]+\s*=\s*[\"']", markup, re.I):
        problems.append("Inline-Event-Handler")
    if re.search(r"<[a-z][^>]*\sstyle=\"", markup, re.I):
        problems.append("Inline-style-Attribut")
    if "confirm(" in text:
        problems.append("confirm()")
    hrefs = re.findall(r'href=\\?"([^"\\]*)', text)
    for href in hrefs:
        if href and not href.startswith(("?", "#", "https://", "data:", "${")):
            problems.append("relativer Link " + href)
            break
    return problems
