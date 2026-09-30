# Moderations-Handbuch

> Für alle, die den Workshop live moderieren. Dieses Handbuch ist die einzige Quelle für Ablauf, Begründung der
> Zeiten und Live-Format. Welche Kapitel in welcher Session laufen, mit Stufe und Minuten, steht im generierten
> [Live-Pfad](../paths/live-workshop.md). Inhalt, Demo und Sprechpunkte stehen in den Kapiteln der
> [Bibliothek](../library/README.md). Was du vorher installierst und prüfst: [vorbereitung.md](vorbereitung.md).
>
> Stand: 2026-09-30.

## Inhalt

- [Format: vier Sessions](#format-vier-sessions)
- [Drei Stufen: was live läuft](#drei-stufen-was-live-läuft)
- [Rhythmus statt Streichen](#rhythmus-statt-streichen)
- [Die vier Sessions im Einzelnen](#die-vier-sessions-im-einzelnen)
- [Demos realistisch planen](#demos-realistisch-planen)
- [Live-Format: drei Personen, drei Rollen](#live-format-drei-personen-drei-rollen)
- [Abrufen: Recall und Quick-Checks](#abrufen-recall-und-quick-checks)
- [Transfer ins eigene Repo](#transfer-ins-eigene-repo)
- [Selbstwirksamkeits-Check](#selbstwirksamkeits-check)
- [Pre-Flight am Workshop-Tag](#pre-flight-am-workshop-tag)
- [Go/No-Go je Demo](#gono-go-je-demo)
- [Typische Fehlerbilder live](#typische-fehlerbilder-live)
- [Notfallplan: wenn alles brennt](#notfallplan-wenn-alles-brennt)
- [Einladung (Vorlage)](#einladung-vorlage)
- [Sprechpunkte je Kapitel](#sprechpunkte-je-kapitel)

## Format: vier Sessions

Der Workshop läuft in vier Sessions zu je etwa drei Stunden.

| Session | Thema | Rolle im Ablauf |
|---|---|---|
| 1 | Erste Schritte mit dem Agenten, sanfter Einstieg | Grundlagen |
| 2 | Das Ökosystem: Skills, Hooks, Plugins, MCP, RAG | Erweitern und kontrollieren |
| 3 | Fortgeschritten, Kern: Agenten, Sicherheit, Automatisierung | Pflicht-Kern des fortgeschrittenen Teils |
| 4 | Fortgeschritten, Kür: Multi-Model, CI/CD, Abschlussprojekt, Fehlersuche | Überlauf als eigener, vollwertiger Termin |

**Warum vier Sessions?** Der fortgeschrittene Teil war früher ein einziger Block mit rund 270 Minuten Inhalt für
einen 180-Minuten-Termin. Der ehrliche Schnitt trennt den Pflicht-Kern (Session 3) vom Überlauf (Session 4) und
macht daraus zwei vollwertige Termine.

**Rohe Minuten, nicht schöngerechnet.** Der Live-Pfad nennt je Session die Summe der Kapitel-Minuten, getrennt nach
Kern, Vertiefung und Kür. Das ist bewusst die ehrliche Roh-Zahl. Ein 180-Minuten-Termin fasst nach Deck-Einstieg,
Pause und Fragen netto etwa 140–150 Minuten Lehrzeit. In den Sessions 1 bis 3 liegt schon die Kern-Summe darüber, in
Session 1 am deutlichsten (beim Umbau 213 Minuten). Die Differenz fängst du durch Rhythmus ab und, wenn der Termin
fest ist, durch Straffen.

## Drei Stufen: was live läuft

Jedes Kapitel trägt eine Stufe (`level` im Frontmatter).

| Stufe | Bedeutung | Im Live-Workshop |
|---|---|---|
| Kern (`core`) | Pflichtpfad: was alle können müssen | Immer gefahren. Weil die Kern-Minuten über der Netto-Lehrzeit liegen, kürzt du Demo-Puffer und behandelst die weichsten Kern-Kapitel flexibel (Hinweise je Session unten). |
| Vertiefung (`deep-dive`) | Optionale Vertiefung desselben Themas | „Wenn Zeit, dann zeigen": eingeplant und gefahren, solange das Zeitbudget reicht, sonst Lesestoff. |
| Kür (`bonus`) | Ausblick und Showcase, oft eigene Workshop-Bausteine (🔧) und experimentelle Funktionen | Nur bei Zeitüberschuss oder auf Nachfrage. |

Vertiefungen streichst du erst, wenn der Kern sonst nicht in den Termin passt, nicht von vornherein.

**Pflicht je Session:** alle Kern-Kapitel, die Hauptdemos und mindestens eine Übung aus der Praxis-Station. Sind drei
Personen im Raum, hat das [Live-Format](#live-format-drei-personen-drei-rollen) Vorrang: Fortschrittsanzeige und Quiz
im Cockpit sind Nachbereitung für Selbstlernende, nicht der Taktgeber im Raum.

**Jedes Kapitel folgt demselben Muster:**

1. Konzept verstehen: „Auf einen Blick", „Bild im Kopf", „Im Detail".
2. Live-Demo sehen: „Vorführen". Die Demo geht vor den Folien.
3. Selbst ausprobieren: „Selbst machen" oder die Praxis-Station der Session.
4. Transfer ins eigene Repo: zehn Minuten am Ende der Session ([Transfer](#transfer-ins-eigene-repo)).
5. Absichern: „Check" im Kapitel und danach die Referenzkarten in `resources/reference/`.

Die Analogien aus der physischen Sicherheit („Bild im Kopf") ziehen sich durch alle Sessions.

## Rhythmus statt Streichen

- **Pausen:** pro Session etwa 10–15 Minuten Pause nach etwa 90 Minuten, dazu Fragen zwischen den Kapiteln.
- **Termin-Länge:** Für die Live-Kohorte ist sie kein harter Rahmen. Vollständigkeit geht vor dem Einpassen in einen
  Slot; die Sessions laufen so lang wie nötig, mit Pausen. Die Minuten im Live-Pfad sind Signale für Tempo und Pausen
  und das Budget fürs Selbststudium, kein Zwang zum Kürzen.
- **Das eigentliche Problem ist Ermüdung.** Mehr als 200 Kern-Minuten am Stück wie in Session 1 sind zu viel auf
  einmal. Die Antwort ist Rhythmus, nicht Streichen: In Session 1 machst du nach etwa S1.6 und nach etwa S1.14 je
  eine Pause mit zwei Abruffragen.
- **Fester 180-Minuten-Termin:** Dann straffst du nach den Hinweisen der jeweiligen Session unten.

## Die vier Sessions im Einzelnen

Jede Session hat dasselbe Gerüst:

1. Selbstwirksamkeits-Check, Eingang: vor der ersten Folie ([Check](#selbstwirksamkeits-check)).
2. Einstieg: Session 1 mit dem Deck (`resources/media/claude-code-praxisbibliothek.pptx`), Session 2 bis 4 mit dem
   5-Minuten-Recall ([Recall](#abrufen-recall-und-quick-checks)), danach das Deck.
3. Die Kapitel in der Reihenfolge des [Live-Pfads](../paths/live-workshop.md), mit Pausen und Quick-Checks.
4. Die Praxis-Station: mindestens eine Übung.
5. Der Transfer-Beat: zehn Minuten.
6. Selbstwirksamkeits-Check, Ausgang: in den letzten fünf Minuten.

### Session 1: Erste Schritte

**Mission:** „Was ist Claude Code, wie steuere ich es, wie arbeite ich sicher mit Git — und behalte die Kosten im
Blick?" Sanfter Einstieg: In den ersten rund 36 Minuten (S1.1 bis S1.3) hat, wer neu ist, schon etwas gebaut, bevor
es um Freigabestufen geht.

- **Der vollste Termin.** Die Kern-Kapitel ergeben beim Umbau 213 Minuten. Hier musst du am stärksten straffen, wenn
  der Termin fest ist.
- **S1.6 bleibt Kern.** [Alle Rechte-Modi im Überblick](../library/s1-06-rechte-modi.md) ist bewusst Kern und keine
  Vertiefung: Die Zielgruppe, Profis aus der physischen Sicherheit, will die Freigabestufen früh vollständig sehen.
  Die sechs Modi opferst du auch beim Straffen nicht.
- **Rhythmus:** je eine Pause mit zwei Abruffragen nach etwa S1.6 und nach etwa S1.14.
- **Straffen, falls nötig:** die [Praxis-Station S1.20](../library/s1-20-praxis-station-1.md) kurz halten,
  [S1.9](../library/s1-09-kontext-steuern.md) straffen, notfalls [S1.4](../library/s1-04-werkzeuge.md) mit
  [S1.3](../library/s1-03-oberflaechen.md) bündeln.
- **Kosten am ersten Tag:** [S1.19](../library/s1-19-kosten-im-blick.md) bleibt Kern: `/cost`, `/usage`,
  Budgetgrenze und ein 5-Minuten-Beat zu Caching, Effort-Stufen und Modell pro Phase. Pipeline-Ökonomie, `/insights`,
  die vollständigen Spar-Taktiken und die Anti-Patterns kommen erst in
  [S4.4](../library/s4-04-ci-zugang-und-kosten.md) bei den CI-Budgetgrenzen. Der Grund: Wer neu ist, kann die
  Ökonomie einer Pipeline ohne Praxisgefühl nicht einordnen, und Budgetgrenzen werden erst bei autonomen Loops und in
  CI wichtig.
- **Quick-Checks** nach S1.6 und S1.10, **Transfer** S1-T.
- **Mitbringen:** Laptop mit installiertem `claude`, GitHub-Konto, ein eigenes unkritisches Repo für den Transfer.
  **Vorher erledigt:** [S0.1 Werkstatt einrichten](../library/s0-01-werkstatt-einrichten.md).

### Session 2: Das Ökosystem

**Mission:** „Wie erweitert und kontrolliert man Claude Code?" Skills, Hooks, Plugins, MCP, RAG.

- **Einstieg:** Recall aus Session 1, danach das Deck.
- **Straffen, falls nötig:** Der Kern (beim Umbau 177 Minuten) ist auf etwa 145 Minuten fahrbar. Elastisch sind
  [S2.2](../library/s2-02-skill-schreiben.md) und die [Praxis-Station S2.20](../library/s2-20-praxis-station-2.md).
- **Quick-Check** nach [S2.10](../library/s2-10-hook-ausgaben.md), wenn du diese Vertiefung fährst. **Transfer** S2-T.
- **Mitbringen:** Setup aus Session 1, Playwright-Browser, NotebookLM-Konto, Transfer-Repo. **Vorher erledigt:**
  Workshop-Plugins installiert ([vorbereitung.md](vorbereitung.md#workshop-plugins)).

### Session 3: Fortgeschritten, Kern

**Mission:** „Spezialisierte Agenten, automatisierte Security-Prüfung, sichere Automation."

- **Einstieg:** Recall aus Session 2, danach der Live-Anker, dann Deck und Demos.
- **Live-Anker:** Du öffnest mit einem 60-Sekunden-Moment, der garantiert live klappt: dem ersten Schritt der
  Headless-Demo, `claude -p "Summarize what this repo does in one sentence."`. Er braucht nur das lokal installierte
  `claude`, kein Plugin, kein Codex, keine Bridge. Die meisten Demos der Sessions 3 und 4 hängen an etwas Externem
  (eigene Plugins, Codex CLI, Websuche, Telegram-Bridge). Scheitert eine davon früh vor Publikum, wirkt der ganze
  Termin wackelig. Mit dem Anker hast du schon einen sauberen Live-Erfolg, bevor die schwereren Demos kommen. Die
  Schritte stehen in [S3.1](../library/s3-01-was-ist-ein-agent.md) unter „Vorführen"; die volle Headless-Demo läuft
  in Session 4 in [S4.3](../library/s4-03-headless.md).
- **Am Morgen:** die [Go/No-Go-Matrix](#gono-go-je-demo) abhaken.
- **Straffen, falls nötig:** Der Kern (beim Umbau 157 Minuten) ist auf etwa 145 Minuten fahrbar. Elastisch sind
  [S3.3](../library/s3-03-eigener-subagent.md) und die [Praxis-Station S3.15](../library/s3-15-praxis-station-3.md).
- **Quick-Check** nach [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md), **Transfer** S3-T.
- **Mitbringen:** Setup aus Session 2, Transfer-Repo. **Vorher erledigt:** Workshop-Playground geklont.

### Session 4: Fortgeschritten, Kür

**Mission:** „Multi-Model, CI/CD, die volle Architektur — und souverän debuggen." Der Überlauf des fortgeschrittenen
Teils als eigener Termin. Hier kommt auch das verschobene Kosten-Thema zurück, bei den CI-Budgetgrenzen in
[S4.4](../library/s4-04-ci-zugang-und-kosten.md).

- **Kern ist nur die Fehlersuche.** [S4.9](../library/s4-09-fehlersuche-werkzeuge.md) und
  [S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md) sind Pflicht, weil alle sie brauchen. Alles andere
  läuft nach Zeitbudget; der volle Track läuft realistisch nie komplett.
- **Ohne vierten Termin:** S4.9 und S4.10 (zusammen 33 Minuten) ans Ende von Session 3 hängen und dafür die
  Vertiefungen von Session 3 streichen. Der Rest von Session 4 wird ein strukturierter Track fürs Selbststudium.
- **Einstieg:** Recall aus Session 3, danach das Deck.
- **Am Morgen:** die [Go/No-Go-Matrix](#gono-go-je-demo) abhaken, Teil Session 4.
- **Abschlussprojekt:** [S4.8](../library/s4-08-abschlussprojekt.md) mit Aufgabe, Rubrik und Ablauf; danach der
  Quick-Check zur Übergabe.
- **Transfer** S4-T mit dem Adoptionsplan.
- **Mitbringen:** Setup aus Session 3, Transfer-Repo, Codex CLI, falls verfügbar (für
  [S4.2](../library/s4-02-codex-schwarm.md)). **Vorher erledigt:** optional ein CI-Repo mit GitHub Actions zum
  Mitschreiben; die Vorlage für den Adoptionsplan liegt bereit.

**In allen Sessions** hast du ein vorbereitetes `~/cc-workshop`-Bundle auf einem USB-Stick dabei, als Ersatz bei
einem kaputten Setup ([Fehlerbilder](#typische-fehlerbilder-live)).

## Demos realistisch planen

- Jeder Demo-Slot ist Demo plus Sprechpunkte plus 2–3 Minuten Puffer. Live-Demos laufen immer langsamer als das
  Skript.
- Faustregel: Die im Kapitel genannte Dauer meint den reinen Ablauf ohne Publikum. Plane real das 1,5-Fache ein.
- Schritte, die als „Bonus", „Stretch" oder „wenn Zeit" markiert sind, zählen nicht zur Slot-Zeit. Wird es knapp,
  streichst du zuerst sie. Der Kern jeder Demo passt in den Slot, die Boni nicht.

## Live-Format: drei Personen, drei Rollen

Das Format ist für drei erfahrene Entwicklerinnen und Entwickler im Raum gedacht, ohne daraus einen Selbstlernkurs zu
machen. Die Kapitel-Landkarte bleibt dein Gerüst und der Pfad der Selbstlernenden; live arbeitest du mit Gespräch,
Pair-Driving und kurzen sokratischen Fragen.

**Grundform:**

1. **Sehen:** Du zeigst den Schritt im Deck oder in der Demo.
2. **Fahren:** Eine Person bedient Claude Code im Playground.
3. **Laut denken:** Die fahrende Person sagt vor dem Enter, was Claude ihrer Erwartung nach tun wird.
4. **Navigieren:** Die zweite Person achtet auf Umfang, Rechte und Tests.
5. **Beobachten:** Die dritte Person achtet auf Kosten, Kontext und den Bezug zum eigenen Arbeits-Repo.
6. **Wechseln:** Nach jedem größeren Praxis-Schritt rotieren die Rollen.

Niemand hakt während des Live-Unterrichts still eine Checkliste im Cockpit ab. Das Cockpit dient dir zum Navigieren
und den Teilnehmenden zum Nacharbeiten nach der Session.

### Rollenkarten

| Rolle | Achtet auf | Sagt laut |
|---|---|---|
| Driver | Prompt, Befehl, Freigabe | „Ich erwarte, dass Claude …" |
| Navigator | Umfang, Rechte, Dateigrenzen, Tests | „Das ist sicher/unsicher, weil …" |
| Observer | Kosten, Kontext, Transfer | „In unserem Arbeits-Repo entspricht das …" |

Fällt ein Setup aus, paart ihr sofort: Die Person mit dem kaputten Rechner wird Navigator, während du parallel
debuggst.

### Eine sokratische Frage je Kapitel

Statt eines Live-Quiz stellst du eine Frage, passend zum Regal des Kapitels.

| Regal | Frage |
|---|---|
| Erste Schritte & Denkmodell, Rechte & Freigaben | „Welche echte Aktion hat Claude gerade ausgeführt, und welche Freigabe hat sie möglich gemacht?" |
| Kontext & Gedächtnis | „Was muss aufgeschrieben werden, damit sich die nächste Sitzung genauso verhält?" |
| Aufträge formulieren | „Welche Grenze im Auftrag verhindert, dass das hier zu breit wird?" |
| Git & Worktrees | „Was macht diesen PR für eine andere Entwicklerin prüfbar?" |
| Skills & Commands, Hooks, Plugins | „Ist das ein wiederverwendbarer Ablauf, ein automatischer Auslöser oder ein Bündel?" |
| MCP & Wissensquellen | „Welche Daten haben gerade eine Grenze überquert, und wem gehören sie?" |
| Agenten & Orchestrierung | „Welcher Teil soll parallel laufen, und welcher muss koordiniert bleiben?" |
| Gegenprüfung & Compliance | „Welcher Befund ist bestätigt, und welcher ist nur plausibel?" |
| Automation & Loops | „Was stoppt das, wenn es teuer, falsch oder veraltet wird?" |
| Abschlussprojekt | „Welcher Beleg macht die Übergabe bereit für das Arbeits-Repo von morgen?" |

### Zeitregel

Je 30 Minuten Live-Zeit:

- 10 Minuten Lehre und Demo,
- 12 Minuten Pair-Driving mit lautem Denken,
- 5 Minuten Nachbesprechung in der Gruppe,
- 3 Minuten Puffer oder Transfernotiz.

Wird es eng, streichst du zuerst das Abhaken im Cockpit und die Quizfragen. Der Live-Bau, die Sicherheitsfrage und
die Transfernotiz bleiben.

## Abrufen: Recall und Quick-Checks

Frühere Sessions werden aktiv abgerufen, bevor Neues kommt. Jede Abfrage ist kurz, mündlich und unbenotet.

| Zeitpunkt | Format | Zweck |
|---|---|---|
| Session 2, vor dem Deck | 5 Fragen aus Session 1 | Grundlagen aktiv abrufen, statt Folien nur wiederzusehen |
| Session 3, vor dem Deck | 5 Fragen aus Session 2 | Begriffe des Ökosystems wieder wach machen |
| Session 4, vor dem Deck | 5 Fragen aus Session 3 | den fortgeschrittenen Kern vor Kür und Abschlussprojekt festigen |
| Nach dichten Analogie-Blöcken | Quick-Check, 60–90 Sekunden | Missverständnisse sofort sichtbar machen |

### 5-Minuten-Recall

Die Teilnehmenden antworten zuerst aus dem Gedächtnis. Danach zeigst du die passende Stelle im Deck oder im Kapitel.

**Session 2 — Grundlagen abrufen**

1. Welcher Rechte-Modus ist für einen ersten Durchgang in einem unbekannten Repo sicher, und warum?
2. Was gehört in `CLAUDE.md` statt nur in den Chat?
3. Woran merkst du, dass Kontext-Komprimierung oder ein abdriftendes Gedächtnis eine Antwort beeinflusst?
4. Welchen engen Check führst du aus, bevor du einer Änderung von Claude traust?
5. Was ist der billigste Weg, damit eine Routineaufgabe nicht zur Kostenüberraschung wird?

**Session 3 — Ökosystem abrufen**

1. Wann ist ein Hook besser als ein Skill?
2. Mit welchem Exit-Code blockt ein PreToolUse-Hook — und was passiert, wenn der Hook mit einem anderen Code abstürzt?
3. Was unterscheidet einen lokalen Plugin-Test mit `--plugin-dir` von einer Installation fürs Team?
4. Wann ist NotebookLM/RAG besser, als ein großes Dokument in den Chat zu kopieren?
5. Was ist die erste Sicherheitsfrage, bevor eine Automatisierung Schreibzugriff bekommt?

**Session 4 — fortgeschrittenen Kern abrufen**

1. Welche Aufgaben profitieren von parallelen Agenten, und welche bleiben besser in einem Strang?
2. Was macht ein adversariales Review vertrauenswürdiger als einen einzelnen generischen Review-Prompt?
3. Welchen Rechte-Modus oder welche Deny-Regel wählst du vor einem autonomen Loop?
4. Was muss gedeckelt sein, bevor `/schedule`, `/loop`, `/goal` oder eine Routine unbeaufsichtigt läuft?
5. Welcher Beleg überzeugt dich, dass ein Security-Befund bestätigt ist und nicht nur plausibel?

### Quick-Checks in der Session

Nach dichten Analogie-Blöcken, 60–90 Sekunden, kein Quiz.

| Nach | Frage | Erwartetes Signal |
|---|---|---|
| [S1.6](../library/s1-06-rechte-modi.md) Rechte-Modi | „Welche Freigabestufe gibst du Claude für ein Repo, das du noch nie gesehen hast?" | Wählt `default` oder `plan` und nennt das Prinzip der geringsten Rechte. |
| [S1.10](../library/s1-10-claude-md.md) `CLAUDE.md` | „Nenn eine Regel, die für dein Team in die Hausordnung `CLAUDE.md` gehört." | Nennt eine dauerhafte Regel, keinen Einmal-Prompt. |
| [S2.10](../library/s2-10-hook-ausgaben.md) Hook-Ausgaben | „Wie verkleinert ein PostToolUse-Hook eine laute Ausgabe, bevor Claude sie liest?" | Nennt `hookSpecificOutput.updatedToolOutput` in der Form der Tool-Ausgabe (bei Bash `stdout`, `stderr`, `interrupted`, `isImage`); weiß, dass `suppressOutput` keine Wirkung hat. |
| [S3.12](../library/s3-12-zeitgesteuert-arbeiten.md) Zeitsteuerung | „Welches Sicherheitsnetz braucht jede unbeaufsichtigte Routine?" | Nennt eine Budgetgrenze plus Abbruchbedingung oder menschliche Prüfung. |
| [S4.8](../library/s4-08-abschlussprojekt.md) Abschlussprojekt | „Welcher Beleg macht deine Übergabe PR-reif?" | Nennt engen Check, Risiko, Rollback und den genau ausgeführten Befehl. |

## Transfer ins eigene Repo

Die Transfer-Beats sind klein, aber Pflicht: Der Playground beweist die Mechanik, das eigene Repo beweist die
Übernahme in die Arbeit. Jede Session reserviert dafür zehn Minuten. Niemand muss proprietären Code zeigen: Ein
privates Repo, ein bereinigter Klon oder eine Bestandsaufnahme auf Papier reichen, wenn Richtlinien den Live-Zugriff
verbieten.

| Beat | Session | Auftrag | Ergebnis |
|---|---|---|---|
| S1-T | 1, Grundlagen | Nimm ein Repo und mach einen Durchgang zu Kontext und Bereitschaft: Welche Dateien soll Claude zuerst lesen, was muss tabu sein, und welcher enge Check beweist eine sichere erste Änderung? | Einstiegskarte fürs Repo: Kontextdateien, geschützte Pfade, erster sicherer Check |
| S2-T | 2, Ökosystem | Wähl einen wiederkehrenden Ablauf aus deinem Repo und entscheide, ob er ein Skill, ein Hook, ein Plugin, eine MCP-Anbindung oder eine RAG-Quelle wird. | Ein Automatisierungskandidat mit Grenze, Auslöser und Installationsort |
| S3-T | 3, Kern | Nimm eine riskante oder repetitive Teamaufgabe und leg ihre sichere autonome Form fest: Agentenrolle, Rechte-Modus, Worktree, Budgetgrenze, Abbruchbedingung. | Ein begrenzter Automatisierungsentwurf mit ausdrücklichem Sicherheitsnetz |
| S4-T | 4, Kür | Mach aus dem Abschlussprojekt einen 30-Tage-Einstieg für dein echtes Team: erster PR, erste Leitplanke, erstes geplantes Follow-up per `/schedule` oder Routine. | Entwurf des Adoptionsplans mit verantwortlicher Person, Datum und Check |

Dein Satz dazu: „Löst nicht das ganze Repo. Nennt den nächsten sicheren Schritt."

Den einseitigen Adoptionsplan füllen die Teilnehmenden in den letzten zehn Minuten von Session 4 aus und legen das
30-Tage-Follow-up an. Die Vorlage kommt nach `resources/reference/adoptionsplan-vorlage.md`; wie die Empfehlung aus
dem Abschlussprojekt dort hineinkommt, steht in [S4.8](../library/s4-08-abschlussprojekt.md).

## Selbstwirksamkeits-Check

In jeder Session zweimal: einmal vor der ersten Folie, einmal in den letzten fünf Minuten. Skala 1–5, 1 = noch nicht,
5 = sicher ohne Hilfe.

1. Ich kann erklären, was Claude Code in meinem Repo tun darf und was nicht.
2. Ich kann Claude Code genug Projektkontext geben, damit es arbeitet, ohne den Umfang zu sprengen.
3. Ich kann eine Änderung von Claude Code mit einem passenden engen Check prüfen.
4. Ich kann eine Leitplanke einbauen oder auswählen, bevor eine Automatisierung riskant wird.
5. Ich kann ein Ergebnis von Claude Code in eine saubere Übergabe für andere Entwicklerinnen und Entwickler verwandeln.

Vergleiche Eingangs- und Ausgangswerte qualitativ. Ziel ist sichtbar wachsende Sicherheit, keine Prüfungsangst. Die
bewertete Aufgabe mit Rubrik ist das Abschlussprojekt in [S4.8](../library/s4-08-abschlussprojekt.md).

## Pre-Flight am Workshop-Tag

30 Minuten vor jeder Session. Der Workshop läuft meist unter Windows, deshalb sind die Befehle Windows-first
(`python`, kein `~`-Pfad); die Varianten für macOS und Linux stehen als Kommentar daneben.

```powershell
# 1. Claude Code funktioniert
claude --version
claude /doctor

# 2. Workshop-Repo aktuell  (Windows-Pfad anpassen; macOS/Linux: cd ~/cc-workshop/dynamic-workshop)
cd $HOME\cc-workshop\dynamic-workshop
git pull

# 3. Playground baut
cd workshop-playground
python -m pytest -v         # Python playground   (macOS/Linux: python3 -m pytest -v)
# make                      # C playground — OPTIONAL, nur wenn gcc/make installiert (auf Windows meist nicht; Demo 3.3 reviewt den C-Quelltext auch ohne Compile)

# 4. Plugins geladen
claude plugin list

# 5. MCP-Server konfiguriert (fuer Demo 2.4)
claude mcp list

# 6. NotebookLM-Notebook vorhanden (fuer Demo 2.5)
notebooklm list             # if CLI available

# 7. Tokens / Budget
/cost                       # current session
/usage                      # day-aggregate
```

- Die Demo-Nummern in den Kommentaren stammen aus dem alten Kursaufbau: Demo 2.4 steht heute in
  [S2.14](../library/s2-14-mcp-stecker.md), Demo 2.5 in [S2.18](../library/s2-18-rag-und-notebooklm.md), Demo 3.3 in
  [S3.6](../library/s3-06-devils-advocate.md).
- `/cost` und `/usage` tippst du in einer laufenden Claude-Code-Sitzung, nicht in PowerShell. `/cost` ist heute ein
  Alias für `/usage`.
- `claude doctor` (ohne Schrägstrich) prüft die Installation nur lesend, ohne eine Sitzung zu starten. `/doctor` in
  der Sitzung kann auch reparieren und fragt vorher nach.
- Welche Syntax das NotebookLM-Werkzeug hat, hängt vom Werkzeug ab: [vorbereitung.md](vorbereitung.md#notebooklm-notebook).

## Go/No-Go je Demo

Am Morgen von Session 3 und Session 4 abhaken. Eine Zeile pro Live-Demo: Preflight ausführen, bei PASS live zeigen,
bei FAIL auf den Fallback wechseln. Unter PowerShell ersetzt `Select-String` das `grep`.

**Session 3**

| Demo (Kapitel) | Preflight | PASS → live | FAIL → Fallback |
|---|---|---|---|
| Headless, Schritt 1 ⚓ ([S3.1](../library/s3-01-was-ist-ein-agent.md)) | `claude --version` (nur lokales `claude`) | Immer live, als Opener der Session | Kann praktisch nicht scheitern; sonst ist die ganze Session blockiert. |
| Multi-Agent ([S3.4](../library/s3-04-orchestrierungsmuster.md)) | `claude --version` (das Agent-Tool ist eingebaut) | Live | Aufzeichnung oder Transkript vorlesen, die Architektur mit zwei Agenten diskutieren |
| Devil's Advocate 🔧 ([S3.6](../library/s3-06-devils-advocate.md)) | `claude plugin list \| grep devil-advocate-swarms` | Live-Swarm | Aufzeichnung und die vier Stufen besprechen, oder live der Weg ohne Plugin aus S3.6: Claude direkt um das Audit von `access_control.py` bitten; alle fünf eingebauten Schwachstellen sind so auffindbar, nur Debatte und Konsens fehlen. `/security-review` taugt hier nicht, es prüft nur den Diff deines Branches gegen den Standard-Branch von `origin`. |
| CVE-Fix ([S3.6](../library/s3-06-devils-advocate.md)) | Websuche erreichbar (`curl -sI https://nvd.nist.gov`) | Live | Vorbereitete CVE-Beschreibung (NVD CVE-2018-18074) aus der Zwischenablage einfügen |
| Rechte-Modi ([S3.8](../library/s3-08-rechte-fuer-autonomie.md)) | `claude --version` (eingebaut) | Live | — (eingebaut, kein Plugin nötig) |
| Self-Improve 🔧 ([S3.14](../library/s3-14-self-improve-loop.md)) | `claude plugin list \| grep agentic-os` und Budgetgrenze gesetzt | Live, nur mit `--max-budget-usd` | Aufzeichnung; Loop-Architektur und Circuit Breaker diskutieren |

**Session 4**

| Demo (Kapitel) | Preflight | PASS → live | FAIL → Fallback |
|---|---|---|---|
| Headless, voller Lauf ([S4.3](../library/s4-03-headless.md)) | `claude --version` (nur lokales `claude`) | Live im Slot | Kann praktisch nicht scheitern. |
| Codex-Schwarm 🔧 ([S4.2](../library/s4-02-codex-schwarm.md)) | `codex --version` **und** `claude plugin list \| grep multi-model-orchestrator` | Live | Aufzeichnung; die Pipeline Claude → Codex → Claude an der Tafel erklären |
| Remote und Architektur ([S4.6](../library/s4-06-remote-und-teleport.md), [S4.8](../library/s4-08-abschlussprojekt.md)) | für den Bonus-Schritt: Telegram-Bridge läuft (Bridge-Status prüfen) | Live | Telegram-Schritt auslassen; `/remote-control` (eingebaut) und die Architektur-Diskussion als Vorlauf fürs Abschlussprojekt bleiben |
| Kaputter Skill ([S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md)) | `broken-greeter` kopiert (`ls ~/.claude/skills/broken-greeter/SKILL.md`) und `/debug` verfügbar | Live | `claude --verbose` statt `/debug`; das Asset liegt in `resources/demos/assets/broken-greeter/` |

Wo die Plugins und Assets herkommen: [vorbereitung.md](vorbereitung.md). Die Demos der Sessions 1 und 2 brauchen in
der Regel nur das lokale `claude` und gegebenenfalls das jeweilige Plugin oder den MCP-Server; die Recovery-Notes
stehen im Kapitel unter „Vorführen → Für Moderierende".

## Typische Fehlerbilder live

| Problem | Schnelle Rettung |
|---|---|
| Demo nicht reproduzierbar, Claude antwortet anders als gestern | Nimm es als Lehrmoment: „Seht ihr, LLMs sind nicht deterministisch — deshalb Hooks und Tests." |
| `gh auth` ist abgelaufen | PR-Schritt auslassen, stattdessen mit `git push` zeigen |
| Plugin nicht installiert | Diskussion statt Demo oder ein vorab aufgezeichnetes Video |
| Internet bricht weg | Ohne Netz antwortet Claude Code nicht, auch nicht mit `--bare`: Das Flag überspringt nur die automatische Erkennung von Hooks, Skills, Plugins, MCP-Servern, Auto-Memory und `CLAUDE.md` und liest zudem kein Abo-Login. Wechsle auf Aufzeichnungen, Tafel und Diskussion ([Notfallplan](#notfallplan-wenn-alles-brennt)). |
| `/cost` zeigt nichts | `/cost` ist ein Alias für `/usage`. Mit Pro- oder Max-Abo zeigt `/usage` Balken der Plan-Nutzung statt einer Kostenrechnung. Bei API-Nutzung ist die Usage-Seite der Claude Console maßgeblich: platform.claude.com/usage. |
| Auto-Memory driftet | Live mit den Mustern aus [S4.9](../library/s4-09-fehlersuche-werkzeuge.md) und [S4.10](../library/s4-10-diagnose-schritt-fuer-schritt.md) debuggen; das wird zur ungeplanten Diagnose-Demo. |
| Rechner einer teilnehmenden Person bricht beim Setup | **Pairing-Fallback:** Die Person paart sich sofort mit der Person daneben (Driver/Navigator), während du parallel debuggst. Bei nur drei Teilnehmenden blockiert ein totes Setup sonst ein Drittel des Praxisblocks. Halte zusätzlich das `~/cc-workshop`-Bundle auf USB-Stick bereit. |

## Notfallplan: wenn alles brennt

Wenn drei oder mehr Demos hintereinander nicht funktionieren:

1. **Den Demo-Fluss stoppen.** „Ich mache fünf Minuten Pause."
2. **Die Referenzkarten als Anker nehmen.** Geh mit den Karten in `resources/reference/` die zehn wichtigsten Befehle
   durch.
3. **Zur Diskussion wechseln.** „Was würdet ihr in eurem Job damit machen?" Sammle Anwendungsfälle und diskutiere sie.
4. **Das Abschlussprojekt vorziehen.** Die Architektur-Diskussion aus [S4.8](../library/s4-08-abschlussprojekt.md)
   lässt sich an jeder Stelle einbauen.
5. **Ehrlich sein.** „Das Werkzeug ist neu, manche Demos sind fragil. So sieht die Einführung eines echten Werkzeugs
   aus."

## Einladung (Vorlage)

Eine Woche vor Session 1 an alle Teilnehmenden. Platzhalter in eckigen Klammern ersetzen.

````text
Betreff: Claude-Code-Workshop — Vorbereitung (1 Woche vor Session 1)

Hallo [Name],

Session 1 ist am [Datum]. Damit wir gleich mit voller Geschwindigkeit starten können,
prüf bitte vorher Folgendes:

1. **Kapitel S0.1 „Werkstatt einrichten" durcharbeiten**
   (resources/library/s0-01-werkstatt-einrichten.md): Setup, Anmeldung, Werkzeuge.
   Plane 1–2 Stunden ein.

2. **Workshop-Repo mit dem Playground klonen:**
   ```bash
   git clone https://github.com/dynamic-dome/dynamic-workshop.git ~/cc-workshop/dynamic-workshop
   cd ~/cc-workshop/dynamic-workshop
   ```

3. **Workshop-Plugins:** optional für Session 2 bis 4. Ich bringe sie zu Session 2 vorbereitet mit.

4. **Konto:** Ein Claude-Abo (Pro oder Max) reicht für Session 1 und 2. Für die Multi-Agent-Demos
   in Session 3 und 4 zusätzliches Budget einplanen; die Schätzung je Session steht in
   resources/reference/kosten-nachbau.md.

5. **Setup-Termin:** Bitte nimm dir am [Termin] 30 Minuten mit mir für den Setup-Check.

Bei Fragen einfach antworten.

Bis bald
[Name der Moderation]
````

## Sprechpunkte je Kapitel

Sprechpunkte, Dauer und Recovery-Notes jeder Demo stehen im Kapitel selbst, im Abschnitt „Vorführen" im
aufklappbaren Block „Für Moderierende". Der [Live-Pfad](../paths/live-workshop.md) führt dich von Kapitel zu Kapitel.
Mit dem Workshop-Plugin fasst `/dynamic-workshop:workshop guide <ID>` ein Kapitel für dich zusammen,
`/dynamic-workshop:workshop guide S1` bis `guide S4` eine ganze Session samt Ablauf, Pausen und Live-Anker aus diesem
Handbuch. Hast du den Skill ohne Plugin nach `~/.claude/skills/` kopiert, heißt der Befehl `/workshop guide …`.
