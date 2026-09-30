# Migration: vom linearen Kurs zur Praxisbibliothek

Dieser Ordner hält fest, wie die Inhalte des Kurses (Stand `ba222d2`) in die Kapitel unter `resources/library/`
umgezogen sind und wie das geprüft wurde. Er ist Arbeitsnachweis, kein Lehrmaterial; `tools/lint_currency.py` klammert
`docs/` aus.

| Datei | Inhalt |
|---|---|
| `chapter-meta.yaml` | verbindliche Metadaten je Kapitel (ID, Typ, Regal, Stufe, Minuten, Reihenfolge, Voraussetzungen, Dateiname); der Validator gleicht jedes Kapitel dagegen ab (`meta-contract`) |
| `source-map.json` | Quellenkarte: alte Datei und Zeilen → Kapitel, mit Lernziel-Entwurf |
| `ownership.json` | Heimat je Quellzeile: jede Zeile der alten Dateien gehört genau einem Kapitel (keine Dubletten) |
| `cockpit-content-ba222d2.json` | Textbausteine des alten Cockpits (Konzept, Analogie, Beispiel, Quiz) als Quelle |
| `WRITER-BRIEF.md`, `VERIFIER-BRIEF.md` | verbindliche Aufträge an Schreib- und Prüf-Agenten |
| `claims/<ID>.json` | Aussagen-Matrix je Kapitel: jede Aussage behalten, geändert, gestrichen oder neu, mit Bewertung und Beleg |

Das Snippet-Ledger (`python tools/migration_ledger.py`) prüft, dass jeder Codeblock der alten Dateien unverändert in
einem Kapitel, einer Referenzkarte oder dem Moderations-Handbuch steht oder in `tools/fixtures/migration-dropped.txt`
begründet gestrichen ist.

## Ablauf

1. **Pilot** (Regal Hooks, S2.6–S2.10): ein Schreib-Agent, unabhängige Prüfer je Kapitel, Nachbesserung; die Lehren
   gingen als Nachträge 11–20 in den Schreib-Brief.
2. **Fan-out** der übrigen 63 Kapitel: 20 Schreib-Agenten (je Regal bzw. Regalteil), je Kapitel ein unabhängiger
   Prüfer (Aussagen-Matrix), bis zu zwei Nachbesserungsrunden für Befunde mit Bewertung `fix`.
3. **Community-Kapitel X.3 (Pi) und X.4 (OpenClaw)**: ohne alte Quelle, deshalb Faktendatei mit URL und wörtlichem Zitat
   je Aussage (X.3: 85, X.4: 131), Zitate per Skript und vom Prüfer live gegengeprüft.
4. **Orchestrator-Entscheidungen** zu allen Befunden mit Bewertung `ask` (Liste und Umsetzung siehe unten), danach
   erneute unabhängige Prüfung.

## Ergebnis

- **Urteile der Prüfer** über die 63 Fan-out-Kapitel: 40 `pass`, 23 `ask` (keine offenen `fix`), dazu die 5 Pilotkapitel
  und X.3 (`ask`, ein gefolgerter Satz, belassen) und X.4 (`pass`). Die `ask`-Befunde wurden als Liste entschieden und
  umgesetzt (u. a. `claude project purge` in S1.11, `/review` als Alias in S1.17, belegte NotebookLM-CLI in S2.18,
  korrigierte CI-YAML-Blöcke in S4.5, Quiz-Längenhinweise); die unabhängige Nachprüfung ergab `pass`.
- **X.1:** acht `ask`-Punkte, die der Prüfer selbst an den Primärquellen bestätigt hatte (README, `marketplace.json`,
  LICENSE); übernommen, der README-Installationsweg ergänzt, Spec-Anhang D nachgezogen.
- **Snippet-Ledger:** 355 alte Codeblöcke, alle erfasst; 60 begründet gestrichen (Dubletten, laut Doku veraltet oder
  korrigiert, durch den Windows-Hook-Fix ersetzt), Liste in `tools/fixtures/migration-dropped.txt`.
- **Regal-Intros:** vier sachlich falsche Intros korrigiert (headless-ci drehte die Gefahr um, remote-isolation
  schrieb Teleport das Handy zu, capstone versprach einen anderen Auftrag, automation Budget-Grenzen ohne `-p`).
- **Validator:** `python tools/build_library.py validate --complete` ohne Befunde (70 Kapitel).

## Stichprobe des Orchestrators (2026-09-30)

- **Zitate in den Matrizen:** Ein Skript zog aus jeder Matrix bis zu drei geänderte oder neue Aussagen, deren
  Begründung ein Zitat aus `code.claude.com/docs/en/*.md` nennt, und suchte jedes Zitat in der Live-Seite:
  143 Aussagen aus 57 Matrizen, 107 Zitate wörtlich gefunden. Die 36 übrigen stichprobenartig von Hand geprüft
  (u. a. S1.14 Plan-Modus, S2.2 `description`, S3.3 `--agents`, S3.4 Workflows, S3.5 `claude stop`, S3.7
  `/code-review ultra`, S2.13 `#ref`): Die Kapitelaussagen sind belegt; die Treffer scheiterten an Tabellen- und
  Codeblock-Formatierung der Doku oder an paraphrasierten Zitaten in der Begründung des Prüfers.
- **Community-Kapitel:** je drei Zitate aus den Faktendateien von X.3 und X.4 live nachgeprüft, 6 von 6 gefunden;
  Datenschutz-Sweep (private Pfade, Hosts, Bot- und Gruppennamen) ohne Treffer.
- **Vollständig gelesen:** S2.6–S2.10 (Pilot), X.3, X.4, S4.4 (Sicherheitsboden, CI-Zugang), S1.1 (Einstieg), S4.8 (Abschlussprojekt), S3.4 (Orchestrierung; die Aussage zu verschachtelten Subagenten an sub-agents.md bestätigt).
- **Gefundene Querschnittsfehler** (außerhalb der Matrizen, von Referenz-Agenten gemeldet und selbst an der Doku
  bestätigt): Shell-Hooks mit `"matcher": "Bash"` feuern unter Windows mit PowerShell-Tool nie (behoben in S2.8,
  S2.9, Moderation, Vorlagen, Guard-Test); `--plugin-dir` zeigte im Installer auf `.claude-plugin` statt auf den
  Plugin-Root (behoben).
