<!-- CANONICAL SOURCE OF TRUTH — do not teach anything that contradicts this file.
     Einzige Stelle im Kurs, an der Modellgenerationen und ihre Fakten stehen (Alias-Regel).
     Geprüft von tools/lint_currency.py (Generationsregel + Stale-Gate) und tools/currency_check.py (Monatslauf).
     Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md -->

# Canonical Registry — Dynamic Workshop

Geprüft: 2026-09-29 · CLI 2.1.284

Das Prüfdatum setzt nur eine Session, die diesen Kanon gegen einen Bericht von `tools/currency_check.py` oder direkt
gegen die Quellen unten abgeglichen hat. `tools/lint_currency.py` warnt nach mehr als 45 Tagen und wird nach mehr als 90 Tagen rot.

## Alias-Regel

- Kursinhalte nennen **keine Modellgeneration** (etwa „Opus 5.5“ oder `claude-opus-5-5`). Code und Config nutzen
  Aliase (`opus`, `sonnet`, `haiku`, `fable`), Prosa nennt die Rolle („das Opus-Tier“) und verweist hierher.
- Preise, Kontextgrößen, Effort-Defaults und Retirement-Daten stehen nur hier.
- Bewusst versionierte Stellen tragen in derselben Zeile `version-pinned: <Grund>`.
- Immer `claude --version`, `/release-notes` und `/model` über jede hier gedruckte Zahl stellen.

## Aktuelle Claude-Modelle

| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |
|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | `fable` | Fable | Active | Not sooner than September 1, 2027 | 1M | 10 | 50 | Härtestes, langlaufendes Reasoning; nie Account-Default |
| Claude Opus 5.5 | `claude-opus-5-5` | `opus` | Opus | Active | Not sooner than September 22, 2027 | 1M | 4 | 20 | Default in Claude Code; Architektur, tiefes Reasoning |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | `sonnet` | Sonnet | Active | Not sooner than September 28, 2027 | 1M | 2 | 10 | Schnelles Standard-Coding, Alltag |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | `haiku` | Haiku | Active | Not sooner than October 15, 2026 | 200K | 1 | 5 | Bulk-Reads, einfache Suchen, Routine-Reviews |

- **Haiku-Risiko:** Haiku 4.5 kann frühestens am 15.10.2026 abgeschaltet werden. Wer `haiku` für Massenarbeit nutzt,
  prüft vor dem Einsatz mit `/model`, worauf der Alias auflöst.
- API-Alias von Haiku 4.5: `claude-haiku-4-5`.

## Aliase und ihre Auflösung (Quelle: model-config.md)

- `default` löst je Kontotyp auf: Opus 5.5 auf Pro, Max, Team, Enterprise und der Anthropic API sowie auf Claude
  Platform on AWS, Amazon Bedrock und Google Cloud; Sonnet 4.5 auf Microsoft Foundry. Eine Organisations-Vorgabe geht vor.
- `opus` und `sonnet` lösen **je Anbieter** unterschiedlich auf:

| Anbieter | `opus` | `sonnet` |
|---|---|---|
| Anthropic API | Opus 5.5 | Sonnet 5.5 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 |
| Amazon Bedrock, Google Cloud | Opus 5.5 | Sonnet 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 |

- `fable` löst auf Fable 5.1 auf, im Claude-apps-Gateway auf Fable 5; `best` = `fable`, wo Fable verfügbar ist, sonst `opus`.
- Weitere Werte: `opusplan` (Opus im Plan-Modus, dann Sonnet), `sonnet[1m]`, `opus[1m]`.

## Effort (Quelle: model-config.md, „Adjust effort level“)

| Modelle | Stufen | Start-Effort in Claude Code |
|---|---|---|
| Fable 5.1 | `low` `medium` `high` `xhigh` `max` | `high` |
| Opus 5.5, Sonnet 5.5 | `low` `medium` `high` `xhigh` `max` | `medium` |
| Haiku 4.5 | kein Effort | — |

- Die Modellübersicht der API nennt für Sonnet 5.5 `high` als Default-Effort; Claude Code startet laut model-config
  mit `medium`. Im Kurs gilt das Claude-Code-Verhalten.
- `max` gilt nur für die laufende Session, außer über `CLAUDE_CODE_EFFORT_LEVEL`.

## Struktur

- **4 Sessions / 65 Lerneinheiten (LE)** — Welle-F-Restrukturierung (`session-plan.md` ist die Ablauf-SSoT).
- Session 1 = Block 1 (Foundations, S1.1–S1.20). Session 2 = Block 2 (Ecosystem, S2.1–S2.20).
  Session 3 = Block 3 Advanced Kern (S3.1–S3.15). Session 4 = Block 3 Advanced Bonus (S4.1–S4.10).
- 17 Module (5+5+7) über 3 Blöcke bleiben die Volltext-Quelle; die 65-LE-Landkarte ist die Navigations-Schicht darüber.

## Quellen

Der Monatslauf (`tools/currency_check.py`) liest genau diese Liste.

- Doku: https://code.claude.com/docs/en/cli-reference.md
- Doku: https://code.claude.com/docs/en/env-vars.md
- Doku: https://code.claude.com/docs/en/hooks.md
- Doku: https://code.claude.com/docs/en/headless.md
- Doku: https://code.claude.com/docs/en/authentication.md
- Doku: https://code.claude.com/docs/en/github-actions.md
- Doku: https://code.claude.com/docs/en/permission-modes.md
- Doku: https://code.claude.com/docs/en/model-config.md
- Doku: https://code.claude.com/docs/en/mcp.md
- Doku: https://code.claude.com/docs/en/skills.md
- Doku: https://code.claude.com/docs/en/settings.md
- Doku: https://platform.claude.com/docs/en/models/overview.md
- Doku: https://platform.claude.com/docs/en/about-claude/model-deprecations.md
- CLI-Version: https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- Changelog: https://code.claude.com/docs/en/changelog.md
