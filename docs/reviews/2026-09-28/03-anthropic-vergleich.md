# 03 — Anthropic-Vergleich (Delta-Bewertung 2026-09-28)

> Vergleich des Kurs-Curriculums (65 LE, `resources/session-plan.md`, Modultexte
> `resources/modules/block-*.md`) gegen öffentlich zugängliches offizielles Anthropic-Lernmaterial.
> Format nach `00-SCHEMA.md`. Nur lesend recherchiert, keine Logins/Registrierungen.

## Offizielle Quellen (gefunden, öffentlich zugänglich, kein Login nötig)

| # | Quelle | URL | Umfang/Format | Stand |
|---|---|---|---|---|
| Q1 | Claude Code Docs — Overview | https://code.claude.com/docs/en/overview | Doku-Seite, Get-started-Tabs + Feature-Accordions | live, kein Datum sichtbar |
| Q2 | Claude Code Docs — Best Practices | https://code.claude.com/docs/en/best-practices | Lange Guide-Seite (Redirect-Ziel von `anthropic.com/engineering/claude-code-best-practices`, 308 Permanent Redirect — der frühere Engineering-Blogpost ist in die Docs verschmolzen) | live |
| Q3 | Claude Code Docs — Common Workflows | https://code.claude.com/docs/en/common-workflows | Rezept-Sammlung, ~10 Abschnitte | live |
| Q4 | Claude Code Docs — Security | https://code.claude.com/docs/en/security | Sicherheits-/Permission-Modell, Best Practices | live |
| Q5 | Claude Code Docs — Permission Modes | https://code.claude.com/docs/en/permission-modes | Referenz aller Modi, Klassifikator-Details (nur Kopf/Tabellenanfang vollständig gelesen, Rest zu groß) | live, nennt CLI-Version v2.1.283 |
| Q6 | Claude Code Docs — Extend Claude Code (Features Overview) | https://code.claude.com/docs/en/features-overview | Entscheidungsleitfaden Skills/Subagents/Hooks/MCP/Workflows | live |
| Q7 | Claude Code Docs — Dynamic Workflows | https://code.claude.com/docs/en/workflows | Vollständige Referenz zu `/deep-research`, `ultracode`, Workflow-Skript-API | live, nennt Versionsgates bis v2.1.271 |
| Q8 | Anthropic Academy — Claude Code in Action | https://academy.claude.com/courses/claude-code-in-action (früher `anthropic.skilljar.com/claude-code-in-action`) | Kurs-Syllabus: 4 Module, 9 Lektionen, 1 Quiz, ~1h, Completion Badge | live, kostenlos |
| Q9 | Anthropic Academy — Claude Code 101 | https://academy.claude.com/courses/claude-code-101 | Kurs-Syllabus: 5 Module, 12 Lektionen + Quiz, ~1,5h, Completion Badge | live, kostenlos |

Alle Fetches erfolgten öffentlich ohne Anmeldung. Der Skilljar-Link leitet/verweist heute auf `academy.claude.com` — das ist die aktuelle Plattform.

---

## Befunde

**A-01**
- Art: `veraltet`
- Schwere: `P1`
- Ort: `resources/modules/block-1-foundations.md:283` (S1.6, ⭐ Audience-Fit-Core-LE)
- Beleg: Kurs-Tabellenzeile: *„**auto** | ML classifier decides risk level (Max-Plan with Opus 4.8, plus Team/Enterprise)"*. Offiziell (Q5/Q4): *„With Claude Code v2.1.283 or later, auto mode is the built-in starting permission mode for interactive terminal and VS Code sessions. On earlier versions, it's the built-in starting permission mode only on Pro, Max, and Team plans."*
- Befund: Zwei Fehler gleichzeitig — (1) der Kurs nennt nur „Max-Plan", offiziell war/ist `auto` auch auf **Pro**-Plan Standard (ältere CLI-Versionen); (2) entscheidender: auf der laut `00-SCHEMA.md` aktuellen CLI-Version (2.1.283) ist `auto` inzwischen der **Standard-Startmodus für ALLE interaktiven Sessions**, unabhängig vom Plan. Das ist genau die vom Kurs zitierte Version — der Kurs beschreibt also einen veralteten Gating-Stand für die eigene Referenzversion, in der ⭐-markierten Core-LE für die Zielgruppe.
- Vorschlag: Tabellenzeile korrigieren: „auto = Standard-Startmodus ab CLI 2.1.283 für alle, davor Pro/Max/Team."
- Aufwand: `S`

