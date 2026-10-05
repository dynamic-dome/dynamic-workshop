# Vorführen: S2.11 · Plugins: ein Bündel schnüren

> Demo und Hinweise für Moderierende zum Kapitel [S2.11 · Plugins: ein Bündel schnüren](../../library/s2-11-plugins-buendeln.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Anatomie eines Plugins

**Ziel:** Zeigen, dass ein Plugin nur ein Verzeichnis mit gut strukturierten Dateien ist. Keine Magie, nichts kompiliert, alles lesbar und änderbar.

Zeig die Übung aus dem Kapitel live: die Übung „ein Mini-Plugin bauen und laden“ in [S2.11](../../library/s2-11-plugins-buendeln.md). Startzustand wie dort: der leere Ordner `~/cc-workshop/plugin`. Du kannst die drei Dateien (Schritt 2) vorher anlegen, dann zeigst du sie im Editor, statt zu tippen. Nichts davon wird installiert, und deine Konfiguration bleibt unberührt.

**Ablauf:** Schritte 3 bis 6 der Übung: `claude plugin validate ./greeter-src` und `plugin details greeter`, die Sitzung mit `--plugin-dir`, `/greeter:hello`, die Änderung auf `GREETER-V2` mit `/reload-plugins` und zum Schluss die Sitzung ohne das Flag, in der der Skill fehlt.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 bis 10 Minuten.

**Sagen:**

- Vor Schritt 3, an den Dateien: „Das Typenschild ist `plugin.json`: Name, Version, Beschreibung. Was eingebaut ist, siehst du an den Ordnern daneben, `skills/` und `agents/`. Das Manifest liegt unter `.claude-plugin/`, alles andere direkt im Plugin-Ordner."
- Schritt 3: „`plugin details` zeigt, was das Plugin mitbringt, ohne eine Sitzung zu öffnen." Zeig den Abschnitt `Component inventory` mit dem Skill `hello` und dem Agent `haiku-writer`. Die Komponenten stehen nicht im Manifest: Claude Code findet sie über die Ordner.
- Schritt 4: „Skills eines Plugins tragen den Plugin-Namen als Präfix, `/greeter:hello`. So können zwei Plugins jeweils einen Skill `hello` haben, ohne zu kollidieren."
- Schritt 5: „Ich ändere die Datei bei laufender Sitzung und lade neu." Nach `/reload-plugins` endet die Antwort mit `GREETER-V2`.
- Schritt 6: „Das Plugin gilt nur für die Sitzungen, in denen ich `--plugin-dir` angebe. Es ist nichts installiert."
- „Ein Plugin ist ein in sich geschlossenes Modul: Skills, Agents, Hooks und weitere Komponenten in einem Paket. Es sind nur Dateien. Du kannst jede Zeile lesen und jede Anweisung ändern."
- „Ein installiertes Plugin schaltest du mit `claude plugin disable <name>` ab, statt Dateien umzubenennen. Es gibt kein Feld `enabled` im Manifest."
- Installierte Plugins legt Claude Code als Kopie unter `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` ab; dort kannst du jede Datei eines fremden Plugins lesen. Wie du Plugins installierst, zeigt [S2.12](../../library/s2-12-plugin-lebenszyklus.md), worauf du bei fremden achtest, [S2.13](../../library/s2-13-plugin-lieferkette.md).

**Wenn `validate` etwas bemängelt:** Meist liegt eine Datei am falschen Ort, oder `author` ist ein einfacher Text statt eines Objekts mit `name`.

**Wenn `/greeter:hello` unbekannt ist:** Die Sitzung wurde ohne `--plugin-dir ./greeter-src` gestartet.

**Wenn das Manifest im Plugin-Ordner statt unter `.claude-plugin/` liegt:** Das Manifest ist optional; Claude Code lädt die Komponenten trotzdem, nimmt den Plugin-Namen aber vom Ordner (`greeter-src@inline` statt `greeter@inline`). Das ist die Extra-Übung des Kapitels.

</details>
