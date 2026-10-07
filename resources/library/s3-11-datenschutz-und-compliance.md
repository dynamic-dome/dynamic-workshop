---
id: S3.11
type: lesson
title: Datenschutz, Aufbewahrung und regulierte Branchen
shelf: security
level: deep-dive
minutes: 25
requires: [S3.9, S2.8]
safety_floor: false
transferable: true
outcome: "Ich kann die Aufbewahrungsstufen der Claude-Pläne benennen, Anliegen wie „nichts speichern“, „kein Gedächtnis“ oder „keine Schlüssel in Dateien“ einer Kontrolle zuordnen und einen PreToolUse-Hook einrichten, der sensible Muster in Datei-Schreibzugriffen blockt."
sources:
  - https://code.claude.com/docs/en/data-usage
  - https://code.claude.com/docs/en/zero-data-retention
  - https://code.claude.com/docs/en/memory
  - https://code.claude.com/docs/en/hooks
aliases: []
---

# S3.11 · Datenschutz, Aufbewahrung und regulierte Branchen

<!-- meta:start -->
> **Regal:** [Gegenprüfung & Compliance](README.md#security) · **Stufe:** Vertiefung · **~25 Min** · **Voraussetzungen:** [S3.9 Geschützte Pfade und Sandbox-Stufen](s3-09-geschuetzte-pfade-und-sandbox.md) · [S2.8 Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
>
> ← [S3.10 Netzwerk und Skills härten](s3-10-netzwerk-und-skills-haerten.md) · [Bibliothek](README.md) · [S3.12 Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](s3-12-zeitgesteuert-arbeiten.md) →
<!-- meta:end -->

## Schnellcheck

- Weißt du, welche Trainings- und Aufbewahrungsregel für deinen Claude-Plan gilt?
- Kannst du ohne Nachschlagen sagen, welcher Exit-Code einen PreToolUse-Hook zum Blocken bringt?

## Auf einen Blick

Wie lange Anthropic deine Prompts und Antworten aufbewahrt und ob damit trainiert wird, hängt vom Plan ab: bei Free, Pro und Max je nach deiner Einstellung 5 Jahre oder 30 Tage, bei Team, Enterprise und API 30 Tage ohne Training, mit Zero Data Retention (ZDR, nur für von Anthropic freigeschaltete Organisationen) keine Speicherung nach der Antwort. Daneben gibt es Kontrollen auf deiner Seite: Auto-Memory abschalten, ein Hook gegen sensible Muster, Regeln für ausgehende Anfragen, menschliche Freigabe.

Dieses Kapitel ist keine Rechtsberatung. Welche Vorschrift für dich gilt und was sie verlangt, klärt dein Compliance-Team. Hier lernst du, was jede Kontrolle technisch tut und wo sie endet.

## Bild im Kopf

Denk an die Aufbewahrungsrichtlinie für Videoaufnahmen. Der Consumer-Plan ist ein Ringspeicher, dessen Dauer davon abhängt, ob du das Archiv erlaubst; wer es erlaubt, erlaubt dem Hersteller auch, die Aufnahmen zur Produktverbesserung zu nutzen. Ein kommerzieller Plan ist ein 30-Tage-Ringspeicher ohne Weitergabe. ZDR sind Kameras, die laufen, aber nichts aufzeichnen: Dafür fallen Funktionen weg, die eine Aufzeichnung brauchen.

## Im Detail

### Aufbewahrung und Training je Plan

| Plan | Training mit deinen Daten? | Aufbewahrung | Hinweis |
|---|---|---|---|
| **Free, Pro, Max** | nur, wenn du es erlaubst | erlaubt: 5 Jahre; nicht erlaubt: 30 Tage | Consumer-Pläne; die Einstellung änderst du jederzeit unter claude.ai/settings/data-privacy-controls |
| **Team, Enterprise, API** | nein (Standard) | 30 Tage | kommerzielle Pläne |
| **Enterprise mit ZDR** | nein | keine Speicherung nach der Antwort | nur für freigeschaltete Organisationen; einige Funktionen sind abgeschaltet |

ZDR ist nicht im normalen Enterprise-Plan enthalten und lässt sich nicht in den Admin-Einstellungen einschalten. Anthropic prüft die Berechtigung und schaltet ZDR je Organisation frei. Auch mit ZDR darf Anthropic Daten aufbewahren, wo das Gesetz es verlangt oder um Missbrauch zu bekämpfen. Weil nichts gespeichert wird, sind Funktionen abgeschaltet, die gespeicherte Sitzungsdaten brauchen, darunter Cloud-Sitzungen, Remote Control und `/feedback`. ZDR gilt nur für die direkte Anthropic-Plattform; bei Amazon Bedrock, Google Cloud oder Microsoft Foundry gelten deren Regeln. Es deckt auch nicht alles: Chat auf claude.ai, Cowork und was MCP-Server oder andere Integrationen verarbeiten, fallen nicht darunter.

### Was auf deinem Rechner bleibt

Prompts und Antworten gehen per TLS 1.2 oder neuer verschlüsselt an den Anbieter; wie sie dort gespeichert sind, hängt vom Anbieter ab. Auf deinem Rechner speichert Claude Code die Sitzungsprotokolle im Klartext unter `~/.claude/projects/`, standardmäßig 30 Tage lang, damit du Sitzungen fortsetzen kannst. Die Dauer stellst du mit `cleanupPeriodDays` ein. Personendaten, die in einer Sitzung auftauchen, liegen also auch lokal.

### Telemetrie abschalten

Claude Code sendet, je nach Anbieter und Anmeldung, Nutzungsmetriken und Fehlerberichte. Die Metriken enthalten laut Doku nie deinen Code, deine Prompts oder Dateipfade. Abschalten kannst du beides getrennt:

```bash
export DISABLE_TELEMETRY=1           # no operational metrics; macOS/Linux/Git Bash
export DISABLE_ERROR_REPORTING=1     # no error reports
```

```powershell
$env:DISABLE_TELEMETRY = "1"         # Windows PowerShell, this session only
$env:DISABLE_ERROR_REPORTING = "1"
```

Telemetrie abzuschalten ändert nichts daran, ob mit deinen Gesprächen trainiert wird; das regeln Plan und Datenschutzeinstellung oben.

### Welche Kontrolle für welches Anliegen

Jede Kontrolle tut etwas Bestimmtes und lässt anderes offen. Welche davon dein Unternehmen für welche Vorschrift verlangt, legt dein Compliance-Team fest; die Tabelle zeigt nur, was sie technisch leisten.

| Anliegen | Kontrolle | Was sie tut | Was sie nicht abdeckt |
|---|---|---|---|
| Nach der Antwort nichts bei Anthropic speichern | ZDR | keine Speicherung nach der Antwort | gilt nur für die direkte Plattform; Chat, Cowork und Integrationen bleiben draußen |
| Keine Inhalte aus früheren Sitzungen in neue Prompts ziehen | Auto-Memory aus: `"autoMemoryEnabled": false` in den Settings, der Schalter in `/memory` oder `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | Claude schreibt und liest kein Gedächtnis mehr | die Sitzungsprotokolle auf deinem Rechner bleiben |
| Keine Schlüssel oder Nummern in Dateien | PreToolUse-Hook mit Matcher `Write\|Edit` (siehe unten) | blockt einen Schreibzugriff, wenn ein Muster passt | erkennt nur Muster, die er kennt; Schreibwege über die Shell, etwa eine Umleitung `>`, deckt er nicht ab |
| Ausgehende Webabrufe begrenzen | `WebFetch(domain:…)`-Regeln, für Sandbox-Befehle `sandbox.network.deniedDomains` ([S3.10](s3-10-netzwerk-und-skills-haerten.md)) | Webabrufe auf freigegebene Domains beschränken, einzelne Domains sperren | jede Regel gilt nur für ihr Werkzeug |
| Ein Mensch gibt Änderungen frei | ein Modus, der fragt (`default`), oder eine Ask-Regel ([S3.8](s3-08-rechte-fuer-autonomie.md)) | Claude Code fragt vor der Aktion | in `dontAsk` fragt niemand, eine Ask-Regel wird dort abgelehnt; in `auto` fragt nur noch die ausdrückliche Ask-Regel, nicht mehr der Modus |

Ein Beispiel dafür, wie das zusammenspielt: Zutrittsprotokolle enthalten Personendaten. Wer sie mit Claude Code bearbeitet, könnte Auto-Memory abschalten, einen Hook gegen Personenkennzahlen setzen und bei sensiblen Änderungen eine Freigabe verlangen. Ob dein Unternehmen das fordert und ob es genügt, ist nicht Sache dieses Kapitels.

Jeder weitere Anbieter, den du anbindest, bekommt Daten unter seinen eigenen Regeln: ein zweites Coding-Werkzeug ([S4.2](s4-02-codex-schwarm.md)) ebenso wie ein Notizbuch-Dienst ([S2.18](s2-18-rag-und-notebooklm.md)). Die Regeln des Abschnitts „Aufbewahrung und Training je Plan“ gelten nur für Anthropic.

### Ein Hook gegen sensible Muster

Der Hook prüft vor jedem Schreibzugriff den neuen Dateitext. Write schickt ihn als `tool_input.content`, Edit als `tool_input.new_string`. Von den Exit-Codes blockt nur `exit 2` den Schreibzugriff, jeder andere Code lässt ihn durch ([S2.8](s2-08-hook-einrichten.md)). Kann das Skript seine Eingabe nicht lesen, blockt es lieber, statt still alles durchzulassen. Den Treffer selbst gibt es absichtlich nicht aus, weil stderr als Begründung an Claude geht. Das ist die getestete Vorlage (Bash, braucht `jq`):

<!-- cockpit:example -->
```bash
#!/bin/bash
# sensitive-data-scanner.sh - PreToolUse hook (matcher "Write|Edit"): block sensitive data in file writes.
# tested asset: resources/demos/assets/hooks/sensitive-data-scanner.sh
#
# Write sends the new file text as tool_input.content, Edit sends it as tool_input.new_string.
# exit 2 blocks the write; any other non-zero exit code would let it through.

INPUT=$(cat)

# Fail closed: if the input cannot be read, block instead of silently allowing the write.
# Readable means a JSON object: jq would turn "null" into empty content without complaint.
READ_CONTENT='if type != "object" then error("hook input is not a JSON object") else
  .tool_input.content // .tool_input.new_string // ""
end'
if ! CONTENT=$(printf '%s' "$INPUT" | jq -er "$READ_CONTENT" 2>/dev/null); then
  echo "SCANNER: could not read the hook input (is jq installed?) - blocking to stay safe." >&2
  exit 2
fi

# Adapt to your domain (card reader formats, internal IP ranges, ...). grep -E has no \d: use [0-9].
PATTERNS='([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(sk-|pk_)[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|password[[:space:]]*=[[:space:]]*"[^"]+")'

if printf '%s' "$CONTENT" | grep -qiE -- "$PATTERNS"; then
  # Do not echo the match itself: stderr goes to Claude as the block reason.
  echo "BLOCKED: sensitive data pattern detected in the file content." >&2
  echo "Redact or remove it before writing (use an environment variable or a secret store)." >&2
  exit 2
fi

exit 0
```

Dieselbe Prüfung als zweite getestete Vorlage in Python, für Rechner ohne Bash oder `jq`:

```python
# sensitive-data-scanner.py - PreToolUse hook (matcher "Write|Edit"): block sensitive data in file writes.
# tested asset: resources/demos/assets/hooks/sensitive-data-scanner.py
#
# Same checks as sensitive-data-scanner.sh, for machines without bash or jq.
# exit 2 blocks the write; any other non-zero exit code would let it through.
import json
import re
import sys

PATTERN = re.compile(
    r"[0-9]{3}-[0-9]{2}-[0-9]{4}"
    r"|[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}"
    r"|(sk-|pk_)[A-Za-z0-9]{20,}"
    r"|AKIA[A-Z0-9]{16}"
    r'|password\s*=\s*"[^"]+"',
    re.IGNORECASE,
)

# Fail closed: if the input cannot be read, block instead of silently allowing the write.
try:
    tool_input = json.load(sys.stdin)["tool_input"]
    content = tool_input.get("content") or tool_input.get("new_string") or ""
    if not isinstance(content, str):
        raise ValueError("content is not a string")
except Exception:
    print("SCANNER: could not read the hook input - blocking to stay safe.", file=sys.stderr)
    sys.exit(2)

if PATTERN.search(content):
    # Do not print the match itself: stderr goes to Claude as the block reason.
    print("BLOCKED: sensitive data pattern detected in the file content.", file=sys.stderr)
    print("Redact or remove it before writing (use an environment variable or a secret store).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
```

Die Muster sind Beispiele für Schlüssel, Kartennummern und Kennwort-Zuweisungen; ersetze sie durch die Formate deiner Arbeit. Hooks sind Wächter nach bestem Bemühen, keine harte Grenze.

## Selbst machen

### Übung: den Scanner einrichten und blocken sehen (etwa 15 Minuten)

**Ziel:** Du richtest den Scanner in einem Wegwerf-Projekt ein, prüfst ihn von Hand und siehst, wie er einen Schreibzugriff mit einem Schlüssel blockt und einen harmlosen durchlässt.

**Startzustand:** Du arbeitest im Ordner `~/cc-workshop/scanner`; deine globale Konfiguration bleibt unberührt. Wähl deine Variante. **Variante A (Bash):** macOS, Linux oder Windows mit Git Bash, dazu `jq` ([Werkstatt erweitern](../reference/werkstatt-erweitern.md#jq)). **Variante B (Python):** nur Python, ohne `jq`; sie nutzt die zweite getestete Vorlage unten, mit denselben Mustern, und läuft auf jedem System. Unter macOS und Linux heißt Python oft `python3`: Nimm dann überall `python3` statt `python`.

1. Leg den Ordner an und wechsle hinein. Bash:

   ```bash
   mkdir -p ~/cc-workshop/scanner/.claude/hooks
   cd ~/cc-workshop/scanner
   ```

   PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force "$HOME\cc-workshop\scanner\.claude\hooks" | Out-Null
   Set-Location "$HOME\cc-workshop\scanner"
   ```

2. Leg das Skript mit einem Editor an (`.claude` ist ein geschützter Pfad, Claude würde dort nachfragen). Variante A: der Bash-Block aus „Im Detail“ als `.claude/hooks/sensitive-data-scanner.sh`. Variante B: der Python-Block aus „Im Detail“ als `.claude/hooks/sensitive-data-scanner.py`.

3. Teste das Skript von Hand, bevor Claude es benutzt. Variante A in Bash:

   ```bash
   echo '{"tool_name":"Write","tool_input":{"file_path":"t.txt","content":"api_key = pk_abcdefghijklmnopqrstuv"}}' | bash .claude/hooks/sensitive-data-scanner.sh; echo "exit=$?"
   echo '{"tool_name":"Write","tool_input":{"file_path":"t.txt","content":"hello"}}' | bash .claude/hooks/sensitive-data-scanner.sh; echo "exit=$?"
   echo 'not json' | bash .claude/hooks/sensitive-data-scanner.sh; echo "exit=$?"
   ```

   Variante A in PowerShell (mit Git Bash) und Variante B: Schreib vor das `|` dieselben JSON-Zeilen, hinter das `|` `bash .claude/hooks/sensitive-data-scanner.sh` bzw. `python .claude/hooks/sensitive-data-scanner.py`, und gib den Code in PowerShell mit `"exit=$LASTEXITCODE"` aus, in Bash mit `echo "exit=$?"`. Erwartet: Beim ersten Aufruf erscheint `BLOCKED: sensitive data pattern detected in the file content.` und `exit=2`. Beim zweiten kommt keine Ausgabe und `exit=0`. Beim dritten, einer Eingabe ohne JSON, erscheint `SCANNER: could not read the hook input` und `exit=2`: Der Scanner fällt geschlossen.
4. Trag den Hook in `.claude/settings.json` ein. Variante A:

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "bash \"${CLAUDE_PROJECT_DIR}\"/.claude/hooks/sensitive-data-scanner.sh"
             }
           ]
         }
       ]
     }
   }
   ```

   Variante B (Exec-Form nach der Hooks-Doku, ohne Quoting-Fallen):

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python",
               "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/sensitive-data-scanner.py"]
             }
           ]
         }
       ]
     }
   }
   ```

