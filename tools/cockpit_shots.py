"""Screenshots of every cockpit view for a visual check (Playwright, Chromium).

usage: python tools/cockpit_shots.py <url of the cockpit> <output folder> [view names...]
example: python -m http.server 8765 --bind 127.0.0.1   (in the repo root, another terminal)
         python tools/cockpit_shots.py http://127.0.0.1:8765/resources/claude-code-workshop-ui.html out/shots

Views come in three states: fresh (nothing stored), placed (a saved placement and three finished chapters) and
mobile (390 px). The script prints script errors and horizontal overflow per view; both should be empty / 0.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = {"v": 1, "at": "2026-10-01T08:00:00.000Z", "why": "Reviews im Team beschleunigen",
           "answers": {"version": 1, "goals": ["alltag"], "time": "abende", "areas": {}, "scenarios": {}, "overrides": {}}}
PROGRESS = {"done": {"S0.1": True, "S1.1": True, "S1.2": True}, "lastId": "S1.3",
            "doneAt": {"S0.1": "2026-09-28T08:00:00.000Z", "S1.1": "2026-09-29T08:00:00.000Z", "S1.2": "2026-10-01T08:00:00.000Z"}}
PLACED = (f"localStorage.setItem('ccWorkshopProfileV1', JSON.stringify({json.dumps(PROFILE)}));"
          f"localStorage.setItem('ccWorkshopUiState', JSON.stringify({json.dumps(PROGRESS)}));")

# name, query, init script, width, action after loading
SHOTS = [
    ("fresh-start", "?screen=start", None, 1280, None),
    ("fresh-bibliothek", "?screen=bibliothek", None, 1280, None),
    ("fresh-kapitel", "?run=S1.5", None, 1280, None),
    ("fresh-kapitel-sprung", "?run=S1.5", None, 1280, "jump"),
    ("fresh-kapitel-ende", "?run=S1.5", None, 1280, "end"),
    ("fresh-pfad", "?screen=pfad", None, 1280, None),
    ("fresh-wiederholen", "?screen=wiederholen", None, 1280, None),
    ("fresh-einstufung", "?screen=einstufung", None, 1280, None),
    ("placed-start", "?screen=start", PLACED, 1280, None),
    ("placed-pfad", "?screen=pfad", PLACED, 1280, None),
    ("placed-bibliothek", "?screen=bibliothek", PLACED, 1280, None),
    ("placed-wiederholen", "?screen=wiederholen", PLACED, 1280, None),
    ("placed-kapitel-skim", "?run=X.2", PLACED, 1280, None),
    ("diagram-kapitel", "?run=S2.8", None, 1280, "diagram"),
    ("diagram-gross", "?run=S2.8", None, 1280, "zoom"),
    ("mobile-start", "?screen=start", PLACED, 390, None),
    ("mobile-bibliothek", "?screen=bibliothek", None, 390, None),
    ("mobile-kapitel", "?run=S1.5", None, 390, None),
    ("mobile-pfad", "?screen=pfad", PLACED, 390, None),
]


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    url, out, only = argv[1], Path(argv[2]), set(argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, query, init, width, action in SHOTS:
            if only and name not in only:
                continue
            page = browser.new_page(viewport={"width": width, "height": 800})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            if init:
                page.add_init_script(init)
            page.goto(url + query)
            if action == "jump":
                page.locator("aside .toc [data-action=jump]", has_text="Selbst machen").click()
            elif action == "end":
                page.locator("[data-action=toggle-done]").scroll_into_view_if_needed()
            elif action == "diagram":
                page.locator(".diagram").first.scroll_into_view_if_needed()
            elif action == "zoom":
                page.locator(".diagram [data-action=zoom]").first.click()
            page.wait_for_timeout(150)
            page.screenshot(path=str(out / f"{name}.jpg"), type="jpeg", quality=80)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(f"{name}: errors={errors} overflow={overflow}")
            page.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
