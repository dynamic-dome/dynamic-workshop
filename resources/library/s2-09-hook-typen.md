---
id: S2.9
type: lesson
title: Hook-Typen und Hooks in Komponenten
shelf: hooks
level: deep-dive
minutes: 20
requires: [S2.8]
safety_floor: false
transferable: false
outcome: "Ich kann für eine Aufgabe den passenden der fünf Hook-Typen (command, http, prompt, agent, mcp_tool) wählen und einen Hook im Frontmatter eines Skills einbetten, dessen Lebensdauer ich kenne."
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
aliases: []
---

# S2.9 · Hook-Typen und Hooks in Komponenten

<!-- meta:start -->
> **Regal:** [Hooks](README.md#hooks) · **Stufe:** Vertiefung · **~15 Min** · **Voraussetzungen:** [S2.8 Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
>
> ← [S2.8 Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md) · [Bibliothek](README.md) · [S2.10 Hook-Ausgaben und das Secure Diff Gate](s2-10-hook-ausgaben.md) →
<!-- meta:end -->

## Schnellcheck

- Kannst du ohne Nachschlagen sagen, wann ein `prompt`-Hook statt eines `command`-Hooks sinnvoll ist?
- Kannst du sagen, wie lange ein Hook lebt, den du ins Frontmatter eines Skills schreibst?

## Auf einen Blick

Hooks führen nicht nur Shell-Befehle aus: Es gibt fünf Typen, nämlich `command`, `http`, `prompt`, `agent` und `mcp_tool`. Für feste Regeln bleibt `command` die beste Wahl. Außerdem müssen Hooks nicht in `settings.json` stehen. Im Frontmatter eines Skills oder Subagenten leben sie mit ihrer Komponente: Subagent-Hooks nur, solange der Subagent läuft, Skill-Hooks ab dem Aufruf des Skills bis zum Ende der Sitzung (`once: true` entfernt einen Handler nach seinem ersten erfolgreichen Lauf).

## Bild im Kopf

Ein Skill-Hook ist ein Sensor, den der Wachmann an die Wand schraubt, sobald er die Dienstanweisung aufschlägt: Er bleibt bis Schichtende scharf, auch bei Vorfällen, die mit der Anweisung nichts zu tun haben. Ist er so gebaut (`once: true`), baut er sich nach seinem ersten erfolgreichen Lauf selbst ab. Ein Subagent-Hook ist dagegen ein Sensor, den ein Wachmann auf der Streife am Gürtel trägt: Er kommt mit ihm zurück und ist dann weg.

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

- **`prompt` und `agent` fragen ein Modell.** Das kostet Tokens und Zeit, und das Urteil kann von Lauf zu Lauf anders ausfallen. Für feste Regeln wie Muster oder Pfade bleibt `command` die bessere Wahl. Agent-Hooks nennt die Doku ausdrücklich experimentell: Verhalten und Konfiguration können sich ändern.
- **`http` schickt die Ereignisdaten nach außen.** Die Hooks-Referenz beschreibt, dass ein `http`-Hook das JSON des Ereignisses als POST-Anfrage an die URL sendet. Tool-Eingaben verlassen damit deinen Rechner. Prüf vorher, was darin stehen kann ([S3.11](s3-11-datenschutz-und-compliance.md)).
- **`mcp_tool` braucht einen MCP-Server.** MCP verbindet Claude mit externen Diensten; wie du einen Server einrichtest, zeigen [S2.14](s2-14-mcp-stecker.md) und [S2.15](s2-15-mcp-einrichten.md). Für den Anfang genügt dir: `command` für feste Regeln, `prompt` für Urteile mit Kontext, die anderen bei Bedarf.

### Hooks in Komponenten: Skill- und Subagent-Frontmatter

Hooks müssen nicht in `settings.json` stehen. Du kannst sie auch **in das Frontmatter eines Skills oder Subagenten einbetten**, im selben verschachtelten Format wie in den Settings (Matcher-Gruppe → Liste `hooks` → Handler). Ein Subagent ist ein von Claude gestarteter Helfer mit eigener Aufgabe ([S3.3](s3-03-eigener-subagent.md)). Die beiden Komponenten unterscheiden sich darin, wie lange ihre Hooks leben:

- **Subagent-Hooks** laufen nur, solange dieser Subagent läuft, und werden entfernt, wenn er fertig ist.
- **Skill-Hooks** werden registriert, sobald der Skill aufgerufen wird, und **bleiben für den Rest der Sitzung aktiv**, auch in späteren Runden. Setz `once: true` an einen Handler, wenn er nach seinem ersten erfolgreichen Lauf entfernt werden soll. Das Feld wirkt nur im Frontmatter eines Skills; in Settings-Dateien wird es ignoriert.

So bringt ein Skill seine eigenen Vor- und Nachprüfungen mit, ohne die globalen Settings zu belasten. Das Beispiel verengt den Nach-Hook mit `if` auf den Deploy-Aufruf; ohne den Filter würde er beim ersten beliebigen Shell-Befehl nach `/deploy` feuern und sich dann entfernen:

<!-- cockpit:example -->
```yaml
---
name: deploy
description: Deploy the current branch to staging
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Bash|PowerShell"
      hooks:
        - type: command
          command: "./pre-deploy-check.sh"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          if: "Bash(./deploy.sh *)"
          command: "./post-deploy-notify.sh"
          once: true
---
```

`pre-deploy-check.sh` ist scharf, sobald `/deploy` läuft, und bleibt es bis zum Ende der Sitzung; `post-deploy-notify.sh` feuert nach dem Deploy-Aufruf einmal und wird dann entfernt. Einen globalen Hook in `settings.json` brauchst du dafür nicht, denn der Skill bringt seine Hooks selbst mit. Wie du die SKILL.md selbst schreibst, zeigt [S2.2](s2-02-skill-schreiben.md).

## Selbst machen

### Übung: ein Hook, der mit dem Skill kommt (etwa 10 Minuten)

**Ziel:** Du schreibst einen Hook in das Frontmatter eines Skills und siehst in einer Logdatei, dass er erst nach dem Aufruf registriert ist, danach in späteren Runden weiterläuft und in einer neuen Sitzung wieder fehlt.

**Startzustand:** ein neuer Ordner `~/cc-workshop/skill-hook` mit dem Skill-Ordner (`mkdir -p ~/cc-workshop/skill-hook/.claude/skills/tidy && cd ~/cc-workshop/skill-hook`, in PowerShell `New-Item -ItemType Directory -Force "$HOME\cc-workshop\skill-hook\.claude\skills\tidy"; Set-Location "$HOME\cc-workshop\skill-hook"`). Der Hook ist ein `echo` ohne `jq` und läuft in Git Bash und PowerShell gleich.

1. Leg `.claude/skills/tidy/SKILL.md` von Hand an (`.claude` ist ein geschützter Pfad):

   ```markdown
   ---
   name: tidy
   description: Starts a tidy-up session and watches shell commands.
   disable-model-invocation: true
   hooks:
     PreToolUse:
       - matcher: "Bash|PowerShell"
         hooks:
           - type: command
             command: "echo skill-hook >> \"${CLAUDE_PROJECT_DIR}/hook-log.txt\""
   ---

   Reply with the single word `ready` and nothing else.
   ```

2. Starte `claude --permission-mode default` und bestätige den Vertrauensdialog. Gib ein: `Run the shell command echo one.` Prüf in einem zweiten Terminal, ob die Datei `hook-log.txt` existiert (`ls`, in PowerShell `dir`). Erwartet: Es gibt sie nicht. Der Skill-Hook ist noch nicht registriert.
3. Gib `/tidy` ein. Erwartet: Claude antwortet `ready`. Gib dann `Run the shell command echo two.` ein und lies die Datei (`cat hook-log.txt`, in PowerShell `Get-Content hook-log.txt`). Erwartet: Jetzt gibt es mindestens eine Zeile `skill-hook`. Gib `/hooks` ein: Du siehst einen Eintrag unter PreToolUse, den es in Schritt 2 nicht gab. Schließ die Ansicht mit `Esc`.
4. Gib ein: `Run the shell command echo three.` Lies die Datei erneut. Erwartet: Es ist mindestens eine weitere Zeile dazugekommen. Der Hook läuft in späteren Runden weiter, auch wenn sie nichts mit dem Skill zu tun haben. (Führt Claude zusätzliche Shell-Befehle aus, stehen mehr Zeilen da; entscheidend ist der Unterschied zwischen vorher und nachher.)
5. Beende die Sitzung mit `/exit`, starte `claude --permission-mode default` neu und gib `Run the shell command echo four.` ein, ohne `/tidy`. Lies die Datei erneut. Erwartet: keine neue Zeile. Der Hook war nur für die vorige Sitzung registriert.

**Aufräumen:** Beende die Sitzung mit `/exit` und lösch den Ordner `~/cc-workshop/skill-hook` selbst.

**Geschafft, wenn:**

- [ ] vor `/tidy` keine `hook-log.txt` existierte
- [ ] nach `/tidy` und einem Shell-Befehl eine Zeile `skill-hook` in der Datei stand
- [ ] ein späterer Shell-Befehl eine weitere Zeile erzeugte
- [ ] in der neuen Sitzung vor `/tidy` keine neue Zeile entstand

## Typische Fallen

- **Der Skill-Hook läuft weiter.** Nach dem ersten Aufruf von `/deploy` bleibt `pre-deploy-check.sh` bis zum Sitzungsende scharf, auch bei Shell-Befehlen, die mit dem Deploy nichts zu tun haben. Soll ein Handler nur einmal laufen, setz `once: true` und verenge ihn mit `if`.
- **Typ und Ereignis verwechseln.** Der Typ sagt, *wie* ein Hook arbeitet (`command`, `http` …). Das Ereignis sagt, *wann* er feuert ([S2.7](s2-07-hook-ereignisse.md)).
- **Ein Modell-Urteil als feste Regel behandeln.** Ein `prompt`-Hook ist kein deterministischer Wächter. Was sicher geblockt werden muss, gehört in einen `command`-Hook mit `exit 2` ([S2.8](s2-08-hook-einrichten.md)).
- **`once: true` in `settings.json` setzen.** Dort wird das Feld ignoriert; es wirkt nur bei Hooks im Skill-Frontmatter.

## Check

Du kannst erklären, wann ein `prompt`-Hook besser passt als ein `command`-Hook, und zeigen, wie ein Hook im Frontmatter einen Skill mit eigener Vor- und Nachprüfung ausstattet, ohne die globale settings.json zu belasten.

1. Welcher Hook-Typ passt für eine feste Musterprüfung, welcher für ein Urteil, das Kontext braucht?
2. Wie lange lebt ein Hook im Skill-Frontmatter, wie lange einer im Subagent-Frontmatter?
3. Was bewirkt `once: true` an einem Handler, und wo wirkt es?

<details><summary>Auflösung</summary>

1. Für eine feste Musterprüfung `command`, für ein Urteil, das Kontext braucht, `prompt`. Der `prompt`-Hook fragt ein Modell, das kostet Tokens und Zeit, und das Urteil kann von Lauf zu Lauf abweichen.
2. Ein Skill-Hook wird beim Aufruf des Skills registriert und bleibt bis zum Ende der Sitzung. Ein Subagent-Hook läuft nur, solange der Subagent läuft, und wird danach entfernt.
3. Es entfernt den Handler nach seinem ersten erfolgreichen Lauf. Es wirkt nur bei Hooks im Frontmatter eines Skills; in Settings-Dateien wird es ignoriert.

</details>

<details><summary>Quizfrage</summary>

**Frage:** Eine Vorab-Prüfung soll nur dann scharf werden, wenn jemand `/deploy` aufruft, und nicht in jeder Sitzung. Wohin gehört der Hook?

- **Richtig:** In das Frontmatter des Deploy-Skills: Dort wird er erst beim Aufruf registriert und bleibt dann bis zum Sitzungsende.
- Falsch: In `~/.claude/settings.json` mit dem Matcher `/deploy`, denn der Matcher vergleicht den Namen des Skills, der gerade läuft.
- Falsch: In das Frontmatter eines Subagenten, denn nur dort leben Hooks genau so lange, wie der Skill aktiv ist.
- Falsch: In `.claude/settings.local.json`, denn diese Datei liest Claude Code erst, wenn du einen Slash-Befehl aufrufst.

</details>

## Weiterlesen

- [Hooks-Referenz](https://code.claude.com/docs/en/hooks)
- [Skills-Doku](https://code.claude.com/docs/en/skills)
- [Subagenten-Doku](https://code.claude.com/docs/en/sub-agents)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S2.2 · Eine SKILL.md schreiben](s2-02-skill-schreiben.md)
- [S3.3 · Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md)
- [S3.11 · Datenschutz, Aufbewahrung und regulierte Branchen](s3-11-datenschutz-und-compliance.md)
