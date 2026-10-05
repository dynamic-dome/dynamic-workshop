---
id: S3.3
type: lesson
title: Einen eigenen Subagenten definieren
shelf: agents
level: core
minutes: 25
requires: [S3.2]
safety_floor: false
transferable: false
outcome: "Ich kann eine Subagent-Datei mit YAML-Frontmatter (name, description, tools, model, maxTurns) schreiben, sie nach dem Prinzip der minimalen Rechte auf lesende Tools begrenzen, einen stillen Feldnamen-Fehler erkennen und sagen, welche Felder Claude Code bei Plugin-Subagenten ignoriert."
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

Ein eigener Subagent ist wie ein neues Streifenmitglied, das du einstellst. In der Personalakte steht, wofür es zuständig ist (die `description`), und welche Ausrüstung es bekommt (`tools`). Ein Späher bekommt keinen Generalschlüssel und ein Prüfer keinen Werkzeugkoffer: Jeder bekommt genau das, was sein Auftrag braucht.

Für Fremdpersonal gilt eine harte Regel. Ein Auftragnehmer, der mit einem Plugin ins Gebäude kommt, kann sich nicht selbst eine höhere Freigabe eintragen und keine eigenen Dienstanweisungen mitbringen. Die Freigabe legt der Betreiber fest, nicht der Gast.

## Im Detail

### Aufbau einer Agent-Datei

Agenten definierst du als YAML-Frontmatter plus Text in `.md`-Dateien. Das Beispiel nutzt mehr Felder, als die Übung unten braucht:

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

Wo die Datei liegt, bestimmt, für wen der Agent gilt: `.claude/agents/` nur für dieses Projekt (checkst du den Ordner ein, nutzt das Team den Agenten mit), `~/.claude/agents/` für alle deine Projekte auf diesem Rechner. Gibt es denselben `name` mehrfach, gewinnt der Ort mit der höheren Priorität: Projekt schlägt Benutzer, Agenten aus Plugins haben die niedrigste.

### Die Kernfelder

- **`name`**: eindeutige Kennung des Agenten. Pflicht.
- **`description`**: Daran entscheidet Claude, *wann* es an diesen Agenten delegiert. Das ist die Routing-Logik. Pflicht. Schreib hinein, wofür der Agent da ist und woran man einen passenden Auftrag erkennt, aber halte sie kurz: Die Beschreibungen aller Subagenten belegen Kontext; Details gehören in den System-Prompt, der erst lädt, wenn der Agent läuft. Mit „use proactively“ ermunterst du Claude, von sich aus zu delegieren.
- **`tools`**: **Sicherheit durch minimale Rechte.** Ein Explorer bekommt kein Write, ein Reviewer weder Write noch Edit; braucht er `git diff`, kommt Bash dazu. Gib genau das frei, was gebraucht wird. Lässt du `tools` weg, erbt der Subagent alle Tools, die Subagenten zur Verfügung stehen. Das Feld heißt `tools`, nicht `allowed_tools`; als Wert geht eine kommagetrennte Zeichenkette (`Read, Grep, Glob`) oder eine YAML-Liste.
- **`model`**: ein Alias `haiku`, `sonnet`, `opus` oder `fable`, `inherit` für das Modell des Hauptgesprächs oder eine volle Modell-ID (die aktuellen IDs stehen im [Kanon](../_canonical.md)). Als Faustregel: Haiku für schnelles Lesen, Sonnet für Analyse, Opus für Architekturentscheidungen. Ohne Angabe nimmt Claude Code in der Regel das Modell des Hauptgesprächs.
- **`maxTurns`**: harte Obergrenze für die Zahl der Runden, ein Schutz gegen Kosten und Endlosläufe. Erreicht der Subagent sie, gibt Claude Code sein Ergebnis als unvollständig markiert zurück.
- **`permissionMode`**: der Rechte-Modus des Subagenten ([S1.6](s1-06-rechte-modi.md)). Er gilt nicht in jedem Fall, siehe „Typische Fallen“.
- **`color`**: Farbe des Agenten in der Aufgabenliste und im Verlauf. Das hilft, parallele Läufe auseinanderzuhalten.

