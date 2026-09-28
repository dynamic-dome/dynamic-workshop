# Plan — Hook-Hotfix (2026-09-28, Größe M)

Auslöser: Delta-Review `resources/review-2026-09-28/05-bewertung.md`, Befunde H-01 bis H-04, F-01, F-04, F-05, A-01.
Quelle der Wahrheit: offizielle Hooks-Referenz `https://code.claude.com/docs/en/hooks.md` (Abruf 2026-09-28).

## Ziel

Jeder Claude-Code-Hook, den der Kurs zum Abtippen oder Kopieren anbietet, stimmt mit der Referenz überein und
ist durch einen ausführbaren Test belegt, der mit Eingaben im offiziellen Format läuft (inkl. Windows-Pfaden).

## Belegte Fakten (Referenz, wörtlich geprüft)

- Nur `exit 2` blockt (PreToolUse u. a.). Andere Nicht-Null-Codes: nicht blockierender Fehler, Aktion läuft weiter.
- Timeout eines PreToolUse-Hooks blockt nicht („don't count on a stalled hook to act as a gate").
- PreToolUse-Eingabe: `tool_name`, `tool_input` (Bash: `tool_input.command`; Write: `file_path`, `content`;
  Edit: `file_path`, `old_string`, `new_string`). Dateipfade immer absolut, unter Windows mit Backslashes.
- PostToolUse-Eingabe: `tool_input` + `tool_response` (Bash: `stdout`, `stderr`, `interrupted`, `isImage`).
- PostToolUse kann nicht blocken (exit 2 zeigt stderr an Claude). Ausgabe ersetzen: `hookSpecificOutput` mit
  `hookEventName: "PostToolUse"` und `updatedToolOutput` in der Form des Tools; falsche Form wird ignoriert.
- `suppressOutput`: „Has no effect". `continueOnBlock` gibt es nur bei prompt-basierten Hooks.

## Test-Nahtstellen

1. Hook-Skript als Blackbox: JSON auf stdin → Exit-Code, stderr, stdout-JSON (`tools/test_course_hooks.py`).
2. Anti-Muster-Lint über Live-Kursinhalt (`tools/lint_hooks.py`), mit Negativkontrolle im Test.

## Aufgaben

1. Test-Harness mit Payload-Bausteinen nach Referenz (Bash-PreToolUse, Write/Edit-PreToolUse mit Windows-Pfad,
   Bash-PostToolUse).
2. `secure-diff-gate.{py,sh}`: Backslashes normalisieren (RED mit Windows-Pfad zuerst).
3. Neues Asset `safety-check.{sh,ps1,py}` (PreToolUse Bash, exit 2) für Übung 2.1, Modul 2.2, Voraussetzungen, Cockpit.
4. Neues Asset `sensitive-data-scanner.py` (PreToolUse Write|Edit) für Übung 3.8.
5. Neues Asset `redact-output.py` (PostToolUse Bash, `updatedToolOutput` in Bash-Form) für Modul 2.2 und Cockpit.
6. Übung 2.6 Token Firewall auf `updatedToolOutput` umstellen; neues Asset `token-firewall.py`.
7. Wächter gegen Anti-Muster + Hook-JSON-Struktur (umgesetzt als Test in `tools/test_course_hooks.py` statt eigenem
   Lint-Skript, mit eingebauter Negativkontrolle).
8. Textkorrekturen: Modul 2.2 (Blockieren, erstes Beispiel, erweiterte Ausgabe, `continueOnBlock`), Übungen 2.1/2.6/3.8,
   Demo 2.2b-Inline-Hook, Voraussetzungen, Cheatsheet, Troubleshooting S4.9/S4.10 (fail-open als Lektion),
   Wiederholungsfragen, Mentor, Cockpit-HTML.
9. Weitere belegte Einzelfehler: `--bare` (F-01), auto-Modus (A-01), `skillListingMaxDescChars` (F-04),
   `claude plugin validate <path>` (F-05).
10. Prüfen: alle Tests, beide Lints, Cockpit im Browser laden (JS darf nicht brechen), Mentor-Sync.

## Nicht in diesem Hotfix

Modell-Lineup und Kanon (Phase 2, alias-basiert), neue Features (W-08 ff.), Cockpit-Export auf die Website (Phase 4).
