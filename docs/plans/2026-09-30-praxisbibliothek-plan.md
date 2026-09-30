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

### Task 1: Kapitel-Modell (`tools/library_model.py`) — erledigt (`d15807e`)

**Files:** `tools/library_model.py`, `tools/test_library_model.py`, `tools/fixtures/library/` (lesson S2.7/S2.8, practice
S2.20 mit `offers`, community X.1 mit `after`; `_shelves.yaml`, `_placement.yaml` Minimalfassungen)

**Interfaces (Produces):**
- `SECTION_ORDER`, `CHAPTER_TYPES`, `LEVELS`, `SESSION_ID`, `EXTRA_ID`, `EXAMPLE_MARKER`
- `order_of(chapter_id: str, after: str | None) -> int` (S<s>.<p> → s·1000 + p·10; X.<n> → order_of(after) + 5)
- `Quiz(question, correct, wrong: list[str])`
- `Chapter(path, id, type, title, shelf, level, minutes, requires, safety_floor, transferable, outcome, sources, aliases,
  after, offers, front, h1, preamble, sections, section_order, quiz, example, example_lang, skip_check, glance, analogy,
  checkpoint, mermaid, links)` mit Properties `order`, `session`
- `parse_chapter(path) -> Chapter` (wirft `ChapterError(path, message)`); `load_library(root) -> Library(root,
  chapters, shelves, placement, problems)` mit Property `by_id`
- 10 Tests grün.

### Task 2: Validator (`tools/build_library.py validate`) — erledigt (`2b0f7a6`)

**Interfaces (Produces):** `validate(lib, *, complete: bool) -> list[Problem]`, `Problem(path, rule, message)`, CLI
`validate [--root] [--complete] [--chapter <datei>]` (Exit 0/1). Regeln mit je eigenem Test: `parse`,
`frontmatter-schema` (inkl. `after` nur und immer für X, `offers` nur und immer für practice), `id-format`, `id-unique`,
`alias-unique`, `filename`, `h1`, `shelf-exists`, `requires-exist`, `requires-backward`, `requires-acyclic`,
`practice-no-requires`, `offers-exist` (existiert, gleiche Session), `sections-allowed`, `sections-required`,
`section-order`, `example-count`, `quiz-count`, `quiz-shape`, `quiz-length-tell` (richtig ≤ 1,35 × Mittel, falsch ≥
0,6 × richtig), `skip-check-count`, `links-resolve`, `no-migration-todo`, `sources-https`, `sources-required`
(lesson/setup), `placement-refs`, `area-unique`, `minimum-path-closed`, `required-ids` (complete). 43 Tests grün.

- [ ] **Nachtrag:** Regel `order-unique` (zwei Kapitel mit gleichem `order`) und Regel `meta-contract` (Task 5), je mit Test.

### Task 3: Regale und Einstufungsdaten — Daten und Tests fertig

**Files:** `resources/library/_shelves.yaml` (19 Regale, Spec §5), `resources/library/_placement.yaml` (Spec §6.2/E),
`docs/migration/chapter-meta.yaml` (verbindliche Metadaten aller 68 Kapitel: id, type, title, shelf, level, minutes,
requires, safety_floor, transferable, aliases, offers, after), `tools/test_placement_rules.py` (12 Tests: Regal-Reihenfolge,
14 Bereiche, ein Bereich je Kapitel, Ziele/Zeiten/Defaults, 6 Szenarien in 6 Bereichen, Optionslängen ±15 %, richtige
Option höchstens in 2 von 6 Szenarien die längste, vollständige Reason-/Warning-Texte).

**Interfaces (Produces, gelesen von Engine und Oberflächen):**
- `times[].id` ∈ {`schnellstart` (stage_minutes null), `stunde` 60, `abende` 150, `gruendlich` 180}; `default_time:
  abende`; `default_goal: alltag`; `skim_percent: 30` (ganzzahlig: skim = ⌈minutes · 30 / 100⌉, gleich in Python und JS); `quickstart_warn_minutes: 180`
