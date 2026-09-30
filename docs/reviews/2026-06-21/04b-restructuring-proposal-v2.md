# Restrukturierungs-Vorschlag v2 — Granulare Feingliederung

## Kernidee & Design-Prinzipien

- **Lerneinheit (LE) statt Modul.** Die heutigen 17 Module werden in **48 kleine, in sich abgeschlossene Lerneinheiten** (Richtwert 10-25 Min) zerlegt. Jede LE hat 1-3 klare Lernziele und endet an einer natuerlichen "ich kann jetzt X"-Grenze.
- **Drei Schichten pro Thema.** Jede LE traegt ein Level:
  - `[core]` — Pflichtpfad. Was jeder Teilnehmer koennen muss. Der Core-Pfad einer Session passt garantiert in <=150 Min.
  - `[deep-dive]` — optionale Vertiefung **desselben** Themas (z.B. erst "die 6 Permission Modes", dann als deep-dive "auto/dontAsk/bypass im Detail"). Wird gezeigt, wenn Zeit/Interesse da ist.
  - `[bonus]` — Kuer/Showcase, oft die `:wrench:`-Custom-Komponenten und experimentellen Features.
- **Sanfter Einstieg, harte Themen spaeter.** Die ersten 3 LEs (S1) sind fuer einen kompletten Agent-Neuling muehelos: "Was ist ein Coding Agent", "Bau sofort eine Datei", "die drei Oberflaechen". Permission Modes, Modellwahl und Kosten kommen erst, wenn das Grundvertrauen sitzt.
- **Cost Engineering wird entzerrt.** Das heutige Modul 1.5 (5. Modul am ersten Tag, sehr dicht) wird aufgeteilt: ein schlanker `[core]`-Teil ("die drei Spend-Befehle + Budget-Cap") bleibt in Session 1, der Rest (Pipeline, Caching, Insights-Deep-Dive) wandert in einen `[deep-dive]`-Block und wird in Session 3 (CI/Headless) wieder aufgegriffen, wo Budget-Caps ohnehin Pflicht sind. Begruendung unten.
- **Block 3 wird ehrlich gesplittet.** Block 3 ist mit 7 Modulen die dichteste Session. Vorschlag: **Session 3a (Kern: Agents + Security + Automation)** und **Session 3b (Bonus-Track: Multi-Model, CI/CD, Capstone, Troubleshooting)**. Wer nur 3 Termine will, fuehrt 3a als Pflicht und 3b als optionalen 4. Termin / Selbststudium. Details unten.
- **Didaktik bleibt.** Demo > Slides, durchgaengige Physical-Security-Analogien, optionale Exercises — alles erhalten. Jede Session startet weiterhin visuell mit der PPT.
- **Nichts geht verloren.** Jede LE traegt eine `aus (alt)`-Spalte, die auf das speisende Modul/den Abschnitt zeigt. Der Abdeckungs-Nachweis unten zeigt: alle 17 Module sind vollstaendig auf LEs abgebildet.

---

## Neue Session-/Einheiten-Landkarte

### Session 1 — Erste Schritte mit dem Agenten (sanfter Einstieg)

> Mission: "Was ist Claude Code, wie steuere ich es, wie arbeite ich sicher mit Git — und behalte die Kosten im Blick."

