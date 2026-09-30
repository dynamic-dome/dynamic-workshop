# Karte: Start, Anmeldung und Flags

Wofür: die Befehle zum Starten, Anmelden und Fortsetzen, der Print-Modus mit seinen Grenzen und die Slash-Befehle für jeden Tag.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/cli-reference

## Starten, anmelden, fortsetzen

| Befehl | Was er tut |
|---|---|
| `claude` · `claude "task"` | Interaktive Sitzung, optional mit erstem Prompt; beim ersten Start öffnet sich die Anmeldung im Browser |
| `claude auth login` · `/login` · `/logout` | Anmelden oder Konto wechseln; `claude auth login --console` rechnet über die Claude Console statt über ein Abo ab |
| `claude auth status` | Zeigt als JSON, welche Anmeldung gewählt ist, nicht, ob sie gültig ist |
| `claude -c` · `--continue` | Letzte Unterhaltung im aktuellen Ordner |
| `claude -r <session>` · `--resume` | Bestimmte Sitzung per Name oder ID; ohne Argument öffnet sich die Auswahl |
| `claude --resume <id> --fork-session` | Fortsetzen unter neuer Sitzungs-ID, das Original bleibt |
| `claude --from-pr 123` | Sitzungsauswahl, gefiltert auf die Sitzungen zu diesem PR |
| `claude --version` · `claude update` | Version prüfen, aktualisieren |

## Print-Modus: `claude -p`

| Flag | Wirkung |
|---|---|
| `-p "prompt"` · `--print` | Einmal ausführen, Antwort auf stdout, dann Ende; Eingabe auch per Pipe: `cat logs.txt \| claude -p "explain"` |
| `--output-format json` | JSON mit Ergebnis und `total_cost_usd` (Schätzung, nicht die Rechnung) |
| `--allowedTools "Read,Edit"` | Diese Tools laufen ohne Rückfrage |
| `--permission-mode dontAsk` | Lehnt alles ab, was fragen würde; ohne Angabe startet `-p` in `default` |
| `--max-budget-usd 0.50` | Kostengrenze; Ausgaben von Subagenten zählen mit |
| `--max-turns 5` | Grenze für Agenten-Runden; beim Erreichen endet der Lauf mit Fehler |

`--max-budget-usd` und `--max-turns` wirken **nur mit `-p`**. `--max-turns` fehlt in `claude --help`, steht aber in der CLI-Referenz: `--help` ist nicht die Referenz.

## `--bare` und die Auth-Falle

- `--bare` überspringt die automatische Erkennung von Hooks, Skills, Commands, Subagenten, Plugins, MCP-Servern, Auto-Memory und CLAUDE.md. Einen Skill rufst du trotzdem ausdrücklich mit `/skill-name` auf.
- **Anmeldung:** nur `ANTHROPIC_API_KEY` oder ein `apiKeyHelper` (über `--settings`); Bedrock, Google Cloud und Foundry nutzen ihre eigenen Zugangsdaten. OAuth, Keychain, Federation und `CLAUDE_CODE_OAUTH_TOKEN` liest `--bare` nie. Ein Abo-Token aus `claude setup-token` meldet einen `--bare`-Aufruf also nicht an.
- **Ohne `--bare`** führt `-p` die Hooks aus der `.claude/settings.json` eines Repos aus und verbindet die Server aus dessen `.mcp.json`, auch in einem Ordner, dem du nie vertraut hast. Für fremden Code nimmst du `--bare`; nur die Hooks abschalten geht mit `--settings '{"disableAllHooks": true}'`.
- Laut Headless-Doku soll `--bare` künftig Standard für `-p` werden.

**Vorrang:** `ANTHROPIC_API_KEY` geht vor `CLAUDE_CODE_OAUTH_TOKEN` und vor dem Abo-Login aus `/login`. Mit `-p` nutzt Claude Code einen gesetzten Key immer, interaktiv fragt es einmal nach. Liegt der Key in deiner Shell, läuft dein Skript über den API-Key, obwohl du ein Abo hast.

## Slash-Befehle für den Alltag

| Befehl | Wofür |
|---|---|
| `/help` | Alle Befehle |
| `/clear` | Neue Unterhaltung mit leerem Kontext (Alias `/reset`, `/new`); die alte bleibt über `/resume` erreichbar |
| `/compact [focus]` | Verlauf zusammenfassen und Kontext frei machen, in derselben Unterhaltung |
| `/context` | Kontextbelegung als Raster |
| `/rewind` | Unterhaltung und/oder Code auf einen früheren Punkt; bei leerer Eingabe auch `Esc` `Esc` |
| `/model <alias>` | `opus`, `sonnet`, `haiku`, `fable`; wird Standard für neue Sitzungen |
| `/effort <level>` | `low`, `medium`, `high`, `xhigh`, `max` oder `auto`; `max` gilt nur für die Sitzung |
| `/usage` | Kosten der Sitzung, Plan-Limits, Statistik; `/cost` und `/stats` sind Aliase |
| `/permissions` · `/hooks` | Rechte-Regeln ([Karte](karte-rechte.md)) bzw. Hooks ([Karte](karte-hooks.md)) ansehen |
| `/init` · `/memory` | CLAUDE.md anlegen bzw. bearbeiten, Auto-Memory an- und ausschalten |
| `/status` · `/doctor` | Version, Modell, Konto · Setup prüfen und reparieren |
| `/release-notes` | Changelog nach Version |

Tasten: `Esc` unterbricht Claude, `Shift+Tab` wechselt den Rechte-Modus.

## Typische Fallen

- **`claude --continue` findet deine `-p`-Läufe nicht.** Sitzungen aus `-p` fehlen in der Auswahl und bei `--continue`. Fortsetzen mit `claude --resume <session-id>` oder `claude -p --continue`.
- **Start-Flags gelten beim Fortsetzen nicht mehr.** `--mcp-config`, `--settings`, `--plugin-dir` und `--add-dir` gibst du erneut mit.
- **`/cost` ist kein eigener Befehl mehr**, sondern ein Alias für `/usage`. Ältere Unterlagen trennen noch „Sitzung" und „Tagessumme".

## Mehr dazu

- [S0.1 · Werkstatt einrichten](../library/s0-01-werkstatt-einrichten.md) (Installation, erste Anmeldung) · [S1.1 · Erster Kontakt](../library/s1-01-erster-kontakt.md)
- [S1.7 · Modellwahl und Effort](../library/s1-07-modellwahl-und-effort.md) · [S1.9 · Kontext steuern mit /compact und /rewind](../library/s1-09-kontext-steuern.md)
- [S1.19 · Kosten im Blick](../library/s1-19-kosten-im-blick.md) · [S4.3 · Headless: claude -p als Pipeline-Stufe](../library/s4-03-headless.md)
- [S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](../library/s4-04-ci-zugang-und-kosten.md)
- Doku: [headless](https://code.claude.com/docs/en/headless) · [authentication](https://code.claude.com/docs/en/authentication) · [sessions](https://code.claude.com/docs/en/sessions) · [commands](https://code.claude.com/docs/en/commands)
