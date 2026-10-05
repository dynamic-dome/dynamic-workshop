# Vorführen: S1.13 · Vager und präziser Auftrag im Vergleich

> Demo und Hinweise für Moderierende zum Kapitel [S1.13 · Vager und präziser Auftrag im Vergleich](../../library/s1-13-vager-und-praeziser-auftrag.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: gute und schlechte Aufträge

**Ziel:** Zwei Aufträge im selben Werkzeug mit sehr unterschiedlichem Ergebnis zeigen: einer ohne jeden Anhaltspunkt, einer als vollständiger Arbeitsauftrag.

**Vorbereitung:** Arbeite im Demo-Ordner aus [S1.10](s1-10-claude-md.md) weiter (`~/cc-workshop/demos/demo-1.2`). Die Git-Demo in [S1.16](s1-16-git-in-einem-fluss.md) braucht die Dateien, die hier entstehen.

**Schritt 1: der vage Auftrag**

Tipp in Claude Code:

```
Fix the code
```

Erwartet: Claude fragt nach („Welcher Code? Was ist das Problem?“) oder sagt, dass es mehr Kontext braucht.

**Schritt 2: der gute Auftrag**

Tipp in Claude Code:

```
Write a Python function called validate_ipv4(address: str) -> bool in a new file
called validators.py.

Requirements:
- Returns True for valid IPv4 addresses, False for anything else
- Valid format: four octets separated by dots, e.g. "192.168.1.1"
- Each octet must be an integer 0-255
- No leading zeros allowed (e.g., "192.168.01.1" is invalid)
- Must handle edge cases: empty string, None input, extra whitespace, IPv6 addresses
- Do not use regex — use explicit parsing for clarity

After creating the function, write pytest tests in tests/test_validators.py covering:
- 5 valid addresses
- Leading zeros (invalid)
- Out-of-range octet (256, -1)
- Too few octets
- Too many octets
- Non-numeric characters
- Empty string
- None input
- IPv6 address (should return False)
```

Erwartet: Claude legt `validators.py` mit einer klaren, expliziten Prüfung an und `tests/test_validators.py` mit allen verlangten Fällen.

**Schritt 3: prüfen lassen**

Wenn Claude fertig ist:

```
Run the tests
```

Erwartet: Claude führt `pytest tests/test_validators.py -v` aus und zeigt, dass alle Tests grün sind.

**Zum Vergleich zeigen oder anschreiben:**

| | Vager Auftrag | Guter Auftrag |
|---|---|---|
| **Eingabe** | „Fix the code“ | Funktion, Datei, Anforderungen, Grenzfälle, Tests |
| **Antwort von Claude** | fragt nach oder rät | setzt genau das Verlangte um |
| **Ergebnis** | unklar | prüfbar: Die Tests zeigen, ob es stimmt |
| **Nötige Runden** | viele | eine (meistens) |

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten.

**Sagen:**

- Vor Schritt 1: „Gleiches Werkzeug, gleiche Fähigkeiten. Mal sehen, was bei einer vagen Bitte passiert.“
- Nach Schritt 1: „Claude macht das Richtige: Es rät nicht. Aber der Prompt ist nutzlos. Hätte ich vorher Code gezeigt, würde Claude vielleicht etwas reparieren, aber ohne Kontext wäre jeder Versuch ein Schuss ins Blaue. Im Alltag hätte es auch einfach eine Deutung wählen können. Jetzt ein Auftrag, der alles mitbringt, was Claude braucht.“
- Während Claude an Schritt 2 arbeitet: „Seht, was der Prompt festlegt: die Signatur, den Dateinamen, die Prüfregeln, die Grenzfälle, eine Vorgabe zur Umsetzung (kein Regex) und die Tests. Das ist ein Arbeitsauftrag, kein Wunsch.“
- Nach Schritt 3: „Erster Versuch, alle Tests grün, weil die Spezifikation vollständig war. Das Werkzeug ist zwischen den beiden Prompts nicht klüger geworden. Die Prompts sind klüger geworden. Das ist die Fähigkeit, um die es geht.“
- Zum Abschluss: „Das ist die Fähigkeit mit dem größten Hebel in diesem Workshop. Nicht die Git-Integration, nicht das Gedächtnis, sondern das hier. Schreibt Prompts wie Arbeitsaufträge: konkret, abgegrenzt, mit Erfolgskriterium. Das Werkzeug belohnt Präzision.“

**Wenn es anders läuft:**

- **Claude liest unerwartet Dateien:** Bei neueren Versionen normal. Mach weiter und besprich in der Rückschau, warum Claude sich Kontext holt.
- **Die Tests des IPv4-Validators schlagen fehl:** Zeig die Fehlermeldung als Lehrmoment: „Seht ihr, auch mit gutem Prompt musst du prüfen.“
- **Claude weigert sich, den vagen Prompt überhaupt zu bearbeiten:** Lass Schritt 1 weg, erzähl, was passiert wäre, und geh direkt zum guten Prompt. Der Kontrast wirkt trotzdem.

Den Schritt „Run the tests“ als festes Muster („Mit Z testen“) behandelt [S1.14](../../library/s1-14-plan-modus.md).

</details>
