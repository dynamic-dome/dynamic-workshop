# Vorführen: S2.2 · Eine SKILL.md schreiben

> Demo und Hinweise für Moderierende zum Kapitel [S2.2 · Eine SKILL.md schreiben](../../library/s2-02-skill-schreiben.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen Skill bauen und nachschärfen

**Ziel:** Zeigen, wie ein Skill aussieht, wie man ihn aufruft, wie er sich ohne Neustart nachschärfen lässt und warum er mehr bringt, als jedes Mal Anweisungen zu tippen.

Zeig die Übung aus dem Kapitel live: die Übung „einen Skill bauen und nachschärfen“ in [S2.2](../../library/s2-02-skill-schreiben.md). Startzustand wie dort: der Ordner `~/cc-workshop/skill-schreiben` mit Git, der gestagten `app.py` (Schritt 2) und der `SKILL.md` unter `.claude/skills/commit-check/` (Schritt 3). Leg sie vorher an und zeig sie der Gruppe im Editor: das Frontmatter und den Body mit den Schritten. Starte mit `claude --permission-mode default`.

**Ablauf:** Schritte 4 bis 7 der Übung: `/skills`, `/commit-check`, die Zeile mit `VERDICT` ergänzen und denselben Befehl in derselben Sitzung noch einmal, dann der Auftrag ohne Befehl.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten.

**Sagen:**

- Schritt 4: „Das sind meine Skills. Jeder löst eine bestimmte Dienstanweisung aus." Die Ansicht mit `Esc` schließen, nicht mit Leertaste oder Enter: Beide ändern dort die Sichtbarkeit eines Skills.
- Schritt 5: „Ich habe Claude nicht erklärt, wie die Prüfung geht. Ich habe den Skill aufgerufen, und Claude ist der ganzen Dienstanweisung gefolgt." Zeig, dass die Antwort mit `PRE-COMMIT CHECK:` beginnt und beide Funde nennt.
- Schritt 6: „Ich ändere die Datei bei laufender Sitzung. Kein Neustart." Nach dem Speichern ein paar Sekunden warten, bis Claude Code die Änderung bemerkt; nutze die Wartezeit für die Erklärung. Dann endet die Antwort mit `VERDICT: BLOCK`: Das konnte der erste Entwurf nicht.
- Schritt 7: „Jetzt ohne Befehl." Nach `Ctrl+O` den Aufruf des Werkzeugs `Skill` im Transkript zeigen. Lädt Claude den Skill nicht, schreib den getippten Satz in `when_to_use`: Die automatische Wahl hängt an Claudes Urteil über die Beschreibung, nicht an einer festen Regel.
- Zum Schluss: „Das ist eine Textdatei. Du kannst sie bearbeiten, versionieren und mit deinem Team teilen." Persönliche Skills in `~/.claude/skills/` sind in jedem Projekt auf diesem Rechner verfügbar.

**Wenn `/commit-check` nicht in `/skills` steht:** Prüf, ob die Datei `.claude/skills/commit-check/SKILL.md` heißt und die erste Zeile die öffnende `---` ist. Ein unbekanntes Feld im Frontmatter ignoriert Claude Code still. Wurde `.claude/skills/` erst während der Sitzung angelegt, hilft `/reload-skills`.

**Wenn der Befehl in Schritt 5 nichts findet:** Prüf mit `git status`, ob `app.py` gestagt ist.

</details>
