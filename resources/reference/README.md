# Referenz: Karten zum Nachschlagen

Wofür: schnell nachschlagen, ohne ein Kapitel zu öffnen. Jede Karte passt auf etwa eine Druckseite, bringt Muster,
Fallen und Entscheidungshilfen, verlinkt die offizielle Doku und trägt ein Prüfdatum. Gelehrt wird in den Kapiteln
([Regal-Übersicht](../library/README.md)); Modellgenerationen und Preise stehen nur im [Kanon](../_canonical.md).

## Karten

| Datei | Inhalt |
|---|---|
| [karte-start-und-flags.md](karte-start-und-flags.md) | Starten, Anmelden und Fortsetzen, der Print-Modus mit seinen Grenzen und die Slash-Befehle für jeden Tag. |
| [karte-rechte.md](karte-rechte.md) | Was jeder der sechs Rechte-Modi ohne Rückfrage erlaubt, womit eine Sitzung startet und wie allow-, ask- und deny-Regeln greifen. |
| [karte-hooks.md](karte-hooks.md) | Welches Ereignis wann feuert, was ein Exit-Code bewirkt, wo die Eingabe steht und warum ein Schutz-Hook still offen sein kann. |
| [karte-kontext.md](karte-kontext.md) | Was im Kontext steckt, wann du verdichtest, leerst oder neu anfängst und welche Anweisung in welche Datei gehört. |
| [karte-erweitern.md](karte-erweitern.md) | Wohin eine Erweiterung gehört, welches Skill-Feld was bewirkt, welcher Plugin- und MCP-Scope für wen gilt und wo MCP-Ausgaben enden. |
| [karte-agenten-worktrees.md](karte-agenten-worktrees.md) | Arbeit an Subagenten und Hintergrund-Sitzungen abgeben, das passende Muster wählen und Änderungen mit Worktrees trennen. |
| [karte-kosten.md](karte-kosten.md) | Modell und Effort nach Aufgabe wählen, Verbrauch lesen, Budget und Rundenlimit setzen. |
| [karte-fehlersuche.md](karte-fehlersuche.md) | Symptom, erste Frage und Abhilfe als Tabelle, dazu die Wahl zwischen `/debug`, `/doctor` und `--verbose`. |
| [karte-alte-namen.md](karte-alte-namen.md) | Alte Begriffe und ihre heutigen Namen, dazu der Reifegrad der Funktionen. |

## Nachschlagewerke und Vorlagen

| Datei | Inhalt |
|---|---|
| [glossar.md](glossar.md) | Die Begriffe der Bibliothek in je einem Satz, mit Kapitel-Verweis. |
| [analogien.md](analogien.md) | Alle Bilder aus der Sicherheitstechnik, je Kapitel eine Zeile; generiert aus „Bild im Kopf" der Kapitel. |
| [faq.md](faq.md) | Die wenigen Fragen, die mehrere Kapitel berühren und keines als Heimat haben. |
| [adoptionsplan-vorlage.md](adoptionsplan-vorlage.md) | Einseitige Vorlage für den ersten echten Schritt mit Claude Code im eigenen Team. |
| [kosten-nachbau.md](kosten-nachbau.md) | Geschätzte Kosten, wenn du alle Vorführungen und Pflichtübungen des Kurses selbst nachmachst. |
| [playground-loesungen.md](playground-loesungen.md) | Die eingebauten Schwachstellen des Playgrounds mit Ort und Erkennungsmerkmal. Erst nach den Übungen lesen. |

`analogien.md` erzeugt der Generator (`python tools/build_library.py build`); ändere sie nicht von Hand, sondern den
Abschnitt „Bild im Kopf" im jeweiligen Kapitel.
