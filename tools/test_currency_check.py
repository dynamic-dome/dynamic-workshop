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


def canon(checked="2026-09-29", cli="2.1.284", rows=(OPUS,), docs=DOCS, foreign=()):
    table = "\n".join(f"| {n} | `{i}` | `{a}` | {t} | {s} | {r} | 1M | 4 | 20 | Rolle |" for n, i, a, t, s, r in rows)
    listed = "\n".join(f"- Doku: {BASE}{d}" for d in docs)
    return (
        f"# Kanon\n\nGeprüft: {checked} · CLI {cli}\n\n"
        "| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n" + table + "\n\n## Quellen\n\n" + listed +
        f"\n- CLI-Version: https://npm.test/latest\n- Changelog: {BASE}changelog.md\n"
        + "".join(f"- Fremdprojekt: {url} ({chapter})\n" for url, chapter in foreign)
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


def changelog_live(groups, version="2.1.285", old="2.1.284"):
    """The format code.claude.com serves since 2026-10: **x.y.z**, a date line, **Group** headings, `* ` bullets."""
    body = "".join(f"**{name}**\n\n" + "".join(f"* {line}\n" for line in lines) + "\n" for name, lines in groups)
    return (f"# Claude Code changelog\n\n**{version}**\n\nOctober 23, 2026\n\n{body}"
            f"**{old}**\n\nOctober 6, 2026\n\n* Old\n" + "z" * 100_000)


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
    assert run(course=course, exceptions="--door | x.md | Übungsparameter\n").exit_code == 0
    orphan = run(exceptions="--orphan | m.md | git-Flag\n")
    assert [f.key for f in levels(orphan, "rot")] == ["orphan-exception:--orphan"]


def test_exception_only_covers_its_own_files():
    """An exception for an exercise parameter must not hide the same string used as a Claude Code flag elsewhere."""
    course = {"x.md": "Run `--door 3` in exercise 1.\n", "y.md": "Start with `claude --door -p hi`.\n"}
    result = run(course=course, exceptions="--door | x.md | Übungsparameter\n")
    [finding] = levels(result, "rot")
    assert finding.key == "missing:flag:--door" and finding.where == ("y.md:1",)


def test_model_values_of_the_subagent_frontmatter_count_as_aliases():
    """`model: inherit` is not in model-config's alias table; the `model` row of sub-agents.md names it. A word that is
    merely backticked elsewhere in the docs (`plan`, a permission mode) stays red."""
    course = {"a.md": "```yaml\nmodel: inherit\n```\n", "b.md": "```yaml\nmodel: plan\n```\n"}
    page = "| `model` | No | Model to use: `sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit` |" + PAD
    result = run(course=course, canon_text=canon(docs=DOCS + ["sub-agents.md"]),
                 available=pages(**{BASE + "sub-agents.md": page}))
    assert [f.key for f in levels(result, "rot")] == ["missing:alias:plan"]


def test_foreign_source_outage_keeps_its_last_hash():
    text = canon(foreign=[(PI, "X.3")])
    first = run(canon_text=text, available=pages(**{PI: PI_PAGE}))
    outage = run(canon_text=text, previous=first.state)
    assert outage.state["sources"][PI] == first.state["sources"][PI]
    changed = run(canon_text=text, available=pages(**{PI: PI_PAGE.replace("four", "seven")}), previous=outage.state)
    assert any("X.3" in f.text for f in levels(changed, "gelb"))


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


def test_active_model_inside_the_warning_window_is_only_info():
    """Review finding on #9957: "Not sooner than" 30 days away with status Active is the same false alarm as a lapsed
    date (Opus 4.6 on 2027-02-05 would turn the monthly run red in Jan and Feb 2027 with no real event)."""
    haiku = ("Claude Haiku 4.5", "claude-haiku-4-5-20251001", "haiku", "Haiku", "Active", "Not sooner than October 15, 2026")
    available = pages(**{BASE + "model-deprecations.md": dep_table([("claude-haiku-4-5-20251001", "Active", "N/A",
                                                                        "Not sooner than October 15, 2026")])})
    result = run(canon_text=canon(rows=(OPUS, haiku)), available=available)
    assert result.exit_code == 0 and levels(result, "rot") == [] and levels(result, "gelb") == []
    assert [f.key for f in levels(result, "info") if f.key.startswith("retiring")] == [
        "retiring-soon-unannounced:claude-haiku-4-5-20251001:2026-10-15"]


def _legacy_haiku(date_text, status="Active"):
    """Haiku 4.5 as a monitored Legacy row; the Deprecations table says `status` with `date_text` (todo #9957)."""
    model = ("Claude Haiku 4.5 (Legacy)", "claude-haiku-4-5-20251001", "haiku", "Haiku", "Active", date_text)
    table = dep_table([("claude-haiku-4-5-20251001", status, "N/A", date_text)])
    return run(canon_text=canon(rows=(OPUS, model)), available=pages(**{BASE + "model-deprecations.md": table}))


def test_active_model_whose_earliest_retirement_date_has_passed_is_only_info():
    """Todo #9957: "Not sooner than" is a floor, not an announcement. Status Active plus a lapsed date (Haiku 4.5 on
    2026-10-24) was a permanent false red; only a status change on the Deprecations page may turn it red."""
    result = _legacy_haiku("Not sooner than September 1, 2026")
    assert result.exit_code == 0 and levels(result, "rot") == [] and levels(result, "gelb") == []
    [info] = [f for f in levels(result, "info") if f.key.startswith("retiring-unannounced:")]
    assert info.key == "retiring-unannounced:claude-haiku-4-5-20251001:2026-09-01"
    assert "keine Abschaltung angekündigt" in info.text and "Active" in info.text


def test_a_retirement_date_equal_to_today_counts_as_passed():
    result = _legacy_haiku("Not sooner than September 29, 2026")
    assert result.exit_code == 0
    assert [f.key for f in levels(result, "info") if f.key.startswith("retiring")] == [
        "retiring-unannounced:claude-haiku-4-5-20251001:2026-09-29"]


@pytest.mark.parametrize("status", ["Deprecated", "Retired"])
def test_lapsed_date_with_a_status_change_is_still_red(status):
    result = _legacy_haiku("Not sooner than September 1, 2026", status=status)
    keys = [f.key for f in levels(result, "rot")]
    assert f"canon-status:claude-haiku-4-5-20251001:{status}" in keys
    assert not any(f.key.startswith("retiring-unannounced") for f in result.findings)


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
    available = pages(**{BASE + "changelog.md": changelog(["Changed --max-turns default", "Changed the default theme", "Added foo"])})
    result = run(available=available)
    assert [f.text for f in levels(result, "gelb")] == ["2.1.285: Changed --max-turns default"]
    assert [f.text for f in levels(result, "info") if f.key.startswith("changelog-kw")] == ["2.1.285: Changed the default theme"]
    assert result.exit_code == 1


@pytest.mark.parametrize("line", [
    "Fixed --max-turns off by one",
    "fixed --max-turns off by one",
    "[VSCode] Fixed --max-turns off by one",
    "\[VSCode] Fixed --max-turns off by one",  # the official changelog escapes the tag bracket
    "\[Claude Tag] Fixed --max-turns off by one",
    "**Security:** Fixed --max-turns off by one",
    "Windows: Fixed --max-turns off by one",
    "Fixed `opus` resolving to the wrong model",
])
def test_fixed_changelog_entries_naming_a_course_identifier_count_as_info_not_yellow(line):
    # Owner decision F9 (2026-10-22, todo #9518): before the monthly run, "Fixed" lines are info, not yellow.
    result = run(available=pages(**{BASE + "changelog.md": changelog([line])}))
    assert levels(result, "gelb") == []
    assert [f.text for f in levels(result, "info") if f.key.startswith("changelog-fixed")] == [f"2.1.285: {line}"]
    assert result.exit_code == 0


def test_fixed_changelog_info_keeps_the_named_identifiers_and_stays_out_of_the_state_keys():
    result = run(available=pages(**{BASE + "changelog.md": changelog(["Fixed --max-turns off by one"])}))
    [finding] = [f for f in levels(result, "info") if f.key.startswith("changelog-fixed")]
    assert finding.where == ("nennt --max-turns",)
    assert result.state["finding_keys"] == []
    assert cc.summary(result, None, Path("r.md"))["yellow"] == 0


def test_only_leading_fixed_downgrades_other_changelog_verbs_stay_yellow():
    lines = ["Changed --max-turns so it no longer fixes the count", "Removed --max-turns", "Added --max-turns, fixed docs"]
    result = run(available=pages(**{BASE + "changelog.md": changelog(lines)}))
    assert [f.text for f in levels(result, "gelb")] == [f"2.1.285: {line}" for line in lines]


def test_verb_labels_before_a_colon_do_not_turn_a_changed_or_removed_line_into_fixed_info():
    lines = ["Changed --max-turns: fixed bug", "Removed --max-turns flag: fixed docs"]
    result = run(available=pages(**{BASE + "changelog.md": changelog(lines)}))
    assert [f.text for f in levels(result, "gelb")] == [f"2.1.285: {line}" for line in lines]


def test_fixed_changelog_entry_without_a_course_identifier_stays_a_plain_keyword_info():
    result = run(available=pages(**{BASE + "changelog.md": changelog(["Fixed the default theme not saving"])}))
    assert levels(result, "gelb") == []
    assert [f.key.split(":")[0] for f in levels(result, "info") if f.key.startswith("changelog")] == ["changelog-kw"]


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


BEACON = ("<!-- Cloudflare Pages Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
          "data-cf-beacon='{\"token\": \"t0ken\"}'></script><!-- Cloudflare Pages Analytics -->")


def test_cockpit_comparison_ignores_the_injected_cloudflare_analytics_block():
    course_cockpit = "<!doctype html>\n<script>render();</script>\n</body>\n</html>\n" + "c" * 100_000
    live = course_cockpit.replace("</script>\n</body>", "</script>\n" + BEACON + "</body>")
    assert live != course_cockpit
    url = "https://site.test/cockpit"
    clean = run(available=pages(**{url: live}), cockpit_text=course_cockpit, cockpit_url=url)
    assert levels(clean, "rot") == []
    changed = run(available=pages(**{url: live.replace("render();", "render(1);")}), cockpit_text=course_cockpit, cockpit_url=url)
    assert [f.key.split(":")[0] for f in levels(changed, "rot")] == ["cockpit-differs"]


PI = "https://pi.test/docs"
PI_PAGE = "<html><body><script>var build = 1;</script><p>Pi has four tools.</p>" + PAD + "</body></html>"


def test_changed_foreign_source_is_yellow_and_names_the_chapter():
    text = canon(foreign=[(PI, "X.3")])
    first = run(canon_text=text, available=pages(**{PI: PI_PAGE}))
    assert first.exit_code == 0 and PI in first.state["sources"]
    same = run(canon_text=text, available=pages(**{PI: PI_PAGE.replace("build = 1", "build = 2")}), previous=first.state)
    assert levels(same, "gelb") == []
    moved = run(canon_text=text, available=pages(**{PI: PI_PAGE.replace("four", "seven")}), previous=first.state)
    [finding] = levels(moved, "gelb")
    assert "X.3" in finding.text and finding.where == (PI,) and moved.exit_code == 1


def test_unreachable_foreign_source_is_yellow_not_a_source_error():
    result = run(canon_text=canon(foreign=[(PI, "X.3")]))
    [finding] = levels(result, "gelb")
    assert "X.3" in finding.text and "nicht lesbar" in finding.text


def test_foreign_pages_never_document_claude_code_identifiers():
    page = PI_PAGE.replace("four tools", "the flag `--metadata`")
    result = run(course={"b3.md": "Pass `--metadata` here.\n"}, canon_text=canon(foreign=[(PI, "X.3")]),
                 available=pages(**{PI: page}))
    assert any("--metadata" in f.text for f in levels(result, "rot"))


def test_docs_with_the_same_file_name_do_not_shadow_each_other():
    """docs/en/cli-reference.md and docs/en/plugins/cli-reference.md: the permission modes come from the first."""
    cli = pages()[BASE + "cli-reference.md"] + "\n| `--permission-mode` | Accepts `default`, `plan`, or `manual` | x |\n"
    plugin_cli = "# Plugin CLI\n| `--strict` | Fail on warnings too |\n" + PAD
    available = pages(**{BASE + "cli-reference.md": cli, BASE + "plugins/cli-reference.md": plugin_cli})
    course = {"m.md": "Start `claude --permission-mode manual`, then `claude plugin validate . --strict`.\n"}
    result = run(course=course, canon_text=canon(docs=DOCS + ["plugins/cli-reference.md"]), available=available)
    assert levels(result, "rot") == []


def test_redirect_to_another_host_is_yellow():
    result = run(final={BASE + "env-vars.md": "https://elsewhere.example/env-vars.md"})
    assert any(f.key == f"redirect-host:{BASE}env-vars.md" for f in levels(result, "gelb"))


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
    # Todo #9957: the Legacy models behind the provider aliases stay in the monitored table (status from the Deprecations page).
    assert {"claude-haiku-4-5-20251001", "claude-sonnet-4-5-20250929", "claude-sonnet-4-6",
            "claude-opus-4-6"} <= {m.model_id for m in models}
    # Sonnet 4.5 is a known deprecation: the canon carries Deprecated plus the fixed date of the Deprecations page.
    [sonnet45] = [m for m in models if m.model_id == "claude-sonnet-4-5-20250929"]
    assert (sonnet45.status, sonnet45.retirement) == ("Deprecated", "November 30, 2026")
    for model in models:
        assert model.model_id.startswith("claude-") and model.alias in {"fable", "opus", "sonnet", "haiku"}
        assert re.fullmatch(r"(Not sooner than )?[A-Z][a-z]+ \d{1,2}, \d{4}", model.retirement), model.retirement
    sources = cx.parse_canon_sources(text)
    assert len(sources["Doku"]) == 15
    assert all(url.startswith("https://") for urls in sources.values() for url in urls)
    names = {url.rsplit("/", 1)[-1] for url in sources["Doku"]}
    assert {"model-deprecations.md", "model-config.md", "permission-modes.md"} <= names


# First live run 2026-09-29: the identifiers recorded in Step 2. The set may only shrink; a swap is caught too.
# Run 2026-10-06 (after the self-learner rebuild): `--orphan` left with S1.18's rewrite; four foreign flags joined
# (git in S4.5 and S4.7, OpenClaw in X.4), each justified in that commit.
FROZEN_EXCEPTIONS = frozenset({"--decompose", "--door", "--headless", "--enable-auto-mode",
                               "--deep", "--disable", "--git-dir", "--no-verify"})


def test_exception_list_only_shrinks():
    cx = _load("currency_extract")
    entries = cx.parse_exceptions((ROOT / "tools" / "currency_exceptions.txt").read_text(encoding="utf-8"))
    assert set(entries) <= FROZEN_EXCEPTIONS, sorted(set(entries) - FROZEN_EXCEPTIONS)


# --- Final review fixes (R14): future dates, pinned rules, floors, boundaries ---

def test_future_check_date_is_red_and_today_is_not():
    future = run(canon_text=canon(checked="2027-09-29"))
    assert [f.key for f in levels(future, "rot")] == ["canon-future:2027-09-29"]
    assert future.exit_code == 1
    assert not any(f.key.startswith("canon-future") for f in run().findings)


def test_canon_cli_newer_than_npm_is_red_and_equal_is_not():
    ahead = run(canon_text=canon(cli="2.1.286"))
    assert [f.key for f in levels(ahead, "rot")] == ["canon-cli-ahead:2.1.286:2.1.285"]
    assert not any(f.key.startswith("canon-cli-ahead") for f in run(canon_text=canon(cli="2.1.285")).findings)


def test_canon_model_with_a_non_active_status_is_red():
    table = dep_table().replace("| claude-opus-5-5 | Active |", "| claude-opus-5-5 | Deprecated |")
    result = run(available=pages(**{BASE + "model-deprecations.md": table}))
    assert "canon-status:claude-opus-5-5:Deprecated" in [f.key for f in levels(result, "rot")]


def test_canon_model_missing_from_the_deprecations_table_is_red():
    ghost = ("Claude Sonnet 9", "claude-sonnet-9", "sonnet", "Sonnet", "Active", "Not sooner than May 1, 2030")
    result = run(canon_text=canon(rows=(OPUS, ghost)))
    assert [f.key for f in levels(result, "rot")] == ["canon-unknown:claude-sonnet-9"]


def test_yellow_findings_are_new_once_then_known():
    available = pages(**{BASE + "changelog.md": changelog(["Removed --max-turns"])})
    first = run(available=available)
    key = levels(first, "gelb")[0].key
    assert key in first.state["finding_keys"]
    assert cc.summary(first, None, Path("r.md"))["new_yellow"] == 1
    second = run(available=available, previous=first.state)
    assert cc.summary(second, first.state, Path("r.md"))["new_yellow"] == 0


def test_size_floor_alone_is_a_source_error_naming_the_minimum():
    small = "| Model alias | Behavior |\n| - | - |\n| **`default`** | x |\n| **`opus`** | x |\n| **`sonnet`** | x |\n| **`haiku`** | x |\n"
    assert 100 < len(small.encode("utf-8")) < 5_000
    with pytest.raises(cc.SourceError, match="Minimum 5000"):
        run(available=pages(**{BASE + "model-config.md": small}))


def _cli_with(count):
    return "# CLI\n" + "\n".join(f"| `--flag-{i}` | x |" for i in range(count)) + "\n| `--max-turns` | x |\n| `--model` | x |" + PAD


def _env_with(count):
    return "# Env\n" + "\n".join(f"| `ANTHROPIC_VAR_{i}` | x |" for i in range(count)) + "\n| `ANTHROPIC_MODEL` | x |" + PAD


def _aliases_with(names):
    return "| Model alias | Behavior |\n| - | - |\n" + "\n".join(f"| **`{n}`** | x |" for n in names) + "\n" + PAD


def _modes_with(names):
    return "| Mode | x |\n| - | - |\n" + "\n".join(f"| `{n}` | x |" for n in names) + "\n" + PAD + "\nPreToolUse Stop\n"


def _few_deprecations():
    rows = [("claude-opus-5-5", "Active", "N/A", "Not sooner than September 22, 2027")]
    rows += [(f"claude-opus-4-{i}", "Active", "N/A", "Not sooner than May 28, 2027") for i in range(1, 5)]
    body = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows)
    return "| API model name | Current state | Deprecated | Tentative retirement date |\n| --- | --- | --- | --- |\n" + body + "\n" + PAD


