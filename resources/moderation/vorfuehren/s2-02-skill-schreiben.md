# Vorführen: S2.2 · Eine SKILL.md schreiben

> Demo und Hinweise für Moderierende zum Kapitel [S2.2 · Eine SKILL.md schreiben](../../library/s2-02-skill-schreiben.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Skills in Aktion

**Ziel:** Zeigen, wie Skills aussehen, wie man sie aufruft und warum sie mehr bringen, als jedes Mal Anweisungen zu tippen.

**Vorbereitung**

- ein Terminal in einem beliebigen Projektordner
- `~/.claude/skills/` vorhanden, auch wenn der Ordner leer ist
- optional: ein einfacher Stub `email-validator.js`, noch ohne Tests

**Schritt 1: die verfügbaren Befehle zeigen**

In Claude Code:

```
/help
```

Die Ausgabe durchgehen und zeigen:

- eingebaute Befehle wie `/compact` und `/clear`
- eigene Befehle aus installierten Plugins

**Schritt 2: die persönlichen Skills auflisten**

Im Terminal:

```bash
ls ~/.claude/skills/
```

Oder in Claude Code:

```
list my skills
```

Zeig, was da ist. Hat jemand im Raum `agent-orchestrator` oder `tdd` installiert, heb einen davon hervor.

**Schritt 3: mit dem TDD-Skill einen E-Mail-Validator bauen**

In Claude Code:

```
/tdd
```

Ist `/tdd` nicht als Befehl installiert, tippst du:

```
Use TDD to implement an email validator function. Start with the failing test.
```

Was passiert:

1. Claude fragt, was gebaut werden soll, oder legt direkt los.
2. Claude schreibt ZUERST den Test. Zeig ihn.
3. Claude führt den Test aus, er schlägt fehl (rot). Zeig die rote Ausgabe.
4. Claude schreibt die minimale Implementierung.
5. Claude führt den Test aus, er läuft durch (grün). Zeig die grüne Ausgabe.

**Schritt 4: die SKILL.md zeigen**

```bash
cat ~/.claude/skills/tdd/SKILL.md
# Or if it's a plugin skill:
cat ~/.claude/plugins/cache/superpowers-marketplace/skills/test-driven-development/SKILL.md
```

Darauf hinweisen:

- das YAML-Frontmatter mit den Trigger-Phrasen
- die eigentlichen Arbeitsschritte im Body

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten (Schritt 1: 1 Min., Schritt 2: 1 Min., Schritt 3: 5 Min., Schritt 4: 1 Min.).

**Sagen:**

- Schritt 1: „Das sind die Alarmknöpfe. Jeder löst eine bestimmte Dienstanweisung aus."
- Schritt 2: „Das sind meine persönlichen Dienstanweisungen, verfügbar in jedem Projekt auf diesem Rechner."
- Schritt 3: „Ich habe Claude nicht gesagt, TDD zu machen. Ich habe den Skill aufgerufen, oder die Trigger-Phrase benutzt, und Claude ist der ganzen Dienstanweisung von selbst gefolgt. Keine Erinnerung, keine Wiederholung."
- Schritt 4: „Das ist die Dienstanweisung. Eine Textdatei. Du kannst sie bearbeiten, versionieren und mit deinem Team teilen."

**Kernbotschaften** (zu [S2.1](../../library/s2-01-skills-und-commands.md)):

- „Skills sind Dienstanweisungen, gespeichert als Textdateien."
- „Commands sind die Alarmknöpfe, die sie auslösen."
- „Persönliche Skills in `~/.claude/skills/` begleiten dich in jedes Projekt."
- „Du kannst für jeden wiederkehrenden Ablauf einen eigenen Skill schreiben: die Review-Checkliste deines Teams, dein Vorgehen beim Deployment, deine Schritte bei einem Sicherheitsvorfall."

**Wenn der TDD-Skill nicht installiert ist:**

```
Let's implement an email validator with tests. Write the failing test first, then implement, then verify the test passes. Follow strict red-green-refactor — no implementation before a failing test exists.
```

Das stößt den TDD-Ablauf von Hand an. Sag dann: „Das habe ich gerade von Hand gemacht. Mit einem Skill tippe ich `/tdd`, und Claude weiß das alles schon."

</details>
