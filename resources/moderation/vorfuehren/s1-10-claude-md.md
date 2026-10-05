# Vorführen: S1.10 · CLAUDE.md: die Hausordnung des Projekts

> Demo und Hinweise für Moderierende zum Kapitel [S1.10 · CLAUDE.md: die Hausordnung des Projekts](../../library/s1-10-claude-md.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: CLAUDE.md live

**Ziel:** Zeigen, wie eine CLAUDE.md entsteht, wie Claude beendet und neu gestartet wird und danach die Regeln noch kennt, ohne dass du sie wiederholst, und dass eine Regel keine Sperre ist. Zeig die Übung aus dem Kapitel live: die Übung „drei Regeln, ein Neustart“ in [S1.10](../../library/s1-10-claude-md.md).

**Startzustand:** der Ordner `~/cc-workshop/claudemd` und eine Sitzung mit `claude --permission-mode acceptEdits`, genau wie im Startzustand der Übung. Dann die Schritte 1 bis 7 der Übung mit denselben Aufträgen und den dort genannten Erwartungen. Sie legen `legacy_panel_parser.py`, `app.py` und die CLAUDE.md mit den drei Regeln an, beenden mit `/exit`, starten neu und prüfen mit `/context all` und der Frage nach `PANEL:`.

Schritt 6 (das Verbot testen) ist der Höhepunkt der Demo.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten, wie die Übung. Den Memory-Eintrag der Folgedemo [S1.11](s1-11-gedaechtnis-ebenen.md) hängst du danach an, wenn die Zeit reicht.

**Sagen:**

- Vor Schritt 1: „Frischer Ordner. Keine CLAUDE.md, kein Memory. Claude weiß über dieses Projekt nichts außer dem, was ich ihm jetzt sage."
- Schritt 2: „Das ist unsere Hausordnung. Jede Regel steht Claude in jeder Sitzung vor Augen, ohne dass ich erinnern muss. Denkt an die Sicherheitsrichtlinie, die jeder Auftragnehmer vor Arbeitsbeginn in die Hand bekommt." Zeig die drei Zeilen und frag die Gruppe, welche davon Claude nicht raten könnte.
- Schritt 3, während des Neustarts: „Neue Sitzung. Leeres Blatt. Claude erinnert sich nicht an unser Gespräch. Außer …"
- Schritt 4 und 5: „Ich habe Claude die Regeln genau einmal gesagt. Ich habe beendet, neu gestartet, und es kennt sie noch. Die CLAUDE.md wird in jeder Sitzung geladen."
- Schritt 6, vor der Antwort: Lass die Gruppe raten, ob Claude die Datei ändert. Danach öffnest du die Datei außerhalb von Claude. Hat Claude sie nicht geändert: „Die Regel hat gehalten. Garantiert ist das nicht." Hat es sie doch geändert: „Genau das ist die Antwort auf die Frage, ob eine Regel eine Sperre ist." Die harte Sperre ist ein Hook ([S2.8](s2-08-hook-einrichten.md)).
- Schritt 7: „Das Verbot gilt für die Datei, nicht für die Arbeit. Mit anderem Ziel läuft es."

**Wenn `/context all` die CLAUDE.md nicht unter Memory files zeigt:** Sie liegt in einem anderen Ordner als dem, in dem Claude gestartet wurde. Mit `ls CLAUDE.md` (PowerShell: `Get-ChildItem CLAUDE.md`) prüfen, dann mit `/exit` beenden und im richtigen Ordner neu starten.

</details>
