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


def stored_profile(overrides=None, goals=("alltag",)):
    """Init script: a saved placement for a newcomer (S2.7 and S2.8 'work', X.1 'skim'), plus own overrides."""
    answers = {"version": 1, "goals": list(goals), "time": "abende", "areas": {}, "scenarios": {},
               "overrides": overrides or {}}
    profile = {"v": 1, "at": "2026-10-01T08:00:00.000Z", "why": "", "answers": answers}
    return f"localStorage.setItem('ccWorkshopProfileV1', JSON.stringify({json.dumps(profile)}));"


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


def test_without_a_placement_a_chapter_opens_with_its_full_text_and_exercise(browser, site):
    """Answer 3 of round 1 (P9): the library is fully usable without a placement."""
    page, errors = open_page(browser, site + "?run=S2.8")  # nothing stored
    assert page.locator("main [data-full=open]").count() == 1
    assert page.locator("main details.full").count() == 0
    assert page.get_by_role("heading", name="Selbst machen").is_visible()
    assert page.locator(".meta .st-later").count() == 0  # no status without a placement
    assert errors == []
    page.close()


@pytest.mark.parametrize("status", ["skip", "later"])
def test_a_chapter_the_path_does_not_recommend_still_opens_in_full(browser, site, status):
    page, errors = open_page(browser, site + "?run=S2.8", init_script=stored_profile({"S2.8": status}))
    assert page.locator("main [data-full=open]").count() == 1
    assert page.locator("main details.full").count() == 0
    assert errors == []
    page.close()


def _done_button_position(page):
    return page.evaluate("""() => {
      const done = document.querySelectorAll('[data-action=toggle-done]');
      const text = document.querySelector('main [data-full=open], main details.full');
      return { count: done.length, inSide: !!done[0].closest('aside'),
               afterText: !!(text.compareDocumentPosition(done[0]) & Node.DOCUMENT_POSITION_FOLLOWING) };
    }""")


def test_only_a_skimmed_chapter_keeps_the_short_view_and_done_sits_at_its_end(browser, site):
    page, errors = open_page(browser, site + "?run=X.1", init_script=stored_profile())
    assert page.locator("main details.full").count() == 1
    assert page.locator("main details.full").get_attribute("open") is None
    assert page.locator("main [data-full=open]").count() == 0
    assert _done_button_position(page) == {"count": 1, "inSide": False, "afterText": True}
    assert errors == []
    page.close()


def test_done_sits_once_at_the_end_of_the_full_view(browser, site):
    page, _ = open_page(browser, site + "?run=S2.8")
    assert _done_button_position(page) == {"count": 1, "inSide": False, "afterText": True}
    page.close()


def test_marking_done_keeps_quiz_result_open_answer_and_scroll_position(browser, site):
    """B7: marking used to rebuild the page; the quiz result vanished and the page jumped."""
    page, errors = open_page(browser, site + "?run=S2.8")
    page.set_viewport_size({"width": 1280, "height": 420})
    page.click(".quiz [data-action=quiz][data-correct='1']")
    page.locator(".prose details summary").first.click()
    button = page.locator("[data-action=toggle-done]")
    button.scroll_into_view_if_needed()
    before = page.evaluate("window.scrollY")
    assert before > 0
    button.click()
    assert page.locator(".quiz .feedback").inner_text().startswith("Richtig")
    assert page.locator(".prose details").first.get_attribute("open") is not None
    assert abs(page.evaluate("window.scrollY") - before) <= 2
    assert button.inner_text() == "Als offen markieren" and button.get_attribute("aria-pressed") == "true"
    assert page.locator(".meta .st-done").count() == 1
    assert page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopUiState')).done['S2.8']") is True
    button.click()
    assert button.inner_text() == "Als erledigt markieren" and button.get_attribute("aria-pressed") == "false"
    assert page.locator(".meta .st-done").count() == 0
    assert errors == []
    page.close()


