# Persona: Currency-Auditor: Modelle, Preise, Effort-Stufen

**Scope:** 

## Gesamteindruck

Der Workshop dokumentiert Modell- und Preis-Daten von Mai 2026, die durch Entwicklungen im Juni 2026 veraltet sind. Claude Opus 4.8 löst 4.7 ab, Claude Fable 5 ist GA, und Effort-Level-Defaults ändern sich. Die Einstiegshuerde für Lernende bleibt moderat (Neulingen ist egal, ob sie 4.7 oder 4.8 nennen), aber die Veralterung untergraebt Vertrauen in die Materialien und führt zu verwirrten Copy-Paste-Commands. Keine Blockade für Lernziele, aber Glaubwürdigkeitsverlust.

## Staerken (was bleiben soll)

- **Preis-Struktur bleibt stabil** — Die Preis-pro-MTok-Verhaeltnisse (Opus ~3x Sonnet, Haiku ~0.2x) sind unverändert und bleiben valid für Cost-Engineering-Diskussionen.
- **Effort-Level-Konzept ist solide** — Die Erklärung der Effort-Levels als Cost-Dial (low/medium/high/xhigh/max) in Modul 1.5 ist konzeptuell korrekt; nur die Zuordnung zu Modellen ist veraltet.
- **Plan/Implement/Review-Pipeline-Strategie gilt immer noch** — Die Multi-Modell-Strategie (Opus für Plan/Review, Sonnet für Implement, Haiku für Bulk) bleibt gültig und ist nicht an ein bestimmtes Modell-Release gebunden.

## Befunde

### [high | currency | S] Opus 4.7 als default nennen, aber 4.8 ist jetzt default seit v2.1.154 (28.5.2026)

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 14: 'Choose the right model (Opus 4.7 / Sonnet 4.6 / Haiku 4.5)' Zeile 162: 'Claude Opus 4.7 (default since 2026-04-16 GA)' Zeile 169: '`xhigh` and `max` unlock the deepest reasoning with Opus 4.7' Aktuelle Realitaet (Web): 'as of v2.1.154 (May 28, 2026), Opus 4.8 is the new default with high effort by default'
- **Empfehlung:** Alle Opus-4.7-Referenzen durch Opus 4.8 ersetzen. Zeile 162 auf 'default since 2026-05-28 (v2.1.154 GA)' aendern. Das Datum 2026-04-16 ist ein frueheres GA-Datum (wahrscheinlich bei Opus 4.7 Announcement), der neue Default kam erst mit 4.8 am 28.5.

### [high | currency | M] Claude Fable 5 vollstaendig abwesend aus Modelltabelle

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 158-164: Tabelle nennt nur Opus 4.7, Sonnet 4.6, Haiku 4.5 Zeile 308-310 (cheatsheet.md): Nur die drei genannten Modelle Actual (web, 2026-06-09 GA): 'Claude Fable 5 is Anthropic\'s most capable widely released model' with pricing $10 / $50 per MTok, 1M context, available on Claude API, Bedrock, Vertex, Foundry
- **Empfehlung:** Modelltabelle erweitern: nach oder vor Opus 4.8 eine Row für Fable 5 hinzufuegen. Kopfzeile sollte Fable 5 alarmieren, dass es ein Premium-Tier ist. Sollte erwähnt werden in: Block 1.1 (Uebersicht), Cheatsheet, Mentor-Agent, Block 3.2 (Multi-Model-Pipelines).

### [high | currency | S] Cheatsheet veraltet: Opus 4.7 statt 4.8, keine Fable 5

- **Datei:** resources/cheatsheet.md
- **Evidenz:** Zeile 308: 'Claude Opus 4.7 | 1M tokens | Default in Claude Code since 2026-04-16 (GA)' Zeile 309: 'Claude Sonnet 4.6 | 1M tokens (beta)' Zeile 310: 'Claude Haiku 4.5 | 200K tokens' Zeile 312: 'Claude Code defaults to Opus 4.7 with 1M context' Keine Fable 5 erwähnt Actual: Opus 4.8 default seit 28.5.2026, Fable 5 GA seit 9.6.2026
- **Empfehlung:** Tabelle neu schreiben: (1) Opus 4.8 als default angeben, (2) Fable 5 hinzufuegen mit Pricing/Context, (3) Datum auf 2026-05-28 aendern, (4) '(beta)' von Sonnet entfernen

### [medium | currency | S] Effort-Level-Verhalten fuer Opus 4.8 ungenau

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 169: '/effort <low|medium|high|xhigh|max> — five tiers ranging from cheap-and-fast to deepest analysis (xhigh and max unlock the deepest reasoning with Opus 4.7)' Actual (web): 'On Claude Opus 4.8, the effort parameter defaults to high on all surfaces, including the Claude API and Claude Code. Set effort explicitly to use a different level.'
- **Empfehlung:** Klarstellen: Opus 4.8 defaults zu `high` (nicht `xhigh`). Die `xhigh`/`max`-Levels existieren weiterhin, sind aber nicht mehr der Default. Satz umschreiben: '`low|medium|high|xhigh|max` — five tiers; Opus 4.8 defaults to `high` (xhigh/max unlock even deeper reasoning when explicitly set)'

