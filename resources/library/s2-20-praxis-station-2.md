---
id: S2.20
type: practice
title: "Praxis-Station Session 2: eine Übung wählen"
shelf: practice
level: core
minutes: 18
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann eine der sechs Übungen aus Session 2 (Skill, Safety-Hook, Plugin, MCP, Wissensbasis, Token Firewall) passend zu meinem Ziel auswählen, sie selbstständig bis zu ihrer Liste Geschafft, wenn durchführen und das Ergebnis begründen."
sources: []
aliases: []
offers: [S2.2, S2.8, S2.10, S2.11, S2.14, S2.18]
---

# S2.20 · Praxis-Station Session 2: eine Übung wählen

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~18 Min** · **Voraussetzungen:** keine
>
> ← [S2.19 Grenzen von RAG und Datenschutz](s2-19-rag-grenzen.md) · [Bibliothek](README.md) · [X.1 Community-Skills: wer baut was, das wirklich hilft](x-01-community-skills.md) →
<!-- meta:end -->

## Auf einen Blick

Hier wählst du eine der sechs Übungen aus Session 2: einen Skill schreiben, einen Safety-Hook bauen, ein Plugin erkunden, einen MCP-Server anbinden, eine eigene Wissensbasis anlegen oder als Bonus eine Token Firewall bauen. Im Workshop nimmst du dir eine vor, die anderen sind fürs Selbststudium. Rechne mit 30–40 Minuten je Übung; die Kernschritte allein schaffst du in etwa 20–25.

## Selbst machen

### Bevor du anfängst

