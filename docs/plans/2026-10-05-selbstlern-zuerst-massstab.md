# Selbstlernende zuerst — Maßstab

> Stand: 2026-10-05 · entstanden im Paket P5 am Pilotregal (S0.1, X.2, S1.1 bis S1.9), Commit `359c9db`.
> Entwurf: `2026-10-05-selbstlern-zuerst-design.md` · Pakete: `2026-10-05-selbstlern-zuerst-tickets.md`.
> Diese Datei ist der Auftrag für alle, die weitere Kapitel umschreiben (P7). Die elf Pilotkapitel sind das Muster:
> Lies vor dem Schreiben zwei davon ganz, am besten S1.5 und S1.9.

## Was der Validator durchsetzt

Kapitel, die in `tools/fixtures/standard-chapters.txt` stehen, prüft `python tools/build_library.py validate` zusätzlich:

| Regel | Befund, wenn … |
|---|---|
| `answers-required` | Abruffragen im Check ohne Block „Auflösung“ stehen |
| `answers-count` | die Zahl der Antworten nicht zur Zahl der Fragen passt |
| `exercise-required` | eine Kern-Lektion keinen Abschnitt „Selbst machen“ hat |
| `exercise-shape` | in „Selbst machen“ keine Überschrift `### … (etwa N Minuten)` oder kein „Geschafft, wenn“ steht |
| `minutes-honest` | `minutes` kein Vielfaches von 5 ist oder mehr als 5 von Lesezeit plus Übungen abweicht |

Alles Übrige in dieser Datei kann kein Werkzeug prüfen. Es wird beim Lesen des Diffs geprüft.

## Die Regeln, je mit einem Beispiel aus dem Pilot

### 1 · Ein Kapitel meint eine Person allein

Kein Gruppenformat ohne Einzelfassung, keine Kürzel des Live-Kurses, keine Sätze an Moderierende, keine Notizen
über die Herkunft des Materials. Demo und Sprechpunkte liegen in `resources/moderation/vorfuehren/`.

- Vorher (S1.1): „Jede Person bekommt eine Karte mit 6 Feldern … Wer zuerst alle 6 hat, ruft ‚Bingo‘“; „Übung 1.0“,
  „W1“; S0.1: „Speicherplatz und die Empfehlungen stammen aus der bisherigen Kursanleitung.“
- Nachher (S1.1): „Extra: Befehle entdecken (etwa 5 Minuten)“, vier Befehle, je ein Satz, allein lösbar.

### 2 · Outcome, Übung und Check sind dasselbe dreimal

Das Outcome nennt ein Können. Die Übung übt genau das. Der Check prüft genau das. Verspricht das Outcome etwas, das
viele nicht erreichen können, wird das Outcome geändert, nicht die Leserin.

- Vorher (S1.3): Outcome „eine laufende Terminal-Sitzung mit /desktop an die Desktop-App übergeben“; den Befehl
  gibt es nur unter macOS und x64-Windows mit Abo; keine Übung.
- Nachher (S1.3): Outcome „… sagen, welcher Befehl eine Terminal-Sitzung an die Desktop-App übergibt“; die Übung
  lässt nachsehen, ob `/desktop` auf dem eigenen Rechner erscheint, und drei Situationen zuordnen.

### 3 · Eine Übung hat eine feste Form

Überschrift mit Zeit `(etwa N Minuten)`, dann **Ziel** (ein Satz), **Startzustand** (Ordner, Modus, was schon da sein
muss, und woher es kommt), nummerierte Schritte, zu jedem Schritt mit Wirkung die erwartete Beobachtung, am Ende
**Geschafft, wenn** als Abhakliste aus Dingen, die man sehen kann. Zuordnungs- und Notizaufgaben bekommen einen
eingeklappten „Vergleich“. Freiwilliges heißt „Extra: …“ und trägt seine eigene Zeit.

