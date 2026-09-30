# Faktencheck 2026-09-28 — stimmt, was der Kurs heute konkret behauptet?

> Teil der Delta-Bewertung 2026-09-28 (siehe `00-SCHEMA.md`). Geprüft: lokale CLI 2.1.283 (`claude --version`,
> `claude --help`, `claude <sub> --help`), offizielle Doku unter `code.claude.com/docs/en/*` sowie `claude.com/pricing`.
> Ausschließlich lesend, keine `-p`/interaktiven Sessions, keine Config-Änderungen.

## Befunde

---

**F-01**
| Feld | Inhalt |
|---|---|
| Art | falsch |
| Schwere | P1 |
| Ort | `resources/cheatsheet.md:62` (`claude --bare \| Headless mode without Hooks/Skills/Plugins/MCP/AutoMemory`); `resources/quick-reference.md:10` (`claude --bare -p "..." \| Headless, kein Skill/Hook-Overhead`) |
| Beleg | `claude --help` (lokal, 2.1.283), wörtlich: „`--bare` Minimal mode: skip hooks (those defined in settings and by installed plugins; features built into Claude Code are unaffected), LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery. […] **Skills still resolve via /skill-name.**" MCP wird im Hilfetext nicht als deaktiviert genannt. |
| Vorschlag | Beide Stellen korrigieren: `--bare` schaltet **keine** Skills ab (die lösen weiter über `/skill-name` auf) und laut Hilfetext auch nicht explizit MCP — nur Hooks aus Settings/Plugins, LSP, Plugin-Sync, Auto-Memory, Keychain-Reads, CLAUDE.md-Auto-Discovery. |
| Aufwand | S |

---

**F-02**
| Feld | Inhalt |
|---|---|
| Art | veraltet |
| Schwere | P2 |
| Ort | `resources/cheatsheet.md:352-365` (Permission-Modes-Tabelle), `resources/quick-reference.md:29-38`, `resources/modules/block-1-foundations.md:87,132,299` |
| Beleg | `claude --help` (lokal): `--permission-mode <mode>` choices jetzt `"acceptEdits", "auto", "bypassPermissions", "manual", "dontAsk", "plan"` — **nicht** `"default"`. Offizielle Doku `code.claude.com/docs/en/permission-modes`, wörtlich: „The mode that reviews every action is named **Manual** in the CLI, in `claude --help` […]. Its config value is `default` […]. The CLI accepts `manual` as an alias […]. The Manual label and the `manual` alias require Claude Code v2.1.200 or later." `default` funktioniert also weiter (Alias), ist aber nicht mehr der offizielle Anzeigename. |
| Vorschlag | Kurs um einen Satz ergänzen: seit v2.1.200 heißt der Modus in CLI/`--help`/IDE-Erweiterungen **Manual**; der Settings-/Hook-Wert bleibt `default`, `claude --permission-mode manual` ist ein gültiges Alias. |
| Aufwand | S |

---

