# -*- coding: utf-8 -*-
"""Generated files of the practice library (spec section 7). Pure functions: build_outputs(lib) -> {path: text}.

Outputs, relative to the parent of the library folder (resources/ in the repo):
  library/catalog.json · library/README.md · library/einstufung.md · paths/*.md · reference/analogien.md
  and the meta block of every chapter.
"""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import build_cockpit  # noqa: E402
import catalog_core  # noqa: E402
import placement as engine  # noqa: E402

GENERATED = "<!-- GENERIERT von tools/build_library.py — nicht von Hand ändern, Quelle: Kapitel und _*.yaml -->"
LEVEL_LABEL = {"core": "Kern", "deep-dive": "Vertiefung", "bonus": "Kür"}
STATUS_LABEL = {"work": "durcharbeiten", "skim": "überfliegen", "skip": "Schnellcheck reicht", "later": "später"}
SESSION_LABEL = {0: "Vorbereitung", 1: "Session 1 — Erste Schritte", 2: "Session 2 — Das Ökosystem",
                 3: "Session 3 — Fortgeschritten: Kern", 4: "Session 4 — Fortgeschritten: Kür"}
ZONES = ["Grundlagen", "Erweitern", "Fortgeschritten", "Betrieb & Abschluss", "Begleitend"]
SHIELD = "🛡"
META_START, META_END = "<!-- meta:start -->", "<!-- meta:end -->"


# --- catalog -----------------------------------------------------------------------------------------

def core_entries(lib):
    entries = []
    for ch in lib.chapters:
        entry = {k: ch.front.get(k) for k in catalog_core.CORE_FIELDS}
        entry["requires"] = list(ch.requires)
        entry["offers"] = list(ch.offers)
        entries.append(entry)
    return entries


def catalog(lib):
    cat = catalog_core.core_catalog(core_entries(lib), lib.shelves, lib.placement)
    by_id = lib.by_id
    for entry in cat["chapters"]:
        ch = by_id[entry["id"]]
        entry.update({
            "title": ch.title, "file": ch.path.name, "outcome": ch.outcome, "aliases": list(ch.aliases),
            "sources": list(ch.sources), "skip_check": list(ch.skip_check), "glance": ch.glance,
            "analogy": ch.analogy, "example": ch.example, "example_lang": ch.example_lang,
            "checkpoint": ch.checkpoint, "transferable": ch.transferable,
            "quiz": _quiz_entry(ch.quiz),
            # moderation layer: demo and moderator notes, relative to the library folder (or None)
            "demo": _demo_link(ch),
            # recall questions of the Check section and their answers (None: the chapter has no answer block yet)
            "recall": list(ch.recall),
            "answers": list(ch.answers) if ch.answers is not None else None,
        })
    cat["shelves"] = [{k: s.get(k, "") for k in ("id", "title", "zone", "purpose", "intro")} for s in lib.shelves]
    return cat


def dump_json(data):
    return json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# --- helpers ---------------------------------------------------------------------------------------------

def _link(ch, prefix=""):
    return f"[{ch.id} {ch.title}]({prefix}{ch.path.name})"


def _quiz_entry(quiz):
    """Quiz of a chapter; 'why' only when every answer has its reason, in the order of the answers."""
    if not quiz:
        return None
    entry = {"q": quiz.question, "correct": quiz.correct, "wrong": list(quiz.wrong)}
    if quiz.why_correct and len(quiz.why_wrong) == len(quiz.wrong) and all(quiz.why_wrong):
        entry["why"] = {"correct": quiz.why_correct, "wrong": list(quiz.why_wrong)}
    return entry


def _demo_link(ch):
    """Demo file of a chapter, relative to the library folder (the paths folder is a sibling, so it fits there too)."""
    if not ch.demo:
        return None
    return "/".join(["..", ch.demo.parent.parent.name, ch.demo.parent.name, ch.demo.name])


def _shelf_titles(lib):
    return {s["id"]: s for s in lib.shelves}


def _minutes_line(chapters):
    sums = {k: sum(c.minutes for c in chapters if c.level == k) for k in LEVEL_LABEL}
    return " · ".join(f"{LEVEL_LABEL[k]} {v} Min" for k, v in sums.items() if v)


# --- meta blocks -----------------------------------------------------------------------------------------