Weitere Felder wie `disallowedTools`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation` und `effort` stehen in der [Frontmatter-Referenz](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields) der offiziellen Doku. Wichtig ist die Grundregel dort: Claude Code ignoriert ein Feld, das es nicht kennt, ohne Fehlermeldung.

### Plugin-Subagenten: drei Felder zählen nicht

Bei Subagenten, die mit einem **Plugin** kommen, ignoriert Claude Code die Felder `hooks`, `mcpServers` und `permissionMode` (ebenso `initialPrompt`). Ein Gast-Plugin soll seine eigene Freigabestufe nicht anheben, keine Hooks einhängen, denen du nicht zugestimmt hast, und keine unangekündigten MCP-Server mitbringen.

Brauchst du diese Felder, kopierst du die Agent-Datei nach `.claude/agents/` oder `~/.claude/agents/`. Alternativ ergänzt du Regeln in `permissions.allow`; die gelten dann aber für die ganze Sitzung, nicht nur für den Plugin-Subagenten. Mehr zu Plugins in [S2.11](s2-11-plugins-buendeln.md), zu ihren Risiken in [S2.13](s2-13-plugin-lieferkette.md).

### Einen Subagenten gezielt aufrufen

Claude delegiert anhand der `description` von selbst. Willst du mehr Kontrolle, gibt es drei Stufen:

- **Im Auftrag nennen:** „Use the code-explorer subagent to …“. Claude entscheidet weiterhin, ob es delegiert.
- **@-Erwähnung:** Tipp `@` und wähl den Agenten aus der Liste, oder schreib `@agent-code-explorer`. Dann läuft genau dieser Subagent für diese Aufgabe. Dein ganzer Satz geht weiter an Claude, das den Auftrag für den Subagenten formuliert.
- **Ganze Sitzung:** `claude --agent code-explorer` startet eine Sitzung, in der das Hauptgespräch selbst die Tool-Grenzen und das Modell des Agenten übernimmt.

### Ohne Datei: `--agents` (für Skripte und CI)

Für Skript- und CI-Läufe kannst du Subagenten ohne Datei definieren, als JSON-Objekt, das nur für diese eine Sitzung gilt. Jeder Schlüssel ist der Name eines Agenten, sein Wert die Definition: `description`, `prompt` (entspricht dem Text unter dem Frontmatter) und die übrigen Felder. Das Beispiel ist für bash und Git Bash geschrieben; PowerShell braucht anderes Quoting für die Anführungszeichen im JSON, und das ist hier nicht durchgespielt. Das `-p` startet einen einmaligen Lauf ohne Sitzung ([S4.3](s4-03-headless.md)).

```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer","model":"sonnet","tools":["Read","Grep"],"permissionMode":"default"}}' \
       -p "Review the latest diff and report any security concerns."
```

CI-Pipelines baust du in [S4.5](s4-05-ci-pipelines.md).

## Selbst machen

### Übung: einen schreibgeschützten Subagenten bauen und seine Grenze testen (etwa 15 Minuten)

**Ziel:** Du schreibst einen Subagenten, der nur lesen darf, rufst ihn per @-Erwähnung auf, siehst ihn an der Grenze scheitern und erlebst, wie ein falscher Feldname die Grenze still aufhebt.

**Startzustand:** ein neuer Ordner `~/cc-workshop/agent-datei`, in dem der Ordner `.claude/agents` schon existiert, bevor du Claude Code startest (`mkdir -p ~/cc-workshop/agent-datei/.claude/agents && cd ~/cc-workshop/agent-datei`, in PowerShell `New-Item -ItemType Directory -Force "$HOME\cc-workshop\agent-datei\.claude\agents"; Set-Location "$HOME\cc-workshop\agent-datei"`). Claude Code beobachtet laut Doku nur `agents`-Ordner, die beim Start der Sitzung schon da waren. Leg im Ordner `agent-datei` außerdem mit einem Editor eine Datei `README.md` an:

```md
# Door Notes

A small tool that reads door events.

## Usage

