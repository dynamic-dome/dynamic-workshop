# Vorführen: S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline

> Demo und Hinweise für Moderierende zum Kapitel [S3.6 · Devil's Advocate: eine adversariale Prüf-Pipeline](../../library/s3-06-devils-advocate.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: Devil's Advocate, adversariales Sicherheitstesten

**Ziel:** Eine automatisierte Pentest-Pipeline in Aktion zeigen. Wer das Plugin nicht hat, zeigt stattdessen die Übung aus dem Kapitel live: die Übung „Ankläger und Verteidiger selbst bauen“ in [S3.6](../../library/s3-06-devils-advocate.md) (Ordner `~/cc-workshop/gegenpruefung`, `door.py`, die Subagenten `accuser` und `defender`, Schritte 1 bis 8). Dort fällst du das Urteil je Befund selbst und belegst es am Programm.

**Vorbereitung**

- Den `workshop-playground/` hast du mit dem Workshop-Repo geklont ([Werkstatt erweitern](../../reference/werkstatt-erweitern.md#workshop-repo-und-playground)). Er wird so verwendet, wie er ist; du legst keine Dateien an.
- 🔧 Das Workshop-Plugin `devil-advocate-swarms` ist installiert (`claude plugin list`).

**Schritt 1: in den Playground wechseln**

```bash
cd workshop-playground/
```

**Schritt 2: den Schwarm starten**

```
/devil-advocate-swarms:swarm scan access_control.py
```

**Schritt 3: Stufe 1, die Scanner**

Die Scanner laufen parallel. Sag, wonach jeder sucht, und zeig: Mehrere finden dieselben eingebauten Probleme. Das hilft gegen Zufallsrauschen, ist aber kein Beleg: Alle Scanner sind dasselbe Modell, ihre Irrtümer hängen zusammen. Erwartet sind die fünf eingebauten Schwachstellen von `access_control.py`; Orte und Erklärung stehen in [Lösungen zum Playground](../../reference/playground-loesungen.md), erst nach den Übungen lesen.

Übersieht der Schwarm den fail-open-Fehler, halte an und untersuche `check_access_resilient()` von Hand. Dieser Befund ist am nächsten am Fach der Teilnehmenden: Eine Zutrittsanlage muss sicher schließen, statt Zutritt zu gewähren, weil die Datenbank des Controllers nicht erreichbar ist.

**Schritt 4: Stufe 2, die Debatte**

Das ist der wichtigste Teil. Werde langsamer und erkläre, was passiert:

- Der Ankläger argumentiert jeden Befund wie in einem Exploit-Bericht.
- Der Verteidiger sucht Gründe, warum er nicht ausnutzbar ist.
- Command Injection: Der Verteidiger hat kein gutes Argument. Bestätigt.
- Path Traversal: Der Verteidiger sagt vielleicht „`logs/` ist ein kontrollierter Ordner", der Ankläger kontert mit dem Beispiel `../../etc/passwd`. Bestätigt.
- Fail-open: Der Verteidiger sagt vielleicht „bei Türen zählt die Verfügbarkeit", der Ankläger kontert, dass Notausgang und Prüfung der Berechtigung getrennte Sicherheitskanäle sind. Bestätigt.
- Fest eingetragenes Passwort: Hier hat der Verteidiger ein gutes Argument, denn `ADMIN_PASSWORD` ist toter Code. Das Ergebnis kann zu Recht CONFIRMED mit niedriger Schwere oder NEEDS INVESTIGATION lauten.
- Wird ein Befund wegdiskutiert, zeig es: So spart die Pipeline Menschen Zeit.

**Schritt 5: Stufe 3, der Konsens**

Zeig die Aufteilung in CONFIRMED und FALSE POSITIVE. Das Urteil fällst du, nicht die Pipeline. Ein Beleg ist ein Test, der den Befund reproduziert, oder ein Programmlauf; zwei überzeugende Texte ersetzen ihn nicht.

**Schritt 6: Stufe 4, die Fixer**

Zeig, wie die Fixes eingespielt werden. Jeder Fix ist klein und gezielt, jeder hat einen Regressionstest.

**Schritt 7: Bilanz ziehen**

Geh die Befunde durch. Ziel ist, dass alle fünf eingebauten Schwachstellen gefunden werden. Findet der Schwarm nur vier, nutze die fehlende als Lehrmoment: Auch adversariale Automatisierung braucht ein fachkundiges menschliches Review.

**Optionaler Schritt: den Schwarm auf den C-Playground ansetzen**

Für Gruppen aus Embedded und physischer Sicherheit:

```
/devil-advocate-swarms:swarm scan osdp_frame_decoder.c
```

Erwartet sind die vier Speicherfehler der Datei; Orte und Erklärung stehen in [Lösungen zum Playground](../../reference/playground-loesungen.md).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 12 Minuten geplant; reserviere live etwa 18 Minuten, falls Debatte und Konsens viel ausgeben.

**Rahmung:** Stell die Demo als automatisierten Penetrationstest mit Gerichtsverfahren vor, denn genau das ist sie. Wer aus der Cybersecurity kommt, fühlt sich hier zu Hause; für diese Gruppe ist die Demo der Höhepunkt.

**Sagen (nach Schritt 7):** „Das ist ein automatisierter Penetrationstest mit eingebauter rechtlicher Prüfung. Der Ankläger ist euer Pentester, der den Exploit-Bericht schreibt. Der Verteidiger ist euer Entwickler, der erklärt, was wirklich ausnutzbar ist und was nicht. Den Konsens zieht am Ende ihr als Sicherheitsverantwortliche: Das Urteil über jeden Befund bleibt bei euch. Die Fixer sind euer Patch-Team. Das Ganze ist gerade von allein durchgelaufen. Für die Security-Leute im Raum: Das ist eure Welt, angewendet auf Code."

**Welcher Playground?** `access_control.py` (Python, Benutzerverwaltung) zeigt Schwachstellen, wie sie in Backend-Diensten vorkommen. `osdp_frame_decoder.c` (C, eingebetteter OSDP-Frame-Parser) zeigt Speicherfehler, wie sie in Firmware vorkommen: eingebettete Protokolle, Parsen von Wire-Formaten. Zeig beide, wenn die Zeit reicht, sonst den, der näher am Arbeitsalltag der Gruppe ist.

**Nach der Demo:** Die Fixer haben `access_control.py` geändert. Setz die Datei im Playground mit `git checkout -- access_control.py` zurück, damit die Schwachstellen für die nächste Runde erhalten bleiben.

**Wenn etwas schiefgeht:**

- **Plugin nicht installiert:** Zeig die Aufzeichnung aus der Vorbereitung und besprich die vier Stufen (Scan → Debatte → Konsens → Fix). Oder zeig live die Übung aus dem Kapitel: Dort laufen Ankläger und Verteidiger als eigene Subagenten nacheinander, und das Urteil fällst du selbst.
- **Der Verteidiger stimmt dem Ankläger einfach zu:** Beide sind dasselbe Modell. Stuft der Verteidiger einen Fund als erreichbar ein, such live selbst nach den Aufrufen, statt dich auf sein Zitat zu verlassen.
- **Beide übersehen dasselbe, etwa den Fail-open:** Hat keiner den Fachfehler genannt, ist die Gegenprobe blind dafür. Das ist ein Lehrmoment.
- **Die Debatte sieht in dieser Plugin-Version anders aus:** Erzähl die Absicht („Der Ankläger argumentiert für die Ausnutzbarkeit, der Verteidiger hält dagegen"), auch wenn die Stufen anders heißen. Die Architektur zählt mehr als die Bezeichnungen.

</details>

### Demo: Vom Advisory zum PR (CVE-Fix-Pipeline)

Diese Demo überträgt die Idee: Sie zeigt keinen Schwarm, sondern den Weg „Research-to-Patch" mit Websuche, Plan-Modus ([S1.14](../../library/s1-14-plan-modus.md)) und automatischem PR. Das Automatisieren von PRs vertieft [S4.5](../../library/s4-05-ci-pipelines.md).

**Ziel:** Zeigen, wie Claude eine echte Schwachstelle in einer Abhängigkeit behebt.

**Schritt 0: eine verwundbare Abhängigkeit einbauen (vor der Demo)**

Die `workshop-playground/requirements.txt` enthält nur ein ungepinntes `pytest`. Pinne vor der Demo vorübergehend eine bekannt verwundbare ältere Bibliothek, damit der CVE-Fix echten Input hat:

```bash
# Inside workshop-playground/
# Option A (Python, recommended):
echo "requests==2.5.0" >> requirements.txt    # CVE-2018-18074

# Option B (alternative Python CVE):
# echo "urllib3==1.24.0" >> requirements.txt
```

Wichtig: Die Version wird **absichtlich nicht installiert**. Die Demo zeigt nur Scan, Fix und PR, keine Ausnutzung. Claude braucht nur den Versionsstring im Manifest, um ein Advisory dazu zu finden.

**Schritt 1: Claude um den Fix bitten**

```
/plan Find and fix any known CVEs in our dependencies.
Search the web for current advisories, identify the fix version,
update the lockfile, run tests, and create a PR.
```

Geh durch, was Claude tut:

1. **WebSearch:** findet das Advisory bei NVD oder GitHub zur gepinnten alten Version
2. **Plan:** bestimmt das betroffene Paket, die Version mit dem Fix und den Migrationsweg
3. **Edit:** ändert die Version in `requirements.txt`
4. **Bash:** führt nach der Änderung `pip install` und die Tests aus (ohne Internet lässt du die Installation weg, den PR kann Claude trotzdem erstellen)
5. **Git:** committet und erstellt einen PR mit Verweis auf die CVE

**Schritt 2: die PR-Beschreibung zeigen**

Zeig, dass Claude aufgenommen hat:

- CVE-ID und Link zum Advisory
- was verwundbar war und warum
- was geändert wurde
- die Testergebnisse

**Schritt 3: nach der Demo aufräumen, mit einem Befehl**

Bearbeite die Datei nicht von Hand, das vergisst man leicht. Ein Revert setzt `requirements.txt` auf den committeten Stand zurück und verwirft damit die eingebaute Zeile aus Schritt 0 **und** jede Änderung, die Claude in der Demo gemacht hat:

```bash
# from the repo root:
git checkout -- workshop-playground/requirements.txt

# verify the planted line is gone (expect 0):
grep -c "requests==2.5.0" workshop-playground/requirements.txt
```

> **⚠️ Führe `pip install` nie auf der eingebauten Zeile aus.** Die ganze Demo ist Scan, Fix und PR; die verwundbare Version darf auf keinem Rechner installiert werden. Hast du Claudes Fix in der Demo auf einen Branch committet, verwirf auch diesen Branch, damit der Playground sauber bleibt.

Der Revert hält den Playground für spätere Sessions im gewünschten Zustand und verhindert, dass jemand versehentlich eine bekannt verwundbare Bibliothek installiert.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 5 Minuten (Schritt 1: 3 Min., Schritt 2: 1 Min.).

**Sagen:**

- Schritt 2: „Von ‚da ist eine CVE' bis ‚hier ist ein PR mit Tests' in wenigen Minuten. Das ist Schwachstellen-Management in Maschinengeschwindigkeit."
- Zum Schluss: „In eurer Welt heißt eine Schwachstelle in der Firmware eines Türcontrollers: Advisory finden, betroffene Geräte bestimmen, den Update-Weg planen, auf dem Prüfstand testen, ausrollen, prüfen. Hier ist es derselbe Ablauf, nur macht Claude die Schritte 1 bis 5 automatisch. Ihr prüft und gebt frei."

**Wenn etwas schiefgeht:**

- **WebSearch ist blockiert (Firmen-Proxy, kein Internet):** Überspring die Live-Suche und füg eine vorbereitete CVE-Beschreibung ein, etwa den NVD-Eintrag zu CVE-2018-18074 aus der Zwischenablage.
- **Du vergisst das Aufräumen:** Das ist das größte Risiko dieser Demo. Setz dir eine Kalender-Erinnerung für das Aufräumen nach dem Workshop.
- **`gh pr create` scheitert:** Zeig es über `git push` und einen PR von Hand im Browser. Oder lass den PR ganz weg und zeig nur Diff und Commit.
- **`pip install` läuft doch auf der verwundbaren Version:** Sofort anhalten, `pip uninstall requests` ausführen und eine sichere Version installieren. Die Demo soll nur Scan und Fix zeigen, nie die CVE installieren.

</details>
