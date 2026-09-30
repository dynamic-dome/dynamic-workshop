# Persona: Anna — Embedded-Entwicklerin (15 J. C/Embedded), NULL Agent-Erfahrung. Wichtigste Einstiegshuerden-Persona.

**Scope:** Erste ~90 Min als kompletter Coding-Agent-Neuling: prerequisites.md, README.md, WORKSHOP_EINFUEHRUNG.md, workshop-guide.md, modules/block-1-foundations.md (Module 1.1-1.5), exercises/block-1-exercises.md (1.1 + 1.2). Fokus: Einstiegshuerde, kognitive Last, Klarheit von Anfang an, Granularitaet.

## Gesamteindruck

Als Embedded-Entwicklerin ohne Agent-Erfahrung komme ich beim Setup gut mit (prerequisites.md ist sauber), aber der inhaltliche Einstieg ueberfordert mich sofort. Modul 1.1 startet mit Lernzielen, die "6 Permission Modes", "5 Surfaces" und "Modell/Effort-Wahl" verlangen — bevor ich ueberhaupt verstanden habe, was ein Coding Agent ist. Die Ueberschrift "The Three Interfaces" listet dann fuenf Interfaces auf, was mich sofort verunsichert ("kann ich noch zaehlen?"). Pro 10 Minuten werden gefuehlt 8-12 neue Konzepte und ein Dutzend Slash-Commands/CLI-Flags eingefuehrt, von denen viele Vorgriffe auf Block 2/3 sind (worktree.baseRef, --fork-session, /autofix-pr, managed CLAUDE.md). Es fehlt ein bewusst minimaler "erste 5 Minuten"-Pfad: das allererste, was ich tun koennte (eine Datei bauen lassen), kommt erst in Exercise 1.1 — im Modul selbst wird vorher die gesamte Theorie-Landschaft ausgebreitet. Modul 1.5 (Cost Engineering) als 5. Modul am ersten Tag ist fuer mich als Neuling klar zu viel: ich habe noch nichts produktiv gebaut, soll aber schon Pricing-Tabellen, Effort-Multiplikatoren und Prompt-Caching-TTLs verarbeiten. Die Einstiegshuerde ist insgesamt HOCH — nicht wegen falscher Inhalte, sondern wegen Dichte, Reihenfolge und fehlender Treppe vom Einfachen zum Komplexen. Die Demos-und-Exercises-Idee ist gut, aber die Module davor schiessen ueber das hinaus, was ein Neuling im ersten Durchgang braucht.

## Staerken (was bleiben soll)

- **Setup-Anleitung (prerequisites.md)** — Klar strukturiert in nummerierte Steps, jeweils Check-Befehl + Install-Befehl pro OS, plus Pre-Workshop-Checklist und Troubleshooting-Tabelle. Als Neuling konnte ich Schritt 1-5 ohne Stocken durchgehen. Die explizite Trennung 'Block 1/2 brauchen die Custom-Plugins NICHT' (Zeile 216, 244) nimmt frueh Druck raus.
- **Security-Analogien als Bruecke** — Die durchgaengigen Analogien (claude.ai = Berater am Telefon, CLI = Berater mit Badge, Context-Window = Kontrollraum mit 20 Monitoren bei 200 Kameras, CLAUDE.md = Site-Access-Policy) sind fuer mich als Hardware/Security-naher Mensch der beste Anker im ganzen Material. Sie machen abstrakte Agent-Konzepte greifbar.
- **Exercise 1.1 als echter sanfter Einstieg** — Exercise 1.1 ('Your First Claude Code Project', ~12-15 Min) ist genau das, was ich am Anfang gebraucht haette: describe -> implement -> run -> extend -> explain, an einem Domaenen-Beispiel (event_log_parser.py). Konkrete Prompts zum Adaptieren, klare Success-Checks mit Checkboxen, hilfreiche Hints. Das ist der beste neulingstaugliche Baustein in Block 1.
- **Bad-vs-Good-Prompt-Gegenueberstellung (Modul 1.3)** — Die Side-by-Side-Tabelle (Zeile 681-686) und die Vague-vs-Specific-Beispiele machen den wichtigsten Lerneffekt sofort sichtbar, ohne Vorwissen. Das haette gut viel frueher kommen koennen.
- **Klare Pflicht/Optional-Trennung im workshop-guide** — workshop-guide.md Zeile 87-98 ('Pflicht / Sehr empfehlenswert / Fortgeschritten') und der Minimalpfad geben mir als Selbstlerner Orientierung, was ich wirklich brauche und was ich erstmal nur ueberfliegen darf.

## Befunde

