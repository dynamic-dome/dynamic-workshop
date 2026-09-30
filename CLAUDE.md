# CLAUDE.md — Claude Code Praxisbibliothek

## Mission

Eine deutschsprachige Praxisbibliothek, mit der Entwicklerinnen und Entwickler Claude Code nach ihrem Stand lernen:
Einstufung → persönlicher Pfad → Kapitel. Zugleich das Material für einen moderierten Workshop in vier Sessions.
Zielgruppe: vor allem Selbstlernende (öffentlich); der Live-Workshop ist ein Pfad unter mehreren.

## Struktur

- `resources/library/` — Kapitel (einzige Quelle für Lehrinhalte), `_shelves.yaml`, `_placement.yaml`;
  `README.md`, `einstufung.md`, `catalog.json` und die Meta-Blöcke sind generiert
- `resources/paths/` (generiert) · `resources/reference/` (Karten; `analogien.md` generiert) · `resources/moderation/`
  · `resources/media/` (Deck, Videos) · `resources/demos/assets/hooks/` (getestete Vorlagen) · `resources/_canonical.md`
- `resources/claude-code-workshop-ui.html` — Lern-Cockpit, generiert aus `tools/cockpit/template.html`
- `tools/` — `build_library.py`, `placement.py`, `build_deck.py`, Aktualitäts-Tools, Tests
- `skills/workshop/`, `agents/workshop-mentor.md` — Tutor-Plugin · `workshop-playground/` — Übungsrepo (5 Schwachstellen)
- `docs/plans/` (Spec + Plan) · `docs/migration/` (Umzug, Verträge) · `docs/reviews/` (Archive, nicht editieren)

## Regeln

- Inhalte nur in den Kapiteln ändern, danach `python tools/build_library.py build` und `python -m pytest tools -q`.
  Generierte Dateien nie von Hand ändern.
- Kapitel: Deutsch mit Umlauten, „du"; Code, Befehle, Dateinamen, Bezeichner Englisch. Aufbau und Typen: Spec §4.
- Neue oder geänderte Fakten nur mit Beleg aus der offiziellen Doku (`curl -sL https://code.claude.com/docs/en/<seite>.md`,
  Zitat im Commit). `--help` ist nicht die Referenz.
- Modellgenerationen, Preise, Kontextgrößen und Retirement-Daten nur in `resources/_canonical.md`; im Material Aliase
  (`opus`, `sonnet`, `haiku`, `fable`) und Rollen. Ausnahme: `version-pinned: <Grund>` in derselben Zeile.
  `python tools/lint_currency.py` prüft das.
- Kopierbare Hooks sind getestete Vorlagen (`tested asset:`); Snippet und Datei bleiben identisch.
- Einstufung oder Kapitel-Metadaten ändern → Vertragskatalog, Personas und Golden bewusst neu (HOW-TO-USE §3).
- Tutor und Mentor halten keine Inhaltskopie; sie lesen Katalog und Kapitel.
- Demos vor Folien; Übungen sind freiwillig. Keine Tests gegen Produktionsdaten.

Anleitung: [HOW-TO-USE.md](HOW-TO-USE.md) · Spec: `docs/plans/2026-09-30-praxisbibliothek-design.md`
