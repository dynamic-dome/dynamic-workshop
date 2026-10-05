# Vorführen: S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben

> Demo und Hinweise für Moderierende zum Kapitel [S2.18 · RAG und NotebookLM: dem Agenten Baupläne geben](../../library/s2-18-rag-und-notebooklm.md). Diese Seite gehört zur Moderationsschicht; wer allein lernt, braucht sie nicht.

### Demo: NotebookLM als Wissensbasis

**Ziel:** Zeigen, dass Claude Fragen aus einer bestimmten, nachprüfbaren Wissensquelle beantworten kann statt aus Trainingswissen, und dass das bei Fachfragen das Risiko von Halluzinationen senkt.

**Vorbereitung**

- Die Kommandozeile `notebooklm` ist installiert und angemeldet; für `/notebooklm …` zusätzlich der Skill der Moderation (`~/.claude/skills/notebooklm/`).
- Ein Notebook mit ein paar Quellen ist schon angelegt. Mach das vor der Session: Anlegen und Indexieren dauern ein paar Minuten.
- Vorschlag: ein Notebook mit der Claude-Code-Doku oder mit eurer eigenen Projektdoku.

**Schritt 1: das Problem erklären**

Erklär, dass Claudes Trainingsdaten einen Stichtag haben und Claude bei neuen APIs, internen Werkzeugen oder Nischenthemen falsch raten kann.

**Schritt 2: den Notebook-Ablauf zeigen**

Zeig das vorbereitete Notebook:

```
notebooklm list --json
```

Oder mit dem Skill:

```
/notebooklm navigate
```

Zeig den Namen des Notebooks und wie viele Quellen es hat.

**Schritt 3: das Notebook abfragen**

In Claude Code:

```
notebooklm use <notebook-id>
notebooklm ask "What is the correct JSON structure for a PreToolUse hook in settings.json?"
```

Sieh dir die Antwort an und zeig darauf:

- Die Antwort enthält **Zitate**: Du siehst, aus welcher Quellseite sie stammt.
- Die Antwort ist konkret, nicht allgemein.
- Du kannst jede Aussage an der zitierten Stelle nachprüfen. Das senkt das Risiko von Halluzinationen, schließt sie aber nicht aus ([S2.19](../../library/s2-19-rag-grenzen.md)).

Frag dann etwas, womit Claude sich sonst schwertut:

```
notebooklm ask "What are the valid matcher patterns for hooks, and what tool names can I match against?"
```

**Schritt 4: der Gegenversuch**

Stell dieselbe Frage OHNE Notebook, in einem frischen Kontext:

```
(new context) What are the valid matcher patterns for hooks in Claude Code settings.json?
```

Claude gibt eine plausibel klingende Antwort, die aber veraltet, unvollständig oder leicht falsch sein kann. Die geprüfte Regel, wann ein Matcher als exakter Name und wann als Regex gilt, steht in [S2.8](../../library/s2-08-hook-einrichten.md); daran kannst du beide Antworten live messen.

<details><summary>Für Moderierende</summary>

**Dauer:** etwa 7 Minuten (Schritt 1: 1 Min., Schritt 2: 2 Min., Schritt 3: 3 Min., Schritt 4: 1 Min.).

**Einstieg:** „RAG heißt: Claude liest deine Doku, bevor es antwortet. Wichtig: Die Daten gehen zu Google. Für sensibles Material gibt es lokale RAG-Alternativen."

**Sagen:**

- Schritt 1: „Claudes Trainingsdaten haben einen Stichtag. Bei neuen APIs, internen Werkzeugen oder Nischenthemen rät Claude vielleicht falsch. Ich zeige euch, wie ihr Claude eine geprüfte Wissensquelle gebt."
- Schritt 2: „Ich habe schon ein Notebook angelegt und Quellen hinzugefügt. So sieht das aus."
- Schritt 3: „Das ist eine genaue, spezifische Frage. Ohne Notebook würde Claude aus allgemeinem Trainingswissen antworten, das falsch sein kann, oder Unsicherheit einräumen. Mit Notebook wird die echte Dokumentation durchsucht, und du bekommst die Antwort mit Zitat."
- Schritt 4: „Gleiche Frage, andere Qualität. Das ist der Unterschied zwischen allgemeinem Sicherheitswissen und euren echten Bauplänen."

**Sprechpunkte:**

- „RAG heißt: Claude bekommt eure echten Baupläne statt allgemeinen Wissens."
- „NotebookLM ist ein gehostetes RAG-System: keine ML-Infrastruktur nötig, es läuft sofort."
- „Die Antworten kommen mit Zitaten: nachprüfbar statt geraten."
- „Einsatzfälle: interne Doku, aktuelle API-Doku, Compliance-Texte, das gesammelte Wissen eures Teams."
- „Das Muster, das trägt: herausfinden, was Claude wissen muss und nicht aus dem Training kennt, ein Notebook dafür bauen und Claude anweisen, dort zuerst nachzusehen."

**Wenn der Skill nicht eingerichtet ist:** Zeig das Prinzip in der Web-Oberfläche.

- Öffne `notebooklm.google.com` (leitet inzwischen auf `notebook.google.com` weiter).
- Zeig ein vorhandenes Notebook mit Quellen.
- Stell eine Frage im Chat der Web-Oberfläche.
- Sag: „Der Skill verpackt dieselbe Schnittstelle, damit ihr aus dem Terminal fragen könnt. In der Übung baut ihr eure eigene Wissensbasis."

**Wenn die Ausgabe unter Windows kaputtgeht:** siehe „Typische Fallen".

</details>
