# Vorführen: S2.14 · MCP: der Integrationsstecker

> Demo und Hinweise für Moderierende zum Kapitel [S2.14 · MCP: der Integrationsstecker](../../library/s2-14-mcp-stecker.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: einen MCP-Server anbinden und ein Tool aufrufen

**Ziel:** Zeigen, dass MCP Claude Code mit einem externen System verbindet: ein Eintrag in der `.mcp.json`, eine Freigabe, und Claude ruft ein Tool auf, dessen Antwort es nur dort bekommen kann. Nichts wird simuliert.

Zeig die Übung aus dem Kapitel live: die Übung „einen Server anbinden und ein Tool aufrufen lassen“ in [S2.14](../../library/s2-14-mcp-stecker.md). Startzustand wie dort: der Ordner `~/cc-workshop/mcp` mit `server.py` (Schritt 1) und der `.mcp.json` aus Schritt 3. Leg beide vorher an; unter Windows steht in der `.mcp.json` `"command": "python"`. Du brauchst Python und sonst nichts, auch kein Internet.

**Ablauf:** Schritte 4 bis 7 der Übung: `claude mcp list` (Status `Pending approval`), die Sitzung mit `claude --permission-mode default`, die Freigabe des Servers und `/mcp`, der Auftrag mit dem Türcode des Labors, die Frage nach dem vollen Werkzeugnamen. Den Handtest des Servers (Schritt 2) kannst du vorab zeigen: Er schickt dem Server eine Zeile und liest die Antwort.

**Zugabe, wenn Zeit bleibt:** der echte Browser aus der Extra-Übung des Kapitels („Playwright, ein echter Browser“). Der Server braucht Node.js mit `npx` und seinen eigenen Ordner `~/cc-workshop/mcp-browser`; die Konfiguration steht im Kapitel. Frag `What browser tools do you have available?`, dann `Navigate to example.com using the browser and take a screenshot`. Nimm keine Seite, die eine Anmeldung verlangt.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten für den Server aus der Übung, mit der Zugabe etwa 15.

**Sagen:**

- Vor Schritt 4: „MCP verbindet Claude Code mit externen Systemen. Das ist ein winziger Server, nur Standardbibliothek. Er kennt zwei Tools."
- Schritt 4: „Der Server steht in der Liste, aber noch nicht freigegeben: `Pending approval`. Claude Code nutzt Server aus einer `.mcp.json` erst nach deiner Freigabe, damit ein geklontes Repo sich keine Server unterschieben kann."
- Schritt 5: Lies die Antwortoptionen vor und wähl „Use this MCP server“. Vorausgewählt ist „Continue without using this MCP server“: Wer nur Enter drückt, wählt das Falsche. Danach `/mcp`, mit `Esc` schließen.
- Schritt 6: „Ohne den Zusatz ‚Without reading any files‘ könnte Claude den Code aus `server.py` lesen. So bekommt es ihn nur vom Server." Antwort: `3088`.
- Schritt 7: „In Claude Code heißt das Tool `mcp__rooms__door_code`."
- Zugabe: „Das ist ein echter Browser: JavaScript läuft, Elemente werden wirklich angeklickt." Was du tippst, steht im Gespräch, und Claude Code legt Sitzungen im Klartext ab. Ob das Fenster sichtbar ist, regelt ein Flag des Servers (`--headless`), nicht Claude Code. Beim ersten Aufruf kann Playwright einen Browser nachladen oder melden, dass er fehlt.
- Abschluss: Frag die Teilnehmenden, welche Weboberflächen und Systeme ihres Alltags sie heute von Hand bedienen: das Admin-Panel der Zutrittskontrolle, das Firmware-Portal eines Herstellers, die Oberfläche einer Alarmzentrale. Sag, dass es Server für viele Systeme gibt und dass man eigene bauen kann.
- Sicherheitshinweis: „MCP-Server laufen mit euren Zugangsdaten. Deshalb sind Hooks und Leitplanken hier noch wichtiger." Vertiefung in [S2.17](../../library/s2-17-mcp-sicherheit.md).

**Wenn die Freigabe nicht erscheint oder `/mcp` den Server nicht zeigt:** Prüf, ob die `.mcp.json` im Ordner liegt, in dem Claude gestartet wurde, und ob `python` bzw. `python3` zur Plattform passt. Der Handtest des Servers (Schritt 2) zeigt, ob er selbst läuft.

**Wenn Playwright nicht eingerichtet ist:** Lass die Zugabe weg oder zeig nur die Konfiguration aus dem Kapitel und sag: „Das probiert ihr gleich in der Übung selbst."

</details>
