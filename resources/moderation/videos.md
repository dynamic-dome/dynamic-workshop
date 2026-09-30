> **Transkript der aufgenommenen Videos, Stand der Aufnahme: drei Sessions — nicht an den heutigen Aufbau angepasst.**
>
> Der Text unten ist wörtlich übernommen. Heute läuft der Workshop in vier Sessions, der Ablauf steht im
> [Moderations-Handbuch](handbuch.md) und im [Live-Pfad](../paths/live-workshop.md). Die Mediendateien liegen künftig
> in `resources/media/`: die Folien der drei Videos (`video-1-was-ist-claude-code.pptx`,
> `video-2-security-analogie.pptx`, `video-3-grenzenlose-werkstatt.pptx`), `workshop-intro-video.mp4` und
> `workshop-intro-podcast.mp3`. Das Deck für den Workshop ist `resources/media/claude-code-praxisbibliothek.pptx`.

# Video Scripts — Workshop Intro

## Video 1: "Was ist Claude Code?" (2-3 Min)

### Ziel
Visueller Appetizer — zeigt in 2 Minuten, warum Claude Code kein normales IDE-Plugin ist.

### Storyboard

**[0:00-0:15] Hook**
- Bild: Dunkler Bildschirm, Terminal blinkt
- Text einblenden: "Was wäre, wenn euer Code sich selbst reviewen könnte?"
- Sprecher: "Stellt euch vor: Ihr tippt einen einzigen Satz — und euer Entwicklungswerkzeug versteht nicht nur WAS ihr wollt, sondern WARUM."

**[0:15-0:45] Das Problem**
- Bild: Split-Screen — links IDE mit vielen Plugins, rechts überfüllter Desktop
- Sprecher: "Wir alle kennen das: 20 Tools, 5 Terminals, ständig Copy-Paste zwischen Systemen. Jedes Tool kann nur eines. Nichts spricht miteinander."
- Visual: Tools als isolierte Inseln dargestellt

**[0:45-1:30] Die Lösung — Claude Code**
- Bild: Terminal öffnet sich, claude-Befehl wird getippt
- Sprecher: "Claude Code ist anders. Es ist kein Plugin — es ist ein Betriebssystem für eure Entwicklung."
- Animation: Bausteine fliegen zusammen
  - Skills (Berechtigungsprofile)
  - Hooks (Alarmsensoren)
  - MCP (der Datenbus)
  - Agents (Wachpersonal)
- Sprecher: "Und das Beste: Diese Bausteine lassen sich frei kombinieren. Nicht additiv — multiplikativ. Jedes neue Tool potenziert alle anderen."

**[1:30-2:15] Live-Moment**
- Screen Recording: Echte Claude Code Session
- Sprecher: "Seht selbst: Ein Satz — und Claude analysiert den Code, findet den Bug, schreibt den Fix, erstellt Tests, committed und erstellt das Ticket. Automatisch. Zuverlässig."
- Visual: Fortschrittsbalken der einzelnen Schritte

**[2:15-2:30] Call to Action**
- Text: "Claude Code Workshop — Von den Grundlagen bis Multi-Agent-Systeme"
- Sprecher: "In drei Sessions zeigen wir euch, wie ihr das alles selbst aufbaut."

---

## Video 2: "Die Security-Analogie" (2-3 Min)

### Ziel
Brücke schlagen zwischen Physical Security und Claude Code — zeigt: Ihr kennt diese Konzepte bereits.

### Storyboard

**[0:00-0:20] Hook**
- Bild: Zutrittskontrollsystem-Dashboard
- Sprecher: "Ihr baut Systeme, die Gebäude schützen. Türen, Sensoren, Berechtigungen, Zentralen. Was wäre, wenn euer Entwicklungstool genauso funktioniert?"

**[0:20-0:50] Hooks = Alarmsensoren**
- Split-Screen: Links PIR-Sensor, rechts Code-Hook
- Sprecher: "Hooks in Claude Code sind wie eure Alarmsensoren. Ein PreToolUse-Hook reagiert, BEVOR etwas passiert — wie ein PIR-Melder, der den Alarm auslöst, bevor der Einbrecher die Tür erreicht."
- Visual: Sensor löst aus → Hook blockiert unsicheren Code