5. Starte `claude --permission-mode acceptEdits`, bestätige den Vertrauensdialog und gib `/hooks` ein. Erwartet: ein Eintrag unter PreToolUse. Schließ die Ansicht mit `Esc`.
6. Gib ein: `Create the file settings-test.txt containing exactly this line: api_key = pk_abcdefghijklmnopqrstuv`. Erwartet: Die Datei entsteht nicht, ohne dass eine Rückfrage kam. Im Transkript (`Ctrl+O`) oder in Claudes Antwort steht `BLOCKED: sensitive data pattern detected`; dieser Text stammt aus deinem Skript. Weigert sich Claude von selbst und die Meldung fehlt, hat nicht der Hook geblockt: Formulier den Auftrag um.
7. Gib ein: `Create the file ok.txt containing exactly this line: hello`. Erwartet: Die Datei entsteht ohne Hook-Meldung.
8. Beende die Sitzung mit `/exit` und prüf in einem zweiten Terminal: `ls` (PowerShell `dir`) zeigt `ok.txt`, aber kein `settings-test.txt`.

**Aufräumen:** Lösch den Ordner `~/cc-workshop/scanner` selbst. Der Hook galt nur dort.

**Geschafft, wenn:**

- [ ] der Handtest `exit=2` für den Schlüssel, `exit=0` für `hello` und `exit=2` für die Eingabe ohne JSON zeigte
- [ ] `/hooks` den Eintrag unter PreToolUse zeigte
- [ ] `settings-test.txt` nicht existierte und `ok.txt` existierte
- [ ] du erklären kannst, was passiert wäre, hätte das Skript bei einem Treffer mit `exit 1` geendet

