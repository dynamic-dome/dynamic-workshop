# Trainer Notes — Claude Code Workshop

> Begleitdokument fuer Workshop-Trainer. Talking-Points pro Modul, Recovery-Strategien,
> Pre-Workshop-Skript, "If everything is on fire"-Cheatsheet.
> Stand: 2026-05-20.

## Quick Reference for Trainers

### Before the Workshop (1-2 Wochen vorher)

1. **Setup-Check mit allen Teilnehmern** — 30 Min Onboarding-Call pro Teilnehmer
   - Verifiziere: `claude --version`, `git --version`, `python3 --version`, `gh auth status`
   - Workshop-Plugins installieren (falls verfuegbar — sonst klar markieren als Demo-only)
   - NotebookLM-Account-Erstellung
   - Workshop-Playground klonen
2. **Eigene Maschine vorbereiten**:
   - Alle Demos einmal komplett durchspielen
   - Pre-flight-Skript: siehe Pre-Flight-Checklist unten
   - Cost-Account mit ~$50 Budget einrichten
3. **Material reviewen**:
   - session-plan.md durchgehen, Reihenfolge memorisieren
   - Recovery-Notes pro Demo lesen
   - faq.md ueberfliegen fuer Standard-Fragen

### Pre-Flight Checklist (am Workshop-Tag)

Vor der Session 30 Min vorher:

```bash
# 1. Claude Code funktioniert
claude --version
claude /doctor

# 2. Workshop-Repo aktuell
cd ~/cc-workshop/dynamic-workshop
git pull

# 3. Playground baut
cd workshop-playground/
python3 -m pytest -v       # Python playground
make                        # C playground (if installed)

# 4. Plugins geladen
claude plugin list

# 5. MCP-Server konfiguriert (fuer Demo 2.4)
claude mcp list

# 6. NotebookLM-Notebook vorhanden (fuer Demo 2.5)
notebooklm list             # if CLI available

# 7. Tokens / Budget
/cost                       # current session
/usage                      # day-aggregate
```

### Common Live-Failure Modes (and Recovery)

| Problem | Schnell-Recovery |
|---|---|
| Demo laeuft nicht reproducible (Claude antwortet anders als gestern) | Akzeptiere als Teaching-Moment: "siehe, LLMs sind nicht deterministisch — deshalb Hooks und Tests" |
| `gh auth` ist abgelaufen | Skip PR-Step, demonstrate per `git push` |
| Plugin nicht installiert | Discussion statt Demo, oder vorab-aufgezeichnetes Video |
| Internet bricht | Switch zu `--bare` / offline-Demos (Modul 1.5 Cost zeigt Pattern) |
| `/cost` zeigt nichts | API-Console oeffnen (console.anthropic.com/usage) |
| Auto-Memory zeigt drift | Live debuggen mit Modul 3.7-Patterns — wird zur unplanned Modul-3.7-Demo |
| Teilnehmer-Maschine bricht beim Setup | Vorab `~/cc-workshop`-Bundle bereithalten, USB-Stick |

### If Everything Is On Fire — 5-Minute Improvisation

Wenn 3+ Demos in Folge nicht funktionieren:

1. **Stop the demo flow.** "Ich mache eine 5-Min-Pause."
2. **Use the Cheatsheet as anchor.** `resources/cheatsheet.md` — geh durch die wichtigsten 10 Commands
3. **Pivot to discussion.** "Was wuerdet ihr in eurem Job damit machen?" — sammle Use-Cases, diskutiere
4. **Use the Capstone (Exercise 3.5) earlier.** Architecture Discussion laesst sich an jeder Stelle einbauen
5. **Be honest.** "Das Tool ist neu, manche Demos sind fragil. Das ist Real-World-Tool-Adoption."

## Module-by-Module Talking Points

### Block 1 — Foundations

#### Module 1.1: What is Claude Code?

**Opener (1 Min):**
> "Wir haben heute drei Stunden, um euch Claude Code beizubringen. Das ist nicht ChatGPT —
> das ist ein Werkzeug mit Filesystem-Access, Bash-Execution, Git-Integration. Heute lernen
> wir, wie man das verantwortlich nutzt."

**Mental Models to Establish:**
1. "Claude Code ist kein Chat — es ist ein Agent mit echten Effekten."
2. "Eure Permission-Modes sind Card-Access-Levels. Default ist Visitor. Auto ist Smart-Badge."
3. "Modelle: Opus fuer Architektur, Sonnet fuer Coding, Haiku fuer Bulk. Das ist die Drei-Klassen-Faustregel."

