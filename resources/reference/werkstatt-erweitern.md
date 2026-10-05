# Werkstatt erweitern: was du erst später brauchst

Wofür: Nach [S0.1](../library/s0-01-werkstatt-einrichten.md) hast du Claude Code, eine Anmeldung, Git und Python. Das reicht bis weit in die erste Session. Alles auf dieser Seite installierst du erst, wenn ein Kapitel es verlangt; die Kapitel verweisen hierher.

Geprüft am 2026-10-05 (CLI 2.1.289). Offizielle Quelle für Claude Code selbst: https://code.claude.com/docs/en/setup · Die Installationsbefehle für Git-Werkzeuge, Node.js und `jq` stammen von den jeweiligen Projekten.

| Baustein | Gebraucht ab | Wofür |
|---|---|---|
| [Workshop-Repo mit Playground](#workshop-repo-und-playground) | [X.2](../library/x-02-lernen-mit-claude-code.md) (Tutor), [S2.8](../library/s2-08-hook-einrichten.md) (Playground) | Tutor-Plugin, Übungsrepo mit eingebauten Schwachstellen, getestete Hook-Vorlagen |
| [GitHub CLI](#github-cli) | [S1.16](../library/s1-16-git-in-einem-fluss.md) | Pull Requests aus der Sitzung heraus (`gh pr create`) |
| [jq](#jq) | [S2.8](../library/s2-08-hook-einrichten.md) | die Bash-Varianten der Hook-Skripte lesen damit ihre Eingabe |
| [Node.js](#nodejs) | [S2.14](../library/s2-14-mcp-stecker.md) | `npx` für MCP-Server; außerdem die npm-Variante von Claude Code |
| [Workshop-Doktor](#workshop-doktor) | freiwillig | prüft unter Windows alles auf einmal |

## Workshop-Repo und Playground

Alles, was zur Bibliothek gehört, liegt unter einem Ordner, `~/cc-workshop`. Deine Übungsordner aus den Kapiteln liegen schon dort (`hello`, `rechte`, `kontext` und so weiter). Das Repo kommt daneben; der Playground ist ein Unterordner des Repos:

```bash
mkdir -p ~/cc-workshop
git clone https://github.com/dynamic-dome/dynamic-workshop.git ~/cc-workshop/dynamic-workshop
cd ~/cc-workshop/dynamic-workshop/workshop-playground

# Install Python dependencies   (Windows: use pip instead of pip3)
pip3 install -r requirements.txt

# Verify tests run   (Windows: use python instead of python3)
python3 -m pytest -v
```

Fertig, wenn die Tests grün sind. Danach sieht dein Ordner so aus:

```
~/cc-workshop/
├── dynamic-workshop/          # the cloned repo: tutor plugin, hook templates, this library
│   └── workshop-playground/   #   the playground: ~/cc-workshop/dynamic-workshop/workshop-playground
├── hello/  rechte/  kontext/  # your exercise folders from the chapters
└── lernen/                    # your learning folder, if you use the tutor (X.2)
```

Übungen, die den Playground nennen, meinen den Pfad im Repo. Arbeite dort auf einem eigenen Branch; der Stand auf `main` ist das Übungsmaterial. Am Ende räumst du mit `rm -rf ~/cc-workshop` alles auf einmal weg, samt Klon und allem, was du darin geändert hast.

- **Die Tests scheitern.** Prüf die Python-Version (`python3 --version`, 3.9 oder neuer) und führ `pip3 install -r requirements.txt` noch einmal aus (Windows: `pip`).
- **Die Lösungen** zu den eingebauten Schwachstellen stehen in [playground-loesungen.md](playground-loesungen.md), absichtlich außerhalb des Playgrounds.

## GitHub CLI

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

Fertig, wenn `gh auth status` dein Konto zeigt.

## jq

Die Bash-Varianten der Hook-Skripte lesen ihre Eingabe mit `jq`. Fehlt `jq`, blocken die Schutz-Hooks absichtlich jeden Aufruf, statt ihn ungeprüft durchzulassen. Unter Windows ohne Git Bash nimmst du die PowerShell-Varianten; die brauchen kein `jq`.

Installieren laut [jq-Downloadseite](https://jqlang.org/download/):

- **Windows:** `winget install jqlang.jq`
- **macOS:** `brew install jq`
- **Linux (Debian, Ubuntu):** `sudo apt-get install jq`

Fertig, wenn `jq --version` eine Version zeigt.

## Node.js

Mit dem nativen Installer braucht Claude Code selbst kein Node.js. Du brauchst es für `npx`, mit dem viele MCP-Server starten, etwa der Playwright-Server in [S2.14](../library/s2-14-mcp-stecker.md).

- **Windows:** Download von [nodejs.org](https://nodejs.org/) (LTS-Version) oder `winget install OpenJS.NodeJS.LTS`
- **macOS:** `brew install node` oder Download von [nodejs.org](https://nodejs.org/)
- **Linux:** die LTS-Version nach der Anleitung auf [nodejs.org](https://nodejs.org/en/download)

Fertig, wenn `node --version` und `npm --version` je eine Version zeigen. Nimm die aktuelle LTS-Version.

**Die npm-Variante von Claude Code.** Claude Code gibt es weiterhin als npm-Paket; empfohlen ist der native Installer. Das npm-Paket verlangt laut Doku Node.js 22 oder neuer. Auf einer älteren Version warnt npm nur (`EBADENGINE`), und `claude` läuft trotzdem. Ohne globale Installation startest du Claude Code über `npx`, das dasselbe Paket lädt:

```bash
npx @anthropic-ai/claude-code
```

Meldet npm einen Rechtefehler (`EACCES`), rät die Doku, auf den nativen Installer zu wechseln, und warnt ausdrücklich vor `sudo npm install -g`.

## Workshop-Doktor

Der Workshop-Doktor ist ein PowerShell-Skript im Repo, also nur für Windows. Er prüft Node.js, Git, Python und Claude Code, den Klon unter `~/cc-workshop/dynamic-workshop`, die Playground-Tests und das Manifest des Workshop-Plugins und meldet am Ende `READY` oder `NOT READY`. Starte ihn im Wurzelordner des Klons, nicht im Playground:

```powershell
# From the cloned workshop repo:
powershell -ExecutionPolicy Bypass -File .\tools\workshop_doctor.ps1
```

`-ExecutionPolicy Bypass` gilt nur für diesen einen Aufruf: PowerShell führt das Skript aus, obwohl es nicht signiert ist. Lies ein Skript, bevor du es so startest. Unter macOS und Linux prüfst du die Bausteine einzeln mit den Befehlen oben.
