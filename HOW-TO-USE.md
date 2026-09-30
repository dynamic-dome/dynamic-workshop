# Anleitung: lernen, moderieren, pflegen

> Das [README](README.md) sagt, was hier liegt. Diese Seite sagt, wie du damit arbeitest.

## 1 · Selbst lernen

**Einrichten.** Kapitel [S0.1 Werkstatt einrichten](resources/library/s0-01-werkstatt-einrichten.md): Claude Code
installieren und anmelden, Git und Python prüfen, Arbeitsordner `~/cc-workshop` anlegen. Unter Windows funktionieren alle
Beispiele in Git Bash; wo es nötig ist, stehen PowerShell-Varianten daneben.

**Einstufen.** Fünf Minuten, keine Noten, jederzeit änderbar — auf einer von drei Oberflächen:

| Oberfläche | Wie | Stärke |
|---|---|---|
| Lern-Cockpit | [`resources/claude-code-workshop-ui.html`](resources/claude-code-workshop-ui.html) im Browser öffnen | Gebäudeplan der Bibliothek, Pfad mit Etappen, Fortschritt im Browser |
| Tutor in Claude Code | Plugin laden (unten), dann `/dynamic-workshop:workshop start` | begleitet dich Kapitel für Kapitel und prüft deine Übungen |
| Markdown | [`resources/library/einstufung.md`](resources/library/einstufung.md) lesen | ohne Werkzeug, direkt auf GitHub |

Ohne Einstufung: ein [fertiger Pfad](resources/paths/README.md) oder die [Bibliothek](resources/library/README.md).

**Ein Kapitel durcharbeiten.** Jedes Kapitel hat denselben Aufbau. Eine gute Routine für eine Lernsitzung:

1. **Schnellcheck** — kannst du beide Fragen sicher beantworten, geh zum nächsten Kapitel.
2. **Auf einen Blick** und **Bild im Kopf** lesen.
3. **Selbst machen** im [Playground](workshop-playground/) oder in einem eigenen, unkritischen Repo — nicht nur lesen.
4. **Check** ohne Nachsehen beantworten; das Quiz gibt Rückmeldung, bucht aber nichts.
5. Als erledigt markieren. Nach ein paar Tagen im Cockpit **Wiederholen** oder `/workshop review`: Abrufen aus dem
   Gedächtnis festigt mehr als erneutes Lesen.

