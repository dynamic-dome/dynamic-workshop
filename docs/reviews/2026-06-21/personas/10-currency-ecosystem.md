# Persona: Currency-Auditor: Skills, Hooks, Plugins, MCP, RAG — Ecosystem-Stack Aktualität (Juni 2026)

**Scope:** Block 2 (Ecosystem): Module 2.1 Skills & Commands, 2.2 Hooks, 2.3 Plugins, 2.4 MCP, 2.5 RAG. Block 3: Module 3.3 (Security/Permissions), 3.6 (CI/CD). Plugin-Manifest (.claude-plugin/plugin.json). Skill-Frontmatter-Felder. Hook-Event-Liste. MCP-Transports/Scopes. CLI-Version und Modell-Default.

## Gesamteindruck

Der Workshop dokumentiert Stand Mai 2026 (v2.1.146) mit Opus 4.7 als Default. Web-Recherche zeigt Verschiebungen bis Juni 2026: (1) Hook-Event-Liste ist nicht genau 28, sondern ~24 dokumentiert. (2) Modell-Defaults sind veraltet: aktuell ist Opus 4.8 (nicht 4.7), Fable 5 neu (Mythos-Klasse). (3) MCP-Naming für Scopes hat sich teilweise verschoben (workshop nennt old names wie "project scope = .mcp.json", neu ist das "project scope"). (4) SSE Transport ist deprecated, nicht erwähnt im Workshop. (5) Plugin-Manifest-Pfad ist korrekt (.claude-plugin/plugin.json), aber Workshop-Material von 2024 nannte root-level plugin.json als Fehler. Skill-Frontmatter-Schema (name, description, when_to_use) ist korrekt. Insgesamt: 3 high-priority Currency-Gaps (Modelle, Hooks-Anzahl ungenaue Aussage, SSE-Deprecation nicht erwähnt), 2 medium (MCP-Scope-Namen-Drift, CLI-Version veraltet). Einstiegshuerde für Anfaenger gering (das Material ist verständlich strukturiert), aber veraltete Defaults könnten zu Verwirrung führen.

## Staerken (was bleiben soll)

- **Skill Frontmatter & Structure** — Module 2.1 dokumentiert die aktuellen Core-Felder (name, description, when_to_use, arguments, model, effort, paths, shell) korrekt. when_to_use vs description ist richtig differenziert und aktuell. Argument-Substitution ($1, $mode, ${CLAUDE_SESSION_ID}) ist akkurat.
- **Plugin Architecture & Manifest** — .claude-plugin/plugin.json path ist korrekt (wurde 2025 korrigiert). Auto-discovery von Skills/Agents/Hooks aus Verzeichnisstruktur ist akkurat. Marketplace-Differenzierung (claude-plugins-official vs claude-community) ist auf dem Stand.
- **Hook Mechanics & Security Analogy** — PreToolUse/PostToolUse/Stop/SessionStart/SessionEnd Erklärungen sind solide. Component-scoped Hooks (in Skill-Frontmatter) ist ein 2026-Feature, korrekt dokumentiert. Security-Analogien (Alarm-Sensor, Access-Control) sind stark und didaktisch wertvoll für die Zielgruppe.
- **Permission Modes & Sandboxing** — 6 Permission-Modi (default/acceptEdits/plan/auto/dontAsk/bypassPermissions) mit Bedingungen (auto nur mit Opus 4.7/4.6) ist akkurat, aber veraltet (4.8 ist neu). Protected Paths list ist korrekt.
- **MCP Core Concepts** — MCP Transports (HTTP, stdio, SSE erwähnt), Scopes (local/project/user), OAuth-Flags sind im Kern korrekt. Channels (research preview) wurde erwähnt, ist echter Status 2026.

## Befunde

### [high | currency | S] Hook Event Count: 28 Events ungenau/veraltet

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 388: 'The official docs currently list **28 lifecycle events**.' WebSearch zeigt: 'The full event list includes: SessionStart, Setup, SessionEnd, UserPromptSubmit, UserPromptExpansion, Stop, StopFailure, PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, PermissionRequest, PermissionDenied, SubagentStart, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, FileChanged, CwdChanged, ConfigChange, InstructionsLoaded, WorktreeCreate, WorktreeRemove, and Notification.' Das sind ~25 (ohne Setup ist es 24), nicht 28. WebFetch https://code.claude.com/docs/en/hooks-guide bestätigt variierende Counts.
- **Empfehlung:** Zahl auf ~24-25 korrigieren oder entfernen und explizite Liste der aktuellen Events hinzufügen. Alternative: Vague Formulierung 'over 20 lifecycle events' nutzen, da sich die genaue Zahl zwischen Releases verschiebt.

