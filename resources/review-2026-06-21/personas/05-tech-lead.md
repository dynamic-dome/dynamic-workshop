# Persona: Dr. Reuter — skeptischer Principal Engineer (Tiefe & Korrektheit)

**Scope:** Gruendliche Durchsicht von resources/modules/block-1-foundations.md, block-2-ecosystem.md, block-3-advanced.md, cheatsheet.md und faq.md. Fokus: Overclaims, unbelegte Zahlen, interne Widersprueche zwischen Dateien (Permission-Modi, Modell-/Effort-/Kostentabellen, Hook-Events, Defaults), fachliche Tiefe fuer erfahrene Entwickler. Sachliche Fehler (accuracy-overclaim) klar getrennt von reiner Aktualitaet (currency, an Currency-Auditoren delegiert).

## Gesamteindruck

Das Material ist fuer einen skeptischen Principal ueberraschend ehrlich: an genau den Stellen, an denen schlechte Schulungen luegen — Devil's-Advocate-False-Positive-Rate, Self-Improve-Loop-Wirksamkeit, Sandbox-84%-Zahl, Effort-Multiplikatoren — stehen explizite Disclaimer ("vendor figure, not an independent benchmark", "anecdotal, not published benchmark data", "not officially published as exact ratios"). Das ist die richtige intellektuelle Haltung und der groesste Pluspunkt. Die fachliche Tiefe ist fuer erfahrene Entwickler ueberwiegend angemessen, stellenweise (Hooks, MCP-Protokolldetails, CI-Auth) sogar exzellent. ABER: es gibt mehrere harte interne Widersprueche zwischen den Dateien, die ein aufmerksamer Teilnehmer sofort findet und die die Glaubwuerdigkeit untergraben — allen voran ein direkter Default-Widerspruch bei worktree.baseRef (Block 1 sagt "head ist default", Block 3 sagt "fresh ist default"). Dazu kommen ein paar Zahlen-Inkonsistenzen (Effort-Cost max: 6x vs. 5-10x) und ein strukturell-irrefuehrender Ueberschrift-Bug ("The Three Interfaces" ueber fuenf Surfaces). Die Einstiegshuerde fuer das skeptische Profil ist niedrig, weil die Quellenhaltung Vertrauen schafft; die Widersprueche sind aber Sand im Getriebe und gehoeren vor Session 2/3 bereinigt. Mehrere "Features" sind nicht als offiziell verifizierbar belegt (z.B. zahlreiche sehr spezifische Versionsnummern, claude project purge "(when available)"), was im currency-Bereich vertieft gehoert.

## Staerken (was bleiben soll)

- **Intellektuelle Ehrlichkeit bei Zahlen** — Die kritischsten Claims sind explizit gehedged statt verkauft. Block 3 zur Devil's-Advocate-Rate: "Traditional security tooling commonly reports 30-50% false positive rates ... We have not benchmarked it against a labeled dataset. Treat it as 'a useful adversarial filter, not a guaranteed false-positive eliminator.'" (block-3, ~Z496-502). Self-Improve: "this is anecdotal, not published benchmark data" (~Z950-955). Sandbox-84%: "note this is a vendor figure, not an independent benchmark" (block-3 Z710, ebenso cheatsheet Z401). Genau das, was ein Skeptiker sehen will.
- **Effort-Multiplikatoren ehrlich als Schaetzung markiert** — block-1 Z1011: "The relative cost numbers below are approximate (effort-multipliers are not officially published as exact ratios) but the order-of-magnitude is real". Kein Pseudo-Praezisions-Theater.
- **Data-Flow-Transparenz Multi-Provider** — block-3 Z364 trennt sauber: "A Codex Swarm sends your source code to OpenAI, not Anthropic. Anthropic's data policies ... cover only the Claude side". Fuer das sicherheitskritische Publikum exakt die richtige Granularitaet, inkl. drei konkreter Mitigationen (skip/local-model/strip).
- **Hooks- und CI-Tiefe** — Modul 2.2 (updatedToolOutput/continueOnBlock/terminalSequence, prompt/agent/mcp_tool execution types, if-Filter mit permission-rule-Syntax) und Modul 3.6 (setup-token, --bare, Bedrock/Vertex/Proxy fuer airgapped Runner, OIDC-Kurzlebigkeit) sind echt auf Principal-Niveau und nicht nur Folien-Wissen.
- **Saubere Caveat-Kultur bei Hard-Limits** — Hooks werden korrekt als "best-effort ... not a hard security boundary" eingeordnet (block-2 Z525), allowed-tools als "Intent scoping (not a hard security boundary!)" (block-2 Z361). Das verhindert die haeufigste gefaehrliche Fehlannahme.

