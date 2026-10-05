# Vorführen: S3.8 · Rechte für autonome Läufe

> Demo und Hinweise für Moderierende zum Kapitel [S3.8 · Rechte für autonome Läufe](../../library/s3-08-rechte-fuer-autonomie.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Regeln für einen Lauf ohne dich

**Ziel:** Zeigen, dass in `dontAsk` nur läuft, was vorab erlaubt ist, und dass Deny und Ask Regeln für einen Lauf ohne dich sind: Dieselben zwei Aufträge verhalten sich ohne und mit Schutzregeln verschieden.

Zeig die Übung aus dem Kapitel live: die Übung „Regeln für einen Lauf ohne dich schreiben und prüfen“ in [S3.8](../../library/s3-08-rechte-fuer-autonomie.md). Startzustand wie dort: das Repository `~/cc-workshop/rechte-lauf` mit `notes.txt` und `config.txt`, einem Startcommit und der Git-Identität nur für dieses Repository. Leg es vorher an; die `settings.json` in `.claude` schreibst du selbst, nicht über Claude. Ablauf: Runde 1 (Schritte 1 bis 3, nur Allow) und Runde 2 (Schritte 4 bis 6, mit Ask und Deny), zum Schluss `/permissions` (Schritt 7).

Als Vorspann (etwa 1 Minute) kannst du die Modi in der Statusleiste zeigen: Starte mit `claude --permission-mode default` und drück `Shift+Tab`, bis `⏵⏵ accept edits on` erscheint. Ohne Flag startet eine neue Sitzung in aktuellen Versionen in `auto`. Die Modi im Einzelnen stehen in [S1.5](../../library/s1-05-rechte-im-alltag.md) und [S1.6](../../library/s1-06-rechte-modi.md).

**Drei Modi nur erklären, nicht live zeigen:** `auto` (ein Klassifikator prüft statt dir, laut Doku „does not guarantee safety“), `bypassPermissions` (der Generalschlüssel, Deny-Regeln blocken aber weiter, nur in abgeschlossenen Testräumen wie Container oder VM ohne Internetzugang) und der Plan-Modus (`claude --permission-mode plan`: Claude legt den Plan vor, geändert wird nichts, bevor du ihn freigibst).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 12 bis 15 Minuten für beide Runden.

**Sagen:**

- Runde 1, Schritt 2: „`dontAsk` ist der Modus für Läufe, deren Erlaubtes ich vorab festlege, etwa im CI. Claude arbeitet, ohne je zu fragen. Alles, was eine Allow-Regel trifft, läuft." Die Statusleiste zeigt `⏵⏵ don't ask on`.
- Schritt 3: „Ohne Schutz hat der Lauf die Datei geändert, die ich nicht ändern wollte." Zeig `git show --stat HEAD` mit beiden Dateien und nimm den Commit mit `git reset --hard HEAD~1` zurück; das gilt nur für dieses Wegwerf-Repository.
- Runde 2, Schritt 4: „Drei Regeln: Allow für das Erlaubte, Ask auf `git commit`, Deny auf `Edit(config.txt)`. In dieser Reihenfolge wertet Claude Code sie aus, erst Deny, dann Ask, dann Allow. Das Ask heißt für einen Menschen ‚frag mich‘, für einen Lauf in `dontAsk` ‚nicht ohne dich‘."
- Schritt 5: „Die Änderung an `config.txt` wird abgelehnt, `git add` läuft, `git commit` wird abgelehnt." Den Wortlaut der Ablehnungen zeigst du im Transkript (`Ctrl+O`). Zeig im Terminal daneben `git diff HEAD --stat` (nur `notes.txt`) und `git log --oneline` (nur der Startcommit).
- Schritt 7: „`/permissions` zeigt die Regeln, die zusätzlich zum Modus gelten, und aus welcher Datei sie stammen. Den Modus selbst wechselt er nicht." Mit `Esc` schließen.
- Grenze: „Eine Regel wie `Bash(rm *)` stoppt `rm -rf build/`, aber nicht `/bin/rm -rf build/` und nicht `bash -c 'rm -rf build/'`. Wer das braucht, setzt zusätzlich eine Sandbox oder einen Hook ein ([S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md), [S2.8](s2-08-hook-einrichten.md))."
- Zum Abschluss: „Einem Handwerker gibst du im laufenden Gebäude nie einen Generalschlüssel. Du wählst die Freigabestufe für die Lage, und für Läufe ohne dich schreibst du die Regeln vorher."

**Wenn es hakt:**

- **Claude packt Änderungen und Commit in eine Shell-Zeile, und `dontAsk` lehnt sie als Ganzes ab:** Gib die zwei Aufträge einzeln ein, so wie in der Übung, jeder mit genau einer Regel.
- **Unklar, welcher Modus aktiv ist:** Die Statusleiste zeigt ihn (`⏸ manual mode on`, `⏵⏵ accept edits on`, `⏵⏵ don't ask on`, `⏸ plan mode on`); `/permissions` zeigt Regeln, keinen Modus.
- **Die Allow-Regeln greifen nicht:** Allow-Regeln aus der `.claude/settings.json` eines Projekts gelten laut Doku erst, nachdem der Vertrauensdialog für den Ordner bestätigt wurde. Starte eine interaktive Sitzung im Ordner und bestätige ihn.
- **`acceptEdits` fragt trotzdem bei Änderungen (Vorspann):** Liegt die Datei außerhalb des Arbeitsordners oder in einem geschützten Pfad wie `.claude/` ([S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md))?

</details>
