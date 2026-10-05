---
id: S2.20
type: practice
title: "Praxis-Station Session 2: alles in einem Ablauf"
shelf: practice
level: core
minutes: 25
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann die Bausteine aus Session 2 in einem Projekt verbinden: einen Skill, der ein MCP-Tool und eine Wissensquelle nutzt, einen Hook, der die Aufrufe mitschreibt, und eine Regel, die ein Tool sperrt."
sources: []
aliases: []
offers: [S2.2, S2.8, S2.10, S2.11, S2.14, S2.18]
---

# S2.20 · Praxis-Station Session 2: alles in einem Ablauf

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~25 Min** · **Voraussetzungen:** keine
>
> ← [S2.19 Grenzen von RAG und Datenschutz](s2-19-rag-grenzen.md) · [Bibliothek](README.md) · [X.1 Community-Skills: wer baut was, das wirklich hilft](x-01-community-skills.md) →
<!-- meta:end -->

## Auf einen Blick

Diese Station schließt Session 2 ab. Du baust ein kleines Projekt, in dem die Bausteine der Session zusammenarbeiten: Ein Skill ruft ein MCP-Tool auf und liest eine Wissensquelle, ein Hook schreibt jeden Aufruf mit, und eine Regel sperrt das Tool, das niemand benutzen soll. Alles liegt in einem Wegwerf-Ordner; deine eigene Konfiguration bleibt, wie sie ist. Das dauert etwa 20 Minuten.

Hast du unterwegs eine Übung ausgelassen, findest du sie in der Tabelle am Ende wieder.

## Selbst machen

### Übung: ein Projekt, vier Bausteine (etwa 20 Minuten)

**Ziel:** Du rufst einen eigenen Skill auf, der einen Bericht aus einem MCP-Tool und einer Wissensdatei baut. Danach liest du in einer Logdatei, dass dein Hook den Aufruf gesehen hat, und prüfst, dass das gesperrte Tool gesperrt bleibt.

**Startzustand:** ein neuer Ordner `~/cc-workshop/station2` mit der Datei `server.py` aus [S2.14](s2-14-mcp-stecker.md). Hast du den Ordner `~/cc-workshop/mcp` noch, kopierst du sie; sonst legst du sie nach S2.14, Schritt 1 neu an. Du brauchst nur Python.

```bash
# macOS / Linux / Git Bash
mkdir -p ~/cc-workshop/station2/kb ~/cc-workshop/station2/.claude/skills/room-report
cd ~/cc-workshop/station2
cp ~/cc-workshop/mcp/server.py .
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\cc-workshop\station2\kb", "$HOME\cc-workshop\station2\.claude\skills\room-report" | Out-Null
Set-Location "$HOME\cc-workshop\station2"
Copy-Item "$HOME\cc-workshop\mcp\server.py" .
```

1. **Die Verbindung ([S2.14](s2-14-mcp-stecker.md)).** Speichere als `.mcp.json` (unter Windows `"command": "python"`):

   ```json
   {
     "mcpServers": {
       "rooms": {
         "command": "python3",
         "args": ["server.py"]
       }
     }
   }
   ```

2. **Die Wissensquelle ([S2.18](s2-18-rag-und-notebooklm.md)).** Speichere als `kb/house-rules.md`:

   ```markdown
   # House rules for door codes

   - The code for the lobby may be given to any employee.
   - The code for the lab is given only to lab staff.
   - The code for the archive is never given out by chat; refer to the front desk.
   ```

3. **Der Skill ([S2.2](s2-02-skill-schreiben.md)).** Speichere als `.claude/skills/room-report/SKILL.md`. Den Ordner `.claude` legst du von Hand an, er ist ein geschützter Pfad. Der Skill startet nur, wenn du ihn aufrufst ([S2.3](s2-03-wer-skills-ausloest.md)):

   <!-- cockpit:example -->
   ```markdown
   ---
   name: room-report
   description: Reports per room who may receive its door code
   disable-model-invocation: true
   ---

   1. Call the rooms tool list_rooms.
   2. Read kb/house-rules.md.
   3. For each room, print one line: the room name, then who may receive its code according to the house rules, then the file name in brackets.
   4. End your reply with the exact line REPORT-DONE.
   ```

4. **Die Regel und der Sensor ([S2.17](s2-17-mcp-sicherheit.md), [S2.6](s2-06-hooks-als-sensoren.md)).** Speichere als `.claude/settings.json`. Die Regeln erlauben `list_rooms` und sperren `door_code`. Der Hook hängt nach jedem gelungenen Aufruf eines Tools des Servers `rooms` eine Zeile an `tool-log.txt`:

   ```json
   {
     "permissions": {
       "allow": ["mcp__rooms__list_rooms"],
       "deny": ["mcp__rooms__door_code"]
     },
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "mcp__rooms__.*",
           "hooks": [{"type": "command", "command": "echo mcp-call >> \"${CLAUDE_PROJECT_DIR}/tool-log.txt\""}]
         }
       ]
     }
   }
   ```

   Der Matcher braucht das `.*` am Ende: Ohne es vergleicht Claude Code den Text als genauen Tool-Namen, und kein Tool heißt `mcp__rooms__`.

