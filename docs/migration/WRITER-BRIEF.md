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

## Nachträge aus dem Pilot (Hooks-Regal, 2026-09-30) — verbindlich

11. **Codeblöcke per Skript einsetzen**, nicht abtippen: lies den Block mit `git show ba222d2:<datei>` und schreibe ihn
    unverändert in dein Kapitel (z. B. mit einem kleinen Python-Skript). So weicht kein Byte ab.
12. **Der alte Cockpit-Text ist eine Quelle wie jede andere**, keine Wahrheit: Im Pilot waren 3 von 5 Quiz-/Konzepttexten
    fachlich falsch. Prüfe ihn gegen die Heimat-Bereiche und die Spec-Korrekturen.
13. **Offizielle Doku gegenprüfen ist erlaubt und erwünscht**, wenn dir eine Aussage zweifelhaft vorkommt:
    `curl -sL https://code.claude.com/docs/en/<seite>.md` (Markdown im Wortlaut, nicht WebFetch). Jede so begründete
    Änderung kommt mit dem wörtlichen Zitat unter `corrections[].evidence` in deinen Bericht. Ohne Zitat keine Änderung.
14. **Leere Platzhalter-Snippets** (z. B. ein Codeblock, der nur einen Kommentar wie `# Add a simple logging hook`
    enthält) und echte Dubletten darfst du weglassen. Jeder weggelassene Block steht dann mit Digest (aus
    `migration_ledger.py --chapter`), Quelle und Grund unter `drop_proposals`. „Ledger grün" heißt für dich: kein
    fehlender Block außer denen in `drop_proposals`. Die Streichliste pflegt der Orchestrator.
15. **`cockpit:example`**: Hat das Kapitel eine Übung, steht der Marker in „Selbst machen"; sonst in „Im Detail" oder
    „Vorführen". Hat der Heimat-Bereich gar keinen Codeblock, darfst du das Beispiel aus dem Cockpit-Text nehmen
    (nach Prüfung) — vermerke das unter `notes`.
16. **Talking Points ziehen mit ihrer Demo um.** Gehören Demo-Schritte einem anderen Kapitel als die Sprechpunkte,
    stehen beide dort, wo die Schritte stehen; das andere Kapitel verlinkt.
17. **„Auf einen Blick"**: Der erste Absatz erscheint allein im Cockpit. Bei `safety_floor: true` muss die
    Sicherheitsaussage in diesem ersten Absatz stehen; ein zweiter Absatz ist erlaubt.
18. **Quiz**: Die richtige Antwort ist nicht die längste — in höchstens 40 % aller Quizfragen der Bibliothek darf sie
    es sein (der Validator prüft das über die ganze Bibliothek). Formuliere die falschen Antworten gleich konkret.
19. **Keine Links auf Referenzkarten** (`resources/reference/…`) — die entstehen später und werden dann ergänzt.
    Links auf noch nicht geschriebene Kapitel sind in Ordnung (Dateiname aus `chapter-meta.yaml`).
20. Voraussetzungen und Links auf **noch nicht geschriebene Kapitel** meldet der Validator während des Umzugs nicht;
    alle anderen Befunde müssen weg.

## Prüfen, bevor du fertig bist

```text
python tools/build_library.py validate --chapter resources/library/<file>
python tools/migration_ledger.py --chapter <ID>
python -m pytest tools/test_course_hooks.py tools/test_course_ci_auth.py tools/test_lint_currency.py -q
python tools/lint_currency.py
```

Alle vier müssen grün sein (Ledger: siehe Regel 14). Beim Ledger ist ein Snippet nur dann „ok", wenn es unverändert
irgendwo im neuen Bestand steht.

## Rückgabe (JSON)

```json
{"chapters": [{"id": "S2.8", "file": "resources/library/s2-08-hook-einrichten.md",
  "snippets_missing": [], "drop_proposals": [{"digest": "…", "source": "datei:zeile", "reason": "…"}],
  "corrections": [{"old": "…", "new": "…", "evidence": "…"}], "todos": [], "unsure": []}],
 "shelf_intro_proposal": "…", "notes": "…"}
```
