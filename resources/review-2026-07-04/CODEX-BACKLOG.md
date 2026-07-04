# Dynamic Workshop — Audit & Codex-Backlog (2026-07-04)

> **Zweck:** Codex-tauglicher, Punkt-für-Punkt abarbeitbarer Verbesserungsplan. Didaktik ist die
> durchgängige Hauptlinse; Korrektheit/Currency und UI-Güte kommen hinzu.
> **Methode:** 78-Agenten-Workflow (9 Fach-Analysten je Bereich → adversariale Verifikation jedes
> Korrektheits-Funds → Vollständigkeits-Kritiker) + eigene **Browser-Runtime-QA** der UI (Playwright,
> lokal via `127.0.0.1`) + Capability-RAG-Abgleich für die pro Punkt empfohlene Codex-Fähigkeit.
> **Rohbasis:** 105 Funde → 101 bestätigt, 4 widerlegt (unten dokumentiert), 7 strategische Lücken.
> Konsolidiert zu **28 Work-Packages (WP)**.

---

## 0. Gesamturteil

**Der Workshop ist inhaltlich tief, fachlich stark und im Kern didaktisch sauber durchdacht** — das ist
keine Höflichkeit, sondern der ehrliche Befund: klarer Bloom-Bogen (Foundations → Ecosystem → Agents →
Architektur), ein wirklich gutes **Drei-Schicht-Modell** (`core`/`deep-dive`/`bonus`) mit ehrlicher
Roh-Minuten-Buchhaltung, konsistente und fachlich korrekte Physical-Security-Analogien im Kern, saubere
Custom-vs-Built-in-Kennzeichnung, und eine erstaunlich reife Demo-Schicht (Recovery-Notes, garantierter
Live-Anker in Session 3, Windows-Hook-Fallbacks). Die interaktive UI rendert fehlerfrei, persistiert
Fortschritt und deckt alle 65 LEs mit Content ab.

