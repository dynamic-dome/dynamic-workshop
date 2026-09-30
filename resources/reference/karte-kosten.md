# Karte: Kosten, Modell und Effort

Wofür: Modell und Effort passend zur Aufgabe wählen, den Verbrauch lesen und unbeaufsichtigte Läufe begrenzen.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/costs

> Zahlen stehen nicht auf dieser Karte. Modellgenerationen, Preise, Kontextgrößen und den Start-Effort je Modell führt nur der [Kanon](../_canonical.md). Worauf ein Alias bei dir gerade auflöst, zeigt `/model`.

## Modell nach Aufgabe

| Aufgabe | Alias | Warum |
|---|---|---|
| Architektur, Planung, Root-Cause-Analyse | `opus` | Default in Claude Code, tiefes Reasoning |
| Die härtesten, lang laufenden Aufgaben | `fable` | Premium-Tier über `opus`, nie Account-Default |
| Standard-Coding, Refactors | `sonnet` | erledigt die meisten Coding-Aufgaben gut und kostet weniger als `opus` |
| Bulk-Reads, einfache Suchen, Routine-Reviews | `haiku` | kleinstes Tier; für einfache Subagenten `model: haiku` im Frontmatter |

Muster „Modell pro Phase": planen mit `opus`, umsetzen mit `sonnet`, Routine-Prüfung mit `haiku` ([S4.1](../library/s4-01-modell-pro-phase.md)). Der Alias `opusplan` nimmt Opus im Plan-Modus und danach Sonnet. Wechseln mit `/model`, für eine Sitzung mit `--model <alias>`.

## Effort nach Aufgabe

| Stufe | Wofür |
|---|---|
| `low` | triviale Aufgaben: Kommentar korrigieren, einfache Lookups |
| `medium` | Standard-Coding |
| `high` | Refactors, schwierigere Bugs |
| `xhigh`, `max` | Architektur-Entscheidungen, komplexe Root-Cause-Analyse |

Mehr Effort heißt mehr Tiefe, aber auch mehr Latenz und Kosten. Setzen mit `/effort <stufe>` (dazu `auto` und `status`), mit den Pfeiltasten im `/model`-Picker oder mit `--effort <stufe>` für eine Sitzung. Welche Stufen ein Modell kennt und womit es startet, steht im Kanon; das Haiku-Tier kennt keinen Effort, und eine Stufe, die das Modell nicht kann, fällt auf die nächstniedrigere unterstützte zurück.

## Verbrauch lesen

| Werkzeug | Zeigt |
|---|---|
| `/usage` (Aliase `/cost`, `/stats`) | Kosten der Sitzung, Plan-Limits, Aktivität; im Abo auch, was gegen die Limits zählt |
| `/context` | was das Kontextfenster füllt ([S1.8](../library/s1-08-kontextfenster.md)) |
| `/insights` | HTML-Bericht über deine Arbeitsweise, nicht über Token; der Lauf verbraucht selbst Token |
| Statuszeile | Kosten und Kontext dauerhaft im Blick |
| Usage-Seite der Claude Console | die verbindliche Abrechnung bei API-Nutzung |

## Budget und Rundenlimit (nur mit `-p`)

| Flag | Wirkung |
|---|---|
| `--max-budget-usd <betrag>` | stoppt, sobald die Ausgaben den Betrag erreichen; Subagenten zählen mit; bei `--continue` oder `--resume` zählen frühere Läufe nicht |
| `--max-turns <n>` | begrenzt die Agenten-Runden und endet mit einem Fehler; ohne das Flag gibt es kein Limit; steht in der CLI-Referenz, fehlt aber in `claude --help` |

Das Budget begrenzt die Kosten, das Rundenlimit die Schleife: In CI und bei Loops setzt du beide ([S3.13](../library/s3-13-autonome-loops-absichern.md), [S4.4](../library/s4-04-ci-zugang-und-kosten.md)). In einer interaktiven Sitzung wirken beide Flags nicht.

## Kosten senken

Kostentreiber sind `opus` statt `sonnet`, `xhigh` oder `max`, viele parallele Subagenten (jeder mit eigenem Kontext) und eine ausufernde `CLAUDE.md`, die in jeder Sitzung mitlädt ([S1.10](../library/s1-10-claude-md.md)). Die Hebel dagegen:

- `sonnet` oder `haiku` statt `opus`, wo es reicht; Effort für einfache Aufgaben senken; Subagenten nur, wo sie nötig sind.
- `/compact`, bevor die Sitzung ausufert ([S1.9](../library/s1-09-kontext-steuern.md)).
- `--bare` für Skripte: keine automatische Erkennung von Hooks, Skills, Plugins, MCP-Servern und `CLAUDE.md` ([S4.3](../library/s4-03-headless.md)).
- Prompt-Caching: Kurz aufeinanderfolgende Aufrufe nutzen den Cache; nach einer längeren Pause wird der ganze Kontext neu verarbeitet.

## Typische Fallen

- Im Pro- oder Max-Abo ist der Dollarbetrag in `/usage` eine Schätzung zu Listenpreisen und für die Abrechnung nicht maßgeblich; dort zählen die Plan-Limits.
- `/model` und `/effort` speichern deine Wahl als Standard für neue Sitzungen. Nur für diese Sitzung: im Picker oder Regler `s` drücken. `max` gilt ohnehin nur für die laufende Sitzung.
- Ein Modellwechsel mitten in der Aufgabe kostet einen Turn ohne Cache, langsamer und teurer. Wähle das Modell möglichst zu Beginn.
- `--bare` liest kein Abo-Token (`CLAUDE_CODE_OAUTH_TOKEN`); nimm `ANTHROPIC_API_KEY` oder einen `apiKeyHelper` ([S4.4](../library/s4-04-ci-zugang-und-kosten.md)).
- Aliase lösen je Anbieter verschieden auf, und für das Haiku-Modell nennt der Kanon ein frühes Retirement-Datum: Prüfe vor großen Bulk-Läufen mit `/model`, was dahintersteht.
- `/fast` (Research Preview) macht nur das Opus-Tier schneller, bei höherem Preis pro Token; im Abo läuft es nur über Usage Credits.

## Mehr dazu

- [S1.7 · Modellwahl und Effort](../library/s1-07-modellwahl-und-effort.md) · [S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen](../library/s1-19-kosten-im-blick.md) · [S4.1 · Das richtige Modell pro Phase](../library/s4-01-modell-pro-phase.md) · [S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](../library/s4-04-ci-zugang-und-kosten.md) · [S3.13 · Autonome Loops absichern: Budget und Worktree](../library/s3-13-autonome-loops-absichern.md)
- Doku: [Kosten](https://code.claude.com/docs/en/costs) · [Effort](https://code.claude.com/docs/en/model-config#adjust-effort-level) · [CLI-Referenz](https://code.claude.com/docs/en/cli-reference) · [Prompt-Caching](https://code.claude.com/docs/en/prompt-caching) · [Fast mode](https://code.claude.com/docs/en/fast-mode)
- Was der ganze Kurs kostet: [Kosten-Nachbau](kosten-nachbau.md) · Zahlen: [Kanon](../_canonical.md)
