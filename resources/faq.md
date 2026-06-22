# FAQ — Claude Code Workshop

> Haeufige Fragen aus dem Workshop-Kontext. Antworten in 3-8 Saetzen.
> Begriffsklaerungen im `resources/glossary.md`, konkrete Fehler im `resources/troubleshooting.md`.
> Stand: 2026-05-20.

---

## Konzepte

### Wann nutze ich Skill, Agent, Command oder Hook?

- **Skill**: Wiederverwendbare Anweisung, die Claude bei passenden Trigger-Phrases laedt. (SOP)
- **Command**: Slash-Command, der eine bestimmte Action triggert. (Alarmbutton) — Seit v2.x funktional mit Skills gemerged: Command = Skill mit `disable-model-invocation: true`.
- **Agent (Subagent)**: Spawned eine separate Claude-Instanz mit eigenem Kontext fuer isolierte Tasks.
- **Hook**: Automatische Action bei einem Lifecycle-Event (vor/nach Tool-Use, Session-Start, etc.).

**Faustregel:** Skill fuer "ich gebe Anweisungen wieder", Agent fuer "ich brauche parallele oder isolierte Arbeit", Hook fuer "passiert automatisch im Hintergrund".

Vertiefung: Modul 2.1 (Skills & Commands), 2.2 (Hooks), 3.1 (Agents).

### Welches Model wann?

Opus 4.8 (oder Fable 5 fuer die haertesten, langlaufenden Aufgaben) fuer Architektur, Planning, Root-Cause-Analysis. Sonnet 4.6 fuer Standard-Coding und Refactors. Haiku 4.5 fuer Bulk-Reads, einfache Suchen, Routine-Reviews.

Pipeline-Pattern: `/plan` mit Opus, `/batch` von Subagents mit Sonnet, `/review` mit Haiku.

### Was kostet Claude Code im Alltag?

Solo-Dev mit aktiver Nutzung: ~$5-10 pro Tag (Sonnet 4.6 als Default). Mit `/cost` kannst du laufende Session pruefen, `/usage` zeigt Rate-Limits und Subscription-Status, `/insights` Analytics ueber Sessions. Monatlich typisch $100-200 pro Dev.

Cost-Drivers: Opus statt Sonnet, `xhigh`/`max` Effort, viele Subagents parallel, ausufernde CLAUDE.md.

### Was sieht Anthropic, was bleibt lokal?

Modell-Calls gehen zu Anthropic (Prompts + Outputs). Files werden NUR im Tool-Call-Context geteilt (nicht das gesamte Filesystem). Mit `DISABLE_TELEMETRY=1` und `DISABLE_ERROR_REPORTING=1` laesst sich Diagnostic-/Sentry-Telemetry deaktivieren. **ZDR (Zero Data Retention)** ist Teil von Enterprise-Plans und reduziert Retention auf 0 Tage.

Free/Pro/Max: Opt-in Training, Retention 5y (Opt-in) oder 30d (Opt-out). Team/Enterprise: kein Training, 30 Tage Retention default.

### Was geht zu OpenAI bei Codex-Pipelines?

Wenn ein Codex-Subagent Tasks bekommt: Prompt + ggf. Code-Snippets gehen zu OpenAI. Fuer sicherheitskritischen Code: Codex-Schritt ueberspringen oder Code vor Senden redacten. Workshop-Disclosure-Slide in Modul 3.2.

### Was sind Claude Code's Surfaces?

Fuenf: CLI, Desktop App, Web App (claude.ai/code), IDE Extension (VS Code/JetBrains), iOS App. Alle teilen die gleiche Agent-Engine. **Achtung:** Cloud-Surfaces (Web + iOS) unterstuetzen nur `acceptEdits` und `plan` als Permission-Mode — keine `auto`, `dontAsk`, `bypassPermissions`.

---

## Setup

### Welche Plugins/Skills brauche ich fuer den Workshop?

Siehe `resources/prerequisites.md` Sektion "Workshop-Specific Plugins & Skills".

### Brauche ich Codex CLI?

Nur fuer Demo 3.2 (Codex Swarm) optional. Demo kann beobachtet werden ohne lokale Codex-Installation. Falls du selbst mitspielen willst: Codex CLI installieren und mit OpenAI-API-Key authentifizieren.

### Mein Skill triggert nicht — was tun?

Siehe `resources/troubleshooting.md` Sektion 1.

### Wie verteile ich mein Claude-Code-Setup an mein Team?

- `.claude/` in Git-Repo committen (Skills, Hooks, Settings, Agents, Rules)
- `.gitignore`: `CLAUDE.local.md`, `.claude/settings.local.json`, `*.local.json`
- `/team-onboarding` generiert teilbaren Setup-Guide aus deiner History
- Skills als Plugin packen und intern (privates Git-Repo als Marketplace) oder ueber `claude-community` publishen
- Pre-built `~/.claude/`-Bundle fuer Neueinsteiger anlegen (z.B. ein Git-Repo, das Teammitglieder klonen und symlinken)

