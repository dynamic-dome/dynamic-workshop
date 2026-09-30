# Kosten-Nachbau: was der ganze Kurs etwa kostet

Wofür: abschätzen, was es kostet, alle Vorführungen und Pflichtübungen des Live-Workshops mit dem eigenen Konto
nachzumachen.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285): Flags und Abrechnungshinweise. Offizielle Quelle: https://code.claude.com/docs/en/costs

> Die Spannen sind Schätzungen aus dem alten Session-Plan (Stand 2026-06-23) und seitdem nicht neu gemessen. Preise pro
> Token stehen nur im [Kanon](../_canonical.md). Im Pro- oder Max-Abo ist die Nutzung im Abo enthalten; der Dollarbetrag
> in `/usage` ist dort eine Schätzung und für die Abrechnung nicht maßgeblich, es zählen die Plan-Limits.

## Spanne je Session

| Session | Aktivitäten | Spanne |
|---|---|---:|
| 1 · Grundlagen | Vorführungen in [S1.1](../library/s1-01-erster-kontakt.md), [S1.10](../library/s1-10-claude-md.md), [S1.13](../library/s1-13-vager-und-praeziser-auftrag.md), [S1.16](../library/s1-16-git-in-einem-fluss.md), eine Übung, Kosten-Grundlagen ([S1.19](../library/s1-19-kosten-im-blick.md)) | 1–3 $ |
| 2 · Ökosystem | Vorführungen in [S2.2](../library/s2-02-skill-schreiben.md), [S2.8](../library/s2-08-hook-einrichten.md), [S2.10](../library/s2-10-hook-ausgaben.md), [S2.11](../library/s2-11-plugins-buendeln.md), [S2.14](../library/s2-14-mcp-stecker.md), [S2.18](../library/s2-18-rag-und-notebooklm.md), zwei bis drei Übungen | 5–15 $ |
| 3 · Fortgeschritten, Kern | Vorführungen in [S3.4](../library/s3-04-orchestrierungsmuster.md), [S3.6](../library/s3-06-devils-advocate.md), [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md), eine Übung, Self-Improve-Loop (Bonus, [S3.14](../library/s3-14-self-improve-loop.md)) | 10–35 $ |
| 4 · Fortgeschritten, Bonus | Vorführungen in [S4.2](../library/s4-02-codex-schwarm.md), [S4.3](../library/s4-03-headless.md), [S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md), Abschlussprojekt ([S4.8](../library/s4-08-abschlussprojekt.md)), CI und Kosten ([S4.4](../library/s4-04-ci-zugang-und-kosten.md), [S4.5](../library/s4-05-ci-pipelines.md)) | 8–25 $ |
| **Gesamt** | | **24–78 $** |

## Was die Kosten nach oben treibt

- mehrere Iterationen von `/agentic-os:run-loop` im Self-Improve-Loop ([S3.14](../library/s3-14-self-improve-loop.md), Bonus)
- parallele Agenten im Codex-Schwarm ([S4.2](../library/s4-02-codex-schwarm.md), Bonus)
- Multi-Agent-Orchestrierung in [S3.1](../library/s3-01-was-ist-ein-agent.md) bis [S3.4](../library/s3-04-orchestrierungsmuster.md) und im Abschlussprojekt ([S4.8](../library/s4-08-abschlussprojekt.md))

## Wie du am unteren Ende bleibst

- `claude --bare -p` für Vorführungen im Stapel: spart den Lade-Aufwand, braucht aber einen API-Key, denn `--bare` liest kein Abo-Token ([S4.4](../library/s4-04-ci-zugang-und-kosten.md)).
- `--max-budget-usd 0.50` und `--max-turns` für autonome `-p`-Schleifen: Das Budget begrenzt die Kosten, das Rundenlimit die Schleife. `--max-turns` steht in der CLI-Referenz, fehlt aber in `claude --help`.
- `haiku` für Läufe, die nur eine Kosten-Basislinie liefern sollen; vorher mit `/model` prüfen, worauf der Alias auflöst.

## Welches Konto

- **Moderierende:** ein Pro- oder Max-Konto mit mindestens 50 $ Budget für sichere Live-Vorführungen.
- **Selbstlernende:** Ein Pro-Abo reicht für die Kapitel ohne Multi-Agent-Arbeit ([Preise der Abos](https://claude.com/pricing)).
  Für Self-Improve-Loop und Codex-Schwarm empfiehlt sich ein API-Key mit nutzungsabhängiger Abrechnung.

## Mehr dazu

- [Kostenkarte](karte-kosten.md) · [S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen](../library/s1-19-kosten-im-blick.md) · [S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](../library/s4-04-ci-zugang-und-kosten.md)
- Doku: [Kosten](https://code.claude.com/docs/en/costs) · [CLI-Referenz](https://code.claude.com/docs/en/cli-reference)
