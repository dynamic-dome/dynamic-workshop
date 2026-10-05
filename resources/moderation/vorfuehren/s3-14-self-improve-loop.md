# Vorführen: S3.14 · Self-Improve-Loop: was geht und wo es endet

> Demo und Hinweise für Moderierende zum Kapitel [S3.14 · Self-Improve-Loop: was geht und wo es endet](../../library/s3-14-self-improve-loop.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

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
