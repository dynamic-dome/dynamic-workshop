# Vorführen: S4.10 · Diagnose Schritt für Schritt

> Demo und Hinweise für Moderierende zum Kapitel [S4.10 · Diagnose Schritt für Schritt](../../library/s4-10-diagnose-schritt-fuer-schritt.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen kaputten Skill diagnostizieren

**Ziel:** Das ganze Diagnose-Vorgehen an einem Skill zeigen, der auf drei Arten nacheinander scheitert. Jeder Fix legt das nächste Problem frei.

**Vorbereitung**

Ein fertig kaputter Skill liegt im Repo unter [`resources/demos/assets/broken-greeter/SKILL.md`](../../demos/assets/broken-greeter/SKILL.md); du musst ihn nicht vor der Session nachbauen. Kopier ihn vorher an seinen Platz:

```bash
mkdir -p ~/.claude/skills/broken-greeter
cp resources/demos/assets/broken-greeter/SKILL.md ~/.claude/skills/broken-greeter/SKILL.md
```
```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills\broken-greeter" | Out-Null
Copy-Item resources\demos\assets\broken-greeter\SKILL.md "$HOME\.claude\skills\broken-greeter\SKILL.md"
```

Er hat **drei eingebaute Probleme**, in dieser Reihenfolge:

1. **Die Beschreibung ist allgemein**, ohne konkrete Auslöser (nur „A skill for greeting.").
2. **`disable-model-invocation: true`** im Frontmatter: Der Skill ist registriert, der automatische Aufruf aber aus.
3. **`paths: ["never-match/**"]`**: ein Filter, den keine echte Datei erfüllt.

Der Skill-Text selbst funktioniert („Reply with a friendly greeting that uses the user's name"). Falsch sind nur die Metadaten.

**Schritte (etwa 7 Minuten)**

> **Die Trace-Ausgaben sind sinngemäß, nicht wörtlich.** Die zitierten `/debug`-Zeilen zeigen, *welche Information*
> erscheint; der **genaue Wortlaut hängt von der Claude-Code-Version ab**. Prüf vor der Session auf dem Vorführrechner,
> was `/debug` und das Debug-Log wirklich zeigen, und lies die echten Zeilen vor. Versprich diese hier nicht als Ausgabe.

**Schritt 1: den Skill normal benutzen**

Prompt:

> "Greet the user."

Der Skill feuert nicht. Claude antwortet mit einem allgemeinen Gruß aus seinem Grundverhalten, ohne ein Zeichen, dass es den Skill überhaupt erwogen hat.

**Schritt 2: prüfen, ob der Skill installiert ist**

```
/skills
```

Zeig: `broken-greeter` steht in der Liste. An der Installation liegt es also nicht.

**Schritt 3: das Frontmatter ansehen**

```bash
cat ~/.claude/skills/broken-greeter/SKILL.md | head -20
```

Auf den ersten Blick wirkt das Frontmatter plausibel. **Lies es jetzt nicht gründlich durch.** Nimm stattdessen das Diagnose-Werkzeug; genau das ist die Lektion.

**Schritt 4: `/debug` einschalten und neu auslösen**

```
/debug skill-not-triggering
```

Wiederhol dann den Prompt: *„Greet the user."*

Lies die Auswertung laut vor. Such nach einer Zeile **sinngemäß** wie dieser (der Wortlaut variiert):

> *"Skill `broken-greeter` matched paths-filter: NO (filter: `never-match/**`, current files: ...)"*

Die erste Ursache ist sichtbar. Reaktion im Raum: „Ah, der paths-Filter ist falsch."

**Schritt 5: Fix 1, den paths-Filter entfernen**

Lösch die Zeile `paths:` im Frontmatter und lös den Prompt erneut aus. **Der Skill feuert immer noch nicht.** Lies die Auswertung noch einmal und such nach etwas **wie** (Wortlaut variiert):

> *"Skill `broken-greeter` registered but auto-invocation disabled (`disable-model-invocation: true`). Available only via explicit `/broken-greeter`."*

**Schritt 6: mit dem Aufruf von Hand gegenprüfen**

```
/broken-greeter
```

Der Skill feuert. Der Skill-Text funktioniert also; gesperrt haben nur die Metadaten.

**Schritt 7: Fix 2, `disable-model-invocation` auf `false` setzen**

Setz im Frontmatter `disable-model-invocation: false` und lös erneut aus:

> "Greet the user."

**Der Skill feuert immer noch nicht**, aber die Auswertung sagt jetzt etwas anderes (sinngemäß):

> *"Skill `broken-greeter` description too generic for prompt — no candidate match."*

**Schritt 8: Fix 3, die Beschreibung mit Auslösern neu schreiben**

Ändere die Beschreibung von `"A skill for greeting"` in etwas wie:

```
description: >
  Greets the user warmly by name. Use whenever the prompt is "greet the user",
  "say hello", "welcome me", "hi", or any opening pleasantry.
```

**Schritt 9: den automatischen Aufruf prüfen**

```
"Greet me"
```

Jetzt feuert der Skill von selbst. Drei Probleme, drei Diagnoseschritte, drei Fixes.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 7 Minuten.

**Sagen:**

„Wir haben nie **geraten**, was falsch ist. `/debug` und `/skills` haben uns den Zustand jeder Schicht gesagt. Wir hätten eine Stunde auf das Frontmatter starren können und den `paths`-Filter übersehen, weil er *vernünftig aussah*. Die Diagnose-Werkzeuge machen aus der Blackbox einen Glaskasten.

Das ist die Schleife der **werkzeuggestützten Fehlersuche**: Frag die Werkzeuge, was sie sehen, behebe, was sie melden, und frag noch einmal. Sobald du anfängst zu raten, lässt sich die Fehlersuche nicht mehr wiederholen."

**Wenn `/debug` in deiner Claude-Code-Version fehlt** (ältere Builds): Starte die Sitzung mit `claude --debug` neu, lös die Prompts erneut aus und lies das Debug-Log in `~/.claude/debug/<session-id>.txt`. Das ist weniger bequem als Claudes Auswertung im Gespräch, zeigt dir aber das Log selbst.

**Wenn jemand fragt, warum drei Probleme statt einem:** Echte Skills haben meist ein Problem auf einmal, aber **die Diagnose-Schleife bleibt dieselbe, egal wie viele Probleme übereinanderliegen**. Es geht um die *Methode*, nicht um die Menge.

**Kürzere Fassung (etwa 4 statt 7 Minuten):** Bau nur die Probleme 1 und 3 ein und lass den Schritt zu `disable-model-invocation` weg.

</details>
