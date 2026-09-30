# TODO-Backlog — Workshop-Review 2026-06-21

> 87 atomare TODOs, dedupliziert aus 129 Roh-Befunden. Bereit fuer eine Umsetzungs-Instanz.

**Prioritaets-Verteilung:** P0=7, P1=29, P2=38, P3=13

## Gesamtliste (nach Prioritaet)

| ID | P | Aufw. | Titel | Cluster | Dateien |
|---|---|---|---|---|---|
| T-001 | P0 | S | BLOCKER: --max-turns aus Exercise 3.6 entfernen (CLI-Flag existiert nicht) | currency | resources/exercises/block-3-exercises.md; resources/exercises/block-1-exercises.md; resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md |
| T-002 | P0 | S | Exercise 3.6 in ein isoliertes Sandbox-Repo umleiten — pre-commit-Hook darf nicht ins Schulungs-Repo schreiben | demo-reliability | resources/exercises/block-3-exercises.md |
| T-003 | P0 | S | Ungeplanten size_t-Unterlauf im C-Hex-Parser haerten oder als 5. Bonus-Vuln dokumentieren | demo-reliability | workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md |
| T-004 | P0 | S | Ueberschrift 'The Three Interfaces' korrigieren — listet fuenf Surfaces | structure | resources/modules/block-1-foundations.md |
| T-005 | P0 | S | python3/pip3 durchgaengig um Windows-Variante (python/pip) im Haupttext ergaenzen | windows-compat | resources/prerequisites.md; README.md |
| T-006 | P0 | M | 'Hello, Claude Code' — Erfolgserlebnis-Kapitel an den Anfang von Modul 1.1 setzen | missing-content | resources/modules/block-1-foundations.md; agents/workshop-mentor.md |
| T-007 | P0 | M | Vorbereitetes, Windows-getestetes secure-diff-gate Hook-Asset ins Repo legen (bash + Python-Variante) | windows-compat | resources/demos/block-2-demos.md; resources/demos/assets/hooks/secure-diff-gate.sh; resources/demos/assets/hooks/secure-diff-gate.py |
| T-008 | P1 | S | OSDP-Frame-Format im C-Playground sachlich korrigieren (ADDR vor LEN, 16-bit LEN, CRC-16/CCITT) | accuracy-overclaim | workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md |
| T-009 | P1 | S | Direkten Default-Widerspruch worktree.baseRef (head vs fresh) zwischen Block 1, Block 3 und Cheatsheet aufloesen | accuracy-overclaim | resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md |
| T-010 | P1 | S | acceptEdits-Beschreibung in Block 1 sicherheitsrelevant nachschaerfen (FS-Bash wie rm/mv wird auto-approved) | accuracy-overclaim | resources/modules/block-1-foundations.md |
| T-011 | P1 | S | Veraltete Modellversion 'Opus 4.6' auf 'Opus 4.8' aktualisieren (Block 1, Cheatsheet, Glossar) | accuracy-overclaim | resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/glossary.md |
| T-012 | P1 | S | Mentor-Agent: Modell-Empfehlung auf Opus 4.8 / Fable 5 aktualisieren | currency | agents/workshop-mentor.md |
| T-013 | P1 | S | Effort-Default fuer Opus 4.8 korrigieren: high (nicht xhigh) ist Default | currency | resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/faq.md |
| T-014 | P1 | S | Garantiert-lokalen Live-Anker fuer Session 3 festlegen und als Block-Eroeffnung positionieren | demo-reliability | resources/demos/block-3-demos.md; resources/session-plan.md |
| T-015 | P1 | S | Plugin-Fallbacks direkt in Exercise 3.3 einbauen (nicht nur in den Demos) | demo-reliability | resources/exercises/block-3-exercises.md |
| T-016 | P1 | S | broken-greeter/SKILL.md als kopierbares Asset ins Repo legen | demo-reliability | resources/demos/assets/broken-greeter/SKILL.md; resources/demos/block-3-demos.md |
| T-017 | P1 | S | Lernziele in Modul 1.1 vom Leichten zum Schweren umsortieren | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-018 | P1 | S | Exercise 3.3 Step 4: Playground-Vuln-Fix nur lokal/uncommitted anwenden und danach verwerfen | exercise-quality | resources/exercises/block-3-exercises.md; workshop-playground/CLAUDE.md |
| T-019 | P1 | S | 'Hooks auf Windows'-Notiz in den Cheatsheet aufnehmen (bash- und pwsh-Form) | missing-content | resources/cheatsheet.md |
| T-020 | P1 | S | Eine Master-Timeline pro Session als Source of Truth — session-plan.md und Dry-Run angleichen | structure | resources/session-plan.md; resources/dry-run-session-2-3-2026-05-21.md |
| T-021 | P1 | S | Widerspruch aufloesen: Exercises registrieren `bash ...`, troubleshooting.md verlangt `pwsh -File` | windows-compat | resources/exercises/block-2-exercises.md; resources/troubleshooting.md |
| T-022 | P1 | S | Pre-Flight-Checklist der trainer-notes auf Windows-tauglich umstellen | windows-compat | resources/trainer-notes.md |
| T-023 | P1 | M | Frontmatter-Feldnamen-Drift klaeren: context:fork und Subagent-Modellwahl (agent vs model) | accuracy-overclaim | resources/modules/block-2-ecosystem.md; resources/cheatsheet.md |
| T-024 | P1 | M | Live-Demo 3.7: zitierte /debug-Trace-Ausgaben gegen das echte Binary verifizieren oder als sinngemaess kennzeichnen | accuracy-overclaim | resources/demos/block-3-demos.md |
| T-025 | P1 | M | Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28) | currency | resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/glossary.md; resources/faq.md; resources/troubleshooting.md; resources/modules/block-3-advanced.md; resources/demos/block-1-demos.md |
| T-026 | P1 | M | Claude Fable 5 (Mythos-Klasse, GA 2026-06-09) in alle Modelltabellen aufnehmen | currency | resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/modules/block-3-advanced.md; resources/quick-reference.md; agents/workshop-mentor.md |
| T-027 | P1 | M | Eine abhakbare Go/No-Go-Demo-Matrix fuer den Workshop-Morgen anlegen | demo-reliability | resources/trainer-notes.md |
| T-028 | P1 | M | Modul 1.2 in Kern (Context + ./CLAUDE.md + /context + /compact) und Vertiefung splitten | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-029 | P1 | M | Preflight-Klausel im Learn-Mode fuer Block-3-Module mit Custom-Plugin-Bedarf ergaenzen | didactics-onboarding | skills/workshop/SKILL.md |
| T-030 | P1 | M | Block-2-Uebungen auf Hook-Merge statt komplettem settings.json-Overwrite umstellen | exercise-quality | resources/exercises/block-2-exercises.md |
| T-031 | P1 | M | PhySec-Logik-Vuln (fail-open) im Python-Playground ergaenzen — Scanner-vs-Domaenenkompetenz | missing-content | workshop-playground/access_control.py; workshop-playground/CLAUDE.md; resources/exercises/block-3-exercises.md |
| T-032 | P1 | M | Gefuehrte Domaenen-Uebung 3.9 ergaenzen: OSDP/Wiegand-Parser mit Claude bauen (TDD/Multi-Agent) | new-exercise-idea | resources/exercises/block-3-exercises.md; agents/workshop-mentor.md; workshop-playground/ |
| T-033 | P1 | M | Block-3-Modul-Titel und -Reihenfolge ueber alle Navigationsdateien vereinheitlichen | structure | README.md; skills/workshop/SKILL.md; resources/glossary.md; resources/modules/block-3-advanced.md; commands/workshop.md |
| T-034 | P1 | M | Session 3 realistisch planen: Live/Recording/Discussion-Spalte + fester 10-Min-Recovery-Puffer | structure | resources/session-plan.md; resources/dry-run-session-2-3-2026-05-21.md; resources/demos/block-3-demos.md |
| T-035 | P1 | M | Hook-Setup in prerequisites.md PowerShell-tauglich machen (Heredoc/jq/chmod/mkdir -p) | windows-compat | resources/prerequisites.md |
| T-036 | P1 | L | PowerShell-Parallelvariante fuer die zentrale Hook-Exercise 2.1 (safety-check) bereitstellen | windows-compat | resources/exercises/block-2-exercises.md |
| T-037 | P2 | S | Falsche Zeilenangaben der Vulnerabilities im C-Playground korrigieren oder entfernen | accuracy-overclaim | workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md |
| T-038 | P2 | S | FAQ-Verkuerzungen mit fehlenden Trade-offs/Eskalationen reparieren (ZDR-Feature-Verlust, Haiku-Eskalation, Modell-Multiplikatoren) | accuracy-overclaim | resources/faq.md; resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md |
| T-039 | P2 | S | Custom-Komponente notebooklm-Skill staerker als nicht-offiziell kennzeichnen + Installation in prerequisites.md dokumentieren | accuracy-overclaim | resources/modules/block-2-ecosystem.md; resources/prerequisites.md |
| T-040 | P2 | S | /model fable Command und Fast-Mode in cheatsheet & quick-reference dokumentieren | currency | resources/cheatsheet.md; resources/quick-reference.md |
| T-041 | P2 | S | Hook-Event-Count '28 lifecycle events' korrigieren oder vage formulieren | currency | resources/modules/block-2-ecosystem.md |
| T-042 | P2 | S | Zentralen Versions-/Stand-Anker einfuehren; divergierende Stand-Daten konsolidieren | currency | README.md; resources/prerequisites.md; resources/faq.md; resources/glossary.md; resources/troubleshooting.md; resources/WORKSHOP_EINFUEHRUNG.md |
| T-043 | P2 | S | Prerequisites: Mindest-CLI-Version und Update-Hinweis aufnehmen | currency | resources/prerequisites.md; resources/session-plan.md |
| T-044 | P2 | S | Budget-Cap in Demo 3.4 (Self-Improve) als Pflicht-Vorgabe VOR den /run-loop-Aufruf setzen | demo-reliability | resources/demos/block-3-demos.md |
| T-045 | P2 | S | CVE-Cleanup in Demo 3.3c als Ein-Befehl-Revert automatisieren | demo-reliability | resources/demos/block-3-demos.md |
| T-046 | P2 | S | Privacy-Block zu Auto-Memory in Modul 1.2 auf Kernwarnung kuerzen, Details nach 3.7 belassen | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-047 | P2 | S | Built-in-Tools-Referenztabelle in Modul 1.1 auf 5-6 Kern-Tools reduzieren, Vollreferenz ins cheatsheet | didactics-onboarding | resources/modules/block-1-foundations.md; resources/cheatsheet.md |
| T-048 | P2 | S | Modul-Header in Block 1 auf 'Experienced programmers NEW to coding agents' schaerfen | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-049 | P2 | S | Modell-Versions-Drift in Modul 1.1 aufloesen (Opus 4.8 Default vs. dokumentiertes 4.7) | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-050 | P2 | S | README-Selbstlern-Quick-Start um Trainer-Ersatz-Dateien und workshop-guide.md ergaenzen | didactics-onboarding | README.md |
| T-051 | P2 | S | Optionale Micro-Uebung 1.0 (~3 Min) vor Uebung 1.1 voranstellen | didactics-onboarding | resources/exercises/block-1-exercises.md |
| T-052 | P2 | S | Pairing-Fallback fuer Setup-Ausfaelle ins Trainer-Skript und Bundle in die Materialliste | didactics-onboarding | resources/session-plan.md; resources/trainer-notes.md |
| T-053 | P2 | S | Exercise 1.2 Step 6: Pushback-Erwartung von absolut ('It should') auf wahrscheinlichkeitsbasiert entschaerfen | exercise-quality | resources/exercises/block-1-exercises.md |
| T-054 | P2 | S | Workdir-Pfad-Inkonsistenz in prerequisites.md beheben (Clone-Pfad vs. dokumentierter Playground-Pfad) | exercise-quality | resources/prerequisites.md; resources/exercises/block-1-exercises.md |
| T-055 | P2 | S | 30-Sekunden-Verifikations-Zwischenschritt in Exercise 1.2 vor dem Restart einbauen | new-exercise-idea | resources/exercises/block-1-exercises.md; agents/workshop-mentor.md |
| T-056 | P2 | S | SKILL.md-Overview-Box: nicht-numerische Modul-Reihenfolge (3.6/3.7 vor 3.5) kennzeichnen oder sortieren | structure | skills/workshop/SKILL.md |
| T-057 | P2 | S | Eine kanonische Einstiegs-Reihenfolge der Orientierungsdateien festlegen und ueberall identisch wiederholen | structure | README.md; WORKSHOP_EINFUEHRUNG.md; resources/workshop-guide.md |
| T-058 | P2 | S | Demo 1.4: gh-PR-Recovery-Note und gh-Checklist-Eintrag mit dem Skript in Einklang bringen | structure | resources/demos/block-1-demos.md |
| T-059 | P2 | S | Exercise 2.3: konkreten Plugin-Namen festlegen — Platzhalter und 'agentic-os' nicht mischen | structure | resources/exercises/block-2-exercises.md |
| T-060 | P2 | S | Plugin-Reinstall in die Pre-Flight-Checklist aufnehmen (Laufzeit-Metadaten vs 17-Modul-Repo) | structure | resources/trainer-notes.md; resources/session-plan.md |
| T-061 | P2 | S | MCP-Config-Beispiel auf `python` statt `python3` umstellen | windows-compat | resources/modules/block-2-ecosystem.md |
| T-062 | P2 | M | V2-'Integer Overflow' im C-Playground entwiderspruechlichen (echter Overflow ODER ehrliche Umbenennung) | accuracy-overclaim | workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md |
| T-063 | P2 | M | Unbelegte Versions-Gates und 'when available'-Befehle bereinigen | accuracy-overclaim | resources/modules/block-2-ecosystem.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md; resources/modules/block-1-foundations.md |
| T-064 | P2 | M | Exercise 2.3: manuelles Schreiben in ~/.claude/plugins/cache/ durch CLI-konformen Weg ersetzen | accuracy-overclaim | resources/exercises/block-2-exercises.md |
| T-065 | P2 | M | Vorgriffe auf Block 2/3 in Block 1 zu 'Ausblick'-Teasern eindampfen | didactics-onboarding | resources/modules/block-1-foundations.md |
| T-066 | P2 | M | Modul 1.5 (Cost Engineering) auf 5-Min-Kern eindampfen und Rest als optional/Vertiefung kennzeichnen | didactics-onboarding | resources/modules/block-1-foundations.md; resources/exercises/block-1-exercises.md |
| T-067 | P2 | M | Modul 3.3 in 3.3a 'Adversarial Testing' und 3.3b 'Hardening & Compliance' splitten | didactics-onboarding | resources/modules/block-3-advanced.md |
| T-068 | P2 | M | Fortschritts-Checkliste (17 Module mit 'Du kannst jetzt X'-Outcomes) fuer Solo-Lerner ergaenzen | didactics-onboarding | resources/workshop-guide.md |
| T-069 | P2 | M | Exercise 3.3 'confirm three vulns'-Erwartung an Playground-Realitaet (ADMIN_PASSWORD toter Code) anpassen | exercise-quality | resources/exercises/block-3-exercises.md; workshop-playground/access_control.py; workshop-playground/CLAUDE.md |
| T-070 | P2 | M | Off-by-one-Vuln V4 in osdp_frame_decoder.c fachlich plausibel umbauen (CRC-Position statt konstruiertem raw[5]) | exercise-quality | workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md |
| T-071 | P2 | M | auto-Mode-Klassifikator entmystifizieren — Klassifikator-Inputs + Cheatsheet-Verweis in Modul 3.3 | missing-content | resources/modules/block-3-advanced.md; resources/cheatsheet.md |
| T-072 | P2 | M | POSIX-Shell-Snippets in allen Exercise-Dateien Windows-tauglich machen (mkdir -p, &&, chmod, Heredoc, ~/) | windows-compat | resources/exercises/block-1-exercises.md; resources/exercises/block-2-exercises.md; resources/exercises/block-3-exercises.md; resources/prerequisites.md |
| T-073 | P2 | M | export/env-vars und Konzept-nur-bash-Beispiele um PowerShell-Aequivalente ergaenzen | windows-compat | resources/prerequisites.md; resources/demos/block-1-demos.md; resources/modules/block-3-advanced.md; resources/modules/block-2-ecosystem.md |
| T-074 | P2 | L | OSDP-Secure-Channel-Abschnitt (SCBK/Default-Key/Replay/Tamper) in Modul 3.3 / C-Playground ergaenzen | missing-content | resources/modules/block-3-advanced.md; workshop-playground/CLAUDE.md; workshop-playground/osdp_frame_decoder.c |
| T-075 | P3 | S | Analogie 'Self-Improve Loop = naechtliche Firmware-Selbstheilung' didaktisch umstellen (Einschraenkung zuerst) | accuracy-overclaim | resources/modules/block-3-advanced.md |
| T-076 | P3 | S | SSE-MCP-Deprecation-Kontext und Scope-Renaming-Warnung schaerfen | currency | resources/modules/block-2-ecosystem.md |
| T-077 | P3 | S | Haiku-Kontextgrenze (200K vs 1M) mit Konsequenz-Footnote versehen | currency | resources/modules/block-1-foundations.md |
| T-078 | P3 | S | Demo-Dauern im session-plan.md realistisch ausweisen und Bonus-Schritte als optional markieren | demo-reliability | resources/session-plan.md |
| T-079 | P3 | S | Exercise 1.5 klar als optional markieren und Modell/Effort-Default-Startpunkte hervorheben | didactics-onboarding | resources/exercises/block-1-exercises.md |
| T-080 | P3 | S | Flag-Erklaerungen ergaenzen: --print in prerequisites und Custom-Plugin-Setup-Zeit in Block 3 | didactics-onboarding | resources/prerequisites.md; resources/modules/block-3-advanced.md |
| T-081 | P3 | S | Log-Injection in access_control.py vom 'Bonus' zur regulaeren PhySec-Vuln aufwerten (EN-50131-Audit-Trail) | exercise-quality | workshop-playground/access_control.py; workshop-playground/CLAUDE.md; resources/exercises/block-3-exercises.md; resources/modules/block-3-advanced.md |
| T-082 | P3 | S | Block-2-Zeitbudgets realistisch anheben und npx-MCP-Erstinstall in prerequisites vorziehen | exercise-quality | resources/exercises/block-2-exercises.md; resources/prerequisites.md; resources/session-plan.md |
| T-083 | P3 | S | C-Playground-Build (gcc/clang/scan-build) fuer Windows framen oder als compile-frei kennzeichnen | windows-compat | workshop-playground/CLAUDE.md; workshop-playground/Makefile |
| T-084 | P3 | M | Kosmetische Cross-Datei-Inkonsistenzen vereinheitlichen (Bundled-Skills-Liste, Quick-Reference/Routine, Windows-Sandbox-Ton, Hook-Event-Zahl) | accuracy-overclaim | resources/glossary.md; resources/cheatsheet.md; resources/quick-reference.md; resources/faq.md; resources/modules/block-2-ecosystem.md; resources/modules/block-3-advanced.md |
| T-085 | P3 | M | Neue Features als Kurz-Notizen ergaenzen: Dynamic Workflows, Lean System Prompt, ultracode | currency | resources/modules/block-3-advanced.md; resources/modules/block-1-foundations.md; resources/modules/block-2-ecosystem.md |
| T-086 | P3 | M | Realistisches Kern-vs-Vertiefung-Zeitbudget pro Modul in Block 1 ausweisen | didactics-onboarding | resources/exercises/block-1-exercises.md; resources/modules/block-1-foundations.md; resources/session-plan.md |
| T-087 | P3 | M | Optionales Fable-5-Vision-Unterkapitel/Exercise fuer PhySec-Use-Cases (CCTV/OCR) ergaenzen | missing-content | resources/modules/block-3-advanced.md; resources/exercises/block-3-exercises.md; agents/workshop-mentor.md |

---

## Details nach Cluster

### Cluster: `didactics-onboarding` (17 TODOs)

20 Roh-Befunde von 6 Personas, konsolidiert zu 14 atomaren TODOs. Dominantes Muster (von der Kern-Einstiegshuerden-Persona Anna + Markus + Lena): Block 1 und Modul 3.3 ueberfordern Neulinge kognitiv — die Module starten mit den schwersten Lernzielen (6 Permission Modes, Modell-/Effort-Wahl), buendeln ~20 neue Begriffe pro Einheit, greifen massiv auf Block 2/3 vor und vermischen Pflicht-Kern mit Vertiefung ohne Kennzeichnung. Loesungs-Leitlinie quer durch fast alle Befunde: NICHTS loeschen, sondern (a) Lernziele/Konzepte vom Leichten zum Schweren ordnen, (b) Kern vs. Vertiefung explizit markieren/splitten, (c) Vorgriffe auf 1-Satz-Teaser eindampfen. Zweiter Cluster (Solo-Lerner-Personas Tom + Lena): fehlende Trainer-Ersatz-Verweise im README, kein Fortschritts-Tracker, kein Plugin-Preflight im Learn-Mode, kein Micro-Erfolgserlebnis vor Uebung 1.1. Dritter Cluster (Currency + Live-Moderation): Modell-Versions-Drift (Opus 4.7 vs. 4.8 Default), undokumentierte Custom-Plugin-Setup-Zeit, kein Setup-Ausfall-Fallback fuer Live-Sessions. Alle stichprobenartig geprueften Evidenz-Zeilen (Modul 1.1 Z.11-14, Built-in-Tools-Tabelle Z.131-148, Privacy-Block Z.338-349, prerequisites Step 3 Z.74-77, README Selbstlern-Block Z.28-37) bestaetigt; die genannten Trainer-Ersatz-Dateien (faq/glossary/troubleshooting/workshop-guide/quick-reference) existieren tatsaechlich, werden aber im README-Selbstlernpfad nicht verlinkt. Priorisierung: Einstiegshuerden-/Lernerfolg-Befunde (Lernziel-Reihenfolge, Modul-Splits, Sackgassen-Risiko im Learn-Mode) vor Korrektheit/Currency (Versions-Drift) vor Komfort (Setup-Zeit-Angaben).

#### T-017 — Lernziele in Modul 1.1 vom Leichten zum Schweren umsortieren  `[P1 | S]`

Modul 1.1 startet mit den schwersten Lernzielen statt einem mentalen Grundmodell. Z.11-14 (verifiziert): erstes Lernziel ist 'Distinguish between Claude Code's surfaces', zweites 'Identify when each of the 6 permission modes (default / acceptEdits / plan / auto / dontAsk / bypassPermissions) applies', drittes 'Choose the right model (Opus 4.7 / Sonnet 4.6 / Haiku 4.5) and effort level'. Ein Neuling braucht zuerst das Grundmodell 'Was ist ein Coding Agent und wie unterscheidet er sich von einem Chat'. Neues erstes Lernziel: 'Verstehen, was ein Coding Agent ist und wie er sich von einem Chat unterscheidet'. Die 6-Modi-Taxonomie und Modell/Effort-Wahl als spaetere/optionale Lernziele markieren oder in einen 'Vertiefung'-Block schieben — Inhalt bleibt, nur Reihenfolge und Kennzeichnung aendern.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Die erste Stunde des allerersten Moduls entscheidet ueber die Einstiegshuerde der Kern-Zielgruppe (erfahrene Programmierer, NULL Agent-Erfahrung). Mit einer 6-Modi-Taxonomie als zweitem Lernziel zu starten erzeugt Ueberforderung, bevor ueberhaupt ein Grundmodell steht.
- **Akzeptanz:** Erstes Lernziel in Modul 1.1 ist das Agent-vs-Chat-Grundmodell; Permission Modes und Modell/Effort sind als spaeter/optional gekennzeichnet oder in einen Vertiefungs-Abschnitt verschoben.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-028 — Modul 1.2 in Kern (Context + ./CLAUDE.md + /context + /compact) und Vertiefung splitten  `[P1 | M]`

Modul 1.2 fuehrt ~20 neue Begriffe/Befehle in einer Einheit ein: Context-Window, Auto-Kompression, CLAUDE.md (2 Levels), CLAUDE.local.md, Managed CLAUDE.md, .claude/rules/ mit YAML-paths, Auto-Memory + MEMORY.md/topic-files, @path-Imports, @AGENTS.md-Interop, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, /context /compact /export /resume /memory /init /rewind, --bare, 'claude project purge'. Aufteilen in (a) Kern-Neulingsteil: Context-Window-Analogie + ./CLAUDE.md + /context + /compact; (b) 'Vertiefung Memory & Multi-Repo': rules/, Managed-CLAUDE.md, --add-dir, @AGENTS.md, Auto-Memory-Internals. Teil (b) explizit als 'beim ersten Durchgang ueberspringbar' kennzeichnen. Nichts loeschen.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Kognitive Ueberlastung: 20 neue Konzepte in einer Lerneinheit verhindern Verankerung. Ein expliziter Kern-/Vertiefungs-Schnitt senkt die Last drastisch, ohne Inhalt zu verlieren.
- **Akzeptanz:** Modul 1.2 hat einen klar abgegrenzten Kern-Teil (nur Context-Window, ./CLAUDE.md, /context, /compact) und einen als 'beim ersten Durchgang ueberspringbar' markierten Vertiefungs-Teil mit den restlichen Themen.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-046 — Privacy-Block zu Auto-Memory in Modul 1.2 auf Kernwarnung kuerzen, Details nach 3.7 belassen  `[P2 | S]`

