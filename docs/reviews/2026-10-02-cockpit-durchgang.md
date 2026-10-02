# Cockpit-Durchgang 2026-10-02 (unterbrochen)

> Gemeinsamer Durchgang Owner + Claude Code durch das Lern-Cockpit aus Sicht einer neuen Person.
> Stand: **unterbrochen**, Fortsetzung siehe unten. Befunde hier sind die einzige Quelle; die DCO-Todos verweisen
> mit der Befund-Nummer (B1 … B11) auf diese Datei: Sammel-Todo DCO #9563, Einzel-Todos #9564–#9571.

## Aufbau

- Frischer Klon von `origin/main` (`2c90477`) in
  `~/Desktop/Claude-Projekte/workshop-testlauf-2026-10-02/dynamic-workshop`, ausgeliefert mit
  `python -m http.server 8765 --bind 127.0.0.1` aus dem Repo-Root, Cockpit unter
  `http://127.0.0.1:8765/resources/claude-code-workshop-ui.html`, Chrome, 1568 px Fensterbreite.
- Gespielte Person: Entwickler, neu bei Claude Code. Ziele `alltag` + `security`, Zeit `abende`.
  Warum: „Ich will Routinearbeit im Alltag an Claude abgeben, ohne mir Sicherheitslücken einzufangen.“
- Selbsteinschätzung: Grundlagen und Git „schon gemacht“; Rechte, Kontext, Modelle, Plugins, MCP „gehört davon“;
  Aufträge, Skills, Hooks, Agenten, Gegenprüfung, Automation, Fehlersuche „neu“.
- Mini-Szenarien: Hook-Exit-Code falsch („wird blockiert“), Subagent-Bericht falsch („zweiten Subagenten fragen“),
  die übrigen vier richtig.
- Ergebnis: 4 Etappen, etwa 9 Stunden, 48 von 70 Kapiteln im Pfad, 8 „Schnellcheck reicht“, 14 „später“.

## Was funktioniert

- Der Pfad folgt den Antworten nachvollziehbar (schon gemacht → Schnellcheck, gehört → überfliegen bzw.
  Vertiefung durcharbeiten, neu → durcharbeiten); Etappen ≤ 150 Min passend zu `abende`; das Warum steht im Pfad.
- Mini-Szenarien geben sofort Rückmeldung mit Kapitelverweis; Antworten lassen sich korrigieren.
- Gebäudeplan zeigt die Empfehlungsfarben; „erledigt“ wird grün und bleibt nach Neuladen erhalten.
- Startseite zeigt Fortschritt und „Weiter, wo du warst“; Hell/Dunkel sauber; keine Konsolenfehler.

## Befunde

