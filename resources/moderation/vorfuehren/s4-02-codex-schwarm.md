# Vorführen: S4.2 · Codex-Schwarm und die Datenfluss-Grenze

> Demo und Hinweise für Moderierende zum Kapitel [S4.2 · Codex-Schwarm und die Datenfluss-Grenze](../../library/s4-02-codex-schwarm.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Codex-Schwarm

**Ziel:** Die Multi-Modell-Pipeline zeigen: Claude plant, Codex baut parallel, Claude prüft.

**Voraussetzung:** Die Codex CLI ist installiert und angemeldet. Prüfen mit `codex --version`. Dazu das Plugin `multi-model-orchestrator`.

**Schritt 1: den Schwarm mit Zerlegung starten**

```
/multi-model-orchestrator:codex-swarm --decompose
```

Wenn nach der Aufgabe gefragt wird, gib ein:

> "Build a Python CLI security tool with three commands:
> 1. scan: given a hostname, attempt connections to ports 21, 22, 23, 25, 80, 443, 3306, 5432, 8080, 8443 and report which are open
> 2. check: given a URL, make an HTTP GET request with a 5-second timeout and report the status code and response time in milliseconds
> 3. report: run both scan and check on a given target and output a JSON report with timestamp, target, open ports, and HTTP status
> Include a CLI entry point using argparse, proper error handling, and a test file."

**Schritt 2: die Zerlegung beobachten**

Zeig, dass Claude die Aufgabe analysiert und in unabhängige Teilaufgaben zerlegt, bevor ein einziger Codex-Agent startet. Benenne jede Teilaufgabe, sobald Claude sie erkennt.

**Schritt 3: die parallele Ausführung beobachten**

Zeig, wie die N Codex-Agenten gleichzeitig hochfahren. Betone, dass sie parallel arbeiten: Die Uhr läuft für alle zugleich.

**Schritt 4: Claude prüft**

Sieh zu, wie Claude alle erzeugten Dateien liest. Zeig, was es findet: Integrationsfehler, fehlende Fehlerbehandlung, Lücken in der Testabdeckung.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 12 Minuten geplant; reserviere live etwa 18 Minuten (× 1,5), weil Zerlegung und Start der Codex-Agenten unterschiedlich lange dauern.

**Sagen:**

„Das ist das Modell Architekt, Monteur, Prüfer. Claude (Opus-Tier) hat die Spezifikation entworfen. Die Codex-Agenten haben die Komponenten parallel gebaut, wie Monteure, die auf verschiedenen Etagen gleichzeitig Leser installieren. Jetzt prüft Claude jede Komponente vor der Abnahme. Drei verschiedene Stärken, eine Pipeline. Das Ergebnis ist besser als jedes einzelne für sich."

**Wenn etwas ausfällt:**

- **Codex CLI nicht installiert:** Lass den Live-Lauf weg, zeig eine Aufzeichnung oder Screenshots aus der Vorbereitung und besprich stattdessen das Muster.
- **Plugin `multi-model-orchestrator` nicht installiert:** Zeig die README des Plugins auf GitHub oder ersetze die Demo durch einen Prompt an Claude: „Pretend you're a Codex swarm with N agents. Show what each would generate."
- **Codex-Anmeldung schlägt fehl:** wie „nicht installiert", zurück zur Diskussion. Erwähne, dass außerhalb des Workshops eine Anmeldung mit `codex login` nötig ist.
- **`--decompose` wird nicht erkannt:** Ältere Plugin-Versionen kennen das Flag nicht. Lass es weg, lass Claude die Aufgabe zuerst von Hand zerlegen und starte dann die Agenten.

</details>
