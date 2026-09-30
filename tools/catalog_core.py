# -*- coding: utf-8 -*-
"""Placement-relevant core of the library catalog.

core_catalog() is shared by the real build (entries from parsed chapters, tools/build_library.py) and by the
contract catalog for the placement tests (entries from docs/migration/chapter-meta.yaml).

  python tools/catalog_core.py --from-meta     # writes tools/fixtures/placement-catalog.json
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "docs" / "migration" / "chapter-meta.yaml"
LIBRARY = ROOT / "resources" / "library"
CONTRACT = ROOT / "tools" / "fixtures" / "placement-catalog.json"

SESSION_ID = re.compile(r"^S([0-4])\.([1-9][0-9]?)$")
EXTRA_ID = re.compile(r"^X\.([1-9][0-9]?)$")
CORE_FIELDS = ("id", "type", "shelf", "level", "minutes", "requires", "safety_floor", "offers", "after")


def order_of(chapter_id, after=None):
    match = SESSION_ID.match(chapter_id or "")
    if match:
        return int(match.group(1)) * 1000 + int(match.group(2)) * 10
    if EXTRA_ID.match(chapter_id or ""):
        if not after:
            raise ValueError(f"{chapter_id}: X-Kapitel brauchen 'after'")
        return order_of(after) + 5
    raise ValueError(f"unbekannte Kapitel-ID: {chapter_id!r}")


def session_of(chapter_id):
    match = SESSION_ID.match(chapter_id or "")
    return int(match.group(1)) if match else None


def core_catalog(entries, shelves, placement):
    """entries: dicts with at least CORE_FIELDS (offers/after optional). Pure function."""
    by_id = {e["id"]: e for e in entries}
    area_of = {}
    for area in placement.get("areas", []) or []:
        for cid in area.get("chapters", []) or []:
            area_of[cid] = area["id"]
    orders = {cid: order_of(cid, e.get("after")) for cid, e in by_id.items()}

    closure = {}

    def requires_all(cid, stack=()):
        if cid in closure:
            return closure[cid]
        if cid in stack:
            raise ValueError("Zyklus in requires: " + " → ".join(stack + (cid,)))
        found = set()
        for req in by_id[cid].get("requires", []) or []:
            if req in by_id:
                found.add(req)
                found |= requires_all(req, stack + (cid,))
        closure[cid] = found
        return found

    chapters = []
    for cid in sorted(by_id, key=lambda c: orders[c]):
        e = by_id[cid]
        chapters.append({
            "id": cid,
            "type": e["type"],
            "shelf": e["shelf"],
            "level": e["level"],
            "minutes": int(e["minutes"]),
            "order": orders[cid],
            "session": session_of(cid),
            "requires": list(e.get("requires", []) or []),
            "requires_all": sorted(requires_all(cid), key=lambda c: orders[c]),
            "safety_floor": bool(e.get("safety_floor")),
            "offers": list(e.get("offers", []) or []),
            "area": area_of.get(cid),
        })
    return {
        "version": 1,
        "shelves": [{"id": s["id"], "title": s.get("title", "")} for s in shelves],
        "placement": placement,
        "chapters": chapters,
    }


def contract_catalog():
    import yaml  # maintainer dependency only
    meta = yaml.safe_load(META.read_text(encoding="utf-8"))
    shelves = yaml.safe_load((LIBRARY / "_shelves.yaml").read_text(encoding="utf-8"))
    placement = yaml.safe_load((LIBRARY / "_placement.yaml").read_text(encoding="utf-8"))
    return core_catalog(meta, shelves, placement)


def dump(catalog):
    return json.dumps(catalog, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from-meta", action="store_true", help="Kontrakt-Katalog aus chapter-meta.yaml schreiben")
    parser.add_argument("--check", action="store_true", help="Exit 1, wenn der Kontrakt-Katalog veraltet ist")
    args = parser.parse_args(argv)
    text = dump(contract_catalog())
    if args.check:
        current = CONTRACT.read_text(encoding="utf-8").replace("\r\n", "\n") if CONTRACT.exists() else ""
        if current != text:
            print(f"veraltet: {CONTRACT.relative_to(ROOT)} — python tools/catalog_core.py --from-meta")
            return 1
        print("OK — Kontrakt-Katalog aktuell.")
        return 0
    if args.from_meta:
        CONTRACT.write_text(text, encoding="utf-8", newline="\n")
        print(f"geschrieben: {CONTRACT.relative_to(ROOT)}")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
