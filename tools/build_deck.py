# -*- coding: utf-8 -*-
"""Generiert das 4-Session-Opener-Deck (WP-04) aus der Welle-F-Struktur.

Eigenes Deck (SOC Command / Amber-auf-Dunkel, passend zur claude-code-workshop-ui.html),
NICHT das alte pre-Welle-F claude-code-workshop.pptx ueberschreibend.
Aufruf (Repo-Root):  python tools/build_deck.py
"""
import os
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "claude-code-workshop-4session.pptx")

# --- Palette (SOC / Amber) ---
BG      = RGBColor(0x0C, 0x0F, 0x0A)
PANEL   = RGBColor(0x14, 0x1B, 0x12)
AMBER   = RGBColor(0xF5, 0x9E, 0x0B)
GREEN   = RGBColor(0x22, 0xC5, 0x5E)
INK     = RGBColor(0xE8, 0xF0, 0xD8)
MUTED   = RGBColor(0x9A, 0xAB, 0x8C)
LINE    = RGBColor(0x2A, 0x3A, 0x2A)
S1C     = RGBColor(0x81, 0x8C, 0xF8)  # indigo
S2C     = RGBColor(0xA7, 0x8B, 0xFA)  # violet
S3C     = RGBColor(0xFB, 0x71, 0x85)  # rose
S4C     = AMBER

FONT   = "Segoe UI"
FONT_SB = "Segoe UI Semibold"
MONO   = "Consolas"

EMU_W = Inches(13.333)
EMU_H = Inches(7.5)

prs = Presentation()
prs.slide_width = EMU_W
prs.slide_height = EMU_H
BLANK = prs.slide_layouts[6]


def _no_line(shape):
    shape.line.fill.background()


def bg(slide, color=BG):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, EMU_W, EMU_H)
    r.fill.solid(); r.fill.fore_color.rgb = color
    _no_line(r)
    r.shadow.inherit = False
    # bg() wird pro Slide ZUERST aufgerufen -> ist ohnehin die unterste Ebene (kein z-order-Hack noetig)
    return r


def rect(slide, x, y, w, h, color, line=None):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    r.fill.solid(); r.fill.fore_color.rgb = color
    if line is None:
        _no_line(r)
    else:
        r.line.color.rgb = line; r.line.width = Pt(1)
    r.shadow.inherit = False
    return r


def text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=6, line_spacing=1.05):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    # runs = list of paragraphs; each = list of (txt, size, color, font, bold)
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        p.line_spacing = line_spacing
        for (txt, size, color, font, bold) in para:
            r = p.add_run(); r.text = txt
            r.font.size = Pt(size); r.font.name = font; r.font.bold = bold
            r.font.color.rgb = color
    return tb


def eyebrow(slide, label, color=AMBER):
    text(slide, Inches(0.7), Inches(0.45), Inches(11), Inches(0.35),
         [[(label, 12, color, MONO, True)]])


def accentbar(slide, x, y, w, color=AMBER, h=Pt(3.5)):
    rect(slide, x, y, w, h, color)


def footer(slide, note="session-plan.md = Single Source of Truth"):
    text(slide, Inches(0.7), Inches(6.95), Inches(12), Inches(0.35),
         [[("CLAUDE CODE WORKSHOP  ·  4 Sessions / 65 Lerneinheiten  ·  " + note, 9.5, MUTED, MONO, False)]])
    accentbar(slide, 0, Inches(6.82), EMU_W, LINE, h=Pt(1))


# ---------- Slide 1: Title ----------
s = prs.slides.add_slide(BLANK); bg(s)
rect(s, 0, 0, Pt(10), EMU_H, AMBER)  # left spine
text(s, Inches(0.9), Inches(0.7), Inches(8), Inches(0.4),
     [[("● SYSTEM ONLINE   ·   SECTOR: ONBOARDING", 13, GREEN, MONO, True)]])
text(s, Inches(0.9), Inches(2.3), Inches(11.4), Inches(2.2),
     [[("Claude Code", 60, INK, FONT_SB, True)],
      [("Workshop", 60, AMBER, FONT_SB, True)]], line_spacing=0.98)
