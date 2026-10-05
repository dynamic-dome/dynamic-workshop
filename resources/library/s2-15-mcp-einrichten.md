---
id: S2.15
type: lesson
title: "MCP einrichten: Transporte, Scopes, CLI"
shelf: mcp-knowledge
level: core
minutes: 15
requires: [S2.14]
safety_floor: false
transferable: false
outcome: "Ich kann einen MCP-Server mit claude mcp add (HTTP oder stdio) im passenden Scope registrieren oder in der .mcp.json mit ${VAR:-default} eintragen und mit claude mcp list oder /mcp prüfen, ob er verbunden ist."
sources:
  - https://code.claude.com/docs/en/mcp
aliases: []
---

# S2.15 · MCP einrichten: Transporte, Scopes, CLI

<!-- meta:start -->
> **Regal:** [MCP & Wissensquellen](README.md#mcp-knowledge) · **Stufe:** Kern · **~15 Min** · **Voraussetzungen:** [S2.14 MCP: der Integrationsstecker](s2-14-mcp-stecker.md)
>
> ← [S2.14 MCP: der Integrationsstecker](s2-14-mcp-stecker.md) · [Bibliothek](README.md) · [S2.16 MCP im Detail: OAuth, Ausgabegrenzen, Protokoll](s2-16-mcp-im-detail.md) →
<!-- meta:end -->

## Schnellcheck

- Kannst du ohne Nachschlagen sagen, welcher Scope in der eingecheckten `.mcp.json` landet und wo Claude Code die beiden anderen speichert?
- Hast du schon einmal einen MCP-Server mit `claude mcp add` angelegt und danach mit `/mcp` oder `claude mcp list` geprüft, ob er verbunden ist?

## Auf einen Blick

Für einen neuen MCP-Server wählst du zwei Dinge. Den Transport: `http` für entfernte Dienste (empfohlen) oder `stdio` für einen lokalen Prozess; SSE ist veraltet. Und den Scope: `local` (Standard, nur du, nur dieses Projekt), `project` (das Team, über die eingecheckte `.mcp.json`) oder `user` (nur du, in allen Projekten). `local` und `user` speichert Claude Code in `~/.claude.json`, nicht in einer `.mcp.json`.

Anlegen kannst du Server mit `claude mcp add` oder direkt in der `.mcp.json`. Zugangsdaten gehören nicht in eine eingecheckte Datei: `${VAR}` und `${VAR:-default}` holen sie aus der Umgebung.

## Bild im Kopf

Der Transport ist die Verkabelung eines Kartenlesers am Controller. `stdio` ist die feste Leitung vor Ort, etwa RS-485 vom Leser zum Controller. `http` ist die Anbindung aus der Ferne über ein gesichertes Netzsegment. SSE weiter zu nutzen ist, wie ein Protokoll zu betreiben, dessen Support ausläuft: Es funktioniert noch, aber der Hersteller empfiehlt den Wechsel.

Der Scope sagt, wo die Anschlussliste hängt: an deinem Arbeitsplatz in einem Gebäude (`local`), im Schaltschrank des Gebäudes für alle Techniker (`project`) oder in deinem eigenen Werkzeugkoffer für jeden Einsatz (`user`).

```mermaid
flowchart TD
  A["neuer MCP-Server"] --> B{"Wo läuft er?"}
  B -- "entfernt, im Netz" --> H["--transport http"]
  B -- "lokaler Prozess" --> S["stdio<br/>claude mcp add name -- befehl"]
  H --> C{"Wer soll ihn sehen?"}
  S --> C
  C -- "nur ich, nur hier" --> L["local (Standard)<br/>~/.claude.json"]
  C -- "das ganze Team" --> P["project<br/>.mcp.json im Repo"]
  C -- "nur ich, überall" --> U["user<br/>~/.claude.json"]
  L --> V["prüfen: /mcp oder claude mcp list"]
  P --> V
  U --> V
```

## Im Detail

### Transporte

MCP-Server sprechen über verschiedene Transporte mit Claude Code:

| Transport | So arbeitet er | Gut für | Status |
|-----------|-------------|----------|--------|
| **HTTP** | Entfernter Server über HTTPS | Cloud-Dienste, gemeinsame Team-Server | **empfohlen** |
| **stdio** | Lokaler Prozess, spricht über stdin/stdout | Lokale Werkzeuge, eigene Skripte, Zugriff aufs System | gut für die Entwicklung |
| **SSE** | Server-Sent Events | alte Server | **veraltet**, nimm HTTP |

**Warum SSE raus ist:** Der SSE-Transport ist zugunsten von **Streamable HTTP** abgekündigt. Neue Server nutzen `http`; in JSON-Konfigurationen heißt derselbe Transport auch `streamable-http` ([S2.16](s2-16-mcp-im-detail.md)). SSE behältst du nur für einen alten Server, der noch nicht umgestellt hat.

### Scopes

Wie Plugins ([S2.12](s2-12-plugin-lebenszyklus.md)) leben auch MCP-Server in verschiedenen Scopes:

| Scope | Gilt in | Mit dem Team geteilt | Gespeichert in |
|-------|---------|----------------------|----------------|
| **local** (Standard) | nur im aktuellen Projekt | nein | `~/.claude.json`, unter dem Eintrag dieses Projekts |
| **project** | nur im aktuellen Projekt | ja, über die Versionskontrolle | `.mcp.json` im Projektordner |
| **user** | in allen deinen Projekten | nein | `~/.claude.json` |

„local" bei MCP ist nicht dasselbe wie die lokalen Einstellungen in `.claude/settings.local.json`: Lokale MCP-Server stehen in `~/.claude.json` in deinem Home-Verzeichnis, nicht im Projektordner.

**Achtung bei älteren Anleitungen:** Die Namen haben sich früh geändert. Seit Claude Code 0.2.49 heißt der frühere Scope `project` jetzt `local`, und `global` heißt `user`. Den heutigen Scope `project` mit der `.mcp.json` gibt es seit Version 0.2.50. Steht in einer alten Anleitung „project scope" für einen privaten Server, ist heute `local` gemeint; steht dort „global scope", ist `user` gemeint. Die Mechanik blieb gleich, nur die Namen wanderten.

### Server über die Kommandozeile verwalten

```bash
# Add remote HTTP server (recommended for cloud services)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Add with auth header (--header goes after the URL)
claude mcp add --transport http myapi https://api.example.com/mcp --header "Authorization: Bearer xxx"

# Add local stdio server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Add with environment variables (another option between --env and the name)
claude mcp add --env GITHUB_TOKEN=xxx --transport stdio github -- npx -y @modelcontextprotocol/server-github

# Add a complex config inline as JSON (skips per-flag bookkeeping)
claude mcp add-json my-server '{"command":"npx","args":["-y","my-package"],"env":{"FOO":"bar"}}'

# Reset stored Approve/Decline choices for project-scope .mcp.json servers
claude mcp reset-project-choices

# Manage servers
claude mcp list                  # List all configured servers
claude mcp get <name>            # Show server details
claude mcp remove <name>         # Remove a server

# Load servers from config file
claude --mcp-config servers.json                       # Load additional MCP config
claude --mcp-config servers.json --strict-mcp-config   # ONLY use servers from that file (no others)

# In-session
/mcp                             # Check status, manage OAuth, troubleshoot
```

Gegenüber älteren Fassungen dieses Kurses stehen zwei Befehle anders, weil sie so scheiterten: `--header` steht hinter der URL, und zwischen `--env` und dem Servernamen steht eine weitere Option. Beide Flags nehmen mehrere Werte an und lesen sonst den Servernamen, bei `--header` auch die URL, als weitere Werte (siehe „Typische Fallen"). `--strict-mcp-config` steht zusammen mit `--mcp-config`, weil es nur die Server aus dieser Datei zulässt.

Die Beispiele nutzen die npm-Pakete `@modelcontextprotocol/server-github` (hier) sowie `-slack` und `-postgres` (unten). Diese Pakete sind auf npm inzwischen als „no longer supported" markiert. Nimm sie als Muster für die Schreibweise; für GitHub zeigt die offizielle Doku einen entfernten HTTP-Server mit Token im Header.

Ein Token direkt im Befehl (`Bearer xxx`, `GITHUB_TOKEN=xxx`) steht danach in deiner Shell-History und im Klartext in `~/.claude.json`. Für Dateien, die du mit dem Team teilst, nimmst du Umgebungsvariablen (nächster Abschnitt).

### Server als Datei: die .mcp.json

Statt per Befehl trägst du Team-Server direkt in die `.mcp.json` im Projektordner ein (Scope `project`). Persönliche Server in den Scopes `local` und `user` legt Claude Code in `~/.claude.json` ab; die verwaltest du mit `claude mcp add` und `claude mcp remove`.

<!-- cockpit:example -->
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {}
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN:-default-dev-token}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${PG_URL:-postgresql://user:pass@localhost/mydb}"
      }
    }
  }
}
```

**Umgebungsvariablen** setzt Claude Code in zwei Formen ein:

- `${VAR}` setzt den Wert von `VAR` ein. Ist `VAR` nicht gesetzt, lädt die Konfiguration trotzdem: Claude Code warnt in `claude mcp list` und in `/mcp` und übernimmt den Text `${VAR}` unverändert.
- `${VAR:-default}` setzt den Wert von `VAR` ein, oder `default`, wenn `VAR` nicht gesetzt ist.

Die Form mit `:-default` ist die sichere Wahl für geteilte `.mcp.json`-Dateien im Repo: Jeder im Team bekommt einen brauchbaren Rückfallwert, und in Produktion überschreibt die echte Umgebungsvariable ihn.

Beim Start liest Claude Code die Konfiguration und verbindet sich mit jedem Server; die Tools stehen Claude dann zur Verfügung. Server aus einer `.mcp.json` nutzt Claude Code in einer interaktiven Sitzung erst, nachdem du sie bestätigt hast. `claude mcp reset-project-choices` setzt diese Entscheidungen zurück. Warum die Bestätigung eine Sicherheitsfrage ist, steht in [S2.17](s2-17-mcp-sicherheit.md).

Ausprobieren kannst du das in der Übung von [S2.14](s2-14-mcp-stecker.md#übung-einen-mcp-server-anbinden): Dort bindest du Playwright über eine `.mcp.json` an.

## Typische Fallen

- **`claude mcp add` meldet `error: missing required argument 'name'`.** `--header` nimmt mehrere Werte an und schluckt Name und URL, wenn sie dahinter stehen. Schreib `--header` hinter die URL.
- **`Invalid environment variable format: github`.** Auch `--env` nimmt mehrere Paare an. Folgt der Servername direkt auf das Paar, liest die CLI ihn als weiteres Paar und lehnt ihn ab. Setz eine andere Option wie `--transport stdio` zwischen `--env` und den Namen.
- **Der Server steht auf `⏸ Pending approval`.** Das ist ein Server aus der `.mcp.json`, den du noch nicht bestätigt hast. Start `claude` interaktiv im Projekt und bestätige ihn.
- **Der Server verbindet nicht oder läuft in einen Timeout.** `/mcp` zeigt den Status und führt bei Bedarf durch eine neue Anmeldung. `claude mcp get <name>` zeigt die Konfiguration und bei `✘ Failed to connect` in der Zeile `Issue:` den Grund.
- **Die Server stehen in `.claude/.mcp.json` oder `~/.claude/.mcp.json`.** Ältere Fassungen dieses Kurses nannten diese Pfade. Claude Code liest dort keine Server: `local` und `user` liegen in `~/.claude.json`, `project` in der `.mcp.json` im Projektordner.

## Check

Du kannst für eine Integration Transport und Scope begründen, den Server mit `claude mcp add` oder in der `.mcp.json` eintragen und prüfen, ob er verbunden ist.

1. Warum nimmst du für einen neuen entfernten Server `http` statt SSE?
2. Wo speichert Claude Code einen Server im Scope `local`, wo im Scope `user` und wo im Scope `project`?
3. Was passiert, wenn in der `.mcp.json` `${VAR}` steht, `VAR` aber nicht gesetzt ist?

<details><summary>Quizfrage</summary>

**Frage:** Ein MCP-Server soll für alle bereitstehen, die das Repo klonen, ohne dass jemand `claude mcp add` aufruft. Welcher Scope passt?

- **Richtig:** `project`: Der Eintrag steht in der `.mcp.json` im Projektordner und wird mit dem Repo eingecheckt.
- Falsch: `user`: Der Eintrag gilt in allen Projekten und reist deshalb beim Klonen automatisch mit.
- Falsch: `local`: Der Standard-Scope schreibt in eine `.claude/.mcp.json`, die jeder im Team automatisch mit auscheckt.
- Falsch: Keiner: Claude Code übernimmt nie Server aus einem Repo, jeder muss sie selbst anlegen.

</details>

## Weiterlesen

- [MCP in Claude Code](https://code.claude.com/docs/en/mcp)
- [S2.14 · MCP: der Integrationsstecker](s2-14-mcp-stecker.md) (Übung)
- [S2.16 · MCP im Detail: OAuth, Ausgabegrenzen, Protokoll](s2-16-mcp-im-detail.md)
- [S2.17 · MCP-Sicherheit und ein eigener Server](s2-17-mcp-sicherheit.md)
- [S2.12 · Plugin-Lebenszyklus, Scopes und Marketplaces](s2-12-plugin-lebenszyklus.md)
