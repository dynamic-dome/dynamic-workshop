# Selbstlernende zuerst — Pakete

> Entwurf: `docs/plans/2026-10-05-selbstlern-zuerst-design.md` · Befunde: `docs/reviews/2026-10-05-lernbogen-und-fakten.md`
> Branch `selbstlern-zuerst`. Diese Datei ist der Stand: Ein Paket ist erledigt, wenn sein Kasten angekreuzt ist und
> der Commit daneben steht. Eine frische Sitzung liest diese Datei, nimmt das erste offene Paket ohne offene
> Vorbedingung und liest dessen Abschnitt ganz.

## Für jede Sitzung

- Vor dem ersten Schritt: `git status -sb` (Branch `selbstlern-zuerst`, sauber) und
  `python -m pytest tools -q -p no:cacheprovider` (grün; Stand nach P7f: 739) und `python tools/build_library.py validate --complete`.
- Nach jeder Änderung an Kapiteln, Regalen oder Regeln:
  `python tools/build_library.py validate --complete` · `python tools/build_library.py build` ·
  `python -m pytest tools -q -p no:cacheprovider` · `python tools/lint_currency.py`.
- Das Repo hat keine Datenbank; die Tests unter `tools/` fassen keine Nutzerdaten an. Die Playground-Tests laufen
  nur in `workshop-playground/` und gehören nicht zur Suite.
- Fakten nur mit Doku-Beleg im Commit. Doku-Stand 2026-10-05:
  `~/AI/analysis-artifacts/workshop-review-2026-10-05/docs-cache/` (bei Bedarf neu laden:
  `curl -sL https://code.claude.com/docs/en/<seite>.md`).
- Commits chirurgisch stagen, nie nach `main`, kein Push. Generierte Dateien nie von Hand ändern.
- Kapiteltext: Deutsch mit Umlauten, „du“, kurze Sätze; Code, Befehle und Beispiel-Prompts Englisch. Nicht
  verwenden: das Bild der verheilten Wunde für Fehler, Werbesprache, unbelegte Zahlen.

## Übersicht

| Paket | Inhalt | Vorbedingung | Stand |
|---|---|---|---|
| P0 | Gate fällt geschlossen; „nur exit 2“ präzisiert (R1, R2) | — | [x] `fcab910` |
| P1 | Moderationsschicht: „Vorführen“ aus den Kapiteln in eigene Dateien | — | [x] `d6c40d5`, `597f9ce` |
| P2 | Cockpit und Tutor zeigen bei „durcharbeiten“ Lehrtext und Übung (R19) | P1 | [x] `4c98ba0` |
| P3 | Auflösungen: Format, Validator, Cockpit, Tutor; ein Kapitel als Durchstich (R15) | — | [x] `d03ea85` |
| P4 | Playground ohne Lösungshinweise (R18, R13) | — | [x] `664d5ca` |
| P5 | Pilotregal Einstieg S0.1 bis S1.9 samt X.2: Maßstab für alle Inhalte (R14, R15, R17, R21, R22, R26, R28) | P1, P3, P4 | [x] `359c9db` und Folge-Commit, siehe Abschluss P5 |
| P6 | Abschluss: Kapitel S4.11 in jedem Pfad, Praxis-Stationen als Session-Abschlüsse (R16) | P5 | [x] `8a96a4a`; S1.20 mit P7a, S2.20 mit P7c, S3.15 mit P7e erledigt |
| P7 | Ausrollen je Regal-Paket nach dem Maßstab (sechs Teilpakete, Sonnet-Schreiber, Codex-Gegenprüfung) | P5 | P7a [x] `bacbf60` · P7b [x] `2c9f792`, `dc7e02e` · P7c [x] `b72b648`, `bdb9082` · P7d [x] `8e75575`, `3a0f513` · P7e [x] `7b75b5e` · P7f [x] cc1052a |
| P8 | Restliche Inhaltsbefunde R3 bis R13, R23, R24, R25, R29, R30 | P7 | [ ] |
| P9 | UI-Überarbeitung des Cockpits (B1 bis B12 und was P2 offen lässt); eigene Fragerunde vorab | P8 | [ ] |

DCO-Todos unter #9632: P1 #9636 · P2 #9637 · P3 #9638 · P4 #9639 · P5 #9640 · P6 #9641 · P7 #9642 · P8 #9643 · P9 #9644.

Gegenüber der mit dem Owner besprochenen Reihenfolge steht der Playground (P4) vor dem Pilotregal, weil die Übung
in S1.8 an ihm hängt.

---

## P1 — Moderationsschicht

**Ziel:** Kein Kapitel enthält mehr „Vorführen“ oder einen Block „Für Moderierende“. Der Inhalt steht unverändert
in `resources/moderation/vorfuehren/<kapiteldatei>.md`. Live-Pfad und Tutor-Modus `guide` führen dorthin.

**Ausgangslage (gemessen 2026-10-05):** 29 Kapitel haben `## Vorführen`, alle 29 enthalten darin einen Block
`<details><summary>Für Moderierende</summary>`; zusammen 12.766 Wörter. „Vorführen“ ist verdrahtet in
`tools/library_model.py` (`SECTION_ORDER`, Sonderbehandlung um Zeile 285), `tools/build_library.py` (Regeln je
Kapiteltyp um Zeile 44 bis 47); `tools/build_cockpit.py` rendert das ganze Kapitel (`chapter_html`).

**Schritte**

1. Skript `docs/migration/2026-10-05-vorfuehren/migrate.py` (einmalig, bleibt als Beleg; nicht unter `tools/`, weil
   es nach dem Lauf nichts mehr zu tun hat). Es nimmt die Abschnittsgrenzen aus dem Parser des Projekts
   (`tools/library_model.py`, zaunfest), nicht aus einer eigenen Suche nach `## `. Je Kapitel den Abschnitt
   „Vorführen“ ausschneiden und nach `resources/moderation/vorfuehren/<kapiteldatei>` schreiben, mit Kopf
   `# Vorführen: <ID> · <Titel>` und einer Zeile mit Link zurück zum Kapitel. Den Abschnittstext wörtlich übernehmen.
   Relative Links umschreiben (Kapitel: `../../library/…`, Vorlagen: `../../demos/assets/…`, Karten:
   `../../reference/…`).
2. Beleg im Skript selbst (`--check` gegen den Stand vor dem Lauf, gelesen per `git show`): Jede nichtleere Zeile
   jedes alten Abschnitts steht, bis auf umgeschriebene Linkziele, in der Zieldatei; Summe der Wörter vorher gleich
   nachher; der Rest jedes Kapitels ist byte-gleich.
2a. **Vier Kapitel haben ihr einziges Cockpit-Beispiel in „Vorführen“** und keine Übung: S1.2, S3.13, S3.14, S4.6
   (gemessen 2026-10-05). Eine Lektion braucht genau ein Beispiel. Für diese vier bleibt der Beispielblock im
   Kapitel, als letzter Unterabschnitt `### Ausprobieren` von „Im Detail“, mit einem Satz davor; in der
   Moderationsdatei steht er weiterhin. Taugt das Beispiel allein nicht (S3.14 ruft einen Befehl, den es nicht mehr
   gibt), bekommt das Kapitel ein Beispiel, das ohne Zusatz läuft, mit Doku-Beleg.
3. Werkzeug anpassen: „Vorführen“ aus `SECTION_ORDER` und den Typregeln nehmen; ein Kapitel mit `## Vorführen` oder
   „Für Moderierende“ ist ein Validator-Befund. Der Katalog bekommt je Kapitel `demo` (Pfad oder `null`).
   `resources/paths/live-workshop.md` verlinkt je Kapitel die Demo. Der Link-Prüfer deckt den neuen Ordner ab;
   Snippet-Ledger, Hook-Wächter und Aktualitäts-Lint lesen ihn mit (Scope prüfen, nicht annehmen).
4. Verweise im Kapiteltext nachziehen: Sätze wie „steht in ‚Vorführen‘“, „Die Demo … steht in S2.8“, „wie in der
   Vorführung“ suchen (`grep -n -i "vorführ\|demo" resources/library/*.md`) und je Fundstelle entscheiden: streichen,
   auf die Übung umlenken oder als Verweis auf die Moderationsschicht nur dort lassen, wo er Moderierende meint.
5. Tutor: `skills/workshop/SKILL.md` (Quellen, Ablauf `next`/`learn` ohne „Vorführen“, Modus `guide` liest die
   Demo-Datei aus dem Katalogfeld), `agents/workshop-mentor.md` falls betroffen.
6. Doku: `resources/moderation/README.md`, `HOW-TO-USE.md` (§1 Routine, §2 Moderieren, §3 Quellenhoheit), `README.md`
   („Kapitel mit festem Aufbau“), `CLAUDE.md` und `AGENTS.md` (Struktur), Hinweis in der Spec vom 2026-09-30 auf den
   neuen Entwurf.

**Tests zuerst (Nähte: Validator-Ergebnis, Katalog, gebautes Cockpit):**
- Validator meldet ein Kapitel mit `## Vorführen` als Fehler; ohne ist es sauber.
- Katalog: Kapitel mit Demo-Datei hat `demo`, ohne hat `null`; jede Datei im Demo-Ordner gehört zu einem Kapitel.
- Cockpit-Daten enthalten in keinem Kapitel den Text „Für Moderierende“.
- `live-workshop.md` verlinkt genau die vorhandenen Demos.

