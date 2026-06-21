# Persona: Tom — Selbstlerner, arbeitet das Repo allein durch (kein Moderator)

**Scope:** Selbstlern-Pfad: README.md, WORKSHOP_EINFUEHRUNG.md, resources/workshop-guide.md, quick-reference.md, cheatsheet.md, faq.md, glossary.md, troubleshooting.md, prerequisites.md, skills/workshop/SKILL.md, commands/workshop.md sowie Quervergleich mit session-plan.md und den Block-1/3-Modul-/Exercise-Dateien. Fokus: Selbsterklaerbarkeit ohne Trainer, Konsistenz der Referenzdateien untereinander und mit den Modulen, /workshop learn als Trainer-Ersatz, Sackgassen, Einstiegshuerde, kognitive Last.

## Gesamteindruck

Als Solo-Lerner komme ich grundsaetzlich durch: der workshop-guide.md gibt einen klaren, gut priorisierten Lernpfad (Pflicht/empfehlenswert/fortgeschritten), prerequisites.md ist ehrlich darueber, was Selbstlerner ohne Moderator nicht haben (Custom-Plugins) und bietet Observation-/Web-UI-Fallbacks, und Glossar/FAQ/Troubleshooting sind dicht und scanbar. Die groesste Huerde ist NICHT der Einstieg, sondern Inkonsistenz zwischen den Navigationsdateien: Block 3 traegt in README, SKILL.md und session-plan/glossary drei verschiedene Reihenfolgen UND verschiedene Titel fuer 3.2 und 3.5 — das verunsichert beim alleinigen Durcharbeiten massiv, weil niemand da ist, der es geradezieht. Zweite Huerde: die Versions-/Modell-Aktualitaet (durchgaengig "Opus 4.7" und Stand-Daten 2026-04/05) wirkt heute (2026-06-21) veraltet, und die Selbstlern-Quick-Start in README verweist auf Dateien, die der Selbstlerner laut WORKSHOP_EINFUEHRUNG zusaetzlich braucht (quick-reference, faq, glossary, troubleshooting), aber nicht alle auflistet. Der /workshop learn Modus ist als Trainer-Ersatz didaktisch gut konzipiert (Concept-Example-YourTurn-Hints-Check-NextSteps mit echter Verifikation), hat aber eine reale Luecke: er kann das fehlende Custom-Plugin-Setup nicht ersetzen und fuehrt Solo-Lerner in Block 3 potenziell in Sackgassen. Die Exercises selbst sind vorbildlich self-contained (Goal/Steps/Success-Check/Hints) — das ist die staerkste Saeule fuer Solo-Lernen.

## Staerken (was bleiben soll)

- **Lernpfad-Klarheit (workshop-guide.md)** — Der Guide uebersetzt das Material explizit in eine Reihenfolge und trennt Pflicht/empfehlenswert/fortgeschritten (Z.87-98) plus einen 'guten Minimalpfad' (Z.66-71: Block 1 komplett, aus Block 2 Skills/Hooks/MCP, aus Block 3 Agents/Security). Das ist genau das, was ein Solo-Lerner ohne Trainer braucht, um nicht querbeet zu lesen.
- **Self-contained Exercises mit klarem Fertig-Signal** — Jede Block-1-Uebung hat Goal, nummerierte Steps, einen Checkbox-'Success Check' und progressive Hints (z.B. Exercise 1.1 Z.88-101). Das 'fertig'-Signal, das ein Selbstlerner sich wuenscht, ist hier bereits vorhanden und konsequent durchgezogen.
- **Ehrliche Plugin-/Setup-Disclosure fuer Solo-Lerner** — prerequisites.md Z.211-245 sagt klar, dass agentic-os/devil-advocate-swarms/multi-model-orchestrator workshop-custom sind, NICHT in offiziellen Marketplaces liegen, und Block 1+2 ohne sie funktionieren — inkl. Option B 'Observation mode only' fuer Selbstlerner. Das verhindert die Frustration, vergeblich nach nicht-existenten Plugins zu suchen.
- **Konsistente Cross-Verweise zwischen Referenzdateien** — faq.md, glossary.md und troubleshooting.md verweisen gegenseitig sauber aufeinander (z.B. faq.md Z.4-5, troubleshooting.md Z.5) und auf die jeweilige Modulnummer (Glossar nennt pro Begriff das Modul). Ein Solo-Lerner findet von einem Begriff zuverlaessig zur Vertiefung.
- **/workshop learn als durchdachter Trainer-Ersatz** — Das Learn-Mode-Format in SKILL.md (Z.162-201) bildet einen Tutor nach: CONCEPT->LIVE EXAMPLE->YOUR TURN->HINTS (nicht sofort)->CHECK (echte Verifikation der Lerner-Ausgabe)->NEXT STEPS. Die explizite Anweisung, nicht weiterzugehen bis der Lerner bestaetigt (Z.201), ist genau die Pacing-Funktion, die ein abwesender Trainer sonst liefert.