**Aber es gibt eine systematische Validitäts- und Delivery-Lücke:** Der Workshop hat viel Maschinerie und
*korrekt aussehendes* Scaffolding, während genau die Schichten fehlen oder veraltet sind, die
entscheiden, ob die Mission („Claude Code eigenständig und produktiv einsetzen") wirklich erreicht wird.
Die fünf strukturellen Kernprobleme:

1. **Zeitbudget — reprioritisiert (kein Blocker).** *Ursprünglich als #1 gewertet.* Auftraggeber-Klarstellung
   2026-07-04: Termin-Länge ist kein Constraint (Content-Vollständigkeit vor Slot-Fitting; Sessions laufen so
   lang wie nötig). Bleibender didaktischer Rest: 213 Min am Stück = Ermüdungs-Firehose → **Pausen + Retrieval**
   einplanen, nicht Inhalt streichen. (Die runtime-belegten 258 Min der UI-„48-Route" bleiben als Zahl korrekt.)
2. **Currency-Drift.** Der gesamte Live-Korpus nennt „Sonnet 4.6"/`claude-sonnet-4-6` (89 Treffer in 22
   Dateien inkl. Mentor, UI, Demos) — aktuell ist **Sonnet 5 / `claude-sonnet-5`**. Kopierbare CLI-Beispiele
   schlagen live fehl. (Der Juni-Review zog Opus 4.8/Fable 5 nach, übersah aber Sonnet.)
3. **Versprochene, aber nicht existierende Navigations-/Mastery-Schicht.** Die `<!-- LE: Sx.y -->`-Anker,
   auf die session-plan und Mentor die LE-Navigation gründen, existieren in **keinem** Modul (0 Treffer).
   Nur 5 Modul-Lernziele für 65 LEs → die meisten LEs haben keine echte „ich kann jetzt X"-Grenze.
4. **Assessment-Theater.** Das prominente „Abschluss-Quiz" ist Low-Bloom-Raterei über eine interne
   Theme-Taxonomie; die Micro-Übung „benotet" per Keyword-Count + Textlänge und setzt ab 70 auto-„erledigt".
   Die exzellenten per-LE-Checkpoints werden nie abgefragt. Kein Instrument misst das Missionsziel.
5. **Zwei primäre Lehrflächen sind pre-Welle-F.** PPT-Deck und `trainer-notes.md` lehren noch die alte
   3-Block/17-Modul-Struktur; die zweite HTML (`workshop-learning-dashboard.html`) zeigt 9 Module statt 65
   LEs. Das Erste, was Teilnehmer sehen, und das Runbook, dem der Trainer folgt, sind veraltet.

**Der eine wichtigste Hebel:** `session-plan.md` kompromisslos als Single-Source-of-Truth setzen und die
zwei veralteten primären Lehrflächen (PPT + trainer-notes) darauf neu bauen — *danach* lohnt die
Detail-Currency-Arbeit, sonst driftet sie beim nächsten Modell-Bump erneut, weil kein kanonisches Registry
das verhindert.

### Urteil zur Struktur/Sinnhaftigkeit
Der 65-LE/4-Session-Aufbau ist **grundsolide und lernlogisch sinnvoll** — die Zerlegung, die Session-Grenzen
(Kern vs. Overflow), die Just-in-Time-Verschiebung der Cost-Tiefe und die Level-Klassifikation sind gut
begründet. Die Sinnhaftigkeit wird **nicht** durch den Aufbau untergraben, sondern durch (a) das nicht
tragfähige Zeitbudget, (b) die fehlende Umsetzung der versprochenen Feinstruktur (Anker, Mastery-Grenzen,
Inter-Session-Retrieval) und (c) einen möglichen Format-vs-Kohorten-Mismatch (MOOC-Skalen-Maschinerie für
N=3 Live-Teilnehmer).

### Urteil zur UI
**Korrektheit:** rendert fehlerfrei, 0 Konsolenfehler, Interaktionen (Progress-Persistenz, Route-Toggle,
Grading) funktionieren, `prefers-reduced-motion` (CSS) gehandhabt. **Aber:** stale Modell-IDs, eine
Titel-Heuristik mit falschem Quiz-Antwortschlüssel, ein deterministischer „Shuffle" (Positions-Tell),
CDN-Font-Abhängigkeit, und mehrere A11y-Verstöße (Kontrast 3.36:1, kein `:focus-visible`, Fokusverlust bei
Re-Render). **Didaktik:** Die Struktur (Konzept→Analogie→Beispiel→Checkpunkt→Slides→Quiz→Übung→Heatmap) ist
reich und motivierend, aber das Tactical-Theming (Vollbild-„ACCESSING SECTOR"-Flash pro Navigation,
Amber-Flicker) ist teils *extraneous cognitive load*, das Assessment ist gaming-anfällig, und die
route-abhängige Zeitüberbuchung bleibt unsichtbar. Das Amber/Dunkel-Security-Framing selbst ist ein
sinnvoller motivierender Anker und sollte **bleiben** — nur entschlackt.

---

## Legende

**Severity:** `P1` = blockt Lernen / faktisch falsch / Live-Fail-Risiko · `P2` = schwächt Didaktik/Qualität
spürbar · `P3` = Politur.
**Codex-Fähigkeit** (pro Punkt, aus dem Capability-RAG gewählt):
- `claude-api` (Skill) — autoritative Model-IDs/Pricing/Effort/Flags.
- `context7` (MCP) — aktuelle CLI-/Feature-Docs zur Existenz-Verifikation.
- `web-design-guidelines` (Skill) — A11y/WCAG/UX-Audit von UI-Code.
- `frontend-design` (Skill) — Visual-Direction/Hierarchie/Theming-Tradeoffs.
- `modern-web-design` (Skill) — Layout/Interaktion/Responsive.
- `dataviz` (Skill) — Heatmap/Progress/Minuten-Budget-Visualisierung.
- `tdd` (Skill) — Regressionstest-getriebene Fixes (Lint/Generator/Shuffle).
- `structural-assertion-hygiene` (Skill) — Section→Theme-Map + Pin-Tests in der UI.
- `superpowers:writing-skills` — Mentor-Agent/SKILL.md-Konsistenz.
- **Bereich: Curriculum-/Didaktik-Redaktion** — sorgfältiges Content-Editing gegen `session-plan.md` als SSOT.
- **Bereich: Cross-File-Konsistenz-Sweep** — regex-restringierter Massen-Replace + Re-Grep (historische Kontexte schützen).

---

# TIER 0 — Fundament (zuerst; entriegelt den Rest)

> **STATUS 2026-07-04 (Claude, in-Session umgesetzt):**
> - **WP-02 ✅ ERLEDIGT** — Sonnet-4.6→Sonnet-5-Sweep (30 Renames/13 Dateien, byte-safe, via `tools/sweep_sonnet5.py`), `claude-opus-4-7`→`4-8`, Effort-Verfügbarkeit auf Opus 4.8/Sonnet 5/Fable 5 angeglichen. Pricing unverändert (Sonnet 5 = $3/$15). UI runtime-verifiziert (0 Fehler, 4 Sonnet-5-Sections). `python tools/lint_currency.py` = grün.
> - **WP-03 ✅ ERLEDIGT** — `resources/_canonical.md` (kanonische Model-IDs + LE-Struktur + Forbidden-Tokens) + `tools/lint_currency.py` (fail-on-drift, Archiv/docs ausgeklammert).
> - **WP-01 ✅ ERLEDIGT (reprioritisiert)** — Auftraggeber-Klarstellung 2026-07-04: **Termin-Länge ist KEIN Constraint** (Content-Vollständigkeit > Slot-Fitting). Damit entfällt die „Core demoten/mergen, um in ~150 Min zu passen"-Hälfte. Umgesetzt: S4-Arithmetik 163→166; Modul-Header B1/B2 auf 4-Session-Realität; S1-Zeitblock von „muss kürzen" auf **Pacing/Pausen-Signal** reframed (Ermüdung via Pausen+Retrieval lösen, nicht Streichen). Strukturelle LE-Merge: **verworfen** (nicht nötig).
> - **WP-04 ✅ ERLEDIGT** — `trainer-notes.md`: 4-Session-Struktur-Korrektiv + SSoT-Zeiger + `python3`→`python`-Fix. **Neues eigenes PPT-Deck** `claude-code-workshop-4session.pptx` (python-pptx generiert, 4-Session-Spine, SOC-Amber-Aesthetik passend zur UI) — das alte pre-Welle-F-Deck bleibt unangetastet daneben. *Visuelle QA limitiert (kein LibreOffice/PowerPoint auf der Box) — strukturell validiert; User/Codex sollte es einmal in PowerPoint gegenchecken.*

## WP-01 · [P1] Zeitbudget ehrlich schließen statt nur „straffen"
**Dateien:** `resources/session-plan.md` (Z.36–38, 70–77, 108, 135, 163, 30) · Modul-Header
`block-1-foundations.md:4`, `block-2-ecosystem.md:4`
**Problem (Cognitive Load):** Die Straffungs-Hebel für Session 1 summieren nur ~20 Min gegen ~63 Min
Überhang → geplanter Overrun. S4-Summe ist 166, nicht „~163" (Arithmetikfehler im „ehrliche-Roh-Zahl"-Doc).
Modul-Header tragen die 3-Session-Altlast „~90 minutes".
- [ ] Jede Straffungs-Maßnahme in `session-plan.md` mit Minuten beziffern.
- [ ] 2–3 schwache Core-LEs strukturell demoten/mergen, bis Roh-Core je Session rechnerisch ≤ ~155 Min fällt
      (z.B. S1.4 in S1.2/S1.3 falten; S1.5+S1.6 Permissions-Overlap kürzen — die 6 Modi *nicht* opfern, siehe WP-… S1.6).
