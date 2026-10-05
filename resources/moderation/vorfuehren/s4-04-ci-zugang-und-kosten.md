# Vorführen: S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff

> Demo und Hinweise für Moderierende zum Kapitel [S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](../../library/s4-04-ci-zugang-und-kosten.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Headless Claude in fünf Minuten, Schritte 3 und 4

Das ist die Fortsetzung der Demo aus [S4.3](s4-03-headless.md); Ziel, Voraussetzungen und die Schritte 1 und 2 stehen dort.

**Zusätzliche Voraussetzung für Schritt 4:** `ANTHROPIC_API_KEY` in der Umgebung. `--bare` liest weder die Browser-Anmeldung noch ein Abo-Token; ohne API-Key ist der `--bare`-Aufruf nicht angemeldet.

**Schritt 3: eine Kostengrenze vorführen**

```bash
claude -p "Refactor this entire codebase from scratch with full test coverage" \
  --max-budget-usd 0.05 \
  < workshop-playground/access_control.py
```

Erwartung: Claude beginnt die ehrgeizige Aufgabe, erreicht die Grenze und beendet den Lauf mit einer Meldung, dass das Budget erschöpft ist. Zeig den Exit-Code (`echo $?`): ungleich 0. CI würde diesen Schritt scheitern lassen, statt ihn endlos laufen zu lassen.

**Schritt 4: `--bare`, den Zeitunterschied zeigen**

Zeitmessung im direkten Vergleich:

```bash
time claude -p "Hello"
time claude --bare -p "Hello"
```

`--bare` sollte spürbar schneller antworten: Es überspringt die Erkennung von Skills, den Verbindungsaufbau zu MCP-Servern und die Registrierung von Hooks. Nenn den Unterschied laut.

<details><summary>Für Moderierende</summary>

**Sagen:**

- Schritt 3: „Ohne dieses Flag hätte dieser Prompt Dollars kosten können. Mit ihm liegt der schlimmste Fall bei ungefähr fünf Cent."
- Schritt 4: „Für ein `Hello` brauchst du keine Plugins. Für einen echten CI-Schritt vielleicht schon. Wähl das passende Werkzeug."

Den Abschluss-Sprechpunkt der ganzen Demo findest du in [S4.3](s4-03-headless.md).

**Wenn kein API-Key da ist:** Zeig Schritt 4 nur als Befehl und erklär, warum `--bare` ohne API-Key nicht angemeldet wäre.

**`claude setup-token` nie live:** Willst du den Befehl zeigen, dann **vor dem Workshop offline**, nicht auf dem geteilten Bildschirm. Er gibt ein langlebiges OAuth-Token aus. Wer damit nachlässig umgeht, geht dasselbe Risiko ein wie mit einem privaten SSH-Schlüssel auf dem Beamer. Nenn den Befehl, verweis auf die Doku und mach weiter.

</details>
