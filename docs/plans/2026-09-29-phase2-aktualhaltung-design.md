# Phase 2 — Aktualhaltung des Kurses (Design)

> Stand: 2026-09-29 · Status: Entwurf zur Abnahme · Bezug: `resources/review-2026-09-28/05-bewertung.md`
> (H-05 Lineup-Drift, H-06 Cockpit-Kopie, H-13 `--metadata`, H-16 `classification=`).
> Phase 2a baut den Mechanismus, Phase 2b bringt den Kurs damit auf den aktuellen Stand.

## Ziel

Der Kurs soll nicht mehr unbemerkt veralten. Zwischen Juli und September 2026 zog das Modell-Lineup um drei
Opus-Generationen und rund 100 CLI-Versionen weiter. Der Drift-Lint blieb grün, weil er nur bekannte Alt-Begriffe
sucht.

**Erfolgskriterium:** Der nächste Modell- oder CLI-Sprung erscheint spätestens nach einem Monat als Befund mit
Beleg. Kein Kursinhalt nennt eine Modellgeneration außerhalb des Kanons, außer an begründet markierten Stellen.
Der Kanon trägt ein Prüfdatum, und ein zu altes Prüfdatum macht den Lint rot.

## Entscheidungen (2026-09-29)

| # | Weiche | Entscheidung |
|---|---|---|
| E1 | Erkennung | Deterministisch (Python, kein LLM, kein `claude -p`). |
| E2 | Alias-Regel | Modellgenerationen und ihre Fakten (Preis, Kontext, Effort-Default, Retirement) stehen nur im Kanon. Code und Config nutzen Aliase, Prosa nennt Rollen und verweist auf den Kanon. |
| E3 | Prüfdatum | Setzt nur eine Session, die den Kanon gegen einen Monatsbericht abgeglichen hat. Lint warnt ab 45 Tagen, rot ab 90 Tagen. Monatslauf erinnert ab 60 Tagen. |
| E4 | Ansatz | Existenzprüfung der Kurs-Bezeichner gegen die Doku plus Faktenabgleich des Kanons; kein Seiten-Diff. |
| E5 | Zuschnitt | Öffentliches Werkzeug im Repo; privater Wrapper außerhalb des Repos meldet Befunde an das persönliche Todo-System des Autors. Der Monatslauf ändert keine Kursdateien und committet nichts. |
| E6 | Website | Der Monatslauf erkennt eine abweichende Cockpit-Kopie; der Re-Export bleibt ein manueller Schritt (live-wirksam). Erster Re-Export direkt nach 2b. Nachtrag 2026-09-29: verglichen wird mit der Live-Seite (Redirects gefolgt), nicht mit einer lokalen Kopie, weil lokale Checkouts auf fremden Branches stehen können. |

## Nicht-Ziele

- Keine neuen Kursinhalte für fehlende Features (neue Hook-Events, Fork-Subagents, `plugin eval`,
  `--safe-mode`, `--restricted`). Das ist Phase 3. Phase 2b behebt nur *veraltet* und *falsch*.
- Keine Prüfung von Slash-Commands und Settings-Keys in v1 (Kandidat v2; `settings.md` ist als Quelle schon dabei).
- Kein Lint auf Preise und Kontextgrößen im Fließtext (zu verrauscht). 2b räumt sie einmalig in den Kanon.
- Kein automatisches Commit, kein automatischer Re-Export, keine LLM-Bewertung.

## Bausteine

### 1. Kanon `resources/_canonical.md`

Einzige Quelle für Versionsfakten. Neu:

- Kopfzeile `Geprüft: YYYY-MM-DD · CLI 2.1.NNN` (maschinenlesbar, genau eine Zeile).
- Modelltabelle mit den Spalten `Modell | ID | Alias | Tier | Status | Retirement frühestens | Kontext | In $/1M | Out $/1M | Rolle`.
- Hinweis zur Alias-Auflösung: `opus`/`sonnet` lösen je nach Anbieter unterschiedlich auf, `fable`/`best` im
  Claude-apps-Gateway auf eine ältere Generation (Quelle: `model-config.md`).
- Abschnitt `Quellen` mit den 13 Doku-URLs, der npm-Adresse und der Changelog-Adresse. Das Werkzeug liest die
  Liste von dort.
- Die bisherige Verbotsliste entfällt; die Generationsregel des Lints deckt sie ab.

### 2. Lint `tools/lint_currency.py`

- **Generationsregel:** Im Live-Content (gleiche Ausschlüsse wie heute: `docs/`, `resources/review-*/`, Archiv,
  `.agent-memory`) ist außerhalb von `_canonical.md` rot:
  `(Opus|Sonnet|Haiku|Fable|Mythos)[ -]?<Zahl>` und `claude-(opus|sonnet|haiku|fable|mythos)-<Zahl>…`
  (case-insensitiv).
