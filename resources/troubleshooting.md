# Troubleshooting — Claude Code Workshop

> 20 haeufige Probleme mit knappen Loesungen. Scanbar.
> Vertieftes Material in Modul 3.7 "Troubleshooting & Debugging" (geplant).
> Begriffsklaerungen im `resources/glossary.md`, konzeptionelle Fragen im `resources/faq.md`.
> Stand: 2026-05-20.

---

## Skills

### 1. Skill triggert nicht
**Symptom:** Du beschreibst eine Task, der passende Skill wird nicht geladen.

**Diagnose:**
1. `/skills` — ist mein Skill in der Liste?
2. `cat ~/.claude/skills/<name>/SKILL.md | head -20` — Description und Frontmatter pruefen
3. `disable-model-invocation: true`? -> Skill nur manuell aufrufbar via `/<name>`
4. `paths:`-Filter? -> Skill nur bei matching Files aktiv
5. `user-invocable: false`? -> Skill ist Background-Knowledge, nicht User-Command
6. Description zu generisch? Trigger-Phrases ergaenzen (Modul 2.1)

```bash
# Verbose-Start zeigt, was geladen wurde
claude --verbose

# /debug Bundled Skill fuer tieferes Tracing
/debug skill triggering
```

### 2. Skill triggert zu oft (False Positive)
Description zu breit, Trigger-Phrases zu generisch. Loesung: praeziser machen, oder `disable-model-invocation: true` setzen, sodass Skill nur via expliziten `/<name>`-Call laeuft.

### 3. Skill kann Shell-Command nicht ausfuehren
- `disableSkillShellExecution: true` in `settings.json`? -> `false` setzen oder Setting entfernen.
- `` !`<command>` `` Syntax falsch geschrieben (Backticks innerhalb, Bang davor)?
- Permission-Rule blockt den Bash-Call? -> `/permissions` pruefen, Pattern adjustieren.

## Hooks

### 4. Hook blockt alles
Matcher zu breit (`".*"` oder nichts gesetzt). Engeren Pattern waehlen, z.B. `"Bash"` nur, oder `"Write|Edit"` fuer File-Mods. Letters/digits/`_`/`|` = exact-match oder Pipe-Liste. Mit Sonderzeichen = JS-Regex.

### 5. Hook-Script laeuft nicht
- `chmod +x` vergessen?
- Shebang fehlt? (`#!/bin/bash` oder `#!/usr/bin/env node`)
- Pfad in `settings.json` falsch (relative vs. absolute)?
- Auf Windows: PowerShell-Pfad richtig? Skript mit `pwsh -File` aufrufen.
- `/hooks` zeigt registrierte Hooks; `/doctor` macht Health-Check.

### 6. Hook haengt
Hook-Script blockiert > 5s, Session friert ein. Async-Code vermeiden, schnell return. Bei Hook-Type `prompt` oder `agent`: Cost und Latenz beobachten. Im Notfall: Hook deaktivieren in `settings.json`, Session neu starten.

## Plugins

### 7. Plugin nicht gefunden
- `claude plugin list` — installiert?
- Manifest unter `.claude-plugin/plugin.json` (NICHT `plugin.json` im Root)?
- `claude plugin validate` lokal laufen lassen — Schema-Check.

### 8. Plugin-Skill triggert nicht
Path im Plugin-Skill relativ zum Plugin-Root? `claude plugin validate <name>` fuer Schema-Check. Plugin-Skills werden als `/<plugin>:<skill>` aufgerufen, nicht als `/<skill>` direkt.

### 9. Plugin nach Update tut nicht
`/reload-plugins` — Hot-Reload erzwingen. Falls das nicht hilft: neue Session, `claude plugin update <name>`, `claude plugin disable <name>` und `enable` als Reset.

## MCP

### 10. MCP-Server timed out
- `/mcp` — Status pruefen
- `claude mcp get <name>` — Detail-Konfig (Transport, URL, Args)
- `claude mcp list` — alle Server, welcher Scope (local/project/user)
- Re-Auth-Flow via `/mcp` -> Auth-Button
- Bei HTTP-Servern: Netzwerk pruefen (`curl <url>`)

### 11. MCP-Server haengt sich auf
- `claude mcp reset-project-choices` — Approval-Reset
- Stale OAuth-Token? Re-Auth via `/mcp`.
- Lokaler stdio-Server haengt? Prozess killen, Session neu.

### 12. MCP-Output zu gross
Default-Max ist 25k Tokens, Warning bei 10k. Per-Tool Override mit `_meta["anthropic/maxResultSizeChars"]` bis 500k chars. Env-Var `MAX_MCP_OUTPUT_TOKENS` hebt nur die Warning-Schwelle.

## CLAUDE.md & Memory

### 13. CLAUDE.md wird ignoriert
- `claude --verbose` zeigt geladene Files
- Hook `InstructionsLoaded` aufsetzen fuer deterministische Diagnose
- `/init` ausfuehren oder neue Session
- Liegt CLAUDE.md im Repo-Root (nicht in Unterordner)?
- `claudeMdExcludes`-Glob filtert es vielleicht raus.

