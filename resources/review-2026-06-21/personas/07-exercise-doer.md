# Persona: Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

**Scope:** Vollstaendig gelesen und durchsimuliert: resources/exercises/block-1-exercises.md, block-2-exercises.md, block-3-exercises.md. Playground real geprueft: 18/18 pytest-Tests bestehen (Python 3.12.10, pytest 9.0.3); access_control.py, test_access_control.py, CLAUDE.md, Makefile, requirements.txt gelesen. CLI-Flags gegen die echte installierte Claude CLI verifiziert (--bare, --effort, --max-budget-usd, --output-format, --json-schema vorhanden; --max-turns NICHT vorhanden). Git-Struktur des Playgrounds geprueft (kein eigenes Repo). Path-Traversal in read_log() real getestet. POSIX-vs-Windows-Shell-Annahmen gezaehlt.

## Gesamteindruck

Die Uebungen sind didaktisch durchdacht aufgebaut (Goal / Steps / Success Check / Hints durchgaengig), und der Playground ist gesund: alle 18 pytest-Tests laufen in 0,08s sauber durch, sodass die Baseline-Green-Anforderung in 3.3 und 1.4 erfuellbar ist. Als QA-Person stosse ich aber auf mehrere harte Blocker: Exercise 3.6 verlangt das Flag --max-turns, das in der aktuellen Claude CLI gar nicht mehr existiert — das Hook-Skript laeuft so nicht und die Success-Check-Checkbox ist unerfuellbar. Exercise 3.6 schreibt zudem den pre-commit-Hook ins falsche .git-Verzeichnis: aus workshop-playground heraus zeigt .git/hooks auf das ELTERN-Repo (dynamic_workshop selbst), nicht auf einen isolierten Sandbox-Klon. Die groesste Einstiegshuerde fuer die Windows-Workshop-Maschinen: nahezu alle Shell-Snippets (25+ Vorkommen von mkdir -p, chmod +x, cat > EOF, ~/.claude-Pfade) sind reines bash/POSIX und scheitern in der PowerShell-Default-Shell von Windows Terminal — es gibt nur einen einzigen Windows-Hinweis in allen drei Dateien. Zeitbudgets sind teils optimistisch (besonders 2.x mit Restart-Zyklen). Insgesamt: solide Struktur, aber mehrere Uebungen sind in der jetzigen Form fuer einen Neuling auf Windows nicht erfolgreich abschliessbar.

## Staerken (was bleiben soll)

- **Playground-Testsuite ist robust und erfuellt die Baseline-Anforderung** — python -m pytest -v liefert reproduzierbar 18 passed in 0.08s. Die autouse-Fixture isolated_db (test_access_control.py:18-31) leitet DB_FILE/LOG_DIR/LOG_FILE per monkeypatch auf tmp_path um — saubere Test-DB-Isolation. Damit ist die in 3.3 Step 4 und 1.4 geforderte 'baseline tests stay green'-Verifikation real machbar.
- **Einheitliche, QA-freundliche Uebungsstruktur** — Jede Uebung hat Goal / Steps (nummeriert, 'do them in order') / Success Check (abhakbare Checkboxen) / Hints. Block 1 erklaert das Schema sogar explizit ('How These Exercises Work', Z.9-17). Als QA kann ich jede Uebung gegen ihre eigene Success-Check-Liste abnehmen — das ist genau das richtige Format.
- **Didaktisch starke Vague-vs-Specific-Gegenueberstellung** — Exercise 1.3 (Z.209-321) laesst denselben IPv4-Validator zweimal bauen (vage vs. 10-Punkte-Spezifikation) und macht den Kontrast erfahrbar statt ihn nur zu behaupten. Reflection Questions und 'no regex'-Constraint zeigen gezielt, dass man Implementierungsentscheidungen erzwingen kann.
- **Realistische Priorisierung und Zeit-Transparenz in Block 3** — Die Priority-Tabelle (block-3 Z.7-19) mit Must-do/Should-do/Nice-to-have und 'Realistic total: 110-145 minutes' gibt der Gruppe ehrliche Erwartungen. Das hilft beim Schritt-fuer-Schritt-Abarbeiten unter Zeitdruck enorm.
- **Defensive Hints fuer typische Stolperstellen** — Wiederkehrende, praezise Recovery-Hinweise: 'Do not manually edit the code. Say: ...' (1.3 Z.318), Plugin-Manifest MUSS unter .claude-plugin/ liegen (2.3 Z.376-378, 450-451), PostToolUse-vs-PreToolUse-Klarstellung beim Token Firewall (2.6 Z.806-808). Das f(ae)ngt echte Fehlversuche ab.

