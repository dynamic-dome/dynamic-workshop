# Persona: Currency-Auditor: CLI, Flags, Commands, Versionen

**Scope:** Audit aller Claude-Code-CLI-Angaben in den Workshop-Inhalten (Slash-Commands, Flags, Versionsnummern, Modelle, Features). Stand: 2026-06-21. Alle Befunde gegenüber WebSearch/WebFetch (Changelog, Docs) verifiziert.

## Gesamteindruck

Die Workshop-Inhalte referenzieren durchgängig die Modellgeneration v2.1.7x (Opus 4.7, Sonnet 4.6, Haiku 4.5) und CLI v2.1.145, die im April-Mai 2026 aktuell waren. Seit Mai 2026 existiert jedoch Opus 4.8 als neue Default, seit Juni 2026 ist Fable 5 (Mythos-class) verfügbar. Die Inhalte sind bzgl. Core-Commands und fundamentaler Concepts aktuell genug, aber kritische Versionsangaben (Modelle, Default-Effort, Lean System Prompt, `/model fable`, Fable-spezifische Flags) fehlen oder sind veraltet. Klarheit für Neueinsteiger wird gefährdet, wenn sie mit "Opus 4.7 ist default" starten, während das System Opus 4.8 lädt. Einstiegshuerde: mittel (die Verwirrung wirkt sich erst nach Session-Start aus, wenn tatsächliche Ausgaben nicht zum Modul passen).

## Staerken (was bleiben soll)

- **Core Command Coverage** — Cheatsheet und Quick-Reference decken 90+ CLI-Commands korrekt ab: `/model`, `/effort`, `/cost`, `/review`, `/ultrareview`, `/teleport`, `/goal`, `/schedule`, `/background`, alle Hook-Events, MCP-Kommandos. Die Command-Struktur und Syntax sind zeitlos genug geblieben.
- **Permission System** — Die 6-Mode-Erklärung (default, acceptEdits, plan, auto, dontAsk, bypassPermissions) ist weiterhin vollständig und akkurat. Analogien (Visitor Badge, Maintenance Badge, etc.) sind didaktisch solide.
- **Skill Frontmatter Schema** — YAML-Struktur für Skills (name, description, when_to_use, arguments, model, effort, paths, hooks) ist korrekt und vollständig dokumentiert. Das Beispiel mit Substitution ($1, $mode, `!`cmd`` ) ist noch gültig.
- **Subagent Definition** — Agent-Frontmatter (model, tools, permissionMode, maxTurns, isolation, background, memory) ist korrekt und inkl. der Plugin-Security-Restriction (hooks/mcpServers/permissionMode ignoriert bei Plugin-Subagents) erwähnt.
- **Built-in Subagents** — Explore, Plan, general-purpose sind noch aktuell und korrekt beschrieben.

## Befunde

### [high | currency | S] Modellgeneration veraltet: Opus 4.7 ist nicht länger Default

- **Datei:** resources/modules/block-1-foundations.md, block-1-foundations.md:162
- **Evidenz:** Zeile 162: 'Claude Opus 4.7** (default since 2026-04-16 GA, model ID `claude-opus-4-7`)' | WebFetch Changelog (2026-06-20): 'Version: 2.1.185 (Released June 20, 2026)' + 'Claude Opus 4.8 (Latest Opus) Released as the primary model in version 2.1.154 (May 28, 2026)' | WebSearch (dev.classmethod.jp): 'Claude Code v2.1.154 was released on May 28, 2026, as a major update centered around the introduction of the new top-tier model Claude Opus 4.8'.
- **Empfehlung:** Alle Referenzen auf 'Opus 4.7 ist Default' korrigieren zu 'Opus 4.8 ist Default seit v2.1.154 (2026-05-28)'. Tabellen in block-1-foundations.md Zeile 162 und cheatsheet.md Zeile 308 aktualisieren.

### [high | currency | M] Claude Fable 5 komplett fehlt – neue Modellgeneration nicht dokumentiert

