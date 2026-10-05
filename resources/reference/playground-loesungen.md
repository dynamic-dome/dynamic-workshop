# Lösungen zum Playground

> **Erst nach den Übungen lesen.** Diese Seite liegt absichtlich außerhalb von `workshop-playground/`. Was dort in
> der `CLAUDE.md` oder in einem Kommentar stünde, läse Claude Code in jeder Sitzung mit, und eine Übung zeigte dann
> nur noch, dass es eine Liste abschreiben kann. `tools/test_playground.py` hält den Playground frei von Hinweisen.

Der Playground enthält neun absichtlich eingebaute Schwachstellen: fünf in `access_control.py`, vier in
`osdp_frame_decoder.c`. Die Orte sind Funktionsnamen, damit sie Änderungen am Code überstehen.

## `access_control.py`

| Nr. | Schwachstelle | Ort | Woran du sie erkennst | Was damit geht |
|---:|---|---|---|---|
| 1 | Fest eingetragenes Passwort | Konstante `ADMIN_PASSWORD` | Zugangsdaten als Zeichenkette im Quelltext | Das Passwort steht im Repo und in jeder Kopie. Im Ablauf wird es nicht benutzt; es ist die leichteste der fünf. |
| 2 | Path Traversal | `read_log()` | Der Dateiname aus dem Unterbefehl `read-log` geht ungeprüft in `open(f"logs/{log_name}")`. | `read-log ../access_control.py` liest eine Datei außerhalb von `logs/`. |
| 3 | Command Injection | `backup_database()` | `subprocess.run(..., shell=True)` mit dem Dateinamen aus dem Unterbefehl `backup` | Ein Dateiname wie `x.json; <befehl>` führt den zweiten Befehl aus. |
| 4 | Log-Injection | `log_event()` | `username` und `action` stehen ungefiltert in der Logzeile. | Ein Zeilenumbruch im Namen fälscht eine ganze Logzeile; das Protokoll taugt dann nicht mehr als Nachweis. |
| 5 | Fail-open in der Fachlogik | `check_access_resilient()` | Fehlt `users.json` oder ist sie kaputt, gibt die Funktion `True` zurück. | `door-check eve` gewährt Zutritt, ohne dass es eine Datenbank gibt. Ein Musterscanner findet das nicht: kein gefährlicher Aufruf, kein Geheimnis, nur die falsche Fehlerrichtung. `check_access()` und `load_db()` daneben verweigern im Fehlerfall. |

Nummer 5 ist die Schwachstelle, an der sich Scanner und Fachwissen trennen ([S3.6](../library/s3-06-devils-advocate.md)).
Nummer 4 findet ein Scan oft von selbst, obwohl kein Kapitel danach fragt.

## `osdp_frame_decoder.c`

| Nr. | Schwachstelle | Ort | Woran du sie erkennst |
|---:|---|---|---|
| 1 | Buffer Overflow | `decode_data_payload()` | `memcpy` kopiert `data_len` Bytes vom Draht, ohne gegen `OSDP_MAX_FRAME_LEN` zu prüfen. |
| 2 | Integer Overflow | `compute_crc()` | `byte_count` wird in `uint8_t` gerechnet. Ab einer Länge von 252 läuft die Addition über, die Prüfsumme deckt dann nur einen Bruchteil des Frames. |
| 3 | Format String | `log_frame()` | `printf(cmd_name)` statt `printf("%s", cmd_name)`; der Name kommt von der Gegenstelle. |
| 4 | Off-by-one (Zusatz) | `read_frame_crc()` | Gelesen wird `raw[frame_len]`; das letzte gültige Byte ist `raw[frame_len - 1]`. |

Kein eingebauter Fehler: Die Prüfung der Hex-Eingabe in `main()` (leer, ungerade Länge) ist bewusst robust.
Das Frame-Layout ist vereinfacht und entspricht nicht dem echten OSDP; der Kopfkommentar der Datei sagt, worin.

## Regeln für die Arbeit im Playground

- Der Stand auf `main` ist das Übungsmaterial. Fixes gehören auf einen eigenen Branch oder in einen Worktree
  ([S1.18](../library/s1-18-worktrees.md)) und werden nicht nach `main` gemergt.
- Die Tests (`python -m pytest -v` im Ordner) prüfen nur das gewollte Verhalten, keine der Schwachstellen.
- Kapitel, die den Playground nutzen: [S1.8](../library/s1-08-kontextfenster.md),
  [S2.8](../library/s2-08-hook-einrichten.md), [S2.18](../library/s2-18-rag-und-notebooklm.md),
  [S3.6](../library/s3-06-devils-advocate.md), [S3.8](../library/s3-08-rechte-fuer-autonomie.md),
  [S4.5](../library/s4-05-ci-pipelines.md), [S4.8](../library/s4-08-abschlussprojekt.md).
