---
id: S1.16
type: lesson
title: "Git in einem Fluss: Branch, Commit, PR"
shelf: git
level: core
minutes: 18
requires: [S1.5, S1.13]
safety_floor: false
transferable: true
outcome: "Ich kann in einer Claude-Code-Sitzung einen Branch anlegen, eine Änderung umsetzen lassen, den Diff prüfen, die Tests laufen lassen, gezielt committen und einen PR erstellen lassen."
sources:
  - https://code.claude.com/docs/en/common-workflows
aliases: ["1.4"]
---

# S1.16 · Git in einem Fluss: Branch, Commit, PR

<!-- meta:start -->
> **Regal:** [Git & Worktrees](README.md#git) · **Stufe:** Kern · **~18 Min** · **Voraussetzungen:** [S1.5 Rechte im Alltag: default und acceptEdits](s1-05-rechte-im-alltag.md) · [S1.13 Vager und präziser Auftrag im Vergleich](s1-13-vager-und-praeziser-auftrag.md)
>
> ← [S1.15 Output Styles und Personas](s1-15-output-styles.md) · [Bibliothek](README.md) · [S1.17 Git-Befehle in der Sitzung](s1-17-git-befehle.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du schon einmal einen ganzen Ablauf von Branch über Commit bis PR in einer einzigen Claude-Code-Sitzung durchgezogen?
- Kannst du ohne Nachschlagen sagen, an welcher Stelle du den Diff prüfst und wann du Dateien gezielt statt alle stagen lässt?

## Auf einen Blick

Claude Code führt Git-Befehle selbst aus: Branch anlegen, Dateien stagen, committen, pushen und mit `gh` einen Pull Request (PR) erstellen, alles in normaler Sprache in einer Sitzung. Claude übernimmt die Mechanik, an zwei Stellen prüfst du selbst: Du liest den Diff vor dem Commit, und du prüfst den PR vor dem Merge.

Der Ablauf hat feste Kontrollpunkte: erst den Stand prüfen, dann Branch, Änderung, Diff, Tests, Commit, Push und PR. Zeigt `git status` Dateien, die nicht zu deiner Änderung gehören, lässt du gezielt stagen statt alles.

## Bild im Kopf

Stell dir das Schichtbuch einer Leitstelle vor. Jeder Eingriff an einer Anlage bekommt dort einen Eintrag: klein, mit Zeitstempel, nachprüfbar. Ein Commit ist so ein Eintrag. Der Branch ist dein eigener Arbeitsauftrag, auf dem du arbeitest, ohne den laufenden Betrieb zu stören, und der PR ist die Abnahme, bevor die Änderung in den Betrieb geht.

Den Eintrag schreibt hier Claude, aber abzeichnen musst du ihn. Bevor etwas ins Schichtbuch kommt, liest du, was wirklich geändert wurde (den Diff), und du schaust, ob die Tests grün sind.

```mermaid
flowchart LR
  A["Stand prüfen"] --> B["Branch"] --> C["Umsetzen"] --> D["Kontrollpunkt:<br/>Diff prüfen"] --> E["Kontrollpunkt:<br/>Tests"]
  E -- "rot" --> C
  E -- "grün" --> F["Commit"] --> G["Push"] --> H["PR, vor dem Merge<br/>von dir geprüft"]
```

## Im Detail

### Was Claude Code mit Git erledigt

Claude Code hat eine eingebaute Git-Anbindung. Du steuerst die ganze Versionsverwaltung aus der Sitzung heraus: Branches, Commits, Push und Pull Requests, ohne die Sitzung zu verlassen. Claude führt Git-Befehle so selbstverständlich aus, wie es Code schreibt:

- `git status`: zeigt, was sich geändert hat
- `git diff`: zeigt die Änderungen vor dem Commit
- `git add`: staged bestimmte Dateien oder alle Änderungen
- `git commit`: legt Commits mit aussagekräftiger Nachricht an
- `git branch` / `git checkout -b`: legt Branches an und wechselt dorthin
- `git push`: schiebt den Branch zum Remote
- `git log`: zeigt die Commit-Historie
- `gh pr create`: legt einen Pull Request auf GitHub an (braucht die GitHub CLI `gh`)

Das alles verlangst du in normaler Sprache, auch in einem einzigen Prompt:

```
Create a branch called feature/alarm-dedup, implement the deduplication
change we discussed, commit it with a good message, and push it.
```

Claude übernimmt die Git-Mechanik. Du prüfst den Diff und gibst frei; wann Claude dafür um Erlaubnis fragt, regeln die Rechte-Modi aus [S1.5](s1-05-rechte-im-alltag.md). In diesem einen Prompt fehlt allerdings der Halt vor dem Commit, an dem du den Diff liest. Deshalb geht der nächste Abschnitt den Ablauf in Schritten durch.

### Der ganze Ablauf in einem Gespräch

Ein kompletter Durchlauf von der Idee bis zum PR läuft in einer Sitzung. Jeder Schritt ist ein kurzer Auftrag.

**1. Den Stand prüfen, bevor du etwas anfasst**

```
What's the current git status?
```

**2. Kontext geben.** Sag Claude, was du vorhast, und lass es zuerst den bestehenden Code lesen, damit es dem vorhandenen Muster folgt.

**3. Den Branch anlegen**

```
Create a new branch called feature/zone-group-correlation
```

**4. Umsetzen.** Lass die Änderung nach dem vorhandenen Muster umsetzen, mit Tests.

**5. Den Diff prüfen, bevor committet wird**

```
Show me the full diff of what would be committed. I want to review before we commit.
```

**6. Die Tests laufen lassen.** Lass Claude die Tests ausführen und dir die Ergebnisse zeigen.

**7. Stagen und committen**

```
Stage all changed files and commit with message:
"Add zone-group correlation support to alarm correlator"
```

„Stage all" ist nur in Ordnung, wenn `git status` und der Diff ausschließlich deine Änderung zeigen. Liegen dort Dateien, die nicht dazugehören, lass nur die Pfade deiner Änderung stagen, statt `git add -A`. Die Nachricht kannst du wie hier vorgeben oder Claude formulieren lassen; den üblichen Stil für Commit-Nachrichten trifft Claude meist gut. Einen festen Ablauf dafür bietet ein `/commit`-Skill ([S1.17](s1-17-git-befehle.md)).

**8. Pushen und den PR anlegen**

```
Push this branch and create a GitHub PR. Title: "Add zone-group correlation".
Description should explain that this adds support for correlating alarms
by zone group, not just individual zones, and that tests cover the
3 new correlation patterns.
```

Der ganze Ablauf passiert im Gespräch: kein Wechsel ins Terminal, kein Abtippen von Commit-Nachrichten, kein vergessenes `-u origin` beim ersten `git push`. Für den PR braucht Claude eine angemeldete GitHub CLI (`gh auth login`).

## Vorführen

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
- Zum Schluss: „Branch, umsetzen, testen, committen, Log. Alles im Gespräch. Git wird zu etwas, worüber du nachdenkst, nicht zu etwas, das du von Hand verwaltest." Den Schlusssatz zu Worktrees findest du in [S1.18](s1-18-worktrees.md).

**Wenn etwas schiefgeht:**

- **`gh pr create` scheitert an der Anmeldung:** Lass den PR-Schritt weg und zeig nur `git push`. Sag dazu: „Für den PR braucht es vor dem Workshop `gh auth login`."
- **`pytest` fehlt:** Als Setup-Problem ansprechen und ohne Testschritt weitermachen, oder `python -m pytest` als Ausweg nehmen.
- **`git status` zeigt unerwartete Dateien:** Nur die Pfade zum Validator gezielt stagen (`git add validators.py tests/`), kein `git add -A`.

</details>

## Selbst machen

### Aufwärmen: One-Word Diff (2 Minuten, leicht)

**Ziel:** Die Schleife von `diff` zu `commit` an der kleinsten möglichen Änderung üben, bevor die größere Git-Übung kommt.

1. Leg ein Repo mit einer einzeiligen `README.md` an.
2. Ändere genau ein Wort.
3. Sag `Show me git diff`, dann `commit it with a clear message`, dann `git log --oneline`.
4. Erkenntnis: Ein Commit ist nur ein beschrifteter Schnappschuss, klein und billig.

### Übung: der Git-Ablauf mit Claude Code (etwa 18–20 Minuten)

**Ziel:** Einen Durchlauf von Branch über Umsetzung und Commit bis zum Log, nur über das Gespräch mit Claude Code. Keine Git-Befehle von Hand. Das Übungs-Repo hat keinen Remote, deshalb endet die Übung beim Commit und beim Log; den Worktree-Bonus findest du in [S1.18](s1-18-worktrees.md).

**Setup**

Nimm das Projekt aus der Übung in [S1.10](s1-10-claude-md.md) oder leg ein neues an:

```bash
# macOS / Linux / Git Bash
mkdir -p ~/cc-workshop/exercises/exercise-1.4-git && cd ~/cc-workshop/exercises/exercise-1.4-git
git init
echo "# Access Control Utilities" > README.md
git add README.md
git commit -m "Initial commit"
claude
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\cc-workshop\exercises\exercise-1.4-git" | Out-Null
Set-Location "$HOME\cc-workshop\exercises\exercise-1.4-git"
git init
"# Access Control Utilities" | Set-Content -Encoding utf8 README.md
git add README.md
git commit -m "Initial commit"
claude
```

**1. Die Ausgangslage prüfen**

Frag Claude:

```
What is the current git status and which branch are we on?
```

Notier dir die Antwort.

**2. Einen Feature-Branch anlegen**

Frag Claude:

```
Create a new branch called feature/access-log-formatter
```

Prüf, ob er angelegt wurde: „Which branch are we on now?"

**3. Eine kleine Funktion umsetzen**

Frag Claude:

```
Create a file called log_formatter.py with a function format_access_event
that takes a dictionary with keys: timestamp, door_id, event_type, card_id
and returns a formatted string like:
  [2024-03-15 09:42:11] DOOR-03 ACCESS_GRANTED (Card: CARD-1047)

Add a small test in tests/test_log_formatter.py that tests:
- Normal case with all fields present
- Event type ACCESS_DENIED
- Missing card_id (should show "Card: UNKNOWN")
```

**4. Vor dem Commit prüfen**

Frag Claude:

```
Show me the git diff — what has changed since the last commit?
```

Lies den Diff durch. Passen die Änderungen zu dem, was du verlangt hast?

**5. Die Tests laufen lassen**

Frag Claude:

```
Run the tests. Show me the full output.
```

**6. Stagen und committen**

Frag Claude:

<!-- cockpit:example -->
```
Stage all new and changed files. Then commit with this message:
"Add access event log formatter

Formats access control events into human-readable log lines.
Handles missing card_id gracefully. Tests cover normal case,
ACCESS_DENIED events, and missing card scenarios."
```

**7. Den Commit bestätigen**

Frag Claude:

```
Show me git log --oneline -5
```

Ist dein Commit da?

**Geschafft, wenn:**

- [ ] der Branch `feature/access-log-formatter` über Claude Code angelegt wurde
- [ ] `log_formatter.py` und die Tests existieren
- [ ] die Tests grün sind
- [ ] der Commit die vorgegebene Nachricht hat
- [ ] `git log` den Commit auf dem richtigen Branch zeigt

## Typische Fallen

- **Ein Test schlägt fehl.** Bearbeite die Datei nicht selbst. Sag Claude: „Test [name] fails with [error message]. Fix the implementation." Lass Claude reparieren und die Tests erneut laufen.
- **Die Commit-Nachricht stimmt nicht.** Sag: „The commit message is wrong. Amend the last commit with this message: [correct message]"
- **Der PR-Schritt scheitert.** `gh pr create` braucht eine installierte und angemeldete GitHub CLI (`gh auth login`).

## Check

Du kannst einen ganzen Ablauf von Branch über Diff, Tests und Commit bis zum PR in einer Claude-Code-Sitzung führen und weißt, an welchen Stellen du selbst prüfst.

1. In welcher Reihenfolge kommen Diff-Prüfung, Tests und Commit, und warum steht der Diff vor dem Commit?
2. Wann lässt du alle Dateien stagen, und wann nennst du die Pfade einzeln?
3. Was brauchst du, damit Claude einen PR anlegen kann?

<details><summary>Quizfrage</summary>

**Frage:** Claude übernimmt im Ablauf die Git-Mechanik. Welche Schritte bleiben trotzdem bei dir?

- **Richtig:** Den Diff vor dem Commit lesen und den PR vor dem Merge prüfen: Claude tippt die Befehle, abnehmen musst du.
- Falsch: Nur den Branch-Namen festlegen: Diff, Tests, Commit und Merge erledigt Claude danach ohne jede Prüfung durch dich.
- Falsch: Die Commit-Nachricht tippen, denn Claude Code darf Commit-Nachrichten aus Sicherheitsgründen nicht selbst schreiben.
- Falsch: Das Pushen, denn `git push` kann Claude Code nur vorschlagen; ausführen musst du es selbst in deinem Terminal.

</details>

## Weiterlesen

- [Häufige Abläufe: Pull Requests erstellen](https://code.claude.com/docs/en/common-workflows#create-pull-requests)
- [S1.5 · Rechte im Alltag: default und acceptEdits](s1-05-rechte-im-alltag.md)
- [S1.13 · Vager und präziser Auftrag im Vergleich](s1-13-vager-und-praeziser-auftrag.md)
- [S1.17 · Git-Befehle in der Sitzung](s1-17-git-befehle.md)
- [S1.18 · Worktrees als Testlabor](s1-18-worktrees.md)
- [S1.20 · Praxis-Station Session 1: eine Übung wählen](s1-20-praxis-station-1.md)
