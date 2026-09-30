# Format: Lernprotokolle

> Idee nach Matt Pococks Skill `teach` (github.com/mattpocock/skills, MIT); hier eigene deutsche Fassung für den
> Workshop-Tutor.

Lernprotokolle liegen in `lernprotokoll/` und sind fortlaufend nummeriert: `0001-<slug>.md`, `0002-<slug>.md`, …
(den Ordner erst beim ersten Protokoll anlegen). Sie sind das Gegenstück zu Architektur-Entscheidungen: Sie halten
fest, was die Person **nachweislich** kann oder schon mitbrachte — und damit, was als Nächstes dran ist.

```md
# S2.8: Blockt nur mit exit 2

Die Person hat einen PreToolUse-Hook gebaut, der `git push --force` mit exit 2 blockt, und erklärt, warum ein
abstürzender Hook die Aktion durchlässt. Hooks-Grundlagen müssen nicht wiederholt werden; weiter mit S2.9.

Beleg: Übung in S2.8 selbst gelaufen, Ausgabe gezeigt.
```

Ein Absatz reicht. Optional: `Beleg:` (wie gezeigt) und `Status: ersetzt durch 0007`, wenn sich ein früheres
Verständnis als falsch herausstellt — alte Protokolle nie löschen.

**Schreiben, wenn** die Person etwas Nicht-Triviales nachweislich richtig anwendet, Vorwissen nennt (mit Tiefe:
„seit einem Jahr Hooks im Team"), eine Fehlvorstellung ausgeräumt wurde (besonders wertvoll: sagt künftige
Stolpersteine voraus) oder sich die Mission verschoben hat.

**Nicht schreiben** für bloß gelesenen Stoff („Abdeckung ist kein Lernen"), als Tagebuch oder als Kopie des Kapitels.