accentbar(s, Inches(0.95), Inches(4.55), Inches(3.2))
text(s, Inches(0.9), Inches(4.8), Inches(11.4), Inches(1.2),
     [[("Vom Agenten-Grundlagen bis zu autonomen Multi-Agent-Systemen — ", 18, INK, FONT, False),
       ("4 Sessions · 65 Lerneinheiten.", 18, AMBER, FONT, True)],
      [("Für erfahrene Entwickler aus Physical Security (Zutrittskontrolle, Alarmsysteme).", 15, MUTED, FONT, False)]])
footer(s)

# ---------- Slide 2: Mission ----------
s = prs.slides.add_slide(BLANK); bg(s)
eyebrow(s, "MISSION")
text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(1.0),
     [[("Nach dem Workshop setzt du Claude Code eigenständig und produktiv ein.", 30, INK, FONT_SB, True)]])
accentbar(s, Inches(0.72), Inches(1.95), Inches(2.6))
box = [
    ("Kein Chat-Fenster — ein Agent.", "Direkter Zugriff auf Filesystem, Shell und Git; du steuerst über das Permission-System (Clearance-Level)."),
    ("Demos > Slides.", "Jede Lerneinheit: Konzept sehen → Live-Demo → selbst ausprobieren → mit Cheatsheet absichern."),
    ("Security-Analogien als Werkzeug.", "Zutrittskontrolle, Alarm-Sensoren, SOC-Team — vertraute Bilder für neue Konzepte."),
]
y = Inches(2.4)
for head, body in box:
    rect(s, Inches(0.72), y, Inches(0.12), Inches(1.0), AMBER)
    text(s, Inches(1.05), y, Inches(11.4), Inches(1.0),
         [[(head + "  ", 17, INK, FONT_SB, True), (body, 15, MUTED, FONT, False)]])
    y += Inches(1.2)
footer(s)

# ---------- Slide 3: Die 4 Sessions ----------
s = prs.slides.add_slide(BLANK); bg(s)
eyebrow(s, "LANDKARTE")
text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(0.7),
     [[("Die vier Sessions", 30, INK, FONT_SB, True)]])
accentbar(s, Inches(0.72), Inches(1.62), Inches(2.6))
sessions = [
    ("SESSION 1", "Erste Schritte mit dem Agenten", "Foundations · S1.1–S1.20", "CLI · Kontext · Prompting · Git · Permissions (6 Modi) · Kosten", S1C),
    ("SESSION 2", "Das Ecosystem", "Ecosystem · S2.1–S2.20", "Skills · Hooks · Plugins · MCP · RAG / NotebookLM", S2C),
    ("SESSION 3", "Advanced Kern", "Advanced-Kern · S3.1–S3.15", "Agents & Orchestrierung · adversariale Security · Hardening · Automation", S3C),
    ("SESSION 4", "Advanced Bonus", "Advanced-Bonus · S4.1–S4.10", "Multi-Model · CI/CD & Headless · Capstone-Architektur · Troubleshooting", S4C),
]
y = Inches(2.0)
for tag, title, meta, topics, col in sessions:
    rect(s, Inches(0.72), y, Inches(11.9), Inches(1.05), PANEL)
    rect(s, Inches(0.72), y, Inches(0.14), Inches(1.05), col)
    text(s, Inches(1.05), y + Inches(0.12), Inches(2.5), Inches(0.8),
         [[(tag, 13, col, MONO, True)], [(meta, 10, MUTED, MONO, False)]])
    text(s, Inches(3.5), y + Inches(0.12), Inches(9.0), Inches(0.8),
         [[(title, 18, INK, FONT_SB, True)], [(topics, 13, MUTED, FONT, False)]])
    y += Inches(1.18)
footer(s)

# ---------- Slide 4: Drei-Schicht-Modell ----------
s = prs.slides.add_slide(BLANK); bg(s)
eyebrow(s, "DIDAKTIK · TIERING")
text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(0.7),
     [[("Drei Schichten pro Lerneinheit", 30, INK, FONT_SB, True)]])