def meta_block(lib, ch):
    shelves = _shelf_titles(lib)
    shelf = shelves.get(ch.shelf, {"title": ch.shelf})
    by_id = lib.by_id
    reqs = " · ".join(_link(by_id[r]) for r in ch.requires if r in by_id) or "keine"
    parts = [f"**Regal:** [{shelf['title']}](README.md#{ch.shelf})", f"**Stufe:** {LEVEL_LABEL.get(ch.level, ch.level)}",
             f"**~{ch.minutes} Min**", f"**Voraussetzungen:** {reqs}"]
    if ch.safety_floor:
        parts.append(f"{SHIELD} **Sicherheitsboden**")
    idx = lib.chapters.index(ch)
    nav = []
    if idx > 0:
        nav.append("← " + _link(lib.chapters[idx - 1]))
    nav.append("[Bibliothek](README.md)")
    if idx + 1 < len(lib.chapters):
        nav.append(_link(lib.chapters[idx + 1]) + " →")
    return "\n".join([META_START, "> " + " · ".join(parts), ">", "> " + " · ".join(nav), META_END])


def with_meta(text, block):
    """Replace or insert the meta block directly after the H1 line. Line endings normalised to LF."""
    text = text.replace("\r\n", "\n")
    pattern = re.compile(re.escape(META_START) + r".*?" + re.escape(META_END), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text, count=1)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[:i + 1] + ["", block] + lines[i + 1:])
    return text


# --- library README ------------------------------------------------------------------------------------

def library_readme(lib):
    shelves = lib.shelves
    by_shelf = {s["id"]: [c for c in lib.chapters if c.shelf == s["id"]] for s in shelves}
    total = sum(c.minutes for c in lib.chapters)
    out = ["# Die Praxisbibliothek", "", GENERATED, "",
           f"{len(lib.chapters)} Kapitel in {len(shelves)} Regalen, zusammen {engine.hours_text(total)}. "
           "Du musst nicht alles lesen: Die Einstufung empfiehlt dir die Kapitel, die zu deinem Stand und Ziel passen.",
           "", "## So findest du deinen Weg", "",
           "1. **Einstufung** — im [Lern-Cockpit](../claude-code-workshop-ui.html), mit `/workshop start` in Claude Code "
           "oder zum Selbermachen in [einstufung.md](einstufung.md).",
           "2. **Fertige Pfade** — je Ziel, als Schnellstart oder als Live-Workshop: [Pfade](../paths/README.md).",
           "3. **Stöbern** — die Regale unten. Jedes Kapitel beginnt mit einem Schnellcheck: Kannst du beide Fragen sicher "
           "mit Ja beantworten, geh weiter.", "",
           f"{SHIELD} = Sicherheitsboden: Diese Kapitel empfehlen wir auch Fortgeschrittenen zum Überfliegen. "
           "Stufen: Kern (für alle), Vertiefung (wenn das Thema dein Schwerpunkt ist), Kür (Ausblick).", "",
           "## Regal-Karte", "", "```mermaid", "flowchart LR"]
    for z, zone in enumerate(ZONES):
        members = [s for s in shelves if s.get("zone") == zone]
        if not members:
            continue
        out.append(f'  subgraph Z{z}["{zone}"]')
        out.append("    direction TB")
        for s in members:
            n = len(by_shelf[s["id"]])
            out.append(f'    {s["id"].replace("-", "_")}["{s["title"]}<br/>{n} Kapitel"]')
        out.append("  end")
    zones_present = [z for z, zone in enumerate(ZONES[:4]) if any(s.get("zone") == zone for s in shelves)]
    for a, b in zip(zones_present, zones_present[1:]):
        out.append(f"  Z{a} --> Z{b}")
    out += ["```", ""]
    for s in shelves:
        chapters = by_shelf[s["id"]]
        out += [f'<a id="{s["id"]}"></a>', "", f"## {s['title']}", "", f"**{s.get('purpose', '')}**", "",
                s.get("intro", "").strip(), ""]
        if chapters:
            out += ["| Kapitel | Stufe | Min | |", "|---|---|---:|---|"]
            for c in chapters:
                out.append(f"| {_link(c)} | {LEVEL_LABEL.get(c.level, c.level)} | {c.minutes} | "
                           f"{SHIELD if c.safety_floor else ''} |")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


# --- paths -----------------------------------------------------------------------------------------------