- [ ] Netto-Zielzahl je Session explizit ausschreiben.
- [ ] `session-plan.md:30` und `:163` auf **166** korrigieren; S4-„passt in 180"-Claim auf den core*-Subset beziehen.
- [ ] `block-1-foundations.md:4` und `block-2-ecosystem.md:4` von „~90 minutes" auf die 4-Session-Realität umschreiben.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-02 · [P1] Currency-Sweep: Sonnet 4.6 → Sonnet 5 (+ opus-4-7, + Fable 5, + Kosten reconcilen)
**Dateien (89 Treffer / 22 Dateien):** `cheatsheet.md` (309/312/313/324/365), `glossary.md` (83/159),
`faq.md` (24/30), `quick-reference.md`, `troubleshooting.md:114`, `agents/workshop-mentor.md:171`,
`block-1-foundations.md` (54/227/1038/1117), `block-1-demos.md:507`, `block-3-advanced.md` (199/670/214),
`cloud-code-workshop-ui.html` (1560/1806/1856/1862), `sectionContent.json` (43/289/339/345),
`workshop-learning-dashboard.html` (229/440), `README.md`.
- [ ] `claude-api` konsultieren: kanonische Sonnet-5-ID (`claude-sonnet-5`), In/Out-Pricing, Effort-Verfügbarkeit.
- [ ] Regex-restringierter Sweep `Sonnet 4.6`→`Sonnet 5`, `claude-sonnet-4-6`→`claude-sonnet-5`. **Archiv
      `resources/review-2026-06-21/` ausklammern**, bewusste historische Refs („früher 4.6") nicht mutieren.
- [ ] `block-3-advanced.md:214` `claude-opus-4-7`→`claude-opus-4-8`; stray „Opus 4.7"-Effort-Refs (block-1:237/1101) normieren.
- [ ] Fable 5 in die Multi-Model-Tabelle `block-3-advanced.md:391–396` aufnehmen (fehlt komplett).
- [ ] Kosten-Widerspruch `block-3-advanced.md:405/411/413` (Opus:Haiku = 15x vs 14x vs 5x) auf **ein** Verhältnis reconcilen.
- [ ] Re-Grep `sonnet-4-6|Sonnet 4\.6|opus-4-7` über Live-Dateien = 0 Treffer.
**Codex-Fähigkeit:** claude-api + Bereich: Cross-File-Konsistenz-Sweep

## WP-03 · [P1] Kanonisches Model/LE-Registry + Drift-Lint (Grundursache)
**Problem (Wartbarkeit):** Die 89-Treffer-Drift ist ein Symptom fehlender SSOT; sie kehrt beim nächsten
Modell-Bump garantiert wieder. Die bereits gescheiterte manuelle Currency-Pflege (Juni) beweist es.
- [ ] `resources/_canonical.(md|json)` mit Model-IDs + `current_model` + der 65-LE-Tabelle anlegen.
- [ ] Kleiner Generator/Lint, der failt, sobald eine Datei eine nicht-kanonische Model-ID oder eine nicht in
      der Tabelle stehende LE referenziert. Jetzt laufen lassen → deckt Rest-Drift auf.
**Codex-Fähigkeit:** Bereich: Cross-File-Konsistenz-Sweep + tdd

## WP-04 · [P1] PPT-Deck + trainer-notes auf 4-Session-Spine neu bauen (pre-Welle-F)
**Dateien:** `claude-code-workshop.pptx`, `resources/trainer-notes.md`
**Problem (PPT↔Text-Konsistenz):** Beide lehren noch 3 Blöcke/17 Module/30 Slides — die primäre visuelle
Lehrfläche und der Facilitator-Fahrplan sind die *ältesten* Artefakte.
- [ ] Deck-Outline aus `session-plan.md` ableiten und Deck via `python-pptx` neu generieren: 4-Session-Spine,
      Cost-Engineering-Slide aus dem Session-1-Block entfernen (gehört nach S4.4).
- [ ] `trainer-notes.md` als 4-Session-Run-of-Show neu schreiben (Pairing-Fallback erhalten).
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion (python-pptx-Regeneration) + Cross-File-Sweep

---

# TIER 1 — Navigations- & Konsistenz-Rückgrat („versprochen, aber fehlt")

> **STATUS 2026-07-04 (Codex, in-Session umgesetzt):**
> - **WP-05 ✅ ERLEDIGT** — 65 reale `<!-- LE: Sx.y -->`-Anker in den Moduldateien gesetzt und je LE eine „Ich kann jetzt"-Mastery-Grenze ergänzt; Re-Grep/Count = 65.
> - **WP-06 ✅ ERLEDIGT** — Demo-Skripte mit LE-Bindungen versehen; Exercise-Mapping für 3.4/3.6/3.7/3.8/3.9 ergänzt; S2.20 auf „pick 1 in-session, Rest optional" korrigiert; Block-2-Demozeit 6 Demos/~40 Min.
> - **WP-07 ✅ ERLEDIGT** — Mentor/Projekttexte auf 5 Hook-Typen (`command/http/mcp_tool/prompt/agent`), `auto`-Verfügbarkeit laut Modul und 5 Playground-Vulns synchronisiert; 84%-Sandbox-Zahl als Vendor-Figure gehedged.
> - **WP-08 ✅ ERLEDIGT** — `cloud-code-workshop-ui.html` als kanonische UI dokumentiert; alte 9-Modul-UI nach `resources/archive/workshop-learning-dashboard-legacy.html` verschoben; `HOW-TO-USE.md` angelegt.
> - **WP-09 ✅ ERLEDIGT** — externe `resources/sectionContent.json` entfernt; HTML-inline `sectionContent`/`sectionQuiz` ist die einzige UI-Content-Quelle; historisches Integrationsbriefing entsprechend markiert.

## WP-05 · [P1] LE-Anker + Per-LE-Mastery-Grenzen real machen
**Dateien:** `resources/modules/block-*.md` (0 Anker vorhanden), `session-plan.md:203`, `agents/workshop-mentor.md:41`
- [ ] **Entweder (bevorzugt):** vor jedem LE-Quellabschnitt einen `<!-- LE: Sx.y -->`-Anker setzen (65 Stück),
      abgeleitet aus der „Lerneinheiten-Landkarte"-Spalte je Modul (z.B. `<!-- LE: S1.2 -->` vor „### First: Hello, Claude Code").