Z.338-349 (verifiziert): ausfuehrlicher Privacy-Block zu Auto-Memory (was an Anthropic gesendet wird, 'Avoid sensitive content', periodisch MEMORY.md reviewen, Opt-out --bare, 'claude project purge', Verweis auf Modul 3.7 Drift-Detection) mitten im zweiten Foundations-Modul. Auf 2-3 Saetze kuerzen: 'Auto-Memory schreibt Notizen auf Platte und sendet sie bei Sessionstart mit — keine Secrets hineinschreiben, Opt-out via --bare.' Details (purge, periodisches Review, Drift-Detection) in Modul 3.7 belassen/verweisen.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Inhaltlich korrekt, aber an dieser fruehen Stelle Overload. Der Neuling muss in 1.2 nur die Kernwarnung (keine Secrets) mitnehmen, nicht das volle Privacy-Regime.
- **Akzeptanz:** Privacy-Hinweis in 1.2 ist auf 2-3 Saetze gekuerzt; die Details (purge, periodisches Review, Drift-Detection) stehen nur noch in/verweisen auf Modul 3.7.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)
- **Abhaengig von:** Modul 1.2 in Kern und Vertiefung splitten

#### T-065 — Vorgriffe auf Block 2/3 in Block 1 zu 'Ausblick'-Teasern eindampfen  `[P2 | M]`

Block 1 erklaert mehrfach voll aus, was erst in Block 2/3 anfassbar ist: Modul 1.4 zu /autofix-pr (Cloud-Session watcht CI), --fork-session, worktree.baseRef 'fresh' fuer 'multi-agent worktree setups in Block 3' (Z.868), --from-pr; Modul 1.1 nennt Computer Use, MCP, Sub-Agents. Als Neuling ohne erste erfolgreiche Session erzeugen diese voll ausgefuehrten Begriffe das Gefuehl 'das ist riesig, ich komme nie hinterher'. Faustregel fuer Block 1: nur voll erklaeren, was man in der ersten Session selbst anfassen kann; den Rest in 'Ausblick'-Kaesten buendeln (1-2 Zeilen + Verweis 'Details in Block 3.x').

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Vorgriffe ohne erste Erfolgserfahrung schrecken die Einstiegshuerden-Persona ab. Teaser statt Vollerklaerung haelt die Block-1-Last auf das beim ersten Durchgang Anfassbare begrenzt.
- **Akzeptanz:** Block-2/3-Vorgriffe in Block 1 (z.B. /autofix-pr, --fork-session, worktree.baseRef, --from-pr, Computer Use) stehen als 1-2-Zeilen-Ausblick mit Verweis statt als Vollerklaerung.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-047 — Built-in-Tools-Referenztabelle in Modul 1.1 auf 5-6 Kern-Tools reduzieren, Vollreferenz ins cheatsheet  `[P2 | S]`

Z.131-148 (verifiziert): Tabelle mit 18 Tools inkl. NotebookEdit, PowerShell, LSP, Skill, Agent, Monitor, AskUserQuestion, TaskCreate/TaskList/TaskUpdate in Modul 1.1; direkt darunter Note Z.152 'Skill and Agent ... explored in depth in Block 2.1 ... Block 3.1.' Im ersten Modul nur die 5-6 sofort sichtbaren Tools zeigen (Read, Edit, Write, Bash, Grep). Die Vollreferenz mit allen 18 Tools ins resources/cheatsheet.md verschieben und in 1.1 darauf verlinken.

- **Dateien:** resources/modules/block-1-foundations.md; resources/cheatsheet.md
- **Begruendung:** Eine 18-Zeilen-Tabelle mit Tools, die erst in Block 2/3 relevant werden, ist Ballast in der ersten Stunde. Die Vollreferenz gehoert ins Nachschlagewerk, nicht in den Erst-Lesefluss.
- **Akzeptanz:** Modul 1.1 zeigt nur ~5-6 Kern-Tools (Read, Edit, Write, Bash, Grep) und verlinkt fuer die Vollreferenz auf cheatsheet.md; die 18-Tool-Tabelle steht (mindestens) im cheatsheet.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-066 — Modul 1.5 (Cost Engineering) auf 5-Min-Kern eindampfen und Rest als optional/Vertiefung kennzeichnen  `[P2 | M]`

Modul 1.5 (Z.927-1130) verlangt nach ~80 Min Theorie ein dichtes Finanz-/Optimierungsthema: Pricing-Tabelle ($/M Input/Output pro Modell), Effort-Multiplikatoren (0.5x-6x), Plan/Implement/Review-Pipeline, --max-budget-usd/--max-turns, Prompt-Caching mit 5-Min-TTL und 90%-Rabatt, --exclude-dynamic-system-prompt-sections — OHNE dass der Neuling bisher Geld ausgegeben oder ein Gefuehl fuer normale Spends hat. Auf 5-Min-Kern eindampfen ('/cost gibt es, schau gelegentlich drauf; Default-Modell ist ok') und Rest (Pricing-Details, Pipeline, Caching, Budget-Caps) als eigenstaendiges Vertiefungs-Modul nach Session 1 / optionalen Anhang fuehren. Konsistenz: die zugehoerige Exercise 1.5 ist bereits als 'Should-do/optional' markiert — das Modul sollte ebenfalls als optional/spaeter gekennzeichnet sein.

- **Dateien:** resources/modules/block-1-foundations.md; resources/exercises/block-1-exercises.md
- **Begruendung:** Cost-Optimierung als 5. Modul des ersten Tages ist fuer Neulinge ohne Spend-Erfahrung zu viel und inkonsistent zur bereits als optional markierten Exercise 1.5.
- **Akzeptanz:** Modul 1.5 hat einen 5-Min-Kern und ist als optional/Vertiefung gekennzeichnet, konsistent zur Exercise-1.5-Markierung; die Detailthemen sind als Anhang/Nachsession ausgewiesen.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-048 — Modul-Header in Block 1 auf 'Experienced programmers NEW to coding agents' schaerfen  `[P2 | S]`

Z.3 (verifiziert): 'Audience: Experienced programmers. Security analogies used throughout — especially relevant for the CySec engineer in the group.' Die Zielgruppe sind laut Auftrag erfahrene Entwickler MIT NULL Agent-Erfahrung. Der jetzige Header wird im Material durchgehend als Lizenz genutzt, Agent-Grundlagen knapp zu halten. Header schaerfen: 'Audience: Experienced programmers who are NEW to coding agents.' Das Material soll Programmier-Vorwissen voraussetzen, aber Agent-Konzepte konsequent bei Null erklaeren.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Der unscharfe Header rechtfertigt knappe Agent-Grundlagen und steht im Widerspruch zur tatsaechlichen Zielgruppe (Programmier-Vorwissen, aber Agent-Neuling). Eine klare Audience-Definition steuert die didaktische Tiefe richtig.
- **Akzeptanz:** Block-1-Header nennt explizit 'experienced programmers who are NEW to coding agents' (oder deutsches Aequivalent), sodass Programmier-Vorwissen vorausgesetzt, Agent-Konzepte aber bei Null erklaert werden.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)

#### T-049 — Modell-Versions-Drift in Modul 1.1 aufloesen (Opus 4.8 Default vs. dokumentiertes 4.7)  `[P2 | S]`

Doppelter Befund. (1) Modul 1.1 nennt 'Opus 4.7 / Sonnet 4.6 / Haiku 4.5' (Z.14) und beschreibt 4.7 als Default. (2) Seit v2.1.154 startet 'claude' ohne Flags automatisch mit Opus 4.8 und lean system prompt — Kontextfenster-Vorhersagen und Kosten-Beispiele aus dem Workshop passen dann nicht zur tatsaechlichen Session. In Modul 1.1 frueh klarstellen, z.B.: 'Beim Starten einer Claude-Code-Session (nach v2.1.154) sehen Sie automatisch Opus 4.8. Dieses Skript wurde mit Opus 4.7 geschrieben — die Commands sind identisch, aber Modell-Effizienzen und Context-Overhead unterscheiden sich. Mit /model opus-4-7 koennen Sie zur Vorgaenger-Version wechseln, um die Beispiele zu replizieren.' Modellnamen in der Selection-Tabelle (ab Z.158) entsprechend pruefen.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Sachliche Currency: Ein Teilnehmer sieht beim ersten Start Opus 4.8, das Skript sagt 4.7. Subtil, aber real verwirrend, weil Context- und Kostenbeispiele dann nicht zur Live-Session passen.
- **Akzeptanz:** Modul 1.1 erklaert die Diskrepanz zwischen dem Live-Default (Opus 4.8/lean prompt) und den im Skript verwendeten 4.7-Beispielen und nennt /model opus-4-7 als Replikationspfad.
- **Quelle:** Currency-Auditor — CLI/Flags/Commands/Versionen

#### T-067 — Modul 3.3 in 3.3a 'Adversarial Testing' und 3.3b 'Hardening & Compliance' splitten  `[P2 | M]`

Modul 3.3 (Z.444-801) packt ~10 eigenstaendige Konzepte unter eine Ueberschrift: Devil's-Advocate-4-Stufen-Pipeline, Security-Audit-Skill, 3 advanced Permission Modes, Protected Paths, Review-Trio, Permission-Rule-Grammatik, sandbox.network.deniedDomains, disableSkillShellExecution, 4 Sandbox-Level, Data-Retention-Tabelle, 6-Zeilen-Compliance-Tabelle (EN50131/GDPR/HIPAA/PCI/DORA/NIS2). Splitten in 3.3a 'Adversarial Testing' (Swarm + Review-Trio + Audit-Skill) und 3.3b 'Hardening & Compliance' (advanced Permission Modes, Protected Paths, Sandbox-Level, Retention, Regulatorik). Feinere Granularitaet hilft besonders dem Compliance-Teil, der fuer regulierte PhySec-Firmen am wertvollsten ist.

- **Dateien:** resources/modules/block-3-advanced.md
- **Begruendung:** 10 Konzepte unter einer Ueberschrift verhindern Verankerung. Der Split trennt das didaktisch wertvolle Compliance-Material sauber ab.
- **Akzeptanz:** Block 3 enthaelt zwei getrennte Lerneinheiten 3.3a (Adversarial Testing) und 3.3b (Hardening & Compliance) statt eines Monolith-Moduls 3.3.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin

#### T-029 — Preflight-Klausel im Learn-Mode fuer Block-3-Module mit Custom-Plugin-Bedarf ergaenzen  `[P1 | M]`

skills/workshop/SKILL.md Learn-Mode laedt Module + Exercises (Z.155-159) und fuehrt den Lerner zu 'YOUR TURN' mit 'what command to run' (Z.178-182) und 'CHECK' (Z.188-192) — aber OHNE Verzweigung fuer den Fall, dass die referenzierten Custom-Plugins (agentic-os, devil-advocate-swarms, multi-model-orchestrator) beim Solo-Lerner nicht installiert sind. Laut prerequisites.md Z.235-238 ist Observation-Mode dann die einzige Option. Ein '/workshop learn 3.3' wuerde den Lerner zu einer Aktion fuehren, die er ohne Plugin nicht ausfuehren kann. Im Learn-Mode bei Block-3-Modulen mit Plugin-Bedarf (3.2/3.3/3.4/3.5) zuerst fragen: 'Hast du die workshop-custom Plugins installiert? Falls nein, hier ist der Observation-/Web-UI-Pfad' (Verweis auf prerequisites Optionen A/B/C).

- **Dateien:** skills/workshop/SKILL.md
- **Begruendung:** Sackgassen-Risiko: Der Trainer-Ersatz fuehrt den Solo-Lerner ohne Vorpruefung in eine YOUR-TURN-Aktion, die er ohne installiertes Plugin nicht ausfuehren kann. Die in prerequisites dokumentierte Fallback-Logik muss auch im Learn-Mode greifen.
- **Akzeptanz:** Learn-Mode prueft bei Block-3-Modulen mit Plugin-Bedarf vor 'YOUR TURN' den Plugin-Status und bietet bei fehlender Installation explizit den Observation-/Web-UI-Pfad an (Verweis auf prerequisites-Optionen).
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch

#### T-050 — README-Selbstlern-Quick-Start um Trainer-Ersatz-Dateien und workshop-guide.md ergaenzen  `[P2 | S]`

README.md Z.28-37 'Als Selbstlerner' nennt nur prerequisites, WORKSHOP_EINFUEHRUNG, modules/demos/exercises und cheatsheet. WORKSHOP_EINFUEHRUNG.md ergaenzt fuer Selbstlerner zusaetzlich quick-reference.md und nennt workshop-guide.md als Hauptnavigation. faq.md, glossary.md, troubleshooting.md tauchen im README-Selbstlern-Pfad gar nicht auf, obwohl sie die Trainer-Ersatz-Funktion liefern. Verifiziert: alle fuenf Dateien (resources/faq.md, glossary.md, troubleshooting.md, workshop-guide.md, quick-reference.md) existieren, werden im README-Selbstlernblock aber nicht verlinkt. Quick-Start ergaenzen: workshop-guide.md als primaeren Einstieg (Schritt 2), plus faq.md (Konzeptfragen), troubleshooting.md (wenn etwas klemmt), glossary.md (unklare Begriffe), quick-reference.md (Referenz).

- **Dateien:** README.md
- **Begruendung:** Der Solo-Lerner ohne Moderator findet ueber das README seine Trainer-Ersatz-Ressourcen nicht — genau die Dateien, die einen Trainer ersetzen, fehlen im Einstiegspfad. Inkonsistenz zwischen README und WORKSHOP_EINFUEHRUNG.
- **Akzeptanz:** README-Selbstlern-Quick-Start nennt workshop-guide.md als Einstieg sowie faq.md, troubleshooting.md, glossary.md und quick-reference.md mit jeweils kurzer Zweckangabe; konsistent zu WORKSHOP_EINFUEHRUNG.
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch

#### T-068 — Fortschritts-Checkliste (17 Module mit 'Du kannst jetzt X'-Outcomes) fuer Solo-Lerner ergaenzen  `[P2 | M]`

workshop-guide.md Z.131-141 'Praktische Arbeitsweise' beschreibt eine Lernabend-Routine, aber es gibt keinen Tracker, an dem ein Solo-Lerner abhakt, welche der 17 Module er abgeschlossen hat. Die Exercises haben 'Success Check', aber auf Modul-/Block-Ebene fehlt das uebergeordnete 'fertig'-Signal, das ein Trainer sonst gibt ('ihr habt Block 1 geschafft'). Eine einfache Fortschritts-Checkliste (17 Module mit Checkboxen, pro Modul ein 1-Satz-'Du kannst jetzt X'-Outcome) in workshop-guide.md oder als eigene progress.md ergaenzen. Die vorhandenen 'Learning Objectives' der Module (z.B. block-1-foundations.md Z.11-14) als abhakbare Self-Check-Liste spiegeln.

- **Dateien:** resources/workshop-guide.md
- **Begruendung:** Ohne Fortschrittssignal fehlt dem Solo-Lerner das motivierende 'fertig'-Erlebnis und die Orientierung, wo er im 17-Modul-Pfad steht — eine zentrale Trainer-Funktion.
- **Akzeptanz:** Es existiert eine abhakbare Fortschritts-Checkliste ueber alle 17 Module (in workshop-guide.md oder progress.md), je Modul mit einer 1-Satz-'Du kannst jetzt X'-Outcome-Zeile.
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch

#### T-051 — Optionale Micro-Uebung 1.0 (~3 Min) vor Uebung 1.1 voranstellen  `[P2 | S]`

Uebung 1.1 startet sofort mit einem komplexen Multi-File-Auftrag: Parser + Sample-Datei + 4 Anforderungen + --door-Flag + diff-Erklaerung (Z.42-83), Zeitbudget 12-15 Min — verifiziert (event_log_parser.py-Prompt, sample_events.txt, --door-Flag, Diff-Erklaerung). Davor fehlt eine 2-3-Minuten-Mini-Uebung, um die describe-implement-run-Schleife einmal trivial zu erleben. Optionale Micro-Uebung 1.0 voranstellen: Claude in leerem Ordner starten, triviale Aufgabe stellen ('Erstelle eine Datei hello.txt mit dem Inhalt Hallo'), Ergebnis pruefen. Senkt die Einstiegslast und gibt sofort ein Erfolgserlebnis.

- **Dateien:** resources/exercises/block-1-exercises.md
- **Begruendung:** Ein triviales Erst-Erfolgserlebnis vor der ersten echten Aufgabe senkt die kognitive Einstiegslast und gibt der Hands-on-Persona Sicherheit in der describe-implement-run-Schleife.
- **Akzeptanz:** Vor Uebung 1.1 steht eine als optional markierte Micro-Uebung 1.0 (~3 Min) mit einer trivialen describe-implement-run-Aufgabe und Erfolgs-Check.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt

#### T-052 — Pairing-Fallback fuer Setup-Ausfaelle ins Trainer-Skript und Bundle in die Materialliste  `[P2 | S]`

trainer-notes.md Failure-Tabelle Z.67 nennt 'Teilnehmer-Maschine bricht beim Setup -> Vorab ~/cc-workshop-Bundle bereithalten, USB-Stick'. session-plan.md plant aber feste Exercise-Bloecke (z.B. Z.25 'Exercises 1.1+1.2 Hands-on', Z.48 'Exercises 2.1+2.2'). Bei nur 3 Teilnehmern blockiert ein gebrochenes Setup ein Drittel des Hands-on-Blocks. Pairing-Fallback-Regel ins Trainer-Skript: 'Bricht ein Setup, Teilnehmer paart sich mit Nachbarn (driver/navigator), waehrend ich parallel debugge.' Zusaetzlich den USB-Stick-/Bundle-Hinweis aus der Failure-Tabelle in die Materialliste (session-plan.md Z.99-105) hochziehen, damit er vorbereitet wird.

- **Dateien:** resources/session-plan.md; resources/trainer-notes.md
- **Begruendung:** Bei nur 3 Teilnehmern ist ein einzelner Setup-Ausfall hoch sichtbar und blockiert die Hands-on-Bloecke. Eine vorab definierte Pairing-Regel + vorbereitetes Bundle haelt die Live-Session am Laufen.
- **Akzeptanz:** session-plan.md/trainer-notes.md enthalten eine Pairing-Fallback-Regel fuer gebrochene Setups, und der USB-/Bundle-Hinweis steht in der Materialliste (nicht nur in der Failure-Tabelle).
- **Quelle:** Sandra — Live-Moderatorin

#### T-086 — Realistisches Kern-vs-Vertiefung-Zeitbudget pro Modul in Block 1 ausweisen  `[P3 | M]`

exercises Z.4 nennt '~85-90 minutes total for all Block 1 exercises'; block-1-foundations.md ist ~1145 Zeilen dichtes Material mit 'Duration: ~90 minutes' (Z.4). Zusammen mit Demos passt das nicht realistisch in eine ~3h-Session, wenn ein Neuling die Module wirklich versteht statt ueberfliegt. Pro Modul kennzeichnen, was Pflicht-Lesestoff (Kern) und was Nachlese (Vertiefung) ist, und ein realistisches Neulings-Zeitbudget ausweisen — damit in 3h ein Erfolgserlebnis statt Hetze entsteht. Dieses TODO buendelt die Kern/Vertiefung-Markierung modulweit; die Splits in 1.2/1.5 liefern die Bausteine.

- **Dateien:** resources/exercises/block-1-exercises.md; resources/modules/block-1-foundations.md; resources/session-plan.md
- **Begruendung:** Das aktuelle Zeitbudget ist fuer die Neulings-Persona unrealistisch; ein klarer Kern-/Vertiefungs-Schnitt mit ehrlichem Timing verhindert Hetze und Frust in der ersten Session.
- **Akzeptanz:** Jedes Block-1-Modul ist als Kern (Pflicht) oder Vertiefung (Nachlese) gekennzeichnet, und session-plan/exercises weisen ein realistisches Neulings-Zeitbudget fuer den Kern aus.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung)
- **Abhaengig von:** Modul 1.2 in Kern und Vertiefung splitten; Modul 1.5 (Cost Engineering) auf 5-Min-Kern eindampfen und Rest als optional/Vertiefung kennzeichnen

#### T-079 — Exercise 1.5 klar als optional markieren und Modell/Effort-Default-Startpunkte hervorheben  `[P3 | S]`

Exercise 1.5 verlangt pro Workflow Model + Effort + Flags zu waehlen (Tabelle Z.499-504) und nennt Aliases --effort xhigh, --model opus/sonnet/haiku (Z.523-525); --effort xhigh ist gegen die CLI verifiziert korrekt (low/medium/high/xhigh/max). Fuer einen kompletten Neuling am Ende der ALLERERSTEN Session ist bewusste Modell/Effort-Wahl kognitiv anspruchsvoll; die Begruendungs-Spalte 'not just felt right' (Z.536) verlangt Erfahrungswissen. 1.5 bleibt 'Should-do/optional' (gut), aber die Hint-Defaults (Z.552 Sonnet/medium etc.) staerker als sicheren Startpunkt hervorheben, damit Neulinge nicht in Analyse-Paralyse geraten. Verschiebung nach Block 2/3 erwaegen.

- **Dateien:** resources/exercises/block-1-exercises.md
- **Begruendung:** Die bewusste Modell-/Effort-Wahl setzt Erfahrungswissen voraus, das in Block 1 noch nicht aufgebaut ist. Klar markierte Default-Startpunkte verhindern Analyse-Paralyse bei der Neulings-Persona.
- **Akzeptanz:** Exercise 1.5 ist sichtbar als optional ausgewiesen und nennt die Hint-Defaults (z.B. Sonnet/medium) prominent als sicheren Startpunkt; ggf. ein Hinweis, dass sie nach Block 2/3 vertieft werden kann.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt

#### T-080 — Flag-Erklaerungen ergaenzen: --print in prerequisites und Custom-Plugin-Setup-Zeit in Block 3  `[P3 | S]`

Zwei kleine Erklaerungs-Luecken fuer Neulinge gebuendelt. (1) prerequisites.md Step 3 (Z.74-77, verifiziert) nutzt 'claude --print "Say hello"' zur Auth-Pruefung (auch Checklist Z.161), ohne --print zu erklaeren — vorher wurde nur 'claude' + '/login' gezeigt. Halbsatz ergaenzen: '--print fuehrt einen einmaligen, nicht-interaktiven Prompt aus und beendet sich danach — gut zum Testen.' (2) block-3-advanced.md markiert Custom-Plugins (multi-model-orchestrator, agentic-os, devil-advocate-swarms, inception) mit :wrench:, quantifiziert aber die Setup-Zeit nicht. In Modul 3.1 oder vor dem ersten :wrench:-Plugin: 'Custom plugins (:wrench:) sind nicht Teil von Standard-Claude-Code. Setup-Zeit: ~10-15 Min pro Plugin (clone, install, verify). Fuer Hands-on: Plugins vor Session 3 bereit haben.'

- **Dateien:** resources/prerequisites.md; resources/modules/block-3-advanced.md
- **Begruendung:** Unerklaerte Flags und unquantifizierte Setup-Zeiten summieren sich beim Neuling zu Verunsicherung. Beide Fixes sind Komfort/Klarheit, kein Lernerfolg-Blocker — daher gebuendelt und niedrig priorisiert.
- **Akzeptanz:** prerequisites.md erklaert --print in einem Halbsatz; block-3-advanced.md (Modul 3.1 oder vor dem ersten :wrench:) nennt die Custom-Plugin-Setup-Zeit (~10-15 Min/Plugin) und die Empfehlung, sie vor Session 3 bereitzuhaben.
- **Quelle:** Anna — Embedded-Entwicklerin (NULL Agent-Erfahrung); Currency-Auditor — Ecosystem-Stack

### Cluster: `structure` (9 TODOs)

12 Roh-Befunde aus 5 Personas konsolidiert zu 8 atomaren TODOs. Zwei dominante Themen: (1) Eine widerspruechliche Ueberschrift "The Three Interfaces" mit 5 gelisteten Surfaces in block-1-foundations.md, dreifach von drei Personas gemeldet — hoechste Lernerfolgs-Prioritaet, weil Einstiegshuerden-Personas an dieser Stelle das Vertrauen in das Material verlieren (P0). (2) Fehlende Single-Source-of-Truth ueber die Navigations-/Plan-Dateien: Block-3-Modul-Titel und -Reihenfolge divergieren (README vs SKILL.md vs glossary vs Modul-Datei), Einstiegs-Reihenfolge der Orientierungsdateien widerspricht sich dreifach, und session-plan.md vs dry-run-Timeline sind nicht deckungsgleich (Pausen/Slots). Dazu kommen vier kleinere lokale Konsistenz-Fixes (Demo-1.4-Recovery-Note ohne PR-Schritt, Exercise-2.3-Plugin-Name-Mismatch, Plugin-Reinstall fuer 17-Modul-Realitaet, Session-3-Recovery-Puffer). Verifikation: Header-Widerspruch, Session-3-Timing und Block-3-Titel/Reihenfolge-Drift wurden gegen die echten Dateien gegengeprueft und bestaetigt.

#### T-004 — Ueberschrift 'The Three Interfaces' korrigieren — listet fuenf Surfaces  `[P0 | S]`

