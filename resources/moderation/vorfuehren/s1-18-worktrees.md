# Vorführen: S1.18 · Worktrees als Testlabor

> Demo und Hinweise für Moderierende zum Kapitel [S1.18 · Worktrees als Testlabor](../../library/s1-18-worktrees.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen Worktree anlegen (Bonus zu Demo 1.4)

**Ziel:** Zeigen, dass ein Experiment in einem eigenen Ordner auf einem eigenen Branch läuft, während der aktuelle Branch unberührt bleibt.

**Vorbereitung:** Die Demo schließt an den Git-Ablauf aus [S1.16](s1-16-git-in-einem-fluss.md) an und läuft im selben Ordner, auf dem Branch `feature/ipv4-validation`. Sie ist ein Bonus, wenn Zeit bleibt.

**Schritt 1: den Worktree anlegen**

Tippe in Claude Code:

```
Create a git worktree at ../validators-experiment on a new branch
called experiment/regex-validators
```

Was passiert: Claude führt `git worktree add ../validators-experiment -b experiment/regex-validators` aus und bestätigt.

**Schritt 2: die Worktrees anzeigen**

Tippe in Claude Code:

```
What worktrees do we have now?
```

Was passiert: Claude führt `git worktree list` aus und zeigt den Hauptordner und den neuen Experiment-Worktree.

<details><summary>Für Moderierende</summary>

**Dauer:** Teil der etwa 10 Minuten von Demo 1.4 ([S1.16](s1-16-git-in-einem-fluss.md)); nur, wenn Zeit bleibt.

**Sagen:**

- Vor Schritt 1: „Angenommen, ich will einen ganz anderen Ansatz ausprobieren, vielleicht doch mit Regex, um zu sehen, ob es damit sauberer wird. Meinen aktuellen Branch will ich dabei nicht durcheinanderbringen. Also: Worktree."
- Nach Schritt 2: „Zwei Branches. Zwei Ordner. Beide gehören zu demselben Repository. Claude kann im Experiment-Ordner arbeiten und den Regex-Ansatz ausprobieren, während mein aktueller Branch völlig unberührt bleibt. Klappt das Experiment, merge ich. Klappt es nicht, lösche ich den Worktree und lasse es liegen. Kein Stash, keine versehentlichen Änderungen an meinem Branch."
- Brücke zur Analogie: „Erinnert euch an die Testbank: eigener Raum, dieselbe Ausstattung, völlig getrennt. Genau das ist das hier. Euer Live-System bekommt nichts davon mit, was im Testlabor passiert."
- Zum Schluss von Demo 1.4: „Worktrees geben euch das Testlabor-Modell, das ihr aus der physischen Sicherheit kennt: getrennte Umgebung, echte Ausstattung, kein Risiko für die Produktion."

**Wenn etwas schiefgeht:**

- **`git worktree add` scheitert, weil es den Branch schon gibt:** Lass `-b` weg; dann nutzt Git den vorhandenen Branch. Den Worktree mit `git worktree remove ../<dir>` zu entfernen, hilft hier allein nicht: Das löscht den Branch nicht, und mit `-b` scheitert der nächste Versuch wieder.

</details>
