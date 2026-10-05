# Vorführen: S4.6 · Unterwegs: Remote Control und /teleport

> Demo und Hinweise für Moderierende zum Kapitel [S4.6 · Unterwegs: Remote Control und /teleport](../../library/s4-06-remote-und-teleport.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Remote Control, eine lokale Sitzung im Browser

**Ziel:** Zeigen, dass eine Sitzung, die auf deinem Rechner läuft, von einem zweiten Gerät aus steuerbar ist: Der Auftrag kommt aus dem Browser, Claude führt ihn lokal aus, die Ausgabe steht an beiden Stellen.

Zeig die Übung aus dem Kapitel live: die Übung „eine lokale Sitzung im Browser öffnen und wieder trennen“ in [S4.6](../../library/s4-06-remote-und-teleport.md). Startzustand wie dort: der Ordner `~/cc-workshop/unterwegs` mit `todo.txt` (drei Zeilen), die Anmeldung über claude.ai mit einem Abo (API-Keys werden nicht unterstützt; bei Team und Enterprise muss ein Owner Remote Control freigeschaltet haben) und ein zweiter Bildschirm: ein Browser-Tab auf claude.ai/code oder das Handy mit der Claude-App. Ablauf: die Schritte 1 bis 6 der Übung (`claude auth status`, `/remote-control Workshop-Test`, das Statusfenster mit URL und QR-Code, ein lesender Auftrag aus dem Browser, Verbindung trennen, Sitzung beenden und archivieren).

`/teleport` (der umgekehrte Weg: eine Cloud-Sitzung samt Branch ins lokale Terminal holen) zeigst du nur, wenn eine Cloud-Sitzung auf einem gepushten Repository bereitsteht; das Kapitel hat dafür keine Übung.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten.

**Vorher prüfen:** Beim ersten `/remote-control` erscheint ein Dialog; laut Doku wählst du **Enable Remote Control**, die Bestätigung gilt einmalig. Mach das vor dem Workshop, damit der Dialog nicht live erscheint.

**Sagen:**

- Schritt 2: „Das ist der offizielle Weg, Claude Code von einem zweiten Gerät aus zu steuern. Keine eigene Infrastruktur nötig: dieselbe Anmeldung, dasselbe Konto." Der Rechner muss an sein und der `claude`-Prozess weiterlaufen.
- Schritt 3: Zeig URL und QR-Code im Statusfenster.
- Schritt 4: „Ausführung und Dateizugriff bleiben auf meinem Rechner. Die Oberfläche schickt nur Prompts." Auch ein Auftrag vom Browser läuft unter den Rechten der Sitzung: Das Lesen im Ordner braucht keine Freigabe, ein Schreibauftrag würde die Rückfrage auslösen, die der Modus vorsieht.
- Was dabei wohin geht: Solange Remote Control verbunden ist, liegt das Transkript der Sitzung (Nachrichten, Antworten, Werkzeugaktivität) auf Anthropics Servern. Die lokale Sitzung baut nur ausgehende HTTPS-Verbindungen auf und öffnet keine Ports.
- Dein Konto ist der Zugang: Wer dein claude.ai-Konto übernimmt, erreicht damit auch deine verbundene Sitzung.
- Für Nachrichten, die von außen in eine Sitzung kommen sollen (etwa aus einem Chat wie Telegram oder Discord), ist Remote Control nicht der Weg: Dafür nennt die Doku Channels (Research Preview). Für „ich will vom Handy aus meinen Laptop steuern" reicht Remote Control.

**Wenn etwas schiefgeht:**

- **`/remote-control` geht nicht:** Steht in `claude auth status` als `authMethod` `api_key`, `api_key_helper` oder `third_party`, ist die Übung nicht möglich: Remote Control braucht ein Abo, die Anmeldung über claude.ai mit `/login` und den Endpunkt `api.anthropic.com`. Mit Amazon Bedrock, Vertex, Foundry oder einem anderen `ANTHROPIC_BASE_URL` geht es nicht. Dann bleib beim Konzept und zeig die Schritte als Aufzeichnung.
- **Die Sitzung erscheint im Browser nicht:** Such sie unter **Code** nach ihrem Namen (`Workshop-Test`) oder öffne die URL aus dem Statusfenster.
- **Nach der Demo:** Trenn die Verbindung, beende die Sitzung und archiviere den Eintrag auf claude.ai/code. Schalte Remote Control nicht für alle Sitzungen ein: Es würde jede künftige Sitzung verbinden.
- **`/teleport` findet keine Cloud-Sitzung:** Laut Doku braucht Teleport einen sauberen Git-Stand, dasselbe Repository (keinen Fork), einen auf den Remote gepushten Branch und dasselbe claude.ai-Konto. Mit einer Anmeldung per API-Key ist es nicht verfügbar.

</details>
