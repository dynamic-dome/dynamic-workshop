# Einstufung zum Selbermachen

<!-- GENERIERT von tools/build_library.py — nicht von Hand ändern, Quelle: Kapitel und _*.yaml -->

Fünf Minuten, keine Noten. Diese Seite ist die einfache Fassung für alle, die lieber lesen; genauer rechnet das [Lern-Cockpit](../claude-code-workshop-ui.html) oder `/workshop start` in Claude Code.

## 1. Dein Ziel

Wähle ein Ziel und nimm den fertigen Pfad als Ausgangspunkt:

- **Meinen Entwickler-Alltag beschleunigen** → [Pfad](../paths/ziel-alltag.md)
- **Claude Code sicher im Team einführen** → [Pfad](../paths/ziel-team.md)
- **Aufgaben automatisieren und in CI einbauen** → [Pfad](../paths/ziel-automation.md)
- **Eigene Agenten-Systeme bauen** → [Pfad](../paths/ziel-agents.md)
- **Sicherheit und Compliance im Griff haben** → [Pfad](../paths/ziel-security.md)
- **Einschätzen, ob und wie wir es einsetzen (Tech Lead)** → [Pfad](../paths/ziel-einschaetzen.md)
- **Den Workshop selbst moderieren** → [Pfad](../paths/live-workshop.md)

Nur wenig Zeit insgesamt? Nimm den [Schnellstart](../paths/schnellstart.md).

## 2. Was du schon kannst

Lies je Bereich die Aussage. Trifft sie auf dich zu, kannst du die Kapitel dieses Bereichs mit dem Schnellcheck am Kapitelanfang überspringen — außer den 🛡-Kapiteln: die überfliegst du trotzdem.

### Grundlagen

> Ich habe Claude Code schon für eine echte Aufgabe genutzt und das Ergebnis selbst geprüft.

Kapitel: [S0.1 Werkstatt einrichten](s0-01-werkstatt-einrichten.md), [S1.1 Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md), [S1.2 Coding-Agent statt Chat: das Denkmodell](s1-02-agent-statt-chat.md), [S1.3 Die Oberflächen: CLI, Desktop, IDE, Web, iOS](s1-03-oberflaechen.md), [S1.4 Eingebaute Werkzeuge und ihre Namen](s1-04-werkzeuge.md)

### Rechte & Freigaben

> Ich weiß, welchen Rechte-Modus ich für ein fremdes Repo wähle, und habe allow/deny-Regeln gesetzt.

Kapitel: [S1.5 Rechte im Alltag: default und acceptEdits](s1-05-rechte-im-alltag.md) 🛡, [S1.6 Alle Rechte-Modi im Überblick](s1-06-rechte-modi.md) 🛡, [S3.8 Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md) 🛡, [S3.9 Geschützte Pfade und Sandbox-Stufen](s3-09-geschuetzte-pfade-und-sandbox.md) 🛡, [S3.10 Netzwerk und Skills härten](s3-10-netzwerk-und-skills-haerten.md)

### Kontext & Gedächtnis

> Ich pflege eine CLAUDE.md und weiß, wann ich /compact nehme und wann eine neue Session.

Kapitel: [S1.8 Das Kontextfenster verstehen](s1-08-kontextfenster.md), [S1.9 Kontext steuern mit /compact und /rewind](s1-09-kontext-steuern.md), [S1.10 CLAUDE.md: die Hausordnung des Projekts](s1-10-claude-md.md), [S1.11 Alle Gedächtnis-Ebenen im Überblick](s1-11-gedaechtnis-ebenen.md), [S1.12 Imports, --add-dir und AGENTS.md](s1-12-imports-und-agents-md.md)

### Aufträge formulieren

> Ich schreibe Aufträge mit Ziel, Grenzen und Prüfschritt und nutze den Plan-Modus.

Kapitel: [S1.13 Vager und präziser Auftrag im Vergleich](s1-13-vager-und-praeziser-auftrag.md), [S1.14 Plan-Modus und schrittweises Vorgehen](s1-14-plan-modus.md), [S1.15 Output Styles und Personas](s1-15-output-styles.md)

### Git & Worktrees

> Ich lasse Claude auf einem Branch arbeiten, prüfe den Diff selbst und nutze Worktrees.

Kapitel: [S1.16 Git in einem Fluss: Branch, Commit, PR](s1-16-git-in-einem-fluss.md), [S1.17 Git-Befehle in der Sitzung](s1-17-git-befehle.md), [S1.18 Worktrees als Testlabor](s1-18-worktrees.md), [S4.7 Isolation mit Docker und Worktrees](s4-07-isolation-docker-worktrees.md)

### Modelle & Kosten

> Ich lese /cost bzw. /usage und deckele autonome Läufe mit Budget und Rundenlimit.

