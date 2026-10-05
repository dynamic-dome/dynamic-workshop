# Vorführen: S2.10 · Hook-Ausgaben und das Secure Diff Gate

> Demo und Hinweise für Moderierende zum Kapitel [S2.10 · Hook-Ausgaben und das Secure Diff Gate](../../library/s2-10-hook-ausgaben.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Secure Diff Gate, Schreibschutz per Hook

**Ziel:** Einen PreToolUse-Hook zeigen, der Claude am Schreiben in sensible Dateien **hindert** (`.env`, `secrets/`, `*.pem`), und die Grenze, an der er nichts mehr sieht. Das ist Zutrittskontrolle für Code.

Zeig die Übung aus dem Kapitel live: die Übung „das Secure Diff Gate“ in [S2.10](../../library/s2-10-hook-ausgaben.md). Startzustand wie dort: der Ordner `~/cc-workshop/gate` mit `.claude/hooks/secure-diff-gate.py`, kopiert aus den getesteten Vorlagen in `resources/demos/assets/hooks/`, und der `.claude/settings.json` aus Schritt 3. Der Vertrauensdialog ist einmal bestätigt. Die Bash-Fassung `secure-diff-gate.sh` braucht `jq`; die Python-Fassung nicht, und die Übung nutzt sie. Starte mit `claude --permission-mode acceptEdits`: Dann sind Dateiänderungen ohne Rückfrage erlaubt, und ein abgelehnter Schreibzugriff kommt vom Hook, nicht von einem Dialog.

**Ablauf:** Schritte 2 bis 8 der Übung: der Handtest des Gates mit `.env` und `utils.py`, der geblockte Auftrag für `.env`, der durchgelassene für `utils.py`, der Shell-Weg `echo DATABASE_URL=x > .env`, der am Gate vorbeigeht, und die Deny-Regel `Edit(./.env)`, die ihn schließt. Zeig dabei die Konfiguration: Der Matcher `Write|Edit` feuert bei jeder Dateiänderung über diese beiden Tools, nicht bei Shell-Befehlen.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 10 bis 12 Minuten für die ganze Übung, etwa 5 Minuten ohne den Shell-Weg und die Deny-Regel.

**Sagen:**

- Handtest (Schritt 2): „Das ist ein Türcontroller mit Sperrliste. Diese Pfade sind wie der Serverraum: kein Zutritt ohne ausdrückliche Freigabe." Das Skript endet mit `exit 2` für `.env` und mit `exit 0` für `utils.py`.
- Schritt 5: „Claude hat nicht beschlossen, die .env-Datei auszulassen. Der Hook hat diesen Schreibzugriff geblockt. Das ist kein Vorschlag an das Modell, sondern eine Sperre an dieser Tür." Zeig im zweiten Terminal, dass es keine `.env` gibt.
- Schritt 6: „Normale Türen gehen normal auf. Nur die geschützten Zonen sind zu. Least Privilege in Aktion."
- Schritt 7: „Die Shell ist eine andere Tür. Der Matcher `Write|Edit` sieht keine Shell-Befehle, deshalb meldet das Gate hier nichts." Frag die Gruppe, wie man diese Tür schließt, bevor du Schritt 8 zeigst. Lösch `.env` danach von Hand.
- Schritt 8: „Eine Deny-Regel gilt laut Doku auch für das Ziel einer Umleitung. Gegen beliebige Unterprozesse, die Dateien indirekt schreiben, hilft erst die Sandbox ([S3.9](../../library/s3-09-geschuetzte-pfade-und-sandbox.md))."
- Zum Schluss: „In eurer Zutrittskontrolle habt ihr Zonen. Manche Türen sind immer offen (Lobby), manche brauchen eine Karte (Büros), manche bleiben ohne ausdrückliche Freigabe zu (Tresor). Dieser Hook ist die Tresor-Regel für euren Code."

**Wenn etwas schiefgeht:**

- **Der Hook feuert, blockt aber nicht (exit 0 statt 2):** Teste das Skript außerhalb von Claude von Hand, wie in Schritt 2 der Übung. Es muss `exit=2` zeigen.
- **Der Schreibzugriff wird nicht geblockt, und es kommt auch keine Meldung:** Prüf den Pfad zum Skript in der `settings.json`, dann, ob der Vertrauensdialog bestätigt wurde. `/hooks` zeigt, ob der Eintrag geladen ist.
- **Die Bash-Fassung blockt jeden Schreibzugriff:** Dann fehlt `jq`, und das Gate blockt, weil es seine Eingabe nicht lesen kann, wie der Wächter aus [S2.8](s2-08-hook-einrichten.md). Nimm die Python-Fassung aus der Übung.
- **Unter macOS und Linux startet `python` nicht:** Dort heißt Python `python3`; ersetze es im Handtest und in der `settings.json`.

</details>
