# 05 — Gesamtbewertung Delta-Review 2026-09-28

> Orchestrator-Synthese über `01-welt-delta.md` (W), `02-faktencheck.md` (F), `03-anthropic-vergleich.md` (A),
> `04-praxis-delta.md` (P) plus eigene Nachprüfungen (H). Die Helfer (Sonnet) haben recherchiert; die
> P1-Befunde und die Modelldaten hat der Orchestrator selbst an der Quelle gegengeprüft (siehe „Stichproben").
> Verdikt-Stufe dieser Datei: **selbst geprüft**, nicht unabhängig belegt.

## Urteil in drei Sätzen

Der Kurs ist breit, tief und in seinen Stärken (Security-Analogien, verwundbarer Playground, Capstone-Rubrik,
mehrstufige Review-Pipelines) dem offiziellen Anthropic-Material voraus. Er ist aber in zwölf Wochen um
drei Opus-Generationen, eine Sonnet-Generation und rund 100 CLI-Versionen gealtert, ohne dass der Drift-Lint
anschlug. Schwerer wiegt ein Fehler, den zwei große Reviews (Juni, Juli) übersehen haben, weil sie Text
gelesen und keinen Hook ausgeführt haben: Die Kernlektion „Hooks als Sicherheitsgrenze" bringt Hooks bei,
die nicht blocken.

## Eigene Befunde (H) — vom Orchestrator an der Quelle geprüft

### H-01 · falsch · P1 · Hooks blocken mit `exit 1` nicht
- **Beleg:** code.claude.com/docs/en/hooks, wörtlich: „Exit 2 means a blocking error." und „Any other exit code
  doesn't block on its own for most hook events … the action proceeds, and the transcript shows a
  `<hook name> hook error` notice".
- **Ort (Claude-Code-Hooks, nicht Git-Hooks):** `modules/block-2-ecosystem.md:448,465,570,655,679,702`;
  `exercises/block-2-exercises.md:207-208,250,407,422`; `exercises/block-3-exercises.md:547,562`;
  `prerequisites.md:364,385`; `cheatsheet.md:510`; `claude-code-workshop-ui.html:1650,1675,1884`.
  Die Demo-Assets `demos/assets/hooks/secure-diff-gate.*` sind seit Commit `26c33b5` korrekt (`exit 2`, getestet).
  Git-Pre-Commit-Hooks (Exercise 3.6, `block-3-exercises.md:443-477`) sind korrekt: dort blockt jeder Nicht-Null-Code.
- **Vorschlag:** Alle Stellen auf `exit 2` + Satz „andere Codes melden nur einen Fehler, die Aktion läuft weiter".
- **Aufwand:** M

### H-02 · falsch · P1 · Hooks lesen die Eingabe am falschen Ort und erkennen nie etwas
- **Beleg:** Offizielles PreToolUse-Eingabebeispiel (code.claude.com/docs/en/hooks): `"tool_name": "Bash",
  "tool_input": { "command": "npm test", … }`. Das Kommando steht unter `tool_input.command`, nicht auf oberster Ebene.
- **Ort:** `exercises/block-2-exercises.md:186` (`d.get('command','')`), `:229`, `:348` (`$data.command`);
  `modules/block-2-ecosystem.md:563` (`jq -r '.command'`), `:665` (`.toolOutput`); `prerequisites.md:359,381`;
  `exercises/block-3-exercises.md:537` (`.content // .new_content`); `claude-code-workshop-ui.html:1650,1674,1884`.
  Korrekt sind nur Exercise 2.6 (`block-2-exercises.md:931`) und die Demo-Assets.
- **Folge:** Übung 2.2 („Build a Safety Hook"), die erste Kern-Übung zu Hooks, kann nicht funktionieren: Der Hook
  sieht immer einen leeren Befehl, lässt alles durch, und der Tipp im Kurs („make sure it exits with `exit 1`") führt
  tiefer in den Fehler. Der Hinweis „What data does the hook receive?" (`block-2-exercises.md:425-428`) zeigt das
  falsche Format sogar ausdrücklich (`{"command": "rm -rf /tmp/test"}`). Mit Trainer im Raum fällt das auf;
  Selbstlernende bleiben allein damit.
- **Aufwand:** M (zusammen mit H-01)

### H-03 · falsch · P1 · Troubleshooting lehrt die Fehlerrichtung verkehrt herum
- **Ort:** `modules/block-3-advanced.md:1710,1800,1811` (S4.9/S4.10): „Any non-zero exit code is interpreted as a
  **block** … Your script … is now denying every operation because it has a syntax error".
- **Beleg:** wie H-01. Ein abstürzender Hook (Syntaxfehler → Exit 1 oder 127) blockt **nicht**; die Aktion läuft
  weiter, es erscheint nur eine Fehlermeldung. Die reale Gefahr ist also fail-open, nicht fail-closed.
- **Vorschlag:** Abschnitt umdrehen und als Sicherheitslektion nutzen: „Ein kaputter Schutz-Hook ist ein offener
  Schutz-Hook." Passt direkt zur fail-open-Vuln im Playground (Exercise 3.3).
- **Aufwand:** S

### H-04 · fehlt · P2 · Hook-Timeout ist ebenfalls fail-open
- **Beleg:** code.claude.com/docs/en/hooks: „A timed-out `command`, `http`, or `mcp_tool` hook doesn't block the tool
  call. The call continues through the normal permission flow, so don't count on a stalled hook to act as a gate."
- **Ort:** S2.8 ff., S4.10. **Vorschlag:** Mit H-03 zusammen lehren. **Aufwand:** S

### H-07 · falsch · P2 · Mehrere Hooks laufen parallel, nicht der Reihe nach
- **Ort:** `exercises/block-2-exercises.md:421-422` („they run in array order. The first one to exit non-zero blocks").
- **Beleg:** Hooks-Referenz (Markdown-Fassung, Abruf 2026-09-28): „All matching hooks run in parallel."
- **Vorschlag:** Satz ersetzen; Folge für die Übung: Ein Audit-Log-Hook sieht auch Befehle, die ein anderer Hook
  gerade blockt. **Aufwand:** S

### H-08 · falsch · P2 · Ausgabe-Felder: `suppressOutput` wirkt nicht, `updatedToolOutput` braucht die Tool-Form
- **Ort:** Übung 2.6 Token Firewall, `retrieval-recap-bridges.md:22,45`, `prerequisites.md:79`,
  `exercises/block-3-exercises.md:724`, `agents/workshop-mentor.md:77`; Redaktions-Beispiel
  `modules/block-2-ecosystem.md:655-702` und Cockpit `claude-code-workshop-ui.html:1672-1675`.
- **Beleg:** Hooks-Referenz: `suppressOutput` — „Has no effect: Claude Code accepts the field but doesn't act on it."
  `updatedToolOutput` — „The value must match the tool's output shape … a value that doesn't match the tool's output
  schema is ignored"; Bash-Form `{stdout, stderr, interrupted, isImage}`, Eingabe unter `tool_response`.
  `continueOnBlock` existiert, aber als Feld prompt-basierter Hooks.
- **Korrektur zu F-08:** Der Faktencheck hielt `updatedToolOutput`/`continueOnBlock` für möglicherweise nicht existent;
  die vollständige Referenz belegt beide. Falsch ist im Kurs nicht der Feldname, sondern Eingabepfad (`.toolOutput`),
  Wertform (String statt Bash-Objekt) und der Hook-Typ bei `continueOnBlock`.
- **Aufwand:** M

### H-09 · falsch · P2 · Getesteter Demo-Hook übersieht Windows-Pfade
- **Ort:** `demos/assets/hooks/secure-diff-gate.{py,sh}`, Tests in `tools/test_workshop_tooling.py:73-92`.
- **Beleg:** Hooks-Referenz: Dateipfade kommen „always absolute … On Windows, the path arrives with backslash
  separators … A comparison written with forward slashes, such as a `/src/` check, never matches a backslash path,
  and the tool call proceeds". Das Muster `secrets/` greift bei `C:\proj\secrets\db.txt` nicht. Die Tests nutzen
  relative Pfade mit Schrägstrich und sehen das deshalb nicht.
- **Aufwand:** S

### H-05 · veraltet · P2 · Lineup hat sich am Tag der Bewertung erneut bewegt
- **Beleg:** platform.claude.com/docs/en/about-claude/models/overview (2026-09-28): aktuelles Lineup Fable 5.1 /
  Opus 5.5 / **Sonnet 5.5** / Haiku 4.5; Sonnet 5 steht unter „Legacy models (still available)". Changelog 2.1.284:
  „Added Claude Sonnet 5.5 … now the default Sonnet model on the Anthropic API". Haiku 4.5: „Retirement: Not sooner
  than October 15, 2026" — der Kurs empfiehlt Haiku für Massenarbeit.
- **Vorschlag:** Beleg dafür, dass Aktualität ein Prozess sein muss (siehe Phase 2), kein Sweep. Haiku-Empfehlung
  alias-basiert formulieren und Retirement-Stand im Kanon führen.

### H-06 · veraltet · P2 · Das Lern-Cockpit auf der Website ist eine abweichende Kopie
- **Beleg:** `diff -q resources/claude-code-workshop-ui.html` gegen `dome-dynamics/public/workshop-cockpit.html`:
  Dateien unterscheiden sich (239 168 vs. 242 677 Bytes, beide vom 2026-07-07). Die Website zeigt damit einen
  eigenen Stand, inkl. der Fehler H-01/H-02 und `--bare`-Text (F-01).
- **Vorschlag:** Export als definierter Schritt mit Prüfsumme; Website zeigt Kursstand und Prüfdatum. **Aufwand:** S

## Zusammengeführte Befunde (Dubletten aufgelöst)

| Thema | Befunde | Schwere | Stand |
|---|---|---|---|
| Hook-Semantik (Exit-Code, Eingabepfad, fail-open) | H-01, H-02, H-03, H-04, F-08 | **P1** | belegt |
| Modell-Lineup & Default | W-01, F-06, H-05, W-02, W-04 | **P1** | belegt (Orchestrator-Stichprobe) |
| Auto-Mode (Standard ab 2.1.283, alle Provider) | A-01, F-03, W-03 | **P1** | belegt (Doku-Zitat) |
| `--bare` schaltet Skills nicht ab | F-01, P-05 | **P1** | belegt (`claude --help`) |
| Falsche Befehle/Keys | F-04 (`skillListingMaxDescChars`), F-05 (`plugin validate <path>`) | P2 | belegt |
| Neue Funktionen fehlen | W-08 (Hook-Events), W-09 (Fork-Subagents), W-10 (`plugin eval`), W-05 (AGENTS.md-Fallback), W-07 (`/doctor` repariert), A-04 (LSP-Plugins), A-11 (Agent SDK), A-02 (Interview→SPEC.md), A-03 (CLAUDE.md < 200 Zeilen), A-05 (`ConfigChange`), A-06 (`ultracode`) | P2/P3 | belegt |
| Umbenennung `default` → Manual | F-02, W-06 | P3 | belegt |
| Praxis-Lücken | P-01 … P-13 | P1–P3 | Betriebsnotizen |
| Offen/unklar | F-07, F-09, F-10, W-11, W-12, W-14, A-12, P-06 | — | Test nötig |

## Gesamtnote (Skala 1–5)

| Dimension | Note | Begründung |
|---|---|---|
| Aktualität | **2** | Opus-Default drei Schritte zurück (4.8 → 5 → 5.5), Sonnet 5.5 fehlt, Auto-Mode-Wechsel fehlt, ~100 CLI-Versionen (W-01, H-05, A-01). Der Lint war per Konstruktion grün. |
| Fachliche Korrektheit | **2** | Rund 130 geprüfte Behauptungen sind überwiegend korrekt (Flags, Frontmatter, Events, Scopes), aber die Kern-Sicherheitslektion ist an ~20 Stellen falsch (H-01–H-03), dazu `--bare` (F-01). |
| Abdeckung heute | **3** | Breit; es fehlen Fork-Subagents, `plugin eval`, neue Hook-Events, AGENTS.md-Fallback, LSP-Plugins, Agent SDK. |
| Praxisnähe | **3** | Stark bei Multi-Agent und Security; es fehlen Prüfen von Agentenergebnissen, Testisolation, Headless-Härtung, Betrieb (P-01, P-04, P-05, P-09). |
| Selbstlerntauglichkeit | **3** | Cockpit, Capstone-Rubrik und Selbstlern-Pfad sind da. Aber die erste Hook-Übung scheitert still, und das trifft Selbstlernende ohne Trainer am härtesten. |
| Versprechenstreue | **2** | Acht Website-Punkte ohne Datum und Status, keiner der vier Ausbau-Punkte geliefert; Cockpit-Kopie weicht ab (H-06). |

**Stärken, die bleiben sollen** (A-07 … A-10, P-14): Security-Analogien, verwundbarer Playground, Capstone-Rubrik,
mehrstufige Review-Pipeline, Tiefe (65 LE, ~12 h, gegenüber ~2,5 h in zwei offiziellen Academy-Kursen),
chirurgisches Stagen, Budget-Caps, Modell pro Phase.

## Was die zwei früheren Reviews übersehen haben — und warum

Juni (12 Perspektiven) und Juli (78 Agenten, adversariale Verifikation) haben Text gegen Text und Text gegen Doku
geprüft. H-01/H-02 findet man so nur, wenn jemand genau diese Doku-Stelle liest. Ausgeführt wurde nur, was schon
als Asset mit Test existierte (Demo-Hooks, Playground). Folgerung für Phase 2: **Jeder kopierbare Hook und jedes
kopierbare Skript im Kurs wird zu einem getesteten Asset**, das gegen das offizielle Eingabeformat läuft. Das ist
dieselbe Lektion wie P-01: Ein grüner Bericht ist kein Beweis, ausgeführter Code ist einer.

## Versprechen der Website ↔ Befunde

| Website-Punkt | Speist sich aus | Vorhandenes Material |
|---|---|---|
| Lücke „Multi-Agent-Eval-Loops" + Ausbau „Modul Coding-Agent-Evaluierung" | P-01, P-02, P-03, W-09 | Eigene Verifier-Runden 2026-09 (4 von 6 grün gemeldeten Paketen fielen durch), Negativkontrollen |
| Lücke + Ausbau „Plugin-Distribution" | W-10, A-04, F-05 | Eigene Marketplaces, `claude plugin`-CLI, `claude plugin eval` |
| Lücke „Token-Ökonomie und Kosten-Patterns" | P-07, P-08, W-02, W-04 | Hook-Overhead-Messung, ccusage-Abgleich, neue Preise und Effort-Defaults |
| Lücke „Production-Operations" | P-04, P-05, P-09, H-03, H-04 | Nachtlauf mit Not-Aus und JSONL-Bericht, Test-DB-Vorfälle |
| Ausbau „Demo-Artefakte aktualisieren" | H-01, H-02, H-06, F-01 | Getestete Hook-Assets als Vorlage |
| Ausbau „Setup-ab-Tag-1-Repo" | A-02, A-03, W-05, A-01 | Kann zugleich Heimat der getesteten Assets werden |

## Stichproben des Orchestrators (Verifikation der Helfer)

- A-01/F-03: Doku-Zitat selbst abgerufen (permission-modes) — bestätigt.
- Hook-Exit-Codes, Eingabeformat, Timeout: Doku selbst abgerufen (hooks) — bestätigt; `updatedToolOutput`/
  `continueOnBlock` (F-08) auch dort nicht gefunden.
- Modell-Lineup W-01/W-04/W-13: Modellübersicht und Changelog selbst abgerufen — bestätigt, inkl. Sonnet 5.5.
- Faktencheck-Helfer musste einen hängengebliebenen `claude remote-control --help`-Prozess beenden; Nachprüfung
  per Prozessliste: kein Rest-Prozess.
- F-05 selbst nachgeprüft (`claude plugin validate --help`: „Usage: claude plugin validate [options] <path>").
- Nicht nachgeprüft: F-04 (Helfer-Beleg mit wörtlichem Zitat, plausibel), die P3-Befunde.

## Korrekturen nach dem ersten Commit (2026-09-28, vor Veröffentlichung)

- H-02 nannte die Hook-Übung „Übung 2.1"; richtig ist **Übung 2.2** („Build a Safety Hook"). 2.1 ist die Skill-Übung.
- F-08 war als „unklar, vermutlich nicht existent" geführt; die vollständige Hooks-Referenz (Markdown statt gekürzter
  WebFetch-Zusammenfassung) belegt beide Felder. Neu bewertet in H-08.
- H-07 bis H-09 kamen beim Lesen der vollständigen Referenz für den Hotfix hinzu.
- F-01 war nur halb richtig. `claude --help` sagt „Skills still resolve via /skill-name", die Headless-Doku
  (code.claude.com/docs/en/headless.md) sagt, `--bare` überspringt die **automatische Erkennung** von Hooks, Skills,
  Subagents, Plugins, MCP-Servern, Auto-Memory und CLAUDE.md. Beides stimmt: keine Auto-Discovery, expliziter
  `/skill-name`-Aufruf geht. Der Hotfix formuliert es so.

## Nachträge aus dem Hotfix (2026-09-28)

### H-10 · falsch · P1 · CI-Anleitung kombiniert `claude setup-token` mit `--bare` — das authentifiziert nicht
- **Beleg:** code.claude.com/docs/en/authentication.md: „Bare mode does not read `CLAUDE_CODE_OAUTH_TOKEN`. If your
  script passes `--bare`, authenticate with `ANTHROPIC_API_KEY` or an `apiKeyHelper` instead." `setup-token` erzeugt
  genau so ein OAuth-Token (Env-Var `CLAUDE_CODE_OAUTH_TOKEN`).
- **Ort:** `modules/block-3-advanced.md` Modul 3.6 (Lernziel, „CI Auth — `claude setup-token`", Env-Name
  `CLAUDE_CODE_TOKEN` statt `CLAUDE_CODE_OAUTH_TOKEN`, Failure-Tabelle), Cockpit S4.4/S4.5, `faq.md:171`,
  `cheatsheet.md:120`, Mentor.
- **Stand:** Im Hotfix nur der `--bare`-Absatz korrigiert (Auth-Hinweis). Die übrige CI-Anleitung ist ein eigener
  Folgepunkt, bewusst nicht halb geändert.
- **Aufwand:** M

### H-11 · fehlt · P2 · `-p` ohne `--bare` führt Hooks und MCP-Server eines fremden Repos aus
- **Beleg:** code.claude.com/docs/en/headless.md: „Without `--bare`, a `-p` session runs the hooks in a project's
  `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted."
- **Stand:** Im Hotfix als Sicherheitsabsatz in Modul 3.6 ergänzt (`--bare`-Abschnitt).

### H-12 · falsch · P2 · Cockpit zeigte Code-Beispiele ohne Zeilenumbrüche in 114 px breiten Karten
- **Beleg:** Browser-Messung (Playwright, 1413 px Fenster): `<p id="example">` mit `white-space: normal`, drei
  Karten à 114 px. Kopiert man ein Beispiel, macht die `#!/bin/bash`-Zeile den ganzen Rest zum Kommentar.
- **Stand:** Behoben — `<pre>` mit `white-space: pre-wrap`, Code-Karte über volle Breite (12 statt 41 Zeilen),
  Test in `tools/test_workshop_ui_behavior.py`.

## Hotfix-Stand (2026-09-28)

Behoben mit Belegen: H-01, H-02, H-03, H-04, H-07, H-08, H-09, H-11, H-12, A-01/F-03 (auto-Modus-Text), F-01
(`--bare`, präzisiert), F-04, F-05; dazu Skill-Frontmatter-Format und -Lebensdauer, `if`-Position,
`terminalSequence`-Allowlist, Hook-Timeout (600 s, fail-open). Neue Absicherung: `tools/test_course_hooks.py`
(Verhalten jeder kopierbaren Hook-Datei mit Eingaben im offiziellen Format inkl. Windows-Pfaden; Abgleich jedes
markierten Kurs-Snippets mit seiner Datei; Wächter gegen die alten Fehlmuster mit eingebauter Gegenprobe).
Offen: H-10 (CI-Auth), Modell-Lineup (Phase 2), neue Features (W-08 ff.).

## Nachträge aus dem CI-Auth-Fix (2026-09-29)

Quellen, im Wortlaut per `curl` als Markdown abgerufen (nicht per WebFetch-Zusammenfassung):
code.claude.com/docs/en/authentication.md, headless.md, github-actions.md, cli-reference.md, env-vars.md;
dazu `claude --help` 2.1.284.

### H-10 · Stand: behoben
- **Befund präzisiert:** Der Kurs vermischte zwei Auth-Wege, die sich ausschließen. `setup-token` druckt ein
  Abo-Token (Pro/Max/Team/Enterprise) für `CLAUDE_CODE_OAUTH_TOKEN`, das nur Modell-Anfragen stellen kann; `--bare`
  liest es nie. Weitere Fehler im selben Abschnitt: Widerruf über „`claude auth status` → manage tokens" existiert
  nicht (`claude auth` kennt nur `login`, `logout`, `status`); Token-Umfang „full Claude Code access" war zu weit;
  der Workflow-Text nannte ein „OAuth secret", der Code nutzt korrekt `ANTHROPIC_API_KEY`; eine Quiz-Falschantwort
  (S4.3) war im Kern richtig.
- **Selbst ausgeführt:** Vorrang mit Dummy-Werten über `claude auth status` (keine Modell-Anfrage): nur OAuth-Token
  → `authMethod: oauth_token`; nur API-Key → `api_key`; beide → `api_key`. `loggedIn` ist auch bei Dummy-Werten
  `true` — `auth status` zeigt die Wahl, nicht die Gültigkeit.
- **Korrektur:** Modul 3.6 lehrt jetzt drei Wege als Tabelle (A: API-Key, mit `--bare`; B: Abo-Token, nur ohne
  `--bare` und nur auf vertrauenswürdigem Code; C: ohne langlebiges Secret — GitHub-Action mit Workload Identity
  Federation oder Bedrock/Vertex per OIDC), dazu Vorrang-Falle, Token-Rotation, Fehlertabelle, Don'ts. Nachgezogen:
  Cockpit S4.4/S4.5 und Quiz S4.3, FAQ, Cheatsheet, Mentor.
- **Bewusst nicht gelehrt:** `--safe-mode` (liest das Abo-Token, schaltet alle Anpassungen ab) und `--restricted`
  als Absicherung für Weg B. Beide sind neu, als Fehlersuch- bzw. Eval-Harness-Werkzeug dokumentiert und nicht real
  in CI getestet. Kandidaten für Phase 2/3 (neue Features), nach einem echten Lauf.
- **Absicherung:** `tools/test_course_ci_auth.py` (bekannte Falschbehauptungen; kein Snippet ruft `claude --bare`
  mit Abo-Token oder `setup-token` ohne API-Key auf; Positiv- und Negativkontrolle). Gegenprobe gegen die Fassungen
  vor dem Fix: Modul 4 Treffer, Cheatsheet 1, Cockpit 2. Den alten FAQ-Text fängt der Wächter nicht (unvollständig,
  nicht musterhaft falsch).

### H-13 · falsch · P2 · `--metadata` existiert nicht
- **Beleg:** Weder `claude --help` 2.1.284 noch cli-reference.md kennen das Flag.
- **Ort:** `modules/block-3-advanced.md` Modul 3.6, Abschnitte *Self-Hosted Runner* (Option A) und *Monitoring CI
  Costs*.
- **Stand:** Offen. Braucht einen belegten Ersatz für die Kostenzuordnung je CI-Lauf (Kandidat: OpenTelemetry-
  Attribute, zu prüfen). **Aufwand:** S

### H-14 · falsch · P3 · `CLAUDE_MODEL` existiert nicht
- **Beleg:** env-vars.md kennt `ANTHROPIC_MODEL`, nicht `CLAUDE_MODEL`.
- **Stand:** Behoben in der Env-Tabelle des Cheatsheets; im Wächter verankert.

### H-15 · falsch · P2 · Pseudonymisierte Env-Namen liest kein Programm
- **Ort:** Cockpit S4.5 (`CLAUDE_CI_CREDENTIAL_PLACEHOLDER`) und Slack-MCP-Beispiel (`SLACK_CREDENTIAL_PLACEHOLDER`),
  eingeführt mit `44e219b` (2026-07-07, „Credential-Pseudonymisierung").
- **Beleg:** Claude Code liest `ANTHROPIC_API_KEY`, der Slack-MCP-Server `SLACK_BOT_TOKEN` (so auch Modul 2.4). Das
  Website-Repo hatte dieselbe Ersetzung am 2026-07-07 verworfen: Lehrbeispiele mit Env-Var-**Namen** sind keine
  Secrets, die Ersetzung macht den Inhalt fachlich falsch. Der Cockpit-Re-Export vom 2026-09-29 (dome-dynamics
  `f4ce412`) hat die Platzhalter trotzdem auf die Website gebracht; der nächste Re-Export behebt das.
- **Stand:** Behoben im Kurs; im Wächter verankert.

### H-16 · irreführend · P3 · Unerklärtes Präfix `classification=… claude …` in acht Cockpit-Beispielen
- **Ort:** Cockpit, u. a. S4.3 (`classification=ci claude --bare -p …`), Datenhaltung, Multi-Model, Codex-Swarm,
  `/loop`; eingeführt mit `5ec8004` (2026-06-30, SOC-Redesign, von Codex umgesetzt).
- **Befund:** Das Präfix setzt nur eine Shell-Variable für den einen Aufruf, die Claude Code nicht auswertet. Weder
  Module noch Cheatsheet noch Cockpit erklären es. Lernende halten es leicht für ein Feature.
- **Vorschlag:** Entfernen oder einmal als Team-Konvention (Daten-Klassifizierungs-Label) erklären. Entscheidung
  offen. **Aufwand:** S

## CI-Auth-Stand (2026-09-29)

Behoben: H-10, H-14, H-15. Offen: H-13 (`--metadata`), H-16 (`classification=`-Präfix), Modell-Lineup (Phase 2),
neue Features (W-08 ff., dazu `--safe-mode`/`--restricted`).

## Unabhängige Prüfung des CI-Auth-Fixes (Codex-Verifier, 2026-09-29)

Codex hat den Diff read-only gegen dieselben Doku-Dateien geprüft; Urteil **REJECT**. Jeder Befund wurde danach an der
Quelle nachgeprüft (Verdikt-Stufe: unabhängig gefunden, selbst bestätigt).

### H-17 · falsch · P1 · Der Kurs bestreitet das dokumentierte Flag `--max-turns` (löst P-06 auf)
- **Beleg:** cli-reference.md: „`--max-turns` | Limit the number of agentic turns (print mode only). Exits with an
  error when the limit is reached." `claude --help` 2.1.284 listet das Flag nicht — daher der Irrtum aus Welle A/B
  (Juni), der das Flag nach der Hilfe entfernte. Selbst ausgeführt: `claude -p --max-turnz 1` → `unknown option`;
  `claude -p --model haiku --max-turns 1` → läuft. Das Abbrechen beim Erreichen des Limits ist Doku-Aussage, nicht
  separat provoziert.
- **Ort (vor dem Fix):** Modul 1 (Cost-Basics), Modul 3.3 (CI-Tipp), Modul 3.6 (Cost Caps), Übung 3.6, Glossar,
  Session-Plan, Troubleshooting, FAQ, Cockpit S3.13/S4.4 — acht Dateien.
- **Stand:** Behoben. `--max-turns` wird als Partner von `--max-budget-usd` gelehrt (beide nur `-p`), Cheatsheet-Zeile
  ergänzt, Wächter-Regel mit Gegenprobe (alle acht Vorher-Fassungen werden gefunden). P-06 ist damit entschieden:
  Die eigene Praxis hatte recht, der Kurs nicht.
- **Lektion:** `--help` ist nicht die Referenz. Dieselbe Fehlerklasse wie H-01: Text gegen Text geprüft, nicht gegen
  die vollständige Quelle.

### Weitere Codex-Befunde
- **P2 Federation mit `--bare` — bestätigt, behoben.** authentication.md: „Claude Code doesn't read profiles or
  federation variables in bare mode." Die Regel „`--bare` = Weg A oder C" war falsch; jetzt: ein direkter
  `claude --bare`-Aufruf braucht API-Key, `apiKeyHelper` oder Bedrock/Vertex-Credentials; Federation erledigt die
  GitHub-Action selbst. Tabelle, Regel 1, `--bare`-Abschnitt und Cockpit S4.5 angepasst.
- **P2 S4.5 verlangte pauschal ein CI-Secret — bestätigt, behoben** („passende CI-Zugangsdaten").
- **P2 Wächter-Lücken — teils übernommen.** Umbrochene Aufrufe (`claude \` + `--bare`) werden jetzt vor der Prüfung
  zusammengezogen (Negativkontrolle ergänzt). Bleibende, dokumentierte Grenze: Ein API-Key irgendwo im selben Snippet
  gilt als vorhanden. Den Vorschlag, den alten FAQ-Text als Negativkontrolle aufzunehmen, nicht übernommen: Der alte
  Text lehrte Weg B ohne `--bare` — unvollständig, aber nicht falsch.
- **P3 mögliche Falsch-Positive** (Warnung, die `CLAUDE_MODEL` beim Namen nennt, würde rot) — akzeptiert als Grenze;
  heute kein Treffer.
- **Nicht von Codex bewertet** (weder bestätigt noch bestritten), vorher selbst an der Doku belegt: 1-Jahres-Token,
  Vorrang API-Key vor OAuth-Token (zusätzlich ausgeführt), `--bare` als künftiger `-p`-Standard (headless.md),
  `id-token: write` (github-actions.md), `claude auth` nur `login`/`logout`/`status` (`--help`), `ANTHROPIC_MODEL`
  (env-vars.md).
