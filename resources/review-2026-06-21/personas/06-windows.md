# Persona: Kevin — Windows-11/PowerShell-Praktiker

**Scope:** Plattform-Annahmen in resources/modules/block-1-3, resources/demos/block-1-3, resources/exercises/block-1-3, prerequisites.md, cheatsheet.md, troubleshooting.md. Fokus: Was bricht 1:1 auf Windows/PowerShell? Wo fehlt eine Windows-Variante? Querverweis gegen tatsaechliche Inhalte (Read/Grep), keine Annahmen.

## Gesamteindruck

Als reiner Windows/PowerShell-Nutzer stosse ich sofort an die Decke, sobald es ueber das Tippen von Prompts hinausgeht. Die Installations- und Slash-Command-Teile sind okay (der Cheatsheet hat sogar eine PowerShell-Install-Zeile, gut), aber das gesamte Hook-Material — der didaktische Kern von Block 2 und 3 — ist zu 100% bash mit jq, chmod +x, python3, sed, heredocs und `bash script.sh`-Aufrufen. Im kompletten Teaching-Content (modules/demos/exercises) kommt kein einziges `powershell`, `pwsh`, `$env:` oder `setx` vor; die einzigen Windows-Hinweise stehen verstreut in troubleshooting.md (pwsh -File) und prerequisites.md und widersprechen sogar den Exercises (Exercise 2.1 registriert `bash ~/.claude/hooks/safety-check.sh`, obwohl troubleshooting.md sagt, auf Windows `pwsh -File` zu nutzen). Die Einstiegshuerde ist niedrig fuer Block 1, aber an Demo 2.2 / Exercise 2.1 wird ein Windows-Teilnehmer ohne Git-Bash-auf-PATH SOFORT blockiert — die zentrale Hook-Uebung laeuft schlicht nicht. python3/pip3 als kanonische Befehle (mit Windows-Fix nur in einer Troubleshooting-Tabelle versteckt) und `"command": "python3"` im MCP-Config-Beispiel sind weitere Sofort-Stolperfallen. Empfehlung: eine durchgaengige Windows-Spalte/-Variante fuer alle Hook- und Setup-Schritte, mindestens fuer die Pflicht-Demos.

## Staerken (was bleiben soll)

- **Cheatsheet-Installation hat Windows-Variante** — cheatsheet.md:13-14 zeigt explizit `# Install (Windows PowerShell)` mit `irm https://claude.ai/install.ps1 | iex` neben der curl|bash-Variante. Das ist genau das Muster, das im Rest des Workshops fehlt — sollte bleiben und als Vorlage fuer alle anderen Stellen dienen.
- **troubleshooting.md enthaelt korrekte Windows-Spezifika** — troubleshooting.md:48 `Auf Windows: PowerShell-Pfad richtig? Skript mit `pwsh -File` aufrufen.` und :97 der korrekte Windows-Pfad-Hash `C:\Users\...\Desktop\projekt` wird zu `C--Users-...-Desktop-projekt`. Sachlich richtig und hilfreich — muss nur mit den Exercises konsistent gemacht werden.
- **Cheatsheet-Hook-Beispiel ist cross-platform** — cheatsheet.md:491 nutzt `node security-check.js` statt eines bash-Scripts — node laeuft identisch auf Windows. Gutes Muster; sollte auch in Exercise 2.1 als Windows-freundliche Alternative angeboten werden.
- **Prerequisites nennt winget fuer alle Tools** — prerequisites.md:32/91/108/120 geben `winget install ...` fuer Node, Git, Python und gh an — moderne, korrekte Windows-Installationswege. Solide Basis.

## Befunde

### [critical | windows-compat | M] Pflicht-Hook-Demo (Demo 2.2) laeuft auf Windows ohne Git Bash nicht

- **Datei:** resources/demos/block-2-demos.md
- **Evidenz:** block-2-demos.md:125 `"command": "bash ~/.claude/hooks/security-check.sh"` und :200 `"command": "bash -c 'INPUT=$(cat); FILE=$(echo \"$INPUT\" | jq -r .file_path ...'"`. Voraussetzung (block-2-demos.md:110) `cat ~/.claude/settings.json | jq '.hooks'`.
- **Empfehlung:** Fuer die Live-Demo eine getestete PowerShell-Variante des Hooks bereitstellen (`"command": "pwsh -File C:/.../security-check.ps1"` mit einem PS-Script, das stdin via `$input | ConvertFrom-Json` parst statt jq). Alternativ klar als Voraussetzung dokumentieren, dass Git Bash UND jq auf PATH liegen muessen, und das in prerequisites.md als Pflicht-Check aufnehmen. Aktuell scheitert der Trainer/Selbstlerner auf einer reinen Windows-Box stillschweigend.

