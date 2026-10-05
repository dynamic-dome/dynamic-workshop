---
id: S1.20
type: practice
title: "Praxis-Station Session 1: alles in einem Ablauf"
shelf: practice
level: core
minutes: 20
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann die Bausteine aus Session 1 in einem Ablauf verbinden: Regeln in CLAUDE.md und settings.json, ein präziser Auftrag und ein geprüfter Commit auf einem eigenen Branch."
sources: []
aliases: []
offers: [S1.1, S1.10, S1.13, S1.16, S1.18]
---

# S1.20 · Praxis-Station Session 1: alles in einem Ablauf

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~20 Min** · **Voraussetzungen:** keine
>
> ← [S1.19 Kosten im Blick: /cost, /usage und Budgetgrenzen](s1-19-kosten-im-blick.md) · [Bibliothek](README.md) · [X.2 Mit Claude Code lernen](x-02-lernen-mit-claude-code.md) →
<!-- meta:end -->

## Auf einen Blick

Diese Station schließt Session 1 ab. Du verbindest in einer einzigen kleinen Aufgabe, was du bisher einzeln geübt hast: eine Sitzung im passenden Rechte-Modus, eine Regel in der CLAUDE.md, eine Sperre in der `settings.json`, einen präzisen Auftrag und einen gezielten Commit auf einem eigenen Branch. Das dauert etwa 15 Minuten.

Hast du unterwegs eine Übung ausgelassen, findest du sie in der Tabelle am Ende wieder.

## Selbst machen

### Übung: ein kleiner Ablauf von Anfang bis Ende (etwa 15 Minuten)

**Ziel:** Du lieferst eine kleine Funktion mit Test als Commit auf einem eigenen Branch. Unterwegs gelten zwei Regeln, die du selbst gesetzt hast, und du prüfst beide.

**Startzustand:** ein neues lokales Repository in `~/cc-workshop/station1` mit einem ersten Commit und einer Sperre fürs Löschen. Git braucht für den Commit einen Namen und eine E-Mail-Adresse (`git config user.name`, `git config user.email`).

```bash
# macOS / Linux / Git Bash
mkdir -p ~/cc-workshop/station1/.claude && cd ~/cc-workshop/station1
git init
echo "# Opening hours" > README.md
git add README.md
git commit -m "Initial commit"
echo '{ "permissions": { "deny": ["Bash(rm *)", "PowerShell(Remove-Item *)"] } }' > .claude/settings.json
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\cc-workshop\station1\.claude" | Out-Null; Set-Location "$HOME\cc-workshop\station1"
git init
"# Opening hours" | Set-Content README.md
git add README.md
git commit -m "Initial commit"
'{ "permissions": { "deny": ["Bash(rm *)", "PowerShell(Remove-Item *)"] } }' | Set-Content .claude\settings.json
```

Starte mit `claude --permission-mode default`: Du gibst jede Änderung und jeden Git-Befehl einzeln frei.

1. **Die Hausordnung ([S1.10](s1-10-claude-md.md)).** Gib ein: `Create a CLAUDE.md with exactly these two rules: every function has a one-line docstring; use only the Python standard library.`
2. **Der Branch ([S1.16](s1-16-git-in-einem-fluss.md)).** Gib ein: `Create a branch called feature/opening-hours.`
3. **Der Auftrag ([S1.13](s1-13-vager-und-praeziser-auftrag.md)).** Schreib ihn selbst, bevor du in den Vergleich schaust. Gebaut werden soll eine Funktion `is_open(hour)` in `hours.py`, die für die Stunden 8 bis 17 `True` liefert und sonst `False`, dazu Tests mit `unittest` in `test_hours.py`. Dein Auftrag nennt den Ort, das gewünschte Verhalten, die Grenze (was Claude nicht anfassen soll) und das Erfolgskriterium.

<details><summary>Vergleich</summary>

<!-- cockpit:example -->
```text
Create hours.py with a function is_open(hour) that returns True for the hours 8 to 17 and False otherwise. Add unittest tests in test_hours.py for 7, 8, 17 and 18. Do not change README.md or CLAUDE.md. Success: python -m unittest prints OK. Run the tests.
```

</details>

4. **Die Prüfung.** Lies jeden Vorschlag, bevor du ihn freigibst. Hat `is_open` einen einzeiligen Docstring? Das war deine Regel aus Schritt 1. Der Testlauf endet mit `OK`.
5. **Der Commit ([S1.16](s1-16-git-in-einem-fluss.md)).** Gib ein: `Stage only hours.py and test_hours.py, show me git diff --staged, then commit with the message "Add opening hours check".` Lies das Diff, bevor du den Commit freigibst.
6. **Die Sperre ([S1.5](s1-05-rechte-im-alltag.md)).** Gib ein: `Delete test_hours.py.` Erwartet: Claude Code lehnt den Befehl ab. Schlägt Claude danach einen anderen Weg vor, etwa über Python, lehn die Rückfrage ab: Die Regel sperrt den Befehl `rm`, nicht das Löschen an sich. Die Datei ist ohnehin committet, es wäre also nichts verloren gewesen.
7. **Der Blick auf den Kontext ([S1.8](s1-08-kontextfenster.md)).** Gib `/context` ein und lies die Zeile „Messages“: So viel hat dieser Ablauf belegt. Beende die Sitzung mit `/exit`.

