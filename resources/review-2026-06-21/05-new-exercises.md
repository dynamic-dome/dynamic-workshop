# Neue & 'verrueckte' Uebungen (Wild-Exercise-Designer) 2026-06-21

8 von 16 neuen Uebungen (Schema-Groessengrenze; weitere benannt: W3 easy, Agent-Race medium, Sabotiere-CLAUDE.md wild, Prompt-Golf medium, SOC-Rollenspiel wild, Blind-Restore hard, Cost-Battle-Royale medium, OSDP-Hardening hard).

## 1. W1 60-Sekunden-Hello  `[Micro-Warmup 60-90 Sek | easy]`

- **Thema/Block:** Block 1 Warmup vor 1.1
- **Geuebtes Konzept:** Grund-Loop, erste CLI-Beruehrung ohne Code
- **Didaktischer Wert:** Senkt Einstiegshuerde fuer Anna (null Agent-Erfahrung); trennt reden vom Datei-bauen.
- **Security-Aufhaenger:** CLI = Consultant with badge access; betritt erstmals das Gebaeude.

**Ablauf:**

claude in leerem Dir; Stell dich in einem Satz vor und sag in welchem Verzeichnis wir sind; Daumen hoch.

## 2. W2 Der Rueckgaengig-Reflex  `[Micro-Warmup 2-3 Min | easy]`

- **Thema/Block:** Block 1 Warmup nach 1.1
- **Geuebtes Konzept:** Kontrolle: Claude erstellt, Mensch verwirft
- **Didaktischer Wert:** Adressiert die groesste Neulings-Angst; zeigt das Sicherheitsnetz vor echter Arbeit.
- **Security-Aufhaenger:** Probelauf der Tuerentriegelung im Testlabor (Worktree = Test bench).

**Ablauf:**

Erstelle junk.txt mit OOPS; zeig Inhalt; loesche und bestaetige; du hast die Kontrolle.

## 3. W4 Ein-Wort-Diff  `[Micro-Warmup 2 Min | easy]`

- **Thema/Block:** Block 1 Warmup vor 1.4 Git
- **Geuebtes Konzept:** git diff/commit auf kleinster Aenderung
- **Didaktischer Wert:** Ex 1.4 ist die schwerste Block-1-Uebung; 2-Min-Vorlauf isoliert das neue Konzept.
- **Security-Aufhaenger:** Eine Tueroeffnung im Schichtbuch protokollieren (PostToolUse = Door-open log).

**Ablauf:**

Repo+README; aendere Wort X in Y; zeig git diff; committe; zeig git log --oneline.

## 4. Capture-the-Vulnerability CTF  `[CTF gegen die Uhr, Scoreboard | wild]`

- **Thema/Block:** Block 3 zu/vor 3.3
- **Geuebtes Konzept:** Adversariale Analyse, Mensch-vs-Agent-Urteil
- **Didaktischer Wert:** Wettkampf statt trockener Scan; nutzt die GENAU 8 bekannten Vulns als Flags; fuellt Domaenen-Luecke.
- **Security-Aufhaenger:** Interner Pentest am Zutrittssystem (Devils Advocate Swarm = Adversarial pentest team).

**Ablauf:**

R1 ohne Claude Vulns notieren; R2 mit Claude neu gefundene; R3 Doppelpunkte: Off-by-one parse_address UND warum raw[2] nicht zu raw[5] passt. Nichts fixen (CLAUDE.md:68).

## 5. Devils-Advocate-Duell  `[Rollenspiel-Duell, Claude als Richter | wild]`

- **Thema/Block:** Block 3 Ergaenzung 3.3 Debate
- **Geuebtes Konzept:** Prosecutor/Defender, False-Positive, Severity
- **Didaktischer Wert:** Input nennt ADMIN_PASSWORD als Grenzfall (toter Code, unreachable); Duell macht die Ambiguitaet zum Spiel; trainiert kritisches Urteil.
- **Security-Aufhaenger:** Audit-Review, Befund zwischen Pentester und Owner verhandelt (/security-review = Routine audit).

**Ablauf:**

ADMIN_PASSWORD admin123 (access_control.py:19, CLAUDE.md:57 unused). A: warum CONFIRMED. B: false-positive. Je 90 Sek. Claude faellt Urteil mit Severity.

## 6. Hook-Honeypot  `[Fallen-Bau dann gegenseitiges Knacken | hard]`

- **Thema/Block:** Block 2 wilde Vertiefung 2.2/3.8
- **Geuebtes Konzept:** Hooks als Detektoren; Audit-Trail; Hook-Debug
- **Didaktischer Wert:** Baut auf 2.2/3.7 auf, ins Offensive: Hook bauen UND umgehen; deckt Schwaeche naiver Pattern-Hooks auf (rm -rf geblockt, rm Doppel-Space nicht).
- **Security-Aufhaenger:** Honeypot-Sensor an der Vault-Tuer; Eindringling umgeht Muster-Sensoren (Hook = Access control sensor, Protected Paths = Vault rooms).

**Ablauf:**

PostToolUse-Honeypot loggt Editier-Versuche an osdp_frame_decoder.c. PreToolUse blockt rm. Bypass: Doppel-Space, rm -r -f, Variable. WICHTIG: projektlokale settings.json nicht global (Input: Bloecke zerstoeren Hooks).

## 7. Wiegand-26-Dojo  `[Gefuehrte Uebung ~25 Min Red-Green-Refactor | medium]`

- **Thema/Block:** Block 3 neue Domaenen-Uebung 3.9
- **Geuebtes Konzept:** TDD, Property-/Edge-Case-Denken, Domaene
- **Didaktischer Wert:** Fuellt Input-Luecke (keine gefuehrte Domaenen-Uebung); Wiegand-26 (8 bit Facility + 16 bit Card + 2 Parity) kennt jeder; staerkster Verkaufspunkt.
- **Security-Aufhaenger:** Wiegand ist das Protokoll Leser-Controller; falsch geparstes Parity = falscher Zutritt. Anschluss an OSDP.

**Ablauf:**

ZUERST Tests: even-parity erste 13 bits, odd-parity letzte 13 bits, Facility 0-255, Card 0-65535, Fehlerfaelle. Rot. Implementiere parse_wiegand26 bis gruen. Bonus: Parity-Bug, faengt der Test ihn?

## 8. Audit-Trail-Integritaet (EN 50131)  `[Domaenen-Uebung plus Mini-CTF ~20 Min | medium]`

- **Thema/Block:** Block 3 wertet Log-Injection auf
- **Geuebtes Konzept:** Audit+Fix mit Compliance; Newline-Injection
- **Didaktischer Wert:** Input: Log-Injection ist im PhySec-Kontext regulatorisch zentral (EN 50131), sollte vom Bonus aufgewertet werden; erst Exploit (Aha) dann Fix mit Compliance-Story.
- **Security-Aufhaenger:** Audit-Trail-Faelschung untergraebt die Beweiskette (Auto-Memory = Patrol log auto-recording).

**Ablauf:**

Exploit auf Kopie: add mit username der Newline plus gefaelschte Logzeile enthaelt; access.log bekommt gefaelschte Admin-Zeile (log_event 105-113 ungefiltert). EN-50131-Verstoss erklaeren. Fix: Newlines sanitisieren. pytest gruen. Bonus: PostToolUse-Hook erkennt manipulierte Zeilen.
