# Selbstlernende zuerst — Entwurf

> Stand: 2026-10-05 · Branch `selbstlern-zuerst` (ab `e693038`) · Größe L (GZIF)
> Anlass: Durchsicht vom 2026-10-05, Befunde R1 bis R31 in `docs/reviews/2026-10-05-lernbogen-und-fakten.md`.
> Pakete und ihr Stand: `docs/plans/2026-10-05-selbstlern-zuerst-tickets.md`. Sammel-Todo: DCO #9632.

## Problem

Die Bibliothek nennt Selbstlernende als Hauptzielgruppe, die Kapitel sind aber noch der Live-Kurs: Demo und
Sprechpunkte stehen im Lernweg, gut die Hälfte der Lektionen hat keine Übung, die Abruffragen haben keine Auflösung,
kein Pfad hat einen Schluss, und Cockpit wie Tutor führen durch die Kurzfassung. Wer allein lernt, liest viel, tut
wenig und erfährt nicht, ob er es kann.

## Entscheidungen des Owners (2026-10-05)

| Frage | Entscheidung |
|---|---|
| Hauptfassung | Selbstlern-Fassung. Moderation und „Vorführen“ bilden eine eigene Schicht. |
| Form der Schicht | Eigene Dateien unter `resources/moderation/vorfuehren/`, je Kapitel eine. Kapitel enthalten kein „Vorführen“ mehr. Erst mechanisch verschieben, dann je Kapitel eine Übung daraus bauen. |
| Reihenfolge | Werkzeug vor Inhalt: Schicht, Cockpit/Tutor, Auflösungen, dann Inhalte; UI-Überarbeitung ganz am Schluss. |
| Pilot | Einstieg (S0.1 bis S1.9, 11 Kapitel), geschrieben von Claude Code (Fable) als Maßstab. |
| Menge | Sonnet-Schreiber je Regal-Paket nach Auftrag, Diff-Lektüre durch Fable, Codex-Gegenprüfung nur lesend je Paket. |
| Abschluss | Neues Kern-Kapitel S4.11 in jedem Pfad; S4.8 bleibt als große Fassung; die Praxis-Stationen werden Abschlüsse ihrer Session. |
| Fachgebiet | Bilder aus der Sicherheitstechnik bleiben; die Anrede „dein Fachgebiet ist Zutrittstechnik“ wird zum Beispiel. |

## Zielbild

- **Ein Kapitel ist für eine Person allein geschrieben.** Es enthält: Schnellcheck, Auf einen Blick, Bild im Kopf,
  Im Detail, Selbst machen, Typische Fallen, Check mit Auflösung, Weiterlesen. Kein „Vorführen“, keine
  Moderationsblöcke, keine Gruppenübung ohne Einzelfassung, kein Baustein, den man allein nicht beschaffen kann,
  ohne dass der Weg ohne ihn danebensteht.
- **Die Moderationsschicht** hält je Kapitel die Demo und die Hinweise für Moderierende. Der Live-Pfad und der
  Tutor-Modus `guide` lesen von dort. Wer moderiert, verliert nichts; wer allein lernt, sieht es nicht.
- **Jede Lektion endet in einer Handlung**, die ihr Outcome einübt, mit Startzustand, Schritten und „Geschafft, wenn“.
- **Jede Abruffrage hat eine Auflösung**, eingeklappt, aus dem Kapiteltext belegt.
- **Jeder Pfad hat einen Schluss:** ein kleiner Build, der Auftrag, Guardrail, Verifikation und Übergabe verbindet.
- **Cockpit und Tutor zeigen bei „durcharbeiten“ den Lehrtext und die Übung**, nicht nur die Kurzfassung.
- **Der Playground verrät nichts:** Die Lösungen liegen außerhalb des Ordners, in dem Claude arbeitet.

## Quellenhoheit (ändert Spec 2026-09-30, §7.1)

