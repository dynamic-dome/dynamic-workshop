# Vorführen: S4.8 · Abschlussprojekt mit Bewertung

> Demo und Hinweise für Moderierende zum Kapitel [S4.8 · Abschlussprojekt mit Bewertung](../../library/s4-08-abschlussprojekt.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: die Architektur am Whiteboard

**Ziel:** Mit dem Architekturbild wiederholen, was die fortgeschrittenen Kapitel gezeigt haben, bevor das Abschlussprojekt beginnt.

Zeichne das Architekturbild aus „Im Detail" an oder zeig es. Geh diese Stationen durch:

- du in der CLI, in der Web-App oder am Handy
- Claude Code als Orchestrator
- Werkzeuge (Read/Write/Bash), MCP-Server, Hintergrund-Agenten und Subagenten
- Worktrees als isolierte Arbeitsbäume

Nutze das Bild als Rückblick. Erkläre an jedem Knoten, was er tut und wo seine Sicherheitsgrenze liegt.

Die übrigen Schritte dieser Vorführung stehen bei ihren Kapiteln: Worktree-Isolation in [S4.7](s4-07-isolation-docker-worktrees.md), Remote Control, `/teleport` und die Telegram-Bridge in [S4.6](s4-06-remote-und-teleport.md).

<details><summary>Für Moderierende</summary>

**Dauer:** 3–4 Minuten.

**Sagen (zum Abschluss):** „Ihr habt jetzt alle fünf Erweiterungsebenen dieses Kurses gesehen: Skills, Hooks, Plugins, MCP, RAG, dazu Multi-Agent, Sicherheit, Automation und CI/CD. Die Telegram-Bridge ist ein selbst gebautes Beispiel für das Muster ‚Fernkoordination‘. Dasselbe Muster gibt es offiziell: `claude remote-control` und Channels (MCP-Push, noch Research Preview)."

Die Fehlersuche ([S4.9](../../library/s4-09-fehlersuche-werkzeuge.md), [S4.10](../../library/s4-10-diagnose-schritt-fuer-schritt.md)) folgt nach dem Abschlussprojekt.

**Gruppenformat:** Im Kapitel steht das Abschlussprojekt als Übung für eine Person. In der Gruppe fährt eine Person, die anderen beobachten mit der Rubrik. Am Ende stellt jede Person am Steuer ihre Übergabe in 5 Minuten vor, am Whiteboard oder anhand von Diff und Guardrail. Im Mittelpunkt stehen die drei Fragen vom Schluss der Übung: Welches Problem löst das? Welche Automatisierung bringt am meisten? Was würdest du diese Woche als Erstes wirklich einbauen?

**Das Abschlussprojekt moderieren:**

- Die Person am Steuer treibt Claude Code, die anderen beobachten mit der Rubrik. Wechsle die Person am Steuer, wenn Zeit bleibt.
- Du beobachtest nur. Rückfragen zur Aufgabe beantwortest du; Befehle wählst du nicht aus, und die Umsetzung schreibst du nicht.
- Am Ende bewertest du mit der Rubrik und gibst eine konkrete Empfehlung für den nächsten Schritt.
- Übertrag diese Empfehlung in den Adoptionsplan zum Mitnehmen und plane das asynchrone Nachfassen nach 30 Tagen.

</details>
