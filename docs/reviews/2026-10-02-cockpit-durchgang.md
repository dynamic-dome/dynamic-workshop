# Cockpit-Durchgang 2026-10-02 (unterbrochen)

> Gemeinsamer Durchgang Owner + Claude Code durch das Lern-Cockpit aus Sicht einer neuen Person.
> Stand: **unterbrochen**, Fortsetzung siehe unten. Befunde hier sind die einzige Quelle; die DCO-Todos verweisen
> mit der Befund-Nummer (B1 … B12) auf diese Datei: Sammel-Todo DCO #9563, Einzel-Todos #9564–#9572 (#9564 erledigt,
> #9565–#9572 am 2026-10-03 in #9563 zusammengelegt).
> **Abgleich 2026-10-24 (HEAD `f0afaf9`):** alle zwölf Befunde sind umgesetzt, siehe „Status je Befund“ unten.
> Offen bleiben die Browserabnahme durch den Owner und zwei kleine Owner-Entscheide.

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
| B12 | Logik, klein | Der Pfad endet mit einer Mini-Etappe: nach B3 bei `alltag` + `security` Etappe 5 nur S4.10 (18 Min). | Etappen-Aufteilung in `tools/placement.py` und JS-Port | Kleinen Rest (z. B. unter 30 Min) an die letzte Etappe anhängen; Golden bewusst neu. |

## Status je Befund (Abgleich 2026-10-24, HEAD `f0afaf9`)

Jeder Befund ist gegen den Ist-Stand geprüft: Commit, Code- bzw. Textstelle und Test. Das Paket P9 (UI-Überarbeitung)
und P10 (Begründung je Quiz-Antwort) stehen in `docs/plans/2026-10-05-selbstlern-zuerst-tickets.md`; der Owner hat P9 am
2026-10-06 angesehen („durchweg verbessert“).

| Nr. | Status | Beleg |
|---|---|---|
| B1 | erledigt | `b2c0a2d` (P9d); Test `test_a_new_placement_step_starts_at_its_top` |
| B2 | erledigt | `b2c0a2d` (P9d): zwei Ziele gewählt → übrige Kacheln gesperrt, Hinweiszeile; Test `test_a_third_goal_is_refused_visibly` |
| B3 | erledigt | `9f3e8bb` (gepusht als `9f9f72c`); Gegenprobe im Test-Klon siehe „Fortsetzung“ |
| B4 | erledigt | `b2c0a2d` (P9d): `reasons.community` lautet jetzt „Blick über den Tellerrand: überfliegen reicht.“ (`_placement.yaml` Z. 213) |
| B5 | erledigt | `fcab910` (R2): „von den Exit-Codes blockt nur 2“ samt Hinweis auf das JSON-`deny` in S2.8, README Z. 33 und weiteren Stellen; Beleg aus `hooks.md` steht im Commit |
| B6 | erledigt, Teilvorschlag bewusst nicht gebaut | `cdeca66` (P9e): Diagramme nutzen die Spalte, schrumpfen bis 72 Prozent, „Vergrößern“ öffnet sie im Dialog; `f0afaf9` Hell-Thema-Palette. Test `test_a_wide_diagram_uses_the_column_and_can_be_enlarged`. Nicht gebaut: breite LR-Flüsse als TD neu setzen (24 Diagramme, Artefakt-Puffer, siehe unten) |
| B7 | erledigt | `eb67fd3` (P9a): Markieren aktualisiert nur Knopf und Chip; Test `test_marking_done_keeps_quiz_result_open_answer_and_scroll_position` |
| B8 | erledigt | `cdeca66` (Verweis bei falscher Antwort), `727f9ce` (P10b: Begründung der gewählten Option, auch bei „Richtig.“ und in „Wiederholen“), Inhalte P10c–P10f (`b6167b4`), Gate `2be2f3c`; `build_library.py validate --complete`: Begründung 61 von 61. Die falsche Antwort ist durch `test_a_wrong_answer_says_why_this_one_and_where_to_look` abgedeckt. Die Owner-Durchsicht der Begründungen läuft getrennt als P10g (#9665) |
| B9 | erledigt | `0c827ae` (P9f): fällig einen Tag nach „erledigt“, sonst „Noch nichts fällig“, Text nennt die echte Zahl; Tests `test_review_waits_a_day_before_it_asks`, `test_review_asks_what_is_due_and_counts_honestly` |
| B10 | erledigt | `5046c84` (P9c): Hauptknopf „Weiter mit <nächstes offenes Kapitel>“, Einstufung als Nebenknopf; Test `test_start_with_a_placement_leads_on_to_the_next_open_chapter` |
| B11 | erledigt | `cdeca66` (P9e): „Kopieren“ über dem Block; Test `test_copy_button_does_not_cover_the_code` |
| B12 | erledigt | `0c827ae` (P9f): Rest unter 30 Minuten wird an die vorige Etappe angehängt, Python-Engine und JS-Port, Golden bewusst neu (Persona P17); Test in `test_placement.py`, Engines stimmen bei allen zwanzig Personas überein |

**Nachprüfung am 2026-10-24:** `build_library.py check` OK, `validate --complete` ohne Befund,
`pytest tools/test_build_cockpit.py tools/test_placement.py tools/test_placement_js.py tools/test_cockpit_browser.py`:
195 passed. Keine Vollsuite, keine Änderung am Cockpit-Artefakt.

**Nicht gebaut, weil nicht eindeutig oder zu groß:**

- B6, breite LR-Flüsse als TD rendern: würde 24 Diagramme neu setzen und Artefakt-Bytes kosten. Das Artefakt liegt bei
  2.987.140 von 3.000.000 Bytes (MAX_BYTES, DCO #9925). Die Vergrößerung löst das Lesen; Owner-Entscheid, ob nötig.
- Die Frage „48 von 70 Kapiteln für zwei Ziele“ unten ist weiter ein Owner-Entscheid; gebaut wird nichts.

Offene Frage an den Owner: 48 von 70 Kapiteln für zwei Ziele — passt das zu „Du musst nicht alles lesen“?

## Fortsetzung (noch nicht getestet)

> Stand 2026-10-24: Das ist die offene **Browserabnahme beim Owner** (Hell-Thema: `python -m http.server 8765 --bind 127.0.0.1`,
> dann `tools/cockpit_shots.py --theme light`). Browser-Tests decken davon die falsche Quiz-Antwort und die Handy-Breite ab;
> Pfad übernehmen, „Einstufung ändern“, „Eigene Änderungen zurücknehmen“, Herunterstufen (`override-safety`) und
> `schnellstart` (`quickstart-long`) sind nur in der Engine getestet, nicht in der Oberfläche. Der Playground (5 absichtliche
> Schwachstellen) wurde am 2026-10-24 nicht ausgeführt.

- [x] Branch `einstufung-security-ausnahme` geprüft (Codex-Verifier read-only: PASS mit Hinweis; Hinweis „Validator
      prüft nicht, ob ein `chapter_goals`-Wert eine Liste ist“ per Test + Prüfung nachgezogen) und lokal nach `main` gemergt.
- [x] Gepusht (`9f9f72c`), im Test-Klon gezogen und im Cockpit mit der gespeicherten Einstufung gegengeprüft:
      S3.13 und S4.4 stehen auf „durcharbeiten“ mit Sicherheitsboden-Plakette, S3.12 und S4.3 als Voraussetzung auf
      „überfliegen“; Pfad jetzt 5 Etappen, etwa 10 Stunden, 52 Kapitel, „später“ 14 → 10.
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