| Information | Einzige Quelle |
|---|---|
| Lehrinhalt, Übung, Quiz, Auflösung, Schnellcheck je Lerneinheit | Kapitel in `resources/library/` |
| Demo, Sprechpunkte, Dauer, Recovery je Lerneinheit | `resources/moderation/vorfuehren/<kapiteldatei>` |
| Ablauf, Zeiten, Live-Format | `resources/moderation/handbuch.md` (unverändert) |
| Lösungen des Playgrounds | eine Datei in `resources/reference/` |

Alles Übrige bleibt wie in der Spec vom 2026-09-30.

## Lern-Geschichten (woran die Pakete gemessen werden)

1. Als Neuling sehe ich nach der Installation innerhalb des ersten Kapitels eine Datei entstehen und laufen, und
   ich sehe die Freigabe-Abfrage, von der das Kapitel spricht.
2. Als Alleinlernende finde ich in jedem Kapitel nur Text, der mich meint.
3. Nach jeder Abruffrage kann ich meine Antwort mit einer Auflösung vergleichen.
4. Wenn die Einstufung „durcharbeiten“ sagt, zeigt mir das Cockpit Lehrtext und Übung, ohne dass ich sie suchen muss.
5. In jeder Kern-Lektion tue ich mindestens einmal selbst etwas und weiß danach, ob es geklappt hat.
6. Am Ende meines Pfads baue ich etwas Kleines, das mehrere Kapitel verbindet, und bewerte es selbst.
7. Wenn ich Claude im Playground nach Schwachstellen suchen lasse, findet es sie durch Lesen des Codes, nicht durch
   eine mitgelieferte Liste.
8. Als Moderierende finde ich zu jedem Kapitel Demo und Sprechpunkte an einem Ort, und der Tutor führt mich hin.

## Umsetzungs- und Prüfentscheidungen

- **Verschieben per Skript, nicht von Hand.** Beleg, dass nichts verloren geht: jede Zeile jedes alten
  „Vorführen“-Abschnitts steht in genau einer Datei der Moderationsschicht; der Snippet-Ledger bleibt grün.
- **Prüfnähte** (hier setzen Tests an, nirgends sonst): das Ergebnis des Validators für ein Kapitel; der erzeugte
  Katalog; das gebaute Cockpit im Browser; Exit-Codes der Hook-Vorlagen; die Ausgabe der Einstufungs-Engine für
  die Personas.
- **Der Validator setzt das Zielbild durch**, sobald ein Paket es herstellt: kein „Vorführen“ im Kapitel; Anzahl
  der Auflösungen gleich Anzahl der Abruffragen; Kern-Lektion ohne „Selbst machen“ ist ein Befund.
- **Fakten nur mit Beleg** aus der offiziellen Doku, Zitat im Commit (Projektregel). Der Doku-Stand vom 2026-10-05
  liegt in `~/AI/analysis-artifacts/workshop-review-2026-10-05/docs-cache/`.
- **Einstufungsvertrag:** Jede Änderung an Reihenfolge, Stufe oder Kapitelbestand schreibt Vertragskatalog,
  Personas und Golden bewusst neu (HOW-TO-USE §3). Betrifft die Pakete 5 und 6.
- **Inhaltsarbeit in Menge:** Auftrag je Regal-Paket nach dem Maßstab des Pilotregals; der Schreiber ändert nur
  seine Kapitel; danach Diff-Lektüre und eine lesende Codex-Gegenprüfung. Kein Paket gilt ohne beide als fertig.
- **Übungen** sind allein lösbar, kosten nichts extra, dauern fünf bis zehn Minuten in Kern-Lektionen, haben
  Startzustand, Schritte und „Geschafft, wenn“, und laufen unter Windows (Git Bash und PowerShell), macOS und Linux.
- **Branch:** Alles auf `selbstlern-zuerst`, ein Commit je abgeschlossenem Schritt. Merge nach `main` und Push nur
  auf Zuruf des Owners.

## Nicht Teil dieses Umbaus

- Neue Themen oder weitere Kapitel außer S4.11.
- Das Deck, die Videos und der Website-Export.
- Ein Eval-Modul oder andere Versprechen aus Phase 3 der alten Planung.
- Die UI-Überarbeitung über das hinaus, was Paket 2 braucht; sie ist das letzte Paket und bekommt dann eine eigene
  Fragerunde.
