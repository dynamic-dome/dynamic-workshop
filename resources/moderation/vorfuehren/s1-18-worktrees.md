# Vorführen: S1.18 · Worktrees als Testlabor

> Demo und Hinweise für Moderierende zum Kapitel [S1.18 · Worktrees als Testlabor](../../library/s1-18-worktrees.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen Worktree anlegen und wieder abräumen

**Ziel:** Zeigen, dass ein Experiment in einem eigenen Ordner auf einem eigenen Branch läuft, während der Hauptordner unberührt bleibt.

Zeig die Übung aus dem Kapitel live: die Übung „ein Worktree, den du wieder abräumst“ in [S1.18](../../library/s1-18-worktrees.md).

**Startzustand:** das Repository `~/cc-workshop/worktree` mit einem Commit und der `.gitignore`-Zeile für `.claude/worktrees/`, in dem du `claude` einmal gestartet und den Vertrauensdialog bestätigt hast, wie im Startzustand der Übung. Ohne diesen Start bricht `claude --worktree` mit einer Fehlermeldung ab. Du brauchst ein zweites Terminal im Hauptordner.

**Ablauf:** Schritte 1 bis 5 der Übung: `claude --worktree test-1 --permission-mode acceptEdits`, die Datei `experiment.txt` anlegen lassen, im zweiten Terminal `git worktree list` und die Probe, dass die Datei nur im Worktree liegt, dann `/exit` mit „Remove worktree“ und die Kontrolle, dass Worktree und Branch weg sind. Der Worktree von Hand (`git worktree add -b …`) ist die Extra-Übung des Kapitels; zeig ihn nur, wenn Zeit bleibt.

Die Demo ist eine Zugabe zur Git-Demo in [S1.16](s1-16-git-in-einem-fluss.md), wenn dort Zeit bleibt; sie braucht deren Ordner nicht.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 bis 8 Minuten; nur, wenn Zeit bleibt.

**Sagen:**

- Vor Schritt 1: „Angenommen, ich will etwas ausprobieren und meinen Hauptordner dabei nicht durcheinanderbringen. Also: Worktree."
- Nach Schritt 3: „Zwei Ordner, zwei Branches, ein gemeinsames `.git`. Die Datei liegt nur im Worktree. Klappt das Experiment, merge ich. Klappt es nicht, entferne ich den Worktree. Kein Stash, keine versehentlichen Änderungen am Hauptordner."
- Schritt 4: Lies die Frage von Claude Code vor und wähl „Remove worktree“. „Entfernen löscht Ordner und Branch samt Arbeit. Wollt ihr sie behalten, wählt ihr ‚Keep worktree‘ oder committet vorher."
- Zum Schluss: Der Worktree trennt Dateien und Branch voneinander, nicht dein Experiment von deinem Rechner. Das ist die Frage 2 im Check des Kapitels; stell sie der Gruppe.

**Wenn etwas schiefgeht:**

- **`claude --worktree` bricht mit einer Fehlermeldung ab:** In diesem Ordner wurde noch nie Claude gestartet. Starte einmal `claude`, bestätige den Vertrauensdialog und versuch es erneut.
- **`git worktree add` scheitert, weil es den Branch schon gibt (Extra-Übung):** `-b` legt nur neue Branches an. Nimm einen neuen Namen, oder lass `-b` weg, dann checkt Git den vorhandenen Branch aus. `git worktree remove` allein löscht den Branch nicht.

</details>
