# Vorführen: S1.11 · Alle Gedächtnis-Ebenen im Überblick

> Demo und Hinweise für Moderierende zum Kapitel [S1.11 · Alle Gedächtnis-Ebenen im Überblick](../../library/s1-11-gedaechtnis-ebenen.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Notiz im Auto-Memory und Pfadregel

Zeig die Übung aus dem Kapitel live: die Übung „Notiz und Pfadregel beobachten“ in [S1.11](../../library/s1-11-gedaechtnis-ebenen.md). Startzustand wie dort: der Ordner `~/cc-workshop/gedaechtnis` und eine Sitzung mit `claude --permission-mode acceptEdits`. Mit der Demo zu [S1.10](s1-10-claude-md.md) hängt sie nur gedanklich zusammen (CLAUDE.md gegen Auto-Memory); sie braucht deren Ordner nicht.

Für eine kurze Fassung nimm die Schritte 1, 3 und 5 der Übung: die Notiz mit `Remember that …`, ein Blick in die `MEMORY.md` im Auto-Memory-Ordner, Neustart und die Frage ohne Werkzeuge. Die Pfadregel (Schritte 4, 6 und 7) kommt dazu, wenn Zeit bleibt; für Schritt 2 legst du die beiden Dateien an, die die Übung nennt.

<details><summary>Für Moderierende</summary>

**Sagen:**

- Nach Schritt 1: „Das ist etwas anderes als die CLAUDE.md. Die CLAUDE.md liegt beim Projekt und ist der verlässliche Ort für Team-Konventionen. Das Auto-Memory schreibt Claude selbst, es liegt unter meinem Nutzerprofil und bleibt auf diesem Rechner. Behandelt es als persönliches Gedächtnis für Vorlieben, nicht als Ersatz für Projektregeln."
- Schritt 3: Öffne die `MEMORY.md` und lies die Zeile zu den Türnummern vor. „Das ist einfaches Markdown. Ihr könnt jede Notiz bearbeiten oder löschen, über `/memory`."
- Schritt 6 und 7, falls gezeigt: Lass die Gruppe raten, ob Claude die Regel für `api/` kennt, bevor es eine Datei dort gelesen hat. „Die Regel lud erst, als Claude die passende Datei mit dem Read-Werkzeug gelesen hat."
- Zum Abschluss: „Die CLAUDE.md ist eure Hausordnung. Sie lebt beim Projekt. Schreibt die Regeln einmal, und Claude hat sie in jeder Sitzung vor Augen."

**Wenn du den Auto-Memory-Ordner nicht findest:** Öffne ihn in einer Sitzung über `/memory`. Sein Name entsteht aus dem Pfad des Projekts, jedes Zeichen außer Buchstaben und Ziffern wird zu `-`.

**Wenn im Memory Drift sichtbar wird:** Nimm es als Lernmoment: „Genau deshalb prüfen wir das Auto-Memory regelmäßig" ([S4.10](../../library/s4-10-diagnose-schritt-fuer-schritt.md)).

</details>