**Fertig, wenn:** kein `## Vorführen` und kein „Für Moderierende“ unter `resources/library/`; `--check` des
Skripts grün; Suite grün; `build_library.py check` aktuell; die acht Kapitel ohne Demo und ohne Übung (S1.2, S2.1,
S2.6, S3.13, S3.14, S4.3, S4.6, S4.7) sind in P5 und P7 als „braucht Übung“ vermerkt.

**Für spätere Pakete notieren (nicht in P1 lösen):** Lehr- und Hilfetext, der in Moderationsblöcken steht und in
den Kapiteltext gehört: S2.6 (Hooks sind Best-Effort-Wächter), S2.10 (Windows-Weg des Gates, Fehlerhilfe), S3.8
(„Wenn es hakt“), S2.2 (Kernbotschaft der Demo), S1.19 (Rücksetzen mit `/model default`).

### Abschluss P1 (2026-10-05)

- Verschoben per `docs/migration/2026-10-05-vorfuehren/migrate.py`: 29 Abschnitte, Beleg in `check-output.txt`
  daneben (12.884 Wörter alt wie neu, jedes Kapitel exakt „alt minus Abschnitt“). Danach `fixups.py`: der
  Moderationsblock aus S1.20 (30. Datei), „Ausprobieren“ in S1.2, S3.13, S3.14, S4.6, 16 Verweise in Kapiteln,
  27 Querverweise zwischen Demo-Dateien.
- Werkzeug: `tools/library_model.py` (kein „Vorführen“ in `SECTION_ORDER`, `Chapter.demo`, `demo_dir`),
  `tools/build_library.py` (Regeln `no-moderation-block`, `demo-orphan`, `demo-h1`, `demo-no-example-marker`,
  Link-Prüfung für Demo-Dateien), `tools/library_generate.py` (Katalogfeld `demo`, Spalte „Vorführen“ im Live-Pfad).
  Tests: acht neue, alle vorher rot gesehen; Suite 677 grün (die Zahl steigt vor allem, weil die Wächter die 30
  neuen Dateien mitlesen).
- Tutor, HOW-TO-USE, README, Moderations-README, CLAUDE.md und AGENTS.md nachgezogen; Hinweis in der Spec vom
  2026-09-30.
- **Dabei entschieden:** S1.1 verweist nicht mehr auf den Passwortgenerator der Demo (die Variante entfällt im
  Kapitel, der Prompt steht in der Demo-Datei). S3.14 hat als Beispiel `/goal` aus der offiziellen Doku.
- **Was Selbstlernende durch das Verschieben verlieren und in P5 oder P7 als Übung zurückbekommen sollen:**
  der Vergleich einer Aufgabe über drei Modelle (Demo S1.19 → P7a), die CVE-Behebung bis zum PR (Demo S3.6 → P7d),
  das Secure Diff Gate zum Selbereinrichten (Demo S2.10 → P7b), der Headless-Ablauf mit Schema und Exit-Code
  (Demos S3.1, S4.3, S4.4 → P7d, P7f), Remote Control mit zweitem Gerät (S4.6 → P7f). S4.2 verweist in der Übung
  vorerst auf die Demo-Datei, weil die Übung ohne sie nicht geht (→ P7e).
- **Kapitel ohne Übung und jetzt auch ohne Demo:** S1.2, S2.1, S2.6, S3.13, S3.14, S4.3, S4.6, S4.7 (→ P5, P7).
- **Nicht angefasst:** `minutes` der Kapitel (enthielten die Demo-Zeit; werden mit der Regel „ehrliche Zeit“ in P5
  und P7 neu gesetzt, zusammen mit dem Einstufungsvertrag).
- **Codex-Gegenprüfung (lesend, Werkzeugänderungen P0 und P1, Stand `d6c40d5`):** Urteil FAIL mit fünf Befunden.
  An der Quelle geprüft: zwei bestätigt und testgetrieben behoben, drei ohne realen Fall.
  - Bestätigt: `secure-diff-gate.sh` ließ die Eingabe `null` durch (jq macht aus `null.tool_input` stillschweigend
    `null`); jetzt gilt nur ein JSON-Objekt mit Zeichenketten-Pfad als lesbar. Tests für `null`, Zeichenkette, Zahl.
  - Bestätigt: Links auf `paths/ziel-*.md` wurden nie geprüft (auch vor P1 nicht). Jetzt darf nur fehlen, was der
    Generator wirklich schreibt (ein Pfad je Ziel).
  - Ohne realen Fall: `--check` übersieht geänderte Link-Titel (es gibt keine); `fixups.py` hätte eine vorhandene
    Demo-Datei überschrieben (S1.20 hatte keine; Schutz nachgetragen); Anker `#vorführen` innerhalb einer Demo
    (kommt nicht vor, der Validator würde ihn melden).
  - **Folgepunkt für P7b:** `safety-check.sh` lässt `null` ebenfalls durch (ausgeführt: Exit 0). Die Vorlage steht
    wortgleich in S2.8; Skript, `.ps1` und Kapitel-Snippet gemeinsam ändern.

---

## P2 — Cockpit und Tutor: „durcharbeiten“ zeigt Lehrtext und Übung

**Ziel:** Hat ein Kapitel im eigenen Pfad den Status `work`, ist der volle Kapiteltext beim Öffnen sichtbar; bei
`skim`, `skip`, `later` und ohne Einstufung bleibt die Kurzansicht. Der Tutor führt bei `work` durch „Im Detail“.

**Ausgangslage:** `tools/cockpit/template.html` Zeile 784: `<details class="full">` ist immer zu. Tutor:
`skills/workshop/SKILL.md` Abschnitt „Ein Kapitel durchgehen“ springt von der Zusammenfassung zur Übung.

**Schritte**
1. Browser-Test zuerst (`tools/test_cockpit_browser.py`): Persona mit S1.1 = `work` → Volltext offen, Überschrift
   „Selbst machen“ sichtbar; Persona mit S1.1 = `skim` → zu; ohne Einstufung → zu.
2. Template: Bei `work` ersetzt der volle Kapiteltext die Kurzblöcke (sonst stünden Schnellcheck, Check und Quiz
   doppelt untereinander); das Quiz bleibt bedienbar, „Als erledigt markieren“ steht dann am Ende des Kapitels.
   Bei allen anderen Zuständen bleibt die Kurzansicht mit eingeklapptem Volltext. Fehlt der Volltext im Artefakt
   (Größengrenze), bleibt die Kurzansicht mit Link. Keine weitere Umgestaltung (das ist P9).
3. Tutor: Bei `work` nach „Auf einen Blick“ und „Bild im Kopf“ den Abschnitt „Im Detail“ abschnittsweise durchgehen
   (je Unterabschnitt die Kernaussagen, dann weiter); hat das Kapitel kein „Selbst machen“, stellt der Tutor eine
   Anwendungsfrage aus dem Outcome. `skim` bleibt: Zusammenfassung und Check. Test in `tools/test_workshop_tutor.py`.

**Fertig, wenn:** Browser-Tests grün (vorher rot gesehen), Suite grün, im Browser an 127.0.0.1 mit einer Persona
nachgesehen (Screenshot nach `%TEMP%`).

### Abschluss P2 (2026-10-05)

- Cockpit: Bei Status `work` ist der volle Kapiteltext die Seite; darunter das Quiz und „Als erledigt markieren“ (einmal,
  nicht mehr in der Seitenleiste). Oben bleibt eine Zeile zum Überspringen per Schnellcheck. Alle anderen Zustände
  behalten die Kurzansicht. Zwei Browser-Tests: der für `work` war vorher rot, der für die Kurzansicht schützt
  bestehendes Verhalten (war von Anfang an grün).
- Am echten Cockpit nachgesehen (Neuling, Ziel Alltag): S1.1 „durcharbeiten“ zeigt Schnellcheck bis Weiterlesen,
  Quiz, Knopf am Ende; X.2 und S2.8 („überfliegen“) zeigen die Kurzansicht; keine Konsolenfehler.
- Tutor: neuer Schritt „Im Detail“ bei `work` (abschnittsweise, mit Rückfrage; ohne Übung endet er in einer
  Anwendungsfrage); `skim` bleibt Zusammenfassung und Check. Test in `tools/test_workshop_tutor.py`.
- **Offen für P9:** Die Seite zeichnet sich beim Markieren neu (B7); der Volltext wiederholt in der Kurzansicht
  die Kurzblöcke; lange Kapitel haben keine Sprungmarken.

---

## P3 — Auflösungen

**Ziel:** Jede Abruffrage im Abschnitt „Check“ hat eine Auflösung. Format, Prüfung und Anzeige stehen; ein Kapitel
ist als Durchstich fertig (S1.1).

**Format im Kapitel** (direkt nach den nummerierten Abruffragen, vor dem Quiz):

```markdown
<details><summary>Auflösung</summary>

1. …
2. …
3. …

</details>
```

Je Antwort ein bis drei Sätze, nur aus dem Kapiteltext belegbar, gleiche Nummer wie die Frage.

**Schritte**
1. Tests zuerst (`tools/test_library_model.py`, `tools/test_build_library_validate.py`): Parser liefert `answers`
   je Kapitel; Validator: Block vorhanden und Anzahl ungleich Anzahl der Fragen → Fehler; Block fehlt → Befund nur
   für Kapitel, die in `tools/fixtures/answers-required.txt` stehen (die Liste wächst mit P5 und P7 und wird am
   Ende durch die Regel „alle Lektionen“ ersetzt).
