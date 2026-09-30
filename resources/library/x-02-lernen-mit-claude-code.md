---
id: X.2
type: community
title: Mit Claude Code lernen
shelf: community
level: bonus
minutes: 12
after: S0.1
requires: []
safety_floor: false
transferable: true
outcome: "Ich kann einen Lernordner mit MISSION.md anlegen, mit dem Workshop-Tutor über start, next, learn, review und guide lernen und prüfen, aus welcher Quelle eine Antwort des Tutors stammt."
sources:
  - https://github.com/mattpocock/skills/tree/main/skills/productivity/teach
  - https://code.claude.com/docs/en/skills
aliases: []
---

# X.2 · Mit Claude Code lernen

<!-- meta:start -->
> **Regal:** [Community & Lernen](README.md#community) · **Stufe:** Kür · **~12 Min** · **Voraussetzungen:** keine
>
> ← [S0.1 Werkstatt einrichten](s0-01-werkstatt-einrichten.md) · [Bibliothek](README.md) · [S1.1 Erster Kontakt: sofort eine Datei bauen](s1-01-erster-kontakt.md) →
<!-- meta:end -->

## Auf einen Blick

Claude Code kann dich beim Lernen begleiten, wenn dein Lernstand in Dateien steht statt im Chat. Matt Pococks Skill `teach` zeigt, wie das geht: eine Mission als Kompass, Lernprotokolle nur für Nachgewiesenes, kurze Lektionen, die dich gerade genug fordern, Abruf mit Abstand statt Wiederlesen und für jede Aussage eine Quelle. Der Workshop-Tutor dieser Bibliothek (`/workshop`) übernimmt diese Bausteine für Claude Code.

Die Grenze: Ein Agent als Lehrer kann sich irren. Der Tutor soll aus den Kapiteln und der offiziellen Doku lehren, nicht aus dem Modellwissen, und du fragst nach, woher eine Antwort stammt.

## Bild im Kopf

Denk an deine Einarbeitung in einer Sicherheitszentrale. Am Anfang steht der Einsatzauftrag: welches Objekt, welche Aufgaben, was ausdrücklich nicht dazugehört. Das ist die Mission. Ins Ausbildungsnachweisheft kommt eine Station erst, wenn du sie am echten Pult vorgeführt hast; die Unterschrift unter der Dienstanweisung zählt nicht. Das sind die Lernprotokolle. Und ob das Wissen hält, zeigt nicht die Wiederholung am selben Nachmittag, sondern die unangekündigte Übung einige Wochen später.

Ein guter Ausbilder schlägt in der gültigen Dienstanweisung nach, statt aus dem Gedächtnis zu zitieren. Genau das verlangt der Tutor von sich: Kapitel und offizielle Doku sind die Dienstanweisung, das Modellwissen ist das Gedächtnis.

## Im Detail

### Die Vorlage: der Skill `teach`

`teach` stammt aus Matt Pococks Sammlung `mattpocock/skills` (MIT-Lizenz, siehe [X.1](x-01-community-skills.md)). Der Skill behandelt Lernen als Vorhaben über mehrere Sitzungen. Das aktuelle Verzeichnis wird zum Lernordner, und der Lernstand steht in Dateien:

| Datei | Inhalt |
|---|---|
| `MISSION.md` | warum du das Thema lernst |
| `learning-records/0001-<name>.md` | was du nachweislich gelernt hast oder schon mitbringst |
| `lessons/0001-<name>.html` | eine Lektion je Datei, eng umrissen |
| `reference/*.html` | die verdichtete Essenz der Lektionen zum Nachschlagen |
| `assets/*` | wiederverwendbare Bausteine der Lektionen, etwa Stylesheet und Quiz-Widgets |
| `RESOURCES.md` | geprüfte Quellen, getrennt nach Wissen und Erfahrung (Communities) |
| `GLOSSARY.md` | die Begriffe, die du schon richtig anwenden kannst |
| `NOTES.md` | deine Vorlieben, wie du lernen willst |

Der Skill setzt `disable-model-invocation: true`: Claude startet ihn nie von selbst, du rufst ihn auf. Aus dem Plugin `mattpocock-skills` lautet der Aufruf `/mattpocock-skills:teach`. Weil der Lernordner das aktuelle Verzeichnis ist, startest du Claude Code für jedes Thema in einem eigenen Ordner.

Die Grundhaltung: Tiefes Lernen braucht Wissen aus vertrauenswürdigen Quellen, Fertigkeiten aus Übungen mit Rückmeldung und Erfahrung aus dem Austausch mit anderen, die dasselbe lernen oder schon anwenden.

### Mission: der Kompass

Jede Lektion hängt an der Mission, dem Grund, warum du lernst. Ist der Grund unklar, fragt `teach` zuerst danach. Die Vorlage hat vier Teile: *Why* (ein bis drei Sätze, das konkrete Ziel), *Success looks like* (Dinge, die du danach beobachtbar kannst), *Constraints* (Zeit, Budget, Vorlieben) und *Out of scope* (was du bewusst nicht verfolgst). Die Regeln:

- **Eine Mission je Lernordner.** Zwei unabhängige Themen sind zwei Ordner.
- **Konkret statt abstrakt.** „Ship a Rust CLI to my team" statt „learn Rust".
- **Bei Vagheit nachfragen.** Lässt sich das Warum nicht sagen, gibt es erst ein Gespräch, dann die Datei.
- **Anpassen, wenn sich das Ziel verschiebt**, nach Rückfrage und mit einem Lernprotokoll dazu.
- **Kurz halten.** Passt die Mission nicht mehr auf einen Bildschirm, ist sie ein Plan und kein Kompass mehr.

### Lernprotokolle: nur, was belegt ist

Lernprotokolle (im Original *learning records*) sind das Gegenstück zu Architektur-Entscheidungen (ADRs): ein bis drei Sätze, was jetzt bekannt ist und warum das ändert, was als Nächstes dran ist. Eines entsteht, wenn

1. du etwas Nicht-Triviales nachweislich richtig anwendest,
2. du Vorwissen nennst, samt Tiefe,
3. eine Fehlvorstellung ausgeräumt wurde (besonders wertvoll, weil sie künftige Stolpersteine voraussagt), oder
4. sich die Mission durch das Lernen verschoben hat.

Kein Lernprotokoll gibt es für bloß durchgenommenen Stoff. Der Satz dazu im Original: „Coverage is not learning." Widerspricht ein späteres Protokoll einem früheren, wird das alte als ersetzt markiert statt gelöscht; auch der Weg des Verstehens ist ein Signal.

### Die Zone der nächsten Entwicklung

Jede Lektion soll dich „just enough" fordern. Nennst du kein Thema, ermittelt `teach` es aus deinen Lernprotokollen und deiner Mission und nimmt das Relevanteste, was in diese Zone passt. Lektionen sind kurz, weil das Arbeitsgedächtnis klein ist, und jede bringt einen greifbaren Erfolg, auf dem die nächste aufbaut.

### Abruf und Abstand: Speicherstärke statt Scheingewandtheit

`teach` unterscheidet zwei Arten von Stärke. **Abrufflüssigkeit** (*fluency strength*) ist, was dir im Moment leicht einfällt. **Speicherstärke** (*storage strength*) ist, was du langfristig behältst. Abrufflüssigkeit kann dir Können vortäuschen, eine Scheingewandtheit; das eigentliche Ziel ist Speicherstärke. Dafür setzt der Skill auf erwünschte Schwierigkeit:

- **Abrufübung:** aus dem Gedächtnis antworten, nicht nachlesen.
- **Abstand:** Übung über die Zeit verteilen.
- **Mischen:** verwandte Themen abwechselnd üben, nur bei Fertigkeiten.

Beim Erwerb von Wissen ist Schwierigkeit dagegen der Feind, weil sie das Arbeitsgedächtnis frisst. Fertigkeiten übst du in einer Rückmeldeschleife, die so eng und so automatisch wie möglich sein soll.

### Gleich lange Quizantworten

Für Quizfragen verlangt `teach`, dass jede Antwortoption genau gleich viele Wörter hat, möglichst auch gleich viele Zeichen, und dass die Formatierung keinen Hinweis gibt. Sonst lernst du, die Form der richtigen Antwort zu erkennen, nicht den Stoff. Diese Bibliothek übernimmt die Regel mit Toleranz: Der Validator meldet ein Quiz, wenn die richtige Antwort mehr als 1,35-mal so lang ist wie die falschen im Mittel oder eine falsche kürzer als 0,6-mal die richtige. Über die ganze Bibliothek darf die richtige Antwort in höchstens 40 % der Fragen die längste sein.

### Primärquellen statt Modellwissen

Der härteste Satz im Skill lautet: „Never trust your parametric knowledge." Was das Modell gelernt hat, ist kein Beleg. `teach` sammelt deshalb zuerst vertrauenswürdige Quellen in `RESOURCES.md`: jede mit einer Zeile, wofür sie taugt, Lücken ausdrücklich benannt, Schwaches konsequent aussortiert. Lektionen sollen voller Belege stecken, und jede empfiehlt eine Primärquelle, die beste, die sich finden ließ.

### Community für Erfahrung

Erfahrung (*wisdom*) entsteht nur im echten Einsatz. Stellst du eine Frage, die Erfahrung braucht, versucht `teach` eine Antwort, verweist dich am Ende aber an eine Community: ein Forum, eine Gruppe, einen Kurs vor Ort. Willst du keiner beitreten, wird das respektiert und in `RESOURCES.md` festgehalten.

### So setzt der Workshop-Tutor das um

Der Tutor ist ein Skill im Plugin dieser Bibliothek. Er übernimmt die Grundidee von `teach`: Lernordner als Gedächtnis, Mission als Kompass, Lernprotokolle für den nächsten Schritt, Abruf mit Abstand. Der Unterschied: Lektionen schreibt der Tutor nicht selbst. Er führt dich durch die Kapitel der Bibliothek, und welches Kapitel als Nächstes dran ist, rechnet die Einstufung (`tools/placement.py`) aus deinen Antworten aus.

Das Plugin lädst du mit:

```bash
claude --plugin-dir ~/cc-workshop/dynamic-workshop
```

Plugin-Skills tragen den Plugin-Namen als Präfix. Der volle Aufruf ist `/dynamic-workshop:workshop <modus>`, hier kurz `/workshop <modus>`:

| Aufruf | Was passiert |
|---|---|
| `/workshop` | Übersicht: die Regale, drei Wege (Einstufung, Live-Pfad, Stöbern) und die Aufrufe |
| `/workshop start` | Lernordner anlegen (Vorschlag `~/cc-workshop/lernen`), Mission im Gespräch, Einstufung nach Ziel, Zeit und Stand, optional und nur mit deinem Ja ein lesender Blick auf dein Setup; daraus `lernpfad.md` und Lernprotokolle für genanntes Vorwissen |
| `/workshop next` | das nächste offene Kapitel deines Pfads, im Ablauf seines Kapiteltyps |
| `/workshop learn <ID>` | ein bestimmtes Kapitel, etwa `S2.8` oder `X.1`; alte Modulnummern wie `2.2` gehen auch |
| `/workshop review` | Abruf mit Abstand über erledigte Kapitel |
| `/workshop guide <ID>` oder `guide S1` bis `S4` | Moderationsmodus: Ablauf, Zeiten, Demo und Hinweise „Für Moderierende" |

Im Lernordner liegen:

| Datei | Inhalt |
|---|---|
| `MISSION.md` | warum du lernst, im Format aus „Selbst machen" |
| `einstufung.json` | deine Antworten aus der Einstufung |
| `lernpfad.md` | der berechnete Pfad, bei jeder Änderung neu erzeugt |
| `fortschritt.json` | erledigte Kapitel mit Datum und das zuletzt bearbeitete |
| `lernprotokoll/0001-<slug>.md` | die Lernprotokolle |
| `NOTIZEN.md` | deine Vorlieben und die Liste „wiederholen" |

So kehren die Bausteine im Tutor wieder:

- **Mission:** eine deutsche Fassung der Vorlage mit Warum, Daran merke ich es, Rahmen und Bewusst nicht. Bleibt deine Antwort vage, fragt der Tutor einmal konkret nach: „Bei welcher Aufgabe diese Woche?"
- **Lernprotokolle:** nur bei Evidenz, etwa wenn du beide Schnellcheck-Fragen sicher beantwortest oder die Übung gelaufen ist. Erledigt ist ein Kapitel erst, wenn du es sagst oder die Übung gelaufen ist. So sieht ein Protokoll aus:

```md
# S2.8: Blockt nur mit exit 2

Die Person hat einen PreToolUse-Hook gebaut, der `git push --force` mit exit 2 blockt, und erklärt, warum ein
abstürzender Hook die Aktion durchlässt. Hooks-Grundlagen müssen nicht wiederholt werden; weiter mit S2.9.

Beleg: Übung in S2.8 selbst gelaufen, Ausgabe gezeigt.
```

- **Zone der nächsten Entwicklung:** Die Einstufung gibt jedem Kapitel einen Status (`work`, `skim`, `skip` oder `later`). `next` nimmt das erste Kapitel mit `work` oder `skim`, das noch nicht erledigt ist.
- **Abruf und Abstand:** `review` wählt bis zu fünf erledigte Kapitel, die am längsten nicht gesehenen zuerst, mischt die Themen und fragt ohne vorherige Erklärung. Sitzt eine Antwort nicht, kommt das Kapitel in `NOTIZEN.md` unter „wiederholen".
- **Abruf vor Quiz:** Im Check stellt der Tutor erst die Abruffragen des Kapitels ohne Spickzettel, dann das Quiz mit gemischten Optionen.
- **Primärquelle:** Am Ende jedes Kapitels nennt der Tutor die Hauptquelle, die erste unter `sources`, und den Pfad zur Kapiteldatei.
- **Selbst machen statt zusehen:** Du arbeitest in deinem eigenen Terminal. Der Tutor gibt den Auftrag Schritt für Schritt, Hinweise nur auf Wunsch, und prüft nur, was du zeigst oder freigibst.

### Grenzen eines Agenten als Lehrer

- **Modellwissen ist kein Beleg.** Der Tutor lehrt deshalb nur aus Katalog und Kapiteln. Fehlt der Katalog oder ein Kapitel, meldet er das als Fehler („Das Kapitel S2.8 fehlt in dieser Installation — bitte das Plugin aktualisieren") und unterrichtet nicht aus dem Gedächtnis weiter.
- **Fragen über das Kapitel hinaus:** Dann prüft der Tutor die offizielle Doku (`curl -sL https://code.claude.com/docs/en/<seite>.md`) und sagt dir, dass die Antwort von dort stammt. Fehlt dieser Hinweis, frag nach: „Woher stammt das?"
- **Auch geprüfter Text kann falsch sein.** Diese Bibliothek hat das selbst erlebt. Der alte Kurs lehrte Hooks, die mit `exit 1` blocken sollten, und zwei große Reviews übersahen den Fehler, weil sie Text gelesen und keinen Hook ausgeführt haben. Erst der Abgleich mit der offiziellen Hooks-Referenz zeigte, dass nur `exit 2` blockt ([S2.8](s2-08-hook-einrichten.md)). Der Maßstab ist die Quelle und der eigene Versuch, nicht ein zweiter Text.
- **Der Tutor sieht nur, was du zeigst.** Ob du etwas kannst, belegt deine Übung im Terminal, nicht ein Gespräch darüber. Der Tutor ist dabei kein Prüfer: keine Noten, „weiß nicht" ist immer eine gute Antwort.
- **Eingebaut oder selbst gebaut:** Der Tutor unterscheidet eingebaute Funktionen von eigenen Workshop-Bausteinen (🔧). Frag nach, wenn du es nicht erkennst.
- **Erfahrung kommt von Menschen.** Wie sich ein Werkzeug im Alltag bewährt, lernst du von denen, die es einsetzen. Dafür verweist `teach` an Communities.

## Selbst machen

### Übung 1: deine Mission schreiben

Leg einen Lernordner an, etwa `~/cc-workshop/lernen`, und schreib darin `MISSION.md` nach dieser Vorlage des Tutors:

<!-- cockpit:example -->
```md
# Mission: Claude Code

## Warum
Ein bis drei Sätze: das konkrete Ziel. Was ändert sich in der Arbeit, wenn es klappt?
Nicht „Claude Code verstehen", sondern z. B. „Unsere Code-Reviews mit Claude beschleunigen, ohne Secrets zu riskieren".

## Daran merke ich es
- eine konkrete, beobachtbare Sache, die ich danach kann
- noch eine

## Rahmen
- Zeit, Rechte im Job, erlaubte Werkzeuge, Vorlieben

## Bewusst nicht
- Themen, die ich gerade nicht verfolge (schützt vor Überforderung)
```

Prüf die Datei dann gegen die Regeln: Steht unter „Warum" ein konkretes Ziel statt „Claude Code verstehen"? Kannst du jeden Punkt unter „Daran merke ich es" beobachten? Steht unter „Bewusst nicht" mindestens ein Thema? Passt alles auf eine Bildschirmseite?

### Übung 2: mit dem Tutor starten

Lade das Plugin wie oben (die Einrichtung steht in der [Anleitung](../../HOW-TO-USE.md)) und ruf `/dynamic-workshop:workshop start` auf. Nenn als Lernordner den Ordner mit deiner `MISSION.md`. Findet der Tutor die Mission, fragt er, ob du weitermachen, anpassen oder neu beginnen willst. Geh die Einstufung durch und öffne danach `lernpfad.md`: Welche Kapitel stehen in der ersten Etappe, und mit welcher Begründung?

### Übung 3: die Quelle prüfen

Stell dem Tutor eine Frage, die über das aktuelle Kapitel hinausgeht, etwa: „Welche Hook-Ereignisse gibt es außer PreToolUse?" Frag danach: „Woher stammt das?" Eine gute Antwort nennt ein Kapitel oder eine Seite der offiziellen Doku. Nennt sie keine Quelle, bitte den Tutor, die Seite mit `curl -sL https://code.claude.com/docs/en/hooks.md` zu lesen und die Stelle zu zitieren.

### Später: Abruf mit Abstand

Nach ein paar Tagen: `/dynamic-workshop:workshop review`. Beantworte die Fragen, ohne vorher nachzulesen. Was nicht sitzt, merkt sich der Tutor zum Wiederholen.

**Geschafft, wenn:**

- [ ] `MISSION.md` in deinem Lernordner liegt und auf eine Bildschirmseite passt
- [ ] `lernpfad.md` erzeugt ist und du dein nächstes Kapitel kennst
- [ ] du bei einer Antwort des Tutors die Quelle erfragt und nachgeprüft hast

## Typische Fallen

- **Mission zu allgemein.** „Besser mit Claude Code werden" lenkt keine einzige Entscheidung. Frag dich: Bei welcher Aufgabe diese Woche?
- **Lesen für Lernen halten.** Ein gelesenes Kapitel ist kein Lernprotokoll wert. Erst die gelaufene Übung oder der sicher beantwortete Schnellcheck zählt.
- **Wiederlesen statt Abrufen.** Wiedererkennen fühlt sich nach Können an. `review` fragt deshalb ohne vorherige Erklärung.
- **Zwei Themen in einem Lernordner.** Eine Mission je Ordner; für ein zweites Thema legst du einen zweiten Ordner an.
- **Der Tutor unterrichtet ohne Kapitel.** Fehlt der Katalog oder ein Kapitel, soll der Tutor das melden. Lehrt er trotzdem weiter, vertrau der Antwort nicht und aktualisiere das Plugin.

## Check

Du kannst erklären, warum ein Lernprotokoll erst nach einem Nachweis entsteht und warum Abruf mit Abstand mehr festigt als Wiederlesen, und du prüfst bei einer Antwort des Tutors, aus welcher Quelle sie stammt.

1. Welche vier Anlässe rechtfertigen ein Lernprotokoll, und welcher häufige Anlass gerade nicht?
2. Was unterscheidet Abrufflüssigkeit von Speicherstärke, und welche der beiden täuscht?
3. Was soll der Tutor tun, wenn ein Kapitel in seiner Installation fehlt?

## Weiterlesen

- [Der Skill `teach` von Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach), mit den Formatdateien für Mission, Lernprotokolle, Quellen und Glossar
- [Skills in Claude Code](https://code.claude.com/docs/en/skills)
- [Anleitung: selbst lernen und den Tutor laden](../../HOW-TO-USE.md)
- [Der Tutor-Skill im Wortlaut](../../skills/workshop/SKILL.md)
- [S0.1 · Werkstatt einrichten](s0-01-werkstatt-einrichten.md)
- [X.1 · Community-Skills: wer baut was, das wirklich hilft](x-01-community-skills.md)
- [S2.2 · Eine SKILL.md schreiben](s2-02-skill-schreiben.md)