- **Marker:** Ein Treffer ist erlaubt, wenn **dieselbe Zeile** `version-pinned: <Grund>` enthält (beliebige
  Kommentarsyntax, Grund mindestens drei Zeichen). Absatzweite Marker gibt es bewusst nicht.
- **Erlaubt bleibt:** CLI-Versionsangaben wie „seit 2.1.145" (Geschichte) und Aliase in Code, Config und `--model`.
- **Stale-Gate:** liest `Geprüft:` aus dem Kanon. Über 45 Tage WARNUNG (Exit 0), über 90 Tage rot. Fehlende oder
  unlesbare Zeile ist rot (fail-closed). Das Datum „heute" ist ein Funktionsparameter; nur der CLI-Aufruf nutzt das
  echte Datum.

### 3. Currency-Check

`tools/currency_extract.py` — reine Funktionen ohne Netz und Dateisystem:

- **Kurs-Bezeichner** (gleiche Dateimenge wie der Lint; `\`-Fortsetzungszeilen werden vorher verbunden):
  - Flags: `--x` in Zeilen, in denen `claude` als Wort vor dem Flag steht, plus Inline-Code, der mit `--x`
    beginnt (`` `--metadata` ``). CSS-Variablen und Fließtext-Flags ohne Backticks zählen nicht.
  - Env-Variablen: `ANTHROPIC_*` und `CLAUDE_*`.
  - Hook-Events: Schlüssel unter `"hooks"` in parsebaren ```` ```json ````-Blöcken; die Zahl nicht parsebarer
    Blöcke kommt in den Bericht.
  - Modell-IDs (`claude-<familie>-…`), Aliase aus `--model <x>` und `model: <x>`, Permission-Modi aus
    `--permission-mode <x>` und `"defaultMode": "<x>"`.
- **Doku-Bezeichner:** Vereinigung aller 13 Doku-Quellen (ein Flag, das nur in `headless.md` steht, existiert).
- **Parser:** Kanon-Kopfzeile und -Tabelle; Deprecations-Tabelle (ID, Status, Retirement, „Not sooner than
  <Datum>"); Alias-Tabelle aus `model-config.md`; Changelog-Abschnitte ab einer Version.

`tools/currency_check.py` — Ablauf, Bericht, Exit-Code:

1. Kanon lesen (Prüfdatum, CLI-Version, Modelltabelle, Quellen).
2. Quellen holen (Redirects folgen, Timeout 30 s je Quelle, UTF-8).
3. Kurs-Bezeichner ziehen, Prüfungen ausführen, Bericht schreiben.
4. Zustand nur nach einem vollständigen Lauf schreiben.

**Quellen (13 Doku-Seiten):** code.claude.com/docs/en/{cli-reference, env-vars, hooks, headless, authentication,
github-actions, permission-modes, model-config, mcp, skills, settings}.md, platform.claude.com/docs/en/models/overview.md,
platform.claude.com/docs/en/about-claude/model-deprecations.md. Dazu die npm-Registry (neueste CLI-Version) und
code.claude.com/docs/en/changelog.md.

**Befundstufen:**

| Stufe | Befund |
|---|---|
| Rot | Kurs-Bezeichner fehlt in der Doku-Vereinigung und nicht in der Ausnahmeliste. |
| Rot | Kanon-Modell nicht mehr `Active`, oder frühestes Retirement in weniger als 60 Tagen. |
| Rot | Neuestes aktives Modell eines Tiers fehlt im Kanon; Kanon-Retirement weicht von der Tabelle ab. Tiers sind die Familien der Kanon-Tabelle; „neuestes" nach Versionstupel aus der ID (Datumssuffix ignoriert). Familien der Deprecations-Tabelle, die der Kanon nicht führt (z. B. Mythos), sind Info. |
| Rot | Kanon älter als 90 Tage. |
| Rot | Cockpit der Website (live abgerufen, Redirects gefolgt) weicht vom Kurs-Cockpit ab (sha256 nach Normalisierung: LF, Provenienz-Zeile entfernt). |
| Rot | Verwaiste Ausnahme (Eintrag kommt im Kurs nicht mehr vor). |
| Gelb | Changelog-Zeile seit der Kanon-CLI-Version, die einen Kurs-Bezeichner nennt (Kandidat, braucht Urteil). |
| Info | Changelog-Zeilen mit `removed|deprecated|renamed|no longer|default` ohne Kurs-Bezug; neue Doku-Bezeichner seit dem letzten Lauf (Vorrat für Phase 3); geänderte Seiten (sha256); Redirects mit neuer URL; Kanon-Alter 45–90 Tage. |

**Fail-closed (Exit 2 statt „sauber"):** HTTP-Fehler, Timeout, Body unter Mindestgröße (5 KB je Seite), Auswertung
unter Mindestmenge (Flag-Vereinigung < 80, Env-Vereinigung < 150, Deprecations-Tabelle < 10 Zeilen, Alias-Tabelle
< 3 Zeilen), Kanon-CLI-Version im Changelog nicht gefunden, Kanon nicht lesbar. Die Mindestwerte stehen als benannte
Konstanten im Code; Messwerte vom 2026-09-29 unten.

**Exit-Codes:** 0 = keine roten und gelben Befunde · 1 = mindestens ein roter oder gelber Befund · 2 = Quelle oder
Kanon unbrauchbar.

**Zustand (lokal, nicht versioniert, `.currency/` in `.gitignore`):** `state.json` mit Bezeichner-Mengen und sha256
je Quelle, Befund-Schlüsseln des letzten Laufs, Datum und CLI-Version; `reports/YYYY-MM-DD.md`.

**Bericht:** Kopf (Datum, Kanon-Prüfdatum, neueste CLI-Version), Zählung je Stufe, Befunde mit `datei:zeile` und
Beleg, Kennzeichnung **neu** oder **weiterhin offen** gegenüber dem letzten Lauf, Quellentabelle (URL, End-URL,
Bytes, sha256-Kurzform, geändert ja/nein).

### 4. Ausnahmeliste `tools/currency_exceptions.txt`

Format `bezeichner | grund`, eine Zeile je Eintrag. Startbestand laut Messung etwa sechs Fremd-Flags (Plugin-,
Übungs-, git- und Playwright-Argumente). Ein Test friert die Anzahl ein: sie darf nur schrumpfen. Neue Einträge nur
mit Begründung im Commit.

### 5. Monatlicher Lauf (privat, außerhalb des Repos)

- Wrapper ruft `python tools/currency_check.py --cockpit-url <Live-URL des Website-Cockpits>` und übersetzt:
  - Exit 1 mit **neuen** roten oder gelben Befunden gegenüber dem letzten Lauf → Todo „Workshop-Drift: n rot,
    m gelb → Bericht <Pfad>". Befunde, die schon im letzten Lauf standen, erzeugen kein neues Todo (kein
    Monats-Duplikat); das Stale-Gate eskaliert, wenn niemand sie abarbeitet.
  - Keine neuen roten oder gelben Befunde und Kanon älter als 60 Tage → Todo „Kanon bestätigen", höchstens einmal
    je Kanon-Prüfdatum (eigener kleiner Zustand des Wrappers). Nachtrag 2026-09-29: nicht an „Exit 0" gebunden, weil
    ein dauerhaft offener Befund (etwa ein Retirement-Hinweis) den Exit auf 1 hält und die Erinnerung sonst nie käme.
  - Exit 2, Absturz oder Timeout (10 min) → Todo „Monatslauf fehlgeschlagen".
- Die Todo-Aktion wird dem Wrapper übergeben; Tests nutzen einen Fake.
- Windows-Aufgabe: monatlich am 1. um 09:00, „Starten, wenn verpasst", ohne gespeichertes Passwort (S4U), ohne
  Fenster (`pythonw -X utf8`), Laufzeitlimit 15 min.
- Eine still tote Aufgabe fällt spätestens über das 90-Tage-Stale-Gate auf.

## Tests und Abnahme

**`tools/test_currency_check.py` (offline, Fixtures unter `tools/fixtures/currency/`, festes Datum):** jede Regel mit
Positiv- und Negativkontrolle.

- Existenz: `--metadata` im Kurs, fehlt in der Doku → rot; vorhanden → sauber.
- Mischregel: `git --orphan` im Fließtext ignoriert; `` `--x` `` erfasst; `claude \`-Fortsetzung erfasst;
  CSS-`--accent` ignoriert.
- Fail-closed: 27-Byte-Redirect-Rumpf, leere Tabelle, Unterschreitung einer Mindestmenge → Exit 2, `state.json`
  unverändert.
- Fakten: „Not sooner than October 15, 2026" als Datum; < 60 Tage → rot; neues aktives Modell → rot;
  Changelog-Bereich beginnt bei der Kanon-Version.
- Ausnahmen: eingefrorene Anzahl; verwaiste Ausnahme → rot.
- Neu/weiterhin offen: zweiter Lauf mit gleichem Befund → „weiterhin offen", kein neuer Befund-Schlüssel.
- Lint: Generationsregel rot/grün; Marker ohne Grund rot; Stale-Gate bei 44/46/91 Tagen; fehlende `Geprüft:`-Zeile rot.
- Gegenprobe: Auszüge aus Vorher-Fassungen (per `git show <commit>:<pfad>`, Commit-Hash im Fixture-Kopf) müssen
  `CLAUDE_MODEL` (H-14) und `claude-opus-4-8` finden.
- Wrapper: Exit-Code-Übersetzung und „nur neue Befunde" mit Fake-Todo-Aktion.

**Mutationsprobe beim Bau:** z. B. Mindestmenge entfernen, Marker-Grund nicht prüfen, Zustand auch bei Exit 2
schreiben — jeweils muss ein Test rot werden.

**Live-Abnahme (einmalig):**

1. Echter Lauf: Bericht enthält `--metadata` als rot.
2. Windows-Aufgabe per `schtasks /Run`: Berichtsdatei und Todo entstehen, kein Fenster.
3. Bestehende Suiten grün: `tools/` (109) und `workshop-playground` (18).

## Reihenfolge

1. **2a-1 Checker:** `currency_extract` + `currency_check` + Ausnahmeliste + Offline-Tests.
2. **2a-2/2b-1 Kanon, Lint und Modell-Sweep in einem Paket:** Kanon auf das aktuelle Lineup (Fable 5.1, Opus 5.5,
   Sonnet 5.5, Haiku 4.5 mit Retirement-Hinweis) und Alias-Hinweis; Generationsregel und Stale-Gate scharf;
   Modellnennungen (58 Zeilen in 12 Dateien) auf Aliase oder Kanon-Verweis. Zusammen, sonst ist der Lint dazwischen rot.
   `agents/workshop-mentor.md` gemäß Repo-Regel nachziehen.
3. **2b-2 Erster Live-Lauf und seine Befunde:** `--metadata` (H-13), `--worktree-base-ref`, `--no-verbose`,
   `--fast`, dazu H-16 `classification=` (steht in denselben Cockpit-Zeilen wie die Modell-IDs).
4. **2a-3 Wrapper, Windows-Aufgabe, Live-Abnahme.**
5. **Doku:** `HOW-TO-USE.md` (Currency-Abschnitt), Stand in `review-2026-09-28/05-bewertung.md`.
6. **Re-Export des Cockpits** auf die Website, nach Freigabe (live-wirksam). Push nach Sweep auf private
   Pfade/Secrets und Freigabe.

## Risiken und bewusste Lücken

- **Doku-Formatwechsel** kann Parser leerlaufen lassen → Mindestmengen machen daraus Exit 2 statt „sauber".
- **Neue Doku-Seiten** außerhalb der 13 Quellen: ein dort dokumentiertes Flag erscheint als Fehlbefund. Abhilfe ist
  eine neue Quelle im Kanon, nicht eine Ausnahme.
- **Verhaltensänderungen ohne neuen Bezeichner** (z. B. geänderter Default) fängt nur die Info-Zeile aus dem
  Changelog; sie erzeugt kein Todo. Der 60-Tage-Bestätigungsschritt liest den Bericht.
- **Preise und Kontextgrößen** im Fließtext sind nicht gelintet (siehe Nicht-Ziele).
- **Alias-Prosa** macht Drift für den Lint unsichtbar; deshalb stehen Fakten nur im Kanon, und der Kanon wird geprüft.

## Messwerte aus dem Entwurf (2026-09-29, Wegwerf-Messung, nicht versioniert)

- Alle 13 Doku-Quellen liefern `text/markdown`; npm meldet 2.1.284. Die Modellübersicht ist umgezogen
  (`/about-claude/models/overview.md` → `/models/overview.md`); ohne Redirect-Folgen kamen 27 Bytes zurück.
- Deprecations-Tabelle: Pipe-Tabelle mit ID, Status, Deprecated, Retirement.
- Doku-Vereinigung (10 Seiten): 119 Flags, 282 Env-Variablen.
- Mischregel mit 13 Quellen: 59 Kurs-Flags, 10 fehlen in der Doku — `--metadata` (bekannt, H-13), drei vermutlich
  neue Befunde (`--worktree-base-ref`, `--no-verbose`, `--fast`), sechs Fremd-Flags für die Ausnahmeliste
  (`--decompose`, `--door`, `--headed`, `--notebook`, `--orphan`, `--or--`).
- Env-Variablen: 12 im Kurs, 0 fehlen.
- Breite Regel „jedes `--x`": 116 Treffer, 70 fehlen (überwiegend CSS-Variablen) — verworfen.
- Modellnennungen außerhalb des Kanons: 58 Zeilen in 12 Dateien (Cockpit 7 Zeilen, keine Modelltabelle).