| Einheit | Titel | Level | Min | Lernziel(e) | aus (alt) |
|---|---|---|---|---|---|
| S1.1 | Coding Agent vs. Chat — das mentale Modell | core | 12 | Verstehen, dass CC ein Agent mit Datei-/Shell-/Git-Zugriff ist, kein Chat | 1.1 "Overview" + "claude.ai vs CLI" + Consultant-Analogie (Phone/Badge) |
| S1.2 | First Contact: bau sofort eine Datei | core | 12 | In einer Live-Session eine erste kleine Datei erzeugen lassen; Angst abbauen | 1.1 "What CC can do" + Demo 1.1 (First Contact / Log-Parser) |
| S1.3 | Die Oberflaechen: CLI, Desktop, IDE, Web, iOS | core | 12 | Die 5 Surfaces unterscheiden und die richtige je Workflow waehlen | 1.1 "Three Interfaces" / "Web&iOS" / "Surface-Switching" |
| S1.4 | Built-in Tools & die Tool-Namen | core | 12 | Die wichtigsten Tool-Namen (Read/Edit/Write/Bash...) kennen — Basis fuer Permissions | 1.1 "Built-in Tools Reference" |
| S1.5 | Permissions Grundlagen: default & acceptEdits | core | 15 | Die zwei Alltags-Modi verstehen + Allow/Deny-Grundidee (least privilege) | 1.1 "Permission System" (Teil: default/acceptEdits/plan + allow/deny) |
| S1.6 | Permission Modes komplett (6 Modi + Cloud) | deep-dive | 15 | Alle 6 Modi inkl. auto/dontAsk/bypass + Cloud-Restriktion einordnen | 1.1 "Permission System" (auto/dontAsk/bypass) + Cloud-2-Modi-Restriktion |
| S1.7 | Modellwahl & Effort-Level | core | 15 | Opus/Sonnet/Haiku + 5 Effort-Tiers grob nach Aufgabe waehlen | 1.1 "Model Selection & Cost Awareness" + 1.3 "Effort as a prompting lever" |
| S1.8 | Kontextfenster verstehen | core | 15 | Wissen wie der Context fuellt, was Auto-Compression macht, `/context` lesen | 1.2 "Context Window" + "Control Room"-Analogie + "Context Compression" |
| S1.9 | `/compact`, `/rewind` & Kontext steuern | core | 12 | Kontext bewusst komprimieren, Checkpoints/Undo nutzen | 1.2 "How to handle it" + "Key Context Commands" + Demo 1.2 |
| S1.10 | CLAUDE.md: die Projekt-Standing-Orders | core | 15 | Eine CLAUDE.md anlegen, wissen was rein-/nicht reingehoert | 1.2 "CLAUDE.md" + beide CLAUDE.md-Analogien + Demo 1.2 |
| S1.11 | Memory-Layer komplett (Auto-Memory, rules/, local, managed) | deep-dive | 18 | Die 4 Memory-Mechanismen + Managed>User>Project-Praezedenz zuordnen | 1.2 "Auto-Memory" + ".claude/rules/" + "CLAUDE.local.md" + "Managed-Policy" |
| S1.12 | `@path`-Imports, `--add-dir`, InstructionsLoaded | deep-dive | 12 | Imports/AGENTS.md-Interop und Multi-Repo-Setup debuggen | 1.2 "@path Imports" + "Multi-Project --add-dir" |
| S1.13 | Vager vs. praeziser Prompt (Contractor-Analogie) | core | 15 | Einen vagen Prompt in ein Work-Order-Format umschreiben (Scope/Kontext/Erfolg) | 1.3 "Clarity" + "Contractor" + "Scope Control" + Demo 1.3 |
| S1.14 | Plan Mode & das Explain/Propose/Refine/Execute-Muster | core | 15 | `/plan` und das 4-Schritt-Muster vor Multi-File-Tasks anwenden | 1.3 "Iterative Work Pattern" + "Plan Mode" + "Patterns" |
| S1.15 | Output Styles & Personas (system-prompt) | deep-dive | 12 | `/output-styles`, `--append-system-prompt`, `--system-prompt-file` einsetzen | 1.3 "Output Styles" + "/voice" + "Persona-Switching" |
| S1.16 | Git in einem Flow: branch -> commit -> PR | core | 18 | Einen kompletten Feature-zu-PR-Zyklus aus einer Session fahren | 1.4 "Built-in Git" + "Full PR Workflow" + Demo 1.4 |
| S1.17 | Git-Slash-Commands: /diff /review /rewind /autofix-pr | deep-dive | 15 | Die Review-/Experiment-Commands unterscheiden und richtig waehlen | 1.4 "Git-Related Slash Commands" + "/branch /fork" + "--from-pr" |
| S1.18 | Worktrees als Test-Labor | deep-dive | 15 | Einen Worktree (`claude --worktree`) + `worktree.baseRef` aufsetzen | 1.4 "Git Worktrees" + "--worktree Flag" + "baseRef" + "When to use" |
| S1.19 | Kosten im Blick: /cost, /usage & Budget-Cap | core | 15 | Spend lesen + `--max-budget-usd`/`--max-turns` als Guardrail setzen | 1.5 "Token Tracking" (core) + "Budget Caps" |
| S1.20 | Demo + Hands-on Puffer (Exercises 1.x pick 1) | core | 18 | Eine Uebung selbst loesen | Exercises 1.1-1.4 |

**Session 1 Core-Summe:** S1.1-S1.5, S1.7-S1.10, S1.13, S1.14, S1.16, S1.19, S1.20 = **12+12+12+12+15+15+15+12+15+15+15+18+15+18 = 201 Min Liste**, davon als Pflicht-Core fuer 1 Termin gebuendelt (siehe Hinweis) auf **~145 Min** zu fahren, wenn Demo-Puffer und einzelne core-LEs gestrafft werden.

