---
id: S2.9
type: lesson
title: Hook-Typen und Hooks in Komponenten
shelf: hooks
level: deep-dive
minutes: 15
requires: [S2.8]
safety_floor: false
transferable: false
outcome: "Ich kann die fünf Hook-Typen (command, http, prompt, agent, mcp_tool) nach ihrem Einsatz wählen und einen Hook mit der richtigen Lebensdauer in das Frontmatter eines Skills oder Subagenten einbetten."
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
aliases: []
---

# S2.9 · Hook-Typen und Hooks in Komponenten

## Schnellcheck

- Kannst du ohne Nachschlagen erklären, wann ein `prompt`-Hook statt eines `command`-Hooks sinnvoll ist?
- Hast du schon einmal einen Hook ins Frontmatter eines Skills geschrieben statt in `settings.json`?

## Auf einen Blick

Hooks führen nicht nur Shell-Befehle aus: Es gibt fünf Typen, nämlich `command`, `http`, `prompt`, `agent` und `mcp_tool`. Außerdem müssen Hooks nicht in `settings.json` stehen. Im Frontmatter eines Skills oder Subagenten leben sie mit ihrer Komponente: Subagent-Hooks nur, solange der Subagent läuft, Skill-Hooks ab dem Aufruf des Skills bis zum Ende der Sitzung (`once: true` entfernt einen Handler nach seinem ersten erfolgreichen Lauf).

## Bild im Kopf

Ein Subagent-Hook ist ein Sensor, den ein Wachmann auf einer Streife mitträgt: Er kommt mit ihm zurück. Ein Skill-Hook ist ein Sensor, den der Wachmann auf der Streife an die Wand schraubt: Er bleibt bis Schichtende scharf, es sei denn, er ist so gebaut, dass er sich nach dem ersten Alarm selbst abschaltet (`once: true`).

Die Hook-Typen sind wie die Reaktionsarten an einem Alarmauslöser: den Wachmann anrufen (Shell-Skript), ein Signal an die externe Leitstelle senden (HTTP), beurteilen lassen, ob es ein Fehlalarm ist (Prompt), einen Spezialisten zur Untersuchung schicken (Agent) oder direkt ins Gebäudeleitsystem schreiben, ohne Umweg (MCP-Tool).

## Im Detail

### Fünf Hook-Typen

Hooks führen nicht nur Shell-Befehle aus. Es gibt fünf Typen:

| Typ | So arbeitet er | Gut für |
|------|-------------|----------|
| **command** | Führt einen Shell-Befehl aus (Standard) | Einfache Prüfungen, Skripte, Logging |
| **http** | Schickt eine HTTP-Anfrage an eine URL | Webhook-Benachrichtigungen, externe APIs |
| **prompt** | Schickt Claude einen Prompt zur Bewertung | Komplexe Entscheidungen, die Kontext brauchen |
| **agent** | Startet einen Subagenten zur Bewertung | Mehrstufige Prüflogik |
| **mcp_tool** | Ruft ein MCP-Tool direkt auf | Nachricht an Slack über MCP, Push an ein Monitoring-Dashboard, strukturierte externe Aktion ohne Umweg über die Shell |

**Beispiel: ein prompt-Hook**, der bewertet, ob ein Shell-Befehl sicher ist (`Bash|PowerShell`, damit er auch unter Windows mit dem PowerShell-Tool greift, [S2.8](s2-08-hook-einrichten.md)):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this command is safe for a production environment. Block if it modifies system files, deletes data, or accesses network resources outside the project scope."
          }
        ]
      }
    ]
  }
}
```

### Was du bei der Wahl bedenkst

- **`prompt` und `agent` fragen ein Modell.** Das kostet Tokens und Zeit, und das Urteil kann von Lauf zu Lauf anders ausfallen. Für feste Regeln wie Muster oder Pfade bleibt `command` die bessere Wahl.
- **`http` schickt die Ereignisdaten nach außen.** Die Hooks-Referenz beschreibt, dass ein `http`-Hook das JSON des Ereignisses als POST-Anfrage an die URL sendet. Tool-Eingaben verlassen damit deinen Rechner. Prüf vorher, was darin stehen kann ([S3.11](s3-11-datenschutz-und-compliance.md)).
- **`mcp_tool` braucht einen MCP-Server.** Was MCP ist und wie du einen Server einrichtest, zeigen [S2.14](s2-14-mcp-stecker.md) und [S2.15](s2-15-mcp-einrichten.md).

### Hooks in Komponenten: Skill- und Subagent-Frontmatter

Hooks müssen nicht in `settings.json` stehen. Du kannst sie auch **in das Frontmatter eines Skills oder Subagenten einbetten**, im selben verschachtelten Format wie in den Settings (Matcher-Gruppe → Liste `hooks` → Handler). Die beiden Komponenten unterscheiden sich darin, wie lange ihre Hooks leben:

- **Subagent-Hooks** laufen nur, solange dieser Subagent läuft, und werden entfernt, wenn er fertig ist.
- **Skill-Hooks** werden registriert, sobald der Skill aufgerufen wird, und **bleiben für den Rest der Sitzung aktiv**, auch in späteren Runden. Setz `once: true` an einen Handler, wenn er nach seinem ersten erfolgreichen Lauf entfernt werden soll.

So bringt ein Skill seine eigenen Vor- und Nachprüfungen mit, ohne die globalen Settings zu belasten.

<!-- cockpit:example -->
```yaml
---
name: deploy
description: Deploy the current branch to staging
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./pre-deploy-check.sh"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./post-deploy-notify.sh"
          once: true