- Vorher (S1.4): „Frag Claude … `What tools do you have access to?` … Vergleiche sie mit der Tabelle oben.“ Kein
  Startzustand, kein Kriterium.
- Nachher (S1.4): fünf Schritte vom Auftrag über `Ctrl+O` bis zum Abgleich mit der Tabelle, drei Kriterien.

### 4 · Übungen arbeiten im Wegwerf-Ordner

Jede Übung nennt ihren Ordner unter `~/cc-workshop/<thema>` (bisher: `hello`, `werkzeug`, `rechte`, `kontext`).
Nichts an der globalen Konfiguration; Einstellungen kommen in die `.claude/settings.json` des Übungsordners. Was
doch global wäre (ein gespeichertes Standardmodell), umgeht die Übung oder nennt Sicherung und Rückweg.

- Vorher (S1.7, Entwurf): `/model sonnet` in der Sitzung hätte das Standardmodell der Lernenden umgestellt.
- Nachher (S1.7): Start-Flags, die nur für die Sitzung gelten; in `/model` wird gelesen und mit `Esc` geschlossen;
  Schritt 5 prüft, dass der Standard unverändert ist.

### 5 · Die Übung zeigt, was sie zeigen soll

Frag bei jedem Schritt: Könnte Claude zum selben Ergebnis kommen, ohne dass der Lehrinhalt wirkt? Ein Agent liest
Dateien von sich aus, lädt die `CLAUDE.md`, rät plausibel. Gute Übungen machen den Effekt messbar oder unausweichlich.

- Vorher (S1.8): „Which three vulnerabilities are in the access control?“ im Playground, dessen `CLAUDE.md` die
  Antwort enthielt; `/clear` „leert“ sie nicht.
- Nachher (S1.8): ein Türcode, der nur in `notes.txt` steht, die Frage mit „Without using any tools“, und
  „Messages“ in `/context` vor dem `@`-Verweis, danach und nach `/clear` (im Durchlauf: 10, 16.600 und 130 Tokens).

### 6 · Jede Übung wird einmal wirklich durchgespielt

Vor dem Abschluss eines Pakets, in einem Wegwerf-Ordner, mit der Version, die das Kapitel beschreibt. Interaktive
Schritte (Rückfragen, `Shift+Tab`, `/rewind`) laufen in einer tmux-Sitzung, die sich fernsteuern lässt; für Windows
genügt, was sich headless (`claude -p`) und in PowerShell prüfen lässt. Wortlaute der Oberfläche werden abgeschrieben,
nicht erinnert. Was sich nicht durchspielen lässt, steht mit Grund im Paketabschluss. Schreiber spielen nicht selbst
durch; das macht, wer das Paket abnimmt.

- Im Pilot gefunden: der Vertrauensdialog mit vorausgewähltem „No, exit“ (S1.1); `wc -l` läuft ohne Rückfrage, weil
  es ein Lesebefehl ist (S1.4, jetzt Schritt 5 der Übung); `/effort status` nennt auf Haiku eine Stufe, obwohl das
  Tier keinen Effort kennt (S1.7 fragt deshalb dort nicht danach).

### 7 · Der Check prüft das Outcome, und jede Frage hat eine Auflösung

Drei Abruffragen, die zusammen das Outcome abdecken. Die Auflösung: je Frage ein bis drei Sätze, nur was im Kapitel
steht, gleiche Nummer. Das Quiz ist ein Szenario; die falschen Antworten sind echte Befehle mit falscher Wirkung
oder verbreitete Fehlvorstellungen, nie erfundene Befehle; alle vier etwa gleich lang. Quiz und Abruffrage fragen
nicht dasselbe.

- Vorher (S1.9): „`/context --undo` nimmt mehrstufige Änderungen zurück“, „`/compact reset`“: Wer die Befehle nicht
  kennt, erkennt die richtige Antwort daran, dass die anderen nicht existieren.