**A-02**
- Art: `fehlt`
- Schwere: `P2`
- Ort: Ziel-LE `S1.14` (Plan Mode & Explain/Propose/Refine/Execute)
- Beleg: Q2, Abschnitt „Let Claude interview you": *„For larger features, have Claude interview you first... using the AskUserQuestion tool... write a complete spec to SPEC.md... start a fresh session to execute it."* Im Kurs kommt `AskUserQuestion` nur als Tool-Name in einer Referenztabelle vor (`block-1-foundations.md:229`), nicht als gelehrte Technik.
- Befund: Eine von Anthropic explizit empfohlene Technik für größere Features (Claude befragt den User strukturiert, schreibt SPEC.md, frische Session für die Umsetzung) fehlt im Kurs als benanntes Pattern.
- Vorschlag: Kurzbeat in S1.14 ergänzen: Interview-Pattern + Beispielprompt + SPEC.md-Workflow.
- Aufwand: `S`

**A-03**
- Art: `fehlt`
- Schwere: `P3`
- Ort: Ziel-LE `S1.10` (CLAUDE.md: die Projekt-Standing-Orders)
- Beleg: Q2: *„Keep CLAUDE.md under 200 lines... For a checked-in CLAUDE.md, run `/doctor` and Claude proposes cuts for content it can derive from the codebase."* Kurs (`block-1-foundations.md:394-397`) bleibt qualitativ: *„keep it concise, Claude reads it every session."*
- Befund: Die offizielle Doku gibt heute eine konkrete Zahl (200 Zeilen) und einen automatisierten Pruning-Workflow (`/doctor`) an; der Kurs nur eine qualitative Faustregel.
- Vorschlag: Faustregel „<200 Zeilen" + `/doctor`-Tipp ergänzen.
- Aufwand: `S`