## Befunde

### [high | accuracy-overclaim | S] Direkter Default-Widerspruch: worktree.baseRef "head" vs. "fresh"

- **Datei:** resources/modules/block-1-foundations.md + block-3-advanced.md
- **Evidenz:** block-1 Z865-866: "`worktree.baseRef: \"head\"` (default) — branch from local HEAD, including unpushed work". block-3 Z1086-1087: "| **`fresh`** (default) | Branches from `origin/<default>` ...". cheatsheet Z428 nennt keinen Default, listet beide. Zwei Module behaupten gegensaetzliche Defaults fuer dieselbe Einstellung.
- **Empfehlung:** Einen Default verifizieren (Doku/echtes settings.json-Verhalten) und beide Stellen + Cheatsheet angleichen. Bis zur Verifikation lieber "Default variiert je Version, explizit setzen" schreiben als eine falsche Behauptung. Ein Teilnehmer, der baseRef setzt, baut sonst auf der falschen Annahme.

### [medium | structure | S] Irrefuehrende Ueberschrift: "The Three Interfaces" listet fuenf Surfaces

- **Datei:** resources/modules/block-1-foundations.md
- **Evidenz:** Lernziel Z12 nennt korrekt fuenf: "(CLI, Desktop App, IDE Extension, Web App, iOS App)". Direkt darunter Z22 Ueberschrift "### The Three Interfaces", gefolgt von nummerierten Eintraegen 1-5 (Z24 bis Z56) UND der Security-Analogie, die ebenfalls vier Modi beschreibt. Die Zahl im Header stimmt mit keinem der Inhalte ueberein.
- **Empfehlung:** Header auf "The Five Surfaces" (konsistent mit Lernziel und CLAUDE.md "Einstieg immer visuell") aendern. Reine Redaktion, aber ein Skeptiker stolpert sofort und fragt sich, ob der Rest auch nicht gegengelesen wurde.

### [medium | accuracy-overclaim | S] acceptEdits-Beschreibung widerspricht sich zwischen Block 1 und Block 3 (ohne Vorwarnung in Block 1)

- **Datei:** resources/modules/block-1-foundations.md + block-3-advanced.md
- **Evidenz:** block-1 Z188 Tabelle: "acceptEdits | Reads + file edits allowed, bash still asks". block-3 Z582-583 korrigiert das selbst: "The Block 1 table summarizes acceptEdits as 'reads + file edits allowed, bash still asks.' That is the conservative version of the truth. In current Claude Code releases, acceptEdits also auto-approves the common filesystem Bash commands ... (mkdir, touch, rm, mv ...)". Sicherheitsrelevant: ein Teilnehmer, der nur Block 1 liest, glaubt rm werde unter acceptEdits abgefragt — es wird auto-approved.
- **Empfehlung:** In Block 1 Z188 eine Fussnote/Klammer ergaenzen: "(vereinfacht; auto-approved auch FS-Bash wie rm/mv im Workdir — Detail in Modul 3.3)". Das cheatsheet (Z356) hat die korrekte Langform bereits, nur Block 1 selbst hinkt nach.

### [medium | accuracy-overclaim | M] Unbelegte/nicht verifizierbare Hyper-Praezision bei Versionsnummern und Feature-Existenz

