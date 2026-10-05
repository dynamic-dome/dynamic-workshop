"""Behaviour of the generated cockpit in a real browser (Playwright, local server on 127.0.0.1).

Replaces the old wording tests of tools/test_workshop_ui_behavior.py (spec section 8.1). Built from the fixture library,
so it runs independently of the migration state. Skipped with a reason when Playwright or its Chromium is missing.
"""
from pathlib import Path
import functools
import http.server
import importlib.util
import json
import shutil
import socket
import sys
import threading

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tools" / "fixtures" / "library"

playwright = pytest.importorskip("playwright.sync_api", reason="Playwright nicht installiert")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    bl = _load("build_library")
    base = tmp_path_factory.mktemp("cockpit")
    shutil.copytree(FIXTURES, base / "library")
    assert bl.build(base / "library", write=True) == 0
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(base))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}/claude-code-workshop-ui.html"
    server.shutdown()


@pytest.fixture(scope="module")
def browser():
    with playwright.sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as err:  # pragma: no cover - browser binaries missing
            pytest.skip(f"Chromium für Playwright fehlt: {err}")
        yield b
        b.close()


def open_page(browser, url, width=1280, init_script=None):
    page = browser.new_page(viewport={"width": width, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    if init_script:
        page.add_init_script(init_script)
    page.goto(url)
    return page, errors


def test_every_screen_renders_without_errors(browser, site):
    page, errors = open_page(browser, site)
    for q in ("?screen=start", "?screen=einstufung", "?screen=pfad", "?screen=bibliothek", "?screen=wiederholen",
              "?run=S2.8", "?run=X.1", "?run=S2.20"):
        page.goto(site + q)
        assert page.locator("main h1").count() == 1, q
    assert errors == []
    page.close()


def test_placement_wizard_produces_the_engine_path(browser, site):
    page, errors = open_page(browser, site + "?screen=einstufung")
    page.check("input[name=goal][value=alltag]")
    page.click("[data-action=step-next]")
    page.check("input[name=time][value=abende]")
    page.click("[data-action=step-next]")
    page.click("[data-action=step-next]")
    page.click("[data-action=finish] >> nth=0")
    page.wait_for_selector("text=Mein Pfad")
    titles = page.locator(".stage .rows li .title a").all_inner_texts()
    assert [t.split(" ·")[0] for t in titles] == ["S2.7", "S2.8", "X.1", "S2.20"]
    profile = page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopProfileV1'))")
    assert profile["answers"]["goals"] == ["alltag"] and profile["answers"]["time"] == "abende"
    assert errors == []
    page.close()


def test_quiz_gives_feedback_but_does_not_book_done(browser, site):
    page, _ = open_page(browser, site + "?run=S2.8")
    page.click(".quiz [data-action=quiz][data-correct='1']")
    assert page.locator(".quiz .feedback").inner_text().startswith("Richtig")
    progress = page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopUiState') || '{}')")
    assert not progress.get("done", {}).get("S2.8")
    page.click("[data-action=toggle-done]")
    progress = page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopUiState'))")
    assert progress["done"]["S2.8"] is True
    page.close()


def test_resume_where_you_left(browser, site):
    page, _ = open_page(browser, site + "?run=S2.7")
    page.goto(site + "?screen=start")
    assert "S2.7" in page.locator(".resume").inner_text()
    page.close()


def test_blocked_storage_still_renders(browser, site):
    blocked = """
      Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } });
    """
    page, errors = open_page(browser, site + "?run=S2.8", init_script=blocked)
    assert page.locator("main h1").inner_text().startswith("S2.8")
    page.click("[data-action=toggle-done]")
    assert page.locator("#storageNotice").is_visible()
    assert [e for e in errors if "blocked" not in e] == []
    page.close()


def test_corrupt_storage_still_renders(browser, site):
    corrupt = "localStorage.setItem('ccWorkshopUiState', 'null'); localStorage.setItem('ccWorkshopProfileV1', '[1,2');"
    page, errors = open_page(browser, site, init_script=corrupt)
    assert page.locator("main h1").count() == 1
    assert errors == []
    page.close()


def test_old_deep_links_still_open_the_chapter(browser, site):
    page, _ = open_page(browser, site + "?view=65&run=S2.8")
    assert page.locator("main h1").inner_text().startswith("S2.8")
    page.goto(site + "?section=S2.7")
    assert page.locator("main h1").inner_text().startswith("S2.7")
    page.close()


def test_mobile_has_no_horizontal_scroll(browser, site):
    page, _ = open_page(browser, site + "?screen=bibliothek", width=390)
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    page.goto(site + "?run=S2.8")
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    page.close()


def test_arrow_keys_page_through_chapters_without_modifiers_only(browser, site):
    page, _ = open_page(browser, site + "?run=S2.7")
    page.locator("main").click(position={"x": 5, "y": 5})
    page.keyboard.press("Alt+ArrowRight")
    assert page.locator("main h1").inner_text().startswith("S2.7")
    page.keyboard.press("ArrowRight")
    assert page.locator("main h1").inner_text().startswith("S2.8")
    page.close()


def test_chapter_html_links_stay_inside_the_cockpit(browser, site):
    page, _ = open_page(browser, site + "?run=S2.8")
    page.click("details.full summary")
    link = page.locator(".prose a[data-chapter='S2.7']").first
    link.click()
    assert page.locator("main h1").inner_text().startswith("S2.7")
    page.close()


# --- "durcharbeiten" shows the teaching text and the exercise (design 2026-10-05, package P2) ----------------

def _newcomer_path_for_alltag(page):
    """The wizard for a newcomer with goal 'alltag': S2.7 and S2.8 become 'work', the community chapter X.1 'skim'."""
    page.check("input[name=goal][value=alltag]")
    page.click("[data-action=step-next]")
    page.check("input[name=time][value=abende]")
    page.click("[data-action=step-next]")
    page.click("[data-action=step-next]")
    page.click("[data-action=finish] >> nth=0")
    page.wait_for_selector("text=Mein Pfad")


def test_a_chapter_to_work_through_opens_with_its_full_text_and_exercise(browser, site):
    page, errors = open_page(browser, site + "?screen=einstufung")
    _newcomer_path_for_alltag(page)
    page.goto(site + "?run=S2.8")
    assert page.locator("main [data-full=open]").count() == 1
    assert page.locator("main details.full").count() == 0
    assert page.get_by_role("heading", name="Selbst machen").is_visible()
    # the quiz stays usable, and "done" sits once, below the text
    page.click(".quiz [data-action=quiz][data-correct='1']")
    assert page.locator(".quiz .feedback").inner_text().startswith("Richtig")
    assert page.locator("[data-action=toggle-done]").count() == 1
    done_follows_text = page.evaluate("""() => {
      const text = document.querySelector('main [data-full=open]');
      const done = document.querySelector('[data-action=toggle-done]');
      return !!(text.compareDocumentPosition(done) & Node.DOCUMENT_POSITION_FOLLOWING);
    }""")
    assert done_follows_text is True
    assert errors == []
    page.close()


def test_skimmed_and_unplaced_chapters_keep_the_short_view(browser, site):
    page, errors = open_page(browser, site + "?screen=einstufung")
    _newcomer_path_for_alltag(page)
    page.goto(site + "?run=X.1")
    assert page.locator("main details.full").count() == 1
    assert page.locator("main details.full").get_attribute("open") is None
    assert page.locator("main [data-full=open]").count() == 0
    assert errors == []
    page.close()
    fresh, fresh_errors = open_page(browser, site + "?run=S2.8")  # nothing stored: no placement
    assert fresh.locator("main details.full").count() == 1
    assert fresh.locator("main details.full").get_attribute("open") is None
    assert fresh.locator("main [data-full=open]").count() == 0
    assert fresh_errors == []
    fresh.close()
