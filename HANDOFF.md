# HANDOFF — Umsetzung des Workshop-Reviews (Stand 2026-06-21)

> **Für die nächste Instanz (Claude Code ODER Codex ODER ein anderer Agent).**
> Dieses Dokument ist selbsterklärend — du brauchst keinen Kontext aus der vorigen Session.
> Lies es ganz, bevor du etwas änderst.

---

## 0. FORTSCHRITT — START HIER (Stand: 2026-06-22)

**Wellen A + B + C + D + E + F sind erledigt und committet. NÄCHSTER EINSTIEG: Playground-Korrektheit & Übungs-Qualität.**

- **Welle F (Restrukturierung, `restructuring`-Cluster) — User-Entscheidung 2026-06-23: 4 Sessions.** Die 17 Module sind jetzt auf **65 Lerneinheiten (LE)** über **4 Sessions** abgebildet (Block 3 → Session 3 Kern + Session 4 Bonus). Umgesetzt: `session-plan.md` komplett neu (4-Session-/65-LE-Landkarte, core/deep-dive/bonus, ehrliche Roh-Core-Minuten, Exercise-Mapping); LE-Navigationsblock am Kopf jeder `modules/block-*.md` (LE↔Section↔Level, robust statt fragiler Inline-Anker); `workshop-mentor.md` auf LE-Granularität + 4-Session-Map; Cost-Verschiebung (S1.19 Basics in S1, Rest → S4.4 bei CI) in cheatsheet + quick-reference gespiegelt; nutzerseitige Struktur-Refs auf 4 Sessions (`CLAUDE.md`, `AGENTS.md`, `README.md`, `WORKSHOP_EINFUEHRUNG.md`, `workshop-guide.md`, `skills/workshop/SKILL.md`-Banner). **User-Entscheidungen:** S1.6 (alle 6 Permission Modes) = `[core]` (Audience-Fit, ggü. Vorschlag), Cost verschieben (nicht nur degradieren), deep-dives „wenn Zeit, zeigen", feinste Granularität (Vorschlags-Label „48", real 65 LEs inkl. 3 Hands-on-Puffer). **Bewusst NICHT angefasst:** `video-scripts.md` („drei Sessions" = Transkript bereits aufgenommener Videos → keine Recording-Drift). Playground-Tests 18/18 grün.
- **`aee9a76` — Welle E (Demo-Robustheit & Live-Sicherheit, `demo-reliability`-Cluster):** T-016 (broken-greeter/SKILL.md als fertiges Asset unter `resources/demos/assets/broken-greeter/` + Copy-Befehl in Demo 3.7), T-014 (Demo 3.6 als garantierter Live-Anker + 60-Sek-Block-3-Opener), T-015 (Exercise 3.3 built-in-`/security-review`-Fallback ohne Plugin), T-002 (Exercise 3.6 in isoliertes `~/cc-workshop/exercise-3.6`-Sandbox-Repo statt git-init-im-Playground; T-001 `--max-turns` war schon in A/B raus), T-027 (Go/No-Go-Demo-Matrix in trainer-notes), T-044 (Demo 3.4 Budget-Cap vor `/run-loop` + `/cost`), T-045 (Demo 3.3c Ein-Befehl-`git checkout`-Cleanup + pip-Warnung), T-078 (Demo-Zeit-Hinweis + Bonus-Markierung session-plan). Mentor nachgezogen. Tests 18/18 grün. **Codex-Verifier auf Welle D** (`aa58d28`): 3.3-Split-Downstream-Drift in session-plan + SKILL.md-Overview-Box gefixt.
- **`d22d051` — Welle D (Didaktik & Einstiegshürde, `didactics-onboarding`-Cluster):** T-006 (Hello-Claude-Code-Hands-on vor Overview von Modul 1.1), T-017 (Lernziele 1.1 leicht→schwer), T-047 (Tools-Tabelle auf 6 Kern-Tools), T-048 (Header "NEW to coding agents"), T-028 (Modul 1.2 Kern/Vertiefung via Deepening-Banner), T-046 (Privacy-Block gekürzt), T-065 (Block-2/3-Vorgriffe als Outlook-Teaser), T-066 (Modul 1.5 optional, 5-Min-Kern), T-067 (Modul 3.3 → 3.3a Adversarial / 3.3b Hardening&Compliance gesplittet), T-029 (SKILL.md Learn-Mode-Preflight für Plugin-Module), T-050 (README Selbstlern-Pfad), T-068 (17-Modul-Fortschritts-Checkliste in workshop-guide), T-051 (Micro-Übung 1.0), T-052 (Pairing-Fallback). T-049 war schon durch Welle B. Mentor-Modul-Map nachgezogen. Tests 18/18 grün. **Codex-Verifier auf Welle C** (`28ec8f7`): fand Exercise-Numerierungsversatz (Hook-Übung=2.2 nicht 2.1, aus Backlog geerbt) → 5 Cross-Refs + prereq-check gefixt.
- **`d02b046` — Welle C (Windows-Tauglichkeit, kompletter `windows-compat`-Cluster + T-019):** T-007 (getestete Hook-Assets `resources/demos/assets/hooks/secure-diff-gate.{sh,py}` — block .env/.pem/secrets/credentials=exit 1, normal=exit 0, .py jq-frei; `.gitattributes` erzwingt LF für `*.sh`), T-036 (Exercise 2.1 safety-check + audit-log mit PowerShell-`.ps1`-Variante neben bash, live gegen powershell.exe getestet), T-021 (bash-vs-pwsh-Widerspruch aufgelöst), T-035 (prerequisites Hook-Setup PowerShell-Block), T-022 (trainer-notes Pre-Flight Windows-first), T-019 (Cheatsheet „Hooks on Windows"-Box), T-061 (MCP-Config `python`), T-072 (Windows-Vorspann in allen 3 Exercise-Dateien + Exercise 1.1 bash+pwsh), T-073 (API-Key/export/echo-e PS-Formen, CI-`/tmp/` als Linux-Runner klargestellt), T-083 (C-Playground compile-frei geframed). Mentor-Agent um Windows-Referenz + FAQ ergänzt. Playground-Tests 18/18 grün.

→ **Weiter mit Playground-Korrektheit & Übungs-Qualität** (für die CySec-Zielgruppe der höchste Glaubwürdigkeits-Hebel):
- **`accuracy-overclaim` OSDP/C-Playground — ✅ ERLEDIGT (2026-06-23):** `T-003` (hex-Parser-`size_t`-Underflow in main() gehärtet, Guard non-empty+even), `T-008` (Frame-Format ehrlich: Header-Disclaimer ADDR-vor-16-bit-LEN + CRC-16/CCITT, SIA OSDP v2.2; struct als simplified-teaching markiert), `T-062` (V2 = echter `uint8_t`-Wrap statt „765 (fine)"-Widerspruch), `T-037` (Zeilennummern raus, Funktionsnamen), `T-070` (V4 `parse_address`→`read_frame_crc`, CRC-Tail-Off-by-one statt konstruiertem raw[5]) — in `osdp_frame_decoder.c` + `workshop-playground/CLAUDE.md` + `block-3-demos.md` (Expected-findings). V1+V3 unangetastet, pytest 18/18 grün. **✅ Auch erledigt (2026-06-23, Doku-Mini-Welle):** `T-010` (acceptEdits-Tabelle Block 1: FS-Bash rm/mv/mkdir/touch wird auto-approved, Verweis Modul 3.3), `T-023` (Frontmatter geklärt via claude-code-guide gegen offizielle Docs: Subagent-Modell = `model:`, KEIN `agent:`; `context: fork` + `agent: <typ>` sind offizielle **Skill**-Felder, `agent` = Subagent-TYP nicht Modell — block-2 Beispiel+Tabelle+Official-Fields, cheatsheet korrigiert), `T-024` (Demo-3.7-Trace-Zeilen als sinngemäß/Wortlaut-variiert gekennzeichnet + Pre-Session-Verifikation gefordert). **Damit accuracy-overclaim weitgehend durch** (Rest: Currency-T-063 u.a. unter Currency-Reste).
- **`exercise-quality` — ✅ P1+P2 ERLEDIGT (2026-06-23):** `T-030` (Exercise 2.2 Step 1: gefährliches `echo '{}' >`-Overwrite gehärtet zu create-if-missing + Backup + projektlokale-`.claude/settings.json`-Option; Merge/`json.tool`-Hinweise in 2.2 Bonus + block-3 Write|Edit ergänzt), `T-018` (Exercise 3.3 Step 4: Fix nur lokal, `git checkout -- access_control.py`, Konflikt zur „Do NOT fix"-Regel aufgelöst), `T-069` (3.3: ADMIN_PASSWORD = dead code → Defender kann es als unreachable/low-severity einstufen; „confirm three" zur Reachability-Diskussion entschärft), `T-053` (Exercise 1.2 Pushback wahrscheinlichkeitsbasiert + Hook=hartes Gate), `T-055` (1.2 neuer 30-Sek-In-Session-Verifikationsschritt vor Restart, Steps renummeriert), `T-054` (prerequisites Struktur-Baum auf echten Clone-Pfad `~/cc-workshop/dynamic-workshop/workshop-playground`). access_control.py unberührt (Vulns intakt), pytest 18/18. **✅ P3 auch erledigt (2026-06-23):** `T-081` (Log-Injection in Exercise 3.3 + playground-CLAUDE.md vom „Bonus" zur regulären **EN-50131-Audit-Trail-Integritäts-Vuln** aufgewertet, Querverweis auf Compliance-Tabelle block-3-advanced.md:819), `T-082` (Block-2-Exercises-Zeitbudget ehrlich auf 30–40 Min + Kern/Bonus-Trennung + Restart/npx-Hinweis; **Playwright-MCP-Preinstall** als Vorab-Schritt in prerequisites.md → Exercise 2.4 lädt nicht mehr live).
- **`missing-content`/`new-exercise-idea`:** **✅ `T-031` ERLEDIGT (2026-06-23):** fail-open-Domänen-Logik-Vuln im Python-Playground — neue `check_access_resilient()` + `door-check`-Subcommand in `access_control.py` (bei fehlender/korrupter `users.json` → ACCESS GRANTED statt DENIED; Scanner findet sie nicht, erreichbar & empirisch bewiesen: `door-check eve` ohne DB = GRANTED exit 0 vs `check` = DENIED exit 1). Dokumentiert in `workshop-playground/CLAUDE.md` (#5 domain-logic, do-NOT-fix) + Exercise-3.3-„For the CySec Engineer"-Challenge (Scanner-vs-Domänenkompetenz; bewusst NICHT in der Setup-Liste = kein Spoiler). 18/18 grün. **✅ `T-032` ERLEDIGT (2026-06-23):** neue geführte **Exercise 3.9** „Build a Domain Parser the Right Way (OSDP/Wiegand)" (Should-do, Format wie 3.6, Varianten A=OSDP-Frame-Parser-Hardening / B=Wiegand-26-TDD, Anbindung an osdp_frame_decoder.c, TDD+Multi-Agent); Priority-Guide + Capstone-3.5-Verweis + workshop-mentor.md nachgezogen. **Offen:** die übrigen ~16 „wild"-Übungen aus `05`/`05b` integrieren (Micro-Warmups/CTFs/Rollenspiele — entscheidungslastig: welche rein, wohin in die LE-Struktur; mit User scopen).
- **Currency-Reste:** `T-040/042/043/063/076/077/085`.

**Welle F (Restrukturierung / 65 Lerneinheiten) ist erledigt** (User-Entscheidung 2026-06-23: 4 Sessions — siehe oberster Bullet).

⚠️ **Playground-Tests vor/nach OSDP-C-Änderungen:** Die 3 absichtlichen Vulns sind Lehr-Material — NICHT „fixen" (außer ein TODO sagt explizit härten/dokumentieren, z.B. T-003). `python -m pytest -q` in `workshop-playground/` muss grün bleiben (18 Tests, harmlos, kein Prod-DB-Risiko).

---

### Frühere Wellen (erledigt)

Erledigt (3 Commits auf `main`, **nicht gepusht** — Push = User):
- **`4dca782` — Welle A (Quick Wins):** T-001 (`--max-turns` aus Exercise 3.6, Flag existiert nicht in CLI v2.1.185), T-004 („Three Interfaces"→„Five Surfaces"), T-005 (python3/pip3 + Windows-Variante), T-009 (worktree.baseRef-Widerspruch vereinheitlicht → „versionsabhängig, explizit setzen"), T-011 („Opus 4.6" entfernt), AGENTS.md-Bug („Codex"→„Claude Code" + tote Ref `deep-research-gap-analysis.md` aus AGENTS.md **und** CLAUDE.md).
- **`e5346f5` — Welle B/1 (Modell-Currency):** T-025 (Opus 4.7→**4.8** als Default), T-026 (**Fable 5** GA 2026-06-09, `claude-fable-5`, $10/$50 in allen Modelltabellen), T-013 (Effort-Default = **`high`** auf Opus 4.8; `xhigh`/`max` auf 4.7/4.8/Fable 5), T-040 (`/model fable` + Fast Mode `/fast`), T-012 (Mentor-Agent). **Alles gegen platform.claude.com-Docs + Live-CLI verifiziert.**
- **`b42a762` — Welle B/2:** `--max-turns` workshop-weit entfernt (existiert nicht in der CLI; ersetzt durch ehrlichen Hinweis „`--max-budget-usd` cappt Loops"), T-041 (28 lifecycle events → vage), HTML-Dashboard „Opus 4.6"→„4.8".

**Verifizierte Fakten für künftige Currency-Arbeit** (nicht neu recherchieren): aktuelles Lineup = Fable 5 / Opus 4.8 (Default) / Opus 4.7 / Sonnet 4.6 / Haiku 4.5; Effort-Default `high` auf Opus 4.8; Fast Mode `/fast` (Opus 4.8/4.7). Live-CLI = **v2.1.185**.

**Wichtig:** `resources/review-2026-06-21/` ist das **historische Review-Archiv** — NIE editieren (auch wenn grep dort alte Begriffe wie „Opus 4.7"/„--max-turns" findet). Das sind die Befunde selbst, kein Kursinhalt.

(Der `windows-compat`-Cluster wurde in Welle C abgeschlossen — siehe oben.) **Welle F (Restrukturierung / 65 Lerneinheiten) ist erledigt** (User-Entscheidung 2026-06-23: 4 Sessions).

---

## 1. Kontext (worum geht es)

Dieses Repo ist der **Dynamic Workshop** — eine praxisnahe Claude-Code-Schulung (4 Sessions à ~3h,
17 Module → 65 Lerneinheiten) für 3 erfahrene Entwickler aus Physical Security (Zutrittskontrolle, Alarmsysteme).
Session 1 wurde am 10.04.2026 durchgeführt; Sessions 2–4 stehen aus. Das Repo dient auch
Selbstlernern und ist gleichzeitig ein Claude-Code-Plugin.

Am 2026-06-21 wurde der gesamte Kurs per Multi-Agent-Review aus 12 Perspektiven durchgespielt.
Das Ergebnis liegt vollständig vor unter **`resources/review-2026-06-21/`**. Es wurde **bewusst
noch nichts am Kursinhalt geändert** — das ist deine Aufgabe.

## 2. Deine Aufgabe (Mission)

Setze das priorisierte TODO-Backlog aus dem Review um — in der unten empfohlenen Reihenfolge,
in Wellen, mit Verifikation vor jeder Änderung. Ziel: den Workshop aktueller, einsteigerfreundlicher
und Windows-tauglich machen, ohne Inhalt zu verlieren.

## 3. Wo alles steht (lies in dieser Reihenfolge)

| Datei | Zweck |
|---|---|
| `resources/review-2026-06-21/01-executive-summary.md` | Gesamturteil, Top-Themen, Quick Wins, Roadmap |
| `resources/review-2026-06-21/02-todo-backlog.md` | **Arbeitsliste: 87 TODOs (T-001…T-087), P0–P3, mit Datei + Akzeptanzkriterium** |
| `resources/review-2026-06-21/03-currency-report.md` | Aktualitäts-Befunde **mit Web-Quellen** (Modelle/CLI/Ecosystem) |
| `resources/review-2026-06-21/04b-restructuring-proposal-v2.md` | Granularer Re-Split (17 Module → 65 LE; 04b nennt sie irrtümlich „48") — **ERLEDIGT in Welle F** |
| `resources/review-2026-06-21/05-new-exercises.md` + `05b-…welle-2.md` | 18 neue Übungen, fertig formuliert |
| `resources/review-2026-06-21/07-curator-addenda.md` | **Wichtig:** manuelle Korrekturen + verifizierte Bugs |
| `resources/review-2026-06-21/06-all-findings.md` | Anhang: alle 129 Roh-Befunde nach Persona |
| `resources/review-2026-06-21/data/todos.json` | Maschinenlesbares Backlog (falls du es programmatisch verarbeiten willst) |

## 4. Empfohlene Umsetzungs-Reihenfolge (Wellen)

**Welle A — Quick Wins (P0/P1, Aufwand S). Zuerst, niedrig-Risiko:**
- `T-001` 🔴 **Blocker:** `--max-turns` aus Übung 3.6 entfernen (Flag existiert in der CLI nicht — **erst mit `claude --help` gegenprüfen**).
- `T-004` Überschrift „The Three Interfaces" → fünf Surfaces korrigieren.
- `T-005` `python3`/`pip3` im Haupttext um Windows-Variante (`python`/`pip`) ergänzen.
- `T-009` `worktree.baseRef`-Default-Widerspruch (`head` vs `fresh`) vereinheitlichen.
- `T-011` veraltete Modellversionen (z.B. Opus 4.6) korrigieren.
- **AGENTS.md-Bug** (Addendum A): „Codex" → „Claude Code" (Zeilen 5/7) + tote Referenz `deep-research-gap-analysis.md` entfernen (Addendum B).

**Welle B — Currency-Sweep (P1, meist M):**
- `T-025` Opus 4.7 → Opus 4.8 (Default seit v2.1.154 / 2026-05-28) global.
- `T-026` Claude Fable 5 (GA 2026-06-09) in alle Modelltabellen.
- `T-012`/`T-013` Mentor-Agent + Effort-Default nachziehen.
- ⚠️ **Vor dem Edit:** alle Versions-/Datumsangaben (v2.1.154, Fable-5-GA usw.) noch einmal gegen die laufende CLI und die offiziellen Docs (`code.claude.com/docs`) verifizieren — sie stammen aus Persona-Web-Recherchen.

**Welle C — Windows-Tauglichkeit (Cluster `windows-compat`):**
- `T-007` getestetes Hook-Asset (bash **und** PowerShell-Variante) ins Repo legen.
- `T-019`/`T-021`/`T-022` Cheatsheet/Exercises/Trainer-Notes auf Windows umstellen.

**Welle D — Didaktik & Einstiegshürde (Cluster `didactics-onboarding`/`structure`):**
- `T-006` „Hello, Claude Code"-Erfolgserlebnis an den Anfang von Modul 1.1.
- `T-017` Lernziele 1.1 vom Leichten zum Schweren sortieren.
- `T-028` Modul 1.2 in Kern + Vertiefung splitten.

**Welle E — Übungen & Demos:** neue Übungen aus `05`/`05b` einpflegen, Demo-Robustheit (`T-014`–`T-016`, `T-027`).

**Welle F — Restrukturierung: ERLEDIGT (2026-06-23, 4 Sessions).** `04b` ist in den neuen `session-plan.md` (4 Sessions / 65 LE) gegossen; Details siehe Abschnitt 0 (oberster Bullet).

## 5. Harte Randbedingungen (nicht verletzen)

- **Verifikation vor Aktion:** Jede Currency-Behauptung vor dem Edit gegen Live-CLI/Docs prüfen. Nicht blind den Persona-Web-Daten vertrauen.
- **Projektregel (`CLAUDE.md` / `AGENTS.md`):** Bei JEDER Inhaltsänderung an Modulen/Demos/Exercises auch `agents/workshop-mentor.md` aktualisieren (Modul-Map, Modellangaben).
- **Sprache:** Deutsch für Kommunikation/Prosa, Englisch für Code/Identifier/Dateinamen. Vollständige Umlaute/Diakritika.
- **Windows-Umgebung:** Der Maintainer arbeitet auf Windows 11 / PowerShell. Hook-Skripte, Befehle und Exercises brauchen PowerShell-taugliche Varianten (kein blindes `bash`/`jq`/`chmod`/`sed -i`).
- **Playground-Tests:** Falls du `pytest` im `workshop-playground/` laufen lässt — die Tests dort sind harmlos (kein Production-DB-Risiko), aber prüfe das `conftest`/Setup, bevor du destruktive Test-Schritte ausführst.
- **Git:** chirurgisch stagen (`git add <pfad>` einzeln, **kein** `git add -A`). Commit/Push nur auf ausdrückliche Anweisung des Users. Nicht auf `main` committen ohne Freigabe.
- **Die 3 absichtlichen Vulnerabilities** in `workshop-playground/access_control.py` und die in `osdp_frame_decoder.c` sind **Lehr-Material** — NICHT „fixen" (außer ein TODO sagt explizit, eine *zusätzliche, ungeplante* Schwäche zu dokumentieren, z.B. `T-003`).

## 6. Was du NICHT tun sollst

- Keine großflächigen Umschreibungen ohne TODO-Bezug. Arbeite TODO für TODO, mit Akzeptanzkriterium.
- ~~Die Restrukturierung (`04b`) nicht eigenmächtig umsetzen — braucht User-Entscheidung (3 vs 4 Sessions).~~ **Erledigt (Welle F, 2026-06-23, 4 Sessions).**
- Den degenerierten `04-restructuring-proposal.md` (nur ein Redirect-Stub) nicht als Vorlage nehmen — nutze `04b`.

## 7. Deliverable & Erfolgskriterien

- Pro umgesetztem TODO: Änderung erfüllt das im Backlog genannte **Akzeptanzkriterium** (oft ein konkretes `grep`).
- `agents/workshop-mentor.md` ist nach Inhaltsänderungen konsistent.
- Playground-Tests laufen weiterhin grün.
- Kurzer Fortschrittsbericht je Welle (welche TODO-IDs erledigt, welche verifiziert).

## 8. Hinweis speziell für einen Codex-Agenten

`AGENTS.md` im Root ist aktuell **fehlerhaft** (nennt „Codex" als Workshop-Thema — das ist ein Bug, siehe `T`/Addendum A; der Workshop behandelt **Claude Code**). Bis dieser Bug behoben ist: behandle **`CLAUDE.md`** als Source of Truth für Projektkontext, nicht `AGENTS.md`. Dieses `HANDOFF.md` und `resources/review-2026-06-21/` sind tool-neutral und für dich genauso gültig.

---
*Erstellt am 2026-06-21 als Abschluss der Review-Session (Workflow-Run `wf_1603866b-421`).*
