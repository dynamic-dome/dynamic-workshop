---
id: S3.15
type: practice
title: "Praxis-Station Session 3: alles in einem Ablauf"
shelf: practice
level: core
minutes: 25
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann die Bausteine aus Session 3 in einem Ablauf verbinden: Regeln für einen Lauf ohne mich, ein gedeckelter Lauf in einem Worktree, ein eigener Subagent als Gegenprüfung und die Übernahme erst nach meiner Prüfung."
sources: []
aliases: []
offers: [S3.4, S3.6]
---

# S3.15 · Praxis-Station Session 3: alles in einem Ablauf

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~25 Min** · **Voraussetzungen:** keine
>
> ← [S3.14 Self-Improve-Loop: was geht und wo es endet](s3-14-self-improve-loop.md) · [Bibliothek](README.md) · [X.3 Der minimale Agent: Pi als Spiegel](x-03-pi-als-spiegel.md) →
<!-- meta:end -->

## Auf einen Blick

Diese Station schließt Session 3 ab. Du lässt Claude einmal ohne dich arbeiten und hältst dabei alle Fäden in der Hand: Regeln legen fest, was der Lauf darf, ein Rundenlimit und ein Budget begrenzen ihn, er arbeitet in einem eigenen Worktree, ein zweiter Agent prüft das Ergebnis gegen, und in deinen Hauptordner kommt es erst, wenn du es gelesen hast. Das dauert etwa 20 Minuten und kostet einen kleinen Lauf mit `sonnet`.

Hast du unterwegs eine Übung ausgelassen, findest du sie in der Tabelle am Ende wieder.

## Selbst machen

### Übung: ein Lauf ohne dich, mit Gegenprüfung (etwa 20 Minuten)

**Ziel:** Ein Lauf ohne Rückfragen behebt einen Fehler in einem Worktree. Du belegst an `git`, dass er nur die erlaubte Datei geändert hat, lässt einen eigenen Subagenten gegenprüfen und übernimmst das Ergebnis dann selbst.

**Startzustand:** ein neues Git-Repository in `~/cc-workshop/station3`. Du brauchst Claude Code, Git und Python; unter macOS und Linux heißt der Befehl meist `python3`. Die Git-Identität gilt nur für dieses Repository.

```bash
# macOS / Linux / Git Bash
mkdir -p ~/cc-workshop/station3/.claude/agents && cd ~/cc-workshop/station3
git init -q
git config user.name "Learner"
git config user.email "learner@example.com"
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\cc-workshop\station3\.claude\agents" | Out-Null
Set-Location "$HOME\cc-workshop\station3"
git init -q
git config user.name "Learner"
git config user.email "learner@example.com"
```

1. **Das Programm und sein Test.** Leg mit einem Editor fünf Dateien an. `calc.py` enthält einen Fehler, den du nicht korrigierst:

   ```python
   def add(a, b):
       return a - b
   ```

   `test_calc.py`:

   ```python
   import unittest
   from calc import add


   class AddTest(unittest.TestCase):
       def test_add(self):
           self.assertEqual(add(2, 3), 5)


   if __name__ == "__main__":
       unittest.main()
   ```

   `.gitignore`, damit der Worktree des Laufs nicht als Änderung erscheint:

   ```text
   .claude/worktrees/
   ```

2. **Die Regeln ([S3.8](s3-08-rechte-fuer-autonomie.md)).** Speichere als `.claude/settings.json`. Der Lauf darf Dateien ändern und die Tests starten, aber die Testdatei selbst ist gesperrt. So kann er die Tests nicht grün machen, indem er sie abschwächt ([S3.14](s3-14-self-improve-loop.md)):

   <!-- cockpit:example -->
   ```json
   {
     "permissions": {
       "allow": [
         "Edit",
         "Bash(python -m unittest*)", "Bash(python3 -m unittest*)",
         "PowerShell(python -m unittest*)", "PowerShell(python3 -m unittest*)"
       ],
       "deny": ["Edit(test_calc.py)"]
     }
   }
   ```