### Extra: ein eigenes Muster (etwa 5 Minuten)

**Ziel:** Du passt den Scanner an ein Format an, das in deiner Arbeit vorkommt.

**Startzustand:** der Ordner `~/cc-workshop/scanner` aus der Übung, falls noch nicht gelöscht.

1. Ergänz im Skript ein Muster, etwa für ein Ausweis-ID-Format deiner Arbeit, in `grep -E`-Schreibweise `[0-9]` statt `\d`. Teste es mit dem Handtest aus Schritt 3 mit einem erfundenen Wert in `content`.

**Geschafft, wenn:**

- [ ] dein Muster einen erfundenen Wert blockt und `hello` weiter durchläuft

## Typische Fallen

- **Telemetrie aus heißt nicht Training aus.** `DISABLE_TELEMETRY` stoppt Nutzungsmetriken. Ob mit deinen Gesprächen trainiert wird, regeln Plan und Datenschutzeinstellung.
- **Plötzlich wird jeder Schreibzugriff geblockt.** Das Skript konnte seine Eingabe nicht lesen und ist absichtlich geschlossen gefallen. Bei Variante A fehlt meist `jq`: Installier es oder nimm Variante B.
- **Der Hook läuft gar nicht.** Hast du den Vertrauensdialog bestätigt? Stimmt der Pfad in `settings.json`? Ein falscher Pfad lässt den Wächter still ausgeschaltet. `/hooks` zeigt, was registriert ist.
- **Der Scanner lässt den Schlüssel durch.** Endet er bei einem Treffer mit `exit 1` statt `exit 2`, läuft der Schreibzugriff trotzdem. Auch ein Schreibweg über die Shell (`echo … > datei`) trifft den Matcher `Write|Edit` nicht.
- **Auto-Memory abschalten mit `--bare`.** `--bare` ist ein Modus für Skripte, der beim Start Hooks, Skills, Plugins, MCP-Server, Auto-Memory und CLAUDE.md gar nicht lädt ([S4.3](s4-03-headless.md)). In deiner normalen Sitzung schaltest du Auto-Memory mit `autoMemoryEnabled` oder `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` ab.
- **ZDR gilt für jede Anmeldung.** Es gilt nur für Anmeldungen in der ZDR-Organisation: Wer sich mit einem privaten Konto oder einem API-Schlüssel aus einer anderen Organisation anmeldet, ist nicht abgedeckt.