**Den Tutor laden.** Das Repository ist zugleich ein Claude-Code-Plugin (`dynamic-workshop`):

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_workshop_plugin.ps1
```

Das Skript klont oder aktualisiert das Repo nach `~/cc-workshop/dynamic-workshop`. Dann eine Sitzung mit dem Plugin starten:

```bash
claude --plugin-dir ~/cc-workshop/dynamic-workshop
```

In der Sitzung: `/dynamic-workshop:workshop start` (Einstufung und Lernordner), `… next`, `… learn S2.8`, `… review`,
`… guide S3`. Der Tutor schreibt nur in deinen Lernordner (Vorschlag `~/cc-workshop/lernen`); Fragen zum Stoff
beantwortet auf Wunsch der Mentor-Agent („frag den Mentor").

**Den Playground prüfen:**

```bash
cd workshop-playground
pip3 install -r requirements.txt   # Windows: pip install -r requirements.txt
python3 -m pytest -v               # Windows: python -m pytest -v
```

## 2 · Moderieren

- Einstieg: [`resources/moderation/README.md`](resources/moderation/README.md) — Handbuch (Ablauf, Zeiten, Live-Format mit
  drei Personen, Recall-Opener, Transfer), Vorbereitung (Plugins, Assets, Checklisten) und Video-Transkripte.
- Reihenfolge und Minuten der vier Sessions: [`resources/paths/live-workshop.md`](resources/paths/live-workshop.md) (generiert).
- Foliensatz für den Einstieg jeder Session: [`resources/media/claude-code-praxisbibliothek.pptx`](resources/media/claude-code-praxisbibliothek.pptx)
  — Diagramme als bearbeitbare Formen, Sprechernotizen auf Deutsch.
- Im Kapitel steht unter „Vorführen" die Demo; Talking Points und Recovery-Hinweise liegen dort in „Für Moderierende".
- Co-Pilot während der Session: `/dynamic-workshop:workshop guide S1` bis `guide S4` oder `guide <Kapitel>`.

## 3 · Pflegen (Maintainer und Agenten)

**Quellenhoheit — jede Information hat genau eine Quelle:**

| Information | Quelle | Daraus erzeugt |
|---|---|---|
| Lehrinhalt, Demo, Übung, Quiz, Schnellcheck | `resources/library/<kapitel>.md` | Cockpit, Katalog, Referenz `analogien.md` |
| Reihenfolge, Stufe, Minuten, Voraussetzungen | Frontmatter der Kapitel (Vertrag: `docs/migration/chapter-meta.yaml`) | Pfade, Katalog, Deck |
| Regale | `resources/library/_shelves.yaml` | Bibliotheks-Übersicht, Cockpit, Deck |
| Einstufung (Fragen, Regeln, Texte) | `resources/library/_placement.yaml` | Katalog, `einstufung.md`, Pfade |
| Modelle, Preise, Prüfdatum | `resources/_canonical.md` | — |
| Moderation | `resources/moderation/` | — |

**Nach jeder Änderung an Kapiteln, Regalen oder Regeln:**

```bash
python tools/build_library.py validate --complete   # Format, Verweise, Quiz, Vollständigkeit
python tools/build_library.py build                 # Katalog, Übersichten, Pfade, Meta-Blöcke, Cockpit
python -m pytest tools -q                           # alle Wächter, Engine Python und JS, Browser-Tests
python tools/lint_currency.py                       # Modellgenerationen nur im Kanon
```

`python tools/build_library.py check` prüft ohne zu schreiben, ob alle generierten Dateien aktuell sind.

- **Einstufung ändern** (`_placement.yaml` oder Metadaten eines Kapitels): `python tools/catalog_core.py --from-meta`
  erzeugt den Vertragskatalog neu; danach die Personas in `tools/fixtures/placement-vectors.json` prüfen und die
  Golden-Datei bewusst neu schreiben. Python-Engine (`tools/placement.py`) und JS-Port im Cockpit müssen gleich bleiben
  — `tools/test_placement_js.py` prüft das.
- **Aktualität:** `python tools/currency_check.py --state-dir .currency/manual` vergleicht Kurs-Bezeichner mit der
  offiziellen Doku (Bericht unter `.currency/manual/reports/`). Danach `Geprüft:` im Kanon setzen. Fremdprojekte der
  Community-Kapitel stehen im Kanon als `- Fremdprojekt: <url> (<Kapitel>)`; ändert sich eine dieser Seiten, meldet der
  Lauf das gelb mit Kapitel — dann das Kapitel gegen die Quelle prüfen und sein „Stand:"-Datum erneuern.
- **Deck:** `python tools/build_deck.py` baut den Foliensatz aus dem Katalog.
- **Diagramme fürs Cockpit** (optional): `python tools/render_diagrams.py`; ohne SVG zeigt das Cockpit den
  Mermaid-Quelltext.
- **Website:** Das Cockpit wird als eigene Datei auf dynamic-dome.com exportiert — das macht die Owner-Seite
  (eigenes Repo); der Monatslauf meldet eine Abweichung.
- Pflege-Abhängigkeiten: `pip install pyyaml markdown python-pptx playwright` und Node für `node --check`. Lernende
  brauchen nur Python (Standardbibliothek) für den Tutor.
- Keine Tests gegen Produktionsdaten: Dieses Repo hat keine Datenbank; die Playground-Tests laufen nur in `workshop-playground/`.