- **Datei:** resources/modules/block-2-ecosystem.md + block-3-advanced.md + cheatsheet.md
- **Evidenz:** Sehr viele extrem spezifische Versions-Gates (z.B. block-2 Z589 "updatedToolOutput (v2.1.119+)", Z607 "continueOnBlock (v2.1.121+)", Z624 "terminalSequence (v2.1.139+)", block-2 Z312 "Since v2.1.59 this Auto-Memory feature is default on") ohne Quelle. Daneben Hedges, die Unsicherheit verraten: block-1 Z347 "claude project purge <path> (when available)" und cheatsheet Z123 "claude auto-mode defaults". Die Mischung aus Schein-Praezision und "(when available)" ist genau das Muster, das ein Skeptiker als Folien-Wissen markiert.
- **Empfehlung:** Inhaltlich an die Currency-Auditoren delegieren (Verifikation gegen Changelog), aber methodisch: entweder jede Versionsnummer ist belegbar, oder sie wird durch "recent versions"/"2026er Releases" ersetzt. "(when available)" neben einem konkreten Befehl ist ein Widerspruch in sich — Befehl als geplant kennzeichnen oder weglassen.

### [medium | accuracy-overclaim | M] "context: fork / agent" (Block 2) vs. "context: fork + agent" Felder — Frontmatter-Feldnamen-Drift

- **Datei:** resources/modules/block-2-ecosystem.md + cheatsheet.md
- **Evidenz:** block-2 Z352-354 nutzt Felder "context: fork" und "agent: sonnet". Die offizielle Schema-Tabelle desselben Moduls (Z88-97) listet diese Felder NICHT (dort nur model/effort/paths/shell/hooks/arguments). cheatsheet Z519-521 fuehrt "context: fork", "agent: haiku" UND "model: haiku|sonnet|opus" parallel — also zwei Felder (agent + model) fuer scheinbar denselben Zweck (Modellwahl der Forked-Context). Unklar, ob "agent" und "model" beide gueltig sind oder eines veraltet ist.
- **Empfehlung:** Klaeren und vereinheitlichen, welches Feld die Subagent-Modellwahl steuert (model vs. agent) und ob context:fork offiziell ist. Das ist fuer erfahrene Entwickler, die selbst Skills schreiben wollen, ein echtes Stolperfeld — widerspruechliche Frontmatter-Felder fuehren zu stillem Ladeverhalten.

### [low | accuracy-overclaim | S] Zahlen-Inkonsistenz: max-Effort-Kosten 6x (Modul 1.5) vs. 5-10x (FAQ)

- **Datei:** resources/modules/block-1-foundations.md + faq.md
- **Evidenz:** block-1 Z1019: "| `max` | ... | 6x |" (Relative cost). faq.md Z201: "`max` kann 5-10x so lange brauchen wie `medium`". Die FAQ vermischt zudem Kosten- und Latenz-Faktor in einer Zahl, das Modul trennt sie.
- **Empfehlung:** Da die Multiplikatoren ohnehin als unbelegt markiert sind (gut), die FAQ an die Modul-Tabelle koppeln oder explizit "Latenz, nicht Kosten" schreiben und auf Modul 1.5 als Single Source verweisen. Eine einzige Quelle fuer alle Multiplikatoren.

### [low | accuracy-overclaim | S] Sandbox-Tabelle Windows: "first-class shell path" vs. cheatsheet "(limited)" — uneinheitliche Aussage

- **Datei:** resources/modules/block-3-advanced.md + cheatsheet.md
- **Evidenz:** block-3 Z708: Windows PowerShell "Not a kernel sandbox, but a first-class shell path rather than a fallback." cheatsheet Z397: "Windows | (limited) | Relies on permission system". Beide sagen technisch dasselbe (kein Kernel-Sandbox), aber der Ton ist gegensaetzlich ("first-class" vs. "limited"), was die Frage aufwirft, was nun gilt.
- **Empfehlung:** Eine konsistente Formulierung waehlen: faktisch ist es kein OS-Sandbox auf Windows. "first-class shell path, aber KEIN Kernel-Sandbox (anders als Seatbelt/bwrap)" in beide Dateien. Den Marketing-Ton ("first-class") nicht ohne die Einschraenkung stehen lassen.

### [low | accuracy-overclaim | S] Hook-Event-Anzahl uneinheitlich: "28 lifecycle events" vs. "~28"

