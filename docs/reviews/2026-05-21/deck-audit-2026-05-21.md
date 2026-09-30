# Deck Audit 2026-05-21

## Befund vor der Aktualisierung

- `claude-code-workshop.pptx` hatte 18 Slides.
- Das Deck deckte faktisch Block 1 und Block 2 ab.
- Der Slide-Index in `resources/trainer-notes.md` erwartete 112 Slides und war als unverifiziert markiert.
- Die nach dem 17-Module-Refresh wichtigen Inhalte fehlten visuell: Module 1.5, 3.1-3.7, Website/Repo-Narrativ und Dry-Run-Check.

## Umgesetzte Deck-Aenderung

- Deck auf 30 Slides erweitert.
- Alter Abschluss-Slide bleibt erhalten und wurde ans Ende der Praesentationsreihenfolge gestellt.
- Neue visuelle Einstiegsslides:
  - Module 1.5: Cost Engineering
  - Block 3 Intro: Advanced Workflow
  - Module 3.1: Agents & Multi-Agent
  - Module 3.2: Multi-Model Pipelines
  - Module 3.3: Security & Adversarial Testing
  - Module 3.4: Automation & Scheduled Work
  - Module 3.6: CI/CD & Headless Mode
  - Module 3.7: Troubleshooting & Debugging
  - Module 3.5: Capstone Workflow Architecture
  - Session 3 Run Sheet
  - Website + Repo
  - Dry Run Checklist
- Folienzaehler auf `30` aktualisiert.
- `resources/trainer-notes.md` auf den echten Slide-Index synchronisiert.

## Aktueller Slide-Plan

| Slides | Fokus | Trainer-Hinweis |
|---:|---|---|
| 1-2 | Intro und Agenda | Kurz halten, dann direkt in Block 1 starten. |
| 3-11 | Block 1 Foundations | Slide 11 setzt den neuen Cost-Engineering-Anker. |
| 12-18 | Block 2 Ecosystem | Bestehende Slides bleiben als kompaktes Systembild. |
| 19-29 | Block 3 Advanced | Neue Slides als visuelle Fuehrung fuer Session 3. |
| 30 | Outro | Einstiegspunkte und naechste Schritte. |

## Dry-Run-Plan

1. Session 2 mit Slides 12-18 plus Demos 2.1, 2.2 und 2.4 einmal komplett durchgehen.
2. Session 3 mit Slides 19-29 trocken laufen lassen und je Modul entscheiden: Live-Demo, Whiteboard oder Discussion.
3. Slide 24 CI/CD nur live zeigen, wenn Token, Budget-Cap und JSON-Output vorher funktionieren.
4. Slide 25 Troubleshooting als geplanten Fallback nutzen: wenn ein Hook, Skill oder MCP-Demo bricht, wird daraus die Debugging-Demo.
5. Slide 26 Capstone erst starten, wenn die Teilnehmer vorher ein eigenes Physical-Security-Szenario nennen.

## Noch offen

- Das Deck wurde strukturell als PPTX validiert und per PowerPoint-PNG-Export visuell geprueft.
- Kontaktbogen und Einzelpruefung der neuen Slides zeigten keine Blank-Slides, keine falsche Reihenfolge und keine sichtbaren Textueberlaeufe.
- Die vorhandenen alten Slides nutzen weiterhin ihre urspruengliche Gestaltung und Sprache; die neuen Slides sind bewusst kompakter und dienen als fehlende visuelle Bruecke.
- Falls das Deck als eigenstaendige Teilnehmerunterlage dienen soll, waere ein spaeterer Layout-Pass sinnvoll.