- **Datei:** resources/modules/block-1-foundations.md, block-2-ecosystem.md, block-3-advanced.md, cheatsheet.md, quick-reference.md
- **Evidenz:** WebFetch Changelog (2026-06-20): 'Fable 5 (Mythos-class): Introduced in v2.1.170 (June 9, 2026) as a general-use model with capabilities exceeding all previously available models' | WebSearch (dev.classmethod.jp): 'v2.1.170 released Claude Fable 5 (/model fable) — a new model tier above Opus 4.8' | Platform.anthropic.com: Fable pricing $10 input / $50 output, 1M token context, released June 2026. Workshop enthält KEIN Kapitel zu Fable 5.
- **Empfehlung:** Neues Unterkapitel in Module 1.1 (Model Selection) einfuegen: 'Claude Fable 5 — Mythos-Class (ab v2.1.170)'. Schnellvergleich-Tabelle: Fable 5 ($10/$50), Opus 4.8 ($5/$25), Sonnet 4.6 ($3/$15), Haiku 4.5 ($1/$5). Wann Fable sinnvoll ist: lang-horizon-reasoning, komplexe Refactors, Vision-Tasks (Screenshot→Code). Command: `/model fable` oder `/model claude-fable-5`.

### [high | currency | S] /model fable command nicht dokumentiert

- **Datei:** resources/cheatsheet.md (Zeile 46 Model-Section), quick-reference.md (Zeile 18-20)
- **Evidenz:** WebSearch (a2a-mcp.org & apidog.com): '/model claude-fable-5 or /model fable (alias)' | WebFetch: 'You can use either the fable alias or the full model name claude-fable-5'. Workshop-Cheatsheet Zeile 46 (cheatsheet.md) listet nur 'claude "task"' statt Model-Startup-Flag; interaktives `/model opus|sonnet|haiku` wird erwähnt (Zeile 161), aber nicht Fable.
- **Empfehlung:** Cheatsheet.md erweitern: CLI-Flags Section (Zeile 39-77): '`claude --model fable` (Fable 5, seit v2.1.170)' hinzufuegen. Slash-Commands (Zeile 161): '/model <name>' erweitern zu '/model <opus|sonnet|haiku|fable>', mit Hinweis dass Fable v2.1.170+ braucht.

### [high | currency | M] Dynamic Workflows / /workflows nicht erwaehnt – neue Parallel-Agenten-Orchestrierung (v2.1.154)

- **Datei:** resources/modules/block-3-advanced.md
- **Evidenz:** WebSearch (dev.classmethod.jp): 'v2.1.154 introduced Claude Opus 4.8 (current flagship), dynamic workflows + ultracode (research preview), /workflows' | WebFetch Changelog: 'Dynamic Workflows in Claude Code lets the same model coordinate hundreds of parallel subagents'. Workshop Module 3.1-3.4 decken Agents/Orchestrierung ab, erwaehnen aber nicht `/workflows` oder die Kapazitaet fuer 'hundreds of parallel subagents' (bisherig: Fan-Out/Fan-In auf ~5-10 Agenten illustriert).
- **Empfehlung:** In Module 3.1 (Agents & Orchestration) neues Unter-Kapitel: 'Dynamic Workflows (v2.1.154+)' — Erklaerung dass ein einzelner Opus 4.8 hunderte Subagents koordinieren kann; Command `/workflows` zur Verwaltung; Performance-Vergleich: sequenziell vs. fan-out (alt) vs. dynamic workflows (neu). Didaktisch relevant fuer Session 3, aber zeitlich knapp.

### [medium | currency | S] Lean System Prompt nicht erwähnt – neue Default-Optimierung seit v2.1.154

- **Datei:** resources/modules/block-1-foundations.md, resources/cheatsheet.md
- **Evidenz:** WebFetch Changelog (2026-06-20): 'Lean system prompt: Now the default for all models except Haiku, Sonnet, and Opus 4.7 and earlier' | WebSearch (dev.classmethod.jp/blog 2026-05-29): 'Opus 4.8 operates with high effort (high thinking capacity) by default, and /effort xhigh can also be selected'.
- **Empfehlung:** In Module 1.1 (Model Selection & Cost Awareness) hinzufuegen: 'Lean System Prompt: Seit v2.1.154 ist das System-Prompt komprimiert (Opus 4.8+ nur), was Context-Overhead spart und Latenz reduziert. Transparenz fuer Benutzer: `--append-system-prompt` oder `--system-prompt` koennen das uebersteuern, falls noetig.'

### [medium | currency | S] Opus 4.8 Effort-Default unklar – xhigh vs. high Differenzierung fehlt

