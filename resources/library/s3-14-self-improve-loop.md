---
id: S3.14
type: lesson
title: "Self-Improve-Loop: was geht und wo es endet"
shelf: automation
level: bonus
minutes: 15
requires: [S3.13]
safety_floor: false
transferable: true
outcome: "Ich kann die sechs Schritte eines Self-Improve-Loops mit Quality Gate erklären und seine Grenzen benennen: Kostenlauf, Schein-Fixes durch entfernte Assertions, Memory-Drift und regulierte Hardware."
sources:
  - https://code.claude.com/docs/en/cli-reference
  - https://code.claude.com/docs/en/hooks-guide
aliases: []
---

# S3.14 · Self-Improve-Loop: was geht und wo es endet

<!-- meta:start -->
> **Regal:** [Automation & Loops](README.md#automation) · **Stufe:** Kür · **~15 Min** · **Voraussetzungen:** [S3.13 Autonome Loops absichern: Budget und Worktree](s3-13-autonome-loops-absichern.md)
>
> ← [S3.13 Autonome Loops absichern: Budget und Worktree](s3-13-autonome-loops-absichern.md) · [Bibliothek](README.md) · [S3.15 Praxis-Station Session 3: eine Übung wählen](s3-15-praxis-station-3.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du schon einmal einen autonomen Verbesserungs-Loop mit Quality Gate und Iterationsgrenze laufen lassen und danach die Commits selbst geprüft?
- Kannst du ohne Nachschlagen sagen, woran du einen Schein-Fix erkennst, bei dem ein Test nur grün wird, weil die Assertion fehlt?

## Auf einen Blick

Ein Self-Improve-Loop sucht die größte Schwäche eines Projekts, plant einen gezielten Fix, schreibt zuerst einen fehlschlagenden Test, setzt um und committet nur, wenn ein Quality Gate grün ist; dann beginnt die nächste Runde. Gezeigt wird das Muster am 🔧 Custom-Plugin `agentic-os`, nicht an einer Funktion von Claude Code. Es ist ein Experiment, das nur mit Budget-Grenze, Quality Gate und Iterationslimit taugt, denn ein grünes Gate beweist nicht, dass ein Fix echt ist.

## Bild im Kopf

Stell dir ein Intrusion-Detection-System vor, das seine Signaturen selbst aktualisiert. Es erkennt ein neues Angriffsmuster (Analyse), plant eine Gegenregel (Planung), testet sie im Sandbox-Modus ohne Wirkung auf den Betrieb (TDD), prüft, dass keine Fehlalarme entstehen (Quality Gate), und schreibt die Signatur in die Live-Datenbank (Commit). Gefährlich wird es, wenn das System lernt, Fehlalarme zu unterdrücken, statt seine Signaturen zu verbessern: Das ist der Schein-Fix in Reinform.

```mermaid
flowchart LR
  A["Analyse"] --> P["Planung"]
  P --> T["TDD: erst der<br/>fehlschlagende Test"]
  T --> Q{"Quality Gate<br/>grün?"}
  Q -- "ja" --> C["Commit mit<br/>Iterationsprotokoll"]
  Q -- "nein" --> V["Iteration verwerfen"]
  C --> N["nächste Runde"]
  N --> A
  G["Grenzen: Budget,<br/>Max-Iterationen, Review-Gate"] -.-> N
```

## Im Detail

### Der Zyklus

> 🔧 **Custom-Komponente:** `agentic-os` ist ein eigenes Plugin, kein Teil von Claude Code. Stand 2026-09-30 gibt es den Befehl `/agentic-os:run-loop` in der installierten Fassung des Plugins (5.1.4) nicht mehr: Er wurde mit v4.0.0 entfernt, der Self-Improve-Skill mit v5.0.0 archiviert. Das Muster bleibt lehrreich; vorführen lässt es sich damit nur noch als Aufzeichnung.

Der Skill `/agentic-os:run-loop` setzte **autonome Verbesserungszyklen** um. Jede Iteration:

1. **Analyse:** liest Qualitätsmetriken, Testfehler, Review-Befunde und die bisherigen Iterationen
2. **Planung:** entwirft einen gezielten Fix für die Schwäche mit der größten Wirkung
3. **TDD-Umsetzung:** schreibt zuerst einen fehlschlagenden Test, dann den Code, der ihn bestehen lässt
4. **Quality Gate:** Tests grün? Qualität über der Schwelle? Keine Regressionen?
5. **Commit (nur wenn das Gate grün ist):** Git-Commit mit ausführlichem Iterationsprotokoll
6. **Wiederholen:** Die nächste Iteration startet mit dem aktualisierten Stand.

### Sicherheitsmechanismen

| Mechanismus | Was er tut |
|---|---|
| Quality Gates | verweigern den Commit, wenn Tests scheitern oder die Qualität sinkt |
| Git-Historie | Jede Iteration ist ein Commit, den du zurücknehmen kannst. |
| Hooks | blocken bestimmte gefährliche Operationen ([S2.8](s2-08-hook-einrichten.md)) |
| Menschliche Review-Gates | halten an und warten auf Freigabe, bevor committet wird |
| Max-Iterationen | begrenzen autonome Läufe pro Sitzung |

Von außen kommt die Budget-Grenze dazu ([S3.13](s3-13-autonome-loops-absichern.md)).

### Was das Gedächtnis mitschreibt

Das Gedächtnissystem von Agentic OS hält alles fest:

- `.agent-memory/iterations/`: vollständiges Protokoll jeder Änderung und Entscheidung
- `.agent-memory/quality/`: Qualitätswerte über die Zeit
- `.agent-memory/learnings/`: Muster, die über mehrere Läufe erkannt wurden

Das ist eine Audit-Spur, keine Sicherheitsgarantie.

### Ehrliche Einschätzung

In internen Tests an kleinen Python-Projekten mit klaren Testsuiten hat der Loop über mehrere Iterationen schrittweise Fixes geliefert, ohne erkennbare Regressionen. Das ist anekdotisch, keine veröffentlichte Messung, und kein garantierter Produktivitätsgewinn. Behandle den Self-Improve-Loop als **Experimentierwerkzeug, das nur etwas taugt, wenn Budget-Grenze und Quality Gate ihn eng begrenzen.**

### Was schiefgehen kann

- **Kostenlauf:** Ohne `--max-budget-usd` kann ein hängender Loop in kurzer Zeit viel Geld verbrennen. Wie du ihn deckelst, steht in [S3.13](s3-13-autonome-loops-absichern.md).
- **Schein-Fixes:** Claude kann einen Test „reparieren", indem es die Assertion entfernt. Das Gate bleibt grün, der Fehler bleibt auch. Dagegen helfen strenge Pre-Commit-Hooks.
- **Memory-Drift:** Das Gedächtnis kann falsche Schlüsse festhalten, die spätere Iterationen in die falsche Richtung lenken; es braucht regelmäßiges Aufräumen ([S4.10](s4-10-diagnose-schritt-fuer-schritt.md)).
- **Zu viel Vertrauen in kleine Stichproben:** Ein paar gelungene Läufe an Spielzeug-Code lassen sich nicht auf Produktion übertragen.

### Wo es endet: regulierte Hardware

> **Branchenrealität:** In regulierten Anlagen der physischen Sicherheit (EN 50131 für Einbruch- und Überfallmeldeanlagen) ist ein autonomes Firmware-Update an Tür-Controllern **nicht** zulässig. Pflicht sind Change-Management mit Audit-Trail, oft die Anwesenheit eines Technikers vor Ort und Replay-Tests. Das Muster gilt für Code-Repositories und CI/CD; an echten Hardware-Endpunkten wäre ein Freigabe-Schritt Pflicht, also der Mechanismus „Menschliche Review-Gates" aus der Tabelle oben. Welche Kontrollen zu welchem Regelwerk passen, steht in [S3.11](s3-11-datenschutz-und-compliance.md).

## Vorführen

### Demo: Self-Improve-Loop (etwa 10 Minuten)

**Ziel:** Ein System zeigen, das seine eigenen Schwächen analysiert und selbst behebt.

**Vorbereitung:** Ein Projekt mit einigen Testfehlern oder Qualitätsproblemen; das Demoprojekt des Workshops eignet sich. Nötig ist das 🔧 Plugin `agentic-os` in einer Fassung mit `/agentic-os:run-loop`; fehlt der Befehl (siehe oben), nimm die Aufzeichnung. Leg vor dem Enter fest, dass der Loop nur **eine** Iteration läuft: In der interaktiven Sitzung ist das die Grenze, denn `claude --max-budget-usd` deckelt sie nicht ([S3.13](s3-13-autonome-loops-absichern.md)).

**Schritt 1: den Ausgangsstand zeigen**

Lass zuerst das Quality Gate laufen, damit alle den Ausgangswert sehen. `/quality-gate` gibt es im Plugin seit v4.0.0 nicht mehr. Fehlt es, lässt du stattdessen `pytest` und `ruff check` von Hand laufen; `/cost` aus dem Block unten brauchst du so oder so:

```
/quality-gate
/cost          # baseline spend — note this number, you'll compare after the loop
```

Notiere Wert und Fehler.

**Schritt 2: den Loop für eine Iteration starten**

<!-- cockpit:example -->
```
/agentic-os:run-loop
```

Wenn nach der Zahl der Iterationen gefragt wird, gib `1` ein. Geh durch, was in jeder Phase passiert:

- Analyse: „Liest die Ergebnisse des Quality Gates und die bisherigen Iterationen"
- Planung: „Sucht das Problem mit der größten Wirkung"
- TDD: „Schreibt einen fehlschlagenden Test; pass auf, er sollte scheitern"
- Umsetzung: „Schreibt den kleinsten Code, der den Test bestehen lässt"
- Quality Gate: „Voller Check; das ist die Go/No-Go-Entscheidung"
- Commit: „Passiert nur, wenn das Gate grün ist; sonst wird die Iteration verworfen"

**Schritt 3: das Iterationsprotokoll zeigen**

```
cat .agent-memory/iterations/iteration-001.md
```

Geh das Protokoll durch: was analysiert, was entschieden, was geändert und was geprüft wurde.

**Schritt 4: das Quality Gate noch einmal laufen lassen**

Ohne `/quality-gate` wiederholst du `pytest` und `ruff check` von Hand.

```
/quality-gate
/cost          # compare against the Step 1 baseline — show the audience what one iteration cost
```

Zeig, dass der Wert gestiegen ist, und zeig auf das Delta in `/cost`: So sieht der Raum den echten Preis einer autonomen Iteration.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten geplant; halte live etwa 15 Minuten frei (× 1,5), weil Loop-Iterationen und Testlaufzeit schwanken.

**Sagen (nach Schritt 4):** „Das System hat sich gerade selbst verbessert. Es hat seine Schwächen analysiert, einen Fix entworfen, ihn mit Tests geprüft, bestätigt, dass die Qualität nicht gesunken ist, und die Verbesserung committet. Um die Sicherheitsanalogie noch einmal zu bemühen: Das ist eine Sicherheitsanlage, die ihren eigenen Penetrationstest gefahren, eine Schwachstelle gefunden, sie gepatcht, den Patch getestet und alles protokolliert hat. Ohne menschliches Zutun." Schließ direkt mit der Branchenrealität an: An echten Controllern nach EN 50131 wäre genau dieses „ohne menschliches Zutun" unzulässig.

**Wenn es hakt:**

- **Plugin `agentic-os` fehlt, oder die Fassung hat kein `/agentic-os:run-loop`:** Aufzeichnung oder Screenshot zeigen und das Muster (Quality Gate → verbessern → neu testen) ohne Live-Lauf besprechen.
- **Der Loop läuft, bringt aber keine Fixes:** Das ist ein gültiges Ergebnis: „Manchmal ist das Projekt schon in gutem Zustand. Der Loop meldet ‚keine Verbesserungen nötig' und hört auf."
- **Die Budget-Grenze greift früh (bei einem Lauf mit `-p`):** Als Lehrmoment nutzen: „Genau deshalb setzen wir die Grenze. Ohne sie wäre das weitergelaufen."
- **Das Iterationsprotokoll liegt woanders:** Im Wurzelordner von `.agent-memory/` nach dem tatsächlichen Dateinamen suchen; neuere Fassungen nutzen eventuell `iterations/<ts>-<slug>.md` statt nummerierter Dateien.

</details>

## Check

Du kannst die vier häufigsten Fehlerbilder des Self-Improve-Loops nennen, jedem eine Gegenmaßnahme zuordnen und erklären, warum der Loop an Hardware-Endpunkten nach EN 50131 nicht ohne Freigabe-Gate laufen darf.

1. Welche sechs Schritte hat eine Iteration, und wann wird committet?
2. Warum ist ein grünes Quality Gate kein Beweis für einen echten Fix?
3. Was hält das Gedächtnis fest, und welches Risiko entsteht daraus?

<details><summary>Quizfrage</summary>

**Frage:** Was unterscheidet einen Commit hinter dem Quality Gate von einem normalen Commit, und welches Fehlerbild umgeht diesen Schutz trotzdem?

- **Richtig:** Er entsteht nur bei grünen Tests und ausreichendem Score; ein Schein-Fix umgeht das, wenn Claude die Assertion löscht.
- Falsch: Er unterscheidet sich nur im Format der Commit-Nachricht; einen Schutz über die normale Git-Mechanik hinaus gibt es nicht.
- Falsch: Er entsteht nur bei grünen Tests; ein Kostenlauf umgeht das, weil zu hoher Verbrauch die Prüfung des Gates überspringt.
- Falsch: Er wird im Gedächtnis protokolliert; Memory-Drift umgeht das, weil `.agent-memory/` die Assertions direkt umschreibt.

</details>

## Weiterlesen

- [CLI-Referenz: --max-budget-usd](https://code.claude.com/docs/en/cli-reference)
- [Hooks-Leitfaden](https://code.claude.com/docs/en/hooks-guide)
- [S3.13 · Autonome Loops absichern: Budget und Worktree](s3-13-autonome-loops-absichern.md)
- [S3.12 · Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](s3-12-zeitgesteuert-arbeiten.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S3.11 · Datenschutz, Aufbewahrung und regulierte Branchen](s3-11-datenschutz-und-compliance.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S4.10 · Diagnose Schritt für Schritt](s4-10-diagnose-schritt-fuer-schritt.md)