**Wenn Teilnehmer fragt "Ist das nicht wie Copilot?":**
> "Copilot vervollstaendigt Code in deinem Editor. Claude Code arbeitet in deinem Filesystem,
> startet Tests, committed Code, ruft externe APIs. Es ist eine andere Kategorie."

**Closing:**
> "Block 1 baut die Grundlagen. Block 2 zeigt wie ihr das Tool erweitert. Block 3 wird Multi-Agent."

#### Module 1.2: Context & Memory

**Opener:**
> "Ein LLM ohne Kontext ist wie ein Sicherheitsbeamter ohne Briefing. CLAUDE.md ist das Briefing-Dokument."

**Mental Models:**
1. "CLAUDE.md = Site-Access-Policy. Wird vor jeder Schicht gelesen."
2. "Auto-Memory = Patrol-Log, der sich selbst schreibt. Wertvoll, aber pruefen."
3. ".claude/rules/ = Zone-spezifische Policies. Wichtig fuer grosse Codebases."

**Wenn Teilnehmer fragt "Geht Auto-Memory zu Anthropic?":**
> "Ja. Auto-Memory wird in den Prompt geladen, der zu Anthropic geht. Deshalb: keine Secrets,
> kein sensibles Material. Periodisch pruefen mit `cat MEMORY.md`."

#### Module 1.3: Effective Prompting

**Opener:**
> "Der Modellqualitaets-Unterschied zwischen einem schlechten und einem guten Prompt ist groesser
> als zwischen Sonnet und Opus."

**Mental Models:**
1. "Contractor-Analogie: Du schreibst keine Demands, du schreibst Work-Orders."
2. "Plan Mode = Sicherheits-Briefing vor der Aktion. Nutzen wenn du nervoes bist."
3. "Effort-Level = Tempo vs Qualitaet. xhigh kostet 4x, gibt ~1.5x Qualitaet."

#### Module 1.4: Git Integration & Worktrees

**Opener:**
> "Git ist eingebaut. Branch, Commit, Push, PR — alles im Gespraech. Worktrees sind die Test-Bench."

**Mental Models:**
1. "Worktree = Test-Bench im Labor. Production-Branch bleibt unberuehrt."
2. "/autofix-pr = Auto-Repair-Truck. Nur fuer Lint/Test-Fehler — nie Production."

#### Module 1.5: Cost Engineering

**Opener:**
> "Das ist das Modul, das euer Manager wissen muss. Cost ist nicht 'wir sehen mal' — Cost ist
> eine bewusste Variable wie Latency oder Memory."

**Mental Models:**
1. "Drei-Modell-Pipeline: Opus plant, Sonnet baut, Haiku reviewt."
2. "Effort-Level ist ein Dial, kein Schalter. xhigh ist nicht 'einfach besser'."
3. "Budget-Cap (`--max-budget-usd`) ist nicht optional — es ist Pflicht fuer autonome Loops."

### Block 2 — Ecosystem

(Talking Points fuer 2.1 - 2.5 in gleicher Struktur — siehe Modul-Files fuer Details)

#### Module 2.1: Skills & Commands

**Opener:**
> "Wenn du eine Anweisung dreimal getippt hast, ist sie ein Skill. Heute lernen wir wie man die packt."

#### Module 2.2: Hooks

**Opener:**
> "Hooks sind Sensoren in deinem Workflow. Sie feuern bei Events. Sie sind nicht 'Policy-Enforcement' —
> sie sind Best-Effort-Guards."

#### Module 2.3: Plugins

**Opener:**
> "Plugins sind Module. Skills + Hooks + Agents + Commands in einem Paket. Im Workshop benutzen
> wir vier Custom-Plugins — die sind als Demonstration gedacht, nicht als 'Produkt'."

#### Module 2.4: MCP

**Opener:**
> "MCP verbindet Claude Code mit der Aussenwelt. Browser, Datenbanken, Slack, eigene APIs."

#### Module 2.5: RAG & NotebookLM

**Opener:**
> "RAG = 'Claude liest deine Doku bevor es antwortet.' Wichtig: Daten gehen zu Google.
> Fuer sensitives Material: lokale RAG-Alternativen."

### Block 3 — Advanced

(siehe Modul-Files)

#### Module 3.1: Agents & Multi-Agent

**Opener:**
> "Subagents = Mehrere Claude-Instanzen, jede mit eigenem Kontext. Wie ein Team von Spezialisten."

#### Module 3.2: Multi-Model Pipelines

