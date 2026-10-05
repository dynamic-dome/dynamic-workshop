# Vorführen: S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben

> Demo und Hinweise für Moderierende zum Kapitel [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](../../library/s2-18-rag-und-notebooklm.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: eine Wissensbasis mit Quellenangabe

**Ziel:** Zeigen, dass Claude Fragen aus einer bestimmten, nachprüfbaren Wissensquelle beantworten kann statt aus Trainingswissen, und dass es bei einer Frage ohne Quelle trotzdem raten kann.

Zeig die Übung aus dem Kapitel live: die Übung „eine Wissensbasis aus Dateien, mit Quellenangabe“ in [S2.18](../../library/s2-18-rag-und-notebooklm.md). Startzustand wie dort: der Ordner `~/cc-workshop/wissen` mit den drei Dateien in `kb/` (Schritt 1). Leg sie vorher an. Du brauchst kein Konto und kein Zusatzprogramm; das Gerät „OL-9“ in den Quellen ist erfunden, Claude kann nichts davon aus dem Training wissen. Starte mit `claude --permission-mode default`.

**Ablauf:** Schritte 2 bis 6 der Übung: dieselbe Frage zuerst ohne und dann mit den Quellen, die Frage am Rand der Quellen, die Frage, die sie sicher nicht abdecken, und der Gegencheck der Fundstelle im Editor. Der NotebookLM-Weg ist die Extra-Übung des Kapitels („dasselbe mit NotebookLM“); zeig sie nur, wenn du Notebook und Anmeldung vor der Session vorbereitet hast (Anlegen und Indexieren dauern ein paar Minuten).

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 8 bis 10 Minuten.

**Einstieg:** „RAG heißt: Claude liest deine Quellen, bevor es antwortet. Die Quellen kommen hier aus Dateien; wichtig, wenn Daten zu einem gehosteten Dienst gehen: Das steht in [S2.19](../../library/s2-19-rag-grenzen.md)."

**Sagen:**

- Schritt 2: „Claudes Trainingsdaten haben einen Stichtag. Das Gerät kennt Claude nicht. Seht, was es ohne Quellen macht: einräumen oder allgemein raten."
- Schritt 3: „Gleiche Frage, andere Qualität. Claude liest in `kb`, antwortet konkret und nennt die Datei und die Zeile." Du kannst jede Aussage an der Stelle nachprüfen. Das senkt das Risiko von Halluzinationen, schließt sie aber nicht aus.
- Schritt 4: „Zur `0` steht nichts in den Quellen. Eine gute Antwort sagt das."
- Schritt 5: „Eine Frage, die sicher nicht drinsteht. Nennt Claude trotzdem eine Zahl, haben wir einen Fall mit Zuversicht ohne Beleg." Schreib auf, was passiert; beide Ausgänge sind brauchbar.
- Schritt 6: Öffne `kb/ol9-errors.md` und vergleich die zitierte Zeile mit der Antwort. „Auch eine Wissensbasis weiß nicht alles: Die Antwort ist nur so gut wie die Quellen und eure Prüfung."
- Abschluss: „Das Muster, das trägt: herausfinden, was Claude wissen muss und nicht aus dem Training kennt, die Quellen dafür bereitstellen und Claude anweisen, dort zuerst nachzusehen." Das geht mit der Extra-Übung auch per `CLAUDE.md`.
- „Einsatzfälle: interne Doku, aktuelle API-Doku, Compliance-Texte, das gesammelte Wissen eures Teams."

**Wenn du NotebookLM zeigst:** Es braucht die inoffizielle Kommandozeile `notebooklm`, installiert und angemeldet wie in der Extra-Übung, und ein Google-Konto. Die Daten gehen zu Google; für sensibles Material gibt es lokale Alternativen ([S2.19](../../library/s2-19-rag-grenzen.md)). Unter Windows hängst du an Befehle mit Ausgabe `--json`, weil die normale Ausgabe dort zerschossen sein kann. Die Antwort kommt mit Zitaten auf Stellen der Quelle; stell dieselbe Frage in einer Sitzung ohne Notebook und vergleich beide.

**Wenn NotebookLM nicht eingerichtet ist:** Bleib bei den Dateien aus der Übung. Sie zeigen dasselbe Prinzip ohne Konto.

</details>