**[0:50-1:20] MCP = Der Datenbus**
- Bild: RS485-Bus mit angeschlossenen Geräten
- Sprecher: "Das Model Context Protocol ist der RS485 eurer KI-Welt. Ein standardisierter Bus, über den Claude mit jedem System kommuniziert — Datenbanken, APIs, Jira, Slack. Plug and Play."
- Animation: MCP-Server docken an wie RS485-Teilnehmer

**[1:20-1:50] Skills = Berechtigungsprofile**
- Bild: Zutrittsprofil-Editor
- Sprecher: "Skills sind wie Berechtigungsprofile in eurer Zutrittskontrolle. Jedes Profil definiert: Was darf in welcher Zone passieren? Ein TDD-Skill erzwingt Tests. Ein Security-Audit-Skill prüft OWASP-Regeln. Frei kombinierbar."
- Visual: Profile als Karten, die zusammengesteckt werden

**[1:50-2:20] Agents = Wachpersonal**
- Bild: Leitstelle mit Monitoren
- Sprecher: "Und Agents? Die sind euer autonomes Wachpersonal. Sie arbeiten eigenständig, treffen Entscheidungen, eskalieren wenn nötig. Ein Agent scannt, ein anderer fixt, ein dritter reviewed — wie ein Security Operations Center."
- Visual: Drei Agents arbeiten parallel an Bildschirmen

**[2:20-2:40] Zusammenführung**
- Animation: Alle Bausteine verbinden sich zu einem Gesamtsystem
- Sprecher: "Ihr baut jeden Tag Systeme, die genau so funktionieren. Jetzt könnt ihr ein Entwicklungssystem bauen, das genauso modular, erweiterbar und intelligent ist wie eure eigenen Produkte."

---

## Video 3: "Die grenzenlose Werkstatt" (1-2 Min)

### Ziel
Emotionaler Closer — zeigt die kreative Freiheit und unbegrenzten Möglichkeiten.

### Storyboard

**[0:00-0:15] Opening**
- Bild: Leere Werkstatt, ein Terminal
- Sprecher: "Eine leere Werkstatt. Ein einziges Werkzeug. Unendliche Möglichkeiten."

**[0:15-0:45] Rapid-Fire Use Cases**
- Schnelle Schnitte, je 3-5 Sekunden:
  - "Security-Audit eures Embedded-Codes — automatisch"
  - "Protokoll-Dokumentation aus dem Source Code generiert"
  - "Drei KI-Modelle debattieren über eure Architektur"
  - "Ein Wächter-Hook verhindert, dass Secrets committet werden"
  - "NotebookLM erstellt einen Podcast aus eurer API-Doku"
  - "Ein Agent refactored während ihr Kaffee holt"
- Visual: Jeder Use Case als kurze Animation/Icon

**[0:45-1:15] Das Multiplikator-Prinzip**
- Sprecher: "Das sind keine getrennten Features. Sie multiplizieren sich. Ein Skill, der einen Hook nutzt, der über MCP mit Jira spricht, gesteuert von einem Agent, der drei andere Agents koordiniert. Die einzige Grenze ist eure Vorstellungskraft."
- Visual: Exponentialkurve der Möglichkeiten

**[1:15-1:30] Closing**
- Text: "Bereit, eure Werkstatt einzurichten?"
- Sprecher: "In drei Workshop-Sessions bauen wir gemeinsam eure persönliche, grenzenlose Entwicklungsumgebung."

---

## Produktionshinweise

### Für eigene Video-Produktion
- **Synthesia/HeyGen**: Storyboard + Sprecher-Text direkt nutzbar als Script
- **Runway/Pika**: Visuals aus den Szenen-Beschreibungen generieren
- **CapCut/DaVinci**: Screen Recordings + Texteinblendungen zusammenschneiden

### Für NotebookLM-Videos
- NotebookLM generiert automatisch Explainer-Videos aus den Quellen
- Style "retro-print" wurde gewählt — modern aber nicht verspielt
- Ideal als visueller Teaser vor dem eigentlichen Workshop

### Empfohlene Reihenfolge im Workshop
1. **NotebookLM Audio Overview** (Podcast) — während Ankommen/Setup anhören
2. **Video 1 oder NotebookLM Video** — als offizieller Einstieg
3. **PowerPoint-Präsentation** — Überblick und Struktur
4. **Dann** erst die Text-Module zur Vertiefung
