---
id: S0.1
type: setup
title: Werkstatt einrichten
shelf: start
level: core
minutes: 25
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann Claude Code installieren und anmelden, Git und Python 3 prüfen und mit `claude --version` und `claude --print` nachweisen, dass meine Werkstatt bereit ist."
sources:
  - https://code.claude.com/docs/en/setup
  - https://code.claude.com/docs/en/authentication
  - https://code.claude.com/docs/en/troubleshoot-install
aliases: [setup]
---

# S0.1 · Werkstatt einrichten

<!-- meta:start -->
> **Regal:** [Erste Schritte & Denkmodell](README.md#start) · **Stufe:** Kern · **~25 Min** · **Voraussetzungen:** keine
>
> [Bibliothek](README.md) · [S1.1 Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du auf diesem Rechner schon `claude --version` und `claude --print "Say hello"` ohne Fehler laufen lassen?
- Zeigen `git --version` und `python3 --version` (Windows: `python --version`) bei dir je eine Version?

## Auf einen Blick

Bevor du mit S1.1 loslegst, richtest du einmal deine Werkstatt ein: Claude Code über den nativen Installer, eine Anmeldung mit Abo oder API-Key, dazu Git und Python 3. Fertig bist du, wenn `claude --version` eine Version zeigt und `claude --print "Say hello"` antwortet.

Mehr brauchst du für den Anfang nicht. Node.js, `jq`, die GitHub CLI und das Workshop-Repo mit dem Playground kommen erst in späteren Kapiteln vor; wie du sie dann nachrüstest, steht auf der Karte [Werkstatt erweitern](../reference/werkstatt-erweitern.md).

## Im Detail

### Was dein Rechner braucht

| Was | Mindestens |
|---|---|
| **Betriebssystem** | macOS 13.0+, Windows 10 1809+ oder Windows Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+ |
| **Hardware** | 4 GB RAM, x64- oder ARM64-Prozessor |
| **Shell** | Bash, Zsh, PowerShell oder CMD |
| **Internet** | nötig, Claude Code arbeitet über die API |
| **Standort** | ein [unterstütztes Land](https://www.anthropic.com/supported-countries) |

### Claude Code installieren (etwa 5 Minuten)

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

**Welche Version.** Die Kapitel beschreiben Claude Code ab Version 2.1.283. Ältere Versionen starten eine Sitzung zum Teil in einem anderen Rechte-Modus, als die Kapitel sagen ([S1.6](s1-06-rechte-modi.md)). Zeigt `claude --version` eine ältere Nummer, führ `claude update` aus.

**Andere Wege.** Wer lieber ohne Terminal arbeitet, nimmt die Desktop-App oder die Web-Version; was die Oberflächen unterscheidet, zeigt [S1.3](s1-03-oberflaechen.md). Die Kapitel arbeiten im Terminal. Die npm-Variante von Claude Code steht auf der Karte [Werkstatt erweitern](../reference/werkstatt-erweitern.md#nodejs).

### Anmelden (etwa 5 Minuten)

Gib im Terminal `claude` ein und drück Enter. Beim ersten Start öffnet Claude Code ein Browserfenster für die Anmeldung. Danach bist du in einer Sitzung; `/exit` beendet sie. Die Anmeldung startest du in einer Sitzung jederzeit neu, indem du dort `/login` eingibst.

Du brauchst eines davon:

- **Ein Claude-Abo:** Pro oder Max, im Unternehmen auch Team oder Enterprise. Der kostenlose claude.ai-Plan enthält Claude Code nicht.
- **Einen API-Key aus der Claude Console**, gesetzt als Umgebungsvariable `ANTHROPIC_API_KEY`. Ist sie gesetzt, fragt Claude Code beim Start einmal, ob es den Key verwenden soll. Unter Windows öffnest du nach `setx` das Terminal neu:

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

Prüf, ob die Anmeldung funktioniert. Der Befehl stellt eine einzige Frage, gibt die Antwort aus und endet:

<!-- cockpit:example -->
```bash
claude --print "Say hello"
# Should return a response without errors
```

### Git

Git brauchst du für die Git-Kapitel ab [S1.16](s1-16-git-in-einem-fluss.md) und später für das Workshop-Repo.

```bash
git --version   # Should show 2.30+
```

Installieren, falls nötig:

- **Windows:** `winget install Git.Git` oder Download von [git-scm.com](https://git-scm.com/)
- **macOS:** `xcode-select --install` oder `brew install git`
- **Linux:** `sudo apt install git`

Unter Windows bringt Git for Windows auch Git Bash mit. Claude Code führt Shell-Befehle dann über Bash oder über PowerShell aus; ohne Git for Windows bleibt PowerShell. Die Beispiele der Kapitel laufen in Git Bash, und wo PowerShell abweicht, steht die Variante daneben.

### Python 3

Python brauchst du ab der ersten Übung in [S1.1](s1-01-erster-kontakt.md): Claude schreibt dort ein kleines Python-Skript und führt es aus.

Prüfen (unter Windows heißen die Befehle `python`/`pip`, unter macOS und Linux `python3`/`pip3`):

```bash
python3 --version   # Windows: python --version    (should show 3.9+)
pip3 --version      # Windows: pip --version
```

Installieren, falls nötig:

- **Windows:** `winget install Python.Python.3.12` oder Download von [python.org](https://python.org/)
- **macOS:** `brew install python`
- **Linux:** `sudo apt install python3 python3-pip`

Die Untergrenzen für Git und Python sind Vorgaben dieser Bibliothek, nicht von Claude Code.

### Was du erst später brauchst

| Baustein | Gebraucht ab |
|---|---|
| GitHub CLI `gh` | [S1.16](s1-16-git-in-einem-fluss.md) |
| Workshop-Repo mit Playground | [X.2](x-02-lernen-mit-claude-code.md) für den Tutor, [S2.8](s2-08-hook-einrichten.md) für den Playground |
| `jq` | [S2.8](s2-08-hook-einrichten.md) |
| Node.js | [S2.14](s2-14-mcp-stecker.md) |

Installier davon jetzt nichts. Die Befehle stehen auf der Karte [Werkstatt erweitern](../reference/werkstatt-erweitern.md), und die Kapitel verweisen dorthin, sobald du etwas brauchst.

## Selbst machen

### Übung: die Werkstatt nachweisen (etwa 5 Minuten)

**Ziel:** Du weist mit vier Befehlen nach, dass alles läuft. Danach kannst du S1.1 direkt beginnen.

**Startzustand:** Claude Code ist installiert, du hast dich einmal angemeldet, das Terminal ist neu geöffnet.

1. `claude --version` zeigt eine Version ab 2.1.283.
2. `claude --print "Say hello"` gibt eine Antwort aus, ohne Fehlermeldung.
3. `git --version` und `python3 --version` (Windows: `python --version`) zeigen je eine Version.
4. Dein Terminal kann Farben. Dieser Befehl schreibt das Wort „Green“ in Grün:
   - macOS, Linux, Git Bash: `echo -e "\033[32mGreen\033[0m"`
   - Windows PowerShell 7+: `` Write-Host "`e[32mGreen`e[0m" `` (in PowerShell 5.1: `"$([char]27)[32mGreen$([char]27)[0m"`)

**Geschafft, wenn:**

- [ ] `claude --version` eine Version ab 2.1.283 zeigt
- [ ] `claude --print "Say hello"` antwortet (die Anmeldung funktioniert)
- [ ] `git --version` 2.30 oder neuer zeigt
- [ ] `python3 --version` (Windows: `python --version`) 3.9 oder neuer zeigt
- [ ] dein Terminal das Wort „Green“ in Grün anzeigt

## Typische Fallen

- **`claude` wird nicht gefunden** (`command not found` oder `'claude' is not recognized`). Der Installationsordner liegt nicht im `PATH`. Der Installer legt `claude` unter `~/.local/bin/claude` (macOS, Linux) bzw. `%USERPROFILE%\.local\bin\claude.exe` (Windows) ab. Öffne ein neues Terminal; hilft das nicht, trag den Ordner in den `PATH` ein ([Anleitung in der Doku](https://code.claude.com/docs/en/troubleshoot-install#command-not-found-claude-after-installation)).
- **`'irm' is not recognized`.** Du bist in CMD, nicht in PowerShell. In PowerShell beginnt der Prompt mit `PS`; führ den Installer dort aus.
- **Die Anmeldung schlägt fehl.** Prüf den API-Key bzw. den Status deines Abos, starte `claude` und gib in der Sitzung `/login` ein.
- **Abo und API-Key zugleich.** Ist `ANTHROPIC_API_KEY` gesetzt, nutzt Claude Code nach deiner Bestätigung den Key statt deines Abos. Gehört der Key zu einer deaktivierten oder abgelaufenen Organisation, scheitert die Anmeldung. `/status` zeigt, welche Methode aktiv ist. Entfernst du die Variable (`unset ANTHROPIC_API_KEY`), nimmt Claude Code wieder das Abo; hast du sie mit `setx` oder in `~/.bashrc` dauerhaft gesetzt, nimm sie auch dort heraus.
- **Python wird unter Windows nicht gefunden.** Nimm `python` statt `python3` oder installier Python aus dem Microsoft Store.
- **Keine oder nur langsame Antworten.** Prüf die Internetverbindung; `claude --verbose` zeigt mehr Details.

Für eine gründliche Diagnose gibst du in einer laufenden Sitzung `/doctor` ein: Es prüft Installation, Einstellungen, Erweiterungen und Kontextnutzung und schlägt Korrekturen vor, die es nach deiner Bestätigung anwendet. Startet `claude` gar nicht, nimmst du im Terminal:

```bash
claude doctor
```

## Check

Du kannst Claude Code installieren und anmelden und mit `claude --version` und `claude --print` nachweisen, dass deine Werkstatt steht.

1. Welche zwei Befehle weisen nach, dass Installation und Anmeldung funktionieren?
2. Was tust du, wenn die Shell nach der Installation `claude` nicht kennt?
3. Wo findest du die Installationsbefehle für `jq`, Node.js, die GitHub CLI und das Workshop-Repo, und wann brauchst du sie?

<details><summary>Auflösung</summary>

1. `claude --version` zeigt, dass Claude Code installiert ist und welche Version läuft. `claude --print "Say hello"` zeigt, dass die Anmeldung funktioniert: Es kommt eine Antwort ohne Fehlermeldung.
2. Ein neues Terminal öffnen. Hilft das nicht, liegt der Installationsordner (`~/.local/bin` bzw. `%USERPROFILE%\.local\bin`) nicht im `PATH`, und du trägst ihn dort ein.
3. Auf der Karte „Werkstatt erweitern“. Du installierst sie erst, wenn ein Kapitel sie verlangt: die GitHub CLI ab S1.16, das Workshop-Repo für den Tutor (X.2) und den Playground (S2.8), `jq` ab S2.8, Node.js ab S2.14.

</details>

<details><summary>Quizfrage</summary>

**Frage:** `claude --version` zeigt eine Version, aber `claude --print "Say hello"` endet mit einem Anmeldefehler. Was sagt dir das, und was tust du zuerst?

- **Richtig:** Die Installation steht, die Anmeldung nicht: Abo oder API-Key prüfen und in einer Sitzung `/login` neu starten.
- Falsch: Der Installationsordner fehlt im `PATH`: ein neues Terminal öffnen und den Ordner `~/.local/bin` dort eintragen.
- Falsch: Python fehlt noch: Ohne Python kann `claude --print` keine Antwort ausgeben, also zuerst Python installieren.
- Falsch: Die Installation ist beschädigt: Claude Code entfernen, den Installer neu ausführen und den Rechner neu starten.

</details>

## Weiterlesen

- [Installation und Systemvoraussetzungen (Advanced setup)](https://code.claude.com/docs/en/setup)
- [Anmeldung (Authentication)](https://code.claude.com/docs/en/authentication)
- [Fehlersuche bei Installation und Anmeldung](https://code.claude.com/docs/en/troubleshoot-install)
- [Quickstart: die erste Sitzung](https://code.claude.com/docs/en/quickstart)
- [Karte: Werkstatt erweitern](../reference/werkstatt-erweitern.md)
- [S1.1 · Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md)
- [S1.3 · Die Oberflächen: CLI, Desktop, IDE, Web, iOS](s1-03-oberflaechen.md)