In resources/modules/block-1-foundations.md Zeile 22 lautet die Ueberschrift '### The Three Interfaces', darunter folgen aber nummeriert FUENF Eintraege: '1. claude.ai (Web Chat)', '2. Claude Code CLI', '3. Desktop App', '4. IDE Extensions', '5. Web App & iOS App' (Z.24-58). Das Lernziel Z.12 nennt korrekt fuenf Surfaces ('CLI, Desktop App, IDE Extension, Web App, iOS App'). Der Header widerspricht damit sowohl dem direkt darunterstehenden Inhalt als auch dem eigenen Lernziel. Fix: Header auf 'The Five Surfaces' bzw. 'Die fuenf Claude-Code-Oberflaechen' aendern (konsistent mit Lernziel-Wording 'surfaces' Z.12). Reine Redaktion. Optional als Folge-Verbesserung (separates TODO sinnvoll, hier nur Kern-Fix): im ersten Durchgang nur CLI vs. claude.ai-Chat zeigen und die restlichen 3 Surfaces in eine Klappbox/spaetere Sektion auslagern, um Neulinge nicht zu ueberfluten.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Dreifach unabhaengig gemeldet (Anna, Dr. Reuter, plus zweite Anna-Meldung). Zwei Personas berichten konkreten Vertrauensverlust GENAU an dieser Stelle ('wenn schon die Ueberschrift nicht stimmt...' / 'ein Skeptiker stolpert sofort und fragt sich, ob der Rest auch nicht gegengelesen wurde'). Es ist der zweite Header des ersten inhaltlichen Moduls — maximale Einstiegshuerden-Wirkung bei minimalem Fix-Aufwand. Damit klar P0 nach dem Kriterium Lernerfolg/Einstiegshuerde.
- **Akzeptanz:** Header in block-1-foundations.md nennt eine Zahl, die zur Anzahl der darunter gelisteten Surfaces (5) UND zum Lernziel Z.12 passt; keine 'Three'-Nennung mehr im Header der Interface-Sektion.
- **Quelle:** Anna — Embedded-Entwicklerin; Dr. Reuter — skeptischer Principal Engineer

#### T-033 — Block-3-Modul-Titel und -Reihenfolge ueber alle Navigationsdateien vereinheitlichen  `[P1 | M]`

Drei widerspruechliche Titel UND Reihenfolgen fuer Block-3-Module ueber die Navigationsdateien (gegen Dateien verifiziert): README.md Z.90-96 listet 3.2='Multi-Model Pipelines' und 3.5='Full Stack Architecture ... (Capstone)' in numerischer Reihenfolge 3.1..3.7. SKILL.md (skills/workshop/SKILL.md) Z.71-76 listet 3.2='Nested Orchestration' und 3.5='Telegram Bridge, Inception & Worktree Isolation (Capstone)' in NICHT-numerischer Reihenfolge (3.1,3.2,3.3,3.4,3.6,3.7,3.5). glossary.md Z.306 nennt 'Modul: 3.5 — Telegram & Inception'. block-3-advanced.md Z.327 nennt 'Module 3.2: Nested Orchestration & Multi-Model Pipelines'. Fix: Modul-Datei block-3-advanced.md als Single Source of Truth festlegen; README, SKILL.md, glossary.md und commands/workshop.md daran angleichen. Konkret: 3.2 einheitlich 'Nested Orchestration & Multi-Model Pipelines'; 3.5 einheitlich 'Telegram Bridge, Inception & Worktrees'; entscheiden und konsistent kennzeichnen, welches Modul der Capstone ist (README sagt 3.5, das passt zu SKILL.md).

- **Dateien:** README.md; skills/workshop/SKILL.md; resources/glossary.md; resources/modules/block-3-advanced.md; commands/workshop.md
- **Begruendung:** Von Tom (Selbstlerner ohne Moderator) gemeldet und gegen die echten Dateien bestaetigt — README vs SKILL.md weichen sowohl im Titel von 3.2 als auch im Capstone-Titel von 3.5 voneinander ab. Ein Solo-Lerner kann diese Drift nicht selbst aufloesen und weiss nicht, welches der 'wahre' Titel/die wahre Reihenfolge ist. Sachliche Korrektheit + Orientierung, daher P1.
- **Akzeptanz:** 3.2 und 3.5 tragen in README.md, SKILL.md, glossary.md, commands/workshop.md und block-3-advanced.md denselben Titel; genau ein Modul ist eindeutig als Capstone gekennzeichnet; alle Listen verwenden entweder strikt numerische Reihenfolge oder kennzeichnen den Capstone-Sonderplatz explizit (siehe separates TODO zur Overview-Box).
- **Quelle:** Tom — Selbstlerner

#### T-056 — SKILL.md-Overview-Box: nicht-numerische Modul-Reihenfolge (3.6/3.7 vor 3.5) kennzeichnen oder sortieren  `[P2 | S]`

In skills/workshop/SKILL.md zeigt die ASCII-Overview-Box (Z.71-76) die Block-3-Module als 3.1, 3.2, 3.3, 3.4, 3.6, 3.7 und erst danach 3.5 ('Telegram Bridge, Inception & Worktree Isolation (Capstone)'). commands/workshop.md Z.26 listet dagegen streng numerisch '3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7'. Fuer den Solo-Lerner sieht die Box wie ein Tippfehler aus. Fix: entweder strikt numerisch sortieren ODER den Capstone-Charakter von 3.5 explizit in der Box kennzeichnen (z.B. '3.5 (Capstone — am Ende)'), damit klar ist, dass die Nicht-Reihenfolge Absicht ist.

- **Dateien:** skills/workshop/SKILL.md
- **Begruendung:** Von Tom gemeldet, gegen SKILL.md bestaetigt (Box endet tatsaechlich mit 3.5 nach 3.6/3.7). Kleinerer Spezialfall des grossen Reihenfolge-Problems; sinnvoll separat, weil hier eine bewusste Design-Entscheidung (Capstone am Ende) nur kenntlich gemacht werden muss, nicht zwingend umsortiert. Orientierungs-Komfort, daher P2.
- **Akzeptanz:** Die SKILL.md-Overview-Box ist entweder strikt numerisch sortiert oder markiert 3.5 sichtbar als Capstone/Endplatz, sodass die Position nicht als Tippfehler missverstanden wird.
- **Quelle:** Tom — Selbstlerner
- **Abhaengig von:** Block-3-Modul-Titel und -Reihenfolge ueber alle Navigationsdateien vereinheitlichen

#### T-057 — Eine kanonische Einstiegs-Reihenfolge der Orientierungsdateien festlegen und ueberall identisch wiederholen  `[P2 | S]`

Drei Orientierungsdateien empfehlen drei leicht verschiedene Einstiegs-Reihenfolgen: README.md Quick Start (Z.30-32): 'prerequisites.md -> WORKSHOP_EINFUEHRUNG.md -> Block durcharbeiten'. workshop-guide.md Lernpfad (Z.54-58): 'prerequisites.md -> session-plan.md -> block-1'. WORKSHOP_EINFUEHRUNG.md (Z.19-20): 'prerequisites.md -> workshop-guide.md'. Fix: eine einzige kanonische Reihenfolge definieren (Vorschlag: prerequisites -> WORKSHOP_EINFUEHRUNG -> workshop-guide -> session-plan -> Block 1) und in allen drei Dokumenten wortgleich wiederholen.

- **Dateien:** README.md; WORKSHOP_EINFUEHRUNG.md; resources/workshop-guide.md
- **Begruendung:** Von Anna (Einstiegshuerden-Persona) gemeldet. Genau diese Orientierungsdateien liest ein Neuling zuerst; widerspruechliche Wegweiser kosten direkt am Anfang Vertrauen und Zeit. Severity vom Befund 'low', aber Einstiegswirkung relevant — P2.
- **Akzeptanz:** prerequisites.md, WORKSHOP_EINFUEHRUNG.md und workshop-guide.md (sowie README Quick Start) nennen dieselbe kanonische Reihenfolge der Einstiegsdateien.
- **Quelle:** Anna — Embedded-Entwicklerin

#### T-020 — Eine Master-Timeline pro Session als Source of Truth — session-plan.md und Dry-Run angleichen  `[P1 | S]`

session-plan.md und die Dry-Run-Timeline (resources/dry-run-session-2-3-2026-05-21.md) sind nicht deckungsgleich, was den Moderator zwingt, zwei widerspruechliche Ablaeufe im Kopf zu halten. Konkret bestaetigt in session-plan.md: SESSION 2 — Z.48-50: '1:00–1:25 Exercises 2.1+2.2', '1:25–1:35 Pause', '1:35–1:45 Modul 2.3'; der Dry-Run springt laut Befund von '1:00-1:25 Exercises' direkt auf '1:35-1:55 Module/Demo 2.3' (Pause-Zeile fehlt, Modul-2.3-Slot weicht ab: Plan 1:35-1:45 vs Dry-Run 1:35-1:55). SESSION 3 — session-plan.md Z.68-69: '0:50–1:10 Modul 3.3+Demo 3.3', '1:10–1:20 Pause'; im Dry-Run fehlt laut Befund die Pause-Zeile und es wird von '0:50-1:10' direkt auf '1:20-1:35' gesprungen. Fix: session-plan.md als alleinige Master-Timeline definieren; die Dry-Run-Datei referenziert diese statt eine zweite, abweichende Tabelle zu fuehren. Pause-Zeilen in beiden Quellen identisch fuehren.

- **Dateien:** resources/session-plan.md; resources/dry-run-session-2-3-2026-05-21.md
- **Begruendung:** Drei separate Sandra-Befunde (Session-2-Pausenlogik, Session-3-10-Minuten-Luecke, Master-Timeline) beschreiben dasselbe Source-of-Truth-Problem und werden hier konsolidiert. Eine widerspruchsfreie Timeline ist die Grundlage fuer einen reibungslosen Live-Workshop; divergierende Ablaeufe erhoehen das Risiko von Live-Fehlern. P1.
- **Akzeptanz:** Fuer Session 2 und Session 3 existiert genau eine maßgebliche Timeline (in session-plan.md); die Dry-Run-Datei verweist darauf oder fuehrt eine byte-gleiche Tabelle; Pause-Zeilen und Slot-Grenzen stimmen in beiden Quellen ueberein.
- **Quelle:** Sandra — Live-Moderatorin

#### T-034 — Session 3 realistisch planen: Live/Recording/Discussion-Spalte + fester 10-Min-Recovery-Puffer  `[P1 | M]`

Die Session-3-Timeline in session-plan.md (Z.62-74) ist zu eng und zu 100% verplant: '0:40–0:50 Modul 3.2 + Demo 3.2 | Multi-Model Pipelines / Codex Swarm' gibt nur 10 Min fuer Modul-Input PLUS eine Codex-Swarm-Demo, die laut block-3-demos.md Demo 3.2 vier Schritte verlangt (Decompose + N parallele Codex-Agents + Claude-Review). Die Timeline fuellt 0:10-2:20 lueckenlos mit Demos, dann 2:20-3:00 Capstone — kein expliziter Recovery-Puffer, obwohl der Dry-Run (resources/dry-run-session-2-3-2026-05-21.md) Session 3 mit 'YELLOW/GREEN ... too many demos depend on plugins, auth, budget, or external services' und 'Session 3 still has more possible demos than time' bewertet. Fix: (1) Demo 3.2 Codex-Swarm aus dem Live-Pfad nehmen und als vorbereitete Aufzeichnung/Screenshots fahren; (2) session-plan.md Session-3-Tabelle um eine Default-Spalte 'Live/Recording/Discussion' ergaenzen, damit der Moderator nicht live entscheiden muss; (3) einen festen 10-Min-Recovery-Puffer einplanen, indem 3.2/3.4/Telegram explizit als Streich-/Bonus-Kandidaten deklariert werden (Plan-Ziel: '5 sichere Demos + Capstone', wie der Dry-Run empfiehlt). Damit wird auch der dort beschriebene 'Demo bricht'-Fall abgedeckt.

- **Dateien:** resources/session-plan.md; resources/dry-run-session-2-3-2026-05-21.md; resources/demos/block-3-demos.md
- **Begruendung:** Zwei Sandra-Befunde (unrealistisches Timing + fehlender Live-Puffer) konsolidiert. Der Dry-Run hat das Risiko bereits identifiziert, aber der verbindliche Plan bildet die Entlastung noch nicht ab. Ein ueberbuchter Session-3-Plan fuehrt live mit hoher Wahrscheinlichkeit zu Zeitnot/abgebrochenen Demos — direkter Lernerfolgs-Schaden fuer Teilnehmer. P1.
- **Akzeptanz:** Session-3-Tabelle in session-plan.md enthaelt pro Slot eine Default-Angabe Live/Recording/Discussion; Demo 3.2 ist nicht mehr als Pflicht-Live-Demo gefuehrt; ein expliziter Recovery-Puffer bzw. klar markierte Streich-Kandidaten (3.2/3.4/Telegram) sind im verbindlichen Plan eingetragen.
- **Quelle:** Sandra — Live-Moderatorin
- **Abhaengig von:** Eine Master-Timeline pro Session als Source of Truth — session-plan.md und Dry-Run angleichen

#### T-058 — Demo 1.4: gh-PR-Recovery-Note und gh-Checklist-Eintrag mit dem Skript in Einklang bringen  `[P2 | S]`

In resources/demos/block-1-demos.md enden die Demo-1.4-Steps 1-6 bei 'git log' und Worktree; ein PR-Schritt existiert nicht. Trotzdem nennen die Recovery-Notes 'If gh pr create fails (auth): Skip the PR step, demonstrate via git push only' (Z.463) und die Pre-Demo-Checklist Z.17 fuehrt 'gh authenticated if Demo 1.4 includes PR creation'. Der konditionale Halbsatz deutet auf eine entfernte PR-Variante. Fix: entweder einen optionalen PR-Schritt (Step 7, 'Bonus') wieder einbauen ODER die gh-pr-Recovery-Note und den gh-Checklist-Eintrag entfernen. Konsistenz herstellen, damit der Moderator nicht gh-Auth vorbereitet und dann keinen PR-Schritt findet.

- **Dateien:** resources/demos/block-1-demos.md
- **Begruendung:** Von Sandra gemeldet. Verschwendete Vorbereitung (gh-Auth) und Verwirrung im Live-Skript, aber lokal begrenzt und nicht lernerfolgs-blockierend. Komfort/Konsistenz, daher P2.
- **Akzeptanz:** In block-1-demos.md gibt es entweder einen expliziten (Bonus-)PR-Schritt in Demo 1.4, auf den sich Recovery-Note und Checklist beziehen, oder die gh-pr-Recovery-Note und der konditionale gh-Checklist-Eintrag sind entfernt — keine Referenz auf einen nicht existierenden PR-Schritt mehr.
- **Quelle:** Sandra — Live-Moderatorin

#### T-059 — Exercise 2.3: konkreten Plugin-Namen festlegen — Platzhalter und 'agentic-os' nicht mischen  `[P2 | S]`

In resources/exercises/block-2-exercises.md spricht Exercise 2.3 Step 1 (Z.359-360) von 'a workshop-provided plugin' und nutzt durchgehend den Platzhalter <plugin-name> (Z.368, 373, 390, 404). Der Success-Check Z.496 verlangt aber konkret 'You can navigate the agentic-os plugin structure from the command line' — 'agentic-os' taucht in den Anweisungen vorher nirgends auf. Der Teilnehmer weiss nicht, welches Plugin er real erkunden soll. Fix: einen konkreten, garantiert vorhandenen Plugin-Namen festlegen (laut Step-1-Note ist das Workshop-Plugin unter dynamic_workshop/ nutzbar) und Success-Check + alle Steps darauf vereinheitlichen; Platzhalter und konkreten Namen nicht mischen.

- **Dateien:** resources/exercises/block-2-exercises.md
- **Begruendung:** Von Lena (Hands-on QA) Schritt fuer Schritt gefunden. Ein Lerner, der die Uebung wirklich durcharbeitet, bleibt am uneindeutigen Plugin-Namen haengen — direkter Hands-on-Reibungspunkt, aber lokal und ohne globale Folgen. P2.
- **Akzeptanz:** Exercise 2.3 verwendet in Steps und Success-Check denselben, konkret benannten und garantiert vorhandenen Plugin-Namen; kein Mix aus <plugin-name>-Platzhalter und einem hartcodierten 'agentic-os' mehr.
- **Quelle:** Lena — Hands-on QA

#### T-060 — Plugin-Reinstall in die Pre-Flight-Checklist aufnehmen (Laufzeit-Metadaten vs 17-Modul-Repo)  `[P2 | S]`

Der final-gap-sweep (resources/final-gap-sweep...md Z.67) warnt, dass die INSTALLIERTE Plugin-Kopie noch '13 modules' meldet, waehrend Repo und Slides eine 17-Modul-Realitaet abbilden (trainer-notes.md Slide-Index Z.257-283 mappt Session 3 auf Slides 19-29, deck-audit bestaetigt '19-29 Block 3 Advanced'). Wenn der Moderator '/workshop' live zeigt und es '13 modules' sagt, widerspricht das den Slides. Fix: Empfehlung des final-gap-sweep (Z.77) umsetzen — vor Session 3 das lokale dynamic-workshop-Plugin neu installieren/aktualisieren, sodass '/workshop'-Laufzeitausgaben zur aktuellen Modul-Realitaet passen; den Schritt 'Plugin neu installieren/aktualisieren' explizit in die Pre-Flight-/Pre-Demo-Checklist (trainer-notes.md bzw. session-plan.md Materialien) aufnehmen.

- **Dateien:** resources/trainer-notes.md; resources/session-plan.md
- **Begruendung:** Von Sandra gemeldet. Betrifft die Live-Demo-Konsistenz (Laufzeit-Ausgabe widerspricht Slides), aber nur wenn '/workshop' live gezeigt wird; durch einen Checklist-Eintrag vollstaendig entschaerfbar. Komfort/Konsistenz, P2.
- **Akzeptanz:** Die Pre-Flight-/Pre-Demo-Checklist (trainer-notes.md oder session-plan.md) enthaelt einen expliziten Schritt 'dynamic-workshop-Plugin vor Session 3 neu installieren/aktualisieren'; verifizierbar, dass '/workshop' nach Reinstall die aktuelle Modulzahl (17) statt '13 modules' ausgibt.
- **Quelle:** Sandra — Live-Moderatorin

### Cluster: `missing-content` (6 TODOs)

5 missing-content-Befunde von 5 Personas, weitgehend disjunkt — daher 5 atomare TODOs, keine echten Merges (die beiden Markus-Befunde sind thematisch verwandt "PhySec-Domaenentiefe", betreffen aber verschiedene Dateien/Lernziele und bleiben getrennt). Alle Evidenzstellen wurden gegen den realen Repo-Stand verifiziert und stimmen: block-1-foundations.md startet tatsaechlich ab Z.16 mit Konzept-Landschaft statt einem Erfolgserlebnis; access_control.py enthaelt nur generische Web/Backend-Vulns (ADMIN_PASSWORD Z.19 laut Playground-CLAUDE.md bewusst toter Code); block-3-advanced.md Z.572 beschreibt auto als Blackbox ohne Klassifikator-Inputs; cheatsheet.md Z.491 zeigt nur node-Hook ohne Windows-bash/pwsh-Bruecke; Vision/Fable 5 fehlt in Block 3 ganz. Priorisierung nach Einstiegshuerde/Lernerfolg > Korrektheit/Aktualitaet > Komfort: P0 = Sanfter Einstieg (Anna, hoechste Einstiegshuerden-Persona, didaktisch zudem von CLAUDE.md "Demos > Slides" gefordert); P1 = Windows-Hook-Bruecke im Cheatsheet (blockiert Windows-Teilnehmer waehrend der Live-Uebung) und PhySec-Logik-Vuln (Differenzierung Pattern-Scanner vs. Domaenenkompetenz, echte Zielgruppe); P2 = OSDP-Secure-Channel-Story und auto-Mode-Transparenz; P3 = Fable-5-Vision (didaktisch wertvoll, aber zeitlich straff/optional).

#### T-006 — 'Hello, Claude Code' — Erfolgserlebnis-Kapitel an den Anfang von Modul 1.1 setzen  `[P0 | M]`

Modul 1.1 startet ab Zeile 16 sofort mit der kompletten Konzept-Landschaft: 5 Surfaces (Z.22-70), Built-in-Tools-Referenztabelle mit 18 Tools (Z.131-148), 6 Permission Modes, Modell-Tabelle (ab Z.158). Das erste echte 'mach es selbst' steht erst in exercises/block-1-exercises.md (Exercise 1.1). Anfaenger (Persona Anna, NULL Agent-Erfahrung) werden mit Theorie ueberflutet, bevor sie ein einziges Erfolgserlebnis hatten. CLAUDE.md fordert explizit 'Demos > Slides' / 'Demo first, Theorie danach' — genau am Einstiegspunkt fehlt das. TODO: Ein kurzes 'Hello, Claude Code'-Kapitel GANZ an den Anfang von Modul 1.1 setzen (vor 'Overview', Z.16): 3 Befehle (mkdir test-project, claude, ein einfacher Prompt wie 'erstelle mir eine hello.py'), Ergebnis sofort sichtbar. Erst nach diesem Erfolgserlebnis die Surfaces/Tools/Modelle erklaeren. Optional einen Verweis auf die spaetere Vertiefung einbauen ('die Mechanik dahinter erklaeren wir gleich').

- **Dateien:** resources/modules/block-1-foundations.md; agents/workshop-mentor.md
- **Begruendung:** Hoechste Prioritaet nach der Regel Einstiegshuerde/Lernerfolg > alles andere. Die wichtigste Einstiegshuerden-Persona (Anna) verliert sich in der Theorie vor dem ersten Erfolg. Didaktisch zudem direkt vom Projekt-CLAUDE.md gefordert ('Demos > Slides', visueller/praktischer Einstieg).
- **Akzeptanz:** Modul 1.1 beginnt vor dem 'Overview'-Abschnitt mit einem in <10 Minuten durchfuehrbaren Hands-on-Block (3 Befehle, sichtbares Ergebnis). Erst danach folgen Surfaces/Tools/Modelle. agents/workshop-mentor.md ist entsprechend aktualisiert (Regel aus CLAUDE.md: bei Inhaltsaenderung an Modulen Mentor mitziehen).
- **Quelle:** Anna — Embedded-Entwicklerin (15 J. C/Embedded), NULL Agent-Erfahrung. Wichtigste Einstiegshuerden-Persona.

#### T-019 — 'Hooks auf Windows'-Notiz in den Cheatsheet aufnehmen (bash- und pwsh-Form)  `[P1 | S]`

cheatsheet.md zeigt bei den Hooks nur die cross-platform-Form "command": "node security-check.js" (Z.491). Die bash-Script-Hook-Form ("command": "bash script.sh"), die Exercise 2.1 / Demo 2.2 voraussetzen, taucht nirgends auf; im ganzen Cheatsheet gibt es keinen pwsh-/$env:-Eintrag (nur die ps1-Install-Zeile). Ein Windows-11/PowerShell-Teilnehmer, der waehrend der Uebung blockiert ist, sucht genau auf der Referenzkarte — und findet nichts. TODO: Eine kurze 'Hooks auf Windows'-Notiz aufnehmen: (1) bash-Scripts brauchen Git Bash auf PATH; (2) native Alternative "command": "pwsh -File path.ps1"; (3) jq-frei via ConvertFrom-Json. Idealerweise direkt beim Hook-Config-Beispiel (um Z.485-496) platzieren.

- **Dateien:** resources/cheatsheet.md
- **Begruendung:** Konkreter Live-Blocker fuer Windows-Teilnehmer waehrend der Hands-on-Uebung — Einstiegs-/Durchfuehrungshuerde, nicht nur Komfort. Geringer Aufwand, hoher Entsperrungs-Wert. Der Cheatsheet ist die Referenzkarte genau fuer diesen Moment.
- **Akzeptanz:** cheatsheet.md enthaelt einen 'Hooks auf Windows'-Block mit der pwsh -File-Alternative, dem Git-Bash-Hinweis und dem ConvertFrom-Json-statt-jq-Hinweis. Die im Cheatsheet gezeigte Hook-Form ist mit der von Exercise 2.1/Demo 2.2 vorausgesetzten konsistent.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker

#### T-031 — PhySec-Logik-Vuln (fail-open) im Python-Playground ergaenzen — Scanner-vs-Domaenenkompetenz  `[P1 | M]`

Die 3 geplanten Vulns in access_control.py sind klassische Web/Backend-Muster: hardcoded ADMIN_PASSWORD (Z.19, laut workshop-playground/CLAUDE.md sogar bewusst toter Code 'unused in flow'), Path-Traversal in read_log (Z.121-128), Command-Injection in backup_database (Z.134-141). Fuer einen Access-Control-Kontext fehlen die domaenentypischen LOGIK-Fehler, die ein Pattern-Scanner NICHT trivial findet: kein Time-of-Day-/Schedule-Bypass, keine Anti-Passback-/Tamper-Logik. Interessant: load_db (Z.36-45) faellt bei JSON-Fehler/fehlender Datei auf eine leere User-Liste zurueck = fail-SECURE (ACCESS DENIED) — eine schoene PhySec-Diskussion, die aktuell nicht thematisiert wird. TODO: Eine domaenenspezifische Logik-Vuln ergaenzen, die ein Scanner nicht per Pattern findet, z.B. einen fail-OPEN-Pfad (bei korrupter/fehlender users.json ACCESS GRANTED statt DENIED) ODER eine fehlende Schedule/Anti-Passback-Pruefung. Die neue Vuln in workshop-playground/CLAUDE.md unter 'Intentional Vulnerabilities' dokumentieren (Konvention: do NOT fix) und den Bezug zu Exercise 3.3 'For the CySec Engineer' (block-3-exercises.md:165-170) herstellen.

