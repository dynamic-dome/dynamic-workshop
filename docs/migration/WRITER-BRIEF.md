# Schreib-Brief: Kapitel der Praxisbibliothek umziehen

> Für die Schreib-Agenten des Umzugs (Plan Task 7/8). Spec: `docs/plans/2026-09-30-praxisbibliothek-design.md` §4.
> Arbeitsort: Worktree `C:\Users\domes\Desktop\Claude-Projekte\dynamic_workshop-bibliothek` (Branch `praxisbibliothek`).
> **Du übersetzt und ordnest. Du erfindest nichts.**

## Was du bekommst

- Eine Liste von Kapitel-IDs (dein Auftrag).
- `docs/migration/chapter-meta.yaml` — **verbindliche** Metadaten je Kapitel (id, type, title, shelf, level, minutes,
  requires, safety_floor, transferable, aliases, offers, after, file). Übernimm sie **unverändert** ins Frontmatter;
  der Dateiname ist `resources/library/<file>`. Der Validator prüft das (Regel `meta-contract`).
- `docs/migration/ownership.json` → `packs[<ID>]`: die **Heimat-Bereiche** deines Kapitels (Datei, Start- und
  Endzeile im Basis-Commit). Lies sie mit `git show ba222d2:<datei>` (z. B. über Python oder `git show … | sed -n
  '<start>,<end>p'`). Nur diese Zeilen gehören inhaltlich in dein Kapitel. `links[<ID>]` nennt verwandte Bereiche,
  die ein anderes Kapitel besitzt — dorthin verlinkst du, du kopierst sie nicht.
- `docs/migration/source-map.json` → `units[<ID>]`: Vorschläge der Bestandsaufnahme (`outcome_de`, `skip_check_de`,
  `diagram_idea`, `primary_source`, `issues` mit Zeilenbelegen, `cross_duplicates`). Vorschläge, keine Pflicht —
  `issues` zeigen dir aber, welche Doppelungen und Unstimmigkeiten du auflösen sollst.
- `docs/migration/cockpit-content-ba222d2.json` → `sectionContent[<ID>]` (concept, analogy, example, checkpoint) und
  `sectionQuiz[<ID>]` (q, correct, wrong[3]): der geprüfte deutsche Cockpit-Text der alten Oberfläche.
- Master der Analogien (alt): `git show ba222d2:resources/security-analogies.md` — halte dich an dessen Zuordnungen.

## Aufbau jeder Datei (Pflicht)

```markdown
---
id: S2.8
type: lesson
title: …                # exakt aus chapter-meta.yaml
shelf: …
level: …
minutes: …
requires: […]
safety_floor: …
transferable: …
outcome: "Ich kann …"   # ein prüfbarer Satz; nimm outcome_de als Ausgangspunkt
sources:
  - https://code.claude.com/docs/en/…   # offizielle Doku, mindestens eine bei lesson/setup
aliases: […]
---

# S2.8 · <title>

## Schnellcheck
- <Verhaltensfrage 1>
- <Verhaltensfrage 2>

## Auf einen Blick
<2–4 Sätze, der Kern. Der erste Absatz erscheint im Cockpit.>

## Bild im Kopf
<Analogie aus der Physical-Security-Welt, erster Absatz erscheint im Cockpit. Optional ein ```mermaid-Diagramm.>

## Im Detail
<Der Lehrtext aus den Heimat-Bereichen, übersetzt und geordnet, mit ###-Unterabschnitten.>

## Vorführen
<Demo-Schritte. Talking Points, Timing, Recovery Notes gehören in:>
<details><summary>Für Moderierende</summary>

…

</details>

## Selbst machen
<Übung(en). Genau ein Codeblock bekommt direkt davor die Zeile <!-- cockpit:example --> (bei lesson Pflicht).>

## Typische Fallen
<optional: Stolpersteine, auch aus FAQ/Troubleshooting, wenn sie dieses Kapitel betreffen>

## Check
<Ein Satz „Du kannst …" (erster Absatz = Cockpit-Checkpunkt), dann 2–3 Abruffragen, dann das Quiz:>

<details><summary>Quizfrage</summary>

**Frage:** …

- **Richtig:** …
- Falsch: …
- Falsch: …
- Falsch: …

</details>

