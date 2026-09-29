"""Currency check flow (design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md). Offline, fixed dates."""
import datetime as dt
import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cc = _load("currency_check")
TODAY = dt.date(2026, 9, 29)
BASE = "https://docs.test/"
PAD = "\n" + "lorem ipsum " * 500
DOCS = ["cli-reference.md", "env-vars.md", "model-deprecations.md", "model-config.md", "permission-modes.md"]
OPUS = ("Claude Opus 5.5", "claude-opus-5-5", "opus", "Opus", "Active", "Not sooner than September 22, 2027")


def canon(checked="2026-09-29", cli="2.1.284", rows=(OPUS,), docs=DOCS):
    table = "\n".join(f"| {n} | `{i}` | `{a}` | {t} | {s} | {r} | 1M | 4 | 20 | Rolle |" for n, i, a, t, s, r in rows)
    listed = "\n".join(f"- Doku: {BASE}{d}" for d in docs)
    return (
        f"# Kanon\n\nGeprüft: {checked} · CLI {cli}\n\n"
        "| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n" + table + "\n\n## Quellen\n\n" + listed +
        f"\n- CLI-Version: https://npm.test/latest\n- Changelog: {BASE}changelog.md\n"
    )


def dep_table(extra=()):
    rows = [("claude-opus-5-5", "Active", "N/A", "Not sooner than September 22, 2027")]
    rows += [(f"claude-opus-4-{i}", "Active", "N/A", "Not sooner than May 28, 2027") for i in range(1, 10)]
    rows += list(extra)
    body = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows)
    return "| API model name | Current state | Deprecated | Tentative retirement date |\n| --- | --- | --- | --- |\n" + body + "\n" + PAD


def changelog(entries=("Added foo",)):
    new = "\n".join(f"  * {e}" for e in entries)
    return (f'<Update label="2.1.285" description="x">\n{new}\n</Update>\n'
            '<Update label="2.1.284" description="y">\n  * Old\n</Update>\n' + "z" * 100_000)


def pages(**override):
    result = {
        BASE + "cli-reference.md": "# CLI\n" + "\n".join(f"| `--flag-{i}` | x |" for i in range(90))
        + "\n| `--max-turns` | x |\n| `--model` | x |" + PAD,
        BASE + "env-vars.md": "# Env\n" + "\n".join(f"| `ANTHROPIC_VAR_{i}` | x |" for i in range(160))
        + "\n| `ANTHROPIC_MODEL` | x |" + PAD,
        BASE + "model-deprecations.md": dep_table(),
        BASE + "model-config.md": "| Model alias | Behavior |\n| - | - |\n| **`default`** | x |\n| **`opus`** | x |\n"
        "| **`sonnet`** | x |\n| **`haiku`** | x |\n" + PAD,
        BASE + "permission-modes.md": "| Mode | x |\n| - | - |\n| `default` | x |\n| `acceptEdits` | x |\n"
        "| `plan` | x |\n| `auto` | x |\n| `dontAsk` | x |\n| `bypassPermissions` | x |\n" + PAD + "\nPreToolUse Stop\n",
        "https://npm.test/latest": json.dumps({"version": "2.1.285", "pad": "x" * 300}),
        BASE + "changelog.md": changelog(),
    }
    result.update(override)
    return result


def fetcher_for(available, final=None):
    final = final or {}

    def fetch(url):
        if url not in available:
            raise cc.SourceError(f"{url}: 404")
        return cc.Fetched(url, final.get(url, url), available[url])
    return fetch


COURSE = {"m.md": "Use `--max-turns` with `claude -p --model opus`.\n"}


def run(course=None, canon_text=None, available=None, exceptions="", previous=None, today=TODAY, final=None, **kw):
    return cc.run(canon_text=canon_text or canon(), course=course or COURSE, exceptions_text=exceptions,
                  fetcher=fetcher_for(available or pages(), final), today=today, previous_state=previous, **kw)


def levels(result, level):
    return [f for f in result.findings if f.level == level]


def test_clean_run_exits_0():
    result = run()
    assert result.exit_code == 0
    assert levels(result, "rot") == [] and levels(result, "gelb") == []


def test_undocumented_course_flag_is_red_with_location():
    result = run(course={"b3.md": "intro\nPass `--metadata '{}'` to tag CI runs.\n"})
    [finding] = levels(result, "rot")
    assert finding.key == "missing:flag:--metadata"
    assert finding.where == ("b3.md:2",)
    assert result.exit_code == 1


def test_exception_suppresses_and_orphaned_exception_is_red():
    course = {"x.md": "Run `--door 3` in exercise 1.\n"}
    assert run(course=course, exceptions="--door | Übungsparameter\n").exit_code == 0
    orphan = run(exceptions="--orphan | git-Flag\n")
    assert [f.key for f in levels(orphan, "rot")] == ["orphan-exception:--orphan"]


@pytest.mark.parametrize("body", ["/docs/en/models/overview.md", "<!doctype html><html>" + "x" * 6000])
def test_redirect_stub_or_html_page_is_a_source_error(body):
    with pytest.raises(cc.SourceError):
        run(available=pages(**{BASE + "model-config.md": body}))


