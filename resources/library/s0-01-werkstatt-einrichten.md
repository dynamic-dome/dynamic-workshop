---
id: S0.1
type: setup
title: Werkstatt einrichten
shelf: start
level: core
minutes: 20
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann Claude Code installieren und anmelden, Git, Python 3 und Node.js prüfen und mit `claude --print` und den Playground-Tests nachweisen, dass meine Werkstatt bereit ist."
sources:
  - https://code.claude.com/docs/en/setup
  - https://code.claude.com/docs/en/authentication
  - https://code.claude.com/docs/en/troubleshoot-install
aliases: [setup]
---

# S0.1 · Werkstatt einrichten

<!-- meta:start -->
> **Regal:** [Erste Schritte & Denkmodell](README.md#start) · **Stufe:** Kern · **~20 Min** · **Voraussetzungen:** keine
>
> [Bibliothek](README.md) · [X.2 Mit Claude Code lernen](x-02-lernen-mit-claude-code.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du auf diesem Rechner schon `claude --version` und `claude --print "Say hello"` ohne Fehler laufen lassen?
- Hast du den `workshop-playground` schon geklont und seine Tests mit `pytest` grün durchlaufen sehen?

## Auf einen Blick

Bevor du mit S1.1 loslegst, richtest du einmal deine Werkstatt ein: Claude Code über den nativen Installer, eine Anmeldung mit Abo oder API-Key, dazu Git, Python 3, Node.js und den geklonten `workshop-playground`. Fertig bist du, wenn `claude --version` eine Version zeigt, `claude --print` antwortet und die Playground-Tests grün sind.

Plane etwa 20 Minuten ein, unter Windows mit Git Bash und `jq` eher 30. Arbeite der Reihe nach und lass Optionales bis zuletzt liegen. `jq` und die GitHub CLI brauchst du erst in späteren Kapiteln. Die Extras für die Demos (Workshop-Plugins, NotebookLM, Playwright, Codex CLI) stehen in der [Vorbereitung für Moderierende](../moderation/vorbereitung.md).

## Im Detail

### Was dein Rechner braucht

| Was | Mindestens | Empfohlen |
|---|---|---|
| **Betriebssystem** | macOS 13.0+, Windows 10 1809+ oder Windows Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+ | aktuelle Version |
| **Hardware** | 4 GB RAM, x64- oder ARM64-Prozessor | 8 GB RAM oder mehr |
| **Speicherplatz** | 500 MB frei | 2 GB oder mehr |
| **Shell und Terminal** | Bash, Zsh, PowerShell oder CMD | Windows Terminal, iTerm2 oder Warp |
| **Internet** | nötig | stabile Verbindung (API-Aufrufe) |
| **Standort** | ein [unterstütztes Land](https://www.anthropic.com/supported-countries) | — |

Betriebssystem, Hardware, Shell, Internet und Standort stehen so in der offiziellen Doku; Speicherplatz und die Empfehlungen stammen aus der bisherigen Kursanleitung. Node.js steht nicht mehr in der Tabelle: Claude Code selbst braucht es mit dem nativen Installer nicht ([unten](#nodejs-für-npx-und-die-npm-variante)).

### Claude Code installieren

Empfohlen ist der native Installer. Öffne ein Terminal und nimm den Befehl für dein System, unter Windows in PowerShell:

```powershell
# Windows
irm https://claude.ai/install.ps1 | iex

# Alternative on Windows
winget install Anthropic.ClaudeCode
```

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Alternative on macOS / Linux
brew install --cask claude-code
```

Die native Installation aktualisiert sich selbst im Hintergrund. Hast du über Homebrew oder WinGet installiert, aktualisierst du selbst: `brew upgrade claude-code` bzw. `winget upgrade Anthropic.ClaudeCode`.

Öffne danach ein neues Terminal und prüf die Installation. `claude update` bringt eine vorhandene Installation sofort auf den neuesten Stand:

```bash
# Verify installation
claude --version

# Already installed? Update to a recent build:
claude update
```

Kennt die Shell `claude` danach nicht, liegt der Installationsordner noch nicht im `PATH` (siehe „Typische Fallen“).

**npm und npx.** Claude Code gibt es weiterhin als npm-Paket, empfohlen ist aber der native Installer. Das npm-Paket verlangt laut Doku seit v2.1.198 Node.js 22 oder neuer; auf einer älteren Version warnt npm nur (`EBADENGINE`), und `claude` läuft trotzdem. Ohne globale Installation startest du Claude Code über `npx`, das dasselbe npm-Paket lädt:

```bash
npx @anthropic-ai/claude-code
```

**Desktop-App und Web (optional).** Wer lieber ohne Terminal arbeitet, nimmt die Desktop-App (macOS und Windows, Linux als Beta), siehe [Desktop-Schnellstart](https://code.claude.com/docs/en/desktop-quickstart). Die Web-Version läuft im Browser unter claude.ai/code. Was die Oberflächen unterscheidet, zeigt [S1.3](s1-03-oberflaechen.md).

### Welche Version du brauchst

Die Kursinhalte wurden am 2026-07-04 gegen `claude --version` **2.1.200** aufgefrischt. Als getestetes Minimum für den ganzen Kurs gilt **2.1.197+**: Ab da sind die Aliase `fable`/`opus`/`sonnet`/`haiku`, die Workflow-Fixes, die Plugin-Verbesserungen und das aktuelle Hook-Verhalten abgedeckt. Die Generationen, auf die diese Aliase heute auflösen, brauchen eine neuere CLI; welche Version für welche Generation, steht im [Kanon](../_canonical.md#aktuelle-claude-modelle). Prüf `claude --version`.

| Im Kurs genutzt | Dokumentiert ab | So prüfst du es |
|---|---:|---|
| `claude plugin init` und lokale Plugin-Verbesserungen | 2.1.157 | `claude plugin init`, `claude --plugin-dir` |
| Fable-Tier | 2.1.170 | `/model` zeigt nach dem Update `fable` |
| Agenten-Details und Status in `/workflows` | 2.1.186 | `/workflows` ist in aktuellen CLI-Builds da |
| Hook-JSON-Ausgabe (`updatedToolOutput`, `systemMessage`, `terminalSequence`) | aktuelle Hooks-Doku | im Repo `python -m pytest tools/test_course_hooks.py`, dann [S2.8](s2-08-hook-einrichten.md) und [S2.10](s2-10-hook-ausgaben.md) |
| Sonnet-Tier mit erweitertem Kontextfenster (Größe im [Kanon](../_canonical.md)) | 2.1.197 | `claude --version`, `/model` |

Im Zweifel gelten `claude --version`, `/model`, `/workflows` und `/release-notes`, nicht eine Versionsnummer in älterem Material. Den kurzen Rundum-Check nach einem Update findest du in „Selbst machen“, Schritt 3.

### Anmelden

```bash
# Start Claude Code and log in
claude
# Then run:
/login
```

Beim ersten Start öffnet Claude Code ein Browserfenster für die Anmeldung; mit `/login` startest du sie jederzeit neu. Ist die Umgebungsvariable `ANTHROPIC_API_KEY` gesetzt, fragt Claude Code stattdessen einmal, ob es den Key verwenden soll.

Du brauchst eines davon:

- **Ein Claude-Abo:** Pro oder Max (für den Workshop empfohlen), im Unternehmen auch Team oder Enterprise. Der kostenlose claude.ai-Plan enthält Claude Code nicht.
- **Einen API-Key aus der Claude Console**, gesetzt als Umgebungsvariable `ANTHROPIC_API_KEY`. Unter Windows öffnest du nach `setx` das Terminal neu:

```powershell
  # Windows PowerShell — current session only:
  $env:ANTHROPIC_API_KEY = "sk-ant-..."
  # Windows — persist across sessions (re-open the terminal afterwards):
  setx ANTHROPIC_API_KEY "sk-ant-..."
```

```bash
  # macOS / Linux / Git Bash:
  export ANTHROPIC_API_KEY="sk-ant-..."        # current session
  echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc   # persist
```

- **Einen Cloud-Anbieter** (Unternehmens-Setups): Amazon Bedrock, Google Cloud's Agent Platform oder Microsoft Foundry.

Prüf, ob die Anmeldung funktioniert:

```bash
claude --print "Say hello"
# Should return a response without errors
```

Hast du ein Abo und zusätzlich einen API-Key gesetzt, nimmt Claude Code nach deiner Bestätigung den Key (siehe „Typische Fallen“).

### Git

Git brauchst du für das Workshop-Repo und die Git-Kapitel ab [S1.16](s1-16-git-in-einem-fluss.md).

```bash
git --version   # Should show 2.30+
```

Installieren, falls nötig:

- **Windows:** `winget install Git.Git` oder Download von [git-scm.com](https://git-scm.com/)
- **macOS:** `xcode-select --install` oder `brew install git`
- **Linux:** `sudo apt install git`

Unter Windows bringt Git for Windows auch Git Bash mit. Claude Code nutzt Git Bash dann für sein Bash-Tool; ohne Git for Windows führt es Shell-Befehle über PowerShell aus.

### Python 3

Python brauchst du ab der ersten Übung ([S1.1](s1-01-erster-kontakt.md), die Aufgabe mit `event_log_parser.py`) und für den `workshop-playground` (pytest-Tests, Schwachstellen-Demos). Installier es also vor S1.1.

Prüfen (unter Windows heißen die Befehle `python`/`pip`, unter macOS und Linux `python3`/`pip3`):

```bash
python3 --version   # Windows: python --version    (should show 3.9+)
pip3 --version      # Windows: pip --version
```

Installieren, falls nötig:

- **Windows:** `winget install Python.Python.3.12` oder Download von [python.org](https://python.org/)
- **macOS:** `brew install python`
- **Linux:** `sudo apt install python3 python3-pip`

### Node.js: für npx und die npm-Variante

Mit dem nativen Installer braucht Claude Code selbst kein Node.js. Du installierst es trotzdem: für `npx` (etwa den Playwright-MCP-Server in [S2.14](s2-14-mcp-stecker.md)), für die npm-Variante von Claude Code, und der Workshop-Doktor in „Selbst machen“ prüft es mit.

```bash
node --version   # Should show v18+ or v20+
npm --version    # Should show 9+
```

Die Untergrenze v18 im Kommentar stammt aus der bisherigen Kursanleitung, die v20 LTS oder v22 LTS empfahl. Für die npm-Variante von Claude Code nennt die Doku Node.js 22 oder neuer ([oben](#claude-code-installieren)).

Installieren, falls nötig:

- **Windows:** Download von [nodejs.org](https://nodejs.org/) (LTS-Version) oder `winget install OpenJS.NodeJS.LTS`
- **macOS:** `brew install node` oder Download von [nodejs.org](https://nodejs.org/)
- **Linux:** `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs`

### jq: für die Bash-Varianten der Hooks

Die Bash-Varianten der Hook-Skripte ab [S2.8](s2-08-hook-einrichten.md) lesen ihre Eingabe mit `jq`. Fehlt `jq`, blockt der Safety-Hook absichtlich jeden Bash-Befehl. Unter Windows ohne Git Bash nimmst du die PowerShell-Varianten; die brauchen kein `jq`.

Installieren laut [jq-Downloadseite](https://jqlang.org/download/):

- **Windows:** `winget install jqlang.jq`
- **macOS:** `brew install jq`
- **Linux (Debian, Ubuntu):** `sudo apt-get install jq`

### GitHub CLI (optional)

Die GitHub CLI `gh` brauchst du für PR-Abläufe wie `gh pr create` in [S1.16](s1-16-git-in-einem-fluss.md) und [S1.17](s1-17-git-befehle.md).

```bash
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh

# Then authenticate
gh auth login
```

## Selbst machen

### Übung: die Werkstatt aufbauen und abhaken

**Ziel:** Alles liegt an seinem Platz, und du hast mit echten Befehlen nachgewiesen, dass es läuft. Danach kannst du S1.1 direkt beginnen.

**Schritt 1: das Workshop-Repo klonen und die Playground-Tests laufen lassen**

Alles, was zum Workshop gehört, kommt unter einen einzigen Ordner, `~/cc-workshop`. Der erste Befehl legt ihn an, dann klonst du das Workshop-Repo hinein. Der Playground ist ein Unterordner des Repos:

```bash
# Variant A: Clone the workshop repo (this contains the playground)
mkdir -p ~/cc-workshop
git clone https://github.com/dynamic-dome/dynamic-workshop.git ~/cc-workshop/dynamic-workshop
cd ~/cc-workshop/dynamic-workshop/workshop-playground

# Variant B: If your workshop moderator provided a different path/URL, use that one instead.

# Install Python dependencies   (Windows: use pip instead of pip3)
pip3 install -r requirements.txt

# Verify tests run   (Windows: use python instead of python3)
python3 -m pytest -v
```

Die Clone-URL war am 2026-09-30 mit `git ls-remote https://github.com/dynamic-dome/dynamic-workshop.git HEAD` erreichbar.

**Schritt 2: den Arbeitsordner kennen**

Unter `~/cc-workshop` gilt diese Aufteilung:

```
~/cc-workshop/
├── dynamic-workshop/          # git clone of the workshop repo (see clone step above)
│   └── workshop-playground/   #   ← the playground lives HERE: ~/cc-workshop/dynamic-workshop/workshop-playground
├── demos/                     # Live demo workdirs (one per demo: demo-1.1, demo-1.2, ...)
└── exercises/                 # Exercise workdirs (one per exercise: exercise-1.1, ...)
```

Der Playground liegt **im geklonten Repo** (`dynamic-workshop/workshop-playground`), nicht direkt unter `~/cc-workshop/`. Übungen, die ihn nennen, meinen diesen Pfad. `demos/` und `exercises/` sind nur Arbeitsordner, die du bei Bedarf von Hand anlegst.

So liegt alles an einem Ort, Demos und Übungen landen nicht in deinem Home-Ordner, und nach dem Workshop räumst du mit `rm -rf ~/cc-workshop` alles auf einmal weg, samt Klon und allem, was du darin geändert hast.

**Schritt 3: der Rundum-Check**

Nach der Installation und nach jedem Update zeigt dieser Check, ob Version und Anmeldung stimmen:

<!-- cockpit:example -->
```bash
# Verify feature surface after update
claude --version
claude --print "Say ready"
```

**Schritt 4 (optional): der Workshop-Doktor**

Der Workshop-Doktor ist ein PowerShell-Skript im Repo. Er prüft Node.js, Git, Python und Claude Code, den Klon unter `~/cc-workshop/dynamic-workshop`, die Playground-Tests und das Manifest des Workshop-Plugins und meldet am Ende `READY` oder `NOT READY`. Starte ihn im Wurzelordner des Klons, nicht im Playground:

```powershell
# From the cloned workshop repo:
powershell -ExecutionPolicy Bypass -File .\tools\workshop_doctor.ps1
```

**Geschafft, wenn:**

- [ ] `claude --version` eine aktuelle Version zeigt
- [ ] `claude --print "Hello"` antwortet (die Anmeldung funktioniert)
- [ ] `git --version` 2.30 oder neuer zeigt
- [ ] `python3 --version` (Windows: `python --version`) 3.9 oder neuer zeigt
- [ ] `node --version` v18 oder neuer zeigt (für die npm-Variante von Claude Code: 22 oder neuer)
- [ ] der Playground geklont ist und seine Tests grün sind
- [ ] dein Terminal Unicode und ANSI-Farben kann:
  - macOS, Linux, Git Bash: `echo -e "\033[32mGreen\033[0m"`
  - Windows PowerShell 7+: `` Write-Host "`e[32mGreen`e[0m" `` (in PowerShell 5.1: `"$([char]27)[32mGreen$([char]27)[0m"`)
- [ ] `jq` installiert ist, falls du die Bash-Varianten der Hooks ab S2.8 nutzen willst

**Für den Live-Workshop:** Bring deinen Laptop mit fertigem Setup mit, dazu gern eine Projektidee, die du mit Claude Code ausprobieren willst. Fragen zum Setup klärst du vor dem Termin mit der Moderation.

## Typische Fallen

- **`claude` wird nicht gefunden** (`command not found` oder `'claude' is not recognized`). Der Installationsordner liegt nicht im `PATH`. Der Installer legt `claude` unter `~/.local/bin/claude` (macOS, Linux) bzw. `%USERPROFILE%\.local\bin\claude.exe` (Windows) ab. Öffne ein neues Terminal; hilft das nicht, trag den Ordner in den `PATH` ein ([Anleitung in der Doku](https://code.claude.com/docs/en/troubleshoot-install#command-not-found-claude-after-installation)).
- **`'irm' is not recognized`.** Du bist in CMD, nicht in PowerShell. In PowerShell beginnt der Prompt mit `PS`; führ den Installer dort aus.
- **npm meldet einen Rechtefehler (`EACCES`).** Das betrifft nur die npm-Variante. Die Doku rät, dann auf den nativen Installer zu wechseln, und warnt ausdrücklich vor `sudo npm install -g`.
- **`npm: command not found`.** Node.js fehlt; installier es ([Node.js](#nodejs-für-npx-und-die-npm-variante)).
- **Die Anmeldung schlägt fehl.** Prüf den API-Key bzw. den Status deines Abos und starte `/login` noch einmal.
- **Abo und API-Key zugleich.** Ist `ANTHROPIC_API_KEY` gesetzt, nutzt Claude Code nach deiner Bestätigung den Key statt deines Abos. Gehört der Key zu einer deaktivierten oder abgelaufenen Organisation, scheitert die Anmeldung. `/status` zeigt, welche Methode aktiv ist. Entfernst du die Variable (`unset ANTHROPIC_API_KEY`), nimmt Claude Code wieder das Abo; hast du sie mit `setx` oder in `~/.bashrc` dauerhaft gesetzt, nimm sie auch dort heraus.
- **Python wird unter Windows nicht gefunden.** Nimm `python` statt `python3` oder installier Python aus dem Microsoft Store.
- **Die Playground-Tests scheitern.** Prüf die Python-Version und führ `pip3 install -r requirements.txt` noch einmal aus (Windows: `pip`).
- **Keine oder nur langsame Antworten.** Prüf die Internetverbindung; `claude --verbose` zeigt mehr Details.

Für eine gründliche Diagnose tippst du in einer laufenden Sitzung `/doctor`: Es prüft Installation, Einstellungen, Erweiterungen und Kontextnutzung und schlägt Korrekturen vor, die es nach deiner Bestätigung anwendet. Startet `claude` gar nicht, nimmst du im Terminal:

```bash
claude doctor
```

## Check

Du kannst Claude Code installieren und anmelden und mit `claude --version`, `claude --print` und den Playground-Tests nachweisen, dass deine Werkstatt steht.

1. Wofür brauchst du Node.js, wenn Claude Code selbst über den nativen Installer kommt?
2. Wo liegt der `workshop-playground` nach dem Klonen?
3. Was tust du, wenn die Shell nach der Installation `claude` nicht kennt?

<details><summary>Quizfrage</summary>

**Frage:** Du hast ein Max-Abo und zusätzlich `ANTHROPIC_API_KEY` in deiner Shell gesetzt. Welche Anmeldung nutzt Claude Code, nachdem du den Key beim Start einmal bestätigt hast?

- **Richtig:** Den API-Key; `/status` zeigt dir, welche Methode gerade aktiv ist.
- Falsch: Das Abo, weil eine `/login`-Anmeldung immer vor Umgebungsvariablen kommt.
- Falsch: Beide abwechselnd, je nachdem, welches Kontingent gerade noch frei ist.
- Falsch: Keine, bis du eine der beiden Anmeldungen wieder entfernt hast.

</details>

## Weiterlesen

- [Installation und Systemvoraussetzungen (Advanced setup)](https://code.claude.com/docs/en/setup)
- [Anmeldung (Authentication)](https://code.claude.com/docs/en/authentication)
- [Fehlersuche bei Installation und Anmeldung](https://code.claude.com/docs/en/troubleshoot-install)
- [Quickstart: die erste Sitzung](https://code.claude.com/docs/en/quickstart)
- [S1.1 · Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md)
- [S1.3 · Die Oberflächen: CLI, Desktop, IDE, Web, iOS](s1-03-oberflaechen.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S2.14 · MCP: der Integrationsstecker](s2-14-mcp-stecker.md)
- Für Moderierende: [Vorbereitung](../moderation/vorbereitung.md) mit Workshop-Plugins, Demo-Hook, NotebookLM-Notebook, Playwright-MCP und Codex CLI
