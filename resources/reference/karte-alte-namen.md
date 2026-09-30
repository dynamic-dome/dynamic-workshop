# Karte: Alte Namen und Reifegrad

Wofür: ältere Anleitungen, Blogposts und Kursstände richtig lesen und einschätzen, wie stabil eine Funktion ist.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/glossary#deprecated-and-renamed-terms

## Begriffliche Drift

| Alter Begriff | Heute | Kontext |
|---|---|---|
| Headless mode | Non-interactive mode | gleiches Flag `-p`, gleiches Verhalten |
| Custom commands (`.claude/commands/`) | Skills | Command-Dateien funktionieren weiter |
| Slash commands | Commands | „Slash" ist aus dem Produkttext gestrichen |
| Web session | Cloud session | „Claude Code on the web" heißt nur noch die Browser-Oberfläche |
| `Task` (Tool) | `Agent` | umbenannt in v2.1.63; `Task(...)` in Settings und Agent-Dateien gilt weiter als Alias |
| `allowed_tools` | `tools` | Subagent-Frontmatter; im Skill-Frontmatter heißt das Feld `allowed-tools` |
| MCP-Scope `project` (alt) | `local` | gespeichert in `~/.claude.json` unter dem Projektpfad; das heutige `project` ist die eingecheckte `.mcp.json` |
| MCP-Scope `global` | `user` | gespeichert in `~/.claude.json` |
| `--enable-auto-mode` | `--permission-mode auto` | Flag entfernt in v2.1.111; `auto` liegt im `Shift+Tab`-Zyklus |
| Modus `default` | Anzeige „Manual" | der Wert bleibt `default`; `manual` gilt ab v2.1.200 als Alias |
| `/vim` | `/config` → Editor mode | entfernt in v2.1.92 |
| `/pr-comments` | Claude direkt fragen | entfernt in v2.1.91 |
| `/cost`, `/stats` | `/usage` | beide sind heute Aliase von `/usage` |
| `TodoWrite` | `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` | `TodoWrite` ist zugunsten der Task-Tools abgeschaltet; beide stellt Claude Code standardmäßig nur noch auf älteren Modellen bereit, sonst mit `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` |
| `~/.claude/skills/<name>.md` | `~/.claude/skills/<name>/SKILL.md` | ein Skill ist immer ein Ordner mit `SKILL.md` |

## Reifegrad

| Stufe | Bedeutung |
|---|---|
| stabil | Teil von Claude Code, ohne Vorschau-Vermerk in der Doku |
| experimentell | in der Doku als „experimental" oder „research preview" markiert; Verhalten und Oberfläche können sich ändern, manches muss man erst einschalten |
| eigenes Muster | Umsetzung dieses Kurses, kein Anthropic-Feature |

| Funktion | Reifegrad | Kapitel |
|---|---|---|
| Eingebaute Subagenten (Explore, Plan, general-purpose) | stabil | [S3.2](../library/s3-02-eingebaute-subagenten.md) |
| Eigene Subagenten | stabil | [S3.3](../library/s3-03-eigener-subagent.md) |
| Git-Worktrees | stabil | [S1.18](../library/s1-18-worktrees.md) |
| `/loop`, `/goal` | stabil | [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md) |
| Sechs Rechte-Modi | stabil | [S1.6](../library/s1-06-rechte-modi.md) |
| Geschützte Pfade (gelten in allen Modi außer `bypassPermissions`; Sonderfall Plan-Modus: [Karte „Rechte"](karte-rechte.md#geschützte-pfade-protected-paths)) | stabil | [S3.9](../library/s3-09-geschuetzte-pfade-und-sandbox.md) |
| `/security-review`, `/code-review` (Alias `/review`) | stabil | [S3.7](../library/s3-07-eingebaute-reviews.md) |
| Sandbox auf Betriebssystemebene | stabil | [S3.9](../library/s3-09-geschuetzte-pfade-und-sandbox.md) |
| `claude remote-control` und `/teleport` | stabil | [S4.6](../library/s4-06-remote-und-teleport.md) |
| `PushNotification`-Tool | stabil | [S4.6](../library/s4-06-remote-und-teleport.md) |
| Agent View (`claude agents`) und Hintergrund-Sitzungen | experimentell (research preview) | [S3.5](../library/s3-05-hintergrund-und-teams.md) |
| Agent Teams | experimentell, einschalten mit `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | [S3.5](../library/s3-05-hintergrund-und-teams.md) |
| `/schedule` und Routinen | experimentell (research preview) | [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md) |
| `/ultrareview` (`/code-review ultra`) | experimentell (research preview) | [S3.7](../library/s3-07-eingebaute-reviews.md) |
| Channels (MCP-Push) | experimentell (research preview) | [S4.6](../library/s4-06-remote-und-teleport.md) |
| Codex-Schwarm (`multi-model-orchestrator`) | eigenes Muster | [S4.2](../library/s4-02-codex-schwarm.md) |
| Devil's-Advocate-Kette | eigenes Muster | [S3.6](../library/s3-06-devils-advocate.md) |
| Self-Improve-Loop (`agentic-os`) | eigenes Muster | [S3.14](../library/s3-14-self-improve-loop.md) |
| Telegram-Bridge | eigenes Muster | [S4.6](../library/s4-06-remote-und-teleport.md) |

Stand dieser Tabelle ist das Prüfdatum oben. Vorschau-Funktionen wechseln oft den Status: Im Zweifel gilt der Vermerk
oben auf der jeweiligen Doku-Seite und `/release-notes`.

## Mehr dazu

- Begriffe mit Definition: [Glossar](glossar.md) · offizielles [Glossary](https://code.claude.com/docs/en/glossary)
- Änderungen je Version: [Changelog](https://code.claude.com/docs/en/changelog) · [Commands](https://code.claude.com/docs/en/commands) (entfernte Befehle mit Version)
- [S1.4 · Eingebaute Werkzeuge und ihre Namen](../library/s1-04-werkzeuge.md) · [S3.5 · Hintergrund-Sitzungen und Agent Teams](../library/s3-05-hintergrund-und-teams.md) · [S3.12 · Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](../library/s3-12-zeitgesteuert-arbeiten.md)