def test_html_prefixed_page_that_still_parses_is_a_source_error():
    # Everything else about the page is valid, so only the HTML guard can catch it.
    body = "<!doctype html><html><body>" + pages()[BASE + "env-vars.md"]
    with pytest.raises(cc.SourceError, match="HTML"):
        run(available=pages(**{BASE + "env-vars.md": body}))


def test_missing_source_is_a_source_error():
    available = pages()
    del available[BASE + "env-vars.md"]
    with pytest.raises(cc.SourceError):
        run(available=available)


def test_parser_floor_violation_is_a_source_error():
    short = "| API model name | Current state | Deprecated | Tentative retirement date |\n| --- | --- | --- | --- |\n" \
            "| claude-opus-5-5 | Active | N/A | Not sooner than September 22, 2027 |\n" + PAD
    with pytest.raises(cc.SourceError):
        run(available=pages(**{BASE + "model-deprecations.md": short}))


def test_canon_cli_version_missing_in_changelog_is_a_source_error():
    with pytest.raises(cc.SourceError):
        run(canon_text=canon(cli="2.1.100"))


def test_retiring_canon_model_is_red():
    haiku = ("Claude Haiku 4.5", "claude-haiku-4-5-20251001", "haiku", "Haiku", "Active", "Not sooner than October 15, 2026")
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-haiku-4-5-20251001", "Active", "N/A",
                                                                        "Not sooner than October 15, 2026")])})
    result = run(canon_text=canon(rows=(OPUS, haiku)), available=available)
    assert [f.key for f in levels(result, "rot")] == ["retiring:claude-haiku-4-5-20251001:2026-10-15"]


def test_newer_active_model_in_a_canon_family_is_red():
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-opus-6", "Active", "N/A", "Not sooner than May 1, 2028")])})
    assert [f.key for f in levels(run(available=available), "rot")] == ["new-model:claude-opus-6"]


def test_active_family_missing_in_canon_is_only_info():
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-mythos-5-1", "Active", "N/A", "Not sooner than May 1, 2028")])})
    result = run(available=available)
    assert levels(result, "rot") == []
    assert any(f.key == "unknown-families" for f in levels(result, "info"))


def test_canon_retirement_text_must_match_the_table():
    changed = ("Claude Opus 5.5", "claude-opus-5-5", "opus", "Opus", "Active", "Not sooner than June 1, 2027")
    assert [f.key.split(":")[0] for f in levels(run(canon_text=canon(rows=(changed,))), "rot")] == ["canon-retirement"]


@pytest.mark.parametrize("checked,level", [("2026-06-30", "rot"), ("2026-08-10", "info")])
def test_canon_age(checked, level):
    result = run(canon_text=canon(checked=checked))
    assert any(f.key.startswith(("canon-stale", "canon-age")) for f in levels(result, level))


def test_changelog_naming_a_course_identifier_is_yellow_keyword_only_is_info():
    available = pages(**{BASE + "changelog.md": changelog(["Fixed --max-turns off by one", "Changed the default theme", "Added foo"])})
    result = run(available=available)
    assert [f.text for f in levels(result, "gelb")] == ["2.1.285: Fixed --max-turns off by one"]
    assert [f.text for f in levels(result, "info") if f.key.startswith("changelog-kw")] == ["2.1.285: Changed the default theme"]
    assert result.exit_code == 1


def test_documented_mode_alias_from_the_cli_reference_is_accepted():
    cli = pages()[BASE + "cli-reference.md"] + "\n| `--permission-mode` | Accepts `default`, `plan`, or `manual` | x |\n"
    result = run(course={"c.md": "claude --permission-mode manual\n"}, available=pages(**{BASE + "cli-reference.md": cli}))
    assert levels(result, "rot") == []


def test_changelog_names_aliases_and_modes_only_in_code_form():
    available = pages(**{BASE + "changelog.md": changelog(["Changed `opus` to resolve differently", "Improved the opus picker"])})
    result = run(available=available)
    assert [f.text for f in levels(result, "gelb")] == ["2.1.285: Changed `opus` to resolve differently"]


def test_cockpit_comparison_ignores_provenance_but_reports_real_differences():
    course_cockpit = "<!doctype html>\n<p>x</p>\n" + "c" * 100_000
    same = course_cockpit.replace("<!doctype html>\n", "<!doctype html>\n<!-- Quelle: dynamic_workshop/resources/claude-code-workshop-ui.html · Stand X -->\n")
    url = "https://site.test/cockpit"
    clean = run(available=pages(**{url: same}), cockpit_text=course_cockpit, cockpit_url=url)
    assert levels(clean, "rot") == []
    differs = run(available=pages(**{url: same.replace("<p>x</p>", "<p>y</p>")}), cockpit_text=course_cockpit, cockpit_url=url)
    assert [f.key.split(":")[0] for f in levels(differs, "rot")] == ["cockpit-differs"]