> **Realismus-Hinweis Session 1:** Die Core-LEs summieren sich roh auf ~150 Min reine Lehrzeit + Pause + Q&A. Das ist fuer einen 180-Min-Termin **genau richtig** (heute war S1 mit 5 Modulen + Cost ueberladen). Empfehlung: S1.6, S1.11, S1.12, S1.15, S1.17, S1.18 (deep-dives) NUR bei Zeit/Interesse, sonst als Lesestoff fuers Cheatsheet.
- **Core gefahren (Pflicht):** ~145-150 Min
- **deep-dive verfuegbar (optional, Ueberlauf):** S1.6 (15) + S1.11 (18) + S1.12 (12) + S1.15 (12) + S1.17 (15) + S1.18 (15) = **87 Min**

---

### Session 2 — Das Ecosystem (Skills, Hooks, Plugins, MCP, RAG)

> Mission: "Wie erweitert und kontrolliert man Claude Code."

| Einheit | Titel | Level | Min | Lernziel(e) | aus (alt) |
|---|---|---|---|---|---|
| S2.1 | Skills = SOPs, Commands = Buttons | core | 12 | Das Skill/Command-Mentalmodell + SOP-Analogie verstehen | 2.1 "Core Idea" + "SOPs and Alarm Buttons" |
| S2.2 | Eine SKILL.md schreiben (Frontmatter-Basics) | core | 18 | name/description/when_to_use/arguments korrekt setzen | 2.1 "Anatomy of a Skill" + "Official Frontmatter Fields" + Demo 2.1 |
| S2.3 | Skills vs Commands & disable-model-invocation | core | 12 | Den realen Unterschied (auto vs manuell) ueber den Frontmatter-Switch verstehen | 2.1 "Skills vs Commands" |
| S2.4 | Bundled Skills (/batch /debug /loop /verify ...) | core | 12 | Wissen welcher bundled Skill welches Problem loest | 2.1 "Bundled Skills" + "/run-skill-generator" + "/skills" |
| S2.5 | Living Prompts: dynamische Injection & Argumente | deep-dive | 15 | `` !`cmd` ``-Injection + `$1/$mode/${CLAUDE_*}`-Substitution einsetzen | 2.1 "Argument Substitution" + "Dynamic Context Injection" + "Advanced Frontmatter" + "Live-Reload" |
| S2.6 | Hooks = Event-Listener (die 3 Eckpfeiler) | core | 15 | PreToolUse/PostToolUse/Stop verstehen + Access-Control-Sensor-Analogie | 2.2 "Core Idea" + "Three Cornerstones" + "Access Control Sensors" |
| S2.7 | Die wichtigsten Hook-Events landkarten | core | 12 | Die 11 meistgenutzten Events ihren Use-Cases zuordnen | 2.2 "Hook Types" (11er-Tabelle) |
| S2.8 | Einen Hook konfigurieren (settings.json, matcher, if) | core | 15 | Einen rm-rf-Block-Hook schreiben; matcher literal vs regex; `if`-Filter | 2.2 "Hook Configuration" + "Real Hook Example" + Demo 2.2 |
| S2.9 | Hook-Exec-Typen & component-scoped Hooks | deep-dive | 15 | command/http/prompt/agent/mcp_tool + Hooks in Skill-/Subagent-Frontmatter | 2.2 "What Hooks Can Do" + "Execution Types" + "Component-Scoped Hooks" |
| S2.10 | Advanced Hook-Outputs + Secure Diff Gate | deep-dive | 15 | updatedToolOutput/continueOnBlock/terminalSequence + $CLAUDE_EFFORT + Circuit Breaker | 2.2 "Advanced Hook Output" + "Circuit Breaker" + Demo 2.2b |
| S2.11 | Plugins: ein Bundle schnueren | core | 15 | Plugin-Layout (`.claude-plugin/plugin.json` + Ordner) + `claude plugin validate` | 2.3 "Core Idea" + "Plugin Structure" + "Security Module"-Analogie + Demo 2.3 |
| S2.12 | Plugin-Lifecycle, Scopes & Marketplaces | deep-dive | 15 | Scopes (user/project/local/managed) + install/enable/disable/prune + Marketplaces | 2.3 "Marketplaces" + "Scopes" + "CLI Management" + "Pinning" + "Dependencies" |
| S2.13 | Plugin-Supply-Chain-Risiken | deep-dive | 10 | Drittanbieter-Risiken benennen + Mitigationen (review/pin/project-scope) | 2.3 "Supply Chain Risks" + "Notable Plugins" |
| S2.14 | MCP: der Integrations-Stecker | core | 15 | Was MCP loest; Playwright/Slack/DB/Custom; Building-Management-Analogie | 2.4 "Core Idea" + "Integrated Building Management" + "Available Servers" + Demo 2.4 |
| S2.15 | MCP konfigurieren: Transports, Scopes, CLI | core | 15 | http/stdio/SSE + local/project/user + `claude mcp add` / `.mcp.json` | 2.4 "Transport Types" + "Scopes" + "CLI Management" + "File-Based Config" |
| S2.16 | MCP OAuth, Output-Limits & Protokoll-Details | deep-dive | 15 | OAuth-Flags + Output-Limits + streamable-http/list_changed/reconnect/CLAUDE_PROJECT_DIR | 2.4 "OAuth" + "Output Limits" + "Protocol Details" |
| S2.17 | MCP-Security & eigenen Server bauen | deep-dive | 18 | Prompt-Injection/Exfil/Token-Theft + fastmcp-Skeleton + Channels | 2.4 "MCP Security" + "Build Your Own" + "Channels" + "What MCP Changes" |
| S2.18 | RAG & NotebookLM: dem Agenten Blueprints geben | core | 18 | Wann RAG schlaegt + NotebookLM end-to-end (create/add-source/use/ask) | 2.5 komplett (Problem, Blueprints-Analogie, Workflow, Use Cases) + Demo 2.5 |
| S2.19 | RAG-Grenzen & Datenschutz-Abwaegung | deep-dive | 10 | Chunk-/Retrieval-Failures + Google-Hosting-Implikation (kein Proprietary-Code) | 2.5 "Data Flow Disclosure" + "RAG Limitations" + "Why this matters" |
| S2.20 | Hands-on Puffer (Exercises 2.x pick 2-3) | core | 18 | 2-3 Uebungen selbst loesen | Exercises 2.1-2.6 |