@pytest.mark.parametrize("label,doc,body", [
    ("Flags in der Doku", "cli-reference.md", _cli_with(50)),
    ("Env-Variablen in der Doku", "env-vars.md", _env_with(100)),
    ("Zeilen der Deprecations-Tabelle", "model-deprecations.md", _few_deprecations()),
    ("Aliase in model-config.md", "model-config.md", _aliases_with(["default", "opus"])),
    ("Permission-Modi", "permission-modes.md", _modes_with(["default", "plan", "auto"])),
], ids=["flags", "env", "deprecations", "aliases", "modes"])
def test_each_parser_floor_alone_is_a_source_error_naming_its_label(label, doc, body):
    with pytest.raises(cc.SourceError, match=re.escape(label)):
        run(available=pages(**{BASE + doc: body}))


def _retiring_in(days, status="Active"):
    date = TODAY + dt.timedelta(days=days)
    text = f"Not sooner than {date.strftime('%B')} {date.day}, {date.year}"
    model = ("Claude Haiku 4.5", "claude-haiku-4-5-20251001", "haiku", "Haiku", "Active", text)
    table = dep_table([("claude-haiku-4-5-20251001", status, "N/A", text)])
    return run(canon_text=canon(rows=(OPUS, model)), available=pages(**{BASE + "model-deprecations.md": table}))


