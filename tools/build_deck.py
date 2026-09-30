# -*- coding: utf-8 -*-
"""Overview deck of the practice library, generated from the catalog (spec section 11).

  python tools/build_deck.py [--catalog resources/library/catalog.json] [--out resources/media/claude-code-praxisbibliothek.pptx]

All numbers and chapter lists come from the catalog, so the deck never drifts from the library. Diagrams are native
shapes (editable in PowerPoint). Speaker notes in German. Maintainer dependency: python-pptx.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "resources" / "library" / "catalog.json"
OUT = ROOT / "resources" / "media" / "claude-code-praxisbibliothek.pptx"
META = ROOT / "docs" / "migration" / "chapter-meta.yaml"

BG = RGBColor(0x14, 0x18, 0x1C)
SURFACE = RGBColor(0x1F, 0x26, 0x2D)
RAISE = RGBColor(0x2A, 0x33, 0x3C)
LINE = RGBColor(0x3A, 0x45, 0x50)
INK = RGBColor(0xE9, 0xED, 0xF1)
INK2 = RGBColor(0xB4, 0xBE, 0xC8)
MUTED = RGBColor(0x8F, 0x9B, 0xA7)
ACCENT = RGBColor(0xE0, 0xA5, 0x26)
WORK = RGBColor(0xFA, 0xB2, 0x19)
SKIM = RGBColor(0x5A, 0xA0, 0xEC)
DONE = RGBColor(0x2F, 0xB3, 0x44)
WARN = RGBColor(0xEC, 0x83, 0x5A)
FONT, MONO = "Calibri", "Consolas"
W, H = Inches(13.333), Inches(7.5)
LEVEL = {"core": "Kern", "deep-dive": "Vertiefung", "bonus": "Kür"}


# --- primitives ---------------------------------------------------------------------------------------------

def blank(prs, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = BG
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def box(slide, x, y, w, h, fill=SURFACE, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1.25)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def text(slide, x, y, w, h, runs, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         font=FONT, spacing=None):
    """runs: str, or list of paragraphs; a paragraph is a str or a list of (text, {overrides})."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, side, 0)
    paragraphs = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.space_after = Pt(spacing)
        parts = para if isinstance(para, list) else [(para, {})]
        for content, opt in parts:
            r = p.add_run()
            r.text = content
            f = r.font
            f.name = opt.get("font", font)
            f.size = Pt(opt.get("size", size))
            f.bold = opt.get("bold", bold)
            f.italic = opt.get("italic", False)
            f.color.rgb = opt.get("color", color)
    return tb


def arrow(slide, x1, y1, x2, y2, color=MUTED):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color
    c.line.width = Pt(1.75)
    ln = c.line._get_or_add_ln()
    tail = ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"})
    ln.append(tail)
    return c


def title(slide, eyebrow, heading, sub=None):
    text(slide, Inches(0.7), Inches(0.5), Inches(11.5), Inches(0.35), eyebrow, size=14, color=ACCENT, bold=True)
    text(slide, Inches(0.7), Inches(0.85), Inches(11.9), Inches(0.9), heading, size=36, bold=True)
    if sub:
        text(slide, Inches(0.7), Inches(1.72), Inches(11.5), Inches(0.6), sub, size=17, color=INK2)