2. Parser und Katalog: `recall` (Fragen) und `answers` je Kapitel.
3. Cockpit: Abruffragen in der Check-Ansicht zeigen, je Frage ein Knopf „Auflösung zeigen“. Browser-Test.
4. Tutor: Rückmeldung zu Abruffragen stützt sich auf die Auflösung; fehlt sie, auf den Kapiteltext.
5. Durchstich: Auflösungen für S1.1 schreiben und S1.1 in die Pflichtliste aufnehmen.
6. Fortschritt sichtbar machen: `build_library.py validate` nennt am Ende zwei Zahlen, Lektionen mit Übung und
   Lektionen mit Auflösung, je von der Gesamtzahl. Daran lässt sich P5 und P7 ablesen.

**Fertig, wenn:** Suite grün, Negativprobe gesehen (eine Antwort zu wenig → Validator rot), S1.1 im Cockpit mit
aufklappbarer Auflösung, Cockpit-Datei unter der Größengrenze von 3 MB.

### Abschluss P3 (2026-10-05)

- Format wie oben beschrieben; der Parser liefert je Kapitel `recall` und `answers` (`None` ohne Block).
- Validator: `answers-count` (Anzahl ungleich, leere Antwort, Block ohne Fragen, Block nicht geschlossen),
  `answers-required` für Kapitel aus `tools/fixtures/answers-required.txt` (heute: S1.1). Negativprobe am echten
  Kapitel gesehen (eine Antwort entfernt → Exit 1).
- `validate` nennt am Ende den Fortschritt. Stand: Lektionen mit Übung 27 von 61, mit Auflösung 1 von 61.
- Cockpit: Die Kurzansicht zeigt jetzt die Abruffragen (vorher gar nicht) und je Frage eine eigene, eingeklappte
  Auflösung; in der Vollansicht steht der Block aus dem Kapitel. Datei 2,53 MB.
- Tutor: stellt die Fragen einzeln, zeigt die Auflösung erst nach der Antwort.
- Anleitung für alle, die Auflösungen schreiben: ein bis drei Sätze, eine Zeile je Antwort, gleiche Nummer wie
  die Frage, nur was im Kapitel steht.

---

## P4 — Playground ohne Lösungshinweise

**Ziel:** Wer Claude im Playground nach Schwachstellen fragt, bekommt eine Antwort aus dem Code, nicht aus einer
mitgeladenen Liste. Die Lösungen bleiben erhalten, aber außerhalb des Ordners.

**Ausgangslage:** `workshop-playground/CLAUDE.md` Zeilen 45 bis 110 listen alle fünf Schwachstellen (Zeilenangaben
veraltet: `backup_database()` steht in Zeile 161, `read_log()` in 148, `log_event()` in 132) und sagen „Do NOT fix“;
`access_control.py` und `osdp_frame_decoder.c` tragen `VULNERABILITY`-Kommentare.

**Schritte**
1. Lösungen nach `resources/reference/playground-loesungen.md` (Deutsch, mit aktuellen Zeilen, je Schwachstelle:
   Ort, Wirkung, woran man sie erkennt, Kapitel, das sie nutzt). In `resources/reference/README.md` eintragen.
2. `workshop-playground/CLAUDE.md` auf das kürzen, was ein Projekt-Gedächtnis ist (Zweck, Befehle, Konventionen);
   keine Liste, keine Blocknummern des Live-Kurses; statt „Do NOT fix“: Fixes nur auf einem eigenen Branch.
3. Kommentare im Code neutralisieren: kein „VULNERABILITY“, keine Erklärung der Lücke; das Verhalten bleibt
   byte-gleich. `cd workshop-playground && python -m pytest -q` vorher und nachher mit gleichem Ergebnis.
4. Kapitel, die auf die Liste verweisen, anpassen: mindestens S1.8 (Auflösung der Übung), S3.6, S2.18, S4.8;
   Suche: `grep -n "CLAUDE.md\|fünf\|VULNERAB" resources/library/*.md`. Fallen Kommentarzeilen weg, verschieben sich
   Zeilennummern: jede Zeilenangabe zu Playground-Dateien in Kapiteln, Karten und Moderationsschicht nachziehen
   (`grep -rn "access_control.py:\|osdp_frame_decoder.c:\|Zeile [0-9]" resources`).
5. Tests unter `tools/`, die die Zahl oder den Ort der Schwachstellen festhalten, auf die neue Datei umstellen.

**Fertig, wenn:** `grep -ri "vulnerab" workshop-playground/` leer; Playground-Tests unverändert; Suite grün.

### Abschluss P4 (2026-10-05)

- Lösungen: `resources/reference/playground-loesungen.md`, neun Schwachstellen (fünf in Python, vier in C), Orte als
  Funktionsnamen statt Zeilennummern. Damit ist auch R13 erledigt (die alte Liste nannte veraltete Zeilen).
- `workshop-playground/CLAUDE.md` ist nur noch Projekt-Gedächtnis; statt „Do NOT fix“ gilt: auf eigenem Branch
  arbeiten, `main` bleibt das Übungsmaterial. S3.6, S3.8 und S4.8 zitieren die neue Regel, S1.8 verweist auf die
  Lösungen.
- Kommentare und Docstrings in `access_control.py`, `osdp_frame_decoder.c` und der Testdatei nennen keine Schwachstelle
  mehr. Beleg: gleicher AST ohne Docstrings (Python) und gleiche Token-Folge ohne Kommentare (C, 511 Token) gegenüber
  dem Stand davor; Playground-Tests 18 grün, vorher wie nachher; der Ordner blieb beim Testlauf unverändert.
- `tools/test_playground.py` hält das fest: kein verräterisches Wort im Playground, die Lösungen nennen jede
  betroffene Funktion und nur Funktionen, die es gibt.
- **Offen für P5 und P7:** S1.8 braucht eine Übung, die auch dann trägt, wenn Claude die Datei von sich aus liest;
  S3.6 zählt die fünf Schwachstellen im Kapiteltext vor der Übung auf.

---

## P5 — Pilotregal Einstieg (S0.1, X.2, S1.1 bis S1.9)

**Ziel:** Elf Kapitel in der Fassung, an der sich alle weiteren messen. Geschrieben von Fable, nicht delegiert.
Grundlage: Bericht `berichte/D1-didaktik-einstieg.md` und `berichte/F1-fakten-einstieg-rechte.md` in
`~/AI/analysis-artifacts/workshop-review-2026-10-05/`.

**Je Kapitel**
- Auflösungen zu allen Abruffragen (Format P3), Kapitel in die Pflichtliste.
- Eine Übung zum Selbermachen, wo das Outcome ein Können verspricht (heute ohne: S1.2, S1.3, S1.6, S1.7, S1.9);
  vorhandene Übungen auf Startzustand, Schritte und „Geschafft, wenn“ prüfen.
- Check prüft das Outcome; Quizantworten plausibel und etwa gleich lang.
- Kein Gruppenformat ohne Einzelfassung, keine Kürzel des Live-Kurses („W1“, „Übung 1.0“), keine
  Baustellenspuren, Fachgebiet als Beispiel statt als Anrede (S1.2:76).
- **Ehrliche Zeit (R20):** `minutes` = Lesezeit des Fließtexts bei 160 Wörtern je Minute plus die Hauptübung,
  auf fünf Minuten gerundet; weitere Übungen tragen ihre eigene Zeit. Minuten gehören zum Einstufungsvertrag,
  also mit Vertrag und Golden zusammen ändern.
- **Übungen arbeiten in einem Wegwerf-Ordner.** Nichts an der globalen Konfiguration ohne Sicherung und Rückweg.
- **Jede neue oder geänderte Übung wird einmal wirklich durchgespielt,** in einem Wegwerf-Ordner, bevor das Paket
  fertig ist. Was sich nicht durchspielen lässt (Konto, Abo, zweites Gerät), steht mit Grund im Paketabschluss.

**Über die Kapitel hinweg**
- S0.1 auf Claude Code, Anmeldung, Git und Python kürzen; Node, `jq`, `gh` und den Playground-Klon dorthin, wo sie
  zuerst gebraucht werden, mit Rückverweis; Versionsangaben berichtigen (R8, Beleg aus `setup.md` und Changelog).
- S1.1: Der erste Unterabschnitt von „Im Detail“ ist die Hallo-Übung, gestartet mit
  `claude --permission-mode default`, damit die Freigabe-Abfrage erscheint. Die Reihenfolge der Hauptabschnitte
  bleibt (Spec §4.3).
- S1.8: Übung neu, ohne Abhängigkeit von einer Lösungsliste (P4).
- Bilder vereinheitlichen: „Besucherausweis“ nur für den Modus `default` (S1.2 gegen S1.5).
- X-Kapitel ans Ende ihrer Session: X.2 nach S1.20, X.1 nach S2.20, X.3 nach S3.15, X.4 nach S4.7. Das ändert die
  Reihenfolge: Vertragskatalog, Personas und Golden bewusst neu (HOW-TO-USE §3).
- Dubletten zwischen S1.1, S1.2 und S1.3 kürzen (Chat gegen Agent, Fähigkeitenliste).

**Danach:** `docs/plans/2026-10-05-selbstlern-zuerst-massstab.md` schreiben: die Regeln, die sich im Pilot
bewährt haben, mit je einem Vorher-nachher-Beispiel. Das ist der Auftrag für P7.

**Fertig, wenn:** Validator ohne Befund für die elf Kapitel inklusive Auflösungs- und Übungsregel; Suite grün;
Codex-Gegenprüfung des Diffs (lesend) ohne offenen Befund; Maßstab-Datei geschrieben.