def test_active_model_30_days_before_the_earliest_date_is_info_not_red():
    result = _retiring_in(30)
    assert levels(result, "rot") == [] and result.exit_code == 0
    [info] = [f for f in levels(result, "info") if f.key.startswith("retiring")]
    assert info.key.startswith("retiring-soon-unannounced:") and "keine Abschaltung angekündigt" in info.text


def test_active_model_beyond_the_warning_window_has_no_retiring_finding():
    assert not any(f.key.startswith("retiring") for f in _retiring_in(60).findings)


def test_retirement_warning_boundary_for_a_deprecated_model_is_59_days_red_60_days_not():
    assert any(f.key.startswith("retiring:") for f in levels(_retiring_in(59, "Deprecated"), "rot"))
    assert not any(f.key.startswith("retiring:") for f in _retiring_in(60, "Deprecated").findings)


def _known_deprecation(days, page_status="Deprecated"):
    """Canon lists Sonnet 4.5 as Deprecated with a fixed retirement date `days` from today (todo #9957)."""
    date = TODAY + dt.timedelta(days=days)
    text = f"{date.strftime('%B')} {date.day}, {date.year}"
    model = ("Claude Sonnet 4.5 (Legacy)", "claude-sonnet-4-5-20250929", "sonnet", "Sonnet", "Deprecated", text)
    table = dep_table([("claude-sonnet-4-5-20250929", page_status, "September 30, 2026", text)])
    return run(canon_text=canon(rows=(OPUS, model)), available=pages(**{BASE + "model-deprecations.md": table}))


