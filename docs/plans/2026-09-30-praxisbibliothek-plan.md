# Praxisbibliothek — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (Owner-Entscheid 2026-09-30: durchziehen,
> Orchestrator setzt selbst um, Migration als Workflow-Fan-out, unabhängige Prüfer an den Gates). Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den Workshop zur deutschsprachigen Claude-Code-Praxisbibliothek umbauen — Kapitel als einzige Quelle,
Einstufung mit persönlichem Pfad auf drei Oberflächen, neu gebautes Cockpit, teach-artiger Tutor, neue Visuals.

**Architecture:** Markdown-Kapitel mit schmalem YAML-Frontmatter sind die Quelle. `tools/library_model.py` parst,
`tools/build_library.py` validiert und generiert (Katalog, Übersichten, Pfade, Cockpit). `tools/placement.py` ist die
Referenz-Engine der Einstufung (nur Standardbibliothek); das Cockpit trägt eine JS-Portierung, beide gegen dieselben
Testvektoren. Der Inhalt zieht per Workflow-Fan-out aus den alten Dateien um, abgesichert durch Snippet-Ledger,
Aussagen-Matrix und die bestehenden Wächter-Tests.

**Tech Stack:** Python 3.12 (PyYAML, markdown, python-pptx nur für Pflege), pytest, Playwright (Python) für
Browser-Tests, Node für `node --check` und JS-Vektortests, PowerPoint-COM für Deck-Sichtprüfung.

**Spec:** `docs/plans/2026-09-30-praxisbibliothek-design.md` (v2 + Codex-Runden). Bei Widerspruch gilt die Spec.

## Global Constraints