## Check

Du kannst die Aufbewahrungsstufen nennen, Anliegen einer Kontrolle zuordnen und einen Hook gegen sensible Muster einrichten.

1. Ordne zu: Welche Kontrolle passt zu (a) „nach der Antwort nichts bei Anthropic speichern“, (b) „keine Inhalte früherer Sitzungen in neue Prompts ziehen“, (c) „keine Schlüssel in Dateien schreiben“, und was deckt jede nicht ab?
2. Welcher Exit-Code lässt einen PreToolUse-Hook blocken, und was tut der Scanner dieses Kapitels, wenn er seine Eingabe nicht lesen kann?
3. Wie lange werden Daten bei einem Pro-Plan aufbewahrt, wenn du Training erlaubst, und wie lange, wenn nicht?

<details><summary>Auflösung</summary>

1. (a) ZDR; es gilt nur für die direkte Anthropic-Plattform, Chat, Cowork und Integrationen bleiben draußen. (b) Auto-Memory aus; die Sitzungsprotokolle auf deinem Rechner bleiben. (c) der PreToolUse-Hook auf `Write|Edit`; er erkennt nur bekannte Muster und deckt Schreibwege über die Shell nicht ab.
2. `exit 2`; jeder andere Code lässt den Schreibzugriff durch. Der Scanner endet bei unlesbarer Eingabe selbst mit `exit 2` und blockt: Ein kaputter Wächter soll die Tür schließen, nicht öffnen.
3. Mit erlaubtem Training 5 Jahre, ohne 30 Tage.

