# Karte: Skills, Plugins und MCP

Wofür: wohin eine Erweiterung gehört, welches Skill-Feld was bewirkt, welcher Plugin- und MCP-Scope für wen gilt und wo MCP-Ausgaben enden.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/plugins-reference · https://code.claude.com/docs/en/mcp

## Skill-Frontmatter: der Kern

| Feld | Wirkung | Falle |
|---|---|---|
| `description`, `when_to_use` | Danach entscheidet Claude, wann der Skill passt | Beide zusammen werden im Listing nach 1.536 Zeichen abgeschnitten: den wichtigsten Fall zuerst |
| `disable-model-invocation: true` | Nur du startest ihn mit `/name` | Die Beschreibung ist dann nicht im Kontext, und Subagenten können ihn nicht vorladen |
| `user-invocable: false` | Nur Claude startet ihn | Er verschwindet aus dem `/`-Menü |
| `allowed-tools` | Diese Tools laufen ohne Rückfrage, nur im aufrufenden Zug | Schränkt nichts ein; zum Sperren gibt es `disallowed-tools`. Gilt auch bei `-p` in nie vertrauten Ordnern: Skills fremder Repos vorher lesen |
| `context: fork` mit `agent` | Läuft als Subagent vom Typ in `agent`, etwa `Explore` | Er sieht deinen Verlauf nicht; `agent` ist ein Agententyp, kein Modell |
| `model`, `effort` | Modell bzw. Effort für diesen Zug | `effort` kennt `low`, `medium`, `high`, `xhigh`, `max`, je nach Modell |
| `paths` | Lädt automatisch nur bei passenden Dateien | Glob-Syntax wie bei `.claude/rules/` |

Feldnamen müssen exakt stimmen, ein unbekanntes Feld ignoriert Claude Code ohne Meldung. Eigene Angaben wie Version oder Autor gehören in `metadata:`. Das Frontmatter zählt nur, wenn `---` in der ersten Zeile steht.

## Wo Skills liegen

| Ort | Pfad | Lädt in |
|---|---|---|
| Persönlich | `~/.claude/skills/<name>/SKILL.md` | allen deinen Projekten auf dieser Maschine, nicht in Cowork- und Cloud-Sitzungen |
| Projekt | `.claude/skills/<name>/SKILL.md` | diesem Repo; einchecken, dann hat das Team ihn auch |
| Unterordner | `<subdir>/.claude/skills/<name>/SKILL.md` | sobald Claude dort eine Datei liest oder bearbeitet |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | überall, wo das Plugin aktiv ist, als `/plugin-name:skill-name` |

Gleicher Name an zwei Orten: Enterprise vor persönlich, persönlich vor Projekt. Ein Skill schlägt eine gleichnamige Datei in `.claude/commands/`.

