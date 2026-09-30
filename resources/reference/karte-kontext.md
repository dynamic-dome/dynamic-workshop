# Karte: Kontext und Gedächtnis

Wofür: was gerade im Kontext steckt, wann du verdichtest, leerst oder neu anfängst und welche Anweisung in welche Datei gehört.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/memory · https://code.claude.com/docs/en/context-window

## Erst nachsehen: `/context`

- `/context` zeigt die Belegung des Kontextfensters als Raster, nach Kategorien, mit Spartipps; `/context all` klappt die Einzelposten auf.
- Unter **Memory files** steht, welche `CLAUDE.md`- und Regeldateien wirklich geladen sind. Fehlt eine dort, kennt Claude sie nicht.
- Belegt, bevor du etwas tippst: `CLAUDE.md`, Auto-Memory, die Namen der MCP-Tools und die Beschreibungen der Skills.

## Verdichten, leeren oder neu anfangen?

| Lage | Griff | Was passiert |
|---|---|---|
| Gleiche Aufgabe, der Kontext wird voll | `/compact <Fokus>` | Eine Zusammenfassung ersetzt den Verlauf; der Fokus bestimmt, was bleibt |
| Nur einen Teil verdichten | `/rewind` oder `Esc` `Esc`, Nachricht wählen, „Summarize from here" bzw. „Summarize up to here" | Der andere Teil bleibt wörtlich stehen |
| Neue Aufgabe ohne Bezug zur alten | `/clear` (Aliase `/reset`, `/new`) | Leerer Kontext; die alte Unterhaltung holst du mit `/resume` zurück |
| Zweimal erfolglos korrigiert | `/clear` und ein besserer erster Prompt | Die Fehlversuche stehen sonst weiter im Kontext |
| Spec steht, jetzt wird gebaut | neue Sitzung | Frischer Kontext nur für die Umsetzung; die Spec liegt als Datei vor |
| Kurze Nebenfrage | `/btw <Frage>` | Die Antwort kommt nicht in den Verlauf; `/btw` hat keine Tools |
| Recherche über viele Dateien | Subagent | Die Dateiinhalte bleiben in seinem Kontextfenster, zu dir kommt die Zusammenfassung |

Kurz vor der Grenze verdichtet Claude Code von selbst. Wie voll der Kontext dafür werden darf, stellst du mit `/autocompact` ein, etwa `/autocompact 500k`.

## Was `/compact` übersteht

| Kommt von der Platte zurück | Kommt erst wieder, wenn Claude passende Dateien liest | Steht danach nur noch in der Zusammenfassung |
|---|---|---|
| `CLAUDE.md` im Projekt-Root, Regeln ohne `paths`, Auto-Memory, der Plan aus dem Plan-Modus | Regeln mit `paths:`, `CLAUDE.md` in Unterordnern | Anweisungen, die du nur im Chat gegeben hast |

Aufgerufene Skills kommen gekürzt zurück: höchstens 5.000 Tokens je Skill und 25.000 insgesamt, die ältesten fallen zuerst weg. Was dauerhaft gelten soll, gehört in `CLAUDE.md`, nicht in den Chat.

## Welche Anweisung gehört wohin?

| Datei | Gilt für | Wird geladen | Typischer Inhalt |
|---|---|---|---|
| `~/.claude/CLAUDE.md`, `~/.claude/rules/` | dich, alle Projekte | beim Start | deine Arbeitsweise |
| `./CLAUDE.md` oder `./.claude/CLAUDE.md` | das Team (eingecheckt) | beim Start, auch aus den Ordnern darüber; aus Unterordnern erst, wenn Claude dort liest | Build-Befehle, Konventionen, Stolpersteine |
| `./CLAUDE.local.md` | nur dich, dieses Projekt | beim Start, nach der `CLAUDE.md` derselben Ebene | Sandbox-URLs, eigene Testdaten; gehört in `.gitignore` |
| `.claude/rules/*.md` ohne `paths` | das Team | beim Start, wie `.claude/CLAUDE.md` | ein Thema je Datei |
| `.claude/rules/*.md` mit `paths:` | das Team | erst, wenn Claude eine passende Datei liest | Regeln für einen Teil des Codes |
| `AGENTS.md` | alle Coding-Agenten im Repo | im Standard nur ohne `CLAUDE.md` (siehe unten) | gemeinsame Regeln mit Codex und anderen Agenten |
| Auto-Memory | nur dich, nur diese Maschine | Anfang von `MEMORY.md` | Claudes eigene Notizen |

