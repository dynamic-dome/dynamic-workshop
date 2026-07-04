# Dynamic Workshop — How To Use

## Kanonischer Einstieg

1. Lies `README.md` fuer Zielgruppe, Struktur und Quick Start.
2. Oeffne `resources/cloud-code-workshop-ui.html` als interaktive Haupt-UI. Sie ist die kanonische Lernoberflaeche fuer 48-Route und 65-LE-Gesamtkarte.
3. Nutze `resources/session-plan.md` als Single Source of Truth fuer Session-Reihenfolge, LE-IDs, Level und Zeitbudget.
4. Vertiefe pro Block in `resources/modules/`, fuehre passende Demos aus `resources/demos/` vor und waehle Exercises aus `resources/exercises/`.

## Fuer Agenten

- Bei Inhaltsaenderungen an Modulen, Demos oder Exercises immer `agents/workshop-mentor.md` mitpruefen.
- LE-Navigation erfolgt ueber die realen `<!-- LE: Sx.y -->`-Anker in den Moduldateien plus die Landkarten-Tabellen am Anfang der Module.
- `resources/cloud-code-workshop-ui.html` enthaelt den section-spezifischen UI-Content inline. Die fruehere externe `resources/sectionContent.json` war ein Generierungsartefakt und ist keine Quelle mehr.
- Die alte 9-Modul-Dashboard-UI ist archiviert; nicht als Trainer- oder Self-Learner-Einstieg verwenden.

## Verifikation

- UI-Aenderungen: Browser oeffnen, DevTools-Konsole pruefen, Route-Toggle/Suche/Done/Quiz testen.
- Playground-Checks: vor Python-Tests sicherstellen, dass keine Produktions-DB beruehrt wird. Dieses Repo hat nur das isolierte `workshop-playground`; historischer Check: `cd workshop-playground && python -m pytest -v`.
- Currency-Checks: `python tools/lint_currency.py`.
