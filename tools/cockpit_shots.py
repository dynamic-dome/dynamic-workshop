"""Screenshots of every cockpit view for a visual check (Playwright, Chromium).

usage: python tools/cockpit_shots.py [--theme light] [--print] <url of the cockpit> <output folder> [view names...]
example: python -m http.server 8765 --bind 127.0.0.1   (in the repo root, another terminal)
         python tools/cockpit_shots.py http://127.0.0.1:8765/resources/claude-code-workshop-ui.html out/shots
         python tools/cockpit_shots.py --theme light --print http://127.0.0.1:8765/resources/claude-code-workshop-ui.html out/shots fresh-kapitel

Views come in three states: fresh (nothing stored), placed (a saved placement and three finished chapters) and
mobile (390 px). `--theme light` stores the light theme the way the Hell/Dunkel button does; `--print` renders
what Ctrl+P would (print media). Both add a suffix to the file names. The script prints script errors and
horizontal overflow per view; both should be empty / 0.
"""
import argparse
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
LIGHT = "localStorage.setItem('ccWorkshopTheme', JSON.stringify({theme: 'light'}));"

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
    ("diagram-notiz", "?run=S1.10", None, 1280, "diagram"),
    ("mobile-start", "?screen=start", PLACED, 390, None),
    ("mobile-bibliothek", "?screen=bibliothek", None, 390, None),
    ("mobile-kapitel", "?run=S1.5", None, 390, None),
    ("mobile-pfad", "?screen=pfad", PLACED, 390, None),
]


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url")
    parser.add_argument("out", type=Path)
    parser.add_argument("views", nargs="*", help="only these views (default: all)")
    parser.add_argument("--theme", choices=("dark", "light"), default="dark",
                        help="theme to store before loading (default: dark, nothing stored)")
    parser.add_argument("--print", dest="print_media", action="store_true", help="emulate print media")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    only = set(args.views)
    suffix = ("-light" if args.theme == "light" else "") + ("-print" if args.print_media else "")
    args.out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, query, init, width, action in SHOTS:
            if only and name not in only:
                continue
            page = browser.new_page(viewport={"width": width, "height": 800})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            if args.theme == "light":
                page.add_init_script(LIGHT)
            if init:
                page.add_init_script(init)
            if args.print_media:
                page.emulate_media(media="print")
            page.goto(args.url + query)
            if args.print_media:
                page.evaluate("window.dispatchEvent(new Event('beforeprint'))")  # what opening the print dialog does
            if action == "jump":
                page.locator("aside .toc [data-action=jump]", has_text="Selbst machen").click()
            elif action == "end":
                page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")  # the done button is hidden in print
            elif action == "diagram":
                page.locator(".diagram").first.scroll_into_view_if_needed()
            elif action == "zoom":
                page.locator(".diagram [data-action=zoom]").first.click()
            page.wait_for_timeout(150)
            page.screenshot(path=str(args.out / f"{name}{suffix}.jpg"), type="jpeg", quality=80)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(f"{name}{suffix}: errors={errors} overflow={overflow}")
            page.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