### Abschluss P5 (2026-10-05)

- **Kapitel** (`359c9db`): S0.1, S1.1 bis S1.9 neu geschrieben, X.2 angepasst. Der Maßstab steht in
  `docs/plans/2026-10-05-selbstlern-zuerst-massstab.md` (16 Regeln, je mit Vorher und Nachher aus dem Pilot).
  Neue Übungen: S1.2 (Rückfrage lesen und ablehnen), S1.3 (eigene Wechselmöglichkeiten), S1.6 (Modus ablesen,
  Zyklus, Start in `plan`), S1.7 (Modell und Effort für eine Sitzung), S1.9 (`/rewind`, dann `/compact` mit Fokus).
  Umgebaut: S1.1 (Hallo-Übung als erster Teil von „Im Detail“, Start mit `--permission-mode default`,
  Vertrauensdialog), S1.4 (Werkzeugnamen aus dem Transkript mit `Ctrl+O`), S1.5 (dritte Runde mit Deny-Regel),
  S1.8 (Türcode in `notes.txt`, „Messages“ in `/context` vor und nach `@` und `/clear`).
- **Werkzeug:** `tools/fixtures/standard-chapters.txt` ersetzt `answers-required.txt`; für Kapitel darauf gelten
  `answers-required`, `exercise-required`, `exercise-shape`, `minutes-honest`, dazu `standard-list` für unbekannte
  IDs. Tests zuerst, rot gesehen. Stand: Lektionen mit Übung 32 von 61, mit Auflösung 9 von 61.
- **Vertrag bewusst neu:** Minuten S0.1 25, S1.1 25, S1.2 15, S1.3 10, S1.4 10, S1.5 20, S1.6 15, S1.7 15, S1.8 15,
  S1.9 15, X.2 35. X.2 nach S1.20, X.1 nach S2.20, X.3 nach S3.15, X.4 nach S4.7. Personas P01, P02, P03 und P14 von
  Hand aus den neuen Metadaten abgeleitet und erst danach gegen die Engine laufen lassen: alle vier trafen. Golden
  neu. **Der Schnellstart-Pfad braucht jetzt 178 Minuten bei einer Warnschwelle von 180;** wächst in P7a eines seiner
  Kapitel, muss die Schwelle oder der Pfad bewusst angepasst werden.
- **S0.1** setzt nur noch Claude Code, Anmeldung, Git und Python voraus. Node.js, `jq`, GitHub CLI, Workshop-Repo
  mit Playground und der Doktor stehen auf der neuen Karte `resources/reference/werkstatt-erweitern.md`; S2.8,
  S2.14, die Vorbereitung für Moderierende und die Demo zu S3.6 verweisen dorthin.
- **Durchgespielt mit Claude Code 2.1.289** (jede Übung einmal, Wegwerf-Ordner):
  - Linux, interaktiv über eine ferngesteuerte tmux-Sitzung, Start jeweils ohne Benutzer-Einstellungen
    (`--setting-sources project,local`): S1.1 Hallo (Vertrauensdialog, zwei Rückfragen, Ergebnis), S1.2 (Löschen
    abgelehnt, Datei bleibt), S1.3 (`/desktop` fehlt unter Linux, `/mobile` zeigt QR-Code, `Esc` schließt), S1.4
    (eine Rückfrage für `Write`; `cat` und `wc -l` laufen ohne Rückfrage; `Ctrl+O` zeigt `Write(…)` und `Bash(…)`),
    S1.5 (Runde 2 ohne Rückfrage; Runde 3: Löschen abgelehnt, `/permissions` zeigt beide Regeln), S1.6 (Start in
    `auto`, Zyklus Manual → accept edits → plan → auto, Start in `plan`), S1.7 (Kopfzeile „with high effort“,
    `/effort status`, Auswahl von `/model`, Haiku), S1.8 („Messages“ 10 → 16.600 → 130 Tokens; Türcode nur mit
    `@notes.txt`), S1.9 (`/rewind` stellt lesbare Namen wieder her, `--door` bleibt; „Messages“ 18.600 → 13.000 nach
    `/compact` mit Fokus).
  - Windows: S1.5 Runde 2 und 3 headless (`claude -p`): Löschen läuft in `acceptEdits`, mit der Deny-Liste wird
    der PowerShell-Befehl mit `Remove-Item` abgelehnt. Die PowerShell-Befehle für die Übungsordner und das
    Anlegen der Dateien in S1.8 ausgeführt.
  - **Nicht durchgespielt:** die interaktiven Rückfragen unter Windows (kein fernsteuerbares Terminal; der Wortlaut
    der Rückfrage für das PowerShell-Tool ist deshalb in S1.2 und S1.4 nur umschrieben); `/desktop` selbst (auf dem
    Testrechner nicht vorhanden); die Installation aus S0.1 (Befehle unverändert, nicht neu installiert); X.2
    Übung 2 und 3 (bis auf Startzustand und Beispielfrage unverändert; der Tutor ist nicht erneut gestartet worden).
- **Beobachtet, für P8 zu klären:** `/model` zeigt auf dem Testkonto (Max) „Default (recommended)“ mit dem
  Fable-Tier, während `model-config.md` sagt: „Neither Fable model is the account-type default on any plan or
  provider.“ S1.7 folgt der Doku. `/effort status` nennt auf Haiku eine Stufe, obwohl das Tier laut Doku keinen
  Effort kennt. Auf dem Windows-Testrechner scheiterte der erste PowerShell-Aufruf einmal mit „Die Befehlszeile ist
  zu lang“ (Eigenheit des Rechners, nicht im Kapitel).
- **Codex-Gegenprüfung (lesend, Stand `359c9db`, zwei Läufe):**
  - Werkzeug: Urteil FAIL, vier Befunde. Bestätigt und behoben: eine auskommentierte Übungsüberschrift zählte als
    Übung (Test zuerst, rot gesehen); die Verdrahtung der Liste in der CLI hatte keinen Test (ergänzt; sofort grün,
    weil das Verhalten bestand, in beide Richtungen empfindlich). Ohne realen Fall: `~~~` innerhalb eines
    Backtick-Blocks und Linkziele mit Klammern (beides kommt in der Bibliothek nicht vor; der Parser behandelt
    Zäune überall so).
  - Kapitel: Urteil FAIL, drei Befunde, alle bestätigt und behoben: Die Wiederherstellung überspringt verlinkte
    Dateien (`checkpointing.md`: „Checkpointing doesn't rewind symlinked or hard-linked files“; S1.2 sagt jetzt
    „meist“, S1.9 nennt die dritte Grenze); die Rückfrage heißt unter Windows nicht „Bash command“ (S1.2, S1.4);
    `s` in der Auswahl von `/model` übernimmt Modell und die dort eingestellte Stufe für die Sitzung
    (`model-config.md`: „`s` in the `/effort` slider or the `/model` picker: apply the level to this session only“).
- **Dabei entschieden:**
  - Eine Karte statt verteilter Installationsanleitungen: Die Paketliste sah vor, Node, `jq`, `gh` und den Klon
    in das Kapitel des ersten Bedarfs zu legen. `jq` und der Playground werden aber in mehreren Kapiteln gebraucht;
    eine Stelle mit Ankern ist leichter zu pflegen.
  - S1.5 bleibt ein Kapitel (der Bericht schlug eine Teilung vor; das änderte den Kapitelbestand und gehört, wenn
    überhaupt, zu R24 in P8). Die überladene Regel-Passage ist in zwei Listen zerlegt.
  - S1.3 bleibt Kern; Outcome auf das Erreichbare geändert.
  - Aus S1.9 entfallen `/export`, `/resume`, `/memory`, `/init` und `claude -r` (weder geübt noch geprüft); aus S1.2
    das Zitat ohne Quelle und der Vergleich mit der Kreissäge; aus S1.7 der Kasten zum System-Prompt; aus S0.1 die
    Versionstabelle, die Zeile zum Speicherplatz und die Spalte „Empfohlen“ (nicht belegbar).
  - `plan` heißt im Bild von S1.6 jetzt „Begehung mit Klemmbrett“ statt „Einsatzbesprechung“.
- **Offen für P7:** S1.12 nennt `--add-dir` einen „Besucherausweis“ (P7a); S1.10 und S1.16 nutzen noch
  `exercises/exercise-1.x` als Ordnernamen (P7a); S1.7 verweist für das Ablesen des Verbrauchs auf S1.19 (P7a prüft,
  ob die Übung dort an S1.7 anschließt); X.1, X.3 und X.4 haben nur ihre neue Position, der Text folgt in P7c,
  P7d und P7f.

---

## P6 — Abschluss

**Ziel:** Jeder Pfad endet mit einem kleinen Build. Die drei Praxis-Stationen schließen ihre Session ab.

**Schritte**
1. Neues Kapitel `s4-11-abschluss-kleiner-build.md`: Kern, Typ `capstone`, 25 Minuten, Voraussetzungen S1.5, S1.13,
   S1.16. Aufgabe im Playground: ein Fix, ein Guardrail (Deny-Regel genügt; Hook als Kür), eine enge Verifikation,
   eine Übergabe. Drei fertige Missionen zur Wahl, eine Vorlage für die Übergabe, eine Rubrik zur Selbstbewertung
   mit je einem Beispiel für „erfüllt“.
2. Einstufung: Kern-Kapitel vom Typ `capstone` gehören für jedes Ziel zur Relevanzmenge und in den Mindestpfad;
   S4.8 bleibt wie bisher (Kür, nur `agents` und `einschaetzen`). Regel in `_placement.yaml` und `tools/placement.py`
   samt JS-Port; Pflicht-IDs im Validator; Vertrag, Personas und Golden neu.