</details>

<details><summary>Quizfrage</summary>

**Frage:** Ein Team auf dem Team-Plan soll laut seiner Datenschutzabteilung „nichts mehr bei Anthropic speichern“. Was sagst du?

- **Richtig:** Dafür braucht es ZDR, das Anthropic je Organisation freischaltet. Der Team-Plan trainiert standardmäßig nicht, bewahrt aber 30 Tage auf.
  - Warum: Der Team-Plan bewahrt 30 Tage auf; erst mit ZDR speichert Anthropic nach der Antwort grundsätzlich nichts. Anthropic prüft die Berechtigung und schaltet ZDR je Organisation frei.
- Falsch: `DISABLE_TELEMETRY=1` in den Umgebungsvariablen aller Rechner genügt, denn damit speichert Claude Code nichts mehr bei Anthropic.
  - Warum: `DISABLE_TELEMETRY` stoppt nur Nutzungsmetriken, und die enthalten laut Doku nie deine Prompts. Wie lange Prompts und Antworten bleiben, hängt vom Plan ab.
- Falsch: Ein Admin schaltet ZDR in den Einstellungen der Organisation ein, danach gilt es für alle Anmeldungen und für alle Funktionen.
  - Warum: ZDR lässt sich nicht in den Admin-Einstellungen einschalten: Anthropic prüft und schaltet es frei. Es gilt nur für Anmeldungen in der ZDR-Organisation, einige Funktionen entfallen.