def test_jump_marks_lead_to_a_section_without_changing_the_address(browser, site):
    page, errors = open_page(browser, site + "?run=S2.8")
    page.set_viewport_size({"width": 1280, "height": 480})
    labels = page.locator("aside .toc [data-action=jump]").all_inner_texts()
    assert labels[:3] == ["Schnellcheck", "Auf einen Blick", "Bild im Kopf"] and "Selbst machen" in labels
    assert "Das ist kein Abschnitt" not in labels  # a heading inside a code block is no section
    page.click(".quiz [data-action=quiz][data-correct='1']")  # state a rebuilt page would lose
    url = page.url
    page.locator("aside .toc [data-action=jump]", has_text="Selbst machen").click()
    page.wait_for_function("""() => {
      const h = [...document.querySelectorAll('.prose h2')].find(e => e.textContent.trim() === 'Selbst machen');
      const top = h.getBoundingClientRect().top;
      const bar = document.querySelector('header.top').getBoundingClientRect().bottom;
      return top >= bar && top < bar + 120;
    }""")
    assert page.url == url
    assert page.locator(".quiz .feedback").inner_text().startswith("Richtig")
    assert errors == []
    page.close()


def test_a_skimmed_chapter_has_no_jump_marks(browser, site):
    page, _ = open_page(browser, site + "?run=X.1", init_script=stored_profile())
    assert page.locator(".toc").count() == 0
    page.close()


# --- recall questions with their answers (design 2026-10-05, package P3) ------------------------------------

def test_short_view_shows_the_recall_questions_and_reveals_an_answer_on_demand(browser, site):
    page, errors = open_page(browser, site + "?run=S2.8", init_script=stored_profile({"S2.8": "skim"}))
    questions = page.locator("main .recall > li")
    assert questions.count() == 2
    answer = questions.nth(0).locator("details.answer")
    assert answer.get_attribute("open") is None
    assert not answer.locator("p").is_visible()
    answer.locator("summary").click()
    assert "blockt nur" in answer.locator("p").inner_text()
    assert questions.nth(1).locator("details.answer").get_attribute("open") is None  # one at a time
    assert errors == []
    page.close()


def test_chapter_without_recall_questions_shows_no_empty_list(browser, site):
    page, errors = open_page(browser, site + "?run=S2.7", init_script=stored_profile({"S2.7": "skim"}))
    assert page.locator("main details.full").count() == 1  # short view
    assert page.locator("main .recall").count() == 0
    assert errors == []
    page.close()


# --- library and start for people who learn alone (P9b, P9c) ------------------------------------------------

def test_library_doors_show_id_and_title(browser, site):
    page, errors = open_page(browser, site + "?screen=bibliothek")
    door = page.locator(".door[data-chapter='S2.8']")
    assert door.locator(".door-id").inner_text() == "S2.8"
    assert door.locator(".door-title").is_visible()
    assert door.locator(".door-title").inner_text() == page.evaluate("CH['S2.8'].title")
    assert errors == []
    page.close()


def test_library_without_a_placement_shows_no_recommendation(browser, site):
    page, _ = open_page(browser, site + "?screen=bibliothek")
    assert page.locator(".door").count() == 4
    assert page.locator(".door.st-later, .door.st-work, .door.st-skim, .door.st-skip").count() == 0
    assert page.locator(".legend .st-work, .legend .st-later").count() == 0
    assert page.locator(".legend .st-done").count() == 1 and page.locator(".legend .safe").count() == 1
    page.close()
    placed, _ = open_page(browser, site + "?screen=bibliothek", init_script=stored_profile())
    assert placed.locator(".door.st-work[data-chapter='S2.8']").count() == 1
    assert placed.locator(".door.st-skim[data-chapter='X.1']").count() == 1
    assert placed.locator(".legend .st-work").count() == 1 and placed.locator(".legend .st-later").count() == 1
    placed.close()


def test_library_marks_done_chapters_with_or_without_a_placement(browser, site):
    done = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.7': true}, doneAt: {'S2.7': '2026-10-01T08:00:00.000Z'}}));"
    page, _ = open_page(browser, site + "?screen=bibliothek", init_script=done)
    assert page.locator(".door.is-done[data-chapter='S2.7']").count() == 1
    assert "erledigt" in page.locator(".door[data-chapter='S2.7']").inner_text()
    page.close()


