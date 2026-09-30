# Karte: Fehlersuche

Wofür: vom Symptom zur ersten Frage und zum passenden Werkzeug. Wie du Schicht für Schicht vorgehst, steht in
[S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md); die Werkzeuge selbst erklärt [S4.9](../library/s4-09-fehlersuche-werkzeuge.md).

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/debug-your-config

## Welches Werkzeug für welche Frage

| Frage | Werkzeug | Hinweis |
|---|---|---|
| Was ist überhaupt geladen? | `/context` | `CLAUDE.md`, Rules, Skills (auch mitgelieferte), MCP-Tools, Subagenten; Details in `/memory`, `/skills`, `/hooks`, `/mcp`, `/permissions` |
| Sind Installation und Konfiguration gesund? | `/doctor` | prüft, schlägt Korrekturen vor und ändert erst nach Rückfrage; startet `claude` gar nicht: `claude doctor` im Terminal (nur lesend) |
| Was ist in dieser Sitzung schiefgegangen? | `/debug [beschreibung]` | schaltet Debug-Logging ab jetzt ein und lässt Claude das Log auswerten; Früheres fehlt, außer du hast mit `claude --debug` gestartet |
| Was passiert ab dem Start, gefiltert? | `claude --debug='mcp,startup'` | der Filter greift nur in der `=`-Form; das Log liegt in `~/.claude/debug/<session-id>.txt`, nicht im Terminal; `--debug-file <pfad>` für einen festen Ort |
| Was hat Claude Turn für Turn getan? | `claude --verbose` | volle Ausgabe je Turn; zeigt nicht, welche Dateien geladen sind (dafür `/context`) |
| Welche Einstellungsquelle gilt? | `/status` | aktive Quellen, auch ob Managed Settings wirken |
| Hat ein Update etwas geändert? | `/release-notes` | Changelog nach Version |

## Symptom → erste Frage → Abhilfe