**Session 2 Core-Summe:** S2.1-S2.4, S2.6-S2.8, S2.11, S2.14, S2.15, S2.18, S2.20 = 12+18+12+12+15+12+15+15+15+15+18+18 = **177 Min Liste** → als Pflicht-Core auf **~145 Min** straffbar (S2.2 und S2.20 sind die elastischen Posten).
- **Core gefahren (Pflicht):** ~140-148 Min
- **deep-dive verfuegbar (optional):** S2.5 (15) + S2.9 (15) + S2.10 (15) + S2.12 (15) + S2.13 (10) + S2.16 (15) + S2.17 (18) + S2.19 (10) = **113 Min**

---

### Session 3a — Advanced Kern (Agents, Security, Automation)

> Mission: "Spezialisierte Agenten, automatisierte Security-Pruefung, sichere Automation." Das ist der Pflicht-Kern von Block 3.

| Einheit | Titel | Level | Min | Lernziel(e) | aus (alt) |
|---|---|---|---|---|---|
| S3.1 | Was ist ein Agent? (Spezialisierung) | core | 12 | Agent vs Skill; warum Rollen-Spezialisierung schlaegt; SOC-Analogie | 3.1 "What Is an Agent" + "Why Specialization" + "Agent Tool" |
| S3.2 | Built-in Subagents nutzen (Explore/Plan/general) | core | 10 | Die 3 eingebauten Subagents kennen, nicht das Rad neu erfinden | 3.1 "Built-in Subagents" |
| S3.3 | Einen Custom Subagent definieren | core | 18 | YAML-Frontmatter (name/description/tools/model/permissionMode/maxTurns) schreiben | 3.1 "Agent Definition Anatomy" + "Full Frontmatter Reference" + Demo 3.1 |
| S3.4 | Orchestrierungs-Muster (Fan-Out/Pipeline/Hierarchie) | core | 15 | Das richtige Muster waehlen + Speedup vs. sequenziell quantifizieren | 3.1 "Orchestration Patterns" + "Quick-Start" + Demo 3.1 (2 parallele Agents) |
| S3.5 | Background-Sessions & Agent Teams | deep-dive | 15 | `claude --bg`/`agents`/attach/logs/stop vs Subagent; Teams (experimentell) | 3.1 "Agent Teams" + "Background Agents" + "/tasks" + "/batch recap" |
| S3.6 | Devil's Advocate: adversariale Security-Pipeline | core | 18 | Die 4 Stufen (Scanners->Debate->Consensus->Fixers) erklaeren | 3.3 "Devil's Advocate Pipeline" (alle 4 Stages) + Demo 3.3 |
| S3.7 | Built-in Review-Trio (/security-review, /review, /ultrareview) | core | 12 | Die eingebauten Reviews vs. Custom-Pipeline waehlen | 3.3 "Security Audit Skill" + "Built-in Code-Review Trio" |
| S3.8 | Permissions fuer Autonomie (advanced modes) | core | 15 | auto/dontAsk/bypass im CI-Kontext + acceptEdits-Reichweite | 3.3 "Permission Modes Going Deeper" + "Permission Rules Beyond Allow/Deny" |
| S3.9 | Protected Paths & Sandboxing-Stufen | core | 15 | Was CC nie anfasst + Level 0-3 Isolation (OS/Worktree/Docker/Remote) | 3.3 "Protected Paths" + "Sandboxing Options" + "Trust Boundaries" |
| S3.10 | Netzwerk-/Skill-Hardening | deep-dive | 12 | deniedDomains/autoMode.hard_deny + disableSkillShellExecution | 3.3 "Sandbox Network Hardening" + "disableSkillShellExecution" |
| S3.11 | Datenschutz, Retention & regulierte Branchen | deep-dive | 15 | Retention-Tabelle + Compliance-Map (EN50131/GDPR/HIPAA...) | 3.3 "Data Retention & Privacy" + "Regulated Industries" + "Known CVEs" |
| S3.12 | Scheduling: /loop, /goal, /schedule, Routines | core | 15 | Time-based vs condition-driven vs persistent unterscheiden | 3.4 "/schedule" + "/loop" + "/goal" + "Routines" + Demo 3.4 |
| S3.13 | Autonome Loops absichern (Budget + Worktree) | core | 12 | Jeden Loop mit `--max-budget-usd`/`--max-turns` + `--worktree` scopen | 3.4 "--max-budget-usd" + "Worktree-Scoped Tasks" + "Channels" |
| S3.14 | Self-Improve Loop (Showcase + Grenzen) | bonus | 15 | Den autonomen Loop verstehen + Failure-Modes (cost runaway, false fixes) | 3.4 "Self-Improve Loops" (inkl. Branchen-Realitaet-Hinweis) |
| S3.15 | Hands-on Puffer (Exercise 3.x pick 1) | core | 15 | Eine Advanced-Uebung selbst loesen | Exercises 3.1-3.3 |

