# Vorführen: S1.13 · Vager und präziser Auftrag im Vergleich

> Demo und Hinweise für Moderierende zum Kapitel [S1.13 · Vager und präziser Auftrag im Vergleich](../../library/s1-13-vager-und-praeziser-auftrag.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: vager und präziser Auftrag

**Ziel:** Zwei Aufträge im selben Werkzeug zeigen, die denselben Fehler beheben sollen: einer ohne Grenze, einer mit den vier Bausteinen. Der Unterschied steht im Diff.

Zeig die Übung aus dem Kapitel live: die Übung „erst vage, dann deine vier Bausteine“ in [S1.13](../../library/s1-13-vager-und-praeziser-auftrag.md).

**Startzustand:** der Ordner `~/cc-workshop/auftrag` mit `prices.py` und `test_prices.py`, so wie im Startzustand der Übung beschrieben. Lege beide Dateien vorher an, damit du live nicht tippst, und mach Schritt 1 der Übung (`git init`, `git add .`, `python -m unittest` mit dem einen Fehlschlag) vor der Gruppe, denn der Fehlschlag ist der Anlass für beide Aufträge.

**Ablauf:** Schritte 2 bis 5 der Übung. Runde 1 mit dem Auftrag `Clean up prices.py and make the tests pass.`, danach `git diff --stat` und `git diff`, dann `git restore prices.py`. Runde 2 mit einem Auftrag, der Ort, Ursache, Scope-Grenze und Erfolgskriterium nennt; nimm den Vergleichsauftrag aus dem Kapitel oder lass die Gruppe ihn vorher aus den vier Bausteinen zusammensetzen.

**Zum Vergleich zeigen oder anschreiben:**

| | Vager Auftrag (Runde 1) | Präziser Auftrag (Runde 2) |
|---|---|---|
| **Eingabe** | „Clean up prices.py and make the tests pass.“ | Ort, Ursache, Scope-Grenze, Erfolgskriterium |
| **Was Claude darf** | alles in der Datei | nur `total()` |
| **Diff** | meist mehr als die eine Zeile, vermutlich auch Aufgeräumtes | nur `total` |
| **Prüfung** | Diff lesen, was nicht verlangt war | `python -m unittest` zeigt `OK` |

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 Minuten, wie die Übung.

**Sagen:**

- Vor Runde 1: „Gleiches Werkzeug, gleicher Fehler. Ich gebe einen Auftrag, wie man ihn schnell hinschreibt."
- Nach Runde 1, beim Diff: Frag die Gruppe, welche Zeilen sie nicht verlangt haben. Ob Claude aufgeräumt hat, ist nicht garantiert; sag das so. „Ohne Grenze wäre es erlaubt gewesen. Deshalb schaue ich ins Diff, nicht nur auf den grünen Test."
- Während die Gruppe Runde 2 formuliert: „Zählt die vier Bausteine, nicht die Zeilen. Ein langer Auftrag ohne Ort und Erfolgskriterium rät trotzdem."
- Nach Runde 2: „Das Werkzeug ist zwischen den beiden Aufträgen nicht klüger geworden. Die Aufträge sind es. Schreibt Aufträge wie Arbeitsaufträge: konkret, abgegrenzt, mit Erfolgskriterium."

**Wenn es anders läuft:**

- **Runde 1 ändert nur die eine Zeile:** Das passiert und beweist nichts gegen die Methode. Sag es offen: „Diesmal hat Claude Maß gehalten; ohne Grenze hätte es das nicht müssen." Zeig dann Runde 2 trotzdem, mit der Scope-Grenze als Absicherung.
- **Nach Runde 2 ist der Test nicht grün:** Zeig die Meldung als Lehrmoment: Auch mit gutem Auftrag prüfst du selbst, hier mit dem Erfolgskriterium.
- **`git restore prices.py` vergessen:** Dann zeigt das Diff von Runde 2 beide Änderungen. Führ es aus und wiederhole Runde 2.

</details>