## Befunde

### [high | structure | M] Block 3: drei widerspruechliche Reihenfolgen UND Titel fuer Modul 3.2/3.5 ueber die Navigationsdateien

- **Datei:** README.md / skills/workshop/SKILL.md / resources/session-plan.md / resources/glossary.md
- **Evidenz:** README.md Z.90-96 listet 3.5='Full Stack Architecture ... (Capstone)' und 3.2='Multi-Model Pipelines', Reihenfolge 3.1..3.5,3.6,3.7. SKILL.md Z.71-76 listet 3.2='Nested Orchestration', Reihenfolge 3.1,3.2,3.3,3.4,3.6,3.7,3.5 und 3.5='Telegram Bridge, Inception & Worktree Isolation (Capstone)'. glossary.md Z.306 'Modul: 3.5 — Telegram & Inception'. block-3-advanced.md Z.327 'Module 3.2: Nested Orchestration & Multi-Model Pipelines'.
- **Empfehlung:** Eine einzige Source-of-Truth fuer Modul-Titel und -Reihenfolge festlegen (Vorschlag: die Modul-Datei block-3-advanced.md) und README + SKILL.md + commands/workshop.md daran angleichen. Insbesondere 3.2 einheitlich 'Nested Orchestration & Multi-Model Pipelines' nennen und 3.5 einheitlich 'Telegram Bridge, Inception & Worktrees' — und entscheiden, welches Modul der Capstone ist (README sagt 3.5, das passt zu SKILL). Ein Solo-Lerner ohne Trainer kann diese Drift nicht selbst aufloesen.

### [high | didactics-onboarding | M] /workshop learn kann fehlendes Custom-Plugin-Setup nicht ersetzen — Sackgassen-Risiko in Block 3

- **Datei:** skills/workshop/SKILL.md
- **Evidenz:** SKILL.md Learn-Mode laedt resources/modules + resources/exercises (Z.155-159) und gibt 'YOUR TURN' mit 'what command to run' (Z.178-182) sowie 'CHECK' (Z.188-192). Es gibt aber KEINE Verzweigung fuer den Fall, dass die referenzierten Custom-Plugins (agentic-os, devil-advocate-swarms, multi-model-orchestrator) beim Solo-Lerner nicht installiert sind — laut prerequisites.md Z.235-238 ist Observation-Mode dann die einzige Option. Ein /workshop learn 3.3 wuerde den Lerner zu einer 'YOUR TURN'-Aktion fuehren, die er ohne Plugin nicht ausfuehren kann, ohne dass der Tutor das vorab prueft.
- **Empfehlung:** In Learn-Mode eine Preflight-Klausel ergaenzen: bei Block-3-Modulen, die Custom-Plugins brauchen (3.3/3.4/3.5/3.2), zuerst 'Hast du die workshop-custom Plugins installiert? Falls nein, hier ist der Observation-/Web-UI-Pfad' fragen (Verweis auf prerequisites.md Optionen A/B/C). So wird die in prerequisites dokumentierte Fallback-Logik auch im Trainer-Ersatz wirksam.

### [medium | currency | S] Modell durchgaengig 'Opus 4.7' — wirkt am Lesedatum 2026-06-21 veraltet

- **Datei:** resources/cheatsheet.md / glossary.md / faq.md / quick-reference.md
- **Evidenz:** cheatsheet.md Z.308 '**Claude Opus 4.7** | 1M tokens | Default in Claude Code since 2026-04-16 (GA)'; glossary.md Z.159 'Opus 4.7 (Default seit 2026-04-16 ...)'; faq.md Z.24 'Opus 4.7 fuer Architektur'. Alle Stand-Daten 2026-05-20. Die laufende Umgebung ist bereits Opus 4.8 (1M context) am 2026-06-21.
- **Empfehlung:** Modellbezeichnungen und Default-Modell pruefen und auf den aktuellen Stand bringen (Opus 4.8 falls GA), oder einen einzigen 'Stand:'-Hinweis mit dem Hinweis 'Modellnamen koennen sich aendern, /model und /release-notes pruefen' setzen, damit der Solo-Lerner die Diskrepanz zwischen Material und seiner laufenden CLI einordnen kann statt zu verunsichern. Web-Verifikation der aktuellen GA-Modelle vor dem Edit.

