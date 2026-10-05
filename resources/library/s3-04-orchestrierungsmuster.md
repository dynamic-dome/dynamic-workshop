---
id: S3.4
type: lesson
title: "Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie"
shelf: agents
level: core
minutes: 15
requires: [S3.1]
safety_floor: false
transferable: true
outcome: "Ich kann bei einer Mehrteil-Aufgabe begründet zwischen Fan-out/Fan-in, Pipeline und Hierarchie wählen und prüfen, ob die Teilaufgaben wirklich unabhängig sind."
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/workflows
aliases: []
---

# S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie

<!-- meta:start -->
> **Regal:** [Agenten & Orchestrierung](README.md#agents) · **Stufe:** Kern · **~15 Min** · **Voraussetzungen:** [S3.1 Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md)
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

**Passt, wenn** jeder Schritt vom vorigen abhängt: Planen, Umsetzen, Testen, Prüfen. In Claude Code bittest du Claude, Subagenten nacheinander einzusetzen. Jeder erledigt seinen Teil und gibt das Ergebnis an Claude zurück, und Claude reicht den relevanten Kontext an den nächsten weiter.

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

### Größer als von Hand: Dynamic Workflows (optional)

Die Muster oben orchestrierst du **von Hand**, mit ein paar delegierten Aufgaben pro Schritt. Neuere Versionen von Claude Code bringen **Dynamic Workflows** mit: ein Skript, das Claude für deinen Auftrag schreibt und das Dutzende bis Hunderte Subagenten pro Lauf koordiniert. Mit `/workflows` beobachtest und verwaltest du diese Läufe. Der Unterschied liegt darin, wer den Plan hält: Bei Subagenten entscheidet Claude Zug um Zug, was als Nächstes läuft, bei einem Workflow das Skript. Nimm die Muster von Hand als Lernmodell und Workflows als dieselbe Idee im großen Maßstab. Ob Workflows auf deiner CLI verfügbar sind, zeigen `/help` und `/release-notes`.

### Schnellstart: Arbeit mit mehreren Agenten auslösen

Sag Claude zum Beispiel:

```text
Analyze this project from two angles simultaneously: one agent maps the architecture, another finds all TODO and FIXME comments. Run them in parallel and give me a combined report.
```

Claude nutzt dafür das Agent-Tool. 🔧 **Custom:** Der Skill `/agent-orchestrator` automatisiert den ganzen Orchestrierungsablauf. Er ist ein eigener Skill der Moderation, nicht Teil von Claude Code.

### `/batch`: Fan-out über Worktrees (Rückblick)

`/batch` kennst du als mitgelieferten Skill aus [S2.4](s2-04-mitgelieferte-skills.md). Er zerlegt eine große Änderung in unabhängige Einheiten und startet je Einheit einen Hintergrund-Subagenten in einem eigenen Worktree. Eine konkrete Anwendung mit mehreren Agenten:

```
/batch migrate src/components/* from Solid to React, one module per worktree
```

Die Gesamtlaufzeit richtet sich nach dem langsamsten Subagenten, nicht nach der Summe. Die Mechanik steht in S2.4; hier ist `/batch` ein Orchestrierungsbaustein unter mehreren.

## Selbst machen

### Übung: deine erste Aufgabe mit mehreren Agenten (etwa 15 Minuten, einzeln)

**Ziel:** Den Unterschied zwischen einer einzelnen Claude-Instanz und mehreren Agenten erleben.

**Aufgabe:** Denk an eine Aufgabe aus deiner Arbeit, die zwei oder drei klar unabhängige Teile hat. Beispiele:

- „Analyze this config file for security issues AND document what each setting does"
- „Find all hardcoded values in this file AND write unit tests for the main functions"
- „Map the directory structure of this project AND list all external dependencies"

Bitte Claude ausdrücklich, für jeden Teil **getrennte Agenten parallel** einzusetzen:

<!-- cockpit:example -->
```text
Use separate agents running in parallel for each part.
Part 1: [describe Part 1]
Part 2: [describe Part 2]
Report the results together.
```

**Worauf du achtest:**

- die zwei Agenten, die in der Ausgabe erscheinen
- jeder Agent hat seinen eigenen Kontext und weiß nicht, was der andere tut
- der Orchestrator führt die Ergebnisse zusammen
- die Gesamtzeit im Vergleich dazu, wie lange es nacheinander gedauert hätte

**Geschafft, wenn:**

- [ ] du in der Ausgabe mindestens zwei getrennte Agenten-Ergebnisse zeigen kannst
- [ ] jeder Agent eine eigene, unabhängige Aufgabe hatte, die nicht vom Ergebnis des anderen abhing
- [ ] die Schlussantwort beide Ergebnisse zu einem Bericht zusammenführt
- [ ] du eine echte Arbeitsaufgabe nennen kannst, bei der Fan-out sicher ist, und eine, bei der eine Pipeline sicherer wäre

**Zum Nachdenken:**

1. Waren die Aufgaben wirklich unabhängig? Mussten sich die Agenten abstimmen?
2. Hat das parallele Arbeiten Probleme verursacht?
3. Wo in deiner Arbeit könntest du dieses Muster einsetzen?

### Extra: Alarmsturm-Korrelator (etwa 25 Minuten, mittel)

**Ziel:** Echtes Fan-out auf unabhängige Datenteile und danach ein Korrelationsschritt, der zeigt, wo Fan-out endet und Zusammenführung beginnt.

**Analogie:** Bei einem Alarmsturm decken drei Streifen drei Zonen parallel ab; die Leitstelle führt die Berichte zusammen.

1. Leg drei kleine Logs an, `door_events.log`, `motion_sensors.log` und `card_reader.log`, mit Zeitstempeln. Ein einzelner Vorfall (Tür um 02:14 aufgebrochen) ist über alle drei verteilt.
2. Fächere ausdrücklich auf: `Use three parallel agents. Agent 1 summarizes door_events.log, Agent 2 motion_sensors.log, Agent 3 card_reader.log. Each sees only its file.`
3. Beachte: Jeder Agent hat seinen eigenen Kontext, keiner sieht die Logs der anderen.
4. Korreliere im Orchestrator: `Merge the three reports into one timeline. Is there an event that appears in all three?`
5. Aha: Erst die Zusammenführung zeigt den koordinierten Vorfall, den kein einzelner Agent sehen konnte. Besprich: Wann ist eine Aufgabe Fan-out, wann Pipeline?

Eine domänennahe Übung mit Parser, Tests und Sicherheitsprüfung (OSDP/Wiegand) findest du in [S3.6](s3-06-devils-advocate.md).

## Typische Fallen

- **Scheinbar unabhängig.** Die Aufgaben müssen wirklich unabhängig sein. Braucht Agent 2 das Ergebnis von Agent 1, ist es eine Pipeline, kein Fan-out.
- **Vage Teilaufträge.** Vage Aufgaben liefern vage Ergebnisse. Halte jeden Teil fokussiert.
- **Gleich zu groß anfangen.** Fang klein an: Zwei Agenten reichen, um das Muster zu sehen.
- **Claude erledigt alles selbst.** Ohne ausdrückliche Bitte arbeitet Claude die Teile womöglich nacheinander ab. Schreib „separate agents running in parallel" in den Auftrag.

## Check

Du kannst zu einer beschriebenen Aufgabe mit mehreren Agenten das passende Muster wählen, für Fan-out den Zeitgewinn gegenüber dem Nacheinander abschätzen und begründen, warum die Teile dafür unabhängig sein müssen.

1. Woran erkennst du, dass eine Aufgabe eine Pipeline ist und kein Fan-out?
2. Wovon hängt die Gesamtlaufzeit beim Fan-out ab?
3. Wann lohnt sich eine Hierarchie?

<details><summary>Quizfrage</summary>

**Frage:** Fünf unabhängige Firmware-Module sollen auf Speichersicherheitslücken gescannt werden, jeder Scan dauert 90 Sekunden. Welches Muster passt, und wie lange dauert es ungefähr?

- **Richtig:** Fan-out/Fan-in: fünf Scanner parallel, der Orchestrator führt zusammen; etwa 90 s statt 450 s.
- Falsch: Pipeline: Jeder Scanner baut auf dem vorigen auf und reicht Modulwissen weiter; etwa 450 s insgesamt.
- Falsch: Hierarchie: Fünf parallele Agenten brauchen immer Unter-Orchestratoren gegen Schreibkonflikte.
- Falsch: Nacheinander: Parallele Agenten teilen sich ein Kontextfenster und blockieren sich gegenseitig.

</details>

## Weiterlesen

- [Subagents: häufige Muster (offizielle Doku)](https://code.claude.com/docs/en/sub-agents#common-patterns)
- [Dynamic Workflows (offizielle Doku)](https://code.claude.com/docs/en/workflows)
- [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md)
- [S3.5 · Hintergrund-Sitzungen und Agent Teams](s3-05-hintergrund-und-teams.md)
- [S2.4 · Mitgelieferte Skills](s2-04-mitgelieferte-skills.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S4.1 · Das richtige Modell pro Phase](s4-01-modell-pro-phase.md)