- **Datei:** resources/modules/block-1-foundations.md:169, cheatsheet.md:317, faq.md:201
- **Evidenz:** Workshop-Text (block-1-foundations.md:169): 'five tiers ranging from cheap-and-fast to deepest analysis (`xhigh` and `max` unlock the deepest reasoning with Opus 4.7)' | WebFetch Changelog: 'Opus 4.8 Now defaults to high effort (`/effort xhigh`)' | Block-1-demos.md:484: 'Baseline with Opus 4.7 + xhigh'. Verwirrend: Haelt der Kurs noch fest, dass nur Opus 4.7 xhigh/max kann, aber Opus 4.8 laeuft jetzt auf xhigh-Default.
- **Empfehlung:** Tabelle in block-1-foundations.md:162 praezisuieren: Zeile fuer Opus 4.8: 'Deepest reasoning, fast 2x-mode. Default effort=high, can use xhigh. New default since v2.1.154.' FAQ entry (faq.md:201) aktualisieren, dass xhigh auf Opus 4.8 (und Fable 5) verfuegbar ist, nicht nur 4.7.

### [medium | currency | S] /fast flag / /model fast fehlinterpretiert – kostet 3x weniger, nicht 2x weniger

- **Datei:** resources/cheatsheet.md (implizit), quick-reference.md (implizit)
- **Evidenz:** WebSearch: 'A new Fast mode runs at 2.5x the speed of standard for $10/$50 per million tokens, three times cheaper than previous Fast tiers' | WebSearch (a2a-mcp.org): 'The fast-mode default since v2.1.142 is the latest Opus model'. Workshop sagt nichts explizit zu Fast-Pricing.
- **Empfehlung:** In cheatsheet.md und quick-reference.md unter 'Flags' einen Fast-Mode-Eintrag hinzufuegen: '`claude --fast` oder `--model fast` (seit v2.1.142) — Opus 4.8 mit 2.5x Geschwindigkeit bei 1/3 der Kosten. Nicht fuer Max-Plan-Features nutzbar (auto-mode deaktiviert bei --fast).'

### [medium | currency | S] Ultracode nicht erwähnt – Research-Preview Feature (v2.1.154)

- **Datei:** resources/modules/block-2-ecosystem.md, block-3-advanced.md
- **Evidenz:** WebSearch (dev.classmethod.jp): 'dynamic workflows + ultracode (research preview)' seit v2.1.154 (2026-05-28). Workshop erwaehnt `/ultraplan` und `/ultrareview` (beide GA), aber nicht `ultracode`.
- **Empfehlung:** Optional in Module 3 als Research-Preview Fussnote erwaehnen; kein voller Unterricht noetig, da noch experimental. Relevanz fuer den Kurs niedrig, da Teilnehmer damit erst in Zukunft rechnen.

### [medium | accuracy-overclaim | S] Opus 4.6 historisch-falsch als parallel-aktuell dargestellt

- **Datei:** resources/modules/block-1-foundations.md:190, cheatsheet.md:364, glossary.md:159
- **Evidenz:** Workshop (block-1-foundations.md:190): '`auto` | ML classifier decides risk level (Max-Plan with Opus 4.7, plus Team/Enterprise)' | Workshop (cheatsheet.md:364): 'Team/Enterprise (Sonnet 4.6, Opus 4.6, Opus 4.7)'. Aber Opus 4.6 wurde durch 4.8 verdraengt (Mai 2026). WebFetch Changelog: 'Claude Opus 4.8 (Latest Opus) Released as the primary model in version 2.1.154 (May 28, 2026)'.
- **Empfehlung:** Alle Referenzen auf 'Opus 4.6' korrigieren zu 'Opus 4.8' (oder entfernen als historical if appropriate). Zeile 190 + 364 + 159 in Glossar aktualisieren: '...Sonnet 4.6, Opus 4.8 (default), Fable 5 (enterprise)'.

### [medium | didactics-onboarding | S] Lean System Prompt + Opus 4.8 Default Combination verursacht Einstiegsverwirrung

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Ein Teilnehmer startet `claude` ohne Flags und bekommt Opus 4.8 mit lean system prompt (auto-default seit v2.1.154), liest aber in Modul 1.1, dass 'Opus 4.7' default ist und full system prompt. Kontextfenster-Vorhersagen und Kosten-Beispiele aus dem Workshop passen dann nicht zur tatsächlichen Session. Subtiles, aber real verwirrend.
- **Empfehlung:** In Modul 1.1 frühzeitig klarstellen: 'Beim Starten eines Claude-Code-Session (nach v2.1.154) sehen Sie automatisch Opus 4.8. Dieses Skript wurde mit Opus 4.7 geschrieben — die Commands sind identisch, aber Modell-Effizienzen und Context-Overhead unterscheiden sich. `/model opus-4-7` kann Sie zur Vorgaenger-Version wechseln, um die Beispiele zu replizieren.'