def test_known_deprecation_inside_the_warning_window_is_yellow_not_red():
    result = _known_deprecation(37)
    assert levels(result, "rot") == []
    [yellow] = [f for f in levels(result, "gelb") if f.key.startswith("retiring-known:")]
    assert yellow.key == f"retiring-known:claude-sonnet-4-5-20250929:{TODAY + dt.timedelta(days=37)}"
    assert "bekannt abgekündigt" in yellow.text and "in 37 Tagen" in yellow.text


def test_known_deprecation_beyond_the_warning_window_has_no_finding():
    result = _known_deprecation(60)
    assert levels(result, "rot") == [] and not any(f.key.startswith("retiring") for f in result.findings)


def test_known_deprecation_turning_retired_is_red_against_the_canon_status():
    result = _known_deprecation(37, page_status="Retired")
    assert "canon-status:claude-sonnet-4-5-20250929:Retired" in [f.key for f in levels(result, "rot")]
    assert not any(f.key.startswith("retiring-known") for f in result.findings)


def test_known_deprecation_past_its_date_but_still_listed_is_red():
    result = _known_deprecation(0)
    assert any(f.key.startswith("retiring:claude-sonnet-4-5-20250929") for f in levels(result, "rot"))


def test_live_changelog_format_is_read_and_the_group_decides_fixed_vs_yellow():
    """Todo #9942: the live changelog has **x.y.z** / **Group** / `* ` bullets; the monthly run must not abort on it, and
    the heading decides the type: lines under "N bug fixes" are info (F9), under "Changed" they stay yellow."""
    groups = [("Changed", ["Changed `--max-turns` default", "Removed --max-turns from the picker"]),
              ("2 bug fixes", ["Windows: the --max-turns limit was ignored", "Fixed --max-turns off by one"])]
    result = run(available=pages(**{BASE + "changelog.md": changelog_live(groups)}))
    assert [f.text for f in levels(result, "gelb")] == [
        "2.1.285: Changed `--max-turns` default", "2.1.285: Removed --max-turns from the picker"]
    assert [f.text for f in levels(result, "info") if f.key.startswith("changelog-fixed")] == [
        "2.1.285: Windows: the --max-turns limit was ignored", "2.1.285: Fixed --max-turns off by one"]


