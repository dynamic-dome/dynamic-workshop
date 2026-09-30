# FAQ: Fragen ohne eigenes Kapitel

Wofür: die wenigen Fragen, die mehrere Kapitel berühren und deshalb keines als Heimat haben. Je Frage eine Antwort und
die Kapitel, in denen es weitergeht.

Geprüft gegen die offizielle Doku am 2026-09-30 (CLI 2.1.285). Offizielle Quelle: https://code.claude.com/docs/en/features-overview

Alle anderen Fragen der alten FAQ beantworten jetzt die Kapitel selbst, meist im Abschnitt „Typische Fallen". Welches
Kapitel wozu gehört, zeigt die [Regal-Übersicht](../library/README.md); Begriffe erklärt das [Glossar](glossar.md).

## Wann nehme ich einen Skill, einen Subagenten, einen Command oder einen Hook?

Skill für Anweisungen, die du immer wieder gibst; Subagent für Arbeit, die isoliert oder parallel laufen soll; Hook für
alles, was automatisch und verlässlich bei einem Ereignis passieren muss; Command für einen Ablauf, den du gezielt per
`/name` startest; soll Claude ihn nie von selbst auslösen, setz `disable-model-invocation: true`.
Weiter: [S2.1 · Skills sind Dienstanweisungen, Commands sind Knöpfe](../library/s2-01-skills-und-commands.md) · [S2.3 · Skills oder Commands, und wer sie auslösen darf](../library/s2-03-wer-skills-ausloest.md) · [S2.6 · Hooks als Sensoren: die drei Eckpfeiler](../library/s2-06-hooks-als-sensoren.md) · [S3.1 · Was ist ein Agent? Spezialisierung statt Allrounder](../library/s3-01-was-ist-ein-agent.md)

## Wie verteile ich mein Claude-Code-Setup an mein Team?

Checke `.claude/` ins Repository ein (Skills, Hooks, Settings, Agents, Rules) und halte Persönliches heraus:
`CLAUDE.local.md` und `.claude/settings.local.json` gehören in `.gitignore` (die zweite hält Claude Code beim Anlegen
selbst aus Git heraus). `/team-onboarding` erzeugt aus deiner Nutzung einen Einrichtungsleitfaden für Teammitglieder.
Was mehrere Repositories brauchen, bündelst du als Plugin und verteilst es über einen eigenen Marketplace (etwa ein
privates Git-Repository) oder reichst es bei Anthropic ein (Community-Marketplace `claude-community`). Für Neue hilft
ein vorbereitetes `~/.claude/`-Bündel als Git-Repository zum Klonen.
Weiter: [S1.10 · CLAUDE.md: die Hausordnung des Projekts](../library/s1-10-claude-md.md) · [S2.11 · Plugins: ein Bündel schnüren](../library/s2-11-plugins-buendeln.md) · [S2.12 · Plugin-Lebenszyklus, Scopes und Marketplaces](../library/s2-12-plugin-lebenszyklus.md)

## Wie schütze ich Secrets?

Schreib sie nie in `CLAUDE.md` oder andere eingecheckte `.claude/`-Dateien und übergib API-Keys als Umgebungsvariablen,
nicht im Klartext im Befehl. Sperre Dateien mit einer Deny-Regel wie `Read(./.env)`: Sie gilt für die Datei-Tools, für
Bash-Befehle, die Claude Code als Dateizugriff erkennt (`cat`, `head`, `tail` …), und blockt auch `Edit` und `Write`
auf dem Pfad, aber nicht `grep -r` oder beliebige Unterprozesse; die Grenze auf Betriebssystemebene zieht die Sandbox.
Ein Hook wie das Secure Diff Gate blockt zusätzlich Schreibzugriffe auf sensible Dateien wie `.env`, `*.pem` oder `secrets/`. Lass `/security-review` regelmäßig laufen,
und schwärze Code, bevor ein Codex-Schritt ihn an OpenAI schickt.
Weiter: [S2.10 · Hook-Ausgaben und das Secure Diff Gate](../library/s2-10-hook-ausgaben.md) · [S3.8 · Rechte für autonome Läufe](../library/s3-08-rechte-fuer-autonomie.md) · [S3.9 · Geschützte Pfade und Sandbox-Stufen](../library/s3-09-geschuetzte-pfade-und-sandbox.md) · [S3.7 · Die eingebauten Reviews](../library/s3-07-eingebaute-reviews.md) · [S4.2 · Codex-Schwarm und die Datenfluss-Grenze](../library/s4-02-codex-schwarm.md)

## Mehr dazu

- Doku: [Wann welche Erweiterung](https://code.claude.com/docs/en/features-overview) · [Rechte-Regeln](https://code.claude.com/docs/en/permissions) · [Sensible Dateien ausschließen](https://code.claude.com/docs/en/settings-reference#exclude-sensitive-files)
- [alle Karten](README.md)
