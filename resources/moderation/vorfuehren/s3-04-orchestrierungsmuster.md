# Vorführen: S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie

> Demo und Hinweise für Moderierende zum Kapitel [S3.4 · Orchestrierungsmuster: Fan-out, Pipeline, Hierarchie](../../library/s3-04-orchestrierungsmuster.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Fan-out und Pipeline

**Ziel:** Zeigen, dass zwei unabhängige Aufgaben parallel laufen und zwei abhängige nacheinander, und dass man den Unterschied an den Aufträgen sieht, die Claude den Subagenten gibt.

Zeig die Übung aus dem Kapitel live: die Übung „Fan-out und Pipeline an einem kleinen Projekt“ in [S3.4](../../library/s3-04-orchestrierungsmuster.md). Startzustand wie dort: der Ordner `~/cc-workshop/muster` mit `access.log`, `cards.csv` und `reader.py`; leg sie vorher an. Starte mit `claude --permission-mode default` und bestätige den Vertrauensdialog. Ablauf: Teil A (Schritte 1 und 2, Fan-out) und Teil B (Schritte 3 und 4, Pipeline).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 Minuten geplant; reserviere live etwa 12 Minuten (× 1,5), falls die Ausgaben der Agenten lang werden.

**Sagen:**

- Teil A, Schritt 1: „Wir haben gerade zwei Sicherheitsteams losgeschickt, die gleichzeitig verschiedene Etagen absuchen. Das eine zählt die abgelehnten Zugriffe im Protokoll, das andere sucht in der Firmware nach offenen Punkten. Beide melden unabhängig zurück; wir bekommen beide Berichte parallel, nicht nacheinander. Genau so arbeitet eine gut geführte Leitstelle." Erwartet sind 5 `DENIED`-Zeilen und die Kommentare in den Zeilen 2, 7 und 12. Mit `Ctrl+O` siehst du zwei Delegationen im Transkript; schließ die Ansicht mit `Ctrl+O`.
- Schritt 2: Lies die beiden Auftragstexte vor. „Keiner verweist auf das Ergebnis des anderen. Jede Aufgabe ließ sich allein lösen. Das macht ein Fan-out aus."
- Teil B, Schritt 3: „Hier braucht die zweite Aufgabe das Ergebnis der ersten." Der erste Subagent nennt `C-231`, der zweite meldet T. Brandt mit Status `blocked`. Die zweite Delegation erscheint im Transkript erst, nachdem die erste fertig ist.
- Schritt 4: „Die Karten-ID konnte Claude erst schreiben, nachdem der erste Subagent geantwortet hatte. Das ist die Abhängigkeit, und deshalb ist das eine Pipeline. Hätte Claude beide gleichzeitig gestartet, hätte der zweite die Karte raten müssen." Frag die Gruppe, warum Teil B kein Fan-out sein konnte.

**Wenn etwas schiefgeht:**

- **Claude startet keine Subagenten und antwortet nacheinander:** Fordere neu auf: „Use SEPARATE agents running IN PARALLEL for each part. I want to see both results separately."
- **Nur ein Subagent startet:** Die Aufgaben sind vielleicht nicht wirklich unabhängig. Formuliere sie klar unabhängig: kein gemeinsamer Zustand, keine Reihenfolge.
- **Die Ausgabe ist live zu lang zum Mitlesen:** Kündige an, was ungefähr kommt („ihr werdet gleich so etwas sehen …"), und überfliege die Ausgaben.

</details>