def test_live_changelog_format_with_only_old_entries_is_clean():
    text = changelog_live([("Added", ["Added --max-turns"])], version="2.1.284", old="2.1.283")
    assert run(available=pages(**{BASE + "changelog.md": text})).exit_code == 0


def test_real_live_changelog_excerpt_runs_through_the_check():
    excerpt = (ROOT / "tools" / "fixtures" / "currency" / "changelog-live-2026-10-24.md").read_text(encoding="utf-8")
    npm = json.dumps({"version": "2.1.310", "pad": "x" * 300})
    result = run(canon_text=canon(cli="2.1.292"),
                 available=pages(**{BASE + "changelog.md": excerpt + "z" * 100_000, "https://npm.test/latest": npm}))
    assert result.exit_code == 0 and levels(result, "gelb") == []
    assert {f.key.split(":")[1] for f in result.findings if f.key.startswith("changelog")} == {"2.1.293"}


# --- Nachprüf-Hook für version-pinned-Zeilen (todo #9518) ---
# `version-pinned: <Grund>` lets a course line name a model generation against the alias rule. Nothing ever looked at
# those lines again, so a pinned claim could outlive its model. The monthly run now re-reads every pinned line against
# the Deprecations table: Active = info (list to re-read), Deprecated/Retired/unknown = yellow (the claim needs a look).

