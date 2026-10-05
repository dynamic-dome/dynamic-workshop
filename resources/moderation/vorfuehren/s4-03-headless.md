# Vorführen: S4.3 · Headless: claude -p als Pipeline-Stufe

> Demo und Hinweise für Moderierende zum Kapitel [S4.3 · Headless: claude -p als Pipeline-Stufe](../../library/s4-03-headless.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Headless Claude in fünf Minuten

**Ziel:** Zeigen, dass derselbe Claude, mit dem du bisher interaktiv gearbeitet hast, auch als einmaliges Kommandozeilen-Werkzeug läuft: mit JSON-Ausgabe, Kostengrenze und `--bare`. Fünf Minuten, vier Flags, ein Umdenken.

Die Demo verteilt sich auf drei Kapitel: Schritt 1 steht in [S3.1](s3-01-was-ist-ein-agent.md), weil er dort als garantierter Live-Einstieg dient; Schritt 2 steht hier; die Schritte 3 und 4 (Kostengrenze, `--bare`) stehen in [S4.4](s4-04-ci-zugang-und-kosten.md).

**Voraussetzung**

- `claude` ist auf dem Rechner der moderierenden Person installiert und angemeldet.
- Eine kleine Datei als Eingabe. `workshop-playground/access_control.py` passt gut.
- Ein Terminal, in dem das Publikum den Befehl und seinen Exit-Code sieht.

**Schritt 1: ein Prompt, eine Antwort**

`claude -p "Summarize what this repo does in one sentence."`, Ablauf und Sprechpunkte in [S3.1](s3-01-was-ist-ein-agent.md).

**Schritt 2: strukturierte Ausgabe mit Schema**

```bash
claude -p "Categorize this file" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"category":{"type":"string"},"language":{"type":"string"}}}' \
  < workshop-playground/access_control.py
```

Wenn die Ausgabe erscheint, leite sie live durch `jq`, um zu zeigen, dass sie wirklich parsebar ist. Das Ergebnis steht im Feld `structured_output`:

```bash
... | jq '.structured_output.category'
```

<details><summary>Für Moderierende</summary>

**Garantierter Anker:** Diese Demo braucht nur das lokal installierte und angemeldete `claude`: kein Plugin, kein Codex, keine Bridge. Eine Netzverbindung zur Claude-API braucht sie wie jeder Aufruf. Schritt 1 dient zugleich als 60-Sekunden-Einstieg in Session 3 (siehe [S3.1](s3-01-was-ist-ein-agent.md)). Wenn alles andere brennt, läuft diese Demo trotzdem.

**Sagen:**

- Schritt 2: „Darauf kann sich eine CI-Pipeline verlassen. Frei formulierte Prosa bricht Parser, ein Schema nicht."
- Zum Abschluss der ganzen Demo, nach Schritt 4 in [S4.4](s4-04-ci-zugang-und-kosten.md): „Wir haben Claude Code gerade in ein Unix-Werkzeug verwandelt. Es nimmt stdin, liefert stdout, gibt einen Exit-Code zurück, beachtet Flags und bleibt im Budget. Das ist die Eintrittskarte in jedes CI-System: GitHub Actions, GitLab, Jenkins, dein eigener Cron. Der interaktive Claude ist die eine Hälfte des Produkts. Das hier ist die andere."

**Wenn `jq` `null` ausgibt:** Du hast das Feld auf oberster Ebene abgefragt (`.category`). Das Schema-Ergebnis liegt eine Ebene tiefer in `structured_output`.

</details>
