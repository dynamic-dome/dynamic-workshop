# Vorführen: S2.14 · MCP: der Integrationsstecker

> Demo und Hinweise für Moderierende zum Kapitel [S2.14 · MCP: der Integrationsstecker](../../library/s2-14-mcp-stecker.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: MCP steuert einen echten Browser

**Ziel:** Zeigen, dass Claude einen echten Browser bedient. Nichts wird simuliert, kein statisches HTML ausgelesen: Claude ruft Seiten auf, klickt und arbeitet mit Live-Webseiten.

**Vorbereitung**

- Der Playwright-MCP-Server ist eingerichtet, in der `.mcp.json` des Projekts wie in „Selbst machen" oder per `claude mcp add` im Scope `user` ([S2.15](../../library/s2-15-mcp-einrichten.md)).
- Internetzugang
- Konfiguration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Schritt 1: die Bühne bereiten**

Kündige an, dass Claude gleich einen echten Browser steuert.

**Schritt 2: GitHub aufrufen**

In Claude Code:

```
Navigate to github.com/anthropics/claude-code using the browser
```

Claude ruft das Playwright-Tool auf. Ein Browserfenster öffnet sich (oder der Browser läuft headless, je nach Konfiguration) und lädt die URL.

Mach einen Screenshot:

```
Take a screenshot of the current page
```

Zeig den Screenshot in der Ausgabe im Terminal.

**Schritt 3: mit der Seite arbeiten**

```
Click on the Issues tab
```

Claude klickt auf den Tab „Issues". Zeig das Ergebnis.

```
List the titles of the first 5 open issues
```

Claude liest die Seite und zieht die Titel der Issues heraus. Zeig die Liste.

**Schritt 4: den Bezug zur eigenen Arbeit herstellen**

Nenn Beispiele aus der Arbeit der Teilnehmenden (Software für Physical Security) und frag, welche Weboberflächen sie heute von Hand bedienen.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten (Schritt 1: 1 Min., Schritt 2: 1 Min., Schritt 3: 3 Min., Schritt 4: 3 Min.).

**Sagen:**

- Schritt 1: „MCP verbindet Claude Code mit externen Systemen. Das anschaulichste Beispiel ist die Browser-Steuerung über Playwright. Passt auf: Claude steuert gleich einen echten Browser."
- Schritt 3: „Das ist ein echter Browser. JavaScript lief, dynamische Inhalte wurden geladen, echte DOM-Elemente geklickt. Keine HTTP-Anfragen, kein Scraping, echte Browser-Automatisierung."
- Schritt 4: „Überlegt, was das für eure Arbeit heißt." Beispiele:
  - „Euer Admin-Panel der Zutrittskontrolle: Claude könnte sich anmelden, Berichte über Türereignisse ziehen, exportieren und an euer Monitoring schicken."
  - „Das Firmware-Portal eures Herstellers: Claude könnte nach neuen Versionen sehen, sie herunterladen und die Update-Historie protokollieren."
  - „Die Weboberfläche eurer Alarmzentrale: Claude könnte Alarme quittieren, Tagesberichte erzeugen und den Zustand der Meldebereiche prüfen."
- Abschluss: „Jede Weboberfläche, die euer Team von Hand bedient, lässt sich mit Playwright-MCP automatisieren. Und das ist nur ein Server: Es gibt Server für Slack, Mail und Datenbanken, und ihr könnt eigene für eure Systeme bauen."

**Kernsätze:**

- „MCP ist die Zutrittskontrolle, die sich mit den anderen Gebäudeanlagen verbindet: Brandmeldeanlage, Videoüberwachung, Besuchermanagement. Claude ist die zentrale Leitstelle."
- „Ein Protokoll, viele Integrationen. Einmal lernen, alles anschließen."
- „Playwright-MCP macht aus jeder Weboberfläche eine API, die Claude bedienen kann."
- „Sicherheitshinweis: MCP-Server laufen mit euren Zugangsdaten. Deshalb sind Hooks und Leitplanken hier noch wichtiger." Vertiefung in [S2.17](../../library/s2-17-mcp-sicherheit.md).

**Wenn Playwright-MCP nicht eingerichtet ist:** Zeig die Konfigurationsdatei und erklär, was sie bewirken würde. Sag: „Das richten wir gleich in der Übung ein. Für jetzt: Glaubt mir, es funktioniert, und ihr probiert es selbst." Oder zeig einen Screenshot, den du bei der Vorbereitung gemacht hast, und beschreib, was passiert ist.

</details>
