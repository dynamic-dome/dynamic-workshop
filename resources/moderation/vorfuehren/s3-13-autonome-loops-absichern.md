# Vorführen: S3.13 · Autonome Loops absichern: Budget und Worktree

> Demo und Hinweise für Moderierende zum Kapitel [S3.13 · Autonome Loops absichern: Budget und Worktree](../../library/s3-13-autonome-loops-absichern.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: erst die Grenze, dann der Loop, und der Worktree als Prüfstand (etwa 5 Minuten)

**Teil 1: die Grenze vor dem Loop**

Der teuerste Moment einer Loop-Demo ist der, in dem du Enter drückst, bevor eine Grenze steht. Setz sie also vorher und halte den Loop auf **eine** Iteration: Die Grenze fängt einen Ausreißer ab, die eine Iteration hält die Demo klein. Beachte dabei: `--max-budget-usd` wirkt nur mit `-p`. Eine interaktive Sitzung, die du mit `claude --max-budget-usd 1.00` startest, ist **nicht** gedeckelt. Zeig die harte Grenze deshalb an einem `-p`-Lauf; in der interaktiven Self-Improve-Demo ([S3.14](s3-14-self-improve-loop.md)) begrenzt nur die eine Iteration den Lauf, und du liest `/cost` vorher und nachher.

**Teil 2: Worktree als Prüfstand (3 Minuten, Pflicht)**

Zeig, wie ein Worktree einen abgeschotteten Arbeitsbaum für riskante Änderungen schafft:

```bash
git worktree add ../experiment-async-processing -b feature/async-experiment
cd ../experiment-async-processing
claude
# Make experimental changes — the main branch stays untouched
```

Ist das Experiment fertig, verwirf es oder führ es zusammen:

```bash
git worktree remove ../experiment-async-processing
```

`claude --worktree <name>` erledigt das Anlegen in einem Schritt und erzwingt die Trennung zusätzlich (siehe „Worktree" oben).

<details><summary>Für Moderierende</summary>

**Sagen:**

- Teil 1: „Ein ungedeckelter Self-Improve-Loop ist laut Sitzungsplan der größte Kostentreiber des Tages, geschätzt etwa 15 bis 50 Dollar. Deshalb steht die Grenze, bevor ich Enter drücke."
- Teil 2: „Worktrees sind wie der Prüfstand im Labor. Hier dürft ihr etwas kaputt machen, ohne die Produktion zu treffen."

</details>
