# Vorführen: S1.1 · Erster Kontakt: sofort eine Datei bauen

> Demo und Hinweise für Moderierende zum Kapitel [S1.1 · Erster Kontakt: sofort eine Datei bauen](../../library/s1-01-erster-kontakt.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Erster Kontakt

**Ziel:** Die Teilnehmenden sehen, wie Claude Code startet, auf normale Sprache reagiert und eine echte Python-Datei anlegt und ausführt, alles in einem Terminalfenster, ohne Kopieren und ohne Fensterwechsel.

Die Demo gehört zu diesem Kapitel und stützt [S1.2](s1-02-agent-statt-chat.md) (Agent statt Chat). Schritt 2, die Selbstbeschreibung, steht dort.

**Schritt 1: Claude Code starten**

Tipp im Terminal, in einem frischen, leeren Ordner (zum Beispiel `~/cc-workshop/hello`, wie in S1.1):

```
claude --permission-mode default
```

Erwartet: Claude Code startet und zeigt eine Begrüßung. Du bist jetzt in der interaktiven Sitzung. Ohne das Flag läuft eine Sitzung ab Version 2.1.283 im Modus `auto` und die Rückfragen bleiben meist aus; mit dem Flag fragt Claude vor dem Schreiben und vor dem Ausführen, und du antwortest jedes Mal mit „Yes“.

**Schritt 2: Claude sich selbst beschreiben lassen**

Steht in [S1.2](s1-02-agent-statt-chat.md), samt Sprechpunkt.

**Schritt 3: einen Passwortgenerator bauen lassen**

Tipp in Claude Code:

```
Create a Python script called password_gen.py in the current directory.
It should generate secure random passwords. Requirements:
- Configurable length via command-line argument (default 16)
- Uses uppercase, lowercase, digits, and special characters
- Special characters: !@#$%^&*
- Uses Python's secrets module (not random — this needs to be cryptographically secure)
- Prints the generated password to stdout
```

Erwartet: Claude legt die Datei an und zeigt den Code, den es geschrieben hat. Die Datei erscheint im aktuellen Ordner.

**Kurz innehalten** und den Teilnehmenden den Code zeigen, einmal durchscrollen.

**Schritt 4: das Skript ausführen**

Tipp in Claude Code:

```
Run password_gen.py with length 20
```

Erwartet: Claude führt `python password_gen.py 20` (Windows) oder `python3 password_gen.py 20` (macOS/Linux) aus, oder etwas Gleichwertiges, und zeigt ein Passwort mit 20 Zeichen.

**Optional, wenn Zeit ist:**

```
Run it 5 times in a row and show me the output of each run
```

Erwartet: Claude führt den Befehl in einer Schleife oder fünfmal hintereinander aus und zeigt fünf verschiedene Passwörter.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten für die ganze Demo, Schritt 2 aus [S1.2](s1-02-agent-statt-chat.md) eingeschlossen.

**Sagen:**

- Schritt 1, während Claude startet: „Das ist kein Browser und kein Chatfenster. Wir sind komplett im Terminal. Hier lebt Claude Code. Ich zeige euch, was es von hier aus kann."
- Schritt 3, während Claude schreibt: „Ich habe keinen Editor geöffnet und keine einzige Zeile Code geschrieben. Ich habe eine Spezifikation geschrieben, einen Arbeitsauftrag, und Claude setzt ihn um. Achtet darauf, wie die Datei erscheint."
- Schritt 3, wenn der Code da ist: „Es nimmt `secrets.choice()`, nicht `random.choice()`. Ich habe ‚kryptografisch sicher' verlangt, und es wusste, welches Python-Modul dazu gehört. Das ist Fachwissen, nicht nur Textgenerierung."
- Schritt 4: „Es hat das Skript ausgeführt. In derselben Sitzung, ohne Fensterwechsel, ohne Kopieren. Beschreiben, was du willst, es schreibt, es führt aus, du siehst das Ergebnis. Das ist die Kernschleife von Claude Code."
- Optionale Erweiterung: „Jeder Lauf liefert ein anderes Passwort. Die kryptografische Zufälligkeit funktioniert. Und ich habe keine einzige Zeile Python geschrieben."
- Zum Abschluss: „Was gerade passiert ist: Ich habe ein Terminal geöffnet und beschrieben, was ich will. Claude hat eine Datei angelegt, ich habe sie geprüft, Claude hat sie ausgeführt. Kein Kopieren, kein Editorwechsel, kein eigener Terminal-Tab zum Ausführen. Die ganze Entwicklungsschleife lief in einem Gespräch. Das meint ‚volle Terminal-Integration'."

**Wenn etwas schiefgeht:**

- **`claude` startet nicht:** `claude --version` und `claude doctor` ausführen. Fehlt die Anmeldung, zeig einen vorbereiteten Screenshot oder eine Aufzeichnung und mach mit dem Denkmodell weiter.
- **Der Python-Befehl heißt anders:** Unter Windows `python password_gen.py 20` sagen, unter macOS/Linux/Git Bash `python3 password_gen.py 20`.
- **Die Datei landet im falschen Ordner:** Lass Claude `pwd` und `ls` ausführen. Dann wechselst du entweder mit `cd` in den gedachten Übungsordner oder startest die Demo in einem frischen Ordner (zum Beispiel `~/cc-workshop/hello`) neu.

</details>