accentbar(s, Inches(0.72), Inches(1.62), Inches(2.6))
tiers = [
    ("core", "Pflichtpfad", "Was jeder können muss. Wird immer gefahren.", GREEN),
    ("deep-dive", "„Wenn Zeit, dann zeigen\"", "Optionale Vertiefung desselben Themas.", RGBColor(0x60, 0xA5, 0xFA)),
    ("bonus", "Kür / Showcase", "Nur bei Überschuss oder auf Nachfrage (Custom-Komponenten).", RGBColor(0xA7, 0x8B, 0xFA)),
]
x = Inches(0.72)
for tag, head, body, col in tiers:
    rect(s, x, Inches(2.1), Inches(3.85), Inches(2.6), PANEL)
    rect(s, x, Inches(2.1), Inches(3.85), Pt(4), col)
    text(s, x + Inches(0.28), Inches(2.4), Inches(3.3), Inches(0.6),
         [[("[" + tag + "]", 20, col, MONO, True)]])
    text(s, x + Inches(0.28), Inches(3.05), Inches(3.3), Inches(1.6),
         [[(head, 16, INK, FONT_SB, True)], [(body, 13, MUTED, FONT, False)]])
    x += Inches(4.02)
text(s, Inches(0.72), Inches(5.05), Inches(11.9), Inches(1.4),
     [[("⏱  Termin-Länge ist kein harter Constraint.  ", 15, AMBER, FONT, True),
       ("Content-Vollständigkeit vor Slot-Fitting; Sessions laufen so lang wie nötig — mit Pausen + kurzen Recall-Fragen gegen Ermüdung.", 15, MUTED, FONT, False)]])
footer(s)

# ---------- Slide 5: Didaktischer Rhythmus ----------
s = prs.slides.add_slide(BLANK); bg(s)
eyebrow(s, "DIDAKTIK · RHYTHMUS")
text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(0.7),
     [[("Jede Lerneinheit im selben Takt", 30, INK, FONT_SB, True)]])
accentbar(s, Inches(0.72), Inches(1.62), Inches(2.6))
steps = [
    ("1", "Konzept verstehen", "LE-Abschnitt im Modul lesen"),
    ("2", "Live-Demo sehen", "Demo > Slides — nachvollziehen"),
    ("3", "Selbst ausprobieren", "Exercise im Hands-on-Puffer"),
    ("4", "Absichern", "Cheatsheet / Quick-Reference"),
]
x = Inches(0.72)
for num, head, body in steps:
    rect(s, x, Inches(2.3), Inches(2.9), Inches(2.3), PANEL)
    text(s, x + Inches(0.25), Inches(2.5), Inches(2.4), Inches(0.9),
         [[(num, 34, AMBER, FONT_SB, True)]])
    text(s, x + Inches(0.25), Inches(3.35), Inches(2.5), Inches(1.1),
         [[(head, 16, INK, FONT_SB, True)], [(body, 12.5, MUTED, FONT, False)]])
    if num != "4":
        text(s, x + Inches(2.78), Inches(3.05), Inches(0.4), Inches(0.6),
             [[("→", 22, AMBER, FONT, True)]])
    x += Inches(3.02)
text(s, Inches(0.72), Inches(5.0), Inches(11.9), Inches(1.2),
     [[("Start jeder Session: visuell mit diesem Deck. ", 15, AMBER, FONT, True),
       ("Interaktives Lern-Cockpit (claude-code-workshop-ui.html) + Mentor-Agent begleiten das Selbststudium.", 15, MUTED, FONT, False)]])
footer(s)