- **Dateien:** workshop-playground/access_control.py; workshop-playground/CLAUDE.md; resources/exercises/block-3-exercises.md
- **Begruendung:** Trifft die echte Zielgruppe (PhySec/Zutrittskontrolle) und macht den Kernlernpunkt von Exercise 3.3 erst real demonstrierbar: Unterschied zwischen Pattern-Scanner und echter Domaenenkompetenz. Korrektheits-/Lernerfolgs-Achse, hoeher als reine Tiefe-Nice-to-haves.
- **Akzeptanz:** access_control.py enthaelt eine zusaetzliche, dokumentierte Domaenen-Logik-Vuln (z.B. fail-open bei korrupter DB oder fehlende Schedule/Anti-Passback-Pruefung), die ein reiner Pattern-Scan nicht trivial findet. workshop-playground/CLAUDE.md listet sie unter 'Intentional Vulnerabilities' (do-NOT-fix-Konvention). Der Bezug zu Exercise 3.3 ist im Exercise-Text hergestellt.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-074 — OSDP-Secure-Channel-Abschnitt (SCBK/Default-Key/Replay/Tamper) in Modul 3.3 / C-Playground ergaenzen  `[P2 | L]`

Modul 3.3 listet generische Checks (Security-Audit-Skill-Tabelle Z.551-561: command/SQL injection, hardcoded creds, ...) und CVE-Beispiele. Der OSDP-C-Playground (osdp_frame_decoder.c) wird in der Domain-Note (Z.537-541) erwaehnt, aber die eigentliche OSDP-Sicherheitsschicht taucht nirgends auf: OSDP Secure Channel (AES-128), das SCBK-0/Default-Key-Problem (viele Installationen laufen mit dem Hersteller-Default-Key), Replay-Schutz, Line-Supervision/Tamper. Genau das ist die Security-Story, die einen PhySec-Entwickler abholt und den Kurs von 'generisch sicher' auf 'kennt OSDP wirklich' hebt. TODO: In Modul 3.3 (idealerweise nahe der Domain-Note Z.537-541) einen kurzen OSDP-Secure-Channel-Abschnitt ergaenzen (1 Absatz Konzept + 1 Vuln-Idee: 'install_mode' bleibt aktiv / Default-SCBK wird nie rotiert). Optional als Demo: Devil's-Advocate-Swarm gegen einen OSDP-Handshake-Stub. Falls eine konkrete Vuln-Idee in den C-Playground wandert, in workshop-playground/CLAUDE.md unter den OSDP-Vulns dokumentieren.

- **Dateien:** resources/modules/block-3-advanced.md; workshop-playground/CLAUDE.md; workshop-playground/osdp_frame_decoder.c
- **Begruendung:** Hebt die fachliche Tiefe/Glaubwuerdigkeit fuer die echte PhySec-Zielgruppe deutlich, ist aber inhaltlich aufwaendiger (Konzept + ggf. Stub/Demo) und nicht einstiegs-blockierend — daher unter den P0/P1-Einstiegs- und Korrektheits-Items.
- **Akzeptanz:** Modul 3.3 enthaelt einen OSDP-Secure-Channel-Abschnitt, der mindestens Secure Channel/AES-128, das SCBK-0/Default-Key-Problem und Replay/Tamper benennt, plus 1 konkrete Vuln-Idee (z.B. install_mode bleibt aktiv / SCBK nie rotiert). Falls eine Vuln im C-Playground landet, ist sie in workshop-playground/CLAUDE.md dokumentiert.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-071 — auto-Mode-Klassifikator entmystifizieren — Klassifikator-Inputs + Cheatsheet-Verweis in Modul 3.3  `[P2 | M]`

block-3-advanced.md Z.572 beschreibt auto als 'the ML-classifier-driven mode where Claude itself decides which actions to auto-approve based on per-action risk'. Fuer ein Publikum, das beruflich Risikoklassifikation betreibt, bleibt voellig offen, WORAUF der Klassifikator entscheidet (Tool-Kategorie? Befehls-Pattern? lokal vs. Netz?). cheatsheet.md nennt 'claude auto-mode defaults' zum Ausdrucken, aber das Modul verweist nicht darauf — auto wirkt dadurch wie Magie statt wie Policy. TODO: Bei der auto-Mode-Beschreibung (um Z.570-579) einen Absatz ergaenzen, der die beobachtbaren Klassifikator-Inputs nennt (z.B. Tool-Kategorie, Befehls-Pattern, lokal vs. Netzwerkzugriff) ODER ehrlich sagt 'undokumentiert, inspizierbar via claude auto-mode defaults', und auf den Cheatsheet-Befehl verweist.

- **Dateien:** resources/modules/block-3-advanced.md; resources/cheatsheet.md
- **Begruendung:** Tiefe/Korrektheit fuer ein anspruchsvolles, skeptisches Publikum (Dr. Reuter). Verhindert, dass auto als 'Magie' statt nachvollziehbarer Policy wahrgenommen wird. Wichtig fuer Glaubwuerdigkeit, aber nicht einstiegs-blockierend.
- **Akzeptanz:** Modul 3.3 nennt bei auto entweder konkrete beobachtbare Klassifikator-Inputs oder erklaert explizit deren Undokumentiertheit + Inspektionsweg, und verweist auf den Cheatsheet-Befehl 'claude auto-mode defaults'.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-087 — Optionales Fable-5-Vision-Unterkapitel/Exercise fuer PhySec-Use-Cases (CCTV/OCR) ergaenzen  `[P3 | M]`

Der Workshop zielt auf Physical Security Engineers, aber Vision/multimodale Faehigkeiten (Fable 5: 'state-of-the-art fuer Vision-Tasks, u.a. Web-Apps aus Screenshots rekonstruieren, numerische Werte aus Diagrammen lesen') werden in Block 3 nicht als eigenes Thema erwaehnt. Fuer die Zielgruppe waeren CCTV-Analyse, Access-Log-Vision-OCR und das Parsen von Zutrittskontroll-Interface-Screenshots oder Raumplan-Visualisierungen sehr relevant. TODO: Ein OPTIONALES Unterkapitel in Modul 3.3 ODER eine neue optionale Exercise 3.7 'Fable 5 for Physical Security Analytics' ergaenzen (Screenshots von Zutrittskontroll-Interfaces parsen, CCTV-Logs/Anzeigen auslesen, Raumplan-Visualisierungen verstehen). Vor dem Schreiben die aktuellen Vision-Faehigkeiten/Modell-Bezeichnung kurz gegen die claude-api-Referenz pruefen (Modell-IDs/Currency).

- **Dateien:** resources/modules/block-3-advanced.md; resources/exercises/block-3-exercises.md; agents/workshop-mentor.md
- **Begruendung:** Didaktisch wertvoll und gut auf die Zielgruppe gemuenzt, aber rein additiv/optional und zeitlich straff (3x ~3h sind schon voll). Komfort-/Erweiterungs-Achse, daher unterste Prioritaet. Currency-relevant: Modell-/Vision-Aussagen vor Aufnahme verifizieren.
- **Akzeptanz:** Block 3 enthaelt entweder ein als optional markiertes Vision-Unterkapitel oder eine optionale Exercise 3.7 mit mindestens einem PhySec-Vision-Use-Case (z.B. Screenshot eines Zutrittskontroll-Interfaces parsen). Die genannten Modell-/Vision-Faehigkeiten sind gegen die aktuelle claude-api-Referenz gegengeprueft. agents/workshop-mentor.md ist bei neuer Exercise mitaktualisiert.
- **Quelle:** Currency-Auditor: CLI, Flags, Commands, Versionen

### Cluster: `windows-compat` (10 TODOs)

21 Roh-Befunde von 7 Personas, dedupliziert auf 10 atomare TODOs. Kernproblem: Der Workshop richtet sich laut prerequisites.md ausdruecklich auch an Windows-Teilnehmer (Default-Shell = PowerShell), aber praktisch ALLE Setup-, Demo- und Exercise-Befehle sind POSIX-only (python3/pip3, mkdir -p, chmod +x, &&, Heredocs, jq, bash-Shebangs, export, /tmp/). Die Windows-Hinweise sind entweder gar nicht vorhanden oder in eine Troubleshooting-Tabelle am Dateiende ausgelagert, die der Lerner erst findet, NACHDEM er gescheitert ist. Drei kritische Blocker fuer die selbststaendige Durchfuehrbarkeit: (1) python3-vs-python schon im Pre-Workshop-Setup -> Teilnehmer scheitern, bevor der Workshop beginnt; (2) die zentrale Pflicht-Hook-Exercise 2.1 und Demo 2.2/2.2b laufen auf reiner Windows-Box nicht (bash/jq/chmod), und das im Recovery referenzierte "pre-prepared secure-diff-gate.sh" existiert nicht einmal im Repo; (3) Widerspruch zwischen Exercises (registrieren `bash ...`) und troubleshooting.md (verlangt `pwsh -File`), den der Solo-Lerner nicht aufloesen kann. Priorisierung folgt Einstiegshuerde > Korrektheit > Komfort: die Blocker im Setup-/Hook-Pfad sind P0/P1, breite POSIX-Snippet-Haertung P2, Konzept-nur-Beispiele und Einzel-Stolpersteine P2/P3.

#### T-005 — python3/pip3 durchgaengig um Windows-Variante (python/pip) im Haupttext ergaenzen  `[P0 | S]`

prerequisites.md nutzt python3/pip3 als kanonische Befehle: Z.103 `python3 --version`, Z.104 `pip3 --version`, Z.147 `pip3 install -r requirements.txt`, Z.150 `python3 -m pytest -v`, Z.163 Checklist `[ ] python3 --version shows 3.9+`. Der Windows-Fix steht erst Z.189 in der Troubleshooting-Tabelle: `Python not found on Windows | Use python instead of python3`. Auf Standard-Windows existiert oft nur `python`, nicht `python3` -> der Teilnehmer scheitert mit `python3: command not found` schon im Pre-Workshop-Setup und findet den Fix am Dateiende moeglicherweise nicht. Fix: direkt bei Step 5, Step 7 und in der Checkliste die Windows-Form danebenstellen, z.B. `python --version  # Windows: python statt python3`. Dieselbe python3-Form auch in README (Z.44/51) pruefen und angleichen. Zusaetzlich klarstellen, dass Python NICHT erst 'fuer Block 2+' noetig ist (Z.97), sondern bereits Block-1-Exercises Python-Code ausfuehren (block-1-exercises.md Z.43 event_log_parser.py, Z.249 validators.py, Z.289 'Run the tests').

- **Dateien:** resources/prerequisites.md; README.md
- **Begruendung:** Hoechste Einstiegshuerde: scheitert VOR Workshop-Beginn beim Self-Setup. Betrifft jeden Windows-Teilnehmer und ist mit minimalem Aufwand behebbar. Vier Personas melden dies unabhaengig.
- **Akzeptanz:** In prerequisites.md stehen bei Step 5, Step 7 und in jeder Checklisten-Zeile sowohl python3/pip3 als auch die Windows-Variante python/pip direkt nebeneinander (nicht nur in der Troubleshooting-Tabelle). Step 5 stellt klar, dass Python bereits ab Block-1-Exercises gebraucht wird. README verwendet keine nackten python3-Befehle ohne Windows-Hinweis mehr.
- **Quelle:** Anna — Embedded-Entwicklerin; Kevin — Windows-11/PowerShell-Praktiker; Tom — Selbstlerner; Lena — Hands-on QA

#### T-007 — Vorbereitetes, Windows-getestetes secure-diff-gate Hook-Asset ins Repo legen (bash + Python-Variante)  `[P0 | M]`

Demo 2.2b (block-2-demos.md Z.200) setzt einen langen Inline-JSON+Bash-Hook mit verschachteltem Quoting (`bash -c 'INPUT=$(cat); FILE=$(echo "$INPUT" | jq -r .file_path ...)'`). Die Recovery-Note Z.246 verweist auf eine vorbereitete `secure-diff-gate.sh` als Fallback — diese Datei existiert NICHT im Repo (workshop-playground/ enthaelt nur CLAUDE.md, Makefile, access_control.py, osdp_frame_decoder.c, test_access_control.py, requirements.txt; kein assets/- oder hooks/-Ordner). Der Dry-Run bestaetigt: 'inline JSON/bash quoting is too risky on Windows'. Fix: ein echtes assets/hooks/-Verzeichnis anlegen (z.B. resources/demos/assets/hooks/) mit (a) secure-diff-gate.sh fuer Git-Bash und (b) einer jq-freien Python-Variante secure-diff-gate.py fuer Windows ohne jq (`python -c`/Datei, liest stdin via json.load). Beide auf Windows-Git-Bash bzw. Windows-python testen. Die Recovery-Note auf die konkreten Pfade verweisen.

- **Dateien:** resources/demos/block-2-demos.md; resources/demos/assets/hooks/secure-diff-gate.sh; resources/demos/assets/hooks/secure-diff-gate.py
- **Begruendung:** Live-Demo-Blocker: Die Moderatorin verlaesst sich auf einen 'pre-prepared' Fallback, der gar nicht existiert. Inline-Quoting bricht laut Dry-Run auf Windows zuverlaessig. Ohne fertige Datei ist 'pre-prepared' nur eine Absichtserklaerung.
- **Akzeptanz:** resources/demos/assets/hooks/ enthaelt eine lauffaehige secure-diff-gate.sh UND eine jq-freie secure-diff-gate.py; beide blocken einen Write auf .env/.pem/secrets/credentials (exit 1) und lassen normale Writes durch (exit 0); beide auf Windows verifiziert. block-2-demos.md Recovery-Note Z.246 verweist auf die realen Pfade statt auf eine nicht-existente Datei.
- **Quelle:** Sandra — Live-Moderatorin; Kevin — Windows-11/PowerShell-Praktiker

#### T-036 — PowerShell-Parallelvariante fuer die zentrale Hook-Exercise 2.1 (safety-check) bereitstellen  `[P1 | L]`

Die Flaggschiff-Hook-Uebung 2.1 (block-2-exercises.md) ist komplett POSIX: Z.167 `#!/bin/bash`, Z.174 `python3 -c "import sys, json; ..."`, Z.206 `chmod +x ~/.claude/hooks/safety-check.sh`, Z.222 Registrierung `"command": "bash ~/.claude/hooks/safety-check.sh"`. Auf reiner Windows-PowerShell existiert `chmod +x` nicht, der `bash`-Aufruf braucht Git Bash auf PATH, und `python3` ist meist `python`. Auch der Bonus-PostToolUse-Hook (audit-log, Z.257-268) nutzt `#!/bin/bash`, `date '+%Y-%m-%d %H:%M:%S'`, `>> ~/.claude/audit.log`, `chmod +x`. Fix: vollstaendige PowerShell-Parallelvariante anbieten — safety-check.ps1 (`$input | Out-String | ConvertFrom-Json`, Pattern-Match via `-match`, `exit 1`), Registrierung `"command": "pwsh -File $HOME/.claude/hooks/safety-check.ps1"`, chmod-Schritt fuer Windows als entfallend kennzeichnen. Bonus audit-log.ps1 analog (`Get-Date -Format 'yyyy-MM-dd HH:mm:ss'`, `Add-Content`).

- **Dateien:** resources/exercises/block-2-exercises.md
- **Begruendung:** Dies ist DIE zentrale Hook-Uebung des Workshops. Ohne Windows-Variante ist Block 2 fuer die Zielgruppe (Windows-Entwickler) nicht selbststaendig durchfuehrbar. Zwei Personas stufen es als kritisch ein.
- **Akzeptanz:** Exercise 2.1 zeigt fuer Skript, chmod-Schritt und settings.json-Registrierung jeweils eine bash- UND eine PowerShell-Variante; die .ps1-Variante parst stdin via ConvertFrom-Json, matched die Gefahren-Patterns und exit 1; der chmod-Schritt ist fuer Windows klar als entfallend markiert; der Bonus audit-log-Hook hat ebenfalls eine PowerShell-Variante.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker

#### T-021 — Widerspruch aufloesen: Exercises registrieren `bash ...`, troubleshooting.md verlangt `pwsh -File`  `[P1 | S]`

exercises/block-2-exercises.md Z.222 registriert den Hook als `"command": "bash ~/.claude/hooks/safety-check.sh"`, waehrend troubleshooting.md Z.48 fuer Windows sagt: 'Auf Windows: PowerShell-Pfad richtig? Skript mit `pwsh -File` aufrufen.' Der Solo-Lerner kann diesen direkten Widerspruch nicht selbst aufloesen und gibt an der ersten roten Fehlermeldung auf. Fix: eine einheitliche Linie ziehen — entweder durchgaengig die `pwsh -File`-Variante in den Exercises ergaenzen (siehe abhaengiges PowerShell-Variante-TODO) ODER in den Exercises explizit auf den Git-Bash-Pfad fuer Windows verweisen. troubleshooting.md und die Exercises muessen dasselbe sagen.

- **Dateien:** resources/exercises/block-2-exercises.md; resources/troubleshooting.md
- **Begruendung:** Sachlicher Widerspruch zwischen zwei Doku-Stellen, den der Solo-Lerner nicht aufloesen kann -> Abbruch. Geringer Aufwand, sobald die Hook-Registrierungslinie festgelegt ist.
- **Akzeptanz:** Exercises und troubleshooting.md beschreiben dieselbe Windows-Hook-Registrierung (entweder beide pwsh -File oder beide Git-Bash-Pfad mit explizitem Hinweis); kein widerspruechlicher Befehl mehr auffindbar.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker
- **Abhaengig von:** PowerShell-Parallelvariante fuer die zentrale Hook-Exercise 2.1 (safety-check) bereitstellen

#### T-035 — Hook-Setup in prerequisites.md PowerShell-tauglich machen (Heredoc/jq/chmod/mkdir -p)  `[P1 | M]`

prerequisites.md Z.279-293 legt den Vorbereitungs-Hook per reinem bash-Heredoc an: `cat > ~/.claude/hooks/security-check.sh << 'EOF'` ... `COMMAND=$(echo "$INPUT" | jq -r '.command // ""')` ... `chmod +x ~/.claude/hooks/security-check.sh`, plus Z.263 `mkdir -p ~/.claude/skills` und Z.278 `mkdir -p ~/.claude/hooks`. In PowerShell sind Heredoc, jq, chmod allesamt nicht verfuegbar; `mkdir -p` kennt PowerShell nicht (braucht `New-Item -ItemType Directory -Force`). Dies ist die Vorbereitung VOR der Session — scheitert sie auf Windows, fehlt die Demo-Voraussetzung. Fix: PowerShell-Block-Variante ergaenzen — Verzeichnisse via `New-Item -ItemType Directory -Force`, Datei via Here-String `@'...'@ | Set-Content`, jq durch `python` (json.load) ersetzen, chmod entfaellt. Pre-Workshop-Pflichtcheck fuer Git Bash + jq (oder Python) aufnehmen, falls die bash-Variante beibehalten wird.

- **Dateien:** resources/prerequisites.md
- **Begruendung:** Pre-Session-Voraussetzung: scheitert das Hook-Setup auf Windows, kann die Hook-Demo am Workshop-Tag nicht laufen. Betrifft alle Windows-Teilnehmer im Vorbereitungsschritt.
- **Akzeptanz:** prerequisites.md zeigt fuer das Anlegen von ~/.claude/hooks und der security-check-Datei eine PowerShell-Variante (New-Item -Force, Here-String, kein jq/chmod) ODER nimmt Git Bash + jq/Python explizit als Pflicht-Voraussetzung mit Check in die Checkliste auf.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker

#### T-022 — Pre-Flight-Checklist der trainer-notes auf Windows-tauglich umstellen  `[P1 | S]`

trainer-notes.md Pre-Flight (Z.29-55) nutzt `python3 -m pytest -v`, `make` und den Pfad `cd ~/cc-workshop/dynamic-workshop`. Auf Windows ist `python3` meist nur `python` (der Dry-Run lief mit `python -m pytest -v: 18 passed`, also python), `make` ist meist nicht installiert ('(if installed)' relativiert es nur), und die `~/`-Pfadannahme greift in cmd nicht. Da der Workshop laut Repo-Kontext auf Windows-Maschinen laeuft, sollte die abhakbare Moderator-Checkliste primaer Windows-tauglich sein, nicht POSIX-first. Fix: Windows-Variante/Spalte ('python' statt 'python3', make-Schritt klar optional, Pfade ohne ~-Annahme bzw. mit Windows-Pfadbeispiel).

- **Dateien:** resources/trainer-notes.md
- **Begruendung:** Die Moderatorin haelt den Workshop live auf einer Windows-Maschine; eine POSIX-first-Pre-Flight-Checkliste fuehrt zu falschen 'Fehlern' kurz vor Start. Geringer Aufwand, hoher Vertrauensgewinn.
- **Akzeptanz:** Pre-Flight-Checklist in trainer-notes.md verwendet python (mit python3 als Alternative), markiert den make-Schritt eindeutig als optional und nutzt keinen ~-Pfad ohne Windows-Aequivalent; abhakbar auf einer reinen Windows-Box.
- **Quelle:** Sandra — Live-Moderatorin

#### T-072 — POSIX-Shell-Snippets in allen Exercise-Dateien Windows-tauglich machen (mkdir -p, &&, chmod, Heredoc, ~/)  `[P2 | M]`

Ueber alle drei Exercise-Dateien hinweg 25+ POSIX-only-Snippets, die auf der Windows-Default-Shell (PowerShell) brechen: `mkdir -p` (block-1 Z.35/120/336, block-2 Z.37/161/418-420), `&&`-Verkettung (funktioniert erst ab PowerShell 7), `chmod +x` (block-2 Z.207), `cat > ... << 'EOF'`-Heredocs (block-2 Z.423-434), `>> ~/.claude/...`, `~/`-Expansion (in cmd gar nicht expandiert). Schon der allererste Schritt der ersten Uebung scheitert: block-1 Z.35 `mkdir -p ~/cc-workshop/exercises/exercise-1.1 && cd ... && claude`. Aktuell gibt es in allen drei Dateien nur EINEN Windows-Hinweis (block-3 Z.374 'On Windows, use Git Bash or WSL'). Fix: einen prominenten Vorspann oben in JEDER Exercise-Datei (und in prerequisites.md) — 'Auf Windows alle Shell-Befehle in Git Bash ausfuehren, nicht in PowerShell/cmd' — UND fuer die Einstiegsuebung 1.1 beide Varianten zeigen (`New-Item -ItemType Directory -Force -Path ...; Set-Location ...`). Niedrige Einzelschwere, aber der erste copy-paste-Schritt scheitert sichtbar genau dort, wo ein Neuling nicht scheitern darf.

- **Dateien:** resources/exercises/block-1-exercises.md; resources/exercises/block-2-exercises.md; resources/exercises/block-3-exercises.md; resources/prerequisites.md
- **Begruendung:** Breite Reibung in jeder Uebung, beginnend mit dem allerersten Schritt. Ein klarer Git-Bash-Vorspann loest 80% mit wenig Aufwand; gehoert nach den harten Blockern, weil Claude Code Verzeichnisse oft selbst anlegt und der Schaden meist 'nur' der erste copy-paste ist.
- **Akzeptanz:** Jede der drei Exercise-Dateien hat ganz oben einen Windows-Hinweis (Git Bash empfohlen, oder PowerShell-Alternative); Exercise 1.1 zeigt den Startbefehl in bash UND PowerShell; spaetere Uebungen verweisen auf diesen Vorspann.
- **Quelle:** Lena — Hands-on QA; Kevin — Windows-11/PowerShell-Praktiker

#### T-061 — MCP-Config-Beispiel auf `python` statt `python3` umstellen  `[P2 | S]`

block-2-ecosystem.md Z.1140 zeigt im .mcp.json-Beispiel `"command": "python3"` (mit `"args": ["my_mcp_server.py"]`). Auf Windows gibt es i.d.R. kein python3.exe -> der MCP-Server startet nicht. Teilnehmer kopieren dieses Snippet 1:1 in ihre eigene .mcp.json, daher direkte Stolperfalle. Fix: auf `"command": "python"` umstellen oder Hinweis `# Windows: "python" statt "python3"` ergaenzen.

- **Dateien:** resources/modules/block-2-ecosystem.md
- **Begruendung:** Copy-paste-Snippet, das auf Windows still fehlschlaegt (MCP-Server startet nicht). Sachliche Korrektheit, kleiner Fix, aber kein Pre-Workshop-Blocker.
- **Akzeptanz:** Das .mcp.json-Beispiel in block-2-ecosystem.md verwendet `python` oder traegt einen expliziten Windows-Hinweis fuer den command-Wert.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker

#### T-073 — export/env-vars und Konzept-nur-bash-Beispiele um PowerShell-Aequivalente ergaenzen  `[P2 | M]`

Mehrere Stellen zeigen Env-Var-Konfiguration und Hook-Konzepte nur in bash, ohne PowerShell-Aequivalent: `export TERM=xterm-256color` (block-1-demos.md Z.591), `export DISABLE_TELEMETRY=1` / `export DISABLE_ERROR_REPORTING=1` (block-3-advanced.md Z.741-742), `set ANTHROPIC_API_KEY environment variable` ohne Syntax (prerequisites.md Z.70). `export` ist kein PowerShell-Cmdlet. Fix: PS-Form danebenstellen — Session `$env:VAR="..."`, persistent `setx VAR "..."`; bei prerequisites.md Z.70 konkret `$env:ANTHROPIC_API_KEY="..."` bzw. `setx ANTHROPIC_API_KEY "..."` zeigen. Ebenfalls in dieses TODO: die Konzept-/Demo-bash-Beispiele (block-2-ecosystem.md Z.594-601 sed/jq -n, Z.628-633, Z.641-652 `case $CLAUDE_EFFORT`; block-3-advanced.md Z.1382/1387 `> /tmp/diff.patch`, Z.1494 `#!/bin/bash`). `/tmp/` existiert auf Windows nicht. Mindestens je einen Hinweissatz ergaenzen: 'Beispiele in bash; auf Windows analog mit PowerShell (`$env:CLAUDE_EFFORT`, `-replace`, `ConvertTo-Json`); fuer Pfade `$env:TEMP` statt /tmp/.' Plus die `echo -e "\033[32m..."`-Checklistenzeile (prerequisites.md Z.165), die in PowerShell `-e` woertlich ausgibt — Windows-Variante mit PowerShell-7-Escape oder [char]27 nennen.