- Nachher (S1.9): `/compact`, `/clear` und `/context`, je mit der Wirkung, die Lernende ihnen fälschlich zutrauen.

### 8 · Kein Begriff vor seiner Erklärung

Was ein späteres Kapitel einführt, kommt hier nicht als Liste vor. Ist ein Vorgriff nötig, bekommt er einen
Halbsatz Erklärung und den Verweis. Check und Quiz fragen nichts ab, was erst später erklärt wird.

- Vorher (S1.4): „Warum sieht ein Hook auf `Grep` unter macOS keine Suchaufrufe?“ (Hooks: S2.6).
- Nachher (S1.4): „Warum taucht unter macOS in deinem Transkript kein `Grep`-Aufruf auf, obwohl Claude Dateien
  durchsucht?“

### 9 · Ein Bild je Kapitel, ein Wort eine Bedeutung

Bilder aus der Sicherheitstechnik bleiben. Über Kapitel hinweg meint ein Wort immer dasselbe, und ein Bild verspricht
nichts, was die Technik nicht hält. Vor einem neuen Bild in `resources/reference/analogien.md` nachsehen.

- Vorher: „Besucherausweis“ hieß in S1.2 „darf überhaupt ins Gebäude“ und in S1.5 „Modus `default`“. In S1.8 kam
  der verdrängte Feed „ins Archiv“ und ließ sich „zurückholen“; eine Zusammenfassung lässt sich nicht zurückholen.
- Nachher: S1.2 sagt „Hausausweis“, die Stufen gehören den Modi. In S1.8 schreibt der Operator einen Lagebericht
  und schaltet den Feed ab: „Das Bild selbst ist weg.“
- Offen für P7a: S1.12 nennt `--add-dir` einen „Besucherausweis für ein zweites Gebäude“.

### 10 · Sicherheitsaussagen nie stärker als die Doku

Eine Grenze, die Claude Code nicht durchsetzt, wird nicht als Eigenschaft formuliert. Zu jeder Schutzmaßnahme steht,
was sie nicht abdeckt, und wo die härtere Maßnahme steht.

- Vorher (S1.2): „Deine laufenden Panels fasst es aber nicht an.“; S1.6: „in `bypassPermissions` prüft niemand“,
  drei Abschnitte später: Deny-Regeln blocken weiter.
- Nachher (S1.2): „Erreicht dein Benutzerkonto das Panel, kann Claude Code es auch erreichen, sobald du den Befehl
  freigibst oder ein Modus ihn durchwinkt. Die Grenze setzt du …“; S1.6: „prüft fast nichts mehr“, Tabelle
  und Auflösung nennen, was bleibt.

### 11 · Fakten mit Beleg, Versionen nur, wo man sie sieht

Jede neue oder geänderte Aussage über Claude Code hat eine Stelle in der offiziellen Doku; das Zitat steht im
Commit. Was die Doku nicht hergibt, wird gestrichen oder als eigene Vorgabe der Bibliothek gekennzeichnet.
Versionsnummern stehen nur dort, wo Lernende das Verhalten sehen (Startmodus ab 2.1.283); alles andere führt der
Kanon. Zitate von Personen ohne Quelle entfallen.

- Vorher (S0.1): eine Tabelle „Im Kurs genutzt / Dokumentiert ab“ mit fünf Versionsständen; S1.2: ein übersetztes
  Zitat ohne Quelle; S1.7: eine Effort-Tabelle mit eigenen Beispielen.
- Nachher: S0.1 nennt eine Version (2.1.283) und den Grund; S1.7 übernimmt die Beispiele der Doku und sagt das in
  der Spaltenüberschrift („Wann laut Doku“).

### 12 · Ehrliche Zeit

`minutes` = Wörter der gelesenen Abschnitte geteilt durch 160, plus die Minuten aller Übungsüberschriften in
„Im Detail“ und „Selbst machen“, die nicht mit „Extra“ beginnen; auf 5 gerundet. Codeblöcke zählen nicht. So
rechnest du nach:

