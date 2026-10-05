# -*- coding: utf-8 -*-
"""Validate and build the practice library.

  python tools/build_library.py validate [--root resources/library] [--complete]
  python tools/build_library.py validate --chapter resources/library/s2-08-hook-konfigurieren.md
  python tools/build_library.py build    # writes generated files (see build_outputs)
  python tools/build_library.py check    # exit 1 if a generated file is stale

Spec: docs/plans/2026-09-30-praxisbibliothek-design.md (sections 4, 6, 7).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import statistics
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover - non-reconfigurable streams
    pass

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import library_model as lm  # noqa: E402

ROOT = TOOLS.parent
DEFAULT_LIBRARY = ROOT / "resources" / "library"
CHAPTER_META = ROOT / "docs" / "migration" / "chapter-meta.yaml"
# Chapters whose recall questions must carry answers. The list grows shelf by shelf (design 2026-10-05, packages
# P5 and P7) and is replaced by the rule "every lesson" once all shelves are done.
ANSWERS_REQUIRED = TOOLS / "fixtures" / "answers-required.txt"
CONTRACT_FIELDS = ("id", "type", "title", "shelf", "level", "minutes", "requires", "safety_floor", "transferable",
                   "aliases", "offers", "after")

REQUIRED_IDS = (["S0.1"] + [f"S1.{n}" for n in range(1, 21)] + [f"S2.{n}" for n in range(1, 21)]
                + [f"S3.{n}" for n in range(1, 16)] + [f"S4.{n}" for n in range(1, 11)] + ["X.1", "X.2", "X.3", "X.4"])

ALL = set(lm.SECTION_ORDER)
# Allowed and required H2 sections per chapter type (spec 4.3).
# "Vorführen" is no chapter section any more: demos live in the moderation layer (_check_demos).
ALLOWED = {
    "lesson": ALL,
    "setup": ALL,
    "practice": {"Auf einen Blick", "Selbst machen", "Check", "Weiterlesen"},
    "capstone": ALL,
    "community": ALL - {"Schnellcheck"},
}
REQUIRED = {
    "lesson": {"Schnellcheck", "Auf einen Blick", "Bild im Kopf", "Im Detail", "Check", "Weiterlesen"},
    "setup": {"Auf einen Blick", "Im Detail", "Selbst machen", "Check", "Weiterlesen"},
    "practice": {"Auf einen Blick", "Selbst machen", "Check"},
    "capstone": {"Auf einen Blick", "Im Detail", "Selbst machen", "Check", "Weiterlesen"},
    "community": {"Auf einen Blick", "Im Detail", "Weiterlesen"},
}
# (min, max) count of cockpit examples and quizzes per type.
EXAMPLES = {"lesson": (1, 1), "setup": (0, 1), "practice": (0, 1), "capstone": (0, 1), "community": (0, 1)}
QUIZZES = {"lesson": (1, 1), "setup": (0, 1), "practice": (0, 0), "capstone": (0, 1), "community": (0, 0)}
SOURCES_REQUIRED = {"lesson", "setup"}
QUIZ_TELL_MAX = 1.35   # correct answer at most 1.35 x mean length of the wrong ones
QUIZ_TELL_MIN = 0.6    # every wrong answer at least 0.6 x the correct one
QUIZ_LONGEST_SHARE = 0.4  # library-wide: correct answer strictly longest in at most 40 % of quizzes
FILENAME = re.compile(r"^(?:s([0-4])-(\d{2})|x-(\d{2}))-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
QUIZ_SUMMARY = re.compile(r"<details><summary>Quizfrage</summary>")


@dataclass(frozen=True)
class Problem:
    path: str
    rule: str
    message: str

    def __str__(self):
        return f"{self.path}: [{self.rule}] {self.message}"


def _rel(path) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def _check_front(ch, add):
    f = ch.front
    required = ["id", "type", "title", "shelf", "level", "minutes", "requires", "safety_floor", "transferable",
                "outcome", "sources", "aliases"]
    for key in required:
        if key not in f:
            add("frontmatter-schema", f"Pflichtfeld '{key}' fehlt")
    if f.get("type") not in lm.CHAPTER_TYPES:
        add("frontmatter-schema", f"type muss eines von {', '.join(lm.CHAPTER_TYPES)} sein")
    if f.get("level") not in lm.LEVELS:
        add("frontmatter-schema", f"level muss eines von {', '.join(lm.LEVELS)} sein")
    minutes = f.get("minutes")
    if not isinstance(minutes, int) or isinstance(minutes, bool) or not 5 <= minutes <= 60:
        add("frontmatter-schema", "minutes muss eine ganze Zahl zwischen 5 und 60 sein")
    for key in ("safety_floor", "transferable"):
        if key in f and not isinstance(f[key], bool):
            add("frontmatter-schema", f"{key} muss true oder false sein")
    for key in ("requires", "sources", "aliases"):
        if key in f and not isinstance(f[key], list):
            add("frontmatter-schema", f"{key} muss eine Liste sein")
    if not str(f.get("title", "")).strip():
        add("frontmatter-schema", "title ist leer")
    if not str(f.get("outcome", "")).startswith("Ich "):
        add("frontmatter-schema", "outcome beginnt mit 'Ich ' (Ich kann danach …)")
    is_extra = bool(lm.EXTRA_ID.match(ch.id))
    if is_extra and not f.get("after"):
        add("frontmatter-schema", "X-Kapitel brauchen 'after'")
    if not is_extra and "after" in f and f.get("after") is not None:
        add("frontmatter-schema", "'after' ist nur für X-Kapitel erlaubt")
    if ch.type == "practice":
        if not isinstance(f.get("offers"), list) or not f.get("offers"):
            add("frontmatter-schema", "Praxis-Stationen brauchen 'offers' (Liste der Kapitel mit Übungen)")
    elif "offers" in f:
        add("frontmatter-schema", "'offers' ist nur für Praxis-Stationen erlaubt")


GENERATED_TARGETS = ("README.md", "einstufung.md", "../paths/README.md", "../paths/live-workshop.md",
                     "../paths/schnellstart.md", "../reference/analogien.md")


def github_slug(text: str) -> str:
    """Heading anchor as GitHub renders it (lower case, punctuation removed, spaces to hyphens)."""
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def anchors_of(path: Path) -> set:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    found, seen, in_fence = set(), {}, False
    for line in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            slug = github_slug(m.group(1))
            n = seen.get(slug, 0)
            found.add(slug if n == 0 else f"{slug}-{n}")
            seen[slug] = n + 1
        found.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', line))
    return found


def _check_body(ch, add, planned=frozenset(), goal_targets=(), answers_required=frozenset()):
    t = ch.type if ch.type in ALLOWED else "lesson"
    for title in ch.section_order:
        if title not in ALLOWED[t]:
            add("sections-allowed", f"Abschnitt '## {title}' ist für Typ {t} nicht erlaubt")
    if len(set(ch.section_order)) != len(ch.section_order):
        add("sections-allowed", "Abschnitt doppelt")
    for title in sorted(REQUIRED[t] - set(ch.section_order)):
        add("sections-required", f"Pflichtabschnitt '## {title}' fehlt")
    known = [s for s in ch.section_order if s in lm.SECTION_ORDER]
    if known != sorted(known, key=lm.SECTION_ORDER.index):
        add("section-order", "Abschnitte stehen nicht in der festen Reihenfolge " + " → ".join(lm.SECTION_ORDER))
    expected_h1 = f"{ch.id} · {ch.title}"
    if ch.h1 != expected_h1:
        add("h1", f"H1 muss '# {expected_h1}' lauten, ist '# {ch.h1}'")
    body = "\n".join(ch.sections.values())
    n_examples = body.count(lm.EXAMPLE_MARKER)
    low, high = EXAMPLES[t]
    if not low <= n_examples <= high or (n_examples and ch.example is None):
        add("example-count", f"{n_examples} cockpit:example (erlaubt {low}–{high}, direkt gefolgt von einem Codeblock)")
    n_quiz = len(QUIZ_SUMMARY.findall(body))
    low, high = QUIZZES[t]
    if not low <= n_quiz <= high:
        add("quiz-count", f"{n_quiz} Quizblöcke (erlaubt {low}–{high})")
    if n_quiz and "Check" in ch.sections and not QUIZ_SUMMARY.search(ch.sections["Check"]):
        add("quiz-count", "der Quizblock gehört in '## Check'")
    q = ch.quiz
    if q is not None and not q.closed:
        add("quiz-shape", "Quizblock ist nicht mit </details> geschlossen")
    elif q is not None:
        if (not q.question or not q.correct or q.n_correct != 1 or len(q.wrong) != 3
                or not all(w.strip() for w in q.wrong)):
            add("quiz-shape", "Quiz braucht **Frage:**, genau eine **Richtig:**- und drei Falsch-Zeilen")
        elif q.correct in q.wrong:
            add("quiz-shape", "richtige Antwort steht auch unter den falschen")
        else:
            mean = statistics.mean(len(w) for w in q.wrong)
            if len(q.correct) > QUIZ_TELL_MAX * mean or min(len(w) for w in q.wrong) < QUIZ_TELL_MIN * len(q.correct):
                add("quiz-length-tell", f"Antwortlängen verraten die Lösung (richtig {len(q.correct)} Zeichen, "
                    f"falsch Ø {mean:.0f}); angleichen auf ≤ {QUIZ_TELL_MAX} × Mittel")
    if ch.answers is not None:
        if not ch.recall or len(ch.answers) != len(ch.recall) or not all(a.strip() for a in ch.answers):
            add("answers-count", f"{len(ch.answers)} Auflösungen zu {len(ch.recall)} Abruffragen "
                "(je Frage genau eine, gleiche Nummer, Block mit </details> geschlossen)")
    elif ch.recall and ch.id in answers_required:
        add("answers-required", f"{len(ch.recall)} Abruffragen ohne Block 'Auflösung' "
            "(<details><summary>Auflösung</summary> nach den Fragen)")
    if t == "lesson" and len(ch.skip_check) != 2:
        add("skip-check-count", f"Schnellcheck braucht genau 2 Fragen, hat {len(ch.skip_check)}")
    elif "Schnellcheck" in ch.sections and len(ch.skip_check) != 2:
        add("skip-check-count", f"Schnellcheck braucht genau 2 Fragen, hat {len(ch.skip_check)}")
    raw = ch.path.read_text(encoding="utf-8")
    if "TODO(migration)" in raw:
        add("no-migration-todo", "offene TODO(migration)-Markierung")
    if lm.MODERATOR_BLOCK in raw:
        add("no-moderation-block", "Block 'Für Moderierende' gehört in die Moderationsschicht "
            "(resources/moderation/vorfuehren/), nicht ins Kapitel")
    for src in ch.sources:
        if not src.startswith("https://"):
            add("sources-https", f"Quelle ohne https: {src}")
    if t in SOURCES_REQUIRED and not ch.sources:
        add("sources-required", "mindestens eine offizielle Quelle unter sources")
    _check_links(ch.path, ch.links, add, planned, generated=GENERATED_TARGETS + tuple(goal_targets))


def _check_links(path, links, add, planned=frozenset(), generated=GENERATED_TARGETS):
    """Relative links of one Markdown file lead to an existing file and, for .md targets, an existing anchor."""
    for target in links:
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        file_part, _, fragment = target.partition("#")
        if file_part in planned or file_part in generated:
            continue
        dest = (path.parent / file_part).resolve() if file_part else path.resolve()
        if file_part and not dest.exists():
            add("links-resolve", f"Link-Ziel existiert nicht: {target}")
        elif fragment and dest.suffix == ".md" and fragment not in anchors_of(dest):
            add("links-resolve", f"Anker #{fragment} gibt es in {dest.name} nicht")


# Generated files as seen from a demo file (two folders below resources/).
DEMO_GENERATED_TARGETS = tuple("../" + t if t.startswith("../") else "../../library/" + t for t in GENERATED_TARGETS)


def goal_path_targets(lib) -> tuple:
    """Goal paths the generator writes (one per goal, none for 'moderieren'), as linked from a chapter."""
    goals = (lib.placement or {}).get("goals", []) or []
    return tuple(f"../paths/ziel-{g['id']}.md" for g in goals
                 if isinstance(g, dict) and g.get("id") and g["id"] != "moderieren")


def _check_demos(lib, report):
    """Moderation layer: every demo file belongs to one chapter, names it, and its links resolve."""
    folder = lib.demo_dir
    if not folder.is_dir():
        return
    by_file = {ch.path.name: ch for ch in lib.chapters}
    for path in sorted(folder.glob("*.md")):
        add = report(path)
        ch = by_file.get(path.name)
        if ch is None:
            add("demo-orphan", "zu dieser Demo-Datei gibt es kein Kapitel mit demselben Dateinamen")
            continue
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        expected = f"# Vorführen: {ch.id} · {ch.title}"
        first = text.split("\n", 1)[0].rstrip()
        if first != expected:
            add("demo-h1", f"erste Zeile muss '{expected}' lauten, ist '{first}'")
        if lm.EXAMPLE_MARKER in text:
            add("demo-no-example-marker", "cockpit:example gehört ins Kapitel, nicht in die Demo-Datei")
        _check_links(path, lm._links(text), add,
                     generated=DEMO_GENERATED_TARGETS + tuple("../" + t for t in goal_path_targets(lib)))


def _check_graph(lib, by_id, report, planned_orders=None):
    for ch in lib.chapters:
        add = report(ch.path)
        planned_orders = planned_orders or {}
        for req in ch.requires:
            if req not in by_id and req not in planned_orders:
                add("requires-exist", f"Voraussetzung {req} gibt es nicht")
                continue
            try:
                req_order = by_id[req].order if req in by_id else planned_orders[req]
                if req_order >= ch.order:
                    add("requires-backward", f"Voraussetzung {req} steht nicht vor {ch.id}")
            except ValueError:
                pass
        if ch.type == "practice":
            if ch.requires:
                add("practice-no-requires", "Praxis-Stationen haben keine requires (nur offers)")
            for off in ch.offers:
                if off not in by_id:
                    add("offers-exist", f"offers nennt {off}, das es nicht gibt")
                elif by_id[off].session != ch.session:
                    add("offers-exist", f"{off} liegt nicht in Session {ch.session}")
    # cycles (defensive: backward order already forbids them, but order may be broken)
    state = {}

    def visit(cid, stack):
        if state.get(cid) == 1:
            report(by_id[cid].path)("requires-acyclic", "Zyklus: " + " → ".join(stack + [cid]))
            return
        if state.get(cid) == 2 or cid not in by_id:
            return
        state[cid] = 1
        for req in by_id[cid].requires:
            visit(req, stack + [cid])
        state[cid] = 2

    for cid in by_id:
        visit(cid, [])


def _check_placement(lib, by_id, report, planned_ids=frozenset()):
    placement = lib.placement or {}
    path = lib.root / "_placement.yaml"
    add = report(path)
    shelves = {s.get("id") for s in lib.shelves if isinstance(s, dict)}
    for shelf in placement.get("base_shelves", []) or []:
        if shelf not in shelves:
            add("placement-refs", f"base_shelves nennt unbekanntes Regal {shelf}")
    for goal in placement.get("goals", []) or []:
        for shelf in goal.get("focus_shelves", []) or []:
            if shelf not in shelves:
                add("placement-refs", f"Ziel {goal.get('id')}: unbekanntes Regal {shelf}")
    seen = {}
    areas = placement.get("areas", []) or []
    area_ids = {a.get("id") for a in areas}
    for area in areas:
        for cid in area.get("chapters", []) or []:
            if cid not in by_id and cid not in planned_ids:
                add("placement-refs", f"Bereich {area.get('id')}: Kapitel {cid} gibt es nicht")
            if cid in seen:
                add("area-unique", f"{cid} steht in den Bereichen {seen[cid]} und {area.get('id')}")
            seen[cid] = area.get("id")
    minimum = list(placement.get("minimum_path", []) or [])
    for cid in minimum:
        if cid not in by_id and cid not in planned_ids:
            add("placement-refs", f"minimum_path nennt {cid}, das es nicht gibt")
    closure, todo = set(), [c for c in minimum if c in by_id]
    while todo:
        cid = todo.pop()
        for req in by_id[cid].requires:
            if req in by_id and req not in closure:
                closure.add(req)
                todo.append(req)
    for req in sorted(closure - set(minimum)):
        add("minimum-path-closed", f"minimum_path braucht auch seine Voraussetzung {req}")
    goal_ids = {g.get("id") for g in placement.get("goals", []) or []}
    for cid, limited in (placement.get("chapter_goals") or {}).items():
        if cid not in by_id and cid not in planned_ids:
            add("placement-refs", f"chapter_goals nennt {cid}, das es nicht gibt")
        if not isinstance(limited, list):
            add("placement-refs", f"chapter_goals {cid}: erwartet eine Liste von Zielen")
            continue
        for g in limited:
            if g not in goal_ids:
                add("placement-refs", f"chapter_goals {cid}: unbekanntes Ziel {g}")
    for sc in placement.get("scenarios", []) or []:
        option_ids = {o.get("id") for o in sc.get("options", []) or []}
        if sc.get("area") not in area_ids:
            add("placement-refs", f"Szenario {sc.get('id')}: unbekannter Bereich {sc.get('area')}")
        if sc.get("correct") not in option_ids:
            add("placement-refs", f"Szenario {sc.get('id')}: correct ist keine Option-ID")
        if sc.get("chapter") not in by_id and sc.get("chapter") not in planned_ids:
            add("placement-refs", f"Szenario {sc.get('id')}: Kapitel {sc.get('chapter')} gibt es nicht")


def load_answers_required(path=ANSWERS_REQUIRED) -> frozenset:
    """Chapter IDs, one per line; '#' starts a comment."""
    if not Path(path).exists():
        return frozenset()
    lines = (line.split("#", 1)[0].strip() for line in Path(path).read_text(encoding="utf-8").splitlines())
    return frozenset(line for line in lines if line)


def coverage(lib) -> str:
    """How far the library is on its way to 'every lesson ends in something to do and can be checked alone'."""
    lessons = [c for c in lib.chapters if c.type == "lesson"]
    with_exercise = sum(1 for c in lessons if "Selbst machen" in c.sections)
    with_answers = sum(1 for c in lessons if c.answers and len(c.answers) == len(c.recall))
    return (f"Lektionen mit Übung: {with_exercise} von {len(lessons)} · "
            f"mit Auflösung: {with_answers} von {len(lessons)}")


def load_meta(path=CHAPTER_META):
    import yaml
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) if Path(path).exists() else None


def _check_contract(ch, entry, add):
    if entry is None:
        add("meta-contract", f"{ch.id} fehlt in docs/migration/chapter-meta.yaml")
        return
    if ch.path.name != entry.get("file"):
        add("meta-contract", f"Dateiname laut Metadaten: {entry.get('file')}")
    for key in CONTRACT_FIELDS:
        want = entry.get(key, [] if key in ("offers", "aliases", "requires") else None)
        have = ch.front.get(key, [] if key in ("offers", "aliases", "requires") else None)
        if want != have:
            add("meta-contract", f"{key}: Metadaten {want!r}, Kapitel {have!r}")


def validate(lib, *, complete: bool, meta=None, answers_required=frozenset()) -> list:
    """meta: binding chapter metadata (list of dicts) or None to skip the contract rule.
    answers_required: IDs of chapters whose recall questions must have answers."""
    problems = []
    meta_by_id = {e["id"]: e for e in meta} if meta else None
    planned = frozenset() if complete or not meta else frozenset(e["file"] for e in meta)

    def report(path):
        rel = _rel(path)
        return lambda rule, message: problems.append(Problem(rel, rule, message))

    for err in lib.problems:
        report(err.path)("parse", err.message)
    shelves = {s.get("id") for s in lib.shelves if isinstance(s, dict)}
    goal_targets = goal_path_targets(lib)
    by_id, aliases = {}, {}
    for ch in lib.chapters:
        add = report(ch.path)
        _check_front(ch, add)
        if not (lm.SESSION_ID.match(ch.id) or lm.EXTRA_ID.match(ch.id)):
            add("id-format", f"ID {ch.id!r} passt nicht zu S<0-4>.<n> oder X.<n>")
        elif ch.id in by_id:
            add("id-unique", f"ID {ch.id} gibt es schon in {_rel(by_id[ch.id].path)}")
        else:
            by_id[ch.id] = ch
        for alias in ch.aliases:
            if alias in aliases:
                add("alias-unique", f"Alias {alias} gibt es schon bei {aliases[alias]}")
            aliases[alias] = ch.id
        match = FILENAME.match(ch.path.name)
        expected = None
        if lm.SESSION_ID.match(ch.id):
            s, p = lm.SESSION_ID.match(ch.id).groups()
            expected = f"s{s}-{int(p):02d}-"
        elif lm.EXTRA_ID.match(ch.id):
            expected = f"x-{int(lm.EXTRA_ID.match(ch.id).group(1)):02d}-"
        if not match or (expected and not ch.path.name.startswith(expected)):
            add("filename", f"Dateiname {ch.path.name} passt nicht zu {ch.id} (erwartet {expected}<slug>.md)")
        if ch.shelf not in shelves:
            add("shelf-exists", f"Regal {ch.shelf!r} fehlt in _shelves.yaml")
        _check_body(ch, add, planned, goal_targets, answers_required)
        if meta_by_id is not None:
            _check_contract(ch, meta_by_id.get(ch.id), add)
    orders = {}
    for ch in lib.chapters:
        try:
            o = ch.order
        except ValueError:
            continue
        if o in orders:
            report(ch.path)("order-unique", f"Reihenfolge {o} hat schon {orders[o]} (after anpassen)")
        orders.setdefault(o, ch.id)
    planned_orders = {}
    if not complete and meta:
        import catalog_core
        for e in meta:
            try:
                planned_orders[e["id"]] = catalog_core.order_of(e["id"], e.get("after"))
            except (KeyError, ValueError):
                continue
    _check_graph(lib, by_id, report, planned_orders)
    planned_ids = frozenset() if complete or not meta else frozenset(e["id"] for e in meta)
    _check_placement(lib, by_id, report, planned_ids)
    _check_demos(lib, report)
    if complete:
        quizzes = [c.quiz for c in lib.chapters if c.quiz and c.quiz.closed and len(c.quiz.wrong) == 3]
        longest = sum(1 for q in quizzes if len(q.correct) > max(len(w) for w in q.wrong))
        if quizzes and longest / len(quizzes) > QUIZ_LONGEST_SHARE:
            report(lib.root)("quiz-longest-share", f"richtige Antwort ist in {longest} von {len(quizzes)} Quizfragen die "
                             f"längste (erlaubt ≤ {int(QUIZ_LONGEST_SHARE * 100)} %)")
        missing = [cid for cid in REQUIRED_IDS if cid not in by_id]
        if missing:
            report(lib.root)("required-ids", "fehlende Kapitel: " + ", ".join(missing))
    return problems


def _norm(text: str) -> str:
    return text.replace("\r\n", "\n")


def build(root, *, write: bool, complete: bool = False) -> int:
    """Validate, then write (build) or compare (check) all generated files."""
    import library_generate as gen

    root = Path(root).resolve()
    lib = lm.load_library(root)
    is_default = root == DEFAULT_LIBRARY.resolve()
    meta = load_meta() if is_default else None
    problems = validate(lib, complete=complete, meta=meta,
                        answers_required=load_answers_required() if is_default else frozenset())
    if problems:
        print("Build abgebrochen, der Validator meldet Befunde:")
        return _print(problems)
    outputs = gen.build_outputs(lib)
    stale = []
    for path, text in sorted(outputs.items()):
        current = _norm(path.read_text(encoding="utf-8")) if path.exists() else None
        if current != _norm(text):
            stale.append(path)
            if write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
    for path in stale:
        print(("geschrieben: " if write else "veraltet: ") + _rel(path))
    if write:
        print(f"{len(stale)} von {len(outputs)} Dateien aktualisiert.")
        return 0
    print("OK — alle generierten Dateien aktuell." if not stale else
          f"{len(stale)} Datei(en) veraltet — python tools/build_library.py build")
    return 1 if stale else 0


def _print(problems) -> int:
    for p in problems:
        print(p)
    print(f"{len(problems)} Befund(e)" if problems else "OK — keine Befunde.")
    return 1 if problems else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--root", type=Path, default=DEFAULT_LIBRARY)
    v.add_argument("--chapter", type=Path)
    v.add_argument("--complete", action="store_true")
    for name in ("build", "check"):
        sp = sub.add_parser(name)
        sp.add_argument("--root", type=Path, default=DEFAULT_LIBRARY)
        sp.add_argument("--complete", action="store_true", help="auch Vollständigkeit prüfen")
    args = parser.parse_args(argv)
    if args.cmd in ("build", "check"):
        return build(args.root, write=args.cmd == "build", complete=args.complete)
    if args.cmd == "validate":
        if args.chapter:
            chapter = args.chapter.resolve()
            lib = lm.load_library(chapter.parent)
            rel = _rel(chapter)
            is_default = chapter.parent == DEFAULT_LIBRARY.resolve()
            meta = load_meta() if is_default else None
            required = load_answers_required() if is_default else frozenset()
            found = [p for p in validate(lib, complete=False, meta=meta, answers_required=required) if p.path == rel]
            if not found and chapter not in {c.path.resolve() for c in lib.chapters}:
                found = [Problem(rel, "parse", "Datei wurde nicht als Kapitel geladen (Dateiname oder Pfad prüfen)")]
            return _print(found)
        is_default = args.root.resolve() == DEFAULT_LIBRARY.resolve()
        meta = load_meta() if is_default else None
        lib = lm.load_library(args.root)
        code = _print(validate(lib, complete=args.complete, meta=meta,
                               answers_required=load_answers_required() if is_default else frozenset()))
        print(coverage(lib))
        return code
    return 2


if __name__ == "__main__":
    sys.exit(main())