- **Dateien:** resources/prerequisites.md; resources/demos/block-1-demos.md; resources/modules/block-3-advanced.md; resources/modules/block-2-ecosystem.md
- **Begruendung:** Ein Neuling weiss sonst nicht, wie er Env-Vars auf Windows setzt (Z.70 nennt keine Syntax). Konzept-Beispiele sind toleranter, aber ein Windows-Leser kann derzeit keins ausprobieren. Komfort/Korrektheit, kein harter Blocker.
- **Akzeptanz:** Bei prerequisites.md Z.70 steht die konkrete PowerShell- und setx-Syntax fuer ANTHROPIC_API_KEY; jede export-Stelle hat eine PS-Form daneben; die bash-Konzeptbloecke in block-2/block-3 tragen je einen Windows-Hinweissatz; /tmp/-Pfade nennen ein Windows-Aequivalent; die echo -e-Checklistenzeile hat eine Windows-Variante.
- **Quelle:** Kevin — Windows-11/PowerShell-Praktiker

#### T-083 — C-Playground-Build (gcc/clang/scan-build) fuer Windows framen oder als compile-frei kennzeichnen  `[P3 | S]`

workshop-playground/Makefile nutzt Z.3 `CC := gcc`, Z.18-19 `static-check: clang --analyze`, Z.22-23 `scan-build`. workshop-playground/CLAUDE.md gibt nur fuer backup_database einen Windows-Hinweis ('run live demos from Git Bash or WSL'), aber keinen fuer den C-Build/clang/scan-build. Auf einer typischen Windows-Workshop-Maschine sind weder gcc noch clang-analyzer/scan-build per Default vorhanden -> `make static-check` schlaegt fehl. Fix (robuste Variante bevorzugt): die Demo so framen, dass der Devil's-Advocate-Swarm rein auf den C-Quelltext osdp_frame_decoder.c schaut (kein Compile/Static-Check noetig). Alternativ in workshop-playground/CLAUDE.md eine Windows-Voraussetzungsnotiz fuer den C-Pfad ergaenzen (MSYS2/mingw oder WSL, clang-tools-extra).

- **Dateien:** workshop-playground/CLAUDE.md; workshop-playground/Makefile
- **Begruendung:** Betrifft nur den optionalen C-Static-Check-Pfad einer Demo, nicht den Kern-Lernpfad. Niedrigste Prioritaet, aber leicht behebbar durch Reframing oder eine kurze Notiz.
- **Akzeptanz:** workshop-playground/CLAUDE.md adressiert den C-Build-Pfad fuer Windows entweder durch Reframing (Source-only-Review ohne Compile/Static-Check) oder durch eine explizite Windows-Toolchain-Notiz (MSYS2/mingw bzw. WSL + clang-tools-extra).
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler

### Cluster: `exercise-quality` (8 TODOs)

8 Roh-Befunde von 4 Personas (Anna/Embedded-Einsteigerin, Markus/Firmware-CySec, Tom/Selbstlerner, Lena/Hands-on-QA) zur Qualitaet der Hands-on-Uebungen. Zwei dominante Themen: (1) Erwartungshaltungen in Uebungen sind zu absolut formuliert fuer nicht-deterministisches LLM-Verhalten bzw. fuer die tatsaechliche Playground-Logik (1.2 Pushback, 3.3 "confirm three vulns"), was Einsteiger verunsichert oder Widersprueche zur workshop-playground/CLAUDE.md erzeugt. (2) Praktische Stolperfallen fuer Selbst-/QA-Durchlaeufer: unrealistische Zeitbudgets durch Restart-Zyklen (Block 2), das Risiko, settings.json oder den Playground beim Mitmachen zu beschaedigen, und inkonsistente Workdir-Pfade in prerequisites. Dazu zwei Inhaltskorrekturen am Code (Off-by-one-Vuln V4 fachlich unsauber, Log-Injection zu Unrecht als "Bonus" statt PhySec-Kern). Nach Deduplizierung 8 atomare TODOs. Hoechste Prioritaet haben die zwei "destruktiven" Fallen (settings.json-Ueberschreiben P1, Playground-Mutation P1), da sie reale Umgebungen bzw. die Wiederverwendbarkeit der Teaching-Vorlage beschaedigen koennen; danach Erwartungs-/Konsistenz-Schaerfungen und Inhaltskorrekturen.

#### T-030 — Block-2-Uebungen auf Hook-Merge statt komplettem settings.json-Overwrite umstellen  `[P1 | M]`

Exercise 2.2 zeigt zweimal vollstaendige settings.json-Bloecke (Z.213-229 und Z.273-300), 2.6 nochmal einen kompletten PostToolUse-Block (Z.813-829). Ein Neuling, der diese Bloecke nacheinander 1:1 kopiert (2.2 PreToolUse -> 2.6 PostToolUse -> 3.8 Write|Edit), ueberschreibt jeweils die vorigen Hooks, weil jeder Block die ganze hooks-Struktur neu definiert. Auf realen Maschinen kann das eine bestehende ~/.claude/settings.json (mit Permissions etc.) beschaedigen. Der Warnhinweis 'add the hooks section carefully — dont break the JSON structure' (Z.231) reicht nicht. Fix: Merge-orientiertes Vorgehen zeigen ('fuege diesen Eintrag in das bestehende hooks.PreToolUse-Array ein'), Validierung mit `python3 -m json.tool` ergaenzen, und Teilnehmer ausdruecklich auf eine projektlokale .claude/settings.json statt der globalen lenken, damit die echte User-Konfiguration nicht gefaehrdet wird.

- **Dateien:** resources/exercises/block-2-exercises.md
- **Begruendung:** Hoechste Prioritaet, weil hier reale Umgebungen (bestehende ~/.claude/settings.json mit Permissions/Hooks) zerstoert werden koennen — ein irreversibler Schaden ausserhalb des Workshops, nicht nur ein didaktisches Aergernis. Trifft jeden, der die Bloecke seriell kopiert.
- **Akzeptanz:** In 2.2, 2.6 und 3.8 werden Hooks als Merge in bestehende Arrays beschrieben (kein komplettes Overwrite der hooks-Struktur), jeder Block enthaelt einen JSON-Validierungsschritt (`python3 -m json.tool`), und es ist explizit auf projektlokale .claude/settings.json statt globaler Datei verwiesen.
- **Quelle:** Lena — Hands-on QA

#### T-018 — Exercise 3.3 Step 4: Playground-Vuln-Fix nur lokal/uncommitted anwenden und danach verwerfen  `[P1 | S]`

3.3 Step 4 (Z.142-148) verlangt 'Choose one ... and let Claude implement the fix in access_control.py' + danach `pytest -v` gruen. Gleichzeitig instruiert workshop-playground/CLAUDE.md (Z.68 Python, ebenso OSDP): 'Do NOT fix them in this playground — they are the teaching target.' Ein QA-Teilnehmer, der den Fix wie verlangt anwendet und committet, mutiert die geplante Teaching-Vorlage; beim naechsten Durchlauf fehlt die Vuln. Fix: In 3.3 explizit sagen, dass der Fix nur lokal/uncommitted angewendet und danach verworfen wird (`git checkout access_control.py`) ODER in einer Kopie gearbeitet wird. Die CLAUDE.md-Regel und die Uebung damit in Einklang bringen.

- **Dateien:** resources/exercises/block-3-exercises.md; workshop-playground/CLAUDE.md
- **Begruendung:** Direkter Widerspruch zwischen Uebung und Playground-Regel, der die Wiederverwendbarkeit der Teaching-Vorlage ueber Workshops hinweg gefaehrdet. Gewissenhafte Teilnehmer (genau die Zielpersona) wuerden dem expliziteren Step folgen und committen.
- **Akzeptanz:** 3.3 Step 4 enthaelt eine ausdrueckliche Anweisung, den Fix nicht zu committen (z.B. `git checkout access_control.py` am Ende oder Arbeit in einer Kopie), und der Konflikt zur workshop-playground/CLAUDE.md 'Do NOT fix'-Regel ist aufgeloest (kein widerspruechlicher Wortlaut mehr).
- **Quelle:** Lena — Hands-on QA

#### T-053 — Exercise 1.2 Step 6: Pushback-Erwartung von absolut ('It should') auf wahrscheinlichkeitsbasiert entschaerfen  `[P2 | S]`

Exercise 1.2 Step 6 (Z.170-177) sagt zu 'Modify the legacy panel interface module': 'Does Claude push back? It should flag that the CLAUDE.md says not to touch it.' LLM-Verhalten ist nicht deterministisch — der Pushback kann ausbleiben, obwohl die CLAUDE.md-Regel korrekt ist. Auch der Success-Check Z.195 formuliert 'Claude pushes back' als Haken. Fix: Erwartung entschaerfen, z.B. 'Claude sollte in der Regel darauf hinweisen ... falls nicht, ist das ein gutes Lehrbeispiel, dass CLAUDE.md-Regeln Leitplanken sind, keine harten Sperren — Hooks (Block 2.2) sind das harte Gate.' Der Hint Z.202 deutet das an, aber Step 6 und der Success-Check formulieren es zu absolut. So denkt ein Neuling bei ausbleibendem Pushback nicht, er habe etwas falsch gemacht.

- **Dateien:** resources/exercises/block-1-exercises.md
- **Begruendung:** Lernerfolg/Einstiegshuerde: Ein Einsteiger ohne Agent-Erfahrung deutet ausbleibenden (nicht-deterministischen) Pushback als eigenen Fehler statt als Lehrmoment — verunsichert genau die wichtigste Einstiegspersona. Verknuepft zudem sauber mit dem Hooks-Konzept aus Block 2.
- **Akzeptanz:** Step 6 und der Success-Check in 1.2 formulieren den Pushback nicht mehr als garantiert ('It should'/Haken), sondern als wahrscheinliches Verhalten mit explizitem Lehrmoment fuer den Ausbleib-Fall (Leitplanke vs. hartes Hook-Gate).
- **Quelle:** Anna — Embedded-Entwicklerin

#### T-069 — Exercise 3.3 'confirm three vulns'-Erwartung an Playground-Realitaet (ADMIN_PASSWORD toter Code) anpassen  `[P2 | M]`

block-3-exercises.md (Z.108-113, Z.138) verspricht 'The swarm should confirm the three planted issues (Command Injection, Hardcoded Credential, Path Traversal)'. Laut workshop-playground/CLAUDE.md ist ADMIN_PASSWORD jedoch 'unused in flow (intentional for demo discoverability)'. In der Debate-Stufe ist genau das ein valides Defender-Argument ('nie verwendet, nicht erreichbar -> kein exploitierbarer Pfad'), wodurch die Consensus-Stufe es als FALSE POSITIVE / NEEDS-INVESTIGATION statt CONFIRMED einstufen kann — entgegen der Exercise-Erwartung. Zwei Optionen: (a) ADMIN_PASSWORD tatsaechlich in einen unsicheren Auth-Pfad einbinden (z.B. 'admin'-Subcommand, der dagegen vergleicht), oder (b) die Erwartung praezisieren: 'Hardcoded Credential wird gefunden, kann aber im Debate als low-severity/unreachable enden — diskutiert warum.' Option (b) ist didaktisch sogar wertvoller, untergraebt aber die jetzige 'confirm three'-Formulierung.

- **Dateien:** resources/exercises/block-3-exercises.md; workshop-playground/access_control.py; workshop-playground/CLAUDE.md
- **Begruendung:** Sachliche Korrektheit + Lernerfolg: Wenn der Swarm das Hardcoded Credential begruendet abweist, widerspricht das Ergebnis der Uebungs-Erwartung und verwirrt — dabei ist die 'unreachable'-Diskussion der eigentliche Lerngewinn. Effort M, falls Option (a) (Code-Anbindung) gewaehlt wird; bei Option (b) waere es S.
- **Akzeptanz:** Entweder ist ADMIN_PASSWORD in einen erreichbaren (unsicheren) Auth-Pfad eingebunden und der Swarm bestaetigt es konsistent, ODER 3.3 erwartet nicht mehr starr 'confirm three', sondern thematisiert ausdruecklich, dass das Credential als unreachable/low-severity enden kann (mit Diskussionsauftrag). workshop-playground/CLAUDE.md ist konsistent zur gewaehlten Variante.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler

#### T-070 — Off-by-one-Vuln V4 in osdp_frame_decoder.c fachlich plausibel umbauen (CRC-Position statt konstruiertem raw[5])  `[P2 | M]`

In parse_address() (Z.72-81) sagt der Kommentar 'address is decoded from raw[2]', aber die Funktion liest `return raw[OSDP_HEADER_LEN]` (=raw[5]), nicht raw[2]. Der Guard `if (raw_len < OSDP_HEADER_LEN)` (Kommentar 'should be raw_len <= OSDP_HEADER_LEN') laesst bei raw_len==5 den Zugriff raw[5] zu -> OOB-Read. Der Bug ist real, aber die fachliche Erzaehlung passt nicht: Die Funktion soll laut Header die ADDRESS (bei raw[2]) liefern, raw[5] ist gar nicht das Adressfeld. Fix: parse_address() so umbauen, dass die OOB-Stelle plausibel ist — z.B. CRC am Frame-Ende lesen wollen (`return raw[frame_len]` statt `raw[frame_len-1]`). Dann ist das Off-by-one eine echte, nachvollziehbare OSDP-Parsing-Falle (CRC-Position) statt eines konstruierten raw[5]-Zugriffs. Achtung: workshop-playground/CLAUDE.md (Tabelle, 'parse_address ~line 135', 'Reads past end of input buffer') ggf. mit-aktualisieren.

- **Dateien:** workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md
- **Begruendung:** Sachliche Korrektheit gegenueber der CySec-affinen Zielgruppe (Markus): Ein konstruiertes Off-by-one, dessen Narrativ nicht zum Code passt, untergraebt die Glaubwuerdigkeit des Domaenen-Playgrounds. Eine CRC-Positions-Falle ist eine echte OSDP-Parsing-Falle und damit lehrreicher.
- **Akzeptanz:** parse_address() enthaelt ein Off-by-one, dessen Code-Logik mit dem begleitenden Kommentar uebereinstimmt (z.B. CRC-am-Frame-Ende statt raw[5]-Adresszugriff); der OOB-Read bleibt real und durch den Guard ausloesbar; workshop-playground/CLAUDE.md beschreibt die Stelle konsistent.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler

#### T-081 — Log-Injection in access_control.py vom 'Bonus' zur regulaeren PhySec-Vuln aufwerten (EN-50131-Audit-Trail)  `[P3 | S]`

log_event() (access_control.py:105-113) schreibt 'username' und 'action' ungefiltert ins Logfile (f-string mit abschliessendem Newline -> Newline-Injection / Log-Forging). workshop-playground/CLAUDE.md und block-3-exercises.md:113 framen das als 'bonus ungeplante issue' / 'Treat that as a bonus'. Im EN-50131/50132-Kontext ist Audit-Trail-Integritaet aber regulatorisch zentral — Log-Forging ist hier kein Nebenschauplatz. Fix: Log-Injection vom 'Bonus' zur regulaeren, namentlich PhySec-relevanten Vuln aufwerten und mit der EN-50131-Audit-Trail-Anforderung verknuepfen (Querverweis auf die Compliance-Tabelle in block-3-advanced.md:755). So wird aus einem generischen OWASP-Befund eine domaenenrelevante Compliance-Geschichte.

- **Dateien:** workshop-playground/access_control.py; workshop-playground/CLAUDE.md; resources/exercises/block-3-exercises.md; resources/modules/block-3-advanced.md
- **Begruendung:** Aktualitaet/Domaenenrelevanz, kein Blocker: Der Befund ist bereits enthalten, nur falsch gewichtet. Aufwertung macht den Workshop fuer die PhySec-Zielgruppe relevanter (Audit-Trail-Integritaet = regulatorischer Kern), ist aber didaktisch nicht blockierend.
- **Akzeptanz:** Log-Injection wird in workshop-playground/CLAUDE.md und block-3-exercises.md nicht mehr als 'Bonus/ungeplant' bezeichnet, sondern als regulaere PhySec-Vuln gefuehrt, mit explizitem Querverweis auf die EN-50131-Audit-Trail-Anforderung in der Compliance-Tabelle (block-3-advanced.md).
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler

#### T-054 — Workdir-Pfad-Inkonsistenz in prerequisites.md beheben (Clone-Pfad vs. dokumentierter Playground-Pfad)  `[P2 | S]`

Exercise 1.1 (Z.35) nutzt `mkdir -p ~/cc-workshop/exercises/exercise-1.1`. prerequisites.md (Z.380-385) definiert die Struktur ~/cc-workshop/{demos,exercises,workshop-playground}. Aber prerequisites.md (Z.141-142) klont das Repo nach ~/cc-workshop/dynamic-workshop, sodass der Playground real unter ~/cc-workshop/dynamic-workshop/workshop-playground liegt — NICHT unter dem in Z.384 versprochenen ~/cc-workshop/workshop-playground. Ein Solo-Lerner findet den Playground am dokumentierten Ort nicht. Fix: Workdir-Konvention (Z.378-385) mit dem tatsaechlichen Clone-Pfad (Z.141-142) in Einklang bringen — entweder das Repo direkt nach ~/cc-workshop klonen oder den Struktur-Baum so anpassen, dass workshop-playground unter dynamic-workshop/ gezeigt wird.

- **Dateien:** resources/prerequisites.md; resources/exercises/block-1-exercises.md
- **Begruendung:** Lernerfolg/Einstiegshuerde speziell fuer den Selbstlerner ohne Moderator (Tom): Ein dokumentierter, aber falscher Pfad blockiert das eigenstaendige Auffinden des Playgrounds — genau dort, wo niemand zum Nachfragen da ist.
- **Akzeptanz:** Der in prerequisites.md (Struktur-Baum Z.378-385) dokumentierte Playground-Pfad stimmt mit dem tatsaechlichen Clone-Ergebnis (Z.141-142) ueberein; ein Solo-Lerner findet workshop-playground am dokumentierten Ort.
- **Quelle:** Tom — Selbstlerner

#### T-082 — Block-2-Zeitbudgets realistisch anheben und npx-MCP-Erstinstall in prerequisites vorziehen  `[P3 | S]`

Block-2-Header nennt '25-30 minutes' pro Uebung (Z.2). Real verlangt 2.1 einen Skill-Edit + Restart-Test (Z.114), 2.2 'Restart Claude Code (hooks are read at startup)' (Z.235) plus Bonus-Hook, 2.4 npx-Install + .mcp.json + 'Restart Claude Code' (Z.567) + 6 Schritte + Bonus. Jeder Neustart kostet einen Neulaeufer real 1-3 Min Orientierung, dazu der npx-Erstdownload bei 2.4. 5 Hauptuebungen a realistisch 30-40 Min sprengen die ~3h-Session inkl. Teaching. Fix: Zeitschaetzungen ehrlich auf 30-40 Min anheben ODER pro Uebung 'Kern (Pflicht)' vs 'Bonus (optional)' klarer trennen (wie Block 3 mit Must/Should/Nice). Zusaetzlich npx-@playwright/mcp-Erstinstall in prerequisites vorziehen, damit 2.4 in der Session nicht am Download haengt.

- **Dateien:** resources/exercises/block-2-exercises.md; resources/prerequisites.md; resources/session-plan.md
- **Begruendung:** Komfort/Erwartungsmanagement: Unrealistische Zeitangaben fuehren zu Stress/Zeitnot, sind aber nicht blockierend. Das Vorziehen des MCP-Downloads in prerequisites verhindert Live-Haenger in Session 2 und verbessert den Flow spuerbar.
- **Akzeptanz:** Block-2-Zeitangaben sind auf realistische 30-40 Min angehoben ODER pro Uebung in Kern/Bonus getrennt; der npx-@playwright/mcp-Erstinstall ist in prerequisites.md als Vorab-Schritt aufgefuehrt, sodass 2.4 keinen Live-Download mehr ausloest.
- **Quelle:** Lena — Hands-on QA

### Cluster: `accuracy-overclaim` (14 TODOs)

19 Roh-Befunde aus 7 Personas zur Kategorie "accuracy-overclaim", konsolidiert auf 14 atomare TODOs. Hauptthemen: (1) Der C-Playground (osdp_frame_decoder.c) enthaelt drei domaenenfachliche Fehler, die echte PhySec-Entwickler sofort als nicht-domaenenkundig entlarven wuerden (falsches OSDP-Frame-Format, falsche Zeilenangaben, eine in sich widerspruechliche "Integer-Overflow"-Demo) — hoechste Lernerfolg/Vertrauens-Prioritaet, da die Zielgruppe genau hier hinschaut. (2) Mehrere DIREKTE Selbstwidersprueche zwischen Modulen/Cheatsheet/FAQ/Glossar, die ein Teilnehmer beim Quervergleich findet: worktree.baseRef-Default (head vs fresh), acceptEdits-Beschreibung (sicherheitsrelevant: rm wird auto-approved), context:fork/agent-vs-model-Frontmatter, Bundled-Skills-Liste, Sandbox-Windows-Ton, Hook-Event-Zahl, Kosten-Multiplikatoren. (3) Veraltete Versionsangaben (Opus 4.6 statt 4.8) und unbelegte Hyper-Praezision bei Versions-Gates. (4) FAQ-Verkuerzungen, die Trade-offs/Eskalationsstufen unterschlagen (ZDR-Feature-Verlust, Haiku-Eskalation). (5) Custom-Komponenten (notebooklm-Skill) und manuelles Plugin-cache-Schreiben, die nicht sauber vom offiziellen Modell getrennt sind. (6) Live-Demo-Risiko: zitierte /debug-Trace-Zeilen sind nicht gegen das echte Binary verifiziert. Priorisierung folgt Lernerfolg/Einstiegshuerde > Korrektheit/Aktualitaet > Komfort: die OSDP-Domaenenfehler (P0/P1) und direkten Widersprueche (P1) zuerst, kosmetische Inkonsistenzen (P3) zuletzt.

#### T-008 — OSDP-Frame-Format im C-Playground sachlich korrigieren (ADDR vor LEN, 16-bit LEN, CRC-16/CCITT)  `[P1 | S]`

In workshop-playground/osdp_frame_decoder.c ist das OSDP-Frame-Format falsch dargestellt. Zeile 5 behauptet 'Frame format: [SOM][LEN][ADDR][CMD][DATA...][CRC]' und der struct (Z.25-32) hat 'uint8_t length;' (Z.27, 8-bit) VOR 'uint8_t address;' (Z.28). Reales OSDP (SIA OSDP v2.2 / IEC 60839-11-5): Frame = SOM(0x53), ADDR, LEN_LSB, LEN_MSB (Length ist 16-bit little-endian), Message-Control-Info, dann Daten, dann CRC-16/CCITT. Reihenfolge ADDR-vor-LEN und 16-bit-LEN sind festgelegt. Die Zielgruppe sind Zutrittskontroll-Firmware-Entwickler, die das in Sekunden erkennen. Fix: Entweder das Frame-Format real korrigieren (ADDR vor LEN, LEN als 2 Bytes LSB/MSB), ODER mindestens einen ehrlichen Disclaimer-Kommentar ergaenzen wie: 'Simplified/teaching frame — real OSDP uses ADDR before a 16-bit little-endian LEN and a CRC-16/CCITT; see SIA OSDP v2.2'. Der Disclaimer ist der pragmatische Minimal-Fix, falls die Trigger-Logik im main() nicht umgebaut werden soll.

- **Dateien:** workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md
- **Begruendung:** Die echte Zielgruppe (PhySec-Firmware-Entwickler) prueft genau diese Domaenendetails. Ein falsches Frame-Format entlarvt den gesamten Playground als nicht-domaenenkundig und zieht das Vertrauen in den Rest des Workshops mit. Hoher Vertrauens-/Glaubwuerdigkeitshebel bei kleinem Aufwand.
- **Akzeptanz:** osdp_frame_decoder.c enthaelt entweder ein korrektes OSDP-Frame-Layout (ADDR vor 16-bit-LEN, CRC-16/CCITT erwaehnt) ODER einen expliziten Disclaimer-Kommentar im Datei-Header, der die Vereinfachung kennzeichnet und auf SIA OSDP v2.2 verweist. Zeile 5 widerspricht nicht mehr unkommentiert dem realen Standard.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-062 — V2-'Integer Overflow' im C-Playground entwiderspruechlichen (echter Overflow ODER ehrliche Umbenennung)  `[P2 | M]`

