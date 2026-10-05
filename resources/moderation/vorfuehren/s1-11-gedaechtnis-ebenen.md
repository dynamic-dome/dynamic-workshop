# Vorführen: S1.11 · Alle Gedächtnis-Ebenen im Überblick

> Demo und Hinweise für Moderierende zum Kapitel [S1.11 · Alle Gedächtnis-Ebenen im Überblick](../../library/s1-11-gedaechtnis-ebenen.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen Memory-Eintrag anlegen (Demo 1.2, Schritt 5)

Fortsetzung der Demo aus [S1.10](s1-10-claude-md.md): Claude kennt die CLAUDE.md schon, jetzt kommt ein persönlicher Eintrag dazu.

Tipp in Claude Code:

```
Remember that I prefer German for communication but all code and file names must be in English.
```

**Erwartet:** Claude bestätigt, dass es das als Memory gespeichert hat. In künftigen Sessions in diesem Projekt spricht Claude mit dir Deutsch.

<details><summary>Für Moderierende</summary>

**Sagen:**

- „Das ist etwas anderes als die CLAUDE.md. Die CLAUDE.md liegt auf Projektebene, beim Projekt, und ist der verlässliche Ort für Team-Konventionen. Das Auto-Memory liegt unter meinem Nutzerprofil und kann über Sessions hinweg bestehen bleiben. Behandelt es als persönliches, situationsbezogenes Gedächtnis für Vorlieben, nicht als Ersatz für Projektregeln."
- Zum Abschluss der Demo: „Die CLAUDE.md ist eure Hausordnung. Sie lebt beim Projekt. Schreibt die Regeln einmal, und Claude hat sie in jeder Session vor Augen."

**Wenn das Auto-Memory nach dem Neustart keine Einträge zeigt:** Sieh selbst nach, mit `cat ~/.claude/projects/<project-hash>/memory/MEMORY.md` oder über `/memory` und den Auto-Memory-Ordner. Speichert Claude etwas, erscheint eine Meldung wie „Saved 2 memories".

**Wenn im Memory Drift sichtbar wird:** Nimm es als Lernmoment: „Genau deshalb prüfen wir das Auto-Memory regelmäßig" ([S4.10](../../library/s4-10-diagnose-schritt-fuer-schritt.md)).

</details>