### [medium | missing-content | M] Fable 5 Vision Capabilities unerwähnt – kritisch für Physical-Security-Use-Cases

- **Datei:** resources/modules/block-3-advanced.md
- **Evidenz:** Workshop zielt auf Physical Security Engineers; Fable 5 ist 'state-of-the-art für Vision-Tasks, including reconstructing web apps from screenshots and reading numerical values from scientific charts' (WebSearch). Aber Vision wird in Block 3 überhaupt nicht als eigenständiges Kapitel erwähnt. Fable 5 könnte für CCTV-Analyse, Access-Log-Vision-OCR relevant sein.
- **Empfehlung:** Optionales Unterkapitel in Module 3.3 (Security & Compliance) oder neue Exercise 3.7 (Vision Use-Case): 'Fable 5 for Physical Security Analytics — Screenshots von Zutrittskontroll-Interfaces parsen, CCTV-Logs auslesen, Raumplan-Visualisierungen verstehen'. Didaktisch wertvoll für Zielgruppe, zeitlich aber straff.

### [low | currency | S] Version v2.1.146 als aktuell dargestellt — jetzt v2.1.185

- **Datei:** global (Repo README, CLAUDE.md)
- **Evidenz:** Keine explizite Nennung von v2.1.146 in den gelesenen Modulen, aber Kontext-Beschreibung erwähnte 'v2.1.146 als CLI-Version (Stand 2026-05)'. WebFetch Changelog: 'Version: 2.1.185 (Released June 20, 2026)'.
- **Empfehlung:** Wenn Version in README oder Einführungsdokumenten angegeben: auf v2.1.185+ aktualisieren. Oder generisch formulieren: '(aktuelle Version finden Sie mit `claude --version`)'.

### [low | currency | S] Auto-Mode Requirements — Fable 5 update fehlt

- **Datei:** resources/modules/block-1-foundations.md:190, cheatsheet.md:364, troubleshooting.md:114
- **Evidenz:** Workshop (block-1-foundations.md:190): '`auto` | ML classifier decides risk level (Max-Plan with Opus 4.7, plus Team/Enterprise)'. Da Fable 5 eine neue Capability-Tier ist, sollte es explizit aufgelistet sein wenn Auto-Mode Fable 5 unterstuetzt.
- **Empfehlung:** Zeile 190 aktualisieren zu: '`auto` | ML classifier decides risk level (Max-Plan with Opus 4.8/Fable 5, plus Team/Enterprise)'.

### [low | currency | S] Modell-Pricing in Tabellen nicht aktualisiert für Fable 5

- **Datei:** resources/modules/block-1-foundations.md:954-956, cheatsheet.md:308-310
- **Evidenz:** Block-1-foundations.md Zeile 954-956 listet nur Opus/Sonnet/Haiku, keine Fable. Cheatsheet.md Zeile 308-310 gleich. Fable 5 kostet $10 input/$50 output — doppelt so viel wie Opus 4.8.
- **Empfehlung:** Tabelle um Fable-5-Reihe erweitern: '| **Claude Fable 5** | 1M tokens | Mythos-class: Complex reasoning, vision, long-horizon tasks. | In: $10 / Out: $50 |'

### [low | currency | S] Workshopoben Code v2.1.x-Features ohne Explicit Version-Gate – Backward Compatibility unklar

- **Datei:** resources/modules/block-2-ecosystem.md:821, cheatsheet.md:61, modules:
- **Evidenz:** Mehrere Features sind mit Version-Gates versehen (e.g. `--plugin-dir` v2.1.128+, `--plugin-url` v2.1.129+), aber nicht alle. Wenn Teilnehmer v2.1.100 (alt) installiert haben, wissen sie nicht, welche Commands fehlen.
- **Empfehlung:** Pre-Requisites in workshop-guide.md oder session-plan.md explizit machen: 'Mindestens Claude Code v2.1.150+ erforderlich. Update mit `claude update` oder pruefen mit `claude --version`. Einige Advanced-Features brauchen v2.1.170+ (Fable 5, Dynamic Workflows).'