# ---------- Slides 6-9: je Session ----------
def session_slide(tag, title, mission, col, clusters, analogy):
    s = prs.slides.add_slide(BLANK); bg(s)
    eyebrow(s, tag, col)
    text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(0.7),
         [[(title, 30, INK, FONT_SB, True)]])
    accentbar(s, Inches(0.72), Inches(1.62), Inches(2.6), col)
    text(s, Inches(0.72), Inches(1.8), Inches(11.9), Inches(0.6),
         [[("Mission: ", 15, col, FONT_SB, True), (mission, 15, MUTED, FONT, False)]])
    # cluster bullets in two columns
    half = (len(clusters) + 1) // 2
    cols = [clusters[:half], clusters[half:]]
    xs = [Inches(0.72), Inches(6.85)]
    for ci, colitems in enumerate(cols):
        y = Inches(2.7)
        for item in colitems:
            rect(s, xs[ci], y + Inches(0.07), Inches(0.1), Inches(0.5), col)
            text(s, xs[ci] + Inches(0.28), y, Inches(5.6), Inches(0.7),
                 [[(item, 15, INK, FONT, False)]])
            y += Inches(0.62)
    # analogy strip
    rect(s, Inches(0.72), Inches(6.1), Inches(11.9), Inches(0.55), PANEL)
    rect(s, Inches(0.72), Inches(6.1), Inches(0.12), Inches(0.55), col)
    text(s, Inches(1.05), Inches(6.16), Inches(11.4), Inches(0.5),
         [[("Security-Analogie:  ", 13, col, FONT_SB, True), (analogy, 13, MUTED, FONT, False)]],
         anchor=MSO_ANCHOR.MIDDLE)
    footer(s)


session_slide(
    "SESSION 1  ·  FOUNDATIONS", "Erste Schritte mit dem Agenten",
    "Was ist Claude Code, wie steuere ich es, wie arbeite ich sicher mit Git — und behalte Kosten im Blick.",
    S1C,
    ["Coding Agent vs. Chat — mentales Modell", "First Contact: sofort eine Datei bauen",
     "Oberflächen: CLI · Desktop · IDE · Web · iOS", "Permission Modes komplett (6 Modi + Cloud)",
     "Modellwahl & Effort (Tiers: Opus / Sonnet / Haiku / Fable)", "Kontextfenster · /compact · /rewind",
     "CLAUDE.md: Projekt-Standing-Orders", "Vager vs. präziser Prompt · Plan Mode",
     "Git in einem Flow: branch → commit → PR", "Kosten im Blick: /cost · /usage · Budget-Cap"],
    "Permission Modes = Clearance-Level. default = Besucherausweis (nur lesen) … bypass = Generalschlüssel (nur versiegelte Umgebungen).")

session_slide(
    "SESSION 2  ·  ECOSYSTEM", "Das Ecosystem",
    "Wie man Claude Code erweitert und kontrolliert.", S2C,
    ["Skills = SOPs, Commands = Buttons", "Eine SKILL.md schreiben (Frontmatter)",
     "Bundled Skills (/run · /verify · /loop …)", "Hooks = Event-Listener (die 3 Eckpfeiler)",
     "Hook-Events landkarten & konfigurieren", "Plugins: ein Bundle schnüren + Scopes",
     "Plugin-Supply-Chain-Risiken", "MCP: der Integrations-Stecker (Transports)",
     "MCP-Security & eigenen Server bauen", "RAG & NotebookLM: dem Agenten Blueprints geben"],
    "Hooks = Alarm-Sensoren (feuern auf Events). Plugin = zertifiziertes Sicherheitsmodul. MCP = Integrations-Stecker zu Fremdsystemen.")

session_slide(
    "SESSION 3  ·  ADVANCED KERN", "Advanced Kern",
    "Spezialisierte Agenten, automatisierte Security-Prüfung, sichere Automation.", S3C,
    ["Was ist ein Agent? (Spezialisierung)", "Built-in Subagents (Explore/Plan/general)",
     "Custom Subagent definieren", "Orchestrierung: Fan-Out · Pipeline · Hierarchie",
     "Devil's Advocate: adversariale Security-Pipeline", "Built-in Review-Trio (/security-review …)",
     "Permissions für Autonomie · Protected Paths", "Sandboxing-Stufen · Datenschutz & Compliance",
     "Scheduling: /loop · /goal · /schedule", "Autonome Loops absichern (Budget + Worktree)"],
    "Agenten = spezialisiertes SOC-Team; die adversariale Pipeline = internes Red-Team, das die eigene Analyse angreift.")

