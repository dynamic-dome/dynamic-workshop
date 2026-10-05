# Vorführen: S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder

> Demo und Hinweise für Moderierende zum Kapitel [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](../../library/s3-01-was-ist-ein-agent.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Einstieg in Session 3: ein garantierter Live-Moment

Die meisten Vorführungen dieser Session hängen von etwas Externem ab: eigenen Plugins, der Codex CLI, dem Internet, der Telegram-Brücke. Scheitert eine davon gleich zu Beginn vor Publikum, wirkt der ganze Block wackelig. Beginne Session 3 deshalb mit einer Vorführung, die nur das lokal installierte `claude` braucht und nicht an einem fehlenden Plugin scheitern kann.

Tipp am Prompt, sodass alle zusehen:

```bash
claude -p "Summarize what this repo does in one sentence."
```

Wenn die einzeilige Antwort erscheint, zeig drei Dinge:

1. Keine interaktive Schleife: Der Prompt ist zur Shell zurückgekehrt.
2. Die Ausgabe ging nach stdout und lässt sich an jedes andere Werkzeug weiterreichen.
3. Exit-Code 0: Die Shell hätte einen Fehler bemerkt.

Danach geht es mit der Vorführung zu den Orchestrierungsmustern weiter ([S3.4](s3-04-orchestrierungsmuster.md)). Die vollständige Headless-Vorführung kommt später an ihrem eigenen Platz ([S4.3](s4-03-headless.md)).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 60 Sekunden, garantiert lauffähig.

**Warum zuerst:** Fällt später eine Plugin-Vorführung aus, hast du schon einen sauberen Live-Erfolg im Raum.

**Sagen:**

- „Das ist derselbe Claude, mit dem ihr bisher gearbeitet habt. Dasselbe Modell, dieselben Skills. Es fehlt nur die Gesprächsschleife."

</details>
