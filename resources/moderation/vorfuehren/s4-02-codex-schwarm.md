# Vorführen: S4.2 · Codex-Schwarm und die Datenfluss-Grenze

> Demo und Hinweise für Moderierende zum Kapitel [S4.2 · Codex-Schwarm und die Datenfluss-Grenze](../../library/s4-02-codex-schwarm.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Codex-Schwarm und die Datenfluss-Grenze

**Ziel:** Zeigen, was ein zweiter Anbieter sieht, und wie das Team entscheidet, was ihn erreichen darf. Wenn die Voraussetzungen stehen, dazu die Multi-Modell-Pipeline: Claude plant, Codex baut parallel, Claude prüft.

**Teil 1: die Übung aus dem Kapitel live (Pflicht, etwa 15 Minuten, ohne Plugin und ohne Konto).** Zeig die Übung „die Dateien eines Projekts für einen zweiten Anbieter sortieren“ in [S4.2](../../library/s4-02-codex-schwarm.md). Startzustand wie dort: die Tabelle mit den zehn Dateien des Projekts `zugangsportal` an der Wand oder auf dem Bildschirm, Papier oder eine Notiz. Ablauf: Schritt 1 (jede Datei: darf raus, darf nicht raus, nur Signatur, mit einem Stichwort) lässt du die Gruppe in Paaren machen, Schritt 2 (die Entscheidung für eine Änderung innerhalb von `access_rules.py`) im Plenum. Erst danach zeigst du den Vergleich aus dem Kapitel.

**Teil 2: der Schwarm live (nur wenn die Voraussetzungen stehen).** Die Codex CLI ist installiert und angemeldet (`codex --version`), dazu das Plugin `multi-model-orchestrator`, und die Gruppe weiß vorher, dass der Quellcode dabei zusätzlich an OpenAI geht. Nimm dafür ein Wegwerf-Projekt ohne Vertrauliches, nicht die Dateien aus Teil 1:

```
/multi-model-orchestrator:codex-swarm --decompose "Build a Python CLI with scan, check, report commands"
```

Zeig, dass Claude die Aufgabe in unabhängige Teilaufgaben zerlegt, bevor ein Codex-Agent startet, dass die Codex-Agenten parallel hochfahren (die Gesamtdauer ist die des langsamsten Agenten) und dass Claude zum Schluss alle Ergebnisse liest und Integrationsfehler sucht.

<details><summary>Für Moderierende</summary>

**Dauer:** Teil 1 etwa 15 Minuten; Teil 2 etwa 12 Minuten geplant, reserviere live etwa 18 Minuten (× 1,5), weil Zerlegung und Start der Codex-Agenten unterschiedlich lange dauern.

**Sagen:**

- Einstieg: „Was Claude liest, geht an Anthropic. Was in den Aufträgen für Codex steht, geht an OpenAI. Die Datenregeln von Anthropic decken nur die Claude-Seite ab. Das gilt für jeden zweiten Anbieter, den ihr anbindet, nicht nur für Codex."
- Teil 1, Schritt 1: Lass die Paare begründen, nicht nur zuordnen. Die Dateien mit Kundendaten, Geheimnissen oder vertraulichem Herstellermaterial bleiben im Haus. Für die Zugriffslogik genügt dem Anbieter die Signatur, solange er sie nur aufrufen soll.
- Schritt 2: „Soll der Anbieter die Logik selbst ändern, reicht das Gerüst nicht: Dann bleibt nur, den Codex-Schritt wegzulassen oder ein lokales Modell zu nehmen." Frag nach: Was verlässt dein Haus, und was kostet dich die Wahl?
- Teil 2: „Das ist das Modell Architekt, Monteur, Prüfer. Claude hat die Aufgabe zerlegt. Die Codex-Agenten bauen die Teile parallel, wie Monteure, die auf verschiedenen Etagen gleichzeitig Leser installieren. Jetzt prüft Claude vor der Abnahme. Und der Subunternehmer sieht alles, was im Montageplan steht."

**Wenn etwas ausfällt:**

- **Codex CLI nicht installiert:** Lass Teil 2 weg, zeig eine Aufzeichnung oder Screenshots aus der Vorbereitung und besprich stattdessen das Muster. Teil 1 braucht nichts davon.
- **Plugin `multi-model-orchestrator` nicht installiert:** Es ist ein eigenes Plugin, kein Teil von Claude Code. Lass Teil 2 weg oder ersetze ihn durch einen Prompt an Claude: „Pretend you're a Codex swarm with N agents. Show what each would generate."
- **Codex-Anmeldung schlägt fehl:** wie „nicht installiert", zurück zur Diskussion. Erwähne, dass außerhalb des Workshops eine Anmeldung mit `codex login` nötig ist.
- **`--decompose` wird nicht erkannt:** Ältere Plugin-Versionen kennen das Flag nicht. Lass es weg, lass Claude die Aufgabe zuerst von Hand zerlegen und starte dann die Agenten.

</details>