**Aufräumen:** Lösch den Ordner `~/cc-workshop/station1` selbst.

**Geschafft, wenn:**

- [ ] `git log --oneline` den Commit „Add opening hours check“ auf `feature/opening-hours` zeigt
- [ ] `git show --stat` genau `hours.py` und `test_hours.py` auflistet
- [ ] `python -m unittest` mit `OK` endet
- [ ] `is_open` einen einzeiligen Docstring hat, ohne dass du es im Auftrag verlangt hast
- [ ] das Löschen abgelehnt wurde und `test_hours.py` noch da ist

### Wenn Claude danebenliegt

Liefert Claude etwas Falsches, korrigiere gezielt: Nenn das konkrete Problem und sag, dass nur das behoben werden soll.

```
That's not quite right. The issue is [specific problem]. Fix only that — don't change anything else.
```

### Drei Fragen zum Schluss

Beantworte sie für dich, schriftlich, je ein Satz:

1. Wo hattest du in dieser Session am meisten das Gefühl, die Kontrolle zu haben, und wo am wenigsten?
2. Welche Regel deines eigenen Projekts würdest du heute in eine CLAUDE.md schreiben, und welche Sperre in die `settings.json`?
3. Welche Information hast du bei deiner Arbeit im Kopf, die in jedem Auftrag stehen müsste?

### Ausgelassene Übungen nachholen

| Du willst üben | Übung | Zeit | Kapitel |
|---|---|---|---|
| die Grundschleife: beschreiben, freigeben, ausführen, erweitern | dein erstes kleines Werkzeug | 15 Min. | [S1.1](s1-01-erster-kontakt.md#selbst-machen) |
| was zwei Rechte-Modi unterscheidet und wie eine Sperre hält | zwei Modi, eine Sperre | 10 Min. | [S1.5](s1-05-rechte-im-alltag.md#selbst-machen) |
| was im Kontextfenster liegt und wie du es leerst | das Fenster füllen und leeren | 8 Min. | [S1.8](s1-08-kontextfenster.md#selbst-machen) |
| eine Änderung zurückdrehen und den Verlauf verdichten | zurückdrehen und verdichten | 10 Min. | [S1.9](s1-09-kontext-steuern.md#selbst-machen) |
| Regeln, die Claude nach einem Neustart kennt | drei Regeln, ein Neustart | 10 Min. | [S1.10](s1-10-claude-md.md#selbst-machen) |
| was ein präziser Auftrag gegenüber einem vagen bringt | erst vage, dann deine vier Bausteine | 10 Min. | [S1.13](s1-13-vager-und-praeziser-auftrag.md#selbst-machen) |
| erst planen lassen, dann freigeben | planen, korrigieren, freigeben | 10 Min. | [S1.14](s1-14-plan-modus.md#selbst-machen) |
| Branch, Test und gezielter Commit über das Gespräch | Branch, Test, gezielter Commit | 10 Min. | [S1.16](s1-16-git-in-einem-fluss.md#selbst-machen) |
| gefahrlos parallel ausprobieren | ein Worktree, den du wieder abräumst | 10 Min. | [S1.18](s1-18-worktrees.md#selbst-machen) |
| was ein Modell für dieselbe Aufgabe kostet | dieselbe Aufgabe, drei Modelle | 10 Min. | [S1.19](s1-19-kosten-im-blick.md#selbst-machen) |

## Check

Du kannst die Bausteine aus Session 1 in einem Ablauf verbinden und für jeden sagen, wo er steht und was er leistet.

1. Zwei Regeln galten in der Übung, ohne dass du sie im Auftrag wiederholt hast. Wo standen sie, und welche der beiden ist eine Sperre?
2. Warum hast du nur zwei Dateien gestagt und das Diff gelesen, bevor du den Commit freigegeben hast?
3. Wie formulierst du eine Korrektur, wenn Claude danebenliegt?

<details><summary>Auflösung</summary>

1. Die Docstring-Regel stand in der CLAUDE.md, die Löschsperre als Deny-Regel in `.claude/settings.json`. Nur die Deny-Regel ist eine Sperre; die CLAUDE.md ist eine Hausordnung, an die sich Claude meist hält.
2. Damit genau das im Commit landet, was zur Änderung gehört. Das Diff vor der Freigabe ist die letzte Stelle, an der du siehst, was gleich in der Historie steht.
3. Du nennst das konkrete Problem und sagst, dass nur das behoben werden soll und sonst nichts geändert wird.

</details>

## Weiterlesen

- [S1.5 · Rechte im Alltag: default und acceptEdits](s1-05-rechte-im-alltag.md)
- [S1.10 · CLAUDE.md: die Hausordnung des Projekts](s1-10-claude-md.md)
- [S1.13 · Vager und präziser Auftrag im Vergleich](s1-13-vager-und-praeziser-auftrag.md)
- [S1.16 · Git in einem Fluss: Branch, Commit, PR](s1-16-git-in-einem-fluss.md)
- [S4.11 · Abschluss: ein kleiner Build](s4-11-abschluss-kleiner-build.md), der Abschluss deines ganzen Pfads
- [X.2 · Mit Claude Code lernen](x-02-lernen-mit-claude-code.md)