**Session 3a Core-Summe:** S3.1-S3.4, S3.6-S3.9, S3.12, S3.13, S3.15 = 12+10+18+15+18+12+15+15+15+12+15 = **157 Min Liste** → auf **~148 Min** straffbar (S3.3/S3.15 elastisch).
- **Core gefahren (Pflicht):** ~145-150 Min
- **deep-dive/bonus verfuegbar:** S3.5 (15) + S3.10 (12) + S3.11 (15) + S3.14 (15) = **57 Min**

---

### Session 3b — Bonus-Track (Multi-Model, CI/CD, Capstone, Troubleshooting)

> Optionaler 4. Termin **oder** strukturierter Selbststudien-Track. Hier liegt der Ueberlauf, der heute Block 3 mit 7 Modulen in 180 Min unrealistisch macht.

| Einheit | Titel | Level | Min | Lernziel(e) | aus (alt) |
|---|---|---|---|---|---|
| S3b.1 | Multi-Model: das richtige Modell pro Phase | deep-dive | 15 | Plan(Opus)/Implement(Sonnet/Codex)/Review(Haiku) begruenden | 3.2 "Different Models" + "Cost Trade-Off" + "Claude->Codex->Claude Pipeline" |
| S3b.2 | Codex Swarm & Daten-Fluss-Grenze | bonus | 15 | `--decompose`-Swarm + welche Daten zu OpenAI gehen + 3 Mitigationen | 3.2 "Data Flow" + "Codex Swarm" + "Practical Example" + Demo 3.2 |
| S3b.3 | Headless Mode: claude -p als Pipeline-Stufe | deep-dive | 15 | `claude -p` + `--output-format json` + `--json-schema` einsetzen | 3.6 "Headless Mode" + "Structured Output" + Demo 3.6 |
| S3b.4 | CI-Auth, Cost-Caps & --bare | deep-dive | 15 | `setup-token` + Budget/Turn-Caps + `--bare` fuer CI kombinieren | 3.6 "CI Auth" + "Cost Caps" + "--bare" + "Persona Override" |
| S3b.5 | CI-Pipelines bauen (GitHub Actions / GitLab) | deep-dive | 18 | Eine komplette PR-Review-Workflow-YAML schreiben + Failure-Patterns | 3.6 "GitHub Actions" + "GitLab CI" + "No-Internet" + "Pre-Commit" + "Failure Patterns" + "Don'ts" |
| S3b.6 | Mobile/Remote: remote-control & /teleport | bonus | 12 | Built-in Mobile-Workflow vs Custom Telegram Bridge waehlen | 3.5 "Built-in Mobile Workflow" + "Telegram Bridge" + "PushNotification" |
| S3b.7 | Inception (Docker) & Worktree-Isolation tief | bonus | 15 | Isolationsstufe waehlen; `worktree.baseRef`/`--tmux` fuer Multi-Agent | 3.5 "Inception" + "Worktree Isolation" + "baseRef" + "--tmux" |
| S3b.8 | Die volle Architektur (Capstone-Diskussion) | bonus | 25 | Eine komplette SOC-fuer-Software-Architektur diskutieren/skizzieren | 3.5 "Full Architecture" + "Complete Security Analogy" + Exercise 3.5 (Capstone) |
| S3b.9 | Troubleshooting: /debug, --verbose, /doctor | core* | 15 | Investigative/descriptive/prescriptive Tools am richtigen Level einsetzen | 3.7 "/debug" + "--verbose and /doctor" |
| S3b.10 | Diagnose-Sequenzen (Hook/Skill/Plugin/MCP) | core* | 18 | Die klassischen Failures + 8-Schritt-Checkliste durchlaufen | 3.7 "Hook-Failure" + "Skill not trigger" + "Plugin" + "MCP" + "InstructionsLoaded" + "Auto-Memory Drift" + "Checklist" + Demo 3.7 |

