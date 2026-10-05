# Claude Code Praxisbibliothek

> Claude Code lernen nach deinem Stand: 70 Kapitel in 19 Regalen — von der ersten Datei bis zur abgesicherten
> Agenten-Pipeline. Eine kurze Einstufung zeigt dir, welche Kapitel zu deinem Ziel passen; du musst nicht alles lesen.

Dieses Repository ist die Materialbasis hinter der Workshop-Seite von DoMe Dynamics
([dynamic-dome.com/systeme/workshop](https://dynamic-dome.com/systeme/workshop/)). Die Website ist das Schaufenster, hier liegt das Material:
Kapitel, getestete Vorlagen, Übungs-Playground, Lern-Cockpit, Tutor-Plugin und Moderationsunterlagen.

## Für wen

- **Entwicklerinnen und Entwickler**, die Claude Code produktiv und sicher einsetzen wollen — Programmiererfahrung ja,
  Erfahrung mit Coding-Agenten nicht nötig.
- **Tech Leads**, die einschätzen wollen, ob und wie ihr Team Claude Code einführt.
- **Moderierende**, die daraus einen Workshop in vier Sessions halten.

## Drei Wege hinein

| Weg | So geht's |
|---|---|
| **Einstufung** (empfohlen) | Im Lern-Cockpit [`resources/claude-code-workshop-ui.html`](resources/claude-code-workshop-ui.html) (im Browser öffnen), mit dem Tutor `/dynamic-workshop:workshop start` in Claude Code oder zum Selbermachen in [`einstufung.md`](resources/library/einstufung.md). Fünf Minuten, keine Noten. |
| **Fertiger Pfad** | [Schnellstart, ein Pfad je Ziel oder die vier Live-Sessions](resources/paths/README.md). |
| **Stöbern** | [Die Bibliothek](resources/library/README.md) mit Regal-Karte. Jedes Kapitel beginnt mit einem Schnellcheck. |

Wie du damit lernst, moderierst oder das Material pflegst: [HOW-TO-USE.md](HOW-TO-USE.md).

## Was drin steckt

- **Kapitel mit festem Aufbau:** Schnellcheck → Auf einen Blick → Bild im Kopf → Im Detail → Selbst machen →
  Typische Fallen → Check → Weiterlesen, mit der offiziellen Doku als Primärquelle. Geschrieben für eine Person, die
  allein lernt; Demos und Hinweise für Moderierende liegen getrennt unter `resources/moderation/`.
- **Bilder aus der Sicherheitstechnik:** Rechte-Modi als Zutrittsebenen, Hooks als Türsensoren, Worktrees als Testlabor.
- **Sicherheitsboden:** Neun Kapitel empfehlen wir auch Fortgeschrittenen — etwa, dass von den Exit-Codes nur `exit 2`
  einen Hook blocken lässt und `claude -p` ohne `--bare` die Hooks eines fremden Repos ausführt.
- **Getestet statt behauptet:** Kopierbare Hooks sind [getestete Vorlagen](resources/demos/assets/hooks/), Wächter-Tests
  verhindern bekannte Falschaussagen, ein [Übungs-Playground](workshop-playground/) mit fünf eingebauten Schwachstellen.
- **Einstufung ohne Druck:** Verhaltensfragen statt Wissensabfrage, freiwillige Mini-Szenarien, Empfehlung mit Begründung.
- **Tutor im Stil von `teach`:** Lernordner mit Mission und Lernprotokollen, Abruf mit Abstand ([X.2](resources/library/x-02-lernen-mit-claude-code.md)).
- **Community-Regal:** belegte Skill-Sammlungen und eine Prüfliste für fremde Skills ([X.1](resources/library/x-01-community-skills.md)), dazu zwei Blicke über den Tellerrand: ein minimaler Agent als Spiegel ([X.3](resources/library/x-03-pi-als-spiegel.md)) und was bei Agenten im Dauerbetrieb schiefgehen kann ([X.4](resources/library/x-04-agenten-im-dauerbetrieb.md)).

## Stand

Modelle, Preise und der geprüfte CLI-Stand stehen an genau einer Stelle: [`resources/_canonical.md`](resources/_canonical.md).
Im Material stehen Aliase (`opus`, `sonnet`, `haiku`, `fable`) und Rollen. Eine monatliche Prüfung vergleicht die im Kurs
genannten Flags, Variablen und Hook-Ereignisse mit der offiziellen Doku. Im Zweifel gelten `/model`, `/release-notes`
und `claude --version` auf deinem Rechner.

## Einordnung

| Ebene | Rolle |
|---|---|
| Werkstatt | wie aus einzelnen Werkzeugen ein persönlicher Arbeitsmodus wurde |
| DCO | ein gebautes agentisches System mit Werkzeuggrenzen, Dashboard und Freigaben |
| Praxisbibliothek | übersetzt diese Praxis in einen Lernweg für Entwicklerteams |
