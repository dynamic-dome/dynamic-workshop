# Vorführen: S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff

> Demo und Hinweise für Moderierende zum Kapitel [S4.4 · CI-Zugangsdaten, Kostengrenzen und Kosten-Feinschliff](../../library/s4-04-ci-zugang-und-kosten.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: ein fremdes Repo, ein Hook, ein Deckel

**Ziel:** Zeigen, dass `claude -p` ohne `--bare` den Hook eines Ordners ausführt, ohne zu fragen, dass `--bare` ihn nicht lädt (und dafür eine Anmeldung braucht), und wie ein Budgetdeckel einen Lauf abbricht.

Zeig die Übung aus dem Kapitel live: die Übung „ein fremdes Repo, ein Hook, ein Deckel“ in [S4.4](../../library/s4-04-ci-zugang-und-kosten.md). Startzustand wie dort: der Ordner `~/cc-workshop/ci-zugang`, der ein fremdes Repo spielt, mit der `.claude/settings.json` aus Schritt 2 (ein harmloser `SessionStart`-Hook, der eine Zeile in `hook-ran.txt` schreibt). In diesem Ordner hast du `claude` nie gestartet und keinen Vertrauensdialog bestätigt. Ablauf: die Schritte 1 bis 5 der Übung (`claude auth status`, der Lauf ohne `--bare`, der Lauf mit `--bare`, der Lauf mit winzigem Budget).

Die Demo setzt die Demo aus [S4.3](s4-03-headless.md) nicht voraus. Die Extra-Übung mit eigenem API-Key zeigst du nur, wenn der Key in deiner Umgebung steht, und nie so, dass er auf dem Bildschirm oder im Verlauf landet.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 bis 15 Minuten.

**Sagen:**

- Schritt 1: „`claude auth status` zeigt, welche Methode gilt, und endet mit Exit-Code 0, wenn ich angemeldet bin. Steht dort `claude.ai` oder `oauth_token`, wird `--bare` gleich nicht angemeldet sein."
- Schritt 3: „Ich habe kein `claude` in diesem Ordner gestartet und keinen Dialog bestätigt. Trotzdem ist der Hook gelaufen." Zeig `hook-ran.txt`. „Ohne `--bare` führt eine `-p`-Sitzung die Hooks aus der `.claude/settings.json` des Projekts aus und verbindet die Server aus seiner `.mcp.json`, auch in einem Ordner, dem ich nie vertraut habe. In einer CI, die Code von Beitragenden auscheckt, wäre das ein Problem." Lies `total_cost_usd` im JSON ab; die Doku nennt es eine Schätzung.
- Schritt 4: „`--bare` schaltet die automatische Erkennung von Hooks, Skills, Plugins, MCP-Servern, Auto-Memory und `CLAUDE.md` ab, der Kaltstart ist schneller. Der Hook läuft nicht." `hook-ran.txt` fehlt. Wer nur per Browser angemeldet ist, sieht einen Fehler, nicht angemeldet, und einen Exit-Code ungleich 0: `--bare` liest weder OAuth-Anmeldungen noch den Schlüsselbund und braucht für die Anthropic-API einen API-Key. `--bare` ist keine Rechte-Grenze: Claude hat auch dann Bash und die Datei-Werkzeuge.
- Schritt 5: „Der Deckel ist winzig, der Lauf endet vorzeitig. Im JSON steht `error_max_budget_usd`. Die Antwort, mit der der Lauf die Grenze überschreitet, wird noch bezahlt: Die Endsumme kann also etwas über der Grenze liegen." Lies den Exit-Code ab, den du siehst: Die Doku nennt keinen, also verlässt sich eine Pipeline nicht auf eine Annahme, sondern auf das Gemessene.
- Zum Abschluss: „In CI setzt ihr immer beide Deckel, `--max-budget-usd` und `--max-turns`. Beide gibt es nur mit `-p`."

**Wenn kein API-Key da ist:** Zeig Schritt 4 trotzdem. Der Fehler, nicht angemeldet, ist der Punkt der Demo: Ein `--bare`-Job, der nur das Abo-Token hat, ist nicht angemeldet.

**`claude setup-token` nie live:** Willst du den Befehl zeigen, dann **vor dem Workshop offline**, nicht auf dem geteilten Bildschirm. Er gibt ein langlebiges OAuth-Token aus, das ein Jahr lang dein Abo verbraucht. Wer damit nachlässig umgeht, geht dasselbe Risiko ein wie mit einem privaten SSH-Schlüssel auf dem Beamer. Das Token kann nur Modell-Anfragen stellen, und `--bare` liest es nie. Nenn den Befehl, verweis auf die Doku und mach weiter.

**Kein Secret in einen Prompt oder eine Datei:** Auch nicht für das Extra.

</details>