HAIKU_45 = "claude-haiku-4-5-20251001"


def _pinned(course_text, rows=(), course_path="m.md"):
    table = dep_table(list(rows))
    return run(course={course_path: course_text}, available=pages(**{BASE + "model-deprecations.md": table}))


def _keys(result, level):
    return [f.key.split(":")[0] for f in levels(result, level)]


def test_pinned_line_with_an_active_model_is_listed_as_info_and_does_not_change_the_exit():
    line = "Haiku 4.5 hat 200K Kontext. <!-- version-pinned: Quiz zu Kontextgrenzen -->\n"
    result = _pinned(line, [(HAIKU_45, "Active", "N/A", "Not sooner than October 15, 2027")])
    assert result.exit_code == 0 and levels(result, "gelb") == [] and levels(result, "rot") == []
    [info] = [f for f in levels(result, "info") if f.key.startswith("pinned-active:")]
    assert info.where == ("m.md:1",) and "Haiku 4.5" in info.text and "Quiz zu Kontextgrenzen" in info.text


@pytest.mark.parametrize("status", ["Deprecated", "Retired"])
def test_pinned_line_whose_model_left_active_is_yellow(status):
    line = "Intro.\nHaiku 4.5 hat 200K Kontext. <!-- version-pinned: Quiz zu Kontextgrenzen -->\n"
    result = _pinned(line, [(HAIKU_45, status, "September 1, 2026", "November 30, 2026")])
    [finding] = levels(result, "gelb")
    assert finding.key.startswith(f"pinned-status:{HAIKU_45}:{status}:")
    assert finding.where == ("m.md:2",) and "Quiz zu Kontextgrenzen" in finding.text
    assert result.exit_code == 1