| Symptom | Erste Frage | Abhilfe |
|---|---|---|
| Skill triggert nicht | Listet `/skills` ihn? | Nein: Liegt er als Ordner `<name>/SKILL.md`, nicht als `<name>.md`? Ja: Badge „user-only" (`disable-model-invocation: true`)? `paths:`-Filter? `description` an deine Formulierung anpassen |
| Skill triggert zu oft | Ist die `description` zu breit? | präzisieren oder `disable-model-invocation: true`, dann nur noch per `/<name>` |
| Skill führt keinen Shell-Befehl aus | Ist `disableSkillShellExecution` gesetzt? | Setting entfernen; `` !`befehl` ``-Syntax prüfen; Regel in `/permissions` prüfen |
| Hook feuert nie | Zeigt `/hooks` ihn? | Nein: Hooks stehen unter `"hooks"` in `settings.json`, nicht in einer eigenen Datei. Ja: `matcher` ist ein String (`"Edit\|Write"`), kein Array, und Tool-Namen sind groß geschrieben (`Bash`); dann `claude --debug` |
| Hook blockt alles | Ist der `matcher` zu breit (`".*"` oder leer)? | enger fassen, etwa `"Bash"` oder `"Edit\|Write"` |
| Schutz-Hook lässt alles durch | Endet er mit `exit 2`? | Nur Exit 2 blockt. Absturz, jeder andere Code und Timeout lassen die Aktion laufen ([S2.8](../library/s2-08-hook-einrichten.md)) |
| Hook-Skript läuft nicht | Läuft es von Hand? | ausführbar (`chmod +x`), Shebang, Pfad; Windows ohne Git Bash: PowerShell-Variante registrieren ([S2.8](../library/s2-08-hook-einrichten.md)) |
| Hook hängt, Sitzung friert | Wartet das Skript auf Eingabe? | `timeout` am Handler setzen (Standard für `command`: 600 s, bei `UserPromptSubmit` 30 s); ein abgelaufener `PreToolUse`-Hook blockt nicht; `Ctrl+C`, sonst Terminal neu und `claude --resume` |
| Plugin fehlt | Zeigt `claude plugin list` es? | Manifest liegt in `.claude-plugin/plugin.json`; `claude plugin validate <pfad>` |
| Plugin-Skill nicht aufrufbar | Rufst du `/<plugin>:<skill>` auf? | Plugin-Skills tragen den Plugin-Namen als Präfix |
| Plugin-Update ändert nichts | Meldet `claude plugin update` „already at the latest version"? | ein fest gesetztes `"version"` im Manifest hält die Version gleich; sonst `/reload-plugins` oder neue Sitzung |
| MCP-Server fehlt oder ist failed | Zeigt `/mcp` ihn verbunden und freigegeben? | Projekt-Server einmal in `/mcp` freigeben; `.mcp.json` im Repo-Root mit `mcpServers`; relative Pfade in `command`/`args` absolut machen; 0 Tools: Reconnect, dann `claude --debug=mcp` |
| MCP-Freigaben verstellt | Welche Projekt-Server hast du abgelehnt? | `claude mcp reset-project-choices` |
| MCP-Ausgabe zu groß | Welches Tool liefert so viel? | Grenzen und Stellschrauben: [Karte „Erweitern"](karte-erweitern.md#mcp-ausgabegrenzen), [S2.16](../library/s2-16-mcp-im-detail.md) |
| `CLAUDE.md` wird ignoriert | Steht sie in `/context` unter Memory files? | Nein: Ort prüfen (eine `CLAUDE.md` im Unterordner lädt erst, wenn Claude dort eine Datei liest), `claudeMdExcludes`. Ja: Anweisung zu vage, widersprüchlich oder Datei zu lang ([S1.10](../library/s1-10-claude-md.md)); ein `InstructionsLoaded`-Hook protokolliert, was wann lädt |
| Auto-Memory notiert Falsches | Was steht im Auto-Memory-Ordner? | über `/memory` öffnen, Notiz löschen oder korrigieren; abschalten mit dem Schalter in `/memory` (`autoMemoryEnabled`) |
| Ständige Rechte-Nachfragen | Zeigt `/permissions` die erwartete Regel? | Muster erweitern; `/fewer-permission-prompts`; `/sandbox`; anderer Rechte-Modus ([S1.6](../library/s1-06-rechte-modi.md)) |
| Erlaubter Befehl fragt trotzdem | Deckt das Muster die Argumente ab? | `Bash(npm test)` passt nicht auf `npm test -v`, `Bash(npm test *)` schon |
| `auto` steht nicht zur Wahl | Unterstütztes Modell? Vom Admin gesperrt? | Voraussetzungen in [S1.6](../library/s1-06-rechte-modi.md) |
| Kosten zu hoch, `-p` läuft endlos | Zeigt `/usage` Ausreißer? Sind `--max-budget-usd` und `--max-turns` gesetzt? | [Kostenkarte](karte-kosten.md) |

## Bug oder Bedienfehler?

- `/release-notes` zeigt, was sich seit dem letzten Update geändert hat; `/doctor` prüft das Setup.
- `/bug` meldet einen Fehler an Anthropic, du wählst vorher, wie viel Verlauf mitgeht. Probleme mit einem Plugin oder
  MCP-Server gehen an dessen Maintainer, Fehler in Claude Code selbst an [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code).

## Mehr dazu

- [S4.9 · Fehlersuche: /debug, --verbose, /doctor](../library/s4-09-fehlersuche-werkzeuge.md) · [S4.10 · Diagnose Schritt für Schritt](../library/s4-10-diagnose-schritt-fuer-schritt.md) · [S2.8 · Einen Hook einrichten, der wirklich blockt](../library/s2-08-hook-einrichten.md)
- Doku: [Konfiguration debuggen](https://code.claude.com/docs/en/debug-your-config) · [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) · [Hooks debuggen](https://code.claude.com/docs/en/hooks#debug-hooks) · [Fehlermeldungen](https://code.claude.com/docs/en/errors)