3. S4.8: Einzelfassung als Hauptweg (Missionen, Übergabe-Vorlage, bewertetes Beispiel), Gruppenformat in die
   Moderationsschicht; verweist auf S4.11 als kleine Fassung.
4. Praxis-Stationen S1.20, S2.20, S3.15: je eine verbindende Aufgabe mit „Geschafft, wenn“ als Hauptteil; die
   Übungsauswahl bleibt als Tabelle für alle, die Übungen ausgelassen haben; Reste des Live-Formats raus.

**Fertig, wenn:** alle fertigen Pfade enden mit S4.11; Python- und JS-Engine treffen alle Vektoren; Suite grün.

### Abschluss P6 (2026-10-05)

- **S4.11 „Abschluss: ein kleiner Build“** (`8a96a4a`): Kern, Typ `capstone`, 30 Minuten (der Plan nannte 25; die
  Rechnung nach dem Maßstab ergibt 28), Voraussetzungen S1.5, S1.13, S1.16. Drei Missionen an `access_control.py`
  (leere Namen, Groß- und Kleinschreibung, sortierte Liste), keine davon ist eine der eingebauten Schwachstellen.
  Guardrail: Push-Sperre in `workshop-playground/.claude/settings.json`, die vor dem Auftrag ausprobiert wird.
  Übergabe als Commit-Nachricht nach Vorlage; Selbstbewertung an fünf Kriterien mit je einem Beispiel.
- **Einstufung:** Kern-Kapitel vom Typ `capstone` gehören für jedes Ziel zur Relevanzmenge und in den Mindestpfad;
  Python-Engine und JS-Port im selben Commit. Tests zuerst (P01, P03, P05 und die neue Invariante „jeder Pfad endet
  mit S4.11“ waren rot). Vertrag, Personas und Golden bewusst neu; P07 bekommt eine Warnung mehr, weil die Persona
  S1.16 überspringt, das S4.11 voraussetzt. **Der Schnellstart-Pfad braucht jetzt 205 Minuten; die Warnschwelle liegt
  bei 240.** Alle sieben erzeugten Pfade enden mit S4.11. 71 Kapitel.
- **S4.8** ist für eine Person geschrieben: drei Vorschläge für eine Mission, Startzustand, ein bewertetes Beispiel
  (der Build aus S4.11 an der Rubrik: 15 von 18), Auflösungen, ehrliche 55 Minuten. Das Gruppenformat steht in der
  Moderationsdatei. Der Tutor gibt bei `capstone` keine Lösungsschritte vor und geht am Ende die Bewertung durch.
- **Durchgespielt:** S4.11 mit Mission A aus einem Klon dieses Branches (Linux, tmux). Der erste Lauf zeigte zwei
  Schwächen: Claude ließ `.claude/settings.json` aus dem Commit und verstand unter „Guardrail“ die fachliche Regel.
  Auftrag und Vorlage nennen jetzt beides ausdrücklich; zweiter Lauf: drei Dateien im Commit, Absatz korrekt.
  Nicht durchgespielt: die große Übung in S4.8 (unverändert bis auf Missionen und Startzustand; 40 Minuten mit
  Agenten und Hooks) und die Missionen B und C.
- **Dabei gefunden:** `pip3 install -r requirements.txt` scheitert auf aktuellen Linux-Systemen und mit
  Homebrew-Python („externally-managed-environment“, PEP 668). Karte und Anleitung richten den Playground jetzt
  über eine virtuelle Umgebung ein (ausgeführt: 18 passed).
- **Verschoben:** Die Stationen nennen in ihren Tabellen Übungen, die P7 umbenennt. S1.20 ist mit P7a neu
  geschrieben; S2.20 folgt mit P7c, S3.15 mit P7e.
- **Codex-Gegenprüfung der Regel (lesend):** PASS; ein Hinweis auf eine Testlücke beim JS-Port, die es nicht gibt
  (`tools/test_placement_js.py` prüft den Port gegen dieselben Golden-Daten).

---

## P7 — Ausrollen je Regal-Paket

**Ziel:** Alle übrigen Lektionen nach dem Maßstab aus P5: Auflösungen, Übung in jeder Kern-Lektion, kein Rest des
Live-Formats im Lernweg, Demo-Inhalt als Übung, wo er trägt.

| Teilpaket | Kapitel | Didaktik-Bericht | Fakten-Bericht |
|---|---|---|---|
| P7a | S1.10 bis S1.19, S1.20 | D2 | F2 |
| P7b | S2.1 bis S2.10 | D3 | F3 |
| P7c | S2.11 bis S2.19, X.1, S2.20 | D4 | F4, F7 |
| P7d | S3.1 bis S3.7, X.3 | D5 | F4, F7 |
| P7e | S3.8 bis S3.14, S4.1, S4.2, S3.15 | D6 | F1, F5 |
| P7f | S4.3 bis S4.10 (ohne S4.8), X.4 | D7 | F6, F7 |

Die Stationen S1.20, S2.20 und S3.15 schreibt, wer das Teilpaket abnimmt, nachdem die Übungen des Teilpakets
feststehen: eine verbindende Aufgabe als Hauptteil, darunter die Tabelle der Übungen (Muster: S1.20).

Ablauf je Teilpaket: Auftrag (Skill `subagent-briefing`) mit Maßstab-Datei, Kapitel-Liste, den beiden Berichten
und der zugehörigen Moderationsdatei als Quelle für Übungen → ein Sonnet-Schreiber (`model: sonnet`, eigener
Worktree) → Fable liest den Diff und prüft Stichproben gegen die Doku → Codex prüft lesend gegen
(`codex exec -s read-only`, Auftrag über stdin) → Befunde einarbeiten → Commit. Höchstens zwei Runden Nacharbeit
je Teilpaket, dann entscheidet Fable selbst. Die Zahlen der Schreiber (Fragen, Übungen) vor Übernahme nachzählen.
Schreiber ändern nur Kapitel und Moderationsdateien ihres Teilpakets; sie bauen nichts und committen keine
generierten Dateien (sonst kollidieren Katalog und Cockpit). Gebaut wird nach dem Übernehmen, ein Teilpaket nach
dem anderen. Die Hauptübung je Kapitel wird durchgespielt (siehe P5), nicht vom Schreiber selbst.

**Fertig, wenn (erfüllt, siehe Abschluss P7):** die Auflösungs- und die Übungsregel im Validator für alle Lektionen gelten (die Pflichtliste aus
P3 entfällt); Suite grün.

### Auftrag für Schreiber (Vorlage, bewährt in P7a)

Je Teilpaket ein eigener Worktree außerhalb des Repos (`git worktree add ~/AI/worktrees/workshop-p7x -b p7x-schreiber
selbstlern-zuerst`), ein Agent mit `model: sonnet`. Der Auftrag (Englisch, nach dem Skill `subagent-briefing`) nennt:

1. **Ziel und Arbeitsort:** nur der Worktree; Dateien mit Write/Edit schreiben, keine Heredocs.
2. **Dateien:** die Kapitel des Teilpakets und `tools/fixtures/standard-chapters.txt` (IDs anhängen); sonst nichts.
3. **Zuerst lesen:** die Maßstab-Datei ganz, zwei Musterkapitel (S1.5, S1.9), je Kapitel seine Moderationsdatei und
   die Befunde der beiden Berichte; Doku-Stand unter `~/AI/analysis-artifacts/workshop-review-2026-10-05/docs-cache/`.
4. **Kontext:** feste Abschnitte, Meta-Block unberührt, genau ein `cockpit:example`, Form von Check und Übung,
   Wegwerf-Ordner `~/cc-workshop/<thema>`, Voraussetzungen nur Claude Code, Git, Python (sonst Karte „Werkstatt
   erweitern“), Start mit `--permission-mode default` oder `acceptEdits`, beide Shells, Bilder, Wortlaute der
   Oberfläche nur aus Doku oder fertigen Kapiteln, keine Modellgenerationen. Dazu die Besonderheiten des Teilpakets.
5. **Frontmatter:** `outcome` und `minutes` dürfen sich ändern, alles andere nicht.
6. **Fertig, wenn:** `validate --chapter` je Kapitel nur noch `[meta-contract] minutes` meldet, `lint_currency` OK,
   `migration_ledger.py --missing` gemeldet (nicht `migration-dropped.txt` ändern), je Kapitel ein Commit auf dem
   Branch, kein Push.
7. **Außerhalb des Auftrags:** `build`, generierte Dateien, Moderationsdateien, Hook-Vorlagen, Tests, `docs/`;
   Kapitel teilen oder umstellen nur als Vorschlag.
8. **Abbruch:** Validator schon vorher rot; Datei außerhalb des Auftrags nötig; derselbe Schritt zweimal gescheitert;
   eine Tatsache, an der eine Übung hängt, ist nicht zu belegen. Nichts erfinden.
9. **Rückgabe:** STATUS, COMMITS, je Kapitel Übung in einem Satz, Minuten alt und neu, Outcome, neue Aussagen mit
   Doku-Zitat, entfernte Codeblöcke mit Digest und Grund, offene Punkte; VERIFICATION im Wortlaut; SOURCES READ.

Danach übernimmt, wer abnimmt: alle Kapitel lesen, jede Hauptübung durchspielen (tmux auf dem Linux-Rechner,
`--setting-sources project,local`), Korrekturen, Vertrag (Minuten, Personas, Golden), Ledger-Begründungen, Station,
`validate --complete`, Suite, lesende Codex-Gegenprüfung, Commit.

