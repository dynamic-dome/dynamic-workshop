"""Checks on the real placement data (resources/library/_shelves.yaml, _placement.yaml)."""
from pathlib import Path
import statistics

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "resources" / "library"
SHELVES = yaml.safe_load((LIB / "_shelves.yaml").read_text(encoding="utf-8"))
RULES = yaml.safe_load((LIB / "_placement.yaml").read_text(encoding="utf-8"))

SPEC_SHELVES = ["start", "permissions", "context", "prompting", "git", "cost", "skills", "hooks", "plugins",
                "mcp-knowledge", "agents", "security", "automation", "headless-ci", "remote-isolation",
                "troubleshooting", "capstone", "practice", "community"]
# Codes the engine (tools/placement.py) may emit.
REASON_CODES = {"new", "heard", "deep-focus", "known", "scenario-gap", "safety-floor", "prerequisite", "not-goal",
                "after-quickstart", "practice", "capstone", "community", "assess", "override"}
WARNING_CODES = {"override-safety", "override-prereq", "quickstart-long"}


def test_shelves_match_spec_order():
    assert [s["id"] for s in SHELVES] == SPEC_SHELVES
    for shelf in SHELVES:
        assert shelf["title"] and shelf["purpose"] and len(shelf["intro"]) > 80


def test_fourteen_areas_one_area_per_chapter():
    assert len(RULES["areas"]) == 14
    seen = [c for a in RULES["areas"] for c in a["chapters"]]
    assert len(seen) == len(set(seen))


def test_goals_times_and_defaults():
    goals = {g["id"] for g in RULES["goals"]}
    assert goals == {"alltag", "team", "automation", "agents", "security", "einschaetzen", "moderieren"}
    times = {t["id"]: t["stage_minutes"] for t in RULES["times"]}
    assert times == {"schnellstart": None, "stunde": 60, "abende": 150, "gruendlich": 180}
    assert RULES["default_goal"] == "alltag" and RULES["default_time"] == "abende"
    shelves = {s["id"] for s in SHELVES}
    for goal in RULES["goals"]:
        assert set(goal["focus_shelves"]) <= shelves


@pytest.mark.parametrize("scenario", RULES["scenarios"], ids=lambda s: s["id"])
def test_scenario_shape_and_fair_lengths(scenario):
    options = scenario["options"]
    assert len(options) == 4
    assert scenario["correct"] in {o["id"] for o in options}
    lengths = [len(o["text"]) for o in options]
    mean = statistics.mean(lengths)
    assert all(abs(n - mean) <= 0.15 * mean for n in lengths), lengths
    areas = {a["id"] for a in RULES["areas"]}
    assert scenario["area"] in areas
    assert scenario["explanation"].strip()


def test_correct_option_is_rarely_the_longest():
    longest = 0
    for sc in RULES["scenarios"]:
        lengths = {o["id"]: len(o["text"]) for o in sc["options"]}
        if lengths[sc["correct"]] == max(lengths.values()):
            longest += 1
    assert longest <= 2, f"richtige Antwort ist in {longest} von 6 Szenarien die laengste"


def test_six_scenarios_in_distinct_areas():
    assert len(RULES["scenarios"]) == 6
    assert len({s["area"] for s in RULES["scenarios"]}) == 6


def test_reason_and_warning_texts_exist():
    assert set(RULES["reasons"]) == REASON_CODES
    assert set(RULES["warnings"]) == WARNING_CODES
