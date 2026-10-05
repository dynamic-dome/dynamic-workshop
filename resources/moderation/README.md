# Moderation

Dieser Ordner ist für dich, wenn du den Claude-Code-Workshop live moderierst: vier Sessions mit einer kleinen Gruppe,
gedacht für drei erfahrene Entwicklerinnen und Entwickler im Raum. Wer allein lernt, braucht ihn nicht; der Einstieg
dafür ist die [Bibliothek](../library/README.md) mit der [Einstufung](../library/einstufung.md).

## Was wo liegt

| Datei | Inhalt |
|---|---|
| [handbuch.md](handbuch.md) | Das Moderations-Handbuch: Format und Rhythmus der vier Sessions mit Begründung, Zeiten und Pausen, Live-Anker, Drei-Personen-Format, Recall und Quick-Checks, Transfer-Beats, Selbstwirksamkeits-Check, Pre-Flight, Go/No-Go, Fehlerbilder, Notfallplan, Einladung |
| [vorbereitung.md](vorbereitung.md) | Zeitplan und Checklisten vor den Sessions; Workshop-Plugins, Hook-Datei, NotebookLM, Playwright, Codex |
| [videos.md](videos.md) | Transkript der drei Intro-Videos, Stand der Aufnahme (drei Sessions) |
| [Live-Pfad](../paths/live-workshop.md) | Die Kapitel je Session mit Stufe und Minuten, aus den Kapiteln generiert |
| [Kapitel](../library/README.md) | Inhalt und Übung je Lerneinheit, geschrieben für Selbstlernende |
| [Vorführen](vorfuehren/) | Je Kapitel eine Datei mit Demo, Sprechpunkten, Dauer und Recovery-Notes; der Live-Pfad verlinkt sie |

Das Deck liegt unter `resources/media/claude-code-praxisbibliothek.pptx`, die Intro-Videos und der Podcast ebenfalls
in `resources/media/`.

## Reihenfolge der Vorbereitung

1. **Handbuch lesen**, zuerst Format, Stufen und Rhythmus, dann das Live-Format mit drei Rollen. So weißt du, was
   Pflicht ist und was du wann straffen darfst.
2. **Einladung verschicken**, eine Woche vor Session 1 ([Vorlage](handbuch.md#einladung-vorlage)), und die
   Setup-Termine mit den Teilnehmenden vereinbaren.
3. **Eigene Maschine vorbereiten** nach [vorbereitung.md](vorbereitung.md): Plugins, Hook-Datei, NotebookLM-Notebook,
   Playwright-Cache, gegebenenfalls Codex. Danach alle Demos einmal komplett durchspielen.
4. **Vor jeder Session** den Abschnitt der Session im [Live-Pfad](../paths/live-workshop.md) öffnen, zu jedem Kapitel
   die Datei unter [Vorführen](vorfuehren/) lesen und die Checkliste „Vor Session N" in [vorbereitung.md](vorbereitung.md#zeitplan)
   abarbeiten.
5. **Am Workshop-Tag** den [Pre-Flight](handbuch.md#pre-flight-am-workshop-tag) laufen lassen, in Session 3 und 4
   zusätzlich die [Go/No-Go-Matrix](handbuch.md#gono-go-je-demo).
6. **Während der Session** helfen dir das Handbuch (Rhythmus, Recall, Fehlerbilder, Notfallplan) und im
   Workshop-Plugin `/dynamic-workshop:workshop guide S1` bis `guide S4` oder `guide <ID>` für ein einzelnes Kapitel.
