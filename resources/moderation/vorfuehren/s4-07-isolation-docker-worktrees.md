# Vorführen: S4.7 · Isolation mit Docker und Worktrees

> Demo und Hinweise für Moderierende zum Kapitel [S4.7 · Isolation mit Docker und Worktrees](../../library/s4-07-isolation-docker-worktrees.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo 3.5: Architektur und Fernarbeit im Überblick

**Ziel:** Zeigen, wie ein produktiver Ablauf mit mehreren Agenten von außen aussieht: Worktree-Isolation für die Sicherheit, Hintergrund-Sitzungen für lange Aufgaben, Remote Control vom Handy aus.

**Dauer:** etwa 10 bis 12 Minuten.

**Vorbereitung:**

- `claude`, angemeldet
- optional: Docker, für den Inception-Schritt
- optional: das Telegram-Bridge-Plugin (🔧), für den Bonus-Schritt

**Ablauf:** Die Schritte stehen in den Kapiteln, zu denen sie gehören.

1. Worktree-Isolation (3 Min., Pflicht): [S3.13](../../library/s3-13-autonome-loops-absichern.md)
2. Architektur am Whiteboard (3 bis 4 Min., Pflicht): [S4.8](../../library/s4-08-abschlussprojekt.md)
3. Remote Control, eingebaut (3 Min., Pflicht): [S4.6](s4-06-remote-und-teleport.md)
4. Telegram-Bridge (Bonus, 3 Min.): [S4.6](s4-06-remote-und-teleport.md)

**Optional zwischen Schritt 1 und 2: Inception**

Willst du auch die Docker-Isolation zeigen, setz sie zwischen Schritt 1 und Schritt 2: Starte `/multi-model-orchestrator:inception` (🔧) mit einer kleinen Aufgabe wie „List all Python files in /workspace and count the lines of code in each."

<details><summary>Für Moderierende</summary>

**Wenn etwas schiefgeht:**

- **Schritt 1: Den Worktree-Ordner gibt es schon.** Entferne ihn mit `git worktree remove ../experiment-async-processing` oder nimm einen anderen Pfad. Gibt es den Branch schon, lass `-b` weg, dann nutzt Git den vorhandenen Branch.
- **Auf dem Workshop-Rechner ist kein Docker installiert:** Lass den Inception-Schritt weg.
- **Schritt 3 und 4:** siehe [S4.6](s4-06-remote-und-teleport.md).

</details>