- **Datei:** resources/modules/block-2-ecosystem.md + cheatsheet.md
- **Evidenz:** block-2 Z387: "The official docs currently list **28 lifecycle events**." (harte Zahl). cheatsheet Z456: "Full list with ~28 events" (ungefaehr). Die Modul-Aussage gibt exakte 28 vor, der Cheatsheet relativiert. Bei einer harten Zahl wuerde ein Skeptiker nachzaehlen.
- **Empfehlung:** Konsistent "~28" verwenden (sicherer) ODER die exakte Liste hinterlegen und 28 belegen. Da der Cheatsheet 17 Kern + 16 weitere namentlich nennt (Z456), kurz pruefen, ob die Summe wirklich 28 ergibt — die genannte Liste wirkt eher nach >28.

### [low | accuracy-overclaim | S] "reduces ... to 0 Tage" ZDR vs. "some features disabled" — korrekt, aber Trade-off in FAQ unterschlagen

- **Datei:** resources/faq.md + block-3-advanced.md
- **Evidenz:** block-3 Z737 + cheatsheet Z679 nennen korrekt "Zero Data Retention (some features disabled)". faq.md Z36 sagt nur: "ZDR ... reduziert Retention auf 0 Tage." — ohne den Feature-Verlust zu erwaehnen. Fuer eine Compliance-Frage ist das Weglassen des Trade-offs irrefuehrend (ein Entscheider koennte ZDR waehlen und ueberrascht sein, dass Features fehlen).
- **Empfehlung:** FAQ-Antwort um den Halbsatz "(einige Features deaktiviert)" ergaenzen, konsistent zu Modul 3.3/Cheatsheet.

### [low | accuracy-overclaim | S] FAQ-Modellpipeline-Beispiel technisch fragwuerdig (/batch mit Sonnet "reviewn" via Haiku)

- **Datei:** resources/faq.md
- **Evidenz:** faq.md Z26: "Pipeline-Pattern: `/plan` mit Opus, `/batch` von Subagents mit Sonnet, `/review` mit Haiku." — Das suggeriert, /review nutze pauschal Haiku, waehrend Modul 3.2 Z356 differenzierter sagt: "Review with Haiku first, escalate disagreements to Opus". Die FAQ-Verkuerzung verliert die Eskalationsstufe, die genau das Qualitaetsargument ist.
- **Empfehlung:** FAQ-Zeile um "...mit Haiku (Eskalation strittiger Punkte an Opus)" ergaenzen, damit die FAQ nicht die schwaechere Aussage als Faustregel etabliert.

### [low | missing-content | M] Tiefe stellenweise zu duenn fuer "erfahrene Entwickler": auto-Mode-Klassifikator bleibt Blackbox

- **Datei:** resources/modules/block-3-advanced.md
- **Evidenz:** block-3 Z572 beschreibt auto als "the ML-classifier-driven mode where Claude itself decides which actions to auto-approve based on per-action risk". Fuer ein Publikum, das beruflich Risikoklassifikation betreibt, bleibt voellig offen, WORAUF der Klassifikator entscheidet (Tool-Kategorie? Befehls-Pattern? lokales vs. Netz?). cheatsheet Z123 nennt immerhin "claude auto-mode defaults" zum Ausdrucken — das Modul verweist nicht darauf.
- **Empfehlung:** Einen Absatz ergaenzen, der die beobachtbaren Klassifikator-Inputs nennt (oder ehrlich sagt: "undokumentiert, inspizierbar via `claude auto-mode defaults`") und auf den Cheatsheet-Befehl verweist. Sonst wirkt auto wie Magie statt wie Policy.

### [low | accuracy-overclaim | S] "Anthropic's official answer to the Devil's-Advocate-Swarm pattern" — Overclaim ueber /ultrareview

- **Datei:** resources/modules/block-3-advanced.md
- **Evidenz:** block-3 Z644: "/ultrareview ... Anthropic's official answer to the Devil's-Advocate-Swarm pattern." Das ist eine interpretierende Behauptung ueber Anthropics Absicht/Positionierung, nicht eine belegbare Tatsache. Anthropic hat /ultrareview nicht zwingend als Antwort auf ein Custom-Plugin dieses Workshops positioniert.
- **Empfehlung:** Umformulieren zu einer Funktionsaussage ohne Intentions-Zuschreibung: "/ultrareview deckt funktional einen aehnlichen Mehr-Reviewer-Konsens-Ansatz ab, ohne Custom-Plugin." Vermeidet eine nicht belegbare Behauptung ueber Hersteller-Strategie.