```bash
python -c "import sys; sys.path.insert(0,'tools'); import library_model as lm; c=lm.parse_chapter(sys.argv[1]); print(lm.reading_words(c), 'Wörter,', lm.exercise_minutes(c), 'Min. Übungen ->', round(lm.honest_minutes(c)), 'Minuten')" resources/library/s1-05-rechte-im-alltag.md
```

Minuten gehören zum Einstufungsvertrag. Wer Kapitel schreibt, meldet den gerechneten Wert; das Frontmatter und den
Vertrag (`docs/migration/chapter-meta.yaml`, Personas, Golden) ändert, wer das Paket abnimmt.

- Vorher: S1.1 trug 12 Minuten bei 15 Minuten Hauptübung; X.2 trug 12 Minuten bei 2.500 Wörtern und drei Übungen.
- Nachher: S1.1 25, X.2 35. Der Schnellstart-Pfad braucht damit 178 Minuten (Warnschwelle 180).

### 13 · Jede Aussage hat ein Heimatkapitel

Was ein anderes Kapitel schon erklärt, bekommt hier einen Satz und den Verweis. Wiederholung ist erlaubt, wenn sie
einmal und kurz als Erinnerung dient.

- Vorher: „Chat berät, Agent handelt“ als eigener Abschnitt in S1.1, S1.2 und S1.3; „default heißt Manual“ fast
  wortgleich in S1.5 und S1.6.
- Nachher: Heimat ist S1.2 bzw. S1.5; S1.3 hat dafür einen Satz unter der Tabelle.

### 14 · Das Fachgebiet ist ein Beispiel, keine Anrede

- Vorher (S1.2): „Zu deinem Fachgebiet gehören Firmware für Zutrittscontroller …“
- Nachher (S1.2): „Ein Beispiel aus der Zutrittstechnik. Angenommen, du arbeitest an Firmware für
  Zutrittscontroller.“ In Übungen: „Das Beispiel stammt aus der Zutrittstechnik … Nimm es, wie es ist, oder ersetz
  Format und Auswertung durch etwas aus deiner eigenen Arbeit.“

### 15 · Beide Shells, und Windows mitdenken

Befehle, die sich unterscheiden, stehen für Bash und PowerShell. Unter Windows führt Claude Shell-Befehle meist über
das PowerShell-Tool aus: Regeln, Erwartungen und Hinweise nennen deshalb beide Werkzeuge.

- Nachher (S1.5): Die Deny-Liste der Übung enthält `Bash(rm *)` und `PowerShell(Remove-Item *)`. Sie hält damit auf
  jedem System; durchgespielt auf Linux und Windows.

### 16 · Demo-Inhalt kommt als Übung zurück, wo er trägt

Die Moderationsdatei des Kapitels ist die erste Quelle für eine Übung. Was dort vorgeführt wird und sich allein in
fünf bis zehn Minuten nachmachen lässt, wird zur Übung nach Regel 3; die Demo-Datei bleibt, wie sie ist.

- Im Pilot: Die Demo zu S1.2 („Describe yourself in exactly 3 bullet points“) trug nicht als Übung, weil Claudes
  Selbstauskunft nichts belegt; an ihre Stelle trat das Ablehnen einer echten Rückfrage.

## Ablauf je Kapitel

1. Kapitel, seine Moderationsdatei und die Befunde der beiden Berichte (Didaktik, Fakten) lesen.
2. Outcome prüfen: Ist es ein Können, das jede Person erreichen kann? Sonst ändern.
3. Übung entwerfen (Regeln 3 bis 5), erst dann den Lehrtext kürzen: Was die Übung nicht braucht und der Check nicht
   prüft, ist Kandidat für einen Verweis.
