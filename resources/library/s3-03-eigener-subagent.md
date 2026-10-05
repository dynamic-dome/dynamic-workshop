---
id: S3.3
type: lesson
title: Einen eigenen Subagenten definieren
shelf: agents
level: core
minutes: 18
requires: [S3.2]
safety_floor: false
transferable: false
outcome: "Ich kann eine Subagent-Datei mit YAML-Frontmatter (name, description, tools, model, permissionMode, maxTurns) schreiben, sie nach dem Prinzip der minimalen Rechte begrenzen und sagen, welche Felder Claude Code bei Plugin-Subagenten ignoriert."
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/cli-reference
aliases: []
---

# S3.3 · Einen eigenen Subagenten definieren

<!-- meta:start -->
> **Regal:** [Agenten & Orchestrierung](README.md#agents) · **Stufe:** Kern · **~18 Min** · **Voraussetzungen:** [S3.2 Eingebaute Subagenten nutzen](s3-02-eingebaute-subagenten.md)
>
> ← [S3.2 Eingebaute Subagenten nutzen](s3-02-eingebaute-subagenten.md) · [Bibliothek](README.md) · [S3.4 Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](s3-04-orchestrierungsmuster.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du schon einmal eine eigene Subagent-Datei in `.claude/agents/` geschrieben und ihre Tools per Allowlist begrenzt?
- Kannst du ohne Nachschlagen erklären, warum die `description` die Routing-Logik ist und welche Felder bei Plugin-Subagenten ignoriert werden?

## Auf einen Blick

Einen eigenen Subagenten legst du als Markdown-Datei mit YAML-Frontmatter an, im Projekt unter `.claude/agents/` oder für alle deine Projekte unter `~/.claude/agents/`. Pflicht sind nur `name` und `description`; die `description` entscheidet, wann Claude an den Agenten delegiert. Mit `tools` gibst du ihm nur die Werkzeuge, die er braucht, denn ohne das Feld erbt er alle. Der Text unter dem Frontmatter wird sein System-Prompt.

## Bild im Kopf

Ein eigener Subagent ist wie ein neues Streifenmitglied, das du einstellst. In der Personalakte steht, wofür es zuständig ist (die `description`), welche Ausrüstung es bekommt (`tools`) und welche Freigabestufe gilt (`permissionMode`). Ein Späher bekommt keinen Generalschlüssel und ein Prüfer keinen Werkzeugkoffer: Jeder bekommt genau das, was sein Auftrag braucht.

Für Fremdpersonal gilt eine harte Regel. Ein Auftragnehmer, der mit einem Plugin ins Gebäude kommt, kann sich nicht selbst eine höhere Freigabe eintragen und keine eigenen Dienstanweisungen mitbringen. Die Freigabe legt der Betreiber fest, nicht der Gast.

## Im Detail

### Aufbau einer Agent-Datei

Agenten definierst du als YAML-Frontmatter plus Text in `.md`-Dateien:

<!-- cockpit:example -->
```yaml
---
name: code-explorer
description: >
  Analyzes codebases to understand structure, dependencies, and patterns.
  Use when you need: project overview, file map, dependency graph, entry points.
  Examples: "explore this project", "what does this codebase do", "map the architecture"
model: haiku
color: cyan
tools:
  - Read
  - Glob
  - Grep
permissionMode: default
maxTurns: 20
---

You are a code exploration specialist.  Your job is to understand, not to change.

When asked to explore a project:
1. Start with the directory structure
2. Read key files: README, main entry points, config
3. Map the dependency graph
4. Identify architectural patterns
5. Report clearly — structure, purpose, notable patterns, risks

Never modify files.  Never execute code.  Explore only.
```

Der Text unter dem Frontmatter ist der System-Prompt des Subagenten. Er bekommt nur diesen Prompt plus Angaben zur Umgebung wie das Arbeitsverzeichnis, nicht den System-Prompt von Claude Code.

Wo die Datei liegt, bestimmt, für wen der Agent gilt:

- `.claude/agents/`: nur dieses Projekt. Checkst du den Ordner ins Repo ein, nutzt das Team den Agenten mit.
- `~/.claude/agents/`: alle deine Projekte auf diesem Rechner.

Gibt es denselben `name` mehrfach, gewinnt der Ort mit der höheren Priorität: Projekt schlägt Benutzer, Agenten aus Plugins haben die niedrigste.

### Die Kernfelder

- **`name`**: eindeutige Kennung des Agenten. Pflicht.
- **`description`**: Daran entscheidet Claude, *wann* es an diesen Agenten delegiert. Das ist die Routing-Logik. Pflicht. Schreib hinein, wofür der Agent da ist und woran man einen passenden Auftrag erkennt. Halte sie trotzdem kurz: Die Beschreibungen aller Subagenten belegen Kontext; Details gehören in den System-Prompt, der erst lädt, wenn der Agent läuft. Mit „use proactively" in der Beschreibung ermunterst du Claude, von sich aus zu delegieren.
- **`model`**: ein Alias `haiku`, `sonnet`, `opus` oder `fable`, `inherit` für das Modell des Hauptgesprächs oder eine volle Modell-ID (die aktuellen IDs stehen im [Kanon](../_canonical.md)). Faustregel: Haiku für schnelles Lesen, Sonnet für Analyse, Opus für Architekturentscheidungen. Ohne Angabe nimmt Claude Code in der Regel das Modell des Hauptgesprächs.
- **`tools`**: **Sicherheit durch minimale Rechte.** Ein Explorer bekommt kein Write, ein Reviewer kein Bash. Gib genau das frei, was gebraucht wird. Lässt du `tools` weg, erbt der Subagent alle Tools, die Subagenten zur Verfügung stehen. Das Feld heißt `tools`, nicht `allowed_tools`.
- **`permissionMode`**: der Rechte-Modus des Subagenten: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk` oder `bypassPermissions` ([S1.6](s1-06-rechte-modi.md)). Er gilt nicht in jedem Fall, siehe „Typische Fallen".
- **`maxTurns`**: harte Obergrenze für die Zahl der Runden, ein Schutz gegen Kosten und Endlosläufe. Erreicht der Subagent sie, gibt Claude Code sein Ergebnis als unvollständig markiert zurück.
- **`color`**: Farbe des Agenten in der Aufgabenliste und im Verlauf (`red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` oder `cyan`). Das hilft, parallele Läufe auseinanderzuhalten.

### Weitere Felder

| Feld | Typ | Zweck |
|---|---|---|
| `disallowedTools` | Liste | Sperrliste statt Allowlist. Nützlich, wenn „alles außer X" kürzer ist als die Allowlist. |
| `skills` | Liste | Skills, deren vollen Inhalt der Subagent beim Start vorab geladen bekommt |
| `mcpServers` | Liste | MCP-Server für diesen Subagenten: der Name eines schon eingerichteten Servers oder eine eigene Definition |
| `hooks` | Objekt | Hooks, die nur laufen, solange dieser Subagent aktiv ist ([S2.9](s2-09-hook-typen.md)) |
| `memory` | String | `user`, `project` oder `local`: ein eigenes, dauerhaftes Gedächtnis-Verzeichnis über Sitzungen hinweg |
| `background` | Bool | `true` hält den Subagenten im Hintergrund, auch wenn Claude ihn im Vordergrund starten will |
| `isolation` | String | `worktree` startet den Subagenten in einem temporären Git-Worktree ([S1.18](s1-18-worktrees.md)) |
| `effort` | String | `low`, `medium`, `high`, `xhigh` oder `max`; überschreibt den Effort der Sitzung, die verfügbaren Stufen hängen vom Modell ab |
| `initialPrompt` | String | wird automatisch als erste Eingabe gesendet, wenn der Agent als Hauptagent der Sitzung läuft (`--agent`) |

Die vollständige Liste steht in der Frontmatter-Referenz der offiziellen Doku.

### Plugin-Subagenten: drei Felder zählen nicht

Bei Subagenten, die mit einem **Plugin** kommen, ignoriert Claude Code die Felder `hooks`, `mcpServers` und `permissionMode` (ebenso `initialPrompt`). Ein Gast-Plugin soll seine eigene Freigabestufe nicht anheben, keine Hooks einhängen, denen du nicht zugestimmt hast, und keine unangekündigten MCP-Server mitbringen.

Brauchst du diese Felder, kopierst du die Agent-Datei nach `.claude/agents/` oder `~/.claude/agents/`. Alternativ ergänzt du Regeln in `permissions.allow`; die gelten dann aber für die ganze Sitzung, nicht nur für den Plugin-Subagenten. Mehr zu Plugins in [S2.11](s2-11-plugins-buendeln.md), zu ihren Risiken in [S2.13](s2-13-plugin-lieferkette.md).

### Einen Subagenten gezielt aufrufen

Claude delegiert anhand der `description` von selbst. Willst du mehr Kontrolle, gibt es drei Stufen:

- **Im Auftrag nennen:** „Use the code-explorer subagent to …". Claude entscheidet weiterhin, ob es delegiert.
- **@-Erwähnung:** Tipp `@` und wähl den Agenten aus der Liste, oder schreib `@agent-code-explorer`. Dann läuft genau dieser Subagent für diese Aufgabe.
- **Ganze Sitzung:** `claude --agent code-explorer` startet eine Sitzung, in der das Hauptgespräch selbst die Tool-Grenzen und das Modell des Agenten übernimmt.

### Inline per `--agents` (für Skripte und CI)

Für Skript- und CI-Läufe kannst du Subagenten ohne Datei definieren, als JSON-Objekt, das nur für diese eine Sitzung gilt. Jeder Schlüssel ist der Name eines Agenten, sein Wert die Definition: `description`, `prompt` (entspricht dem Text unter dem Frontmatter) und die übrigen Frontmatter-Felder:

```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer","model":"sonnet","tools":["Read","Grep"],"permissionMode":"default"}}' \
       -p "Review the latest diff and report any security concerns."
```

Das ist nützlich, wenn der CI-Runner kein dauerhaftes `.claude/agents/`-Verzeichnis hat oder du die Definition neben der Workflow-YAML versionieren willst. CI-Pipelines baust du in [S4.5](s4-05-ci-pipelines.md).

## Typische Fallen

- **Ein falscher Feldname fällt nicht auf.** Claude Code ignoriert Felder, die es nicht kennt, ohne Fehlermeldung. Mehrwortige Felder schreibst du in camelCase (`maxTurns`, `disallowedTools`). `allowed_tools` steht nicht in der Frontmatter-Referenz: Verlass dich nicht darauf, sonst erbt der Agent womöglich alle Tools. Skills verwenden übrigens `allowed-tools` mit Bindestrich ([S2.3](s2-03-wer-skills-ausloest.md)), Subagenten `tools`.
- **`permissionMode` greift nicht immer.** Läuft das Hauptgespräch in `bypassPermissions`, `acceptEdits` oder `auto`, läuft der Subagent im selben Modus, und dein Feld wird ignoriert. Ein Subagent mit `bypassPermissions` bekommt diesen Modus nur, wenn das Hauptgespräch ihn auch hat. Begrenze deshalb vor allem über `tools`.
- **Der neue Agent wird nicht gefunden.** Claude Code beobachtet nur `agents`-Ordner, die es beim Start der Sitzung schon gab. Legst du den ersten Agenten in einem neuen Ordner an, starte Claude Code neu.
- **`/agents` öffnet keinen Assistenten mehr.** Seit v2.1.198 zeigt `/agents` nur einen Hinweis. Neue Subagenten schreibst du als Datei oder lässt Claude die Datei anlegen.

## Check

Du kannst einen eigenen Subagenten mit YAML-Frontmatter definieren, seine Tools nach dem Prinzip der minimalen Rechte begrenzen und erklären, warum die `description` das Routing steuert und warum Plugin-Subagenten ihre Rechte nicht selbst anheben können.

1. Welche zwei Felder sind Pflicht, und was passiert, wenn `tools` fehlt?
2. Welche drei Felder ignoriert Claude Code bei Subagenten aus einem Plugin?
3. Wann wird der `permissionMode` eines Subagenten ignoriert?

<details><summary>Quizfrage</summary>

**Frage:** Ein Plugin bringt einen Subagenten mit, der im Frontmatter `permissionMode: bypassPermissions` und eigene `hooks` setzt. Was macht Claude Code damit?

- **Richtig:** Es ignoriert beide Felder, damit ein Plugin weder seine Freigabestufe anhebt noch ungefragt Hooks einhängt.
- Falsch: Es übernimmt beide Felder, zeigt dir aber vor dem ersten Start des Subagenten einen eigenen Bestätigungsdialog an.
- Falsch: Es verweigert das ganze Plugin, weil Subagenten aus Plugins grundsätzlich kein YAML-Frontmatter haben dürfen.
- Falsch: Es übernimmt beide Felder, sofern das Plugin aus dem offiziellen Plugin-Marketplace von Anthropic stammt.

</details>

## Weiterlesen

- [Subagents: Frontmatter-Referenz (offizielle Doku)](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields)
- [CLI-Referenz: `--agent` und `--agents`](https://code.claude.com/docs/en/cli-reference)
- [S3.2 · Eingebaute Subagenten nutzen](s3-02-eingebaute-subagenten.md)
- [S1.6 · Alle Rechte-Modi im Überblick](s1-06-rechte-modi.md)
- [S2.9 · Hook-Typen und Hooks in Komponenten](s2-09-hook-typen.md)
- [S2.11 · Plugins: ein Bündel schnüren](s2-11-plugins-buendeln.md)
- [S2.13 · Lieferkettenrisiken bei Plugins](s2-13-plugin-lieferkette.md)
- [S4.5 · CI-Pipelines bauen mit GitHub Actions und GitLab](s4-05-ci-pipelines.md)
