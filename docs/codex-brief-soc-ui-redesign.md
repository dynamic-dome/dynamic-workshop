# Codex Brief: SOC Command — Tactical Edition UI Redesign

*Erstellt: 2026-06-30 | Basis: Multi-Agent Design-Ideation (13 Agenten, 92% Confidence)*

---

## Kontext

Die `resources/cloud-code-workshop-ui.html` (Single-File, ~2582 Zeilen) bekommt ein
vollständiges visuelles Redesign. Das Konzept: **Security Operations Center / Military Tactical**.
Zielgruppe sind Physical-Security-Entwickler (Zutrittskontrolle, Alarmanlagen) — das Design
spricht deren Branchensprache.

**Kein Layout-Umbau, kein Feature-Umbau.** Nur CSS + minimale JS-Erweiterungen.
Alle bestehenden IDs, Klassen, Funktionen und localStorage-Daten bleiben erhalten.

---

## Schritt 0: Google Fonts CDN einbauen

**Wo:** Im `<head>`, nach der Zeile mit `<link rel="icon" ...>` (Zeile ~7), VOR dem `<style>`.

**Was einfügen:**
```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## Schritt 1: :root vollständig ersetzen + color-scheme + SOC Status-Bar-CSS

### 1a. :root block ersetzen

**Finde exakt (Zeilen 9–32):**
```css
    :root {
      color-scheme: light;
      --ink: #17202a;
      --muted: #667085;
      --line: #d8dee8;
      --soft-line: #e9edf4;
      --paper: #f6f8fb;
      --panel: #ffffff;
      --panel-2: #f0f4f8;
      --charcoal: #101820;
      --cyan: #1177aa;
      --green: #218b57;
      --amber: #b75e05;
      --red: #b42318;
      --violet: #6840a3;
      --blue-soft: #dff3ff;
      --green-soft: #e5f6ed;
      --amber-soft: #fff1d7;
      --red-soft: #ffe6e2;
      --shadow: 0 16px 40px rgba(16, 24, 32, .10);
      --radius: 8px;
      --mono: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
```

**Ersetze durch:**
```css
    :root {
      color-scheme: dark;

      /* SOC Core Backgrounds */
      --bg:              #0c0f0a;
      --surface:         #111810;
      --surface-hover:   #192218;
      --sidebar:         #0d1510;
      --sidebar-active:  #1a2a1a;
      --charcoal:        #0d1510;

      /* SOC Accents */
      --accent-primary:  #f59e0b;
      --accent-secondary:#22c55e;
      --accent-glow:     rgba(245,158,11,0.20);
      --success-glow:    rgba(34,197,94,0.20);

      /* Session Heatmap Colors */
      --s1-color:        #4f46e5;
      --s2-color:        #7c3aed;
      --s3-color:        #f43f5e;
      --s4-color:        #f59e0b;
      --done-color:      #16a34a;
      --done-glow:       rgba(22,163,74,0.25);
      --active-cell-bg:  #1e1b4b;

      /* Text */
      --ink:             #e8f0d8;
      --muted:           #5a6b50;
      --text-accent:     #f59e0b;

      /* Borders */
      --line:            #1e2a1a;
      --soft-line:       #2a3a2a;
      --border-active:   #f59e0b;
      --border-done:     #16a34a;

      /* Legacy aliases (keep for backward-compat with existing JS/HTML) */
      --paper:           #0c0f0a;
      --panel:           #111810;
      --panel-2:         #192218;
      --cyan:            #f59e0b;
      --green:           #22c55e;
      --amber:           #f59e0b;
      --red:             #dc2626;
      --violet:          #7c3aed;
      --blue-soft:       rgba(79,70,229,0.15);
      --green-soft:      rgba(34,197,94,0.12);
      --amber-soft:      rgba(245,158,11,0.12);
      --red-soft:        rgba(220,38,38,0.12);

      /* Shadow */
      --shadow:          0 4px 24px rgba(0,0,0,0.5);
      --radius:          6px;

      /* Typography */
      --mono:            'JetBrains Mono', 'Fira Code', 'Cascadia Code', ui-monospace, monospace;
      --sans:            'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;

      /* Timing */
      --t-fast:          150ms ease;
      --t-med:           220ms ease-out;
      --t-slow:          400ms ease-out;
    }
```

### 1b. body background + Raster-Lines

**Finde:**
```css
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--paper);
      color: var(--ink);
      font-family: var(--sans);
      letter-spacing: 0;
    }
