# Vorführen: S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder

> Demo und Hinweise für Moderierende zum Kapitel [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](../../library/s3-01-was-ist-ein-agent.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: was ein Subagent weiß und was nicht

**Ziel:** Zeigen, dass ein Subagent ein Codewort aus deinem Gespräch nur kennt, wenn der Auftrag es enthält. Zeig die Übung aus dem Kapitel live: die Übung „was ein Subagent weiß und was nicht“ in [S3.1](../../library/s3-01-was-ist-ein-agent.md).

**Startzustand:** der leere Ordner `~/cc-workshop/agent-kontext`, darin eine Sitzung mit `claude --permission-mode default` und bestätigtem Vertrauensdialog, wie im Startzustand der Übung. Im Ordner liegt keine `CLAUDE.md`. Ablauf: Schritte 1 bis 4 der Übung (Codewort nennen, Lauf 1 ohne Codewort im Auftrag, den übergebenen Auftragstext prüfen, Lauf 2 mit Codewort im Auftrag). Den Fork aus der Extra-Übung zeigst du, wenn Zeit bleibt.

#### Einstieg in Session 3: ein garantierter Live-Moment

Die meisten Vorführungen dieser Session hängen von etwas Externem ab: eigenen Plugins, der Codex CLI, dem Internet, der Telegram-Brücke. Scheitert eine davon gleich zu Beginn vor Publikum, wirkt der ganze Block wackelig. Beginne Session 3 deshalb mit einer Vorführung, die nur das lokal installierte `claude` braucht: Wechsle in einen beliebigen Projektordner mit ein paar Dateien (der Übungsordner `agent-kontext` ist dafür noch zu leer) und tipp am Prompt, sodass alle zusehen:

```bash
claude -p "Summarize what this repo does in one sentence."
```

Wenn die einzeilige Antwort erscheint, zeig drei Dinge:

1. Keine interaktive Schleife: Der Prompt ist zur Shell zurückgekehrt.
2. Die Ausgabe ging nach stdout und lässt sich an jedes andere Werkzeug weiterreichen.
3. Exit-Code 0: Die Shell hätte einen Fehler bemerkt.

Danach geht es mit der Vorführung zu den Orchestrierungsmustern weiter ([S3.4](s3-04-orchestrierungsmuster.md)). Die vollständige Headless-Vorführung kommt später an ihrem eigenen Platz ([S4.3](s4-03-headless.md)).

<details><summary>Für Moderierende</summary>

**Dauer:** der Einstieg etwa 60 Sekunden; die Übung etwa 10 Minuten.

**Warum zuerst:** Fällt später eine Plugin-Vorführung aus, hast du schon einen sauberen Live-Erfolg im Raum.

**Sagen:**

- Einstieg: „Das ist derselbe Claude, mit dem ihr bisher gearbeitet habt. Dasselbe Modell, dieselben Skills. Es fehlt nur die Gesprächsschleife."
- Schritt 2 der Übung: „Der Subagent kennt das Codewort nicht. Das Gespräch gelangt nicht von allein zu ihm." Mit `Ctrl+O` zeigst du den Aufruf des Subagenten im Transkript und schließt die Ansicht mit `Ctrl+O` wieder.
- Schritt 3: Lies den übergebenen Auftragstext vor. Steht das Codewort doch darin, hat Claude den Auftrag ergänzt; dann zählt der Lauf nicht, und du wiederholst Schritt 2 mit demselben Wortlaut.
- Schritt 4: „Typ, Anweisung und Gespräch waren gleich. Geändert hat sich allein der Auftragstext. Alles, was ein Subagent wissen soll, muss im Auftrag stehen."
- Fork (Extra): Laut Doku erbt ein Fork das ganze Gespräch, der Preis ist, dass die Isolation wegfällt. `/subtask` braucht laut Doku Claude Code ab Version 2.1.212; fehlt der Befehl, überspring das Extra.

</details>