3. **Der Gegenprüfer ([S3.3](s3-03-eigener-subagent.md)).** Speichere als `.claude/agents/fix-checker.md`. Er darf nur lesen:

   ```md
   ---
   name: fix-checker
   description: Checks whether a change is a real fix or weakens a test. Use when asked to check a fix.
   tools: Read, Grep, Glob
   ---

   You check a change. You are given a changed file, the original file and a test file. Read all three. Say in two sentences whether the change makes the code do what the test demands, and whether the test file still demands the same as the original test file. Do not modify any files.
   ```

4. Committe alles. Der Lauf arbeitet gleich in einem Worktree, und der enthält nur, was eingecheckt ist, also auch Regeln und Agent:

   ```bash
   git add .gitignore calc.py test_calc.py .claude/settings.json .claude/agents/fix-checker.md
   git commit -q -m "start"
   ```

5. **Vertrauen, einmal von Hand.** Allow-Regeln aus der `.claude/settings.json` eines Projekts gelten laut Doku erst, nachdem du den Vertrauensdialog für den Ordner bestätigt hast, und ein Lauf mit `-p` zeigt diesen Dialog nie. Ohne diesen Schritt würde der Lauf gleich jede Änderung ablehnen. Starte deshalb einmal `claude --permission-mode default` im Ordner. Erwartet: Der Dialog zählt die Freigaben auf, die der Ordner mitbringt (deine fünf Allow-Regeln), und warnt, dass sie ohne Rückfrage gelten werden. Bestätige ihn. Gib `/permissions` ein und such deine Regeln in den Reitern Allow und Deny. Schließ die Ansicht mit `Esc` und beende die Sitzung mit `/exit`.

6. **Der Lauf ohne dich ([S3.13](s3-13-autonome-loops-absichern.md)).** Gib die Zeile in einem Stück ein, sie gilt in beiden Shells:

   ```bash
   claude -p --worktree fix-add --model sonnet --permission-mode dontAsk --max-turns 10 --max-budget-usd 0.50 "The unit tests in this folder fail. Fix the code so that they pass. Do not change test_calc.py."
   ```

   Erwartet: Der Lauf endet von selbst mit einem kurzen Bericht, ohne eine einzige Rückfrage. Dein Hauptordner ist unverändert: `git status --short` zeigt nichts. Meldet der Lauf, dass er die Tests nicht starten durfte, hat sein Befehl nicht auf deine Regel gepasst (etwa weil er mehrere Befehle in eine Zeile schrieb); den Testlauf machst du in Schritt 9 ohnehin selbst.

7. **Die Prüfung an git.** Sieh nach, was der Lauf im Worktree getan hat:

   ```bash
   git -C .claude/worktrees/fix-add status --short
   git -C .claude/worktrees/fix-add diff
   ```

   Erwartet: Nur `calc.py` ist geändert, aus `a - b` wurde `a + b`. `test_calc.py` taucht nicht auf.

8. **Die Gegenprüfung ([S3.6](s3-06-devils-advocate.md)).** Starte im Hauptordner `claude --permission-mode default` und gib ein:

   ```text
   @agent-fix-checker Check the change in .claude/worktrees/fix-add/calc.py against the original calc.py in this folder. The test files are test_calc.py here and .claude/worktrees/fix-add/test_calc.py. Is it a real fix, and was the test weakened?
   ```

   Erwartet: Der Subagent liest die Dateien und meldet, dass die Änderung den Test erfüllt und die Testdatei gleich geblieben ist. Sein Urteil ist ein zweiter Blick, kein Beweis: Den Beweis liefert der Testlauf im nächsten Schritt. Beende die Sitzung mit `/exit`.

