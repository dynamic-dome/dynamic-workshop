# Vorführen: S1.20 · Praxis-Station Session 1: alles in einem Ablauf

> Demo und Hinweise für Moderierende zum Kapitel [S1.20 · Praxis-Station Session 1: alles in einem Ablauf](../../library/s1-20-praxis-station-1.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

**Vor Session 1: Checkliste für die Demos**

- [ ] Terminal offen, Claude Code installiert (`claude --version`) und angemeldet (`claude auth status`)
- [ ] Arbeitsordner an einem neutralen Ort: Jede Demo zeigt die Übung ihres Kapitels und legt ihren Ordner unter `~/cc-workshop/<name>` an (`hello`, `claudemd`, `auftrag`, `git`, `worktree`, `kosten`, `station1`)
- [ ] keine sensiblen Dateien offen oder sichtbar
- [ ] Schrift groß genug für die Leinwand (Terminal-Schriftgröße 16 oder mehr)
- [ ] `gh` (GitHub CLI) angemeldet, falls die Git-Demo ([S1.16](s1-16-git-in-einem-fluss.md)) einen PR anlegt
- [ ] Python 3 vorhanden (`python --version` unter Windows, `python3 --version` unter macOS/Linux)

Dein Publikum sind erfahrene Entwicklerinnen und Entwickler aus der physischen Sicherheit. Nutze ihre Begriffe, wo es geht. Den Pre-Flight für jeden Workshop-Tag findest du im [Handbuch](../handbuch.md#pre-flight-am-workshop-tag).

**Wenn es in einer Demo hakt**

- **Claude liefert etwas Falsches.** Versteck es nicht, mach einen Lehrmoment daraus: „Genau deshalb prüfen wir, bevor wir etwas übernehmen. Ich zeige euch, wie man den Kurs korrigiert." Dann korrigierst du mit dem Muster aus dem Abschnitt „Wenn Claude danebenliegt" in [S1.20](../../library/s1-20-praxis-station-1.md).
- **Die Demo läuft langsam.** Erklär die Konzepte weiter, während du wartest: „Während Claude nachdenkt, erkläre ich euch, was unter der Haube passiert …"
- **Jemand fragt nach einer Funktion, die in der Demo nicht vorkommt.** „Gute Frage. Die parken wir für die Übungszeit, da habt ihr Zeit zum Ausprobieren. Kommen wir nicht dazu, sprecht mich in der Pause an."
- **Die Terminal-Ausgabe ist auf der Leinwand schlecht lesbar.** Setz vor der Demo den Terminaltyp:

```bash
export TERM=xterm-256color          # macOS / Linux / Git Bash
```
```powershell
$env:TERM = "xterm-256color"        # Windows PowerShell
```

Und stell die Schrift größer. Hilft das nicht, erzähl, was gerade passiert, und mach weiter.
