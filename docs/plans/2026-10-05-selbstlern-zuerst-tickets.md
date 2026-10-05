# Selbstlernende zuerst — Pakete

> Entwurf: `docs/plans/2026-10-05-selbstlern-zuerst-design.md` · Befunde: `docs/reviews/2026-10-05-lernbogen-und-fakten.md`
> Branch `selbstlern-zuerst`. Diese Datei ist der Stand: Ein Paket ist erledigt, wenn sein Kasten angekreuzt ist und
> der Commit daneben steht. Eine frische Sitzung liest diese Datei, nimmt das erste offene Paket ohne offene
> Vorbedingung und liest dessen Abschnitt ganz.

## Für jede Sitzung

- Vor dem ersten Schritt: `git status -sb` (Branch `selbstlern-zuerst`, sauber) und
  `python -m pytest tools -q -p no:cacheprovider` (grün; Stand nach P2: 688).
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
| P2 | Cockpit und Tutor zeigen bei „durcharbeiten“ Lehrtext und Übung (R19) | P1 | [x] siehe Abschluss P2 |
| P3 | Auflösungen: Format, Validator, Cockpit, Tutor; ein Kapitel als Durchstich (R15) | — | [ ] |
| P4 | Playground ohne Lösungshinweise (R18, R13) | — | [ ] |
| P5 | Pilotregal Einstieg S0.1 bis S1.9 samt X.2: Maßstab für alle Inhalte (R14, R15, R17, R21, R22, R26, R28) | P1, P3, P4 | [ ] |
| P6 | Abschluss: Kapitel S4.11 in jedem Pfad, Praxis-Stationen als Session-Abschlüsse (R16) | P5 | [ ] |
| P7 | Ausrollen je Regal-Paket nach dem Maßstab (sechs Teilpakete, Sonnet-Schreiber, Codex-Gegenprüfung) | P5 | [ ] |
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

---

## P7 — Ausrollen je Regal-Paket

**Ziel:** Alle übrigen Lektionen nach dem Maßstab aus P5: Auflösungen, Übung in jeder Kern-Lektion, kein Rest des
Live-Formats im Lernweg, Demo-Inhalt als Übung, wo er trägt.

| Teilpaket | Kapitel | Didaktik-Bericht | Fakten-Bericht |
|---|---|---|---|
| P7a | S1.10 bis S1.19 | D2 | F2 |
| P7b | S2.1 bis S2.10 | D3 | F3 |
| P7c | S2.11 bis S2.19, X.1 | D4 | F4, F7 |
| P7d | S3.1 bis S3.7, X.3 | D5 | F4, F7 |
| P7e | S3.8 bis S3.14, S4.1, S4.2 | D6 | F1, F5 |
| P7f | S4.3 bis S4.10, X.4 | D7 | F6, F7 |

Ablauf je Teilpaket: Auftrag (Skill `subagent-briefing`) mit Maßstab-Datei, Kapitel-Liste, den beiden Berichten
und der zugehörigen Moderationsdatei als Quelle für Übungen → ein Sonnet-Schreiber (`model: sonnet`, eigener
Worktree) → Fable liest den Diff und prüft Stichproben gegen die Doku → Codex prüft lesend gegen
(`codex exec -s read-only`, Auftrag über stdin) → Befunde einarbeiten → Commit. Höchstens zwei Runden Nacharbeit
je Teilpaket, dann entscheidet Fable selbst. Die Zahlen der Schreiber (Fragen, Übungen) vor Übernahme nachzählen.
Schreiber ändern nur Kapitel und Moderationsdateien ihres Teilpakets; sie bauen nichts und committen keine
generierten Dateien (sonst kollidieren Katalog und Cockpit). Gebaut wird nach dem Übernehmen, ein Teilpaket nach
dem anderen. Die Hauptübung je Kapitel wird durchgespielt (siehe P5), nicht vom Schreiber selbst.

**Fertig, wenn:** die Auflösungs- und die Übungsregel im Validator für alle Lektionen gelten (die Pflichtliste aus
P3 entfällt); Suite grün.

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
Die Befunde sind technische Schärfungen und oben eingearbeitet. Eine Entscheidung bleibt beim Owner: der Merge-Takt.

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
nicht (P7). Offen beim Owner: nach jedem Paket nach `main` mergen (Empfehlung) oder gesammelt am Ende.
P8 und P9 sind bewusst grob gehalten und werden vor ihrem Beginn geschnitten.