### [critical | windows-compat | L] Flagship-Hook-Exercise 2.1 komplett bash/python3/chmod, keine PowerShell-Variante

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** block-2-exercises.md:167 `#!/bin/bash`, :174 `python3 -c "import sys, json; ..."`, :206 `chmod +x ~/.claude/hooks/safety-check.sh`, :222 `"command": "bash ~/.claude/hooks/safety-check.sh"`. `chmod +x` existiert in PowerShell nicht; `bash`-Aufruf braucht Git Bash auf PATH; `python3` ist auf Windows i.d.R. `python`.
- **Empfehlung:** Komplette PowerShell-Parallelvariante anbieten: `safety-check.ps1` mit `$input | Out-String | ConvertFrom-Json`, Pattern-Match via `-match`, `exit 1`; Registrierung `"command": "pwsh -File $HOME/.claude/hooks/safety-check.ps1"`. `chmod +x`-Schritt fuer Windows als entfallend kennzeichnen. Dies ist DIE zentrale Hook-Uebung des Workshops — ohne Windows-Variante ist Block 2 fuer die Zielgruppe (Windows-Entwickler) nicht selbststaendig durchfuehrbar.

### [high | windows-compat | S] Widerspruch: Exercises registrieren `bash ...`, troubleshooting.md verlangt `pwsh -File` auf Windows

- **Datei:** global
- **Evidenz:** exercises/block-2-exercises.md:222 `"command": "bash ~/.claude/hooks/safety-check.sh"` vs. troubleshooting.md:48 `Auf Windows: PowerShell-Pfad richtig? Skript mit `pwsh -File` aufrufen.`
- **Empfehlung:** Einheitliche Linie ziehen: entweder durchgaengig `pwsh -File`-Variante in den Exercises ergaenzen oder in den Exercises explizit auf den Git-Bash-Pfad fuer Windows verweisen. Der Teilnehmer kann den Widerspruch sonst nicht selbst aufloesen und gibt an der ersten roten Fehlermeldung auf.

### [high | windows-compat | S] python3/pip3 als kanonische Befehle, Windows-Fix nur in Troubleshooting-Tabelle versteckt

- **Datei:** resources/prerequisites.md
- **Evidenz:** prerequisites.md:103 `python3 --version`, :104 `pip3 --version`, :147 `pip3 install -r requirements.txt`, :150 `python3 -m pytest -v`, :163 Checklist `[ ] python3 --version shows 3.9+`. Erst :189 in der Troubleshooting-Tabelle: `Python not found on Windows | Use python instead of python3`.
- **Empfehlung:** Im Haupttext (Step 5, Step 7, Checkliste) `python`/`pip` als Windows-Variante direkt neben `python3`/`pip3` nennen, statt den Fix in eine Fehlertabelle am Ende auszulagern. Beispiel: `python --version  # Windows: python, nicht python3`. Sonst scheitert jeder Windows-Teilnehmer schon beim Pre-Workshop-Setup an `python3: command not found`.

### [high | windows-compat | S] MCP-Config-Beispiel nutzt `"command": "python3"` — bricht auf Windows

- **Datei:** resources/modules/block-2-ecosystem.md
- **Evidenz:** block-2-ecosystem.md:1140 `"command": "python3",` im `.mcp.json`-Beispiel (`"args": ["my_mcp_server.py"]`).
- **Empfehlung:** Auf Windows gibt es i.d.R. kein `python3.exe` — der MCP-Server startet nicht. Beispiel auf `"command": "python"` umstellen oder einen Hinweis ergaenzen: `# Windows: "python" statt "python3"`. Da Teilnehmer dieses Snippet 1:1 in ihre eigene .mcp.json kopieren, ist das eine direkte Stolperfalle.

### [high | windows-compat | M] Hook-Setup in prerequisites.md ist reines bash-Heredoc mit jq/chmod, keine Windows-Form