### [high | didactics-onboarding | S] Modul 1.1 startet mit den schwersten Lernzielen statt den leichtesten

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 12-14: 'Identify when each of the 6 permission modes (default / acceptEdits / plan / auto / dontAsk / bypassPermissions) applies ... Choose the right model (Opus 4.7 / Sonnet 4.6 / Haiku 4.5) and effort level ...' — das sind die ersten beiden Lernziele des allerersten Moduls.
- **Empfehlung:** Lernziele umsortieren: erstes Lernziel sollte 'Verstehen, was ein Coding Agent ist und wie er sich von einem Chat unterscheidet' sein. Permission Modes (6 Stueck) und Modell/Effort-Wahl als spaetere/optionale Lernziele markieren oder in einen 'Vertiefung'-Block schieben. Ein Neuling braucht im ersten Modul ein mentales Grundmodell, keine 6-Modi-Taxonomie.

### [high | structure | S] Ueberschrift 'The Three Interfaces' listet fuenf Interfaces — Zaehl-Widerspruch verunsichert Neulinge

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 23 Ueberschrift 'The Three Interfaces', danach nummeriert '1. claude.ai', '2. Claude Code CLI', '3. Desktop App', '4. IDE Extensions', '5. Web App & iOS App' (Zeile 24-58).
- **Empfehlung:** Ueberschrift auf 'The Surfaces' oder 'Die Claude-Code-Oberflaechen' korrigieren. Als Neuling habe ich an dieser Stelle aufgehoert dem Text zu vertrauen ('wenn schon die Ueberschrift nicht stimmt...'). Idealerweise im ersten Durchgang nur CLI vs. claude.ai-Chat zeigen und die restlichen 3 Surfaces in eine Klappbox/spaetere Sektion auslagern.

### [high | didactics-onboarding | M] Zu viele neue Konzepte und Slash-Commands/Flags pro Lerneinheit (kognitive Ueberlastung)

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Allein Modul 1.2 fuehrt ein: Context-Window, Auto-Kompression, CLAUDE.md (2 Levels), CLAUDE.local.md, Managed CLAUDE.md, .claude/rules/ mit YAML-paths, Auto-Memory + MEMORY.md/topic-files, @path-Imports, @AGENTS.md-Interop, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, /context /compact /export /resume /memory /init /rewind, --bare, 'claude project purge'. Das sind ~20 neue Begriffe/Befehle in einem Modul.
- **Empfehlung:** Modul 1.2 in zwei Einheiten splitten: (a) Kern-Neulingsteil = nur Context-Window-Analogie + ./CLAUDE.md + /context + /compact; (b) 'Vertiefung Memory & Multi-Repo' = rules/, Managed-CLAUDE.md, --add-dir, @AGENTS.md, Auto-Memory-Internals. Teil (b) explizit als 'beim ersten Durchgang ueberspringbar' kennzeichnen. Das senkt die kognitive Last drastisch ohne Inhalt zu loeschen.

### [high | missing-content | M] Kein expliziter 'Sanfter-Einstieg' / 'Erste 5 Minuten'-Pfad vor der Theorie

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Modul 1.1 breitet ab Zeile 16 erst die komplette Konzept-Landschaft aus (5 Surfaces, Tool-Referenz-Tabelle mit 18 Tools Zeile 131-148, 6 Permission Modes, Modell-Tabelle). Das erste tatsaechliche 'mach es selbst' (eine Datei bauen lassen) steht erst in exercises/block-1-exercises.md Exercise 1.1.
- **Empfehlung:** Ein kurzes 'Hello, Claude Code'-Kapitel GANZ an den Anfang von Modul 1.1 setzen: 3 Befehle (mkdir, claude, ein einfacher Prompt), Ergebnis sofort sichtbar. Erst nach diesem Erfolgserlebnis die Konzepte erklaeren. Das klassische didaktische 'Demo first, Theorie danach' wird im CLAUDE.md sogar gefordert ('Demos > Slides'), fehlt aber genau am Einstiegspunkt.

### [medium | didactics-onboarding | M] Massive Vorgriffe auf Block 2/3 mitten in den Foundations

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Modul 1.4 erklaert /autofix-pr (Cloud-Session watcht CI), --fork-session, worktree.baseRef 'fresh' fuer 'multi-agent worktree setups in Block 3' (Zeile 868), --from-pr. Modul 1.1 nennt Computer Use, MCP, Sub-Agents. Als Neuling ohne erste erfolgreiche Session sagen mir diese Begriffe nichts und erzeugen das Gefuehl 'das ist alles riesig, ich komme nie hinterher'.
- **Empfehlung:** Vorgriffe konsequent in 'Ausblick'-Kaesten buendeln (1-2 Zeilen + Verweis 'Details in Block 3.x') statt sie voll auszuerklaeren. Faustregel fuer Block 1: nur erklaeren, was man in der ersten Session selbst anfassen kann. Der Rest = ein Satz Teaser.