### Abschluss P7a (2026-10-05)

- **Schreiber** (Sonnet, Worktree `~/AI/worktrees/workshop-p7a`, Branch `p7a-schreiber`, zehn Commits, rund 390.000
  Tokens, 15 Minuten): alle zehn Kapitel mit neuer Übung, Auflösungen, Quiz mit echten Fehlvorstellungen; jede neue
  Aussage mit Doku-Zitat gemeldet. Übernommen als Merge `bacbf60`.
- **Gelesen und durchgespielt:** alle zehn Hauptübungen und die neue Station, je einmal (Claude Code 2.1.289, Linux,
  tmux). Neun liefen wie geschrieben. Korrigiert: S1.10 (`/context all` nennt die Dateien, Deny-Regel als nächste
  harte Sperre), S1.14 (dritte Antwort heißt in der Oberfläche „Tell Claude what to change“; Korrekturschritt verlangt
  jetzt `to_json` in `report.py`), S1.17 (Diff-Panel ist in breiten Terminals schon offen; `/review` läuft als
  Hintergrund-Agent mit einer Rückfrage), S1.18 („Keep worktree“, „Remove worktree“), S1.19 (`/cost` öffnet die
  Ansicht „Usage“, `Esc` schließt sie).
- **S1.20** ist der Abschluss von Session 1: CLAUDE.md, Deny-Regel, eigener präziser Auftrag, gezielter Commit auf
  einem Branch; Tabelle der zehn Übungen der Session. Neuer Titel „Praxis-Station Session 1: alles in einem Ablauf“.
  Durchgespielt (Docstring kam aus der CLAUDE.md, Löschen abgelehnt, zwei Dateien im Commit).
- **Vertrag:** Minuten S1.11 20, S1.12 20, S1.15 15, S1.16 15, S1.17 20, S1.18 20, S1.20 20; Titel S1.20; P02 von
  Hand (205 Minuten); Golden. 36 alte Codeblöcke mit Begründung im Ledger.
- **Wächter:** Ein toter Anker in S4.5 (auf eine umbenannte Überschrift in S1.17) fiel erst bei
  `validate --complete` auf; der Test der echten Bibliothek läuft jetzt vollständig.
- **Codex-Gegenprüfung der Kapitel (lesend, zwei Läufe):** beide FAIL, neun Befunde, alle an der Quelle geprüft
  und acht eingearbeitet: Regel in S1.10 verlangt jetzt einen Docstring; S1.11 nennt das Read-Werkzeug (Pfadregeln
  laden nicht bei `cat`); S1.15 verspricht den `Insight`-Block nicht mehr für jede Antwort; S1.14 prüft nur
  `git diff`; das Extra in S1.16 pusht erst den Hauptbranch; `/fork` mit Ausnahme; die Quizfragen in S1.18 und
  S1.19 nennen den Fall genauer; S1.20 sagt, was die Regel nicht sperrt. Der neunte betraf den JS-Port (siehe P6).
- **Nicht durchgespielt:** die Extras (PR in S1.16 braucht ein GitHub-Konto; `--system-prompt-file` in S1.15;
  Worktree von Hand in S1.18; Opus-Lauf in S1.19), alles unter Windows, und die Übungen nach den letzten
  Wortlaut-Korrekturen (geändert wurden Erwartungstexte und zwei Prompts: „Use the Read tool …“, die Regel mit
  „has a docstring“).
- **Offen:** Die Moderationsdateien zu S1.10, S1.13, S1.16, S1.18 und S1.19 beschreiben noch die alten Demos
  (`demo-1.2`, `validators.py`, „Testbank“); sie verweisen damit auf Übungsstände, die es im Kapitel nicht mehr
  gibt (→ P8, Moderationsschicht nachziehen). Der Schreiber schlägt vor, S1.11 zu teilen (Auto-Memory gegen übrige
  Ebenen) und `/voice` aus S1.15 in einen eigenen Hinweis zu legen (→ P8, mit R24).
- **Vorbereitung P7b:** `safety-check.sh` und `safety-check.ps1` blocken jetzt jede Eingabe, die kein JSON-Objekt
  ist (Tests zuerst: die Bash-Fassung ließ `null` durch, die PowerShell-Fassung auch leere Eingabe, Listen und
  bloße Werte). Die Snippets in S2.8 sind mitgezogen.

### Abschluss P7b (2026-10-05)

- **Schreiber** (Sonnet, zehn Commits `e70f6cb..b705de0`): S2.1 bis S2.10. Keine Übung schreibt mehr in die globale
  Konfiguration: Skills, Hook-Skripte und Registrierung liegen im Wegwerf-Ordner (`${CLAUDE_PROJECT_DIR}`). Befund
  R3 (PostToolUse nur nach Erfolg) steht im Text und in einer Übung. Übernommen als Merge `2c9f792`.
- **Durchgespielt:** alle zehn Hauptübungen, der `if`-Filter, das offene Gate und drei Handtest-Extras (Linux, tmux);
  unter Windows headless die Echo-Hooks aus S2.6 (Git Bash und `"shell": "powershell"`) und der Wächter aus S2.8 in
  der Exec-Form. Alle liefen wie geschrieben. Ergänzt: nach dem Speichern einer geänderten SKILL.md ein paar Sekunden
  warten (S2.2, S2.5).
- **Vertrag:** Minuten S2.1 bis S2.5 je 25, S2.6, S2.7, S2.9 je 20, S2.8 und S2.10 je 35; Golden. 26 alte Codeblöcke
  mit Begründung.
- **Codex-Gegenprüfung (lesend, zwei Läufe):** beide FAIL, fünf Befunde, alle bestätigt und eingearbeitet
  (`dc7e02e`): S2.3 (Claude kann die SKILL.md als Datei finden und von Hand befolgen; verwaltete Rechner), S2.6
  (`git status` schlägt nur außerhalb eines Repositorys fehl, jetzt `git show no-such-commit`, nachgespielt), S2.7
  (SessionStart feuert auch nach `/clear`, beim Fortsetzen und nach dem Komprimieren; das Extra braucht den Ordner).
- **Nicht durchgespielt:** PreCompact-Extra (S2.7), Panel-Migration (S2.2), interaktive Rückfragen unter Windows.
- **Offen (→ P8, mit R24):** S2.8 teilen (35 Minuten); das Gate aus S2.10 als eigenes Kapitel.

### Abschluss P7c (2026-10-05)

- **Schreiber** (Sonnet, dreizehn Commits `03d3e72..84c90de`): S2.11 bis S2.19 und X.1. Die MCP-Kapitel brauchen
  kein Node.js mehr: S2.14 bringt einen Server aus 75 Zeilen Python (nur Standardbibliothek), S2.15 und S2.17 nutzen
  ihn weiter, S2.16 hat einen zweiten mit 60.000 Zeichen Ausgabe. Playwright und NotebookLM sind Extras. Befund R4
  (Token als Rückfallwert) ist behoben. Übernommen als Merge `b72b648`.
- **S2.20** ist der Abschluss von Session 2 (neuer Titel „alles in einem Ablauf“): ein Skill ruft ein MCP-Tool und
  liest eine Wissensdatei, ein Hook schreibt den Aufruf mit, eine Regel sperrt das andere Tool; darunter die Tabelle
  der neunzehn Übungen. Durchgespielt samt Extra (derselbe Skill als Plugin).
- **Durchgespielt:** jede Hauptübung, die Extras von S2.11, S2.12 (ganzer Lebenszyklus im Scope `local`), S2.17 und
  S2.18 (Linux, tmux). Unter Windows headless: `plugin validate`, `plugin details`, die PowerShell-Pipe aus S2.14
  und der Server mit `"command": "python"`. **Sicherheitsprobe** für S2.13 und X.1: `plugin validate`,
  `plugin details` und `plugin list` mit `--plugin-dir` führen weder den SessionStart-Hook aus noch starten sie den
  MCP-Server eines Marker-Plugins.
- **Korrigiert nach den Läufen:** Die Server-Freigabe wählt „Continue without using this MCP server“ vor;
  `claude mcp add` schreibt schon ein leeres `env`; S2.16 Schritt 4 trifft die Zeichengrenze und formuliert anders;
  S2.17 fragte nach einem Standortnamen, der dort „unset“ ist; in S2.19 löste Claude den Widerspruch selbst, weil
  die alte Datei die Jahreszahl im Namen trug (jetzt ohne Datum, und der Vermerk in der Quelle ist ein eigener
  Schritt); nach dem Lebenszyklus in S2.12 bleibt die Kopie im Plugin-Cache liegen (zehnter Schritt).
- **Vertrag:** Minuten S2.11 25, S2.12 20, S2.13 25, S2.14 25, S2.15 25, S2.16 20, S2.17 25, S2.18 25, S2.19 20,
  S2.20 25, X.1 30; Titel S2.20; Katalog, Golden. 16 alte Codeblöcke mit Begründung.
- **Codex-Gegenprüfung (lesend, zwei Läufe):** beide FAIL, sieben Befunde; sechs eingearbeitet (`bdb9082`): „Will
  install“ ist nicht bei jedem Plugin eine Komponentenliste; zwei Ausnahmen der `./`-Regel; der Kopierbefehl der
  Station hing an einem Ordner, den S2.17 löschen lässt; „jeder gelungene Aufruf“; zwei Formulierungen als
  Beobachtung. Einer widerlegt (das Zeichenlimit je Tool ersetzt für Text auch das Token-Limit, mcp.md und Lauf).