- **Datei:** resources/prerequisites.md
- **Evidenz:** prerequisites.md:279-293 `cat > ~/.claude/hooks/security-check.sh << 'EOF'` ... `COMMAND=$(echo "$INPUT" | jq -r '.command // ""')` ... `chmod +x ~/.claude/hooks/security-check.sh`. Auch :263 `mkdir -p ~/.claude/skills` und :278 `mkdir -p ~/.claude/hooks`.
- **Empfehlung:** Heredoc + jq + chmod sind in PowerShell allesamt nicht verfuegbar (`mkdir -p` ebenso wenig — PS `mkdir` kennt kein `-p`, braucht `New-Item -ItemType Directory -Force`). Eine PowerShell-Block-Variante zum Anlegen der Datei (`Set-Content` mit Here-String `@'...'@`) und Verzeichnisse (`New-Item -Force`) ergaenzen. Diese Datei ist die Vorbereitung VOR der Session — wenn sie auf Windows scheitert, fehlt die Demo-Voraussetzung.

### [medium | windows-compat | M] `mkdir -p ...` in fast allen Exercise-Startschritten — scheitert in PowerShell

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** block-1-exercises.md:35 `mkdir -p ~/cc-workshop/exercises/exercise-1.1 && cd ...`, :120 `mkdir -p ~/cc-workshop/exercises/exercise-1.2 && cd ...`, :336 `mkdir -p ~/cc-workshop/exercises/exercise-1.4-git && cd ...`. Ebenso block-2-exercises.md:37/161/418-420 und prerequisites.md:140/375.
- **Empfehlung:** `mkdir -p` ist POSIX; PowerShells `mkdir` akzeptiert `-p` nicht (Parameter-Fehler) und `&&` funktioniert erst ab PowerShell 7. Entweder cross-platform formulieren (`New-Item -ItemType Directory -Force -Path ...; Set-Location ...`) oder eine Windows-Zeile danebenstellen. Niedrige Schwere, weil Claude Code das Verzeichnis meist selbst anlegt, aber der erste copy-paste-Schritt scheitert sichtbar.

### [medium | windows-compat | S] PostToolUse-Logging-Hook (Exercise 2.1 Bonus) nutzt bash `date`/`>>`/chmod

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** block-2-exercises.md:257-268 `#!/bin/bash` ... `TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')` ... `echo "[$TIMESTAMP] BASH: $COMMAND" >> ~/.claude/audit.log` ... `chmod +x ~/.claude/hooks/audit-log.sh`.
- **Empfehlung:** `date '+...'` (POSIX-Formatstring), `chmod` und die Shebang funktionieren auf Windows nicht. Bei der PowerShell-Variante: `Get-Date -Format 'yyyy-MM-dd HH:mm:ss'`, `Add-Content`, Shebang/chmod entfaellt. Als Bonus weniger kritisch, aber Teil derselben Pflicht-Exercise.

### [medium | windows-compat | M] Git-pre-commit-Hook-Exercise nur knapp mit Windows-Hinweis, Bonus-Zeile wieder bash-only

- **Datei:** resources/exercises/block-3-exercises.md
- **Evidenz:** block-3-exercises.md:344 `#!/bin/bash`, :371 `chmod +x .git/hooks/pre-commit`, :374 `(On Windows, use Git Bash or WSL — git's hook subsystem looks for executable POSIX scripts.)`, Bonus :389 `echo "$(date) | $(basename "$0") | budget=0.10 | result=$(echo "$RESULT" | head -1)" >> ~/.claude/precommit-trace.log`.
- **Empfehlung:** Der Windows-Hinweis :374 ist gut, aber die Bonus-Zeile :389 mit `$(date)`, `basename`, `head -1` funktioniert auch in Git Bash nur, wenn die Tools da sind — auf reiner PowerShell gar nicht. Entweder Exercise klar als 'nur in Git Bash/WSL' kennzeichnen ODER eine native PowerShell-pre-commit-Variante anbieten (git ruft auf Windows mit Git Bash, daher ggf. akzeptabel — dann aber prominent als Pflicht-Voraussetzung dokumentieren).

### [medium | windows-compat | M] Advanced-Hook-Beispiele in Block 3 / Block 2 durchgehend bash (sed, jq -n, case, $CLAUDE_EFFORT)