In workshop-playground/osdp_frame_decoder.c ist die als 'VULNERABILITY 2: Integer Overflow' deklarierte Demo (compute_crc(), Z.46-59) in sich widerspruechlich. Der Kommentar Z.48 sagt selbst: 'If length == 255, byte_count == 255*3 == 765 (fine)' — gibt also zu, dass NICHTS ueberlaeuft ('fine'), und schiebt den eigentlichen Bug auf V1 ab (Z.49-50: 'accesses frame->data[i] - already overflowed (see V1)'). Das ist keine saubere Integer-Overflow-Demo, sondern ein OOB-Read, der auf V1 beruht. Ein CySec-Teilnehmer nutzt diesen Selbstwiderspruch im Devil's-Advocate-Debate sofort als Defender-Argument. Fix: Entweder V2 zu einem ECHTEN Integer-Overflow umbauen (z.B. uint8_t-Arithmetik mit Wrap-around, etwa 'frame->length + offset' in uint8_t gerechnet), ODER ehrlich umbenennen, z.B. 'Unchecked length feeds OOB read' statt 'Integer Overflow', inkl. angepasstem Kommentar in CLAUDE.md (Tabelle Z. unter 'OSDP Frame Decoder', Eintrag #2).

- **Dateien:** workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md
- **Begruendung:** Der Selbstwiderspruch ('fine' + 'Integer Overflow') untergraebt die Security-Demo (Block 3.3 Devil's Advocate Swarm) didaktisch — die Demo soll Schwachstellen sauber illustrieren, nicht selbst angreifbar sein. Mittlere Prioritaet, weil weniger sofort sichtbar als das Frame-Format, aber zentral fuer die Glaubwuerdigkeit der Swarm-Demo.
- **Akzeptanz:** VULNERABILITY 2 ist entweder ein verifizierbar echter Integer-Overflow (mit nachvollziehbarem Wrap-around) ODER praezise als das benannt, was sie ist (z.B. 'unchecked length feeds OOB read'). Der Kommentar enthaelt keine 'fine'-Aussage mehr, die der Vulnerability-Bezeichnung widerspricht. CLAUDE.md-Tabelleneintrag #2 ist konsistent zur neuen Benennung.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-037 — Falsche Zeilenangaben der Vulnerabilities im C-Playground korrigieren oder entfernen  `[P2 | S]`

In workshop-playground/osdp_frame_decoder.c stimmen die Zeilenangaben im Header nicht mit dem Code ueberein. Header Z.8-11 verspricht 'Buffer Overflow ... line ~50', 'Integer Overflow ... line ~85', 'Format String ... line ~110', '(Bonus) Off-by-one ... line ~135'. Tatsaechlich liegen sie auf Z.40-44 (decode_data_payload), Z.52-59 (compute_crc), Z.65-70 (log_frame), Z.76-81 (parse_address). Dieselbe Drift steckt in workshop-playground/CLAUDE.md (Tabelle 'OSDP Frame Decoder', die '~line 50/85/110/135' wiederholt). Fix: Zeilenangaben an den realen Code anpassen ODER ganz weglassen (robuster gegen kuenftige Edits — Funktionsnamen statt Zeilen referenzieren).

- **Dateien:** workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md
- **Begruendung:** Falsche Zeilenangaben sind eine kleine, aber konkret nachpruefbare Ungenauigkeit, die ein aufmerksamer Teilnehmer beim Nachschlagen sofort bemerkt. Weglassen statt korrigieren reduziert kuenftige Drift. Geringe Einstiegshuerde, hohe Sichtbarkeit.
- **Akzeptanz:** Die im Header und in CLAUDE.md genannten Fundstellen verweisen entweder auf die korrekten Zeilen ODER referenzieren nur noch die Funktionsnamen ohne Zeilennummer. Kein '~line 50/85/110/135' mehr, das auf leere/falsche Stellen zeigt.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-009 — Direkten Default-Widerspruch worktree.baseRef (head vs fresh) zwischen Block 1, Block 3 und Cheatsheet aufloesen  `[P1 | S]`

Zwei Module behaupten gegensaetzliche Defaults fuer dieselbe Einstellung. block-1-foundations.md Z.865-866: "`worktree.baseRef: \"head\"` (default) — branch from local HEAD, including unpushed work". block-3-advanced.md Z.1086-1087: "| **`fresh`** (default) | Branches from `origin/<default>` ...". cheatsheet.md Z.428 nennt keinen Default, listet aber beide. Fix: Den tatsaechlichen Default verifizieren (offizielle Doku / echtes settings.json-Verhalten) und alle drei Stellen angleichen. Bis zur Verifikation lieber 'Default variiert je Version, explizit setzen' schreiben als eine falsche Behauptung stehen zu lassen.

- **Dateien:** resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md
- **Begruendung:** Ein Teilnehmer, der worktree.baseRef konfiguriert, baut auf einer falschen Annahme auf (lokaler HEAD vs origin) — das hat reale Konsequenzen fuer welcher Code im Worktree landet. Direkter, im Repo selbst nachweisbarer Widerspruch zwischen zwei Modulen ist ein klassischer Glaubwuerdigkeits-Killer beim Quervergleich.
- **Akzeptanz:** Alle drei Dateien nennen denselben Default fuer worktree.baseRef (verifiziert gegen Doku) ODER alle drei sagen einheitlich, dass der Default versionsabhaengig ist und explizit gesetzt werden soll. Kein widerspruechliches 'head (default)' vs 'fresh (default)' mehr.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-010 — acceptEdits-Beschreibung in Block 1 sicherheitsrelevant nachschaerfen (FS-Bash wie rm/mv wird auto-approved)  `[P1 | S]`

block-1-foundations.md Z.188 (Tabelle) sagt: "acceptEdits | Reads + file edits allowed, bash still asks". block-3-advanced.md Z.582-583 korrigiert das selbst: "The Block 1 table summarizes acceptEdits as 'reads + file edits allowed, bash still asks.' That is the conservative version of the truth. In current Claude Code releases, acceptEdits also auto-approves the common filesystem Bash commands ... (mkdir, touch, rm, mv ...)". Sicherheitsrelevant: Ein Teilnehmer, der nur Block 1 liest, glaubt 'rm' werde unter acceptEdits abgefragt — tatsaechlich wird es auto-approved. cheatsheet.md Z.356 hat die korrekte Langform bereits. Fix: In Block 1 Z.188 eine Fussnote/Klammer ergaenzen, z.B. '(vereinfacht; auto-approved auch FS-Bash wie rm/mv im Workdir — Detail in Modul 3.3)'.

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Sicherheitsrelevante Untertreibung: Ein Teilnehmer koennte acceptEdits im Vertrauen darauf aktivieren, dass destruktive Bash-Kommandos abgefragt werden — und dann ueberrascht ein 'rm' auto-approved bekommen. Block 1 ist der Einstieg, viele lesen nur ihn. Hoher Schutz-/Lernerfolgshebel bei minimalem Aufwand.
- **Akzeptanz:** block-1-foundations.md Z.188 enthaelt einen Hinweis, dass acceptEdits auch gaengige Filesystem-Bash-Kommandos (rm/mv/mkdir/touch) im Workdir auto-approved, mit Verweis auf Modul 3.3. Die Aussage widerspricht nicht mehr unkommentiert dem Cheatsheet und Block 3.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-023 — Frontmatter-Feldnamen-Drift klaeren: context:fork und Subagent-Modellwahl (agent vs model)  `[P1 | M]`

block-2-ecosystem.md Z.352-354 nutzt die Felder 'context: fork' und 'agent: sonnet'. Die offizielle Schema-Tabelle DESSELBEN Moduls (Z.88-97) listet diese Felder NICHT (dort nur model/effort/paths/shell/hooks/arguments). cheatsheet.md Z.519-521 fuehrt 'context: fork', 'agent: haiku' UND 'model: haiku|sonnet|opus' parallel — also zwei Felder (agent + model) fuer scheinbar denselben Zweck (Modellwahl des Forked-Context). Unklar, ob 'agent' und 'model' beide gueltig sind oder eines veraltet ist, und ob 'context: fork' offiziell ist. Fix: Verifizieren, welches Feld die Subagent-Modellwahl steuert (model vs agent) und ob context:fork offiziell ist; danach Modul-Schema-Tabelle, Beispiel und Cheatsheet vereinheitlichen.

- **Dateien:** resources/modules/block-2-ecosystem.md; resources/cheatsheet.md
- **Begruendung:** Erfahrene Entwickler, die selbst Skills schreiben wollen, sind die Zielgruppe — widerspruechliche/undokumentierte Frontmatter-Felder fuehren zu stillem Ladeverhalten (Skill laedt nicht wie erwartet, ohne Fehler). Echtes Stolperfeld mit Auswirkung auf eigene Arbeit der Teilnehmer.
- **Akzeptanz:** Es ist eindeutig dokumentiert, welches Feld die Subagent-Modellwahl steuert (genau eines von agent/model, oder klar beide mit definierter Semantik) und ob context:fork offiziell ist. Die Schema-Tabelle in block-2 (Z.88-97), das Beispiel (Z.352-354) und cheatsheet.md (Z.519-521) verwenden konsistente Feldnamen.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-011 — Veraltete Modellversion 'Opus 4.6' auf 'Opus 4.8' aktualisieren (Block 1, Cheatsheet, Glossar)  `[P1 | S]`

Opus 4.6 wird mehrfach als aktuell/parallel-verfuegbar dargestellt, ist aber seit Mai 2026 durch Opus 4.8 verdraengt (Changelog: 'Claude Opus 4.8 ... Released as the primary model in version 2.1.154, May 28 2026'). Betroffene Stellen: block-1-foundations.md:190 ('auto | ML classifier decides risk level (Max-Plan with Opus 4.7, plus Team/Enterprise)'), cheatsheet.md:364 ('Team/Enterprise (Sonnet 4.6, Opus 4.6, Opus 4.7)'), glossary.md:159. Fix: Alle 'Opus 4.6'-Referenzen auf 'Opus 4.8' korrigieren (bzw. als historisch kennzeichnen, falls bewusst rueckblickend). Empfohlene Zielformulierung laut Roh-Befund: '...Sonnet 4.6, Opus 4.8 (default), Fable 5 (enterprise)'. Vor dem Edit gegen den aktuellen Changelog/Modell-Lineup verifizieren (z.B. via claude-api-Skill), nicht blind das Zitat uebernehmen.

- **Dateien:** resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/glossary.md
- **Begruendung:** Falsche aktuelle Modellnamen sind die sichtbarste Form von Veraltung — Teilnehmer merken im eigenen /model-Menue sofort, dass es kein 'Opus 4.6' (mehr) gibt. Aktualitaet ist fuer einen Tool-Workshop ein Kernversprechen.
- **Akzeptanz:** Keine 'Opus 4.6'-Referenz mehr in den drei Dateien, soweit sie aktuelle Verfuegbarkeit suggeriert; ersetzt durch das gegen den Changelog verifizierte aktuelle Lineup (z.B. Opus 4.8 als primaeres Modell). Rein historische Erwaehnungen sind als solche gekennzeichnet.
- **Quelle:** Currency-Auditor: CLI, Flags, Commands, Versionen

#### T-024 — Live-Demo 3.7: zitierte /debug-Trace-Ausgaben gegen das echte Binary verifizieren oder als sinngemaess kennzeichnen  `[P1 | M]`

resources/demos/block-3-demos.md Demo 3.7 zitiert woertliche Trace-Ausgaben als ERWARTET, z.B. 'Skill broken-greeter matched paths-filter: NO (filter: never-match/**, current files: ...)' (Z.642) und 'description too generic for prompt — no candidate match' (Z.667). Ob '/debug skill-not-triggering' bzw. 'claude --verbose' real exakt solche Zeilen ausgibt, ist nicht verifiziert; die Recovery-Note Z.695 raeumt selbst ein, '/debug' sei in aelteren Builds evtl. gar nicht vorhanden. Fix: Vor Session 3 auf der Moderations-Maschine real pruefen, was '/debug' / 'claude --verbose' tatsaechlich ausgibt, und die zitierten Zeilen an die echte Ausgabe anpassen ODER explizit als 'sinngemaess, Wortlaut variiert' kennzeichnen.

- **Dateien:** resources/demos/block-3-demos.md
- **Begruendung:** Live-Demo-Risiko vor Publikum: Wenn die versprochene Trace-Zeile nicht erscheint, merken die (technisch versierten) Teilnehmer das sofort und der Moderator verliert Glaubwuerdigkeit. Direkter Einfluss auf den Live-Eindruck — Pflicht laut Verifikation-vor-Aktion (Pre-Demo).
- **Akzeptanz:** Die in Demo 3.7 zitierten Trace-Zeilen sind entweder gegen die reale Ausgabe des aktuellen Binaries verifiziert und ggf. angepasst, ODER eindeutig als sinngemaess/variabel gekennzeichnet. Die Abhaengigkeit von '/debug'-Verfuegbarkeit ist transparent gemacht.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

#### T-063 — Unbelegte Versions-Gates und 'when available'-Befehle bereinigen  `[P2 | M]`

In block-2-ecosystem.md, block-3-advanced.md und cheatsheet.md gibt es viele extrem spezifische, unbelegte Versions-Gates, z.B. block-2 Z.589 'updatedToolOutput (v2.1.119+)', Z.607 'continueOnBlock (v2.1.121+)', Z.624 'terminalSequence (v2.1.139+)', Z.312 'Since v2.1.59 this Auto-Memory feature is default on'. Daneben Hedges, die Unsicherheit verraten: block-1 Z.347 'claude project purge <path> (when available)' und cheatsheet Z.123 'claude auto-mode defaults'. Die Mischung aus Schein-Praezision und '(when available)' ist genau das Muster, das ein Skeptiker als blosses Folien-Wissen markiert. Fix (methodisch): Versionsnummern entweder belegen (gegen Changelog verifizieren — an Currency-Auditoren delegierbar) oder durch 'recent versions'/'2026er Releases' ersetzen. '(when available)' neben einem konkreten Befehl ist ein Widerspruch in sich — den Befehl als geplant kennzeichnen oder weglassen.

- **Dateien:** resources/modules/block-2-ecosystem.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md; resources/modules/block-1-foundations.md
- **Begruendung:** Schein-Praezision (exakte Patch-Versionen ohne Quelle) plus '(when available)' untergraebt das Vertrauen eines skeptischen Senior-Publikums in den ganzen Inhalt. Aktualitaet/Korrektheit-Ebene, daher unter den Lernerfolgs-Blockern, aber wichtig fuer die Tiefen-Glaubwuerdigkeit.
- **Akzeptanz:** Jede konkrete Versionsnummer ist entweder gegen den Changelog belegt ODER durch eine weichere Formulierung ('recent versions') ersetzt. Kein Befehl steht mehr mit '(when available)' als ob er real existiere — entweder als geplant gekennzeichnet oder entfernt.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-038 — FAQ-Verkuerzungen mit fehlenden Trade-offs/Eskalationen reparieren (ZDR-Feature-Verlust, Haiku-Eskalation, Modell-Multiplikatoren)  `[P2 | S]`

Drei FAQ-Antworten verkuerzen so stark, dass sie irrefuehrend werden — jeweils widerspricht die FAQ einer differenzierteren Aussage in Modul/Cheatsheet: (1) faq.md Z.36: 'ZDR ... reduziert Retention auf 0 Tage' OHNE den Feature-Verlust, waehrend block-3 Z.737 + cheatsheet Z.679 korrekt 'Zero Data Retention (some features disabled)' sagen — fuer eine Compliance-Frage irrefuehrend. Fix: Halbsatz '(einige Features deaktiviert)' ergaenzen. (2) faq.md Z.26: 'Pipeline-Pattern: /plan mit Opus, /batch von Subagents mit Sonnet, /review mit Haiku' — suggeriert /review nutze pauschal Haiku, waehrend Modul 3.2 Z.356 differenziert 'Review with Haiku first, escalate disagreements to Opus' sagt. Fix: '...mit Haiku (Eskalation strittiger Punkte an Opus)' ergaenzen. (3) faq.md Z.201: 'max kann 5-10x so lange brauchen wie medium' vermischt Kosten und Latenz, waehrend block-1 Z.1019 sauber '6x (Relative cost)' trennt. Fix: FAQ an die Modul-Tabelle koppeln oder explizit 'Latenz, nicht Kosten' schreiben und auf Modul 1.5 als Single Source verweisen.

- **Dateien:** resources/faq.md; resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md; resources/cheatsheet.md
- **Begruendung:** Die FAQ ist oft die erste Anlaufstelle (besonders fuer Solo-Lerner). Verkuerzungen, die Trade-offs (ZDR-Features), Qualitaetsstufen (Haiku->Opus-Eskalation) oder Kennzahl-Semantik (Kosten vs Latenz) weglassen, etablieren die schwaechere Aussage als Faustregel und koennen zu Fehlentscheidungen (z.B. ZDR waehlen, dann Feature-Verlust) fuehren.
- **Akzeptanz:** faq.md Z.36 erwaehnt den Feature-Verlust bei ZDR; faq.md Z.26 nennt die Haiku->Opus-Eskalation; faq.md Z.201 unterscheidet klar Kosten vs Latenz und verweist auf Modul 1.5 als Single Source. Keine der drei FAQ-Antworten widerspricht mehr der jeweiligen Modul-/Cheatsheet-Aussage.
- **Quelle:** Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-039 — Custom-Komponente notebooklm-Skill staerker als nicht-offiziell kennzeichnen + Installation in prerequisites.md dokumentieren  `[P2 | S]`

block-2-ecosystem.md Z.1209-1228 behandelt RAG/NotebookLM. Der Disclaimer Z.1220-1228 ('The notebooklm user skill ... is a custom-built wrapper, not part of the official Claude Code installation') existiert, ist aber klein und wird direkt danach durch '### Notation convention' (Z.1230) abgeloest, was die Skill-Nutzung wie Standard wirken laesst — Anfaenger uebersehen den Disclaimer leicht. Zusaetzlich (Z.1209-1220) ist der Google-Workspace-vs-Personal-Daten-Unterschied nur vage ('Enterprise data policies apply'), was fuer eine regulierte Branche (Physical Security, GDPR) kritisch ist. Fix: (a) Disclaimer zu einer prominenten Callout-Box erweitern, z.B. 'The notebooklm skill below requires separate installation (see prerequisites.md). Without it, use the NotebookLM web UI and copy results into Claude Code via @-file-includes. The pattern is real; the CLI tool is custom.' (b) In prerequisites.md die notebooklm-CLI-Installation explizit dokumentieren. (c) Optional die Workspace-vs-Personal-Policy konkretisieren ('Workspace: Google Workspace Data Governance, typischerweise strenger; Personal: Google ToS — vor proprietaerem Code mit Compliance abklaeren').

- **Dateien:** resources/modules/block-2-ecosystem.md; resources/prerequisites.md
- **Begruendung:** Solo-Lerner ohne Moderator koennen den kleinen Disclaimer ueberlesen und annehmen, der notebooklm-Skill sei Bundled — scheitern dann an einem fehlenden Tool. Die vage Datenpolicy ist fuer die GDPR-/PhySec-Zielgruppe ein reales Compliance-Risiko. Trennung offiziell vs custom ist ein wiederkehrendes Workshop-Thema.
- **Akzeptanz:** Der notebooklm-Abschnitt in block-2 hat eine prominente Callout-Box, die (1) den Skill als custom kennzeichnet, (2) auf die separate Installation verweist und (3) einen UI-Fallback nennt. prerequisites.md dokumentiert die notebooklm-CLI-Installation. Die Workspace-vs-Personal-Datenpolicy ist konkreter als 'Enterprise data policies apply'.
- **Quelle:** Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

#### T-064 — Exercise 2.3: manuelles Schreiben in ~/.claude/plugins/cache/ durch CLI-konformen Weg ersetzen  `[P2 | M]`

resources/exercises/block-2-exercises.md Step 4 laesst Teilnehmer per Hand Ordner + Manifest in den CLI-verwalteten Plugin-cache schreiben: 'mkdir -p ~/.claude/plugins/cache/my-mini-plugin-marketplace/.claude-plugin' (Z.418) und 'cat > .../plugin.json' (Z.423); zusaetzlich Hint 'Team distribution: ... drop the directory into ~/.claude/plugins/cache/' (Z.511). Der cache-Ordner ist Claude-Code-managed — manuelles Hineinschreiben ist fragil und kann beim naechsten Plugin-Sync verschwinden. Das widerspricht dem CLI-only-Plugin-Modell (claude plugin marketplace add / claude plugin install). Fix: Scaffolding in ein neutrales Verzeichnis legen (z.B. ~/cc-workshop/my-mini-plugin) und mit 'claude --plugin-dir ./my-mini-plugin' laden — so wie es Exercise 3.5 Variant C bereits korrekt macht (Z.301). cache/ nur lesend erkunden, nicht beschreiben.

- **Dateien:** resources/exercises/block-2-exercises.md
- **Begruendung:** Eine Hands-on-Uebung, die einen fragilen, vom Tool spaeter ueberschriebenen Weg lehrt, vermittelt ein falsches mentales Modell und kann live scheitern (Plugin verschwindet nach Sync). Der korrekte CLI-/--plugin-dir-Weg existiert schon in Exercise 3.5 — Konsistenz herstellen.
- **Akzeptanz:** Exercise 2.3 scaffoldet das Plugin in einem neutralen Verzeichnis und laedt es via 'claude --plugin-dir' (analog Exercise 3.5 Variant C). Kein 'mkdir'/'cat >' mehr in ~/.claude/plugins/cache/; der cache wird hoechstens lesend erkundet. Der Team-Distribution-Hint nennt den CLI-Weg statt 'drop into cache/'.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

#### T-084 — Kosmetische Cross-Datei-Inkonsistenzen vereinheitlichen (Bundled-Skills-Liste, Quick-Reference/Routine, Windows-Sandbox-Ton, Hook-Event-Zahl)  `[P3 | M]`

Vier kleinere Inkonsistenzen, die ein Solo-Lerner/Skeptiker beim Quervergleich als Widerspruch erlebt; gebuendelt, da alle 'eine kanonische Quelle definieren, Rest verweisen lassen' lauten: (1) BUNDLED-SKILLS: glossary.md Z.49 nennt '/batch, /loop, /run, /verify, /debug, /simplify, /claude-api, /fewer-permission-prompts, /run-skill-generator', cheatsheet.md Z.243-249/257-267 zieht die Grenze Bundled vs workshop-custom (/commit, /tdd) anders. Fix: kanonische Bundled-Liste im Glossar definieren, Cheatsheet darauf verweisen statt duplizieren; offiziell-bundled vs workshop-custom klar trennen. (2) QUICK-REFERENCE/ROUTINE: quick-reference.md Z.40 listet '/goal /loop /schedule' gleichrangig, waehrend faq.md Z.119-125 und glossary.md Z.236 ('Routine = offizielle Variante, Ersatz fuer /schedule + /loop') den Routine-Vorrang zeigen. Fix: Mini-Hinweis '/schedule+/loop -> Routine ist die persistente offizielle Variante (s. FAQ)' in der Quick-Reference. (3) WINDOWS-SANDBOX-TON: block-3-advanced.md Z.708 'first-class shell path rather than a fallback' vs cheatsheet.md Z.397 '(limited) | Relies on permission system' — technisch dasselbe (kein Kernel-Sandbox), aber gegensaetzlicher Ton. Fix: einheitlich 'first-class shell path, aber KEIN Kernel-Sandbox (anders als Seatbelt/bwrap)' in beiden. (4) HOOK-EVENT-ZAHL: block-2-ecosystem.md Z.387 '28 lifecycle events' (hart) vs cheatsheet.md Z.456 '~28' (ungefaehr). Fix: konsistent '~28' ODER exakte Liste hinterlegen und 28 belegen (kurz nachzaehlen, ob die im Cheatsheet genannten 17 Kern + 16 weitere wirklich 28 ergeben — wirkt eher nach mehr als 28).

- **Dateien:** resources/glossary.md; resources/cheatsheet.md; resources/quick-reference.md; resources/faq.md; resources/modules/block-2-ecosystem.md; resources/modules/block-3-advanced.md
- **Begruendung:** Reine Konsistenz-/Komfort-Ebene: keine sachlich falsche Kernaussage, aber beim Quervergleich entstehen scheinbare Widersprueche, die das Vertrauen leicht ankratzen — vor allem fuer Solo-Lerner, die zwischen Dateien hin- und herspringen. Niedrigste Prioritaet laut Lernerfolg-vor-Komfort, aber gebuendelt schnell abzuarbeiten.
- **Akzeptanz:** (1) Eine kanonische Bundled-Skills-Liste existiert (im Glossar), Cheatsheet verweist darauf; Bundled vs workshop-custom ist klar getrennt. (2) Quick-Reference enthaelt den Routine-Vorrang-Hinweis. (3) block-3 und cheatsheet beschreiben die Windows-Sandbox mit konsistentem Ton (kein Kernel-Sandbox). (4) Hook-Event-Zahl ist in Modul und Cheatsheet identisch formuliert und gegen die genannte Liste plausibilisiert.
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch (kein Moderator); Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

#### T-075 — Analogie 'Self-Improve Loop = naechtliche Firmware-Selbstheilung' didaktisch umstellen (Einschraenkung zuerst)  `[P3 | S]`

block-3-advanced.md Z.964-971 praesentiert ein Szenario als positives Vorbild: 'Your access control system runs overnight diagnostics ... It applies the update ... No human involvement. Full audit trail.' Genau das ist unter EN 50131 unzulaessig. Der Kurs faengt es zwar direkt danach mit dem Hinweis-Kasten Z.973-980 ab — aber die Analogie wird zuerst als Vorbild gezeigt und erst dann widerrufen, was didaktisch holprig ist (ein PhySec-Experte stutzt erst 'das duerfen wir gar nicht' und wird dann beruhigt). Fix: Reihenfolge umdrehen — zuerst 'fuer Hardware-Endpunkte NICHT zulaessig, aber als Bild fuer Code/CI-Repos:', dann die Self-Healing-Erzaehlung. So bleibt die Mechanik-Illustration ohne den Stolper-dann-Beruhigung-Effekt.

- **Dateien:** resources/modules/block-3-advanced.md
- **Begruendung:** Bereits durch den nachfolgenden Hinweis-Kasten abgefedert (severity low), daher niedrige Prioritaet — aber die Umstellung der Reihenfolge verbessert den didaktischen Fluss fuer die Domaenenexperten-Zielgruppe spuerbar bei minimalem Aufwand.
- **Akzeptanz:** In block-3-advanced.md steht die EN-50131-Einschraenkung VOR der Self-Healing-Erzaehlung, sodass die Analogie von Anfang an als Code/CI-Bild gerahmt ist und nicht erst als Hardware-Vorbild praesentiert und dann widerrufen wird.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

### Cluster: `demo-reliability` (9 TODOs)

11 Roh-Befunde von 3 Personas (Markus/Firmware-Entwickler, Sandra/Live-Moderatorin, Lena/Hands-on-QA) zur Demo-Zuverlaessigkeit. Verifiziert gegen die echten Dateien: alle technischen Kern-Claims stimmen. Zwei Befunde wuerden eine Live-Demo bzw. eine Uebung HART zum Scheitern bringen und sind P0: (1) Exercise 3.6 installiert einen claude-aufrufenden pre-commit-Hook ins SCHULUNGS-Repo selbst (Playground ist kein eigenes Repo — `git init` ist No-op, Hook landet via ../.git im dynamic_workshop-Repo und blockiert dessen Commits); (2) der ungeplante size_t-Unterlauf in osdp_frame_decoder.c (Z.102 `hex_len - 1`) kann Demo 3.3 abstuerzen lassen, bevor der Swarm scannt. Konsolidiert zu 9 atomaren TODOs: 2x P0 (Demo/Uebung-Crash), 4x P1 (fehlende Go/No-Go-Matrix, Cluster-Risiko Session 3, fehlende Plugin-Fallbacks, fehlendes broken-greeter-Asset), 3x P2/P3 (Budget-Cap-Konsistenz, CVE-Cleanup-Automatisierung, Demo-Timing, Traversal-Vorbedingung). Dominante Themen: (a) Moderator braucht abhakbare Entscheidungshilfen am Workshop-Morgen, (b) Plugin/Auth/Internet-Abhaengigkeiten brauchen lokale Fallback-Anker, (c) fehlende Artefakte muessen ins Repo statt am Morgen gebastelt zu werden.

#### T-002 — Exercise 3.6 in ein isoliertes Sandbox-Repo umleiten — pre-commit-Hook darf nicht ins Schulungs-Repo schreiben  `[P0 | S]`

VERIFIZIERT: Der Playground ist KEIN eigenes Git-Repo. `ls workshop-playground/.git` -> 'No such file or directory'; `git ls-files workshop-playground/` zeigt alle Dateien im Eltern-Repo getrackt; `git -C workshop-playground rev-parse --git-path hooks/pre-commit` liefert `../.git/hooks/pre-commit` — also den Hook des dynamic_workshop-Repos selbst. Exercise 3.6 (Z.334-336 `cd workshop-playground` + `git init`, Z.341 Schreiben nach `.git/hooks/pre-commit`) ist damit doppelt kaputt: `git init` im Playground ist ein No-op, und der claude-aufrufende pre-commit-Hook wird im Schulungs-Repo installiert und blockiert dessen eigene Commits. FIX: Teilnehmer in ein frisches, separates Verzeichnis schicken (z.B. `mkdir -p ~/cc-workshop/exercise-3.6 && cd ~/cc-workshop/exercise-3.6 && git init`) — konsistent mit den Block-1-Uebungen, die alle ~/cc-workshop/... nutzen. Mindestens aber explizit warnen, dass `git init` im Playground ein No-op ist.

- **Dateien:** resources/exercises/block-3-exercises.md
- **Begruendung:** Hoechste Einstiegshuerde: Die Uebung kann das Schulungs-Repo selbst beschaedigen (Commits blockieren) und scheitert in der vorgesehenen Form garantiert. Trifft jeden Teilnehmer, der die Uebung Schritt fuer Schritt macht.
- **Akzeptanz:** Exercise 3.6 nutzt ein separates ~/cc-workshop/exercise-3.6-Verzeichnis mit eigenem `git init`; ein Testlauf der Schritte erzeugt einen funktionierenden pre-commit-Hook OHNE die .git/hooks des dynamic_workshop-Repos zu beruehren.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

#### T-003 — Ungeplanten size_t-Unterlauf im C-Hex-Parser haerten oder als 5. Bonus-Vuln dokumentieren  `[P0 | S]`

VERIFIZIERT in osdp_frame_decoder.c Z.102: `for (size_t i = 0; i < hex_len - 1; i += 2)`. Bei ungerader hex_len wird das letzte Nibble verschluckt; bei hex_len==0 unterlaeuft `hex_len - 1` (size_t-Wrap auf SIZE_MAX) -> riesige Schleife / OOB-Schreibzugriff via `buf[buf_len++]`. Das ist ein VIERTER ungeplanter Memory-Bug im main(), nicht in der dokumentierten V1-V4-Tabelle (workshop-playground/CLAUDE.md) erfasst. Risiko: Bei Demo 3.3 kann dieser Bug unkontrolliert feuern und die geplanten Trigger V1-V4 verdecken oder die Demo abstuerzen lassen, BEVOR der Swarm ueberhaupt scannt (der Swarm liest statisch — fuer ihn irrelevant, aber jede Live-Ausfuehrung des Binaries ist betroffen). FIX (eine der beiden Optionen): (a) haerten mit `if (hex_len == 0 || hex_len % 2) { fprintf(stderr, "Invalid hex length\n"); return 1; }` vor der Schleife; ODER (b) bewusst als 5. Bonus-Vuln in workshop-playground/CLAUDE.md aufnehmen. Empfehlung: haerten, da unkontrolliertes Verhalten in einer Live-Demo schlechter steuerbar ist als ein sauberer Satz geplanter Vulns.

- **Dateien:** workshop-playground/osdp_frame_decoder.c; workshop-playground/CLAUDE.md
- **Begruendung:** Sachliche Korrektheit + Demo-Stabilitaet: Ein unkontrollierter Crash vor dem geplanten Swarm-Lauf untergraebt die zentrale Security-Demo. Entweder weg oder bewusst kuratiert — Zwischenzustand ist das einzige inakzeptable.
- **Akzeptanz:** Entweder die Schleife ist gegen hex_len==0 und ungerade Laenge gehaertet (verifiziert per Build + Lauf mit leerem/ungeradem Input ohne Crash), ODER der Bug ist als 5. Vuln in der V-Tabelle von workshop-playground/CLAUDE.md dokumentiert. Die V1-V4-Tabelle und der tatsaechliche Code-Stand stimmen ueberein.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-027 — Eine abhakbare Go/No-Go-Demo-Matrix fuer den Workshop-Morgen anlegen  `[P1 | M]`

Die Live-vs-Fallback-Logik ist auf drei Dokumente verstreut: trainer-notes.md (Failure-Tabelle Z.59-67), die Dry-Run-Datei (Verdicts + Timeline) und jede einzelne Demo-Datei (Recovery-Notes). Es fehlt EINE Seite, die der Moderator am Morgen linear abhaken kann. FIX: In trainer-notes.md eine 1-seitige Go/No-Go-Matrix ergaenzen — eine Zeile pro Demo, Spalten: 'Demo', 'Preflight-Check (konkreter Befehl, z.B. `claude plugin list | grep devil-advocate-swarms`)', 'wenn PASS -> live', 'wenn FAIL -> Fallback-Artefakt + Pfad'. Die Recovery-Notes existieren bereits; sie muessen nur in diese abhakbare Matrix verdichtet werden. Diese Matrix ist auch der natuerliche Ankerpunkt fuer die Fallback-Pfade aus den uebrigen TODOs dieses Clusters.

- **Dateien:** resources/trainer-notes.md
- **Begruendung:** Lernerfolg/Live-Sicherheit: Die wichtigste fehlende Moderatoren-Hilfe. Verstreute Recovery-Infos sind unter Live-Druck nicht nutzbar; eine einzige abhakbare Matrix verhindert Blackouts vor Publikum.
- **Akzeptanz:** trainer-notes.md enthaelt eine Tabelle mit je einer Zeile pro Live-Demo, jede mit ausfuehrbarem Preflight-Befehl und explizitem Fallback-Pfad; jede in block-3-demos.md genannte Plugin-/Auth-/Internet-Abhaengigkeit ist in der Matrix abgedeckt.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

#### T-014 — Garantiert-lokalen Live-Anker fuer Session 3 festlegen und als Block-Eroeffnung positionieren  `[P1 | S]`

Cluster-Risiko in Session 3: Die fragilsten Demos haengen kumuliert an externen Voraussetzungen. Demo 3.2 braucht Codex CLI installiert+authentifiziert (Z.61-63) UND das multi-model-orchestrator-Plugin; Demo 3.4 braucht agentic-os-Plugin + Budget-Cap; Demo 3.3 braucht devil-advocate-swarms-Plugin; Demo 3.3c braucht WebSearch/Internet (Z.353); Demo 3.5 Step 4 braucht die Telegram-Bridge. Faellt eines vor Publikum aus, droht eine Kettenreaktion ('3+ Demos in Folge', genau der trainer-notes.md-Notfall Z.71). FIX: EINEN garantiert-live-Anker festlegen, der NUR auf lokal installiertem `claude` beruht — laut Dry-Run ist Demo 3.6 Headless ('Should-show live, because claude is installed locally') der Kandidat. Diese Demo explizit als 'laeuft sicher' markieren und als Eroeffnung von Block 3 ziehen, damit das Publikum frueh einen funktionierenden Live-Moment sieht (psychologisch wichtig, falls spaeter Plugin-Demos kippen).

- **Dateien:** resources/demos/block-3-demos.md; resources/session-plan.md
- **Begruendung:** Lernerfolg/Live-Sicherheit: Ein frueher garantierter Live-Erfolg fangt spaetere Plugin-Ausfaelle psychologisch ab und verhindert, dass Block 3 mit einer Ausfall-Kette startet.
- **Akzeptanz:** In session-plan.md und block-3-demos.md ist Demo 3.6 (oder ein anderer rein-lokaler Demo) als garantierter Live-Anker markiert und an den Anfang von Block 3 gezogen; die Reihenfolge in beiden Dateien ist konsistent.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team
- **Abhaengig von:** Eine abhakbare Go/No-Go-Demo-Matrix fuer den Workshop-Morgen anlegen

#### T-015 — Plugin-Fallbacks direkt in Exercise 3.3 einbauen (nicht nur in den Demos)  `[P1 | S]`

Exercise 3.3 ruft hart `/devil-advocate-swarms:swarm scan ...` (Z.127); die gesamte Uebung (Step 3-4, 'What to Report') haengt am Swarm-Output. Ein Fallback existiert NUR in den Demos (block-3-demos.md:211 'If devil-advocate-swarms plugin not installed: Show recording'), nicht in der Exercise selbst. devil-advocate-swarms ist ein Custom-Workshop-Plugin (prerequisites.md:225/249) — ein Selbstlerner ohne installiertes Plugin bleibt haengen. FIX: In Exercise 3.3 einen expliziten Fallback ergaenzen: ohne Plugin stattdessen `/security-review` (built-in) ODER einen normalen Audit-Prompt gegen access_control.py laufen lassen — die drei geplanten Vulns (Command Injection, Hardcoded Credentials, Path Traversal) sind so oder so auffindbar. Plugin-Voraussetzung am Uebungsanfang explizit nennen.

- **Dateien:** resources/exercises/block-3-exercises.md
- **Begruendung:** Einstiegshuerde fuer Selbstlerner: Eine Uebung, die ohne ein optionales Custom-Plugin hart blockiert, ist fuer einen Teil der Zielgruppe unausfuehrbar. Built-in-Fallback macht sie universell durchfuehrbar.
- **Akzeptanz:** Exercise 3.3 nennt die Plugin-Voraussetzung am Anfang und enthaelt einen built-in-Fallback (`/security-review` oder Audit-Prompt), mit dem die drei geplanten Vulns ohne devil-advocate-swarms gefunden werden koennen.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

#### T-016 — broken-greeter/SKILL.md als kopierbares Asset ins Repo legen  `[P1 | S]`

VERIFIZIERT: `resources/demos/assets/` existiert nicht. Demo 3.7 setzt voraus: 'The moderator has prepared an intentionally broken skill at ~/.claude/skills/broken-greeter/SKILL.md with three problems planted in this order' (Z.596-603). Diese SKILL.md liegt nirgends im Repo als kopierbares Artefakt — der Moderator muss sie am Workshop-Morgen aus der Prosa-Beschreibung rekonstruieren (generische Description, disable-model-invocation:true, paths:[never-match]). FIX: Die fertige Datei als Asset ins Repo legen (resources/demos/assets/broken-greeter/SKILL.md), inkl. der drei geplanten Fehler exakt in der im Skript beschriebenen Reihenfolge. Demo 3.7 ist laut Dry-Run ein Live-Kandidat — mit fertigem Asset ist sie reproduzierbar statt Morgen-Bastelei.

- **Dateien:** resources/demos/assets/broken-greeter/SKILL.md; resources/demos/block-3-demos.md
- **Begruendung:** Reproduzierbarkeit: Ein Live-Demo-Kandidat, dessen zentrales Artefakt manuell aus Prosa rekonstruiert werden muss, ist fehleranfaellig und verschwendet Vorbereitungszeit. Asset-im-Repo macht die Demo deterministisch.
- **Akzeptanz:** resources/demos/assets/broken-greeter/SKILL.md existiert mit genau den drei im Skript beschriebenen Fehlern in korrekter Reihenfolge; block-3-demos.md verweist auf den Asset-Pfad statt auf manuelle Rekonstruktion.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

#### T-044 — Budget-Cap in Demo 3.4 (Self-Improve) als Pflicht-Vorgabe VOR den /run-loop-Aufruf setzen  `[P2 | S]`

Budget-Cap-Empfehlung ist uneinheitlich: Demo 3.6 Step 3 setzt sauber `--max-budget-usd 0.05 --max-turns 2` (Z.558-561). Demo 3.4 Self-Improve (Z.380-393) ruft `/agentic-os:run-loop` mit '1' Iteration, nennt aber im Step KEINEN expliziten Budget-Cap — der Cap taucht erst in den Recovery-Notes auf ('If --max-budget-usd is hit early', Z.418). Gleichzeitig warnt session-plan.md, der Self-Improve-Loop sei der Haupt-Kostentreiber ($15-50, Z.118/122). FIX: In Demo 3.4 Step 2 einen expliziten Budget-Cap als Pflicht-Vorgabe VOR den /run-loop-Aufruf setzen (analog Demo 3.6), nicht nur reaktiv in den Recovery-Notes. Zusaetzlich einen `/cost`-Blick vor und nach dem Loop ins Skript aufnehmen.

- **Dateien:** resources/demos/block-3-demos.md
- **Begruendung:** Komfort/Kostenkontrolle: Der Cap muss gesetzt sein BEVOR der Moderator Enter drueckt, nicht erst reaktiv greifen. Bei der teuersten Demo schuetzt das vor unerwarteten Live-Kosten.
- **Akzeptanz:** Demo 3.4 Step 2 enthaelt einen expliziten Budget-Cap (analog --max-budget-usd in Demo 3.6) als Pflicht-Vorgabe vor dem /run-loop-Aufruf, plus einen /cost-Check vor und nach dem Loop.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

#### T-045 — CVE-Cleanup in Demo 3.3c als Ein-Befehl-Revert automatisieren  `[P2 | S]`

Demo 3.3c Step 0 fuegt bewusst eine verwundbare Dependency ein: `requests==2.5.0 (CVE-2018-18074)` in requirements.txt (Z.306). Recovery-Note Z.354: 'If you forget the cleanup step: Document this as the demos biggest risk — always revert the planted vulnerable line.' Step 3 Cleanup verlangt manuelles Editieren der Datei (Z.341-346). FIX: Cleanup nicht der Erinnerung ueberlassen — ein Ein-Befehl-Revert ins Skript setzen (`git checkout -- workshop-playground/requirements.txt` o.ae.), plus den expliziten Hinweis 'NIEMALS `pip install` auf dieser Zeile ausfuehren'. Ein `git checkout` ist sicherer und schneller als 'Datei oeffnen und Zeile manuell loeschen', besonders mit 17 Modulen im Kopf.

- **Dateien:** resources/demos/block-3-demos.md
- **Begruendung:** Live-Sicherheit/Sauberkeit: Ein vergessener manueller Cleanup hinterlaesst eine echte verwundbare Dependency im Schulungs-Material. Ein-Befehl-Revert eliminiert den vom Skript selbst als 'biggest risk' markierten Schritt.
- **Akzeptanz:** Demo 3.3c Cleanup-Step ersetzt das manuelle Editieren durch einen Ein-Befehl-Revert (git checkout der requirements.txt) und enthaelt eine 'NIEMALS pip install auf dieser Zeile'-Warnung.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

#### T-078 — Demo-Dauern im session-plan.md realistisch ausweisen und Bonus-Schritte als optional markieren  `[P3 | S]`

Demo-Skript-Dauern uebersteigen die Plan-Slots. session-plan.md Z.30: 'Demo 1.4 | 2:10-2:20' = 10-Min-Slot, aber block-1-demos.md Demo 1.4 ist '~10 minutes' OHNE den Worktree-Bonus (Step 6) — mit Bonus deutlich mehr. Analog Demo 1.1: Plan-Slot 0:30-0:40 (10 Min), Skript '~8 minutes' (Z.26), aber Modul 1.1 davor hat nur 0:15-0:30 = 15 Min fuer 'drei Interfaces, Permissions, Models'. FIX: Pro Demo eine realistische 'Demo-Dauer inkl. Talking-Points' neben den Plan-Slot schreiben; Bonus-Schritte (z.B. Worktree Step 6) im session-plan.md als 'nur bei Zeitueberschuss' kennzeichnen (im Skript schon mit 'Bonus' getan, im Plan aber nicht sichtbar). 2-3 Min Puffer pro Demo einplanen — Live-Demos laufen IMMER langsamer als das Skript.

- **Dateien:** resources/session-plan.md
- **Begruendung:** Komfort/Planungssicherheit: Unrealistische Slots fuehren zu Hetze oder Ueberziehen. Sichtbare Bonus-Markierung und Puffer geben dem Moderator eine ehrliche Zeitkalkulation.
- **Akzeptanz:** session-plan.md weist pro Demo eine realistische Dauer inkl. Talking-Points aus, markiert Bonus-Schritte als optional ('nur bei Zeitueberschuss') und enthaelt 2-3 Min Puffer pro Demo.
- **Quelle:** Sandra — Live-Moderatorin, haelt den Workshop live fuer ihr Team

### Cluster: `new-exercise-idea` (2 TODOs)

Zwei thematisch disjunkte Uebungs-Ideen, keine Deduplizierung noetig. (1) Hoechster Verkaufspunkt fuer die echte Zielgruppe: eine gefuehrte Domaenen-Uebung (OSDP/Wiegand-Parser) in Block 3 fehlt komplett — bislang ist alles generisch, OSDP taucht nur als beilaeufige Skill-Variante im Capstone 3.5 (block-3-exercises.md:299) auf. (2) Kleines Lernergonomie-Plus in Block 1: ein 30-Sekunden-Verifikations-Zwischenschritt in Exercise 1.2 vor dem Restart, damit der Teilnehmer den Unterschied Kontext-im-Lauf vs. persistiert zweimal erlebt. Priorisierung nach Lernerfolg/Einstiegshuerde: Befund 1 ist P1 (staerkster zielgruppenspezifischer Aha-Moment, aber optional/Bonus), Befund 2 ist P2 (sanfter Zwischenschritt, kleines Erfolgserlebnis).

#### T-032 — Gefuehrte Domaenen-Uebung 3.9 ergaenzen: OSDP/Wiegand-Parser mit Claude bauen (TDD/Multi-Agent)  `[P1 | M]`

In block-3-exercises.md fehlt eine gefuehrte, domaenenechte PhySec-Uebung. Alle Block-3-Uebungen (3.1-3.8) sind generisch (Multi-Agent, Codex-Swarm, Security-Audit, Automation, Pre-Commit-Hook, HIPAA, Broken-Hook). OSDP wird nur beilaeufig als Skill-Variante im Capstone 3.5 genannt (block-3-exercises.md:299: 'Generate OSDP frame tests'), aber nie als eigene gefuehrte Uebung. Fuer 3 erfahrene PhySec-Entwickler (Zutrittskontrolle/Alarmsysteme) ist genau das der staerkste Aha-Moment und der beste Verkaufspunkt des Kurses.

Neue optionale 'Should-do'-Uebung 3.9 anlegen, die Multi-Agent/TDD-Inhalt mit echter Domaene verbindet. Zwei Varianten anbieten:
- Variante A: 'Lass Claude einen robusten OSDP-Frame-Parser mit Bounds-Checks aus dem verwundbaren osdp_frame_decoder.c bauen + property-based tests fuer Length-Field-Fuzzing'.
- Variante B: 'Wiegand-26-bit-Parser (Facility-Code + Card-Number + Parity) mit TDD'.
Die Uebung soll an das vorhandene verwundbare osdp_frame_decoder.c im workshop-playground anknuepfen (vor Aufnahme dort verifizieren, dass die Datei existiert und welchen genauen Pfad sie hat) und den TDD-/Multi-Agent-Workflow aus Block 3 wiederverwenden. Format konsistent zu 3.6 halten (Type, Priority: Should-do, Goal, Background, Steps, Success Check, Hints).

Laut Projekt-CLAUDE.md zusaetzlich Pflicht: agents/workshop-mentor.md bei dieser Inhaltsaenderung mit aktualisieren (neue Uebung 3.9 dort eintragen).

- **Dateien:** resources/exercises/block-3-exercises.md; agents/workshop-mentor.md; workshop-playground/
- **Begruendung:** Staerkster moeglicher Verkaufspunkt fuer die konkrete Zielgruppe (3 PhySec-Firmware-Entwickler): verbindet abstrakten Multi-Agent/TDD-Stoff mit echter Domaene und erzeugt den eigentlichen Aha-Moment. Aktuell bleibt der Domaenenbezug auf eine beilaeufige Skill-Variante (3.5:299) beschraenkt — der hoechste Lernerfolg liegt brach. Optional/Bonus-Charakter (keine Pflicht-Hausaufgabe) haelt es P1 statt P0.
- **Akzeptanz:** block-3-exercises.md enthaelt eine neue gefuehrte Uebung 3.9 mit beiden Varianten (OSDP-Frame-Parser bzw. Wiegand-26-bit-Parser), im selben Format wie 3.6 (Type/Priority/Goal/Background/Steps/Success Check/Hints), die explizit an das verwundbare osdp_frame_decoder.c (Pfad verifiziert) und den TDD-/Multi-Agent-Workflow anknuepft. agents/workshop-mentor.md fuehrt Uebung 3.9 auf. Der OSDP-Hinweis in Capstone 3.5 (Z.299) verweist optional auf die neue Vollform 3.9.
- **Quelle:** Markus — Zutrittskontroll-Firmware-Entwickler, CySec-affin (echte Zielgruppe)

#### T-055 — 30-Sekunden-Verifikations-Zwischenschritt in Exercise 1.2 vor dem Restart einbauen  `[P2 | S]`

In block-1-exercises.md springt Exercise 1.2 von 'CLAUDE.md schreiben' (Step 2-3) direkt zu 'exit/restart + Persistenz testen' (Step 5, Z.161-168) und dann zur 'never-change'-Boundary (Step 6, Z.170-177). Zwischen Anlegen und Restart fehlt ein kleiner verifizierender Zwischenschritt im selben Lauf. Der entsprechende Hinweis existiert nur passiv als Hint ('You can ask Claude to show you the current CLAUDE.md at any time', Z.203).

Vor dem Restart einen 30-Sekunden-Check als expliziten Schritt einbauen, z.B.: 'Frag Claude JETZT sofort — noch vor dem Neustart: Welche Konventionen gelten fuer dieses Projekt? So siehst du den Effekt zweimal: in derselben Session (Kontext im laufenden Prozess) und nach dem Restart (persistiert aus CLAUDE.md geladen).' Dadurch versteht der Teilnehmer den Unterschied Kontext-im-Lauf vs. persistiert und bekommt ein kleines Zwischen-Erfolgserlebnis, bevor der Restart kommt. Die bestehende Schritt-Nummerierung (5,6,7) entsprechend anpassen.

Laut Projekt-CLAUDE.md ist agents/workshop-mentor.md bei Aenderungen an Uebungen mitzupflegen — pruefen, ob 1.2 dort detailliert beschrieben ist und ggf. den neuen Zwischenschritt nachziehen.

- **Dateien:** resources/exercises/block-1-exercises.md; agents/workshop-mentor.md
- **Begruendung:** Senkt die Einstiegshuerde im allerersten Hands-on-Block: ein sanfter, verifizierender Zwischenschritt macht den abstrakten Unterschied 'Kontext im Lauf vs. persistiert' konkret erfahrbar und liefert ein frueheres Erfolgserlebnis, bevor der (technisch unsichere) Restart-Schritt kommt. Geringer Aufwand, aber spuerbar bessere didaktische Treppe — daher P2.
- **Akzeptanz:** Exercise 1.2 in block-1-exercises.md enthaelt vor dem Restart-Schritt (vormals Step 5) einen neuen, explizit nummerierten 30-Sekunden-Schritt 'Konventionen im laufenden Lauf abfragen' mit dem Hinweis, dass derselbe Effekt nach dem Restart erneut sichtbar wird. Die nachfolgenden Schritte sind konsistent umnummeriert. agents/workshop-mentor.md ist falls noetig nachgezogen.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

### Cluster: `currency` (12 TODOs)

32 Roh-Befunde von 5 Personas, konsolidiert zu 12 atomaren TODOs. Hauptthemen: (1) Modellgeneration durchgaengig veraltet — Opus 4.7 statt 4.8 (Default seit v2.1.154/2026-05-28) und die komplett fehlende neue Klasse Claude Fable 5 (GA 2026-06-09) ziehen sich quer durch fast alle Dateien (block-1/2/3, cheatsheet, glossary, faq, mentor-agent, demos). (2) Ein BLOCKIERENDER Fehler: Exercise 3.6 verlangt das CLI-Flag `--max-turns`, das in der installierten CLI nicht existiert — Lena (Hands-on QA) kann die Uebung nicht abschliessen (Success-Check unerfuellbar). (3) Mehrere kleinere Aktualitaets-Luecken: Hook-Event-Count (28 ungenau), Effort-Default-Verhalten von Opus 4.8 (high statt xhigh), divergierende Stand-Daten ohne zentralen Versionsanker, fehlende neue Features (Fast-Mode, Dynamic Workflows, Lean System Prompt, SSE-Deprecation-Kontext). Prio-Logik: Der CLI-Flag-Blocker (P0) verhindert konkreten Lernerfolg. Die Modell-Updates (P1) sind sachliche Korrektheit, die der Solo-Lerner direkt gegen seine laufende CLI abgleicht und sonst verunsichert wird. Komfort-/Vollstaendigkeits-Erweiterungen (P2/P3) folgen. Alle Web-Behauptungen der Personas (Versionen, Daten, Preise) sollten vor dem Edit ein letztes Mal verifiziert werden, da sie aus Persona-WebSearches stammen.

#### T-001 — BLOCKER: --max-turns aus Exercise 3.6 entfernen (CLI-Flag existiert nicht)  `[P0 | S]`

Exercise 3.6 in block-3-exercises.md verwendet `--max-turns 2` im Hook-Skript (Z.351) und der Success-Check verlangt zwingend, dass das Flag im Hook auftaucht (Z.408: 'Every Module 3.6 flag (--bare, --max-budget-usd, --max-turns, --output-format) appears in your hook.'). Verifiziert: das Flag ist in allen drei Stellen vorhanden (Z.351, Z.365, Z.408). Die installierte CLI kennt `--max-turns` NICHT (`claude --help | grep -c max-turns` = 0); vorhanden sind nur --bare, --effort, --max-budget-usd, --output-format, --json-schema. Folge: Das Hook-Skript laeuft nicht und der Success-Check ist unerfuellbar — Lena bleibt an der Uebung haengen. Fix: --max-turns aus Skript (Z.351, Z.365) und Success-Check (Z.408) entfernen; die Loop-Begrenzung uebernimmt --max-budget-usd 0.10 ohnehin. Falls eine harte Iterationsgrenze didaktisch gewuenscht ist, im Text als Hinweis dokumentieren, dass die CLI das nicht mehr per Flag bietet. Zusaetzlich Exercise 1.5 pruefen (--max-turns dort nicht im Alias, aber laut Befund im Modultext referenziert) und Block-1/3-Modultexte gegen-greppen. Das Stretch-Goal mit --json-schema bleibt (Flag existiert).

- **Dateien:** resources/exercises/block-3-exercises.md; resources/exercises/block-1-exercises.md; resources/modules/block-1-foundations.md; resources/modules/block-3-advanced.md
- **Begruendung:** Hoechste Prio-Klasse 'Lernerfolg/Einstiegshuerde': Die Uebung ist nicht abschliessbar, der Erfolgs-Check kann nie gruen werden. Ein Solo-Lerner ohne Moderator kommt nicht weiter und verliert Vertrauen ins Material.
- **Akzeptanz:** `grep -rn 'max-turns' resources/` liefert keine Treffer mehr (oder nur eine bewusste Prosa-Notiz, die erklaert, dass das Flag nicht existiert). Das Hook-Skript in Exercise 3.6 laeuft mit der installierten CLI fehlerfrei durch und der Success-Check listet nur noch real existierende Flags.
- **Quelle:** Lena — Hands-on QA, macht jede Uebung Schritt fuer Schritt durch

#### T-025 — Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28)  `[P1 | M]`

Durchgaengig wird Opus 4.7 als Default-Modell genannt, obwohl Opus 4.8 seit v2.1.154 (28.05.2026) der primaere Default ist. Betroffene verifizierte Stellen: block-1-foundations.md Z.14 ('Opus 4.7 / Sonnet 4.6 / Haiku 4.5'), Z.162 ('Claude Opus 4.7 (default since 2026-04-16 GA, model ID claude-opus-4-7)'), Z.190 (auto-mode 'Max-Plan with Opus 4.7'); cheatsheet.md Z.308 ('Default in Claude Code since 2026-04-16 (GA)'), Z.312 ('defaults to Opus 4.7'), Z.364 (auto-mode), Z.309 (Sonnet '(beta)' entfernen); glossary.md Z.159; faq.md Z.24; block-3-advanced.md (Agent-Beispiele, u.a. claude-opus-4-7, 'Opus 4.7 only'); block-1-demos.md ('Baseline with Opus 4.7 + xhigh'); troubleshooting.md. WICHTIG: Das Datum 2026-04-16 war das GA-Datum von Opus 4.7; der neue Default kam erst mit 4.8 am 2026-05-28 — Datum entsprechend auf 'default since 2026-05-28 (v2.1.154 GA)' aendern, NICHT nur die Versionsnummer. Modell-ID auf claude-opus-4-8 anpassen wo genannt.

- **Dateien:** resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/glossary.md; resources/faq.md; resources/troubleshooting.md; resources/modules/block-3-advanced.md; resources/demos/block-1-demos.md
- **Begruendung:** Sachliche Aktualitaet mit direktem Lernerfolgs-Bezug: Der Solo-Lerner sieht in seiner laufenden CLI (am Lesedatum bereits Opus 4.8) ein anderes Modell als im Material und wird verunsichert, ob das Material noch gilt. Modell-Default ist die zentralste Faktenangabe des Kurses.
- **Akzeptanz:** `grep -rn 'Opus 4.7' resources/ agents/` liefert nur noch bewusste historische Referenzen (z.B. 'frueher 4.7'), nicht mehr als aktuellen Default. Default-Datum steht konsistent auf 2026-05-28 / v2.1.154. Modell-ID claude-opus-4-8 wo eine ID genannt wird.
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch (kein Moderator); Currency-Auditor: Modelle, Preise, Effort-Stufen; Currency-Auditor: CLI, Flags, Commands, Versionen; Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

#### T-026 — Claude Fable 5 (Mythos-Klasse, GA 2026-06-09) in alle Modelltabellen aufnehmen  `[P1 | M]`

Die neue Top-Tier-Modellklasse Claude Fable 5 fehlt im gesamten Workshop. Laut Persona-WebSearch GA seit 2026-06-09 (in v2.1.170), Pricing $10 input / $50 output je MTok, 1M Context, Command `/model fable` oder `/model claude-fable-5`. Betroffene Modelltabellen/Stellen: block-1-foundations.md Z.158-164 (Modelltabelle 1.1) und Z.950-956 (Pricing Reference, Datum dort '(as of 2026-05)' auf '(as of 2026-06)' aendern); cheatsheet.md Z.308-310; block-3-advanced.md Z.336-341 (Modell-Staerken-Tabelle 3.2) und Z.190 (auto-mode); quick-reference.md (Model-Section). Inhalt der neuen Zeile: Fable 5 als Premium/Mythos-Tier kennzeichnen, Staerken 'Highest reasoning, frontier performance, long-horizon agentic tasks, vision (Screenshot->Code)', Hinweis 'use when maximum capability is worth the cost'. In Module 1.1 ein kurzes Unterkapitel 'Claude Fable 5 — Mythos-Class (ab v2.1.170)' mit Schnellvergleich Fable 5 ($10/$50) / Opus 4.8 ($5/$25) / Sonnet 4.6 ($3/$15) / Haiku 4.5 ($1/$5). VORHER die Preise und das GA-Datum per WebSearch final verifizieren, da diese Zahlen aus Persona-Recherche stammen.

- **Dateien:** resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/modules/block-3-advanced.md; resources/quick-reference.md; agents/workshop-mentor.md
- **Begruendung:** Aktualitaet: Ein komplett fehlendes, am Lesedatum schon ueber zwei Wochen verfuegbares Top-Modell ist eine sichtbare Luecke. Der Lerner, der `/model` aufruft und Fable sieht, findet im Material keine Einordnung. Hoeher als reine Komfort-Items, da es die zentrale Modell-Auswahl-Lektion betrifft.
- **Akzeptanz:** Fable 5 erscheint mit Pricing/Context in: Modelltabelle 1.1, Pricing Reference 1.5, cheatsheet, Modell-Staerken-Tabelle 3.2, quick-reference. Mindestens ein Satz erklaert, wann Fable sinnvoll ist. Command `/model fable` ist dokumentiert (siehe abhaengiges TODO).
- **Quelle:** Currency-Auditor: Modelle, Preise, Effort-Stufen; Currency-Auditor: CLI, Flags, Commands, Versionen; Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)
- **Abhaengig von:** Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28)