def test_redirect_is_reported_as_info():
    result = run(final={BASE + "env-vars.md": BASE + "moved/env-vars.md"})
    assert any(f.key == f"redirect:{BASE}env-vars.md" for f in levels(result, "info"))


def test_second_identical_run_marks_findings_as_known():
    course = {"b3.md": "Pass `--metadata` here.\n"}
    first = run(course=course)
    second = run(course=course, previous=first.state)
    report = cc.render_report(second, today=TODAY, previous_state=first.state)
    assert "weiterhin offen" in report and "**neu**" not in report
    assert cc.summary(second, first.state, Path("r.md"))["new_red"] == 0
    assert cc.summary(first, None, Path("r.md"))["new_red"] == 1


def test_new_doc_identifiers_since_last_run_are_info():
    first = run()
    more = pages(**{BASE + "cli-reference.md": pages()[BASE + "cli-reference.md"] + "\n`--brand-new`"})
    second = run(available=more, previous=first.state)
    assert any("--brand-new" in f.text for f in levels(second, "info"))


def test_identifier_the_docs_deny_is_red_even_though_mentioned():
    env = pages()[BASE + "env-vars.md"] + "\nThere is no `$CLAUDE_MODEL` environment variable.\n"
    result = run(course={"c.md": "export CLAUDE_MODEL=x\n"}, available=pages(**{BASE + "env-vars.md": env}))
    assert [f.key for f in levels(result, "rot")] == ["denied:env:CLAUDE_MODEL"]


def _patch_main(monkeypatch, tmp_path, available):
    canon_file = tmp_path / "canon.md"
    canon_file.write_text(canon(), encoding="utf-8")
    exceptions_file = tmp_path / "exceptions.txt"
    exceptions_file.write_text("", encoding="utf-8")
    cockpit_file = tmp_path / "cockpit.html"
    cockpit_file.write_text("<p>x</p>", encoding="utf-8")
    monkeypatch.setattr(cc, "CANON", canon_file)
    monkeypatch.setattr(cc, "EXCEPTIONS", exceptions_file)
    monkeypatch.setattr(cc, "COCKPIT", cockpit_file)
    monkeypatch.setattr(cc, "read_course", lambda root=None: dict(COURSE))
    monkeypatch.setattr(cc, "fetch", fetcher_for(available))


def test_main_writes_report_state_and_summary_as_last_line(monkeypatch, tmp_path, capsys):
    _patch_main(monkeypatch, tmp_path, pages())
    state_dir = tmp_path / "state"
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(state_dir)]) == 0
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert last.startswith("SUMMARY ")
    assert json.loads(last[len("SUMMARY "):])["exit"] == 0
    assert (state_dir / "state.json").exists() and (state_dir / "reports" / "2026-09-29.md").exists()


def test_main_keeps_previous_state_on_source_error(monkeypatch, tmp_path, capsys):
    available = pages()
    del available["https://npm.test/latest"]
    _patch_main(monkeypatch, tmp_path, available)
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "state.json").write_text('{"keep": true}', encoding="utf-8")
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(state_dir)]) == 2
    assert (state_dir / "state.json").read_text(encoding="utf-8") == '{"keep": true}'
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert json.loads(last[len("SUMMARY "):])["exit"] == 2


def test_main_turns_an_unreadable_canon_into_exit_2(monkeypatch, tmp_path, capsys):
    _patch_main(monkeypatch, tmp_path, pages())
    monkeypatch.setattr(cc, "CANON", tmp_path / "missing.md")
    assert cc.main(["--today", "2026-09-29", "--state-dir", str(tmp_path / "s")]) == 2


def test_real_canon_is_machine_readable():
    cx = _load("currency_extract")
    text = (ROOT / "resources" / "_canonical.md").read_text(encoding="utf-8")
    cx.parse_canon_header(text)
    models = cx.parse_canon_models(text)
    assert {m.tier for m in models} == {"Fable", "Opus", "Sonnet", "Haiku"}
    for model in models:
        assert model.model_id.startswith("claude-") and model.alias in {"fable", "opus", "sonnet", "haiku"}
        assert re.fullmatch(r"(Not sooner than )?[A-Z][a-z]+ \d{1,2}, \d{4}", model.retirement), model.retirement
    sources = cx.parse_canon_sources(text)
    assert len(sources["Doku"]) == 13
    assert all(url.startswith("https://") for urls in sources.values() for url in urls)
    names = {url.rsplit("/", 1)[-1] for url in sources["Doku"]}
    assert {"model-deprecations.md", "model-config.md", "permission-modes.md"} <= names


# First live run 2026-09-29: the identifiers recorded in Step 2. The set may only shrink; a swap is caught too.
FROZEN_EXCEPTIONS = frozenset({"--decompose", "--door", "--headless", "--orphan", "--enable-auto-mode"})


def test_exception_list_only_shrinks():
    cx = _load("currency_extract")
    entries = cx.parse_exceptions((ROOT / "tools" / "currency_exceptions.txt").read_text(encoding="utf-8"))
    assert set(entries) <= FROZEN_EXCEPTIONS, sorted(set(entries) - FROZEN_EXCEPTIONS)