```

**Ersetze durch:**
```css
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      font-size: 15px;
      line-height: 1.65;
      letter-spacing: 0;
      /* SOC Tactical: subtile horizontale Rasterlinien */
      background-image: linear-gradient(rgba(245,158,11,0.035) 1px, transparent 1px);
      background-size: 100% 80px;
      overflow-x: hidden;
    }

    /* Atmosphärischer Amber-Blob-Drift (Glass Cosmos Steal, amber recolor) */
    body::before {
      content: "";
      position: fixed;
      top: -100px;
      right: -150px;
      width: 600px;
      height: 400px;
      background: #f59e0b;
      opacity: 0.06;
      filter: blur(160px);
      border-radius: 50%;
      pointer-events: none;
      z-index: 0;
      animation: blob-drift 35s linear infinite;
    }
```

### 1c. SOC Status-Bar (neu, ganz oben im Viewport)

**Füge NACH `body { ... }` und NACH `body::before { ... }` (also direkt nach den body-Blöcken) ein:**

```css
    /* SOC Status-Bar */
    .soc-status-bar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 28px;
      background: rgba(13,21,16,0.95);
      border-bottom: 1px solid rgba(245,158,11,0.3);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 200;
      animation: amber-flicker 9s ease-in-out infinite;
      backdrop-filter: blur(8px);
    }

    .soc-status-bar .soc-left,
    .soc-status-bar .soc-right {
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-primary);
    }

    .soc-status-bar .soc-center {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .soc-status-dot {
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent-secondary);
      margin-right: 6px;
      vertical-align: middle;
      animation: dot-pulse 2s ease-in-out infinite;
    }

    /* Shift .app down to make room for status bar */
    .app {
      margin-top: 28px;
    }
```

---

## Schritt 2: Sidebar (`.left`) SOC-Styling

**Finde:**
```css
    .left {
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      background: var(--charcoal);
      color: #edf5f8;
      border-right: 1px solid rgba(255,255,255,.10);
    }
```

**Ersetze durch:**
```css
    .left {
      position: sticky;
      top: 28px;
      height: calc(100vh - 28px);
      overflow: auto;
      background: var(--sidebar);
      color: var(--ink);
      border-right: 1px solid rgba(245,158,11,0.15);
    }
```

**Finde:**
```css
    .brand {
      padding: 18px 18px 16px;
      border-bottom: 1px solid rgba(255,255,255,.10);
    }
```

**Ersetze durch:**
```css
    .brand {
      padding: 18px 18px 16px;
      border-bottom: 1px solid rgba(245,158,11,0.2);
    }
```

**Finde:**
```css
    .mark {
      display: grid;
      width: 34px;
      height: 34px;
      place-items: center;
      border-radius: 8px;
      background: #e8f7ff;
      color: var(--charcoal);
      font-family: var(--mono);
      font-weight: 800;
      font-size: 13px;
    }
```

**Ersetze durch:**
```css
    .mark {
      display: grid;
      width: 34px;
      height: 34px;
      place-items: center;
      border-radius: 6px;
      background: rgba(245,158,11,0.15);
      border: 1px solid rgba(245,158,11,0.4);
      color: var(--accent-primary);
      font-family: var(--mono);
      font-weight: 800;
      font-size: 13px;
    }
```

**Finde:**
```css
    .brand p {
      margin: 0;
      color: #b8c7d2;
      font-size: 12px;
      line-height: 1.45;
    }