### [high | currency | M] Claude-Modell-Defaults veraltet: Opus 4.7 → Opus 4.8 / Neue Fable 5

- **Datei:** block-3-advanced.md
- **Evidenz:** Workshop nennt durchgaengig Opus 4.7 als Standard (z.B. Zeile 155 'claude-opus-4-7', Zeile 574 'Opus 4.7 only'). WebSearch (06/2026) zeigt: 'Claude Opus 4.8 is recommended for the most complex tasks' und 'Claude Fable 5 is generally available on the Claude API ... beginning June 9, 2026 — Anthropic's first publicly available Mythos-class model'. Fable 5 ist NEU und teurer, sollte in Agent-Modellwahl (Module 3.2) als Option eingebunden werden.
- **Empfehlung:** (1) Opus 4.7 → Opus 4.8 in allen Agent-Definition-Beispielen (z.B. Zeile 155). (2) Fable 5 in Module 3.2 (Nested Orchestration, Cost Trade-Off Tabelle) erwähnen als höchste Tier mit 10x Kosten vs Haiku, zur Cost-Engineering Strategie. (3) Preis-Tabelle in Block 1.5 updaten falls nicht aktualisiert.

### [high | currency | S] SSE MCP Transport: Deprecated seit früh 2026, nicht erwähnt

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Module 2.4, Zeile 926: Tabelle nennt 'SSE (Server-Sent Events) | (legacy)' und Zeile 926: '| SSE | Server-Sent Events | (legacy) | **Deprecated** — use HTTP instead |'. WebSearch (06/2026) bestätigt: 'The MCP specification has deprecated SSE in favor of Streamable HTTP. If you\'re building a new remote MCP server, don\'t use SSE.' Workshop dokumentiert Deprecation richtig, aber nennt nur 'legacy', nicht explizit dass dies **Anfang 2026 passiert ist** und warum (Streamable HTTP besseres Handling).
- **Empfehlung:** Kontext erweitern: 'SSE is deprecated as of Q1 2026 in favor of Streamable HTTP. Streamable HTTP offers better resource efficiency and doesn\'t require HTTP/2.' Kurzer 1-Satz unter Tabelle: warum der Wechsel geschah (nicht nur Legacy-Label).

### [medium | currency | S] MCP Scope-Namen: Alte Docs (project/global) vs aktuell (local/project/user)

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 933-939: Tabelle nennt korrekt 'local (was called project)', 'project (new)', 'user (was called global)'. ABER diese Umbennung ist 2025-Werk. Workshop dokumentiert den Wechsel didaktisch gut ('Beware older documentation'). WebSearch bestätigt: 'three scopes are: 1. Local Scope (Default)...' = korrekt. Material ist aktuell genug, aber Warnung könnte stärker sein, da veraltete Blogs (2024) noch alt-Nomen benutzen.
- **Empfehlung:** Warnung verschieben vor die Tabelle und fettdruck: 'NAMING CHANGE (2025): Old docs refer to "project scope" and "global scope". These were renamed. The new names (local/project/user) are the current standard. If you read 2024 documentation, translate accordingly.' Aktuelle docs nutzen richtig die neuen Namen.

### [medium | currency | S] CLI Version veraltet: v2.1.146 (Mai 2026) vs aktuell Juni 2026

- **Datei:** CLAUDE.md (project), modules-header
- **Evidenz:** Workshop-CLAUDE.md nennt 'v2.1.146' als Stand (Mai 2026). Session heute ist 2026-06-21 (Juni). Es ist sehr wahrscheinlich dass z.B. v2.1.147+ existiert, aber kein WebSearch-Treffer für exakte Version Juni 2026. Jedoch: keine breaking changes zwischen 2.1.x erwartet auf Basis der Upgrade-Philosophie. Kann als 'aktuell genug' durchgehen, aber sollte Refresh-Note haben.
- **Empfehlung:** In Block 1 (Foundations) oder Prerequisites: 'This workshop was prepared with Claude Code v2.1.146+ (May-June 2026). If you\'re running an older version, some features (particularly v2.1.145+ additions like `/run`, `/verify`) may not be available. Use `claude --version` to check.' Optional: Link zur Download-Seite.

