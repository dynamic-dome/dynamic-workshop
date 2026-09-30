# Dynamic Workshop — Persona-Review & TODO-Backlog (2026-06-21)

> Multi-Agent-Review des gesamten Claude-Code-Workshops aus 10 Personas + 2 Design-Rollen.
> Erzeugt per Workflow-Orchestrierung (Run `wf_1603866b-421`). Dieses Verzeichnis ist die
> Analyse-Grundlage fuer eine spaetere Umsetzungs-Instanz — es aendert KEINEN Kursinhalt.

## Kennzahlen

| Metrik | Wert |
|---|---:|
| Personas / Audit-Rollen | 10 |
| Roh-Befunde | 129 |
| Konsolidierte Cluster | 9 |
| Atomare TODOs | 87 |
| Neue Uebungsideen | 18 (8 Welle 1 + 10 Welle 2) |

## Dateien (Lese-Reihenfolge)

| Datei | Inhalt |
|---|---|
| `01-executive-summary.md` | Management-Synthese: Gesamturteil, Top-Themen, Quick Wins, Roadmap, Struktur-Empfehlung |
| `02-todo-backlog.md` | **Das zentrale Liefer-Artefakt** — alle 87 TODOs, priorisiert (P0-P3, mit Akzeptanzkriterium) |
| `03-currency-report.md` | Aktualitaets-Befunde mit Web-Quellen (Modelle, CLI, Ecosystem) |
| `04b-restructuring-proposal-v2.md` | **Granularer Neu-Schnitt** des Curriculums: 17 Module → 48 Lerneinheiten (core/deep-dive/bonus) |
| `04-restructuring-proposal.md` | (degenerierter v1-Lauf — nur Redirect-Stub auf 04b) |
| `05-new-exercises.md` | Neue & 'verrueckte' Uebungen — Welle 1 (Nr. 1-8) |
| `05b-new-exercises-welle-2.md` | Neue & 'verrueckte' Uebungen — Welle 2 (Nr. 9-18) |
| `06-all-findings.md` | Anhang: alle 129 Roh-Befunde nach Persona |
| `07-curator-addenda.md` | **Wichtig:** manuelle Zusatz-Befunde + Korrekturen (AGENTS.md-Bug, Architekt-v1-Korrektur) |
| `personas/` | Eine Persona-Karte + Report je Persona (10 Stueck) |
| `data/` | Maschinenlesbar: findings.json, todos.json, raw-workflow-output.json |

## Methode

Welle 1 (parallel): 7 Lern-/Liefer-Personas spielen den Kurs durch + 3 Currency-Auditoren
(Web-Recherche). Welle 2: Curriculum-Architekt + Wild-Exercise-Designer. Welle 3: gruppenweise
Konsolidierung je Kategorie -> atomare TODOs. Welle 4: Master-Synthese. Danach 2 Kuratoren-Re-Runs
(Architekt v2 = `04b`, Wild-Exercises Welle 2 = `05b`), weil der Architekt-Erstlauf degeneriert war
(siehe `07-curator-addenda.md`).