## Weiterlesen
- <offizielle Doku zuerst, dann verwandte Kapitel als relative Links auf <file>, dann Referenzkarten>
```

Welche Abschnitte je Typ Pflicht/optional/verboten sind: Spec §4.3 (Tabelle). `practice`: nur Auf einen Blick,
Selbst machen (Auswahlhilfe + Links auf die Übungen in den Kapiteln aus `offers` + optionaler Übungspool), Check,
optional Weiterlesen. Keinen Meta-Block schreiben — den erzeugt der Generator.

## Regeln

1. **Sprache:** Deutsch mit korrekten Umlauten, Anrede „du", kurze Sätze. Code, Befehle, Dateinamen, Flags,
   Bezeichner, Tool-Namen, Event-Namen bleiben Englisch. Übersetze Fachbegriffe nur, wenn es einen gängigen
   deutschen gibt (Rechte-Modus, Kontextfenster); sonst Englisch lassen (Hook, Skill, Worktree, Subagent).
2. **Codeblöcke byte-identisch** aus der Quelle — auch Kommentare, Leerzeichen, Platzhalter. Codeblöcke stehen
   **am Zeilenanfang** (nie in eine Liste eingerückt), sonst sehen die Wächter-Tests sie nicht. Zeilen wie
   `# tested asset: resources/demos/assets/hooks/…` und `version-pinned: …` bleiben, wo sie stehen.
3. **Keine Modellgenerationen** (Nummern wie „Opus 4.8"); Aliase `opus`, `sonnet`, `haiku`, `fable` und Rollen.
   Ausnahme nur mit `version-pinned: <Grund>` in derselben Zeile, wie in der Quelle.
4. **Nichts erfinden.** Keine neuen Fakten, Zahlen, Flags, Befehle. Du darfst kürzen, umstellen, Doppelungen
   zusammenführen und Unstimmigkeiten auflösen, die in `issues` oder in Spec Anhang B belegt sind — jede
   inhaltliche Korrektur kommt in deinen Bericht (`corrections`). Bist du unsicher, schreib
   `<!-- TODO(migration): <Frage> -->` an die Stelle und melde es; rate nie.
5. **Doppelungen:** Was ein anderes Kapitel besitzt (`links`), verlinkst du. Was in der Quelle doppelt steht,
   steht bei dir einmal.
6. **Quiz:** Nimm die alte Frage, behalte den fachlichen Inhalt, aber **gleiche die Antwortlängen an**: die richtige
   höchstens 1,35 × so lang wie das Mittel der falschen, jede falsche mindestens 0,6 × so lang wie die richtige. Die
   richtige soll nicht systematisch die längste sein.
7. **Schnellcheck:** 2 Verhaltensfragen („Hast du schon …?", „Kannst du ohne Nachschlagen …?"), keine Wissensabfrage.
8. **Sicherheitsboden** (`safety_floor: true`): Die Sicherheitsaussage gehört in „Auf einen Blick" — wer nur
   überfliegt, muss sie trotzdem mitnehmen.
9. **Stil:** keine Werbesprache, keine KI-Floskeln (u. a. nie das Bild der „verheilten Wunde" für Fehler —
   stattdessen „was schiefgegangen ist", „Fehler"), keine unbelegten Zahlen.
10. **Nur deine Dateien** in `resources/library/` anlegen. Keine anderen Dateien ändern, nichts committen,
    `tools/fixtures/migration-dropped.txt` nicht anfassen (Streichungen schlägst du im Bericht vor).

## Prüfen, bevor du fertig bist

```text
python tools/build_library.py validate --chapter resources/library/<file>
python tools/migration_ledger.py --chapter <ID>
python -m pytest tools/test_course_hooks.py tools/test_course_ci_auth.py tools/test_lint_currency.py -q
python tools/lint_currency.py
```

Alle vier müssen grün sein. Beim Ledger ist ein Snippet nur dann „ok", wenn es unverändert irgendwo im neuen Bestand
steht; fehlende Snippets entweder übernehmen oder im Bericht als Streichung vorschlagen (mit Grund: Dublette von
<wo>, veraltet laut <Beleg>).

## Rückgabe (JSON)

```json
{"chapters": [{"id": "S2.8", "file": "resources/library/s2-08-hook-einrichten.md",
  "snippets_missing": [], "drop_proposals": [{"digest": "…", "source": "datei:zeile", "reason": "…"}],
  "corrections": [{"old": "…", "new": "…", "evidence": "…"}], "todos": [], "unsure": []}],
 "shelf_intro_proposal": "…", "notes": "…"}
```
