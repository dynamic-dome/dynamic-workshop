# Workshop Guide

## Worum es in diesem Workshop geht

Der Workshop fuehrt in Claude Code ein, aber nicht aus Sicht eines Anfaengers im Programmieren. Die Zielgruppe kann entwickeln, testen, debuggen und mit Git arbeiten. Neu ist hier vor allem die Arbeitsweise mit einem Coding Agent: also wie man einem Tool Aufgaben gibt, wie man Kontext steuert, wie man Guardrails setzt und wie man aus einzelnen Prompts reproduzierbare Arbeitsablaeufe macht.

Kurz gesagt:

- Block 1 erklaert das Grundmodell.
- Block 2 zeigt, wie man das Tool erweitert und kontrolliert.
- Block 3 zeigt fortgeschrittene Arbeitsweisen mit Agents, Automatisierung und Security.

## Wie der Workshop aufgebaut ist

Der Workshop besteht aus drei Sessions mit insgesamt 14 Modulen (Block 1: 4, Block 2: 5, Block 3: 5):

- Block 1: Foundations
  Was Claude Code ist, wie Kontext funktioniert, wie gutes Prompting aussieht und wie Git/Worktrees in den Workflow passen.
- Block 2: Ecosystem
  Wie Skills, Commands, Hooks, Plugins, MCP und Knowledge-Workflows zusammenspielen.
- Block 3: Advanced
  Wie man Agents, Multi-Agent-Muster, Security-Pruefungen und Automatisierung sinnvoll einsetzt.

Jeder Block folgt demselben didaktischen Muster:

1. Konzept verstehen
2. Live-Demo sehen
3. selbst ausprobieren
4. mit Cheat Sheet und Rueckfragen absichern

Das ist wichtig, weil der Workshop nicht nur erklaeren will, was Claude Code kann, sondern wie man daraus eine verlaessliche Arbeitsweise macht.

## Welche Dateien welche Rolle spielen

Wenn du den Workshop selbst durcharbeiten willst, sind diese Dateien die Hauptnavigation:

- `prerequisites.md`
  Erst lesen. Ohne funktionierendes Setup sind viele Demos und Exercises nur Theorie.
- `session-plan.md`
  Gibt den roten Faden ueber alle Sessions.
- `modules/block-*.md`
  Das sind die eigentlichen Lehrinhalte pro Block.
- `demos/block-*.md`
  Zeigt, was praktisch vorgefuehrt werden soll.
- `exercises/block-*.md`
  Dient zum Selbermachen und Festigen.
- `cheatsheet.md`
  Schnelle Referenz waehrend und nach dem Durcharbeiten.

## Empfohlener Lernpfad fuer Selbststudium

Wenn du keine Vorerfahrung mit Coding Agents hast, arbeite nicht querbeet, sondern in dieser Reihenfolge:

1. `resources/prerequisites.md`
   Stelle sicher, dass Claude Code, Git und Python funktionieren.
2. `resources/session-plan.md`
   Verstehe erst den Gesamtaufbau.
3. `resources/modules/block-1-foundations.md`
   Block 1 ist Pflicht. Ohne diesen Teil wirken die spaeteren Komponenten schnell wie Einzeltricks.
4. `resources/demos/block-1-demos.md`
   Schau dir an, wie die Konzepte praktisch vorgefuehrt werden.
5. `resources/exercises/block-1-exercises.md`
   Uebungen wirklich ausprobieren, nicht nur lesen.
6. Danach dasselbe Schema fuer Block 2 und Block 3 wiederholen.

Ein guter Minimalpfad ist:

- Block 1 komplett
- aus Block 2 mindestens Skills, Hooks und MCP
- aus Block 3 mindestens Agents und Security

## Wie das Vorgehen im Workshop gedacht ist

Der Workshop ist nicht so gebaut, dass man alles auswendig lernen soll. Er ist eher eine Einfuehrung in Denk- und Arbeitsmuster:

