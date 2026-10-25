# Architektur — dynamic_workshop

## Überblick

Die Kapitel unter `resources/library/` sind die einzige Quelle für Lehrinhalte. `tools/build_library.py` erzeugt daraus Katalog, Übersichten, Pfade und das Lern-Cockpit. Cockpit, Tutor-Plugin und Markdown-Seite lesen dieselbe Regeldatei für die Einstufung (Quelle: `docs/plans/2026-09-30-praxisbibliothek-design.md`, §1). Fakten zu Modellen und Preisen stehen nur im Kanon `resources/_canonical.md`.

## Komponentendiagramm

```
resources/library/<kapitel>.md (Frontmatter + Text)     _shelves.yaml     _placement.yaml
              |                                               |                 |
              +---------- tools/build_library.py build -------+-----------------+
                                     |
        +------------+---------------+-----------+----------------------+
        v            v               v           v                      v
   catalog.json  library/README   resources/   Meta-Blöcke     tools/build_cockpit.py
   einstufung.md                  paths/       in Kapiteln      -> claude-code-workshop-ui.html
                                  (generiert)                    (aus tools/cockpit/template.html)

catalog.json ------> tools/build_deck.py --> resources/media/*.pptx
catalog.json + skills/workshop/SKILL.md --> Tutor /dynamic-workshop:workshop
resources/_canonical.md --> tools/lint_currency.py, tools/currency_check.py (Monatslauf)
```

## Kernkomponenten

### Kapitel und Quellen
- **Datei(en):** `resources/library/*.md`, `_shelves.yaml`, `_placement.yaml`, Vertrag `docs/migration/chapter-meta.yaml`
- **Aufgabe:** Lehrinhalt, Übung, Quiz, Schnellcheck; Reihenfolge, Stufe, Minuten und Voraussetzungen im Frontmatter
- **Abhängigkeiten:** keine; generierte Dateien (`README.md`, `einstufung.md`, `catalog.json`, Meta-Blöcke) werden daraus gebaut

### Build und Validierung
- **Datei(en):** `tools/build_library.py`, `library_model.py`, `library_generate.py`, `catalog_core.py`
- **Aufgabe:** `validate --complete` (Format, Verweise, Quiz, Vollständigkeit), `build`, `check` (prüft ohne zu schreiben, auch Mermaid zu SVG)
- **Abhängigkeiten:** `pyyaml`, `markdown`

### Einstufung
- **Datei(en):** `tools/placement.py`, JS-Port im Cockpit-Template, Fixtures `tools/fixtures/placement-*.json`
- **Aufgabe:** berechnet Empfehlung und Pfad aus der Einstufung
- **Abhängigkeiten:** `catalog.json`; Python-Engine und JS-Port müssen gleich bleiben (`tools/test_placement_js.py`)

### Cockpit
- **Datei(en):** `tools/build_cockpit.py`, `tools/cockpit/template.html`, `resources/claude-code-workshop-ui.html`
- **Aufgabe:** Lern-Oberfläche im Browser, Fortschritt im Browser
- **Abhängigkeiten:** Katalog, optional SVG-Diagramme aus `tools/render_diagrams.py` (ohne SVG zeigt das Cockpit den Mermaid-Quelltext)

### Tutor und Mentor
- **Datei(en):** `skills/workshop/` (`SKILL.md`, `MISSION-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`), `agents/workshop-mentor.md`, `.claude-plugin/plugin.json`, `tools/install_workshop_plugin.ps1`
- **Aufgabe:** begleitet Lernende kapitelweise; schreibt nur in den Lernordner (Vorschlag `~/cc-workshop/lernen`)
- **Abhängigkeiten:** Katalog und Kapitel (keine Inhaltskopie)

### Aktualität
- **Datei(en):** `resources/_canonical.md`, `tools/lint_currency.py`, `tools/currency_check.py`, `tools/currency_extract.py`, `tools/currency_exceptions.txt`
- **Aufgabe:** hält Modell-, Preis- und CLI-Aussagen an genau einer Stelle und vergleicht Kurs-Bezeichner mit der offiziellen Doku
- **Abhängigkeiten:** Netzzugriff auf die offizielle Doku für `currency_check.py`; der Monatslauf selbst läuft privat außerhalb des Repos (`docs/plans/2026-09-29-phase2-aktualhaltung-design.md`, §5)

## Datenfluss (Pflege)

1. Kapitel, Regale oder Einstufungsregeln ändern.
2. `python tools/build_library.py validate --complete`, danach `build`.
3. `python -m pytest tools -q` und `python tools/lint_currency.py`.
4. Bei Änderung der Einstufung: `python tools/catalog_core.py --from-meta`, Personas und Golden-Datei bewusst neu schreiben.
5. Cockpit-Export auf die Website: Owner-Seite, eigenes Repo.

Quelle: `HOW-TO-USE.md` §3.

## Persistenz

| Speicher | Typ | Pfad | Inhalt |
|---|---|---|---|
| Katalog | JSON | `resources/library/catalog.json` | Kapitel, Regale, Einstufung (generiert) |
| Aktualitätszustand | Dateien | `.currency/` | Berichte und Zustand des Prüflaufs (in `.gitignore`) |
| Lernfortschritt | Browser | im Cockpit | Fortschritt der Lernenden |
| Lernordner | Dateien | `~/cc-workshop/lernen` (Vorschlag) | Mission und Lernprotokolle des Tutors |

Es gibt keine Datenbank im Repo.

## Sicherheit

- Der Tutor schreibt nur in den Lernordner der Person (`HOW-TO-USE.md` §1).
- Kopierbare Hooks sind getestete Vorlagen; Snippet und Datei bleiben identisch (`CLAUDE.md`).
- Der Sicherheitsboden der Kapitel (z. B. `exit 2` blockt einen Hook, `claude -p` ohne `--bare` führt Hooks eines fremden Repos aus) steht in `README.md`.
