"""Placement engine: hand-written persona expectations, invariants, golden outputs, CLI."""
from pathlib import Path
import copy
import importlib.util
import json
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tools" / "fixtures"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


placement = _load("placement")
catalog_core = _load("catalog_core")
CATALOG = json.loads((FIX / "placement-catalog.json").read_text(encoding="utf-8"))
VECTORS = json.loads((FIX / "placement-vectors.json").read_text(encoding="utf-8"))["personas"]
BY_ID = {p["id"]: p for p in VECTORS}
GOLDEN_PATH = FIX / "placement-golden.json"
ORDER = {c["id"]: c["order"] for c in CATALOG["chapters"]}


def run(answers):
    return placement.place(CATALOG, answers)


def by_chapter(result):
    return {c["id"]: c for c in result["chapters"]}


def test_contract_catalog_is_current():
    assert catalog_core.main(["--check"]) == 0


@pytest.mark.parametrize("persona", VECTORS, ids=lambda p: p["id"])
def test_vectors_core(persona):
    result = run(persona["answers"])
    exp = persona["expect"]
    if "same_as" in exp:
        assert result == run(BY_ID[exp["same_as"]]["answers"])
        return
    if "same_as_answers" in exp:
        assert result == run(exp["same_as_answers"])
        return
    ch = by_chapter(result)
    for cid, (status, reason) in exp.get("status", {}).items():
        assert (ch[cid]["status"], ch[cid]["reason"]) == (status, reason), cid
    if "recommended" in exp:
        rec = [c["id"] for c in result["chapters"] if c["status"] in ("work", "skim")]
        assert rec == exp["recommended"]
    if "first_stage" in exp:
        assert [c["id"] for c in result["chapters"] if c["stage"] == 1] == exp["first_stage"]
    if "first_stage_minutes" in exp:
        assert result["stages"][0]["minutes"] == exp["first_stage_minutes"]
    if "stages" in exp:
        assert len(result["stages"]) == exp["stages"]
    if "max_stage_minutes" in exp:
        singles = {s["n"] for s in result["stages"]
                   if sum(1 for c in result["chapters"] if c["stage"] == s["n"]) == 1}
        assert all(s["minutes"] <= exp["max_stage_minutes"] or s["n"] in singles for s in result["stages"])
    if "overridden" in exp:
        assert sorted(c["id"] for c in result["chapters"] if c["override"]) == exp["overridden"]
    if exp.get("all_session_chapters_recommended"):
        for c in CATALOG["chapters"]:
            if c["session"] is not None:
                assert ch[c["id"]]["status"] in ("work", "skim"), c["id"]
    assert result["warnings"] == exp.get("warnings", [])


@pytest.mark.parametrize("persona", VECTORS, ids=lambda p: p["id"])
def test_prerequisites_recommended_or_skipped(persona):
    result = run(persona["answers"])
    ch = by_chapter(result)
    overrides = persona["answers"].get("overrides", {})
    for c in CATALOG["chapters"]:
        if ch[c["id"]]["status"] in ("work", "skim"):
            for p in c["requires_all"]:
                assert ch[p]["status"] in ("work", "skim", "skip") or p in overrides, (c["id"], p)


@pytest.mark.parametrize("persona", VECTORS, ids=lambda p: p["id"])
def test_stages_are_contiguous_in_order(persona):
    result = run(persona["answers"])
    stages = [c["stage"] for c in result["chapters"] if c["stage"] is not None]
    assert stages == sorted(stages)
    assert [s["n"] for s in result["stages"]] == list(range(1, len(result["stages"]) + 1))
    for c in result["chapters"]:
        assert (c["stage"] is None) == (c["status"] in ("skip", "later"))


@pytest.mark.parametrize("persona", VECTORS, ids=lambda p: p["id"])
def test_stage_budget_and_totals(persona):
    result = run(persona["answers"])
    time = persona["answers"].get("time", CATALOG["placement"]["default_time"])
    budget = {t["id"]: t["stage_minutes"] for t in CATALOG["placement"]["times"]}[time]
    for s in result["stages"]:
        members = [c for c in result["chapters"] if c["stage"] == s["n"]]
        assert budget is None or s["minutes"] <= budget or len(members) == 1
    assert sum(s["minutes"] for s in result["stages"]) == result["totals"]["work_min"] + result["totals"]["skim_min"]


def test_skim_minutes_use_integer_ceiling():
    # 10 * 30 % must be 3, not ceil(3.0000000000000004) = 4
    assert placement._minutes({"minutes": 10}, "skim", 30) == 3
    assert placement._minutes({"minutes": 12}, "skim", 30) == 4
    assert placement._minutes({"minutes": 15}, "work", 30) == 15


def test_deterministic():
    answers = BY_ID["P08"]["answers"]
    assert json.dumps(run(answers), sort_keys=True) == json.dumps(run(copy.deepcopy(answers)), sort_keys=True)


def test_quickstart_long_warning_when_minimum_path_grows():
    cat = copy.deepcopy(CATALOG)
    cat["placement"]["quickstart_warn_minutes"] = 100
    result = placement.place(cat, {"time": "schnellstart"})
    assert result["warnings"] == [{"code": "quickstart-long", "ids": []}]