Kapitel: [S1.7 Modellwahl und Effort](s1-07-modellwahl-und-effort.md), [S1.19 Kosten im Blick: /cost, /usage und Budgetgrenzen](s1-19-kosten-im-blick.md), [S4.1 Das richtige Modell pro Phase](s4-01-modell-pro-phase.md)

### Skills & Commands

> Ich habe einen eigenen Skill oder Slash-Command geschrieben und benutzt.

Kapitel: [S2.1 Skills sind Dienstanweisungen, Commands sind Knöpfe](s2-01-skills-und-commands.md), [S2.2 Eine SKILL.md schreiben](s2-02-skill-schreiben.md), [S2.3 Skills oder Commands, und wer sie auslösen darf](s2-03-wer-skills-ausloest.md), [S2.4 Mitgelieferte Skills](s2-04-mitgelieferte-skills.md), [S2.5 Lebendige Prompts: Argumente und dynamischer Inhalt](s2-05-lebendige-prompts.md)

### Hooks

> Ich habe einen Hook gebaut, der eine Aktion wirklich blockt.

Kapitel: [S2.6 Hooks als Sensoren: die drei Eckpfeiler](s2-06-hooks-als-sensoren.md), [S2.7 Die wichtigsten Hook-Ereignisse](s2-07-hook-ereignisse.md), [S2.8 Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md) 🛡, [S2.9 Hook-Typen und Hooks in Komponenten](s2-09-hook-typen.md), [S2.10 Hook-Ausgaben und das Secure Diff Gate](s2-10-hook-ausgaben.md)

### Plugins

> Ich habe Plugins geprüft, installiert oder selbst gebündelt.

Kapitel: [S2.11 Plugins: ein Bündel schnüren](s2-11-plugins-buendeln.md), [S2.12 Plugin-Lebenszyklus, Scopes und Marketplaces](s2-12-plugin-lebenszyklus.md), [S2.13 Lieferkettenrisiken bei Plugins](s2-13-plugin-lieferkette.md) 🛡

### MCP & Wissensquellen

> Ich habe einen MCP-Server angebunden und weiß, mit welchen Rechten er läuft.

Kapitel: [S2.14 MCP: der Integrationsstecker](s2-14-mcp-stecker.md), [S2.15 MCP einrichten: Transporte, Scopes, CLI](s2-15-mcp-einrichten.md), [S2.16 MCP im Detail: OAuth, Ausgabegrenzen, Protokoll](s2-16-mcp-im-detail.md), [S2.17 MCP-Sicherheit und ein eigener Server](s2-17-mcp-sicherheit.md) 🛡, [S2.18 RAG und NotebookLM: dem Agenten Baupläne geben](s2-18-rag-und-notebooklm.md), [S2.19 Grenzen von RAG und Datenschutz](s2-19-rag-grenzen.md)

### Agenten & Orchestrierung

> Ich habe Subagenten definiert oder mehrere Agenten parallel arbeiten lassen.

Kapitel: [S3.1 Was ist ein Agent? Spezialisierung statt Allrounder](s3-01-was-ist-ein-agent.md), [S3.2 Eingebaute Subagenten nutzen](s3-02-eingebaute-subagenten.md), [S3.3 Einen eigenen Subagenten definieren](s3-03-eigener-subagent.md), [S3.4 Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](s3-04-orchestrierungsmuster.md), [S3.5 Hintergrund-Sitzungen und Agent Teams](s3-05-hintergrund-und-teams.md), [S4.2 Codex-Schwarm und die Datenfluss-Grenze](s4-02-codex-schwarm.md)

### Gegenprüfung

> Ich lasse Agenten-Ergebnisse gezielt gegenprüfen, bevor ich sie übernehme.

Kapitel: [S3.6 Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md), [S3.7 Die eingebauten Reviews](s3-07-eingebaute-reviews.md), [S3.11 Datenschutz, Aufbewahrung und regulierte Branchen](s3-11-datenschutz-und-compliance.md)

### Automation & Headless

> Ich habe Claude Code zeitgesteuert oder headless (claude -p) laufen lassen.

Kapitel: [S3.12 Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](s3-12-zeitgesteuert-arbeiten.md), [S3.13 Autonome Loops absichern: Budget und Worktree](s3-13-autonome-loops-absichern.md) 🛡, [S3.14 Self-Improve-Loop: was geht und wo es endet](s3-14-self-improve-loop.md), [S4.3 Headless: claude -p als Pipeline-Stufe](s4-03-headless.md), [S4.4 CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](s4-04-ci-zugang-und-kosten.md) 🛡, [S4.5 CI-Pipelines bauen mit GitHub Actions und GitLab](s4-05-ci-pipelines.md), [S4.6 Unterwegs: Remote Control und /teleport](s4-06-remote-und-teleport.md)

### Fehlersuche

> Ich finde selbst heraus, warum ein Hook, Skill oder MCP-Server nicht greift.

Kapitel: [S4.9 Fehlersuche: /debug, --verbose, /doctor](s4-09-fehlersuche-werkzeuge.md), [S4.10 Diagnose Schritt für Schritt](s4-10-diagnose-schritt-fuer-schritt.md)

