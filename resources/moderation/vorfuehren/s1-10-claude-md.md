# Vorführen: S1.10 · CLAUDE.md: die Hausordnung des Projekts

> Demo und Hinweise für Moderierende zum Kapitel [S1.10 · CLAUDE.md: die Hausordnung des Projekts](../../library/s1-10-claude-md.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: CLAUDE.md live

**Ziel:** Zeigen, wie eine CLAUDE.md entsteht, wie Claude beendet und neu gestartet wird und danach die Projektkonventionen noch kennt, ohne dass du sie wiederholst. Schritt 5 der Demo, ein Memory-Eintrag, steht in [S1.11](s1-11-gedaechtnis-ebenen.md).

**Schritt 1: das Demo-Projekt anlegen**

Im Terminal (außerhalb von Claude Code oder über Claudes Bash):

```
mkdir -p ~/cc-workshop/demos/demo-1.2 && cd ~/cc-workshop/demos/demo-1.2 && git init
```

Starte dann Claude Code in diesem Ordner:

```
claude
```

**Schritt 2: die CLAUDE.md über Claude Code anlegen**

Tipp in Claude Code:

```
Create a CLAUDE.md file for this project. It's a Python CLI tool for access control management.
Include these conventions:
- Python 3.11+
- pytest for all tests (pytest-cov for coverage)
- black for formatting (line length 88)
- Type hints required on all function signatures
- Explicit error handling — never use bare except clauses
- No global state — all configuration passed as parameters
- Log using the standard logging module, not print statements
- The legacy module legacy_panel_parser.py must never be modified
```

**Erwartet:** Claude legt `./CLAUDE.md` mit diesen Konventionen in sauberem Markdown an.

Zeig die Datei kurz. Du kannst Claude bitten: „Show me the CLAUDE.md you just created."

**Schritt 3: beenden und neu starten**

Tipp in Claude Code:

```
exit
```

Starte dann neu:

```
claude
```

**Schritt 4: prüfen, ob die CLAUDE.md geladen wurde**

Tipp in Claude Code:

```
What are the coding conventions for this project?
```

**Erwartet:** Claude zählt die Konventionen aus der CLAUDE.md auf: pytest, black, Type Hints, kein globaler Zustand, kein nacktes `except` und so weiter. Es hat die CLAUDE.md beim Start gelesen.

Eine Nachfrage zum Festigen:

```
If I ask you to modify legacy_panel_parser.py, what would you do?
```

**Erwartet:** Claude sagt, dass es ablehnen oder nachfragen würde, weil die CLAUDE.md verbietet, diese Datei zu ändern.

<details><summary>Für Moderierende</summary>

**Dauer:** Die ganze Demo 1.2 dauert etwa 10 Minuten, Schritt 5 aus [S1.11](s1-11-gedaechtnis-ebenen.md) eingeschlossen.

**Sagen:**

- Schritt 1: „Frisches Projekt. Keine CLAUDE.md, kein Memory. Claude weiß über dieses Projekt nichts außer dem, was ich ihm jetzt sage."
- Schritt 2: „Das ist unsere Hausordnung. Jede Regel steht Claude in jeder Session vor Augen, ohne dass ich erinnern muss. Denkt an die Sicherheitsrichtlinie, die jeder Auftragnehmer vor Arbeitsbeginn in die Hand bekommt."
- Schritt 3, während des Neustarts: „Neue Session. Leeres Blatt. Claude erinnert sich nicht an unser Gespräch. Außer …"
- Schritt 4: „Ich habe Claude die Regeln genau einmal gesagt. Ich habe beendet, neu gestartet, und es kennt sie noch. Die CLAUDE.md wird jede Session automatisch geladen. So schreibst du die Regeln einmal, und Claude hat sie immer vor Augen."
- Nach der Nachfrage: „Die Vorgabe steht in der Datei, nicht in meinem Kopf. Ich muss nicht daran denken, sie Claude zu sagen. Durchgesetzt ist sie damit aber nicht: Das schafft erst ein Hook."

**Wenn Claude die CLAUDE.md nach dem Neustart nicht kennt:** Prüf, ob die Datei im Arbeitsordner oder unter `~/.claude/CLAUDE.md` liegt. `/context` zeigt unter **Memory files**, was geladen ist.

**Wenn Claude die Konventionen in Schritt 4 nicht kennt:** Prüf mit `ls -la CLAUDE.md`, ob die Datei im aktuellen Ordner liegt. Starte Claude Code dann neu und versuch es noch einmal; vielleicht ist die Datei in einem anderen Ordner gelandet.

</details>