session_slide(
    "SESSION 4  ·  ADVANCED BONUS", "Advanced Bonus",
    "Multi-Model, CI/CD, die volle Architektur — und souverän debuggen.", S4C,
    ["Multi-Model: richtiges Modell pro Phase", "Codex Swarm & Daten-Fluss-Grenze",
     "Headless Mode: claude -p als Pipeline-Stufe", "CI-Auth, Cost-Caps & Cost-Engineering",
     "CI-Pipelines bauen (GitHub Actions / GitLab)", "Mobile/Remote · Inception & Worktree-Isolation",
     "Die volle Architektur (Capstone-Diskussion)", "Troubleshooting: /debug · --verbose · /doctor",
     "Diagnose-Sequenzen (Hook/Skill/Plugin/MCP)"],
    "Multi-Model = Dienstplan-Staffing (richtige Rolle pro Aufgabe). Troubleshooting = Alarmpanel-Fehlerisolation, Schicht für Schicht.")

# ---------- Slide 10: So arbeitest du ----------
s = prs.slides.add_slide(BLANK); bg(s)
eyebrow(s, "MATERIALIEN")
text(s, Inches(0.7), Inches(0.9), Inches(11.9), Inches(0.7),
     [[("So arbeitest du durch den Workshop", 30, INK, FONT_SB, True)]])
accentbar(s, Inches(0.72), Inches(1.62), Inches(2.6))
mats = [
    ("Interaktives Lern-Cockpit", "claude-code-workshop-ui.html — 65 LEs, Slides, Übungen, Quiz, Fortschritt."),
    ("Cheatsheet & Quick-Reference", "50+ Commands, Permission-Modi, Hook-Typen, MCP — die Referenzkarte."),
    ("Workshop-Playground", "Demo-Repo mit gepflanzten Vulnerabilities (Zutrittskontrolle, OSDP/Wiegand)."),
    ("Mentor-Agent", "Beantwortet Konzeptfragen und verweist auf die richtige Lerneinheit."),
    ("Prerequisites", "prerequisites.md — Setup, bevor Session 1 startet."),
    ("session-plan.md", "Single Source of Truth: Ablauf, Level-Tiering, Zeiten als Pacing-Signal."),
]
y = Inches(2.1); x = Inches(0.72)
for i, (head, body) in enumerate(mats):
    col = x if i % 2 == 0 else Inches(6.85)
    if i % 2 == 0 and i > 0:
        y += Inches(1.42)
    yy = y
    rect(s, col, yy, Inches(5.75), Inches(1.25), PANEL)
    rect(s, col, yy, Inches(0.12), Inches(1.25), AMBER)
    text(s, col + Inches(0.3), yy + Inches(0.15), Inches(5.3), Inches(1.0),
         [[(head, 15, INK, FONT_SB, True)], [(body, 12, MUTED, FONT, False)]])
footer(s)

# ---------- Slide 11: Closing ----------
s = prs.slides.add_slide(BLANK); bg(s)
rect(s, 0, 0, Pt(10), EMU_H, AMBER)
text(s, Inches(0.9), Inches(0.7), Inches(8), Inches(0.4),
     [[("● SECTOR T-1-1 · CLEARANCE GRANTED", 13, GREEN, MONO, True)]])
text(s, Inches(0.9), Inches(2.6), Inches(11.4), Inches(1.6),
     [[("Los geht's.", 54, INK, FONT_SB, True)]])
accentbar(s, Inches(0.95), Inches(3.9), Inches(3.2))
text(s, Inches(0.9), Inches(4.2), Inches(11.4), Inches(1.4),
     [[("Session 1 öffnet mit einem Bau-Erfolg in den ersten Minuten — ", 18, INK, FONT, False),
       ("erst bauen, dann über Clearance-Level nachdenken.", 18, AMBER, FONT, True)],
      [("Fragen jederzeit an den Mentor. Der Rest ist Hands-on.", 15, MUTED, FONT, False)]])
footer(s)

prs.save(OUT)

# --- Verify ---
chk = Presentation(OUT)
print("Deck gespeichert:", os.path.relpath(OUT, ROOT))
print("Slides:", len(chk.slides))
titles = []
for i, sl in enumerate(chk.slides, 1):
    txts = []
    for sh in sl.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            txts.append(sh.text_frame.text.strip().split("\n")[0][:48])
    titles.append("  S{:>2}: {}".format(i, " | ".join(txts[:3])))
print("\n".join(titles))