- **Nicht durchgespielt:** Playwright (S2.14), NotebookLM (S2.18), die zweite Frage aus S2.19 in einer frischen
  Sitzung, alles Interaktive unter Windows.
- **Für P8 notiert:** `claude plugin list` zeigt über claude.ai gekommene Plugins in einem eigenen Abschnitt; die
  Moderationsdateien zu S2.11, S2.14 und S2.18 beschreiben noch die alten Demos.

### Abschluss P7d (2026-10-05)

- **Schreiber** (Sonnet, acht Commits `8861587..b4e5abd`): S3.1 bis S3.7 und X.3. Jedes Kapitel des Agenten-Regals
  hat jetzt eine Hauptübung (vier von sieben hatten keine). S3.6 funktioniert ohne Plugin und ohne Playground:
  Ankläger und Verteidiger als eigene Subagenten an einem Türprogramm mit 40 Zeilen, Auflösung nach der Übung; die
  Aussage „zwei Scanner einig, also echt“ ist ersetzt. Übernommen als Merge `8e75575`.
- **Durchgespielt:** alle Hauptübungen und die Extras von S3.1 (Fork) und S3.6 (Test belegt den Fehler). S3.1, S3.2,
  S3.4, S3.6 und S3.7 liefen wie geschrieben; `/security-review` arbeitet gegen ein lokales Bare-Repository als
  `origin`. **S3.3 korrigiert:** Wer um die Schreibfreigabe bittet, ist an der Rückfrage nicht abzulesen (beim
  lesenden Agenten fragte das Hauptgespräch, beim Agenten mit falschem Feldnamen der Subagent selbst); beide werden
  jetzt zuerst nach ihren Werkzeugen gefragt. **S3.5 korrigiert:** Nach `/exit` in einer angehängten Sitzung landet
  man auf der Tafel, nicht in der Shell (`Esc`). Auf dem Testrechner blieb kein Hintergrunddienst zurück.
- **Vertrag:** Minuten S3.1 20, S3.2 15, S3.3 25, S3.4 25, S3.5 20, S3.6 35, S3.7 25, X.3 25; Katalog, Golden. Fünf
  alte Codeblöcke mit Begründung.
- **Codex-Gegenprüfung (lesend, zwei Läufe):** beide FAIL, vier Befunde, alle bestätigt und eingearbeitet
  (`3a0f513`): `omitClaudeMd` (S3.2, S3.1), CLAUDE.md kommt trotz eigenem System-Prompt an (S3.3), Platzhalter im
  Suchbefehl (S3.6), „der Ordner“ als Grenze (X.3).
- **Nicht durchgespielt:** die Inventur in X.3, `--agents`, alles unter Windows.
- **Offen (→ P8, mit R24):** S3.7 vor S3.6 stellen und S3.6 teilen (ändert Kapitelbestand oder Nummern);
  Voraussetzungen S3.6 → S3.3 und S3.7 → S1.17; ein Quizblock in Community-Kapiteln (der Validator lässt keinen zu);
  X.3 nennt den Wegwerf-Ordner an zwei Stellen noch als äußere Grenze (mit F7 prüfen).

### Abschluss P7e (2026-10-05)

- **Schreiber** (Sonnet, neun Commits `a107ff0..f1a92ab`): S3.8 bis S3.14, S4.1, S4.2. Die Sicherheitskapitel haben
  Übungen, deren Ergebnis an `git` abzulesen ist; S3.14 hängt nicht mehr an einem Plugin-Befehl, den es nicht gibt;
  S4.2 hat eine Übung ohne zweiten Anbieter. Übernommen als Merge `7b75b5e`.
- **S3.15** ist der Abschluss von Session 3 (neuer Titel „alles in einem Ablauf“): Regeln, gedeckelter Lauf im
  Worktree, eigener Subagent als Gegenprüfung, Übernahme erst durch den eigenen Merge.
- **Neue getestete Vorlage:** `sensitive-data-scanner.py` (Tests zuerst; beide Scanner teilen die Tests). Damit
  braucht die Übung in S3.11 kein `jq` mehr. Offen für P8/R23: Die Bash-Fassung lässt die Eingabe `null` durch.
- **Durchgespielt und korrigiert:**
  - S3.8: Ein Sammelauftrag landete als eine Shell-Zeile und wurde in `dontAsk` als Ganzes abgelehnt; die Runden
    haben jetzt zwei Aufträge. Endfassung nachgespielt (Runde 1: Commit mit beiden Dateien; Runde 2: Änderung an
    `config.txt` und Commit abgelehnt), dazu das Extra (drei Umgehungsversuche, alle gestoppt).
  - S3.9: lief in allen drei Runden wie geschrieben (Rückfrage trotz Allow-Regel, Ablehnung in `dontAsk`).
  - S3.10, S3.11 (Python-Fassung), S3.13 (Linux und Windows): liefen wie geschrieben; in S3.13 ist der Worktree
    nach einem `-p`-Lauf immer gesperrt, das Aufräumen entsperrt jetzt zuerst.
  - **Allow-Regeln eines Projekts gelten in einem `-p`-Lauf erst nach dem Vertrauensdialog** (Probelauf der Station
    und permissions.md). Die Station hat dafür einen eigenen Schritt, S3.8 und S3.13 sagen es.
- **Codex-Gegenprüfung (lesend, zwei Läufe):** beide FAIL, acht Befunde, alle bestätigt und eingearbeitet (Ask-Regel
  fragt auch in `auto`; `/sandbox` trägt die lokale Settings-Datei in die globale Ignore-Liste ein; „mindestens fünf
  Runden“ war nicht belegt; Ausweich-Präfix in S3.14; Datenfluss in S4.2; zweites Terminal in S3.12; `python3`).
- **Vertrag:** Minuten S3.8 30, S3.9 30, S3.10 20, S3.11 25, S3.12 30, S3.13 25, S3.14 20, S3.15 25, S4.1 25,
  S4.2 25; Titel S3.15; Katalog, Golden. Neun alte Codeblöcke mit Begründung.
- **Nicht durchgespielt:** die Extras zu Sandbox (S3.9), eigenem Muster (S3.11), Routine (S3.12) und falscher Regel (S3.14); in S3.12 `/goal` ohne Argument und `/goal clear` (die Eingaben landeten im Probelauf in einer Rückfrage zum Testbefehl); S4.1 nach der Planfreigabe (läuft beim Commit, Nachtrag folgt); S4.2 ist eine Papierübung; unter Windows alles außer den PowerShell-Startblöcken (S3.8, S3.9, S3.13, S3.14, S3.15) und dem gedeckelten Lauf aus S3.13.
- **Offen (→ P8):** Voraussetzungen S3.10 → S3.8/S2.5, S3.11 → S2.8, S3.13 → S3.8, S4.2 → S3.11; S3.9 teilen
  (geschützte Pfade, Sandbox-Stufen); die Moderationsdateien zu S3.8, S3.13, S3.14 und S4.2 beschreiben die alten
  Demos; unter Windows hinterlassen Hooks aus den eigenen Benutzer-Einstellungen Dateien im Worktree, dann scheitert
  `git worktree remove` (Hinweis für S3.13 prüfen).

### Abschluss P7f (2026-10-05)

- **Schreiber** (Sonnet, neun Commits `b8c539c..ac73790`): S4.3 bis S4.7, S4.9, S4.10, X.4. Damit hat jede der 61
  Lektionen eine Übung und eine Auflösung. S4.4 trägt jetzt der Sicherheitskern (Zugang, Deckel, `--bare`); S4.7
  braucht kein Workshop-Plugin mehr; S4.9 und S4.10 haben Übungen für eine Person; der Notaus in X.4 gilt einer
  eigenen Hintergrund-Sitzung. Übernommen als Merge `cc1052a`.
- **Durchgespielt (Linux):** S4.3, S4.4, S4.5 vollständig per Skript; S4.7, S4.9 (mit Extra), S4.10 und X.4 in
  tmux. Unter Windows (PowerShell 5.1) die PowerShell-Blöcke von S4.3 samt Quoting des Schemas. Bestätigt: Der
  Hook eines nie bestätigten Ordners läuft in einem `-p`-Lauf ohne `--bare` (S4.4); `--bare` ohne API-Key endet
  mit „Not logged in“; der Budgetdeckel liefert `error_max_budget_usd` und Exit 1.
- **Korrigiert nach den Läufen:** Meldung zum ungültigen Schema (S4.3); das Debug-Log der interaktiven Sitzung
  enthielt zum Hook keine Zeile (S4.10, Schritt 4 nennt jetzt beide Ausgänge); in S4.7 fragt Claude Code erst um
  Erlaubnis, die Datei im Hauptordner zu lesen; zwei Quiz-Antworten gekürzt (Regel `quiz-longest-share`).
  S4.9: Mit dem ungültigen `matcher` öffnet die Sitzung einen eigenen Dialog („Files with errors are skipped
  entirely“; Fix with Claude / Exit and fix manually / Continue without these settings) und überspringt die
  Freigabe des Projekt-MCP-Servers („skipping .mcp.json server approval (settings errors in …)“). Der Server
  steht deshalb erst nach der Reparatur von Fehler 1 und einem Neustart in `/mcp` (Schritte 2 und 6 umgestellt).
  Im Safe Mode listet `/hooks` den Projekt-Hook weiter auf, er läuft aber nicht (Extra prüft das jetzt nach).