Run it with a card id.
```

1. Leg mit dem Editor die Datei `.claude/agents/readme-reviewer.md` an. Sie hat nur lesende Tools:

   <!-- cockpit:example -->
   ```md
   ---
   name: readme-reviewer
   description: Reviews a README file for missing steps and unclear wording. Use when the user asks for a README review.
   tools: Read, Grep, Glob
   model: inherit
   maxTurns: 10
   ---

   You review README files. Read the file you are given and list up to five concrete problems, each with the line it refers to. Follow the request you are given.
   ```
2. Starte `claude --permission-mode default` im Ordner und bestätige den Vertrauensdialog.
3. Ruf den Agenten per @-Erwähnung auf:

   ```text
   @agent-readme-reviewer Review README.md and list the problems you find.
   ```

   Erwartet: Im Transkript (`Ctrl+O`) steht eine Zeile mit `readme-reviewer`, und die Antwort nennt Probleme mit Zeilenangaben, etwa den fehlenden Installationsschritt.
4. Bitte ihn um etwas, das ihm fehlt:

   ```text
   @agent-readme-reviewer Write your findings into a new file called review.txt.
   ```

   Erwartet: Der Subagent meldet, dass er keine Dateien anlegen kann. Möglicherweise will Claude danach selbst `review.txt` anlegen und fragt dich um Freigabe: Lehn ab. Die Grenze gilt für den Subagenten, nicht für dein Hauptgespräch. Prüf in einem zweiten Terminal im selben Ordner (`ls`, in PowerShell `Get-ChildItem`): Es gibt keine `review.txt`.
5. Provozier den stillen Fehler. Leg, während die Sitzung läuft, die Datei `.claude/agents/readme-checker.md` an. Sie ist bis auf Name und die Zeile mit den Tools gleich; der Feldname ist falsch:

   ```md
   ---
   name: readme-checker
   description: Checks a README file for missing steps and unclear wording. Use when the user asks for a README check.
   allowed_tools: Read, Grep, Glob
   model: inherit
   maxTurns: 10
   ---

   You review README files. Read the file you are given and list up to five concrete problems, each with the line it refers to. Follow the request you are given.
   ```

   Claude Code erkennt neue Dateien in einem schon vorhandenen Ordner nach wenigen Sekunden. Findet Claude den Agenten im nächsten Schritt nicht, beende die Sitzung und starte sie neu.
6. Stell dieselbe Bitte wie in Schritt 4:

   ```text
   @agent-readme-checker Review README.md and write your findings into a new file called check.txt.
   ```

   Erwartet: Diesmal fragt Claude Code, ob die Datei `check.txt` angelegt werden darf. Gib sie mit „Yes“ frei und prüf, dass `check.txt` im Ordner liegt. Es gab keine Fehlermeldung zu `allowed_tools`.

**Aufräumen:** Beende die Sitzung mit `/exit` und lösch den Ordner `~/cc-workshop/agent-datei` selbst. Die Agenten lagen nur in diesem Projekt.

<details><summary>Vergleich</summary>

Beide Dateien unterscheiden sich nur in einer Zeile: `tools:` gegen `allowed_tools:`. Claude Code kennt `allowed_tools` nicht und ignoriert es ohne Meldung. Ohne `tools` erbt der Subagent alle Tools, die Subagenten zur Verfügung stehen, auch Write. Ein Tippfehler hat die Grenze aufgehoben, ohne dass du etwas gemerkt hättest, bis du sie getestet hast. Teste jede Grenze, die dir wichtig ist.

</details>

**Geschafft, wenn:**

- [ ] `readme-reviewer` per @-Erwähnung lief und Probleme mit Zeilenangaben nannte
- [ ] die Bitte, eine Datei zu schreiben, bei ihm scheiterte und keine `review.txt` entstand
- [ ] `readme-checker` ohne Fehlermeldung eine Schreibfreigabe anfragte
- [ ] du erklären kannst, warum: Unbekannte Felder werden ignoriert, ohne `tools` erbt der Agent alle Tools

## Typische Fallen

- **Ein falscher Feldname fällt nicht auf.** Das hast du in der Übung gesehen. Mehrwortige Felder schreibst du in camelCase (`maxTurns`, `disallowedTools`). Skills verwenden übrigens `allowed-tools` mit Bindestrich ([S2.3](s2-03-wer-skills-ausloest.md)), Subagenten `tools`.
- **`permissionMode` greift nicht immer.** Läuft das Hauptgespräch in `bypassPermissions`, `acceptEdits` oder `auto`, läuft der Subagent im selben Modus, und dein Feld wird ignoriert. Ein Subagent mit `bypassPermissions` bekommt diesen Modus nur, wenn das Hauptgespräch ihn auch hat. Begrenze deshalb vor allem über `tools`.
- **Der neue Agent wird nicht gefunden.** Der erste Agent in einem Ordner, den es beim Start der Sitzung noch nicht gab, wird erst nach einem Neustart geladen. Dasselbe gilt für Dateien unter `--add-dir`.
- **Die Datei lädt gar nicht.** Fehlt `name` oder `description`, lädt Claude Code die Datei nicht und meldet das nicht in der Sitzung. Bei fehlender `description` steht der Grund im Debug-Log (`claude --debug`).
- **`/agents` öffnet keinen Assistenten mehr.** Seit v2.1.198 zeigt `/agents` nur einen Hinweis. Neue Subagenten schreibst du als Datei oder lässt Claude die Datei anlegen.

## Check

Du kannst einen eigenen Subagenten mit YAML-Frontmatter definieren, seine Tools nach dem Prinzip der minimalen Rechte begrenzen, einen falsch geschriebenen Feldnamen als Ursache erkennen und erklären, warum Plugin-Subagenten ihre Rechte nicht selbst anheben können.

1. Welche zwei Felder sind Pflicht, und was passiert, wenn `tools` fehlt?
2. Was geschieht, wenn du in der Frontmatter `allowed_tools` statt `tools` schreibst?
3. Welche drei Felder ignoriert Claude Code bei Subagenten aus einem Plugin?

<details><summary>Auflösung</summary>

1. `name` und `description`. Fehlt `tools`, erbt der Subagent alle Tools, die Subagenten zur Verfügung stehen.
2. Claude Code ignoriert das unbekannte Feld ohne Fehlermeldung, und der Agent erbt alle Tools, als hättest du keine Grenze gesetzt.
3. `hooks`, `mcpServers` und `permissionMode`.

</details>

<details><summary>Quizfrage</summary>

**Frage:** Dein Subagent `reviewer` setzt `permissionMode: default`. Du arbeitest im Hauptgespräch im Modus `acceptEdits` und lässt ihn Änderungen prüfen. In welchem Modus läuft er?

- **Richtig:** In `acceptEdits`: Das Hauptgespräch bestimmt den Modus, dein Feld wird ignoriert. Begrenzen kannst du ihn zuverlässig nur über `tools`.
- Falsch: In `default`, denn das Feld im Subagenten hat Vorrang vor dem Modus des Hauptgesprächs, solange es in der Datei steht.
- Falsch: Claude Code meldet einen Konflikt und lässt den Subagenten erst laufen, wenn du den Moduswechsel ausdrücklich bestätigt hast.
- Falsch: Er startet nur, wenn beide Modi übereinstimmen; sonst bricht Claude Code den Aufruf des Subagenten mit einer Fehlermeldung ab.

</details>

## Weiterlesen

- [Subagents: Frontmatter-Referenz (offizielle Doku)](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields)
- [CLI-Referenz: `--agent` und `--agents`](https://code.claude.com/docs/en/cli-reference)
- [S3.2 · Eingebaute Subagenten nutzen](s3-02-eingebaute-subagenten.md)
- [S1.6 · Alle Rechte-Modi im Überblick](s1-06-rechte-modi.md)
- [S2.11 · Plugins: ein Bündel schnüren](s2-11-plugins-buendeln.md)
- [S2.13 · Lieferkettenrisiken bei Plugins](s2-13-plugin-lieferkette.md)
- [S4.5 · CI-Pipelines bauen mit GitHub Actions und GitLab](s4-05-ci-pipelines.md)
