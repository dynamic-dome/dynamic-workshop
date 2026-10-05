# Vorführen: S2.6 · Hooks als Sensoren: die drei Eckpfeiler

> Demo und Hinweise für Moderierende zum Kapitel [S2.6 · Hooks als Sensoren: die drei Eckpfeiler](../../library/s2-06-hooks-als-sensoren.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

Die Demo „Hooks: die Alarmanlage" steht in [S2.8](s2-08-hook-einrichten.md). Zu den drei Eckpfeilern gehören diese Sprechpunkte.

<details><summary>Für Moderierende</summary>

Einstieg: „Hooks sind Sensoren in deinem Workflow. Sie feuern bei Ereignissen. Sie sind keine Policy-Durchsetzung, sondern Best-Effort-Wächter."

Sprechpunkte:

- „Hooks sind die Sensoren deiner Alarmanlage: Sie feuern bei Ereignissen, nicht auf Zuruf."
- „PreToolUse ist der Sensor, der prüft, bevor die Tür aufgeht. Er kann sie verriegeln, über den Exit-Code aber nur mit `exit 2`."
- „PostToolUse ist der Sensor, der protokolliert, nachdem jemand durch ist."
- „Stop ist die Meldung zum Schichtende: Sie feuert, wenn Claude mit der Antwort fertig ist."
- „Eine Hook-Konfiguration gilt für jede Sitzung, jedes Projekt und jedes Teammitglied, das dieselbe Konfiguration nutzt."
- „So prüfst du Sicherheitsstandards, Code-Konventionen und Compliance-Vorgaben automatisch."

</details>
