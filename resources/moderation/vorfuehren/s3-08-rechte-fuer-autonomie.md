# Vorführen: S3.8 · Rechte für autonome Läufe

> Demo und Hinweise für Moderierende zum Kapitel [S3.8 · Rechte für autonome Läufe](../../library/s3-08-rechte-fuer-autonomie.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Rechte-Modi, vom Besucherausweis zum Generalschlüssel (etwa 5 Minuten)

**Ziel:** Die Rechte-Modi live zeigen: Dieselbe Aufgabe verhält sich je nach Freigabestufe anders.

**Schritt 1: Manual zeigen (1 Min.)**

Starte Claude Code mit `claude --permission-mode default`. Ohne Flag startet eine neue Sitzung in aktuellen Versionen in `auto`. Frag:

```
Show me the contents of package.json
```

Das läuft ohne Rückfrage, Lesen ist frei.

Jetzt:

```
Add a comment to the top of README.md
```

Claude fragt nach einer Freigabe.

**Schritt 2: zu acceptEdits wechseln (1 Min.)**

Drück `Shift+Tab`, bis die Statusleiste `⏵⏵ accept edits on` zeigt. Frag noch einmal:

```
Add a comment to the top of README.md
```

Diesmal läuft es ohne Rückfrage. Bei diesem Auftrag dagegen fragt Claude weiter nach:

```
Run npm test
```

**Schritt 3: Plan-Modus zeigen (2 Min.)**

Starte eine neue Sitzung mit:

```bash
claude --permission-mode plan
```

Frag:

```
Refactor this file to use async/await instead of callbacks, add error handling, and run tests
```

Claude liest, erkundet und legt zuerst den ganzen Plan vor; geändert wird nichts, bevor du ihn freigibst. Bei der Freigabe wählst du, wie es weitergeht: in `auto`, mit automatisch angenommenen Änderungen oder mit Einzelfreigabe jeder Änderung.

**Schritt 4: auto, dontAsk und bypassPermissions nur erklären (1 Min.)**

Diese drei zeigst du nicht live, das ist für eine Vorführung zu riskant:

- `auto`: Ein Klassifikator prüft statt dir. Auch in Cloud-Sitzungen wählbar, wenn Organisation und Modell es erlauben.
- `dontAsk`: vorab genehmigte Arbeitsaufträge für CI/CD. Nur Erlaubtes läuft, alles andere wird abgelehnt.
- `bypassPermissions`: der Generalschlüssel, nur in abgeschlossenen Testräumen (Docker, Sandbox).

Öffne zum Schluss:

```
/permissions
```

Der Dialog zeigt die Allow-, Ask- und Deny-Regeln, die zusätzlich zum Modus gelten, und aus welcher Datei sie stammen. Den Modus selbst wechselt er nicht.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 Minuten (Schritt 1: 1 Min., Schritt 2: 1 Min., Schritt 3: 2 Min., Schritt 4: 1 Min.).

**Sagen:**

- Schritt 1: „Manual, der Modus mit dem Wert default. Besucherausweis. Lesen ist frei, Schreiben braucht eine Freigabe."
- Schritt 2: „Wartungsausweis. Du kommst in die Büros, aber der Serverraum braucht weiter eine Freigabe."
- Schritt 3: „Plan-Modus ist die Einsatzbesprechung. Du genehmigst den Einsatzplan als Ganzes; ob danach jede Änderung einzeln gegengezeichnet wird, entscheidest du bei der Freigabe. Das hilft bei mehrstufigen Aufgaben, bei denen ständiges Freigeben ermüdet."
- Schritt 4: „Einem Handwerker würdest du im laufenden Gebäude nie einen Generalschlüssel geben. Hier gilt dieselbe Regel: bypassPermissions nur in abgeschlossenen Testumgebungen."
- Zum Abschluss: „Sechs Freigabestufen, vom Besucherausweis bis zum Generalschlüssel. Du wählst die passende für die Lage, so wie du einem Lieferfahrer nie denselben Zugang gibst wie dem Haustechniker."

**Wenn es hakt:**

- **Der `Shift+Tab`-Zyklus geht nicht:** Starte ausdrücklich mit `claude --permission-mode plan` im Plan-Modus.
- **Unklar, welcher Modus aktiv ist:** Die Statusleiste zeigt ihn (`⏸ manual mode on`, `⏵⏵ accept edits on`, `⏸ plan mode on`); `/permissions` zeigt Regeln, keinen Modus. Den eingestellten Startmodus siehst du mit `cat ~/.claude/settings.json | jq .permissions`.
- **`acceptEdits` fragt trotzdem bei Änderungen:** Liegt die Datei außerhalb des Arbeitsordners oder in einem geschützten Pfad wie `.claude/` ([S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md))? Prüf auch die projektlokale `.claude/settings.local.json` auf Ask-Regeln; sie geht den Projekt- und Nutzer-Einstellungen vor.
- **`claude --permission-mode plan` wird nicht erkannt:** Prüf mit `claude --version`, ob die Installation aktuell ist. In der Sitzung erreichst du den Plan-Modus auch mit `Shift+Tab` oder mit `/plan` vor einer einzelnen Anfrage.

Die Karte der sechs Modi für die Nachbesprechung steht in [S1.6](../../library/s1-06-rechte-modi.md), die geschützten Pfade in [S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md).

</details>