## Befunde

### [critical | currency | S] Exercise 3.6: --max-turns existiert in der aktuellen Claude CLI nicht — Hook-Skript laeuft nicht, Success-Check unerfuellbar

- **Datei:** resources/exercises/block-3-exercises.md
- **Evidenz:** Das Hook-Skript verwendet `--max-turns 2` (Z.350) und die Success-Check verlangt zwingend: 'Every Module 3.6 flag (`--bare`, `--max-budget-usd`, `--max-turns`, `--output-format`) appears in your hook.' (Z.408). Verifikation gegen die installierte CLI: `claude --help | grep -c max-turns` ergibt 0; das Flag fehlt. Vorhanden sind nur --bare, --effort, --max-budget-usd, --output-format, --json-schema.
- **Empfehlung:** --max-turns aus Skript und Success-Check entfernen. Loop-Begrenzung uebernimmt --max-budget-usd 0.10 ohnehin. Falls eine harte Iterationsgrenze gewuenscht ist, im Modul-/Cheatsheet-Text dokumentieren, dass die CLI das nicht mehr per Flag bietet. Gilt auch fuer Exercise 1.5 (dort nicht im Alias, aber im Modultext referenziert) und das Stretch-Goal mit --json-schema (das existiert, ist also ok).

### [high | demo-reliability | S] Exercise 3.6: pre-commit-Hook landet im Eltern-Repo, nicht in einem isolierten Sandbox

- **Datei:** resources/exercises/block-3-exercises.md
- **Evidenz:** Die Uebung sagt `cd workshop-playground` + `git init` (Z.334-336) und schreibt dann nach `.git/hooks/pre-commit` (Z.341). Real geprueft: der Playground ist KEIN eigenes Repo (`ls workshop-playground/.git` -> 'No such file or directory'; alle Dateien sind im Eltern-Repo getrackt: `git ls-files workshop-playground/`). `git rev-parse --git-path hooks/pre-commit` aus dem Playground liefert `../.git/hooks/pre-commit` — also den Hook des dynamic_workshop-Repos selbst. Der Teilnehmer installiert einen claude-aufrufenden Hook in das Schulungs-Repo und blockiert dessen eigene Commits.
- **Empfehlung:** Teilnehmer in ein wirklich frisches, separates Verzeichnis schicken (z.B. `mkdir -p ~/cc-workshop/exercise-3.6 && cd ... && git init`) statt in den bereits getrackten Playground. ODER explizit warnen, dass `git init` im Playground ein No-op ist und der Hook ins Eltern-Repo schreibt. Konsistent mit Block-1-Uebungen, die alle ~/cc-workshop/... nutzen.

### [high | windows-compat | M] Fast alle Shell-Snippets sind POSIX-only und scheitern auf der Windows-PowerShell-Default-Shell

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** 25+ Vorkommen von `mkdir -p`, `chmod +x`, `cat > ... << 'EOF'`, `>> ~/.claude/...` ueber alle drei Exercise-Dateien (z.B. 2.1 Z.36-41 `mkdir -p ~/.claude/skills/...`, 2.2 Z.207 `chmod +x`, 2.3 Z.423 `cat > ... << 'EOF'`). prerequisites.md:12+16 erlaubt explizit Windows + 'Windows Terminal' (Default-Shell = PowerShell). In PowerShell schlagen `mkdir -p`, `chmod +x`, Heredocs und `~/`-Expansion fehl. In allen drei Exercise-Dateien gibt es nur EINEN Windows-Hinweis (block-3 Z.374 'On Windows, use Git Bash or WSL').
- **Empfehlung:** Einen klaren Vorspann ergaenzen: 'Auf Windows alle Shell-Befehle in Git Bash ausfuehren, nicht in PowerShell/cmd' — prominent in jeder Exercise-Datei und in prerequisites.md. Alternativ kritische Snippets (Skill-/Hook-Anlage) zusaetzlich als PowerShell-Variante anbieten. Das ist die groesste Einstiegshuerde fuer einen Neuling auf der Workshop-Maschine.