9. **Die Übernahme.** Erst jetzt kommt die Änderung in deinen Hauptordner, und zwar durch dich:

   ```bash
   git -C .claude/worktrees/fix-add commit -q -am "Fix add"
   git merge -q worktree-fix-add
   python -m unittest
   ```

   Nimm `python3 -m unittest`, wenn `python` bei dir nicht läuft. Erwartet: Der Testlauf endet mit `OK`, und `git log --oneline` zeigt „Fix add“ über „start“.

10. **Aufräumen.** Der Lauf hat seinen Worktree gesperrt zurückgelassen:

   ```bash
   git worktree unlock .claude/worktrees/fix-add
   git worktree remove .claude/worktrees/fix-add
   git branch -d worktree-fix-add
   ```

   Erwartet: `git worktree list` nennt nur noch den Hauptordner. Lösch danach den Ordner `~/cc-workshop/station3` selbst (in PowerShell mit `Remove-Item -Recurse -Force`, falls Windows sich an `.git` stört). Es läuft nichts weiter.

**Geschafft, wenn:**

- [ ] der Lauf ohne Rückfrage endete und dein Hauptordner danach unverändert war
- [ ] im Worktree nur `calc.py` geändert war und `test_calc.py` nicht
- [ ] der Subagent `fix-checker` die Änderung als echten Fix einstufte
- [ ] `python -m unittest` nach deinem Merge mit `OK` endete
- [ ] `git worktree list` am Ende nur den Hauptordner zeigte

### Was jede Schicht geleistet hat

| Schicht | Wo sie stand | Was ohne sie passiert wäre |
|---|---|---|
| Rechte-Modus `dontAsk` und Allow-Regeln | Start-Flag und `.claude/settings.json`, wirksam nach deiner Bestätigung des Ordners | der Lauf hätte auf eine Antwort gewartet oder alles gedurft |
| Deny-Regel auf die Testdatei | `.claude/settings.json` | ein abgeschwächter Test hätte genauso „grün“ ergeben |
| Rundenlimit und Budget | `--max-turns`, `--max-budget-usd` | ein festgefahrener Lauf hätte weiter Tokens verbraucht |
| Worktree | `--worktree fix-add` | die Änderung wäre ungeprüft in deinem Hauptordner gelandet |
| Gegenprüfer | `.claude/agents/fix-checker.md` | nur ein Blick, deiner, auf das Ergebnis |
| Dein Merge | Schritt 9 | niemand hätte entschieden, dass die Änderung gut ist |

### Drei Fragen zum Schluss

Beantworte sie für dich, schriftlich, je ein Satz:

1. Welche Aufgabe aus deiner Arbeit würdest du so laufen lassen, und welche Datei bekäme die Deny-Regel?
2. Woran würdest du bei dieser Aufgabe ablesen, dass der Lauf nur getan hat, was er sollte?
3. Was davon dürfte nie ohne deine Übernahme in den Hauptbranch?

### Ausgelassene Übungen nachholen

