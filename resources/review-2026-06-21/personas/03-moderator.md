# Persona: Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

**Scope:** Live-Durchfuehrbarkeit aus Moderatoren-Sicht: Gelesen wurden session-plan.md, trainer-notes.md, demos/block-1/2/3-demos.md (inkl. aller Recovery-Notes), dry-run-session-2-3-2026-05-21.md, final-gap-sweep-2026-05-21.md, deck-audit-2026-05-21.md. Bewertet: Timing-Realismus ueber 3x3h, Zeitdruck-Stellen, Live-Fragilitaet einzelner Demos (Auth/Plugin/Budget/Internet), Ausreichen der Recovery-Notes, fehlende Moderator-Hilfsmittel (Skripte/Fallbacks/Checklisten) sowie Vorbereitungsluecken fuer die noch ausstehenden Sessions 2 & 3. Cross-checks der Timing-Arithmetik gegen die im Demo-Skript angegebenen Dauern wurden vorgenommen.

## Gesamteindruck

Als Live-Moderatorin finde ich ein bemerkenswert reifes Trainer-Paket vor: trainer-notes.md hat ein "If Everything Is On Fire"-Skript, eine Pre-Flight-Checkliste und Modul-Opener; jeder Demo-Block hat Recovery-Notes; der Dry-Run vom 21.05. liefert mir bereits eine ehrliche GREEN/YELLOW-Einschaetzung mit Live-Spine und Fallback-Empfehlung pro Demo. Das ist die beste Absicherung gegen meinen Albtraum (Demo bricht vor Publikum), die ich je in einem Workshop-Repo gesehen habe. ABER: Das Timing ist an mehreren Stellen unrealistisch eng — besonders Session 3, wo eine Codex-Swarm-Demo (Decompose + parallele Agents + Review) in einen 10-Minuten-Slot gepresst wird und sieben Module plus Capstone in 3h sollen. Session 1 hat Slot-Konflikte (Demo-Skript-Dauern uebersteigen die Plan-Slots). Die fragilsten Demos (Codex Swarm, Self-Improve-Loop, Telegram, Devil-Advocate, Playwright, NotebookLM) haengen alle an Plugins/Auth/Budget/Internet, die zur Live-Zeit kippen koennen — die Recovery-Notes adressieren das gut, aber es fehlt eine konsolidierte "Was-ist-heute-live-vs-Discussion"-Entscheidung VOR der Session und eine Budget-/Auth-Pruefroutine. Fuer die noch ausstehenden Sessions 2 & 3 bleibt eine echte Plugin-Preflight auf MEINER Maschine die groesste offene Luecke. Einstiegshuerde fuer mich als Moderatorin: niedrig bei Block 1, mittel-hoch bei Block 3 wegen Tooling-Abhaengigkeiten.

## Staerken (was bleiben soll)

- **Recovery-Notes-Disziplin** — Jede Demo hat konkrete, durchdachte Recovery-Notes mit Schnell-Pivots (z.B. block-3-demos.md Demo 3.2: 'If Codex auth fails: Same as not installed — fall back to discussion'). Das nimmt mir live enorm Druck.
- **'If Everything Is On Fire'-Skript** — trainer-notes.md Zeilen 69-77 geben mir ein 5-Schritte-Improvisationsskript fuer den Totalausfall ('Stop the demo flow. Ich mache eine 5-Min-Pause.' ... 'Be honest: Das Tool ist neu, manche Demos sind fragil'). Genau das, was eine Moderatorin im Panik-Moment braucht.
- **Ehrlicher Dry-Run als Entscheidungsgrundlage** — dry-run-session-2-3 liefert pro Demo eine Live-vs-Fallback-Entscheidung und ein 'Live-Spine'-Konzept (Demo 2.1, 2.2/2.2b, 2.4). Verdict GREEN/YELLOW mit Begruendung ist Gold fuer die Vorbereitung.
- **Pre-Flight-Checklist + Common-Failure-Tabelle** — trainer-notes.md Zeilen 25-67: konkrete Bash-Checks am Workshop-Tag plus eine Failure-Mode-Tabelle ('gh auth abgelaufen -> Skip PR-Step', 'Internet bricht -> Switch zu --bare'). Das ist sofort ausfuehrbar.
- **Windows-Realitaetscheck bereits eingebaut** — block-3-demos.md Demo 3.3 hat eine explizite 'Windows note for moderators' zum fehlenden cp-Befehl (Zeile 125) und block-2-demos.md Demo 2.2b nennt jq-auf-Windows-Fallback (Zeile 247). Zeigt, dass an die reale Maschine gedacht wurde.
- **Budget-Transparenz** — session-plan.md 'Estimated Cost to Replicate' (Zeilen 109-134) gibt mir Block-Kosten ($1-3 / $5-15 / $15-50) und konkrete Spar-Hebel. Ich weiss vorher, womit ich rechnen muss.