def test_pinned_line_with_a_model_missing_from_the_deprecations_table_is_yellow():
    result = _pinned("Opus 3.7 war langsam. <!-- version-pinned: Vergleich mit heute -->\n")
    [finding] = levels(result, "gelb")
    assert finding.key.startswith("pinned-unknown:") and "Opus 3.7" in finding.text


def test_historical_pin_may_name_a_retired_model():
    line = "Bis Juli 2026 war Haiku 4.5 der Standard. <!-- version-pinned: historischer Vergleich -->\n"
    result = _pinned(line, [(HAIKU_45, "Retired", "May 1, 2026", "June 1, 2026")])
    assert result.exit_code == 0 and levels(result, "gelb") == []
    assert [f.key.split(":")[0] for f in levels(result, "info") if f.key.startswith("pinned")] == ["pinned-historical"]


def test_every_model_on_a_pinned_line_is_checked_and_id_and_prose_forms_both_resolve():
    line = f"`{HAIKU_45}` statt Opus 4.1. <!-- version-pinned: Migrationsbeispiel -->\n"
    result = _pinned(line, [(HAIKU_45, "Deprecated", "September 1, 2026", "November 30, 2026")])
    assert _keys(result, "gelb") == ["pinned-status"]
    assert _keys(result, "info").count("pinned-active") == 1  # Opus 4.1 stays Active in dep_table()


def test_unpinned_model_mentions_are_not_this_hooks_business():
    result = _pinned("Haiku 4.5 hat 200K Kontext.\n", [(HAIKU_45, "Retired", "May 1, 2026", "June 1, 2026")])
    assert not any(f.key.startswith("pinned") for f in result.findings)


def test_a_marker_without_a_reason_is_not_a_pin():
    result = _pinned("Haiku 4.5 hat 200K. <!-- version-pinned: -->\n", [(HAIKU_45, "Retired", "May 1, 2026", "June 1, 2026")])
    assert not any(f.key.startswith("pinned") for f in result.findings)


def test_pinned_finding_keys_survive_a_line_shift():
    row = [(HAIKU_45, "Deprecated", "September 1, 2026", "November 30, 2026")]
    line = "Haiku 4.5 hat 200K. <!-- version-pinned: Quiz -->\n"
    first = _pinned(line, row)
    shifted = _pinned("neue Zeile davor\n" + line, row)
    assert [f.key for f in levels(first, "gelb")] == [f.key for f in levels(shifted, "gelb")]


def test_dated_id_of_a_single_number_generation_resolves_to_its_family_and_not_to_the_date():
    """Review finding: `claude-sonnet-4-20250514` was read as version (4, 20250514) and landed in pinned-unknown."""
    sonnet_4 = "claude-sonnet-4-20250514"
    line = f"`{sonnet_4}` ist der Beispiel-Pin. <!-- version-pinned: Migrationsbeispiel -->\n"
    result = _pinned(line, [(sonnet_4, "Active", "N/A", "Not sooner than June 15, 2027")])
    assert "pinned-unknown" not in _keys(result, "gelb")
    assert _keys(result, "info").count("pinned-active") == 1