- **Datei:** resources/modules/block-2-ecosystem.md
- **Evidenz:** block-2-ecosystem.md:594-601 `sed -E 's/(sk-...)/[REDACTED]/g'` + `jq -n --arg out ...`, :628-633 `jq -n '{"terminalSequence":...}'`, :641-652 `case "$CLAUDE_EFFORT" in xhigh|max) ...`. Auch block-3-advanced.md:1494 `#!/bin/bash` und :1382/1387 `> /tmp/diff.patch`.
- **Empfehlung:** Diese sind Konzept-/Demonstrationsbeispiele, daher etwas toleranter — aber ein Windows-Leser kann KEINS davon ausprobieren. Mindestens einen Satz ergaenzen: 'Beispiele in bash; auf Windows analog mit PowerShell (`$env:CLAUDE_EFFORT`, `-replace`, `ConvertTo-Json`).' `/tmp/` existiert auf Windows nicht — fuer kopierbare CI-Snippets `$env:TEMP` bzw. plattformneutrale Pfade nennen.

### [medium | windows-compat | S] `export VAR=...` als Konfigurationsmuster — kein PowerShell-Aequivalent gezeigt

- **Datei:** resources/demos/block-1-demos.md
- **Evidenz:** block-1-demos.md:591 `export TERM=xterm-256color`; modules/block-3-advanced.md:741 `export DISABLE_TELEMETRY=1`, :742 `export DISABLE_ERROR_REPORTING=1`; prerequisites.md:70 nennt nur 'set ANTHROPIC_API_KEY environment variable' ohne Syntax.
- **Empfehlung:** `export` ist kein PowerShell-Cmdlet. Fuer Env-Vars die PS-Form danebenstellen: Session `$env:DISABLE_TELEMETRY=1`, persistent `setx DISABLE_TELEMETRY 1`. Bei prerequisites.md:70 konkret `$env:ANTHROPIC_API_KEY="..."` (Session) bzw. `setx ANTHROPIC_API_KEY "..."` (persistent) zeigen — ein Neuling weiss sonst nicht, wie er die Variable auf Windows setzt.

### [low | windows-compat | S] Checklisten-Zeile `echo -e` zur Terminal-Pruefung scheitert in PowerShell

- **Datei:** resources/prerequisites.md
- **Evidenz:** prerequisites.md:165 `[ ] Terminal supports Unicode and ANSI colors (try `echo -e "\033[32mGreen\033[0m"`)`.
- **Empfehlung:** PowerShells `echo` ist `Write-Output` und interpretiert `-e` nicht (gibt `-e ...` woertlich aus). Windows-Variante: `"`e[32mGreen`e[0m"` mit PowerShell-7-Escape oder `[char]27`. Klein, aber es ist ein Pre-Workshop-Pflicht-Check, der auf Windows verwirrend fehlschlaegt.

### [low | windows-compat | S] Plugin-Exploration (Exercise 2.3) nutzt `cat ... | head -60` und Heredoc

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** block-2-exercises.md:405 `cat ~/.claude/plugins/cache/<plugin-name>/agents/*.md | head -60`, :423-434 `cat > ~/.claude/plugins/cache/.../plugin.json << 'EOF' ... EOF`.
- **Empfehlung:** `cat`/`ls` existieren als PS-Aliase, aber `head -60` und der `<< 'EOF'`-Heredoc nicht. PS-Aequivalente nennen: `Get-Content ... | Select-Object -First 60` und Here-String `@'...'@ | Set-Content`. Niedrig, weil die Exploration auch ohne exakten Befehl gelingt, aber der copy-paste-Pfad bricht.

### [low | missing-content | S] Cheatsheet zeigt nie die bash-Script-Hook-Form, die die Exercises voraussetzen — keine Windows-Bruecke

- **Datei:** resources/cheatsheet.md
- **Evidenz:** cheatsheet.md:491 zeigt nur `"command": "node security-check.js"` (cross-platform), aber nirgends den `"command": "bash script.sh"`-/`pwsh -File`-Fall, den Exercise 2.1/Demo 2.2 nutzen. Im ganzen Cheatsheet kein `pwsh`/`$env:`-Eintrag (Grep: nur die ps1-Install-Zeile :14).
- **Empfehlung:** Eine kurze 'Hooks auf Windows'-Notiz in den Cheatsheet aufnehmen: bash-Scripts brauchen Git Bash auf PATH; native Alternative `"command": "pwsh -File path.ps1"`; jq-frei via `ConvertFrom-Json`. Der Cheatsheet ist die Referenzkarte waehrend der Uebung — genau hier sucht ein blockierter Windows-Teilnehmer.