`core*` = innerhalb von Session 3b Pflicht; Troubleshooting (S3b.9/S3b.10) ist der einzige wirklich "jeder braucht es"-Teil von 3b. **Empfehlung:** Falls kein 4. Termin moeglich ist, S3b.9 + S3b.10 (33 Min) ans Ende von Session 3a haengen und 3a-deep-dives streichen; der Rest von 3b wird Selbststudium.

**Session 3b Summe (voller Track):** 15+15+15+15+18+12+15+25+15+18 = **163 Min** (passt in einen 180-Min-Termin mit Pause).

---

## Was sich gegenueber heute aendert (konkret)

1. **Reihenfolge im Einstieg umgedreht.** Heute startet Modul 1.1 sofort mit 6 Permission Modes + 5 Surfaces + Modellwahl. Neu: S1.1 ("Agent vs Chat") → S1.2 ("sofort eine Datei bauen") → S1.3 ("Oberflaechen") → erst S1.5 bringt Permissions, und nur die zwei Alltags-Modi (default/acceptEdits) als `[core]`. Die vollen 6 Modi werden zu `[deep-dive]` S1.6. Ein Neuling hat in den ersten 36 Min **gebaut**, bevor er ueber Clearance-Level nachdenken muss.

2. **Modul 1.1 in 7 LEs gesplittet** (S1.1-S1.7): Modell, Surfaces, Tools, Permissions-Basis, Permissions-Deep-Dive, Modellwahl. Jede LE 12-15 Min statt einem 15-Min-Block, der drei Themen presst.

3. **Modul 1.2 in 5 LEs gesplittet** (S1.8-S1.12): Kontextfenster, Kontext-Steuerung, CLAUDE.md, Memory-Layer-komplett (deep-dive), Imports/add-dir (deep-dive). Die 4 Memory-Layer + Praezedenz sind heute in einem Block — das ist die zweite Ueberforderungs-Stelle und wird entlastet.

4. **Cost Engineering (1.5) entzerrt und verschoben.** Statt 5. Pflicht-Modul am ersten Tag bleibt nur S1.19 ("/cost, /usage, Budget-Cap", `[core]`, 15 Min) in Session 1. Der Rest (Pipeline, Caching, Insights-Deep-Dive, Cost-Reduktions-Taktiken, Anti-Patterns) wird in Session 3b bei CI/Budget-Caps (S3b.4) praktisch wieder aufgegriffen. **Begruendung:** (a) Ein Neuling kann am Tag 1 ohne Praxis-Gefuehl die Pipeline-Oekonomie nicht einordnen; (b) Budget-Caps werden erst bei autonomen Loops/CI wirklich relevant (Session 3); (c) entlastet den ueberladenen ersten Tag um ~20 Min.

5. **Modul 3.3 in 6 LEs gesplittet** (S3.6-S3.11): Devil's-Advocate-Pipeline, Review-Trio, advanced Permissions, Protected Paths/Sandboxing, Netzwerk-Hardening (deep-dive), Datenschutz/Compliance (deep-dive). Das war mit Abstand das dichteste Modul (Adversarial + 6-Modi-Recap + Protected Paths + 4 Sandbox-Level + Retention-Tabelle + 7-Zeilen-Compliance-Map + CVEs).

6. **Block 3 ehrlich in 3a + 3b gesplittet.** Heute: 7 Module in 180 Min = unrealistisch (faktisch ~270 Min Inhalt). Neu: 3a = Agents + Security + Automation (Pflicht-Kern, ~148 Min Core). 3b = Multi-Model + CI/CD + Capstone + Troubleshooting (Bonus-Track, eigener Termin oder Selbststudium). Troubleshooting wird als einziger 3b-Teil als "core*" markiert und kann notfalls an 3a angehaengt werden.

7. **Drei-Schicht-Markierung neu.** Jede LE ist `[core]`/`[deep-dive]`/`[bonus]`. Der Trainer kann jede Session als "nur Core" (≈145 Min, sicher im Zeitrahmen) oder "Core + ausgewaehlte deep-dives" fahren. Das ersetzt die heutige grobe "Pflicht/Optional"-Trennung auf Modul-Ebene durch eine feinkoernige auf LE-Ebene.