### [high | windows-compat | S] Block 1 nutzt durchgehend bash-Setup (mkdir -p, &&) ohne Windows-Hinweis — erste Huerde gleich in Uebung 1.1

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** Schon der allererste Schritt der allerersten Uebung: `mkdir -p ~/cc-workshop/exercises/exercise-1.1 && cd ... && claude` (Z.35). Dieselbe Form in 1.2 (Z.120-122), 1.4 (Z.336-341 mit `echo ... > README.md`). `mkdir -p` und die `&&`-Verkettung sind in PowerShell nicht 1:1 lauffaehig; `~/` wird in cmd gar nicht expandiert. Genau in der Einstiegsuebung darf ein Neuling nicht an der Shell scheitern.
- **Empfehlung:** Ganz oben in Block-1-Exercises (nach Z.7) einen Kasten: 'Windows-Teilnehmer: diese Befehle in Git Bash ausfuehren. PowerShell-Alternative: `mkdir ~/cc-workshop/...; cd ~/cc-workshop/...`'. Mindestens fuer 1.1 beide Varianten zeigen, danach Verweis darauf.

### [medium | accuracy-overclaim | M] Exercise 2.3: Plugins manuell unter ~/.claude/plugins/cache/ anlegen widerspricht dem CLI-only-Plugin-Modell

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** Step 4 laesst Teilnehmer per Hand Ordner + Manifest in den von der CLI verwalteten cache schreiben: `mkdir -p ~/.claude/plugins/cache/my-mini-plugin-marketplace/.claude-plugin` (Z.418) und `cat > .../plugin.json` (Z.423). Hint 'Team distribution: ... drop the directory into ~/.claude/plugins/cache/' (Z.511). Der cache-Ordner ist Claude-Code-managed; manuelles Hineinschreiben ist fragil und kann beim naechsten Plugin-Sync verschwinden. Sauberer Weg ist `claude plugin marketplace add` / `claude plugin install`.
- **Empfehlung:** Scaffolding in ein neutrales Verzeichnis legen (z.B. ~/cc-workshop/my-mini-plugin) und mit `claude --plugin-dir ./my-mini-plugin` laden (so wie es Exercise 3.5 Variant C bereits korrekt macht, Z.301). cache/ nur lesend erkunden, nicht beschreiben.

### [medium | structure | S] Exercise 2.3: Success-Check nennt 'agentic-os plugin', Step 1 aber 'workshop-provided plugin' / <plugin-name>

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** Step 1 (Z.359-360) spricht von 'a workshop-provided plugin' und nutzt durchgehend den Platzhalter `<plugin-name>` (Z.368, 373, 390, 404). Die Success-Check Z.496 verlangt konkret: 'You can navigate the agentic-os plugin structure from the command line'. Welches Plugin der Teilnehmer real erkundet, bleibt offen — und 'agentic-os' taucht vorher nirgends als Anweisung auf.
- **Empfehlung:** Einen konkreten, garantiert vorhandenen Plugin-Namen festlegen (das Workshop-Plugin selbst unter dynamic_workshop/ ist laut Step-1-Note nutzbar) und Success-Check + Steps darauf vereinheitlichen. Platzhalter und konkreten Namen nicht mischen.

### [medium | exercise-quality | S] Block 2 Zeitbudgets unrealistisch durch viele Restart-Zyklen

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** Header: '25-30 minutes' pro Uebung (Z.2). Aber 2.1 verlangt mind. einen Skill-Edit + 'works the same way in a new Claude Code session (restart and try)' (Z.114); 2.2 'Restart Claude Code (hooks are read at startup)' (Z.235) plus Bonus-Hook; 2.4 fordert npx-Install + .mcp.json + 'Restart Claude Code' (Z.567) + 6 Schritte + Bonus. Jeder Claude-Neustart kostet einen Neulaeufer real 1-3 Min Orientierung, dazu npx-Erstdownload bei 2.4. 5 Hauptuebungen a realistisch 30-40 Min sprengen die ~3h-Session inkl. Teaching.
- **Empfehlung:** Zeitschaetzungen ehrlich auf 30-40 Min anheben ODER pro Uebung 'Kern (Pflicht)' vs 'Bonus (optional)' klarer trennen (wie Block 3 es mit Must/Should/Nice macht). npx-@playwright/mcp-Erstinstall in prerequisites vorziehen, damit 2.4 in der Session nicht am Download haengt.

