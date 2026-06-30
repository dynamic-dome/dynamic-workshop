# Codex Brief: HTML-Integration sectionContent.json → cloud-code-workshop-ui.html

*Erstellt: 2026-06-30 | Phase 2 des UI-Overhaul*

---

## Kontext

Ein Claude-Workflow hat aus den echten Modul-Markdown-Dateien section-spezifischen Inhalt
für alle 65 Workshop-Sections destilliert und in `resources/sectionContent.json` gespeichert.
Deine Aufgabe ist die mechanische Integration dieser Daten in die HTML-Datei.

---

## Deine Eingabe-Dateien

| Datei | Rolle |
|---|---|
| `resources/sectionContent.json` | Generierter Content (lesen, als const einfügen) |
| `resources/cloud-code-workshop-ui.html` | Ziel-Datei (modifizieren) |

---

## Was du änderst (exakt 3 Eingriffe)

### Eingriff 1 — `sectionContent` + `sectionQuiz` als JS-Konstanten einbauen

**Wo:** Direkt NACH dem schließenden `};` von `const themeCopy = { ... }` (Zeile ~1224).

**Was:** Lese `resources/sectionContent.json`. Die Datei hat diese Struktur:

```json
{
  "meta": { "sections_total": 65 },
  "sectionContent": {
    "S1.1": { "concept": "...", "analogy": "...", "example": "...", "checkpoint": "..." },
    ...
  },
  "sectionQuiz": {
    "S1.1": { "q": "...", "correct": "...", "wrong": ["...", "...", "..."] },
    ...
  }
}
```

Füge nach `const themeCopy = { ... };` ein:

```js
    const sectionContent = /* inhalt von sectionContent.json → .sectionContent */ {
      "S1.1": { concept: "...", analogy: "...", example: "...", checkpoint: "..." },
      // ... alle 65 Einträge
    };

    const sectionQuiz = /* inhalt von sectionContent.json → .sectionQuiz */ {
      "S1.1": { q: "...", correct: "...", wrong: ["...", "...", "..."] },
      // ... alle 65 Einträge
    };
```

**Wichtig:** Kopiere die Daten aus der JSON-Datei als JS-Objekt-Literale (Anführungszeichen
bei Keys weglassen oder lassen — beides valid JS). Keine externe Datei laden, alles inline.

---

### Eingriff 2 — `copyFor()` erweitern mit sectionContent-Fallback

**Wo:** Funktion `copyFor(s)` (aktuell Zeile ~1243).

**Aktuell:**
```js
function copyFor(s) {
  return themeCopy[themeFor(s)] || themeCopy.foundation;
}
```

**Neu:**
```js
function copyFor(s) {
  return sectionContent[s.id] || themeCopy[themeFor(s)] || themeCopy.foundation;
}
```

Das ist die vollständige Änderung an dieser Funktion. sectionContent hat Vorrang vor
den generischen Templates, fällt aber auf themeCopy zurück, wenn eine Section fehlt.

---

### Eingriff 3 — `renderCumulativeQuiz()` auf echte Quiz-Fragen umstellen

**Wo:** Funktion `renderCumulativeQuiz(s)` (aktuell Zeile ~1389).

**Aktuell (relevante Zeilen):**
```js
const correct = copyFor(q).checkpoint;
const options = shuffle([
  correct,
  "Mehr Autonomie ist immer besser, solange die Aufgabe klar formuliert ist.",
  "Wenn ein Tool geladen ist, kann man auf explizite Verifikation verzichten.",
  "Die beste Loesung ist, alle Konfigurationen erst am Ende der Session zu pruefen."
]);
$("quizQuestion").textContent = `Bis ${s.id}: Welche Aussage passt zu ${q.id} (${q.title})?`;
```

**Neu (exakter Ersatz dieser 3 Blöcke):**
```js
const qz = sectionQuiz[q.id];
const correct = qz ? qz.correct : copyFor(q).checkpoint;
const wrongOpts = qz
  ? qz.wrong
  : [
      "Mehr Autonomie ist immer besser, solange die Aufgabe klar formuliert ist.",
      "Wenn ein Tool geladen ist, kann man auf explizite Verifikation verzichten.",
      "Die beste Loesung ist, alle Konfigurationen erst am Ende der Session zu pruefen."
    ];
const options = shuffle([correct, ...wrongOpts]);
$("quizQuestion").textContent = qz
  ? `Bis ${s.id}: ${qz.q}`
  : `Bis ${s.id}: Welche Aussage passt zu ${q.id} (${q.title})?`;
```

Der Rest der Funktion bleibt unverändert.

---

## Was du NICHT änderst

- Das 3-Panel-Layout und alle CSS/Styles
- Die `sections`-Array-Definition
- Die `themeCopy`-Definition (bleibt als Fallback erhalten)
- Die `themeFor()`-Funktion
- Die `keywordBank` und `keywordsFor()`-Funktion
- Die `renderFinalQuiz()`-Funktion (Final-Quiz bleibt theme-basiert)
- Die `slidesFor()`-Funktion (nutzt jetzt automatisch sectionContent via copyFor)
- Die `gradeExercise()`-Funktion
- localStorage-Persistenz
- Route-Toggle-Logik (48/65)
- Die kleinen Wins aus 2026-06-29 (Resource-Links, Keyboard-Shortcuts, Reset-Button)

---

## Verifikation (führe diese Checks aus)

1. **Syntax-Check:** Öffne die HTML-Datei in einem Browser (kein Server nötig). Öffne DevTools → Console. Keine Fehler beim Laden.

2. **Content-Check:** Klicke S1.1. Das `concept`-Feld darf NICHT mehr "Claude Code wird als aktiver Entwicklungsagent verstanden..." zeigen (das war der generische Template-Text). Es muss section-spezifischen Inhalt zeigen.

3. **Quiz-Check:** Klicke S1.3. Das Quiz-Panel zeigt eine Frage — sie soll sich auf den Inhalt von S1.3 beziehen, nicht auf den generischen Checkpoint.

4. **Fallback-Check:** Wenn `sectionContent["S1.1"]` undefined wäre (Testfall: kommentiere einen Eintrag kurz aus), darf die Seite nicht abstürzen — `copyFor()` fällt auf `themeCopy` zurück.

5. **Zeilenanzahl:** Die modifizierte HTML-Datei soll 2500–3500 Zeilen haben (von ~1560 vorher). Wenn sie kleiner als 2000 ist, fehlt Content.

---

## Commit-Message (nach erfolgreichem Verify)

```
feat(ui): integrate section-specific content into workshop UI

- sectionContent (65 entries) replaces generic themeCopy lookup
- sectionQuiz (65 entries) powers cumulative quiz with real questions
- copyFor() falls back to themeCopy if sectionContent entry is missing
- renderCumulativeQuiz() uses sectionQuiz.q/.correct/.wrong
```