- Arbeitsort: Worktree `Desktop/Claude-Projekte/dynamic_workshop-bibliothek`, Branch `praxisbibliothek`; kein Push, kein Merge, kein Website-Export (Owner).
- Kapitel: Deutsch mit Umlauten, Anrede „du"; Code, Befehle, Dateinamen, Bezeichner Englisch; Codeblöcke byte-identisch zur Quelle.
- Modellgenerationen nur in `resources/_canonical.md`; sonst Aliase/Rollen; Ausnahme `version-pinned: <Grund>` in derselben Zeile (`python tools/lint_currency.py`).
- Dateien UTF-8 ohne BOM, LF; Python-Subprozesse mit `encoding="utf-8"`; Pfade per `pathlib`/`os.scandir`, keine Shell-Strings.
- Cockpit: genau ein Inline-`<script>`, keine Inline-Handler, keine Inline-`style`-Attribute, keine externen Referenzen, kein `confirm(`; Pfad `resources/claude-code-workshop-ui.html`.
- localStorage-Keys: Fortschritt `ccWorkshopUiState` (Feld `done` kompatibel), Profil `ccWorkshopProfileV1`.
- Lernende brauchen nur Python-Standardbibliothek (`tools/placement.py`); PyYAML/markdown/python-pptx nur für Pflege.
- Tests nie gegen Produktionsdaten: dieses Repo hat keine DB; Playground-Tests nur in `workshop-playground/`.
- Stilregel: keine KI-Floskeln der Nutzerliste (u. a. das Bild der „verheilten Wunde" für Fehler), keine unbelegten Zahlen, keine Werbesprache.
- Lokale Server nur `--bind 127.0.0.1`, Browser auf `127.0.0.1:<port>`.

## Review Focus

- **Blockierter/kaputter localStorage** (Safari privat, Sandbox-iframe, `null`/Array-JSON): Cockpit rendert trotzdem, speichert nur nicht — Test in Task 12.
- **Quiz-/Kapiteltext mit `"`, `<`, `&`, `</script>`**: bricht weder Attribute noch das einzige Script — Generator-Test in Task 10, Escaping-Test in Task 12.
- **Einstufung abgebrochen oder teilweise ausgefüllt** (nur Ziel, keine Bereiche): Engine liefert trotzdem einen vollständigen, sinnvollen Pfad — Vektor in Task 4.
- **Windows-Pfade und CRLF** bei Generator/`--check` (autocrlf=true im Checkout): `--check` vergleicht zeilenend-normalisiert, schreibt LF — Test in Task 5.
- **Alte Deep-Links/Aliase** (`?view=65&run=S2.3`, `/workshop learn 2.2`): führen zum richtigen Kapitel statt ins Leere — Tests in Task 12 und Task 14.

---

## Phase 1 — Bibliotheks-Werkzeuge

### Task 1: Kapitel-Modell (`tools/library_model.py`)

**Files:**
- Create: `tools/library_model.py`, `tools/test_library_model.py`, `tools/fixtures/library/` (3 Mini-Kapitel: lesson, practice, community; plus `_shelves.yaml`, `_placement.yaml` Minimalfassungen)

**Interfaces:**
- Produces:
  - `SECTION_ORDER = ["Schnellcheck", "Auf einen Blick", "Bild im Kopf", "Im Detail", "Vorführen", "Selbst machen", "Typische Fallen", "Check", "Weiterlesen"]`
  - `@dataclass Quiz(question: str, correct: str, wrong: list[str])`
  - `@dataclass Chapter(path, id, type, title, shelf, level, minutes, requires, safety_floor, transferable, outcome, sources, aliases, after, sections: dict[str, str], section_order: list[str], quiz: Quiz | None, example: str | None, example_lang: str, skip_check: list[str], glance: str, analogy: str, checkpoint: str, mermaid: list[str], links: list[str])` with properties `order: int` and `session: int | None`
  - `def order_of(chapter_id: str, after: str | None) -> int` — `S<s>.<p>` → `s*1000 + p*10`; `X.<n>` needs `after` → `order_of(after) + 5`
  - `def parse_chapter(path: Path) -> Chapter` (raises `ChapterError(path, message)`)
  - `def load_library(root: Path) -> Library` with `Library(chapters: list[Chapter] sorted by order, shelves: list[dict], placement: dict, root: Path)`

- [ ] **Step 1: Failing tests** in `tools/test_library_model.py`:
  - `test_order_of_session_ids`: `order_of("S2.8", None) == 2080`, `order_of("S0.1", None) == 10`, `order_of("S4.10", None) == 4100`, `order_of("X.1", "S2.13") == 2135`; `order_of("X.1", None)` raises `ValueError`.
  - `test_parse_lesson_fixture`: fixture `s2-08-demo.md` → `id == "S2.8"`, `session == 2`, `section_order` equals the fixture's H2s, `quiz.correct` and 3 `wrong`, `example` is the fenced block after `<!-- cockpit:example -->`, `skip_check` has 2 items, `glance` = first paragraph of „Auf einen Blick", `analogy` = first paragraph of „Bild im Kopf", `checkpoint` = first paragraph of „Check", `mermaid` has 1 entry.
  - `test_h2_inside_code_fence_is_not_a_section`: a `## Fake` line inside a ``` fence stays in the body.
  - `test_meta_block_is_ignored_for_sections`: content between `<!-- meta:start -->` and `<!-- meta:end -->` is not part of any section.
  - `test_crlf_input_parses_like_lf`: same fixture read with CRLF endings → identical `Chapter` fields.
  - `test_missing_frontmatter_raises`: file without `---` header → `ChapterError`.
- [ ] **Step 2:** `python -m pytest tools/test_library_model.py -q` → FAIL (module missing).
- [ ] **Step 3:** Implement `tools/library_model.py` (PyYAML `safe_load`; fence-aware H2 split; quiz regex over the `<details>` block: `**Frage:**`, `- **Richtig:**`, `- Falsch:`; example = first fence after marker; links = markdown `](target)` outside code).
- [ ] **Step 4:** Tests PASS.
- [ ] **Step 5:** Commit `feat(library): chapter model and parser`.

### Task 2: Validator (`tools/build_library.py validate`)

**Files:**
- Create: `tools/build_library.py` (CLI `validate | build | check`, plus `--chapter <file>` for single-chapter validation), `tools/test_build_library_validate.py`

**Interfaces:**
- Consumes: `load_library`, `parse_chapter`
- Produces: `def validate(lib: Library, *, complete: bool) -> list[Problem]`, `@dataclass Problem(path: str, rule: str, message: str)`; CLI exit 0 (ok) / 1 (problems); `complete=False` skips the „all required IDs present" rule (used by `--chapter` and during migration).
- Rules (each a named `rule` string, tested individually):
  `frontmatter-schema` (required keys per type, types of values, `type` ∈ {lesson, setup, practice, capstone, community}, `level` ∈ {core, deep-dive, bonus}), `id-format` (`S<0-4>.<n>` or `X.<n>`), `id-unique`, `alias-unique`, `filename` (`s<s>-<nn>-<slug>.md` / `x-<nn>-<slug>.md` matching id), `shelf-exists`, `requires-exist`, `requires-backward` (only smaller `order`), `requires-acyclic`, `sections-allowed` (type table §4.3), `sections-required`, `section-order`, `example-count`, `quiz-count`, `quiz-shape` (1 richtig, 3 falsch, none empty), `quiz-length-tell` (richtig ≤ 1.35 × Mittel der falschen, alle ≥ 0.6 × richtig), `skip-check-count` (lesson: genau 2), `links-resolve` (relative targets exist), `no-migration-todo` (`TODO(migration)` verboten), `required-ids` (complete: S0.1, S1.1–S1.20, S2.1–S2.20, S3.1–S3.15, S4.1–S4.10, X.1, X.2), `placement-refs` (areas/minimum_path/scenarios zeigen auf existierende Kapitel, Szenario-`correct` ist eine Option-ID), `sources-https`.
- [ ] **Step 1:** Failing tests: one test per rule with a minimal broken fixture built in `tmp_path` (helper `write_chapter(tmp_path, **overrides)`), plus `test_valid_fixture_library_has_no_problems`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Implement rules.
- [ ] **Step 4:** PASS; `python tools/build_library.py validate --root tools/fixtures/library --partial` exit 0.
- [ ] **Step 5:** Commit `feat(library): validator with per-rule tests`.

### Task 3: Regale und Einstufungsregeln (Daten)

**Files:**
- Create: `resources/library/_shelves.yaml`, `resources/library/_placement.yaml`, `tools/test_placement_rules.py`

**Interfaces:**
- `_shelves.yaml`: list of `{id, title, purpose, intro}` in spec §5 order (19 Regale).
- `_placement.yaml`: `{version: 1, skim_factor: 0.3, base_shelves: [...], minimum_path: [S0.1, S1.1, S1.2, S1.8, S1.10, S1.13, S1.14, S1.16, S1.19], times: [{id, label, stage_minutes|null}], goals: [{id, label, focus_shelves, flags}], areas: [{id, label, statement, chapters}], scenarios: [{id, area, question, options: [{id, text}], correct, explanation, chapter}], reasons: {code: text}}` — contents exactly Spec §6.2/§6.3 and Anhang E (14 Bereiche, 7 Ziele, 4 Zeiten, 6 Szenarien).
- [ ] **Step 1:** Failing tests: shelves count 19 and ids match spec table; 14 areas; every chapter id in areas appears in exactly one area; 6 scenarios, each with 4 options, `correct` ∈ option ids, option length spread ≤ 15 % around the mean; every reason code used by the engine exists (list in test).
- [ ] **Step 2–4:** write data, PASS.
- [ ] **Step 5:** Commit `feat(library): shelves and placement rules as data`.

### Task 4: Einstufungs-Engine (`tools/placement.py`) + Vertrag

**Files:**
- Create: `tools/placement.py`, `tools/fixtures/placement-vectors.json`, `tools/test_placement.py`

**Interfaces:**
- Produces: `def place(catalog: dict, answers: dict) -> dict` (pure; `catalog` = parsed `resources/library/catalog.json`, which embeds the rules) returning `{version: 1, chapters: [{id, status, reason, stage, override}], stages: [{n, minutes}], totals: {work_min, skim_min}, warnings: [str]}`; CLI `python tools/placement.py --answers <file> [--catalog resources/library/catalog.json] [--format json|md]`; `--template` prints an empty answers document.
- Answers schema: `{version: 1, goals: [id], time: id, areas: {area: 0|1|2|null}, scenarios: {id: option_id|null}, overrides: {chapter_id: status}}`; missing keys = defaults (goals → [alltag], time → nach-und-nach, areas → 0).
- Algorithm: Spec §6.3 Schritte A–F wörtlich; stage minutes: `work` = minutes, `skim` = `ceil(minutes * skim_factor)`; sorting by `order` everywhere; ties impossible (orders unique).
- [ ] **Step 1:** Write `placement-vectors.json` by hand from the spec (≥ 12 personas, each with `answers` and expected `chapters` status map + stage of 5 marker chapters + warnings): P1 Anfänger alltag kurz · P2 alles gemacht security · P3 einschaetzen komplett · P4 automation, basics=2, hooks=0, Hook-Szenario falsch · P5 Override S2.8 → skip (Warnung, Status skip) · P6 zwei Ziele team+agents · P7 moderieren · P8 nur Ziel, keine Bereiche · P9 MCP r=1 ohne MCP-Ziel → S2.17 work · P10 Kette S4.4 → Voraussetzungen skim · P11 kurz mit Mindestpfad > 120 Min → Warnung · P12 alles „weiß nicht".
- [ ] **Step 2:** Failing tests: `test_vectors_python` (parametrized over vectors, against a catalog built from `tools/fixtures/placement-catalog.json` — a frozen catalog snapshot generated in Task 5 and refreshed with `build_library.py build --refresh-fixture`), `test_every_recommended_chapter_has_prereqs_recommended_or_skipped`, `test_stage_minutes_sum`, `test_first_chapter_of_a_stage_always_fits`, `test_deterministic` (same input twice → identical JSON), `test_cli_template_roundtrip`.
- [ ] **Step 3:** Implement `place()` (stdlib only: `json`, `math`, `argparse`, `pathlib`).
- [ ] **Step 4:** PASS. Hand-check P1 output against spec reasoning; adjust vectors only where the spec is ambiguous, and write the decision into spec §6.3 in the same commit.
- [ ] **Step 5:** Commit `feat(placement): reference engine and shared test vectors`.

### Task 5: Generatoren und `--check`

**Files:**
- Modify: `tools/build_library.py` (subcommands `build`, `check`)
- Create: `tools/test_build_library_generate.py`
- Generated (committed): `resources/library/catalog.json`, `resources/library/README.md`, `resources/library/einstufung.md`, `resources/paths/README.md`, `resources/paths/live-workshop.md`, `resources/paths/ziel-<goal>.md` (7), meta blocks in every chapter, `tools/fixtures/placement-catalog.json`

**Interfaces:**
- Produces: `def build_outputs(lib: Library) -> dict[Path, str]` (pure: path → content); `build` writes them (LF, UTF-8), `check` compares normalized (`\r\n` → `\n`) and lists stale files; catalog JSON uses `sort_keys=True, ensure_ascii=False, indent=1`.
- Catalog chapter fields: `id, type, title, shelf, level, minutes, order, session, requires, requires_all, safety_floor, transferable, outcome, aliases, file, sources, skip_check, glance, analogy, example, example_lang, checkpoint, quiz, area` (`area` looked up from placement).
- Meta block format (one line each): `> **Regal:** [Titel](README.md#<shelf>) · **Stufe:** Kern|Vertiefung|Kür · **~N Min** · **Voraussetzungen:** [S1.5](file) … · 🛡 Sicherheitsboden (nur wenn true)` and `> ← [S2.7 Titel](file) · [Bibliothek](README.md) · [S2.9 Titel](file) →`.
- [ ] **Step 1:** Failing tests: build over fixture library → expected files present; `check` on fresh build → no stale; mutate one chapter title → `check` lists README + catalog + that chapter; CRLF working copy → `check` clean; catalog `requires_all` is transitive; live-workshop path lists sessions 0–4 with minute sums per level.
- [ ] **Step 2–4:** implement, PASS.
- [ ] **Step 5:** Commit `feat(library): generators for catalog, overviews, paths and meta blocks`.

**Gate A (nach Task 5):** Codex-Verifier (read-only) auf Tasks 1–5 gegen Spec §4, §6, §7. Befunde an der Quelle prüfen, beheben, erst dann Phase 2.

## Phase 2 — Umzug der Inhalte

### Task 6: Snippet-Ledger

**Files:**
- Create: `tools/migration_ledger.py`, `tools/test_migration_ledger.py`, `tools/fixtures/migration-dropped.txt`

**Interfaces:**
- Produces: `def old_snippets(base="ba222d2") -> list[Snippet]` (reads the 9 source files plus cheatsheet/quick-reference/faq/troubleshooting/prerequisites/glossary via `git show <base>:<path>`; fenced blocks; `Snippet(path, line, lang, text, digest)` with digest = sha256 of text with trailing whitespace stripped per line); `def new_corpus(root) -> str` (all `resources/**/*.md` except `docs/`); CLI `python tools/migration_ledger.py --chapter S2.8` prints the snippets owned by that chapter (via `docs/migration/ownership.json`) with found/missing.
- Test `test_every_old_snippet_is_kept_or_dropped_with_reason`: each digest found in new corpus **or** listed in `migration-dropped.txt` as `<digest> <path>:<line> <reason>`; reasons must be non-empty; dropped list only shrinks (test compares against committed count header).
- [ ] Steps: failing test (expected to fail until migration is done — mark `xfail(strict=False)` with reason „Migration läuft" until Task 9, then remove xfail), implement CLI, commit `test(migration): snippet ledger against the base commit`.

### Task 7: Pilot-Regal Hooks (S2.6–S2.10)

- [ ] **Step 1:** Writer-Brief nach Anhang „Schreib-Brief" unten, Kapitel S2.6–S2.10, ein Agent.
- [ ] **Step 2:** Validator `--chapter` je Datei grün; `python tools/migration_ledger.py --chapter S2.x` ohne fehlende Snippets außer begründet.
- [ ] **Step 3:** Prüfer-Agent (unabhängig, sonnet) erstellt Aussagen-Matrix `docs/migration/S2.x.json` je Kapitel.
- [ ] **Step 4:** Orchestrator liest alle fünf Kapitel vollständig, prüft Matrix-Stichproben an der Quelle, `pytest tools/test_course_hooks.py -q` grün.
- [ ] **Step 5:** Brief schärfen (Erkenntnisse ins Brief-Anhang), Commit `docs(library): hooks shelf as pilot`.

### Task 8: Fan-out aller übrigen Regale + neue Kapitel

- [ ] **Step 1:** Workflow: ein Schreiber je Regal (große Regale geteilt: agents 2, mcp-knowledge 2, context 2, start 2), dann je Kapitel Prüfer (Aussagen-Matrix), dann Fix-Runde (max. 2) — Pipeline ohne Barriere.
- [ ] **Step 2:** S0.1 (aus `prerequisites.md`, Lernenden-Teil), X.1 (Community, Fakten aus Spec Anhang D), X.2 (Lernen mit Claude Code, `/teach`-Mechanik) als eigene Schreib-Aufträge.
- [ ] **Step 3:** `python tools/build_library.py validate` (complete) grün; `build`; `check` grün.
- [ ] **Step 4:** Orchestrator-Stichprobe: je Regal ein Kapitel vollständig gelesen, je Matrix drei Aussagen an der Quelle geprüft (Ergebnis in `docs/migration/README.md`).
- [ ] **Step 5:** Commits je Regal `docs(library): <shelf> shelf`.

### Task 9: Referenz, Moderation, Archiv, Aufräumen

**Files:**
- Create: `resources/reference/` (README + 9 Karten + glossar, analogien, faq, adoptionsplan-vorlage, kosten-nachbau), `resources/moderation/` (README, handbuch, vorbereitung, videos), `resources/media/` (Video-Folien, mp3, mp4)
- Move (git mv, unverändert): `resources/review-*` → `docs/reviews/<datum>/…`, `resources/deck-audit-2026-05-21.md`, `dry-run-…`, `final-gap-sweep-…` → `docs/reviews/2026-05-21/`, `HANDOFF.md` → `docs/reviews/2026-06-21/HANDOFF.md`
- Delete (git rm): `resources/modules/`, `resources/demos/block-*.md`, `resources/exercises/`, `WORKSHOP_EINFUEHRUNG.md`, `resources/workshop-guide.md`, `resources/session-plan.md`, `resources/prerequisites.md`, `resources/cheatsheet.md`, `resources/quick-reference.md`, `resources/faq.md`, `resources/troubleshooting.md`, `resources/glossary.md`, `resources/security-analogies.md`, `resources/trainer-notes.md`, `resources/live-3-person-mode.md`, `resources/retrieval-recap-bridges.md`, `resources/transfer-retention-plan.md`, `resources/capstone-exit-assessment.md`, `resources/video-scripts.md`, `resources/archive/workshop-learning-dashboard-legacy.html`, alte Decks (erst in Task 16)
- Modify: `tools/test_course_hooks.py`, `tools/test_course_ci_auth.py`, `tools/lint_currency.py` (Review-Archiv-Regel → `docs/` ist schon ausgeklammert; tote Sonderfälle entfernen), `tools/test_workshop_ui_behavior.py` (in Task 12 ersetzt), Fixtures der Currency-Tests bleiben (eigene Kopien)
- [ ] **Step 1:** Referenzkarten schreiben lassen (ein Agent je 3 Karten) aus cheatsheet/quick-reference/glossary/faq/troubleshooting mit Doku-Links und Prüfstempel `Geprüft: 2026-09-30 · CLI 2.1.285` (aus Kanon); Widersprüche aus Spec Anhang B korrigiert.
- [ ] **Step 2:** Moderations-Handbuch aus trainer-notes/live-3/recap/transfer/session-plan-Begründungen.
- [ ] **Step 3:** `grep -rn` nach allen alten Pfaden in Live-Dateien → 0 Treffer (Test `test_no_links_to_removed_files`).
- [ ] **Step 4:** Ledger ohne xfail grün; alle Tools-Tests grün; Lint OK.
- [ ] **Step 5:** Commit `refactor: move reviews to docs, retire the old module files`.

**Gate B (nach Task 9):** Codex-Verifier auf die Migration (Stichprobe: 10 zufällige Kapitel gegen `ba222d2`-Quelle, alle Sicherheitsboden-Kapitel vollständig).

## Phase 3 — Cockpit

### Task 10: Cockpit-Build (`tools/build_cockpit.py`)

**Files:**
- Create: `tools/cockpit/template.html` (Gerüst, CSS, JS-Platzhalter `/*@@LIBRARY_DATA@@*/`), `tools/build_cockpit.py`, `tools/test_build_cockpit.py`
- Modify: `tools/build_library.py` (`build` ruft `build_cockpit.render(lib)`), Output `resources/claude-code-workshop-ui.html`

**Interfaces:**
- `def chapter_html(ch: Chapter, lib: Library) -> str` (markdown → HTML mit `markdown` + `fenced_code`, `tables`; sanitisiert: keine `<script>`, `<iframe>`, `on*`-Attribute; Links umgeschrieben nach Spec §7); `def render(lib) -> str` (Template + `const LIBRARY = <json>;` mit `</` → `<\/` escaped).
- [ ] Tests: genau ein `<script` im Artefakt; `node --check` auf dem Script; Kapiteltext mit `</script>` bleibt inert; keine relativen `href` außer `?`/`#`; Kapitel-Link → `?run=`; Repo-Link → GitHub-URL; Artefakt ≤ 1,5 MB, sonst `full_html` weggelassen und `full_url` gesetzt (Test mit künstlich großem Kapitel).
- [ ] Commit `feat(cockpit): generated from the library`.

### Task 11: Cockpit-UI

**Files:** `tools/cockpit/template.html` (Ansichten Start, Einstufung, Mein Pfad, Bibliothek, Kapitel, Wiederholen; JS-Engine `place()` 1:1 zur Python-Referenz)
- [ ] Skills zuerst lesen: `frontend-design:frontend-design`, dataviz (Status-Palette validieren mit `validate_palette.js`).
- [ ] Test `tools/test_placement_js.py`: extrahiert die JS-Engine aus dem Artefakt (Marker `/*@@ENGINE_START@@*/…/*@@ENGINE_END@@*/`), führt alle Vektoren per `node` aus, vergleicht exakt mit Erwartung (skip mit Grund, wenn `node` fehlt).
- [ ] Invarianten-Tests: Fisher-Yates-Mischung (`shuffle`), keine Flash-Tokens, kein `confirm(`, keine Inline-Handler/-Styles, `aria-live` an Feedback-Regionen.
- [ ] Commit `feat(cockpit): placement, path, library and chapter views`.

### Task 12: Browser-Verhaltenstests + QA

**Files:** Create `tools/test_cockpit_browser.py` (Playwright, lokaler Server `127.0.0.1` auf freiem Port, übersprungen mit Grund, wenn Playwright fehlt); Delete `tools/test_workshop_ui_behavior.py` (ersetzt, siehe Spec §8.1)
- [ ] Tests: 0 Konsolenfehler/Page-Errors auf allen Ansichten; Persona P1 durch den Assistenten klicken → „Mein Pfad" zeigt die Vektor-Erwartung; Quiz beantworten bucht kein `done`; „Erledigt" bucht; Reload → „weiter, wo du warst"; `localStorage` blockiert (Init-Skript wirft bei Zugriff) → Seite rendert mit Hinweis; kaputter JSON-Wert → Seite rendert; `?view=65&run=S2.3` → S2.3; 390 px Breite ohne horizontales Scrollen; Tastatur: Tab erreicht alle Bedienelemente, Pfeiltasten nur ohne Modifier.
- [ ] Screenshots Desktop + Mobil je Ansicht nach `%TEMP%/workshop-qa/` und Sichtprüfung durch den Orchestrator.
- [ ] Commit `test(cockpit): behavior tests in a real browser`.

### Task 13: Diagramme (abwerfbar)

- [ ] `tools/render_diagrams.py`: Mermaid-Blöcke aller Kapitel mit Playwright + Mermaid (Build-Zeit-Download nach `tools/.cache/`, nicht committet) nach `resources/library/diagrams/<sha8>.svg` (committet, dunkles Thema); Renderfehler = Exit 1; Cockpit bettet SVG inline ein (bereinigt: keine `<script>`, keine `foreignObject`-HTML-Handler).
- [ ] Wenn das in vertretbarer Zeit nicht stabil läuft: Cockpit zeigt den Mermaid-Quelltext als Code und verlinkt die GitHub-Fassung; Entscheidung im Bericht.

## Phase 4 — Tutor

### Task 14: `/workshop` im teach-Stil

**Files:** Modify `skills/workshop/SKILL.md`, `commands/workshop.md`, `agents/workshop-mentor.md`, `.claude-plugin/plugin.json`, `tools/install_workshop_plugin.ps1`, `tools/workshop_doctor.ps1`; Create `skills/workshop/MISSION-FORMAT.md`, `skills/workshop/LEARNING-RECORD-FORMAT.md` (angelehnt an mattpocock/skills `teach`, MIT, mit Attribution)
- [ ] Vorher: `${CLAUDE_SKILL_DIR}`/Plugin-Root gegen die aktuelle Skills-Doku prüfen (`curl -s https://code.claude.com/docs/en/skills.md`), Ergebnis im Commit-Text.
- [ ] Test `tools/test_workshop_tooling.py` erweitern: jede im SKILL/Command genannte Datei existiert; jede ID-Form (`S2.8`, `2.2`, `X.1`, `start`, `next`, `review`, `guide S3`) ist in der Routing-Tabelle; Mentor nennt keine gelöschten Pfade; `plugin.json` beschreibt 65 LE + Bibliothek.
- [ ] Trockenlauf: `python tools/placement.py --template` → Beispielantworten → `--format md` → plausibler `lernpfad.md`.
- [ ] Commit `feat(tutor): teach-style /workshop start|next|learn|review|guide`.

## Phase 5 — Doku und Deck

### Task 15: Einstiege und Projektregeln

- [ ] `README.md` (Schaufenster), `HOW-TO-USE.md` (Anleitung, drei Rollen), `CLAUDE.md`/`AGENTS.md` (≤ 40 Zeilen, neue Struktur/Regeln, Quellenhoheit), `docs/CHANGELOG.md` (neu), `workshop-playground/CLAUDE.md` (Vuln-Zahl, falls falsch).
- [ ] Test `test_no_links_to_removed_files` über Root-Dokumente; Lint OK.
- [ ] Commit `docs: one showcase, one guide, rules for the library`.

### Task 16: Deck neu

- [ ] Skill `anthropic-skills:pptx` lesen; `tools/build_deck.py` neu: Daten aus `catalog.json`, Folien laut Spec §11, Schrift ≥ 14 pt, Diagramm-Folien als native Formen; Ausgabe `resources/media/claude-code-praxisbibliothek.pptx`; alte Decks `git rm`.
- [ ] PowerPoint-Export nach PNG (`%TEMP%/workshop-qa/deck/`), Kontaktbogen ansehen, Überläufe beheben.
- [ ] `tools/test_workshop_tooling.py`: Deck hat erwartete Folienzahl und Titel aus dem Katalog.
- [ ] Commit `feat(deck): overview deck generated from the catalog`.

## Phase 6 — Abnahme

### Task 17: Gesamtprüfung

- [ ] `python tools/build_library.py check` · `python -m pytest tools -q` · `python tools/lint_currency.py` · `python tools/currency_check.py --state-dir .currency/manual` (erwartet: nur Haiku-Retirement rot; Cockpit-Abweichung zur Website ist erwartet, bis der Owner exportiert) · `cd workshop-playground && python -m pytest -q`.
- [ ] Codex-Verifier (Gate C) gegen Spec + Plan über den ganzen Branch; jeden Befund an der Quelle prüfen, beheben.
- [ ] Sweep vor Owner-Push: private Pfade/Hosts/Namen (`grep -rn "Users/domes\|domes\|192.168\." -- resources docs tools README.md HOW-TO-USE.md`).
- [ ] Wiki-TODO und DCO nachziehen, Session-Summary, Bericht an Dominic mit Screenshots und offenen Owner-Schritten.

---

## Anhang: Schreib-Brief (für Task 7/8, wird nach dem Pilot geschärft)

Du ziehst Kapitel der Claude-Code-Praxisbibliothek um. **Du übersetzt und ordnest, du erfindest nichts.**

1. Lies Spec §4 (Format, Typen, Stilregeln) und diesen Brief. Lies deine Heimat-Bereiche aus
   `docs/migration/ownership.json` (Zeilen der Datei im Basis-Commit — lies sie mit `git show ba222d2:<pfad>`),
   die Felder deiner Kapitel in `docs/migration/source-map.json` (Outcome, Schnellcheck, Diagramm-Idee, Primärquelle,
   didaktische Befunde) und den geprüften deutschen Cockpit-Text in `docs/migration/cockpit-content-ba222d2.json`.
2. Schreibe je Kapitel eine Datei nach `resources/library/`. „Auf einen Blick" und „Bild im Kopf" dürfen den
   Cockpit-Text nutzen; „Im Detail", „Vorführen", „Selbst machen" kommen aus den Heimat-Bereichen. Moderationshinweise
   (Talking Points, Recovery Notes, Timing) gehören in `<details><summary>Für Moderierende</summary>` unter „Vorführen".
3. Codeblöcke, Befehle, JSON, Pfade **byte-identisch**. Marker `tested asset: …` und `version-pinned: …` bleiben in
   derselben Zeile bzw. direkt am Snippet. Prüfe mit `python tools/migration_ledger.py --chapter <ID>`.
4. Quiz: nimm die alte Frage, **gleiche die Antwortlängen an** (richtig ≤ 1,35 × Mittel der falschen), ändere den
   fachlichen Inhalt nicht. Schnellcheck: 2 Verhaltensfragen.
5. Behebe nur Widersprüche, die in Spec Anhang B oder in den Befunden der Quellenkarte belegt sind, und vermerke
   jede inhaltliche Korrektur im Bericht. Unklar? `<!-- TODO(migration): Frage -->` statt Raten (der Validator
   verhindert, dass es so bleibt; der Orchestrator entscheidet).
6. Validiere jede Datei: `python tools/build_library.py validate --chapter resources/library/<datei>.md`.
7. Rückgabe (JSON): je Kapitel `{id, file, snippets_missing: [], corrections: [{old, new, evidence}],
   todos: [], unsure: []}` plus Vorschlag für die Regal-Einleitung.