- **Zeit.** Eine Übung braucht realistisch 30–40 Minuten, wenn du die Neustarts mitzählst, die die Hook- und MCP-Übungen vorsehen, und den ersten Download per `npx`. Die Kernschritte passen in etwa 20–25 Minuten. Bonus- und Stretch-Schritte sind freiwillig; lass sie weg, wenn die Zeit knapp ist. Im Workshop hat die Station 18 Minuten.
- **Playwright vorab laden.** Lade den Playwright-MCP vor Session 2 herunter ([Vorbereitung](../moderation/vorbereitung.md#playwright-mcp-vorab-laden)), damit Übung 2.4 nicht an einem Live-Download hängen bleibt.
- **Aufbau.** Jede Übung hat ein Ziel, Schritte, eine Liste „Geschafft, wenn" und Tipps, wie in [S1.20](s1-20-praxis-station-1.md#selbst-machen) beschrieben.

### Welche Übung passt zu dir?

| Dein Ziel | Übung | Du brauchst | Kapitel |
|---|---|---|---|
| Eine Anweisung, die du immer wieder von Hand tippst, nur noch einmal aufschreiben | Übung 2.1: deinen ersten Skill bauen | einen Ablauf, den du oft wiederholst | [S2.2](s2-02-skill-schreiben.md#selbst-machen) |
| Ein Sicherheitsnetz, das gefährliche Shell-Befehle in jeder Sitzung abfängt | Übung 2.2: einen Safety-Hook bauen | `jq` für die bash-Fassung, sonst die PowerShell-Fassung | [S2.8](s2-08-hook-einrichten.md#selbst-machen) |
| Verstehen, was in einem Plugin steckt, und ein eigenes Mini-Plugin aufsetzen | Übung 2.3: ein Plugin erkunden und selbst aufsetzen | ein installiertes Plugin oder das Kurs-Repo | [S2.11](s2-11-plugins-buendeln.md#selbst-machen) |
| Claude einen echten Browser steuern lassen | Übung 2.4: einen MCP-Server anbinden (Playwright) | Node.js mit `npx` | [S2.14](s2-14-mcp-stecker.md#selbst-machen) |
| Antworten aus deinen geprüften Quellen statt geratener | Übung 2.5: deine eigene Wissensbasis in NotebookLM | Zugang zu NotebookLM und Quellen, die auf Google-Server dürfen | [S2.18](s2-18-rag-und-notebooklm.md#selbst-machen) |
| Lange Testausgaben aus Claudes Kontext heraushalten (Bonus, etwa 20 Min.) | Bonus-Übung 2.6: Token Firewall | `jq` | [S2.10](s2-10-hook-ausgaben.md#selbst-machen) |

### Was du danach hast

Hast du alle Übungen von Session 2 gemacht, hast du:

1. **einen Skill**, der dein häufigstes wiederkehrendes Anweisungsmuster automatisiert
2. **einen Safety-Hook**, der ab jetzt jede Claude-Code-Sitzung automatisch mitbewacht, nach bestem Bemühen ([S2.8](s2-08-hook-einrichten.md))
3. **ein Verständnis für den Aufbau von Plugins** und dein eigenes, aufgesetztes Mini-Plugin
4. **eine funktionierende MCP-Verbindung** zu einem echten Browser und einen Plan für die Automatisierung
5. **eine persönliche Wissensbasis**, mit der Claude in deinem Fachgebiet aus deinen Quellen antwortet
6. **(Bonus) eine Token Firewall**, die bei lauten Befehlsausgaben Kontext und Geld spart

Das sind keine Spielzeuge, sondern Infrastruktur. Jeder Baustein wirkt über die Übung hinaus. Das Bild zeigt, wie die Schichten übereinanderliegen:

```
┌─────────────────────────────────────────────────────┐
│                   Your Workflow                      │
├─────────────────────────────────────────────────────┤
│  Commands (/tdd, /commit)  →  Skills (SKILL.md)     │ ← Module 2.1
├─────────────────────────────────────────────────────┤
│  Hooks (PreToolUse, PostToolUse, Stop)               │ ← Module 2.2
├─────────────────────────────────────────────────────┤
│  Plugins (bundle of skills + commands + agents)      │ ← Module 2.3
├─────────────────────────────────────────────────────┤
│  MCP (Playwright, Slack, DBs, custom services)       │ ← Module 2.4
├─────────────────────────────────────────────────────┤
│  RAG / NotebookLM (your knowledge base)              │ ← Module 2.5
└─────────────────────────────────────────────────────┘
```

Jede Schicht erweitert, was Claude Code erreicht: Skills und Commands automatisieren deinen eigenen Ablauf, Hooks setzen Regeln automatisch und still durch, Plugins verteilen gemeinsame Fähigkeiten im Team, MCP verbindet externe Systeme, und RAG verankert Claude in deinem Fachwissen. Die Modulnummern rechts stammen aus dem alten Kursaufbau: 2.1 ist heute das Regal Skills & Commands (S2.1–S2.5), 2.2 Hooks (S2.6–S2.10), 2.3 Plugins (S2.11–S2.13), 2.4 MCP (S2.14–S2.17) und 2.5 RAG und NotebookLM (S2.18–S2.19). Ein Plugin kann neben Skills, Commands und Agents auch Hooks und MCP-Server mitbringen ([S2.11](s2-11-plugins-buendeln.md)).

Wer aus der Sicherheitstechnik kommt, denkt schon in Systemen: Sensoren, Abläufe, Rollen im Team, integrierte Plattformen. Das ist genau das Denkmodell, das du für ein gutes Claude-Code-Setup brauchst. Der Unterschied ist nur: Die Anlage, die du schützt und verbesserst, ist dein Entwicklungsablauf.

Weiter geht es in Session 3 mit Agenten und Multi-Agent-Systemen, ab [S3.1](s3-01-was-ist-ein-agent.md).

### Extra-Übungen (freiwillig)

Freiwillige Vertiefungen aus der Sammlung der wilden Formate. Setz sie neben die passende Kernübung. ⚠️ Alle Hook-Übungen hier nutzen eine **projekt-lokale** `.claude/settings.json`, nie deine globale Konfiguration.

| Extra | Art und Dauer | Vertieft | Steht in |
|---|---|---|---|
| Hook-Honeypot | etwa 25 Min., schwer | Hooks (Übung 2.2) | [S2.8](s2-08-hook-einrichten.md#selbst-machen) |
| OSDP Cop: Frame-Forensik gegen die echte Spezifikation | etwa 25 Min., mittel | RAG und NotebookLM (Übung 2.5) | [S2.18](s2-18-rag-und-notebooklm.md#selbst-machen) |
| Panel-Migrations-Diff | etwa 25 Min., mittel | Skills (Übung 2.1) | [S2.2](s2-02-skill-schreiben.md#selbst-machen) |
| Saboteur on Shift: Hook-Diagnose unter Zeitdruck | zu zweit, etwa 20 Min., wild | Hooks und die Diagnose-Schleife aus Session 4 | [S4.10](s4-10-diagnose-schritt-fuer-schritt.md) |

## Check

Du kannst eine Übung aus Session 2 passend zu deinem Ziel wählen, sie bis zu ihrer Liste „Geschafft, wenn" durcharbeiten und begründen, welche Schicht du damit gebaut hast und wofür du sie einsetzt.

1. Welche Übung gehört zu welcher Schicht: Skill, Hook, Plugin, MCP, Wissensbasis?
2. Warum gehören Hook-Experimente wie der Honeypot in eine projekt-lokale `.claude/settings.json`?
3. Was macht eine Übung länger als ihre Kernschritte, und was lässt du weg, wenn die Zeit knapp ist?

## Weiterlesen

- [S2.1 · Skills sind Dienstanweisungen, Commands sind Knöpfe](s2-01-skills-und-commands.md)
- [S2.6 · Hooks als Sensoren: die drei Eckpfeiler](s2-06-hooks-als-sensoren.md)
- [S2.11 · Plugins: ein Bündel schnüren](s2-11-plugins-buendeln.md)
- [S2.14 · MCP: der Integrationsstecker](s2-14-mcp-stecker.md)
- [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](s2-18-rag-und-notebooklm.md)
- [S1.20 · Praxis-Station Session 1: eine Übung wählen](s1-20-praxis-station-1.md)
- [S3.15 · Praxis-Station Session 3: eine Übung wählen](s3-15-praxis-station-3.md)