- `minimum_path: [S0.1, S1.1, S1.2, S1.5, S1.6, S1.10, S1.13, S1.14, S1.16, S1.19]` (unter `requires` geschlossen)
- Reason-Codes: `new, heard, deep-focus, known, scenario-gap, safety-floor, prerequisite, not-goal, after-quickstart,
  practice, capstone, community, assess, override`; Warning-Codes: `override-safety, override-prereq, quickstart-long`

- [ ] Commit `feat(library): shelves, placement rules and binding chapter metadata`.

### Task 4: Einstufungs-Engine (`tools/placement.py`) und Vertrag

**Files:**
- Create: `tools/catalog_core.py`, `tools/placement.py`, `tools/fixtures/placement-catalog.json` (erzeugt aus
  `docs/migration/chapter-meta.yaml` + `_shelves.yaml` + `_placement.yaml` mit `python tools/catalog_core.py
  --from-meta`), `tools/fixtures/placement-vectors.json`, `tools/fixtures/placement-golden.json`, `tools/test_placement.py`

**Interfaces:**
- Consumes: `docs/migration/chapter-meta.yaml`, die Daten aus Task 3.
- Produces:
  - `catalog_core.core_catalog(entries: list[dict], shelves: list[dict], placement: dict) -> dict` — reine Funktion,
    in Task 5 für den echten Katalog wiederverwendet. Kapitelfelder: `id, type, shelf, level, minutes, order, session,
    requires, requires_all (transitiv, nach order sortiert), safety_floor, offers, area`; oben `placement` (Regeln
    unverändert) und `shelves`.
  - `placement.place(catalog: dict, answers: dict) -> dict` mit Ausgabe `{version: 1, chapters: [{id, status, reason,
    stage, override}], stages: [{n, minutes}], totals: {work_min, skim_min}, warnings: [{code, ids}]}`; `chapters` nach
    `order`; `stage` = null für `skip`/`later`; `warnings` nach (code, ids) sortiert, `ids` nach `order`.
  - Answers `{version: 1, goals: [id], time: id, areas: {area: 0|1|2|null}, scenarios: {id: option_id|null},
    overrides: {chapter_id: status}}`; fehlende Schlüssel → Defaults (`goals` → [`alltag`], `time` → `abende`,
    Bereiche → 0); mehr als zwei Ziele → die ersten zwei; **unbekannte IDs → `ValueError`** (die Oberflächen erzeugen
    nur gültige IDs, der Fehler zeigt Programmierfehler früh).
  - CLI `python tools/placement.py --answers <datei> [--catalog resources/library/catalog.json] [--format json|md]`;
    `--template` gibt ein leeres Antwort-Dokument aus; `--write-golden` (nur Pflege) schreibt die Golden-Datei.
- Algorithmus: Spec §6.3 A–F wörtlich. Reason-Zuordnung: B r=0 → `new`, r=1 → `heard` (deep-dive → `deep-focus`),
  r=2 → `known`, Szenario-Deckel wirksam → `scenario-gap`; Praxis → `practice`, Capstone → `capstone`, Community →
  `community`; Nur-Einschätzen-Herabstufung → `assess`; C → `safety-floor`; D → `prerequisite`; E → `override`;
  `later` → `not-goal` bzw. `after-quickstart`.