### Wo lege ich Skills ab — Projekt vs. User vs. Plugin?

- **Projekt** (`.claude/skills/`): Team-spezifisch, eingecheckt, vom Repo abhaengig.
- **User** (`~/.claude/skills/`): persoenlich, gilt in allen Projekten.
- **Plugin** (`<plugin>/skills/`): teilbar, versionierbar, ueber Marketplace.

Bei Team-Konventionen: Projekt-Skill. Bei eigenen Daily-Workflows: User-Skill. Bei "andere koennten das auch wollen": Plugin.

---

## Sicherheit

### Ist es OK, `--dangerously-skip-permissions` zu nutzen?

Nur in isolierten VMs oder Docker-Containern. Niemals auf deinem Haupt-Dev-Laptop fuer interaktive Sessions. Wenn du es brauchst, denke nochmal nach. Alternative: `--permission-mode auto` (Max-Plan oder Team/Enterprise) plus `allow/deny`-Rules fuer feingranulare Kontrolle.

### Was sind Protected Paths?

Auch in `bypassPermissions` schuetzt Claude bestimmte Pfade: `.git/`, `.claude/`, `.mcp.json`, Shell-Configs (`.bashrc`, `.zshrc`, `.profile`). Diese Liste ist hardcoded — Sicherheitsnetz gegen Self-Sabotage. Du kannst sie nicht override.

### Wie schuetze ich Secrets?

- Nie in `CLAUDE.md` schreiben (oder Project-`.claude/`-Files)
- `.env`-Files via Hook gegen Reads schuetzen (siehe Demo 2.2b "Secure Diff Gate")
- API-Keys als Env-Vars, nicht inline
- Permission-Rule `deny: ["Bash(cat .env*)", "Read(.env*)"]`
- `/security-review` regelmaessig laufen lassen
- Bei Codex-Pipelines: Code redacten vor Versand zu OpenAI

### Was ist der Unterschied zwischen Permission-Mode und Permission-Rule?

**Permission Mode** ist der globale Default-Level fuer eine Session (default / acceptEdits / plan / auto / dontAsk / bypassPermissions). **Permission Rule** ist die feingranulare Override-Regel in `settings.json` unter `allow`/`deny`/`ask` mit Patterns wie `Bash(npm test)` oder `WebFetch(domain:github.com)`.

Faustregel: Modes setzen die Tonart, Rules die einzelnen Noten.

### Kann ich Claude verbieten, bestimmte Files zu schreiben?

Ja, ueber Permission-Rules: `deny: ["Write(secrets/**)", "Edit(*.env)"]`. Zusaetzlich `paths:`-Filter in Skills, sodass bestimmte Skills nur in matchenden Verzeichnissen aktiv sind.

---

## Workflow

### Wie viele Subagents kann ich parallel laufen lassen?

Praktisch: 3-8 sind ein guter Wert (mit `/batch`). Mehr riskieren Ratelimits, je nach Plan. Token-Cost skaliert linear pro Subagent. Bei Background-Agents (`claude --bg`): laufen detached, Cost laeuft mit, also `--max-budget-usd` setzen.

### Wann nutze ich `/loop` vs. `/goal` vs. Routine?

- `/loop <interval> <prompt>`: Zeit-/Intervall-getriggert ("alle 5 Min check deploy")
- `/goal <condition>`: Condition-getriggert ("arbeite, bis Tests gruen") — seit v2.1.139
- **Routine**: Persistent, cron-aehnlich, ueberlebt CLI-Restart. Offizielle Variante.

Faustregel: `/loop` fuer adhoc Monitoring, `/goal` fuer task-orientierte Loops, Routine fuer Production-Scheduling.

### Wie passt das alles in einen Workflow?

Beispiel: `Plan -> Implement -> Review` mit Opus/Sonnet/Haiku. `/plan` mit Opus, `/batch` von Subagents mit Sonnet, `/review` mit Haiku. Plus: Pre-commit Hook der `/security-review` triggert, Hook auf `Stop` der Cost loggt.

### Wann nutze ich `/compact` vs. `/clear`?

- `/compact [focus]`: komprimiert die Conversation, behaelt relevante Kontextpunkte. Fuer lange Sessions, die nicht zu Ende sind.
- `/clear` (alias `/reset`, `/new`): wirft den gesamten Kontext weg. Fuer kompletten Themenwechsel.

Faustregel: `/compact` proaktiv bei ~70% Context-Fuelle, `/clear` zwischen voellig unzusammenhaengenden Tasks.

### Wie debugge ich einen Skill, der nicht triggert?

