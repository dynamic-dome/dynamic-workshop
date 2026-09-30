# Kuratoren-Addendum — manuelle Zusatz-Befunde & Korrekturen (2026-06-21)

> Diese Datei ergaenzt die Agenten-Ergebnisse um Befunde, die der orchestrierende Hauptagent
> direkt verifiziert hat, sowie um Korrekturen an degenerierten Teil-Ergebnissen.

---

## A. Verifizierter Bug: `AGENTS.md` spricht von "Codex" statt "Claude Code"

**Schweregrad: HIGH (accuracy) · Aufwand: S · Prioritaet: P0**

`AGENTS.md` im Repo-Root beschreibt die Mission des Workshops mit dem FALSCHEN Produkt:

- Zeile 5: *"...einen vollumfaenglichen Eindruck von **Codex** vermittelt..."*
- Zeile 7: *"Die Teilnehmer sollen nach dem Workshop **Codex** eigenstaendig und produktiv ... einsetzen koennen."*

Der gesamte Workshop ist **Claude Code**. `CLAUDE.md` (die Schwesterdatei) ist korrekt; `AGENTS.md`
ist offenbar aus einer Codex-Vorlage uebernommen und nie angepasst worden.

**Warum kritisch:** Modul 1.2 empfiehlt explizit, `AGENTS.md` per `@AGENTS.md` in `CLAUDE.md` zu
importieren (Cross-Tool-Interop). Wuerde jemand dieser Empfehlung folgen, zoege er die falsche
Produktbezeichnung in den aktiven Kontext.

**Empfehlung:** In `AGENTS.md` "Codex" → "Claude Code" korrigieren (Zeilen 5 und 7).
**Akzeptanz:** `grep -i codex AGENTS.md` liefert keine produktbezeichnenden Treffer mehr.

---

## B. Verifizierte Stale-Referenz in `AGENTS.md`

**Schweregrad: MEDIUM (accuracy) · Aufwand: S · Prioritaet: P2**

`AGENTS.md` Zeile 35 und Zeile 40 referenzieren `resources/deep-research-gap-analysis.md`.
Diese Datei existiert im Repo **nicht** (vorhanden sind stattdessen `final-gap-sweep-2026-05-21.md`,
`deck-audit-2026-05-21.md`, `dry-run-session-2-3-2026-05-21.md`).

**Empfehlung:** Referenz entfernen oder auf die tatsaechlich existierenden Gap-/Audit-Dateien
umbiegen. Gleichzeitig pruefen, ob `AGENTS.md` und `CLAUDE.md` (Struktur-/Regel-Abschnitte)
sonst noch auseinanderlaufen (Single-Source-Drift).

---

## C. Korrektur: Architekt-v1-Lauf war degeneriert — granulare Neu-Struktur IST empfohlen

**Wichtige Einordnung fuer die Umsetzungs-Instanz.**

Der erste Curriculum-Architekt-Agent im Workflow lieferte ein degeneriertes Ergebnis
(Zusammenfassung = "x", nur die bestehenden 3 Bloecke mit unrealistischen Dauern von
382/270 Min). Datei `04-restructuring-proposal.md` ist deshalb nur noch ein Redirect-Stub.

Die **Master-Synthese** (`01-executive-summary.md`) kam zum Verdikt *"Keine granulare
Neu-Struktur"* — dieses Verdikt beruht jedoch teilweise auf dem fehlerhaften Architekt-v1-Input
und steht im Widerspruch zum ausdruecklichen Kundenwunsch (granular aufspalten, weniger pro
Einheit, mehr Tiefe pro Thema).

**Korrigierte Empfehlung:** Ein zweiter, dedizierter Architekt-Lauf hat einen tragfaehigen,
granularen Vorschlag erzeugt — `04b-restructuring-proposal-v2.md` (17 Module → 48 Lerneinheiten,
core/deep-dive/bonus, Block 3 ehrlich in 3a/3b). Der valide Kern der Master-Synthese bleibt:
*nichts loeschen, vorhandene Reihenfolge entzerren, Cost Engineering entdichten*. Beides passt
zusammen: 04b setzt genau diese Entzerrung als Feingliederung um. **Die Umsetzungs-Instanz
sollte 04b als Grundlage nehmen, nicht das "Nein" der Synthese.**

---

## D. Hinweis zu den Uebungsideen-Zahlen

Der Workflow lieferte in Welle 1 **8** neue Uebungsideen (`05-new-exercises.md`). Da der
Kundenwunsch "ein paar extra verrueckte Ideen" eher mehr Bandbreite nahelegt, wurde eine
**zweite Welle mit 10 weiteren Uebungen** ergaenzt (`05b-new-exercises-welle-2.md`).
Gesamt: **18 neue Uebungs-/Engagement-Formate**, gemischt von Micro-Warmup (easy) bis
Red-Team-Wettbewerb (wild).

---

## E. Provenienz dieses Reviews

| Detail | Wert |
|---|---|
| Workflow-Run-ID | `wf_1603866b-421` |
| Datum | 2026-06-21 |
| Agenten gesamt | 22 (10 Personas + 2 Design-Erstlauf + 9 Konsolidierungs-Cluster + 1 Synthese, plus 2 Re-Runs) |
| Subagent-Tokens | ~2,2 Mio |
| Personas | 7 Lern-/Liefer-Personas + 3 Currency-Auditoren (Web-Recherche) |
| Methode | 4-Wellen-Orchestrierung: Durchspielen → Currency → Design → Konsolidierung → Synthese |
| Re-Runs (Kuratoren-Korrektur) | Curriculum-Architekt v2 (`04b`), Wild-Exercises Welle 2 (`05b`) |

**Wichtig:** Dieses Review-Verzeichnis aendert KEINEN Kursinhalt. Es ist die Analyse-Grundlage;
die Umsetzung der TODOs erfolgt durch eine separate Instanz. Bei jeder Inhaltsaenderung an
Modulen/Demos/Exercises gilt die Projektregel: auch `agents/workshop-mentor.md` nachziehen.