### 14. Auto-Memory schreibt falsche Notes
- Falsche Notes manuell loeschen aus `~/.claude/projects/<hash>/memory/`
- Oder via Prompt: "Vergiss dass X, ich habe vorher Y gemeint"
- Permanent off: `--bare` Mode
- Pfad-Hash auf Windows: `C:\Users\...\Desktop\projekt` wird zu `C--Users-...-Desktop-projekt`

### 15. CLAUDE.md zu gross
- In `.claude/rules/` aufsplitten mit `paths:`-Filter (siehe Modul 1.2)
- Oder per `@path` Imports modulares Setup
- `/compact` proaktiv vor jeder Session
- Symptom: Context-Window fuellt sich schon beim Start zu >30%

## Permissions

### 16. Endlose Permission-Prompts
`/fewer-permission-prompts` Bundled Skill: scant Transcripts, generiert `permissions.allow`-Liste. Alternativ: `/sandbox` toggeln (reduziert Prompts laut Anthropic um ~84%). Oder Permission-Mode wechseln (`acceptEdits` statt `default`).

### 17. Allowed Bash-Command failed mit Permission
Pattern in `allow:` zu eng. Beispiel: `Bash(npm test)` matched nicht `npm test -v`. Wildcard: `Bash(npm test*)` oder `Bash(npm test *)`. Bei Sonderzeichen: ggf. Quotes oder Escapes pruefen.

### 18. `auto` Mode nicht verfuegbar
- Voraussetzungen pruefen: **Max-Plan mit Opus 4.8** ODER Team/Enterprise (Sonnet 4.6, Opus 4.8)
- Anthropic API only, nicht Bedrock/Vertex
- Claude Code v2.1.83+ noetig
- Admins koennen `auto` per Managed Settings sperren

## Cost & Limits

### 19. Token-Verbrauch zu hoch
- `/cost` waehrend Session pruefen
- Auf Sonnet/Haiku wechseln wo moeglich (`/model sonnet`)
- Effort-Level senken (`/effort low` fuer simple Tasks)
- CLAUDE.md kuerzen — jedes Token zaehlt im Context
- `/compact` proaktiv vor langen Sessions
- Subagents reduzieren, wo nicht noetig

### 20. `claude -p` laeuft endlos
Cost-Cap setzen: `--max-budget-usd 0.50`. Die aktuelle CLI bietet keine harte Turn-Grenze per Flag mehr — `--max-budget-usd` kappt Endlos-Loops/Runaway-Kosten. Bei Endless-Loop in CI: Pre-flight Check, dass das Flag gesetzt ist. Bei Routines/Loops: zusaetzlich `autoMode.hard_deny` fuer riskante Patterns.

---

## Debug-Tools im Ueberblick

| Tool | Wann |
|---|---|
| `/skills` | Liste aller Skills |
| `/hooks` | Aktive Hooks |
| `/mcp` | MCP-Server-Status |
| `claude plugin list` | Installierte Plugins |
| `claude plugin validate <name>` | Plugin-Schema-Check |
| `/permissions` | Aktuelle Permission-Rules |
| `/cost` | Token-Verbrauch Session |
| `/usage` | Tages-/Wochenstatistik |
| `/insights` | Analytics ueber Sessions |
| `/stats` | Streaks, Patterns |
| `/doctor` | Health-Check Konfiguration |
| `claude --verbose` | Verbose-Start, zeigt was geladen wird |
| `claude --debug <category>` | Granulares Debug-Filter |
| `/debug [description]` | Bundled Skill fuer detailliertes Tracing |
| `/release-notes` | Aktuelles Changelog (was wurde geaendert/entfernt) |

---

## Quick-Diagnose-Tabelle

| Symptom | Erste Frage | Wenn ja: | Wenn nein: |
|---|---|---|---|
| Skill triggert nicht | `/skills` listet ihn? | Description praeziser, Trigger-Phrases | Pfad richtig? `--verbose` |
| Hook blockt | `/hooks` zeigt Matcher? | Matcher engen | Hook-File-Pfad pruefen |
| MCP timed out | `/mcp` zeigt connected? | Re-Auth | `.mcp.json` Pfad/Transport pruefen |
| Permission-Loop | `/permissions` zeigt erwartete Rule? | Pattern erweitern | `/fewer-permission-prompts` laufen lassen |
| CLAUDE.md ignoriert | `--verbose` listet es? | Inhalt zu generisch? | Pfad/Repo-Root pruefen |
| Cost zu hoch | `/cost` zeigt Outlier? | Modell/Effort senken | Subagents/Loops auditieren |
| Plugin nicht da | `claude plugin list` zeigt es? | `/reload-plugins` | `claude plugin install` neu |
| Session friert | Hook der haengt? | Hook deaktivieren | `Escape`, neue Session |

---

## Wann ist es ein Bug, nicht User-Error?

- `/release-notes` zeigt Aenderung seit letztem Update
- `/bug` oder `/feedback` zum Report
- `/doctor`-Output sammeln
- Bei MCP/Plugin: Issue beim Maintainer (nicht bei Anthropic)
- Bei Core-Bug: github.com/anthropics/claude-code

---

*Siehe Modul 3.7 fuer vertieftes Material. Siehe `resources/glossary.md` und `resources/faq.md` fuer Begriffe und Konzepte.*