### [medium | currency | M] Block 3.2: Modell-Staerken-Tabelle fehlt Fable 5

- **Datei:** resources/modules/block-3-advanced.md
- **Evidenz:** Zeile 336-341: Tabelle nennt 'Claude Opus | Claude Sonnet | Claude Haiku | Codex (OpenAI)' Zeile 343-344: 'Using both together beats either alone' Keine Fable 5; kein Hinweis auf Mythos-Klasse Actual: Fable 5 uebertrifft alle genannten Claude-Modelle, ist ein separate Tier
- **Empfehlung:** Tabelle erweitern: 'Claude Fable 5' als neue Zeile hinzufuegen mit Strengths wie 'Highest reasoning, frontier performance, long-horizon agentic tasks'. Context: 'This is Anthropic\'s new Mythos-class tier, available since June 2026. Use when maximum capability is worth the cost.' Codex-Kontext klären: 'Codex (OpenAI) remains relevant for fast, parallel implementation, though Claude Sonnet/Opus can often substitute.'

### [medium | currency | S] Mentor-Agent nennt alte Modelle, keine Fable 5

- **Datei:** agents/workshop-mentor.md
- **Evidenz:** Zeile 149: 'Which model should I use? Think of it like staffing (module 1.1, Model Selection): Opus is your senior architect ... Sonnet is your experienced technician ... Haiku is your assistant — cheap for simple tasks.' Keine Erwähnung Fable 5, alte Modell-Generationen
- **Empfehlung:** Antwort aendern: 'Opus 4.8 is your senior architect. Fable 5 (new, since June 2026) is your principal engineer — highest capability, premium cost. Sonnet is your experienced technician. Haiku is your assistant.'

### [low | currency | S] Modul 1.5 Preistabelle (as of 2026-05) ist noch aktuell, aber Datum sollte auf 2026-06 aendern

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 950: '### Pricing Reference (as of 2026-05)' Zeile 954-956: Tabelle mit Opus 4.7, Sonnet, Haiku — preise korrekt Aber: Das Datum ist vorbei, und Fable 5 fehlt
- **Empfehlung:** Datum auf '(as of 2026-06)' aendern, Fable 5-Row hinzufuegen ($10/$50), Note hinzufuegen: '(Fable 5 is a new premium tier, generally available since June 9, 2026 — see Module 1.1 for context)'

### [low | currency | S] Haiku Kontext 200K vs 1M fuer Opus 4.8 nicht erklauert

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Zeile 164: 'Claude Haiku 4.5 | 200K tokens' Zeile 162: 'Claude Opus 4.7 | 1M tokens' Die Implication (1M vs 200K) ist offensichtlich, aber kein expliziter Hinweis auf Konsequenzen (z.B. Haiku kann weniger Dateien auf einmal lesen)
- **Empfehlung:** Footnote hinzufuegen: '200K context limits bulk-read tasks — use Haiku for small/focused reads, Opus for whole-codebase analysis.' Nicht essentiell fuer Anfaenger, aber hilft bei Troubleshooting.

### [low | currency | S] Mentor-Agent Module Map hat veraltete Block-Struktur: 'model: sonnet' statt Fable 5 / Opus 4.8 als Beispiel

- **Datei:** agents/workshop-mentor.md
- **Evidenz:** Zeile 28: 'model: sonnet' — OK fuer Read-Only Agent, aber wenn der Mentor kuenftig komplexere Fragen beantworten soll (z.B. Entscheidungslogik fuer Modell-Wahl), sollte er Zugriff auf Opus/Fable haben
- **Empfehlung:** Nicht dringend. Optional: auf 'model: opus' aendern, wenn der Mentor in Zukunft tiefere Reasoning-Faehigkeiten braucht. Jetzt: Notiz hinzufuegen '(Can be upgraded to Opus 4.8 or Fable 5 if future versions require deeper reasoning.)'

### [low | currency | S] Veraltete CLI-Version in Struktur-Kontext

- **Datei:** global
- **Evidenz:** Repo-Header erwaehnt: 'mutmasslich veraltet — pruefe gegen aktuelle Claude-Code-Releases und die aktuelle Modell-/Preis-Liste' und nennt 'v2.1.146 als CLI-Version (Stand 2026-05)' Aktual (web): v2.1.170+ (Juni 2026), mit Fable 5 Support, dynamischen Workflows, etc.
- **Empfehlung:** Nicht im Workshop-Content selbst erwaehnt, aber der Setup-Guide / Prerequisites sollte klarstellen: 'Update to Claude Code v2.1.170+ (June 2026 or later) for Fable 5 support and latest features. Run `claude update` to get the latest version.'
