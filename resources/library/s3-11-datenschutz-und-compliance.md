---
id: S3.11
type: lesson
title: Datenschutz, Aufbewahrung und regulierte Branchen
shelf: security
level: deep-dive
minutes: 15
requires: [S3.9]
safety_floor: false
transferable: true
outcome: "Ich kann die Aufbewahrungsstufen der Claude-Pläne benennen, für eine regulierte Branche passende Kontrollen aus dem Kurs zuordnen und einen PreToolUse-Hook einsetzen, der sensible Muster in Datei-Schreibzugriffen blockt."
sources:
  - https://code.claude.com/docs/en/data-usage
  - https://code.claude.com/docs/en/zero-data-retention
  - https://code.claude.com/docs/en/memory
  - https://code.claude.com/docs/en/hooks
aliases: []
---

# S3.11 · Datenschutz, Aufbewahrung und regulierte Branchen

<!-- meta:start -->
> **Regal:** [Gegenprüfung & Compliance](README.md#security) · **Stufe:** Vertiefung · **~15 Min** · **Voraussetzungen:** [S3.9 Geschützte Pfade und Sandbox-Stufen](s3-09-geschuetzte-pfade-und-sandbox.md)
>
> ← [S3.10 Netzwerk und Skills härten](s3-10-netzwerk-und-skills-haerten.md) · [Bibliothek](README.md) · [S3.12 Zeitgesteuert arbeiten: /loop, /goal, /schedule, Routinen](s3-12-zeitgesteuert-arbeiten.md) →
<!-- meta:end -->

## Schnellcheck

- Hast du schon geprüft, welche Trainings- und Aufbewahrungsregeln für deinen Claude-Plan gelten und ob Zero Data Retention (ZDR) für euch in Frage kommt?
- Kannst du ohne Nachschlagen einen PreToolUse-Hook skizzieren, der sensible Muster in Datei-Schreibzugriffen blockt?

## Auf einen Blick

Wie lange Anthropic deine Prompts und Antworten aufbewahrt und ob damit trainiert wird, hängt vom Plan ab: bei Free, Pro und Max je nach deiner Einstellung 5 Jahre oder 30 Tage, bei Team, Enterprise und API 30 Tage ohne Training, mit Zero Data Retention (ZDR, nur für geprüfte Enterprise-Organisationen) keine Speicherung nach der Antwort. In regulierten Umgebungen kommen Kontrollen aus dem Kurs dazu: Auto-Memory aus, Freigabe-Gates in jeder Automation, ein Hook gegen sensible Daten und eine Allowlist für ausgehende Anfragen.

Die Muster hier sind Vorlagen, keine Rechtsberatung. Wie EN 50131, DSGVO oder NIS2 für dein Unternehmen auszulegen sind, entscheidet dein Compliance-Team.

## Bild im Kopf

Das ist wie die Aufbewahrungsrichtlinie für Videoaufnahmen. Der Consumer-Plan ist ein 30-Tage-Ringspeicher mit Opt-in-Archiv, und wer das Archiv erlaubt, erlaubt dem Hersteller auch, die Aufnahmen zur Produktverbesserung zu nutzen. Enterprise ist derselbe 30-Tage-Ringspeicher, aber ohne Weitergabe. ZDR sind Kameras, die laufen, aber nichts aufzeichnen: maximaler Datenschutz, dafür fällt die Wiedergabe weg.

## Im Detail

### Aufbewahrung und Training je Plan

| Plan | Training mit deinen Daten? | Aufbewahrung | Hinweis |
|---|---|---|---|
| **Free, Pro, Max** | nur, wenn du es erlaubst | erlaubt: 5 Jahre; nicht erlaubt: 30 Tage | Consumer-Pläne; die Einstellung änderst du jederzeit unter claude.ai/settings/data-privacy-controls |
| **Team, Enterprise, API** | nein (Standard) | 30 Tage | kommerzielle Pläne |
| **Enterprise mit ZDR** | nein | keine Speicherung nach der Antwort | nur für geprüfte Organisationen; einige Funktionen sind abgeschaltet |

ZDR ist nicht im normalen Enterprise-Plan enthalten und lässt sich nicht in den Admin-Einstellungen einschalten. Anthropic prüft die Berechtigung und schaltet ZDR je Organisation frei. Auch mit ZDR darf Anthropic Daten aufbewahren, wo das Gesetz es verlangt oder um Missbrauch zu bekämpfen. Weil nichts gespeichert wird, sind Funktionen abgeschaltet, die gespeicherte Sitzungsdaten brauchen, darunter Cloud-Sitzungen, Remote Control und `/feedback`. ZDR gilt nur für die direkte Anthropic-Plattform; bei Amazon Bedrock, Google Cloud oder Microsoft Foundry gelten deren Regeln.

### Verschlüsselung: unterwegs, beim Anbieter, auf deinem Rechner

Prompts und Antworten gehen per TLS 1.2 oder neuer verschlüsselt an den Anbieter. Wie sie dort gespeichert sind, hängt vom Anbieter ab: Die Anthropic-API verschlüsselt ihre Datenträger mit AES-256, Bedrock nutzt AES-256 mit von AWS verwalteten Schlüsseln (eigene Schlüssel über AWS KMS), Google Cloud von Google verwaltete Schlüssel (eigene über CMEK), bei Foundry hängt es von der Hosting-Variante ab.

Auf deinem Rechner speichert Claude Code die Sitzungsprotokolle im Klartext unter `~/.claude/projects/`, standardmäßig 30 Tage lang, damit du Sitzungen fortsetzen kannst. Die Dauer stellst du mit `cleanupPeriodDays` ein. Personendaten, die in einer Sitzung auftauchen, liegen also auch lokal.

### Telemetrie abschalten

Claude Code sendet, je nach Anbieter und Anmeldung, Nutzungsmetriken und Fehlerberichte. Die Metriken enthalten laut Doku nie deinen Code, deine Prompts oder Dateipfade. Abschalten kannst du beides getrennt:

```bash
export DISABLE_TELEMETRY=1           # No operational metrics (Statsig)   — macOS/Linux/Git Bash
export DISABLE_ERROR_REPORTING=1     # No error logging (Sentry)
```

```powershell
$env:DISABLE_TELEMETRY = "1"         # Windows PowerShell (session); persist with setx
$env:DISABLE_ERROR_REPORTING = "1"
```

Telemetrie abzuschalten ändert nichts daran, ob mit deinen Gesprächen trainiert wird; das regeln Plan und Datenschutzeinstellung oben.

### Regulierte Branchen: welche Kontrolle wofür

Branchen und Rechtsräume regeln unterschiedlich, was du automatisieren darfst. Für den Blick aus der physischen Sicherheit sind **EN 50131/50132, DSGVO und NIS2** der Kern. HIPAA, PCI-DSS, DORA und MiFID II stehen als Transferbeispiele in der Tabelle: Dieselben Schutzmechanismen lassen sich übertragen, sie sind aber nicht das Hauptziel.

| Branche / Region | Regelwerk | Was das für Claude Code heißt |
|---|---|---|
| **EU, physische Sicherheit** | EN 50131 (Einbruchmeldeanlagen), EN 50132 (Videoüberwachung) | Autonome Firmware-Updates an Alarm- und Zutrittscontrollern sind nicht zulässig: Freigabe-Gate und Audit-Trail sind Pflicht. Drift der Auto-Memory bei Firmware-Code vermeiden ([S4.10](s4-10-diagnose-schritt-fuer-schritt.md)). |
| **EU allgemein** | DSGVO | Personendaten in Zutrittsprotokollen oder Video-Metadaten: Auto-Memory kann sie in Prompts ziehen, also für sensible Sitzungen abschalten (Grundsatz 1). ZDR (Enterprise) für produktive Datenflüsse. Anthropic im Vertrag zur Auftragsverarbeitung als Auftragsverarbeiter nennen. |
| **US, Gesundheit** | HIPAA | Gesundheitsdaten (PHI) dürfen deine Kontrolle nicht verlassen. ZDR dringend empfohlen; für produktive PHI ist ein Business Associate Agreement (BAA) mit Anthropic nötig. Siehe die Übung unten. |
| **US, Finanzen** | PCI-DSS | Kartendaten in Test-Fixtures oder Logs per PreToolUse-Hook blocken (dasselbe Muster wie in der Übung unten) und eine `WebFetch(domain:...)`-Allowlist setzen. |
| **EU, Finanzen** | DORA, MiFID II | Audit-Trail ist Pflicht. Auto-Memory und Transkript-Export zusammen nutzen, damit die Begründungen nachvollziehbar bleiben. `/autofix-pr` auf PRs regulierter Systeme nicht ohne menschliches Review. |
| **EU, Industrie und kritische Infrastruktur** | NIS2-Richtlinie | Betreiber kritischer Infrastruktur: Freigabe-Gates in jeder Automationsschleife. Den Datenfluss von Claude Code in der NIS2-Risikobewertung dokumentieren. |

**Grundsätze für regulierte Arbeit:**

1. **Auto-Memory für sensible Sitzungen abschalten**, damit keine Personendaten versehentlich dauerhaft gespeichert werden: `"autoMemoryEnabled": false` in den Projekt- oder Nutzer-Settings (oder der Schalter in `/memory`), per Umgebungsvariable `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. `--bare` ist dafür kein Schalter: Es ist ein Modus für Skripte und `-p`-Läufe, der beim Start Hooks, Skills, Plugins, MCP-Server, Auto-Memory und CLAUDE.md nicht lädt ([S4.3](s4-03-headless.md)).
2. **ZDR nutzen**, wo das Regelwerk verlangt, dass der Auftragsverarbeiter nichts aufbewahrt (HIPAA mit BAA, manche Auslegungen der DSGVO, Behördenverträge mit ZDR-Pflicht).
3. **Disziplin beim Audit-Trail:** Git-Commits mit klarer Urheberschaft; `/autofix-pr` nie auf geschützte Branches pushen lassen; Transkripte für die Aufbewahrungsfrist der Aufsicht archivieren.
4. **Datenfluss an deinen Datenschutzbeauftragten melden:** Anthropic für Claude (`api.anthropic.com` oder euer Bedrock- bzw. Google-Cloud-Mandant), OpenAI für Codex, falls du es anbindest ([S4.2](s4-02-codex-schwarm.md)), Google für NotebookLM ([S2.18](s2-18-rag-und-notebooklm.md)). Jeder davon ist eine eigene Auftragsverarbeitung. Auch mit ZDR gilt: Daten, die MCP-Server und andere Integrationen verarbeiten, deckt ZDR nicht ab.
5. **Rechte-Regel `WebFetch(domain:...)`:** ausgehende HTTP-Anfragen auf freigegebene Domains beschränken, damit nichts versehentlich bei Scraping-Diensten landet.
6. **Sandbox-Netz mit `sandbox.network.deniedDomains`:** versehentlichen Abfluss schon in der Sandbox sperren ([S3.10](s3-10-netzwerk-und-skills-haerten.md)).

**Vorbehalt:** Jedes Unternehmen legt diese Regelwerke anders aus, und nationale Behörden (BfDI in Deutschland, CNIL in Frankreich, ICO im Vereinigten Königreich) weichen teils voneinander ab. Der Kurs liefert Muster; **die Auslegung für euren Fall macht euer Compliance-Team.** Im Zweifel nimm den vorsichtigeren Weg: menschliche Freigabe, ZDR, Auto-Memory aus.

### Bekannte Schwachstellen als Lehrbeispiele

- **CVE-2025-53110:** Pfad-Traversal in der Pfadprüfung eines MCP-Servers. Die Prüfung mit `startsWith()` ließ sich mit `../`-Folgen umgehen; behoben wurde das mit strikter Pfad-Normalisierung. Die Lehre: Pfade nie per einfachem Zeichenvergleich prüfen. Schon der alte Kurs vermerkte (Stand 2026-05), dass die aktuelle Claude-Code-Doku dieses CVE nicht mehr in dieser Form als Beispiel führt. Das Muster dahinter, Präfixvergleich statt Kanonisierung, bleibt aktuell ([S2.17](s2-17-mcp-sicherheit.md)).
- **Lieferkette:** Verlassene Repositories in Skill-Marktplätzen lassen sich übernehmen, und über das nächste Update landen bösartige Skills bei ahnungslosen Nutzern. Muster und Gegenmaßnahmen stehen in [S2.13](s2-13-plugin-lieferkette.md).

Beide Beispiele zeigen an echten Fällen, warum das Rechtesystem und die Prüfung von Plugins zählen.

## Selbst machen

### Bonus-Übung: Leitplanke für sensible Daten im HIPAA-Stil (etwa 20 Minuten, allein)

**Ziel:** Einen Hook bauen, der jeden Schreibzugriff auf sensible Datenmuster prüft, als Nachbau einer Compliance-Leitplanke.

> **Nicht in den USA?** Die Übung nutzt HIPAA als konkretes Beispiel. Das Muster, sensible Daten per PreToolUse-Hook von unsicheren Orten fernzuhalten, gilt genauso für die DSGVO (Personendaten in der EU), PCI-DSS (Zahlungskarten) und EN 50131 (Zutrittsprotokolle der physischen Sicherheit). Pass die Muster an dein Regelwerk an; der Hook-Mechanismus bleibt gleich. Welche Kontrolle zu welchem Regelwerk passt, steht oben unter „Regulierte Branchen".

**Hintergrund:** Im Gesundheitswesen (HIPAA), in der Finanzbranche (PCI-DSS) und in der physischen Sicherheit (Zutrittsprotokolle mit Personendaten) gibt es strenge Regeln, welche Daten in Dateien landen dürfen. Dieser PreToolUse-Hook hält Claude davon ab, versehentlich sensible Muster in Code oder Konfigurationsdateien zu schreiben. Die Grundlagen zu Hooks stehen in [S2.8](s2-08-hook-einrichten.md).

**Analogie:** Der Scanner am Ausgang eines Hochsicherheitsgeländes, der prüft, dass niemand Verschlusssachen aus dem Gebäude trägt.

**Schritt 1: sensible Muster festlegen**

Wähl Muster für deine Domäne (geschrieben für `grep -E`, das kein `\d` kennt):

- US-Sozialversicherungsnummern: `[0-9]{3}-[0-9]{2}-[0-9]{4}`
- Kreditkartennummern: `[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}`
- API-Schlüssel: `(sk-|pk_)[A-Za-z0-9]{20,}` und `AKIA[A-Z0-9]{16}`
- Ausweis-IDs (deine Domäne!): Muster aus dem Format deiner Kartenleser
- IP-Adressen der internen Infrastruktur: `10\.[0-9]+\.[0-9]+\.[0-9]+` oder `192\.168\.`

**Schritt 2: den Scanner-Hook anlegen**

Leg `~/.claude/hooks/sensitive-data-scanner.sh` an (getestet im Repo als [`resources/demos/assets/hooks/sensitive-data-scanner.sh`](../demos/assets/hooks/sensitive-data-scanner.sh)). `grep -E` versteht kein `\d`, deshalb schreibt das Skript Ziffern als `[0-9]`.

<!-- cockpit:example -->
```bash
#!/bin/bash
# sensitive-data-scanner.sh - PreToolUse hook (matcher "Write|Edit"): block sensitive data in file writes.
# tested asset: resources/demos/assets/hooks/sensitive-data-scanner.sh
#
# Write sends the new file text as tool_input.content, Edit sends it as tool_input.new_string.
# exit 2 blocks the write; any other non-zero exit code would let it through.

INPUT=$(cat)

# Fail closed: if the input cannot be read, block instead of silently allowing the write.
if ! CONTENT=$(printf '%s' "$INPUT" | jq -er '.tool_input.content // .tool_input.new_string // ""' 2>/dev/null); then
  echo "SCANNER: could not read the hook input (is jq installed?) - blocking to stay safe." >&2
  exit 2
fi

# Adapt to your domain (card reader formats, internal IP ranges, ...). grep -E has no \d: use [0-9].
PATTERNS='([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(sk-|pk_)[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|password[[:space:]]*=[[:space:]]*"[^"]+")'

if printf '%s' "$CONTENT" | grep -qiE -- "$PATTERNS"; then
  # Do not echo the match itself: stderr goes to Claude as the block reason.
  echo "BLOCKED: sensitive data pattern detected in the file content." >&2
  echo "Redact or remove it before writing (use an environment variable or a secret store)." >&2
  exit 2
fi

exit 0
```

Write schickt den neuen Dateitext als `tool_input.content`, Edit als `tool_input.new_string`. Von den Exit-Codes blockt nur `exit 2` den Schreibzugriff. Kann das Skript seine Eingabe nicht lesen, blockt es lieber, statt still alles durchzulassen. Den Treffer selbst gibt es absichtlich nicht aus, weil stderr als Begründung an Claude geht.

**Schritt 3: eintragen und testen**

Trag den Hook unter einem `Write|Edit`-Matcher ein. **Führe** ihn in deine bestehende `hooks`-Struktur ein, statt den ganzen Block zu überschreiben, und prüf danach mit `python -m json.tool ~/.claude/settings.json`. Nimm am besten eine projekt-lokale `.claude/settings.json`, dann bleibt deine globale Konfiguration unberührt. Zum Testen bittest du Claude, eine Konfigurationsdatei mit einem fest eingetragenen API-Schlüssel anzulegen.

**Geschafft, wenn:**

- [ ] der Hook Schreibzugriffe mit sensiblen Mustern blockt
- [ ] normale Schreibzugriffe ohne sensible Daten durchgehen
- [ ] du mindestens ein Muster an deine Domäne angepasst hast
- [ ] du erklären kannst, warum von den Exit-Codes nur `exit 2` blockt und was passiert, wenn der Scanner mit einem anderen Code abstürzt (der Schreibzugriff geht durch: Der Scanner fällt offen)

**Zum Nachdenken**

1. Welche sensiblen Datenmuster gibt es in deinen echten Projekten?
2. Könntest du den Hook auch als PostToolUse-Hook laufen lassen, der nur protokolliert statt zu blocken?
3. Wie gehst du mit Fehlalarmen um, etwa mit Testdaten, die wie echte Zugangsdaten aussehen?

Eine weitere Übung mit Compliance-Bezug, die Integrität des Audit-Trails nach EN 50131, steht als Extra in [S3.6](s3-06-devils-advocate.md).

## Typische Fallen

- **Telemetrie aus heißt nicht Training aus.** `DISABLE_TELEMETRY` stoppt Nutzungsmetriken. Ob mit deinen Gesprächen trainiert wird, regeln Plan und Datenschutzeinstellung.
- **`--bare` als Memory-Schalter.** `--bare` ist für Skripte und `-p`-Läufe gedacht und liest dein Abo-Login gar nicht, sondern einen API-Schlüssel oder die Zugangsdaten eines Cloud-Anbieters. In deiner normalen Sitzung schaltest du Auto-Memory mit `autoMemoryEnabled` oder `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` ab.
- **ZDR deckt nicht alles.** Chat auf claude.ai, Cowork und Daten, die MCP-Server oder andere Integrationen verarbeiten, fallen nicht darunter. Und ZDR gilt nur für Anmeldungen in der ZDR-Organisation: Wer sich mit einem privaten Konto oder mit einem API-Schlüssel aus einer anderen Organisation anmeldet, ist nicht abgedeckt.
- **Der Scanner lässt alles durch.** Endet er bei einem Treffer mit `exit 1` statt `exit 2`, läuft der Schreibzugriff trotzdem. Warum, steht in [S2.8](s2-08-hook-einrichten.md).

## Check

Du kannst die drei Aufbewahrungsstufen nennen und für EN 50131, DSGVO und NIS2 jeweils eine passende Kontrolle aus dem Kurs zuordnen: Plan, Schalter, Rechte-Regel oder Freigabe-Gate.

1. Wie lange werden Daten bei einem Pro-Plan aufbewahrt, wenn du Training erlaubst, und wie lange, wenn nicht?
2. Welche Funktionen fallen unter ZDR weg, und warum?
3. Womit schaltest du Auto-Memory für eine sensible Sitzung ab?

<details><summary>Quizfrage</summary>

**Frage:** Eine Firma für Sicherheitstechnik prüft, ob sie Claude Code für Code-Reviews an der Firmware einer nach EN 50131 zertifizierten Alarmzentrale einsetzen darf. Welche Kombination passt zu den Mustern dieses Kapitels?

- **Richtig:** Enterprise-Plan, bei Bedarf mit ZDR, Auto-Memory aus, Freigabe-Gate in jeder Automation, kein `/autofix-pr` auf geschützten Branches.
- Falsch: Pro-Plan, `DISABLE_TELEMETRY=1` gegen das Training, Auto-Memory an, Firmware-Updates dürfen autonom in einer nächtlichen Schleife laufen.
- Falsch: Enterprise mit ZDR, das allein erfüllt EN 50131, DSGVO und NIS2 schon; Auto-Memory darf an bleiben, Freigabe-Gates entfallen.
- Falsch: Team-Plan, Anthropics API-Domain in `sandbox.network.deniedDomains`, Auto-Memory aus, `/autofix-pr` auf allen Branches erlaubt.

</details>

## Weiterlesen

- [Datennutzung und Aufbewahrung](https://code.claude.com/docs/en/data-usage)
- [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention)
- [Auto-Memory ein- und ausschalten](https://code.claude.com/docs/en/memory)
- [Hooks-Referenz](https://code.claude.com/docs/en/hooks)
- [S3.10 · Netzwerk und Skills härten](s3-10-netzwerk-und-skills-haerten.md)
- [S2.8 · Einen Hook einrichten, der wirklich blockt](s2-08-hook-einrichten.md)
- [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](s3-06-devils-advocate.md)
- [S2.13 · Lieferkettenrisiken bei Plugins](s2-13-plugin-lieferkette.md)
- [S2.17 · MCP-Sicherheit und ein eigener Server](s2-17-mcp-sicherheit.md)
- [S4.2 · Codex-Schwarm und die Datenfluss-Grenze](s4-02-codex-schwarm.md)
- [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](s2-18-rag-und-notebooklm.md)
- [S4.3 · Headless: claude -p als Pipeline-Stufe](s4-03-headless.md)
- [S4.10 · Diagnose Schritt für Schritt](s4-10-diagnose-schritt-fuer-schritt.md)
- Getestete Hook-Datei: [`sensitive-data-scanner.sh`](../demos/assets/hooks/sensitive-data-scanner.sh)