**A-04**
- Art: `fehlt`
- Schwere: `P2`
- Ort: Ziel-LE `S2.11`–`S2.13` (Plugins)
- Beleg: Q1 (*„install a code intelligence plugin to give Claude precise symbol navigation"*), Q2 (Tip im Abschnitt „Install plugins"), Q3 (Tip unter „Find relevant code"), Q6 (eigene Zeile „Code intelligence" in der Feature-Tabelle + im „Build your setup over time"-Trigger). Kurs-Grep auf „code intelligence"/„LSP" in `block-2-ecosystem.md` (Plugin-Modul) ist negativ; `LSP` taucht nur als Tool-Name in `block-1-foundations.md:229` auf.
- Befund: Ein Feature, das die offizielle Doku an mindestens vier Stellen als Standard-Empfehlung für typisierte Sprachen nennt, fehlt im Kurs-Plugin-Modul komplett.
- Vorschlag: Kurzabschnitt in S2.11/S2.13 ergänzen (LSP-Tool + Code-Intelligence-Plugin).
- Aufwand: `S`

**A-05**
- Art: `fehlt`
- Schwere: `P3`
- Ort: Ziel-LE `S2.7` (Die wichtigsten Hook-Events landkarten)
- Beleg: Q4: *„Audit or block settings changes during sessions with `ConfigChange` hooks."* Kurs-Hook-Typen-Tabelle (`block-2-ecosystem.md`, Modul 2.2) enthält `PreToolUse`/`PostToolUse`/`Notification`/etc., aber kein `ConfigChange` oder `PermissionRequest`.
- Befund: Zwei Hook-Typen aus der offiziellen Sicherheits-Empfehlung (Team-Security-Praxis) fehlen in der Hook-Types-Landkarte.
- Vorschlag: Zwei Zeilen in der Hook-Types-Tabelle ergänzen.
- Aufwand: `S`

**A-06**
- Art: `veraltet`
- Schwere: `P3`
- Ort: `resources/modules/block-3-advanced.md:682`
- Beleg: Kurs: *„Footnote — `ultracode` (research preview)... It's a research preview and may change — noted here only so the name isn't a surprise."* Offiziell (Q7): `ultracode` ist heute ein vollständig dokumentiertes, konfigurierbares Feature mit Settings-Key, Org-Effort-Caps, `/effort ultracode`, Versionsgates (ab v2.1.203) und eigenem Abschnitt „Let Claude decide with ultracode" — keine „research preview"-Kennzeichnung mehr in der Doku.
- Befund: Die Framing als vage/experimentelle Randnotiz spiegelt nicht mehr den aktuellen Doku-Stand (ausführlich spezifiziertes Produktfeature).
- Vorschlag: Fußnote aktualisieren: kurz auf `/effort ultracode`, Org-Caps und Dynamic-Workflow-Verweis (Modul 3.1, Zeile 297) verweisen.
- Aufwand: `S`

**A-07**
- Art: `stärke`
- Schwere: `P2`
- Ort: Kurs durchgängig (Security-Analogien in allen 3 Blöcken)
- Beleg: Alle 9 gefetchten offiziellen Quellen (Q1–Q9) verwenden ausschließlich generische Software-/DevOps-Beispiele; keine einzige Domänen-Analogie-Schicht (z. B. Clearance-Level, Zugangskontrolle, SOPs) in Docs oder Kurs-Syllabi.
- Befund: Das durchgängige Physical-Security-Analogie-Gerüst des Kurses hat kein Pendant im offiziellen Material.
- Vorschlag: keiner (bereits Stärke, ggf. auf Website hervorheben)
- Aufwand: —

**A-08**
- Art: `stärke`
- Schwere: `P2`
- Ort: `workshop-playground/` (durchgängiges Übungsobjekt Block 1–3)
- Beleg: Q8/Q9-Syllabi listen nur Lektionstitel + 1 Abschluss-Quiz, keine mitgelieferte Übungscodebasis oder Lab-Umgebung erkennbar.
- Befund: Ein reproduzierbares, absichtlich verwundbares Repo (5 Sicherheitslücken + pytest-Suite) als durchgängiges Praxisobjekt fehlt im offiziellen Material komplett.
- Vorschlag: keiner
- Aufwand: —

**A-09**
- Art: `stärke`
- Schwere: `P2`
- Ort: `resources/capstone-exit-assessment.md`
- Beleg: Q8/Q9 enden jeweils in einem einzelnen „Course Quiz" + Completion Badge, keine projektbasierte Bewertung sichtbar. Kurs: 6-Dimensionen-Rubrik (0–3-Skala), Passing-Threshold, Session-Entry/Exit-Self-Efficacy-Check (`capstone-exit-assessment.md:24-49`).
- Befund: Eine beobachtbare, mehrdimensionale Skills-Rubrik mit Selbstwirksamkeits-Tracking hat kein offizielles Pendant.
- Vorschlag: keiner
- Aufwand: —

**A-10**
- Art: `stärke`
- Schwere: `P2`
- Ort: `S3.6` (Devil's Advocate, 4-Stage) + `S3.2`/`S4.2` (Claude→Codex→Claude, Codex Swarm)
- Beleg: Q2, Abschnitt „Add an adversarial review step" beschreibt als offizielles Pendant nur **einen** Subagenten, der **einen** Diff gegen Kriterien prüft — kein Multi-Stage-Konsens, kein Cross-Vendor-Aspekt.
- Befund: Die mehrstufige adversariale Security-Pipeline (Scanner→Debate→Consensus→Fixer) plus Multi-Model/Multi-Vendor-Orchestrierung geht deutlich über das offizielle Single-Subagent-Review-Pattern hinaus.
- Vorschlag: keiner
- Aufwand: —

**A-11**
- Art: `fehlt`
- Schwere: `P3`
- Ort: Ziel-LE `S3.1` (Was ist ein Agent?) oder `S4.1` (Multi-Model)
- Beleg: Q1: *„For fully custom workflows, the Agent SDK lets you build your own agents powered by Claude Code's tools and capabilities, with full control over orchestration, tool access, and permissions."* Kurs erwähnt Agent SDK nur als `/claude-api`-Befehlszeile in einer Referenztabelle (`block-2-ecosystem.md:345`), keine inhaltliche Einordnung.
- Befund: Der offizielle „Ausweg" für Teams, die über die interaktive Claude-Code-Oberfläche hinaus eigene Agenten bauen wollen, wird nicht als Konzept eingeordnet.
- Vorschlag: 2-3 Sätze „Agent SDK vs. Claude Code interaktiv" ergänzen.
- Aufwand: `S`

**A-12**
- Art: `unklar`
- Schwere: `P3`
- Ort: `S2.4`/`S3.1` (`/batch`-Erwähnungen)
- Beleg: Q2: *„Run `/batch <instruction>` to have Claude split the change across 5 to 30 subagents."* Ob der Kurs exakt diese Zahl übernimmt oder eine andere, wurde hier nicht tiefengeprüft (gehört strenggenommen zu `02-faktencheck.md`, dort ggf. gegenlesen).
- Vorschlag: Abgleich in `02-faktencheck.md` nachschlagen bzw. dort ergänzen, falls nicht abgedeckt.
- Aufwand: `S`

---

## Format-Ideen für Selbstlernende

Was das offizielle Material für Selbstlerner besser löst und der Kurs übernehmen könnte:

1. **Kurze Lektionsstruktur (9–12 Lektionen à ~5-10 Min) statt langer Textmodule.** Beide Academy-Kurse zerlegen den Stoff in sehr kleine, klar betitelte Häppchen mit direktem Bezug auf einen Befehl/eine Aktion. Der Kurs hat mit den 65 LE strukturell schon eine feine Körnung, aber die Modultexte selbst (`block-*.md`) sind lange Fließtext-Dokumente. **Aufwand: M** (Reformatierung, kein neuer Inhalt).
2. **Shareable Completion Badge/Zertifikat.** Beide Academy-Kurse geben ein Abschluss-Badge aus. Der Kurs hat mit dem Capstone-Rubrik-Score bereits die Bewertungsgrundlage, aber kein ausgebbares Artefakt für LinkedIn/Bewerbungen. **Aufwand: S** (einfaches HTML/PDF-Zertifikatstemplate, das den Rubrik-Score einträgt).
3. **Gehostete Sandbox/Cloud-Session ohne lokale Installation.** Offiziell gibt es `claude.ai/code` als Web-Surface ohne lokales Setup (Q1, Tab „Web"). Für Selbstlerner, die `prerequisites.md` noch nicht durchgearbeitet haben, wäre ein Hinweis „probiere die ersten 2 LE direkt im Browser via claude.ai/code, bevor du lokal installierst" eine niedrigschwellige Einstiegsoption. **Aufwand: S** (nur Doku-Hinweis, keine neue Infrastruktur).
4. **„Related resources"/„Next steps"-Kacheln am Ende jeder Doku-Seite.** Q1/Q6/Q7 enden konsequent mit einer Kartengruppe zu verwandten Themen. Das interaktive Cockpit (`claude-code-workshop-ui.html`) könnte am Ende jeder LE-Sektion automatisch 2-3 verwandte LEs/Demos verlinken. **Aufwand: S** (Datenstruktur für Cross-Links existiert vermutlich schon über die LE-Landkarte).
5. **Inline-Check-Fragen pro Lektion statt nur am Blockende.** Die Academy-Kurse koppeln (laut Struktur) Assessment eng an die Lektion; der Kurs hat laut `session-plan.md` ein „kumulatives Quiz" im Self-Learner-Cockpit, aber die Retrieval-Fragen (`retrieval-recap-bridges.md`) sitzen nur an 3 Session-Übergängen. Mehr Mikro-Checks direkt nach dichten LEs (S1.6, S1.8, S3.6) würden die Lücke zum offiziellen Pro-Lektion-Pattern schließen. **Aufwand: M**.

---

## Positionierung

Das Alleinstellungsmerkmal des Kurses gegenüber dem offiziellen Material ist die Kombination aus **Tiefe und Praxisdichte**: 65 Lerneinheiten über vier ~3h-Sessions stehen zwei kostenlosen Academy-Kursen mit zusammen ~2,5 Stunden und je einem Abschluss-Quiz gegenüber (Q8, Q9) — die offiziellen Kurse sind Produktorientierung, der Workshop ist ein vollständiges Curriculum. Der Kurs hat mit dem absichtlich verwundbaren `workshop-playground/`-Repo (A-08) und der mehrdimensionalen Capstone-Rubrik (A-09) reproduzierbare, bewertbare Praxisartefakte, die im offiziellen Material fehlen. Die durchgängigen Physical-Security-Analogien (A-07) sind eine bewusste didaktische Entscheidung ohne offizielles Pendant — generisch übertragbar, aber zielgruppenscharf. Und bei Security/Multi-Agent-Orchestrierung geht der Kurs mit der vierstufigen Devil's-Advocate-Pipeline und der Cross-Vendor-Pipeline (Claude→Codex→Claude) über das offizielle „ein Subagent prüft einen Diff"-Pattern hinaus (A-10). Kurz: das offizielle Material lehrt, **wie man die Werkzeuge bedient**; der Kurs lehrt zusätzlich, **wie man daraus einen verlässlichen, auditierbaren Arbeitsprozess für ein Team baut** — und dient laut `README.md` explizit als Engineering-Arbeitsprobe, nicht als Produktmarketing.

---

## Zählung

**Nach Art:** `falsch`/`veraltet` = 2 (A-01, A-06) · `fehlt` = 5 (A-02, A-03, A-04, A-05, A-11) · `stärke` = 4 (A-07, A-08, A-09, A-10) · `unklar` = 1 (A-12)
**Nach Schwere:** P1 = 1 (A-01) · P2 = 6 (A-02, A-04, A-07, A-08, A-09, A-10) · P3 = 5 (A-03, A-05, A-06, A-11, A-12)
**Gesamt:** 12 Befunde

## Was ich NICHT prüfen konnte und warum

- **Video-/Lektionsinhalte hinter Academy-Login:** Nur öffentliche Syllabus-/Marketing-Seiten (Q8, Q9) gefetcht, keine Registrierung/kein Login (per Auftrag verboten) — der tatsächliche Lektionstext, exakte Inline-Quiz-Fragen und Video-Skripte der Academy-Kurse bleiben ungeprüft.
- **Skilljar- vs. Academy-Plattform-Historie:** Nicht abschließend verifiziert, ob `anthropic.skilljar.com` noch eigenständig aktiv ist oder vollständig zu `academy.claude.com` migriert wurde — Suchergebnisse und Redirect-Verhalten deuten auf Migration, aber kein direkter Redirect-Test durchgeführt.
- **`permission-modes`-Doku vollständig:** Die Seite war zu groß für einen einzelnen Fetch (>88 KB); nur Kopf/Modus-Tabellenanfang gelesen. Der Abschnitt „How the classifier evaluates actions" und „When auto mode falls back" wurde nicht im Detail gegen den Kurs abgeglichen.
- **Einzelne Feature-Docs (hooks-guide, skills, sub-agents, sandboxing, mcp) nicht seitenweise 1:1 gegen die Kurs-Module geprüft** — Abgleich erfolgte über Kurs-Grep + Erwähnungen in `best-practices`/`features-overview`/`security`, nicht über direktes Fetchen jeder Einzelseite. Größere thematische Lücken in diesen Bereichen sind möglich, aber unentdeckt.
- **PDF „Scaling Agentic Coding Across Your Organization"** (resources.anthropic.com, in der Suche gefunden) nicht gefetcht — potenziell relevant für Team-Rollout-Themen (S2.20/S3.13), aber außerhalb des Zeitbudgets.
- **`/batch`-Subagenten-Zahl (5-30) im Kurs nicht direkt gegengelesen** — als `unklar`/A-12 markiert, Cross-Check gehört zu `02-faktencheck.md`.
- **Pricing-/Modell-Lineup-Vergleich bewusst ausgeklammert** — das ist laut `00-SCHEMA.md` Aufgabe von `01-welt-delta.md`/`02-faktencheck.md`, nicht dieser Datei.
- **Didaktik-Qualität (Aufbau, Pacing, Lernziel-Formulierung) nicht neu bewertet** — laut `00-SCHEMA.md` bereits am 2026-07-04 vollständig geprüft (`review-2026-07-04/`) und hier bewusst nicht wiederholt.
