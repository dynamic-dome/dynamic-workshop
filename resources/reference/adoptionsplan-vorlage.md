# Vorlage: Adoptionsplan auf einer Seite

Wofür: den ersten echten Schritt mit Claude Code in deinem eigenen Repository planen. Fülle die Vorlage in den letzten
zehn Minuten des Kurses aus (am besten direkt nach [S4.8](../library/s4-08-abschlussprojekt.md)) und leg sie zu deinen Unterlagen.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/routines

## 1. Ziel-Repository

- Repository / System:
- Geschäftlicher Kontext:
- Sensibilität der Daten:
- Geschützte Pfade:

## 2. Erster nützlicher Ablauf mit Claude Code

- Aufgabe:
- Warum sie zählt:
- Baustein (CLI / Skill / Hook / Plugin / MCP / CI / Routine):
- Punkt, an dem ein Mensch freigibt:

## 3. Die ersten 7 Tage

- Tag 1:
- Tag 3:
- Tag 7:
- Enger Prüfschritt, der zeigt, dass es funktioniert:
- Weg zurück, falls nicht:

## 4. Nachfrage nach 30 Tagen

Lege mit den Werkzeugen zur Zeitsteuerung aus [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md) eine Nachfrage an:

```text
/schedule 30 days from now "Review the adoption plan for <repo>: what shipped, what blocked, what guardrail is missing?"
```

Für wiederkehrende Adoptions-Runden nimm lieber eine Routine als einen einmaligen Termin:

```text
Routine: monthly-claude-code-adoption-review
Cadence: monthly for 3 months
Scope: adoption plan, merged PRs, open risks, next guardrail
Budget cap: set explicitly before unattended runs
Worktree: dedicated review branch if files will be written
```

`/schedule` legt Routinen an. Sie laufen in der Cloud, nicht auf deinem Rechner, und sind eine Research Preview.
Lege Budget und Worktree fest, bevor der erste Lauf unbeaufsichtigt startet ([S3.13](../library/s3-13-autonome-loops-absichern.md)).

## 5. Erfolgssignal

Ein Satz:

> In 30 Tagen funktioniert Claude Code bei uns, wenn …

## Mehr dazu

- [S4.8 · Abschlussprojekt mit Bewertung](../library/s4-08-abschlussprojekt.md) · [S3.12 · Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](../library/s3-12-zeitgesteuert-arbeiten.md) · [S3.13 · Autonome Loops absichern: Budget und Worktree](../library/s3-13-autonome-loops-absichern.md)
- Doku: [Routinen](https://code.claude.com/docs/en/routines) · [Aufgaben in der Sitzung planen](https://code.claude.com/docs/en/scheduled-tasks)