Siehe `resources/troubleshooting.md` Sektion 1. Kurz: `/skills` listet, `disable-model-invocation` pruefen, `paths:`-Filter pruefen, Trigger-Phrases praeziser machen.

---

## CLAUDE.md & Memory

### Wann CLAUDE.md, wann `.claude/rules/`?

- **CLAUDE.md**: globale Projekt-Regeln (immer geladen). Fuer Stack-Info, Konventionen, No-Go-Zones.
- **`.claude/rules/`**: pfad-spezifische Regeln (`paths:`-Filter). Werden nur geladen, wenn matchende Files im Kontext sind. Besser fuer grosse Codebases.

Faustregel: kleines Projekt (<50 Files) -> CLAUDE.md reicht. Grosses Projekt oder Monorepo -> rules/ mit modularen Pfaden.

### Auto-Memory ist nervig — wie deaktiviere ich es?

`claude --bare` startet ohne Auto-Memory (auch ohne Hooks, Skills, Plugins, MCP). Permanent off: in `settings.json` die Memory-Defaults anpassen (Setting-Name in der Doku pruefen). Falsche Auto-Notes kannst du auch direkt aus `~/.claude/projects/<hash>/memory/` loeschen, oder Claude per Prompt korrigieren ("Vergiss dass X, ich meinte Y").

### CLAUDE.md vs. AGENTS.md?

`AGENTS.md` ist die Codex/OpenAI-Convention. Per `@AGENTS.md`-Import in `CLAUDE.md` kannst du Interop nutzen, ohne beide Files getrennt zu pflegen. Real-world Setups, die mit mehreren Coding-Agents arbeiten, haben oft beides — `AGENTS.md` als Source-of-Truth, `CLAUDE.md` als Wrapper mit Claude-spezifischen Ergaenzungen.

### Wo schreibe ich persoenliche Notes, die NICHT ins Repo sollen?

`CLAUDE.local.md` im Repo-Root. In `.gitignore` aufnehmen. Wird neben `CLAUDE.md` geladen.

---

## CI/CD

### Kann ich Claude in GitHub Actions laufen lassen?

Ja — Modul 3.6 (geplant) zeigt das im Detail. Kern: `claude setup-token` einmalig fuer langlebigen OAuth-Token (~1 Jahr), `claude -p "task" --output-format json` als Befehl, `--max-budget-usd 0.50` als Sicherheitsnetz. Die aktuelle CLI bietet keine harte Turn-Grenze per Flag mehr — `--max-budget-usd` kappt Endlos-Loops/Runaway-Kosten.

### Was kostet ein Claude-PR-Reviewer im CI?

Pro PR ~$0.10-1.00 abhaengig von Diff-Groesse und Effort-Level. `--max-budget-usd` setzen. Fuer kleine PRs: Haiku reicht oft. Fuer Architektur-Reviews: Opus mit `--effort high`.

### Wie automatisiere ich PR-Fixes?

`/autofix-pr <num>` spawned eine Cloud-Session, die PR-CI watcht und Fixes pusht. Alternativ: GitHub-Action mit `claude -p`, die auf PR-Comments reagiert. Beides setzt einen langlebigen Token via `claude setup-token` voraus.

### Was ist `--bare` Mode?

Headless ohne Hooks, Skills, Plugins, MCP, Auto-Memory. Maximal schnell, maximal predictable, maximal Token-sparend. Fuer CI/Scripts, wo du genau eine Operation willst ohne Side-Effects der Konfiguration.

---

## Cost & Limits

### Wie senke ich meine Tagespauschale?

- Modell-Wechsel: Sonnet/Haiku statt Opus, wo moeglich
- Effort-Level absenken (`/effort low` fuer einfache Tasks)
- `CLAUDE.md` schlank halten — jedes Token zaehlt
- `/compact` proaktiv vor langen Sessions
- `--bare` Mode fuer Scripts
- Subagents nur wo wirklich noetig (jeder hat eigenen Token-Stack)
- Cache-Reuse: Bei kurz aufeinanderfolgenden `claude -p`-Calls profitiert prompt-caching

### Was ist Effort-Level und wann nutze ich was?

`low` fuer triviale Aufgaben (kommentar-fix, einfache Lookups). `medium` fuer Standard-Coding. `high` (Default auf Opus 4.8) fuer Refactors und schwierigere Bugs. `xhigh` und `max` (auf Opus 4.7, Opus 4.8 und Fable 5) fuer Architektur-Entscheidungen und komplexe Root-Cause-Analyse. Trade-off: Tiefe vs. Latenz/Cost — `max` kann 5-10x so lange brauchen wie `medium`.

---

*Siehe auch `resources/glossary.md` und `resources/troubleshooting.md`. Vertieftes Material in den Modulen.*
