---
id: S3.15
type: practice
title: "Praxis-Station Session 3: eine Übung wählen"
shelf: practice
level: core
minutes: 15
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann eine Übung aus Session 3 (mehrere Agenten, Security-Audit oder Domänen-Parser) passend zu meinem Projekt auswählen, sie selbstständig durchführen und an ihrer Liste „Geschafft, wenn“ belegen, dass sie gelungen ist."
sources: []
aliases: []
offers: [S3.4, S3.6]
---

# S3.15 · Praxis-Station Session 3: eine Übung wählen

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~15 Min** · **Voraussetzungen:** keine
>
> ← [S3.14 Self-Improve-Loop: was geht und wo es endet](s3-14-self-improve-loop.md) · [Bibliothek](README.md) · [X.3 Der minimale Agent: Pi als Spiegel](x-03-pi-als-spiegel.md) →
<!-- meta:end -->

## Auf einen Blick

Hier wählst du eine Übung aus Session 3: eine erste Aufgabe mit mehreren Agenten, ein Security-Audit am Playground oder einen Domänen-Parser mit TDD. In die 15 Minuten der Station passt die Aufgabe mit mehreren Agenten; Audit und Parser brauchen 25–30 Minuten. Die Prioritätenliste unten zeigt, welche Übungen der fortgeschrittenen Sessions zuerst kommen und in welchem Kapitel sie heute stehen.

## Selbst machen

### Welche Übung passt zu dir?

| Dein Ziel | Übung | Zeit | Kapitel |
|---|---|---|---|
| Erleben, was mehrere Agenten gegenüber einer einzelnen Claude-Instanz ändern | Übung 3.1: deine erste Aufgabe mit mehreren Agenten | etwa 15 Min. | [S3.4](s3-04-orchestrierungsmuster.md#selbst-machen) |
| An echtem Code sehen, was adversariales Sicherheitstesten findet | Übung 3.3: Security-Audit am Playground | 25–30 Min. | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| Aus der Zutrittskontrolle kommen und einen grenzgeprüften Parser selbst bauen | Übung 3.9: einen Domänen-Parser richtig bauen (OSDP oder Wiegand, TDD) | 25–30 Min. | [S3.6](s3-06-devils-advocate.md#selbst-machen) |

Für das Security-Audit nutzt du das Workshop-Plugin `devil-advocate-swarms`; fehlt es, beschreibt S3.6 den Weg ohne Plugin. Statt des Audits kannst du auch Übung 3.4 nehmen, Automation einrichten (etwa 20 Minuten), in [S3.12](s3-12-zeitgesteuert-arbeiten.md).

### Prioritäten der fortgeschrittenen Übungen

Die Übungen des alten Blocks 3 verteilen sich heute auf Session 3 und Session 4. Die Liste sagt dir, was zuerst kommt:

| Priorität | Übung | Realistische Zeit | Kapitel |
|---|---|---|---|
| **1 · zuerst** | 3.1 Deine erste Aufgabe mit mehreren Agenten | etwa 15 Min. | [S3.4](s3-04-orchestrierungsmuster.md#selbst-machen) |
| **1 · zuerst** | 3.5 Abschlussprojekt mit Architektur-Diskussion | etwa 45 Min. | [S4.8](s4-08-abschlussprojekt.md), Session 4 |
| 2 · empfohlen | 3.3 Security-Audit **oder** 3.4 Automation einrichten | 25–30 Min. / etwa 20 Min. | [S3.6](s3-06-devils-advocate.md#selbst-machen) / [S3.12](s3-12-zeitgesteuert-arbeiten.md) |
| 2 · empfohlen | 3.6 Einen Pre-Commit-Hook mit Claude bauen | etwa 25 Min. | [S4.5](s4-05-ci-pipelines.md), Session 4 |
| 2 · empfohlen | 3.7 Einen kaputten Hook debuggen | etwa 20 Min. | [S4.10](s4-10-diagnose-schritt-fuer-schritt.md), Session 4 |
| 2 · empfohlen | 3.9 Einen Domänen-Parser bauen (OSDP/Wiegand, TDD) | 25–30 Min. | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| 3 · wenn Zeit bleibt | 3.2 Codex-Schwarm (nur als Demo) | etwa 15 Min. | [S4.2](s4-02-codex-schwarm.md#selbst-machen), Session 4 |
| 3 · wenn Zeit bleibt | Bonus 3.8 HIPAA-Hook | etwa 20 Min. | [S3.11](s3-11-datenschutz-und-compliance.md) |

Realistisch brauchst du für den Kernpfad zusammen 110–145 Minuten. Nimm die Übungen mit Priorität 1 zuerst. Für Entwicklerinnen und Entwickler von Zutrittskontrolle ist 3.9 die stärkste Wahl: Kommt die Gruppe vor allem aus diesem Fach, nimm 3.9 statt 3.6 oder 3.7.

### Extra-Übungen (freiwillig)

Wettkampf-, Fach- und Team-Formate aus der Sammlung der wilden Formate, gut für Energie nach einem dichten Kapitel. ⚠️ Es gilt dieselbe Regel wie beim Security-Audit (Übung 3.3): Die Schwachstellen im Playground sind Lehrziele, **committe keine Fixes**.

| Extra | Art und Dauer | Passt zu | Steht in |
|---|---|---|---|
| Capture-the-Vulnerability-CTF | etwa 20 Min., wild | rund um das Security-Audit (Übung 3.3) | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| Devil's-Advocate-Duell | etwa 15 Min., wild | vertieft die Debatte aus dem Audit | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| Audit-Trail-Integrität (EN 50131) | etwa 20 Min., mittel | vertieft die Log-Fälschung aus dem Audit | [S3.6](s3-06-devils-advocate.md#selbst-machen) |
| Alarmsturm-Korrelator | etwa 25 Min., mittel | Fach-Variante von Übung 3.1 | [S3.4](s3-04-orchestrierungsmuster.md#selbst-machen) |
| Stille Post mit Agenten | etwa 15 Min., wild | verspielte Variante zu Übung 3.1: Kontext-Isolation | [S3.1](s3-01-was-ist-ein-agent.md#selbst-machen) |
| Wrong-Door Heist, ein Rechte-Red-Team | etwa 25 Min., wild | Security-Audit und Rechte-Modi | [S3.8](s3-08-rechte-fuer-autonomie.md#selbst-machen) |

## Check

Du kannst eine Übung aus Session 3 passend zu deinem Projekt wählen, sie bis zu ihrer Liste „Geschafft, wenn" durcharbeiten und erklären, warum die Teile einer Fan-out-Aufgabe wirklich unabhängig voneinander sein müssen.

1. Welche Übungen der Prioritätenliste gehören zu Session 3, welche zu Session 4?
2. Woran erkennst du, dass eine Aufgabe Fan-out verträgt und keine Pipeline braucht?
3. Warum committest du keine Fixes an den Schwachstellen im Playground?

## Weiterlesen

- [S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](s3-04-orchestrierungsmuster.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md)
- [S3.12 · Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](s3-12-zeitgesteuert-arbeiten.md)
- [S4.8 · Abschlussprojekt mit Bewertung](s4-08-abschlussprojekt.md)
- [S1.20 · Praxis-Station Session 1: alles in einem Ablauf](s1-20-praxis-station-1.md)
- [S2.20 · Praxis-Station Session 2: alles in einem Ablauf](s2-20-praxis-station-2.md)