## Befunde

### [high | structure | M] Session-3-Timing ist unrealistisch: 7 Module + 8 Demos + 40-Min-Capstone in 3h

- **Datei:** resources/session-plan.md
- **Evidenz:** Session-3-Tabelle (Z.62-74): '0:40 – 0:50 | Modul 3.2 + Demo 3.2 | Multi-Model Pipelines / Codex Swarm' — nur 10 Min fuer Modul-Input PLUS eine Codex-Swarm-Demo. Block-3-demos.md Demo 3.2 verlangt aber: Decompose + N parallele Codex-Agents + Claude-Review (4 Schritte, Z.68-96). Auch '0:40-0:50 Modul 3.2+Demo 3.2' und '0:50-1:10 Modul 3.3+Demo 3.3' lassen pro Doppel-Slot kaum Luft fuer Modul-Teaching.
- **Empfehlung:** Session 3 in der Praxis NICHT als '7 Module live' fahren. Dem Dry-Run folgen (3.2/3.4/Telegram als optional). Konkret: Demo 3.2 Codex-Swarm aus dem Live-Pfad nehmen und durch eine vorbereitete Aufzeichnung/Screenshots ersetzen — 10 Min reichen real nicht fuer Decompose+Parallel+Review. Slot-Spalte im session-plan um eine 'Live/Recording/Discussion'-Default-Spalte ergaenzen, damit ich nicht live entscheiden muss.

### [high | demo-reliability | M] Keine konsolidierte 'Heute live vs. Fallback'-Entscheidungs-Checkliste fuer den Sessiontag

- **Datei:** resources/trainer-notes.md
- **Evidenz:** Die Live-vs-Fallback-Logik ist auf drei Dokumente verteilt: trainer-notes.md (Failure-Tabelle Z.59-67), dry-run...md (Verdicts + Timeline), und jede Demo-Datei (Recovery-Notes). Es gibt KEINE einzelne Seite, die ich am Workshop-Morgen abhake: 'Plugin X installiert? -> Demo live. Nicht? -> Recording bereit?'
- **Empfehlung:** Eine 1-seitige 'Go/No-Go-Demo-Matrix' anlegen (z.B. in trainer-notes.md): Zeile pro Demo, Spalten 'Preflight-Check (Befehl)', 'wenn PASS -> live', 'wenn FAIL -> Fallback-Artefakt + Pfad'. Die Recovery-Notes existieren schon; sie muessen nur in eine abhakbare Matrix verdichtet werden. Das ist die wichtigste fehlende Moderatoren-Hilfe.

### [high | demo-reliability | S] Fragilste Demos haengen kumuliert an Auth/Plugin/Budget/Internet — Cluster-Risiko in Session 3

