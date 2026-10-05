# Vorführen: S3.13 · Autonome Loops absichern: Budget und Worktree

> Demo und Hinweise für Moderierende zum Kapitel [S3.13 · Autonome Loops absichern: Budget und Worktree](../../library/s3-13-autonome-loops-absichern.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: ein gedeckelter Lauf im Worktree (etwa 10 Minuten)

**Ziel:** Zeigen, dass ein unbeaufsichtigter Lauf erst mit Grenzen sicher ist: Das Rundenlimit stoppt ihn mit einem Fehler, und der Worktree hält die Arbeit vom Hauptordner getrennt.

Zeig die Übung aus dem Kapitel live: die Übung „einen gedeckelten Lauf im Worktree stoppen sehen“ in [S3.13](../../library/s3-13-autonome-loops-absichern.md). Startzustand wie dort: das Repository `~/cc-workshop/nachtlauf` mit den fünf Dateien `notes-1.txt` bis `notes-5.txt`, der `.gitignore`-Zeile für `.claude/worktrees/` und einem Startcommit. Leg es vorher an. Ablauf: Schritte 1 bis 5 der Übung, also Lauf 1 mit `--max-turns 2`, den Rückgabewert ablesen, Lauf 2 mit `--max-turns 12`, `git worktree list` und das Aufräumen mit `unlock` zuerst.

**Teil 1: die Grenze vor dem Loop.** Der teuerste Moment einer Loop-Demo ist der, in dem du Enter drückst, bevor eine Grenze steht. Setz sie also vorher. Beachte: `--max-budget-usd` und `--max-turns` wirken nur mit `-p`. Eine interaktive Sitzung, die du mit `claude --max-budget-usd 1.00` startest, ist **nicht** gedeckelt. Zeig die harte Grenze deshalb an einem `-p`-Lauf; die Demo in [S3.14](s3-14-self-improve-loop.md) ist interaktiv, dort greifen weder Budget noch Rundenlimit.

**Teil 2: der Worktree als Prüfstand.** In der Übung läuft jeder Lauf mit `--worktree` in einem eigenen Worktree unter `.claude/worktrees/`, das Hauptverzeichnis bleibt unberührt.

<details><summary>Für Moderierende</summary>

**Sagen:**

- Lauf 1: „Die Aufgabe ist nur lesen: Jede Datei nennt die nächste. Ich gebe dem Lauf nur zwei Runden und 0,50 Dollar. Er kommt nicht ans Ende." Zeig den Fehler zum Rundenlimit und danach den Rückgabewert ungleich 0 (`echo "exit=$?"`, in PowerShell `"exit=$LASTEXITCODE"`). Ein Skript oder eine CI-Pipeline erkennt so, dass der Lauf nicht fertig geworden ist. Wie viele Runden Claude für die Kette braucht, steht nicht fest; meldet Lauf 1 doch die ganze Kette, wiederhole ihn mit `--max-turns 1`.
- Lauf 2: „Mit zwölf Runden läuft er durch." Das Budget von 0,50 Dollar ist bei dieser kleinen Aufgabe ein Sicherheitsnetz, das nicht erreicht wird: Das Rundenlimit hat in Lauf 1 gestoppt. Das Budget als Auslöser zeigt die Extra-Übung des Kapitels.
- Schritt 4: „Worktrees sind wie der Prüfstand im Labor. Hier dürft ihr etwas kaputt machen, ohne die Produktion zu treffen." Zeig `git status --short` im Hauptordner (leer) und `git worktree list` mit den beiden Worktrees, beide `locked`.
- Schritt 5: „Ein `-p`-Lauf räumt seinen Worktree nicht auf, und er lässt seine Sperre stehen. Ohne `git worktree unlock` verweigert Git das Entfernen. Die Reihenfolge ist immer: `unlock`, `remove`, dann den Branch löschen."

**Wenn etwas schiefgeht:**

- **Das Entfernen scheitert:** Der Worktree ist noch gesperrt. `git worktree unlock <Pfad>`, dann `git worktree remove <Pfad>`.
- **Der Worktree fehlt im Hauptordner:** Er liegt unter `.claude/worktrees/<name>`; `git worktree list` nennt die Pfade.

</details>
