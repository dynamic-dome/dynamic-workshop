# -*- coding: utf-8 -*-
"""
Render the persona-review workflow output (JSON) into structured markdown artifacts.
Provenance: generated from workflow run wf_1603866b-421 on 2026-06-21.
Run: python resources/review-2026-06-21/_generator.py
"""
import json
import os
import shutil
import io

SRC = r"C:\Users\domes\AppData\Local\Temp\claude\C--Users-domes-Desktop-dynamic-workshop\6faae23a-4514-4469-a97b-f86fdb9d0f01\tasks\w1peni9j0.output"
OUT = r"C:\Users\domes\Desktop\dynamic_workshop\resources\review-2026-06-21"
DATE = "2026-06-21"

PERSONA_IDS = [
    "newcomer", "phys-sec", "moderator", "self-learner", "tech-lead",
    "windows", "exercise-doer",
    "currency-models-pricing", "currency-cli-features", "currency-ecosystem",
]

PRIO_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
EFFORT_ORDER = {"S": 0, "M": 1, "L": 2}
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "nice-to-have": 4}


def writef(relpath, content):
    path = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


def cell(s):
    """Sanitize a value for a markdown table cell."""
    if s is None:
        return ""
    if isinstance(s, (list, tuple)):
        s = "; ".join(str(x) for x in s)
    s = str(s)
    return s.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", "<br>").strip()


def blk(s):
    """Block text (outside tables)."""
    if s is None:
        return ""
    if isinstance(s, (list, tuple)):
        return "\n".join("- " + str(x) for x in s)
    return str(s).strip()


def slug(s):
    out = []
    for ch in str(s).lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
    r = "".join(out)
    while "--" in r:
        r = r.replace("--", "-")
    return r.strip("-")[:48] or "x"


