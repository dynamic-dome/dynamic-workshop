# Brief: Große UI-Überarbeitung — cloud-code-workshop-ui.html

*Erstellt: 2026-06-29 | Status: Bereit für nächste Session*

## Problem

Die aktuelle `cloud-code-workshop-ui.html` ist ein gut gebauter Shell mit solidem UX-Gerüst,
aber **generischem Content**: Alle 65 Sections teilen sich 14 Themen-Templates.
Das bedeutet — S2.6 (Hooks Grundlagen) und S2.10 (Advanced Hook-Outputs) zeigen denselben
Konzepttext, dieselbe Analogie, dasselbe Beispiel. Die UI ist schön, aber leer.

## Ziel

Jede Section bekommt **eigenen, aus den echten Modul-Dateien destillierten Inhalt**:
konkrete Bullets, relevante Demo-Referenzen, eine echte Quiz-Frage — kein generisches Template.

---

## Was in der letzten Session (2026-06-29) als kleine Wins erledigt wurde

- ↗ Ressource-Links (Modul / Demo / Exercise) pro Section im Header
- ⌨ Keyboard-Shortcuts: `←` `→` navigieren, `m` erledigt markieren
- 🔍 Exercise-Feedback zeigt jetzt welche Keywords gefunden vs. welche fehlen
- 🔄 "Fortschritt zurücksetzen"-Button in der Progress-Karte

---

## Scope der großen Überarbeitung

### 1. Section-spezifischer Inhalt (Kernaufgabe, ~60–70% Aufwand)

Für jede der 65 Sections (Prio: 48 in der Hauptroute) brauchen wir:

| Feld | Heute | Ziel |
|------|-------|------|
| `concept` | 1 generischer Template-Satz | 2–3 Bullets aus dem echten Modul-Abschnitt |
| `analogy` | 1 generischer Security-Vergleich | Konkreter auf den Section-Inhalt zugeschnitten |
| `example` | 1 generischer Befehl | Echter Befehl / Code-Snippet aus Demo-Datei |
| `checkpoint` | 1 generischer Prüfsatz | Direkt aus dem Modul destilliert |
| `slides` | 2 generische Folien | 2–3 Folien mit echten Bullets aus dem Modul |

**Vorgehen:**
1. Modul-Dateien (block-1/2/3-foundations/ecosystem/advanced.md) als Input lesen
2. Pro Section die relevanten Absätze extrahieren (anhand der `source`-Referenz im sections-Array)
3. Destilliert als JS-Objekt in die HTML einbauen — das `themeCopy`-Objekt wird durch ein
   `sectionContent`-Objekt mit 65 Einträgen ersetzt

**Machbar per Workflow:** Fan-out über alle 65 Sections, je 1 Subagent liest die Modul-Quelle
und schreibt den destillierten Eintrag. Parallel-Batches à 10–15 Sections.

### 2. Echte Quiz-Fragen (mittel, ~20% Aufwand)

Das kumulative Quiz fragt aktuell nach der Checkpoint-Aussage (Multiple Choice aus 4 Optionen,
davon 3 hardgecodete Platzhalter). Das finale Quiz fragt "Ordne Section zur Themenfamilie".

**Ziel:** Pro Section 1 echte Multiple-Choice-Frage mit 3 plausiblen Distraktoren.
Distraktoren aus benachbarten Sections oder verwandten Konzepten generieren.

Format in der HTML: neues `sectionQuiz`-Objekt:
```js
const sectionQuiz = {
  "S1.1": {
    q: "Was unterscheidet Claude Code von einem Chat-Assistenten?",
    correct: "Er liest, schreibt und führt aus — im Rahmen expliziter Freigaben.",
    wrong: [
      "Er antwortet schneller auf kurze Fragen.",
      "Er kann keine Dateien lesen.",
      "Er benötigt kein Kontextfenster."
    ]
  },
  // ... 64 weitere
}
```

### 3. Folie 1 mit echten Lernzielen (klein, ~10% Aufwand)

Aktuell zeigt Folie 1 immer denselben Template-Text. Mit `sectionContent` kann jede
Section 3 echte Bullet-Lernziele bekommen, die aus dem Modul stammen.

---

## Technische Hinweise für die nächste Session

- **Source-Mapping:** Das `source`-Feld in den sections (z.B. `"1.1 Overview + Consultant-Analogie"`)
  mappt auf echte Überschriften in `resources/modules/block-1-foundations.md`.
  Die Modul-Dateien sind strukturiert als `## 1.1 ...`, `### Demo 1.1` etc.

- **Datenstruktur:** `themeCopy` (14 Einträge) → ersetzen durch `sectionContent` (65 Einträge).
  `themeFor(s)` + `themeCopy[theme]` → einfach `sectionContent[s.id]` mit Fallback auf theme.
  Minimal-invasiv: bestehende Logik bleibt, nur der Lookup ändert sich.

- **Quiz-Struktur:** `renderCumulativeQuiz()` nutzt aktuell `copyFor(q).checkpoint` als korrekte
  Antwort. Mit `sectionQuiz[q.id]` bekommt jede Section eine eigene echte Frage.

- **Dateigröße:** Aktuell 1560 Zeilen. Mit 65 Section-Objekten wächst auf ca. 2500–3000 Zeilen —
  noch vertretbar als Single-File. Bei >4000 Zeilen über externe JSON nachdenken.

- **Konsistenz-Check:** Nach Befüllung prüfen, ob `source`-Referenzen in den Modul-Dateien
  noch existieren (grep auf `## 1.1` etc.). Modul-Dateien dürfen während der Überarbeitung
  nicht umbenannt werden.

---

## Empfohlene Vorgehensweise nächste Session

```
Phase 1 — Destillation (Workflow, fan-out):
  Input:  resources/modules/block-*.md + sections-Array aus der HTML
  Output: sectionContent-Objekt (65 Einträge, JS-Format)
  Agent:  1 Subagent pro 10 Sections, liest Modul-Abschnitt, schreibt Eintrag
  Check:  Alle 65 IDs vorhanden, kein leeres Feld

Phase 2 — Quiz-Generierung (Workflow, fan-out):
  Input:  sectionContent (aus Phase 1) + benachbarte Sections als Distraktor-Pool
  Output: sectionQuiz-Objekt (65 Einträge)
  Check:  Distraktoren plausibel aber falsch, Antwort eindeutig korrekt

Phase 3 — Integration + Test:
  themeCopy-Lookup durch sectionContent-Lookup ersetzen
  sectionQuiz in renderCumulativeQuiz() einhängen
  Browser-Test: 5 Sections manuell durchklicken, Quiz ausfüllen
```

---

## Was NICHT geändert werden soll

- Das 3-Panel-Layout (funktioniert gut)
- Die localStorage-Persistenz (funktioniert)
- Die Route-Toggle 48/65 (funktioniert)
- Die Fortschrittsanzeige (Ring, Map, Session-Balken)
- Die kleinen Wins aus 2026-06-29 (Links, Keyboard, Feedback, Reset)