8. **Demos bleiben an ihre LE gebunden.** Jede Demo aus den `demos/block-*.md` ist in der `aus (alt)`-Spalte ihrer LE vermerkt (Demo 1.1->S1.2, 2.2b->S2.10, 3.3->S3.6 usw.), damit der "Demo > Slides"-Grundsatz erhalten bleibt.

---

## Migrations-Plan (vom Ist zum Soll, ohne Inhaltsverlust)

1. **Phase 0 — Keine Inhalte loeschen, nur re-indexieren.** Die drei `modules/block-*.md` bleiben physisch die Quelle der Wahrheit. Die LE-Landkarte ist zunaechst nur eine **neue Navigationsschicht** darueber (dieser Vorschlag + ein aktualisierter `session-plan.md`). Risiko: null.

2. **Phase 1 — `session-plan.md` neu schreiben.** Die heutige 3-Session-Tabelle durch die 5-Session-/LE-Landkarte oben ersetzen (Session 1, 2, 3a, 3b). Core-Minuten-Summen pro Session ausweisen. Hier entsteht der eigentliche Mehrwert fuer den Trainer.

3. **Phase 2 — Anker in den Modul-Dateien setzen.** In `block-*.md` vor jedem Abschnitt, der jetzt eine eigene LE ist, einen HTML-Kommentar-Anker `<!-- LE: S1.5 -->` einfuegen. So bleibt der Volltext eine Datei, aber jede LE ist adressierbar (fuer den `workshop-mentor`-Agent und das `/workshop`-Command).

4. **Phase 3 — Level-Tags in die Modul-Ueberschriften.** Pro Abschnitt die Schicht ergaenzen, z.B. `### Permission Modes komplett [deep-dive]`. Reiner Additiv-Edit, kein Loeschen.

5. **Phase 4 — `agents/workshop-mentor.md` aktualisieren** (Pflicht laut CLAUDE.md-Projektregel: "Bei jeder Inhaltsaenderung an Modulen ... auch workshop-mentor.md aktualisieren"). Der Mentor muss die neue LE-Granularitaet kennen, damit "guide"/"learn"-Modi auf LE-Ebene navigieren koennen statt auf Modul-Ebene.

6. **Phase 5 — Cheatsheet & quick-reference pruefen.** Cost-Engineering-Verschiebung in Cheatsheet spiegeln (Budget-Caps bei Session-1-Kosten, Pipeline/Caching bei Session-3-CI).

7. **Phase 6 — Exercises neu zuordnen** (nur Mapping, kein Umschreiben): Exercise-Dateien bleiben; im session-plan wird vermerkt, welche Exercise an welche LE haengt (1.x->S1.20, 2.x->S2.20, 3.x->S3.15, Capstone 3.5->S3b.8).

8. **Validierung:** Nach Phase 1 einen Trockendurchlauf gegen den bestehenden `dry-run-session-2-3-2026-05-21.md` machen — passt jede Session-Core-Summe unter 150 Min?

**Kein Schritt loescht Lehrtext.** Die einzigen schreibenden Aenderungen sind: session-plan neu, Anker/Tags additiv, mentor-Agent, Cheatsheet-Spiegelung, Exercise-Mapping.

---

## Abdeckungs-Nachweis (heutiges Modul -> neue Einheit(en))

