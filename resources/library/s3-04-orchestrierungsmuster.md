---
id: S3.4
type: lesson
title: "Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie"
shelf: agents
level: core
minutes: 25
requires: [S3.1]
safety_floor: false
transferable: true
outcome: "Ich kann bei einer Mehrteil-Aufgabe begründet zwischen Fan-out/Fan-in, Pipeline und Hierarchie wählen, prüfen, ob die Teilaufgaben wirklich unabhängig sind, und an den Aufträgen der Subagenten ablesen, ob eine Abhängigkeit bestand."
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/workflows
aliases: []
---

# S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie

<!-- meta:start -->
> **Regal:** [Agenten & Orchestrierung](README.md#agents) · **Stufe:** Kern · **~25 Min** · **Voraussetzungen:** [S3.1 Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md)
>
> ← [S3.3 Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md) · [Bibliothek](README.md) · [S3.5 Hintergrund-Sitzungen und Agent Teams](s3-05-hintergrund-und-teams.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du schon einmal zwei unabhängige Teilaufgaben parallel an getrennte Agenten gegeben und die Ergebnisse zusammenführen lassen?
- Kannst du ohne Nachschlagen sagen, woran du erkennst, dass eine Aufgabe eine Pipeline ist und kein Fan-out?

## Auf einen Blick

Drei Muster decken die meisten Aufgaben mit mehreren Agenten ab. Fan-out/Fan-in startet unabhängige Agenten parallel und führt ihre Ergebnisse zusammen; eine Pipeline reicht das Ergebnis eines Agenten an den nächsten weiter, weil jeder Schritt den vorigen braucht; eine Hierarchie schachtelt Unter-Orchestratoren für Aufgaben, die sich auf mehreren Ebenen zerlegen lassen. Die wichtigste Prüfung vor jedem Fan-out: Sind die Teile wirklich unabhängig?

## Bild im Kopf

Fan-out ist die Leitstelle, die zwei Sicherheitsteams gleichzeitig losschickt, um zwei Etagen abzusuchen. Das eine Team nimmt den Grundriss auf, das andere sucht nach Gefahren. Beide melden unabhängig zurück, und die Leitstelle hat beide Berichte, ohne dass einer auf den anderen gewartet hat. Eine Pipeline ist der Zutrittsablauf: Karte lesen, Berechtigung prüfen, Tür freigeben, Ereignis protokollieren; jeder Schritt braucht das Ergebnis des vorigen. Eine Hierarchie ist die Alarmzentrale mit Bereichszentralen: Die Hauptleitstelle koordiniert die Bereiche, jeder Bereich seine eigenen Melder.

## Im Detail

### Muster 1: Fan-out / Fan-in

N Agenten parallel starten, alle Ergebnisse einsammeln, zusammenführen.

```
Orchestrator
  |-> Agent A (Task 1) -> Result A -+
  |-> Agent B (Task 2) -> Result B -+-> Synthesize -> Final Output
  `-> Agent C (Task 3) -> Result C -+
```

**Passt, wenn** die Aufgaben unabhängig sind: drei Module analysieren, fünf Dateien gleichzeitig scannen.

**Zeitgewinn, als Rechenbeispiel:** Jede Teilaufgabe dauert 60 Sekunden. Nacheinander sind das 180 Sekunden, parallel im günstigsten Fall etwa 60, also die Dauer des langsamsten Agenten. Tokens sparst du dabei nicht: Jeder Agent verbraucht seine eigenen.

### Muster 2: Pipeline (nacheinander)

Die Ausgabe von Agent A wird zur Eingabe von Agent B.

```
Orchestrator -> Agent A (Explore) -> Agent B (Review) -> Agent C (Fix)
```

**Passt, wenn** jeder Schritt vom vorigen abhängt: Planen, Umsetzen, Testen, Prüfen. In Claude Code bittest du Claude, Subagenten nacheinander einzusetzen. Jeder erledigt seinen Teil und gibt das Ergebnis an Claude zurück, und Claude reicht den relevanten Kontext an den nächsten weiter. Woran du die Abhängigkeit erkennst: Der Auftrag für Agent B enthält etwas, das Claude erst nach Agent A wissen konnte.

### Muster 3: Hierarchie

Ein Orchestrator startet Unter-Orchestratoren, die jeweils eigene Agenten führen.

```
Master Orchestrator
  |-> Sub-Orchestrator 1 (Security)
  |     |-> Scanner Agent
  |     `-> Validator Agent
  `-> Sub-Orchestrator 2 (Quality)
        |-> Reviewer Agent
        `-> Test Writer Agent
```

**Passt, wenn** sich das Problem auf mehreren Ebenen zerlegen lässt, etwa in großen Codebasen. Claude Code kann das von Haus aus: Ein Subagent darf eigene Subagenten starten, standardmäßig bis zu drei Ebenen unter dem Hauptgespräch. In einer interaktiven Sitzung kommt zu dir nur die Zusammenfassung der obersten Ebene zurück.

### `/batch`: Fan-out über Worktrees (Rückblick)

`/batch` kennst du als mitgelieferten Skill aus [S2.4](s2-04-mitgelieferte-skills.md). Er zerlegt eine große Änderung in unabhängige Einheiten und startet je Einheit einen Hintergrund-Subagenten in einem eigenen Worktree. Eine konkrete Anwendung mit mehreren Agenten:

```
/batch migrate src/components/* from Solid to React, one module per worktree
```

Die Gesamtlaufzeit richtet sich nach dem langsamsten Subagenten, nicht nach der Summe. Die Mechanik steht in S2.4; hier ist `/batch` ein Orchestrierungsbaustein unter mehreren.

### Größer als von Hand: Dynamic Workflows (optional, mit Kosten)

Die Muster oben orchestrierst du **von Hand**, mit ein paar delegierten Aufgaben pro Schritt. Neuere Versionen von Claude Code bringen **Dynamic Workflows** mit: ein Skript, das Claude für deinen Auftrag schreibt und das Dutzende bis Hunderte Subagenten pro Lauf koordiniert. Mit `/workflows` beobachtest und verwaltest du diese Läufe. Der Unterschied liegt darin, wer den Plan hält: Bei Subagenten entscheidet Claude Zug um Zug, was als Nächstes läuft, bei einem Workflow das Skript.

Das hat seinen Preis. Laut Doku kann ein einzelner Lauf deutlich mehr Tokens verbrauchen als dieselbe Aufgabe im Gespräch, und die Läufe zählen auf die Nutzungsgrenzen deines Plans. Probier einen Workflow zuerst an einem kleinen Ausschnitt aus, etwa einem Ordner statt dem ganzen Repo. Ob Workflows auf deiner CLI verfügbar sind, zeigen `/help` und `/release-notes`.

## Selbst machen

### Übung: Fan-out und Pipeline an einem kleinen Projekt (etwa 15 Minuten)

**Ziel:** Du lässt zwei unabhängige Aufgaben parallel laufen und danach zwei abhängige nacheinander, und du erkennst den Unterschied an den Aufträgen, die Claude den Subagenten gibt.

**Startzustand:** ein neuer Ordner `~/cc-workshop/muster` (`mkdir -p ~/cc-workshop/muster && cd ~/cc-workshop/muster`, in PowerShell `New-Item -ItemType Directory -Force "$HOME\cc-workshop\muster"; Set-Location "$HOME\cc-workshop\muster"`) mit drei Dateien, die du mit einem Editor anlegst. Die Inhalte stehen hier, du musst nichts erfinden. Das Beispiel stammt aus der Zutrittstechnik; es zählt nur, dass die Dateien genau so aussehen.

`access.log`:

```text
2026-10-01 08:02 card=C-104 door=lobby result=GRANTED
2026-10-01 08:05 card=C-231 door=server result=DENIED
2026-10-01 08:06 card=C-231 door=server result=DENIED
2026-10-01 09:14 card=C-117 door=lab result=GRANTED
2026-10-01 09:15 card=C-231 door=lab result=DENIED
2026-10-01 10:40 card=C-104 door=server result=DENIED
2026-10-01 11:02 card=C-117 door=lobby result=GRANTED
2026-10-01 11:30 card=C-231 door=server result=DENIED
```

`cards.csv`:

```text
card,owner,status
C-104,M. Weber,active
C-117,S. Koch,active
C-231,T. Brandt,blocked
```

`reader.py`:

```python
def read_card(raw):
    # TODO: check the length of raw
    return raw.strip()


def open_door(card):
    # TODO: ask the controller before opening
    return True


def log_result(card, granted):
    # FIXME: write to access.log instead of printing
    print(card, granted)
```

Starte `claude --permission-mode default` im Ordner und bestätige den Vertrauensdialog.

**Teil A: Fan-out.**

1. Gib diesen Auftrag ein:

   <!-- cockpit:example -->
   ```text
   Use two separate subagents running in parallel. Subagent 1 reads access.log and reports how many lines contain DENIED. Subagent 2 reads reader.py and lists every TODO and FIXME comment with its line number. Then give me both results in one short report.
   ```

   Erwartet: Zwei Subagenten laufen, und der Bericht nennt 5 `DENIED`-Zeilen und die Kommentare in den Zeilen 2, 7 und 12. Mit `Ctrl+O` siehst du im Transkript zwei Delegationen, bevor der Bericht kommt; schließ die Ansicht mit `Ctrl+O`.
2. Prüf die Aufträge:

   ```text
   Show me, word for word, the task text you gave each of the two subagents.
   ```

   Erwartet: zwei Texte. Keiner verweist auf das Ergebnis des anderen, jede Aufgabe ließ sich allein lösen.

**Teil B: Pipeline.**

3. Gib diesen Auftrag ein:

   ```text
   Use subagents one after the other. First, a subagent finds the card id with the most DENIED lines in access.log. Then a second subagent, to which you pass that card id, looks it up in cards.csv and reports the owner and the status. Do not start the second subagent before the first one has answered.
   ```

   Erwartet: Der erste Subagent nennt `C-231` (4 von 5 abgelehnten Zugriffen), der zweite meldet T. Brandt mit Status `blocked`. Im Transkript erscheint die zweite Delegation erst, nachdem die erste fertig ist.
4. Prüf den zweiten Auftrag:

   ```text
   Show me, word for word, the task text you gave the second subagent.
   ```

   Erwartet: Der Text enthält `C-231`.

**Aufräumen:** Beende die Sitzung mit `/exit` und lösch den Ordner `~/cc-workshop/muster` selbst.

<details><summary>Vergleich</summary>

Die Karten-ID in Schritt 4 konnte Claude erst schreiben, nachdem der erste Subagent geantwortet hatte. Das ist die Abhängigkeit, und deshalb war Teil B eine Pipeline. Hätte Claude beide Subagenten gleichzeitig gestartet, hätte der zweite die Karte raten müssen. In Teil A stand in keinem Auftrag etwas, das erst ein anderer Subagent herausfinden musste.

</details>

**Geschafft, wenn:**

- [ ] du in Teil A zwei Delegationen im Transkript gesehen hast und der Bericht beide Ergebnisse enthielt
- [ ] keiner der beiden Aufträge aus Teil A auf das Ergebnis des anderen verwies
- [ ] der zweite Auftrag aus Teil B `C-231` enthielt
- [ ] du in einem Satz sagen kannst, warum Teil B kein Fan-out sein konnte

## Typische Fallen

- **Scheinbar unabhängig.** Die Aufgaben müssen wirklich unabhängig sein. Braucht Agent 2 das Ergebnis von Agent 1, ist es eine Pipeline, kein Fan-out. Lies im Zweifel die Aufträge nach, wie in der Übung.
- **Vage Teilaufträge.** Vage Aufgaben liefern vage Ergebnisse. Halte jeden Teil fokussiert.
- **Gleich zu groß anfangen.** Fang klein an: Zwei Agenten reichen, um das Muster zu sehen.
- **Claude erledigt alles selbst.** Ohne ausdrückliche Bitte arbeitet Claude die Teile womöglich nacheinander selbst ab. Schreib „separate subagents running in parallel“ in den Auftrag.

## Check

Du kannst zu einer beschriebenen Aufgabe mit mehreren Agenten das passende Muster wählen, für Fan-out den Zeitgewinn gegenüber dem Nacheinander abschätzen und begründen, warum die Teile dafür unabhängig sein müssen.

1. Woran erkennst du, dass eine Aufgabe eine Pipeline ist und kein Fan-out?
2. Wovon hängt die Gesamtlaufzeit beim Fan-out ab?
3. Wann lohnt sich eine Hierarchie?

<details><summary>Auflösung</summary>

1. Der Auftrag für einen späteren Agenten enthält etwas, das erst ein früherer herausfinden muss: Jeder Schritt braucht das Ergebnis des vorigen.
2. Vom langsamsten Agenten, nicht von der Summe aller Laufzeiten. Tokens sparst du dabei nicht.
3. Wenn sich das Problem auf mehreren Ebenen zerlegen lässt, etwa in großen Codebasen; ein Subagent darf dann eigene Subagenten starten, standardmäßig bis zu drei Ebenen tief.

</details>

<details><summary>Quizfrage</summary>

**Frage:** Du willst `reader.py` verbessern lassen: Agent 1 listet alle Funktionen ohne Prüfung der Eingabe, Agent 2 schreibt Tests für genau diese Funktionen. Welches Muster passt?

- **Richtig:** Pipeline: Agent 2 braucht die Liste von Agent 1, und liefe er parallel, müsste er die Funktionen raten.
- Falsch: Fan-out/Fan-in: Beide Agenten lesen dieselbe Datei, also sind ihre Teilaufgaben unabhängig und laufen gleichzeitig.
- Falsch: Hierarchie: Zwei zusammenarbeitende Agenten brauchen einen Unter-Orchestrator, der ihre Ergebnisse laufend abgleicht.
- Falsch: Fan-out/Fan-in: Parallel ist schneller, also starten beide gleichzeitig und Claude gleicht die Ergebnisse nachher ab.

</details>

## Weiterlesen

- [Subagents: häufige Muster (offizielle Doku)](https://code.claude.com/docs/en/sub-agents#common-patterns)
- [Dynamic Workflows (offizielle Doku)](https://code.claude.com/docs/en/workflows)
- [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md)
- [S3.3 · Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md)
- [S3.5 · Hintergrund-Sitzungen und Agent Teams](s3-05-hintergrund-und-teams.md)
- [S2.4 · Mitgelieferte Skills](s2-04-mitgelieferte-skills.md)
- [S4.1 · Das richtige Modell pro Phase](s4-01-modell-pro-phase.md)
