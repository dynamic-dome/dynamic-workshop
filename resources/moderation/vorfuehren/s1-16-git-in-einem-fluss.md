# Vorführen: S1.16 · Git in einem Fluss: Branch, Commit, PR

> Demo und Hinweise für Moderierende zum Kapitel [S1.16 · Git in einem Fluss: Branch, Commit, PR](../../library/s1-16-git-in-einem-fluss.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: der Git-Ablauf

**Ziel:** Einen kompletten Ablauf zeigen, von Branch über Umsetzung, Test und gezieltes Stagen bis zum Commit, alles in einem Gespräch, und dass eine Datei, die nicht zur Änderung gehört, draußen bleibt.

Zeig die Übung aus dem Kapitel live: die Übung „Branch, Test, gezielter Commit“ in [S1.16](../../library/s1-16-git-in-einem-fluss.md).

**Startzustand:** das Repository `~/cc-workshop/git` mit `README.md` (ein Commit) und der unbekannten Datei `secrets.txt`, genau wie im Startzustand der Übung. Lege es vor der Demo an; Git braucht für den Commit einen Namen und eine E-Mail-Adresse (`git config user.name`, `git config user.email`). Starte mit `claude --permission-mode acceptEdits`.

**Ablauf:** Schritte 1 bis 7 der Übung mit denselben Aufträgen. Der PR ist die Extra-Übung des Kapitels und braucht ein leeres, privates Test-Repository auf GitHub, einen Push des Hauptbranches und eine angemeldete GitHub CLI (`gh auth login` vor dem Workshop). Zeig ihn nur, wenn das vorbereitet ist.

Eine Worktree-Zugabe steht in [S1.18](s1-18-worktrees.md).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten für die Schritte 1 bis 7.

**Sagen:**

- Schritt 1: „Bevor wir irgendetwas anfassen, schauen wir, in welchem Zustand wir sind. Eine gute Gewohnheit, ob in Claude Code oder nicht." Zeig, dass `secrets.txt` als unbekannte Datei auftaucht, und sag, dass sie nie in einen Commit darf.
- Schritt 3, während Claude arbeitet: Der Auftrag legt Funktion und Tests fest, du schreibst keinen Code.
- Schritt 5: „Immer vor dem Commit prüfen. Das gilt, ob du den Code geschrieben hast oder Claude. Besonders, wenn es Claude war." Zeig im Diff, dass nur zwei Dateien drin sind. Frag die Gruppe, was bei `git add .` passiert wäre.
- Schritt 6: Den Commit gibst du frei; im Modus `acceptEdits` laufen Dateiänderungen ohne Rückfrage, Git-Befehle, die etwas ändern, nicht.
- Schritt 7: „Branch, Code, Test, Commit. Der ganze Ablauf in einem Gespräch. Kein Wechsel in eine Git-Oberfläche, kein zweites Terminal. Und die Datei, die nicht dazugehörte, ist weiter draußen."
- Zum Schluss: „Git wird zu etwas, worüber du nachdenkst, nicht zu etwas, das du von Hand verwaltest." Worktrees findest du in [S1.18](../../library/s1-18-worktrees.md).

**Wenn etwas schiefgeht:**

- **Der Diff ist leer, obwohl Claude Dateien angelegt hat:** `git diff` zeigt neue, ungetrackte Dateien nicht. Erst stagen, dann `git diff --staged`.
- **Git meldet beim Commit, dass Name und E-Mail fehlen:** Das ist ein Setup-Problem. Setz beides mit `git config user.name` und `git config user.email` und lass Claude den Commit wiederholen.
- **Ein Test schlägt fehl:** Bearbeite die Datei nicht selbst, sondern gib Claude die Fehlermeldung zurück und lass es reparieren und neu testen.
- **`gh pr create` scheitert (Extra-Übung):** Es braucht eine angemeldete GitHub CLI und einen Remote. Lass den PR-Schritt weg und sag, was dafür vorher nötig ist.

</details>
