# 01 — Welt-Delta: Claude-Modelle & Claude-Code-CLI (Stand 2026-09-28)

> Teil der Delta-Bewertung 2026-09-28. Vergleicht Kanon-Stand `_canonical.md` (2026-07-04, CLI 2.1.185)
> gegen den heutigen Stand: offizielle Anthropic-Modelldoku/Pricing (WebFetch, 2026-09-28) und das
> offizielle Claude-Code-Changelog (`github.com/anthropics/claude-code/CHANGELOG.md`, Versionen
> 2.1.186–2.1.283). Format je Schema `00-SCHEMA.md`.

## 1. Modelle — Verifikationsergebnis

**Quellen:** `https://platform.claude.com/docs/en/about-claude/models/overview` (WebFetch, 2026-09-28),
`https://platform.claude.com/docs/en/about-claude/pricing` (WebFetch, 2026-09-28), lokale
`claude --version` / `claude --help`, offizielles CLI-Changelog.

**Aktuelles Lineup (offizielle Vergleichstabelle, Stand Abruf):**

| Modell | Claude-API-ID | Kontext | Max Output | In $/1M | Out $/1M | Cache-Read | Default Effort | Effort-Stufen |
|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 128K | 10 | 50 | 0.025× (≈$0,25) | `high` | low/medium/high/xhigh/max |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | 4 | 20 | 0.05× (≈$0,20) | `medium` | low/medium/high/xhigh/max |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | 2 | 10 | 0.1× (≈$0,20) | `high` | adaptive (kein separates Effort-Sperrverhalten dokumentiert) |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` (Alias `claude-haiku-4-5`) | 200K | 64K | 1 | 5 | 0.1× (≈$0,10) | — kein Effort | „Extended“ Thinking, kein Effort-Parameter |

**Legacy, weiterhin verfügbar (nicht deprecated):** laut Modell-Übersichtsseite wörtlich „Legacy models
(still available)": Claude Fable 5 (`claude-fable-5`, 10/50), Claude Opus 5 (`claude-opus-5`, 5/25),
**Claude Opus 4.8** (`claude-opus-4-8`, 5/25), Claude Opus 4.7, Claude Opus 4.6, Claude Opus 4.5,
**Claude Sonnet 5** (`claude-sonnet-5`), Claude Sonnet 4.6, Claude Sonnet 4.5.

→ **Opus 4.8 und Fable 5 sind bestätigt NICHT deprecated** — Kanon-Annahme aus dem Auftrag stimmt.

**Sonnet-5-Preis-Korrektur (wichtig, siehe W-04):** Pricing-Seite, Fußnote 3, wörtlich: *„The $2/$10
per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory
pricing through August 31, 2026, is now the standard price. The previously scheduled increase to
$3/$15 per million input/output tokens on September 1, 2026 will not occur."*

**Tier-Aliase:** `claude --help` bestätigt wörtlich: *„--model <model> ... Provide an alias for the
latest model (e.g. 'fable', 'opus', or 'sonnet') or a model's full name (e.g. 'claude-fable-5')."*
→ Aliase lösen weiterhin auf die aktuelle Generation auf.

**Claude-Code-Default:** Aus dem offiziellen CLI-Changelog (nicht aus der Modell-Doku, die keinen
Claude-Code-spezifischen Default nennt):
- CLI 2.1.219: *„Added Claude Opus 5 (`claude-opus-5`), now the default Opus model"*
- CLI 2.1.280: *„Added Claude Opus 5.5 (`claude-opus-5-5`), now the default Opus model — 1M context,
  $4/$20 per Mtok with $0.20/Mtok cache reads"* + *„Changed the default model on Pro and Team Standard
  plans from Sonnet to Opus, matching Max, Team Premium, and Enterprise"*
- CLI 2.1.257: *„Added Claude Fable 5.1 (`claude-fable-5-1`), now the default Fable model"*
- CLI 2.1.197: *„Introducing Claude Sonnet 5: now the default model in Claude Code..."*
- **Außerhalb des geprüften CLI-Deltas (>2.1.283), aber schon offiziell live:** CLI-Changelog 2.1.284
  (erste Zeile nach dem geprüften Fenster): *„Added Claude Sonnet 5.5 (`claude-sonnet-5-5`), now the
  default Sonnet model on the Anthropic API — 1M context, $2/$10 per Mtok..."* — siehe W-13.

→ **Der Claude-Code-Default für Opus ist heute Opus 5.5, nicht Opus 4.8.** Zwischen dem Kanon-Stand
(Opus 4.8, 2026-07-04) und heute lag mindestens ein Zwischenschritt (Opus 5, CLI 2.1.219) und der
aktuelle Stand (Opus 5.5, CLI 2.1.280).

---

## 2. CLI-Delta 2.1.185 → 2.1.283 — Methodik

Installierte Version verifiziert: `claude --version` → wörtlich `2.1.283 (Claude Code)`.
Changelog geladen via `curl https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`
(WebFetch auf dieselbe URL timeoutete; curl gelang). Ausgewertet: **alle 99 Versionseinträge** von
2.1.186 bis 2.1.283 (siehe Versionsliste unten), vollständig gelesen (nicht nur gegrept), Bugfix-Rauschen
(VSCode-Extension-Detailfixes, Slack/„Claude Tag"-Admin-UI, Claude-Code-on-the-Web-Spezifika, Code-Review-
Bot-Feinschliff) herausgefiltert, da außerhalb des CLI-Kern-Scopes dieses Workshops.

Geprüfte Versionsspanne (Header aus dem Changelog): 2.1.283, 282, 281, 280, 278, 277, 276, 275, 274,
273, 272, 271, 270, 269, 268, 267, 266, 265, 263, 261, 260, 259, 258, 257, 251, 250, 248, 247, 246, 245,
243, 241, 240, 239, 238, 237, 236, 235, 234, 233, 232, 231, 229, 228, 227, 226, 225, 224, 223, 222, 221,
220, 219, 218, 217, 216, 215, 214, 212, 211, 210, 209, 208, 207, 206, 205, 204, 203, 202, 201, 200, 199,
198, 197, 196, 195, 193, 191, 190, 187, 186.

---

## Befunde

| ID | Art | Schwere | Ort | Beleg | Vorschlag | Aufwand |
|---|---|---|---|---|---|---|
| W-01 | veraltet | P1 | `resources/_canonical.md:12`; `resources/modules/block-1-foundations.md:243,247,1066,1097,1173,1177`; `resources/cheatsheet.md:308,312,314,318,365` | CLI-Changelog 2.1.219: „Added Claude Opus 5 (`claude-opus-5`), now the default Opus model"; CLI-Changelog 2.1.280: „Added Claude Opus 5.5 (`claude-opus-5-5`), now the default Opus model"; platform.claude.com/docs/models/overview listet Opus 4.8 nur noch unter „Legacy models (still available)" | Alle „Opus 4.8 = aktueller Default"-Aussagen im Kanon und in Modul/Cheatsheet auf Opus 5.5 aktualisieren (Preis 4/20 statt 5/25, Default-Effort `medium` statt `high`). Course-Text ("Model names move fast... run `/model`") als Absicherung beibehalten, aber die Live-Aussagen selbst korrigieren. | M |
| W-02 | veraltet | P2 | `resources/cheatsheet.md:163,314` | CLI-Changelog 2.1.219: „Removed Opus 4.7 from fast mode; `/fast` now applies to Opus 5 and Opus 4.8"; Pricing-Seite: Fast Mode heute auf Opus 5.5 ($8/$40), Opus 5 ($10/$50), Opus 4.8 ($10/$50) — Opus 4.7 fehlt in der Fast-Mode-Tabelle | Cheatsheet-Zeile „Opus 4.8/4.7" auf „Opus 5.5/5/4.8" korrigieren, Opus 4.7 explizit als „kein Fast Mode mehr" markieren. | S |
| W-03 | falsch | P1 | `resources/cheatsheet.md:365` | Zitat cheatsheet.md: „auto mode requirements: ... Anthropic API only (not Bedrock/Vertex)"; CLI-Changelog 2.1.207: „Auto mode is now available without `CLAUDE_CODE_ENABLE_AUTO_MODE` opt-in on Bedrock, Vertex AI, and Foundry"; 2.1.278: „Changed auto mode for Claude API and Enterprise users, and on Bedrock, Vertex, Foundry and gateways, to default to the server-side classifier" | Satz streichen/korrigieren: Auto Mode läuft seit CLI 2.1.207 auch auf Bedrock/Vertex/Foundry (zunächst lokaler Classifier, seit 2.1.278 auch dort serverseitig by default). | S |
| W-04 | falsch | P1 | `resources/cheatsheet.md:309` | Pricing-Seite Fußnote 3 (wörtlich siehe Abschnitt 1 oben): „The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur." Cheatsheet zeigt Sonnet 5 fest mit „In: 3 / Out: 15". | Sonnet-5-Preis in der Modelltabelle auf 2/10 (dauerhafter Standardpreis) korrigieren, nicht nur „Einführungspreis bis 31.08." | S |
| W-05 | veraltet | P2 | `resources/glossary.md:17`; `resources/modules/block-1-foundations.md:506` (LE S1.12) | Glossar wörtlich: „Claude Code laedt es nicht automatisch, aber via `@AGENTS.md`-Import ... ist Interop moeglich." CLI-Changelog 2.1.277: „Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead; change it under 'Project instructions' in `/config`." | Glossar/Modul ergänzen: Claude Code liest AGENTS.md heute automatisch als Fallback, wenn kein CLAUDE.md existiert (seit CLI 2.1.277); `@AGENTS.md`-Import bleibt der Weg für Koexistenz mit CLAUDE.md. | S |
| W-06 | veraltet | P3 | `resources/session-plan.md` S1.5/S1.6; `resources/modules/block-1-foundations.md:21-22,267,270,281-285` | `claude --help` Output: `--permission-mode <mode> ... (choices: "acceptEdits", "auto", "bypassPermissions", "manual", "dontAsk", "plan")`; CLI-Changelog 2.1.200: „Changed the 'default' permission mode to 'Manual' across the CLI, `--help`, VS Code, and JetBrains; `--permission-mode manual` and `'defaultMode': 'manual'` are accepted alongside `default`." | Terminologie in S1.5/S1.6 von „default" auf „manual" umstellen (Alt-Name als Alias erwähnen, funktioniert weiter, daher nur Politur). Die „6 Modi"-Zählung selbst stimmt weiterhin (acceptEdits/auto/bypassPermissions/manual/dontAsk/plan). | S |
| W-07 | veraltet | P2 | `resources/modules/block-3-advanced.md:1766,1774` (LE S4.9) | Modul-Zitat: „`/doctor` is non-interactive — it just prints a report." CLI-Changelog 2.1.205: „`/doctor` is now a full setup checkup that can diagnose and fix issues; `/checkup` is its alias." Weitere Erweiterungen seither: `/doctor prompt-audit` (2.1.283). | Satz korrigieren: `/doctor` kann seit 2.1.205 auch aktiv reparieren (fix), nicht nur reporten; `/checkup`-Alias und `/doctor prompt-audit`-Subcommand ergänzen. | S |
| W-08 | fehlt | P2 | `resources/modules/block-2-ecosystem.md:426,448-459` (LE S2.7, „12 Hook-Events") | CLI-Changelog 2.1.251: „Added `PreModelSwitch` and `PostModelSwitch` hook events (block, confirm, or annotate a model switch)"; CLI-Changelog 2.1.219: „Added `DirectoryAdded` hook that fires after `/add-dir` ... registers a new working directory mid-session." Beide fehlen in der 12-Zeilen-Tabelle. | Hook-Tabelle um `PreModelSwitch`/`PostModelSwitch` und `DirectoryAdded` ergänzen (ggf. auf 14 Events erweitern oder als „weitere Events" Fußnote). | S |
| W-09 | fehlt | P2 | `resources/modules/block-3-advanced.md` (LE S3.3 „Custom Subagent", S3.4 „Orchestrierungs-Muster") — kein Treffer für `fork`/`subagent_type` | CLI-Changelog 2.1.232: „Subagent forking is now on by default: a `subagent_type: 'fork'` subagent inherits the full conversation and prompt cache, and non-teammate agent spawns in interactive sessions now run in the background by default." | Neue LE-Ergänzung oder Absatz in S3.3/S3.4: `subagent_type: "fork"` als eigenes Orchestrierungsmuster (voller Kontext-Erbe statt frischer Subagent) — seit CLI 2.1.232 Standardverhalten für Fan-out-Delegation. | M |
| W-10 | fehlt | P3 | `resources/modules/block-2-ecosystem.md` (LE S2.11–S2.13 Plugins) — kein Treffer für „plugin eval" | CLI-Changelog 2.1.269: „Added `claude plugin eval`: run a plugin's eval suite against Claude Code and get scored, reproducible results (JSON + HTML report); see `claude plugin eval --help`." | Kurzer Hinweis in S2.11/S2.13 (Plugin-Supply-Chain/Marketplaces) auf `claude plugin eval` als Qualitätssicherungs-Tool für selbst gebaute Plugins. | S |
| W-11 | unklar | P3 | `resources/cheatsheet.md:192` | Cheatsheet: „`/output-styles` — Switch persona/output style". CLI-Changelog 2.1.269: „Added `/output-style [name]` to list and switch output styles" (Singular). Konnte den tatsächlichen Slash-Command-Namen nicht in einer interaktiven Session verifizieren (Regel verbietet `-p`/interaktive Sessions). | Vor nächstem Kurs-Update in einer echten interaktiven Session `/output-style` vs. `/output-styles` gegenprüfen (z. B. `/help`-Output) und Cheatsheet-Schreibweise fixen. | S |
| W-12 | unklar | P3 | `resources/prerequisites.md:72` vs. `resources/_canonical.md:3` | prerequisites.md: „This workshop was refreshed against `claude --version` **2.1.200** on 2026-07-04." _canonical.md: „Stand: 2026-07-04" mit CLI 2.1.185 laut Auftragskontext. Zwei Kurs-eigene Quellen nennen unterschiedliche CLI-Referenzversionen für denselben Stichtag. | Bei der nächsten Aktualisierung eine einzige CLI-Referenzversion pro Kanon-Stand führen (vermutlich Tippfehler/Versionsdrift zwischen den Dateien beim letzten Update). | S |
| W-13 | fehlt | P2 | Keine LE (Modell-Verifikation, Auftragspunkt 2) | platform.claude.com/docs/models/overview listet in der Vergleichstabelle bereits „Claude Sonnet 5.5" (`claude-sonnet-5-5`, 1M Kontext, 2/10 $/MTok) als Teil des aktuellen 4er-Lineups (statt Sonnet 5). CLI-Changelog-Zeile unmittelbar nach dem geprüften Fenster (2.1.284): „Added Claude Sonnet 5.5 ..., now the default Sonnet model on the Anthropic API." | Vor Kanon-Freigabe nochmal kurz prüfen, ob CLI-Update auf 2.1.284+ ansteht — Sonnet 5.5 ist laut offizieller Modell-Doku schon Teil des aktuellen Lineups, obwohl die lokale/geprüfte CLI (2.1.283) das noch nicht zeigt. | S |
| W-14 | unklar | P3 | `resources/modules/block-1-foundations.md:901-908` (LE S1.17), `resources/modules/block-3-advanced.md` (LE S3.7 Review-Trio) | CLI-Changelog 2.1.223: „Changed `/review` to be an alias of `/code-review`, which reviews the current diff or a PR"; 2.1.218: „Changed `/code-review` to run as a background subagent"; 2.1.215: „Claude no longer runs the `/verify` and `/code-review` skills on its own." Kursbeschreibung von `/review` als eigenständigem „lokalem PR-Review" evtl. nicht mehr exakt, konnte aber ohne interaktive Session nicht live nachvollzogen werden. | Vor nächstem Update `/review` vs. `/code-review` Verhalten in einer echten Session gegenprüfen (Engine-Gleichheit, Auto-Invoke-Verhalten) und Modultext ggf. präzisieren. | M |

---

## Entwurf neuer Kanon

> Ersetzt NICHT `_canonical.md` selbst — Entwurf für die nächste manuelle Aktualisierung, im Stil der
> bestehenden Tabelle.

<!-- CANONICAL SOURCE OF TRUTH DRAFT — Stand Verifikation: 2026-09-28. -->

### Current Claude models (as of 2026-09, verifiziert gegen platform.claude.com)

| Modell | Model-ID (kanonisch) | Kontext | Max Output | In $/1M | Out $/1M | Rolle im Workshop |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 128K | 10 | 50 | Premium/Mythos-Tier — härtestes, langlaufendes Reasoning; Effort-Default `high` |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | 4 | 20 | **Aktueller Default in Claude Code** (seit CLI 2.1.280); Effort-Default `medium` (nicht `high`!) |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | 2 | 10 | Neuester Sonnet — laut offizieller Modell-Doku bereits im Lineup; lokal geprüfte CLI (2.1.283) zeigt noch Sonnet 5, CLI-Changelog-Zeile 2.1.284 bestätigt Sonnet 5.5 als neuen Default-Sonnet — **vor Freigabe re-verifizieren** |
| Claude Haiku 4.5 | `claude-haiku-4-5` (voll: `claude-haiku-4-5-20251001`) | 200K | 64K | 1 | 5 | Bulk-Reads, einfache Suchen, Routine-Reviews; kein Effort-Parameter |

**Weiterhin verfügbar, nicht deprecated (Legacy-Tier):** Claude Fable 5 (`claude-fable-5`, 10/50),
Claude Opus 5 (`claude-opus-5`, 5/25), Claude Opus 4.8 (`claude-opus-4-8`, 5/25), Claude Sonnet 5
(`claude-sonnet-5`, **2/10 dauerhaft — die für 2026-09-01 angekündigte Erhöhung auf 3/15 wurde
zurückgenommen**).

- Tier-Aliase `opus` / `sonnet` / `fable` / `haiku` lösen weiterhin automatisch auf die aktuelle
  Generation auf (bestätigt via `claude --help`).
- Effort-Tiers `low|medium|high|xhigh|max`. Opus 5.5 defaultet neu auf `medium` (nicht mehr `high` wie
  Opus 4.8) — **explizit setzen, wer die alte Tiefe will.**
- Sonnet-5-Einführungspreis ist der neue Dauerpreis (2/10) — keine Preiserhöhung zum 2026-09-01.
- Immer `claude --version` / `/release-notes` / `/model` über jede hier gedruckte Zahl stellen.

### CLI

- Geprüfte Version: **2.1.283** (lokal, `claude --version`). Offizielles Changelog zeigt bereits
  2.1.284 (Sonnet 5.5) — beim nächsten Kurs-Update Zielversion neu festlegen.

---

## Zählung

**Nach Art:** falsch = 2 (W-03, W-04) · veraltet = 5 (W-01, W-02, W-05, W-06, W-07) · fehlt = 4
(W-08, W-09, W-10, W-13) · stärke = 0 · unklar = 3 (W-11, W-12, W-14)

**Nach Schwere:** P1 = 3 (W-01, W-03, W-04) · P2 = 6 (W-02, W-05, W-07, W-08, W-09, W-13) · P3 = 5
(W-06, W-10, W-11, W-12, W-14)

**Gesamt: 14 Befunde.**

## Was ich NICHT prüfen konnte und warum

- **Live-Slash-Command-Verhalten** (`/output-style` vs. `/output-styles`, `/review`-vs-`/code-review`-
  Engine-Gleichheit, `/doctor`-Fix-Umfang in der Praxis): Auftrag verbietet `claude -p` und jede
  interaktive/Headless-Session zur Verifikation — diese Befunde (W-07 teilweise, W-11, W-14) stützen
  sich ausschließlich auf die wörtlichen Changelog-Zeilen, nicht auf eigenes Nachvollziehen im Terminal.
- **Nicht jede der ~99 CLI-Versionszeilen einzeln gegen jede der 65 LE gegengeprüft.** Bei einem
  Changelog von über 3.100 Zeilen (davon der überwiegende Teil VSCode-Extension-, Slack-„Claude Tag"-,
  Claude-Code-on-the-Web- und Code-Review-Bot-Detailfixes) wurden nur `Added`-Zeilen und Kurs-relevante
  `Changed`-Zeilen mit CLI-Kern-Bezug (Modelle, Permissions, Hooks, Plugins/MCP, Subagents, Headless/CI,
  Kosten/Kontext, Git/Worktrees) tief geprüft; reines Bugfix-Rauschen (Rendering-Glitches, Tastatur-Edge-
  Cases, Terminal-Kompatibilität) wurde bewusst nicht einzeln gegen den Kurs abgeglichen.
- **VSCode-Extension, Claude Tag (Slack), Claude Code on the Web, Code-Review-Bot:** Diese Surfaces
  haben im geprüften Zeitraum sehr viele eigene Änderungen bekommen, wurden aber nicht einzeln bewertet,
  da der Workshop laut `CLAUDE.md`/`session-plan.md` CLI-zentriert ist (Trainer nutzt Terminal, nicht
  die IDE-Extension oder Slack-Integration als Primärsurface).
- **Modell-Einzelseiten** (z. B. `platform.claude.com/docs/models/opus-5-5/overview`) wurden nicht
  einzeln abgerufen — nur die Vergleichstabelle auf der Übersichtsseite plus die zentrale Pricing-Seite.
  Retirement-Daten der Einzelmodelle (z. B. exaktes Non-Deprecation-Commitment für Opus 4.8) wurden
  daher nicht Wort für Wort verifiziert, nur der Status „still available" aus der Übersichtstabelle.
- **`claude <subcommand> --help`** wurde nur für den Top-Level-Aufruf (`claude --help`) genutzt, nicht
  für jeden der ~18 Subcommands einzeln (`agents`, `mcp`, `plugin`, `auth`, `gateway`, …) — eine
  vollständige Subcommand-Flag-Inventur war im Zeitbudget nicht leistbar.
- **Fable 5.1 / Opus 5.5 Detail-Verhalten** (preserved thinking, refusal-Fallbacks, Effort-Feinheiten)
  wurde nicht mit dem Kurs abgeglichen, da diese API-Feinheiten (Fable-5.1-Migrationsguide) für den
  Workshop-Scope (Claude-Code-CLI-Nutzung, nicht direkte API-Integration) nur am Rand relevant sind.
