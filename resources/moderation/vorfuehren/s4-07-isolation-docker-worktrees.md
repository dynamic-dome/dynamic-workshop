# Vorführen: S4.7 · Isolation mit Docker und Worktrees

> Demo und Hinweise für Moderierende zum Kapitel [S4.7 · Isolation mit Docker und Worktrees](../../library/s4-07-isolation-docker-worktrees.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: wo die Grenze eines Worktrees verläuft

**Ziel:** Zeigen, was ein Worktree isoliert und was nicht: Claude Code lehnt die Bearbeitung des Hauptordners ab, aber das Repository ist gemeinsam, und ein Commit im Worktree liegt sofort im Hauptordner sichtbar. Ein Worktree isoliert Dateien, er ist kein Sicherheitsrand um den Rechner.

**Dauer:** etwa 12 bis 15 Minuten.

Zeig die Übung aus dem Kapitel live: die Übung „wo die Grenze eines Worktrees verläuft“ in [S4.7](../../library/s4-07-isolation-docker-worktrees.md). Startzustand wie dort: das Repository `~/cc-workshop/isolation` mit `notes.txt`, `.gitignore` und der gitignorierten `local.env`, einem Commit und einem einmal bestätigten Vertrauensdialog. Du brauchst zwei Terminals: eines für Claude, eines für den Hauptordner. Notier dir den absoluten Pfad des Ordners für Schritt 3. Ablauf: die Schritte 1 bis 6 der Übung (`claude --worktree isolation-a --permission-mode acceptEdits`, `local.env` fehlt im Worktree, die Bearbeitung des Hauptordners wird abgelehnt, der Commit im Worktree, `git branch` und `git log` im Hauptordner, aufräumen mit „Remove worktree“).

Die Worktrees selbst führt die Demo in [S1.18](s1-18-worktrees.md) ein, einen Worktree mit Budget und Rundenlimit die Demo in [S3.13](s3-13-autonome-loops-absichern.md).

<details><summary>Für Moderierende</summary>

**Sagen:**

- Schritt 2: „Der Worktree ist ein frischer Checkout. Gitignorierte Dateien kommen nicht mit, Abhängigkeiten installiere ich im Worktree neu." Mit einer Datei `.worktreeinclude` lassen sich ignorierte Dateien in jeden neuen Worktree kopieren.
- Schritt 3: „Claude Code blockt in einer Worktree-Sitzung die Bearbeitung des Hauptordners. Die Doku nennt vier Prüfungen: Dateibearbeitung, Arbeitsverzeichnis von Befehlen, Git-Umleitungen und Befehlsform. Was sie nicht abdecken, blocken sie nicht: Ob ein Shell-Befehl mit einem absoluten Pfad in den Hauptordner schreiben könnte, sagt die Doku nicht. Dafür gelten der Rechte-Modus und seine Rückfragen." Fragt Claude zuerst, ob es die Datei im Hauptordner lesen darf, antworte mit „Yes“: Das Lesen ist erlaubt, es geht um das Schreiben.
- Schritt 4: Beantworte die Rückfrage zu `git commit` mit „Yes“, nicht mit „Yes, and don't ask again“: Diese Wahl würde laut Doku eine Regel im Hauptordner speichern, die für jeden Worktree des Repositories gilt.
- Schritt 5: „Die Dateien sind getrennt, das Repository ist gemeinsam. Der Commit liegt ohne Push im gemeinsamen Repository, der Branch ist im Hauptordner sichtbar." Nenn, was ein Worktree sonst noch teilt: gespeicherte Freigaben und die Projekt-Plugins. Und was er nicht trennt: laufende Prozesse, Ports, Datenbanken und dein Benutzerkonto.
- Schritt 6: „Entfernen löscht Worktree und Branch samt Arbeit."
- Container: Das Kapitel hat dafür keine Übung. Ein Container gibt Claude Code ein eigenes Dateisystem und eigene Prozesse; für ein Repository, dem du nicht traust, nennt die Doku eine eigene VM oder eine Cloud-Sitzung. Auch ein Dev-Container ist keine absolute Grenze: Mit `--dangerously-skip-permissions` hindert er ein bösartiges Projekt nicht daran, alles abzugreifen, was im Container erreichbar ist.

**Wenn etwas schiefgeht:**

- **Claude ändert nach der Ablehnung die Kopie im Worktree:** Das stört die folgenden Schritte nicht. Prüf im zweiten Terminal, dass `notes.txt` im Hauptordner `v1` blieb.
- **Claude versucht es mit einem Shell-Befehl und fragt nach Freigabe:** Lehn mit „No“ ab: Gemeint ist die Prüfung der Bearbeitung.
- **Den Worktree-Ordner gibt es schon, oder der Branch existiert:** Entferne den alten Worktree (`git worktree remove`) und den Branch oder nimm einen anderen Namen als `isolation-a`.
- **Optional, wenn Docker und das Plugin `multi-model-orchestrator` (🔧) vorbereitet sind:** Zeig die Docker-Isolation mit `/multi-model-orchestrator:inception` und einer kleinen Aufgabe wie „List all Python files in /workspace and count the lines of code in each.“ Fehlt Docker, lass das weg.

</details>