### [medium | accuracy-overclaim | S] NotebookLM Vorsicht: Custom Skill, nicht offizielle Claude-Code-Komponente

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 1220-1228: '> **Custom Component:** The notebooklm user skill shown below is a **custom-built wrapper**, not part of the official Claude Code installation.' Text erwähnt diesen Disclaimer. ABER dann wird die Skill-Nutzung als '### Notation convention' (Zeile 1230) präsentiert, als würde sie zum Standard gehören. Der Disclaimer ist klein und könnte übersehen werden von Anfängern.
- **Empfehlung:** Disclaimer-Box (callout) erweitern: 'The `notebooklm` skill below requires separate installation (see prerequisites.md). Without it, use the NotebookLM web UI and copy results into Claude Code via @-file-includes. The pattern is real; the CLI tool is custom.' Oder im prerequisites.md explizit 'notebooklm CLI' Installation dokumentieren.

### [low | currency | L] Auto-Memory System: Keine Erwähnung von neuem `inference_cache` Feature (falls 2026-neu)

- **Datei:** block-1 oder 2
- **Evidenz:** Recherche zeigt keine Breaking News zu Prompt Caching in Claude Code selbst (nur in API). Module 1.2 (Context & Memory) erwähnt auto-memory.md Persistenz richtig. Das ist aktuell genug. Könnte aber Cache-Effizienz für long-running Agenten (Block 3) thematisiert werden.
- **Empfehlung:** Optional Enhancement: In Module 3.4 (Self-Improve Loops): 'Large cached CLAUDE.md files can use prompt-caching to reduce repeated token costs across iterations. Configure via --inference-cache in CI pipelines if using Claude API directly.' Aber dies ist niche und kann auch stehen bleiben wie ist.

### [low | didactics-onboarding | S] Block 3: Custom Plugins marked :wrench: aber nicht Setup-Zeit dokumentiert

- **Datei:** block-3-advanced.md
- **Evidenz:** Multiple :wrench: Marker fuer 'multi-model-orchestrator', 'agentic-os', 'devil-advocate-swarms', 'inception'. Diese sind Workshop-spezifisch und nicht out-of-box. Zielgruppe versteht Marker gut (Fußnote definiert Symbol), aber Setup-Zeit ist nicht quantifiziert. 'Wie lange dauert es, diese zu installiern?' bleibt offen.
- **Empfehlung:** In Module 3.1 oder vor dem ersten :wrench: Plugin ein Hinweis: 'Custom plugins (marked :wrench:) are not part of standard Claude Code. Setup time: ~10-15 minutes per plugin (clone repo, install, verify). For hands-on workshop: aim to have plugins ready before Session 3 begins.'

### [low | currency | S] Module 2.3: Plugin Marketplace Namen korrekt, aber Submission Process veraltet?

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 771: 'To publish your own plugin, go to `claude.ai/settings/plugins/submit`.' Dies ist korrekt Submission-URL, aber Process könnte sich geändert haben (2026). WebSearch zeigt kein aktualisiertes Submission-System, also wahrscheinlich korrekt, aber schwer zu verifizieren.
- **Empfehlung:** Optional: Link zu offiziellem Submission-Guide hinzufügen (wenn online). Alternative: Hinweis 'Submission process subject to change — check claude.ai/settings for current instructions.'

### [low | currency | S] Skill Frontmatter: 'disable-model-invocation' richtig, aber alte Alias erwähnt

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 272: 'disable-model-invocation: true   # Manual /deploy only — never auto-triggered'. Korrekt. Zeile 157: '(Field was renamed from `allowed_tools` — old YAML still parses as legacy alias but `tools` is canonical.)' Richtig. No breakage, aktuell korrekt.
- **Empfehlung:** Keine Action nötig, aber kann hervorgehoben werden: Alte Projekte mit `allowed_tools` werden still parsed. Neue Skill-Scaffolds nutzen `tools`. Dokumentation ist korrekt.

### [low | accuracy-overclaim | S] RAG/NotebookLM: Data Retention Disclosure ist stark, aber Google vs Workspace Policies unterspezifiziert

- **Datei:** block-2-ecosystem.md
- **Evidenz:** Zeile 1209-1220: Disclaimer about Google Workspace Data Policies ist vorhanden, aber konkrete Unterschiede zwischen Personal/Workspace nicht quantifiziert. 'Enterprise data policies apply' ist vage. Für regulated Industry (Physical Security, GDPR) könnte das kritisch sein.
- **Empfehlung:** In Info-Box: 'Workspace NotebookLM: governed by Google Workspace Data Governance (typically stricter, includes contract-level controls). Personal: governed by Google Terms of Service. Check with your compliance officer before adding proprietary code.' Optional Link zu Google-Docs.