- **Nachtrag P7e:** S4.1 nach der Planfreigabe (Rückfrage zu Prüfbefehlen, Haiku ohne Befund).
- **Codex-Gegenprüfung (lesend, zwei Läufe):** beide FAIL, sechs Befunde, alle an der Quelle bestätigt und behoben: S4.3 (`dontAsk` allein heißt nicht nur lesen; die Abschlussliste lässt den längeren Auftrag zu), S4.4 zweimal („immer genutzt“ meint die fehlende Rückfrage im `-p`-Modus, die Rangfolge ist eine eigene Aussage), S4.5 (die Kurzschreibweise im Extra war kein JSON Schema), S4.7 zweimal (ein Container trennt nicht vollständig; für ein Repository, dem man nicht traut, nennt die Doku eine eigene VM oder eine Cloud-Sitzung).
- **Vertrag:** Minuten S4.3 25, S4.4 30, S4.5 30, S4.6 20, S4.7 25, S4.9 30, S4.10 30, X.4 35; Katalog, Golden.
  17 alte Codeblöcke mit Begründung.
- **Nicht durchgespielt:** S4.6 (Remote Control braucht einen Browser oder ein zweites Gerät), das GitHub- und GitLab-Material von S4.5, die Extras außer dem von S4.9; aus P7e weiterhin `/cost` in S4.1.
- **Offen (→ P8):** S4.4 teilen (R24); X.4 mit 35 Minuten und `requires` (D7 schlägt S3.13, S4.4 vor); S4.9 und
  S4.10 stehen als Kern hinter S4.8; `--output-format json` liefert mit `verbose` in den Benutzer-Einstellungen
  ein Array statt eines Objekts (auf dem Windows-Rechner beobachtet, Hinweis für S4.3 prüfen).

### Abschluss P7 (2026-10-05)

Alle sechs Teilpakete sind übernommen. Die Regeln des Maßstabs gelten im Validator für jedes Kapitel; die
Pflichtliste `tools/fixtures/standard-chapters.txt` ist entfallen (`load_standard` nimmt alle Kapitel der
Bibliothek). 61 von 61 Lektionen haben eine Übung und eine Auflösung, die drei Stationen sind Session-Abschlüsse,
S4.11 schließt jeden Pfad. Was die Läufe gelehrt haben, steht im Maßstab unter „mitzunehmen“. Als Nächstes: P8.

---

## P8 — Restliche Inhaltsbefunde

R3 (PostToolUse nur nach Erfolg: Kapiteltext, Handtest, zweiter Hook an PostToolUseFailure), R4 (S2.15
Rückfallwerte), R5 (50.000-Zeichen-Schwelle, auch `karte-erweitern.md`), R6 (Quoting, Cache-Pfad), R7 (Demo S2.8,
jetzt in der Moderationsschicht), R9 (`claude purge`, Kanon, Karten), R10, R11, R12 (Rechtsaussagen mit Quelle oder
weicher), R23 (Windows-Weg der Hook-Kapitel, `.ps1` für Schwärzung und Token Firewall mit Tests), R24 (S2.10,
S3.6, S4.4 teilen: ändert den Kapitelbestand, also wie P6 mit Vertrag), R25 (Bilder), R29 (Fehlersuche früher:
Diagnose-Kasten in S2.8, Verweis von S2.2 und S2.15), R30 (Stufen der Sicherheitskapitel). Vor Beginn in
Teilpakete schneiden; was P7 schon erledigt hat, hier abhaken.

## P9 — UI-Überarbeitung

Erst nach P8. Eingang: B1 bis B12 aus `docs/reviews/2026-10-02-cockpit-durchgang.md`, die Beobachtungen vom
2026-10-05 (Bibliothekskacheln zeigen nur IDs; ohne Einstufung steht jedes Kapitel auf „später“; „Als erledigt
markieren“ steht vor dem Inhalt; Kurzansicht und Volltext doppeln sich) und was P2 bewusst offen lässt. Eigene
Fragerunde mit dem Owner, bevor etwas gebaut wird.

---

## Plan-Prüfung 2026-10-05 (Modus: Scope halten)

Der Owner hat Umfang und Reihenfolge bestätigt; geprüft wurde auf Fehlermodi, nicht auf mehr oder weniger Umfang.
Die Befunde sind technische Schärfungen und oben eingearbeitet. Der Merge-Takt ist entschieden (Owner, 2026-10-05): Pakete auf dem Branch sammeln; ein Merge oder Push zwischendurch ist möglich, aber nicht nötig.

### Geprüfte Alternativen

| Ansatz | Kern | Urteil |
|---|---|---|
| Nur ausblenden | Cockpit und Tutor verbergen „Vorführen“, dazu Auflösungen | zu wenig: Markdown auf GitHub bleibt der Live-Kurs, Übungen fehlen weiter |
| **Schicht und Inhalte (gewählt)** | Moderation in eigene Dateien, Kapitel für eine Person allein, Abschluss | erhält geprüften Inhalt und Werkzeug, in Paketen lieferbar |
| Neuer Selbstlernkurs | rund 30 Kapitel neu schreiben | löst auch den Umfang (36 bis 53 von 70), verwirft aber belegten Text und den Snippet-Ledger; nicht jetzt |

### Was schon da ist und genutzt wird

Parser und Validator (`library_model`, `build_library`), Generator für Katalog, Pfade und Cockpit, der
Einstufungsvertrag mit Personas und Golden, Snippet-Ledger, getestete Hook-Vorlagen, der Aktualitäts-Lint, der
Tutor im teach-Stil, die 14 Berichte der Durchsicht als Auftragsgrundlage, der Doku-Stand vom 2026-10-05.

### Fluss

```
Kapitel (resources/library)  ──parse──▶  Modell  ──validate──▶  Befunde (Exit 1)
        │                                  │
        │                                  ├──▶ catalog.json ──▶ Tutor (next, learn, review)
        │                                  ├──▶ Cockpit (eine Datei) ──▶ Browser, localStorage
        │                                  └──▶ Pfade, README, einstufung.md
Moderation (resources/moderation/vorfuehren)  ──▶  Live-Pfad, Tutor (guide)   [nicht ins Cockpit]
```

Kapitelansicht im Cockpit nach P2:

```
Status work ──▶ voller Kapiteltext, Quiz, „erledigt“ am Ende
Status skim / skip / later / keine Einstufung ──▶ Kurzansicht, Volltext eingeklappt
Volltext fehlt im Artefakt ──▶ Kurzansicht mit Link
```

### Fehlermodi

| Was schiefgehen kann | Wie es sichtbar wird | Was dann gilt |
|---|---|---|
| Migrationsskript schneidet falsch (eine `## `-Zeile in einem Codeblock) | Abschnittsgrenzen kommen aus dem Projekt-Parser; `--check` vergleicht Zeilen und Wortsummen | Lauf verwerfen (`git checkout`), Skript korrigieren |
| Ein relativer Link zeigt nach dem Verschieben ins Leere | Link-Prüfung deckt den neuen Ordner ab, Exit 1 | Ziel im Skript nachziehen |
| Lektion ohne Cockpit-Beispiel nach dem Verschieben | Validator („genau ein Beispiel“) | Schritt 2a in P1 |
| Auflösungen zählen nicht zu den Fragen | Validator, Exit 1 | Kapitel korrigieren |
| Schreiber erfindet einen Befehl oder ein Flag | Doku-Beleg im Auftrag Pflicht, Diff-Lektüre, Codex-Gegenprüfung, Aktualitäts-Lauf | Aussage streichen oder belegen |
| Übung lässt sich allein nicht lösen | Durchspiel-Probe je Hauptübung | Übung ändern, bevor das Paket schließt |
| Python- und JS-Engine laufen nach einer Regeländerung auseinander | Vektoren-Tests beider Engines | beide Seiten im selben Commit |
| Zwei Schreiber ändern dieselbe generierte Datei | Schreiber bauen nicht; ein Teilpaket nach dem anderen | Konflikt gar nicht erst erzeugen |
| Cockpit überschreitet 3 MB | Generator-Prüfung (in P3 nachsehen, ob sie greift) | Diagramme fallen zuerst weg (Spec §8) |
| Demo-Datei ohne Kapitel oder Kapitel verweist auf fehlende Demo | Katalog-Test in P1 | Datei oder Verweis entfernen |
| Tutor findet im Modus `guide` keine Demo | sagt es und improvisiert nicht (Regel aus dem Skill, auf die Demo-Datei erweitern) | — |

### Zurückgestellt (als Todo unter DCO #9632)

- Übungen automatisch in einem Lauf prüfen („getestet statt behauptet“ auch für Übungen): Idee, kein Paket.
- Umfang der Neulingspfade (36 bis 53 von 70): erst nach P7 beurteilen, wenn Kapitel zusammengelegt sind.
- Website-Export des Cockpits bleibt DCO #9528.

### Zusammenfassung

Modus Scope halten · Ansatz „Schicht und Inhalte“ · Schärfungen: Skriptort und Parser-Naht (P1), vier Kapitel mit
Beispiel in „Vorführen“ (P1), Volltext ersetzt Kurzblöcke bei `work` (P2), Fortschrittszahlen und Größengrenze (P3),
Zeilennummern im Playground (P4), ehrliche Zeit, Wegwerf-Ordner und Durchspiel-Probe (P5, P7), Schreiber bauen
nicht (P7). Merge-Takt: gesammelt, siehe oben.
P8 und P9 sind bewusst grob gehalten und werden vor ihrem Beginn geschnitten.
