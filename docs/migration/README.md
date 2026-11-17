# Migration: vom linearen Kurs zur Praxisbibliothek

Dieser Ordner hält die beiden Verträge fest, gegen die Werkzeuge und Tests prüfen. Er ist kein Lehrmaterial;
`tools/lint_currency.py` klammert `docs/` aus. Der Umzug der Inhalte des Kurses (Stand `ba222d2`) in die Kapitel unter
`resources/library/` ist abgeschlossen; die Arbeitsprotokolle dazu sind nicht Teil des öffentlichen Repos.

| Datei | Inhalt |
|---|---|
| `chapter-meta.yaml` | verbindliche Metadaten je Kapitel (ID, Typ, Regal, Stufe, Minuten, Reihenfolge, Voraussetzungen, Dateiname); der Validator gleicht jedes Kapitel dagegen ab (`meta-contract`), Deck und Einstufungstests lesen sie ebenfalls |
| `ownership.json` | Heimat je Quellzeile: jede Zeile der alten Dateien gehört genau einem Kapitel (keine Dubletten) |

Das Snippet-Ledger (`python tools/migration_ledger.py`) prüft, dass jeder Codeblock der alten Dateien unverändert in
einem Kapitel, einer Referenzkarte oder dem Moderations-Handbuch steht oder in `tools/fixtures/migration-dropped.txt`
begründet gestrichen ist.