**F-03**
| Feld | Inhalt |
|---|---|
| Art | veraltet |
| Schwere | P2 |
| Ort | `resources/cheatsheet.md:365` (Zeile „auto mode requirements: Max-Plan with Opus 4.8 OR Team/Enterprise (Sonnet 5, Opus 4.8). Anthropic API only (not Bedrock/Vertex). Claude Code v2.1.83+.") |
| Beleg | `code.claude.com/docs/en/permission-modes`, wörtlich: „**Provider**: available by default on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in Claude apps gateway sessions." und „Only Claude Sonnet 5 or later, Opus 4.7 or later, and the Fable models are supported on these providers." Zusätzlich, ebenfalls auf derselben Seite: mit **CLI v2.1.283 (der installierten Version) ist `auto` bereits der eingebaute Start-Permission-Mode** für interaktive Terminal-/VS-Code-Sessions, nicht mehr `default`/Manual. Bestätigt auf `code.claude.com/docs/en/auto-mode-config`: „Auto mode is available to all users on every provider, including […] Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry […]." |
| Vorschlag | Zeile ersetzen: Auto-Mode läuft heute auch auf Bedrock/Vertex/Foundry, ab Sonnet 5/Opus 4.7/Fable, und ist seit v2.1.283 der Standard-Start-Modus in interaktiven Terminal-/VS-Code-Sessions (nicht mehr Manual/`default`). Das ist eine Verhaltensänderung, die Lernende an ihrer eigenen v2.1.283-Installation sofort bemerken. |
| Aufwand | S |

---

**F-04**
| Feld | Inhalt |
|---|---|
| Art | falsch |
| Schwere | P2 |
| Ort | `resources/cheatsheet.md:436` (`maxSkillDescriptionChars: 200 \| Cap description length used in listings`) |
| Beleg | Zwei unabhängige gezielte Abfragen von `code.claude.com/docs/en/settings-reference` (Gesamtliste aller „skill"-Keys) finden `maxSkillDescriptionChars` nicht, listen aber `skillListingMaxDescChars` mit exakt derselben Funktion: „Cap each skill's description length in the skill listing." |
| Vorschlag | Key-Name auf `skillListingMaxDescChars` korrigieren. Ein falscher Key in `settings.json` wird von Claude Code stillschweigend ignoriert (kein Fehler) — Lernende würden die Einstellung für wirksam halten, obwohl sie es nicht ist. |
| Aufwand | S |

---

**F-05**
| Feld | Inhalt |
|---|---|
| Art | falsch |
| Schwere | P2 |
| Ort | `resources/cheatsheet.md:103` (`claude plugin validate  # Local pre-submission check`); `resources/quick-reference.md:77` (`claude plugin validate <name>`) |
| Beleg | `claude plugin validate --help` (lokal, 2.1.283): „Usage: claude plugin validate [options] **\<path\>**" — Positional-Argument ist Pflicht, kein `<name>`. Beschreibung: „Validate a plugin or marketplace manifest, or the skills, agents, and commands in a directory." |
| Vorschlag | Cheatsheet-Zeile um `<path>` ergänzen (Befehl ist sonst nicht 1:1 copy-pasteable — bricht mit „missing required argument"); quick-reference `<name>` zu `<path>` korrigieren. |
| Aufwand | S |

---

**F-06**
| Feld | Inhalt |
|---|---|
| Art | veraltet |
| Schwere | P1 |
| Ort | `resources/cheatsheet.md:301-318` (Models-&-Context-Tabelle + „Claude Code defaults to **Opus 4.8**"); `resources/modules/block-1-foundations.md:1066` („the default model (Opus 4.8) is a fine starting point"); Modell-IDs in `resources/modules/block-3-advanced.md:208,223` (`claude-opus-4-8`) |
| Beleg | `resources/review-2026-09-28/00-SCHEMA.md` (dieselbe Review-Serie) nennt den heutigen Weltstand explizit: „2026-09-28: Opus 5.5, Fable 5.1, CLI 2.1.283." `claude.com/pricing` (heute abgerufen) führt als aktuelle Top-Modelle **Fable 5.1** (In:10/Out:50 $/MTok, „Next generation intelligence for long-running agents"), **Opus 5.5** (In:4/Out:20 $/MTok, „Daily driver for agentic coding and enterprise work"), **Sonnet 5.5** und **Haiku 4.5** (In:1/Out:5 — hier stimmt der Kurs); Opus 4.8/Fable 5 laufen dort explizit unter „Legacy Models". |
| Vorschlag | Modelltabelle und die „Default"-Aussage auf Opus 5.5 / Fable 5.1 aktualisieren. Preis-Detail: der Fable-Preis (10/50) hat sich zufällig nicht geändert, der Opus-Preis schon (Kurs: ~5/~25, aktuell Opus 5.5: 4/20). Haiku-Zeile ist weiterhin korrekt. |
| Aufwand | M (mehrere Fundstellen: cheatsheet, quick-reference, block-1, block-3) |

---

**F-07**
| Feld | Inhalt |
|---|---|
| Art | unklar |
| Schwere | P3 |
| Ort | `resources/cheatsheet.md:110` (`claude logs <id>  # Stream logs from background session`) |
| Beleg | `claude --help` (lokal, 2.1.283): „`logs <id>` **Print** a background session's recent terminal output" — kein Hinweis auf Live-Streaming/Follow-Modus im Hilfetext. `claude logs --help` selbst wurde nicht geprüft (könnte ein `--follow`-Flag enthalten, das „Stream" rechtfertigt). |
| Vorschlag | Entweder mit `claude logs --help` verifizieren, ob ein Follow-/Stream-Modus existiert, oder „Stream" zu „Print recent output" abschwächen. |
| Aufwand | S |

---

**F-08**
| Feld | Inhalt |
|---|---|
| Art | unklar |
| Schwere | P2 |
| Ort | `resources/modules/block-2-ecosystem.md:657-692` (Abschnitt „Advanced Hook Output": Felder `updatedToolOutput` für PostToolUse-Output-Rewriting und `continueOnBlock: true` für Soft-Warnings) |
| Beleg | Drei gezielte Abfragen von `code.claude.com/docs/en/hooks` (einmal Gesamt-Feldliste, zweimal Exakt-String-Suche) finden weder `updatedToolOutput` noch `continueOnBlock`. Die dokumentierte Feldliste enthält stattdessen `updatedInput` (Input-Rewriting bei PreToolUse) und `systemMessage`/`hookSpecificOutput` für Warnungen. Die Hooks-Referenzseite ist sehr lang und wurde beim Abruf als teilweise „truncated" markiert — daher keine belastbare Negativ-Sicherheit, nur konsistente Nicht-Fund-Ergebnisse über drei Versuche. |
| Vorschlag | Vor Vertrauen in diesen Abschnitt: Rohseite selbst durchsuchen (Ctrl+F auf `updatedToolOutput`/`continueOnBlock`) oder mit einem echten Hook-Testlauf verifizieren. Falls die Felder nicht existieren, betrifft das ein zentrales Live-Demo-Beispiel (Secret-Redaction über PostToolUse) im Kurs. |
| Aufwand | S (Recherche), ggf. M falls Demo-Code angepasst werden muss |

---

**F-09**
| Feld | Inhalt |
|---|---|
| Art | unklar |
| Schwere | P3 |
| Ort | `resources/cheatsheet.md:72` (`claude --remote-control` / `--rc`) |
| Beleg | `claude --help` (lokal, 2.1.283) listet nur `--remote-control [name]` und `--remote-control-session-name-prefix <prefix>` — kein `--rc`-Alias für das CLI-Flag. (Das separat aufgeführte Slash-Command-Pendant `/remote-control (/rc)` im selben Cheatsheet ist davon nicht betroffen und korrekt.) `--rc` wurde nicht aktiv gegen die CLI getestet, um keinen hängenden Remote-Control-Serverprozess zu riskieren. |
| Vorschlag | `--rc` als CLI-Flag-Alias entweder in der offiziellen CLI-Referenz verifizieren oder aus der Flag-Zeile entfernen. |
| Aufwand | S |

---

**F-10**
| Feld | Inhalt |
|---|---|
| Art | unklar |
| Schwere | P3 |
| Ort | `resources/cheatsheet.md:89` / `resources/quick-reference.md:89` (`Scopes: local (was project) · project (shared via .mcp.json) · user (was global)`) |
| Beleg | `code.claude.com/docs/en/mcp` beschreibt heute drei klar unterschiedliche Scopes (local = privat/einzelnes Projekt, project = geteilt via `.mcp.json`, user = alle Projekte/privat) — aber ohne jeden Hinweis auf eine historische Umbenennung „local (was project)" oder „user (was global)" in der aktuell abgerufenen Doku-Fassung. Konnte weder bestätigt noch widerlegt werden (Changelog nicht durchsucht). |
| Vorschlag | Rename-Behauptung gegen Anthropic-Changelog/Release-Notes abgleichen, sonst neutral als „lokal / projekt-geteilt / user-weit" ohne Rename-Anspruch formulieren. |
| Aufwand | S |

---

## Zählung

| Art | Anzahl |
|---|---|
| falsch | 3 (F-01, F-04, F-05) |
| veraltet | 3 (F-02, F-03, F-06) |
| unklar | 4 (F-07, F-08, F-09, F-10) |
| **Gesamt** | **10** |

| Schwere | Anzahl |
|---|---|
| P1 | 2 (F-01, F-06) |
| P2 | 5 (F-02, F-03, F-04, F-05, F-08) |
| P3 | 3 (F-07, F-09, F-10) |

## Bestätigt korrekt (keine Abweichung gefunden)

Geprüft wurden schätzungsweise **~130 Einzelbehauptungen** (Obergrenze 200 nicht ausgeschöpft — Fokus auf `cheatsheet.md` + `quick-reference.md` vollständig, Module gezielt über Grep auf Versionsmarker/Flags/Model-IDs/Settings-Keys/Hook-Felder gesampelt). Ohne Abweichung bestätigt, je eine Zeile pro Gruppe:

- **Installation/Update**: `curl…install.sh`, `irm…install.ps1`, `npm install -g @anthropic-ai/claude-code`, `brew install --cask claude-code`, `claude update`, `claude --version` (lokal exakt `2.1.283 (Claude Code)` reproduziert).
- **CLI-Flags** (gegen `claude --help`, 2.1.283): `-c/--continue`, `-r/--resume`, `-p/--print`, `--output-format json`, `--json-schema`, `--model`, `--permission-mode` (als Flag selbst), `--allowedTools`, `--add-dir`, `--verbose`, `--debug [filter]`, `-w/--worktree`, `--mcp-config`, `--strict-mcp-config`, `--plugin-dir` (inkl. `.zip`), `--plugin-url`, `--tools`, `--max-budget-usd`, `--append-system-prompt`, `--system-prompt`, `--teleport`, `--bg`, `--from-pr`, `--fork-session`, `--tmux`, `--agents`, `--setting-sources`, `--dangerously-skip-permissions`.
- **CLI-Subcommands**: `claude auth login/logout/status`, `claude mcp add/add-json/list/get/remove/reset-project-choices`, `claude plugin install/uninstall/enable/disable/update/prune/marketplace add`, `claude agents`, `claude attach`, `claude stop`, `claude respawn`, `claude rm`, `claude update`, `claude install [version]`, `claude remote-control` (existiert tatsächlich als Pseudo-Subcommand, trotz Fehlens in der Top-Level-Commands-Liste von `claude --help`), `claude ultrareview`, `claude setup-token`, `claude project purge`, `claude auto-mode defaults`.
- **Permission-Modes**: alle 6 Modus-Namen (`default`/Manual, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) existieren weiterhin; Shift+Tab-Zyklus-Grundprinzip bestätigt.
- **Hook Events**: alle 12 im Cheatsheet gelisteten Events (PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, SubagentStart, SubagentStop, FileChanged, InstructionsLoaded, Notification) sind Teil der aktuellen ~31-Event-Referenz.
- **Hook Execution Types**: `command`, `http`, `prompt`, `agent`, `mcp_tool` — alle 5 bestätigt.
- **Hook-JSON-Feld `terminalSequence`** und **`$CLAUDE_EFFORT`-Env-Var für Hook-Prozesse** — beide bestätigt (siehe aber F-08 für die zwei nicht bestätigten Felder aus demselben Abschnitt).
- **Skill-Frontmatter**: alle im Cheatsheet gelisteten Felder (`name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `model`, `effort`, `paths`, `shell`, `hooks`) bestätigt, inkl. `agent: Explore/Plan/general-purpose` + Custom-Subagents.
- **Subagent-Frontmatter**: `name`, `description`, `tools` (ausdrücklich **nicht** `allowed_tools` — Kurs hat das richtig), `model`, `permissionMode`, `maxTurns`, `skills`, `isolation`, `background` — alle bestätigt.
- **MCP-Transports**: `stdio`, `http`, `sse` (als „deprecated" markiert, exakt wie im Kurs) bestätigt.
- **Settings-Keys**: `worktree.baseRef` (inkl. `"fresh"`/`"head"`-Semantik und Versionshinweis-Bereich), `autoMode.hard_deny`, `sandbox.network.deniedDomains`, `disableSkillShellExecution`, `claudeMdExcludes`, `skillOverrides`, `skillListingBudgetFraction` — alle bestätigt (nur `maxSkillDescriptionChars` falsch, siehe F-04).
- **Modelle**: Haiku-4.5-Zeile (Name, 200K-Kontext, Preis 1/5 $/MTok) exakt bestätigt gegen `claude.com/pricing`.
- **Plugin-Struktur**: `claude plugin marketplace add <owner/repo>` exakt bestätigt (`claude plugin marketplace add [options] <source> — Add a marketplace from a URL, path, or GitHub repo`).

## Was ich nicht prüfen konnte und warum

- **Vollständige Slash-Command-Liste** (Session-Management, Models & Context, Config, Security, Integration, Agents & Automation — insgesamt ~55 Commands in `cheatsheet.md`): interaktive Slash-Commands lassen sich nicht per `--help` prüfen; laut Auftrag gegen die Doku-Seite zu Built-in-Commands zu verifizieren, das wurde aus Zeit-/Aufwandsgründen nur stichprobenartig gemacht (keine WebFetch-Vollprüfung aller ~55 Einträge einzeln).
- **Environment-Variablen-Tabelle** (`CLAUDE_MODEL`, `AWS_REGION`, `CLOUD_ML_REGION`, `MAX_MCP_OUTPUT_TOKENS`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` u.a.): nicht einzeln gegen die Env-Vars-Referenzseite geprüft, nur die im Kurs selbst mehrfach wiederkehrenden (`ANTHROPIC_API_KEY`, `CLAUDE_PROJECT_DIR`, `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`) plausibilisiert, nicht verifiziert.
- **MCP-Output-Limits (Tokenschwellen 10k/25k/500k Zeichen)** und **Data-Retention-Tabelle (5y/30d/0d)**: nicht gegen die offizielle Doku gegengeprüft — beide sind Compliance-relevante Zahlen für die Security-Zielgruppe des Workshops und sollten in einer Folge-Runde priorisiert werden.
- **`claude logs --help`, `claude remote-control` `--rc`-Alias-Test**: bewusst nicht ausgeführt, weil ein Test von `--rc` einen laufenden Remote-Control-Serverprozess hätte starten können (siehe F-09) — ein `claude remote-control --help`-Testaufruf in dieser Session lief tatsächlich in den Hintergrund und musste per `taskkill` beendet werden, nachdem die Hilfeausgabe bereits vorlag.
- **Block-2/Block-3-Module vollständig Zeile für Zeile**: bei ~4.700 Zeilen wurden nur Grep-Treffer auf Versionsmarker (`v2.1.*`), Env-Vars, Modell-IDs und JSON-Keys stichprobenartig gegengeprüft, nicht der volle Fließtext. Größere Restwahrscheinlichkeit für weitere Einzelbefunde in Demo-Skripten und Exercise-Dateien (`resources/demos/`, `resources/exercises/`), die laut Auftrag ohnehin nachrangig zu `cheatsheet.md`/`quick-reference.md`/Modulen waren und hier nicht angefasst wurden.
- **Workshop-eigene Komponenten** (`/commit`, `/tdd`, `/workshop guide/learn`): laut Auftrag nur auf Kennzeichnung als eigene Komponente zu prüfen, nicht auf technische Korrektheit gegen offizielle Doku. `cheatsheet.md` führt sie klar getrennt unter „Workshop-Specific Skills" — keine Kennzeichnungslücke gefunden, daher kein P2-Befund nötig.