5. Starte `claude --permission-mode default` im Ordner. Bestätige den Dialog zum Ordner und wähl bei der Frage nach dem Server „Use this MCP server“ (vorausgewählt ist die Antwort ohne Server). Gib `/room-report` ein. Erwartet: Claude ruft `list_rooms` ohne Rückfrage auf, liest die Regeldatei und antwortet mit je einer Zeile für `lobby`, `lab` und `archive`, jeweils mit `house-rules.md` in Klammern. Die letzte Zeile lautet `REPORT-DONE`.

6. **Der Sensor.** Lies in einem zweiten Terminal im selben Ordner die Logdatei (`cat tool-log.txt`, in PowerShell `Get-Content tool-log.txt`). Erwartet: eine Zeile `mcp-call`, für den einen Aufruf von `list_rooms`. Das Lesen der Regeldatei steht nicht darin: Der Matcher trifft nur die Tools des Servers.

7. **Die Sperre.** Gib ein:

   ```text
   Without reading any files, use the rooms tool door_code to get the door code of the archive.
   ```

   Erwartet: Claude nennt keinen Code. Es meldet, dass es dieses Tool nicht hat (und verweist vielleicht zusätzlich auf die Hausregel). Lies die Logdatei noch einmal: Es ist keine Zeile dazugekommen, denn einen Aufruf gab es nicht. Beende die Sitzung mit `/exit`.

**Aufräumen:** Lösch den Ordner `~/cc-workshop/station2` selbst. Skill, Hook, Regel und Server hingen nur an diesem Ordner.

**Geschafft, wenn:**

- [ ] der Bericht drei Räume nannte, die Regeldatei als Quelle angab und mit `REPORT-DONE` endete
- [ ] `tool-log.txt` nach dem Bericht genau eine Zeile enthielt
- [ ] Claude den Code des Archivs nicht nennen konnte und die Logdatei dabei unverändert blieb
- [ ] du zu jeder der vier Dateien sagen kannst, welchen Baustein sie stellt

### Extra: denselben Skill als Plugin verpacken (etwa 10 Minuten)

Ein Plugin bündelt, was du weitergeben willst ([S2.11](s2-11-plugins-buendeln.md)). Leg im Übungsordner die Ordner `station-kit/.claude-plugin` und `station-kit/skills/room-report` an, kopier deine `SKILL.md` in den zweiten und speichere als `station-kit/.claude-plugin/plugin.json`:

```json
{
  "name": "station-kit",
  "description": "The room report skill as a plugin",
  "version": "0.1.0",
  "author": { "name": "You" }
}
```

Prüf das Plugin mit `claude plugin validate ./station-kit` und starte `claude --permission-mode default --plugin-dir ./station-kit`. Gib `/station-kit:room-report` ein. Erwartet: derselbe Bericht, diesmal aus dem Plugin. Server, Regel und Hook kommen weiter aus dem Projekt; ein Plugin könnte auch sie mitbringen, dann prüfst du es wie in [S2.13](s2-13-plugin-lieferkette.md).

### Was du gebaut hast

| Datei | Baustein | Leistet |
|---|---|---|
| `.mcp.json` und `server.py` | MCP-Server | verbindet Claude mit einem System außerhalb der Dateien |
| `kb/house-rules.md` | Wissensquelle | Antworten mit Fundstelle statt aus dem Training |
| `.claude/skills/room-report/SKILL.md` | Skill | ein Ablauf, den du einmal aufschreibst und immer gleich aufrufst |
| `.claude/settings.json` | Regel und Hook | die Regel sperrt ein Tool, der Hook schreibt mit, ohne dass Claude darüber entscheidet |

### Drei Fragen zum Schluss

Beantworte sie für dich, schriftlich, je ein Satz:

1. Welchen Ablauf aus deiner Arbeit tippst du so oft, dass er ein Skill sein sollte?
2. Was soll in deinem Projekt nie ohne Spur passieren, und an welchem Ereignis würde ein Hook es mitschreiben?
3. Welches System kopierst du heute von Hand in das Gespräch, und was müsste ein Server dafür dürfen und was nicht?

### Ausgelassene Übungen nachholen