def test_start_offers_two_ways_for_learners_and_keeps_the_live_path_apart(browser, site):
    page, errors = open_page(browser, site + "?screen=start")
    ways = page.locator(".start-grid .way")
    assert ways.count() == 2
    assert ways.nth(0).get_attribute("data-screen") == "einstufung"
    assert ways.nth(1).get_attribute("data-screen") == "bibliothek"
    live = page.locator("section.for-moderators [data-action=live-path]")
    assert live.count() == 1 and page.locator(".start-grid [data-action=live-path]").count() == 0
    assert "Für Moderierende" in page.locator("section.for-moderators").inner_text()
    live.click()
    page.wait_for_selector("text=Mein Pfad")
    assert page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopProfileV1')).answers.goals") == ["moderieren"]
    assert errors == []
    page.close()


def test_start_with_a_placement_leads_on_to_the_next_open_chapter(browser, site):
    """B10: after a saved placement the main button was still 'Einstufung starten'."""
    done = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.7': true}, doneAt: {'S2.7': '2026-10-01T08:00:00.000Z'}}));"
    page, errors = open_page(browser, site + "?screen=start", init_script=stored_profile() + done)
    main_button = page.locator(".start-grid .btn.primary")
    assert main_button.count() == 1
    assert main_button.inner_text().startswith("Weiter mit S2.8")  # S2.7 is done, S2.8 is next on the path
    assert page.locator(".start-grid .way").nth(0).get_attribute("data-chapter") == "S2.8"
    assert page.locator(".start-grid [data-screen=einstufung]").count() == 0
    assert page.locator("[data-screen=einstufung]", has_text="Einstufung ändern").count() == 1
    main_button.click()
    assert page.locator("main h1").inner_text().startswith("S2.8")
    assert errors == []
    page.close()


def test_start_with_a_finished_path_says_so(browser, site):
    all_done = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.7': true, 'S2.8': true, 'X.1': true, 'S2.20': true}, doneAt: {}}));"
    page, errors = open_page(browser, site + "?screen=start", init_script=stored_profile() + all_done)
    assert "Dein Pfad ist geschafft" in page.locator(".start-grid .way").nth(0).inner_text()
    assert errors == []
    page.close()


def test_start_does_not_say_the_same_chapter_twice(browser, site):
    same = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {}, doneAt: {}, lastId: 'S2.7'}));"
    page, _ = open_page(browser, site + "?screen=start", init_script=stored_profile() + same)
    assert page.locator(".start-grid .btn.primary").inner_text().startswith("Weiter mit S2.7")
    assert page.locator(".resume").count() == 0
    page.close()
    other = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {}, doneAt: {}, lastId: 'X.1'}));"
    page, _ = open_page(browser, site + "?screen=start", init_script=stored_profile() + other)
    assert "X.1" in page.locator(".resume").inner_text()
    page.close()


# --- the real cockpit (generated file in the repo): behaviour that needs the real library ----------------------

@pytest.fixture(scope="module")
def real_site():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "resources"))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}/claude-code-workshop-ui.html"
    server.shutdown()


def test_a_third_goal_is_refused_visibly(browser, real_site):
    """B2: the third goal could not be ticked, without any hint why."""
    page, errors = open_page(browser, real_site + "?screen=einstufung")
    boxes = page.locator("input[name=goal]")
    assert boxes.count() >= 3
    assert not page.locator(".goal-hint").is_visible()
    boxes.nth(0).check()
    boxes.nth(1).check()
    assert page.locator(".goal-hint").is_visible()
    assert boxes.nth(2).is_disabled() and boxes.nth(0).is_enabled()
    page.click("[data-action=step-next]")
    page.click("[data-action=step-back]")  # the step is drawn again from the draft
    assert boxes.nth(2).is_disabled() and page.locator(".goal-hint").is_visible()
    boxes.nth(0).uncheck()
    assert boxes.nth(2).is_enabled() and not page.locator(".goal-hint").is_visible()
    assert errors == []
    page.close()