def main():
    with io.open(SRC, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Workflow output is wrapped: {summary, agentCount, logs, result}
    data = raw.get("result", raw) if isinstance(raw, dict) else raw

    counts = data.get("counts", {})
    lens = data.get("lensResults", []) or []
    all_findings = data.get("allFindings", []) or []
    architect = data.get("architect", {}) or {}
    crazy = data.get("crazy", {}) or {}
    clusters = data.get("clusterResults", []) or []
    all_todos = data.get("allTodos", []) or []
    master = data.get("master", {}) or {}

    # ---- data dumps (provenance) ----
    shutil.copyfile(SRC, os.path.join(OUT, "data", "raw-workflow-output.json")
                    if os.path.isdir(os.path.join(OUT, "data")) else _ensure_data())
    writef("data/findings.json", json.dumps(all_findings, ensure_ascii=False, indent=2))
    writef("data/todos.json", json.dumps(all_todos, ensure_ascii=False, indent=2))

    # ---- 00 README / index ----
    idx = []
    idx.append("# Dynamic Workshop — Persona-Review & TODO-Backlog (%s)\n" % DATE)
    idx.append("> Multi-Agent-Review des gesamten Claude-Code-Workshops aus 10 Personas + 2 Design-Rollen.")
    idx.append("> Erzeugt per Workflow-Orchestrierung (Run `wf_1603866b-421`). Dieses Verzeichnis ist die")
    idx.append("> Analyse-Grundlage fuer eine spaetere Umsetzungs-Instanz — es aendert KEINEN Kursinhalt.\n")
    idx.append("## Kennzahlen\n")
    idx.append("| Metrik | Wert |")
    idx.append("|---|---:|")
    idx.append("| Personas / Audit-Rollen | %s |" % counts.get("personas", len(lens)))
    idx.append("| Roh-Befunde | %s |" % counts.get("findings", len(all_findings)))
    idx.append("| Konsolidierte Cluster | %s |" % counts.get("clusters", len(clusters)))
    idx.append("| Atomare TODOs | %s |" % counts.get("todos", len(all_todos)))
    idx.append("| Neue Uebungsideen | %s |" % counts.get("crazyIdeas", len(crazy.get("ideas", []))))
    idx.append("")
    idx.append("## Dateien\n")
    idx.append("| Datei | Inhalt |")
    idx.append("|---|---|")
    idx.append("| `01-executive-summary.md` | Management-Synthese: Gesamturteil, Top-Themen, Quick Wins, Roadmap, Struktur-Empfehlung |")
    idx.append("| `02-todo-backlog.md` | **Das zentrale Liefer-Artefakt** — alle %s TODOs, priorisiert (P0-P3) |" % len(all_todos))
    idx.append("| `03-currency-report.md` | Aktualitaets-Befunde mit Web-Quellen (Modelle, CLI, Ecosystem) |")
    idx.append("| `04-restructuring-proposal.md` | Granularer Neu-Schnitt des Curriculums (Pflichtpfad/Deep-Dive/Bonus) |")
    idx.append("| `05-new-exercises.md` | Neue & 'verrueckte' Uebungs-/Engagement-Formate |")
    idx.append("| `06-all-findings.md` | Anhang: alle %s Roh-Befunde nach Persona |" % len(all_findings))
    idx.append("| `07-curator-addenda.md` | Manuelle Zusatz-Befunde des Orchestrators |")
    idx.append("| `personas/` | Eine Persona-Karte + Report je Persona |")
    idx.append("| `data/` | Maschinenlesbar: findings.json, todos.json, raw-workflow-output.json |")
    idx.append("")
    idx.append("## Methode\n")
    idx.append("Welle 1 (parallel): 7 Lern-/Liefer-Personas spielen den Kurs durch + 3 Currency-Auditoren ")
    idx.append("(Web-Recherche). Welle 2: Curriculum-Architekt + Wild-Exercise-Designer. ")
    idx.append("Welle 3: gruppenweise Konsolidierung je Kategorie -> atomare TODOs. Welle 4: Master-Synthese.\n")
    writef("00-README.md", "\n".join(idx))

    # ---- 01 executive summary ----
    es = []
    es.append("# Executive Summary — Workshop-Review %s\n" % DATE)
    es.append(blk(master.get("executiveSummary")))
    es.append("\n## Top-Themen\n")
    es.append("| Thema | Impact |")
    es.append("|---|---|")
    for t in master.get("topThemes", []) or []:
        es.append("| %s | %s |" % (cell(t.get("theme")), cell(t.get("impact"))))
    es.append("\n## Quick Wins (zuerst angehen)\n")
    for q in master.get("quickWins", []) or []:
        es.append("- " + blk(q).replace("\n", " "))
    es.append("\n## Umsetzungs-Roadmap\n")
    for ph in master.get("roadmap", []) or []:
        es.append("### %s — %s\n" % (cell(ph.get("phase")), blk(ph.get("goal")).replace("\n", " ")))
        for td in ph.get("todos", []) or []:
            es.append("- " + blk(td).replace("\n", " "))
        es.append("")
    es.append("## Empfehlung zur Neu-Struktur\n")
    es.append(blk(master.get("restructuringVerdict")))
    es.append("\n## Risiken\n")
    for r in master.get("risks", []) or []:
        es.append("- " + blk(r).replace("\n", " "))
    writef("01-executive-summary.md", "\n".join(es))

    # ---- 02 todo backlog ----
    # stable IDs across full sorted list
    def todo_sort_key(t):
        return (PRIO_ORDER.get(t.get("priority"), 9), EFFORT_ORDER.get(t.get("effort"), 9), t.get("cluster", ""))

    sorted_todos = sorted(all_todos, key=todo_sort_key)
    for i, t in enumerate(sorted_todos, 1):
        t["_id"] = "T-%03d" % i

    tb = []
    tb.append("# TODO-Backlog — Workshop-Review %s\n" % DATE)
    tb.append("> %s atomare TODOs, dedupliziert aus %s Roh-Befunden. Bereit fuer eine Umsetzungs-Instanz.\n" % (len(all_todos), len(all_findings)))
    # priority distribution
    dist = {}
    for t in all_todos:
        dist[t.get("priority", "?")] = dist.get(t.get("priority", "?"), 0) + 1
    tb.append("**Prioritaets-Verteilung:** " + ", ".join("%s=%s" % (k, dist[k]) for k in sorted(dist, key=lambda x: PRIO_ORDER.get(x, 9))))
    tb.append("")
    tb.append("## Gesamtliste (nach Prioritaet)\n")
    tb.append("| ID | P | Aufw. | Titel | Cluster | Dateien |")
    tb.append("|---|---|---|---|---|---|")
    for t in sorted_todos:
        tb.append("| %s | %s | %s | %s | %s | %s |" % (
            t["_id"], cell(t.get("priority")), cell(t.get("effort")),
            cell(t.get("title")), cell(t.get("cluster")), cell(t.get("files"))))
    tb.append("\n---\n")
    tb.append("## Details nach Cluster\n")
    for c in clusters:
        cname = c.get("cluster", "?")
        ctodos = c.get("todos", []) or []
        tb.append("### Cluster: `%s` (%s TODOs)\n" % (cname, len(ctodos)))
        tb.append(blk(c.get("clusterSummary")))
        tb.append("")
        # find ids for these todos
        for ct in ctodos:
            tid = next((x["_id"] for x in sorted_todos if x is not None and x.get("title") == ct.get("title") and x.get("cluster") == cname), "T-???")
            tb.append("#### %s — %s  `[%s | %s]`\n" % (tid, blk(ct.get("title")).replace("\n", " "), cell(ct.get("priority")), cell(ct.get("effort"))))
            tb.append(blk(ct.get("description")))
            tb.append("")
            tb.append("- **Dateien:** %s" % cell(ct.get("files")))
            tb.append("- **Begruendung:** %s" % blk(ct.get("rationale")).replace("\n", " "))
            if ct.get("acceptance"):
                tb.append("- **Akzeptanz:** %s" % blk(ct.get("acceptance")).replace("\n", " "))
            tb.append("- **Quelle:** %s" % cell(ct.get("sourcePersonas")))
            if ct.get("dependencies"):
                tb.append("- **Abhaengig von:** %s" % cell(ct.get("dependencies")))
            tb.append("")
    writef("02-todo-backlog.md", "\n".join(tb))

    # ---- 03 currency report ----
    cr = []
    cr.append("# Currency-Report — Aktualitaets-Befunde %s\n" % DATE)
    cr.append("> Web-verifizierte Aktualitaets-Luecken. Stand-Anker: Opus 4.8 ist Default, Fable 5 existiert;")
    cr.append("> Inhalte nennen noch Opus 4.7 / v2.1.146 (Stand 2026-05).\n")
    cur_cluster = next((c for c in clusters if c.get("cluster") == "currency"), None)
    if cur_cluster:
        cr.append("## Konsolidierte Currency-TODOs\n")
        cr.append(blk(cur_cluster.get("clusterSummary")))
        cr.append("")
        for ct in cur_cluster.get("todos", []) or []:
            cr.append("### %s `[%s | %s]`\n" % (blk(ct.get("title")).replace("\n", " "), cell(ct.get("priority")), cell(ct.get("effort"))))
            cr.append(blk(ct.get("description")))
            cr.append("\n- **Dateien:** %s" % cell(ct.get("files")))
            if ct.get("acceptance"):
                cr.append("- **Akzeptanz:** %s" % blk(ct.get("acceptance")).replace("\n", " "))
            cr.append("")
    cr.append("\n## Roh-Befunde der 3 Currency-Auditoren (mit Quellen)\n")
    for f in all_findings:
        if f.get("category") == "currency":
            cr.append("- **%s** _(%s, %s)_ — %s  \n  Evidenz/Quelle: %s  \n  Empfehlung: %s" % (
                blk(f.get("title")).replace("\n", " "), cell(f.get("severity")), cell(f.get("file")),
                blk(f.get("recommendation")).replace("\n", " "),
                blk(f.get("evidence")).replace("\n", " "),
                blk(f.get("recommendation")).replace("\n", " ")))
    writef("03-currency-report.md", "\n".join(cr))

    # ---- 04 restructuring ----
    rs = []
    rs.append("# Restrukturierungs-Vorschlag (Curriculum-Architekt) %s\n" % DATE)
    rs.append(blk(architect.get("summary")))
    if architect.get("designPrinciples"):
        rs.append("\n## Design-Prinzipien\n")
        for p in architect.get("designPrinciples", []):
            rs.append("- " + blk(p).replace("\n", " "))
    rs.append("\n## Vorgeschlagene Feinstruktur\n")
    rs.append("| Einheit | Titel | Level | Dauer | aus (alt) |")
    rs.append("|---|---|---|---|---|")
    for u in architect.get("proposedStructure", []) or []:
        rs.append("| %s | %s | %s | %s | %s |" % (
            cell(u.get("unit")), cell(u.get("title")), cell(u.get("level")),
            cell(u.get("duration")), cell(u.get("mapsFromOld"))))
    rs.append("\n### Einheiten im Detail\n")
    for u in architect.get("proposedStructure", []) or []:
        rs.append("#### %s — %s  `[%s, %s]`\n" % (cell(u.get("unit")), blk(u.get("title")).replace("\n", " "), cell(u.get("level")), cell(u.get("duration"))))
        if u.get("prerequisites"):
            rs.append("- **Voraussetzung:** %s" % cell(u.get("prerequisites")))
        if u.get("learningGoals"):
            rs.append("- **Lernziele:**")
            for g in u.get("learningGoals", []):
                rs.append("  - " + blk(g).replace("\n", " "))
        if u.get("contents"):
            rs.append("- **Inhalte:**")
            for ccc in u.get("contents", []):
                rs.append("  - " + blk(ccc).replace("\n", " "))
        if u.get("exercises"):
            rs.append("- **Uebungen:** %s" % cell(u.get("exercises")))
        rs.append("")
    rs.append("## Rationale\n")
    rs.append(blk(architect.get("rationale")))
    rs.append("\n## Migrations-Hinweise\n")
    rs.append(blk(architect.get("migrationNotes")))
    if architect.get("openQuestions"):
        rs.append("\n## Offene Fragen\n")
        for q in architect.get("openQuestions", []):
            rs.append("- " + blk(q).replace("\n", " "))
    writef("04-restructuring-proposal.md", "\n".join(rs))

    # ---- 05 new exercises ----
    ex = []
    ex.append("# Neue & 'verrueckte' Uebungen (Wild-Exercise-Designer) %s\n" % DATE)
    ex.append(blk(crazy.get("summary")))
    ex.append("")
    for i, idea in enumerate(crazy.get("ideas", []) or [], 1):
        ex.append("## %s. %s  `[%s | %s]`\n" % (i, blk(idea.get("title")).replace("\n", " "), cell(idea.get("format")), cell(idea.get("difficulty"))))
        ex.append("- **Thema/Block:** %s" % cell(idea.get("topic")))
        ex.append("- **Geuebtes Konzept:** %s" % cell(idea.get("concept")))
        ex.append("- **Didaktischer Wert:** %s" % blk(idea.get("why")).replace("\n", " "))
        if idea.get("securityAngle"):
            ex.append("- **Security-Aufhaenger:** %s" % blk(idea.get("securityAngle")).replace("\n", " "))
        ex.append("\n**Ablauf:**\n")
        ex.append(blk(idea.get("sketch")))
        ex.append("")
    writef("05-new-exercises.md", "\n".join(ex))

    # ---- 06 all findings (appendix, by persona) ----
    af = []
    af.append("# Anhang: Alle Roh-Befunde nach Persona %s\n" % DATE)
    for lr in lens:
        pname = lr.get("persona", "?")
        af.append("\n## %s\n" % blk(pname).replace("\n", " "))
        if lr.get("scope"):
            af.append("_Scope:_ %s\n" % blk(lr.get("scope")).replace("\n", " "))
        af.append("**Zusammenfassung:** " + blk(lr.get("summary")).replace("\n", " "))
        if lr.get("strengths"):
            af.append("\n**Staerken:**")
            for s in lr.get("strengths", []):
                af.append("- *%s* — %s" % (cell(s.get("area")), blk(s.get("detail")).replace("\n", " ")))
        fnd = sorted(lr.get("findings", []) or [], key=lambda x: SEV_ORDER.get(x.get("severity"), 9))
        if fnd:
            af.append("\n| Sev | Kat | Titel | Datei | Empfehlung | Aufw |")
            af.append("|---|---|---|---|---|---|")
            for f in fnd:
                af.append("| %s | %s | %s | %s | %s | %s |" % (
                    cell(f.get("severity")), cell(f.get("category")), cell(f.get("title")),
                    cell(f.get("file")), cell(f.get("recommendation")), cell(f.get("effort"))))
        af.append("")
    writef("06-all-findings.md", "\n".join(af))

    # ---- personas index + per-persona files ----
    pidx = ["# Personas — Workshop-Review %s\n" % DATE,
            "Eine Datei je Persona (Karte + Report). 7 Lern-/Liefer-Personas + 3 Currency-Auditoren.\n",
            "| Persona | Datei |", "|---|---|"]
    for i, lr in enumerate(lens):
        pid = PERSONA_IDS[i] if i < len(PERSONA_IDS) else slug(lr.get("persona", "p%d" % i))
        fname = "%02d-%s.md" % (i + 1, pid)
        pidx.append("| %s | `%s` |" % (cell(lr.get("persona")), fname))
        pf = []
        pf.append("# Persona: %s\n" % blk(lr.get("persona")).replace("\n", " "))
        pf.append("**Scope:** %s\n" % blk(lr.get("scope")).replace("\n", " "))
        pf.append("## Gesamteindruck\n")
        pf.append(blk(lr.get("summary")))
        pf.append("\n## Staerken (was bleiben soll)\n")
        for s in lr.get("strengths", []) or []:
            pf.append("- **%s** — %s" % (cell(s.get("area")), blk(s.get("detail")).replace("\n", " ")))
        pf.append("\n## Befunde\n")
        fnd = sorted(lr.get("findings", []) or [], key=lambda x: SEV_ORDER.get(x.get("severity"), 9))
        for f in fnd:
            pf.append("### [%s | %s | %s] %s\n" % (cell(f.get("severity")), cell(f.get("category")), cell(f.get("effort")), blk(f.get("title")).replace("\n", " ")))
            pf.append("- **Datei:** %s" % cell(f.get("file")))
            pf.append("- **Evidenz:** %s" % blk(f.get("evidence")).replace("\n", " "))
            pf.append("- **Empfehlung:** %s" % blk(f.get("recommendation")).replace("\n", " "))
            pf.append("")
        writef("personas/%s" % fname, "\n".join(pf))
    writef("personas/index.md", "\n".join(pidx))

    # ---- digest to stdout ----
    print("=== RENDER OK ===")
    print("counts:", json.dumps(counts, ensure_ascii=False))
    print("clusters:")
    for c in clusters:
        print("  - %s: %d todos" % (c.get("cluster"), len(c.get("todos", []) or [])))
    print("priority distribution:", json.dumps(dist, ensure_ascii=False))
    print("\n--- MASTER executiveSummary ---")
    print(blk(master.get("executiveSummary")))
    print("\n--- MASTER topThemes ---")
    for t in master.get("topThemes", []) or []:
        print("  * %s :: %s" % (t.get("theme"), t.get("impact")))
    print("\n--- MASTER quickWins ---")
    for q in master.get("quickWins", []) or []:
        print("  * %s" % str(q).replace("\n", " "))
    print("\n--- MASTER restructuringVerdict ---")
    print(blk(master.get("restructuringVerdict")))
    print("\n--- MASTER risks ---")
    for r in master.get("risks", []) or []:
        print("  * %s" % str(r).replace("\n", " "))
    print("\n--- ARCHITECT summary ---")
    print(blk(architect.get("summary"))[:1200])
    print("\n--- ARCHITECT proposed units ---")
    for u in architect.get("proposedStructure", []) or []:
        print("  %s %s [%s, %s]" % (u.get("unit"), u.get("title"), u.get("level"), u.get("duration")))
    print("\n--- CRAZY ideas ---")
    for idea in crazy.get("ideas", []) or []:
        print("  * [%s/%s] %s" % (idea.get("format"), idea.get("difficulty"), idea.get("title")))


def _ensure_data():
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    return os.path.join(OUT, "data", "raw-workflow-output.json")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    _ensure_data()
    main()
