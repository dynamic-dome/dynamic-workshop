# Vorführen: S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen

> Demo und Hinweise für Moderierende zum Kapitel [S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen](../../library/s1-19-kosten-im-blick.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: dieselbe Aufgabe, drei Modelle

**Ziel:** Zeigen, dass Modellwahl und Effort Kostenhebel sind, nicht nur Qualitätshebel.

**Was die Gruppe sieht:** Dieselbe realistische Coding-Aufgabe läuft dreimal mit verschiedenen Kombinationen aus Modell und Effort, nach jedem Lauf `/cost`, damit ihr die Beträge nebeneinander vergleichen könnt. Die Aufgabe ist der IPv4-Validator, den ihr aus [S1.13](../../library/s1-13-vager-und-praeziser-auftrag.md) kennt.

**Vorbereitung**

- Terminal in einem Wegwerf-Ordner (`~/cost-demo/`)
- Claude Code angemeldet, eine frische Sitzung
- `/cost` vor dem Workshop einmal ausprobieren

**Schritt 1: Ausgangswert mit dem Opus-Tier und xhigh**

In Claude Code:

```
/model opus
/effort xhigh
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

Erwartet: Claude liefert eine gründliche Umsetzung mit mehreren Randfällen (führende Nullen, Oktette außerhalb des Bereichs, leere Strings, eingebettete Leerzeichen) und einem kleinen Testblock.

Danach:

```
/cost
```

Erwartet: die Kosten dieses einen Durchgangs. Notier den Betrag; es kommt auf die Größenordnung an, nicht auf den genauen Wert.

**Schritt 2: dieselbe Aufgabe mit dem Sonnet-Tier und medium**

Starte vorher mit `/clear` neu. Sonst zählt `/cost` alle Läufe zusammen, und das neue Modell liest den ganzen bisherigen Verlauf ohne Cache-Treffer neu; der Vergleich wäre schief.

```
/model sonnet
/effort medium
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

Danach:

```
/cost
```

Erwartet: deutlich weniger als im ersten Lauf. Schon der Preis pro Token ist beim Sonnet-Tier etwa halb so hoch wie beim Opus-Tier ([Kanon](../../_canonical.md)), dazu kommt die niedrigere Effort-Stufe.

**Schritt 3: dieselbe Aufgabe mit dem Haiku-Tier (ohne Effort)**

Haiku kennt keine Effort-Stufen, deshalb fehlt hier die `/effort`-Zeile: Die Modellwahl allein ist der Hebel. (Aliase, Generationen und Effort je Tier: [Kanon](../../_canonical.md).) Wieder vorher `/clear`.

```
/model haiku
Write a Python function that validates IPv4 addresses with proper edge case handling. Include a few tests at the bottom of the file demonstrating valid and invalid inputs.
```

```
/cost
```

Erwartet: der günstigste der drei Läufe. Pro Token kostet das Haiku-Tier etwa ein Viertel des Opus-Tiers.

**Schritt 4: nebeneinander vergleichen**

Öffne die drei erzeugten Dateien im Editor oder zeig sie nebeneinander im Terminal. Frag die Runde:

- Sind alle drei Ergebnisse fachlich korrekt? (Meist ja.)
- Wo liegt der Qualitätsunterschied? (Opus zählt meist mehr Randfälle auf, Haiku erklärt knapper.)
- Wie groß ist der Abstand zwischen dem günstigsten und dem teuersten Lauf? Lest ihn an euren eigenen Zahlen ab.
- Ist das Opus-Tier bei genau dieser Aufgabe, einer klar umrissenen IPv4-Prüfung ohne Architekturentscheidung, den Aufpreis wert? Fast nie.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 6 Minuten.

**Einstieg:** „Das ist das Kapitel, das euer Manager kennen muss. Kosten sind nicht ‚schauen wir mal‘, Kosten sind eine bewusste Variable wie Latenz oder Speicher.“

**Sagen:**

- Schritt 1: „Das ist eine teure Kombination, Opus auf einer tiefen Effort-Stufe. Schaut auf die Kosten. Jetzt sehen wir, was wir für weniger bekommen.“
- Schritt 2: „Sonnet auf seiner Start-Stufe. Dieselbe Aufgabe, vermutlich ähnliche Codequalität. Seht ihr, was das im Vergleich zum ersten Lauf kostet?“
- Schritt 3: „Haiku, das günstigste Tier. Die Ausgabe ist etwas knapper, vielleicht fehlen ein, zwei Randfälle. Aber für eine IPv4-Prüfung, eine Aufgabe mit bekannter richtiger Antwort, reicht Haiku.“
- Schritt 4: „Die eigentliche Frage stellt ihr *vor* der Sitzung: Wie wichtig ist hier die Qualität? Für ein einmaliges Hilfsskript reicht Haiku. Entwerft ihr einen Protokoll-Parser, der zehn Jahre in einer Firmware lebt, zahlt ihr für Opus mit xhigh. Kostenregler und Effort-Regler gehören zu eurem Job.“
- Abschluss: „Kosten sind kein Aufkleber am Monatsende, sondern ein Regler, den ihr in jeder Sitzung dreht. `/cost` zeigt, wo ihr in dieser Sitzung steht; im Abo zeigt `/usage` die letzten 24 Stunden oder 7 Tage und was sie getrieben hat. Schaut nach, bevor ihr einen Ablauf hochskaliert.“
- Merksätze: „Effort ist ein Regler, kein Schalter: xhigh ist nicht einfach besser.“ und „Die Budgetgrenze ist für autonome `-p`-Läufe Pflicht, nicht Kür.“

**Wenn `/cost` in einer älteren Version fehlt:** Wechsle auf die Usage-Seite der Claude Console (https://platform.claude.com/usage). Die zeigt die Summe; der Punkt kommt trotzdem an.

**Wenn zwei Läufe verdächtig gleich viel kosten:** Wahrscheinlich hat der Cache gegriffen. Starte zwischen den Läufen mit `/clear` neu oder ändere den Prompt leicht.

**Wenn jemand bezweifelt, dass Haiku korrekten Code liefert:** Führ das Gegenbeispiel live aus. Der Punkt der Demo bleibt, und nebenbei hast du adversariales Debugging gezeigt.

**Nach der Demo:** `/model` und `/effort` haben deine Wahl als Standard gespeichert, zuletzt `haiku`. `/model default` holt das Standardmodell deines Kontos zurück, `/effort auto` löscht die gespeicherte Stufe des aktiven Modells.

</details>