| Du willst üben | Übung | Zeit | Kapitel |
|---|---|---|---|
| was ein Subagent weiß und was nicht | was ein Subagent weiß und was nicht | 10 Min. | [S3.1](s3-01-was-ist-ein-agent.md#selbst-machen) |
| einen eingebauten Subagenten anfordern | Explore anfordern und die Delegation finden | 8 Min. | [S3.2](s3-02-eingebaute-subagenten.md#selbst-machen) |
| einen eigenen Subagenten begrenzen | einen schreibgeschützten Subagenten bauen und seine Grenze testen | 15 Min. | [S3.3](s3-03-eigener-subagent.md#selbst-machen) |
| parallele und abhängige Aufgaben unterscheiden | Fan-out und Pipeline an einem kleinen Projekt | 15 Min. | [S3.4](s3-04-orchestrierungsmuster.md#selbst-machen) |
| eine Sitzung im Hintergrund führen | eine Hintergrund-Sitzung starten, lesen, stoppen und entfernen | 10 Min. | [S3.5](s3-05-hintergrund-und-teams.md#selbst-machen) |
| Befunde gegenprüfen lassen und selbst urteilen | Ankläger und Verteidiger selbst bauen | 25 Min. | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| die eingebauten Reviews einsetzen | zwei Reviews an einem Branch mit eingebautem Fehler | 15 Min. | [S3.7](s3-07-eingebaute-reviews.md#selbst-machen) |
| Regeln für einen Lauf ohne dich | Regeln für einen Lauf ohne dich schreiben und prüfen | 15 Min. | [S3.8](s3-08-rechte-fuer-autonomie.md#selbst-machen) |
| was geschützte Pfade in jedem Modus tun | geschützte Pfade in drei Modi | 12 Min. | [S3.9](s3-09-geschuetzte-pfade-und-sandbox.md#selbst-machen) |
| einen Skill ohne Shell-Befehle laden | die Skill-Shell abschalten und sehen | 10 Min. | [S3.10](s3-10-netzwerk-und-skills-haerten.md#selbst-machen) |
| sensible Muster vor dem Schreiben abfangen | den Scanner einrichten und blocken sehen | 15 Min. | [S3.11](s3-11-datenschutz-und-compliance.md#selbst-machen) |
| im Takt oder bis zu einer Bedingung arbeiten lassen | wählen, einrichten, prüfen, aufräumen | 15 Min. | [S3.12](s3-12-zeitgesteuert-arbeiten.md#selbst-machen) |
| einen Lauf hart begrenzen | einen gedeckelten Lauf im Worktree stoppen sehen | 15 Min. | [S3.13](s3-13-autonome-loops-absichern.md#selbst-machen) |
| aus einem Fehler eine Regel machen | aus einem Fehler eine Regel machen und prüfen | 12 Min. | [S3.14](s3-14-self-improve-loop.md#selbst-machen) |

Weiter geht es in Session 4 mit Modellen, Pipelines und Fehlersuche, ab [S4.1](s4-01-modell-pro-phase.md).

## Check

Du kannst einen Lauf ohne dich so aufsetzen, dass Regeln, Grenzen, Worktree, Gegenprüfung und deine Übernahme ineinandergreifen, und für jede Schicht sagen, was sie abdeckt.

1. Warum mussten die Regeln und der Subagent eingecheckt sein, bevor der Lauf startete?
2. Was hat verhindert, dass der Lauf die Tests durch eine Änderung an der Testdatei grün macht, und was hätte dich gewarnt, wenn es doch passiert wäre?
3. Der Subagent nannte die Änderung einen echten Fix. Warum war das noch kein Beleg, und was war der Beleg?

<details><summary>Auflösung</summary>

1. Der Lauf arbeitet in einem Worktree, und ein Worktree enthält nur, was eingecheckt ist. Regeln und Agent, die nur im Hauptordner liegen, gäbe es dort nicht. Dazu kam Schritt 5: Die Allow-Regeln gelten erst, seit du den Ordner einmal als vertrauenswürdig bestätigt hast.
2. Die Deny-Regel `Edit(test_calc.py)`: Sie blockt in jedem Modus. Gewarnt hätte dich Schritt 7: `git status --short` im Worktree hätte die Testdatei als geändert gezeigt.
3. Der Subagent ist dasselbe Modell wie der Lauf und kann sich im selben Punkt irren; sein Urteil ist ein zweiter Blick. Der Beleg war der Testlauf nach deinem Merge, zusammen mit dem Diff, den du selbst gelesen hast.

</details>

## Weiterlesen

- [S3.3 · Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S3.8 · Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md)
- [S3.13 · Autonome Loops absichern: Budget und Worktree](s3-13-autonome-loops-absichern.md)
- [S3.14 · Self-Improve-Loop: was geht und wo es endet](s3-14-self-improve-loop.md)
- [S2.20 · Praxis-Station Session 2: alles in einem Ablauf](s2-20-praxis-station-2.md)
- [S4.11 · Abschluss: ein kleiner Build](s4-11-abschluss-kleiner-build.md), der Abschluss deines ganzen Pfads
