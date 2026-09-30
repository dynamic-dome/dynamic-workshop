# Prüf-Brief: Aussagen-Matrix eines umgezogenen Kapitels

> Für die Prüfer-Agenten des Umzugs (Plan Task 7/8, Spec §12.5). Du bist **unabhängig** vom Schreiber und prüfst,
> ob beim Übersetzen und Ordnen Fakten verloren gingen, sich verändert haben oder neu erfunden wurden.
> Arbeitsort: Worktree `C:\Users\domes\Desktop\Claude-Projekte\dynamic_workshop-bibliothek`. Du änderst **nur** deine
> Matrix-Datei `docs/migration/claims/<ID>.json`, sonst nichts.

## Eingaben

- Das neue Kapitel: `resources/library/<file>` (Dateiname aus `docs/migration/chapter-meta.yaml`).
- Die Quelle: die Heimat-Bereiche des Kapitels aus `docs/migration/ownership.json` → `packs[<ID>]`, gelesen aus dem
  Basis-Commit mit `git show ba222d2:<datei>` (nur die angegebenen Zeilen).
- Bekannte, **gewollte** Korrekturen: Spec `docs/plans/2026-09-30-praxisbibliothek-design.md` Anhang B (Liste der
  Widersprüche) und die Hook-Fakten aus `docs/reviews/2026-09-28/05-bewertung.md` (H-01 bis H-17).

## Vorgehen

1. Zerlege die Quelle in **fachliche Aussagen**: jede Behauptung über Verhalten, jede Tabellenzeile, jeder Demo- und
   Recovery-Schritt, jede Voraussetzung, jede Zahl, jeder Befehl mit seiner Wirkung. Keine Stilfragen.
2. Suche jede Aussage im neuen Kapitel. Status:
   - `kept` — sinngleich vorhanden (Übersetzung, Umstellung, Kürzung ohne Bedeutungsverlust sind in Ordnung)
   - `changed` — vorhanden, aber mit anderer Bedeutung (alter und neuer Wortlaut)
   - `dropped` — fehlt (dann: steht sie in einem anderen Kapitel? `ownership.json` → `links`, oder per grep in
     `resources/library/`)
3. Suche umgekehrt **neue Aussagen** im Kapitel, die in keiner Quelle stehen (`new`). Formulierungshilfen,
   Überleitungen und die Pflichtteile „Schnellcheck", „Auf einen Blick" (wenn inhaltsgleich zur Quelle) zählen nicht.
   Neue Fakten, Zahlen, Flags, Befehle, Verhaltensaussagen zählen.
4. Bewerte jede Abweichung:
   - `ok` — gewollte Korrektur (Anhang B / Bewertung H-xx) oder unschädliche Straffung
   - `fix` — muss der Schreiber beheben (Bedeutung verändert, Fakt verloren ohne Ziel, Erfindung, falscher Befehl)
   - `ask` — unklar, der Orchestrator entscheidet (mit Begründung)
5. Prüfe zusätzlich: Sprache (Deutsch, Umlaute, „du"; Code/Bezeichner Englisch), keine Modellgeneration außerhalb
   des Kanons, Quizantworten ohne Längen-Hinweis auf die Lösung, Sicherheitsaussage in „Auf einen Blick" bei
   `safety_floor: true`, Codeblöcke am Zeilenanfang.

## Ausgabe

Schreibe `docs/migration/claims/<ID>.json` und gib dasselbe JSON zurück:

```json
{"id": "S2.8", "verdict": "pass|fix|ask",
 "counts": {"kept": 0, "changed": 0, "dropped": 0, "new": 0},
 "items": [{"status": "changed|dropped|new", "source": "datei:zeile", "old": "…", "new": "…",
            "rating": "ok|fix|ask", "reason": "…"}],
 "style": [{"rating": "fix|ask", "where": "Abschnitt", "issue": "…"}]}
```

`items` enthält nur Abweichungen (`changed`, `dropped`, `new`); `kept` nur als Zahl. `verdict` = `fix`, sobald ein
Eintrag `fix` ist; `ask`, wenn nur `ask` offen ist; sonst `pass`. Belege jede Angabe mit Zeile; rate nie.
