# Vorführen: S4.6 · Unterwegs: Remote Control und /teleport

> Demo und Hinweise für Moderierende zum Kapitel [S4.6 · Unterwegs: Remote Control und /teleport](../../library/s4-06-remote-und-teleport.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo 3.5, Schritte 3 und 4: Remote Control und Telegram-Bridge

Ziel, Dauer und Vorbereitung der ganzen Demo stehen in [S4.7](s4-07-isolation-docker-worktrees.md). Schritt 1 (Worktree-Isolation) steht in [S3.13](s3-13-autonome-loops-absichern.md), Schritt 2 (Architektur am Whiteboard) in [S4.8](s4-08-abschlussprojekt.md).

**Schritt 3: Remote Control, eingebaut (3 Min., Pflicht)**

Zeig den offiziellen Weg, eine Sitzung von einem zweiten Gerät aus zu steuern:

```
/remote-control
```

Claude Code verbindet die Sitzung und nennt eine Sitzungs-URL. Ruf `/remote-control` noch einmal auf, dann zeigt das Statusfenster URL und QR-Code. Öffne die URL auf Handy oder Laptop, dann liest und antwortest du von dort.

**Oder `/teleport`**, um eine Cloud-Sitzung ins lokale Terminal zu holen:

```
/teleport
```

Du wählst eine Cloud-Sitzung aus, Claude Code holt ihren Branch und Verlauf, und du machst im Terminal weiter. Das ist praktisch, wenn du am Handy etwas begonnen hast und am Schreibtisch weitermachen willst.

**Schritt 4 (Bonus, nur wenn vorbereitet): Telegram-Bridge (3 Min., optional)**

> **Voraussetzung:** das Token eines Telegram-Bots, ein laufender Bridge-Dienst und das Workshop-Plugin `telegram-bridge` (🔧). **Ist das nicht vorbereitet, lass den Schritt weg.**

Zeig, wie die Workshop-eigene Telegram-Bridge Abläufe im Gruppenchat möglich macht:

- einen Befehl aus Telegram an deine lokale Claude-Sitzung schicken
- die Antworten als Telegram-Nachrichten zurückbekommen
- nützlich für Szenarien mit mehreren Nutzern oder für Gruppenkoordination

Das ist **eine Vorführung des Musters**, kein empfohlener Aufbau für den Betrieb: `/remote-control` (eingebaut) deckt die meisten Fälle einfacher und sicherer ab.

<details><summary>Für Moderierende</summary>

**Dauer:** Schritt 3 etwa 3 Minuten, Schritt 4 als Bonus weitere 3 Minuten.

**Vorher prüfen:** Beim ersten `/remote-control` fragt Claude Code einmalig nach deiner Zustimmung (**Enable Remote Control**). Bestätige das vor dem Workshop, damit der Dialog nicht live erscheint.

**Sagen:**

- Schritt 3: „Das ist der offizielle Weg, Claude Code von einem zweiten Gerät aus zu steuern. Keine eigene Infrastruktur nötig: derselbe Kanal, den Anthropic ausliefert, dieselbe Anmeldung, dasselbe Audit."

**Wenn etwas schiefgeht:**

- **Schritt 3: `/remote-control` geht nicht.** Meldet der Befehl, dass Remote Control ein claude.ai-Abo braucht, bist du nicht mit einem Abo angemeldet, etwa weil ein API-Key greift: Melde dich mit `/login` über claude.ai an. `Unknown command: /remote-control` zeigen ältere Versionen, die den Befehl noch nicht kennen oder eine fehlende Abo-Anmeldung so melden; aktualisiere dann Claude Code. Hilft beides nicht, beschränke dich auf Schritt 1 und 2 und erwähne, dass aktuelle Versionen die Funktion haben.
- **Schritt 3: `/teleport` findet keine Cloud-Sitzung.** Starte zuerst eine Sitzung auf claude.ai/code und ruf `/teleport` dann erneut auf. Oder lass es weg und zeig nur `/remote-control`.
- **Schritt 4: Die Bridge läuft nicht, oder das Plugin fehlt.** Lass den Schritt kommentarlos weg und sag: „Im Betrieb bräuchtet ihr einen laufenden Bridge-Dienst; das Muster steht in diesem Kapitel unter Telegram-Bridge."
- **Schritt 1 und der optionale Inception-Schritt:** siehe [S4.7](s4-07-isolation-docker-worktrees.md).

</details>