```

**Ersetze durch:**
```css
    .brand p {
      margin: 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
```

**Finde:**
```css
    .route-toggle {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      margin: 14px 0 0;
      padding: 4px;
      border: 1px solid rgba(255,255,255,.13);
      border-radius: 8px;
      background: rgba(255,255,255,.05);
    }

    .route-toggle button {
      min-height: 30px;
      border-radius: 6px;
      background: transparent;
      color: #bfd0da;
      font-size: 12px;
      font-weight: 700;
    }

    .route-toggle button.active {
      background: #edf5f8;
      color: var(--charcoal);
    }
```

**Ersetze durch:**
```css
    .route-toggle {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      margin: 14px 0 0;
      padding: 4px;
      border: 1px solid rgba(245,158,11,0.2);
      border-radius: 6px;
      background: rgba(245,158,11,0.05);
    }

    .route-toggle button {
      min-height: 30px;
      border-radius: 4px;
      background: transparent;
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .route-toggle button.active {
      background: rgba(245,158,11,0.2);
      color: var(--accent-primary);
    }
```

**Finde:**
```css
    .side-search {
      width: calc(100% - 28px);
      margin: 14px;
      padding: 10px 11px;
      border: 1px solid rgba(255,255,255,.14);
      border-radius: 8px;
      outline: 0;
      background: rgba(255,255,255,.08);
      color: #fff;
      font-size: 13px;
    }

    .side-search::placeholder { color: #9eb1bd; }
```

**Ersetze durch:**
```css
    .side-search {
      width: calc(100% - 28px);
      margin: 14px;
      padding: 10px 11px;
      border: 1px solid rgba(245,158,11,0.2);
      border-radius: 6px;
      outline: 0;
      background: rgba(0,0,0,0.3);
      color: var(--ink);
      font-size: 13px;
      font-family: var(--mono);
    }

    .side-search::placeholder { color: var(--muted); }
    .side-search:focus { border-color: rgba(245,158,11,0.5); }
```

**Finde:**
```css
    .session-label {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      padding: 9px 8px 7px;
      color: #9eb1bd;
      font-size: 11px;
      font-family: var(--mono);
      text-transform: uppercase;
    }
```

**Ersetze durch:**
```css
    .session-label {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      padding: 9px 8px 7px;
      color: var(--accent-primary);
      font-size: 10px;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      border-left: 2px solid rgba(245,158,11,0.4);
      margin-left: 8px;
    }
```

---

## Schritt 3: Nav-Items (.nav-item) SOC-Styling

**Finde:**
```css
    .nav-item {
      display: grid;
      grid-template-columns: 40px 1fr auto;
      gap: 8px;
      align-items: center;
      width: 100%;
      min-height: 44px;
      margin: 2px 0;
      padding: 8px;
      border-radius: 8px;
      background: transparent;
      color: #dbe7ed;
      text-align: left;
    }

    .nav-item:hover {
      background: rgba(255,255,255,.08);
    }

    .nav-item.active {
      background: #edf5f8;
      color: var(--charcoal);
    }
```

**Ersetze durch:**
```css
    .nav-item {
      display: grid;
      grid-template-columns: 40px 1fr auto;
      gap: 8px;
      align-items: center;
      width: 100%;
      min-height: 44px;
      margin: 2px 0;
      padding: 8px;
      border-radius: 4px;
      background: transparent;
      color: var(--ink);
      text-align: left;
      border-left: 2px solid transparent;
      transition: background var(--t-fast), border-color var(--t-fast);
    }

    .nav-item:hover {
      background: var(--sidebar-active);
      border-left-color: rgba(245,158,11,0.3);
    }

    .nav-item.active {
      background: var(--sidebar-active);
      color: var(--ink);
      border-left-color: var(--accent-primary);
    }
```

**Finde:**
```css
    .nav-id {
      color: inherit;
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 800;
      opacity: .84;
    }
```

**Ersetze durch:**
```css
    .nav-id {
      color: var(--accent-primary);
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.06em;
    }

    .nav-item.active .nav-id {
      color: var(--accent-primary);
    }
```

**Finde:**
```css
    .nav-state {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      border: 1px solid currentColor;
      opacity: .65;
    }

    .nav-item.done .nav-state {
      background: var(--green);
      border-color: var(--green);
      opacity: 1;
    }
```

**Ersetze durch:**
```css
    .nav-state {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      border: 1px solid var(--muted);
      opacity: .6;
    }

    .nav-item.done .nav-state {
      background: var(--accent-secondary);
      border-color: var(--accent-secondary);
      opacity: 1;
      animation: dot-pulse 2s ease-in-out infinite;
    }

    .nav-item.active .nav-state {
      border-color: var(--accent-primary);
      background: rgba(245,158,11,0.2);
      opacity: 1;
    }
```

---

## Schritt 4: Hauptbereich (.main) + Karten (.panel)

**Finde:**
```css
    .main {
      min-width: 0;
      padding: 22px 28px 34px;
      overflow: hidden;
    }
```

**Ersetze durch:**
```css
    .main {
      min-width: 0;
      padding: 22px 28px 34px;
      overflow: hidden;
      position: relative;
    }

    /* Scan-Line Sweep (JS-triggered via .scanning class) */
    .main.scanning::after {
      content: "";
      position: fixed;
      left: 280px;
      right: 330px;
      height: 2px;
      background: var(--accent-primary);
      box-shadow: 0 0 12px var(--accent-primary), 0 0 24px rgba(245,158,11,0.4);
      pointer-events: none;
      z-index: 100;
      animation: scan-line 400ms ease-out forwards;
    }
```

**Finde:**
```css
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: 0 1px 0 rgba(16,24,32,.03);
    }
```

**Ersetze durch:**
```css
    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-left: 2px solid var(--accent-primary);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      animation: card-slide-in var(--t-med) both;
    }

    .panel:nth-child(2) { animation-delay: 60ms; }
    .panel:nth-child(3) { animation-delay: 120ms; }
```

**Finde:**
```css
    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
```

*(Lies die nächste Zeile um Kontext zu haben, dann:)*

Nach dem bestehenden `.panel-head`-Block, füge hinzu:

```css
    .panel-head h3 {
      font-family: var(--mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent-primary);
    }
```

---

## Schritt 5: Topbar + Titel SOC-Styling

**Finde im CSS-Block für `.topbar h2`:**
```css
    .topbar h2 {
      margin: 0;
      font-size: clamp(28px, 4vw, 48px);
      line-height: .96;
      letter-spacing: 0;
      max-width: 980px;
    }
```

**Ersetze durch:**
```css
    .topbar h2 {
      margin: 0;
      font-size: clamp(22px, 3.5vw, 40px);
      line-height: .96;
      letter-spacing: -0.02em;
      max-width: 980px;
      color: var(--ink);
    }
```

**Finde:**
```css
    .source {
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }
```

**Ersetze durch:**
```css
    .source {
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      font-family: var(--mono);
      font-size: 12px;
      letter-spacing: 0.04em;
    }
```

---

## Schritt 6: Pills SOC-Styling

**Finde:**
```css
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 24px;
      padding: 4px 8px;
      border-radius: 999px;
      background: var(--panel);
      border: 1px solid var(--line);
      color: var(--muted);
      font-size: 12px;
      font-weight: 720;
      white-space: nowrap;
    }

    .pill.core { color: var(--green); background: var(--green-soft); border-color: #b7e3c8; }
    .pill.deep-dive { color: var(--cyan); background: var(--blue-soft); border-color: #b8def0; }
    .pill.bonus { color: var(--violet); background: #efe8ff; border-color: #d7c7ff; }
    .pill.corestar { color: var(--amber); background: var(--amber-soft); border-color: #f5d59c; }
```

**Ersetze durch:**
```css
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 22px;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--surface);
      border: 1px solid var(--line);
      color: var(--muted);
      font-size: 11px;
      font-weight: 600;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.07em;
      white-space: nowrap;
    }

    .pill.core { color: var(--accent-secondary); background: var(--green-soft); border-color: rgba(34,197,94,0.3); }
    .pill.deep-dive { color: #60a5fa; background: rgba(96,165,250,0.1); border-color: rgba(96,165,250,0.25); }
    .pill.bonus { color: var(--s2-color); background: rgba(124,58,237,0.1); border-color: rgba(124,58,237,0.25); }
    .pill.corestar { color: var(--accent-primary); background: var(--amber-soft); border-color: rgba(245,158,11,0.3); }
```

---

## Schritt 7: Buttons (.tool-btn) SOC-Styling

**Finde:**
```css
    .tool-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      min-height: 38px;
      padding: 9px 12px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      font-size: 13px;
      font-weight: 760;
      box-shadow: 0 1px 0 rgba(16,24,32,.04);
    }

    .tool-btn:hover {
      border-color: #aeb8c7;
    }

    .tool-btn.primary {
      border-color: var(--charcoal);
      background: var(--charcoal);
      color: #fff;
    }

    .tool-btn.good {
      border-color: #9bd3b5;
      background: var(--green-soft);
      color: var(--green);
    }
```

**Ersetze durch:**
```css
    .tool-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      min-height: 36px;
      padding: 8px 12px;
      border-radius: var(--radius);
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--ink);
      font-size: 12px;
      font-weight: 600;
      font-family: var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      box-shadow: none;
      transition: border-color var(--t-fast), background var(--t-fast);
    }

    .tool-btn:hover {
      border-color: var(--accent-primary);
      background: var(--surface-hover);
    }

    .tool-btn.primary {
      border-color: var(--accent-primary);
      background: rgba(245,158,11,0.15);
      color: var(--accent-primary);
    }

    .tool-btn.good {
      border-color: rgba(34,197,94,0.4);
      background: var(--green-soft);
      color: var(--accent-secondary);
    }