| Du willst üben | Übung | Zeit | Kapitel |
|---|---|---|---|
| wann Claude einen Skill lädt | erst die Beschreibung, dann der Inhalt | 10 Min. | [S2.1](s2-01-skills-und-commands.md#selbst-machen) |
| einen eigenen Skill schreiben und verbessern | einen Skill bauen und nachschärfen | 15 Min. | [S2.2](s2-02-skill-schreiben.md#selbst-machen) |
| steuern, wer einen Skill starten darf | wer darf den Skill starten? | 10 Min. | [S2.3](s2-03-wer-skills-ausloest.md#selbst-machen) |
| einen mitgelieferten Skill einsetzen | `/simplify` an einer eigenen Änderung | 10 Min. | [S2.4](s2-04-mitgelieferte-skills.md#selbst-machen) |
| Skills mit Argumenten und frischen Daten | ein Skill mit Argument und Live-Diff | 15 Min. | [S2.5](s2-05-lebendige-prompts.md#selbst-machen) |
| sehen, wann welcher Hook feuert | drei Sensoren in einer Logdatei | 10 Min. | [S2.6](s2-06-hooks-als-sensoren.md#selbst-machen) |
| Text über einen Hook in den Kontext legen | Briefing und Ticket-Notiz | 10 Min. | [S2.7](s2-07-hook-ereignisse.md#selbst-machen) |
| einen Befehl blocken, bevor er läuft | einen Wächter einrichten und blocken sehen | 15 Min. | [S2.8](s2-08-hook-einrichten.md#selbst-machen) |
| einen Hook an einen Skill binden | ein Hook, der mit dem Skill kommt | 10 Min. | [S2.9](s2-09-hook-typen.md#selbst-machen) |
| eine Datei vor Claudes Werkzeugen schützen | das Secure Diff Gate | 20 Min. | [S2.10](s2-10-hook-ausgaben.md#selbst-machen) |
| ein Plugin bauen und ohne Installation laden | ein Mini-Plugin bauen und laden | 15 Min. | [S2.11](s2-11-plugins-buendeln.md#selbst-machen) |
| Scopes von Plugins zuordnen | Bestand lesen und Scopes zuordnen | 10 Min. | [S2.12](s2-12-plugin-lebenszyklus.md#selbst-machen) |
| ein fremdes Plugin vor der Installation lesen | ein verdächtiges Plugin prüfen, ohne es zu laden | 15 Min. | [S2.13](s2-13-plugin-lieferkette.md#selbst-machen) |
| einen MCP-Server anbinden | einen Server anbinden und ein Tool aufrufen lassen | 15 Min. | [S2.14](s2-14-mcp-stecker.md#selbst-machen) |
| Server per Befehl anlegen und per Umgebung steuern | einen Server im Scope project anlegen | 15 Min. | [S2.15](s2-15-mcp-einrichten.md#selbst-machen) |
| was mit zu großen Tool-Ausgaben passiert | eine zu große Ausgabe erleben | 10 Min. | [S2.16](s2-16-mcp-im-detail.md#selbst-machen) |
| ein einzelnes MCP-Tool sperren | ein MCP-Tool sperren und die Sperre prüfen | 15 Min. | [S2.17](s2-17-mcp-sicherheit.md#selbst-machen) |
| Antworten aus eigenen Quellen mit Fundstelle | eine Wissensbasis aus Dateien, mit Quellenangabe | 15 Min. | [S2.18](s2-18-rag-und-notebooklm.md#selbst-machen) |
| Quellen einordnen und Fundstellen prüfen | Quellen sortieren und eine Fundstelle prüfen | 10 Min. | [S2.19](s2-19-rag-grenzen.md#selbst-machen) |

Weiter geht es in Session 3 mit Agenten, ab [S3.1](s3-01-was-ist-ein-agent.md).

## Check

Du kannst die Bausteine aus Session 2 in einem Projekt verbinden und für jeden sagen, wo er steht und wer ihn auslöst.

1. Wer hat in der Übung den Skill ausgelöst, wer das MCP-Tool und wer den Hook?
2. Warum stand nach dem gesperrten Auftrag keine neue Zeile in der Logdatei?
3. Was davon würde in ein Plugin wandern, wenn du das Projekt an dein Team weitergibst, und was müsste das Team vorher prüfen?

<details><summary>Auflösung</summary>

1. Den Skill du, mit `/room-report`; Claude konnte ihn wegen `disable-model-invocation: true` nicht von selbst starten. Das MCP-Tool hat Claude aufgerufen, weil der Skill es verlangt. Den Hook hat Claude Code ausgelöst, bei dem Ereignis PostToolUse, ohne dass Claude darüber entscheidet.
2. Die Deny-Regel nimmt `door_code` aus Claudes Werkzeugen; es gab also keinen Aufruf, und PostToolUse feuert nur nach einem gelungenen Aufruf.
3. Der Skill, und wenn gewünscht auch Hook und Server (`hooks/hooks.json`, `.mcp.json` im Plugin). Das Team liest vorher genau diese Dateien, denn Hooks und Server eines Plugins laufen mit den Rechten der Person, die es lädt.

</details>

## Weiterlesen

- [S2.2 · Eine SKILL.md schreiben](s2-02-skill-schreiben.md)
- [S2.6 · Hooks als Sensoren: die drei Eckpfeiler](s2-06-hooks-als-sensoren.md)
- [S2.11 · Plugins: ein Bündel schnüren](s2-11-plugins-buendeln.md)
- [S2.14 · MCP: der Integrationsstecker](s2-14-mcp-stecker.md)
- [S2.17 · MCP-Sicherheit und ein eigener Server](s2-17-mcp-sicherheit.md)
- [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](s2-18-rag-und-notebooklm.md)
- [S1.20 · Praxis-Station Session 1: alles in einem Ablauf](s1-20-praxis-station-1.md)
- [S4.11 · Abschluss: ein kleiner Build](s4-11-abschluss-kleiner-build.md), der Abschluss deines ganzen Pfads
