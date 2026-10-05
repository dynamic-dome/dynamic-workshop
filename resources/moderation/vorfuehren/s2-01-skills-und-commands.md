# Vorführen: S2.1 · Skills sind Dienstanweisungen, Commands sind Knöpfe

> Demo und Hinweise für Moderierende zum Kapitel [S2.1 · Skills sind Dienstanweisungen, Commands sind Knöpfe](../../library/s2-01-skills-und-commands.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: erst die Beschreibung, dann der Inhalt

**Ziel:** Zeigen, dass ein Skill vor dem Aufruf nur mit seiner Beschreibung im Kontext liegt und erst durch den Aufruf seinen Inhalt preisgibt, auf beiden Wegen: mit deinem Befehl und von Claude selbst geladen.

Zeig die Übung aus dem Kapitel live: die Übung „erst die Beschreibung, dann der Inhalt“ in [S2.1](../../library/s2-01-skills-und-commands.md). Startzustand wie dort: der Ordner `~/cc-workshop/skills` mit `.claude/skills/codeword/SKILL.md`; leg die Datei vorher an, `.claude` ist ein geschützter Pfad, und starte mit `claude --permission-mode default`. Ablauf: Schritte 3 bis 6 der Übung (Frage ohne Werkzeuge, `/codeword`, Frage erneut, `/clear` und die Frage mit Werkzeugen).

Das Schreiben einer SKILL.md zeigt die Demo in [S2.2](s2-02-skill-schreiben.md).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 Minuten.

**Sagen:**

- Schritt 3: „Claude kennt das Codewort nicht. Von meinem Skill liegt vorher nur die Beschreibung im Kontext, nicht der Inhalt."
- Schritt 4: „Mein Befehl hat den Inhalt geladen, und Claude folgt der Anweisung darin."
- Schritt 6, nach `Ctrl+O`: „Ich habe keinen Befehl getippt. Claude hat den Skill selbst geladen." Zeig den Aufruf des Werkzeugs `Skill` im Transkript. Liest Claude stattdessen die Datei direkt, steht dort ein `Read`-Aufruf; auch das zeigt, dass die Anweisung in der Datei steckt. Danach noch einmal `Ctrl+O`, um zurückzukehren.

**Kernbotschaften:**

- „Skills sind Dienstanweisungen, gespeichert als Textdateien."
- „Commands sind die Knöpfe, die sie auslösen."
- „Du kannst für jeden wiederkehrenden Ablauf einen eigenen Skill schreiben: die Review-Checkliste deines Teams, dein Vorgehen beim Deployment, deine Schritte bei einem Sicherheitsvorfall."

**Wenn Claude in Schritt 3 das Codewort doch nennt:** Prüf, ob die Frage mit „Without using any tools“ gestellt wurde und ob der Skill noch nicht aufgerufen wurde (neue Sitzung starten).

</details>