Faustregeln der Doku: jede `CLAUDE.md` unter 200 Zeilen. Was nur für einen Teil des Codes gilt, wird eine `paths`-Regel; ein mehrstufiger Ablauf wird ein Skill; was garantiert passieren muss, wird ein Hook. `@path`-Imports ordnen eine lange Datei, sparen aber keinen Kontext: Auch importierte Dateien laden beim Start.

## `AGENTS.md` neben `CLAUDE.md`

- Ab CLI 2.1.277 liest Claude Code `AGENTS.md` selbst, im Standard (`claude-md-or-agents-md`) aber nur, wenn im Arbeitsordner und darüber keine `CLAUDE.md`, `.claude/CLAUDE.md` oder `CLAUDE.local.md` liegt. `~/.claude/CLAUDE.md` und `.claude/rules/` zählen dabei nicht.
- Falle: Legst du in einem `AGENTS.md`-Projekt eine `CLAUDE.local.md` an, liest Claude die `AGENTS.md` nicht mehr.
- Beides laden: `@AGENTS.md` in die `CLAUDE.md` schreiben oder in `/config` **Project instructions** auf `claude-md-and-agents-md` stellen. Prüfen: `/memory` listet die gelesene `AGENTS.md`.

## Auto-Memory-Drift

- Auto-Memory ist standardmäßig an. Die Notizen liegen in `~/.claude/projects/<project>/memory/`; `<project>` leitet sich vom Git-Repo ab, alle Worktrees eines Repos teilen sich einen Ordner. Auf Windows wird aus `C:\Users\...\Desktop\projekt` der Ordner `C--Users-...-Desktop-projekt`.
- Geladen werden nur die ersten 200 Zeilen oder 25 KB von `MEMORY.md`; die Themendateien liest Claude bei Bedarf.
- Notizen können falsch sein oder veralten und widersprechen dann dem heutigen Code oder deiner `CLAUDE.md`. Das Frontmatter-Feld `modified` zeigt, wann Claude eine Notiz zuletzt geschrieben hat.
- Aufräumen: `/memory` öffnet den Memory-Ordner; die Dateien sind Markdown, du darfst sie ändern oder löschen. Oder du sagst Claude: „Vergiss, dass X, ich meinte Y".
- Abschalten: Schalter in `/memory` (schreibt `autoMemoryEnabled` in `~/.claude/settings.json`), für ein Projekt `"autoMemoryEnabled": false` in dessen Settings, oder `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. `--bare` ist kein Memory-Schalter: Es überspringt für diesen einen Aufruf die automatische Erkennung von fast allem, auch von `CLAUDE.md`, Hooks, Skills und MCP-Servern.

## Typische Fallen

- „Claude ignoriert meine `CLAUDE.md`": zuerst `/context`. Steht die Datei unter Memory files, liegt es an vagen oder widersprüchlichen Anweisungen. `CLAUDE.md` kommt als Nutzernachricht nach dem Systemprompt an, nicht als harte Regel; was garantiert passieren muss, gehört in einen Hook oder eine Rechte-Regel.
- Eine `CLAUDE.md` im Unterordner lädt erst, wenn Claude dort eine Datei mit dem Read-Tool liest, nicht beim Start und nicht beim Schreiben.
- `claudeMdExcludes` in den Settings blendet Dateien aus. Ein `InstructionsLoaded`-Hook protokolliert, welche Datei wann und warum geladen wurde; für eine direkt gelesene `AGENTS.md` feuert er nicht.
- Zu lange Datei: Claude Code warnt beim Start und in `/status`, `/doctor` schlägt Kürzungen vor.
- `CLAUDE.local.md` ist gitignoriert und existiert deshalb nur in dem Worktree, in dem du sie angelegt hast.

## Mehr dazu

- [S1.8 · Das Kontextfenster verstehen](../library/s1-08-kontextfenster.md) · [S1.9 · Kontext steuern mit /compact und /rewind](../library/s1-09-kontext-steuern.md)
- [S1.10 · CLAUDE.md: die Hausordnung des Projekts](../library/s1-10-claude-md.md) · [S1.11 · Alle Gedächtnis-Ebenen im Überblick](../library/s1-11-gedaechtnis-ebenen.md)
- [S1.12 · Imports, --add-dir und AGENTS.md](../library/s1-12-imports-und-agents-md.md) · [S4.9 · Fehlersuche: /debug, --verbose, /doctor](../library/s4-09-fehlersuche-werkzeuge.md)
