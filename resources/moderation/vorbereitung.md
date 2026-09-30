# Vorbereitung für Moderierende

> Was vor den Terminen installiert, kopiert und geprüft sein muss. Das Setup der Teilnehmenden steht in
> [S0.1 Werkstatt einrichten](../library/s0-01-werkstatt-einrichten.md); hier geht es um die Extras für die Demos und
> um deine eigene Maschine. Ablauf, Pre-Flight am Workshop-Tag und Go/No-Go stehen im [Handbuch](handbuch.md).
>
> Stand: 2026-09-30.

## Zeitplan

### 1–2 Wochen vorher

1. **Setup-Check mit allen Teilnehmenden:** 30 Minuten Onboarding-Call pro Person.
   - Prüfen: `claude --version`, `git --version`, `python --version` (Windows; macOS/Linux `python3`), `gh auth status`.
   - Workshop-Plugins installieren, falls verfügbar; sonst klar als „nur Demo" markieren.
   - NotebookLM-Konto anlegen.
   - Workshop-Playground klonen.
2. **Eigene Maschine vorbereiten:**
   - Alle Demos einmal komplett durchspielen (Abschnitt „Vorführen" der Kapitel).
   - Den [Pre-Flight](handbuch.md#pre-flight-am-workshop-tag) einmal durchlaufen.
   - Ein Konto mit festem Budget einrichten. Die Größenordnung liefert die Kostenschätzung je Session in
     `resources/reference/kosten-nachbau.md`, die Modellpreise stehen in [`_canonical.md`](../_canonical.md).
   - Die Plugins, Skills und Dateien aus den Abschnitten unten vorbereiten.
3. **Material durchgehen:**
   - Den [Live-Pfad](../paths/live-workshop.md) durchgehen und die Reihenfolge einprägen.
   - In jedem Kapitel den Block „Für Moderierende" lesen, vor allem die Recovery-Notes.
   - Die FAQ (`resources/reference/faq.md`) nach Standardfragen überfliegen.
4. **Eine Woche vor Session 1:** die [Einladung](handbuch.md#einladung-vorlage) verschicken.

### Vor Session 2

- Einen Demo-Skill in `~/.claude/skills/` vorbereiten oder prüfen, dass mindestens ein Skill vorhanden ist
  ([S2.2](../library/s2-02-skill-schreiben.md)).
- Hook-Skripte als eigene Dateien vorbereiten, nicht als Inline-Shell im JSON ([Hook-Datei](#hook-datei-für-die-demo)).
- Prüfen, dass `jq` oder das JSON-Parsing von Python in der Shell funktioniert, in der die Hooks laufen.
- Den Playwright-MCP vorab laden ([unten](#playwright-mcp-vorab-laden)) oder einen Screenshot- bzw. Video-Fallback
  bereithalten ([S2.14](../library/s2-14-mcp-stecker.md)).
- Das NotebookLM-Notebook vor der Session anlegen; Quellen nicht live indexieren
  ([unten](#notebooklm-notebook), [S2.18](../library/s2-18-rag-und-notebooklm.md)).

### Vor Session 3

- `claude --version` und den Login-Status prüfen.
- `devil-advocate-swarms` prüfen oder ein statisches Transkript bzw. einen Screenshot als Fallback bereithalten
  ([S3.6](../library/s3-06-devils-advocate.md)).
- Für jeden Headless- oder autonomen Befehl eine ausdrückliche Budgetgrenze setzen
  ([S3.13](../library/s3-13-autonome-loops-absichern.md), [S3.14](../library/s3-14-self-improve-loop.md)).

### Vor Session 4

- `codex --version` prüfen; den Codex-Schwarm nur zeigen, wenn Anmeldung und Plugin geprüft sind
  ([S4.2](../library/s4-02-codex-schwarm.md)).
- `~/.claude/skills/broken-greeter/SKILL.md` vor der Diagnose-Demo anlegen; die Vorlage liegt in
  `resources/demos/assets/broken-greeter/` ([S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md)).
- Für jeden Headless-Befehl eine ausdrückliche Budgetgrenze setzen ([S4.3](../library/s4-03-headless.md)).
- Die Ausgabe von `claude setup-token` nie auf dem Bildschirm zeigen ([S4.4](../library/s4-04-ci-zugang-und-kosten.md)).
- Die Telegram-Bridge weglassen, außer sie ist vorkonfiguriert und schon getestet
  ([S4.6](../library/s4-06-remote-und-teleport.md)).

### Am Workshop-Tag

Pre-Flight und, in Session 3 und 4, die Go/No-Go-Matrix aus dem [Handbuch](handbuch.md#gono-go-je-demo).

## Workshop-Plugins

Zwei Arten von Plugins kommen vor, und sie werden unterschiedlich beschafft:

- **Das Workshop-Plugin `dynamic-workshop`** aus diesem Repo: Tutor `/dynamic-workshop:workshop` und Mentor-Agent.
  Es ist öffentlich erreichbar und für alle gedacht.
- **Die Demo-Plugins** 🔧 `agentic-os`, `devil-advocate-swarms` und `multi-model-orchestrator`, dazu der User-Skill
  `notebooklm` und das Plugin `telegram-bridge`. Sie wurden eigens für diesen Workshop gebaut. Sie gehören nicht zur
  offiziellen Claude-Code-Installation, stehen in keinem öffentlichen Marketplace von Anthropic und werden nicht von
  Anthropic gepflegt.

Session 1 braucht keines davon. Session 2 läuft auch ohne sie: Für die Plugin-Anatomie in S2.11 reicht jedes
installierte Plugin, und statt des `notebooklm`-Skills geht die Web-Oberfläche. Nötig sind die Demo-Plugins nur für die
Live-Varianten in Session 3 und 4. Installiere, was du live zeigen willst, **vor Session 2**.

### Welche Demo welches Plugin nutzt

| Baustein 🔧 | Genutzt in | Ohne ihn |
|---|---|---|
| `agentic-os` | [S2.11](../library/s2-11-plugins-buendeln.md) Plugin-Anatomie (jedes andere installierte Plugin geht auch), [S3.14](../library/s3-14-self-improve-loop.md) Self-Improve-Loop | Fallback im Kapitel unter „Für Moderierende" |
| `devil-advocate-swarms` | [S3.6](../library/s3-06-devils-advocate.md) Devil's Advocate | Weg ohne Plugin aus S3.6 oder Aufzeichnung |
| `multi-model-orchestrator` | [S4.2](../library/s4-02-codex-schwarm.md) Codex-Schwarm, [S4.7](../library/s4-07-isolation-docker-worktrees.md) Inception (optional) | Fallback im Kapitel unter „Für Moderierende" |
| `notebooklm` (User-Skill) | [S2.18](../library/s2-18-rag-und-notebooklm.md) Demo und Übung | Web-Oberfläche notebooklm.google.com |
| `telegram-bridge` | [S4.6](../library/s4-06-remote-und-teleport.md), nur der Bonus-Schritt | `/remote-control` (eingebaut) |

### Das Workshop-Plugin aus diesem Repo

Das Plugin liegt im Workshop-Repo `https://github.com/dynamic-dome/dynamic-workshop.git`. Das Installationsskript
klont das Repo nach `~/cc-workshop/dynamic-workshop` oder aktualisiert einen vorhandenen, sauberen Klon:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_workshop_plugin.ps1
```

Dann startest du Claude Code mit dem Repo als Plugin-Quelle. Das Skript gibt am Ende einen Pfad mit `.claude-plugin`
aus; nimm stattdessen diesen Befehl:

```bash
claude --plugin-dir ~/cc-workshop/dynamic-workshop
```

`--plugin-dir` bekommt das Wurzelverzeichnis des Plugins, also den Ordner, der `.claude-plugin/plugin.json` enthält,
nicht den Ordner `.claude-plugin` selbst.

### Die Demo-Plugins

Du hast drei Wege, dazu einen vierten für Selbstlernende:

- **Live zeigen:** Willst du `agentic-os`, `devil-advocate-swarms` oder `multi-model-orchestrator` live zeigen, stell
  den Teilnehmenden vor dem Workshop einen echten Git- oder Drive-Release-Link bereit. Verlass dich beim Setup der
  Teilnehmenden nicht auf einen unveröffentlichten Tarball.
- **Nur beobachten:** Die Teilnehmenden sehen die Demo bei dir oder als Aufzeichnung. Die Muster dahinter
  (adversariale Swarms, Multi-Model-Pipelines, Self-Improve-Loops) lassen sich auf eigene Plugins übertragen.
- **Selbst nachbauen:** Nach [S2.2](../library/s2-02-skill-schreiben.md) (Skills) und
  [S2.11](../library/s2-11-plugins-buendeln.md) (Plugins) lassen sich vereinfachte Versionen dieser Muster bauen; die
  Kapitel zeigen den Aufbau.

## notebooklm-Skill

Der User-Skill `notebooklm` 🔧 gehört nicht zum offiziellen Claude Code. Er wird in der Demo und der Übung von
[S2.18](../library/s2-18-rag-und-notebooklm.md) genutzt.

**Option A: Skill von dir als Moderation.** Du gibst den Teilnehmenden einen Tarball oder eine lokale Kopie; sie entpacken
sie nach `~/.claude/skills/notebooklm/`.

```bash
mkdir -p ~/.claude/skills
# Then place the moderator-provided skill folder at ~/.claude/skills/notebooklm
```

Prüfen mit `/skills`: `notebooklm` muss in der Liste stehen.

**Option B: die offizielle Web-Oberfläche** (notebooklm.google.com). Dann laufen Demo und Übung über die Web-Oberfläche
statt über die CLI-Befehle; die Recovery-Schritte stehen im Kapitel.

## Hook-Datei für die Demo

Die Hook-Demo in [S2.8](../library/s2-08-hook-einrichten.md) nutzt eine vorbereitete Hook-Datei unter
`~/.claude/hooks/security-check.sh`. Leg sie vor der Demo an.

Der Hook ist das getestete Safety-Skript aus dem Repo (`resources/demos/assets/hooks/safety-check.*`), dasselbe, das
die Übung in S2.8 baut. Es liest den Befehl aus `tool_input.command` und blockt mit **exit 2**, dem einzigen
Exit-Code, der blockt. Kopier es, statt es abzutippen.

**macOS, Linux, Git Bash** (braucht `jq`, siehe [S0.1](../library/s0-01-werkstatt-einrichten.md)):

```bash
mkdir -p ~/.claude/hooks
cp ~/cc-workshop/dynamic-workshop/resources/demos/assets/hooks/safety-check.sh ~/.claude/hooks/security-check.sh
chmod +x ~/.claude/hooks/security-check.sh

# Smoke test with an input in the real format - expect "blocked" and exit=2:
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"}}' | bash ~/.claude/hooks/security-check.sh; echo "exit=$?"
```

**Windows, PowerShell** (kein `jq`, kein `chmod` nötig):

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.claude/hooks" | Out-Null
Copy-Item "$HOME/cc-workshop/dynamic-workshop/resources/demos/assets/hooks/safety-check.ps1" "$HOME/.claude/hooks/security-check.ps1"

# Smoke test with an input in the real format - expect "blocked" and exit=2:
'{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"}}' | powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME/.claude/hooks/security-check.ps1"; "exit=$LASTEXITCODE"
```

Trag den Hook in `~/.claude/settings.json` ein. Nimm den `command`, der zu deinem Skript passt:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash ~/.claude/hooks/security-check.sh" }
        ]
      }
    ]
  }
}
```

> **Windows:** Ersetze den Wert von `command` durch `"pwsh -File $HOME/.claude/hooks/security-check.ps1"` (oder
> `powershell -File ...` für Windows PowerShell 5.1). Willst du die bash-Variante, installiere **Git Bash und `jq`**
> (siehe [S0.1](../library/s0-01-werkstatt-einrichten.md)) und behalte den Befehl `bash ...`.

## NotebookLM-Notebook

Die Demo in [S2.18](../library/s2-18-rag-und-notebooklm.md) nutzt ein vorbereitetes Notebook namens
`claude-code-docs` mit der offiziellen Claude-Code-Dokumentation als Quellen. Leg es vor Session 2 an:

```bash
# CLI variant (if notebooklm CLI is available)
notebooklm create "claude-code-docs"
notebooklm add-source https://code.claude.com/docs/en/overview --notebook claude-code-docs
notebooklm add-source https://code.claude.com/docs/en/skills --notebook claude-code-docs
notebooklm add-source https://code.claude.com/docs/en/hooks --notebook claude-code-docs
```

Die Befehle hängen vom Werkzeug ab: Die Kursquellen nennen für das Hinzufügen zwei Schreibweisen, und das
Python-Paket `notebooklm-py` (geprüft mit Version 0.8.2) kennt kein `add-source`. Dort heißt es
`notebooklm source add <url>`, und es wirkt auf das aktive Notebook (`notebooklm create "claude-code-docs" --use`).
Prüf die Syntax vorher mit `notebooklm --help`.

Oder du nimmst die Web-Oberfläche: notebooklm.google.com → Notebook anlegen → „claude-code-docs" → Webquellen
hinzufügen.

## Playwright-MCP vorab laden

Die Übung in [S2.14](../library/s2-14-mcp-stecker.md) bindet den Playwright-MCP-Server ein, der über
`npx @playwright/mcp` läuft. Beim ersten Start lädt `npx` das Paket **und** Playwright eine Browser-Binärdatei
herunter. Das kann die Live-Session eine Minute oder länger aufhalten. Füll den Cache deshalb **vor Session 2**, damit
auf der Bühne nichts lädt:

```bash
# Pre-download the MCP package + its browser into the npx/Playwright cache:
npx -y @playwright/mcp@latest --help   # pulls the package
npx -y playwright install chromium     # pulls the browser binary
```

Danach startet die Übung den Server aus dem Cache, ohne Download.

## Codex CLI

Die OpenAI Codex CLI ist **optional** und nur für [S4.2](../library/s4-02-codex-schwarm.md) (Codex-Schwarm) nötig.
S4.2 ist Kür; die Teilnehmenden können deine Demo auch nur beobachten.

**Weg 1: die offizielle Codex CLI**, sofern in deiner Region verfügbar. Doku: https://developers.openai.com/codex/cli.
Installation über den Paketmanager oder die GitHub-Releases.

**Weg 2: ohne Installation.** Die Demo lässt sich beobachten, aber nicht lokal nachfahren.

Prüfen, wenn du Weg 1 gegangen bist:

```bash
codex --version
codex login status  # ensure authenticated to your OpenAI account
```

## Abschlussprüfung

Nach allen Installationen ein kurzer Durchlauf:

```bash
claude plugin list                      # shows installed plugins (0–3 depending on which option you chose)
claude --plugin-dir ~/cc-workshop/dynamic-workshop   # verifies local workshop plugin loads
/skills                                 # should show notebooklm (only if you used Custom User-Skills Option A)
ls ~/.claude/hooks/security-check.sh    # macOS/Linux/Git Bash — the hook file should exist
# Windows PowerShell: Test-Path "$HOME/.claude/hooks/security-check.ps1"   # should print True
notebooklm list                         # should show claude-code-docs (only if you used CLI variant)
```

Die Zeilen zu Plugin, Skill und `notebooklm` betreffen dich nur, wenn du die optionalen Demo-Plugins, den
`notebooklm`-Skill oder die `notebooklm`-CLI installiert hast. Session 1 und der größte Teil von Session 2 laufen ohne
sie. `/skills` tippst du in einer laufenden Claude-Code-Sitzung.
