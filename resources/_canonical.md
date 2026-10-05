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
- `claude --version`, `/release-notes` und `/model` haben Vorrang vor jeder hier gedruckten Zahl.

## Aktuelle Claude-Modelle

| Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle |
|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | `fable` | Fable | Active | Not sooner than September 1, 2027 | 1M | 10 | 50 | Härtestes, langlaufendes Reasoning; nie Account-Default |
| Claude Opus 5.5 | `claude-opus-5-5` | `opus` | Opus | Active | Not sooner than September 22, 2027 | 1M | 4 | 20 | Default in Claude Code (außer Microsoft Foundry); Architektur, tiefes Reasoning |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | `sonnet` | Sonnet | Active | Not sooner than September 28, 2027 | 1M | 2 | 10 | Schnelles Standard-Coding, Alltag |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | `haiku` | Haiku | Active | Not sooner than October 15, 2026 | 200K | 1 | 5 | Bulk-Reads, einfache Suchen, Routine-Reviews |

Die Retirement-Daten in der Tabelle sind Daten der Anthropic-Plattform; Amazon Bedrock und Google Cloud veröffentlichen eigene (Quellen: model-deprecations.md, models/overview.md).

- **Haiku-Risiko:** Haiku 4.5 kann frühestens am 15.10.2026 abgeschaltet werden. Wer `haiku` für Massenarbeit nutzt,
  prüft vor dem Einsatz mit `/model`, worauf der Alias auflöst.
- API-Alias von Haiku 4.5: `claude-haiku-4-5`.
- **Mindest-CLI je Generation** (Changelog: „Added Claude … now the default … model"): Fable 5.1 ab 2.1.257,
  Opus 5.5 ab 2.1.280, Sonnet 5.5 ab 2.1.284. Ältere CLIs lösen die Aliase auf ältere Generationen auf.

## Aliase und ihre Auflösung (Quelle: model-config.md)

- `default` löst je Kontotyp auf: Opus 5.5 auf Pro, Max, Team, Enterprise und der Anthropic API sowie auf Claude
  Platform on AWS, Amazon Bedrock und Google Cloud; Sonnet 4.5 auf Microsoft Foundry. Eine Organisations-Vorgabe geht vor; außerdem lässt sich `default` u. a. über `ANTHROPIC_DEFAULT_MODEL` oder das im Konto hinterlegte Modell überschreiben.
- `opus` und `sonnet` lösen **je Anbieter** unterschiedlich auf:

| Anbieter | `opus` | `sonnet` |
|---|---|---|
| Anthropic API | Opus 5.5 | Sonnet 5.5 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 |
| Amazon Bedrock, Google Cloud | Opus 5.5 | Sonnet 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 |

Diese Tabelle nennt Modelle, die der Monatslauf nicht überwacht (Sonnet 4.6, Sonnet 4.5, Opus 4.6). Sonnet 4.5 ist laut Deprecations-Seite seit dem 30.09.2026 abgekündigt („Deprecated“) und wird auf der Claude API am 30.11.2026 abgeschaltet; empfohlener Ersatz ist Sonnet 5.5 (nachgesehen am 2026-10-05). Vor dem Einsatz von `sonnet` auf Bedrock, Google Cloud oder Foundry den Lifecycle des Anbieters prüfen.

- `fable` löst auf Fable 5.1 auf (u. a. überschreibbar per `ANTHROPIC_DEFAULT_FABLE_MODEL`), im Claude-apps-Gateway auf Fable 5; `best` = `fable`, wo Fable verfügbar ist, sonst `opus`.
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

## Rechte-Startmodus (Quelle: permission-modes.md, „Which mode a session starts in“)

| Wie du Claude Code startest | Eingebauter Startmodus |
|---|---|
| Eine Settings-Datei setzt `disableAutoMode` auf `"disable"` | `default` (Manual) |
| `claude -p` oder Agent SDK | `default` (Manual) in Sitzungen, die Feature-Flags abrufen; ohne Abruf, etwa bei einem Drittanbieter oder mit abgeschalteter Telemetrie, `auto` ab CLI 2.1.285, davor `default`. Hält die Richtlinie einer Organisation die `auto`-Vorgabe zurück, `default` |
| Terminal oder VS Code-Erweiterung | `auto` ab CLI 2.1.283; davor `auto` nur auf Pro, Max, Team, sonst `default` |

- Ist `auto` für die Session nicht verfügbar (Modell, Einstellung, serverseitig aus), startet sie in Manual.
- Die erste Session nach Installation oder Upgrade kann abweichen; die nächste folgt der Tabelle.
- Die Zeile zu `claude -p` steht seit dem Doku-Stand vom 2026-10-05 so in der Tabelle (vorher nur im Changelog
  2.1.285). Für Läufe ohne Aufsicht heißt das: den Modus immer selbst setzen (`--permission-mode`).
- Kapitel S1.6, die Karte „Rechte“ und der Mentor verweisen hierher, statt den Startmodus selbst zu nennen.

## Struktur

- **Quellenhoheit:** Lehrinhalte stehen nur in den Kapiteln unter `resources/library/` (eine Datei je Kapitel,
  IDs `S0.1`–`S4.10` und `X.1`–`X.4`); Regale, Einstufung und Reihenfolge in `_shelves.yaml` und `_placement.yaml`.
- Der Live-Workshop ist ein Pfad durch die Bibliothek: Session 0 (Werkstatt), Sessions 1–4 (`S1.*`–`S4.*`); Ablauf
  und Moderation in `resources/paths/live-workshop.md` (generiert) und `resources/moderation/handbuch.md`.
- Die alten Module, Demos und Übungen (Stand `ba222d2`) sind in die Kapitel umgezogen; ihre Review-Archive liegen
  unter `docs/reviews/`.

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
- Doku: https://code.claude.com/docs/en/plugins/cli-reference.md
- Doku: https://code.claude.com/docs/en/settings.md
- Doku: https://platform.claude.com/docs/en/models/overview.md
- Doku: https://platform.claude.com/docs/en/about-claude/model-deprecations.md
- CLI-Version: https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- Changelog: https://code.claude.com/docs/en/changelog.md

Fremdprojekte der Community-Kapitel: Der Monatslauf meldet eine inhaltliche Änderung oder einen Ausfall gelb und nennt
das Kapitel; ihr Text zählt nie als Beleg für Claude-Code-Bezeichner.

- Fremdprojekt: https://pi.dev/ (X.3)
- Fremdprojekt: https://pi.dev/docs/latest/security (X.3)
- Fremdprojekt: https://pi.dev/docs/latest/cli (X.3)
- Fremdprojekt: https://pi.dev/docs/latest/extensions (X.3)
- Fremdprojekt: https://docs.openclaw.ai/gateway/security/trust-model.md (X.4)
- Fremdprojekt: https://docs.openclaw.ai/gateway/security/hardened-baseline.md (X.4)
- Fremdprojekt: https://docs.openclaw.ai/gateway/security/operator-incident-response.md (X.4)
- Fremdprojekt: https://docs.openclaw.ai/gateway/heartbeat.md (X.4)
- Fremdprojekt: https://docs.openclaw.ai/cli/channels.md (X.4)