### [medium | didactics-onboarding | S] README Quick-Start (Selbstlerner) listet nicht dieselben Referenzdateien wie WORKSHOP_EINFUEHRUNG

- **Datei:** README.md
- **Evidenz:** README.md Z.28-37 'Als Selbstlerner' nennt nur prerequisites, WORKSHOP_EINFUEHRUNG, modules/demos/exercises und cheatsheet. WORKSHOP_EINFUEHRUNG.md Z.18-23 fuegt fuer den Selbstlerner zusaetzlich quick-reference.md hinzu, und Z.66-67 nennt fuer 'Selbstlerner ohne Workshop' explizit nur workshop-guide.md+modules/demos/exercises. faq.md, glossary.md, troubleshooting.md tauchen im README-Selbstlern-Pfad gar nicht auf, obwohl sie genau die Trainer-Ersatz-Funktion liefern.
- **Empfehlung:** Den Selbstlern-Quick-Start in README um die drei Trainer-Ersatz-Dateien ergaenzen (faq.md bei Konzeptfragen, troubleshooting.md wenn etwas klemmt, glossary.md bei unklaren Begriffen) und auf workshop-guide.md als primaeren Einstieg verweisen — aktuell wird workshop-guide.md im README-Selbstlern-Block nicht als Schritt 2 genannt, obwohl die EINFUEHRUNG ihn als Hauptnavigation empfiehlt.

### [medium | didactics-onboarding | M] Kein durchgaengiges 'Du bist hier / fertig'-Fortschrittssignal ueber Module hinweg fuer Solo-Lerner

- **Datei:** resources/workshop-guide.md
- **Evidenz:** workshop-guide.md Z.131-141 'Praktische Arbeitsweise' beschreibt eine Lernabend-Routine (Modul lesen -> Demo -> 1 Uebung -> cheatsheet), aber es gibt keine Checkliste/keinen Tracker, an dem ein Solo-Lerner abhakt, welche der 17 Module er abgeschlossen hat. Die Exercises haben ein 'Success Check' (gut), aber auf Modul-/Block-Ebene fehlt das uebergeordnete 'fertig'-Signal, das ein Trainer sonst gibt ('ihr habt Block 1 geschafft').
- **Empfehlung:** Eine einfache Fortschritts-Checkliste (17 Module mit Checkboxen, plus pro Modul ein 1-Satz-'Du kannst jetzt X'-Outcome) in workshop-guide.md oder als eigene progress.md ergaenzen. Bei jedem Modul ein klares Abschluss-Outcome (die Module haben bereits 'Learning Objectives', z.B. block-1-foundations.md Z.11-14 — diese als abhakbare Self-Check-Liste spiegeln).

### [low | exercise-quality | S] Exercise 1.1 nutzt ~/cc-workshop/exercises, prerequisites legt nur die Struktur an — und Pfade kollidieren teils

- **Datei:** resources/exercises/block-1-exercises.md / resources/prerequisites.md
- **Evidenz:** Exercise 1.1 Z.35 'mkdir -p ~/cc-workshop/exercises/exercise-1.1'. prerequisites.md Z.380-385 definiert ~/cc-workshop/{demos,exercises,workshop-playground}. Aber prerequisites.md Z.141-142 klont das Repo nach '~/cc-workshop/dynamic-workshop' und der playground liegt dann unter '~/cc-workshop/dynamic-workshop/workshop-playground', NICHT unter dem in Z.384 versprochenen '~/cc-workshop/workshop-playground'. Ein Solo-Lerner, der spaeter den Playground sucht, findet ihn am dokumentierten Ort nicht.
- **Empfehlung:** Workdir-Konvention (prerequisites.md Z.378-385) mit dem tatsaechlichen Clone-Pfad (Z.141-142) in Einklang bringen — entweder das Repo direkt nach ~/cc-workshop klonen oder den Struktur-Baum so anpassen, dass workshop-playground unter dynamic-workshop/ gezeigt wird.

### [low | windows-compat | S] prerequisites mischt 'python3/pip3' und Block-1 ist Python-frei — Reihenfolge irritiert Windows-Solo-Lerner

