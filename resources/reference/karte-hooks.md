# Karte: Hooks

Wofür: welches Ereignis wann feuert, was ein Exit-Code bewirkt, wo die Eingabe steht und warum ein Schutz-Hook still offen sein kann.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/hooks

## Der Vertrag (command-Hooks)

| Frage | Antwort |
|---|---|
| Was kommt an? | JSON auf stdin mit `tool_name` und `tool_input`. Der Shell-Befehl steht in `tool_input.command`, bei Write in `file_path` und `content`, bei Edit in `file_path`, `old_string`, `new_string`. PostToolUse bringt zusätzlich `tool_response` |
| Was blockt? | Nur `exit 2`, bei Ereignissen, die blocken können; bei PreToolUse geht stderr als Grund an Claude. Der Block gilt auch, wenn eine allow-Regel passen würde |
| Und `exit 0`? | Kein Einwand; danach entscheidet der normale Rechte-Ablauf. stderr eines Hooks mit `exit 0` sieht Claude nie |
| Jeder andere Code (1, 127 …) | Ohne gültiges JSON auf stdout nur ein Hook-Fehler: Die Aktion läuft weiter |
| Timeout | Bei `PreToolUse` Standard 600 s (`command`, `http`, `mcp_tool`); ein Timeout blockt dort nicht, der Aufruf läuft weiter. Andere Ereignisse haben eigene Werte, etwa 30 s bei `UserPromptSubmit` |
| Mehrere passende Hooks | laufen parallel |
| Dateipfade | immer absolut, unter Windows mit Backslash |

Ein kaputter Schutz-Hook ist also ein offener Schutz-Hook. Ein Wächter, der seine Eingabe nicht lesen kann, endet deshalb selbst mit `exit 2` ([S2.8](../library/s2-08-hook-einrichten.md)).

## Ereignisse für den Alltag

| Ereignis | Feuert | `exit 2` bewirkt |
|---|---|---|
| `PreToolUse` | vor einem Tool-Aufruf | blockt den Aufruf |
| `PostToolUse` | nach einem erfolgreichen Tool-Aufruf | blockt nichts mehr; stderr geht an Claude |
| `UserPromptSubmit` | nach dem Absenden, bevor Claude den Prompt sieht | weist den Prompt ab |
| `Stop` | Claude ist mit der Antwort fertig | Claude macht weiter |
| `SubagentStart` · `SubagentStop` | ein Subagent startet · ist fertig | nur Meldung · Subagent macht weiter |
| `SessionStart` · `SessionEnd` | Sitzung beginnt oder wird fortgesetzt · endet | nur Meldung an dich |
| `PreCompact` | vor dem Komprimieren des Kontexts | blockt das Komprimieren |
| `FileChanged` | eine beobachtete Datei ändert sich auf der Platte | nur Meldung an dich |
| `InstructionsLoaded` | CLAUDE.md oder `.claude/rules/*.md` wird geladen | wird ignoriert |
| `Notification` | Claude Code schickt eine Benachrichtigung | wird ignoriert |

Die Doku führt über 30 Ereignisse und für jedes, was `exit 2` bewirkt (Tabelle „Exit code 2 behavior per event").

## matcher und if

- **`matcher`** nur aus Buchstaben, Ziffern, `_`, `-`, Leerzeichen, `,` und `|`: exakter Name oder Liste wie `Edit|Write`. Jedes andere Zeichen macht ihn zum JavaScript-Regex ohne Anker: `Edit.*` trifft auch `NotebookEdit`, `^Edit$` nur Edit. `"*"`, `""` oder kein matcher: alles.
- **`if`** steht am einzelnen Handler neben `type` und `command`, enthält genau eine Rechte-Regel wie `"Bash(git *)"` oder `"Edit(*.ts)"` ([Karte Rechte](karte-rechte.md)) und wirkt nur bei `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` und `PermissionDenied`. Bei anderen Ereignissen läuft ein Hook mit `if` nie.
- **Aufbau:** `hooks` → Ereignis → Liste von `{ "matcher": …, "hooks": [ { "type": "command", "command": …, "if": …, "timeout": … } ] }`. Ein vollständiges, getestetes Beispiel steht in S2.8.

## Windows

| Aufgabe | So |
|---|---|
| PowerShell-Skript eintragen | `"command": "pwsh -NoProfile -ExecutionPolicy Bypass -File $HOME/.claude/hooks/safety-check.ps1"`, mit Windows PowerShell 5.1 `powershell -NoProfile -ExecutionPolicy Bypass -File …`; kein `chmod` nötig |
| Befehl direkt in PowerShell | `"shell": "powershell"` am Handler; Claude Code nimmt `pwsh.exe`, sonst `powershell.exe` |
| Eingabe lesen | `[Console]::In.ReadToEnd() \| ConvertFrom-Json`, der Befehl steht in `$data.tool_input.command` |
| Shell-Befehle abfangen | matcher `Bash\|PowerShell`: Wo das PowerShell-Tool aktiv ist, laufen Shell-Befehle darüber, und ein Hook nur auf `Bash` feuert dort nie |
| Pfade vergleichen | erst `\` in `/` umwandeln; ein Vergleich auf `/src/` trifft `C:\proj\src\…` nie, und der Aufruf läuft durch |

## Circuit Breaker: ein Muster, kein Feature

Ein eigener Hook zählt identische Fehlschläge (gleiches Tool, gleiche Argumente, gleicher Fehler) und blockt ab einer Schwelle, etwa beim dritten Mal, mit `exit 2`. So stoppt er Schleifen, die Tokens verbrennen, und zwingt zu einem anderen Ansatz ([S2.10](../library/s2-10-hook-ausgaben.md)). Nicht verwechseln: Die Doku nennt auch den eingebauten Schutz vor `rm` auf kritischen Pfaden einen „circuit breaker".

## Typische Fallen

- **Feuert, blockt aber nicht:** `exit 1` statt `exit 2`, oder das Skript liest ein Feld `command` auf oberster Ebene statt `tool_input.command`.
- **Tor still offen:** Falscher Pfad oder fehlendes `chmod +x`, die Shell endet mit 127, es erscheint nur ein Hinweis `hook error`, und die Aktion läuft. Achte beim ersten Lauf darauf.
- **`Stop`-Hook hört nicht auf:** `exit 2` lässt Claude weitermachen. Prüf das Eingabefeld `stop_hook_active`; nach acht Fortsetzungen in Folge beendet Claude Code den Zug selbst.
- **Fremdes Repo mit `claude -p`:** Dessen Hooks laufen ohne Vertrauensdialog. Nimm `--bare` oder `--settings '{"disableAllHooks": true}'`.

## Mehr dazu

- [S2.6 · Hooks als Sensoren](../library/s2-06-hooks-als-sensoren.md) · [S2.7 · Die wichtigsten Hook-Ereignisse](../library/s2-07-hook-ereignisse.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](../library/s2-08-hook-einrichten.md) · [S2.9 · Hook-Typen und Hooks in Komponenten](../library/s2-09-hook-typen.md)
- [S2.10 · Hook-Ausgaben und das Secure Diff Gate](../library/s2-10-hook-ausgaben.md) · [S4.10 · Diagnose Schritt für Schritt](../library/s4-10-diagnose-schritt-fuer-schritt.md)
- Doku: [Hooks-Leitfaden](https://code.claude.com/docs/en/hooks-guide) · getestete Hook-Dateien: [`resources/demos/assets/hooks/`](../demos/assets/hooks/)