### [medium | demo-reliability | S] Versteckte Abhaengigkeit: Exercise 3.3 setzt das devil-advocate-swarms-Plugin voraus, ohne Fallback in der Uebung

- **Datei:** resources/exercises/block-3-exercises.md
- **Evidenz:** Step 2 ruft hart `/devil-advocate-swarms:swarm scan ...` (Z.127) und die gesamte Uebung (Step 3-4, 'What to Report') haengt am Swarm-Output. Ein Fallback steht nur in den Demos (block-3-demos.md:211 'If devil-advocate-swarms plugin not installed: Show recording'), nicht in der Exercise selbst. Ein Selbstlerner ohne installiertes Plugin (es ist ein Custom-Workshop-Plugin laut prerequisites.md:225/249) bleibt haengen.
- **Empfehlung:** In 3.3 einen expliziten Fallback ergaenzen: ohne Plugin stattdessen `/security-review` (built-in) oder einen normalen Audit-Prompt gegen access_control.py laufen lassen — die drei geplanten Vulns sind so oder so auffindbar. Plugin-Voraussetzung am Uebungsanfang nennen.

### [medium | didactics-onboarding | S] Kein Micro-Erfolgserlebnis vor Uebung 1.1 — Spruch direkt zur Tool-Bau-Aufgabe

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** 1.1 startet sofort mit einem komplexen Multi-File-Auftrag: Parser + Sample-Datei + 4 Anforderungen + --door-Flag + diff-Erklaerung (Z.42-83), Zeitbudget 12-15 Min. Es gibt davor keine 2-Minuten-Mini-Uebung (z.B. 'frag Claude: was steht in diesem Verzeichnis?' oder 'lass dir den /help-Output erklaeren'), um die describe-implement-run-Schleife einmal trivial zu erleben, bevor es ernst wird.
- **Empfehlung:** Eine optionale Micro-Uebung 1.0 (~3 Min) voranstellen: Claude in leerem Ordner starten, eine triviale Frage stellen ('Erstelle eine Datei hello.txt mit dem Inhalt Hallo'), Ergebnis pruefen. Senkt die kognitive Last des Einstiegs deutlich und gibt sofort ein Erfolgserlebnis.

### [medium | exercise-quality | M] Exercise 2.2/2.6: Mehrfache 'settings.json komplett ueberschreiben'-Snippets koennen vorhandene Hooks zerstoeren

- **Datei:** resources/exercises/block-2-exercises.md
- **Evidenz:** 2.2 zeigt vollstaendige settings.json-Bloecke zum Einfuegen (Z.213-229 und erneut komplett Z.273-300), 2.6 nochmal einen kompletten PostToolUse-Block (Z.813-829). Der Warnhinweis 'add the hooks section carefully — don't break the JSON structure' (Z.231) ist da, aber ein Neuling, der die Bloecke nacheinander 1:1 kopiert (2.2 PreToolUse, dann 2.6 PostToolUse, dann 3.8 Write|Edit), ueberschreibt jeweils die vorigen hooks, weil jeder Block die ganze hooks-Struktur neu definiert. Auf realen Maschinen kann das eine bestehende ~/.claude/settings.json (mit Permissions etc.) beschaedigen.
- **Empfehlung:** Statt kompletter settings.json-Bloecke ein Merge-orientiertes Vorgehen zeigen: 'fuege diesen Eintrag in das bestehende hooks.PreToolUse-Array ein' + Validierung mit `python3 -m json.tool`. Oder Teilnehmer auf eine projektlokale .claude/settings.json statt der globalen lenken, um die echte Konfiguration nicht zu gefaehrden.