```

---

## Schritt 8: Progress-Ring als Heartbeat (Bioluminescent Steal)

**Finde:**
```css
    .ring {
      width: 92px;
      height: 92px;
      border-radius: 50%;
      background: conic-gradient(var(--green) var(--pct), #d7dee8 0);
      display: grid;
      place-items: center;
      position: relative;
    }

    .ring::after {
      content: "";
      position: absolute;
      inset: 10px;
      border-radius: 50%;
      background: #fff;
    }

    .ring span {
      position: relative;
      z-index: 1;
      font-family: var(--mono);
      font-size: 18px;
      font-weight: 850;
    }
```

**Ersetze durch:**
```css
    .ring {
      width: 92px;
      height: 92px;
      border-radius: 50%;
      background: conic-gradient(var(--accent-primary) var(--pct), #1e2a1a 0);
      display: grid;
      place-items: center;
      position: relative;
      animation: heartbeat 2.8s ease-in-out infinite;
    }

    .ring::after {
      content: "";
      position: absolute;
      inset: 10px;
      border-radius: 50%;
      background: var(--surface);
    }

    .ring span {
      position: relative;
      z-index: 1;
      font-family: var(--mono);
      font-size: 18px;
      font-weight: 700;
      color: var(--accent-primary);
    }
```

---

## Schritt 9: Map-Cells (Heatmap-Farben nach Session)

**Finde:**
```css
    .map-cell:hover { border-color: var(--cyan); color: var(--cyan); }
    .map-cell.active { border-color: var(--charcoal); background: var(--charcoal); color: #fff; }
    .map-cell.done { border-color: #9bd3b5; background: var(--green-soft); color: var(--green); }
    .map-cell.quiz-ok { box-shadow: inset 0 -3px 0 var(--cyan); }
```

**Ersetze durch:**
```css
    .map-cell:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
    .map-cell.active { border-color: var(--active-cell-bg); background: var(--active-cell-bg); color: #fff; box-shadow: 0 0 8px rgba(79,70,229,0.4); }
    .map-cell.done { border-color: var(--done-color); background: var(--green-soft); color: var(--done-color); transform: scale(1.04); }
    .map-cell.quiz-ok { box-shadow: inset 0 -3px 0 var(--accent-primary); }

    /* Session-specific cell colors (session encoded via data-session attr — added in JS) */
    .map-cell[data-session="1"]:not(.done):not(.active) { border-color: rgba(79,70,229,0.35); color: rgba(79,70,229,0.7); }
    .map-cell[data-session="2"]:not(.done):not(.active) { border-color: rgba(124,58,237,0.35); color: rgba(124,58,237,0.7); }
    .map-cell[data-session="3"]:not(.done):not(.active) { border-color: rgba(244,63,94,0.35); color: rgba(244,63,94,0.7); }
    .map-cell[data-session="4"]:not(.done):not(.active) { border-color: rgba(245,158,11,0.35); color: rgba(245,158,11,0.7); }
```

**Finde:**
```css
    .map-cell {
      aspect-ratio: 1;
      border-radius: 5px;
      border: 1px solid #cad3de;
      background: #fff;
      color: var(--muted);
      font-size: 9px;
      font-family: var(--mono);
      display: grid;
      place-items: center;
      cursor: pointer;
    }
```

**Ersetze durch:**
```css
    .map-cell {
      aspect-ratio: 1;
      border-radius: 4px;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--muted);
      font-size: 9px;
      font-family: var(--mono);
      display: grid;
      place-items: center;
      cursor: pointer;
      transition: border-color var(--t-fast), transform var(--t-fast), background var(--t-fast);
    }
```

---

## Schritt 10: Progress-Panel + Stats SOC-Styling

**Finde:**
```css
    .stat {
      padding: 10px;
      border-radius: 8px;
      background: #f8fafc;
      border: 1px solid var(--soft-line);
    }
```

**Ersetze durch:**
```css
    .stat {
      padding: 10px;
      border-radius: 6px;
      background: var(--bg);
      border: 1px solid var(--line);
    }

    .stat strong {
      color: var(--accent-primary);
    }
```

**Finde:**
```css
    .quiz-options button {
      width: 100%;
      padding: 10px;
      border: 1px solid var(--soft-line);
      border-radius: 8px;
      background: #fff;
      color: #344054;
      text-align: left;
      font-size: 13px;
      line-height: 1.35;
    }

    .quiz-options button:hover { border-color: var(--cyan); }
```

**Ersetze durch:**
```css
    .quiz-options button {
      width: 100%;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--bg);
      color: var(--ink);
      text-align: left;
      font-size: 13px;
      line-height: 1.35;
      transition: border-color var(--t-fast);
    }

    .quiz-options button:hover { border-color: var(--accent-primary); }
```

---

## Schritt 11: Alle @keyframes + Animationen einbauen

**Füge VOR dem schließenden `</style>` Tag ein:**

```css
    /* ═══════════════════════════════════════════════
       SOC COMMAND ANIMATIONS
    ═══════════════════════════════════════════════ */

    /* Blob-Drift: atmosphärischer Hintergrund-Layer */
    @keyframes blob-drift {
      0%,100% { transform: translate(0,0) scale(1); }
      33%      { transform: translate(-40px, 30px) scale(1.08); }
      66%      { transform: translate(20px, -50px) scale(0.95); }
    }

    /* Amber-Flicker: Phosphor-Monitor-Simulation */
    @keyframes amber-flicker {
      0%,89%,91%,97%,100% { opacity: 1; }
      90%                  { opacity: 0.65; }
      98%                  { opacity: 0.82; }
    }

    /* Heartbeat: Progress-Ring (Bioluminescent Steal, amber recolor) */
    @keyframes heartbeat {
      0%  { transform: scale(1);    box-shadow: 0 0 0 0    rgba(245,158,11,0.6); }
      14% { transform: scale(1.04); box-shadow: 0 0 0 8px  rgba(245,158,11,0.15); }
      28% { transform: scale(1);    box-shadow: 0 0 0 0    rgba(245,158,11,0); }
      42% { transform: scale(1.02); box-shadow: 0 0 0 5px  rgba(245,158,11,0.10); }
      70%,100% { transform: scale(1); box-shadow: 0 0 0 0  rgba(245,158,11,0); }
    }

    /* Dot-Pulse: Status-LEDs in Nav + Status-Bar */
    @keyframes dot-pulse {
      0%,100% { box-shadow: 0 0 4px rgba(34,197,94,0.4); }
      50%     { box-shadow: 0 0 12px rgba(34,197,94,0.95), 0 0 24px rgba(34,197,94,0.3); }
    }

    /* Scan-Line: Section-Wechsel (JS-triggered via .scanning class) */
    @keyframes scan-line {
      0%   { top: 28px; opacity: 1; }
      100% { top: 100vh; opacity: 0; }
    }

    /* Card-Slide-In: Staggered beim Section-Load */
    @keyframes card-slide-in {
      from { opacity: 0; transform: translateX(-14px); }
      to   { opacity: 1; transform: translateX(0); }
    }

    /* Sector-Flash: Overlay beim Nav-Klick */
    @keyframes sector-flash-in  { from { opacity: 0; } to { opacity: 1; } }
    @keyframes sector-flash-out { from { opacity: 1; } to { opacity: 0; } }

    /* Reduced motion: alle Animationen deaktivieren außer Farbe */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
    }

    /* Sector-Flash Overlay (statisch positioniert, JS steuert opacity) */
    #soc-flash-overlay {
      position: fixed;
      inset: 0;
      z-index: 1000;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
    }

    #soc-flash-overlay span {
      font-family: var(--mono);
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--accent-primary);
      text-shadow: 0 0 20px rgba(245,158,11,0.6);
    }