def test_a_new_placement_step_starts_at_its_top(browser, real_site):
    """B1: the next step opened at the scroll position of the previous one, its heading under the sticky header."""
    page, errors = open_page(browser, real_site + "?screen=einstufung")
    page.set_viewport_size({"width": 1280, "height": 500})
    page.click("[data-action=step-next]")
    page.click("[data-action=step-next]")  # step 3 of 4: the long list of areas
    page.locator("[data-action=step-next]").scroll_into_view_if_needed()
    assert page.evaluate("window.scrollY") > 200
    page.click("[data-action=step-next]")
    assert page.evaluate("window.scrollY") == 0
    page.locator("[data-action=step-back]").scroll_into_view_if_needed()
    page.click("[data-action=step-back]")
    assert page.evaluate("window.scrollY") == 0
    assert errors == []
    page.close()


def test_a_wide_diagram_uses_the_column_and_can_be_enlarged(browser, real_site):
    """B6: diagrams were boxed into the reading width (S2.8: 1404 px wide, less than half visible)."""
    page, errors = open_page(browser, real_site + "?run=S2.8")
    box = page.locator(".prose .diagram").first
    text_width = page.locator(".prose > p").first.evaluate("e => e.getBoundingClientRect().width")
    column = page.locator(".chapter-main").evaluate("e => e.getBoundingClientRect().width")
    width = box.evaluate("e => e.getBoundingClientRect().width")
    assert width > text_width + 50 and width <= column + 1
    zoom = box.locator("[data-action=zoom]")
    assert zoom.is_visible()
    zoom.click()
    dialog = page.locator("dialog.zoom-dialog")
    assert dialog.evaluate("d => d.open") is True and dialog.locator("svg").count() == 1
    page.keyboard.press("Escape")
    assert dialog.evaluate("d => d.open") is False and dialog.locator("svg").count() == 0
    assert page.locator("main h1").inner_text().startswith("S2.8")  # still the same page
    assert errors == []
    page.close()


def test_copy_button_does_not_cover_the_code(browser, real_site):
    """B11: the button sat on the end of the first line of code."""
    page, _ = open_page(browser, real_site + "?run=S1.5", init_script=stored_profile({"S1.5": "skim"}))
    button = page.locator(".code [data-action=copy]").bounding_box()
    pre = page.locator(".code pre").bounding_box()
    assert button["y"] + button["height"] <= pre["y"] + 1
    page.close()


def test_a_wrong_quiz_answer_says_where_to_look(browser, site):
    """B8: a wrong answer always points to where the chapter explains it (with or without a reason per option)."""
    page, _ = open_page(browser, site + "?run=S2.8")
    page.locator(".quiz [data-action=quiz][data-correct='0']").first.click()
    feedback = page.locator(".quiz .feedback").inner_text()
    assert feedback.startswith("Nicht ganz") and "Auflösung" in feedback and "Im Detail" in feedback
    page.close()



# --- P10b: after an answer the cockpit shows the reason of the chosen option, and only that one -------------

WHY_RIGHT = "Nur Exit-Code 2 gilt als blockierender Fehler"
WHY_ONE = "Exit-Code 1 ist ein Fehler, der nicht blockt"
WHY_OTHERS = ("Ein anderer Code ungleich null", "Ein Timeout blockt nicht")


def _answer(page, text):
    page.locator(".quiz [data-action=quiz]", has_text=text).first.click()
    return page.locator(".quiz .feedback").inner_text()


def test_a_right_answer_says_why(browser, site):
    page, errors = open_page(browser, site + "?run=S2.8")
    feedback = _answer(page, "Exit-Code 2 blockt den Aufruf")
    assert feedback.startswith("Richtig.") and WHY_RIGHT in feedback
    assert page.locator(".quiz .feedback code", has_text="exit 2").count() == 1  # code span, not escaped markup
    assert errors == []
    page.close()


