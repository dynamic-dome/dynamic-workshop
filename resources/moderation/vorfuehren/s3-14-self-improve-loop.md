# Vorführen: S3.14 · Self-Improve-Loop: was geht und wo es endet

> Demo und Hinweise für Moderierende zum Kapitel [S3.14 · Self-Improve-Loop: was geht und wo es endet](../../library/s3-14-self-improve-loop.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: aus einem Fehler eine Regel machen (etwa 12 Minuten)

**Ziel:** Das Muster eines Self-Improve-Loops im Kleinen zeigen: Ein Lauf verstößt gegen eine Konvention, die nur du kennst, du hältst sie als eine Zeile in `CLAUDE.md` fest, und ein zweiter Lauf wendet sie an. Ein Mensch liest die Regel und den Diff.

Zeig die Übung aus dem Kapitel live: die Übung „aus einem Fehler eine Regel machen und prüfen“ in [S3.14](../../library/s3-14-self-improve-loop.md). Startzustand wie dort: das Repository `~/cc-workshop/lernregel` mit der fast leeren `shop.py` und einem Startcommit. Leg es vorher an. Ablauf: Schritte 1 bis 7 der Übung (Lauf 1 ohne Regel, Funktionsnamen ablesen, `CLAUDE.md` mit genau einer Regel, `git restore shop.py`, Lauf 2 in einer neuen Sitzung, vergleichen, die Regel als Fremder lesen). Starte beide Läufe mit `claude --permission-mode acceptEdits`.

Wer mehr Automatik zeigen will, sagt vorher laut, welche Grenze steht: Ein Budget und ein Rundenlimit wirken nur in `-p`-Läufen und nicht in einer interaktiven Sitzung ([S3.13](s3-13-autonome-loops-absichern.md)).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 12 Minuten geplant; halte live etwa 18 Minuten frei (× 1,5), weil die Läufe schwanken.

**Sagen:**

- Nach Schritt 2: „Claude kann die Konvention nicht erraten. Die Namen beginnen nicht mit `shop_`. Das ist der Fehler, den ich an einer Stelle ablesen kann."
- Schritt 3: „Die Gegenmaßnahme muss sich prüfen lassen: eine Zeile, konkret, kurz. Je konkreter und kürzer, desto zuverlässiger folgt Claude."
- Schritt 5: „Dasselbe in einer neuen Sitzung, denn die `CLAUDE.md` wird beim Start geladen."
- Schritt 6: „Jeder Name beginnt mit `shop_`: Das habe ich gemessen, nicht geglaubt." Danach die Einschränkung: Eine Regel in `CLAUDE.md` ist Kontext, keine erzwungene Konfiguration; sie macht das Verhalten wahrscheinlicher, nicht sicher. Was in jedem Fall verhindert werden muss, blockt ein PreToolUse-Hook ([S2.8](s2-08-hook-einrichten.md)).
- Schritt 7: „Ich habe die Regel eben mit einem `grep` nachgeprüft. Eine Regel, die ich so nicht nachprüfen kann, taugt nicht als Beleg. Und eine Regel, die nie ein Mensch gelesen hat, ist eine Behauptung."
- Was schiefgehen kann: Schein-Fixes (ein Test wird repariert, indem die Assertion entfällt; der Testlauf bleibt grün, der Fehler bleibt), falsche Regeln (Claude befolgt sie auch dann), zu viel Vertrauen in kleine Stichproben. Zeig die Extra-Übung „eine falsche Regel“, wenn Zeit bleibt.
- Wo es endet: „Ein autonomer Verbesserungskreislauf gehört in ein Repository, in dem sich jede Änderung zurücknehmen lässt. Wo ein Fehler echte Geräte oder Daten trifft, steht eine menschliche Freigabe davor ([S3.8](s3-08-rechte-fuer-autonomie.md))."

**Wenn Lauf 1 schon mit `shop_` beginnt:** Nimm als Konvention stattdessen das Präfix `cart_` und schreib es überall, wie in Schritt 2 und 3 der Übung beschrieben.

**Wenn Lauf 2 die Regel nicht befolgt:** Das ist möglich, denn eine Regel in `CLAUDE.md` ist keine Sperre. Benutz es als Lehrmoment und nenne den Hook als Weg, wenn es in jedem Fall gelten muss.

</details>
