# Vorführen: S1.16 · Git in einem Fluss: Branch, Commit, PR

> Demo und Hinweise für Moderierende zum Kapitel [S1.16 · Git in einem Fluss: Branch, Commit, PR](../../library/s1-16-git-in-einem-fluss.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: der Git-Ablauf

**Ziel:** Einen kompletten Ablauf zeigen, von Branch über Umsetzung, Diff, Tests und Commit bis zu Push und PR, alles in einem Gespräch.

**Vorbereitung**

- Die Demo baut auf dem Ordner `~/cc-workshop/demos/demo-1.2` aus der Vorführung in [S1.10](s1-10-claude-md.md) auf. Er braucht `validators.py` und die Tests aus der Vorführung in [S1.13](s1-13-vager-und-praeziser-auftrag.md); du kannst beides auch frisch anlegen.
- Für Schritt 5: ein Remote für `git push` und eine angemeldete GitHub CLI (`gh auth login` vor dem Workshop).

**Schritt 1: einen Feature-Branch anlegen**

Tippe in Claude Code:

```
What's the current git status?
```

Was passiert: Claude führt `git status` aus und zeigt den aktuellen Stand.

```
Create a new branch called feature/ipv4-validation
```

Was passiert: Claude führt `git checkout -b feature/ipv4-validation` aus und bestätigt.

**Schritt 2: eine Funktion umsetzen**

```
Add a function validate_ip_range(start: str, end: str) -> bool to validators.py.
It should verify that both addresses are valid IPv4 and that start comes before end
numerically. Use the existing validate_ipv4 function for the per-address check.
Add tests for it in the existing test file.
```

Was passiert: Claude liest die bestehende Datei, ergänzt die neue Funktion im selben Stil und schreibt Tests dazu.

**Schritt 3: den Diff prüfen**

```
Show me the full diff before we commit. I want to review the changes.
```

Was passiert: Claude führt `git diff` aus und zeigt die Änderungen.

**Schritt 4: Tests laufen lassen und committen**

```
Run the tests. If they pass, stage everything and commit with message:
"Add IP range validation with tests

Adds validate_ip_range() to validators.py, using existing validate_ipv4()
for per-address validation. Tests cover valid ranges, inverted ranges,
and invalid address inputs."
```

Was passiert: Claude führt die Tests aus, zeigt die Ausgabe, staged und committet mit der vorgegebenen Nachricht.

**Schritt 5: pushen und den PR anlegen**

```
Push this branch and create a GitHub PR with a short description of the validator change and test coverage.
```

Was passiert: Claude führt `git push -u origin feature/ipv4-validation` aus und, wenn `gh` angemeldet ist, `gh pr create --fill` oder einen gleichwertigen PR-Befehl.

**Schritt 6: das Git-Log zeigen**

```
Show me git log --oneline -5
```

Was passiert: Das Log zeigt die letzten Commits, darunter den gerade angelegten.

Schritt 7 (Bonus, wenn Zeit bleibt) legt einen Worktree an; er steht in [S1.18](s1-18-worktrees.md).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten für die ganze Demo, einschließlich des Worktree-Bonus aus [S1.18](s1-18-worktrees.md).

**Sagen:**

- Schritt 1: „Bevor wir irgendetwas anfassen, schauen wir, in welchem Zustand wir sind. Eine gute Gewohnheit, ob in Claude Code oder nicht."
- Schritt 2, während Claude arbeitet: „Claude hat zuerst die bestehende Datei gelesen. Es weiß, dass die vorhandene Funktion da ist, und nutzt sie, statt sie neu zu schreiben. Das ist der Vorteil, wenn Claude Kontext hat: Es baut auf dem auf, was schon da ist."
- Schritt 3: „Immer vor dem Commit prüfen. Das gilt, ob du den Code geschrieben hast oder Claude. Besonders, wenn es Claude war."
- Schritt 4: „Diese Commit-Nachricht ist bereit für einen PR: ein beschreibender Titel, ein kurzer Text zum Warum. Ich habe sie im Prompt vorgegeben, damit ich das Format bestimme. Du kannst Claude die Nachricht auch selbst formulieren lassen; den üblichen Commit-Stil trifft es meist gut."
- Schritt 5: „Das ist die letzte Meile: nicht nur ein lokaler Commit, sondern ein PR, den jemand prüfen kann. Im Alltag entwirft Claude die PR-Beschreibung aus dem Diff; vor dem Merge prüfst du trotzdem selbst."
- Schritt 6: „Branch, Code, Test, Commit. Der ganze Ablauf in einem Gespräch. Kein Wechsel in eine Git-Oberfläche, kein zweites Terminal."
- Zum Schluss: „Branch, umsetzen, testen, committen, Log. Alles im Gespräch. Git wird zu etwas, worüber du nachdenkst, nicht zu etwas, das du von Hand verwaltest." Den Schlusssatz zu Worktrees findest du in [S1.18](../../library/s1-18-worktrees.md).

**Wenn etwas schiefgeht:**

- **`gh pr create` scheitert an der Anmeldung:** Lass den PR-Schritt weg und zeig nur `git push`. Sag dazu: „Für den PR braucht es vor dem Workshop `gh auth login`."
- **`pytest` fehlt:** Als Setup-Problem ansprechen und ohne Testschritt weitermachen, oder `python -m pytest` als Ausweg nehmen.
- **`git status` zeigt unerwartete Dateien:** Nur die Pfade zum Validator gezielt stagen (`git add validators.py tests/`), kein `git add -A`.

</details>