#### T-012 — Mentor-Agent: Modell-Empfehlung auf Opus 4.8 / Fable 5 aktualisieren  `[P1 | S]`

agents/workshop-mentor.md Z.149 nennt in der Staffing-Analogie nur 'Opus (senior architect) / Sonnet (technician) / Haiku (assistant)' — ohne Opus-Generation und ohne Fable 5. Antwort umschreiben zu: 'Opus 4.8 is your senior architect. Fable 5 (new since June 2026) is your principal/highest-capability tier — premium cost. Sonnet is your experienced technician. Haiku is your assistant.' Zusaetzlich (laut CLAUDE.md-Regel 'Bei jeder Inhaltsaenderung an Modulen/Demos/Exercises auch agents/workshop-mentor.md aktualisieren') sicherstellen, dass der Mentor mit den geaenderten Modulen konsistent bleibt. Optionale Notiz beim Frontmatter (Z.28 'model: sonnet'): '(Can be upgraded to Opus 4.8 or Fable 5 if future versions require deeper reasoning.)' — niedrige Prio, nicht zwingend.

- **Dateien:** agents/workshop-mentor.md
- **Begruendung:** Der Mentor-Agent ist der interaktive Einstieg fuer Solo-Lerner (/workshop guide/learn). Veraltete Modell-Aussagen hier widersprechen direkt der laufenden CLI. CLAUDE.md verlangt explizit Mentor-Sync bei Modul-Aenderungen.
- **Akzeptanz:** Z.149 nennt Opus 4.8 und Fable 5. Keine Modell-Aussage im Mentor widerspricht den aktualisierten Modultabellen.
- **Quelle:** Currency-Auditor: Modelle, Preise, Effort-Stufen
- **Abhaengig von:** Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28); Claude Fable 5 (Mythos-Klasse, GA 2026-06-09) in alle Modelltabellen aufnehmen