### [low | didactics-onboarding | S] Exercise 1.5 setzt Modell-/Effort-Wissen voraus, das in Block 1 noch nicht sauber eingefuehrt ist

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** 1.5 verlangt pro Workflow Model + Effort + Flags zu waehlen (Tabelle Z.499-504) und nennt Aliases mit `--effort xhigh`, `--model opus/sonnet/haiku` (Z.523-525). --effort xhigh ist gegen die CLI verifiziert korrekt (low/medium/high/xhigh/max). Fuer einen kompletten Neuling ohne Vorerfahrung (Zielgruppe!) ist die bewusste Modell/Effort-Wahl am Ende der ALLERERSTEN Session aber kognitiv anspruchsvoll; die Begruendungs-Spalte 'not just felt right' (Z.536) verlangt Wissen, das erst durch Erfahrung entsteht.
- **Empfehlung:** 1.5 als klar optional markieren (ist bereits 'Should-do', gut) und die Hint-Defaults (Z.552 Sonnet/medium etc.) noch staerker als sicheren Startpunkt hervorheben, damit Neulinge nicht in Analyse-Paralyse geraten. Evtl. nach Block 2/3 verschieben.

### [low | exercise-quality | S] Exercise 3.3 'No vulnerability planting required' aber CLAUDE.md sagt 'Do NOT fix them' — Konfliktpotential mit Step 4

- **Datei:** resources/exercises/block-3-exercises.md
- **Evidenz:** 3.3 Step 4: 'Choose one ... and let Claude implement the fix in access_control.py' + danach `pytest -v` gruen (Z.142-148). Gleichzeitig instruiert workshop-playground/CLAUDE.md:68: 'Do NOT fix them in this playground — they are the teaching target.' und Z.81 (OSDP) ebenso. Ein QA-Teilnehmer, der den Fix wie verlangt anwendet und committet, mutiert die geplante Teaching-Vorlage; beim naechsten Durchlauf fehlt die Vuln.
- **Empfehlung:** In 3.3 explizit sagen: Fix nur lokal/uncommitted anwenden und danach verwerfen (`git checkout access_control.py`) ODER in einer Kopie arbeiten. So bleibt der Playground fuer den naechsten Workshop intakt. Die CLAUDE.md-Regel und die Uebung in Einklang bringen.

### [low | demo-reliability | S] Erwartung in 3.3, der read_log-Path-Traversal sei sofort demonstrierbar, ist umgebungsabhaengig

- **Datei:** workshop-playground/access_control.py
- **Evidenz:** read_log oeffnet `open(f"logs/{log_name}")` (access_control.py:127). Real getestet: `read_log('../../Windows/win.ini')` wirft FileNotFoundError 'logs/../../Windows/win.ini', solange das Verzeichnis logs/ noch nicht existiert (es wird erst von log_event() via os.makedirs angelegt). Auf einer frischen Checkout-Maschine ohne vorher ausgefuehrtes add/check schlaegt eine Live-Traversal-Demo also fehl, obwohl die Schwachstelle real ist.
- **Empfehlung:** Falls in 3.3/Demos eine manuelle Traversal-Vorfuehrung geplant ist: vorher einen Logeintrag erzeugen (`python access_control.py check alice`), damit logs/ existiert. Als Hinweis in trainer-notes/demo aufnehmen. Fuer die Swarm-basierte statische Analyse ist es irrelevant (sie liest den Code).

### [nice-to-have | new-exercise-idea | S] Neue Micro-Uebung: 'CLAUDE.md-Boundary in Aktion' als sanfter Zwischenschritt vor 1.2 Step 6

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** 1.2 springt von 'CLAUDE.md schreiben' (Step 2-3) direkt zu 'exit/restart + Persistenz testen' (Step 4-5) und dann 'never-change-Boundary' (Step 6, Z.170-177). Zwischen Anlegen und Testen fehlt ein kleiner verifizierender Zwischenschritt im selben Lauf ('Zeig mir den aktuellen Inhalt von CLAUDE.md' steht nur als Hint Z.203).
- **Empfehlung:** Vor dem Restart einen 30-Sekunden-Check einbauen: 'Frag Claude jetzt sofort: Welche Konventionen gelten? — bevor du neu startest.' So sieht der Teilnehmer den Effekt zweimal (selbe Session + nach Restart) und versteht den Unterschied Kontext-im-Lauf vs. persistiert. Kleines Zwischen-Erfolgserlebnis.