- Falsch: Jeder Enterprise-Plan enthält ZDR bereits, deshalb ist der Wechsel vom Team-Plan auf Enterprise die einzige nötige Änderung.
  - Warum: Der normale Enterprise-Plan enthält kein ZDR. Ohne Freischaltung durch Anthropic bleibt es auch dort bei 30 Tagen Aufbewahrung.

</details>

## Weiterlesen

- [Datennutzung und Aufbewahrung](https://code.claude.com/docs/en/data-usage)
- [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention)
- [Auto-Memory ein- und ausschalten](https://code.claude.com/docs/en/memory)
- [Hooks-Referenz](https://code.claude.com/docs/en/hooks)
- [S3.10 · Netzwerk und Skills härten](s3-10-netzwerk-und-skills-haerten.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S2.13 · Lieferkettenrisiken bei Plugins](s2-13-plugin-lieferkette.md)
- [S2.17 · MCP-Sicherheit und ein eigener Server](s2-17-mcp-sicherheit.md)
- [S4.2 · Codex-Schwarm und die Datenfluss-Grenze](s4-02-codex-schwarm.md)
- [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](s2-18-rag-und-notebooklm.md)
- [S4.3 · Headless: claude -p als Pipeline-Stufe](s4-03-headless.md)
- Getestete Hook-Dateien: [`sensitive-data-scanner.sh`](../demos/assets/hooks/sensitive-data-scanner.sh), [`sensitive-data-scanner.py`](../demos/assets/hooks/sensitive-data-scanner.py)