def _path_doc(lib, cat, title, intro, answers):
    result = engine.place(cat, answers)
    by_id = lib.by_id
    rules = lib.placement
    total = result["totals"]["work_min"] + result["totals"]["skim_min"]
    out = [f"# {title}", "", GENERATED, "", intro, "",
           f"**Umfang:** {engine.stages_text(len(result['stages']))}, zusammen {engine.hours_text(total)} "
           f"({result['totals']['work_min']} Min durcharbeiten, {result['totals']['skim_min']} Min überfliegen).", ""]
    for w in result["warnings"]:
        out += [f"> ⚠ {rules['warnings'][w['code']]}", ""]
    for stage in result["stages"]:
        out += [f"## Etappe {stage['n']} (~{stage['minutes']} Min)", ""]
        for row in result["chapters"]:
            if row["stage"] == stage["n"]:
                c = by_id[row["id"]]
                mark = f" {SHIELD}" if c.safety_floor else ""
                out.append(f"- {_link(c, '../library/')}{mark} — {STATUS_LABEL[row['status']]}")
        out.append("")
    return "\n".join(out).rstrip() + "\n", result


def paths(lib, cat):
    rules = lib.placement
    docs, index = {}, []
    text, res = _path_doc(lib, cat, "Schnellstart",
                          "Das Wichtigste in wenigen Stunden: der Mindestpfad für alle, die schnell produktiv werden wollen.",
                          {"time": "schnellstart"})
    docs["schnellstart.md"] = text
    index.append(("schnellstart.md", "Schnellstart", res))
    for goal in rules.get("goals", []):
        if goal["id"] == "moderieren":
            continue
        text, res = _path_doc(lib, cat, f"Pfad: {goal['label']}",
                              "Vorschlag für alle, die hier noch neu sind. Kennst du Teile schon, mach die Einstufung — "
                              "dann wird der Pfad kürzer.",
                              {"goals": [goal["id"]], "time": rules.get("default_time", "abende")})
        docs[f"ziel-{goal['id']}.md"] = text
        index.append((f"ziel-{goal['id']}.md", goal["label"], res))
    live = ["# Live-Workshop: vier Sessions", "", GENERATED, "",
            "Die Reihenfolge des moderierten Workshops. Ablauf, Zeiten, Pausen und Live-Anker stehen im "
            "[Moderations-Handbuch](../moderation/handbuch.md). Die Spalte „Vorführen“ führt zur Demo und zu den "
            "Hinweisen für Moderierende; die Kapitel selbst sind für Selbstlernende geschrieben.", ""]
    for session in sorted({c.session for c in lib.chapters if c.session is not None}):
        chapters = [c for c in lib.chapters if c.session == session]
        live += [f"## {SESSION_LABEL.get(session, f'Session {session}')}", "", _minutes_line(chapters), "",
                 "| Kapitel | Stufe | Min | | Vorführen |", "|---|---|---:|---|---|"]
        for c in chapters:
            demo = f"[Demo]({_demo_link(c)})" if c.demo else ""
            live.append(f"| {_link(c, '../library/')} | {LEVEL_LABEL.get(c.level, c.level)} | {c.minutes} | "
                        f"{SHIELD if c.safety_floor else ''} | {demo} |")
        live.append("")
    extra = [c for c in lib.chapters if c.session is None]
    if extra:
        live += ["## Außerhalb der Sessions", "", "| Kapitel | Stufe | Min |", "|---|---|---:|"]
        live += [f"| {_link(c, '../library/')} | {LEVEL_LABEL.get(c.level, c.level)} | {c.minutes} |" for c in extra]
        live.append("")
    docs["live-workshop.md"] = "\n".join(live).rstrip() + "\n"
    readme = ["# Fertige Lernpfade", "", GENERATED, "",
              "Jeder Pfad ist eine Empfehlung für jemanden, der neu im Thema ist. Mit der "
              "[Einstufung](../library/einstufung.md) wird er persönlich und kürzer.", "",
              "| Pfad | Etappen | Umfang |", "|---|---:|---:|"]
    for file, label, res in index:
        total = res["totals"]["work_min"] + res["totals"]["skim_min"]
        readme.append(f"| [{label}]({file}) | {len(res['stages'])} | {engine.hours_text(total).replace('etwa ', '')} |")
    readme += ["| [Live-Workshop (moderiert)](live-workshop.md) | 4 Sessions | — |", ""]
    docs["README.md"] = "\n".join(readme)
    return docs


# --- self-service placement ----------------------------------------------------------------------------