## 3. Mini-Szenarien (freiwillig)

Kein Test — nur ein Spiegel. Liegst du daneben, lohnt das genannte Kapitel, auch wenn du den Bereich oben als bekannt markiert hast.

**1. Dein Schutz-Hook bricht mit einem Syntaxfehler ab (Exit-Code 1). Was passiert mit dem Tool-Aufruf?**

a) Claude fragt dich, ob er trotzdem laufen soll
b) Die ganze Session bricht sofort mit einem Fehler ab
c) Er läuft weiter, nur eine Fehlermeldung erscheint
d) Er wird blockiert, bis du den Hook reparierst

<details><summary>Auflösung</summary>

Richtig ist c). Nur Exit-Code 2 blockt. Jeder andere Code meldet einen Fehler, und die Aktion läuft weiter — ein kaputter Schutz-Hook ist ein offener Schutz-Hook. Das verwechseln viele; Kapitel S2.8 zeigt es. Mehr in [S2.8 Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md).

</details>

**2. Du startest claude -p ohne --bare in einem frisch geklonten, fremden Repo. Was kann passieren?**

a) Claude verweigert den Start ohne Freigabe
b) Hooks und MCP-Server aus dem Repo laufen mit
c) Nichts, -p lädt keine Projekt-Dateien
d) Nur die CLAUDE.md wird gelesen, sonst nichts

<details><summary>Auflösung</summary>

Richtig ist b). Ohne --bare führt eine -p-Sitzung die Hooks aus .claude/settings.json aus und verbindet die Server aus .mcp.json — auch in einem Ordner, dem du nie vertraut hast. Kapitel S4.4 zeigt, wie CI das verhindert. Mehr in [S4.4 CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](s4-04-ci-zugang-und-kosten.md).

</details>

**3. Ein autonomer -p-Lauf soll weder zu teuer werden noch endlos laufen. Was setzt du?**

a) --max-budget-usd für Kosten, --max-turns für Runden
b) Effort auf low, dann reicht das Budget von allein
c) Ein kleineres Modell wählen, das begrenzt die Runden
d) Nur /cost beobachten und notfalls von Hand abbrechen

<details><summary>Auflösung</summary>

Richtig ist a). Budget und Rundenlimit sind zwei getrennte Grenzen; beide gelten nur im Print-Modus (-p). Beobachten allein hält einen Lauf nicht an. Kapitel S1.19 und S4.4 zeigen beide Flags. Mehr in [S1.19 Kosten im Blick: /cost, /usage und Budgetgrenzen](s1-19-kosten-im-blick.md).

</details>

**4. Du willst ein fremdes Repo erst verstehen, ohne dass etwas geändert wird. Womit startest du?**

a) Plan-Modus: lesen, planen, ändern erst nach Freigabe
b) acceptEdits, weil Git jede Änderung rückgängig macht
c) auto, weil der Klassifikator Gefährliches erkennt
d) bypassPermissions, damit keine Rückfragen mehr stören

<details><summary>Auflösung</summary>

Richtig ist a). Der Plan-Modus liest und plant, ändert aber nichts, bis du den Plan freigibst. Die anderen Modi erlauben Änderungen oder Befehle ohne Rückfrage. Kapitel S1.6 vergleicht alle Modi. Mehr in [S1.6 Alle Rechte-Modi im Überblick](s1-06-rechte-modi.md).

</details>

**5. Nach langer Session hält sich Claude nicht mehr an eine frühe Absprache. Was hilft am zuverlässigsten?**

a) Absprache in CLAUDE.md festhalten, dann neu starten
b) Die Absprache im Chat einfach mehrfach wiederholen
c) Effort auf max stellen, dann merkt es sich mehr
d) Einfach weitermachen, das korrigiert sich von selbst

<details><summary>Auflösung</summary>

Richtig ist a). Frühe Absprachen können beim Komprimieren verloren gehen. Was in CLAUDE.md steht, wird bei jedem Start geladen. Kapitel S1.10 zeigt, was hineingehört. Mehr in [S1.10 CLAUDE.md: die Hausordnung des Projekts](s1-10-claude-md.md).

</details>

**6. Ein Subagent meldet „alle 40 Tests grün". Was tust du, bevor du das übernimmst?**

a) Die Tests selbst laufen lassen und die Ausgabe lesen
b) Die Zahl direkt in die Commit-Nachricht übernehmen
c) Einen zweiten Subagenten fragen, ob es wirklich stimmt
d) Nichts, Subagenten berichten grundsätzlich korrekt

<details><summary>Auflösung</summary>

Richtig ist a). Ein grüner Bericht ist kein Beweis, ausgeführter Code ist einer. Auch ein zweiter Agent liefert nur einen weiteren Bericht. Kapitel S3.6 baut daraus eine Prüf-Pipeline. Mehr in [S3.6 Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md).

</details>