```

---

## Schritt 12: HTML — SOC Status-Bar + Flash-Overlay einfügen

**Finde im HTML-Body (kurz nach `<body>` oder vor `.app`):**
```html
  <div class="app">
```

**Ersetze durch:**
```html
  <!-- SOC Status Bar -->
  <div class="soc-status-bar" id="socStatusBar">
    <span class="soc-left"><span class="soc-status-dot"></span>SYSTEM ONLINE</span>
    <span class="soc-center">CLAUDE CODE WORKSHOP — DYNAMIC WORKSHOP</span>
    <span class="soc-right" id="socStatusRight">SECTOR T-001 STANDBY</span>
  </div>

  <!-- Sector Flash Overlay -->
  <div id="soc-flash-overlay"><span id="soc-flash-text">ACCESSING SECTOR T-001...</span></div>

  <div class="app">
```

---

## Schritt 13: Map-Cells JS — data-session Attribut hinzufügen

**Finde in `renderMap()` (Zeile ~2469):**
```js
      $("map").innerHTML = route.map(s => `
        <button class="map-cell ${s.id === activeId ? "active" : ""} ${state.done[s.id] ? "done" : ""} ${state.quiz[s.id]?.ok ? "quiz-ok" : ""}" type="button" data-id="${s.id}" title="${s.id}: ${s.title}">
          ${s.id.replace("S","")}
        </button>`).join("");
