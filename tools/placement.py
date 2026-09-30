# -*- coding: utf-8 -*-
"""Placement engine of the practice library (reference implementation, standard library only).

  python tools/placement.py --template > einstufung.json        # empty answers document
  python tools/placement.py --answers einstufung.json --format md
  python tools/placement.py --answers einstufung.json --catalog resources/library/catalog.json

place(catalog, answers) implements spec docs/plans/2026-09-30-praxisbibliothek-design.md, section 6.3, steps A-F.
The cockpit carries a line-by-line JavaScript port; tools/fixtures/placement-golden.json keeps both in step.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "resources" / "library" / "catalog.json"
RANK = {"later": 0, "skip": 1, "skim": 2, "work": 3}
STATUSES = tuple(RANK)


def _minutes(chapter, status, percent):
    if status == "work":
        return chapter["minutes"]
    return -(-chapter["minutes"] * percent // 100)  # integer ceil, identical in JS


def normalize(catalog, answers):
    """Validate answers against the catalog and fill defaults. Raises ValueError on unknown ids."""
    rules = catalog["placement"]
    answers = answers or {}
    goal_ids = [g["id"] for g in rules["goals"]]
    time_ids = [t["id"] for t in rules["times"]]
    area_ids = [a["id"] for a in rules["areas"]]
    scenarios = {s["id"]: s for s in rules.get("scenarios", [])}
    chapter_ids = {c["id"] for c in catalog["chapters"]}

    goals = list(answers.get("goals") or [rules["default_goal"]])
    for g in goals:
        if g not in goal_ids:
            raise ValueError(f"unbekanntes Ziel: {g!r}")
    goals = goals[:2]
    time = answers.get("time") or rules["default_time"]
    if time not in time_ids:
        raise ValueError(f"unbekannte Zeitangabe: {time!r}")
    rating = {a: 0 for a in area_ids}
    for a, v in (answers.get("areas") or {}).items():
        if a not in rating:
            raise ValueError(f"unbekannter Bereich: {a!r}")
        if v is None:
            continue
        if v not in (0, 1, 2) or isinstance(v, bool):
            raise ValueError(f"Stand für {a} muss 0, 1, 2 oder null sein")
        rating[a] = v
    wrong_areas = set()
    for sid, opt in (answers.get("scenarios") or {}).items():
        if sid not in scenarios:
            raise ValueError(f"unbekanntes Szenario: {sid!r}")
        if opt is None:
            continue
        options = {o["id"] for o in scenarios[sid]["options"]}
        if opt not in options:
            raise ValueError(f"Szenario {sid}: unbekannte Option {opt!r}")
        if opt != scenarios[sid]["correct"]:
            wrong_areas.add(scenarios[sid]["area"])
    overrides = {}
    for cid, st in (answers.get("overrides") or {}).items():
        if cid not in chapter_ids:
            raise ValueError(f"Übersteuerung für unbekanntes Kapitel {cid!r}")
        if st not in STATUSES:
            raise ValueError(f"Übersteuerung {cid}: unbekannter Status {st!r}")
        overrides[cid] = st
    return {"goals": goals, "time": time, "rating": rating, "wrong_areas": wrong_areas, "overrides": overrides}


def place(catalog, answers):
    rules = catalog["placement"]
    chapters = sorted(catalog["chapters"], key=lambda c: c["order"])
    by_id = {c["id"]: c for c in chapters}
    a = normalize(catalog, answers)
    goals, time, overrides = a["goals"], a["time"], a["overrides"]
    effective = {k: (min(v, 1) if k in a["wrong_areas"] else v) for k, v in a["rating"].items()}
    gap_areas = {k for k in a["wrong_areas"] if a["rating"][k] == 2}
    goal_rules = {g["id"]: g for g in rules["goals"]}
    focus = set()
    for g in goals:
        focus |= set(goal_rules[g].get("focus_shelves") or [])
    base = set(rules["base_shelves"])
    only_assess = goals == ["einschaetzen"]
    percent = rules["skim_percent"]

    def r(c):
        return effective[c["area"]] if c.get("area") else None

    # --- A: relevance set R -------------------------------------------------
    if time == "schnellstart":
        relevant = set(rules["minimum_path"])
        later_reason = "after-quickstart"
    elif "moderieren" in goals:
        relevant = {c["id"] for c in chapters if c["session"] is not None}
        later_reason = "not-goal"
    else:
        relevant = set()
        for c in chapters:
            if c["type"] not in ("lesson", "setup"):
                continue
            if c["level"] == "core" and c["shelf"] in base:
                relevant.add(c["id"])
            if c["shelf"] in focus and (c["level"] in ("core", "deep-dive")
                                        or (c["level"] == "bonus" and time == "gruendlich")):
                relevant.add(c["id"])
        for c in chapters:
            if c["type"] == "practice" and any(
                    o in relevant and (r(by_id[o]) or 0) < 2 for o in c["offers"]):
                relevant.add(c["id"])
            elif c["type"] == "capstone" and ({"agents", "einschaetzen"} & set(goals)):
                relevant.add(c["id"])
            elif c["type"] == "community" and any(g != "einschaetzen" for g in goals):
                relevant.add(c["id"])
        later_reason = "not-goal"

    # --- B: status inside R -------------------------------------------------
    status, reason = {}, {}
    for c in chapters:
        cid = c["id"]
        if cid not in relevant:
            status[cid], reason[cid] = "later", later_reason
            continue
        t = c["type"]
        if t in ("lesson", "setup") and c.get("area"):
            rv = r(c)
            if rv == 0:
                st, rs = "work", "new"
            elif rv == 1 and t == "setup":
                st, rs = "work", "new"  # without an installation nothing works
            elif rv == 1:
                st, rs = ("work", "deep-focus") if c["level"] == "deep-dive" else ("skim", "heard")
                if c["area"] in gap_areas:
                    rs = "scenario-gap"
            else:
                st, rs = "skip", "known"
        elif t in ("lesson", "setup"):
            st, rs = "work", "new"
        elif t == "practice":
            st, rs = "work", "practice"
        elif t == "capstone":
            st, rs = ("skim" if only_assess else "work"), "capstone"
        else:  # community
            st, rs = "skim", "community"
        if only_assess and st == "work" and not c["safety_floor"]:
            st, rs = "skim", "assess"
        status[cid], reason[cid] = st, rs

    # --- C: safety floor ----------------------------------------------------
    for c in chapters:
        if not c["safety_floor"]:
            continue
        rv = r(c) or 0
        if c["id"] in relevant or rv == 2:
            floor = "work" if rv < 2 else "skim"
            if RANK[floor] > RANK[status[c["id"]]]:
                status[c["id"]], reason[c["id"]] = floor, "safety-floor"

    # --- D: prerequisites (requires_all is transitive: one pass suffices) ---
    def prerequisites(frozen):
        for c in chapters:
            if status[c["id"]] in ("work", "skim"):
                for p in c["requires_all"]:
                    if p not in frozen and status[p] == "later":
                        if (r(by_id[p]) or 0) == 2:
                            status[p], reason[p] = "skip", "known"
                        else:
                            status[p], reason[p] = "skim", "prerequisite"

    prerequisites(frozen=set())

    # --- E: overrides -------------------------------------------------------
    computed = dict(status)
    for cid, st in overrides.items():
        status[cid], reason[cid] = st, "override"
    prerequisites(frozen=set(overrides))
    warnings = []
    for cid in overrides:
        c = by_id[cid]
        if c["safety_floor"] and RANK[status[cid]] < RANK[computed[cid]]:
            warnings.append({"code": "override-safety", "ids": [cid]})
    for c in chapters:
        if status[c["id"]] not in ("work", "skim"):
            continue
        for p in c["requires_all"]:
            if p in overrides and status[p] in ("skip", "later") and computed[p] in ("work", "skim"):
                warnings.append({"code": "override-prereq", "ids": [p, c["id"]]})

    # --- F: stages (contiguous in teaching order) ---------------------------
    budget = {t["id"]: t["stage_minutes"] for t in rules["times"]}[time]
    stage_of, stages = {}, []
    n, acc = 1, 0
    work_min = skim_min = 0
    for c in chapters:
        st = status[c["id"]]
        if st not in ("work", "skim"):
            continue
        m = _minutes(c, st, percent)
        if st == "work":
            work_min += m
        else:
            skim_min += m
        if acc > 0 and budget is not None and acc + m > budget:
            stages.append({"n": n, "minutes": acc})
            n, acc = n + 1, 0
        stage_of[c["id"]] = n
        acc += m
    if acc > 0:
        stages.append({"n": n, "minutes": acc})
    if time == "schnellstart" and work_min + skim_min > rules["quickstart_warn_minutes"]:
        warnings.append({"code": "quickstart-long", "ids": []})

    order = {c["id"]: c["order"] for c in chapters}
    for w in warnings:
        w["ids"] = sorted(w["ids"], key=lambda i: order[i])
    warnings.sort(key=lambda w: (w["code"], [order[i] for i in w["ids"]]))
    return {
        "version": 1,
        "chapters": [{"id": c["id"], "status": status[c["id"]], "reason": reason[c["id"]],
                      "stage": stage_of.get(c["id"]), "override": c["id"] in overrides} for c in chapters],
        "stages": stages,
        "totals": {"work_min": work_min, "skim_min": skim_min},
        "warnings": warnings,
    }


def template(catalog):
    rules = catalog["placement"]
    return {
        "version": 1,
        "goals": [rules["default_goal"]],
        "time": rules["default_time"],
        "areas": {a["id"]: None for a in rules["areas"]},
        "scenarios": {s["id"]: None for s in rules.get("scenarios", [])},
        "overrides": {},
    }


def to_markdown(catalog, result):
    rules = catalog["placement"]
    meta = {c["id"]: c for c in catalog["chapters"]}
    label = {"work": "durcharbeiten", "skim": "überfliegen", "skip": "Schnellcheck reicht", "later": "später"}
    out = ["# Dein Lernpfad", ""]
    hours = (result["totals"]["work_min"] + result["totals"]["skim_min"]) / 60
    out.append(f"Etappen: {len(result['stages'])} · zusammen etwa {hours:.1f} Stunden.")
    for w in result["warnings"]:
        ids = ", ".join(w["ids"])
        out.append(f"> ⚠ {rules['warnings'][w['code']]}" + (f" ({ids})" if ids else ""))
    for stage in result["stages"]:
        out += ["", f"## Etappe {stage['n']} (~{stage['minutes']} Min)", ""]
        for ch in result["chapters"]:
            if ch["stage"] == stage["n"]:
                title = meta[ch["id"]].get("title", "")
                file = meta[ch["id"]].get("file", "")
                name = f"[{ch['id']} {title}]({file})" if file else f"{ch['id']} {title}".strip()
                out.append(f"- {name} — {label[ch['status']]}: {rules['reasons'][ch['reason']]}")
    skipped = [c for c in result["chapters"] if c["status"] == "skip"]
    if skipped:
        out += ["", "## Schnellcheck reicht", ""]
        out += [f"- {c['id']} {meta[c['id']].get('title', '')}".rstrip() for c in skipped]
    return "\n".join(out) + "\n"


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--answers", type=Path)
    parser.add_argument("--format", choices=("json", "md"), default="json")
    parser.add_argument("--template", action="store_true")
    args = parser.parse_args(argv)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    if args.template:
        print(json.dumps(template(catalog), ensure_ascii=False, indent=1))
        return 0
    if not args.answers:
        parser.error("--answers oder --template angeben")
    answers = json.loads(args.answers.read_text(encoding="utf-8"))
    try:
        result = place(catalog, answers)
    except ValueError as err:
        print(f"Fehler in den Antworten: {err}", file=sys.stderr)
        return 2
    print(to_markdown(catalog, result) if args.format == "md" else json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