@pytest.mark.parametrize("answers", [
    {"goals": ["irgendwas"]},
    {"time": "nie"},
    {"areas": {"hooks": 3}},
    {"areas": {"unbekannt": 1}},
    {"scenarios": {"hook-crash": "z"}},
    {"scenarios": {"gibt-es-nicht": "a"}},
    {"overrides": {"S9.9": "skip"}},
    {"overrides": {"S2.8": "vielleicht"}},
])
def test_unknown_ids_raise(answers):
    with pytest.raises(ValueError):
        run(answers)


def test_more_than_two_goals_uses_the_first_two():
    assert run({"goals": ["team", "agents", "security"]}) == run({"goals": ["team", "agents"]})


def test_empty_answers_equal_defaults():
    assert run({}) == run({"goals": ["alltag"], "time": "abende"})


def test_golden_outputs():
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert set(golden) == {p["id"] for p in VECTORS}
    for p in VECTORS:
        assert run(p["answers"]) == golden[p["id"]], p["id"]


def test_cli_template_roundtrip(tmp_path):
    catalog = FIX / "placement-catalog.json"
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "placement.py"), "--catalog", str(catalog), "--template"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    answers = json.loads(out)
    assert answers["time"] == "abende" and answers["goals"] == ["alltag"]
    path = tmp_path / "einstufung.json"
    path.write_text(json.dumps(answers), encoding="utf-8")
    md = subprocess.run([sys.executable, str(ROOT / "tools" / "placement.py"), "--catalog", str(catalog),
                         "--answers", str(path), "--format", "md"],
                        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert md.startswith("# Dein Lernpfad") and "## Etappe 1" in md


def write_golden():  # maintainer helper: python -c "import tools.test_placement as t; t.write_golden()"
    golden = {p["id"]: run(p["answers"]) for p in VECTORS}
    GOLDEN_PATH.write_text(json.dumps(golden, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                           encoding="utf-8", newline="\n")


CHAPTER_GOAL_CASES = [
    ({"goals": ["security"]}, {"S3.13": True, "S4.4": True}),
    ({"goals": ["alltag"]}, {"S3.13": False, "S4.4": False}),
    ({"goals": ["alltag", "security"]}, {"S3.13": True, "S4.4": True}),
    ({"goals": ["security"], "time": "schnellstart"}, {"S3.13": False, "S4.4": False}),
    ({"goals": ["security", "moderieren"]}, None),
]


def test_chapter_goals_pull_safety_chapters_into_security_path():
    for answers, expect in CHAPTER_GOAL_CASES:
        ch = by_chapter(run(answers))
        if expect is None:  # moderieren: Zweig unverändert, kein Sicherheits-Zusatz durch chapter_goals
            assert run(answers) == run({"goals": ["moderieren"]})
            continue
        for cid, included in expect.items():
            assert (ch[cid]["status"] != "later") is included, (answers, cid)


def test_chapter_goals_security_schnellstart_unchanged():
    assert run({"goals": ["security"], "time": "schnellstart"}) == run({"goals": ["alltag"], "time": "schnellstart"})


def test_duplicate_goals_count_once():
    assert run({"goals": ["einschaetzen", "einschaetzen"]}) == run({"goals": ["einschaetzen"]})


def test_every_path_ends_with_the_small_build():
    """Design 2026-10-05: a core capstone belongs to every goal and to the quick start; the bonus one does not."""
    rules = CATALOG["placement"]
    for goal in [g["id"] for g in rules["goals"]]:
        for time in [t["id"] for t in rules["times"]]:
            result = run({"goals": [goal], "time": time})
            recommended = [c["id"] for c in result["chapters"] if c["status"] in ("work", "skim")]
            assert recommended[-1] == "S4.11", (goal, time)
            assert by_chapter(result)["S4.11"]["reason"] == "capstone"
    assert by_chapter(run({"goals": ["alltag"]}))["S4.8"]["status"] == "later"
    assert by_chapter(run({"goals": ["agents"]}))["S4.8"]["status"] == "work"
    assert run({"time": "schnellstart"})["warnings"] == []


def test_cli_markdown_links_use_link_base(tmp_path):
    cat = json.loads((FIX / "placement-catalog.json").read_text(encoding="utf-8"))
    for c in cat["chapters"]:
        c["file"] = c["id"].lower().replace(".", "-") + "-x.md"
        c["title"] = "Titel"
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps(cat), encoding="utf-8")
    path = tmp_path / "a.json"
    path.write_text(json.dumps({"time": "schnellstart"}), encoding="utf-8")
    base = [sys.executable, str(ROOT / "tools" / "placement.py"), "--catalog", str(catalog), "--answers", str(path),
            "--format", "md"]
    default = subprocess.run(base, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert "(https://github.com/dynamic-dome/dynamic-workshop/blob/main/resources/library/s0-1-x.md)" in default
    local = subprocess.run(base + ["--link-base", "C:/repo/resources/library/"], capture_output=True, text=True,
                           encoding="utf-8", check=True).stdout
    assert "(C:/repo/resources/library/s0-1-x.md)" in local and "https://github.com" not in local