def node(slide, x, y, w, h, label, sub=None, fill=SURFACE, color=INK, line=LINE, size=15):
    box(slide, x, y, w, h, fill=fill, line=line)
    paras = [[(label, {"bold": True, "size": size, "color": color})]]
    if sub:
        paras.append([(sub, {"size": size - 3, "color": INK2})])
    text(slide, x + Inches(0.15), y, w - Inches(0.3), h, paras, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def flow(slide, items, x, y, w_each, h, gap, fill=SURFACE):
    """Left-to-right process of (label, sub) nodes with arrows."""
    for i, (label, sub) in enumerate(items):
        nx = x + i * (w_each + gap)
        node(slide, nx, y, w_each, h, label, sub, fill=fill)
        if i < len(items) - 1:
            arrow(slide, nx + w_each + Inches(0.05), y + h // 2, nx + w_each + gap - Inches(0.05), y + h // 2)


# --- data -----------------------------------------------------------------------------------------------------

def load_catalog(path):
    cat = json.loads(Path(path).read_text(encoding="utf-8"))
    if cat["chapters"] and "title" not in cat["chapters"][0] and META.exists():
        import yaml
        titles = {e["id"]: e["title"] for e in yaml.safe_load(META.read_text(encoding="utf-8"))}
        for c in cat["chapters"]:
            c["title"] = titles.get(c["id"], c["id"])
    shelves = cat.get("shelves", [])
    if shelves and "zone" not in shelves[0]:
        import yaml
        full = {s["id"]: s for s in yaml.safe_load((ROOT / "resources" / "library" / "_shelves.yaml").read_text(encoding="utf-8"))}
        cat["shelves"] = [full.get(s["id"], s) for s in shelves]
    return cat


def hours(minutes):
    halves = (minutes * 2 + 30) // 60
    value = halves / 2
    return (f"{value:.1f}".rstrip("0").rstrip(".").replace(".", ",")) + " h"


# --- slides ---------------------------------------------------------------------------------------------------

def slide_title(prs, cat):
    chapters = cat["chapters"]
    total = sum(c["minutes"] for c in chapters)
    s = blank(prs, "Willkommen. Diese Bibliothek ersetzt den linearen Kurs: Du musst nicht alles durcharbeiten. "
                   "Eine kurze Einstufung zeigt, welche Kapitel zu deinem Stand und Ziel passen.")
    # floor-plan motif: a small door grid on the right
    for row in range(5):
        for col in range(6):
            fill = [WORK, SKIM, RAISE, RAISE, DONE][(row + col) % 5]
            box(s, Inches(8.3) + col * Inches(0.72), Inches(1.6) + row * Inches(0.95), Inches(0.56), Inches(0.72),
                fill=fill if (row * 6 + col) % 3 else RAISE, radius=0.12)
    text(s, Inches(0.8), Inches(1.5), Inches(7.2), Inches(1.9), ["Claude Code", "Praxisbibliothek"], size=48, bold=True)
    text(s, Inches(0.8), Inches(3.55), Inches(6.9), Inches(1.0), "Lernen nach deinem Stand — von der ersten Datei bis zur "
         "abgesicherten Agenten-Pipeline.", size=20, color=INK2)
    stats = [(str(len(chapters)), "Kapitel"), (str(len(cat["shelves"])), "Regale"), (hours(total), "Gesamtumfang"),
             ("4", "Live-Sessions")]
    for i, (big, small) in enumerate(stats):
        x = Inches(0.8) + i * Inches(1.75)
        text(s, x, Inches(4.9), Inches(1.6), Inches(0.8), big, size=40, bold=True, color=ACCENT)
        text(s, x, Inches(5.7), Inches(1.6), Inches(0.4), small, size=14, color=MUTED)


def slide_agent(prs):
    s = blank(prs, "Das Denkmodell zuerst: Ein Chat berät, ein Coding-Agent handelt in deiner Umgebung. Jede Freigabe hat "
                   "echte Folgen — deshalb gehören Rechte-Modi, Hooks und das Prüfen von Ergebnissen zum Grundhandwerk.")
    title(s, "Denkmodell", "Ein Agent handelt — du gibst frei und prüfst.")
    flow(s, [("Auftrag", "Ziel, Grenzen, Prüfschritt"), ("Plan", "lesen, vorschlagen"), ("Werkzeug", "Read, Edit, Bash …"),
             ("Freigabe", "Rechte-Modus entscheidet"), ("Ergebnis", "Diff, Ausgabe, Tests")],
         Inches(0.7), Inches(2.9), Inches(2.1), Inches(1.3), Inches(0.42))
    arrow(s, Inches(12.3), Inches(4.3), Inches(12.3), Inches(5.1))
    node(s, Inches(7.4), Inches(5.1), Inches(5.2), Inches(1.0), "Du prüfst selbst", "Ein grüner Bericht ist kein Beweis — "
         "ausgeführter Code ist einer.", fill=RAISE, line=ACCENT)
    text(s, Inches(0.7), Inches(5.2), Inches(6.2), Inches(1.2), [[("Chat: ", {"bold": True}), ("gibt Ratschläge, du setzt um.", {})],
         [("Agent: ", {"bold": True}), ("setzt um, du steuerst die Freigaben.", {})]], size=18, color=INK2, spacing=6)


def slide_ways(prs):
    s = blank(prs, "Drei Einstiege, je nach Zeit und Vorlieben. Alle drei führen in dieselben Kapitel.")
    title(s, "Einstieg", "Drei Wege in die Bibliothek")
    ways = [("Einstufung", "Fünf Minuten: Ziel, Zeit, was du schon kannst. Ergebnis: dein Pfad in Etappen.",
             "Cockpit · /workshop start · einstufung.md"),
            ("Fertiger Pfad", "Schnellstart, ein Pfad je Ziel oder die vier Live-Sessions.", "resources/paths/"),
            ("Stöbern", "Regale als Gebäudeplan. Jedes Kapitel beginnt mit einem Schnellcheck.", "resources/library/")]
    for i, (head, body, where) in enumerate(ways):
        x = Inches(0.7) + i * Inches(4.05)
        box(s, x, Inches(2.5), Inches(3.75), Inches(3.6), fill=SURFACE, line=LINE)
        box(s, x + Inches(0.3), Inches(2.8), Inches(0.62), Inches(0.62), fill=[ACCENT, SKIM, DONE][i], shape=MSO_SHAPE.OVAL)
        text(s, x + Inches(0.3), Inches(3.6), Inches(3.2), Inches(0.5), head, size=24, bold=True)
        text(s, x + Inches(0.3), Inches(4.2), Inches(3.2), Inches(1.2), body, size=16, color=INK2)
        text(s, x + Inches(0.3), Inches(5.45), Inches(3.2), Inches(0.4), where, size=13, color=MUTED, font=MONO)


def slide_placement(prs, cat):
    rules = cat["placement"]
    s = blank(prs, "Die Einstufung fragt nach Verhalten, nicht nach Wissen, weil Selbsteinschätzung zu Überschätzung neigt. "
                   "Weiß nicht ist eine gute Antwort. Mini-Szenarien sind freiwillig und unbenotet. Sicherheitskapitel fallen "
                   "nie unter Überfliegen, außer du entscheidest es selbst.")
    title(s, "Einstufung", "In fünf Minuten zum persönlichen Pfad", "Keine Noten. Das Ergebnis ist eine Empfehlung, die du jederzeit änderst.")
    steps = [("1  Ziel", f"{len(rules['goals'])} Ziele, höchstens zwei"), ("2  Warum + Zeit", "Sitzungslänge oder Schnellstart"),
             ("3  Stand", f"{len(rules['areas'])} Bereiche, Verhaltensfragen"), ("4  Szenarien", f"{len(rules['scenarios'])} Stolpersteine, freiwillig")]
    flow(s, steps + [("Mein Pfad", "Etappen mit Begründung")], Inches(0.7), Inches(2.8), Inches(2.02), Inches(1.25),
         Inches(0.38))
    legend = [("durcharbeiten", WORK), ("überfliegen", SKIM), ("Schnellcheck reicht", MUTED), ("später", LINE)]
    text(s, Inches(0.7), Inches(4.7), Inches(6), Inches(0.4), "Je Kapitel ein Status mit Begründung:", size=16, color=INK2)
    for i, (label, col) in enumerate(legend):
        x = Inches(0.7) + i * Inches(2.2)
        box(s, x, Inches(5.25), Inches(0.28), Inches(0.28), fill=col, shape=MSO_SHAPE.OVAL)
        text(s, x + Inches(0.4), Inches(5.2), Inches(1.8), Inches(0.4), label, size=15)
    text(s, Inches(0.7), Inches(6.0), Inches(11.8), Inches(0.8), "Etappen folgen immer der Lehrreihenfolge; die Zeitangabe "
         "schneidet sie in Sitzungen. Voraussetzungen kommen automatisch mit.", size=15, color=MUTED)


def slide_map(prs, cat):
    s = blank(prs, "Der Gebäudeplan: Stockwerke sind Themenzonen, Räume sind Regale, jede Tür ist ein Kapitel. Im Cockpit "
                   "zeigt die Farbe deiner Türen deine Empfehlung.")
    title(s, "Bibliothek", "Der Gebäudeplan: Zonen, Regale, Kapitel")
    zones = []
    for sh in cat["shelves"]:
        if sh.get("zone") not in zones:
            zones.append(sh.get("zone"))
    count = {}
    for c in cat["chapters"]:
        count[c["shelf"]] = count.get(c["shelf"], 0) + 1
    y = Inches(2.0)
    row_h = Inches(0.95)
    for zone in zones:
        shelves = [sh for sh in cat["shelves"] if sh.get("zone") == zone]
        text(s, Inches(0.7), y + Inches(0.2), Inches(2.0), Inches(0.6), zone, size=15, bold=True, color=INK2)
        x = Inches(2.8)
        width = min(Inches(1.72), int((Inches(12.6) - Inches(2.8)) / max(len(shelves), 1)) - Inches(0.12))
        for sh in shelves:
            box(s, x, y, width, row_h - Inches(0.15), fill=SURFACE, line=LINE, radius=0.04)
            text(s, x + Inches(0.1), y + Inches(0.06), width - Inches(0.2), Inches(0.5), sh["title"], size=12, bold=True)
            text(s, x + Inches(0.1), y + Inches(0.5), width - Inches(0.2), Inches(0.3), f"{count.get(sh['id'], 0)} Kapitel",
                 size=11, color=MUTED)
            x += width + Inches(0.12)
        y += row_h


def slide_floor(prs, cat):
    floor = [c for c in cat["chapters"] if c.get("safety_floor")]
    s = blank(prs, "Neun Kapitel empfehlen wir allen, auch Fortgeschrittenen, mindestens zum Überfliegen. Das Wichtigste: "
                   "Nur exit 2 blockt, ein abstürzender Hook lässt die Aktion durch. Und claude -p ohne --bare führt die Hooks "
                   "eines fremden Repos aus.")
    title(s, "Sicherheitsboden", f"{len(floor)} Kapitel, die niemand auslässt",
          "Wer ein Feature nutzt, liest dessen Sicherheitskapitel — auch ohne passendes Ziel.")
    for i, c in enumerate(floor):
        col, row = i % 3, i // 3
        x, y = Inches(0.7) + col * Inches(4.05), Inches(2.6) + row * Inches(1.35)
        box(s, x, y, Inches(3.8), Inches(1.15), fill=SURFACE, line=LINE)
        text(s, x + Inches(0.2), y + Inches(0.15), Inches(1.0), Inches(0.4), c["id"], size=14, bold=True, color=ACCENT, font=MONO)
        text(s, x + Inches(0.2), y + Inches(0.5), Inches(3.45), Inches(0.6), c.get("title", ""), size=14)


def slide_session(prs, cat, session, name, mission, diagram, notes):
    chapters = [c for c in cat["chapters"] if c.get("session") == session]
    s = blank(prs, notes)
    minutes = sum(c["minutes"] for c in chapters if c["level"] == "core")
    title(s, f"Session {session} · {len(chapters)} Kapitel · Kern {minutes} Min", name, mission)
    # chapter list (left): ID column + title column with hanging indent, row height by title length
    top, bottom = Inches(2.45), Inches(6.45)
    col_w, title_w, chars_per_line = Inches(3.4), Inches(2.62), 33
    listed = chapters if len(chapters) <= 12 else [c for c in chapters if c["level"] == "core"]
    rest = [c for c in chapters if c not in listed]
    x, yy, column = Inches(0.7), top, 0
    chars_per_line = 36
    for c in listed:
        lines = 1 + (len(c.get("title", "")) - 1) // chars_per_line
        row = Inches(0.21) * lines + Inches(0.1)
        if yy + row > bottom:
            column += 1
            x, yy = x + col_w, top
        if column > 1:  # never a third column: the diagram lives there
            rest.insert(len(rest) - len([r for r in rest if r["order"] > c["order"]]), c)
            continue
        colr = INK if c["level"] == "core" else (INK2 if c["level"] == "deep-dive" else MUTED)
        text(s, x, yy, Inches(0.7), Inches(0.3), c["id"], size=11, color=ACCENT, font=MONO)
        text(s, x + Inches(0.62), yy, title_w + Inches(0.06), row, c.get("title", ""), size=11, color=colr,
             bold=c["level"] == "core")
        yy += row
    if rest:
        text(s, Inches(0.7), Inches(6.5), Inches(6.6), Inches(0.35),
             [[("Weitere: ", {"bold": True, "color": INK2}),
               (" · ".join(c["id"] for c in sorted(rest, key=lambda r: r["order"])), {"font": MONO})]],
             size=11, color=MUTED)
    text(s, Inches(0.7), Inches(6.95), Inches(6.5), Inches(0.3), "fett = Kern · normal = Vertiefung · grau = Kür", size=11,
         color=MUTED)
    diagram(s, Inches(7.55), Inches(2.5))


def diagram_modes(s, x, y):
    modes = [("Manual (default)", "nur Lesen"), ("acceptEdits", "+ Datei-Änderungen"), ("plan", "lesen, planen"),
             ("auto", "Klassifikator prüft"), ("dontAsk", "nur Vorab-Erlaubtes"), ("bypassPermissions", "alles — nur in VMs")]
    text(s, x, y, Inches(5), Inches(0.4), "Sechs Rechte-Modi — wie Zutrittsebenen", size=15, bold=True, color=INK2)
    for i, (m, d) in enumerate(modes):
        yy = y + Inches(0.55) + i * Inches(0.63)
        box(s, x + i * Inches(0.18), yy, Inches(4.4), Inches(0.52), fill=[SURFACE, SURFACE, SURFACE, RAISE, RAISE, RAISE][i],
            line=WARN if i == 5 else LINE)
        text(s, x + i * Inches(0.18) + Inches(0.15), yy, Inches(4.1), Inches(0.52),
             [[(m + "  ", {"font": MONO, "size": 13, "bold": True}), (d, {"size": 13, "color": INK2})]], anchor=MSO_ANCHOR.MIDDLE)


def diagram_hooks(s, x, y):
    text(s, x, y, Inches(5), Inches(0.4), "Hook-Lebenslauf: nur exit 2 blockt", size=15, bold=True, color=INK2)
    node(s, x, y + Inches(0.6), Inches(2.3), Inches(0.8), "PreToolUse", "Ereignis + matcher")
    arrow(s, x + Inches(2.35), y + Inches(1.0), x + Inches(2.85), y + Inches(1.0))
    node(s, x + Inches(2.9), y + Inches(0.6), Inches(2.3), Inches(0.8), "Skript", "liest tool_input")
    outs = [("exit 2", "blockt, Grund an Claude", WARN), ("exit 0", "Aktion läuft", DONE),
            ("1, 127, Timeout", "läuft trotzdem: fail-open", WORK)]
    for i, (a, b, col) in enumerate(outs):
        bx = x + i * Inches(1.77)
        arrow(s, x + Inches(4.05), y + Inches(1.45), bx + Inches(0.8), y + Inches(2.15))
        box(s, bx, y + Inches(2.2), Inches(1.65), Inches(1.05), fill=SURFACE, line=col)
        text(s, bx + Inches(0.12), y + Inches(2.2), Inches(1.45), Inches(1.05), [[(a, {"bold": True, "size": 13, "color": col})],
             [(b, {"size": 11, "color": INK2})]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x, y + Inches(3.55), Inches(5.3), Inches(0.8), "Ein kaputter Schutz-Hook ist ein offener Schutz-Hook.",
         size=16, color=INK, bold=True)


def diagram_patterns(s, x, y):
    text(s, x, y, Inches(5), Inches(0.4), "Drei Orchestrierungsmuster", size=15, bold=True, color=INK2)
    labels = [("Fan-out", "parallel, dann zusammenführen"), ("Pipeline", "Stufe für Stufe"), ("Hierarchie", "Leitstelle verteilt")]
    for i, (a, b) in enumerate(labels):
        yy = y + Inches(0.6) + i * Inches(1.45)
        text(s, x, yy, Inches(1.6), Inches(0.6), [[(a, {"bold": True, "size": 14})], [(b, {"size": 11, "color": INK2})]])
        if i == 0:
            node(s, x + Inches(1.8), yy + Inches(0.25), Inches(0.7), Inches(0.5), "A", size=12)
            for k in range(3):
                arrow(s, x + Inches(2.55), yy + Inches(0.5), x + Inches(3.1), yy + Inches(0.1) + k * Inches(0.4))
                box(s, x + Inches(3.15), yy - Inches(0.05) + k * Inches(0.4), Inches(0.9), Inches(0.32), fill=RAISE)
        elif i == 1:
            for k in range(4):
                box(s, x + Inches(1.8) + k * Inches(0.95), yy + Inches(0.25), Inches(0.7), Inches(0.5), fill=RAISE)
                if k < 3:
                    arrow(s, x + Inches(2.52) + k * Inches(0.95), yy + Inches(0.5), x + Inches(2.73) + k * Inches(0.95), yy + Inches(0.5))
        else:
            node(s, x + Inches(2.8), yy - Inches(0.05), Inches(1.0), Inches(0.42), "Leitung", size=11)
            for k in range(3):
                arrow(s, x + Inches(3.3), yy + Inches(0.4), x + Inches(2.0) + k * Inches(1.2), yy + Inches(0.75))
                box(s, x + Inches(1.6) + k * Inches(1.2), yy + Inches(0.78), Inches(0.8), Inches(0.3), fill=RAISE)


def diagram_ci(s, x, y):
    text(s, x, y, Inches(5), Inches(0.4), "Claude als Pipeline-Stufe", size=15, bold=True, color=INK2)
    node(s, x, y + Inches(0.6), Inches(1.4), Inches(0.9), "Diff / Aufgabe", "stdin")
    arrow(s, x + Inches(1.45), y + Inches(1.05), x + Inches(1.8), y + Inches(1.05))
    node(s, x + Inches(1.85), y + Inches(0.6), Inches(1.7), Inches(0.9), "claude -p", "--output-format json", fill=RAISE, line=ACCENT)
    arrow(s, x + Inches(3.6), y + Inches(1.05), x + Inches(3.95), y + Inches(1.05))
    node(s, x + Inches(4.0), y + Inches(0.6), Inches(1.3), Inches(0.9), "Urteil", "JSON")
    rules = ["--max-budget-usd und --max-turns begrenzen Kosten und Runden (nur -p)",
             "Fremder Code: --bare mit API-Key, sonst laufen die Hooks des Repos",
             "Zugang: API-Key, Abo-Token nur ohne --bare, oder OIDC-Federation"]
    for i, r in enumerate(rules):
        yy = y + Inches(1.9) + i * Inches(0.75)
        box(s, x, yy + Inches(0.1), Inches(0.22), Inches(0.22), fill=ACCENT, shape=MSO_SHAPE.OVAL)
        text(s, x + Inches(0.4), yy, Inches(4.9), Inches(0.7), r, size=13, color=INK2)


def slide_verify(prs):
    s = blank(prs, "Die wichtigste Gewohnheit im Umgang mit Agenten: Ergebnisse selbst prüfen. Tests selbst laufen lassen, "
                   "Diffs lesen, bei wichtigen Änderungen einen unabhängigen Gegenprüfer einsetzen.")
    title(s, "Haltung", "Ein grüner Bericht ist kein Beweis.", "Ausgeführter Code ist einer.")
    flow(s, [("Agent meldet", "„alle Tests grün"), ("Du führst aus", "Tests, Diff, Ausgabe"), ("Gegenprüfer", "unabhängig, adversarial"),
             ("Erst dann", "übernehmen")], Inches(0.7), Inches(3.0), Inches(2.6), Inches(1.3), Inches(0.5))
    text(s, Inches(0.7), Inches(5.0), Inches(11.8), Inches(1.2), "In der Bibliothek: Devil's Advocate (S3.6), eingebaute Reviews "
         "(S3.7), Fehlersuche Schicht für Schicht (S4.9, S4.10).", size=17, color=INK2)


def slide_tutor(prs):
    s = blank(prs, "Lernen mit Claude Code über Claude Code: Der Tutor stuft ein, führt Kapitel für Kapitel und fragt mit "
                   "Abstand ab. Angelehnt an Matt Pococks Skill teach.")
    title(s, "Tutor", "Mit Claude Code lernen: /workshop", "Der Lernordner ist das Gedächtnis: Mission, Pfad, Fortschritt, Lernprotokolle.")
    cmds = [("/workshop start", "Einstufung, Mission, persönlicher Pfad"), ("/workshop next", "das nächste Kapitel deines Pfads"),
            ("/workshop learn S2.8", "ein bestimmtes Kapitel"), ("/workshop review", "Abruf mit Abstand"),
            ("/workshop guide S3", "Co-Pilot für Moderierende")]
    for i, (c, d) in enumerate(cmds):
        y = Inches(2.6) + i * Inches(0.78)
        box(s, Inches(0.7), y, Inches(4.2), Inches(0.62), fill=SURFACE, line=LINE)
        text(s, Inches(0.9), y, Inches(3.9), Inches(0.62), c, size=16, font=MONO, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
        text(s, Inches(5.2), y, Inches(7.2), Inches(0.62), d, size=17, color=INK2, anchor=MSO_ANCHOR.MIDDLE)


def slide_end(prs):
    s = blank(prs, "Zum Abschluss die drei Einstiege noch einmal. Fragen gehen an den Mentor-Agenten oder an die offizielle Doku.")
    text(s, Inches(0.8), Inches(2.0), Inches(11), Inches(1.2), "Los geht's.", size=54, bold=True)
    text(s, Inches(0.8), Inches(3.3), Inches(11), Inches(2.0),
         [[("Einstufung: ", {"bold": True}), ("Lern-Cockpit oder /workshop start", {})],
          [("Fertige Pfade: ", {"bold": True}), ("resources/paths/", {"font": MONO})],
          [("Alle Kapitel: ", {"bold": True}), ("resources/library/README.md", {"font": MONO})]], size=22, color=INK2, spacing=10)
    text(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.5), "Stand von Modellen und CLI: resources/_canonical.md",
         size=14, color=MUTED)


def build(catalog_path=CATALOG, out=OUT):
    cat = load_catalog(catalog_path)
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    slide_title(prs, cat)
    slide_agent(prs)
    slide_ways(prs)
    slide_placement(prs, cat)
    slide_map(prs, cat)
    slide_floor(prs, cat)
    slide_session(prs, cat, 1, "Erste Schritte mit dem Agenten", "Bauen, verstehen, steuern: Werkstatt, Rechte, Kontext, "
                  "Aufträge, Git, Kosten.", diagram_modes,
                  "Session 1 beginnt mit einem Bau-Erfolg in den ersten Minuten, danach die Rechte-Modi als Zutrittsebenen.")
    slide_session(prs, cat, 2, "Das Ökosystem", "Skills, Hooks, Plugins, MCP und Wissensquellen — erweitern und kontrollieren.",
                  diagram_hooks, "Session 2: Erweitern mit Kontrolle. Merksatz für Hooks: nur exit 2 blockt.")
    slide_session(prs, cat, 3, "Fortgeschritten: Kern", "Spezialisierte Agenten, adversariale Prüfung, sichere Automation.",
                  diagram_patterns, "Session 3: Agenten spezialisieren, gegenprüfen lassen, autonome Läufe begrenzen.")
    slide_session(prs, cat, 4, "Fortgeschritten: Kür", "Modell pro Phase, Headless und CI, Isolation, Abschlussprojekt, "
                  "Fehlersuche.", diagram_ci, "Session 4: Claude als Pipeline-Stufe, das Abschlussprojekt und die Fehlersuche, "
                  "die alle brauchen.")
    slide_verify(prs)
    slide_tutor(prs)
    slide_end(prs)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out, len(prs.slides)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)
    out, n = build(args.catalog, args.out)
    print(f"{n} Folien → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
