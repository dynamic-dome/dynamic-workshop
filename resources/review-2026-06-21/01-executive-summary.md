# Executive Summary — Workshop-Review 2026-06-21

Workshop inhaltlich stark, im Kern durchfuehrbar, Feinschliff fehlt. Drei Schwaechen: hohe Einstiegshuerde Block 1 und 3.3, Windows-Inkompatibilitaet der Hooks, harte verifizierte Blocker. Plus Modell-Drift 4.7 statt 4.8, Fable 5 fehlt. Nichts loeschen, Quick-Wins plus didaktische Treppe.

## Top-Themen

| Thema | Impact |
|---|---|
| Einstiegshuerde Block 1 und 3.3 | HOCH Lernerfolg |
| Windows-Inkompatibilitaet Hooks | HOCH Durchfuehrbarkeit |
| Harte Blocker Flag Hook Crash | HOCH Blocker |
| Glaubwuerdigkeit OSDP | HOCH Vertrauen |
| Currency-Drift | MITTEL-HOCH Korrektheit |
| Single-Source Navigation | MITTEL Solo |
| Zielgruppen-Tiefe | MITTEL Differenzierung |

## Quick Wins (zuerst angehen)

- P0 Currency-Sweep 22 Opus-4-x auf 4.8, Versionsanker. S.
- P0 Exercise 3.6 Turn-Flag entfernen. S.
- P0 Header-Bug Three zu Five Interfaces. S.
- P0 worktree-baseRef vereinheitlichen. S.
- P1 3.6-Hook nicht ins Eltern-Repo. S.
- P1 size-t-Unterlauf absichern. S.
- P1 python3 zu python im Setup. S.
- P1 Cheatsheet-Hook-Bruecke. S.
- P1 README-Selbstlernpfad verlinken. S.
- P1 settings.json nicht ueberschreiben. S.
- P1 Block-3-Titel Single Source. S.
- P1 acceptEdits rm klarstellen. S.

## Umsetzungs-Roadmap

### Phase 1 Quick Wins und Currency — Vertrauen sofort herstellen.

- Currency-Sweep 4.8, Versionsanker, Fable 5
- Exercise 3.6 und Hook-Ziel fixen
- Header-Bug, worktree-baseRef, acceptEdits
- size-t-Unterlauf absichern
- README verlinken
- Block-3-Titel angleichen

### Phase 2 Windows und Live — Pflicht-Pfade laufen auf Windows.

- python3 zu python, Hook-Bruecke
- Hook-Pfad Windows, secure-diff-gate-Asset
- bash gegen pwsh aufloesen
- POSIX-Haertung
- Go-No-Go-Matrix, Preflight
- settings-Schutz

### Phase 3 Didaktik und Tiefe — Einstiegshuerde senken.

- Block 1 und 3.3 leicht zu schwer
- 60-Sekunden-Hello vor 1.1
- OSDP-Playground korrigieren
- Domaenen-Uebung OSDP oder Wiegand
- Erwartungen 1.2 und 3.3 relativieren
- Learn-Mode-Preflight

### Phase 4 Veredelung optional — Feinheiten und Timing.

- accuracy-Funde, debug-Traces
- FAQ, Custom-Komponenten trennen
- Timing entzerren
- Optionale Uebungen CTF, Honeypot
- mentor nachziehen

## Empfehlung zur Neu-Struktur

Keine granulare Neu-Struktur. Der 3-Block-Schnitt S1, S2, S3 ist tragfaehig, aber mit zwei Korrekturen. Slot-Dauern unrealistisch: S2 382 und S3 270 Minuten sprengen die je 180, pro Block 180 Minuten Kern plus Vertiefung. Hauptproblem ist die Reihenfolge in den Modulen, nicht die Granularitaet. Modul 1.5 Cost Engineering in Vertiefung verschieben, Block-3 als Single Source konsolidieren.

## Risiken

- Currency verfaellt ohne Versionsanker.
- Scope-Creep, Uebungen optional halten.
- OSDP-Korrektur gegen Spec belegen.
- Live-Tooling kippt, Go-No-Go noetig.
- Eltern-Repo, Fixes im Klon.
- mentor und Navigation nachziehen.