**Opener:**
> "Manche Tasks profitieren von Claude-PLUS-Codex. Aber: Codex schickt Code zu OpenAI. Bei sensiblem Code: skip."

#### Module 3.3: Security & Adversarial Testing

**Opener:**
> "Der spannendste Block. Adversarial Testing mit Devil's-Advocate-Swarms. Permission-Modes, Protected Paths, Sandboxing."

#### Module 3.4: Scheduled Tasks & Automation

**Opener:**
> "Was kann Claude fuer dich tun, waehrend du nicht zuschaust? Schedule, Loop, Goal — alle mit Budget-Cap."

#### Module 3.5: Telegram, Inception & Worktrees

**Opener:**
> "Multi-Agent visualisiert. /remote-control fuer Mobile, Worktree-Isolation fuer sichere Experimente."

#### Module 3.6: CI/CD & Headless

**Opener:**
> "Claude Code in der Pipeline. claude -p, JSON-Output, Cost-Caps. Das ist die Produktions-Integration."

#### Module 3.7: Troubleshooting & Debugging

**Opener:**
> "Wenn etwas nicht laeuft: 8 Schritte. Skill triggert nicht? Hook blockt falsch? MCP timed out?
> Hier ist die Werkbank."

## Pre-Workshop Email Template

Eine Woche vor Session 1, an alle Teilnehmer:

```
Subject: Claude Code Workshop — Pre-Workshop Setup (1 Woche vor Session 1)

Hi [Name],

eure Session 1 ist am [Datum]. Damit wir mit voller Geschwindigkeit starten koennen,
bitte folgendes vorher pruefen:

1. **`resources/prerequisites.md` durcharbeiten** — Setup, Auth, Tools.
   Plane 1-2 Stunden ein.

2. **Workshop-Playground klonen:**
   ```bash
   git clone https://github.com/dynamic-dome/dynamic-workshop.git ~/cc-workshop/dynamic-workshop
   cd ~/cc-workshop/dynamic-workshop
   ```

3. **Workshop-Plugins:** Optional fuer Block 2/3. Ich bringe sie vorbereitet mit fuer Session 2.

4. **Account-Setup:** Claude Pro/Max ($20/Monat) reicht fuer Block 1+2. Fuer Block 3
   Multi-Agent-Demos: $30-50 zusaetzliches Budget einplanen.

5. **Pre-Session-Call:** Bitte 30 Min mit mir am [Termin] fuer Setup-Check.

Bei Fragen: einfach antworten.

Bis bald,
[Trainer]
```

## Slide-Index zu claude-code-workshop.pptx

(Arbeitsstand fuer `claude-code-workshop.pptx`. Vor einer Live-Session einmal gegen das Deck pruefen.)

| Modul | Slide-Nummern | Inhalt |
|---|---|---|
| Intro | 1-5 | Welcome, Agenda, Format |
| Module 1.1 | 6-12 | Five Surfaces, Tools, Permissions, Models |
| Module 1.2 | 13-18 | CLAUDE.md, Auto-Memory, Rules |
| Module 1.3 | 19-24 | Prompting Patterns, Plan Mode, Effort |
| Module 1.4 | 25-30 | Git, Worktrees, /autofix-pr |
| Module 1.5 | 31-36 | Cost Engineering, Pricing, Effort-Strategy |
| Module 2.1 | 37-43 | Skills, Frontmatter, Bundled Skills |
| Module 2.2 | 44-49 | Hook Events, Execution Types |
| Module 2.3 | 50-54 | Plugin Anatomy, Marketplaces |
| Module 2.4 | 55-60 | MCP Transports, OAuth, Building Your Own |
| Module 2.5 | 61-65 | RAG, NotebookLM, Limitations |
| Module 3.1 | 66-73 | Agents, Background, Patterns |
| Module 3.2 | 74-77 | Multi-Model, Cost Trade-Off |
| Module 3.3 | 78-86 | Security, Permissions, Sandboxing, CVE |
| Module 3.4 | 87-91 | Schedule, Loop, Goal, Routines |
| Module 3.5 | 92-96 | Remote, Telegram, Inception |
| Module 3.6 | 97-102 | CI/CD, Headless, GitHub Actions |
| Module 3.7 | 103-108 | Troubleshooting, Debug, Diagnosis |
| Outro | 109-112 | Capstone, Resources, Q&A |

**Note:** Slide-Nummern sind ein Arbeitsindex. Vor der naechsten Live-Session gegen das aktuelle Deck verifizieren.

---

*Stand 2026-05-20. Diese Datei begleitet den Workshop fuer Trainer. Teilnehmer brauchen sie nicht.*