---
```

`pre-deploy-check.sh` ist scharf, sobald `/deploy` läuft, und bleibt es bis zum Ende der Sitzung; `post-deploy-notify.sh` feuert einmal und wird dann entfernt. Einen globalen Hook, der nach dem Skill-Namen filtert, brauchst du nicht.

Wie du die SKILL.md selbst schreibst, zeigt [S2.2](s2-02-skill-schreiben.md), einen eigenen Subagenten [S3.3](s3-03-eigener-subagent.md).

## Typische Fallen

- **Der Skill-Hook läuft weiter.** Nach dem ersten Aufruf von `/deploy` bleibt `pre-deploy-check.sh` bis zum Sitzungsende scharf, auch bei Bash-Befehlen, die mit dem Deploy nichts zu tun haben. Soll ein Handler nur einmal laufen, setz `once: true`.
- **Typ und Ereignis verwechseln.** Der Typ sagt, *wie* ein Hook arbeitet (`command`, `http` …). Das Ereignis sagt, *wann* er feuert ([S2.7](s2-07-hook-ereignisse.md)).
- **Ein Modell-Urteil als feste Regel behandeln.** Ein `prompt`-Hook ist kein deterministischer Wächter. Was sicher geblockt werden muss, gehört in einen `command`-Hook mit `exit 2` ([S2.8](s2-08-hook-einrichten.md)).

## Check

Du kannst erklären, wann ein `prompt`-Hook besser passt als ein `command`-Hook, und zeigen, wie ein Hook im Frontmatter einen Deploy-Skill mit eigener Vor- und Nachprüfung ausstattet, ohne die globale settings.json zu belasten.

1. Welcher Hook-Typ passt für eine feste Musterprüfung, welcher für ein Urteil, das Kontext braucht?
2. Wie lange lebt ein Hook im Skill-Frontmatter, wie lange einer im Subagent-Frontmatter?
3. Was bewirkt `once: true` an einem Handler?

<details><summary>Quizfrage</summary>

**Frage:** Warum ist ein Hook im Frontmatter eines Skills oft besser als ein globaler Hook, der nach dem Skill-Namen filtert?

- **Richtig:** Er gehört zum Skill: Er wird erst beim Aufruf registriert, und kein globaler Hook muss selbst herausfinden, ob gerade dieser Skill läuft.
- Falsch: Er ist schneller, weil er fest in die Skill-Datei kompiliert wird, während ein globaler Hook bei jedem Aufruf einen neuen Prozess startet.
- Falsch: Es gibt keinen Unterschied in der Wirkung; beide werden gleich ausgewertet, das Frontmatter liest sich nur besser.
- Falsch: Nur im Frontmatter gehen die Typen `prompt` und `agent`; in settings.json sind nur `command` und `http` erlaubt.

</details>

## Weiterlesen

- [Hooks-Referenz](https://code.claude.com/docs/en/hooks)
- [Skills-Doku](https://code.claude.com/docs/en/skills)
- [Subagenten-Doku](https://code.claude.com/docs/en/sub-agents)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S2.2 · Eine SKILL.md schreiben](s2-02-skill-schreiben.md)
- [S3.3 · Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md)
- [S3.11 · Datenschutz, Aufbewahrung und regulierte Branchen](s3-11-datenschutz-und-compliance.md)