- [ ] **Oder:** `session-plan.md:203` + Mentor auf die real vorhandene Landkarten-Tabelle als Mechanismus umschreiben und die Anker-Erwähnung streichen.
- [ ] Je Core-LE eine Ein-Zeilen-„**Ich kann jetzt:** …"-Mastery-Aussage ergänzen (aktuell nur 5 Modul-Lernziele für 65 LEs).
- [ ] Danach Mentor-Navigationsclaim gegen die real vorhandenen Anker re-verifizieren.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-06 · [P2] Demo↔LE-Bindung + Exercise↔LE-Mapping vervollständigen
**Dateien:** `resources/demos/block-*.md`, `resources/exercises/block-3-exercises.md`, `session-plan.md:179–184`
- [ ] Jeder Demo-Sektion eine LE-Bindung geben (Block 1 bindet an alte Modulnummern, Block 2/3 gar nicht).
      Mapping z.B.: 1.1→S1.2, 1.2→S1.9/10, 1.3→S1.13, 1.4→S1.16, 2.1→S2.2, 2.2→S2.8, 2.4→S2.14, 3.1→S3.4, 3.3→S3.6 …
- [ ] Exercise-Mapping in `session-plan.md` um 3.4/3.6/3.7/3.8/3.9 ergänzen (aktuell heimatlos; 3.9 ist laut
      Mentor „strongest domain hook"). 3.6/3.7 → S4.9/S4.10 bzw. S4.3–S4.5.
- [ ] Puffer-Zeit-Widerspruch klären: „pick 2–3" (S2.20=18 Min) vs. „20–25 Min je Übung" ist unmöglich →
      auf „pick 1 in-session, Rest optional" ändern.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-07 · [P2] Mentor-Agent synchronisieren (CLAUDE.md-Sync-Regel)
**Datei:** `agents/workshop-mentor.md`
- [ ] `auto`-Mode-Verfügbarkeit (Modul: Max-Consumer+Team/Ent; Mentor Z.120: Team/Enterprise only) angleichen (Modul ist Referenz).
- [ ] Hook-Execution-Typen: Mentor Z.77 nennt 4, Modul 5 (`mcp_tool`) — via `context7` verifizieren, dann angleichen.
- [ ] 84%-Sandbox-Zahl (Z.183) als Vendor-Angabe hedgen (wie `block-3-advanced.md:781`).
- [ ] Vuln-Zahl: Projekt-`CLAUDE.md` sagt „3 geplante Vulns", Mentor/Übung sagen 5 — auf 5 vereinheitlichen.
**Codex-Fähigkeit:** superpowers:writing-skills

## WP-08 · [P2] Zwei divergente Lern-UIs → eine kanonische
**Dateien:** `resources/cloud-code-workshop-ui.html` (65 LE, im README), `resources/workshop-learning-dashboard.html` (9 Module, Cyan, nicht im README), `HOW-TO-USE.md`
**Problem:** Widersprüchliche mentale Modelle (65 LE vs 9 Module, Amber vs Cyan, 48-Route vs 0/9). Dashboard
enthält zusätzlich stale Fakten (Sonnet 4.6; `auto`-Mode falsch beschrieben).
- [ ] Kanonische UI festlegen: `workshop-learning-dashboard.html` **löschen/archivieren** (empfohlen — vom Cockpit überholt) *oder* aus 65-LE-Daten neu generieren + Theme angleichen.
- [ ] In `HOW-TO-USE.md` dokumentieren, welche Datei der Einstieg ist.
**Codex-Fähigkeit:** frontend-design + Bereich: Cross-File-Konsistenz-Sweep

## WP-09 · [P2] `sectionContent.json`-Verwaisung auflösen
**Dateien:** `resources/sectionContent.json` (983 Z.), `resources/cloud-code-workshop-ui.html`
**Problem:** Der Content wurde als `const sectionContent` inlined; die JSON wird zur Laufzeit **nicht** geladen → zwei Wahrheitsquellen, Drift-Risiko bei jedem Content-Edit.
- [ ] Entscheidung: JSON **löschen** (Inline ist SSOT) *oder* HTML per `fetch` daraus speisen *oder* Build-Step, der inlined. Danach nur noch **eine** Quelle pflegen.
**Codex-Fähigkeit:** Bereich: Cross-File-Konsistenz-Sweep

---

# TIER 2 — UI-Korrektheit & Barrierefreiheit

> **STATUS 2026-07-04 (Codex):**
> - **WP-10 ✅ ERLEDIGT** — `sections`-Array hat jetzt ein explizites `theme`-Feld pro Section; `themeFor(s)` bevorzugt `s.theme` vor dem alten Titel-Fallback. Strukturcheck: 65/65 Themes; Pins S2.4=`skills`, S3.4=`agents`, S3.6=`agents`, S3.7=`guardrails`.
> - **WP-11 ✅ ERLEDIGT** — `--muted` auf `#8a9b80`, globale `:focus-visible`-Regel, Suchfeld-`aria-label`, Map-Labels 10.5px, Fokus-Restore nach `renderAll()` und JS-Flash/Blink/Scan-Line bei `prefers-reduced-motion: reduce` deaktiviert. Dashboard war bereits in Tier 1 archiviert.
> - **WP-12 ✅ ERLEDIGT** — Google-Fonts-`preconnect`/Stylesheet entfernt; `--sans`/`--mono` nutzen nur noch System-Font-Stacks. Browser-Smoke: 0 externe Requests beim Laden der lokalen HTML.
> - **WP-13 ✅ ERLEDIGT** — `shuffle()` ist jetzt echte Fisher-Yates-Permutation mit `Math.random()` statt deterministischem Hash-Sort; tote `hash()`-Hilfsfunktion entfernt; Regressionstest `tools/test_workshop_ui_behavior.py` ergänzt.

## WP-10 · [P2] Falscher Quiz-Antwortschlüssel durch Titel-Heuristik
**Datei:** `resources/cloud-code-workshop-ui.html` (Z.1419–1426 `themeFor`, 2717 Antwortschlüssel, 2524 keywordsFor)
**Problem:** `themeFor()` klassifiziert per Titel-Substring und ist Quiz-**Lösung** *und* Keyword-Bank.
Falsch: S3.4 „…Pipeline"→`ci` (statt agents), S3.6 „…Security-Pipeline"→`ci`, S2.4 „…/debug…"→`debug` (statt skills), S3.7→`debug`.
- [ ] Explizites `theme`-Feld pro Section im `sections`-Array (Z.1304–1368); `themeFor(s)` auf `s.theme || <fallback>` umstellen.
- [ ] Für die 4 IDs verifizieren, dass Final-Quiz-`correct` und `keywordsFor` stimmen.
- [ ] Optional: struktureller Pin-Test, der Section→Theme fixiert.
**Codex-Fähigkeit:** structural-assertion-hygiene

## WP-11 · [P2] A11y-Paket: Kontrast, Fokus, Labels, Reduced-Motion
**Datei:** `resources/cloud-code-workshop-ui.html` (+ Dashboard, falls es bleibt)
**Runtime-belegt:** `--muted` #5a6b50 = **3.36:1** (WCAG-AA-Fail); **kein `:focus-visible`**; Fokusverlust bei innerHTML-Re-Render.
- [ ] `--muted` (Z.40) auf ≥ ~#8a9b80 (≥4.5:1 auf `--bg` #0c0f0a *und* `--surface` #111810) anheben.
- [ ] Globale `:focus-visible { outline:2px solid var(--accent-primary); outline-offset:2px }`-Regel.
- [ ] Nach Re-Render (setActive→renderAll, Z.2798) Fokus auf das aktive `.nav-item`/`.map-cell` zurücksetzen.
- [ ] Suchfeld (Z.1176) `aria-label`/verstecktes `<label for="search">`; Map-Labels (Z.817) von 9px auf ≥10–11px.
- [ ] JS-Blink (Z.2819–2827) + Flash-Overlay bei `prefers-reduced-motion: reduce` überspringen (CSS-Query erfasst JS nicht).
- [ ] Falls Dashboard bleibt: klickbare `<div>` (Tabs/Karten) → `<button>` bzw. `role/tabindex/keydown` + eigene Reduced-Motion-Regel.
**Codex-Fähigkeit:** web-design-guidelines

## WP-12 · [P3] Google-Fonts-CDN → offline-tauglich
**Datei:** `resources/cloud-code-workshop-ui.html` (Z.8–10)
**Problem:** einzige externe Abhängigkeit; Physical-Security-Trainings laufen oft air-gapped → Font lädt nicht, `preconnect` ist Datenschutz-/Latenz-Leck.
- [ ] Inter + JetBrains Mono als WOFF2/base64 in `@font-face` inlinen (0 externe Requests) *oder* die drei `<link>`-Zeilen entfernen und auf den vorhandenen System-Stack setzen. Danach offline verifizieren (Network-Tab = 0 externe Requests).
**Codex-Fähigkeit:** Bereich: Font-Self-Hosting (inline @font-face / System-Stack)

## WP-13 · [P3] „shuffle" ist ein deterministischer Hash-Sort (Positions-Tell)
**Datei:** `resources/cloud-code-workshop-ui.html` (Z.2846–2847)
- [ ] Echte Fisher-Yates-Permutation (optional seeded pro Render / pro Attempt), damit die Position der richtigen Antwort variiert. Bei bewusstem Determinismus: Funktion in `orderOptions` umbenennen.
**Codex-Fähigkeit:** tdd

---

# TIER 3 — UI-Didaktik (Assessment-Integrität + Theming-Load)

> **STATUS 2026-07-04 (Codex):**
> - **WP-14 ✅ ERLEDIGT** — UI-Exercises werden aus dem konkreten `checkpoint` generiert; Exercise-Score ist nur noch Feedback ohne Auto-Done und ohne Laengen-Score; Kurzquiz rotiert offene Route-Fragen und bucht `q.id`; Final-Quiz nutzt echte `sectionQuiz`-Recall-Fragen; erfolgreiche Quizantworten setzen die geprüfte Section auf Done; Schwelle auf 70 vereinheitlicht.
> - **WP-15 ✅ ERLEDIGT** — Vollbild-`ACCESSING`-Overlay, Scan-Line, Statusbar-`amber-flicker`, Blink-Intervall und kuenstliche `T-xxx`-Sektorcodes entfernt; Statusrail bleibt ruhig mit echten Section-IDs (`Sx.y ACCESSED`), Amber/Security-Framing bleibt erhalten.
> - **WP-16 ✅ ERLEDIGT** — Route-Toggle hat einen Tooltip zur 48/65-Bedeutung; Resource-Links enthalten das `cheatsheet.md`; Session-Bars zeigen aktive Minutenbudgets als `Sx: n Min / ~150` und markieren >150 Minuten rot.

## WP-14 · [P2] Assessment-Überholung: echte Checkpoints prüfen statt Keyword-Gate
**Datei:** `resources/cloud-code-workshop-ui.html` (2610–2642 Übung, 2665–2727 Quizze)
**Problem (Mastery-Grenze/Validität):** Jede LE hat einen präzisen `checkpoint`, der nur als Karte angezeigt,
aber nie abgefragt wird. Stattdessen 3× generischer Reflexions-Task + „Benotung" aus Keyword-Count +
Textlänge + Checkboxen → „done" (≥70) durch Keyword-Stuffing erreichbar. Final-Quiz = Themen-Slug-Raterei
mit fixen Distraktoren. Kurzquiz bucht eine *fremde* Section als „gemeistert". Schwellen-Mismatch 70 vs 78.
- [ ] Micro-Übung pro Section aus dem `checkpoint`-Feld generieren („Demonstriere: <checkpoint>"); generische 3-Task-Liste (2611–2615) ersetzen.
- [ ] Auto-„done"-Gate (2639) entkoppeln: „done" nur per `markBtn`/korrekt beantwortetem Quiz; Exercise-Score = reines Feedback; Längen-Score entfernen.
- [ ] Final-Quiz auf den vorhandenen `sectionQuiz`-Pool umstellen (echte q/correct/wrong-Recall-Fragen der bereits gesehenen Route) statt Themenfamilien-Zuordnung.
- [ ] Kurzquiz-Erfolg auf die tatsächlich geprüfte `q.id` buchen, nicht auf `s.id`; Schwellen 70/78 angleichen.
- [ ] „Quiz bis hierher": Fragen-Auswahl rotieren (Reshuffle / an schwache Sections koppeln) statt fixer Formel.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion (checkpoint-getriebene Exercises)

## WP-15 · [P2] Tactical-Theming entschlacken (extraneous Load raus, Framing behalten)
**Datei:** `resources/cloud-code-workshop-ui.html` (125/1082 Flicker, 1160–1161 Overlay, 2801–2836 setActive)
- [ ] Vollbild-„ACCESSING SECTOR"-Flash pro Navigation entfernen oder auf dezenten, nicht-blockierenden Rahmenpuls reduzieren.
- [ ] `amber-flicker`-Animation (Z.125) entfernen (mindert periodisch die Textlesbarkeit).
- [ ] „SECTOR T-xxx"-Codes an die echten IDs (S1.1) angleichen oder droppen (konkurrieren mit der echten Nummerierung).
- [ ] **Amber/Dunkel-Palette + Security-Framing bewusst behalten** — es ist ein motivierender Anker, nur die Bewegungs-/Doppel-ID-Reibung stört.
**Codex-Fähigkeit:** frontend-design

## WP-16 · [P3] Route-Transparenz: Minuten-Budget sichtbar machen + Toggle erklären + Cheatsheet verlinken
**Datei:** `resources/cloud-code-workshop-ui.html` (2557 Min-Pille, 2772–2784 Session-Bars, 2561–2565 Resource-Links, 1172–1173 Toggle)
**Runtime-belegt:** 48-Route-Minuten pro Session = **258/225/169/51**; S1 also weit über ~150 fahrbar — im Cockpit unsichtbar.
- [ ] Pro Session-Block die Minutensumme der aktiven Route anzeigen (z.B. „S1: 258 Min / ~150 fahrbar"), rot ab > 150.
- [ ] Ein-Satz-Tooltip am Route-Toggle: „48 = Pflicht-Core + frühe Vertiefungen; 65 = komplette Landkarte".
- [ ] Resource-Links um `../resources/cheatsheet.md` erweitern (kanonische Referenzkarte fehlt).
**Codex-Fähigkeit:** dataviz + Bereich: Curriculum-/Didaktik-Redaktion

---

# TIER 4 — Inhaltliche Korrektheit (Module / Demos / Exercises)

> **STATUS 2026-07-04 (Codex):**
> - **WP-17 ✅ ERLEDIGT** — Exercise 2.6 nutzt jetzt PostToolUse statt PreToolUse; Filter-Script gibt JSON mit `suppressOutput: true` und gefiltertem `systemMessage` aus, statt stdout additiv zu drucken. Blueprint #2 in Block 3 und Mentor-Hook-Landkarte sind synchronisiert. context7: Exit-0-stdout wird angezeigt; Suppression braucht Hook-JSON.

## WP-17 · [P2] Exercise 2.6 „Token Firewall" funktioniert mechanisch nicht + Hook-Typ-Fehletikett
**Dateien:** `resources/exercises/block-2-exercises.md` (862/888/926), `block-3-exercises.md:699`
**Problem (context7-verifiziert):** Ein PostToolUse-Hook mit `echo …; exit 0` **ersetzt** die Tool-Ausgabe nicht (stdout wird *zusätzlich* gezeigt) → verspricht Token-Ersparnis, liefert das Gegenteil. Zudem: Goal nennt „PreToolUse", Body korrigiert auf PostToolUse; Blueprint #2 wiederholt den Fehler.
- [ ] Übung auf echten Mechanismus umstellen: JSON-Output `{"suppressOutput": true, "systemMessage": "<gefiltert>"}` *oder* ehrlich als Wrapper-Command (`pytest … | grep …`), das Tokens wirklich reduziert.
- [ ] `block-2-exercises.md:862` „PreToolUse"→„PostToolUse"; `block-3-exercises.md:699` Blueprint analog. Danach Re-Grep „PreToolUse … filter/output".
**Codex-Fähigkeit:** context7

## WP-18 · [P2] Demo-Live-Fail-Risiken & Worked-Example-Lücken
**Dateien:** `resources/demos/block-*.md`
- [ ] **3.3 Pfad-Doppelfehler:** `cd workshop-playground/` (Z.145) + präfixierter Scan-Pfad (Z.151/207) → „Datei nicht gefunden". Eine Variante konsistent wählen.
- [ ] **3.3 fail-OPEN-Vuln fehlt:** Demo nennt nur 3(+1) Vulns; die 5. (fail-open Domain-Logik) ist *das* Domänen-Lesson für die Zielgruppe → nach Step 7 ergänzen + Überleitung zu Exercise 3.3.
- [ ] **3.5 worktree ohne `-b`** (Z.480) scheitert für neuen Branch; Recovery (Z.537) widerspricht sich → `-b` einfügen (wie Demo 1.4).
- [ ] **3.3b verspricht 6 Modi, zeigt 5** (`auto` fehlt, Z.232/285) → ergänzen oder Zahl korrigieren.
- [ ] **Demo 1.4 erzeugt nie einen PR**, obwohl S1.16 „branch→commit→PR" verspricht → Step 5b (`gh pr create --fill`) ergänzen.
- [ ] **Block-1-Demos nutzen `python3`** (Z.18/94) → auf Windows `python` (Block 2 kennt die Regel bereits).
- [ ] **Demo 1.1 hat keine Recovery-Notes** — die allererste Live-Aktion → Sektion ergänzen (claude startet nicht / python-Verwechslung / Datei im falschen Verzeichnis).
- [ ] **Block-1-Demos 3.1/3.2/3.3/3.4 ohne Dauerangabe** (gerade die überzieh-anfälligen Swarm-Demos) → realistische „Duration" + „×1,5 für Live".
- [ ] **Header-Zeitbudget falsch:** `block-2-demos.md:4` „~35 min / 5 Demos" → real 6 Demos/~40 Min (2.2b fehlt).
- [ ] **Demo 2.5 notebooklm ohne `--json`** → cp1252-Bruch auf Windows; `--json` bzw. Recovery-Zeile ergänzen.
- [ ] **Demo 1.2 Memory-Scope** („applies to all projects", Z.216–219) via `context7`/Live prüfen — Auto-Memory ist i.d.R. projekt-scoped.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion (+ context7 für Scope/Flag-Verifikationen)

## WP-19 · [P2] Exercise-Fixes: Mechanik, Scaffolding, Windows
**Dateien:** `resources/exercises/block-1-exercises.md`, `block-2-exercises.md`, `block-3-exercises.md`
- [ ] **2.3** lässt Plugin von Hand in `~/.claude/plugins/cache/` scaffolden + erwartet Auto-Load — widerspricht Loader & globaler CLAUDE.md §12 → auf `claude --plugin-dir ./…` / `--scope local` umstellen; Loader via `context7` verifizieren.
- [ ] **1.5** verlangt Pro-Run-Kostenschätzung von Tag-1-Anfängern — widerspricht der Welle-F-Cost-Verschiebung → $-Spalte durch qualitative Einordnung ersetzen, Verweis auf S4.4.
- [ ] **1.2** überlädt 15-Min-Budget mit 8 Schritten + 2 Neustarts → auf ~22 Min anheben *oder* in 1.2a/1.2b splitten (nur 1 Restart im Kernpfad).
- [ ] **3.1 (Must-do Multi-Agent) hat keinen Success-Check** → beobachtbare Checkbox-Mastery-Grenze ergänzen; 3.4 „Verification" in Checkbox-Form.
- [ ] **Block-1-Warmups (W2/W4)** greifen auf ungelehrte Konzepte vor (PostToolUse-Hook, Worktree) → Analogie-Klammern streichen/umformulieren.
- [ ] **Windows-Lösbarkeit:** POSIX-only Setup-Snippets ab 1.2/1.4 mit PowerShell-Parallele bzw. `# macOS/Linux/Git Bash`-Fence taggen; `echo "…" > file.md` (UTF-16+BOM in PS) → `Set-Content -Encoding utf8`.
**Codex-Fähigkeit:** context7 + Bereich: Curriculum-/Didaktik-Redaktion

## WP-20 · [P2] Modul-Korrektheit & Analogie-Präzision
**Dateien:** `resources/modules/block-2-ecosystem.md`, `block-3-advanced.md`
- [ ] **Turn-Cap-Phantom** `block-3-advanced.md:1471` („budget cap and turn cap") widerspricht Z.700/1355 („no turn-limit flag") und dem YAML → „and turn cap" streichen.
- [ ] **Hook-Events 11 vs 12:** Prosa (Z.409/421) sagt 11, Tabelle listet 12 → auf 12 korrigieren (Tabelle stimmt), auch `session-plan.md:93`.
- [ ] **Bundled-Skills-Namen** (`/batch`, `/debug`, `/run-skill-generator`, Z.328–368) via `context7` gegen aktuelle Harness prüfen (aktuell u.a. `/run`, `/verify`, `/simplify`, `/loop`, `/claude-api`) → anpassen + Mentor Z.110–114.
- [ ] **`/workflows` „hunderte Subagenten"** (Z.289) via `context7` verifizieren; falls nicht belegbar, entschärfen.
- [ ] **Marketplace-Namen** (Z.794/800/804) inkonsistent (`claude-community` vs `claude-plugins-community`) → kanonisieren, `context7`.
- [ ] **Analogie-Leck (Prior-Knowledge):** Stop-Hook als „scheduled/18:00-Uhr" (Z.456) beschrieben — ist event-, nicht zeitgetriggert → umformulieren, Wort „scheduled" streichen.
- [ ] **Windows-Reibung am ersten core-Hook** (S2.8, Z.529) — jq/grep/`bash`, Rettung erst im deep-dive → Ein-Zeilen-Windows-Notiz direkt beim Beispiel + Verweis auf `demos/assets/hooks/`.
- [ ] **Devil's-Advocate-Pipeline** (Z.513) liest sich als Built-in; 🔧-Custom-Marker erst 70 Zeilen später → 🔧-Hinweis direkt unter die Überschrift (Ehrlichkeits-Gebot).
- [ ] **Compliance-LE S3.11** (8 Regularien in 15 Min, Z.828) → EN 50131/50132 + GDPR + NIS2 als audience-Kern markieren; HIPAA/PCI/MiFID als generalisierbares Beispiel.
- [ ] **deep-dive-Inseln** (S2.5 zwischen core, Z.132–198) mit Inline-Level-Tags an Überschriften (`### … [deep-dive · S2.5]`).
**Codex-Fähigkeit:** context7 + claude-api + Bereich: Curriculum-/Didaktik-Redaktion

---

# TIER 5 — Didaktische Tiefe (strategische Kritiker-Lücken)

## WP-21 · [P2] Summative, missions-verankerte Lernzielkontrolle
**Problem:** Kein Instrument misst „eigenständig und produktiv einsetzen". Die vorhandenen Quizze sind keine valide Assessment-Schicht (siehe WP-14).
- [ ] Authentische **Capstone-Exit-Aufgabe** mit beobachtbarer Rubrik: Teilnehmer treibt Claude Code unassistiert (Feature + Hook + PR auf dem Playground).
- [ ] Pro Session ein 5-Item-Entry/Exit-Self-Efficacy-Check.
- [ ] `S4.8` von „Diskussion" auf „bewerteter Build" heben.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-22 · [P2] Transfer-Brücke + Post-Workshop-Retention-Loop
**Problem:** Alles bleibt im synthetischen Playground; die Mission ist Arbeitsalltags-Adoption.
- [ ] Pro Session eine „Bring-your-own-repo"-Transfer-LE (10 Min: heutige Fertigkeit auf ein Job-Repo anwenden).
- [ ] 1-seitiger Take-Home-Adoptionsplan.
- [ ] Geplanter 30-Tage-async-Follow-up (dogfoodet die `/schedule`+Routines aus S3.12).
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-23 · [P2] Retrieval-/Recap-Brücken zwischen Sessions
**Problem (Retrieval & Spacing):** Nur S3 hat einen Opener-Anker; PPT-Start ist passives Review. Bei TBD-Terminen (Wochen Abstand) ist Vergessen hoch.
- [ ] Für S2/S3/S4 je einen 5-Min-Aktiv-Recall-Opener (3–5 Fragen zur Vorsession) **vor** der PPT verankern.
- [ ] In-Session Quick-Checks nach den Analogie-Clustern (z.B. nach S1.6 Permission-Modi, nach S1.10 CLAUDE.md) — optional/unbenotet.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-24 · [P2] Security-Analogien über Session 4 fortführen (inverses Fading beheben)
**Datei:** `resources/security-analogies.md`
**Problem:** Das Signatur-Gerüst bricht über S4 weg — nicht weil die Lerner Mastery erreichten, sondern weil dem Autor die Analogien ausgingen.
- [ ] S4-Konzepte ergänzen + in die S4-LEs verdrahten: Troubleshooting = Alarmpanel-Fehlerisolation (Sensor→Verkabelung→Panel→Comms), CI/CD = automatisierte nächtliche Wachrunde, Multi-Model = Dienstplan-Staffing.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-25 · [P2] Prerequisites deterministisch & self-serve machen
**Datei:** `resources/prerequisites.md`
**Problem:** Unpinned Versions-Gate, harte Moderator-Tarball-Abhängigkeit, unverifizierte Clone-URL, kein Zeitbudget.
- [ ] Getestetes Minimum `claude --version` pinnen + Feature→Version-Tabelle (Fable 5, Dynamic Workflows, Hook-Outputs) — via `context7` verifizieren.
- [ ] Plugins an einen real erreichbaren Ort veröffentlichen (Git-Release/Drive-Link) + Self-Serve-Install-Skript; Clone-URL auf Auflösbarkeit prüfen.
- [ ] „~45 Min, in dieser Reihenfolge"-Zeitbudget + ein Copy-Paste-Doctor-Skript.
**Codex-Fähigkeit:** context7 + Bereich: Curriculum-/Didaktik-Redaktion

## WP-26 · [P3] Cost-Engineering-Verschiebung absichern
**Problem:** S4.4 (die Cost-Tiefe) ist `deep-dive` in der explizit streichbaren Overflow-Session → das relevante Thema droht nie geliefert zu werden.
- [ ] Entweder kompakten Core-Beat „Cost-Reduction-Taktiken" (5 Min: Caching, Effort-Tiers, Modell-pro-Phase) in S1.19 behalten, *oder* den Kosten-Teil von S4.4 ins core*-Fallback-Set (neben S4.9/S4.10) heben.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-27 · [P3] Concrete-before-abstract: Einstiegsrampe korrigieren
**Dateien:** `session-plan.md:49–50`, `block-1-foundations.md` (Landkarte + Objectives Z.50–54)
**Problem:** S1.1 (abstraktes mentales Modell) steht VOR S1.2 (konkret bauen) — kehrt das concrete-first-Design des eigenen Modultexts („do this now") und die Mission („gebaut bevor nachgedacht") um.
- [ ] S1.1 und S1.2 tauschen (Build-First als Opener); Tabellen angleichen.
- [ ] Die zwei „(Comes later)"-Objectives (Permissions/Modellwahl) aus dem Kopf-Block unter die First-Contact-Übung verschieben.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

## WP-28 · [P3] Format-vs-Kohorten-Fit explizit machen (N=3 live)
**Problem:** MOOC-Skalen-Maschinerie (65 sequenzierte LEs, Self-Paced-Cockpit, Completion-Dashboard) für 3 erfahrene Devs live im Raum.
- [ ] 65-LE-Map als Facilitator-Gerüst + Self-Learner-Track behalten, aber einen expliziten „Live-3-Personen-Modus"-Run-of-Show definieren (Think-Aloud-Pair-Driving am Playground + Per-LE-Sokrates-Prompts statt Quizze); Completion-UI auf Self-Learner-Track demoten.
**Codex-Fähigkeit:** Bereich: Curriculum-/Didaktik-Redaktion

---

## Anhang A — Bewusst verworfene Funde (Verifikation widerlegte den Kern)
1. „S4.6 remote-control/`/teleport` unter Wert als bonus verkauft" — Zitate real, aber bonus-Einstufung ist eine legitime Zeit-Entscheidung, kein Fehler.
2. „Unverifizierte Flags in Demos (`/insights`, `--json-schema`, `/plan`, `--bare`)" — existieren an den Stellen; Kernvorwurf „unverifiziert/fiktiv" nicht belegt (separat via context7 als Sammelcheck in WP-20 aufgenommen).
3. „`--bare`/`--effort` im Live-Pfad ungeprüft → Hook scheitert bei jedem Commit" — spekulativ, kein belegter Fehler.
4. „Opus 4.7 als parallel-aktuell dargestellt" — die *echte* stale Stelle ist nur `block-3-advanced.md:214` (in WP-02); der breitere Vorwurf war überzogen.

## Anhang B — Capability-Index (welche Codex-Fähigkeit deckt was)
| Fähigkeit | Work-Packages |
|---|---|
| `claude-api` | WP-02 (Model-IDs/Pricing/Effort) |
| `context7` | WP-07, WP-17, WP-18, WP-19, WP-20, WP-25 (Feature/Flag-Existenz) |
| `web-design-guidelines` | WP-11 (A11y/Kontrast/Fokus) |
| `frontend-design` | WP-08, WP-15 (Theming/kanonische UI) |
| `dataviz` | WP-16 (Minuten-Budget-Viz) |
| `tdd` | WP-03 (Lint/Generator), WP-13 (Shuffle) |
| `structural-assertion-hygiene` | WP-10 (Section→Theme-Map + Pin-Test) |
| `superpowers:writing-skills` | WP-07 (Mentor-Sync) |
| Bereich: Cross-File-Konsistenz-Sweep | WP-02, WP-03, WP-04, WP-08, WP-09 |
| Bereich: Font-Self-Hosting | WP-12 |
| Bereich: Curriculum-/Didaktik-Redaktion | WP-01, WP-04, WP-05, WP-06, WP-14, WP-16, WP-18–WP-28 |

## Anhang C — Empfohlene Reihenfolge für Codex
1. **TIER 0** zuerst (WP-01…04) — schafft die ehrliche Zeitbasis, die Currency-Wahrheit, das Anti-Drift-Registry und die aktualisierten Primär-Lehrflächen.
2. **TIER 1** (WP-05…09) — repariert die Navigations-/Konsistenz-Versprechen, auf die alles andere referenziert.
3. **TIER 2/3** (WP-10…16) — UI-Korrektheit, A11y, Assessment-Integrität.
4. **TIER 4** (WP-17…20) — inhaltliche Live-Fail-Fixes.
5. **TIER 5** (WP-21…28) — didaktische Tiefe (Assessment, Transfer, Retrieval, Format-Fit).

> Nach jedem TIER: `pytest` NUR gegen isolierte Test-DB (hier nicht relevant — kein DB-Code), und für UI-WPs
> eine In-Browser-Runtime-QA (die Diff-Review allein deckt Render-/Interaktions-Bugs nicht auf).