- [ ] **Step 1: Vektoren schreiben.** `placement-vectors.json` mit den 14 Personas aus Spec §6.3; jede Persona hat
  `answers` und `expect` mit **handgeschriebenen Kernaussagen** (aus Spec + `chapter-meta.yaml` abgeleitet, unabhängig
  vom Code): Status und Grund ausgewählter Kapitel, Warnungen, Etappenzahl, IDs der ersten Etappe. Vorgerechnet:
  - P01 Anfänger `alltag` `abende`: erste Etappe = S0.1, X.2, S1.1–S1.9 (20 + 4 + 12·4 + 15·4 + 12 = 144 Min; mit
    S1.10 wären es 159 > 150); X.2 `skim` (`community`, 30 % von 12 = 4 Min), S2.6 `later` (`not-goal`), S1.20 `work`
    (`practice`).
  - P02 Anfänger `schnellstart`: genau die 10 Mindestpfad-Kapitel `work`, eine Etappe (152 Min), alles andere `later`
    (`after-quickstart`), keine Warnung.
  - P03 alles 2 + `security`: alle 9 Sicherheitsboden-Kapitel `skim`, S0.1 `skip`, Praxis-Stationen `later`, X.1/X.2
    `skim`.
  - P04 Nur-Einschätzen `gruendlich`: Grund-Kern `skim` (`assess`), S1.5/S1.6/S3.8/S3.9 `work` (`safety-floor`), S4.8
    `skim`, X.1/X.2 `later`.
  - P05 `automation`, basics 2, hooks 0, Szenario `hook-crash` falsch: S0.1–S1.4 `skip`, S2.6–S2.10 `work`, S4.4 `work`.
  - P06 Ziel `security`, alles 0, Übersteuerung S2.8 → `skip`: S2.8 `skip`, Warnung `override-safety` [S2.8] und
    `override-prereq` für jedes empfohlene Kapitel mit S2.8 in `requires_all`.
  - P07 Ziel `alltag`, Übersteuerung S1.16 → `skip`: `override-prereq` für S1.17 und S1.18.
  - P08 `team` + `agents`, alles 0: Hooks-, Plugins-, Security-, Agents-, Automation-Kapitel relevant, S4.8 `work`.
  - P09 `moderieren`: alle S-Kapitel in R, X.1/X.2 `later`.
  - P10 nur `goals: [alltag]` → Ausgabe identisch zu P01.
  - P11 Ziel `alltag`, `mcp: 2`: S2.17 `skim` (`safety-floor`), S2.14 `later`.
  - P12 alle Bereiche `null`, Ziel `automation` → identisch zu „alles 0".
  - P13 Zeitfrage fehlt, Ziel `alltag` → identisch zu P01.
  - P14 `stunde`, Ziel `alltag`: erste Etappe = S0.1, X.2, S1.1, S1.2, S1.3 (genau 60 Min; S1.4 ergäbe 72).
  (Die Zahlen hängen an `chapter-meta.yaml`; weicht die Engine ab, wird zuerst die Rechnung hier geprüft, dann der Code.)
- [ ] **Step 2: Failing tests:** `test_vectors_core` (Kernaussagen je Persona), `test_prerequisites_recommended_or_
  skipped`, `test_stages_are_contiguous_in_order`, `test_stage_budget` (jede Etappe ≤ Budget oder genau ein Kapitel),
  `test_deterministic`, `test_unknown_ids_raise`, `test_cli_template_roundtrip`, `test_golden_outputs` (vollständige
  Ausgabe je Persona = `placement-golden.json`; die Golden-Datei liest der Orchestrator einmal vollständig und gibt sie
  frei; sie ist die Grundlage der JS-Parität in Task 11).
- [ ] **Step 3:** `catalog_core.py` und `placement.py` implementieren (nur Standardbibliothek).
- [ ] **Step 4:** PASS; Golden-Datei erzeugen, jede Persona lesen, Auffälligkeiten an der Spec klären.
- [ ] **Step 5:** Commit `feat(placement): reference engine, contract catalog and vectors`.

### Task 5: Generatoren und `check`