### [medium | didactics-onboarding | S] Built-in-Tools-Referenztabelle (18 Tools) zu frueh und zu vollstaendig

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 131-148: Tabelle mit 18 Tools inkl. NotebookEdit, LSP, Skill, Agent, Monitor, AskUserQuestion, TaskCreate/TaskList/TaskUpdate — in Modul 1.1. Direkt darunter Note (Zeile 152): 'Skill and Agent are introduced here as tool names; they are explored in depth in Block 2.1 ... Block 3.1.'
- **Empfehlung:** Im ersten Modul nur die 5-6 Tools zeigen, die ein Neuling sofort sieht (Read, Edit, Write, Bash, Grep). Die Vollreferenz mit allen 18 Tools ins cheatsheet.md verschieben und hier nur verlinken. Eine 18-Zeilen-Tabelle mit Tools, die erst in Block 2/3 relevant werden, ist reiner Ballast in der ersten Stunde.

### [medium | didactics-onboarding | M] Modul 1.5 (Cost Engineering) als 5. Modul am ersten Tag ist fuer Neulinge zu viel

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Modul 1.5 (Zeile 927-1130) verlangt nach ~80 Min Theorie: Pricing-Tabelle ($/M Input/Output pro Modell), Effort-Multiplikatoren (0.5x-6x), Plan/Implement/Review-Pipeline, --max-budget-usd/--max-turns, Prompt-Caching mit 5-Min-TTL und 90%-Rabatt, --exclude-dynamic-system-prompt-sections. Sehr dichtes Finanz-/Optimierungs-Thema OHNE dass der Neuling bisher ueberhaupt Geld ausgegeben oder ein Gefuehl fuer normale Spends hat.
- **Empfehlung:** Modul 1.5 auf einen 5-Minuten-Kern eindampfen ('/cost gibt es, schau gelegentlich drauf; Default-Modell ist ok') und den Rest (Pricing-Details, Pipeline, Caching, Budget-Caps) als eigenstaendiges Vertiefungs-Modul nach Session 1 oder als optionalen Anhang fuehren. Die zugehoerige Exercise 1.5 ist bereits korrekt als 'Should-do/optional' markiert (exercises Zeile 473) — das Modul sollte konsistent dazu ebenfalls als optional/spaeter gekennzeichnet sein.

### [medium | didactics-onboarding | S] Modul-Header 'Audience: Experienced programmers' ignoriert die Neulings-Persona der Zielgruppe

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 3: 'Audience: Experienced programmers. Security analogies used throughout — especially relevant for the CySec engineer in the group.' Die Zielgruppe sind laut Auftrag erfahrene Entwickler MIT NULL Agent-Erfahrung. 'Experienced programmers' wird im Material durchgehend als Lizenz genutzt, Agent-Grundlagen knapp zu halten.
- **Empfehlung:** Header schaerfen: 'Audience: Experienced programmers who are NEW to coding agents.' Das ist der entscheidende Unterschied — ich kann C, aber ich habe noch nie einem Tool eine Aufgabe delegiert. Das Material sollte Programmier-Vorwissen voraussetzen, aber Agent-Konzepte konsequent bei Null erklaeren.

### [medium | windows-compat | S] Windows-Stolperstein python3 vs python: Setup verlangt python3, Troubleshooting widerspricht erst spaeter

- **Datei:** resources/prerequisites.md
- **Evidenz:** Step 5 (Zeile 102-104) und Step 7 (Zeile 150) verwenden durchgaengig 'python3 --version' / 'python3 -m pytest'. Erst in der Troubleshooting-Tabelle am Ende (Zeile 189) steht: 'Python not found on Windows | Use python instead of python3'. Auf einer Standard-Windows-Installation ist 'python3' oft nicht vorhanden (nur 'python').
- **Empfehlung:** Bei jedem python3-Befehl im Windows-Kontext direkt einen Hinweis '(Windows: python statt python3)' setzen oder einen kurzen Hinweiskasten direkt bei Step 5. Als Windows-Embedded-Entwicklerin wuerde ich bei 'python3: command not found' in der Pre-Workshop-Checkliste haengenbleiben und das Troubleshooting am Dateiende moeglicherweise nicht finden.

### [low | didactics-onboarding | S] Auth-Verifikation per 'claude --print' vor erklaerter Erstnutzung — Henne-Ei fuer Neulinge