- **Datei:** resources/prerequisites.md
- **Evidenz:** prerequisites.md Z.97 'Step 5: Install Python 3 (for Block 2+)' und Block 1 braucht laut Z.216 keine Plugins; aber Exercise 1.1/1.3/1.4 (block-1-exercises.md, z.B. Z.43 'event_log_parser.py', Z.249 'validators.py') lassen Claude Python-Code erzeugen UND ausfuehren ('Run the tests', Z.289). Auf Windows ist 'python3' oft nicht der Befehl (nur 'python'); die Troubleshooting-Zeile Z.189 erwaehnt das, aber erst ganz unten. README Z.44/51 nutzt durchgaengig 'python3 -m pytest'.
- **Empfehlung:** Fuer Windows-Solo-Lerner frueh (bei Step 5 oder im README Quick Start) den Hinweis 'auf Windows ggf. python statt python3' platzieren und klarstellen, dass schon Block-1-Exercises Python ausfuehren (also Python doch ab Block 1 noetig ist, sobald man die Exercises macht — nicht erst 'Block 2+').

### [low | accuracy-overclaim | S] Bundled-Skills-Liste in glossary widerspricht der cheatsheet-Liste

- **Datei:** resources/glossary.md / resources/cheatsheet.md
- **Evidenz:** glossary.md Z.49 nennt Bundled Skills: '/batch, /loop, /run, /verify, /debug, /simplify, /claude-api, /fewer-permission-prompts, /run-skill-generator'. cheatsheet.md Z.257-267 listet zusaetzlich keine /tdd/-Bundled, aber faq/quick-reference behandeln /tdd und /commit unter 'Workshop-Specific Skills' (cheatsheet Z.243-249) — die Grenze Bundled vs. Workshop-custom ist zwischen den Dateien nicht deckungsgleich gezogen, was ein Solo-Lerner beim Nachschlagen als Widerspruch erlebt.
- **Empfehlung:** Eine kanonische Bundled-Skills-Liste definieren (am besten im Glossar) und cheatsheet darauf verweisen lassen, statt die Liste zu duplizieren. Klar trennen: offiziell-bundled vs. workshop-custom (/commit, /tdd).

### [low | currency | S] Stand-Daten der Referenzdateien (2026-05-20) und prerequisites (2026-04-03) divergieren — kein zentraler Versionsanker

- **Datei:** global
- **Evidenz:** faq.md Z.5 'Stand: 2026-05-20', glossary.md Z.5 'Stand: 2026-05-20', troubleshooting.md Z.6 'Stand: 2026-05-20', WORKSHOP_EINFUEHRUNG.md Z.69 'Stand: 2026-05-20', aber prerequisites.md Z.205 'Last Updated: 2026-04-03'. README/CLAUDE.md tragen kein Stand-Datum.
- **Empfehlung:** Einen einzigen Versions-/Stand-Anker einfuehren (z.B. eine Zeile in README oder ein VERSION-Feld) und die Einzeldateien darauf verweisen, damit ein Solo-Lerner auf einen Blick sieht, wie aktuell das Material insgesamt ist — statt acht verschiedene Stand-Zeilen zu vergleichen.

### [low | structure | S] SKILL.md Overview-Box listet Module in nicht-numerischer Reihenfolge (3.6/3.7 vor 3.5)

- **Datei:** skills/workshop/SKILL.md
- **Evidenz:** SKILL.md Z.71-76 zeigt in der ASCII-Box 3.1,3.2,3.3,3.4,3.6,3.7 und erst danach 3.5 ('Telegram Bridge, Inception & Worktree Isolation (Capstone)'). commands/workshop.md Z.26 listet dagegen 'Block 3 ...: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7' streng numerisch.
- **Empfehlung:** In der Overview-Box entweder strikt numerisch sortieren oder den Capstone-Charakter von 3.5 explizit kennzeichnen (z.B. '3.5 (Capstone — am Ende)'), damit der Solo-Lerner versteht, dass die Nicht-Reihenfolge Absicht ist und kein Tippfehler.

### [nice-to-have | accuracy-overclaim | S] Quick-Reference fuehrt /goal, /loop, /schedule auf, aber Glossar/FAQ markieren Routine als offizielle Variante — leichte Inkonsistenz beim Selbst-Nachschlagen

- **Datei:** resources/quick-reference.md / resources/faq.md
- **Evidenz:** quick-reference.md Z.40 fuehrt '/goal /loop /schedule' als 'Hot Slash-Commands' nebeneinander. faq.md Z.119-125 differenziert sie sauber (/loop=Zeit, /goal=Condition, Routine=persistent) und glossary.md Z.236 nennt Routine 'Offizielle Variante ... (Ersatz fuer /schedule + /loop)'. Die Quick-Reference suggeriert Gleichrangigkeit, ohne den Routine-Vorrang zu zeigen.
- **Empfehlung:** In der Quick-Reference einen Mini-Hinweis '/schedule+/loop -> Routine ist die persistente offizielle Variante (s. FAQ)' ergaenzen, damit der 1-Pager nicht im Widerspruch zur FAQ steht.
