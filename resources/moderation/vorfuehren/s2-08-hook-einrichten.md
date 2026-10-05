# Vorführen: S2.8 · Einen Hook einrichten, der wirklich blockt

> Demo und Hinweise für Moderierende zum Kapitel [S2.8 · Einen Hook einrichten, der wirklich blockt](../../library/s2-08-hook-einrichten.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Hooks, die Alarmanlage

**Ziel:** Zeigen, dass Hooks automatisch auf Claudes Aktionen reagieren, gefährliche Operationen blocken können und nach dem Einrichten ohne dein Zutun laufen.

**Vorbereitung**

- `~/.claude/settings.json` mit mindestens einem Hook
- Ideal: Der innerHTML-Sicherheits-Hook ist aktiv (warnt bei `innerHTML` in JS-Dateien). Das ist ein PostToolUse-Hook auf Datei-Änderungen, nicht der Bash-Hook aus Schritt 1.
- Alternativ: ein einfacher `echo`-Hook, der Tool-Aufrufe loggt

**Schritt 1: die Hook-Konfiguration zeigen**

```bash
cat ~/.claude/settings.json | jq '.hooks'
# If jq not available:
cat ~/.claude/settings.json
```

Die Struktur durchgehen:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/security-check.sh"
          }
        ]
      }
    ]
  }
}
```

**Schritt 2: den innerHTML-Hook auslösen**

In Claude Code:

```
Add a div to the page and set its content to the user's name using innerHTML
```

Was passiert:

- Claude schreibt den Code mit `innerHTML`.
- Der PostToolUse-Hook feuert.
- Eine Warnung erscheint, etwa *„Security: innerHTML usage detected. Prefer textContent for user-controlled data."*

**Schritt 3: das Hook-Skript zeigen**

```bash
cat ~/.claude/hooks/security-check.sh
# Or wherever the hook is
```

Zeig, dass es nur ein Bash-Skript ist. Es liest JSON von stdin (die Daten des Tool-Aufrufs), prüft auf Muster und endet entweder mit 0 (erlauben) oder mit 2 (blocken, der Grund steht auf stderr).

**Schritt 4: das Blocken ansprechen**

Ein PreToolUse-Hook kann eine Aktion ganz stoppen, über den Exit-Code aber nur mit exit 2. PostToolUse-Hooks reagieren nur: Sie loggen oder melden hinterher, machen die Aktion aber nicht rückgängig.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 7 Minuten (Schritt 1: 2 Min., Schritt 2: 3 Min., Schritt 3: 1 Min., Schritt 4: 1 Min.).

**Sagen:**

- Schritt 1: „Drei Teile: welches Ereignis (PreToolUse), welches Tool (Bash), was läuft (ein Shell-Skript). Mehr ist es nicht."
- Schritt 2: „Ich habe Claude nicht gebeten, auf Sicherheitsprobleme zu achten. Der Hook hat automatisch gefeuert, als Claude den Code geschrieben hat. Er ist ein Sensor an der Edit-Aktion, keine Erinnerung, die ich jede Sitzung wiederholen muss."
- Schritt 3: „Das ist ein Bewegungsmelder. Er ist immer an. Du richtest ihn einmal ein, und er beobachtet jede Aktion von Claude."
- Schritt 4: „PreToolUse-Hooks können auch BLOCKEN. Endet dieser Hook mit Code 2, stoppt Claude Code die Aktion ganz, wie eine Tür, die nicht aufgeht. Mit Code 1 läuft sie trotzdem weiter. PostToolUse-Hooks reagieren nur, sie loggen oder melden hinterher, können die Aktion aber nicht rückgängig machen."

Die Sprechpunkte zu den drei Eckpfeilern stehen in [S2.6](s2-06-hooks-als-sensoren.md).

**Wenn der innerHTML-Hook fehlt:** Lass Schritt 2 weg und zeig das Blocken in Schritt 4 live mit `safety-check.sh` aus „Selbst machen" (Schritt 4 dort).

**Wenn gar keine Hooks eingerichtet sind:** Richte live einen ein:

```bash
# Add a simple logging hook to settings.json
```

Oder zeig die Struktur nur als Konzept und sag: „Das richtet ihr gleich in der Übung selbst ein, ihr baut euch einen Safety-Hook."

</details>