- **Datei:** resources/prerequisites.md
- **Evidenz:** Step 3 (Zeile 74-76): 'claude --print "Say hello"' zur Auth-Pruefung, und Checklist Zeile 161 'claude --print "Hello" returns a response'. Vorher wurde nur 'claude' + '/login' gezeigt. Als Neuling weiss ich nicht, was --print/--print-Modus bedeutet vs. interaktiv.
- **Empfehlung:** Einen Halbsatz ergaenzen: 'claude --print fuehrt einen einmaligen, nicht-interaktiven Prompt aus und beendet sich danach — gut zum Testen.' Kleinigkeit, aber genau solche unerklaerten Flags summieren sich beim Neuling zu Verunsicherung.

### [low | structure | S] Reihenfolge-Konflikt zwischen den Einstiegsdateien (prerequisites -> ? )

- **Datei:** global
- **Evidenz:** README.md Quick Start (Zeile 30-32): 'prerequisites.md -> WORKSHOP_EINFUEHRUNG.md -> Block durcharbeiten'. workshop-guide.md Lernpfad (Zeile 54-58): 'prerequisites.md -> session-plan.md -> block-1'. WORKSHOP_EINFUEHRUNG.md (Zeile 19-20): 'prerequisites.md -> workshop-guide.md'. Drei Dateien empfehlen drei leicht verschiedene Reihenfolgen.
- **Empfehlung:** Eine einzige kanonische Einstiegs-Reihenfolge festlegen und in allen drei Dokumenten identisch wiederholen (z.B. prerequisites -> WORKSHOP_EINFUEHRUNG -> workshop-guide -> session-plan -> Block 1). Als Neuling, der genau diese Orientierungsdateien zuerst liest, kosten kleine Abweichungen Vertrauen und Zeit.

### [low | didactics-onboarding | S] Modul 1.2 Auto-Memory-Privacy-Block ist korrekt, aber an dieser Stelle Overload

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 338-349: ausfuehrlicher Privacy-Block zu Auto-Memory (was an Anthropic gesendet wird, Opt-out --bare, 'claude project purge', Verweis auf Modul 3.7 Drift-Detection) mitten im zweiten Foundations-Modul.
- **Empfehlung:** Privacy-Hinweis auf 2-3 Saetze kuerzen ('Auto-Memory schreibt Notizen auf Platte und sendet sie bei Sessionstart mit — keine Secrets hineinschreiben, Opt-out via --bare') und die Details (purge, Drift-Detection) in Modul 3.7 belassen. Der Neuling muss in 1.2 nur die Kernwarnung mitnehmen, nicht das volle Privacy-Regime.

### [low | exercise-quality | S] Exercise 1.2 setzt 'never-change'-Pushback-Verhalten als verlaesslich voraus

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** Exercise 1.2 Step 6 (Zeile 170-177): 'Modify the legacy panel interface module' -> 'Does Claude push back? It should flag that the CLAUDE.md says not to touch it.' LLM-Verhalten ist nicht deterministisch; der Pushback kann ausbleiben, obwohl die Regel korrekt ist.
- **Empfehlung:** Erwartung entschaerfen: 'Claude sollte in der Regel darauf hinweisen ... falls nicht, ist das ein gutes Lehrbeispiel, dass CLAUDE.md-Regeln Leitplanken sind, keine harten Sperren — Hooks (Block 2.2) sind das harte Gate.' Das verhindert, dass ein Neuling bei ausbleibendem Pushback denkt, er habe etwas falsch gemacht. Der Hint Zeile 202 deutet das an, aber Step 6 selbst formuliert es zu absolut ('It should').

### [low | didactics-onboarding | M] Zeitbudget Block-1-Exercises vs. Modul-Lesezeit unrealistisch fuer Neulinge

- **Datei:** resources/exercises/block-1-exercises.md
- **Evidenz:** Exercises Zeile 4: '~85-90 minutes total for all Block 1 exercises'. Modul block-1-foundations.md ist ~1145 Zeilen dichtes Material mit Header 'Duration: ~90 minutes' (Zeile 4). Zusammen mit Demos passt das nicht realistisch in eine ~3h-Session, wenn ein Neuling die Module wirklich versteht statt nur ueberfliegt.
- **Empfehlung:** Realistisches Zeitbudget fuer die Neulings-Persona ausweisen oder einen klaren 'Kern vs. Vertiefung'-Schnitt machen, damit in 3h ein Erfolgserlebnis statt Hetze entsteht. Konkret: pro Modul kennzeichnen, was Pflicht-Lesestoff (Kern) und was Nachlese ist.