**Files:** Modify `tools/build_library.py` (`build`, `check`); Create `tools/test_build_library_generate.py`.
Generiert (committet): `resources/library/catalog.json`, `resources/library/README.md`, `resources/library/einstufung.md`,
`resources/paths/README.md`, `resources/paths/live-workshop.md`, `resources/paths/schnellstart.md`,
`resources/paths/ziel-<goal>.md` (7), `resources/reference/analogien.md` (aus „Bild im Kopf"), Meta-Blöcke in allen Kapiteln.

**Interfaces:**
- Consumes: `load_library`, `validate`, `catalog_core.core_catalog`, `placement.place`
- Produces: `build_outputs(lib) -> dict[Path, str]` (rein); `build` schreibt (UTF-8, LF); `check` vergleicht
  zeilenend-normalisiert und listet veraltete Dateien (Exit 1). `catalog.json` = `core_catalog(...)` + Anzeigefelder
  `title, file, outcome, aliases, sources, skip_check, glance, analogy, example, example_lang, checkpoint, quiz,
  transferable` (JSON `sort_keys=True, ensure_ascii=False, indent=1`).
- Meta-Block je Kapitel: Zeile 1 Regal-Link · Stufe (Kern/Vertiefung/Kür) · ~N Min · Voraussetzungen als Links ·
  „🛡 Sicherheitsboden" nur wenn true; Zeile 2 ← vorheriges Kapitel · Bibliothek · nächstes Kapitel →.
- Pfade: `live-workshop.md` = Sessions 0–4 mit Minutensummen je Stufe; `schnellstart.md` = Engine mit `{time:
  schnellstart}`; `ziel-<goal>.md` = Engine mit `{goals: [<goal>], time: abende}` (Etappen als Abschnitte).
- **Vertrag** (Validator-Regel `meta-contract`): Felder `id, type, shelf, level, minutes, requires, safety_floor, offers,
  after` jedes Kapitels = `docs/migration/chapter-meta.yaml`. Wer sie ändert, erzeugt Meta-Datei, Kontrakt-Katalog und
  Golden-Datei bewusst neu.

- [ ] Tests: Build über die Fixture-Bibliothek → erwartete Dateien; `check` nach `build` sauber; Titel ändern → README,
  Katalog und das Kapitel veraltet; CRLF-Arbeitskopie → `check` sauber; `requires_all` transitiv; `live-workshop.md`
  nennt Sessions 0–4 mit Summen; `analogien.md` enthält jede Kapitel-Analogie genau einmal.
- [ ] Commit `feat(library): generators for catalog, overviews, paths and meta blocks`.

**Gate A (nach Task 5):** Codex-Verifier (read-only) auf Tasks 1–5 gegen Spec §4, §6, §7. Befunde an der Quelle prüfen,
beheben, erst dann Phase 2.

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
- [ ] **Step 2:** `python tools/build_library.py validate --chapter <datei>` je Datei grün; `python tools/migration_ledger.py --chapter S2.x` ohne fehlende Snippets außer begründet.
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
- Create: `resources/reference/` (README + 9 Karten + glossar, faq, adoptionsplan-vorlage, kosten-nachbau; `analogien.md` erzeugt Task 5), `resources/moderation/` (README, handbuch, vorbereitung, videos), `resources/media/` (Video-Folien, mp3, mp4)
- Move (git mv, unverändert): `resources/review-*` → `docs/reviews/<datum>/…`, `resources/deck-audit-2026-05-21.md`, `dry-run-…`, `final-gap-sweep-…` → `docs/reviews/2026-05-21/`, `HANDOFF.md` → `docs/reviews/2026-06-21/HANDOFF.md`
- Delete (git rm): `resources/modules/`, `resources/demos/block-*.md`, `resources/exercises/`, `WORKSHOP_EINFUEHRUNG.md`, `resources/workshop-guide.md`, `resources/session-plan.md`, `resources/prerequisites.md`, `resources/cheatsheet.md`, `resources/quick-reference.md`, `resources/faq.md`, `resources/troubleshooting.md`, `resources/glossary.md`, `resources/security-analogies.md`, `resources/trainer-notes.md`, `resources/live-3-person-mode.md`, `resources/retrieval-recap-bridges.md`, `resources/transfer-retention-plan.md`, `resources/capstone-exit-assessment.md`, `resources/video-scripts.md`, `resources/archive/workshop-learning-dashboard-legacy.html`, alte Decks (erst in Task 16)
- Modify: `tools/test_course_hooks.py` (Live-Dateien = `resources/**/*.md` + Cockpit + Mentor, Gegenprobe bleibt), `tools/lint_currency.py` (Review-Archiv-Regel: `docs/` ist ausgeklammert; toten Sonderfall entfernen), `tools/currency_exceptions.txt` (Begründungstexte auf neue Pfade), `resources/_canonical.md` Z. 68 (Quellenhoheit statt `session-plan.md`). **Nicht** in diesem Task: `test_course_ci_auth.py` und `test_workshop_ui_behavior.py` — das alte Cockpit bleibt bis Task 10 unverändert im Repo, beide Tests laufen bis dahin unverändert gegen es.
- [ ] **Step 1:** Referenzkarten schreiben lassen (ein Agent je 3 Karten) aus cheatsheet/quick-reference/glossary/faq/troubleshooting mit Doku-Links und Prüfstempel `Geprüft: 2026-09-30 · CLI 2.1.285` (aus Kanon); Widersprüche aus Spec Anhang B korrigiert.
- [ ] **Step 2:** Moderations-Handbuch aus trainer-notes/live-3/recap/transfer/session-plan-Begründungen.
- [ ] **Step 3:** `grep -rn` nach allen alten Pfaden in Live-Dateien → 0 Treffer (Test `test_no_links_to_removed_files`).
- [ ] **Step 4:** Ledger ohne xfail grün; alle Tools-Tests grün (das alte Cockpit ist noch da); Lint OK.
- [ ] **Step 5:** Commit `refactor: move reviews to docs, retire the old module files`.

**Gate B (nach Task 9):** Codex-Verifier auf die Migration (Stichprobe: 10 zufällige Kapitel gegen `ba222d2`-Quelle, alle Sicherheitsboden-Kapitel vollständig). Cockpit-Nachweise sind nicht Teil von Gate B (Task 10–12).

## Phase 3 — Cockpit

### Task 10: Cockpit-Build (`tools/build_cockpit.py`)

**Files:**
- Create: `tools/cockpit/template.html` (Gerüst, CSS, JS-Platzhalter `/*@@LIBRARY_DATA@@*/`), `tools/build_cockpit.py`, `tools/test_build_cockpit.py`
- Modify: `tools/build_library.py` (`build` ruft `build_cockpit.render(lib)`), Output `resources/claude-code-workshop-ui.html`; `tools/test_course_ci_auth.py` (neuer JSON-Parser für den Datenblock, Anzahl Beispiele = Kapitel mit `cockpit:example`, Negativprobe) im selben Task

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

- [ ] `tools/render_diagrams.py` (eigener, optionaler Schritt, nicht Teil von `build`/`check`): Mermaid-Blöcke aller Kapitel mit Playwright + Mermaid (Download nach `tools/.cache/`, nicht committet) nach `resources/library/diagrams/<sha8>.svg` (committet, dunkles Thema); Renderfehler = Exit 1. `build` bettet ein vorhandenes SVG mit passendem Hash ein (bereinigt: keine `<script>`, keine Event-Attribute), sonst Mermaid-Quelltext + GitHub-Link.
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

### Task 16b: Über den Tellerrand — Pi Agent und OpenClaw (Owner-Idee 2026-09-30, nach der Migration)

- [ ] Zwei Community-Kapitel `x-03-pi-als-spiegel.md` (X.3, after S3.2: was ein Harness ist, was Claude Code darüber
  hinaus leistet) und `x-04-agenten-im-dauerbetrieb.md` (X.4, after S4.6: Gateway, Zugangsdaten, Härtung, Not-Aus,
  typische Betriebsfehler), Typ `community`, Stufe `bonus`, relevant nur für die Ziele `agents`, `security`,
  `einschaetzen` (Regel in `_placement.yaml`, Vektoren ergänzen).
- [ ] Quellen: offizielle Doku/Repos (per curl/WebFetch belegt, Lizenz), `~/Desktop/pi-agent/` und das OpenClaw-Vault
  (nur verallgemeinerte Lehren). **Sweep vor Commit:** keine Hosts, IPs, Bot-/Gruppennamen, Pfade der privaten Instanz.
- [ ] Doku-URLs in die Quellenliste des Kanons (`resources/_canonical.md`), damit der Monatslauf sie mitprüft; Kapitel
  tragen „Geprüft: <Datum>".
- [ ] Prüfer-Agent (Aussagen-Matrix gegen die Quellen), Validator, `chapter-meta.yaml`, Kontrakt-Katalog und Golden
  neu erzeugen; Commit `docs(library): beyond Claude Code — Pi and OpenClaw`.

## Phase 6 — Abnahme

### Task 17: Gesamtprüfung

- [ ] `python tools/build_library.py validate --complete` · `python tools/build_library.py check` · `python -m pytest tools -q` · `python tools/lint_currency.py` · `python tools/currency_check.py --state-dir .currency/manual` (erwartet: nur Haiku-Retirement rot; Cockpit-Abweichung zur Website ist erwartet, bis der Owner exportiert) · `cd workshop-playground && python -m pytest -q`.
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
