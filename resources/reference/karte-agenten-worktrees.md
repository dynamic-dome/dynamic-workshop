# Karte: Subagenten, Hintergrund und Worktrees

Wofür: wie du Arbeit an Subagenten und Hintergrund-Sitzungen abgibst, welches Muster wann passt und wie Worktrees ihre Änderungen trennen.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/worktrees

## Subagent-Datei: die Alltagsfelder

Ablage: `.claude/agents/<name>.md` (Projekt), `~/.claude/agents/` (du), `agents/` im Plugin, für eine Sitzung `claude --agents '<json>'`. Gleicher Name: Managed vor `--agents` vor Projekt vor persönlich vor Plugin. Pflicht sind nur `name` und `description`.

| Feld | Beispiel | Wirkung | Falle |
|---|---|---|---|
| `name` | `code-reviewer` | Kennung | Ein `:` im Namen, und die Datei lädt nicht |
| `description` | `"Use when …"` | Wann Claude delegiert | |
| `tools` | `Read, Grep, Bash` | Allowlist | Komma-Liste oder YAML-Liste. `allowed_tools` oder `allowed-tools` ignoriert Claude Code, dann erbt der Subagent alle Tools. Löst kein Eintrag auf, startet er in der Regel nicht |
| `disallowedTools` | `Write, Edit` | Denylist | `Bash(git push *)` entfernt die ganze Bash; einzelne Befehle sperrt eine deny-Regel in den Settings |
| `model` | `haiku` | Alias, volle Modell-ID oder `inherit` | Welche IDs es gibt, steht im [Kanon](../_canonical.md) |
| `permissionMode` | `acceptEdits` | Rechte-Modus des Subagenten | Plugin-Subagenten ignorieren ihn, ebenso `hooks` und `mcpServers` |
| `maxTurns` | `5` | Rundengrenze | Danach kommt die Ausgabe als unvollständig markiert zurück |
| `skills` | `[test-driven]` | Lädt den ganzen Skill-Inhalt beim Start | |
| `isolation` | `worktree` | Eigener temporärer Worktree | Zweigt vom Default-Branch ab, nicht von deinem `HEAD` (siehe unten) |
| `background` | `true` | Bleibt im Hintergrund | |

Mehrteilige Feldnamen schreibst du in camelCase (`maxTurns`, `disallowedTools`); ein unbekanntes Feld ignoriert Claude Code ohne Meldung.

## Muster: welches wann?

| Muster | So sieht es aus | Nimm es, wenn | Achte auf |
|---|---|---|---|
| Fan-out/Fan-in | mehrere Subagenten parallel, Claude führt die Ergebnisse zusammen | die Teile unabhängig sind | Jedes Ergebnis landet in deinem Kontext, jeder Subagent verbraucht eigene Tokens |
| Pipeline | Subagenten nacheinander, Claude reicht weiter | jeder Schritt den vorigen braucht | Der nächste Subagent sieht nur, was Claude ihm weitergibt |
| Hierarchie | ein Subagent startet eigene Subagenten | eine Teilaufgabe wieder in parallele Teile zerfällt | Standard sind bis zu drei Ebenen unter der Hauptunterhaltung (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `1` schaltet es ab); auf der letzten Ebene fehlt das `Agent`-Tool |
| Agent Teams | mehrere Sitzungen mit gemeinsamer Aufgabenliste, die sich direkt schreiben | Teammitglieder ihre Befunde gegenseitig prüfen sollen | experimentell, erst mit `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; deutlich mehr Tokens |

Bleib in der Hauptunterhaltung bei viel Hin und Her, bei Phasen mit viel gemeinsamem Kontext und bei kleinen, gezielten Änderungen. Standardmäßig laufen höchstens 20 Subagenten gleichzeitig (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).

## Hintergrund

| Du willst … | Griff |
|---|---|
| einen laufenden Subagenten weglegen | `Ctrl+B`; dauerhaft mit `background: true` |
| die ganze Sitzung abgeben | `/background` (`/bg`) oder `claude --bg "<prompt>"`, nicht zusammen mit `-p` |
| Hintergrund-Sitzungen verwalten | `claude agents`, `claude attach <id>`, `claude logs <id>`, `claude stop <id>`, `claude respawn <id>`, `claude rm <id>` |
| sehen, was in dieser Sitzung läuft | `/tasks` |

Hintergrund-Subagenten haben weniger eingebaute Tools als Vordergrund-Subagenten. Ihre Rechteabfragen erscheinen in deiner Hauptsitzung; eine Freigabe, die länger als einen Aufruf gilt, gilt dann für die ganze Sitzung, auch für dich. In einem Git-Repo zieht eine Hintergrund-Sitzung vor dem ersten Edit in einen eigenen Worktree unter `.claude/worktrees/`.

## Worktrees

```bash
git worktree add ../exp feature/x
claude --worktree feature/x
# worktree.baseRef: "fresh" | "head"
```

`git worktree add` legt den Ordner an, wo du willst, auf dem Branch, den du nennst. `claude --worktree <name>` legt `.claude/worktrees/<name>/` mit dem neuen Branch `worktree-<name>` an und startet Claude darin; `.claude/worktrees/` gehört in `.gitignore`.

## Die `worktree.baseRef`-Falle

| Wert | Neuer Worktree zweigt ab von | Folge |
|---|---|---|
| `"fresh"` (Standard) | `origin/<default-branch>` | Deine ungepushten Commits und dein Feature-Branch fehlen, bei `--worktree`, bei `EnterWorktree` und bei Subagenten mit `isolation: worktree` |
| `"head"` | deinem lokalen `HEAD` | Der Worktree trägt deinen Zwischenstand |

- Einen Branch-Namen kannst du nicht eintragen; für einen bestimmten Branch nimm `git worktree add`.
- Ein Flag `--worktree-base-ref` gibt es nicht. Für einen einzelnen Aufruf: `claude --settings '{"worktree":{"baseRef":"head"}}' --worktree <name>`.
- Ohne Remote, oder wenn `origin/HEAD` weder lokal vorliegt noch abrufbar ist, fällt `"fresh"` auf deinen lokalen `HEAD` zurück.
- Der Standard war nicht immer `"fresh"` (Changelog 2.1.133). Laufen auf euren Rechnern verschiedene CLI-Versionen, setz den Wert ausdrücklich.
- Gitignorierte Dateien wie `.env` fehlen im neuen Worktree; eine `.worktreeinclude` im Projekt-Root kopiert sie mit.
- `-p`-Läufe räumen ihre Worktrees nicht auf: `git worktree remove`, bei einer Sperre vorher `git worktree unlock`.

## Mehr dazu

- [S1.18 · Worktrees als Testlabor](../library/s1-18-worktrees.md) · [S4.7 · Isolation mit Docker und Worktrees](../library/s4-07-isolation-docker-worktrees.md) · [S3.13 · Autonome Loops absichern: Budget und Worktree](../library/s3-13-autonome-loops-absichern.md)
- [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](../library/s3-01-was-ist-ein-agent.md) · [S3.2 · Eingebaute Subagenten nutzen](../library/s3-02-eingebaute-subagenten.md) · [S3.3 · Einen eigenen Subagenten definieren](../library/s3-03-eigener-subagent.md)
- [S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](../library/s3-04-orchestrierungsmuster.md) · [S3.5 · Hintergrund-Sitzungen und Agent Teams](../library/s3-05-hintergrund-und-teams.md) · [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](../library/s3-06-devils-advocate.md)
