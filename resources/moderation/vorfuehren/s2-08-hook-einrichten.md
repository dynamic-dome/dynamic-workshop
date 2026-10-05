# Vorführen: S2.8 · Einen Hook einrichten, der wirklich blockt

> Demo und Hinweise für Moderierende zum Kapitel [S2.8 · Einen Hook einrichten, der wirklich blockt](../../library/s2-08-hook-einrichten.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Hooks, die Alarmanlage

**Ziel:** Zeigen, dass ein PreToolUse-Hook eine gefährliche Shell-Aktion blockt, bevor sie läuft, harmlose Befehle durchlässt und nach dem Einrichten ohne dein Zutun arbeitet.

Zeig die Übung aus dem Kapitel live: die Übung „einen Wächter einrichten und blocken sehen“ in [S2.8](../../library/s2-08-hook-einrichten.md). Startzustand wie dort: der Ordner `~/cc-workshop/waechter` mit dem Skript `.claude/hooks/safety-check.sh` (mit Git Bash und `jq`) oder `.claude/hooks/safety-check.ps1` (Windows ohne Git Bash), das du vorher aus den getesteten Vorlagen in `resources/demos/assets/hooks/` kopierst, und der `.claude/settings.json` aus Schritt 4. Der Vertrauensdialog des Ordners ist einmal bestätigt, und der Ordner `build` mit `old.txt` (Schritt 5) liegt bereit.

**Ablauf:** Schritte 3, 5, 6 und 7 der Übung: den Handtest des Skripts mit den drei Eingaben, `/hooks`, der geblockte Auftrag `rm -rf build`, dann `echo hello`. Schritt 4 zeigst du als Konfiguration; sie hat drei Ebenen: welches Ereignis (`PreToolUse`), welches Tool (`matcher`), was läuft (`type` und `command`).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 bis 10 Minuten.

**Sagen:**

- Handtest (Schritt 3): „Bevor Claude das Skript benutzt, teste ich es von Hand. Es liest JSON von stdin, prüft den Befehl auf Muster und endet mit 0 (kein Einwand) oder mit 2 (blocken, der Grund steht auf stderr). Und bei einer Eingabe, die es nicht lesen kann, blockt es lieber: Ein kaputter Wächter soll die Tür schließen, nicht öffnen."
- Konfiguration (Schritt 4): „Drei Teile: welches Ereignis, welches Tool, was läuft. Der Matcher heißt `Bash|PowerShell`, weil unter Windows Shell-Befehle meist über das PowerShell-Tool laufen. Ein Hook nur mit `Bash` feuert dort nie."
- Schritt 6: „Ich habe Claude nicht gebeten, auf Gefahren zu achten. Der Hook hat vor der Rechte-Prüfung gefeuert und geblockt, es kam nicht einmal eine Löschen-Rückfrage. Der Ordner `build` ist noch da." Zeig `build/old.txt`. Den Hook-Block erkennst du am Text `SAFETY HOOK: potentially destructive command blocked` aus deinem Skript.
- Schritt 7: „Harmloses läuft normal durch, ohne Meldung."
- Blocken: „Ein PreToolUse-Hook kann eine Aktion ganz stoppen, über den Exit-Code aber nur mit `exit 2`. Mit Code 1 läuft sie trotzdem weiter." Ein PostToolUse-Hook kommt erst nach einem erfolgreichen Aufruf und macht ihn nicht rückgängig ([S2.6](s2-06-hooks-als-sensoren.md)).
- Grenze: „Hooks arbeiten nach bestem Bemühen: Ein falscher Pfad in der `settings.json` oder ein Absturz mit einem anderen Code als 2 lässt die Aktion durch. Ein Muster-Wächter erkennt nur die Schreibweisen, die er kennt. Für echte Isolation kommen Rechte-Regeln und eine Sandbox dazu."

Die Sprechpunkte zu den drei Eckpfeilern stehen in [S2.6](s2-06-hooks-als-sensoren.md).

**Wenn der Befehl trotzdem lief:** Prüf zuerst den Matcher (`Bash|PowerShell`) und den Pfad zum Skript in der `settings.json`, dann, ob der Vertrauensdialog bestätigt wurde. `/hooks` zeigt, ob der Eintrag geladen ist.

**Wenn Claude sich von selbst weigert:** Dann stammt die Ablehnung nicht vom Hook. Der Text `SAFETY HOOK: …` aus deinem Skript fehlt; formuliere den Auftrag mit dem genauen Befehl neu.

**Wenn unter Windows das Skript nicht startet:** In der Exec-Form der PowerShell-Variante gehören `-NoProfile` und `-ExecutionPolicy Bypass` dazu; sonst bricht Windows PowerShell mit der Standard-Richtlinie ab, und der Hook fällt still offen.

</details>