def einstufung(lib):
    rules = lib.placement
    by_id = lib.by_id
    out = ["# Einstufung zum Selbermachen", "", GENERATED, "",
           "Fünf Minuten, keine Noten. Diese Seite ist die einfache Fassung für alle, die lieber lesen; genauer rechnet "
           "das [Lern-Cockpit](../claude-code-workshop-ui.html) oder `/workshop start` in Claude Code.", "",
           "## 1. Dein Ziel", "", "Wähle ein Ziel und nimm den fertigen Pfad als Ausgangspunkt:", ""]
    for goal in rules.get("goals", []):
        target = "../paths/live-workshop.md" if goal["id"] == "moderieren" else f"../paths/ziel-{goal['id']}.md"
        out.append(f"- **{goal['label']}** → [Pfad]({target})")
    out += ["", "Nur wenig Zeit insgesamt? Nimm den [Schnellstart](../paths/schnellstart.md).", "",
            "## 2. Was du schon kannst", "",
            "Lies je Bereich die Aussage. Trifft sie auf dich zu, kannst du die Kapitel dieses Bereichs mit dem "
            f"Schnellcheck am Kapitelanfang überspringen — außer den {SHIELD}-Kapiteln: die überfliegst du trotzdem.", ""]
    for area in rules.get("areas", []):
        chapters = [by_id[c] for c in area["chapters"] if c in by_id]
        links = ", ".join(_link(c) + (f" {SHIELD}" if c.safety_floor else "") for c in chapters) or "—"
        out += [f"### {area['label']}", "", f"> {area['statement']}", "", f"Kapitel: {links}", ""]
    scenarios = rules.get("scenarios", [])
    if scenarios:
        out += ["## 3. Mini-Szenarien (freiwillig)", "",
                "Kein Test — nur ein Spiegel. Liegst du daneben, lohnt das genannte Kapitel, auch wenn du den Bereich oben "
                "als bekannt markiert hast.", ""]
        for n, sc in enumerate(scenarios, 1):
            options = sorted(sc["options"], key=lambda o: o["text"])  # stable order that does not reveal the answer
            letters = "abcd"
            out += [f"**{n}. {sc['question']}**", ""]
            out += [f"{letters[i]}) {o['text']}" for i, o in enumerate(options)]
            correct = letters[[o["id"] for o in options].index(sc["correct"])]
            chapter = by_id.get(sc.get("chapter"))
            ref = f" Mehr in {_link(chapter)}." if chapter else ""
            out += ["", f"<details><summary>Auflösung</summary>", "", f"Richtig ist {correct}). "
                    f"{sc['explanation'].strip()}{ref}", "", "</details>", ""]
    return "\n".join(out).rstrip() + "\n"


# --- generated reference -------------------------------------------------------------------------------

def analogies(lib):
    out = ["# Analogien: Bild im Kopf", "", GENERATED, "",
           "Jedes Kapitel erklärt sein Thema zuerst mit einem Bild aus der Welt der Sicherheitstechnik. Diese Übersicht "
           "sammelt sie; die Quelle ist jeweils der Abschnitt „Bild im Kopf\" des Kapitels.", "",
           "| Kapitel | Bild im Kopf |", "|---|---|"]
    for c in lib.chapters:
        if c.analogy:
            cell = c.analogy.replace("|", "\\|")
            out.append(f"| {_link(c, '../library/')} | {cell} |")
    return "\n".join(out) + "\n"


# --- all outputs -----------------------------------------------------------------------------------------

def build_outputs(lib, cockpit=True):
    base = lib.root.parent
    cat = catalog(lib)
    outputs = {
        lib.root / "catalog.json": dump_json(cat),
        lib.root / "README.md": library_readme(lib),
        lib.root / "einstufung.md": einstufung(lib),
        base / "reference" / "analogien.md": analogies(lib),
    }
    for name, text in paths(lib, cat).items():
        outputs[base / "paths" / name] = text
    for ch in lib.chapters:
        outputs[ch.path] = with_meta(ch.path.read_text(encoding="utf-8"), meta_block(lib, ch))
    if cockpit:
        outputs[base / "claude-code-workshop-ui.html"] = build_cockpit.render(lib, cat, diagrams=load_diagrams(lib))
    return outputs


def load_diagrams(lib):
    """Pre-rendered SVGs from tools/render_diagrams.py (optional step), keyed by build_cockpit.diagram_key."""
    folder = lib.root / "diagrams"
    found = {}
    if folder.exists():
        for path in sorted(folder.glob("*.svg")):
            found[path.stem] = path.read_text(encoding="utf-8")
    return found