| Nr. | Art | Befund | Ort / Beleg | Vorschlag |
|---|---|---|---|---|
| B1 | UX, mittel | Schrittwechsel in der Einstufung behält die Scrollposition: Man landet mitten oder unten im nächsten Schritt (Schritt 4 begann mit der ersten Frage außerhalb des Bildes), die Überschrift verschwindet unter der fixierten Kopfleiste. | `tools/cockpit/template.html`, Einstufungs-Schritte | Beim Schrittwechsel an den Anfang der Einstufung scrollen (inkl. Versatz für die Kopfleiste). |
| B2 | UX, klein | Ein drittes Ziel lässt sich nicht anhaken (richtig), aber ohne jeden Hinweis. | Einstufung Schritt 1 | Kurzer Hinweis „höchstens zwei — erst eins abwählen“ oder übrige Kacheln sichtbar sperren. |
| B3 | Logik | Bei Ziel `security` lagen die Sicherheitsboden-Kapitel S3.13 und S4.4 unter „später — gehört nicht zu deinem Ziel“. | `tools/placement.py` Schritt C greift nur in R; Regale von `security` ohne `automation`/`headless-ci` | **Umgesetzt** auf Branch `einstufung-security-ausnahme` (Owner-Entscheid: Ausnahme über `chapter_goals`). |
| B4 | Text, klein | Die Begründung „Leute und Skills, die weiterhelfen.“ steht bei allen X-Kapiteln, passt aber nur zu X.1. | `_placement.yaml` → `reasons.community` | Neutraler Text („Blick über den Tellerrand — überfliegen reicht“) oder Begründung je Kapitel. |
| B5 | **Inhalt, mittel** | „Ein Schutz-Hook blockt **nur** mit `exit 2`“ ist zu absolut: S2.10 (Z. 99) sagt richtig, dass bei PreToolUse auch `permissionDecision: "deny"` blockt. Die Kapitel widersprechen sich. | S2.8 „Auf einen Blick“; `README.md` Z. 32 („dass nur `exit 2` einen Hook blocken lässt“). Das Szenario-Feedback in `_placement.yaml` Z. 129 spricht nur über Exit-Codes und ist korrekt. | „Von den Exit-Codes blockt nur 2 — oder ein JSON-`deny` (S2.10).“ Beleg aus `code.claude.com/docs/en/hooks.md` im Commit zitieren. |
| B6 | **UX, mittel** | Diagramme sind breiter als die Lesespalte (636 px). Im generierten Cockpit haben 57 SVGs eine viewBox breiter als 636 px, 24 breiter als 1200 px (Zählung enthält evtl. einzelne Nicht-Diagramme). S2.8: 1404 px, sichtbar weniger als die Hälfte, seitliches Scrollen, rechts bleibt Platz frei. | `tools/cockpit/template.html` (`.diagram`), `tools/render_diagrams.py` | Diagramm aus der Spalte auf volle Inhaltsbreite ausbrechen lassen und/oder per Klick vergrößern; breite LR-Flüsse ggf. als TD rendern. |
| B7 | UX, klein | „Als erledigt markieren“ zeichnet die Kapitelseite neu: Quiz-Ergebnis weg, „Ganzes Kapitel lesen“ wieder zu, Scrollposition springt. | Kapitelansicht (`?run=`) | Nur Statusknopf und Markierung aktualisieren statt Neuaufbau. |
| B8 | UX, klein | Kapitel-Quiz meldet bei richtiger Antwort nur „Richtig.“ ohne Begründung; die Einstufungs-Szenarien erklären. Falsche Antwort nicht getestet. | Kapitel-Check | Begründung zeigen, sofern das Kapitel eine hat; falsche Antwort im nächsten Durchgang prüfen. |
| B9 | Logik, klein | „Wiederholen“ fragt ein gerade erst erledigtes Kapitel sofort ab (widerspricht „Abrufen mit Abstand“); Text sagt „Fünf Fragen“, es kam eine. | Ansicht Wiederholen | Mindestabstand (z. B. 1 Tag) oder Hinweis „noch nichts fällig“; Text an die Anzahl anpassen. |
| B10 | UX, klein | Nach gespeicherter Einstufung bleibt der Hauptknopf der Startseite „Einstufung starten“. | Startseite | Dann „Weiter zu meinem Pfad“ als Hauptknopf, Einstufung als Nebenknopf. |
| B11 | UX, klein | Der Knopf „Kopieren“ überdeckt das Zeilenende im Code-Block. | „Ausprobieren“-Block | Knopf über/neben den Block setzen oder rechts Innenabstand reservieren. |

Offene Frage an den Owner: 48 von 70 Kapiteln für zwei Ziele — passt das zu „Du musst nicht alles lesen“?

## Fortsetzung (noch nicht getestet)

- [x] Branch `einstufung-security-ausnahme` geprüft (Codex-Verifier read-only: PASS mit Hinweis; Hinweis „Validator
      prüft nicht, ob ein `chapter_goals`-Wert eine Liste ist“ per Test + Prüfung nachgezogen) und lokal nach `main` gemergt.
- [ ] Pushen (Owner-OK), dann im Test-Klon `git pull` und die Einstufung mit Ziel `security` gegenprüfen
      (S3.13 und S4.4 im Pfad, nicht unter „später“).
- [ ] Tutor-Plugin: `claude --plugin-dir "<Test-Klon>"`, dann `/dynamic-workshop:workshop start`, `next`, `learn S2.8`,
      `review`, `guide S1`. Den neuen Klon nehmen — `~/cc-workshop/dynamic-workshop` steht noch auf `19f42de`.
- [ ] Cockpit: falsche Antwort im Kapitel-Quiz, „Pfad übernehmen“ (Live-Workshop), „Einstufung ändern“ und
      „Eigene Änderungen zurücknehmen“, Herunterstufen eines Sicherheitsboden-Kapitels (Warnung `override-safety`),
      Zeitoption `schnellstart` (Warnung `quickstart-long`), schmales Fenster bzw. Handy-Breite.
- [ ] Playground: `cd workshop-playground && python -m pytest -v`.

## Wieder aufnehmen

```bash
cd ~/Desktop/Claude-Projekte/workshop-testlauf-2026-10-02/dynamic-workshop
git pull
python -m http.server 8765 --bind 127.0.0.1
# Browser: http://127.0.0.1:8765/resources/claude-code-workshop-ui.html
```

Die Einstufung und „erledigt“ (S2.8) liegen im `localStorage` von `127.0.0.1:8765` und sind beim nächsten Mal noch
da, solange Port und Browser gleich bleiben.