```

**Ersetze durch:**
```js
      $("map").innerHTML = route.map(s => `
        <button class="map-cell ${s.id === activeId ? "active" : ""} ${state.done[s.id] ? "done" : ""} ${state.quiz[s.id]?.ok ? "quiz-ok" : ""}" type="button" data-id="${s.id}" data-session="${s.session}" title="${s.id}: ${s.title}">
          ${s.id.replace("S","")}
        </button>`).join("");
```

---

## Schritt 14: setActive() — Scan-Line + Sector-Flash JS

**Finde:**
```js
    function setActive(id) {
      activeId = id;
      const route = routeSectionsNoSearch();
      if (!route.some(s => s.id === activeId)) activeId = route[0]?.id || "S1.1";
      renderAll();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
```

**Ersetze durch:**
```js
    function setActive(id) {
      activeId = id;
      const route = routeSectionsNoSearch();
      if (!route.some(s => s.id === activeId)) activeId = route[0]?.id || "S1.1";
      renderAll();
      window.scrollTo({ top: 0, behavior: "smooth" });

      // SOC Tactical: Sector-Flash + Scan-Line + Status-Bar Update
      const secNum = activeId.replace("S","").replace(".", "-");
      const flashOverlay = document.getElementById("soc-flash-overlay");
      const flashText = document.getElementById("soc-flash-text");
      const statusRight = document.getElementById("socStatusRight");
      if (flashOverlay && flashText) {
        flashText.textContent = `ACCESSING SECTOR T-${secNum}...`;
        flashOverlay.style.transition = "opacity 100ms ease";
        flashOverlay.style.opacity = "1";
        setTimeout(() => {
          flashOverlay.style.transition = "opacity 200ms ease";
          flashOverlay.style.opacity = "0";
        }, 400);
      }
      if (statusRight) {
        statusRight.textContent = `SECTOR T-${secNum} ACCESSED • CLEARANCE GRANTED`;
        statusRight.style.animation = "none";
        // Amber blink 3x
        let blinks = 0;
        const blinkInterval = setInterval(() => {
          statusRight.style.opacity = statusRight.style.opacity === "0" ? "1" : "0";
          blinks++;
          if (blinks >= 6) {
            clearInterval(blinkInterval);
            statusRight.style.opacity = "1";
          }
        }, 130);
      }
      // Scan-Line: CSS animation via class toggle
      const mainEl = document.querySelector(".main");
      if (mainEl) {
        mainEl.classList.remove("scanning");
        void mainEl.offsetWidth; // force reflow
        mainEl.classList.add("scanning");
        setTimeout(() => mainEl.classList.remove("scanning"), 450);
      }
    }
```

---

## Schritt 15: Favicon aktualisieren (optisch)

**Finde:**
```html
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23101820'/%3E%3Ctext x='32' y='39' text-anchor='middle' font-family='monospace' font-size='20' font-weight='700' fill='%23edf5f8'%3ECC%3C/text%3E%3C/svg%3E">
```

**Ersetze durch:**
```html
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230c0f0a'/%3E%3Crect width='64' height='64' rx='12' fill='none' stroke='%23f59e0b' stroke-width='3'/%3E%3Ctext x='32' y='39' text-anchor='middle' font-family='monospace' font-size='20' font-weight='700' fill='%23f59e0b'%3ECC%3C/text%3E%3C/svg%3E">
```

---

## Was du NICHT änderst

- Alle JavaScript-Funktionen außer `setActive()` und `renderMap()` (nur additive Änderungen)
- Die `sections`-Array-Definition
- `sectionContent`, `sectionQuiz`, `themeCopy`, alle Copy-Logik
- `renderNav()`, `renderMain()`, `renderProgress()`, `renderSessionBars()`
- localStorage-Persistenz und alle State-Logik
- Route-Toggle-Logik (48/65)
- Die HTML-Struktur der 3 Spalten (`.left`, `.main`, `.right` / `.app`)

---

## Verifikation

1. **Öffne im Browser** via `python -m http.server 8042 --bind 127.0.0.1` → `http://127.0.0.1:8042/cloud-code-workshop-ui.html`
2. **Kein heller Hintergrund** — das Panel soll dunkelgrün-schwarz sein, nicht weiß
3. **Status-Bar oben** — amber Text "SYSTEM ONLINE" sichtbar
4. **Nav-Klick-Test** — Klick auf S1.2: Scan-Line fährt durch, Status-Bar zeigt "SECTOR T-1-2 ACCESSED • CLEARANCE GRANTED", Karten gleiten rein
5. **Progress-Ring** — pulsiert mit Heartbeat-Animation (kein statischer Ring mehr)
6. **Map-Zellen** — haben Session-Farben (Indigo/Violett/Rot/Amber je nach Session)
7. **Keine JS-Errors** in DevTools Console
8. **Alle Features funktionieren** — Done-Toggle, Quiz, Exercise, Route-Toggle, Suche

---

## Commit-Message

```
feat(ui): SOC Command Tactical Edition redesign

- Dark SOC control-room aesthetic (#0c0f0a bg, amber #f59e0b accents)
- Status bar: "SECTOR T-NNN ACCESSED • CLEARANCE GRANTED" on nav click
- Heartbeat progress ring (Bioluminescent steal, amber recolor)
- Sector flash overlay + scan-line sweep on section change
- Session heatmap: S1=Indigo, S2=Violet, S3=Alarm-Red, S4=Amber
- JetBrains Mono for IDs + status codes, Inter for body
- Amber blob-drift background, dot-pulse LEDs, staggered card-slide-in
- prefers-reduced-motion: all animations off, text stays visible
```
