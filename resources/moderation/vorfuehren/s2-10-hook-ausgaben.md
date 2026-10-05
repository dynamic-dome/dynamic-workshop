# Vorführen: S2.10 · Hook-Ausgaben und das Secure Diff Gate

> Demo und Hinweise für Moderierende zum Kapitel [S2.10 · Hook-Ausgaben und das Secure Diff Gate](../../library/s2-10-hook-ausgaben.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Secure Diff Gate, Schreibschutz per Hook

**Ziel:** Einen PreToolUse-Hook zeigen, der Claude am Schreiben in sensible Dateien **hindert** (`.env`, `secrets/`, `*.pem`). Das ist Zutrittskontrolle für Code.

**Vorbereitung:** Kopiere das getestete Gate aus dem Repo und trag es in die `.claude/settings.json` des Demo-Projekts ein:

```bash
mkdir -p ~/.claude/hooks
cp resources/demos/assets/hooks/secure-diff-gate.sh ~/.claude/hooks/   # Windows without jq: secure-diff-gate.py
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/secure-diff-gate.sh"
          }
        ]
      }
    ]
  }
}
```

Das Gate liest das Ziel aus `tool_input.file_path` (absolut; unter Windows mit Backslashes, die es vereinheitlicht) und blockt mit exit 2, in jeder Schreibweise (`.ENV` ist unter Windows und macOS dieselbe Datei wie `.env`). Kann es seine Eingabe nicht lesen, etwa weil `jq` fehlt, blockt es ebenfalls, wie der Wächter aus [S2.8](../../library/s2-08-hook-einrichten.md).

**Die Grenze des Gates:** Der Matcher `Write|Edit` sieht keine Shell-Befehle. `echo X > .env` über das Bash- oder PowerShell-Tool geht am Gate vorbei. Für eine harte Grenze trägst du zusätzlich eine Deny-Regel ein, etwa `Edit(./.env)`: Sie gilt für die Datei-Tools, für Datei-Befehle, die Claude Code in Bash erkennt, und für Umleitungsziele wie `> .env`. Gegen beliebige Unterprozesse, die Dateien indirekt schreiben, hilft erst die Sandbox ([S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md)).

**Schritt 1: die Hook-Konfiguration zeigen.** Öffne die Settings-Datei und erkläre:

- Der Matcher `Write|Edit` feuert bei jeder Dateiänderung über diese beiden Tools, nicht bei Shell-Befehlen.
- Das Skript prüft den Zielpfad gegen ein Muster.
- Passt er zu `.env`, `.pem`, `secrets/` oder `credentials`, heißt das exit 2 = BLOCK.

**Schritt 2: den Block auslösen.** In Claude Code:

```
Create a .env file with DATABASE_URL=postgres://localhost/mydb
```

Beobachte: Claude versucht zu schreiben → der Hook feuert → eine **BLOCKED**-Meldung erscheint → Claude meldet, dass es nicht weitermachen kann.

**Schritt 3: zeigen, dass normale Schreibzugriffe durchgehen.**

```
Create a file called utils.py with a hello world function
```

Das geht durch: Der Hook prüft den Pfad, findet kein sensibles Muster und endet mit 0.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 Minuten (Schritt 1: 1 Min., Schritt 2: 2 Min., Schritt 3: 1 Min.).

**Sagen:**

- Schritt 1: „Das ist ein Türcontroller mit Sperrliste. Diese Pfade sind wie der Serverraum: kein Zutritt ohne ausdrückliche Freigabe."
- Schritt 2: „Claude hat nicht beschlossen, die .env-Datei auszulassen. Der Hook hat diesen Schreibzugriff geblockt. Das ist kein Vorschlag an das Modell, sondern eine Sperre an dieser Tür. Die Shell ist eine andere Tür; dafür gibt es Deny-Regeln und die Sandbox."
- Schritt 3: „Normale Türen gehen normal auf. Nur die geschützten Zonen sind zu. Least Privilege in Aktion."
- Zum Schluss: „In eurer Zutrittskontrolle habt ihr Zonen. Manche Türen sind immer offen (Lobby), manche brauchen eine Karte (Büros), manche bleiben ohne ausdrückliche Freigabe zu (Tresor). Dieser Hook ist die Tresor-Regel für euren Code."

**Wenn etwas schiefgeht:**

- **Das Bash-Quoting bricht live:** Nimm das vorbereitete, getestete Skript aus dem Repo: [`resources/demos/assets/hooks/secure-diff-gate.sh`](../../demos/assets/hooks/secure-diff-gate.sh). Kopiere es nach `~/.claude/hooks/` und trag es mit `command: bash ~/.claude/hooks/secure-diff-gate.sh` ein. Gleiches Verhalten, kein Inline-Quoting, das schiefgehen kann.
- **`jq` fehlt (Windows ohne Git Bash):** Das Gate blockt dann jeden Schreibzugriff und meldet, dass es seine Eingabe nicht lesen kann. Nimm die Python-Variante ohne `jq`, [`resources/demos/assets/hooks/secure-diff-gate.py`](../../demos/assets/hooks/secure-diff-gate.py) (keine externen Abhängigkeiten). Trag sie als `"command": "python \"$HOME/.claude/hooks/secure-diff-gate.py\""` ein (unter Windows `python`, sonst `python3`). `$HOME` lösen Git Bash und PowerShell auf, `%USERPROFILE%` keine von beiden. Beide Skripte sind geprüft: Sie blocken Schreibzugriffe auf `.env`, `*.pem`, `secrets/` und `credentials` (exit 2), lassen normale Schreibzugriffe durch (exit 0) und blocken, wenn sie ihre Eingabe nicht lesen können.
- **Der Hook feuert, blockt aber nicht (exit 0 statt 2):** Teste das Skript außerhalb von Claude von Hand: `echo '{"tool_input":{"file_path":".env"}}' | bash ~/.claude/hooks/secure-diff-gate.sh; echo "exit=$?"` muss `exit=2` zeigen.
- **`settings.json` lässt sich nicht parsen:** Häufige Ursache sind nicht maskierte Anführungszeichen im Inline-Befehl. Leg das Skript in eine eigene Datei und verweise per Pfad darauf.

</details>