- Claude Code ist nicht einfach "ein besserer Chat".
  Es ist ein Arbeitswerkzeug mit Tools, Dateizugriff, Shell-Zugriff und Kontextverwaltung.
- Gute Ergebnisse kommen nicht nur vom Modell.
  Sie kommen aus sauberem Kontext, praezisen Aufgaben und guten Schutzmechanismen.
- Wiederverwendbarkeit ist ein Kernthema.
  Deshalb spielen Skills, Commands, Hooks und strukturierte Projektregeln eine grosse Rolle.
- Sicherheit ist nicht Beiwerk.
  Im Workshop wird mehrfach betont, dass Permissions, Hooks, Worktrees und Scoping zum normalen Arbeiten gehoeren.

Die Inhalte sind daher absichtlich von "einfach und direkt" zu "strukturierter und automatisierter" aufgebaut.

## Pflicht, optional, fortgeschritten

Fuer jemanden ohne Agent-Erfahrung ist diese Trennung sinnvoll:

- Pflicht:
  Setup, Grundkonzept, Kontext/Memory, Prompting, Git/Worktrees
- Sehr empfehlenswert:
  Skills, Commands, Hooks, MCP
- Fortgeschritten:
  Custom Agents, Multi-Agent-Orchestrierung, Self-Improve-Loops, komplexere Security-/Automation-Muster

Wenn du allein lernst, ist es voellig in Ordnung, Block 3 zunaechst nur orientierend zu lesen und spaeter praktisch zu vertiefen.

## Was Claude-Code-spezifisch ist und was allgemeiner gilt

Claude-Code-spezifisch sind zum Beispiel:

- die konkrete CLI-Nutzung
- Slash-Commands wie `/workshop`
- das Plugin-Layout in diesem Repository
- bestimmte Bedienkonzepte aus Claude Code

Allgemein auf andere Coding Agents uebertragbar sind:

- gutes Task-Framing
- Kontext klein und relevant halten
- Regeln und Guardrails explizit machen
- Aufgaben in reproduzierbare Workflows ueberfuehren
- Spezialisierung ueber Skills, Rollen oder Teilagenten

Das hilft beim Einordnen: Auch wenn der Workshop klar auf Claude Code fokussiert ist, lernst du hier viele Muster, die spaeter auch mit anderen Agenten nuetzlich sind.

## Wie du die workshop-spezifischen Extras nutzen solltest

Die Spezialkomponenten in `commands/`, `skills/`, `agents/` und `.claude-plugin/` sind Hilfsmittel fuer den Workshop selbst. Sie ersetzen nicht das eigentliche Material in `resources/`, sondern machen es leichter zugaenglich.

Empfehlung:

- Erst die Struktur des Workshops verstehen
- Dann die Specials gezielt nutzen
- Nicht mit dem Agent oder dem Command starten, bevor die Blocklogik klar ist

Die Details dazu stehen in `resources/workshop-specials.md`.

## Praktische Arbeitsweise fuer Selbstlerner

Eine gute Routine fuer einen Lernabend sieht so aus:

1. Ein Modul oder einen Block auswaehlen
2. Erst das Modul lesen
3. Danach die Demo nachvollziehen
4. Danach genau eine Uebung selbst umsetzen
5. Zum Schluss die wichtigsten Punkte mit `cheatsheet.md` gegenpruefen

Wenn du dabei festhaengst, ist das kein Zeichen, dass der Workshop schlecht strukturiert ist. Meistens fehlt dann entweder praktischer Claude-Code-Kontext oder die Uebung wurde ohne den vorigen Block begonnen.

## Fazit

Aus Sicht eines Entwicklers ohne Agent-Erfahrung ist der Workshop stark inhaltlich, aber nicht vollstaendig selbsterklaerend, wenn man nur die Dateien anliest. Genau dafuer ist dieses Guide-Dokument da: Es uebersetzt die vorhandenen Bausteine in eine klare Lernreihenfolge und macht sichtbar, was Kerninhalt, was Werkzeug und was Zusatzmaterial ist.