def test_a_wrong_answer_says_why_this_one_and_where_to_look(browser, site):
    page, errors = open_page(browser, site + "?run=S2.8")
    feedback = _answer(page, "Exit-Code 1 blockt den Aufruf")
    assert feedback.startswith("Nicht ganz.") and WHY_ONE in feedback
    assert "Auflösung" in feedback and "versuch es noch einmal" in feedback
    assert WHY_RIGHT not in feedback and not any(w in feedback for w in WHY_OTHERS)  # the others stay hidden
    assert page.locator(".quiz [data-action=quiz]", has_text="Exit-Code 2 blockt").get_attribute("class") in (None, "")
    feedback = _answer(page, "Exit-Code 2 blockt den Aufruf")  # trying again still works
    assert feedback.startswith("Richtig.") and WHY_ONE not in feedback
    assert errors == []
    page.close()


def test_a_quiz_without_reasons_answers_as_before(browser, site):
    page, errors = open_page(browser, site + "?run=S2.7")
    assert _answer(page, "Bevor ein Werkzeug ausgeführt wird") == "Richtig."
    feedback = _answer(page, "Nachdem ein Werkzeug gelaufen ist")
    assert feedback.startswith("Nicht ganz. Lies") and feedback.endswith("dann versuch es noch einmal.")
    assert errors == []
    page.close()

def _done_script(days_ago):
    return ("localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.8': true}, doneAt: {'S2.8': "
            f"new Date(Date.now() - {days_ago} * 86400000).toISOString()}}}}));")


def test_review_waits_a_day_before_it_asks(browser, site):
    """B9: a chapter marked a minute ago was asked at once, under the heading 'Abrufen mit Abstand'."""
    page, errors = open_page(browser, site + "?screen=wiederholen", init_script=_done_script(0))
    assert page.locator(".review-q").count() == 0
    assert "Noch nichts fällig" in page.locator("main").inner_text()
    assert errors == []
    page.close()


def test_review_shows_the_reason_too(browser, site):
    page, errors = open_page(browser, site + "?screen=wiederholen", init_script=_done_script(2))
    feedback = _answer(page, "Exit-Code 1 blockt den Aufruf")
    assert feedback.startswith("Nicht ganz.") and WHY_ONE in feedback and "verlinkt" in feedback
    assert errors == []
    page.close()


def test_review_asks_what_is_due_and_counts_honestly(browser, site):
    page, errors = open_page(browser, site + "?screen=wiederholen", init_script=_done_script(2))
    assert page.locator(".review-q").count() == 1
    lead = page.locator("main .lead").inner_text()
    assert lead.startswith("Eine Frage") and "Fünf" not in lead
    assert errors == []
    page.close()


# --- taking progress along, phone width (P9g) ----------------------------------------------------------------

DONE_S27 = "localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.7': true}, doneAt: {'S2.7': '2026-10-01T08:00:00.000Z'}}));"


def _export(page, tmp_path):
    with page.expect_download() as download:
        page.click("[data-action=export]")
    target = tmp_path / "export.json"
    download.value.save_as(str(target))
    return target


def test_export_and_import_carry_progress_and_placement_to_another_browser(browser, site, tmp_path):
    source, errors = open_page(browser, site + "?screen=start", init_script=stored_profile() + DONE_S27)
    exported = _export(source, tmp_path)
    data = json.loads(exported.read_text(encoding="utf-8"))
    assert data["app"] == "cc-workshop-cockpit" and data["v"] == 1
    assert data["progress"]["done"] == {"S2.7": True} and data["profile"]["answers"]["goals"] == ["alltag"]
    assert errors == []
    source.close()

    context = browser.new_context(viewport={"width": 1280, "height": 900})  # another browser: empty storage
    target = context.new_page()
    target.goto(site + "?screen=start")
    assert target.locator(".start-grid [data-screen=einstufung]").count() == 1
    target.set_input_files("input[data-action=import]", str(exported))
    target.wait_for_selector(".start-grid [data-chapter='S2.8']")  # the page now leads on along the imported path
    assert "1 erledigtes Kapitel" in target.locator("#carryFeedback").inner_text()
    assert target.evaluate("JSON.parse(localStorage.getItem('ccWorkshopUiState')).done") == {"S2.7": True}
    assert target.evaluate("JSON.parse(localStorage.getItem('ccWorkshopProfileV1')).answers.goals") == ["alltag"]
    context.close()


