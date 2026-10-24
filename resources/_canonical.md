<!-- CANONICAL SOURCE OF TRUTH — do not teach anything that contradicts this file.
     Einzige Stelle im Kurs, an der Modellgenerationen und ihre Fakten stehen (Alias-Regel).
     Geprüft von tools/lint_currency.py (Generationsregel + Stale-Gate) und tools/currency_check.py (Monatslauf).
     Design: docs/plans/2026-09-29-phase2-aktualhaltung-design.md -->

# Canonical Registry — Dynamic Workshop

Geprüft: 2026-10-24 · CLI 2.1.310

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
| Claude Haiku 5.5 | `claude-haiku-5-5` | `haiku` | Haiku | Active | Not sooner than October 7, 2027 | 1M | 0.10 | 0.50 | Bulk-Reads, einfache Suchen, Routine-Reviews |
| Claude Opus 4.6 (Legacy) | `claude-opus-4-6` | `opus` | Opus | Active | Not sooner than February 5, 2027 | 1M | 5 | 25 | Legacy: `opus` auf Microsoft Foundry |
| Claude Sonnet 4.6 (Legacy) | `claude-sonnet-4-6` | `sonnet` | Sonnet | Active | Not sooner than February 17, 2027 | 1M | 3 | 15 | Legacy: `sonnet` auf Claude Platform on AWS |
| Claude Sonnet 4.5 (Legacy, abgekündigt) | `claude-sonnet-4-5-20250929` | `sonnet` | Sonnet | Deprecated | November 30, 2026 | 200K | 3 | 15 | Legacy, abgekündigt seit 30.09.2026: `sonnet` auf Amazon Bedrock, Google Cloud, Microsoft Foundry |
| Claude Haiku 4.5 (Legacy) | `claude-haiku-4-5-20251001` | `haiku` | Haiku | Active | Not sooner than October 15, 2026 | 200K | 1 | 5 | Legacy: `haiku` auf Claude Platform on AWS, Amazon Bedrock, Google Cloud, Foundry |

