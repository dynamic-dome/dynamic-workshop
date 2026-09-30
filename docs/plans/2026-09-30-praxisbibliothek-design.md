# Praxisbibliothek statt Kursordner — Design

> Stand: 2026-09-30 · Branch `praxisbibliothek` (Worktree `dynamic_workshop-bibliothek`, ab `ba222d2`)
> Auftrag und Entscheidungen: Dominic, 2026-09-30 (siehe „Entscheidungen"). Status: v3.2 — freigegeben durch Codex-Runde 4 (APPROVE-WITH-CHANGES, §15).

## 1. Auftrag in einem Absatz

Der Kurs ist fachlich solide (Phase 1+2, September), aber schwer zu bedienen. Er wird zur **deutschsprachigen
Claude-Code-Praxisbibliothek** umgebaut: ein Kapitel je Lerneinheit als **einzige Quelle**, thematische Regale,
eine **Einstufung** (Stand, Ziel, Warum, Zeit), die einen **persönlichen Pfad** empfiehlt, statt alles von vorn bis
hinten durchzuarbeiten. Das Cockpit, der `/workshop`-Tutor in Claude Code und eine Markdown-Seite lesen dieselbe
Regeldatei. Doppelungen verschwinden, Visualisierungen und das Deck werden neu gebaut, ein Community-Regal stellt
Leute und Skills vor, die wirklich helfen (Matt Pococks `/teach` ist zugleich Vorbild für den Tutor).

### Entscheidungen (Dominic, 2026-09-30)

| Frage | Entscheidung |
|---|---|
| Umbau-Tiefe | Bibliothek als Quelle — alte Modul-/Demo-/Übungsdateien werden ersetzt, nicht kopiert |
| Sprache | Deutsch; Code, Befehle, Dateinamen, Bezeichner Englisch |
| Einstufung | Cockpit + `/workshop start` + Markdown, eine gemeinsame Regeldatei |
| Haltepunkte | durchziehen; unabhängiger Prüfer (Codex/Sonnet) statt Owner-Review; Halt nur vor Push und Website-Export |
| Ressourcen | Workflows/Multi-Agent ausdrücklich erlaubt |

### Was er gesagt hat vs. was ich annehme

- **Gesagt:** überarbeiten, korrigieren, besser handhabbar, Stärken hervorheben, Schwächen ausbessern, Doppelungen
  weg, bessere Visualisierungen/Präsentationen, sinnvolle Anleitung, Einstufung ohne Bedrängen, Kapitel empfehlen,
  groß gedacht eine Wissensbibliothek, `/teach`-Ideen integrieren, interessante Leute/Skills vorstellen.
- **Angenommen:** Hauptzielgruppe bleibt das öffentliche Selbstlernen (Entscheid 2026-09-28); der Live-Workshop
  wird ein Pfad unter mehreren. Die 65 LE-IDs bleiben als stabile Schlüssel (Cockpit-Fortschritt in localStorage,
  Mentor, Deep-Links). Inhaltlich wird nichts Neues gelehrt außer den zwei Community-Kapiteln; die Phase-3-Versprechen
  (Eval-Modul usw.) bleiben eigene Tickets.

## 2. Befund (Kurzfassung)

Stärken, die bleiben und sichtbarer werden: Security-Analogien, verwundbarer Playground, Capstone-Rubrik,
getestete Hook-Assets + Wächter-Tests (203 grün), Aktualitäts-Mechanismus (Kanon, Lint, Monatslauf),
Drei-Schicht-Modell `core`/`deep-dive`/`bonus`, Recovery-Notes in Demos.

Schwächen (Belege in der Bestandsaufnahme, Anhang A):
1. Vier überlappende Einstiege (README, `WORKSHOP_EINFUEHRUNG.md`, `resources/workshop-guide.md`, `HOW-TO-USE.md`),
   zwei Decks; `CLAUDE.md`/README verweisen auf das alte Deck vor Welle F.
2. Vier Nummernsysteme (Module 1.1–3.7, LE S1.1–S4.10, Übungen 1.1–3.9, Demos 2.2b …); Session 4 speist sich aus Modul 3.x.
3. Ein Thema über 5–6 Orte verteilt (Modul, Demo-Datei, Übungsdatei, Cheatsheet, Cockpit-Kopie); Moduldateien
   folgen nicht der Lehrreihenfolge.
4. Das Cockpit hält eine zweite Inhaltskopie (≈207 KB Inline-Daten) — historisch die Drift-Quelle.
5. Sprachmix: Module Englisch, Cockpit/Website/Landkarten Deutsch.
6. Review-Archive und Arbeitsnotizen liegen zwischen Lernmaterial in `resources/`; ein 821-Zeilen-Cheatsheet baut
   die offizielle Doku nach (größte Drift-Fläche).
7. Keine Einstufung, kein persönlicher Pfad; Minimalpfad nur als Prosa-Satz.

## 3. Zielbild

```
README.md                      Schaufenster: was, für wen, drei Einstiege, Regal-Karte
HOW-TO-USE.md                  Anleitung: Selbstlernen · Moderieren · Pflegen
resources/
  library/                     DIE Quelle: ein Kapitel je LE (+ X.1, X.2), flach, ID-sortiert
    _shelves.yaml              Regale: id, Titel, Beschreibung, Reihenfolge, Farbe
    _placement.yaml            Einstufung: Fragen, Bereiche, Ziele, Regeln
    README.md                  GENERIERT: Regal-Übersicht + Karte
    einstufung.md              GENERIERT: Selbst-Einstufung zum Ausfüllen (Markdown-Oberfläche)
    catalog.json               GENERIERT: Metadaten + Regeln für Cockpit und Tutor
    s1-01-first-contact.md … s4-10-diagnose-sequenzen.md, x-01-community-skills.md, x-02-lernen-mit-claude-code.md
  paths/                       GENERIERT aus Kapiteln + Regeln: live-workshop.md, schnellstart.md, ziel-*.md
  reference/                   druckbare Karten (je ≤ 1 Seite, Doku-Link + Prüfstempel): karte-start-und-flags,
                               karte-rechte, karte-hooks, karte-kontext, karte-erweitern (Skills/Plugins/MCP),
                               karte-agenten-worktrees, karte-kosten, karte-fehlersuche, karte-alte-namen;
                               glossar.md, analogien.md (GENERIERT aus „Bild im Kopf" der Kapitel), faq.md (nur Fragen ohne
                               Kapitelheimat), adoptionsplan-vorlage.md, kosten-nachbau.md; README.md (Index)
  moderation/                  README.md, handbuch.md (trainer-notes, live-3-person, recap-bridges, transfer,
                               Ablauf/Zeiten aus session-plan), vorbereitung.md (Plugins/Assets aus prerequisites,
                               Dry-Run-Checklisten), videos.md (video-scripts, als historisches Transkript markiert)
  media/                       Deck (neu), Video-Folien, Intro-Video/Podcast
  demos/assets/                bleibt (getestete Hook-Assets, broken-greeter)
  _canonical.md                bleibt Kanon (Modelle, Preise, Prüfdatum)
  claude-code-workshop-ui.html GENERIERT aus tools/cockpit/template.html + catalog (Pfad bleibt, Website-Export)
docs/reviews/                  alle Review-Archive (2026-05-21, 06-21, 07-04, 09-28) + HANDOFF.md
tools/build_library.py         Parser, Validator, Generator (validate | build | check)
tools/placement.py             Einstufungs-Engine (nur Standardbibliothek), CLI für den Tutor
tools/cockpit/template.html    Cockpit-Quelle (CSS/JS), Daten werden injiziert
```

Entfällt (Inhalt migriert, Historie in Git): `resources/modules/`, `resources/demos/*.md`, `resources/exercises/`,
`WORKSHOP_EINFUEHRUNG.md`, `resources/workshop-guide.md`, `resources/quick-reference.md`, `resources/cheatsheet.md`,
`resources/faq.md`, `resources/troubleshooting.md` (→ Kapitel + Referenzkarten), `resources/session-plan.md`
(→ `paths/live-workshop.md` + Moderations-Handbuch), `resources/prerequisites.md` (→ S0.1 + `moderation/vorbereitung.md`),
`resources/trainer-notes.md`, `live-3-person-mode.md`, `retrieval-recap-bridges.md`, `transfer-retention-plan.md`,
`capstone-exit-assessment.md` (→ S4.8), `security-analogies.md`, `glossary.md` (→ `reference/`), altes Deck
`claude-code-workshop.pptx` und `claude-code-workshop-4session.pptx` (→ neues Deck in `media/`). `HANDOFF.md` und
die Review-/Audit-Dateien wandern unverändert nach `docs/reviews/`. Genaue Zielorte je Datei: Anhang B.

## 4. Kapitel-Format

### 4.1 Dateiname, ID, Reihenfolge

- IDs: `S<s>.<p>` mit s ∈ 0–4 (S0.1 = neues Setup-Kapitel „Werkstatt einrichten", Session 0 = Vorbereitung vor
  Session 1) und `X.<n>` für Kapitel ohne Live-Session (X.1, X.2).
- Dateiname: `resources/library/s<s>-<pp>-<slug>.md` (pp zweistellig, z. B. `s2-08-hook-konfigurieren.md`),
  `x-<nn>-<slug>.md`. Der Validator prüft, dass Dateiname und ID zusammenpassen.
- Reihenfolge wird **abgeleitet**, nicht gepflegt: `order(S<s>.<p>) = s × 1000 + p × 10` (S0.1 = 10, S2.8 = 2080,
  S4.10 = 4100); `order(X.n) = order(after) + 5` mit Pflichtfeld `after`. Session = s (X-Kapitel: keine Session).
- Pflicht-IDs (Validator, Vollständigkeit): S0.1, S1.1–S1.20, S2.1–S2.20, S3.1–S3.15, S4.1–S4.10, X.1, X.2.
- Alte Modulnummern bleiben als `aliases` erreichbar (`/workshop learn 2.2` → Einstieg Hooks-Regal), eindeutig über
  alle Kapitel.

### 4.2 Frontmatter (YAML, schmal)

```yaml
---
id: S2.8
type: lesson           # lesson | setup | practice | capstone | community
title: Einen Hook konfigurieren
shelf: hooks
level: core            # core | deep-dive | bonus
minutes: 15
after: null            # nur X-Kapitel: ID, nach der sie einsortiert werden (z. B. S2.13)
requires: [S2.6, S2.7] # nur Kapitel mit kleinerem order (Validator), keine Zyklen
safety_floor: false    # true = nie unter „überfliegen" (Regel §6.3)
transferable: true     # Agentic-Coding-Prinzip, nicht nur Claude-Code-Bedienung
outcome: "Ich kann einen PreToolUse-Hook eintragen, der mit exit 2 wirklich blockt."
sources:
  - https://code.claude.com/docs/en/hooks
aliases: ["2.2"]       # alte Modulnummern, eindeutig über alle Kapitel
# nur type: practice →  offers: [S2.2, S2.8, S2.11]  (Kapitel, deren Übungen die Station anbietet; requires: [])
---
```

### 4.3 Körper (feste H2-Reihenfolge, deutsch, „du")

Kapiteltypen und ihre Pflichtabschnitte (✔ Pflicht, ○ optional, – nicht erlaubt):

| Abschnitt | lesson | setup | practice | capstone | community |
|---|---|---|---|---|---|
| Schnellcheck | ✔ | ○ | – | ○ | – |
| Auf einen Blick | ✔ | ✔ | ✔ | ✔ | ✔ |
| Bild im Kopf | ✔ | ○ | – | ○ | ○ |
| Im Detail | ✔ | ✔ | – | ✔ | ✔ |
| Vorführen | ○ | – | – | ○ | – |
| Selbst machen | ○ | ✔ | ✔ (Übungswahl + Links + Pool) | ✔ (Aufgabe + Rubrik) | ○ |
| Typische Fallen | ○ | ○ | – | ○ | ○ |
| Check | ✔ | ✔ | ✔ | ✔ | ○ |
| Weiterlesen | ✔ | ✔ | ○ | ✔ | ✔ |
| `cockpit:example` | genau 1 | ≤ 1 | ≤ 1 | ≤ 1 | ≤ 1 |
| Quiz im Check | genau 1 | ≤ 1 | – | ≤ 1 | – |

Übungen stehen nur in ihrem Heimat-Kapitel (§5); Praxis-Stationen verlinken sie und besitzen nur Einleitung,
Auswahlhilfe und den optionalen Übungspool.

```markdown
# S2.8 · Einen Hook konfigurieren
<!-- meta:start -->  … GENERIERT: Regal · Stufe · Minuten · Voraussetzungen · zurück/weiter · Sicherheitsboden-Hinweis …  <!-- meta:end -->

## Schnellcheck            2 Verhaltensfragen; „Beides sicher ja? → weiter zu …" (optional nur für practice)
## Auf einen Blick         2–4 Sätze Kern (→ Cockpit „Konzept")
## Bild im Kopf            Security-Analogie, erster Absatz → Cockpit „Analogie"; optional ```mermaid
## Im Detail               eigentlicher Lehrtext (migriert), ### Unterabschnitte
## Vorführen               Demo (migriert); Moderationshinweise in <details><summary>Für Moderierende</summary>
## Selbst machen           Übung(en) (migriert); genau ein Block mit <!-- cockpit:example --> davor
## Typische Fallen         optional
## Check                   Checkpoint-Satz (→ Cockpit „Checkpunkt"), Quiz in <details>, 2–3 Abruffragen
## Weiterlesen             offizielle Doku (sources) zuerst, verwandte Kapitel, Referenzkarte
```

Pflichtabschnitte je Typ: Tabelle oben. Quiz-Block (parsebar):

```markdown
<details><summary>Quizfrage</summary>

**Frage:** …

- **Richtig:** …
- Falsch: …
- Falsch: …
- Falsch: …

</details>
```

Quiz-Regel aus `/teach`: Antworten etwa gleich lang (Validator warnt, wenn die richtige > 1,3 × Mittel der falschen).

### 4.4 Stilregeln für Kapitel

- Deutsch mit korrekten Umlauten, Anrede „du", kurze Sätze; Fachbegriffe beim ersten Auftreten erklärt und dann
  wie in `resources/reference/glossar.md` verwendet.
- **Codeblöcke, Befehle, JSON, Pfade byte-identisch aus der Quelle** (Snippet-Ledger prüft). Kommentare in
  Codeblöcken bleiben, wie sie sind.
- Marker bleiben erhalten und stehen an derselben Stelle relativ zum Snippet: `tested asset: …`, `version-pinned: …`.
- Keine Modellgenerationen außerhalb des Kanons (Lint), Aliase und Rollen.
- Custom- vs. Built-in-Kennzeichnung (🔧) bleibt.
- Nicht verwenden: KI-typische Floskeln (Nutzerliste, u. a. das Bild der „verheilten Wunde" für Fehler — stattdessen „was schiefgegangen ist", „Fehler"), keine Werbesprache, keine unbelegten Zahlen.

## 5. Regale

`_shelves.yaml` (Reihenfolge = Lernlogik). Jedes Regal hat Titel, einen Satz „wofür", eine kurze Einleitung
(2–4 Sätze, gespeist aus den bisherigen Modulköpfen/Lernzielen) und optional ein Regal-Diagramm. **Regale bekommen
keine eigene Farbe** (19 Kategorien sind mit keiner farbfehlsicheren Palette unterscheidbar, siehe dataviz-Regeln);
Farbe trägt im Cockpit nur den **Pfad-Status**, Regale werden über Position und Beschriftung erkannt.

| Regal | Titel | Kapitel |
|---|---|---|
| `start` | Erste Schritte & Denkmodell | S0.1 (neu: Werkstatt einrichten, aus `prerequisites.md`), S1.1–S1.4 |
| `permissions` | Rechte & Freigaben | S1.5, S1.6, S3.8, S3.9 |
| `context` | Kontext & Gedächtnis | S1.8–S1.12 |
| `prompting` | Aufträge formulieren | S1.13–S1.15 |
| `git` | Git & Worktrees | S1.16–S1.18 |
| `cost` | Modelle & Kosten | S1.7, S1.19, S4.1 |
| `skills` | Skills & Commands | S2.1–S2.5 |
| `hooks` | Hooks | S2.6–S2.10 |
| `plugins` | Plugins | S2.11–S2.13 |
| `mcp-knowledge` | MCP & Wissensquellen | S2.14–S2.19 |
| `agents` | Agenten & Orchestrierung | S3.1–S3.5, S4.2 |
| `security` | Gegenprüfung & Compliance | S3.6, S3.7, S3.10, S3.11 |
| `automation` | Automation & Loops | S3.12–S3.14 |
| `headless-ci` | Headless & CI/CD | S4.3–S4.5 |
| `remote-isolation` | Remote, Docker, Isolation | S4.6, S4.7 |
| `troubleshooting` | Fehlersuche | S4.9, S4.10 |
| `capstone` | Abschlussprojekt | S4.8 |
| `practice` | Praxis-Stationen | S1.20, S2.20, S3.15 (verlinken die Übungen, besitzen nur Einleitung + Übungspools) |
| `community` | Community & Lernen | X.1, X.2 |

Heimat-Regel beim Umzug: Jeder Quelltext-Abschnitt hat genau **ein** Heimat-Kapitel (kleinster zuordnender
Bereich, Praxis-Stationen zuletzt, dann primär vor sekundär, dann Lehrreihenfolge); andere Kapitel verlinken.
Berechnet aus der Quellenkarte, Anhang A.

## 6. Einstufung

### 6.1 Leitplanken („ohne Bedrängen")

- Dauer ≤ 5 Minuten, jederzeit überspringbar, Ergebnis jederzeit änderbar; keine Punkte, keine Noten.
- **Verhaltens- statt Wissensfragen** („Hast du schon einen Hook gebaut, der wirklich blockt?"), weil
  Selbsteinschätzung zu Überschätzung neigt. „Weiß nicht" ist eine gültige Antwort und zählt wie „neu".
- **Mini-Szenarien sind freiwillig**, unbenotet, mit erklärender Rückmeldung („Das verwechseln viele — Kapitel S2.8").
  Eine falsche Antwort deckelt den Bereich auf „gehört davon", mehr nicht.
- Das Ergebnis heißt „Empfehlung", zeigt je Kapitel eine **Begründung** und lässt sich pro Kapitel übersteuern.
- **Sicherheitsboden:** Kapitel mit `safety_floor: true` (Rechte-Modi, fail-open bei Hooks, Secrets, fremder Code)
  fallen nie unter „überfliegen" — außer die Person übersteuert selbst; dann zeigt das Ergebnis eine Warnung.
- Freitext („Warum") bleibt lokal (localStorage bzw. `MISSION.md`), fließt nicht in Regeln.

### 6.2 Fragen (`_placement.yaml`, endgültige Liste in Anhang E)

1. **Ziel** (1–2 wählen, 7 Optionen): `alltag` · `team` · `automation` · `agents` · `security` · `einschaetzen` ·
   `moderieren`. Keine Auswahl = `alltag`; doppelte Angaben zählen einmal; mehr als zwei lässt die Oberfläche nicht zu
   (Engine nimmt die ersten zwei).
2. **Warum** (Freitext, optional) und **Zeit** — gemeint ist die Länge einer Lernsitzung, nicht der Gesamtumfang;
   für wenig Gesamtzeit gibt es den Schnellstart:
   `schnellstart` („nur ein paar Stunden insgesamt": Mindestpfad, eine Etappe) · `stunde` (Etappen à 60 Min) ·
   `abende` (Etappen à 150 Min, **Voreinstellung**, auch wenn die Frage übersprungen wird) · `gruendlich`
   (Etappen à 180 Min, Kür-Kapitel im Schwerpunkt werden relevant).
3. **Stand je Bereich** (genau 14 Bereiche, Anhang E.1; Bereiche sind **keine** Regale, sie zeigen direkt auf
   Kapitel; **jedes Kapitel gehört höchstens einem Bereich**, Validator-Regel): `neu` (0) · `gehört davon` (1) ·
   `schon gemacht` (2) · `weiß nicht` (= 0). Unbeantwortet = 0.
4. **Mini-Szenarien** (optional, 6, je genau einem Bereich zugeordnet): falsch beantwortet → Bereich höchstens 1;
   nicht beantwortet → keine Wirkung. Mehrere falsche Szenarien im selben Bereich wirken wie eines.

### 6.3 Regeln (deterministisch, reine Funktion `place(catalog, answers)`)

Status je Kapitel: `work` (durcharbeiten) · `skim` (überfliegen: Auf einen Blick + Check) · `skip` (Schnellcheck
reicht) · `later` (nicht empfohlen; mit Begründung). Jedes `work`/`skim`-Kapitel bekommt eine **Etappe** (1, 2, …).
Notation: r(c) = Stand des Bereichs von Kapitel c nach Szenario-Deckel (Kapitel ohne Bereich: kein r).
„Nur-Einschätzen" heißt: `goals == [einschaetzen]`.

**Schritt A — Relevanzmenge R.**
- `schnellstart`: R = Mindestpfad (`_placement.yaml`, Validator erzwingt, dass er alle eigenen Voraussetzungen
  enthält). Sonst nichts.
- sonst, Ziel `moderieren` gewählt: R = alle Kapitel mit Session 0–4 (der Live-Workshop); X-Kapitel sind dann `later`
  mit Grund `not-goal` und werden im Pfad als eigenes Regal verlinkt.
- sonst: R = `core`-Kapitel der Grundregale (`start`, `permissions`, `context`, `prompting`, `git`, `cost`,
  `troubleshooting` — Fehlersuche braucht jede Person)
  ∪ `core`- und `deep-dive`-Kapitel der Schwerpunkt-Regale aller gewählten Ziele ∪ bei `gruendlich` deren `bonus`-Kapitel
  ∪ jede Praxis-Station, deren `offers` ein Kapitel aus R mit r < 2 enthält (die Station zeigt dann nur diese Übungen)
  ∪ `capstone`, wenn ein Ziel `agents` oder `einschaetzen` ist
  ∪ X-Kapitel, wenn ein Ziel nicht `einschaetzen` ist — außer das Kapitel steht in `chapter_goals`: dann nur, wenn
  eines der dort genannten Ziele gewählt ist (X.3 Pi, X.4 OpenClaw: `agents`, `security`, `einschaetzen`).
- Kapitel außerhalb R: `later`, Grund `after-quickstart` (bei `schnellstart`) bzw. `not-goal`.

**Schritt B — Status in R.**
- Lesson/Setup mit Bereich: r = 0 → `work`; r = 1 → `skim` (`deep-dive` → `work`; Setup → `work`, ohne Installation
  geht nichts); r = 2 → `skip`.
- Ohne Bereich: Praxis-Station → `work`; Capstone → `work` (bei Nur-Einschätzen `skim`); Community → `skim`.
- Nur-Einschätzen: `work` → `skim` für alle Kapitel ohne Sicherheitsboden, außer Setup (ohne Installation kein
  Einschätzen).

**Schritt C — Sicherheitsboden.** Kapitel mit `safety_floor: true` (Liste unten), die in R liegen **oder** deren
Bereich r = 2 hat (wer ein Feature schon nutzt, liest dessen Sicherheitskapitel auch ohne passendes Ziel): Status
mindestens `skim`, bei r < 2 `work`; ein so neu hinzugekommenes Kapitel bekommt Grund `safety-floor`.
Liste (bewusst knapp): S1.5, S1.6 (Rechte-Modi), S2.8 (nur `exit 2` blockt, fail-open), S2.13 (Plugin-Lieferkette),
S2.17 (MCP-Sicherheit), S3.8, S3.9 (Rechte für Autonomie, geschützte Pfade, Sandbox), S3.13 (autonome Loops mit
Budget + Worktree), S4.4 (`-p` ohne `--bare` führt fremde Hooks aus; CI-Zugangsdaten).

**Schritt D — Voraussetzungen.** Für jedes Kapitel mit `work`/`skim` wird jede transitive Voraussetzung
(`requires_all` im Katalog) mit Status `later` zu `skim` (Grund `prerequisite`) — außer ihr Bereich hat r = 2,
dann wird sie `skip` (Grund `known`; die Person kann es schon). Ein Durchlauf genügt, weil
`requires_all` bereits transitiv ist. `skip` bleibt `skip`.

**Schritt E — Übersteuerung.** Die Wahl der lernenden Person je Kapitel gilt zuletzt und schlägt alles, auch den
Sicherheitsboden. Danach Schritt D noch einmal. Warnungen: `override-safety`, wenn ein Sicherheitsboden-Kapitel
dadurch unter seinen berechneten Status fällt; `override-prereq`, wenn ein `work`/`skim`-Kapitel eine per
Übersteuerung (nicht per r = 2) übersprungene Voraussetzung hat — mit beiden Kapitel-IDs. War die Voraussetzung
schon vor der Übersteuerung `skip` (Bereich r = 2, die Person kann es), gibt es keine Warnung — es fehlt nichts.

**Schritt F — Etappen.** L = alle `work`/`skim`-Kapitel nach `order` (= Lehrreihenfolge; Voraussetzungen stehen
immer vorher). Minuten: `work` = `minutes`, `skim` = `ceil(minutes × 0,3)`. Budget B aus der Zeitantwort
(`schnellstart`: eine Etappe). Gierig und zusammenhängend: Die aktuelle Etappe schließt, wenn sie nicht leer ist und
das nächste Kapitel B überschreiten würde. Die Reihenfolge wird nie umgestellt. Warnung `quickstart-long`, wenn der
Schnellstart mehr als 180 Minuten ergibt (mit gerundeten Stunden).

**Ausgabe:** `{version: 1, chapters: [{id, status, reason, stage|null, override: bool}], stages: [{n, minutes}],
totals: {work_min, skim_min}, warnings: [{code, ids}]}`, stabil nach `order`. Begründungs- und Warncodes → deutsche
Textbausteine in `_placement.yaml`. Kein leerer Pfad: S0.1 und S1.1 sind in jedem R (Grundregal bzw. Mindestpfad).

**Vertrag:** `tools/fixtures/placement-vectors.json` ist die Spezifikation (≥ 14 Personas): Anfänger `alltag`
`abende` · Anfänger `schnellstart` · alles `schon gemacht` + `security` · Nur-Einschätzen `gruendlich` ·
`automation` mit `basics` = 2, `hooks` = 0 und falschem Hook-Szenario · Übersteuerung S2.8 → `skip` (Warnungen) ·
Übersteuerung einer Voraussetzung · zwei Ziele `team` + `agents` · `moderieren` · nur Ziel, sonst nichts · MCP r = 2 ohne
MCP-Ziel → S2.17 `skim` · alles „weiß nicht" · Zeitfrage ausgelassen (= `abende`) · `stunde` mit vielen Etappen.
Python- und JS-Engine müssen jeden Vektor exakt treffen.

### 6.4 Drei Oberflächen, eine Engine-Semantik

- **Cockpit:** Assistent beim ersten Besuch (und über „Einstufung" jederzeit), Ansicht „Mein Pfad", Kacheln der
  Bibliothek eingefärbt nach Status. JS-Engine im Template.
- **Tutor:** `/workshop start` fragt per Dialog, schreibt `einstufung.json`, ruft `python tools/placement.py`.
- **Markdown:** `resources/library/einstufung.md` (generiert) ist bewusst die **vereinfachte, menschlich ausführbare**
  Fassung: (1) Ziel wählen → fertiger Pfad je Ziel (von der Engine mit einem Standardprofil „alles neu" erzeugt,
  liegt als `resources/paths/ziel-*.md`), (2) je Bereich die Aussage lesen: „schon gemacht" → die Kapitel dieses
  Bereichs per Schnellcheck überspringen, außer Sicherheitsboden. Sie behauptet nicht, dieselben Etappen wie die
  Engine zu liefern.
- **Gleichheit:** gemeinsame Testvektoren `tools/fixtures/placement-vectors.json`; Python-Test gegen `placement.py`,
  JS-Test extrahiert die Engine aus dem gebauten Cockpit und führt sie mit `node` aus (übersprungen mit Grund, wenn
  `node` fehlt).

## 7. Generator und Validator (`tools/build_library.py`)

- **Parse:** Frontmatter (PyYAML), H2-Abschnitte, Quiz, `cockpit:example`, Mermaid-Blöcke.
- **Validieren (fail-closed, Exit 1):** Schema; IDs eindeutig; alle 65 LE + X-Kapitel vorhanden; `requires` existiert und
  zeigt rückwärts; Pflichtabschnitte, Beispiel- und Quizanzahl **je Kapiteltyp** (Tabelle §4.3); Quiz parsebar (1 richtig, 3 falsch);
  relative Links existieren; Regale/Bereiche aus `_placement.yaml` referenzieren nur existierende Kapitel;
  generierte Blöcke aktuell.
- **Generieren:** `library/README.md`, `library/einstufung.md`, `library/catalog.json`, `paths/*.md`, Meta-Blöcke in
  Kapiteln, Cockpit (`template.html` + Daten → `resources/claude-code-workshop-ui.html`).
- CLI: `python tools/build_library.py validate [--complete] [--chapter <datei>]` · `build` · `check` (generiert in
  den Speicher und vergleicht zeilenend-normalisiert; Abweichung = Exit 1; das ist der Aufruf in Tests und Abnahme).
- **Links:** Im Markdown sind relative Links erlaubt und werden auf Existenz geprüft. Beim Cockpit-HTML schreibt der
  Generator um: Link auf ein Kapitel → Cockpit-Route (`?run=S2.8`), jeder andere Repo-Pfad → absolute GitHub-URL
  (`https://github.com/dynamic-dome/dynamic-workshop/blob/main/<pfad>`), externe URLs bleiben. Der Validator prüft
  das gebaute Artefakt: kein relativer `href` außer `?`-Routen und `#`-Ankern.

### 7.1 Quellenhoheit je Feld (ersetzt alle bisherigen „Single Source of Truth"-Aussagen)

| Information | Einzige Quelle | Erzeugt daraus |
|---|---|---|
| Lehrinhalt, Demo, Übung, Quiz, Outcome, Schnellcheck je LE | `resources/library/<kapitel>.md` | Cockpit, Tutor liest direkt, Deck-Stichworte |
| Reihenfolge, Session, Minuten, Stufe, Voraussetzungen | Frontmatter der Kapitel | `paths/live-workshop.md`, Katalog, Deck |
| Regale (Titel, Einleitung) | `resources/library/_shelves.yaml` | `library/README.md`, Cockpit, Deck |
| Einstufung (Fragen, Regeln, Texte) | `resources/library/_placement.yaml` | Katalog, `einstufung.md`, `paths/ziel-*.md` |
| Modelle, Preise, Prüfdatum | `resources/_canonical.md` (unverändert) | — |
| Moderationsablauf, Zeiten-Begründung, Live-Format | `resources/moderation/handbuch.md` | — |
| Befehls-/Konfig-Kurzfakten | `resources/reference/karte-*.md` (mit Doku-Link + Prüfstempel) | — |

Normative Verweise, die mitziehen: `CLAUDE.md`, `AGENTS.md` (Struktur, Regeln, Deck), `HOW-TO-USE.md`,
`tools/build_deck.py` (Footer „session-plan.md = SSoT"), `skills/workshop/SKILL.md`, `commands/workshop.md`,
`agents/workshop-mentor.md`, `.claude-plugin/plugin.json` (Beschreibung „17 modules"), `tools/install_workshop_plugin.ps1`,
`tools/workshop_doctor.ps1`, `workshop-playground/CLAUDE.md` (Vuln-Zahl).
- Abhängigkeiten (nur Pflege): PyYAML (robustes Frontmatter statt Eigenbau-Parser), `markdown` (Kapitel-HTML fürs
  Cockpit), python-pptx (Deck, schon bisher). Lernende brauchen nichts davon.

## 8. Cockpit

**Entscheidung nach Analyse (Anhang C): Neubau statt Umbau.** Die Logik des alten Cockpits ist nur ~370 Zeilen, der
Rest (~190 KB) sind Daten. Es hat genau eine Ansicht mit drei Spalten und ~12 Blöcken, eine für alle 65 LE identische
Stichwort-„Übung", „erledigt" durch eine zufällig richtige MCQ, in 63/65 Quizfragen ist die längste Antwort die
richtige, Quizfragen würfeln bei jedem Render neu, kein „weiter, wo ich war", mobile Überlappung, Fachjargon
(„48 Route", „Operator-Bild"). Die Tests fixieren Code-Wortlaut statt Verhalten.

- **Quelle:** `tools/cockpit/template.html` (CSS + JS, hand gepflegt) + generierte Daten in genau einem Marker-Block
  im einzigen Inline-Script → `resources/claude-code-workshop-ui.html` (Pfad bleibt: Website-Test und Provenienz
  hängen daran). CSP bleibt: genau ein Inline-Script, keine Inline-Handler, keine externen Referenzen, keine
  Inline-`style`-Attribute (CSS-Variablen per JS `style.setProperty`), kein `confirm()`.
- **Ansichten (eine Aufgabe je Bildschirm):** *Start* (drei Wege: Einstufung · Live-Workshop-Pfad · Bibliothek
  stöbern; „weiter, wo du warst") → *Einstufung* (Assistent: Ziel → Warum & Zeit → Stand je Bereich → Mini-Szenarien
  optional → Ergebnis) → *Mein Pfad* (Kapitel nach Status gruppiert, Begründung, Minuten, je Kapitel übersteuern) →
  *Bibliothek* (Regale als Raster, Kacheln mit Status-Farbe **und** Icon/Text) → *Kapitel* (Auf einen Blick, Bild im
  Kopf, Diagramm, Beispiel mit Kopieren, Check, Quiz zur **aktuellen** LE — jeweils nur, wenn der Kapiteltyp das Feld hat (§4.3) —, „ganzes Kapitel lesen", zurück/weiter
  im eigenen Pfad) → *Wiederholen* (Abruf über erledigte Kapitel mit Abstand).
- **„Erledigt"** setzt nur die lernende Person selbst (Button); das Quiz gibt Rückmeldung, bucht aber nichts.
  Quiz-Optionen einmal je Kapitelaufruf gemischt (Fisher-Yates), nicht bei jedem Render.
- **Zustand:** Fortschritt bleibt unter `ccWorkshopUiState` (`done` bleibt gültig, Bestandsdaten gehen nicht
  verloren), Einstufung in eigenem Key `ccWorkshopProfileV1` mit Versionsfeld; beide fail-soft (blockierter oder
  kaputter Storage → Sitzung ohne Speichern statt leerer Seite); getrennte Reset-Aktionen mit eigenem
  Bestätigungsdialog. Deep-Links `?run=`/`?section=` bleiben, `?view=` wird ignoriert, neu `?screen=`.
- **Escaping:** alle Inhalte als Text oder über eine Escape-Funktion; vorgerendertes Kapitel-HTML vom Generator
  bereinigt (keine `<script>`, keine `on*`-Attribute; der Generator prüft, dass im Artefakt genau ein `<script>` steht).
- **Barrierefreiheit:** Status nie nur per Farbe, `aria-pressed`/`aria-current`/`aria-live`, Labels an allen
  Eingaben, Tastatur ohne Modifier-Kollision, Schrift ≥ 13 px, Kontrast ≥ 4,5:1 für Text.
- **Größenregel:** Wird die Datei mit Volltext > 1,5 MB, zeigt „ganzes Kapitel lesen" auf die GitHub-Fassung.
- **Abwerfbar (Plan Task 13 und Volltext):** Fehlen vorgerenderte SVG-Diagramme oder der Volltext, zeigt die
  Kapitelansicht Mermaid-Quelltext bzw. den GitHub-Link; keine andere Funktion hängt davon ab.
- **Look:** SOC-Anker (dunkel, Amber) bleibt, aber ruhiger; Status-Farben aus der geprüften Status-Palette.
- **Tests:** Die Wortlaut-Tests (`tools/test_workshop_ui_behavior.py`) werden durch **Verhaltenstests** ersetzt
  (Playwright gegen `127.0.0.1`: Einstufung für 3 Personas → erwarteter Pfad, Kapitel-Navigation, Quiz bucht nichts,
  Storage blockiert → Seite rendert, 0 Konsolenfehler) plus die bleibenden Invarianten: genau ein Inline-Script,
  `node --check`, keine Flash-/Flicker-Tokens, Fisher-Yates-Mischung, Artefakt = Build (`check`).
  `tools/test_course_ci_auth.py`/`test_course_hooks.py` prüfen die Kapitel (Quelle) direkt; ihre Cockpit-Regex wird
  an das neue Datenformat angepasst, damit das Artefakt weiter mitgeprüft wird.

### 8.1 Test-Migration (vor dem Formatwechsel festgelegt, damit kein Nachweis still verschwindet)

| Bisheriger Nachweis | Neuer gleichwertiger Nachweis |
|---|---|
| `test_course_ci_auth`: ≥ 50 Cockpit-Beispiele per Regex `example: "…"`, keine `--bare`-Abo-Token-Kombination | Scan über **alle** Codeblöcke aller Live-Markdown-Dateien und **alle** Beispiele im Cockpit-Datenblock (neuer JSON-Parser); Vollständigkeit ohne Mindestzahl: Anzahl Cockpit-Beispiele = Anzahl Kapitel mit `cockpit:example` laut Katalog, und der Snippet-Ledger belegt, dass jeder der ~300 alten Quellblöcke ein Ziel hat; Negativprobe: absichtlich falsche `--bare`+`CLAUDE_CODE_OAUTH_TOKEN`-Zeile im Fixture wird gefunden |
| `test_course_hooks`: WRONG_IDIOMS auf Rohtext aller Live-Dateien inkl. Cockpit | unverändert (Rohtext); Live-Dateien = Kapitel + Referenz + Moderation + Cockpit; Gegenprobe gegen die Fassung `ba222d2` bleibt |
| `test_course_hooks`: `tested asset:`-Marker ↔ identisches Snippet | unverändert, läuft über `resources/**/*.md` |
| `test_workshop_ui_behavior`: Fisher-Yates, Quiz bucht die gefragte LE, Übung ist nur Feedback, genau ein Script + `node --check`, keine Flash-Tokens, fail-soft `loadState`, Deep-Link | Invarianten-Tests auf dem Template (Fisher-Yates-Funktion, genau ein Script, `node --check`, keine Flash-Tokens, kein `confirm(`, keine Inline-Handler/-Styles) **plus** Playwright-Verhaltenstests (Quiz bucht nichts, Storage blockiert/kaputt → Seite rendert, `?run=S2.3` öffnet S2.3, Personas → Pfad) |
| `test_workshop_ui_behavior`: 48er-Route, Cheatsheet-Link, Session-Minuten-Literal | entfällt bewusst (Funktionen gibt es nicht mehr); ersetzt durch Test „Etappen-Minuten im UI = Engine-Ergebnis" |
| `lint_currency` / `currency_check` über alle Live-Dateien | unverändert; neue Ordner liegen unter `resources/` und sind automatisch im Scope; Test, dass `library/`, `reference/`, `moderation/` gescannt werden |
| `test_workshop_tooling` (Deck, Assets) | angepasst an neue Deck-Quelle (Katalog) und Asset-Pfade |

## 9. Tutor: `/workshop` im Stil von `/teach`

Übernommen aus Matt Pococks `teach` (MIT, github.com/mattpocock/skills): Mission als Kompass, Lernprotokolle für die
Zone der nächsten Entwicklung, kurze Lektionen mit einem greifbaren Erfolg, Primärquelle je Lektion, Abrufübung und
Abstand (Speicherstärke statt Scheingewandtheit), gleich lange Quizantworten, Glossar-Treue, Community für Erfahrung.

| Aufruf | Verhalten |
|---|---|
| `/workshop` | Übersicht: Regale, drei Einstiege |
| `/workshop start` | Lernordner anlegen (Vorschlag `~/cc-workshop/lernen`), `MISSION.md` im teach-Format, Einstufung im Dialog, optional (nur mit Zustimmung, nur lesend) Blick auf das echte Setup, `einstufung.json` → `placement.py` → `lernpfad.md`, erste Lernprotokolle für genanntes Vorwissen |
| `/workshop next` | nächstes Kapitel aus Pfad + Lernprotokollen, Ablauf je Kapiteltyp (§4.3; fehlende Abschnitte werden übersprungen): Schnellcheck → Auf einen Blick → Bild im Kopf → selbst machen (im eigenen Terminal, Tutor prüft Ergebnis) → Check → Lernprotokoll, wenn Evidenz |
| `/workshop learn <ID\|Alias>` | bestimmtes Kapitel im selben Ablauf |
| `/workshop review` | Abruf über erledigte Kapitel mit Abstand, gemischt; Fehler → Wiederholung vormerken |
| `/workshop guide <ID\|Session>` | Moderationsmodus: Ablauf, Zeiten, „Für Moderierende"-Hinweise |

Der Mentor-Agent (`agents/workshop-mentor.md`) beantwortet Fragen und gründet Antworten auf Kapitel und offizielle
Doku; er hält **keine** Inhaltskopie mehr (die alte Regel „bei jeder Inhaltsänderung Mentor aktualisieren" wird durch
„Mentor verweist auf Kapitel" ersetzt).

**Im selben Schritt migriert** (sonst laufen `/workshop guide|learn` ins Leere und fallen still auf Modellwissen
zurück): `commands/workshop.md` (Modi `start|next|learn|review|guide`, IDs `S0.1…S4.10`, `X.1/X.2`, Aliase), `SKILL.md`
(liest `${CLAUDE_PLUGIN_ROOT}/resources/library/catalog.json` und das Kapitel, ruft
`${CLAUDE_PLUGIN_ROOT}/tools/placement.py`; belegt in code.claude.com/docs/en/skills.md, Abruf 2026-09-30, CLI
2.1.285: „`${CLAUDE_PLUGIN_ROOT}` — The plugin's installation directory. Substituted only in plugin skills";
benannte Argumente über `arguments: [mode, target]` → `$mode`, `$target`), Mentor, `plugin.json`. Wird der Skill
ohne Plugin (kopiert nach `~/.claude/skills/`) genutzt, fragt er nach dem Repo-Pfad. **Fehlt ein Kapitel oder der Katalog, meldet der Tutor das als
Fehler** und rät nicht aus dem Modellwissen. Alias-Auflösung: `2.2` → erstes Kapitel des Regals, Liste der übrigen.

## 10. Community-Regal (neu)

- **X.1 Community-Skills: wer baut was, das wirklich hilft** — nur belegte Einträge (Quelle, Lizenz, Installationsweg):
  Matt Pocock (`mattpocock/skills`), Jesse Vincent (`obra/superpowers`), Anthropic (`anthropics/skills`), gstack
  (Garry Tan) — endgültige Liste aus der Faktenprüfung (Anhang D). Mit Prüfliste „fremden Skill vor der Installation
  bewerten" (Supply-Chain, verlinkt S2.13).
- **X.2 Mit Claude Code lernen** — `/teach` und der Workshop-Tutor: Mission, Lernprotokolle, Abruf, und warum ein
  Agent als Lehrer Grenzen hat (Quellen prüfen, nicht dem Modellwissen trauen).

## 11. Visualisierung

- **Mermaid in Kapiteln** (GitHub rendert nativ, hell/dunkel): Agenten-Schleife, Rechte-Leiter, Kontextfenster,
  Hook-Lebenslauf (Event → Matcher → Exit-Code → blockt/läuft/fail-open), Plugin-Anatomie, MCP-Architektur,
  Orchestrierungsmuster, CI-Stufe, Fehlersuch-Entscheidungsbaum, Regal-Karte. Ideen je Kapitel aus der Quellenkarte;
  nur wo ein Diagramm mehr sagt als ein Absatz.
- **Cockpit:** dieselben Diagramme als vorab gerenderte SVG. Das Rendern ist ein **eigener, optionaler Schritt**
  (`python tools/render_diagrams.py`, Playwright + Mermaid, Ergebnis `resources/library/diagrams/<sha8>.svg` im Repo);
  Renderfehler dort = Exit 1. `build`/`check` rendern nichts: Liegt zu einem Mermaid-Block ein SVG mit passendem
  Hash vor, bettet das Cockpit es ein, sonst zeigt es den Mermaid-Quelltext und den GitHub-Link.
- **Deck** (`tools/build_deck.py` neu, Daten aus dem Katalog): Titel · Was ist die Bibliothek · Wie du einsteigst
  (Einstufung) · Regal-Karte · vier Session-Opener · Kern-Denkmodelle · Weiter. Sichtprüfung per PowerPoint-Export
  nach PNG.

## 12. Migrationsmethode (Umzug statt Neuschreiben)

1. **Quellenkarte** (fertig in der Bestandsaufnahme): je LE Zeilenbereiche in Modul, Demo, Übung; Waisen mit Ziel.
2. **Pilot:** ein Regal (Hooks: sicherheitskritisch, mit getesteten Assets) wird zuerst migriert und von mir geprüft;
   danach wird der Auftrag an die Schreib-Agenten geschärft.
3. **Schreib-Agenten** je Regal (parallel, getrennte Dateien): übersetzen und ordnen, erfinden nichts; offene Fragen
   als `<!-- TODO(migration): … -->` statt Raten (Validator lässt keine TODO übrig).
4. **Snippet-Ledger** (`tools/test_migration_ledger.py`): jeder Codeblock aus den Altdateien (gelesen aus dem
   Basis-Commit `ba222d2` per `git show`) steht unverändert in Bibliothek/Referenz/Moderation oder begründet in
   `tools/fixtures/migration-dropped.txt` (nur schrumpfend).
5. **Aussagen-Matrix + Fakten-Prüfer** je Kapitel (unabhängig vom Schreiber): Der Prüfer liest die Heimat-Bereiche
   des Kapitels (Zeilen aus Anhang A, jede Zeile gehört genau einem Kapitel oder ist eine entschiedene Waise) und
   listet **jede fachliche Aussage** — Prosa, Tabellenzeilen, Demo- und Recovery-Schritte, Voraussetzungen, Zahlen —
   mit Status `übernommen` · `verändert` (mit altem und neuem Wortlaut) · `ausgelassen` (Begründung Pflicht: Dublette
   von Kapitel X, veraltet laut Beleg, in Referenzkarte). Zusätzlich: **neue Aussagen**, die in keiner Quelle stehen
   (Erfindungsverdacht). Die Matrix liegt als `docs/migration/<id>.json` im Repo; offene `verändert`/`ausgelassen`
   ohne tragfähige Begründung und jede unbelegte neue Aussage gehen zurück an den Schreiber (höchstens zwei Runden,
   danach entscheide ich selbst an der Quelle).
6. Bestehende Wächter laufen automatisch auf den neuen Dateien (`test_course_hooks`, `test_course_ci_auth`, Lint,
   `currency_check`) — die P1-Fehler vom September können nicht unbemerkt zurückkommen.

## 13. Verifikation (Definition of Done)

- `python tools/build_library.py check` Exit 0; `pytest tools` grün (alte Tests angepasst, neue für Generator,
  Einstufung Py+JS, Ledger); `python tools/lint_currency.py` OK; `currency_check --state-dir .currency/manual` ohne neue
  Rot-Befunde gegenüber dem Stand vor dem Umbau (Haiku-Retirement bleibt erwartet rot).
- Browser-QA (Playwright, `127.0.0.1`): 0 Konsolenfehler; Einstufung für 3 Personas ergibt die erwarteten Pfade;
  Bibliothek, Mein Pfad, Kapitel, Quiz, Tastatur, 390 px Breite; Screenshots im Bericht.
- Deck als PNG gerendert und angesehen; Mermaid-SVG ohne Renderfehler.
- Codex-Verifier gegen diese Spec; Befunde an der Quelle geprüft und behoben.
- Alles lokal auf `praxisbibliothek` committet; Push/Merge/Website-Export = Owner.

## 14. Nicht-Ziele und Risiken

- Nicht-Ziele: neue Kursthemen außer X.1/X.2; englische Fassung; Website-Umbau; Monatslauf-Registrierung (#9517).
- Risiko Übersetzung verfälscht Fakten → Ledger + Fakten-Prüfer + Wächter-Tests.
- Risiko Cockpit-Größe → Größenregel (§8).
- Risiko Parallel-Session auf `main` → Worktree; vor Merge `git log main` gegenprüfen.
- Risiko externe Links auf alte Pfade: Website verlinkt nur das Repo und das Cockpit (geprüft 2026-09-30);
  innerhalb des Repos prüft der Validator Links.

## 15. Prüfprotokoll der Spec

**Runde 1 (Codex, read-only, 2026-09-30): REJECT, 10 Befunde.** Jeder Befund an Spec und Repo nachgeprüft:

| # | Befund (Kurz) | Urteil | Änderung |
|---|---|---|---|
| 1 | Zeitbudget kann Kern-`work` nicht kürzen → absurder Kurzpfad | berechtigt | §6.3 F: Etappen statt Streichen, ehrliche Zeitangabe |
| 2 | Voraussetzungen nach Kürzung ungeprüft, keine Fixpunkt-Regel | berechtigt | §6.3 D/E/F: Fixpunkt, Etappe mit Vorläufern |
| 3 | Command/Skill/Mentor laden gelöschte Dateien, fallen still auf Modellwissen zurück | berechtigt (`SKILL.md` Z. 103–109, 159–165) | §9: Migration im selben Schritt, fehlendes Kapitel = Fehler |
| 4 | Cockpit-Wächter (`test_course_ci_auth` ≥ 50 Beispiele, UI-Tests) würden still wegfallen | berechtigt | §8.1 Test-Migrationstabelle |
| 5 | Relative Links im exportierten Cockpit tot | berechtigt (z. B. `block-1-foundations.md` Z. 229, 247) | §7 Link-Umschreibung + Artefakt-Prüfung |
| 6 | Quellenhoheit widerspricht `CLAUDE.md`/`AGENTS.md`/`build_deck.py` | berechtigt | §7.1 Quellenhoheit je Feld + Liste normativer Verweise |
| 7 | Ledger sichert nur Codeblöcke, Prosa-Fakten ungeprüft | berechtigt | §12.5 Aussagen-Matrix je Kapitel |
| 8 | Einstufungsdaten uneindeutig (10–12 vs. 14 Bereiche, Vorrang fehlt) | berechtigt | §6.2/6.3 endgültig, Anhang E |
| 9 | Einheitsvorlage erzwingt Beispiele/Übungen überall | berechtigt | §4.3 Kapiteltypen |
| 10 | Zu viel für V1 (2 Engines, Markdown-Einstufung, Übersteuerung, Lernprotokolle, Volltext, SVG) | teilweise | Beibehalten, weil ausdrücklich gewünscht (drei Oberflächen, `/teach`, bessere Visualisierung); Markdown-Einstufung ehrlich vereinfacht (§6.4); Volltext und SVG im Plan als spätere, abwerfbare Aufgaben |

**Runde 2 (Codex, read-only, 2026-09-30): REJECT.** Status Runde 1: 3 gelöst, 7 teilweise; 9 neue Befunde, dazu
eine Persona-Simulation, die zeigte, dass die Etappen-Priorisierung die Lehrreihenfolge umkehren konnte.

| # | Befund (Kurz) | Urteil | Änderung (v3) |
|---|---|---|---|
| R2-1 | Kapiteltypen vs. Validator/Cockpit/Tutor („genau ein Beispiel") | berechtigt | §7, §8, §9: überall „je Kapiteltyp (§4.3)" |
| R2-2 | „immer work" für Security-Kapitel nicht umgesetzt | berechtigt | Zusage gestrichen (E.2); Status folgt §6.3 B/C |
| R2-3 | Priorisierte Etappen kehren Lehrreihenfolge um; Warnung unerreichbar | berechtigt | §6.3 F: zusammenhängende Etappen in `order`; Zeit = Sitzungslänge; eigene Option `schnellstart` |
| R2-4 | Community/Capstone/Einschätzen mit konkurrierenden Regeln | berechtigt | §6.3 A/B eindeutig, „Nur-Einschätzen" definiert |
| R2-5 | Kapitel in zwei Bereichen (S4.4, S4.7) | berechtigt | E.1 bereinigt, Validator-Regel „höchstens ein Bereich" |
| R2-6 | S0.1 nicht im Schema | berechtigt | §4.1 IDs/Order/Pflicht-IDs, Anhang A Quelle |
| R2-7 | Mindestzahlen im Abdeckungstest erlauben Verlust | berechtigt | §8.1: Gleichheit mit Katalog + Ledger statt Mindestzahl |
| R2-8 | Zwei Master für Analogien | berechtigt | Kapitel sind Quelle, `analogien.md` generiert |
| R2-9 | Zeitantwort fehlt → nicht bestimmt | berechtigt | Voreinstellung `abende` |
| R1-2 (Rest) | Übersteuerte Voraussetzung bleibt übersprungen | berechtigt | §6.3 E: Warnung `override-prereq` |
| R1-10 (Rest) | Volltext/SVG als abwerfbar genannt, aber vorausgesetzt | berechtigt | §8: Fallback ausdrücklich |

**Runde 3 (Codex, 2026-09-30): REJECT — Spec überwiegend gelöst, Plan noch auf v2.** Übernommen: Plan Tasks 1–5 neu
auf v3 (Zeiten, Defaults, Mindestpfad, 14 Personas, Warnungs-Schema `{code, ids}`), `offers` im Modell und Katalog,
Kontrakt-Katalog aus `docs/migration/chapter-meta.yaml` (verbindliche Metadaten aller 68 Kapitel, jetzt festgelegt,
damit Task 4 vor Task 5 grün werden kann), `schnellstart.md` und `analogien.md` als Generator-Ausgaben, eine CLI
(`validate | build | check`), Cockpit-Testumstellung erst mit Task 10–12, `moderieren` nur Session 0–4, Diagramm-Rendern
als eigener optionaler Schritt.

**Runde 4 (Codex, 2026-09-30): APPROVE-WITH-CHANGES.** Metadaten, Sicherheitsboden, Mindestpfad, Bereiche und die
vorgerechneten Personas geprüft. P11 ist durch die Verfeinerung von Regel D (bekannte Voraussetzungen → `skip`)
anders gelöst als vorgeschlagen; der Produktions-Build ist als Gate A2 nach dem Umzug festgelegt.

## Anhang A — Quellenkarte und Heimat-Zuordnung

Liegt maschinenlesbar in `docs/migration/source-map.json` (je LE: Zeilenbereiche in Modul/Demo/Übung, Regal-Vorschlag,
Voraussetzungs-Vorschlag, Outcome, Schnellcheck, Diagramm-Idee, Primärquelle, didaktische Befunde mit Zeilenbeleg)
und `docs/migration/ownership.json` (Heimat-Kapitel je Zeile nach der Regel in §5). Abdeckung mechanisch geprüft:
alle Zeilen der neun Quelldateien sind einem Kapitel oder einer entschiedenen Waise zugeordnet, bis auf Anker-/
Banner-Zeilen (werden zu `outcome`). 466 Waisen-Zeilen: Modulköpfe/Lernziele → Regal-Einleitungen; LE-Landkarten,
Blockenden → entfallen (Dubletten des Session-Plans); Kosten-Vertiefung → S4.4; Blueprints → S4.8; „Saboteur on
Shift" → S4.10; Übungspools → Praxis-Stationen; Feature-Reife-Tabelle → `reference/karte-alte-namen.md` + Badges.
Regal- und Voraussetzungs-Vorschläge der Agenten sind Eingabe, nicht Beschluss; Sicherheitsboden legt §6.3 C fest.
S0.1 hat keine Quellenkarten-Zeile: Quelle ist `resources/prerequisites.md` Z. 1–266 und 466–490 (Lernenden-Setup), der Rest
(Moderations-Plugins, Z. 271–460) geht nach `moderation/vorbereitung.md`; der Snippet-Ledger deckt `prerequisites.md` mit ab.

## Anhang B — Zielorte je Bestandsdatei

| Datei | Ziel |
|---|---|
| `README.md` | Schaufenster ≤ 80 Zeilen: was, für wen, drei Einstiege, Regal-Karte, Stand-Anker, Einordnung DoMe Dynamics |
| `HOW-TO-USE.md` | Anleitung: Selbst lernen (Einstufung → Pfad → Kapitel, Lernroutine) · Moderieren (→ `moderation/`) · Pflegen (Generator, Lint, Currency, Tests) |
| `CLAUDE.md` / `AGENTS.md` | ≤ 40 Zeilen, neue Struktur und Regeln; `AGENTS.md` mit denselben Kernregeln (Codex liest nur diese) |
| `WORKSHOP_EINFUEHRUNG.md`, `resources/workshop-guide.md` | entfallen; Lernroutine und Minimalpfad → HOW-TO-USE bzw. Einstufung |
| `resources/session-plan.md` | Tabellen → `paths/live-workshop.md` (generiert); Begründungen, Pausen, Live-Anker, Materialien → `moderation/handbuch.md`; Kostenschätzung → `reference/kosten-nachbau.md` |
| `resources/prerequisites.md` | Lernenden-Setup → S0.1; Moderations-Plugins/Assets → `moderation/vorbereitung.md` |
| `trainer-notes.md`, `live-3-person-mode.md`, `retrieval-recap-bridges.md`, `transfer-retention-plan.md` | `moderation/handbuch.md` (Talking Points je LE → „Für Moderierende" im Kapitel); Recall-Fragen → Check der Kapitel; Adoptionsplan → `reference/adoptionsplan-vorlage.md` |
| `capstone-exit-assessment.md` | S4.8 (Aufgabe + Rubrik); Selbstwirksamkeits-Check → Handbuch |
| `video-scripts.md` + Medien | `moderation/videos.md` + `media/` (Transkript bleibt wörtlich, Vermerk „3 Sessions, historisch") |
| `cheatsheet.md`, `quick-reference.md` | Referenzkarten; Nachbau der Doku wird zu Link + wenigen Alltagsfakten; Hook-Vertrag, Auth-Falle → Kapitel |
| `glossary.md` | `reference/glossar.md` (Widersprüche vorher korrigiert, LE-IDs statt Modulnummern) |
| `security-analogies.md` | Analogie je Kapitel in „Bild im Kopf" (einzige Quelle); `reference/analogien.md` wird daraus generiert (Tabelle Kapitel → Analogie); die Konsistenzregeln der alten Datei gehen in den Schreib-Brief |
| `faq.md`, `troubleshooting.md` | Antworten als „Typische Fallen"/Faustregeln in die Kapitel; Rest als `reference/faq.md` und `reference/karte-fehlersuche.md` |
| `deck-audit-…`, `dry-run-…`, `final-gap-sweep-…`, `review-2026-*`, `HANDOFF.md` | `docs/reviews/` unverändert (Verweise darauf angepasst) |
| `claude-code-workshop*.pptx` | ersetzt durch neues Deck `resources/media/claude-code-praxisbibliothek.pptx` |

Bekannte Widersprüche, die beim Umzug korrigiert werden (Belege in der Bestandsaufnahme): Playground hat 5 Schwachstellen
(README nennt einmal 3); „Hook-Script blockiert > 5 s" ist falsch (Timeout 600 s, fail-open); `--bare` ist kein
Memory-Schalter; Plugin-Scope-Pfade im Glossar; `/effort`-Stufen ohne `medium`; Shift+Tab-Zyklus; veraltete
„geplant"-Vermerke; Demo 1.1 an S1.2 statt S1.1 gebunden; 17-Modul-Beschreibung in `plugin.json`.

## Anhang C — Cockpit-Analyse (Kurzfassung)

Siehe §8. Zusätzliche Befunde: `loadState` stirbt bei blockiertem Storage (unbewachtes `removeItem`, `null`-JSON);
Anführungszeichen in Quizantworten brechen `data-correct`-Attribute (S1.18, S2.16); Tastaturkürzel fangen Alt+Pfeil
ab; 15 Stellen mit 10–11 px Schrift; Status nur per Farbe; `target=_blank` ohne `rel`; relative Links im Export tot.
Alle adressiert der Neubau.

## Anhang D — Community-Fakten (belegt 2026-09-30)

| Wer | Projekt | Lizenz (Beleg) | Installation (Beleg) | Passt zu |
|---|---|---|---|---|
| Matt Pocock | `mattpocock/skills` | MIT (LICENSE lokal + raw) | `claude plugin marketplace add mattpocock/skills`, dann `claude plugin install mattpocock-skills@mattpocock` (README Z. 49–57) | X.1, X.2 (`teach`, `grilling`, `tdd`, `handoff`, `writing-great-skills`) |
| Jesse Vincent | `obra/superpowers` | MIT (LICENSE im Plugin-Cache + raw) | `/plugin install superpowers@claude-plugins-official` (README Z. 52–81) | X.1; Verifikation/Planung (S3.4, S3.6) |
| Anthropic | `anthropics/skills` | gemischt: `skill-creator` Apache-2.0, Dokument-Skills source-available (LICENSE.txt je Skill) | `/plugin marketplace add anthropics/skills` | X.1; Skill-Bau (S2.2) |
| Anthropic | `anthropics/claude-plugins-official` | Apache-2.0 für das Verzeichnis, Plugins einzeln | registrierter Marketplace | X.1; Lieferkette (S2.13) |
| Garry Tan | `garrytan/gstack` | MIT (raw LICENSE) | Klon + `./setup` laut README — Vollinstallation bringt viel Infrastruktur, deshalb Extrakte lesen | X.1 („erst denken, dann bauen") |

Nicht belegt und deshalb nicht gelehrt: Sternzahlen, `npx skills@latest`-Installer, Inhalte einzelner Plugins im
offiziellen Verzeichnis. Prüfliste „fremden Skill bewerten" (12 Punkte) aus der Faktenprüfung geht in X.1.

## Anhang E — Einstufungs-Inhalte (Entwurf)

### E.1 Bereiche (Stand-Fragen, Verhaltensaussage → Kapitel)

| Bereich | Aussage („Trifft zu?" neu · gehört davon · schon gemacht · weiß nicht) | Kapitel |
|---|---|---|
| `basics` | Ich habe Claude Code schon für eine echte Aufgabe genutzt und das Ergebnis selbst geprüft. | S0.1, S1.1–S1.4 |
| `permissions` | Ich weiß, welchen Rechte-Modus ich für ein fremdes Repo wähle, und habe allow/deny-Regeln gesetzt. | S1.5, S1.6, S3.8–S3.10 |
| `context` | Ich pflege eine CLAUDE.md und weiß, wann ich `/compact` nehme und wann eine neue Session. | S1.8–S1.12 |
| `prompting` | Ich schreibe Aufträge mit Ziel, Grenzen und Prüfschritt und nutze den Plan-Modus. | S1.13–S1.15 |
| `git` | Ich lasse Claude auf einem Branch arbeiten, prüfe den Diff selbst und nutze Worktrees. | S1.16–S1.18, S4.7 |
| `cost` | Ich lese `/cost` bzw. `/usage` und deckele autonome Läufe mit Budget und Rundenlimit. | S1.7, S1.19, S4.1 |
| `skills` | Ich habe einen eigenen Skill oder Slash-Command geschrieben und benutzt. | S2.1–S2.5 |
| `hooks` | Ich habe einen Hook gebaut, der eine Aktion wirklich blockt. | S2.6–S2.10 |
| `plugins` | Ich habe Plugins geprüft, installiert oder selbst gebündelt. | S2.11–S2.13 |
| `mcp` | Ich habe einen MCP-Server angebunden und weiß, mit welchen Rechten er läuft. | S2.14–S2.19 |
| `agents` | Ich habe Subagenten definiert oder mehrere Agenten parallel arbeiten lassen. | S3.1–S3.5, S4.2 |
| `review` | Ich lasse Agenten-Ergebnisse gezielt gegenprüfen, bevor ich sie übernehme. | S3.6, S3.7, S3.11 |
| `automation` | Ich habe Claude Code zeitgesteuert oder headless (`claude -p`) laufen lassen. | S3.12–S3.14, S4.3–S4.6 |
| `troubleshooting` | Ich finde selbst heraus, warum ein Hook, Skill oder MCP-Server nicht greift. | S4.9, S4.10 |

Setup (S0.1) hängt an `basics`. Praxis-Stationen (S1.20, S2.20, S3.15), Capstone (S4.8) und Community (X.1, X.2)
hängen an keinem Bereich (Regeln §6.3 A/B).

**Mindestpfad** (nur für `schnellstart`, §6.3 A; muss seine eigenen Voraussetzungen enthalten): S0.1, S1.1, S1.2, S1.5,
S1.6, S1.10, S1.13, S1.14, S1.16, S1.19 — zusammen ≈ 150 Min bei Stand „neu".

### E.2 Ziele → Schwerpunkt-Regale

| Ziel | Schwerpunkt (deep-dive/bonus werden work) | Besonderheit |
|---|---|---|
| `alltag` Alltag beschleunigen | context, prompting, git, skills | — |
| `team` sicher im Team einführen | permissions, context, hooks, plugins, security | CLAUDE.md-Ebenen, Managed Policy |
| `automation` automatisieren & CI | automation, headless-ci, cost, hooks | — |
| `agents` Agenten-Systeme bauen | agents, automation, remote-isolation, capstone, mcp-knowledge | Capstone im Pfad |
| `security` Sicherheit & Compliance | permissions, hooks, security, plugins, mcp-knowledge | Vertiefungen S2.13, S2.17, S3.10, S3.11 sind dadurch relevant (Status nach §6.3 B/C) |
| `einschaetzen` einschätzen/entscheiden | — | Nur-Einschätzen: Kern `skim`, Sicherheitsboden nach §6.3 C; Capstone relevant (`skim`); keine X-Kapitel |
| `moderieren` moderieren | alle Kern-Kapitel + Praxis-Stationen | Pfad = Live-Workshop, Verweis Moderations-Handbuch |

### E.3 Mini-Szenarien (freiwillig, unbenotet)

Belegbasis: Delta-Review `docs/reviews/2026-09-28/05-bewertung.md` (H-01/H-03, H-11, H-17) und die jeweiligen Kapitel.

1. **hooks** — Dein Schutz-Hook bricht mit einem Syntaxfehler ab (Exit-Code 1). Was passiert mit dem Tool-Aufruf?
   ✔ Er läuft weiter, es erscheint nur eine Fehlermeldung · ✘ Er wird blockiert, bis du den Hook reparierst ·
   ✘ Claude fragt dich, ob er trotzdem laufen soll · ✘ Die ganze Session bricht sofort mit Fehler ab.
2. **automation** — Du startest `claude -p` ohne `--bare` in einem frisch geklonten, fremden Repo. Was kann passieren?
   ✔ Hooks und MCP-Server aus dem Repo laufen mit · ✘ Nichts, `-p` lädt keinerlei Projekt-Dateien ·
   ✘ Claude verweigert den Start ohne Vertrauensdialog · ✘ Nur die CLAUDE.md wird gelesen, sonst nichts.
3. **cost** — Ein autonomer `-p`-Lauf soll weder zu teuer werden noch endlos laufen. Was setzt du?
   ✔ `--max-budget-usd` für Kosten und `--max-turns` für Runden · ✘ Nur `/cost` beobachten und notfalls abbrechen ·
   ✘ Effort auf `low`, dann reicht das Budget von allein · ✘ Ein kleineres Modell, das begrenzt die Runden.
4. **permissions** — Du willst ein fremdes Repo erst verstehen, ohne dass etwas geändert wird. Womit startest du?
   ✔ Plan-Modus: lesen und planen, ändern erst nach Freigabe · ✘ bypassPermissions, damit keine Rückfragen stören ·
   ✘ acceptEdits, weil Git jede Änderung rückgängig macht · ✘ auto, weil der Klassifikator Gefährliches erkennt.
5. **context** — Nach langer Session hält sich Claude nicht mehr an eine frühe Absprache. Was hilft am zuverlässigsten?
   ✔ Absprache in CLAUDE.md festhalten, dann neu starten · ✘ Die Absprache im Chat mehrfach laut wiederholen ·
   ✘ Effort auf `max` stellen, dann merkt es sich mehr · ✘ Einfach weitermachen, das korrigiert sich wieder.
6. **review** — Ein Subagent meldet „alle 40 Tests grün". Was tust du, bevor du das übernimmst?
   ✔ Die Tests selbst laufen lassen und die Ausgabe lesen · ✘ Nichts, Subagenten berichten grundsätzlich korrekt ·
   ✘ Einen zweiten Subagenten fragen, ob es stimmt · ✘ Die Zahl in die Commit-Nachricht übernehmen.

Bei der Umsetzung werden Wortlaut und Fakten jedes Szenarios gegen das Zielkapitel geprüft; Antworten gleich lang
(±15 %), Reihenfolge im UI gemischt (Fisher-Yates).