#### T-013 — Effort-Default fuer Opus 4.8 korrigieren: high (nicht xhigh) ist Default  `[P1 | S]`

Mehrere Stellen suggerieren, xhigh/max sei an Opus 4.7 gebunden bzw. der tiefste Default. Laut Persona-Recherche: Opus 4.8 defaultet auf effort=high auf allen Surfaces (API + Claude Code); xhigh/max existieren weiter, sind aber NICHT mehr Default und muessen explizit gesetzt werden. Betroffene verifizierte Stellen: block-1-foundations.md Z.169 ('xhigh and max unlock the deepest reasoning with Opus 4.7') und Z.1018 ('xhigh | ... (Opus 4.7 only) | 4x') und Z.1033 (Plan-Phase 'Opus 4.7 | xhigh'); cheatsheet.md Z.317 ('xhigh and max available on Opus 4.7'); faq.md Z.201 (Effort-Eintrag). Umformulieren z.B.: 'low|medium|high|xhigh|max — five tiers; Opus 4.8 defaults to high (xhigh/max unlock even deeper reasoning when explicitly set).' Die 'Opus 4.7 only'-Beschraenkung bei xhigh streichen — xhigh ist auch auf Opus 4.8 (und Fable 5) verfuegbar.

- **Dateien:** resources/modules/block-1-foundations.md; resources/cheatsheet.md; resources/faq.md
- **Begruendung:** Sachliche Korrektheit mit Kosten-Relevanz: Wer glaubt, der Default sei xhigh, fuerchtet unnoetig hohe Kosten; wer xhigh fuer 'Opus-4.7-only' haelt, nutzt das Modell falsch. Effort-Steuerung ist eine Kern-Lektion (Modul 1.3/1.5).
- **Akzeptanz:** Keine Stelle bindet xhigh/max ausschliesslich an Opus 4.7. Mindestens eine Stelle sagt explizit, dass Opus 4.8 auf high defaultet. Die Cost-Engineering-Tabelle (Z.1018/1033) ist konsistent.
- **Quelle:** Currency-Auditor: Modelle, Preise, Effort-Stufen; Currency-Auditor: CLI, Flags, Commands, Versionen
- **Abhaengig von:** Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28)

#### T-040 — /model fable Command und Fast-Mode in cheatsheet & quick-reference dokumentieren  `[P2 | S]`

Zwei CLI-Aktualisierungen fuer die Referenzkarten. (1) /model fable: cheatsheet.md Z.163 ('/model <name> | Switch model (opus, sonnet, haiku)') auf '(opus, sonnet, haiku, fable)' erweitern, plus CLI-Flag-Section ein Eintrag 'claude --model fable (Fable 5, seit v2.1.170)'; quick-reference.md analog. (2) Fast-Mode: Laut Persona-WebSearch existiert seit v2.1.142 ein Fast-Mode (claude --fast / --model fast) = Opus 4.8 mit ~2.5x Geschwindigkeit bei ~1/3 der Kosten frueherer Fast-Tiers; auto-mode bei --fast deaktiviert. Eintrag in cheatsheet.md (Flags-Section) und quick-reference.md hinzufuegen. VORHER Versionsnummern (v2.1.142, v2.1.170) und Fast-Mode-Pricing-Claim per WebSearch verifizieren — diese stammen aus Persona-Recherche und sind nicht im Repo belegt.

- **Dateien:** resources/cheatsheet.md; resources/quick-reference.md
- **Begruendung:** Komfort/Vollstaendigkeit der Referenzkarte: Die Befehle sind nuetzlich, aber kein Blocker fuer den Lernpfad. Folgt aus den Modell-Updates.
- **Akzeptanz:** cheatsheet und quick-reference listen /model fable und den Fast-Mode mit verifizierter Versionsangabe. Keine unbelegten Versionsnummern.
- **Quelle:** Currency-Auditor: CLI, Flags, Commands, Versionen
- **Abhaengig von:** Claude Fable 5 (Mythos-Klasse, GA 2026-06-09) in alle Modelltabellen aufnehmen

#### T-041 — Hook-Event-Count '28 lifecycle events' korrigieren oder vage formulieren  `[P2 | S]`

block-2-ecosystem.md Z.387 (verifiziert): 'The official docs currently list 28 lifecycle events. We focus on the 11 you will reach for most often.' Laut Persona-WebSearch liegt die tatsaechliche Zahl eher bei ~24-25 und variiert zwischen Releases. Da eine harte Zahl bei jedem Release veraltet, ist die robusteste Loesung eine vage Formulierung: 'over 20 lifecycle events' statt '28'. Alternativ die exakte aktuelle Liste eintragen — das erhoeht aber den Pflegeaufwand. Empfehlung: vage Formulierung. Die '11 wichtigsten'-Auswahl bleibt unveraendert.

- **Dateien:** resources/modules/block-2-ecosystem.md
- **Begruendung:** Sachliche Aktualitaet, geringe Lernerfolgs-Auswirkung: Die Zahl ist Hintergrund, nicht Pruefstoff. Eine vage Formulierung macht die Stelle release-robust.
- **Akzeptanz:** Z.387 nennt keine exakte, leicht veraltbare Zahl mehr (entweder 'over 20' oder eine verifizierte aktuelle Zahl). Die Fokus-auf-11-Aussage bleibt erhalten.
- **Quelle:** Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

#### T-042 — Zentralen Versions-/Stand-Anker einfuehren; divergierende Stand-Daten konsolidieren  `[P2 | S]`

Die Stand-Daten divergieren ohne zentralen Anker: faq.md Z.5, glossary.md Z.5, troubleshooting.md Z.6, WORKSHOP_EINFUEHRUNG.md Z.69 tragen 'Stand: 2026-05-20'; prerequisites.md Z.205 'Last Updated: 2026-04-03'; README/CLAUDE.md tragen kein Stand-Datum. Block-1-foundations.md Z.950 'Pricing Reference (as of 2026-05)'. Massnahme: EINEN Versionsanker definieren (z.B. eine Zeile/VERSION-Feld in README oder einem zentralen Dokument) mit Workshop-Stand-Datum + getesteter Claude-Code-Version, und die Einzeldateien darauf verweisen statt acht separate Stand-Zeilen zu pflegen. Bei dieser Gelegenheit alle Stand-Daten auf den Update-Tag heben. Hinweistext ergaenzen: 'Modellnamen und Versionen koennen sich aendern — pruefe /model, /release-notes und claude --version gegen dein Material.' Hilft dem Solo-Lerner, Diskrepanzen einzuordnen statt verunsichert zu werden.

- **Dateien:** README.md; resources/prerequisites.md; resources/faq.md; resources/glossary.md; resources/troubleshooting.md; resources/WORKSHOP_EINFUEHRUNG.md
- **Begruendung:** Einstiegshuerde/Orientierung: Acht verschiedene Stand-Zeilen erschweren dem Solo-Lerner die Einschaetzung der Aktualitaet. Ein zentraler Anker plus 'pruefe selbst'-Hinweis senkt Verunsicherung — daher ueber reinem Komfort, aber unter den Faktenkorrekturen.
- **Akzeptanz:** Es existiert genau ein Versions-/Stand-Anker, auf den die Einzeldateien verweisen. Kein Stand-Datum liegt mehr im April 2026, sofern beim Update angefasst. Ein 'pruefe /model & claude --version'-Hinweis ist vorhanden.
- **Quelle:** Tom — Selbstlerner, arbeitet das Repo allein durch (kein Moderator)

#### T-043 — Prerequisites: Mindest-CLI-Version und Update-Hinweis aufnehmen  `[P2 | S]`

Die Setup-/Prerequisites-Doku nennt keine Mindest-CLI-Version, obwohl mehrere Workshop-Features Version-Gates haben (z.B. --plugin-dir v2.1.128+, --plugin-url v2.1.129+) und Advanced-Features neuere Versionen brauchen (Fable 5 v2.1.170+, Dynamic Workflows v2.1.154+). Ergaenzen in prerequisites.md (und ggf. session-plan.md): 'Mindestens Claude Code v2.1.154+ empfohlen; einige Advanced-Features (Fable 5, Dynamic Workflows) brauchen v2.1.170+. Update mit `claude update`, pruefen mit `claude --version`.' Generische Formulierung bevorzugen ('aktuelle Version finden Sie mit claude --version'), damit die Angabe nicht selbst schnell veraltet. Die exakte aktuelle Version (laut Persona-WebSearch v2.1.185, Stand 2026-06-20) nur als 'oder neuer' nennen, nicht hart einfrieren.

- **Dateien:** resources/prerequisites.md; resources/session-plan.md
- **Begruendung:** Einstiegshuerde: Ein Teilnehmer mit alter CLI scheitert sonst still an Features, ohne die Ursache zu kennen. Praeventiver Setup-Hinweis spart Frust — aber kein akuter Blocker fuer den Hauptpfad.
- **Akzeptanz:** prerequisites.md nennt eine Mindest-CLI-Version + claude update / claude --version Hinweis. Keine hart eingefrorene 'aktuelle' Version ohne 'oder neuer'.
- **Quelle:** Currency-Auditor: CLI, Flags, Commands, Versionen; Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

#### T-076 — SSE-MCP-Deprecation-Kontext und Scope-Renaming-Warnung schaerfen  `[P3 | S]`

Zwei kleinere Ecosystem-Praezisierungen in block-2-ecosystem.md, die inhaltlich bereits korrekt, aber zu knapp sind. (1) SSE-Transport (Z.926, Tabelle '| SSE | ... | (legacy) | Deprecated — use HTTP instead |'): einen Satz Kontext ergaenzen, warum/wann: 'SSE is deprecated as of Q1 2026 in favor of Streamable HTTP, which offers better resource efficiency and does not require HTTP/2.' (2) MCP-Scope-Renaming (Z.933-939, local/project/user mit Hinweis auf alte Namen project/global): Die Warnung vor die Tabelle ziehen und hervorheben: 'NAMING CHANGE (2025): Old docs say project scope / global scope — these were renamed. Current standard: local/project/user. Translate 2024-era docs accordingly.' Beides ist Komfort/Klarheit, keine Fehlerkorrektur.

- **Dateien:** resources/modules/block-2-ecosystem.md
- **Begruendung:** Komfort: Material ist bereits korrekt, die Ergaenzungen verbessern nur Verstaendlichkeit/Einordnung gegenueber veralteten Fremd-Docs. Niedrigste der umsetzungswuerdigen Prioritaeten.
- **Akzeptanz:** SSE-Tabelle hat einen Begruendungssatz (Q1-2026-Deprecation + Streamable-HTTP-Vorteil). Die Scope-Renaming-Warnung steht sichtbar vor der Tabelle.
- **Quelle:** Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

#### T-085 — Neue Features als Kurz-Notizen ergaenzen: Dynamic Workflows, Lean System Prompt, ultracode  `[P3 | M]`

Drei neuere Features, die der Workshop noch nicht erwaehnt (laut Persona-WebSearch). (1) Dynamic Workflows (v2.1.154+): In Module 3.1 (Agents & Orchestration) ein kurzes Unterkapitel — ein einzelnes Opus-4.8-Modell kann hunderte parallele Subagents koordinieren; Command /workflows; Abgrenzung zum bisher gezeigten Fan-Out/Fan-In (~5-10 Agenten). Didaktisch relevant fuer Session 3, aber zeitlich knapp — daher als optionale Vertiefung. (2) Lean System Prompt (Default seit v2.1.154 fuer Opus 4.8+): kurze Notiz in Module 1.1 oder 1.2 — komprimierter System-Prompt spart Context-Overhead; --append-system-prompt / --system-prompt zum Uebersteuern. (3) ultracode (Research Preview seit v2.1.154): nur als Fussnote in Block 3 neben den bereits erwaehnten /ultraplan und /ultrareview — niedrige Relevanz, da experimentell. Alle Versionsnummern und Feature-Claims VORHER per WebSearch verifizieren.

- **Dateien:** resources/modules/block-3-advanced.md; resources/modules/block-1-foundations.md; resources/modules/block-2-ecosystem.md
- **Begruendung:** Komfort/Vollstaendigkeit: Nice-to-have-Aktualisierungen, die den Kurs auf Frontier-Stand bringen, aber den Kern-Lernpfad nicht blockieren. Dynamic Workflows ist die wichtigste der drei; ultracode die am ehesten verzichtbare.
- **Akzeptanz:** Dynamic Workflows ist in Module 3.1 als optionale Vertiefung mit Command /workflows beschrieben. Lean System Prompt ist als Kurz-Notiz in Block 1 erwaehnt. ultracode steht als Research-Preview-Fussnote in Block 3. Alle Versionsangaben verifiziert.
- **Quelle:** Currency-Auditor: CLI, Flags, Commands, Versionen
- **Abhaengig von:** Modell-Default global aktualisieren: Opus 4.7 -> Opus 4.8 (Default seit v2.1.154, 2026-05-28)

#### T-077 — Haiku-Kontextgrenze (200K vs 1M) mit Konsequenz-Footnote versehen  `[P3 | S]`

block-1-foundations.md Z.164 ('Claude Haiku 4.5 | 200K tokens') vs Z.162 (Opus 1M). Die Implikation (Haiku kann weniger auf einmal lesen) ist nicht ausgesprochen. Kurze Footnote ergaenzen: '200K context limits bulk-read tasks — use Haiku for small/focused reads, Opus/Fable for whole-codebase analysis.' Reines Verstaendnis-Plus, nicht essentiell fuer Anfaenger, hilft aber beim Troubleshooting ('warum bricht Haiku bei grossen Reads ab').

- **Dateien:** resources/modules/block-1-foundations.md
- **Begruendung:** Komfort: Kleine didaktische Ergaenzung ohne Aktualitaets- oder Korrektheitsdruck. Niedrigste Prio.
- **Akzeptanz:** Eine Footnote bei der Modelltabelle erklaert die praktische Konsequenz der 200K-Grenze von Haiku.
- **Quelle:** Currency-Auditor: Modelle, Preise, Effort-Stufen
- **Abhaengig von:** Claude Fable 5 (Mythos-Klasse, GA 2026-06-09) in alle Modelltabellen aufnehmen
