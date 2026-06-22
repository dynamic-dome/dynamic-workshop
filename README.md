# Claude Code Workshop

> Praxisnaher Workshop fuer Entwickler, die Claude Code produktiv einsetzen wollen.
> 3 Sessions, 17 Module (Block 1: 5, Block 2: 5, Block 3: 7), demo-lastig mit optionalen Hands-on-Uebungen.

Dieses Repository ist die Materialbasis hinter der DoMe-Dynamics-Workshop-Seite:

- **Website:** https://dynamic-dome.com/workshop - kuratierter Ueberblick und Arbeitsprobe
- **Repo:** Material, Demos, Exercises, Mentor-Agent und Playground
- **Kontext:** Teil der DoMe-Dynamics-Werkstattlinie: Werkstatt -> DCO -> Workshop

Die Website zeigt, warum der Workshop als Engineering-Arbeitsprobe zaehlt. Dieses Repo zeigt, womit er konkret funktioniert.

---

## Fuer wen ist das?

- **Selbstlerner** — Du willst Claude Code eigenstaendig lernen und suchst strukturiertes Material mit Demos und Uebungen.
- **Moderatoren** — Du willst den Workshop fuer dein Team oder deine Community halten und brauchst fertige Unterlagen.
- **Reviewer / Tech Leads** — Du willst einschaetzen, ob hier nur Folien liegen oder ein reproduzierbarer Lernpfad mit Demos, Recovery-Notes und Playground existiert.

Vorkenntnisse: Programmiererfahrung vorhanden, aber keine Erfahrung mit Coding Agents noetig.

---

## Quick Start

### Als Selbstlerner

1. `resources/prerequisites.md` durcharbeiten (Installation, Auth, Tools)
2. `resources/workshop-guide.md` als **Haupt-Navigation** und Lern-Routine nutzen (ersetzt den Moderator); `WORKSHOP_EINFUEHRUNG.md` gibt die Kurz-Orientierung
3. Block fuer Block durcharbeiten:
   - `resources/modules/block-1-foundations.md` lesen
   - `resources/demos/block-1-demos.md` nachvollziehen
   - `resources/exercises/block-1-exercises.md` ausprobieren
4. Trainer-Ersatz-Ressourcen (wenn du allein arbeitest und niemand zum Fragen da ist):
   - `resources/faq.md` — Konzeptfragen ("warum/wann nutze ich X?")
   - `resources/troubleshooting.md` — wenn etwas klemmt (Fehlermeldungen, Hooks, Plugins)
   - `resources/glossary.md` — unklare Begriffe nachschlagen
   - `resources/cheatsheet.md` + `resources/quick-reference.md` — Referenz / Schnellzugriff
5. Weiter mit Block 2 und 3

### Als Reviewer

1. Website-Ueberblick lesen: https://dynamic-dome.com/workshop
2. `resources/session-plan.md` pruefen: Ablauf, Timing, Session-Logik
3. `resources/modules/` und `resources/demos/` gegenlesen: fachliche Tiefe und Demo-Faehigkeit
4. Playground testen: `cd workshop-playground && pip3 install -r requirements.txt && python3 -m pytest -v` (Windows: `pip`/`python` statt `pip3`/`python3`)
5. `agents/workshop-mentor.md` pruefen: guide/learn-Modus und didaktische Rueckfragen

### Als Moderator

1. `resources/prerequisites.md` **vorab an Teilnehmer schicken** (min. 1 Woche vorher)
2. Eigene Installation pruefen: `claude --version`, `python3 --version` (Windows: `python --version`), `git --version`
3. Playground testen: `cd workshop-playground && pip3 install -r requirements.txt && python3 -m pytest -v` (Windows: `pip`/`python` statt `pip3`/`python3`)
4. Optional — Workshop-Plugin installieren und `/workshop guide 1.1` testen
5. Praesentationsfolien: `claude-code-workshop.pptx` als visuellen Einstieg nutzen
6. Pro Session: Folien → Demos vorführen → Teilnehmer ueben lassen → Q&A

---

## Kursstruktur

### Session 1 — Foundations (~3h)

> "Was ist Claude Code und warum sollte mich das interessieren?"

| Modul | Thema | Highlight-Demo |
|-------|-------|----------------|
| **1.1** | Was ist Claude Code? | Log-Parser in 3 Minuten bauen |
| **1.2** | Context & Memory | CLAUDE.md anlegen, `/compact` + `/cost` zeigen |
| **1.3** | Effective Prompting | Vager vs. praeziser Prompt Side-by-Side |
| **1.4** | Git Integration | Branch → Feature → Commit → PR in einem Flow |
| **1.5** | Cost Engineering & Effort Management | `/cost`, `/usage`, `/insights` und Effort-Level als Kosten-Hebel |

### Session 2 — Ecosystem (~3h)

> "Wie macht man Claude Code richtig maechtig?"

| Modul | Thema | Highlight-Demo |
|-------|-------|----------------|
| **2.1** | Skills & Commands | Eigenen Security-Skill live bauen |
| **2.2** | Hooks | Hook der `rm -rf` blockiert |
| **2.3** | Plugins | Plugin-Anatomie durchgehen |
| **2.4** | MCP | Playwright: Claude steuert einen Browser |
| **2.5** | RAG & NotebookLM | Knowledge Base erstellen und abfragen |