Die vier Legacy-Zeilen stehen in der überwachten Tabelle, weil die Anbieter-Aliase unten noch darauf auflösen (todo #9957): Der Monatslauf prüft ihren Status auf der Deprecations-Seite und meldet rot, sobald einer vom Kanon-Status abweicht (bei Active also bei jeder Abkündigung). Ein verstrichenes „Not sooner than“ bei Status Active ist nur Info (kein Abschaltbeschluss). Sonnet 4.5 steht bewusst mit Status Deprecated und dem festen Abschaltdatum der Deprecations-Seite: Solange Seite und Kanon übereinstimmen, meldet der Monatslauf es ab 60 Tagen vor der Abschaltung gelb als bekannte Abkündigung; wechselt es auf Retired oder verschwindet die Zeile, wird er rot und die Zeile samt Alias-Hinweis ist zu streichen. Kontext der 4.6-Zeilen (1M Tokens) laut Modellseiten opus-4-6 und sonnet-4-6 (nachgesehen am 2026-10-24); die Modellübersicht führt beide nur noch als „Legacy models (still available)“ ohne Werte.

Die Retirement-Daten in der Tabelle sind Daten der Anthropic-Plattform; Amazon Bedrock und Google Cloud veröffentlichen eigene (Quellen: model-deprecations.md, models/overview.md).

- **Haiku 5.5, Preis:** Der Preis in der Tabelle gilt für Prompts bis 100K Tokens. Über 100K Tokens Prompt kostet Haiku 5.5
  0.50 $ Input und 2.50 $ Output je 1M Tokens (Quelle: pricing.md). Alle anderen Modelle der Tabelle haben keinen Aufschlag für das 1M-Fenster.
- **Haiku 4.5 (Legacy):** `claude-haiku-4-5-20251001` (200K Kontext, 1 $ / 5 $ je 1M Tokens, kein Effort, API-Alias
  `claude-haiku-4-5`) steht in der Modellübersicht unter „Legacy models (still available)". Die Deprecations-Seite führt es
  weiter als Active mit „Not sooner than October 15, 2026", also ohne angekündigte Abschaltung. Es steht als Legacy-Zeile in der
  überwachten Tabelle: Der Monatslauf meldet ein verstrichenes Datum bei Status Active nur als Info und wird rot, wenn die
  Deprecations-Seite einen anderen Status zeigt (Vorlauf einer Abschaltung mindestens 60 Tage; nachgesehen am 2026-10-24).
  Wo der Alias `haiku` noch darauf auflöst (Tabelle unten), prüfst du vor Bulk-Läufen mit `/model`, worauf er steht.
- **Mindest-CLI je Generation** (Changelog: „Added Claude … now the default … model"): Fable 5.1 ab 2.1.257,
  Opus 5.5 ab 2.1.280, Sonnet 5.5 ab 2.1.284, Haiku 5.5 ab 2.1.293. Ältere CLIs lösen die Aliase auf ältere Generationen auf.

## Aliase und ihre Auflösung (Quelle: model-config.md)

- `default` löst je Kontotyp auf: Opus 5.5 auf Pro, Max, Team, Enterprise und der Anthropic API sowie auf Claude
  Platform on AWS, Amazon Bedrock und Google Cloud; Sonnet 4.5 auf Microsoft Foundry. Eine Organisations-Vorgabe geht vor; außerdem lässt sich `default` u. a. über `ANTHROPIC_DEFAULT_MODEL` oder das im Konto hinterlegte Modell überschreiben.
- `opus`, `sonnet` und `haiku` lösen **je Anbieter** unterschiedlich auf:

| Anbieter | `opus` | `sonnet` | `haiku` |
|---|---|---|---|
| Anthropic API | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 | Haiku 4.5 |
| Amazon Bedrock, Google Cloud | Opus 5.5 | Sonnet 4.5 | Haiku 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 | Haiku 4.5 |

Diese Tabelle nennt Legacy-Modelle: Haiku 4.5, Sonnet 4.5, Sonnet 4.6 und Opus 4.6 überwacht der Monatslauf (Zeilen oben). Sonnet 4.5 ist laut Deprecations-Seite seit dem 30.09.2026 abgekündigt („Deprecated“) und wird auf der Claude API am 30.11.2026 abgeschaltet; empfohlener Ersatz ist Sonnet 5.5 (Quelle: model-deprecations.md, Modellseite sonnet-4-5, nachgesehen am 2026-10-24). Vor dem Einsatz von `sonnet` auf Bedrock, Google Cloud oder Foundry den Lifecycle des Anbieters prüfen.

- `fable` löst auf Fable 5.1 auf (u. a. überschreibbar per `ANTHROPIC_DEFAULT_FABLE_MODEL`), im Claude-apps-Gateway auf Fable 5; `best` = `fable`, wo Fable verfügbar ist, sonst `opus`.
- Weitere Werte: `opusplan` (Opus im Plan-Modus, dann Sonnet), `sonnet[1m]`, `opus[1m]`.

## Effort (Quelle: model-config.md, „Adjust effort level“)

| Modelle | Stufen | Start-Effort in Claude Code |
|---|---|---|
| Fable 5.1 | `low` `medium` `high` `xhigh` `max` | `high` |
| Opus 5.5, Sonnet 5.5, Haiku 5.5 | `low` `medium` `high` `xhigh` `max` | `medium` |
| Haiku 4.5 (Legacy) | kein Effort | — |

- Die Modellübersicht der API nennt für Sonnet 5.5 `high` als Default-Effort; Claude Code startet laut model-config
  mit `medium`. Im Kurs gilt das Claude-Code-Verhalten.
- `max` gilt nur für die laufende Session, außer über `CLAUDE_CODE_EFFORT_LEVEL`.

## Rechte-Startmodus (Quelle: permission-modes.md, „Which mode a session starts in“)

| Wie du Claude Code startest | Eingebauter Startmodus |
|---|---|
| Eine Settings-Datei setzt `disableAutoMode` auf `"disable"` | `default` (Manual) |
| `claude -p` oder Agent SDK | `default` (Manual) ab CLI 2.1.302 in allen Fällen. Davor `default` in Sitzungen mit Feature-Flag-Abruf, sonst (Drittanbieter, abgeschaltete Telemetrie, frische Installation) `auto` ab 2.1.285. Mit `--permission-mode auto` startet der Lauf in `auto` |
| Terminal oder VS Code-Erweiterung | `auto` ab CLI 2.1.283; davor `auto` nur auf Pro, Max, Team, sonst `default` |

- Ist `auto` für die Session nicht verfügbar (Modell, Einstellung, serverseitig aus), startet sie in Manual.
- Die erste Session nach Installation oder Upgrade kann abweichen; die nächste folgt der Tabelle.
- Die Zeile zu `claude -p` folgt seit dem Doku-Stand vom 2026-10-24 der Tabelle („`default`") und dem Abschnitt „Tool calls
  denied in `claude -p` and Agent SDK runs" (Changelog 2.1.302). In `default` lehnt ein Lauf ohne Mensch jeden Aufruf ab,
  den keine Allow-Regel, kein Hook, kein `canUseTool`-Callback und kein `--permission-prompt-tool` freigibt. Für Läufe ohne
  Aufsicht heißt das weiter: den Modus immer selbst setzen (`--permission-mode`).
- **Auto-Modus und Modell** (Quelle: permission-modes.md, „Eliminate prompts with auto mode"): Auf der Anthropic API und
  Claude Platform on AWS unterstützen Opus 4.6 oder neuer, Sonnet 4.6 oder neuer, Haiku 5.5 und die Fable-Modelle `auto`;
  auf Amazon Bedrock, Google Cloud, Microsoft Foundry und im Claude-apps-Gateway nur Sonnet 5 oder neuer, Opus 4.7 oder
  neuer, Haiku 5.5 und die Fable-Modelle (Haiku 5.5 dort ab CLI 2.1.293). Ältere Modelle, darunter Haiku 4.5, sind auf keinem Anbieter unterstützt.
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
- Doku: https://code.claude.com/docs/en/sub-agents.md
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
