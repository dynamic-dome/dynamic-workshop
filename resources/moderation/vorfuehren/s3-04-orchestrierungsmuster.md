# Vorführen: S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie

> Demo und Hinweise für Moderierende zum Kapitel [S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](../../library/s3-04-orchestrierungsmuster.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Zwei Agenten parallel

**Ziel:** Zeigen, dass zwei Agenten gleichzeitig an unabhängigen Aufgaben arbeiten.

**Vorbereitung:** Ein mittelgroßes Projekt ist offen, das Workshop-Demo-Projekt oder eine echte Codebasis mit mehr als zehn Dateien.

**Schritt 1: Claude aus zwei Blickwinkeln parallel analysieren lassen**

Tipp den Auftrag sichtbar ein, damit alle den Prompt sehen:

```text
Analyze this project using two separate agents running in parallel:
Agent 1 maps the overall architecture — directory structure, key files, main entry points, technology stack.
Agent 2 scans for all TODO, FIXME, HACK, and XXX comments and lists them with file and line number.
Run both agents simultaneously and give me a combined report.
```

Achte darauf, wie die beiden Agenten in der Ausgabe erscheinen. Zeig, dass beide gleichzeitig laufen und nicht aufeinander warten.

**Schritt 2: 🔧 `/agent-orchestrator` für Arbeit mit mehreren Modellen**

```
/agent-orchestrator
```

Wähle Haiku für das Brainstorming und Sonnet für die Analyse. Auftrag: „Generate 5 architectural improvement ideas for this project, then evaluate each one for feasibility and impact." Zeig, wie Haiku schnell und günstig Ideen liefert und Sonnet sie gründlicher bewertet.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten geplant; reserviere live etwa 12 Minuten (× 1,5), falls die Ausgaben der Agenten lang werden.

**Sagen:**

- „Wir haben gerade zwei Sicherheitsteams losgeschickt, die gleichzeitig verschiedene Etagen absuchen. Das eine nimmt den Grundriss auf, das andere sucht nach Gefahren. Beide melden unabhängig zurück; wir bekommen beide Berichte parallel, nicht nacheinander. Genau so arbeitet eine gut geführte Leitstelle."

**Wenn etwas schiefgeht:**

- **Claude startet keine Subagenten und antwortet nacheinander:** Fordere neu auf: „Use SEPARATE agents running IN PARALLEL for each part. This is important — I want to see Agent 1 and Agent 2 outputs separately."
- **Nur ein Agent startet:** Die Aufgaben sind vielleicht nicht wirklich unabhängig. Formuliere sie klar unabhängig: kein gemeinsamer Zustand, keine Reihenfolge.
- **Die Ausgabe ist live zu lang zum Mitlesen:** Kündige an, was ungefähr kommt („ihr werdet gleich so etwas sehen …"), und überfliege die Ausgaben.
- **`/agent-orchestrator` ist nicht installiert:** Lass Schritt 2 weg und erzähl das Muster: „Mit dem Orchestrator-Plugin könntet ihr jedem Agenten ein anderes Modell zuweisen. Heute haben wir parallele Agenten mit demselben Modell."

</details>