### Session 3 — Advanced (~3h)

> Multi-Agent-Workflows, Security, Automation, CI/CD und Troubleshooting.

| Modul | Thema | Highlight-Demo |
|-------|-------|----------------|
| **3.1** | Agents | 2 parallele Agents auf echtem Task |
| **3.2** | Multi-Model Pipelines | Codex Swarm baut CLI-Tool |
| **3.3** | Security & Adversarial | Devil's Advocate Swarm auf vulnerablem Code |
| **3.4** | Automation | Self-Improve Loop: Vorher/Nachher |
| **3.5** | Full Stack Architecture | Gruppen-Discussion: Design your Workflow (Capstone) |
| **3.6** | CI/CD & Headless Mode | `claude -p` mit `--output-format json` als Pipeline-Stage |
| **3.7** | Troubleshooting & Debugging | `/debug`, `/doctor`, `claude --verbose` Layer-fuer-Layer |

Jeder Block hat passende Dateien unter `resources/modules/`, `resources/demos/` und `resources/exercises/`.

---

## Wie das Repo in DoMe Dynamics passt

Die Workshop-Seite auf DoMe Dynamics ist bewusst kein Buchungsangebot, sondern ein sichtbarer Lab-Stand. Das Repo ist der Nachweis dahinter:

| Ebene | Rolle |
|-------|-------|
| `Werkstatt` | Erklaert, wie aus einzelnen Tools ein persoenlicher Arbeitsmodus wurde. |
| `DCO` | Zeigt ein gebautes agentisches System mit Toolgrenzen, Dashboard und Freigaben. |
| `dynamic_workshop` | Uebersetzt diese Praxis in ein Curriculum fuer Entwicklerteams. |

Damit ist der Workshop nicht nur "Lehre ueber Claude Code", sondern eine Enablement-Schicht ueber realer Agentenpraxis.

---

## Verzeichnisstruktur

```
dynamic_workshop/
├── README.md                       ← Du bist hier
├── WORKSHOP_EINFUEHRUNG.md         ← Orientierung und Einstieg
├── CLAUDE.md                       ← Projektkontext fuer Claude Code
├── claude-code-workshop.pptx       ← Praesentationsfolien
├── resources/
│   ├── prerequisites.md            ← Setup-Anleitung (vorab verteilen!)
│   ├── cheatsheet.md               ← Referenz-Karte (CLI, Shortcuts, Commands)
│   ├── workshop-guide.md           ← Leitfaden fuer Selbststudium
│   ├── modules/
│   │   ├── block-1-foundations.md   ← Lehrmaterial: Foundations
│   │   ├── block-2-ecosystem.md     ← Lehrmaterial: Ecosystem
│   │   └── block-3-advanced.md      ← Lehrmaterial: Advanced
│   ├── demos/
│   │   ├── block-1-demos.md         ← Demo-Scripts Block 1
│   │   ├── block-2-demos.md         ← Demo-Scripts Block 2
│   │   └── block-3-demos.md         ← Demo-Scripts Block 3
│   └── exercises/
│       ├── block-1-exercises.md     ← Uebungen Block 1
│       ├── block-2-exercises.md     ← Uebungen Block 2
│       └── block-3-exercises.md     ← Uebungen Block 3
├── workshop-playground/             ← Demo-Repo mit 3 Vulnerabilities
│   ├── access_control.py
│   ├── test_access_control.py
│   └── requirements.txt
├── .claude-plugin/                  ← Plugin-Manifest
├── skills/                          ← Workshop-Skill (guide/learn Logik)
├── agents/                          ← Workshop-Mentor Agent
└── commands/                        ← /workshop Command
```

---

## Workshop-Plugin (optional)

Dieses Repo ist gleichzeitig ein Claude-Code-Plugin mit zwei Modi:

- **`/workshop guide 1.1`** — Moderator-Modus: Talking Points, Demo-Scripts, Timing
- **`/workshop learn 1.1`** — Lern-Modus: Interaktive Erklaerungen mit Verifikation

**Installation:** Repo klonen, dann in Claude Code als lokales Plugin einbinden.
Modulnummern: `1.1`–`1.5`, `2.1`–`2.5`, `3.1`–`3.7`

---

## Workshop Playground

Das Verzeichnis `workshop-playground/` enthaelt ein kleines Python-Projekt mit **3 absichtlich eingebauten Sicherheitsluecken** (Command Injection, Hardcoded Credentials, Path Traversal). Es dient als realistisches Uebungsobjekt fuer Demos und Exercises.

```bash
cd workshop-playground
pip3 install -r requirements.txt   # Windows: pip install -r requirements.txt
python3 -m pytest -v               # Windows: python -m pytest -v
```

---

## Materialien auf einen Blick

| Ich will... | Starte hier |
|-------------|-------------|
| Alles installieren | `resources/prerequisites.md` |
| Den Workshop verstehen | `WORKSHOP_EINFUEHRUNG.md` |
| Selbst durcharbeiten | `resources/workshop-guide.md` |
| Oeffentlichen Kontext sehen | https://dynamic-dome.com/workshop |
| Schnell nachschlagen | `resources/cheatsheet.md` |
| Live praesentieren | `claude-code-workshop.pptx` + `resources/demos/` |
| Ueben | `resources/exercises/` + `workshop-playground/` |
