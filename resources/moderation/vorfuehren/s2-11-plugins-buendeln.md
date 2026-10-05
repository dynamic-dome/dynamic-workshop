# Vorführen: S2.11 · Plugins: ein Bündel schnüren

> Demo und Hinweise für Moderierende zum Kapitel [S2.11 · Plugins: ein Bündel schnüren](../../library/s2-11-plugins-buendeln.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Anatomie eines Plugins (etwa 5 Minuten)

**Ziel:** Zeigen, dass ein Plugin nur ein Verzeichnis mit gut strukturierten Dateien ist. Keine Magie, nichts kompiliert, alles lesbar und änderbar.

**Vorbereitung**

- Den Pfad `~/.claude/plugins/cache/` kennen
- Mindestens ein Plugin installiert haben (ideal ist 🔧 agentic-os, eine eigene Erweiterung, siehe [S2.13](../../library/s2-13-plugin-lieferkette.md))

**Schritt 1: installierte Plugins auflisten**

```bash
ls ~/.claude/plugins/cache/
```

Zeig die Liste. Die Ordner auf der obersten Ebene sind die Marketplaces. Darunter liegt je Plugin ein Ordner und darin je installierter Version einer: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Sag: „Jeder Plugin-Ordner hier ist ein Plugin. Machen wir eins auf."

**Schritt 2: die Struktur erkunden**

```bash
ls ~/.claude/plugins/cache/agentic-os-marketplace/agentic-os/
# Expected: one folder per installed version

cd ~/.claude/plugins/cache/agentic-os-marketplace/agentic-os/<version>/
ls -a
# Expected: .claude-plugin/  skills/  commands/  agents/  hooks/ (varies)

cat .claude-plugin/plugin.json
```

Geh das Manifest durch:

- `name`, `version`, `description`
- Welche Skills, Commands und Agents das Plugin mitbringt, steht meist **nicht** im Manifest. Claude Code findet sie über die Ordner `skills/`, `commands/` und `agents/`.
- Ein Feld zum Abschalten gibt es nicht. Abgeschaltet wird mit `claude plugin disable <name>`.

Sag: „Das ist das Typenschild des Moduls: Name, Version, Beschreibung. Was eingebaut ist, siehst du an den Ordnern daneben."

**Schritt 3: einen Skill und einen Agent lesen**

```bash
ls skills/
cat skills/wrap-up/SKILL.md | head -30
```

Zeig das YAML-Frontmatter und den Markdown-Teil darunter.

```bash
ls agents/
cat agents/<agent>.md | head -20
```

Sag: „Agents sind wie spezialisierte Teammitglieder: Jeder hat eine Rolle, Zuständigkeiten und eine Anleitung, wie er arbeitet."

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 Minuten (Schritt 1: 1 Min., Schritt 2: 2 Min., Schritt 3: 2 Min.).

**Sagen:**

- „Ein Plugin ist ein in sich geschlossenes Sicherheitsmodul: Sensoren (Hooks), Verfahren (Skills), Teamrollen (Agents) und Bedientasten (Commands) in einem Paket."
- „Es sind nur Dateien. Du kannst jede Zeile lesen, jede Anweisung ändern und es für die Abläufe deines Teams forken."
- „Einmal installieren, und es ist in jedem deiner Projekte da. Updates kommen über den Marketplace, mit `claude plugin update` oder automatisch."
- „Abschalten, ohne zu löschen: `claude plugin disable <name>`."
- „Euer Team kann Plugins für eure eigenen Abläufe bauen und intern verteilen."

**Wenn agentic-os nicht installiert ist:** Jedes installierte Plugin geht. `claude plugin list` zeigt, welche da sind; dann `cat ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/.claude-plugin/plugin.json`.

**Wenn du den Pfad nicht findest:** `claude plugin list --json` nennt für jedes Plugin `installPath`, das Verzeichnis, aus dem es lädt. `claude plugin details <name>` listet die Komponenten eines Plugins, ohne dass du Ordner durchsuchen musst.

**Wenn gar kein Plugin installiert ist:** Zeig das Kurs-Repo selbst, es ist ein Plugin: `.claude-plugin/plugin.json`, `skills/`, `agents/`.

**Wenn ein Plugin kein `.claude-plugin/plugin.json` hat:** Das ist erlaubt, das Manifest ist optional. Die Komponenten liegen trotzdem in den üblichen Ordnern.

</details>
