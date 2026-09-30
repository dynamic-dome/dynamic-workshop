# -*- coding: utf-8 -*-
"""Monthly currency check for the Dynamic Workshop.

Are the identifiers the course teaches still documented, and is the canon still the current model lineup?
Exit 0 = clean, 1 = red or yellow findings, 2 = a source or the canon is unusable (fail-closed).
The last stdout line is 'SUMMARY {json}' for the monthly wrapper.

Aufruf (aus dem Repo-Root):  python tools/currency_check.py [--cockpit-url URL] [--today YYYY-MM-DD]
Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.request
from urllib.parse import urlsplit
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import currency_extract as cx  # noqa: E402
import lint_currency  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "resources" / "_canonical.md"
COCKPIT = ROOT / "resources" / "claude-code-workshop-ui.html"
EXCEPTIONS = ROOT / "tools" / "currency_exceptions.txt"
STATE_DIR = ROOT / ".currency"

TIMEOUT_S = 30
MIN_BYTES = {"doc": 5_000, "cli": 200, "changelog": 100_000, "cockpit": 100_000, "foreign": 500}
MIN_FLAGS, MIN_ENV, MIN_DEPRECATIONS, MIN_ALIASES, MIN_MODES = 80, 150, 10, 3, 5
RETIREMENT_WARN_DAYS = 60
CANON_INFO_DAYS, CANON_RED_DAYS = 45, 90
REQUIRED_DOCS = ("cli-reference.md", "model-deprecations.md", "model-config.md", "permission-modes.md")
KEYWORDS = re.compile(r"\b(removed|deprecated|renamed|no longer|default)\b", re.I)
SPECIFIC_KINDS = ("flag", "env", "hook_event", "model_id")
KIND_LABEL = {
    "flag": "Flag", "env": "Env-Variable", "hook_event": "Hook-Event",
    "model_id": "Modell-ID", "alias": "Modell-Alias", "permission_mode": "Permission-Modus",
}


class SourceError(Exception):
    """A source or the canon is unusable; the run must end with exit 2, never 'clean'."""


@dataclass(frozen=True)
class Fetched:
    url: str
    final_url: str
    text: str


@dataclass(frozen=True)
class Finding:
    level: str  # "rot" | "gelb" | "info"
    key: str  # stable across runs: decides "neu" vs "weiterhin offen"
    text: str
    where: tuple = ()


@dataclass
class RunResult:
    exit_code: int
    findings: list
    state: dict
    sources: list  # (url, final_url, bytes, sha256, changed)
    unparsed_json: int
    canon_checked: dt.date
    canon_age_days: int
    cli_canon: str
    cli_latest: str


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "dynamic-workshop-currency-check/1"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            return Fetched(url, response.geturl(), response.read().decode("utf-8"))
    except (OSError, ValueError) as exc:  # URLError/HTTPError/timeouts are OSError; bad UTF-8 is ValueError
        raise SourceError(f"{url}: {exc}") from exc


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _short(text):
    return _sha(text)[:10]


def fetch_checked(fetcher, url, kind):
    got = fetcher(url)
    size = len(got.text.encode("utf-8"))
    if size < MIN_BYTES[kind]:
        raise SourceError(f"{url}: nur {size} Bytes (Minimum {MIN_BYTES[kind]})")
    if kind in ("doc", "changelog") and "<html" in got.text[:500].lower():
        raise SourceError(f"{url}: HTML statt Markdown (Fehler- oder Challenge-Seite?)")
    return got


def read_course(root=None):
    root = str(root or ROOT)
    return {rel: "".join(lint_currency.read_lines(full)) for rel, full in lint_currency.live_files(root)}


def _collect_course(course):
    by_value, unparsed = {}, 0
    for path in sorted(course):
        hits, count = cx.extract_course_hits(path, course[path])
        unparsed += count
        for hit in hits:
            by_value.setdefault((hit.kind, hit.value), []).append(f"{hit.path}:{hit.line}")
    return by_value, unparsed


def _check_course(by_value, exceptions, union, aliases, modes):
    findings = []
    taught_in = {}
    for (kind, value), where in sorted(by_value.items()):
        taught_in.setdefault(value, set()).update(w.rsplit(":", 1)[0] for w in where)
        if value in exceptions:
            # an exception covers only the files it names: the same string elsewhere is checked like any other
            where = [w for w in where if w.rsplit(":", 1)[0] not in exceptions[value]["files"]]
            if not where:
                continue
        denial = cx.denied_in_docs(value, union)
        if denial:
            findings.append(Finding("rot", f"denied:{kind}:{value}",
                                    f"{KIND_LABEL[kind]} `{value}` steht im Kurs, die Doku verneint ihn: {denial[:160]}",
                                    tuple(sorted(set(where)))))
        elif not cx.exists_in_docs(kind, value, union, aliases, modes):
            findings.append(Finding("rot", f"missing:{kind}:{value}",
                                    f"{KIND_LABEL[kind]} `{value}` steht im Kurs, aber in keiner Doku-Quelle",
                                    tuple(sorted(set(where)))))
    for value in sorted(exceptions):
        if not taught_in.get(value, set()) & exceptions[value]["files"]:
            findings.append(Finding("rot", f"orphan-exception:{value}",
                                    f"Ausnahme `{value}` kommt in ihren Dateien nicht mehr vor: in currency_exceptions.txt "
                                    "anpassen oder streichen"))
    return findings


def _check_canon_models(canon_models, deprecations, today):
    findings, families = [], {}
    for model in canon_models:
        family, version = cx.model_family_version(model.model_id)
        families[family] = max(families.get(family, ()), version)
        row = deprecations.get(model.model_id)
        if row is None:
            findings.append(Finding("rot", f"canon-unknown:{model.model_id}",
                                    f"Kanon-Modell `{model.model_id}` fehlt in der Deprecations-Tabelle"))
            continue
        if row.status != "Active":
            findings.append(Finding("rot", f"canon-status:{model.model_id}:{row.status}",
                                    f"Kanon-Modell `{model.model_id}` hat Status {row.status}"))
        if row.retirement != model.retirement:
            findings.append(Finding("rot", f"canon-retirement:{model.model_id}:{row.retirement}",
                                    f"Retirement von `{model.model_id}`: Kanon „{model.retirement}“, Doku „{row.retirement}“"))
        earliest = cx.parse_date(row.retirement)
        if earliest and (earliest - today).days < RETIREMENT_WARN_DAYS:
            findings.append(Finding("rot", f"retiring:{model.model_id}:{earliest}",
                                    f"`{model.model_id}` kann ab {earliest} abgeschaltet werden "
                                    f"({(earliest - today).days} Tage)"))
    unknown = set()
    for model_id, row in sorted(deprecations.items()):
        if row.status != "Active":
            continue
        family, version = cx.model_family_version(model_id)
        if family not in families:
            unknown.add(family)
        elif version > families[family]:
            findings.append(Finding("rot", f"new-model:{model_id}",
                                    f"Neues aktives Modell `{model_id}` ist neuer als der Kanon-Stand der Familie {family}"))
    if unknown:
        findings.append(Finding("info", "unknown-families",
                                "Aktive Modellfamilien, die der Kanon nicht führt: " + ", ".join(sorted(unknown))))
    return findings


def _check_changelog(entries, by_value):
    specific = sorted({v for (k, v) in by_value if k in SPECIFIC_KINDS}, key=len, reverse=True)
    # Aliases and modes are ordinary words ("default", "plan"): they count only in code form.
    words = sorted({v for (k, v) in by_value if k not in SPECIFIC_KINDS}, key=len, reverse=True)
    findings = []
    for version, line in entries:
        named = [v for v in specific if re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", line)]
        named += [v for v in words if "`" + v + "`" in line]
        if named:
            findings.append(Finding("gelb", f"changelog:{version}:{_short(line)}", f"{version}: {line}",
                                    tuple(f"nennt {v}" for v in named)))
        elif KEYWORDS.search(line):
            findings.append(Finding("info", f"changelog-kw:{version}:{_short(line)}", f"{version}: {line}"))
    return findings


def run(*, canon_text, course, exceptions_text, fetcher, today, previous_state, cockpit_text=None, cockpit_url=None):
    """Pure orchestration over injected inputs. Raises SourceError for anything unusable."""
    try:
        checked, cli_canon = cx.parse_canon_header(canon_text)
        canon_models = cx.parse_canon_models(canon_text)
        sources = cx.parse_canon_sources(canon_text)
        foreign = cx.parse_canon_foreign(canon_text)
        exceptions = cx.parse_exceptions(exceptions_text)
    except ValueError as exc:
        raise SourceError(str(exc)) from exc

    docs = [fetch_checked(fetcher, url, "doc") for url in sources["Doku"]]
    cli = fetch_checked(fetcher, sources["CLI-Version"][0], "cli")
    changelog = fetch_checked(fetcher, sources["Changelog"][0], "changelog")
    live_cockpit = fetch_checked(fetcher, cockpit_url, "cockpit") if cockpit_url else None

    by_name = {}
    for doc in docs:  # the first listed page wins: plugins/cli-reference.md must not shadow cli-reference.md
        by_name.setdefault(doc.url.rsplit("/", 1)[-1], doc)
    missing = [name for name in REQUIRED_DOCS if name not in by_name]
    if missing:
        raise SourceError("Kanon-Quellenliste ohne " + ", ".join(missing))
    union = "\n".join(d.text for d in docs)
    doc_ids = cx.doc_identifiers(union)
    deprecations = cx.parse_deprecations(by_name["model-deprecations.md"].text)
    aliases = cx.parse_aliases(by_name["model-config.md"].text)
    modes = cx.parse_permission_modes(by_name["permission-modes.md"].text, by_name["cli-reference.md"].text)
    for label, got, floor in (
        ("Flags in der Doku", len(doc_ids["flag"]), MIN_FLAGS),
        ("Env-Variablen in der Doku", len(doc_ids["env"]), MIN_ENV),
        ("Zeilen der Deprecations-Tabelle", len(deprecations), MIN_DEPRECATIONS),
        ("Aliase in model-config.md", len(aliases), MIN_ALIASES),
        ("Permission-Modi", len(modes), MIN_MODES),
    ):
        if got < floor:
            raise SourceError(f"{label}: {got} < Minimum {floor} (Format geändert?)")
    try:
        cli_latest = json.loads(cli.text)["version"]
        entries = cx.changelog_since(changelog.text, cli_canon)
    except (ValueError, KeyError) as exc:
        raise SourceError(f"CLI-Version/Changelog: {exc}") from exc

    by_value, unparsed = _collect_course(course)
    findings = _check_course(by_value, exceptions, union, aliases, modes)
    findings += _check_canon_models(canon_models, deprecations, today)
    findings += _check_changelog(entries, by_value)

    age = (today - checked).days
    if age < 0:
        findings.append(Finding("rot", f"canon-future:{checked}",
                                f"Kanon-Prüfdatum {checked} liegt in der Zukunft (Tippfehler?)"))
    if cx.version_tuple(cli_canon) > cx.version_tuple(cli_latest):
        findings.append(Finding("rot", f"canon-cli-ahead:{cli_canon}:{cli_latest}",
                                f"Kanon nennt CLI {cli_canon}, neuer als npm {cli_latest} (Tippfehler?)"))
    if age > CANON_RED_DAYS:
        findings.append(Finding("rot", f"canon-stale:{checked}",
                                f"Kanon-Prüfdatum {checked} ist {age} Tage alt (> {CANON_RED_DAYS})"))
    elif age > CANON_INFO_DAYS:
        findings.append(Finding("info", f"canon-age:{checked}", f"Kanon-Prüfdatum {checked} ist {age} Tage alt"))

    if live_cockpit is not None:
        mine, theirs = _sha(cx.normalize_cockpit(cockpit_text)), _sha(cx.normalize_cockpit(live_cockpit.text))
        if mine != theirs:
            findings.append(Finding("rot", f"cockpit-differs:{mine[:12]}:{theirs[:12]}",
                                    "Cockpit auf der Website weicht vom Kurs-Cockpit ab (Re-Export fällig)",
                                    (live_cockpit.final_url,)))

    previous = previous_state or {}
    for kind in ("flag", "env"):
        before = set(previous.get("doc_" + kind, []))
        new = sorted(doc_ids[kind] - before) if before else []
        if new:
            findings.append(Finding("info", f"doc-new:{kind}:{_short(' '.join(new))}",
                                    f"Neu in der Doku ({KIND_LABEL[kind]}): " + ", ".join(new)))

    # Third-party pages (community chapters) are only watched for changes; their text never joins `union`, so they
    # cannot make an undocumented Claude Code flag look documented. An outage there must not stop the monthly run.
    chapter_of, foreign_got = {}, []
    for url, chapter in foreign:
        chapter_of[url] = chapter
        try:
            foreign_got.append(fetch_checked(fetcher, url, "foreign"))
        except SourceError as exc:
            findings.append(Finding("gelb", f"foreign-unreadable:{url}",
                                    f"Fremdprojekt-Quelle nicht lesbar ({exc}) — Kapitel {chapter} von Hand prüfen", (url,)))

    known_sources = previous.get("sources", {})
    rows = []
    for got in docs + [cli, changelog] + ([live_cockpit] if live_cockpit else []) + foreign_got:
        sha = _sha(cx.normalize_foreign(got.text) if got.url in chapter_of else got.text)
        changed = got.url in known_sources and known_sources[got.url]["sha256"] != sha
        rows.append((got.url, got.final_url, len(got.text.encode("utf-8")), sha, changed))
        if changed and got.url in chapter_of:
            findings.append(Finding("gelb", f"foreign-changed:{got.url}:{sha[:12]}",
                                    f"Fremdprojekt-Quelle geändert — Kapitel {chapter_of[got.url]} gegen die Quelle "
                                    "prüfen und das Prüfdatum erneuern", (got.url,)))
        if got.final_url != got.url and urlsplit(got.final_url).netloc != urlsplit(got.url).netloc:
            findings.append(Finding("gelb", f"redirect-host:{got.url}",
                                    f"Quelle auf einen anderen Host umgeleitet: {got.url} -> {got.final_url} (prüfen, "
                                    "ob das noch die offizielle Quelle ist)", (got.final_url,)))
        elif got.final_url != got.url:
            findings.append(Finding("info", f"redirect:{got.url}",
                                    f"Quelle umgezogen: {got.url} -> {got.final_url} (Kanon-Quellenliste nachziehen)"))

    exit_code = 1 if any(f.level in ("rot", "gelb") for f in findings) else 0
    state = {
        "version": 1,
        "date": today.isoformat(),
        "cli_latest": cli_latest,
        "doc_flag": sorted(doc_ids["flag"]),
        "doc_env": sorted(doc_ids["env"]),
        "sources": {
            # an unreadable third-party page keeps its last hash, so a change during the outage is still reported
            **{url: known_sources[url] for url in chapter_of if url in known_sources},
            **{url: {"sha256": sha, "final_url": final} for url, final, _size, sha, _changed in rows},
        },
        "finding_keys": sorted(f.key for f in findings if f.level in ("rot", "gelb")),
    }
    return RunResult(exit_code, findings, state, rows, unparsed, checked, age, cli_canon, cli_latest)


def render_report(result, *, today, previous_state):
    known = set((previous_state or {}).get("finding_keys", []))
    count = {level: sum(f.level == level for f in result.findings) for level in ("rot", "gelb", "info")}
    lines = [
        f"# Currency-Check {today}",
        "",
        f"- Kanon geprüft: {result.canon_checked} ({result.canon_age_days} Tage) · CLI laut Kanon "
        f"{result.cli_canon} · neueste CLI {result.cli_latest}",
        f"- Befunde: {count['rot']} rot · {count['gelb']} gelb · {count['info']} info",
        f"- Nicht parsebare JSON-Blöcke im Kurs: {result.unparsed_json}",
        "",
    ]
    for level, title in (("rot", "Rot"), ("gelb", "Gelb"), ("info", "Info")):
        items = [f for f in result.findings if f.level == level]
        lines += [f"## {title} ({len(items)})", ""]
        for finding in items:
            tag = "" if level == "info" else (" · weiterhin offen" if finding.key in known else " · **neu**")
            lines.append(f"- {finding.text}{tag}")
            lines += [f"  - {where}" for where in finding.where[:10]]
            if len(finding.where) > 10:
                lines.append(f"  - … {len(finding.where) - 10} weitere")
        lines.append("")
    lines += ["## Quellen", "", "| URL | End-URL | Bytes | sha256 | geändert |", "|---|---|---|---|---|"]
    for url, final, size, sha, changed in result.sources:
        lines.append(f"| {url} | {'' if final == url else final} | {size} | {sha[:12]} | {'ja' if changed else ''} |")
    return "\n".join(lines) + "\n"


def summary(result, previous_state, report_path):
    known = set((previous_state or {}).get("finding_keys", []))
    red = [f for f in result.findings if f.level == "rot"]
    yellow = [f for f in result.findings if f.level == "gelb"]
    return {
        "exit": result.exit_code,
        "red": len(red),
        "yellow": len(yellow),
        "new_red": sum(f.key not in known for f in red),
        "new_yellow": sum(f.key not in known for f in yellow),
        "canon_checked": result.canon_checked.isoformat(),
        "canon_age_days": result.canon_age_days,
        "report": str(report_path),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Monatlicher Currency-Check des Dynamic Workshop")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--cockpit-url")
    parser.add_argument("--state-dir", type=Path, default=STATE_DIR)
    args = parser.parse_args(argv)
    state_path = args.state_dir / "state.json"
    report_path = args.state_dir / "reports" / f"{args.today}.md"
    try:
        previous = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
        result = run(
            canon_text=Path(CANON).read_text(encoding="utf-8"),
            course=read_course(),
            exceptions_text=Path(EXCEPTIONS).read_text(encoding="utf-8"),
            fetcher=fetch,
            today=args.today,
            previous_state=previous,
            cockpit_text=Path(COCKPIT).read_text(encoding="utf-8"),
            cockpit_url=args.cockpit_url,
        )
    except (SourceError, OSError, ValueError) as exc:
        print(f"FEHLER (fail-closed): {exc}")
        print("SUMMARY " + json.dumps({"exit": 2, "error": str(exc)}, ensure_ascii=False))
        return 2
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(result, today=args.today, previous_state=previous), encoding="utf-8")
    state_path.write_text(json.dumps(result.state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Bericht: {report_path}")
    print("SUMMARY " + json.dumps(summary(result, previous, report_path), ensure_ascii=False))
    return result.exit_code


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
