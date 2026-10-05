# Vorführen: S4.3 · Headless: claude -p als Pipeline-Stufe

> Demo und Hinweise für Moderierende zum Kapitel [S4.3 · Headless: claude -p als Pipeline-Stufe](../../library/s4-03-headless.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Headless Claude, drei Aufrufe, ein Umschlag, ein Deckel

**Ziel:** Zeigen, dass derselbe Claude, mit dem du bisher interaktiv gearbeitet hast, auch als einmaliges Kommandozeilen-Werkzeug läuft: Text über stdin, JSON-Umschlag, ein festes Schema, und der Exit-Code sagt, ob es geklappt hat.

Zeig die Übung aus dem Kapitel live: die Übung „drei Aufrufe, ein Umschlag, ein Deckel“ in [S4.3](../../library/s4-03-headless.md). Startzustand wie dort: der Ordner `~/cc-workshop/headless` mit `issue.txt`. Leg ihn vorher an. Du tippst alles in der Shell und brauchst keine Claude-Sitzung. Jeder Aufruf steht mit `--model haiku` und einer Zug-Grenze da, damit er wenig kostet; `jq` brauchst du nicht. Ablauf: die Schritte 1 bis 5 der Übung (Text über stdin und `exit=0`, der JSON-Umschlag mit seinen Feldnamen, das Schema, der Fehlschlag mit einem ungültigen Schema, der gedeckelte Lauf mit `--max-turns 1`).

Die Kostengrenze und `--bare` zeigt die Demo in [S4.4](s4-04-ci-zugang-und-kosten.md). Der garantierte Live-Einstieg in Session 3, ein einzelner `claude -p`-Aufruf, steht in [S3.1](s3-01-was-ist-ein-agent.md).

<details><summary>Für Moderierende</summary>

**Garantierter Anker:** Diese Demo braucht nur das lokal installierte und angemeldete `claude`: kein Plugin, kein Codex, keine Bridge. Eine Netzverbindung zur Claude-API braucht sie wie jeder Aufruf.

**Sagen:**

- Schritt 1: „Es gab keinen Vertrauensdialog und keine Rückfrage. Ein Wort auf stdout, danach der Exit-Code." Zeig `exit=0`.
- Schritt 2: „Das ist der Umschlag. Mein Skript muss das richtige Feld wählen." Lies die Feldnamen vor: darunter laut Doku `result`, `session_id` und `total_cost_usd`.
- Schritt 3: „Darauf kann sich eine CI-Pipeline verlassen. Frei formulierte Prosa bricht Parser, ein Schema nicht." Das Ergebnis liegt im Feld `structured_output`, eine Ebene tiefer; die Abfrage `category` auf oberster Ebene liefert nichts.
- Schritt 4: „Keine Prosa zurück, sondern eine Fehlermeldung und ein Exit-Code ungleich 0. Ein Skript, das den Exit-Code beachtet, bemerkt den Fehler."
- Schritt 5: „Der Deckel hält, bevor die Antwort fertig ist." Der Lauf endet mit einem Fehler und einem Exit-Code ungleich 0. Kommt der Lauf mit einem Zug durch, nimm den längeren Auftrag aus dem Kapitel.
- Zum Abschluss der ganzen Demo, nach der Demo in [S4.4](s4-04-ci-zugang-und-kosten.md): „Wir haben Claude Code gerade in ein Unix-Werkzeug verwandelt. Es nimmt stdin, liefert stdout, gibt einen Exit-Code zurück, beachtet Flags und bleibt im Budget. Das ist die Eintrittskarte in jedes CI-System: GitHub Actions, GitLab, Jenkins, dein eigener Cron. Der interaktive Claude ist die eine Hälfte des Produkts. Das hier ist die andere."

**Wenn die Auswertung nichts findet:** Du hast das Feld auf oberster Ebene abgefragt. Das Schema-Ergebnis liegt eine Ebene tiefer in `structured_output`.

**Wenn unter Windows PowerShell 5.1 das Schema abgelehnt wird:** Windows PowerShell 5.1 reicht Anführungszeichen in Argumenten nicht unverändert an Programme weiter, PowerShell 7 schon. Nimm den Befehl aus dem Kapitel, der die Anführungszeichen für 5.1 maskiert.

</details>
