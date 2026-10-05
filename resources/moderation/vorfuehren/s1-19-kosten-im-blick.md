# Vorführen: S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen

> Demo und Hinweise für Moderierende zum Kapitel [S1.19 · Kosten im Blick: /cost, /usage und Budgetgrenzen](../../library/s1-19-kosten-im-blick.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: dieselbe Aufgabe, drei Modelle

**Ziel:** Zeigen, dass Modellwahl und Effort Kostenhebel sind, nicht nur Qualitätshebel.

Zeig die Übung aus dem Kapitel live: die Übung „dieselbe Aufgabe, drei Modelle“ in [S1.19](../../library/s1-19-kosten-im-blick.md).

**Startzustand:** der leere Ordner `~/cc-workshop/kosten`, Claude Code angemeldet, `/cost` vor dem Workshop einmal ausprobiert. Du stellst Modell und Effort nur mit Start-Flags ein und tippst in diesen Sitzungen weder `/model` noch `/effort`: Beide würden deine Wahl als Standard speichern.

**Ablauf:** Schritte 1 bis 4 der Übung. Jeder Lauf ist eine neue Sitzung (`claude --model opus --effort xhigh …`, dann `sonnet` mit `medium`, dann `haiku` ohne `--effort`), derselbe Auftrag mit je eigenem Dateinamen, danach `/cost`, den Betrag notieren, `Esc`, `/exit`. Schritt 5 (Standard unverändert) zeigst du zum Schluss.

Danach frag die Runde:

- Sind alle drei Dateien fachlich korrekt?
- Wie groß ist der Abstand zwischen dem günstigsten und dem teuersten Lauf? Lest ihn an euren eigenen Zahlen ab.
- Zeigt sich der Aufpreis bei dieser Aufgabe in der Qualität? Sieh in die drei Dateien.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 6 bis 10 Minuten.

**Einstieg:** „Das ist das Kapitel, das euer Manager kennen muss. Kosten sind nicht ‚schauen wir mal‘, Kosten sind eine bewusste Variable wie Latenz oder Speicher.“

**Sagen:**

- Lauf 1: „Das ist eine teure Kombination, das Opus-Tier auf einer tiefen Effort-Stufe. Schaut in die Ansicht Usage auf `Total cost`. Jetzt sehen wir, was wir für weniger bekommen."
- Lauf 2: „Sonnet auf mittlerer Stufe. Gleiche Aufgabe. Seht ihr, was das im Vergleich zum ersten Lauf kostet?" Pro Token kostet das Sonnet-Tier etwa die Hälfte des Opus-Tiers ([Kanon](../../_canonical.md)).
- Lauf 3: „Haiku, das günstigste Tier, ohne Effort-Stufen: Die Modellwahl allein ist der Hebel." Pro Token kostet es etwa ein Viertel des Opus-Tiers ([Kanon](../../_canonical.md)). Einzelne Läufe können trotzdem abweichen, etwa wegen unterschiedlich langer Antworten; sag das, wenn die Zahlen nicht sauber sinken.
- Vergleich: „Die eigentliche Frage stellt ihr *vor* der Sitzung: Wie wichtig ist hier die Qualität? Für ein einmaliges Hilfsskript reicht vermutlich das günstige Tier. Kostenregler und Effort-Regler gehören zu eurem Job."
- Abschluss: „Kosten sind kein Aufkleber am Monatsende, sondern ein Regler, den ihr in jeder Sitzung dreht. `/usage` zeigt, wo ihr in dieser Sitzung steht; `/cost` ist ein anderer Name dafür. Im Abo zeigt er darunter, was den Verbrauch getrieben hat. Schaut nach, bevor ihr einen Ablauf hochskaliert."
- Merksatz: „Die Budgetgrenze ist für unbeaufsichtigte `-p`-Läufe Pflicht, nicht Kür." Die Extra-Übung des Kapitels zeigt `--max-budget-usd` und `--max-turns`; beide wirken nur mit `-p`.

**Wenn die Ansicht offen bleibt:** `/cost` bleibt offen, bis du `Esc` drückst; der nächste Auftrag landet sonst in der Ansicht.

**Wenn du in einer Sitzung das Modell wechselst:** Starte lieber eine neue Sitzung. Wechselst du das Modell in derselben Sitzung, liest das neue Modell den Verlauf ohne Cache-Treffer neu, und `/cost` zählt alle Läufe zusammen. Der Vergleich wäre schief.

**Wenn ein Modell nicht zur Verfügung steht:** Lass es aus (wie in der Übung).

**Wenn doch `/model` oder `/effort` getippt wurde:** Beide haben deine Wahl als Standard gespeichert. `/model default` holt das Standardmodell deines Kontos zurück, `/effort auto` löscht die gespeicherte Stufe des aktiven Modells.

</details>