## Plugin-Baum

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest (name, version, description)
├── skills/
│   └── hello/SKILL.md       # Skills (invoked as /plugin:skill)
├── agents/*.md              # Subagent definitions
├── commands/*.md            # Slash commands
├── hooks/hooks.json         # Lifecycle hooks
├── .mcp.json                # Bundled MCP servers
├── .lsp.json                # Language server config
├── output-styles/*.md       # Output formatting
├── bin/*                    # Executables (added to PATH)
└── scripts/*                # Helper scripts
```

Nur `plugin.json` gehört in `.claude-plugin/`; Komponenten, die dort liegen, laden nicht, und eine `CLAUDE.md` im Plugin-Root lädt nicht als Kontext. Die Doku kennt weitere Standardorte, etwa `monitors/`, `themes/`, `workflows/`, `settings.json`. Lokal testen mit `claude --plugin-dir ./my-plugin`, prüfen mit `claude plugin validate <path>`, Änderungen laden mit `/reload-plugins`.

| Plugin-Scope | `enabledPlugins` steht in | Für wen |
|---|---|---|
| `user` (Standard bei `claude plugin install`) | `~/.claude/settings.json` | dich, alle Projekte |
| `project` | `.claude/settings.json` (eingecheckt) | alle im Repo; installieren muss trotzdem jede Person einmal selbst |
| `local` | `.claude/settings.local.json` | dich, nur dieses Repo |
| `managed` | Managed Settings der Organisation | alle; in `/plugin` nicht änderbar |

Ist ein Plugin in mehreren Scopes gesetzt, gilt local vor project vor user.

## MCP-Scopes

| Scope | Gespeichert in | Lädt in | Geteilt |
|---|---|---|---|
| `local` (Standard) | `~/.claude.json` unter dem Projektpfad, nicht `.claude/settings.local.json` | nur diesem Projekt | nein |
| `project` | `.mcp.json` im Projekt-Root | nur diesem Projekt | ja, per Git |
| `user` | `~/.claude.json` | allen deinen Projekten | nein |

- Setzen mit `claude mcp add --scope local|project|user …`, ansehen mit `claude mcp list` und `claude mcp get <name>`, in der Sitzung mit `/mcp`.
- Alte Namen: Vor CLI 0.2.49 hieß der heutige `local`-Scope `project` und `user` hieß `global`. Eine Anleitung aus der Zeit davor meint mit `--scope project` also den heutigen `local`-Scope.
- Gleicher Servername in mehreren Scopes: local vor project vor user, danach Plugin-Server und claude.ai-Connectors. Der ganze Eintrag gewinnt, Felder werden nicht gemischt.

## MCP-Ausgabegrenzen

| Schwelle | Wert | Stellschraube |
|---|---|---|
| Warnung | ab 10.000 Tokens je Tool-Ausgabe | fest |
| Obergrenze | 25.000 Tokens (Standard) | `MAX_MCP_OUTPUT_TOKENS` hebt sie an |
| je Tool, gesetzt vom Server-Autor | bis 500.000 Zeichen | `_meta["anthropic/maxResultSizeChars"]` im `tools/list`-Eintrag |

Ein Text-Ergebnis über der Grenze wird nicht abgeschnitten: Claude Code legt es als Datei ab und setzt den Pfad in den Verlauf. Bilder zählen immer gegen `MAX_MCP_OUTPUT_TOKENS`.

## Typische Fallen

- Server aus `.mcp.json` brauchen interaktiv deine Zustimmung, in `claude -p`-Läufen lädt Claude Code sie ohne Frage. Bei fremden Repos: `--strict-mcp-config` oder `disabledMcpjsonServers`.
- Umgebungsvariablen in `.mcp.json` schreibst du `${VAR}` oder `${VAR:-default}`, nicht `${env:VAR}`.
- `claude mcp add --transport stdio --env KEY=wert name -- …` bricht ab: Folgt der Servername direkt auf das `--env`-Paar, liest die CLI ihn als weiteres Paar. Schreib den Namen vor `--env` oder setz eine andere Option dazwischen.

## Mehr dazu

- Skills: [S2.1 · Skills sind Dienstanweisungen, Commands sind Knöpfe](../library/s2-01-skills-und-commands.md) · [S2.2 · Eine SKILL.md schreiben](../library/s2-02-skill-schreiben.md) · [S2.3 · Skills oder Commands, und wer sie auslösen darf](../library/s2-03-wer-skills-ausloest.md)
- Plugins: [S2.11 · Plugins: ein Bündel schnüren](../library/s2-11-plugins-buendeln.md) · [S2.12 · Plugin-Lebenszyklus, Scopes und Marketplaces](../library/s2-12-plugin-lebenszyklus.md) · [S2.13 · Lieferkettenrisiken bei Plugins](../library/s2-13-plugin-lieferkette.md)
- MCP: [S2.14 · MCP: der Integrationsstecker](../library/s2-14-mcp-stecker.md) · [S2.15 · MCP einrichten: Transporte, Scopes, CLI](../library/s2-15-mcp-einrichten.md) · [S2.16 · MCP im Detail: OAuth, Ausgabegrenzen, Protokoll](../library/s2-16-mcp-im-detail.md) · [S2.17 · MCP-Sicherheit und ein eigener Server](../library/s2-17-mcp-sicherheit.md)
