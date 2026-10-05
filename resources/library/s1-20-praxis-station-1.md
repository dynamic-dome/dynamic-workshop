---
id: S1.20
type: practice
title: "Praxis-Station Session 1: eine Übung wählen"
shelf: practice
level: core
minutes: 15
requires: []
safety_floor: false
transferable: false
outcome: "Ich kann aus den Übungen von Session 1 die passende für meine Lücke auswählen, sie allein durchführen und an ihrer Liste Geschafft, wenn prüfen, ob sie gelungen ist."
sources: []
aliases: []
offers: [S1.1, S1.10, S1.13, S1.16, S1.18]
---

# S1.20 · Praxis-Station Session 1: eine Übung wählen

<!-- meta:start -->
> **Regal:** [Praxis-Stationen](README.md#practice) · **Stufe:** Kern · **~15 Min** · **Voraussetzungen:** keine
>
> ← [S1.19 Kosten im Blick: /cost, /usage und Budgetgrenzen](s1-19-kosten-im-blick.md) · [Bibliothek](README.md) · [X.2 Mit Claude Code lernen](x-02-lernen-mit-claude-code.md) →
<!-- meta:end -->

## Auf einen Blick

Diese Station hilft dir, aus den Übungen von Session 1 die eine zu wählen, die deine größte Lücke schließt: die Grundschleife, CLAUDE.md, präzise Aufträge oder Git. Im Workshop hast du dafür 15 Minuten, das reicht für eine Übung. Die Übungen selbst stehen in ihren Kapiteln; hier findest du die Auswahl, Fragen für die Nachbesprechung und kurze Extras zum Aufwärmen.

## Selbst machen

### So sind die Übungen gebaut

Jede Übung hat:

- ein **Ziel**: was du übst
- **Schritte**: nummeriert, du gehst sie der Reihe nach durch
- eine Liste **„Geschafft, wenn"**: daran erkennst du, dass du fertig bist
- **Tipps** für den Fall, dass du hängst (bei der Übung oder unter „Typische Fallen" im Kapitel)

Die Übungen sind kurz und praktisch. Du baust kein Produktivsystem, du trainierst Handgriffe, bis sie sitzen. Du arbeitest allein oder zu zweit; im Workshop ist die Moderation für Fragen da. Die Übungen richten sich an erfahrene Entwicklerinnen und Entwickler und nutzen durchgehend Bilder aus der Sicherheitstechnik.

> **Unter Windows?** Die Shell-Schnipsel in den Übungen nutzen POSIX-Syntax (`mkdir -p`, `&&`, `~/`, `chmod`). Am einfachsten führst du sie in **Git Bash** aus, dort laufen sie wie geschrieben. Arbeitest du lieber in **PowerShell**, nimm die PowerShell-Form, die beim ersten Befehl daneben steht, und denk an diese Übersetzung: `New-Item -ItemType Directory -Force -Path ...` statt `mkdir -p`, `;` statt `&&`, `$HOME` statt `~`, kein `chmod`. Claude Code legt Ordner oft selbst an; stolpern wirst du vor allem beim allerersten Kopieren aus einer Übung.

### Welche Übung passt zu dir?

| Deine Lücke | Übung | Zeit | Kapitel |
|---|---|---|---|
| Du willst die Grundschleife sicher können: beschreiben, umsetzen, ausführen, erweitern, erklären | Übung 1.1: dein erstes kleines Werkzeug, ohne selbst Code zu schreiben | 12–15 Min. | [S1.1](s1-01-erster-kontakt.md#selbst-machen) |
| Claude soll die Regeln deines Projekts auch nach einem Neustart der Sitzung kennen | Übung 1.2: deinen Kontext einrichten, mit einer CLAUDE.md für deinen echten Arbeitsbereich; den persönlichen Memory-Eintrag dazu findest du in [S1.11](s1-11-gedaechtnis-ebenen.md#selbst-machen) | etwa 22 Min. | [S1.10](s1-10-claude-md.md#selbst-machen) |
| Du willst selbst spüren, was ein präziser Auftrag gegenüber einem vagen bringt | Übung 1.3: die Prompting-Challenge, dieselbe Aufgabe in zwei Runden | etwa 15 Min. | [S1.13](s1-13-vager-und-praeziser-auftrag.md#selbst-machen) |
| Du willst Branch, Umsetzung, Commit und Log nur über das Gespräch erledigen | Übung 1.4: der Git-Ablauf mit Claude Code, ohne Git-Befehle von Hand | 18–20 Min. | [S1.16](s1-16-git-in-einem-fluss.md#selbst-machen) |
| Du hast Übung 1.4 geschafft und willst gefahrlos parallel ausprobieren | Bonus zu Übung 1.4: einen Experiment-Worktree anlegen | – | [S1.18](s1-18-worktrees.md#selbst-machen) |

In die 15 Minuten der Station passen Übung 1.1 und Übung 1.3. Übung 1.2 und 1.4 brauchen länger; plane dafür mehr Zeit ein oder nimm sie dir nach der Session vor. Die Kosten-Übung 1.5 ist freiwillig und steht in [S1.19](s1-19-kosten-im-blick.md#selbst-machen).

### Wenn Claude danebenliegt

Liefert Claude etwas Falsches, korrigiere gezielt: Nenn das konkrete Problem und sag, dass nur das behoben werden soll.

<!-- cockpit:example -->
```
That's not quite right. The issue is [specific problem]. Fix only that — don't change anything else.
```

### Nachbesprechung

Diese Fragen passen nach den Übungen zur Diskussion in der Gruppe oder zum Nachdenken für dich allein.

**Claude Code als Werkzeug**

1. Was hat dich daran überrascht, wie Claude Code arbeitet, verglichen mit deiner Erwartung?
2. Wo hattest du am meisten das Gefühl, die Kontrolle zu haben, und wo am wenigsten?
3. Was müsstest du an deiner jetzigen Arbeitsweise ändern, um Claude Code sinnvoll einzubinden?

**Aufträge formulieren**

1. Welche Informationen hast du routinemäßig im Kopf, die du im Auftrag ausdrücklich nennen müsstest?
2. Welche Aufgaben aus deinem Fachgebiet profitieren am meisten von Aufträgen im Stil eines Arbeitsauftrags?
3. Wann ist es richtig, weniger genau zu sein und Claude entscheiden zu lassen?

**Kontext und Gedächtnis**

1. Welche Konventionen oder Vorgaben deines aktuellen Projekts würdest du heute in die CLAUDE.md schreiben?
2. Welche persönlichen Vorlieben würdest du als Memory ablegen?
3. Wie gehst du mit einem Projekt um, in dem mehrere Leute im Team Claude Code nutzen: Wie stimmt ihr die Konventionen in der CLAUDE.md ab?

**Git**

1. Welchen Teil des Git-Ablaufs findest du über Claude Code am wertvollsten?
2. Wann würdest du Git-Befehle weiterhin lieber selbst eingeben?
3. Wie verändert das Worktree-Modell deinen Blick auf parallele Entwicklungsarbeit?

### Extras zum Aufwärmen (freiwillig)

Kurze, schnelle Übungen ohne Druck aus der Sammlung der wilden Formate. Setz ein Mikro-Aufwärmen vor oder hinter die passende Kernübung; die Formate zu zweit oder in der Gruppe sind für Energie oder für fortgeschrittene Gruppen. Nichts davon ist Hausaufgabe.

| Extra | Art und Dauer | Einsatz | Steht in |
|---|---|---|---|
| Nur reden (W1) | Mikro-Aufwärmen, 60–90 Sek., leicht | vor dem Einstieg | [S1.1](s1-01-erster-kontakt.md#selbst-machen) |
| Tab-Complete-Bingo | Mikro-Aufwärmen in der Gruppe, etwa 5 Min., leicht | vor dem Einstieg | [S1.1](s1-01-erster-kontakt.md#selbst-machen) |
| Der Rückgängig-Reflex (W2) | Mikro-Aufwärmen, 2–3 Min., leicht | nach dem Einstieg, bevor echte Arbeit beginnt | [S1.5](s1-05-rechte-im-alltag.md#selbst-machen) |
| Das Orakel-Spiel | Mikro-Aufwärmen, etwa 3 Min., leicht | zwischen Einstieg und „Aufträge formulieren" | [S1.13](s1-13-vager-und-praeziser-auftrag.md#selbst-machen) |
| Die Kontext-Streichliste | Mikro-Aufwärmen, etwa 4 Min., leicht | nach „Kontext & Gedächtnis" | [S1.8](s1-08-kontextfenster.md#selbst-machen) |
| One-Word Diff (W4) | Mikro-Aufwärmen, 2 Min., leicht | vor Übung 1.4 (Git) | [S1.16](s1-16-git-in-einem-fluss.md#selbst-machen) |
| Blind Vault: Spezifikation diktieren | zu zweit, etwa 20 Min., schwer | vertieft „Aufträge formulieren" | [S1.13](s1-13-vager-und-praeziser-auftrag.md#selbst-machen) |

## Check

Du kannst für deine größte Lücke aus Session 1 die passende Übung wählen, sie allein bis zu ihrer Liste „Geschafft, wenn" durcharbeiten und in einem Satz sagen, welche Fähigkeit sie trainiert hat.

1. Welche Übung trainiert die Grundschleife, welche den Kontext über einen Neustart hinweg, welche präzise Aufträge und welche den Git-Ablauf?
2. Welche Übungen passen in die 15 Minuten der Station, und welche planst du für später ein?
3. Wie formulierst du eine Korrektur, wenn Claude in einer Übung danebenliegt?

## Weiterlesen

- [S1.1 · Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md)
- [S1.10 · CLAUDE.md: die Hausordnung des Projekts](s1-10-claude-md.md)
- [S1.13 · Vager und präziser Auftrag im Vergleich](s1-13-vager-und-praeziser-auftrag.md)
- [S1.16 · Git in einem Fluss: Branch, Commit, PR](s1-16-git-in-einem-fluss.md)
- [S1.18 · Worktrees als Testlabor](s1-18-worktrees.md)
- [S2.20 · Praxis-Station Session 2: eine Übung wählen](s2-20-praxis-station-2.md)