def test_import_adds_to_what_is_there_and_never_takes_progress_away(browser, site, tmp_path):
    source, _ = open_page(browser, site + "?screen=start", init_script=DONE_S27)
    exported = _export(source, tmp_path)
    source.close()
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    page.goto(site + "?screen=start")
    page.evaluate("localStorage.setItem('ccWorkshopUiState', JSON.stringify({done: {'S2.8': true}, doneAt: {'S2.8': '2026-10-02T08:00:00.000Z'}}))")
    page.reload()
    page.set_input_files("input[data-action=import]", str(exported))
    page.wait_for_function("document.querySelector('#carryFeedback').textContent.includes('Importiert')")
    assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ccWorkshopUiState')).done).sort()") == ["S2.7", "S2.8"]
    context.close()


@pytest.mark.parametrize("content", [
    "this is not json",
    '{"foo": 1}',
    '{"app": "cc-workshop-cockpit", "v": 1, "progress": {"done": {"S9.99": true, "S2.7": true}, "doneAt": {}}, "profile": {"answers": {"version": 1, "goals": ["gibt-es-nicht"]}}}',
], ids=["garbage", "foreign", "unknown-ids"])
def test_import_refuses_what_it_cannot_read_and_keeps_only_what_it_knows(browser, site, tmp_path, content):
    path = tmp_path / "import.json"
    path.write_text(content, encoding="utf-8")
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(site + "?screen=start")
    page.set_input_files("input[data-action=import]", str(path))
    page.wait_for_function("document.querySelector('#carryFeedback').textContent.trim() !== ''")
    feedback = page.locator("#carryFeedback").inner_text()
    stored = page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopUiState') || '{}').done || {}")
    profile = page.evaluate("localStorage.getItem('ccWorkshopProfileV1')")
    if "S9.99" in content:
        assert stored == {"S2.7": True}  # the unknown chapter is dropped, the known one kept
        assert profile is None and "Einstufung" in feedback  # a placement the engine rejects is not taken over
    else:
        assert "keine Export-Datei" in feedback and stored == {} and profile is None
    assert errors == []
    context.close()


def test_phone_width_every_screen_fits_and_the_navigation_is_reachable(browser, real_site):
    page, errors = open_page(browser, real_site + "?screen=start", width=390, init_script=stored_profile())
    for query in ("?screen=start", "?screen=einstufung", "?screen=pfad", "?screen=bibliothek", "?screen=wiederholen",
                  "?run=S1.5", "?run=S2.8", "?run=S4.8"):
        page.goto(real_site + query)
        assert page.evaluate("document.documentElement.scrollWidth") <= 390, query
    rights = page.locator(".nav button").evaluate_all("els => els.map(e => e.getBoundingClientRect().right)")
    assert len(rights) == 5 and max(rights) <= 390  # no item hidden beyond the edge
    assert errors == []
    page.close()


def test_phone_width_has_jump_marks_above_the_text_and_marking_works(browser, real_site):
    page, errors = open_page(browser, real_site + "?run=S1.5", width=390)
    assert not page.locator("aside .toc").is_visible()
    inline = page.locator("details.toc-inline")
    assert inline.is_visible()
    in_front = page.evaluate("""() => {
      const toc = document.querySelector('details.toc-inline'), text = document.querySelector('main [data-full=open]');
      return !!(toc.compareDocumentPosition(text) & Node.DOCUMENT_POSITION_FOLLOWING);
    }""")
    assert in_front is True
    inline.locator("summary").click()
    inline.locator("[data-action=jump]", has_text="Selbst machen").click()
    page.wait_for_function("""() => {
      const h = [...document.querySelectorAll('.prose h2')].find(e => e.textContent.trim() === 'Selbst machen');
      const top = h.getBoundingClientRect().top;
      return top >= 0 && top < 260;
    }""")
    page.locator("[data-action=toggle-done]").click()
    assert page.locator("[data-action=toggle-done]").inner_text() == "Als offen markieren"
    assert errors == []
    page.close()