| Heutiges Modul | Neue Einheit(en) | vollstaendig? |
|---|---|---|
| 1.1 What is Claude Code? | S1.1, S1.2, S1.3, S1.4, S1.5, S1.6, S1.7 | ja (Overview+Surfaces->S1.1/1.3; Tools->S1.4; Permissions->S1.5/1.6; Models->S1.7) |
| 1.2 Context & Memory | S1.8, S1.9, S1.10, S1.11, S1.12 | ja (Context->S1.8/1.9; CLAUDE.md->S1.10; Memory-Layer->S1.11; Imports/add-dir->S1.12) |
| 1.3 Effective Prompting | S1.13, S1.14, S1.15 (+ Effort-Anteil in S1.7) | ja (Clarity/Scope->S1.13; Plan/Pattern->S1.14; Styles/Personas->S1.15) |
| 1.4 Git & Worktrees | S1.16, S1.17, S1.18 | ja (PR-Flow->S1.16; Slash-Commands->S1.17; Worktrees->S1.18) |
| 1.5 Cost Engineering | S1.19 (core) + S3b.4 (deep-dive Wiederaufnahme) | ja (Spend/Caps->S1.19; Pipeline/Caching/Insights/Taktiken->bei CI in S3b.4) |
| 2.1 Skills & Commands | S2.1, S2.2, S2.3, S2.4, S2.5 | ja (Modell->S2.1; SKILL.md->S2.2; vs Commands->S2.3; bundled->S2.4; dynamic/args->S2.5) |
| 2.2 Hooks | S2.6, S2.7, S2.8, S2.9, S2.10 | ja (Eckpfeiler->S2.6; Events->S2.7; config->S2.8; exec-types/scoped->S2.9; advanced/circuit->S2.10) |
| 2.3 Plugins | S2.11, S2.12, S2.13 | ja (Bundle/Layout->S2.11; Lifecycle/Scopes/Marketplaces->S2.12; Supply-Chain->S2.13) |
| 2.4 MCP | S2.14, S2.15, S2.16, S2.17 | ja (Idee/Server->S2.14; Transports/Scopes/CLI->S2.15; OAuth/Limits/Protokoll->S2.16; Security/Build/Channels->S2.17) |
| 2.5 RAG & NotebookLM | S2.18, S2.19 | ja (Workflow/Use-Cases->S2.18; Grenzen/Datenschutz->S2.19) |
| 3.1 Agents | S3.1, S3.2, S3.3, S3.4, S3.5 | ja (Was/Warum->S3.1; built-in->S3.2; custom def->S3.3; Muster->S3.4; background/Teams->S3.5) |
| 3.2 Multi-Model | S3b.1, S3b.2 | ja (Modellwahl/Pipeline->S3b.1; Swarm/Data-Flow->S3b.2) |
| 3.3 Security & Adversarial | S3.6, S3.7, S3.8, S3.9, S3.10, S3.11 | ja (DevilAdv->S3.6; Review-Trio->S3.7; Permissions->S3.8; ProtectedPaths/Sandbox->S3.9; Net-Harden->S3.10; Retention/Compliance/CVE->S3.11) |
| 3.4 Scheduling/Loops | S3.12, S3.13, S3.14 | ja (Scheduling-Primitive->S3.12; Budget/Worktree->S3.13; Self-Improve->S3.14) |
| 3.5 Telegram/Inception/Worktrees | S3b.6, S3b.7, S3b.8 | ja (remote-control/Telegram->S3b.6; Inception/Worktree->S3b.7; Architektur/Capstone->S3b.8) |
| 3.6 CI/CD Headless | S3b.3, S3b.4, S3b.5 | ja (Headless/JSON->S3b.3; Auth/Caps/--bare->S3b.4; Pipelines/Failures->S3b.5) |
| 3.7 Troubleshooting | S3b.9, S3b.10 | ja (Tools->S3b.9; Diagnose-Sequenzen/Checkliste->S3b.10) |

**Ergebnis:** Alle 17 Module sind vollstaendig auf 48 + 2 (Capstone-Diskussion zaehlt doppelt zu 3.5) LEs abgebildet. Kein Abschnitt ohne Ziel-LE.

---

## Offene Fragen / Entscheidungen fuer den Kunden

1. **3 oder 4 Termine?** Der ehrlichste Schnitt ist Session 3a + 3b als getrennte Termine (4 Termine gesamt). Variante "3 Termine": 3a wird Pflicht-Session, 3b wird Selbststudien-Track (nur S3b.9/S3b.10 Troubleshooting ans Ende von 3a haengen). **Welche Variante soll der session-plan abbilden?**

2. **Cost-Engineering-Verschiebung — einverstanden?** Vorschlag verschiebt den Grossteil von 1.5 in Session 3b (bei CI). Alternative: 1.5 bleibt komplett in Session 1 als `[deep-dive]`-Block am Ende (statt Pflicht), wird aber nicht verschoben. **Verschieben oder nur degradieren?**

3. **deep-dive-Default:** Sollen deep-dive-LEs im Live-Workshop standardmaessig **uebersprungen** und nur auf Nachfrage gezeigt werden, oder "wenn Zeit, dann zeigen"? Das aendert das Trainer-Skript.

4. **Permission Modes Split (S1.5 core / S1.6 deep-dive):** Reichen default+acceptEdits wirklich als Tag-1-Core, oder will die Zielgruppe (Physical-Security-Profis, security-affin) die vollen 6 Modi sofort? Es koennte sein, dass gerade dieses Publikum die Clearance-Level frueh sehen will — dann waere S1.6 doch `[core]`.

5. **Granularitaet:** 48 LEs sind deutlich feiner als heute. Ist das die gewuenschte Aufloesung, oder lieber ~30 etwas groessere LEs (15-25 Min)? Der Vorschlag laesst sich nach oben aggregieren, ohne Inhalte zu verschieben.

6. **Naming-Schema:** "S1.1 ... S3b.10" vs. ein flacher Index "LE-01 ... LE-50" vs. sprechende Slugs. Was passt besser zum `workshop-mentor`-Agent und `/workshop`-Command?
