# Fähigkeiten — dynamic_workshop

Die Daten in der Spalte „Seit“ sind das Datum des ersten Commits der Datei bzw. des Ordners (`git log --diff-filter=A`). Bei Dateien, die später neu angelegt wurden, kann der Inhalt älter sein.

## Tools und Bestandteile

| Tool / Feature | Status | Seit | Beschreibung |
|---|---|---|---|
| Kapitel `resources/library/` | aktiv | 2026-09-30 | 71 Kapitel in 19 Regalen, einzige Quelle für Lehrinhalte; `_shelves.yaml` und `_placement.yaml` steuern Regale und Einstufung |
| `tools/build_library.py` | aktiv | 2026-09-30 | `validate --complete`, `build`, `check`: erzeugt Katalog, Übersichten, Pfade, Meta-Blöcke, Cockpit |
| `tools/placement.py` | aktiv | 2026-09-30 | Einstufungs-Engine (Python); JS-Port im Cockpit, Gleichstand prüft `tools/test_placement_js.py` |
| Lern-Cockpit `resources/claude-code-workshop-ui.html` | aktiv | 2026-09-30 (Generator `tools/build_cockpit.py`) | Einstufung, Gebäudeplan, Pfad mit Etappen, Fortschritt im Browser; generiert aus `tools/cockpit/template.html` |
| Tutor-Plugin `dynamic-workshop` | aktiv | 2026-04-09 | `skills/workshop/SKILL.md` mit `/dynamic-workshop:workshop` (start, next, learn, review, guide); Installation per `tools/install_workshop_plugin.ps1` |
| Mentor-Agent `agents/workshop-mentor.md` | aktiv | 2026-04-09 | beantwortet Fragen zum Stoff; hält keine Inhaltskopie, liest Katalog und Kapitel |
| Hook-Vorlagen `resources/demos/assets/hooks/` | aktiv | 2026-06-22 | getestete Vorlagen (`.sh`, `.py`, `.ps1`) als Quelle für kopierbare Hooks |
| Playground `workshop-playground/` | aktiv | 2026-04-09 | Übungsrepo mit fünf eingebauten Schwachstellen und eigenen Tests |
| Foliensatz `tools/build_deck.py` | aktiv | 2026-07-04 | baut `resources/media/claude-code-praxisbibliothek.pptx` aus dem Katalog |
| Diagramme `tools/render_diagrams.py` | aktiv | 2026-09-30 | rendert Mermaid-Blöcke zu SVG für das Cockpit |
| Cockpit-Bilder `tools/cockpit_shots.py` | aktiv | 2026-10-06 | Bilder aller Cockpit-Ansichten per Browser |
| Aktualitätskanon `resources/_canonical.md` | aktiv | 2026-07-04 | einzige Stelle für Modellgenerationen, Preise, Kontextgrößen, Retirement-Daten |
| `tools/lint_currency.py` | aktiv | 2026-07-04 | prüft, dass Modellgenerationen nur im Kanon stehen |
| `tools/currency_check.py` | aktiv | 2026-09-29 | vergleicht Kurs-Bezeichner und Fremdprojekte mit der offiziellen Doku; Bericht unter `.currency/` (nicht versioniert) |
| `tools/workshop_doctor.ps1` | aktiv | 2026-07-04 | Umgebungsprüfung (PowerShell) |
| Moderationsunterlagen `resources/moderation/` | aktiv | 2026-09-30 | Handbuch, Vorbereitung, Video-Transkripte, Demo und Hinweise je Kapitel unter `vorfuehren/` |
| `tools/migration_ledger.py`, `tools/sweep_sonnet5.py` | einmalig | 2026-09-30 / 2026-07-04 | Umzugs-Ledger bzw. einmaliger Rename-Sweep (laut Kopf der Dateien); nicht Teil des laufenden Betriebs |

Status-Werte: `aktiv`, `experimentell`, `geplant`, `deprecated`, `entfernt`, `einmalig`.

## Tests

- 20 Testdateien `tools/test_*.py` (`ls tools/test_*.py | wc -l`), Aufruf `python -m pytest tools -q`.
- Das Repo hat keine Datenbank; die Playground-Tests laufen nur in `workshop-playground/` (`HOW-TO-USE.md` §3).

## Einschränkungen

- Generierte Dateien nie von Hand ändern (Cockpit, Katalog, Pfade, Meta-Blöcke, `analogien.md`); siehe `CLAUDE.md`.
- Der Export des Cockpits auf die Website ist nicht Teil dieses Repos.
- Aussagen über Modelle, Preise und CLI-Stand gelten nur so weit, wie der Kanon (Prüfdatum 2026-10-25) sie trägt.