4. Check schreiben (Regel 7).
5. Zeit rechnen (Regel 12) und melden.
6. `python tools/build_library.py validate --chapter <datei>` ohne Befund. Kein `build`, kein Commit generierter
   Dateien, keine Änderung an `title`, `level`, `requires`, `shelf` oder am Dateinamen.
7. Überschriften unter „Im Detail“ nur umbenennen, wenn kein anderes Kapitel auf ihren Anker verlinkt
   (`grep -rn "<dateiname>#" resources`). Sonst die Überschrift behalten oder den Fund melden.
8. Zurückmelden: je Kapitel die neue Übung in einem Satz, die gerechnete Zeit, jede neue Tatsachenaussage mit
   Doku-Zitat, und was offen blieb.

## Was Schreiber nicht entscheiden

Kapitel teilen oder zusammenlegen, Stufe oder Voraussetzungen ändern, ein Kapitel in ein anderes Regal stellen,
Hook-Vorlagen ändern (die sind getestete Dateien unter `resources/demos/assets/hooks/`). Solche Vorschläge kommen
in die Rückmeldung.

## Aus dem Pilot mitzunehmen

- Übungsordner heißen nach dem Thema. S1.10 und S1.16 nutzen noch `~/cc-workshop/exercises/exercise-1.2` und
  `exercise-1.4-git` (P7a).
- Seit dem Pilot ist nur noch Claude Code, Git und Python vorausgesetzt. Braucht eine Übung den Playground, `gh`,
  `jq` oder Node.js, nennt ihr Startzustand das und verweist auf die Karte
  [Werkstatt erweitern](../../resources/reference/werkstatt-erweitern.md).
- Sitzungen der Übungen starten mit `claude --permission-mode default`, solange die Übung Rückfragen zeigen soll;
  ohne Flag startet eine Sitzung in `auto`.
- Was aus den Demos als Übung zurückkommen soll, steht im Abschluss von P1 in der Paketliste.

## Aus P7a mitzunehmen (S1.10 bis S1.20, Commit `bacbf60`)

Zehn Übungen eines Schreibers wurden durchgespielt; neun liefen wie geschrieben. Was die Läufe gezeigt haben:

- **Die Doku nennt Beschriftungen, die in der Oberfläche anders heißen können.** Die dritte Antwort der
  Plan-Freigabe heißt in der Doku „No, keep planning“, in Version 2.1.289 „Tell Claude what to change“. Wer schreibt,
  zitiert die Doku und sagt dazu, dass es der Wortlaut der Doku ist; die Abnahme gleicht mit der Oberfläche ab.
- **Ein Korrekturschritt muss etwas verlangen, das der erste Entwurf sicher nicht enthält.** „Do not change
  log_reader.py“ bewies nichts, weil Claude die Datei nie anfassen wollte. Jetzt verlangt der Schritt eine Funktion
  an einem bestimmten Ort; das zeigt sich im neuen Plan und im Diff.
- **Ansichten, die sich öffnen, müssen wieder zugehen.** `/cost`, `/permissions`, `/model` und das Menü von `/rewind`
  bleiben offen, bis man `Esc` drückt; der nächste Auftrag landet sonst in der Ansicht. Der Schritt nennt das.
- **Hintergrund-Agenten fragen selbst um Freigabe und brauchen Zeit.** `/review` läuft etwa eine Minute und stellt
  eine Rückfrage; der Schritt kündigt beides an.
- **`/context` zählt die Gedächtnis-Dateien, `/context all` nennt sie.**
- **Anker:** Eine umbenannte Überschrift in S1.17 hinterließ einen toten Link in S4.5. `validate --complete` findet
  das; der Wächter-Test der echten Bibliothek läuft seitdem vollständig.
- **Bewährt am Auftrag:** je Kapitel ein Commit, Rückmeldung mit Doku-Zitaten, Minuten nur als Meldung. Der Auftrag
  steht in `docs/plans/2026-10-05-selbstlern-zuerst-tickets.md` beim Abschluss von P7a.