def test_wide_screens_show_the_jump_marks_only_in_the_side_column(browser, site):
    page, _ = open_page(browser, site + "?run=S2.8")
    assert page.locator("aside .toc").is_visible() and not page.locator("details.toc-inline").is_visible()
    page.close()


def test_a_chapter_id_that_names_an_object_property_is_no_chapter(browser, site, tmp_path):
    """Lookups by id must not find 'constructor' or '__proto__' on the lookup table itself."""
    page, errors = open_page(browser, site + "?run=constructor")
    assert page.locator("main h1").inner_text().startswith("Lerne Claude Code")  # unknown id: the start page
    assert errors == []
    path = tmp_path / "import.json"
    path.write_text('{"app": "cc-workshop-cockpit", "v": 1, "progress": {"done": {"constructor": true, "__proto__": true, "S2.7": true}, "doneAt": {}}}', encoding="utf-8")
    page.goto(site + "?screen=start")
    page.set_input_files("input[data-action=import]", str(path))
    page.wait_for_function("document.querySelector('#carryFeedback').textContent.includes('Importiert')")
    assert "1 erledigtes Kapitel" in page.locator("#carryFeedback").inner_text()
    assert page.evaluate("Object.keys(JSON.parse(localStorage.getItem('ccWorkshopUiState')).done)") == ["S2.7"]
    assert errors == []
    page.close()


def test_an_imported_placement_is_stored_the_way_the_wizard_would_store_it(browser, real_site, tmp_path):
    """Codex finding on P9: the engine cuts to two goals for its computation, but the import stored all three."""
    path = tmp_path / "import.json"
    path.write_text(json.dumps({"app": "cc-workshop-cockpit", "v": 1, "progress": {"done": {}, "doneAt": {}},
                                "profile": {"why": "x", "answers": {"goals": ["alltag", "security", "agents"],
                                                                    "junk": {"a": 1}}}}), encoding="utf-8")
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    page.goto(real_site + "?screen=start")
    page.set_input_files("input[data-action=import]", str(path))
    page.wait_for_function("document.querySelector('#carryFeedback').textContent.includes('Importiert')")
    answers = page.evaluate("JSON.parse(localStorage.getItem('ccWorkshopProfileV1')).answers")
    assert answers["goals"] == ["alltag", "security"] and "junk" not in answers
    assert sorted(answers) == ["areas", "goals", "overrides", "scenarios", "time", "version"]
    page.goto(real_site + "?screen=einstufung")
    assert page.locator("input[name=goal]:checked").count() == 2
    context.close()


@pytest.mark.parametrize("stored", [None, "light"])
def test_printing_is_light_and_the_stored_theme_comes_back(browser, site, stored):
    init = f"localStorage.setItem('ccWorkshopTheme', JSON.stringify({{theme: '{stored}'}}));" if stored else None
    page, errors = open_page(browser, site + "?run=S2.8", init_script=init)
    theme = "document.documentElement.dataset.theme ?? null"
    assert page.evaluate(theme) == stored
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    page.emulate_media(media="print")
    assert page.evaluate(theme) == "light"
    # light code boxes: with the dark theme kept, code would print as black boxes
    rgb = page.locator("main code").first.evaluate("el => getComputedStyle(el).backgroundColor")
    assert min(int(v) for v in rgb[rgb.index("(") + 1:rgb.rindex(")")].split(",")[:3]) >= 230, rgb
    assert page.locator("main h1").is_visible()
    assert not page.locator(".nav").is_visible() and not page.locator("[data-action=toggle-done]").is_visible()
    page.emulate_media(media="screen")
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.evaluate(theme) == stored
    assert errors == []
    page.close()
