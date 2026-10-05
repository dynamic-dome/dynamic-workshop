# Vorführen: S2.6 · Hooks als Sensoren: die drei Eckpfeiler

> Demo und Hinweise für Moderierende zum Kapitel [S2.6 · Hooks als Sensoren: die drei Eckpfeiler](../../library/s2-06-hooks-als-sensoren.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: drei Sensoren in einer Logdatei

**Ziel:** Zeigen, in welcher Reihenfolge PreToolUse, PostToolUse und Stop feuern und wann PostToolUse nicht feuert.

Zeig die Übung aus dem Kapitel live: die Übung „drei Sensoren in einer Logdatei“ in [S2.6](../../library/s2-06-hooks-als-sensoren.md). Startzustand wie dort: der Ordner `~/cc-workshop/hooks-sensoren` mit der `.claude/settings.json` aus Schritt 1; leg sie vorher an, bestätige den Vertrauensdialog einmal, und halte ein zweites Terminal im Ordner bereit, um `hook-log.txt` zu lesen. Ablauf: Schritte 3 bis 6 der Übung.

Die Demo „Hooks: die Alarmanlage“ mit einem Hook, der wirklich blockt, steht in [S2.8](s2-08-hook-einrichten.md).

<details><summary>Für Moderierende</summary>

Einstieg: „Hooks sind Sensoren in deinem Workflow. Sie feuern bei Ereignissen, nicht auf Zuruf.“

**Sagen:**

- Schritt 4: „`pre`, `post`, `stop`, in dieser Reihenfolge. PreToolUse ist der Sensor, der prüft, bevor die Tür aufgeht. Er kann sie verriegeln, über den Exit-Code aber nur mit `exit 2`. PostToolUse protokolliert, nachdem jemand durch ist. Stop ist die Meldung zum Schichtende: Sie feuert, wenn Claude mit der Antwort fertig ist."
- Schritt 5: Lass die Gruppe raten, was in der Datei steht, bevor du sie öffnest. „Stop feuert nach jeder abgeschlossenen Antwort, die Tool-Hooks nur bei Tool-Aufrufen."
- Schritt 6: „Der Befehl ist fehlgeschlagen. Es gibt `pre`, aber kein `post`: PostToolUse feuert nur nach Erfolg. Ein Protokoll-Hook nur an PostToolUse sieht fehlgeschlagene Aufrufe nicht." Bei einem Fehlschlag feuert stattdessen PostToolUseFailure.
- „Wo ein Hook steht, bestimmt, wofür er gilt: In `.claude/settings.json` nur im Projekt, in `~/.claude/settings.json` in all deinen Projekten. Claude Code führt Hooks aus Settings-Dateien erst aus, wenn der Vertrauensdialog für den Ordner bestätigt ist."
- „Der Matcher `Bash|PowerShell` trifft Shell-Befehle auf beiden Systemen. Unter Windows laufen Shell-Befehle meist über das PowerShell-Tool."

**Wenn die Logdatei leer bleibt:** Der Vertrauensdialog wurde nicht bestätigt, oder der Matcher steht nicht auf `Bash|PowerShell`. `/hooks` zeigt, ob die Hooks geladen sind.

</details>