- **Datei:** resources/demos/block-3-demos.md
- **Evidenz:** Demo 3.2 braucht 'Codex CLI installed and authenticated' (Z.61-63) UND das multi-model-orchestrator-Plugin; Demo 3.4 braucht agentic-os-Plugin + Budget-Cap; Demo 3.3 braucht devil-advocate-swarms-Plugin; Demo 3.3c braucht WebSearch/Internet (Z.353); Demo 3.5 Step 4 braucht Telegram-Bridge. Faellt eines vor Publikum aus, kann eine Kettenreaktion entstehen ('3+ Demos in Folge', genau der trainer-notes.md-Notfall Z.71).
- **Empfehlung:** Fuer Session 3 EINEN garantiert-live-Anker festlegen, der NUR auf lokal-installiertem claude beruht: Demo 3.6 Headless (laut Dry-Run 'Should-show live, because claude is installed locally'). Den explizit als 'das laeuft sicher'-Demo markieren und als Eroeffnung von Block 3 ziehen, damit das Publikum frueh einen funktionierenden Live-Moment sieht — psychologisch wichtig, falls spaeter Plugin-Demos kippen.

### [high | windows-compat | M] Demo 2.2b Inline-Hook ist live fragil (Bash/jq-Quoting auf Windows) — Fallback existiert nur als Verweis, nicht als fertige Datei

