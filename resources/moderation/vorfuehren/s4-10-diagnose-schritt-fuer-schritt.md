# Vorführen: S4.10 · Diagnose Schritt für Schritt

> Demo und Hinweise für Moderierende zum Kapitel [S4.10 · Diagnose Schritt für Schritt](../../library/s4-10-diagnose-schritt-fuer-schritt.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: ein Wächter, der still offen fällt

**Ziel:** Das Diagnose-Vorgehen an einem Wächter-Hook zeigen, der keine Meldung erzeugt: Die Registrierung ist in Ordnung, das Log warnt nicht, und trotzdem blockt der Hook nichts. Erst der Handlauf mit einer Eingabe im echten Format und ein sichtbar gemachter Fehler führen zur Ursache.

Zeig die Übung aus dem Kapitel live: die Übung „ein Wächter, der still offen fällt“ in [S4.10](../../library/s4-10-diagnose-schritt-fuer-schritt.md). Startzustand wie dort: der Ordner `~/cc-workshop/waechter-defekt` mit `.claude/settings.json` und `.claude/hooks/guard.py`, so wie im Kapitel angegeben. Leg beide Dateien vorher an; der Wächter hat einen eingebauten Fehler (er liest das Feld `cmd` statt `command` und fängt jede Ausnahme mit `exit 0` ab). Unter macOS und Linux steht überall `python3`, wo im Kapitel `python` steht, auch in der `settings.json`. Ablauf: die Schritte 1 bis 7 der Übung. Starte den ersten Lauf mit `claude --permission-mode default --debug-file debug.log`.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 15 bis 20 Minuten.

**Sagen:**

- Schritt 1: „Der Befehl mit `release.lock` läuft. Im Transkript steht kein `hook error`. Nichts meldet einen Fehler." Nur Exit-Code 2 blockt. Ein Skript, das alle Fehler abfängt und mit `exit 0` endet, sieht für Claude Code aus wie ein Hook, der zugestimmt hat.
- Schritt 2: „`/hooks` zeigt den Hook unter PreToolUse. Die Registrierung ist in Ordnung. Das war nicht das Problem."
- Schritt 3: „Jetzt spiele ich die Eingabe im echten Format von Hand ein: Der Shell-Befehl steht in `tool_input.command`." Das Ergebnis ist `exit=0`, obwohl der Befehl `release.lock` nennt: Der Wächter sagt leise „kein Einwand".
- Schritt 4: „Das Debug-Log hätte uns hier nicht gewarnt." In der interaktiven Sitzung steht zum Hook möglicherweise keine Zeile, in einem `-p`-Lauf schon; in beiden Fällen meldet das Log keinen Fehler. Verlässlich ist der Handlauf aus Schritt 3.
- Schritt 5: „Ich mache den verschluckten Fehler laut, bevor ich etwas anderes ändere." Die Fehlermeldung endet auf `KeyError: 'cmd'`: Das Skript sucht das Feld `cmd`, im Ereignis heißt es `command`.
- Schritt 6: „Zwei Änderungen: das richtige Feld, und der `except`-Block fällt geschlossen. Ein kaputter Wächter soll die Tür schließen, nicht öffnen." Die drei Handtests: `release.lock` ergibt `exit=2`, `echo hi` ergibt `exit=0`, `not json` ergibt `exit=2`.
- Schritt 7: „Jetzt belegt der geblockte Befehl in der Sitzung die Reparatur."
- Zum Abschluss: „Wir haben nie geraten. Wir haben jede Schicht gefragt, was sie sieht: `/hooks`, den Handlauf, das Log. Sobald du anfängst zu raten, lässt sich die Fehlersuche nicht mehr wiederholen." Die Diagnose-Checkliste des Kapitels beginnt mit `/doctor` und geht dann CLAUDE.md, Skills, Plugins, Hooks, MCP und Rechte durch, zuletzt das Debug-Log.

**Wenn die Hooks nicht laufen:** Claude Code führt Hooks aus Settings-Dateien erst aus, wenn der Vertrauensdialog für den Ordner bestätigt ist.

**Wenn Claude auf ein anderes Werkzeug ausweicht und nach einer Dateiänderung fragt (Schritt 7):** Lehn mit „No“ ab.

**Zugabe: „Mein Skill greift nicht“**

Dieselbe Methode an einem Skill, wenn Zeit bleibt. Ein fertig kaputter Skill liegt im Repo unter [`resources/demos/assets/broken-greeter/SKILL.md`](../../demos/assets/broken-greeter/SKILL.md). Er hat drei eingebaute Metadaten-Probleme: eine allgemeine Beschreibung, `disable-model-invocation: true` und einen `paths`-Filter, den keine echte Datei erfüllt. Der Skill-Text selbst funktioniert. Kopier ihn in einen Wegwerf-Ordner (`.claude/skills/broken-greeter/SKILL.md` im Ordner), nicht nach `~/.claude`, und starte dort eine Sitzung.

Gehe die Diagnose-Reihenfolge des Kapitels durch:

1. `/skills`: Steht der Skill in der Liste? Hier ja, an der Installation liegt es nicht.
2. Das Frontmatter ansehen: `disable-model-invocation`, `paths`, Konkretheit der Beschreibung.
3. Ausdrücklich auslösen: `/broken-greeter`. Der Skill-Text funktioniert; gesperrt haben nur die Metadaten.
4. `/debug` mit einer Beschreibung des Problems, dann denselben Prompt („Greet the user.“) noch einmal.

Behebe die Probleme eines nach dem anderen und prüf nach jedem, ob der Skill von selbst greift. Zum Schluss schreibst du die Beschreibung mit konkreten Auslösern neu, etwa „Greets the user warmly by name. Use whenever the prompt is "greet the user", "say hello" or "welcome me".“

Die Ausgaben von `/debug` und des Debug-Logs hängen von der Claude-Code-Version ab. Prüf vor der Session auf dem Vorführrechner, was sie wirklich zeigen, und lies die echten Zeilen vor; versprich keinen Wortlaut. Fehlt `/debug`, starte mit `claude --debug` neu und lies das Log in `~/.claude/debug/<session-id>.txt`. Eine Kürzung auf zwei Probleme ist möglich: Bau nur die allgemeine Beschreibung und den `paths`-Filter ein.

</details>
