# Delta-Bewertung 2026-09-28 — Befund-Schema

> Historisches Review-Archiv wie `review-2026-06-21/` und `review-2026-07-04/`: Befunde, kein Kursinhalt.
> Von `tools/lint_currency.py` ausgeklammert. Nach Abschluss nicht mehr editieren.

## Anlass

Seit dem letzten Stand (Kanon `_canonical.md` vom 2026-07-04, CLI v2.1.185, letzter Commit 2026-08-06)
haben sich Modelle und CLI weiterbewegt (2026-09-28: Opus 5.5, Fable 5.1, CLI 2.1.283). Die Zielgruppe
hat sich verschoben: Der Kurs wird vor allem als **öffentliches Selbstlern-Curriculum und Arbeitsprobe**
weitergebaut; der Live-3-Personen-Modus bleibt, hat aber keinen Vorrang.

Maßstäbe dieser Bewertung (Entscheid des Autors 2026-09-28):
1. **Welt-Delta** — Modelle und CLI: neu, geändert, weggefallen (`01-welt-delta.md`)
2. **Faktencheck** — stimmt, was der Kurs heute konkret behauptet? (`02-faktencheck.md`)
3. **Anthropic-Vergleich** — offizielles Lernmaterial und Doku (`03-anthropic-vergleich.md`)
4. **Praxis-Delta** — was der Autor seit Juli anders macht, als der Kurs lehrt (`04-praxis-delta.md`)

Die Didaktik wurde am 2026-07-04 voll geprüft (`review-2026-07-04/`) und wird nicht wiederholt.

## Pflichtformat je Befund

| Feld | Inhalt |
|---|---|
| ID | Präfix je Datei: `W-nn` (Welt), `F-nn` (Fakten), `A-nn` (Anthropic), `P-nn` (Praxis) |
| Art | `falsch` (stimmt heute nicht) · `veraltet` (stimmte mal, heute überholt) · `fehlt` (relevantes Thema nicht im Kurs) · `stärke` (Kurs hat etwas, das die Vergleichsquelle nicht hat) · `unklar` (nicht verifizierbar) |
| Schwere | `P1` Lernende scheitern oder lernen Falsches (kopierbarer Befehl bricht, falsche Aussage) · `P2` spürbare Lücke/Veraltung · `P3` Politur |
| Ort | `datei:zeile` im Kurs (bei `fehlt`: die LE aus `resources/session-plan.md`, an die es andocken würde) |
| Beleg | URL der offiziellen Quelle ODER Befehl + wörtliche Ausgabe. Ohne Beleg → Art `unklar`, nie raten |
| Vorschlag | ein Satz, was zu tun wäre |
| Aufwand | `S` (<30 Min) · `M` (<1 Tag) · `L` (mehr) |

Befunde als Markdown-Tabelle oder als je ein Block mit diesen Feldern. Am Dateiende: Zählung je Art und
Schwere, plus eine Liste „Was ich NICHT prüfen konnte und warum".

## Gesamtbewertung (füllt der Orchestrator in `05-bewertung.md`)

Skala 1–5 je Dimension, jeweils mit Begründung und Verweis auf Befund-IDs:
Aktualität · Fachliche Korrektheit · Abdeckung des heutigen Funktionsumfangs · Praxisnähe ·
Selbstlerntauglichkeit (neue Hauptzielgruppe) · Versprechenstreue (Website ↔ Kurs).