- **Datei:** resources/demos/block-2-demos.md
- **Evidenz:** Demo 2.2b setzt eine lange Inline-JSON+Bash-Hook-Zeile mit verschachteltem Quoting (Z.200): 'command: "bash -c '\''INPUT=$(cat); FILE=$(echo ...| jq -r .file_path...'\'' ...'. Recovery-Note Z.246 sagt 'Have a pre-prepared secure-diff-gate.sh file ready' — aber diese Datei liegt NICHT im Repo (workshop-playground/ enthaelt sie nicht). Der Dry-Run bestaetigt: 'inline JSON/bash quoting is too risky on Windows' (dry-run...md Z.49).
- **Empfehlung:** Die fertige secure-diff-gate.sh (und eine Python-Variante fuer Windows ohne jq) tatsaechlich ins Repo legen (z.B. resources/demos/assets/hooks/), damit ich sie nur kopieren muss. Das Skript sollte auf Windows-Git-Bash getestet sein. Ohne fertige Datei ist 'pre-prepared' nur eine Absichtserklaerung.

### [medium | structure | S] Session-3-Timeline hat eine ungeklaerte 10-Minuten-Luecke / Slot-Mathematik geht nicht auf

- **Datei:** resources/session-plan.md
- **Evidenz:** Session-3-Tabelle: '0:50 – 1:10 Modul 3.3+Demo 3.3' (20 Min), dann '1:10 – 1:20 Pause', danach '1:20 – 1:35' usw. Im Dry-Run (dry-run...md Z.69-79) erscheint dieselbe Reihe aber OHNE Pause-Zeile und mit Sprung von '0:50-1:10' direkt auf '1:20-1:35' — d.h. die beiden Quelldokumente sind nicht deckungsgleich, und die Pause fehlt in der Dry-Run-Tabelle.
- **Empfehlung:** Eine einzige Master-Timeline als Source of Truth definieren (session-plan.md), Dry-Run darauf referenzieren statt eine zweite, leicht abweichende Tabelle zu fuehren. Pause-Zeile in beide aufnehmen. So vermeide ich, dass ich live zwei widerspruechliche Ablaeufe im Kopf habe.

### [medium | demo-reliability | S] Demo-Skript-Dauern uebersteigen die Plan-Slots in Session 1

- **Datei:** resources/session-plan.md
- **Evidenz:** session-plan.md Z.30: 'Demo 1.4 | 2:10 – 2:20' = 10-Min-Slot. block-1-demos.md Demo 1.4 ist aber '~10 minutes' OHNE den Worktree-Bonus (Step 6) — mit Bonus deutlich mehr. Analog Demo 1.1: Plan-Slot 0:30-0:40 (10 Min), Skript sagt '~8 minutes' (Z.26), aber Modul 1.1 davor hat nur 0:15-0:30 = 15 Min fuer 'drei Interfaces, Permissions, Models'.
- **Empfehlung:** Pro Demo eine realistische 'Demo-Dauer inkl. Talking-Points' neben den Plan-Slot schreiben und Bonus-Schritte (Worktree Step 6) klar als 'nur bei Zeitueberschuss' markieren — ist im Skript schon mit 'Bonus' getan, aber im session-plan.md nicht sichtbar. Puffer von 2-3 Min pro Demo einplanen; Live-Demos laufen IMMER langsamer als das Skript.

### [medium | demo-reliability | S] Budget-Cap-Empfehlung uneinheitlich: Demo 3.6 nutzt 0.05$, Plan empfiehlt 50$-Konto, Self-Improve hat keinen Default-Cap im Skript

- **Datei:** resources/demos/block-3-demos.md
- **Evidenz:** Demo 3.6 Step 3 setzt '--max-budget-usd 0.05 --max-turns 2' (Z.558-561). Demo 3.4 Self-Improve (Z.380-393) ruft '/agentic-os:run-loop' mit '1' Iteration, nennt aber im Step KEINEN expliziten Budget-Cap — der Cap taucht erst in den Recovery-Notes auf ('If --max-budget-usd is hit early', Z.418). session-plan.md warnt zugleich, der Self-Improve-Loop sei der Haupt-Kostentreiber ($15-50, Z.118/122).
- **Empfehlung:** In Demo 3.4 Step 2 einen expliziten Budget-Cap als Pflicht-Vorgabe vor den /run-loop-Aufruf setzen (analog Demo 3.6), nicht nur in den Recovery-Notes. Als Moderatorin will ich den Cap GESETZT haben, bevor ich Enter druecke — nicht erst reagieren, wenn er greift. Ein '/cost'-Blick vor und nach dem Loop ins Skript aufnehmen.

### [medium | demo-reliability | S] Demo 3.7 'broken-greeter'-Skill muss vom Moderator selbst gebaut werden, liegt aber nicht im Repo

- **Datei:** resources/demos/block-3-demos.md
- **Evidenz:** Demo 3.7 setzt voraus: 'The moderator has prepared an intentionally broken skill at ~/.claude/skills/broken-greeter/SKILL.md with three problems planted in this order' (Z.596-603). Diese SKILL.md liegt nirgends im Repo als kopierbares Artefakt; ich muss sie aus der Prosa-Beschreibung selbst rekonstruieren (generische Description, disable-model-invocation:true, paths:[never-match]).
- **Empfehlung:** Die fertige broken-greeter/SKILL.md als Asset ins Repo legen (resources/demos/assets/broken-greeter/SKILL.md), inkl. der drei geplanten Fehler exakt wie im Skript beschrieben. Dann ist Demo 3.7 (laut Dry-Run ein Live-Kandidat) wirklich reproduzierbar statt Bastelei am Workshop-Morgen.

### [medium | accuracy-overclaim | M] Demo 3.7 setzt /debug-Trace-Ausgaben voraus, die so evtl. gar nicht existieren — Overclaim-Risiko vor Publikum

- **Datei:** resources/demos/block-3-demos.md
- **Evidenz:** Demo 3.7 zitiert woertliche Trace-Ausgaben als erwartet, z.B. 'Skill broken-greeter matched paths-filter: NO (filter: never-match/**, current files: ...)' (Z.642) und 'description too generic for prompt — no candidate match' (Z.667). Ob '/debug skill-not-triggering' real exakt solche Zeilen ausgibt, ist nicht verifiziert; Recovery-Note Z.695 raeumt ein, '/debug' sei in aelteren Builds evtl. gar nicht vorhanden.
- **Empfehlung:** Vor Session 3 auf meiner Maschine real pruefen, was '/debug' bzw. 'claude --verbose' tatsaechlich ausgibt, und die zitierten Trace-Zeilen an die echte Ausgabe anpassen ODER als 'sinngemaess, Wortlaut variiert' kennzeichnen. Sonst stehe ich vor Entwicklern, die merken, dass die versprochene Zeile nicht erscheint — Glaubwuerdigkeitsverlust.

### [medium | windows-compat | S] Pre-Flight-Checklist mischt POSIX-Pfade/Befehle, die auf einer Windows-Moderatorenmaschine scheitern

- **Datei:** resources/trainer-notes.md
- **Evidenz:** Pre-Flight (Z.29-55) nutzt 'python3 -m pytest -v', 'make', 'notebooklm list' und den Pfad 'cd ~/cc-workshop/dynamic-workshop'. Auf Windows ist 'python3' oft nur 'python', 'make' meist nicht installiert (im Skript selbst '(if installed)' relativiert), und der Dry-Run lief mit 'python -m pytest -v: 18 passed' (dry-run...md Z.29) — also 'python', nicht 'python3'.
- **Empfehlung:** Die Pre-Flight-Checklist mit einer Windows-Spalte/Variante versehen ('python' statt 'python3', make-Schritt klar als optional, Pfade ohne ~-Annahme). Da der Workshop laut Repo-Kontext auf Windows-Maschinen laeuft, sollte die abhakbare Liste primaer Windows-tauglich sein, nicht POSIX-first.

### [medium | demo-reliability | S] Demo 3.3c (CVE-Fix) plant eine verwundbare Dependency ein — Cleanup-Schritt ist als 'biggest risk' selbst markiert

- **Datei:** resources/demos/block-3-demos.md
- **Evidenz:** Demo 3.3c Step 0 fuegt 'requests==2.5.0 (CVE-2018-18074)' in requirements.txt ein (Z.306); Recovery-Note Z.354: 'If you forget the cleanup step: Document this as the demos biggest risk — always revert the planted vulnerable line.' Step 3 Cleanup verlangt manuelles Editieren (Z.341-346).
- **Empfehlung:** Cleanup nicht der Erinnerung ueberlassen: ein fertiges Revert-Snippet/Script (z.B. git checkout -- requirements.txt) als Ein-Befehl-Cleanup ins Skript setzen, plus den Hinweis 'NIEMALS pip install auf dieser Zeile'. Als Moderatorin mit 17 Modulen im Kopf vergesse ich genau solche manuellen Nach-Demo-Schritte — ein 'git checkout' ist sicherer als 'oeffne die Datei und loesche die Zeile'.

### [medium | structure | M] Session 3 hat 8 Demos + Capstone und keinen Live-Puffer fuer das wahrscheinliche 'Demo bricht'-Szenario

- **Datei:** resources/dry-run-session-2-3-2026-05-21.md
- **Evidenz:** Dry-Run-Verdikt Session 3: 'YELLOW/GREEN ... too many demos depend on plugins, auth, budget, or external services' und 'Session 3 still has more possible demos than time' (Z.58, Z.121). Die Timeline (Z.69-79) fuellt 0:10-2:20 lueckenlos mit Demos, dann 2:20-3:00 Capstone — kein expliziter Recovery-Puffer, obwohl trainer-notes ein '3+ Demos brechen'-Szenario antizipiert.
- **Empfehlung:** Einen 10-Min-Recovery-Puffer fest in die Session-3-Timeline einbauen (z.B. Demo 3.2 ODER 3.4 von vornherein als Streich-Kandidat deklarieren) statt 100% verplanen. Realistisch sollte Session 3 als '5 sichere Demos + Capstone' geplant werden, mit 3.2/3.4/Telegram als reine Bonusse — genau wie der Dry-Run empfiehlt, aber im verbindlichen Plan noch nicht abgebildet.

### [medium | didactics-onboarding | S] Kein Plan-B fuer ausgefallene Teilnehmer-Setups waehrend der Live-Exercises

- **Datei:** resources/session-plan.md
- **Evidenz:** trainer-notes.md Failure-Tabelle Z.67 nennt 'Teilnehmer-Maschine bricht beim Setup -> Vorab ~/cc-workshop-Bundle bereithalten, USB-Stick'. session-plan.md plant aber feste Exercise-Bloecke (z.B. Z.25 'Exercises 1.1+1.2 Hands-on', Z.48 'Exercises 2.1+2.2'). Wenn bei 1 von 3 Teilnehmern das Setup bricht, blockiert das den ganzen Hands-on-Block — bei nur 3 Teilnehmern faellt ein Drittel aus.
- **Empfehlung:** Fuer die Hands-on-Bloecke eine Pairing-Fallback-Regel ins Trainer-Skript: 'Bricht ein Setup, Teilnehmer paart sich mit Nachbarn (driver/navigator), waehrend ich parallel debugge.' Bei nur 3 Personen ist ein Ausfall sonst hoch sichtbar. Dazu den USB-Stick-/Bundle-Hinweis aus der Failure-Tabelle in die Materialliste (session-plan.md Z.99-105) hochziehen, damit ich ihn vorbereite.

### [low | structure | S] Demo 1.4 Recovery-Note referenziert 'gh pr create', das in den Demo-Schritten gar nicht vorkommt

- **Datei:** resources/demos/block-1-demos.md
- **Evidenz:** Demo 1.4 Steps 1-6 enden bei 'git log' und Worktree; ein PR-Schritt existiert nicht. Die Recovery-Notes nennen aber 'If gh pr create fails (auth): Skip the PR step, demonstrate via git push only' (Z.463). Pre-Demo-Checklist Z.17 fuehrt 'gh authenticated if Demo 1.4 includes PR creation' — der konditionale Halbsatz deutet auf eine entfernte PR-Variante.
- **Empfehlung:** Entweder einen optionalen PR-Schritt (Step 7, 'Bonus') wieder einbauen ODER die gh-pr-Recovery-Note und den gh-Checklist-Eintrag entfernen. Aktuell stiftet die Note Verwirrung: ich bereite gh-auth vor, finde dann aber keinen PR-Schritt im Skript.

### [low | structure | S] Slide-Index-Diskrepanz: trainer-notes mappt Session 3 auf Slides 19-29, Outro=30; Block-3-Slide-Anzahl deckt 7 Module nur knapp

- **Datei:** resources/trainer-notes.md
- **Evidenz:** trainer-notes.md Slide-Index (Z.257-283) ordnet Session 3 elf Slides (19-29) sieben Modulen + Run Sheet + Website + Dry-Run-Checklist zu, also ~1 Slide pro Modul. deck-audit...md Z.36-37 bestaetigt '19-29 Block 3 Advanced'. final-gap-sweep...md Z.67 warnt aber, die INSTALLIERTE Plugin-Kopie melde noch '13 modules' — Laufzeit-Metadaten und Repo divergieren.
- **Empfehlung:** Vor Session 3 das lokale dynamic-workshop-Plugin neu installieren/aktualisieren (final-gap-sweep Empfehlung Z.77), damit '/workshop'-Laufzeitausgaben zur 17-Modul-Realitaet passen. Falls ich '/workshop' live zeige und es '13 modules' sagt, widerspricht das meinen Slides. Kurz: Plugin-Reinstall in die Pre-Flight-Checklist aufnehmen.

### [low | structure | S] Pausen-Logik in Session 2 unsauber: Slot 1:25-1:35 Pause, aber Module 2.3 startet erst 1:35 — der 1:25-1:35-Block fehlt im Demo-Spine des Dry-Runs

- **Datei:** resources/session-plan.md
- **Evidenz:** session-plan.md Session-2-Tabelle Z.48-50: '1:00 – 1:25 Exercises 2.1+2.2', '1:25 – 1:35 Pause', '1:35 – 1:45 Modul 2.3'. Der Dry-Run-Timeline (dry-run...md Z.50-51) springt aber von '1:00-1:25 Exercises' direkt auf '1:35-1:55 Module/Demo 2.3' — die Pause 1:25-1:35 ist dort nicht als Zeile gefuehrt, und die Modul-2.3-Zeit weicht ab (Plan 1:35-1:45 vs Dry-Run 1:35-1:55).
- **Empfehlung:** Plan und Dry-Run-Timeline fuer Session 2 angleichen (gleiche Slot-Grenzen, Pause in beiden). Das ist Teil desselben Source-of-Truth-Problems wie bei Session 3 — eine konsolidierte Timeline pro Session loest beide Befunde.
