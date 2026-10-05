# Karte: Rechte-Modi und Rechte-Regeln

Wofür: was jeder der sechs Rechte-Modi ohne Rückfrage erlaubt, womit eine Sitzung startet und wie allow-, ask- und deny-Regeln greifen.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/permission-modes (Regeln: https://code.claude.com/docs/en/permissions)

## Die sechs Modi

| Modus | Läuft ohne Rückfrage | Wofür |
|---|---|---|
| `default` (in der CLI „Manual", Alias `manual`) | Nur Lesen | Heikle Arbeit, fremder Code |
| `acceptEdits` | Lesen, Dateiänderungen sowie `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`, jeweils nur im Arbeitsordner | Code iterieren, den du danach mit `git diff` prüfst |
| `plan` | Lesen (plus vom Klassifikator freigegebene Befehle, wenn `auto` verfügbar ist); ändern erst nach Freigabe des Plans | Erkunden vor dem Ändern |
| `auto` | Alles; ein zweites Modell, der Klassifikator, prüft Aktionen, bevor sie laufen | Lange Aufgaben; nicht mit dem Haiku-Tier, Admins können `auto` sperren |
| `dontAsk` | Lesen und vorab Erlaubtes; alles, was fragen würde, wird abgelehnt | CI und Skripte |
| `bypassPermissions` (= `--dangerously-skip-permissions`) | Alles | Nur isolierte Container oder VMs |

## Womit eine Sitzung startet

| Wie du startest | Eingebauter Startmodus |
|---|---|
| Interaktiv im Terminal oder in VS Code | `auto` (ab CLI 2.1.283); ist `auto` nicht verfügbar, Manual |
| `claude -p` oder Agent SDK | `default`; bei einem Drittanbieter oder mit abgeschalteter Telemetrie `auto` (ab CLI 2.1.285). In Skripten immer selbst setzen |
| Eine Settings-Datei setzt `disableAutoMode` auf `"disable"` | `default` |

Vorrang: `--permission-mode` (oder `--dangerously-skip-permissions`) vor `permissions.defaultMode` in einer Settings-Datei vor dem eingebauten Start. `auto` und `bypassPermissions` wirken aus `.claude/settings.json` und `.claude/settings.local.json` nicht. Prüf nach jedem Update, womit deine Sitzung startet. `Shift+Tab` wechselt `default` → `acceptEdits` → `plan` → (falls freigeschaltet `bypassPermissions`, dann `auto`) → `default`; `dontAsk` steht nie im Zyklus.

## Regeln: allow, ask, deny

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(npm test)", "Skill(my-skill)", "Agent(reviewer)"],
    "deny": ["Bash(rm *)", "Bash(curl*)", "WebFetch(domain:evil.com)"],
    "ask": ["Bash(git push *)"]
  }
}
```

- **Reihenfolge:** erst deny, dann ask, dann allow; der erste Treffer entscheidet, Spezifität zählt nicht. Ein allow schneidet kein Loch in ein deny.
- **deny** blockt in jedem Modus, auch in `bypassPermissions`. **ask** fragt auch in `auto`; in `dontAsk` wird stattdessen abgelehnt.
- Regeln setzt Claude Code durch, nicht das Modell: Ein Satz in CLAUDE.md ändert kein Recht. Ansehen und ändern mit `/permissions`. Faustregel: Der Modus setzt die Tonart, die Regeln setzen die einzelnen Noten.

| Regel | Trifft | Trifft nicht |
|---|---|---|
| `Bash(npm test)` | genau `npm test` | `npm test -v` |
| `Bash(npm test *)` | `npm test`, `npm test -v` | `npm install` |
| `Bash(ls *)` | `ls`, `ls -la` | `lsof` |
| `Bash(ls*)` | `ls -la`, `lsof` | — |
| `WebFetch(domain:example.com)` | Abrufe von example.com | andere Domains |

**Falle `npm test` gegen `npm test*`:** Steht `Bash(npm test)` in allow, fragt `npm test -v` trotzdem, denn eine Regel ohne `*` gilt exakt. Nimm `Bash(npm test *)`. Das Leerzeichen vor dem `*` gehört zur Regel: `Bash(npm test*)` erlaubt zusätzlich alles, was ohne Leerzeichen weitergeht, so wie `Bash(ls*)` auch `lsof` trifft.

- **Zusammengesetzte Befehle:** `Bash(npm test *)` erlaubt nicht `npm test && rm -rf build`; jeder Teil muss passen. deny und ask greifen, sobald ein Teil passt.
- **deny ist keine Mauer:** `Bash(rm *)` stoppt `rm -rf build/`, aber nicht `/bin/rm -rf build/` oder `bash -c 'rm -rf build/'`. Muster auf Argumente wie `Bash(curl http://github.com/ *)` sind brüchig. Was sicher halten muss, gehört in die Sandbox.

## Geschützte Pfade (Protected Paths)

Schreibzugriffe auf `.git`, `.claude` (außer `.claude/worktrees`), `.vscode`, `.idea`, `.husky`, Shell-Configs wie `.bashrc`, `.zshrc`, `.profile`, dazu `.gitconfig`, `.npmrc`, `.mcp.json`, `.claude.json` und weitere (vollständige Liste in der Doku) gibt kein Modus automatisch frei, **außer `bypassPermissions`**:

| `default`, `acceptEdits` | `plan` | `auto` | `dontAsk` | `bypassPermissions` |
|---|---|---|---|---|
| fragt | fragt oder Klassifikator; erlaubt, wenn `bypassPermissions` im Zyklus ist | Klassifikator | abgelehnt | **erlaubt** |

Eine allow-Regel wie `Edit(.claude/**)` ändert daran nichts. Weil geschützte Pfade in `bypassPermissions` offen sind, läuft dieser Modus nur in Container oder VM. Getrennt davon: `rm` und `rmdir` auf kritische Pfade (Wurzel, Home, Arbeitsordner) fragen auch in `bypassPermissions` und werden in `dontAsk` abgelehnt; weder eine allow-Regel noch ein Hook-„allow" gibt sie frei.

## Typische Fallen

- **`auto` in `.claude/settings.json`:** Die Sitzung startet ohne Fehlermeldung in Manual. `auto` als Start gehört nach `~/.claude/settings.json`.
- **`auto` nicht verfügbar:** Modell prüfen (nicht das Haiku-Tier), `disableAutoMode` in einer Settings-Datei, oder Anthropic hat `auto` serverseitig abgeschaltet; dann später eine neue Sitzung.

## Mehr dazu

- [S1.5 · Rechte im Alltag: default und acceptEdits](../library/s1-05-rechte-im-alltag.md) · [S1.6 · Alle Rechte-Modi im Überblick](../library/s1-06-rechte-modi.md)
- [S3.8 · Rechte für autonome Läufe](../library/s3-08-rechte-fuer-autonomie.md) · [S3.9 · Geschützte Pfade und Sandbox-Stufen](../library/s3-09-geschuetzte-pfade-und-sandbox.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](../library/s2-08-hook-einrichten.md) (`if` nutzt dieselbe Regel-Syntax) · [Karte Hooks](karte-hooks.md)
