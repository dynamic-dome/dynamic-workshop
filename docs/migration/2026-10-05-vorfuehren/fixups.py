# -*- coding: utf-8 -*-
"""Second step of the move (run once, after migrate.py and its --check): what a script cannot decide by itself.

  python docs/migration/2026-10-05-vorfuehren/fixups.py

1. S1.20 carried a moderator block outside a 'Vorführen' section. It moves to the moderation layer as well.
2. Four lessons had their only cockpit example inside 'Vorführen' (S1.2, S3.13, S3.14, S4.6). A lesson needs
   exactly one example, so each gets a last subsection '### Ausprobieren' in 'Im Detail'. The commands of S1.2,
   S3.13 and S4.6 are the ones from the old demo, word for word. S3.14 used a plugin command that no longer
   exists; its example is now the built-in /goal, taken verbatim from code.claude.com/docs/en/goal.md
   (fetched 2026-10-05): "/goal all tests in test/auth pass and the lint step is clean".
3. Sentences in chapters that pointed readers to a demo are reworded or removed. Every replacement is asserted
   to match exactly once.
4. (--demo-crossrefs, run once afterwards) Demo files that refer to demo steps or talking points kept with
   another chapter now link to that chapter's demo file, not to the chapter.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import migrate  # noqa: E402

lm = migrate.lm
LIBRARY, DEMOS = migrate.LIBRARY, migrate.DEMOS
FENCE3 = "`" * 3


def read(name):
    return lm._read(LIBRARY / name)


def write(name, text):
    (LIBRARY / name).write_text(text, encoding="utf-8", newline="\n")


def replace_once(name, old, new):
    text = read(name)
    assert text.count(old) == 1, (name, old[:70], text.count(old))
    write(name, text.replace(old, new))


def move_moderator_block(name):
    text = read(name)
    start_tag, end_tag = "<details><summary>Für Moderierende</summary>", "</details>"
    start = text.index(start_tag)
    end = text.index("\n" + end_tag, start) + len("\n" + end_tag)
    body = text[start + len(start_tag):end - len(end_tag)].strip("\n")
    rest = text[:start].rstrip("\n") + "\n\n" + text[end:].lstrip("\n")
    if not rest.endswith("\n"):
        rest += "\n"
    chapter_id, title = migrate.front_of(text, LIBRARY / name)
    has_demo = {p.name for p in DEMOS.glob("*.md")}
    (DEMOS / name).write_text(migrate.demo_text(chapter_id, title, name, body, has_demo), encoding="utf-8", newline="\n")
    write(name, rest)
    print(f"Moderationsblock verschoben: {name} ({len(body.split())} Wörter)")


def add_try_it(name, block):
    """Append a subsection to 'Im Detail' (before the next H2 outside code fences)."""
    lines = read(name).split("\n")
    in_fence, inside, at = False, False, None
    for i, line in enumerate(lines):
        if lm.FENCE.match(line):
            in_fence = not in_fence
        if in_fence:
            continue
        h2 = lm.H2.match(line)
        if h2 and inside:
            at = i
            break
        if h2 and h2.group(1) == "Im Detail":
            inside = True
    assert at is not None, name
    head = lines[:at]
    while head and not head[-1].strip():
        head.pop()
    write(name, "\n".join(head + ["", *block.strip("\n").split("\n"), ""] + lines[at:]))
    print(f"Ausprobieren ergänzt: {name}")


EXAMPLES = {
    "s1-02-agent-statt-chat.md": f"""### Ausprobieren

Frag Claude Code selbst, worin es sich von einem Chat unterscheidet:

{lm.EXAMPLE_MARKER}
{FENCE3}
Describe yourself in exactly 3 bullet points. Focus on what makes you different from a chat interface.
{FENCE3}

Erwartet: Claude antwortet mit drei knappen Punkten, etwa zu (1) Zugriff aufs Dateisystem, (2) Ausführen von Befehlen, (3) Git- und Werkzeug-Integration. Der Wortlaut schwankt, die Substanz ist da.
""",
    "s3-13-autonome-loops-absichern.md": f"""### Ausprobieren

So legst du für einen riskanten Versuch einen abgeschotteten Arbeitsbaum an:

{lm.EXAMPLE_MARKER}
{FENCE3}bash
git worktree add ../experiment-async-processing -b feature/async-experiment
cd ../experiment-async-processing
claude
# Make experimental changes — the main branch stays untouched
{FENCE3}

Ist das Experiment fertig, verwirf es oder führ es zusammen:

{FENCE3}bash
git worktree remove ../experiment-async-processing
{FENCE3}
""",
    "s3-14-self-improve-loop.md": f"""### Ausprobieren

Den Plugin-Befehl gibt es nicht mehr. Mit Bordmitteln kommst du dem Zyklus am nächsten, wenn du Claude Code ein Ziel mit prüfbarer Bedingung gibst ([S3.12](s3-12-zeitgesteuert-arbeiten.md)). Probier es in einem Wegwerf-Repo mit Tests, auf einem eigenen Branch:

{lm.EXAMPLE_MARKER}
{FENCE3}
/goal all tests in test/auth pass and the lint step is clean
{FENCE3}

Vergleiche mit dem Zyklus oben: Welche der sechs Schritte siehst du, und welche Sicherheitsmechanismen aus der Tabelle unten musst du selbst mitbringen?
""",
    "s4-06-remote-und-teleport.md": f"""### Ausprobieren

Mit einem Befehl gibst du die laufende Sitzung für ein zweites Gerät frei:

{lm.EXAMPLE_MARKER}
{FENCE3}
/remote-control
{FENCE3}

Claude Code verbindet die Sitzung und nennt eine Sitzungs-URL. Ruf `/remote-control` noch einmal auf, dann zeigt das Statusfenster URL und QR-Code. Öffne die URL auf Handy oder Laptop, dann liest und antwortest du von dort.
""",
}

# (file, old, new) — sentences that sent readers to a demo
REWORD = [
    ("s1-01-erster-kontakt.md",
     "**Wie in der Vorführung.** Statt `hello.py` kannst du auch den Passwortgenerator aus „Vorführen\" nachbauen.\n\n",
     ""),
    ("s1-05-rechte-im-alltag.md",
     "- [S3.8 · Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md), mit Live-Vorführung der Modi",
     "- [S3.8 · Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md)"),
    ("s1-06-rechte-modi.md",
     "- [S3.8 · Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md), mit Live-Vorführung vom Besucherausweis zum Generalschlüssel",
     "- [S3.8 · Rechte für autonome Läufe](s3-08-rechte-fuer-autonomie.md)"),
    ("s1-07-modellwahl-und-effort.md",
     "Den direkten Vergleich, dieselbe Aufgabe mit drei Modellen und `/cost` nach jedem Lauf, zeigt die Demo in [S1.19](s1-19-kosten-im-blick.md). Dort steht auch die Übung, in der du Modell und Effort für deine eigenen Abläufe festlegst.",
     "Wie du den Verbrauch abliest und Modell und Effort für deine eigenen Abläufe festlegst, übst du in [S1.19](s1-19-kosten-im-blick.md)."),
    ("s1-13-vager-und-praeziser-auftrag.md",
     "Die Aufgabe aus Demo und Übung unten, ein IPv4-Validator, kommt später wieder: Die Git-Demo in [S1.16](s1-16-git-in-einem-fluss.md) baut auf `validators.py` und den Tests auf, und in [S1.19](s1-19-kosten-im-blick.md) löst du dieselbe Aufgabe mit drei Modellen.",
     "Die Aufgabe der Übung unten ist ein IPv4-Validator."),
    ("s1-14-plan-modus.md", "In Demo und Übung von [S1.13]", "In der Übung von [S1.13]"),
    ("s1-18-worktrees.md", " So arbeiten die Vorführung und die Übung unten.", ""),
    ("s2-11-plugins-buendeln.md", "wie in der Demo und der Übung unten.", "wie in der Übung unten."),
    ("s2-15-mcp-einrichten.md", "(s2-14-mcp-stecker.md) (Demo und Übung)", "(s2-14-mcp-stecker.md) (Übung)"),
    ("s3-02-eingebaute-subagenten.md",
     "Die meisten Vorführungen dieses Regals drehen sich um eigene Subagenten",
     "Der Rest dieses Regals dreht sich vor allem um eigene Subagenten"),
    ("s3-06-devils-advocate.md", "Demo und Übung prüfen `workshop-playground/access_control.py`.",
     "Die Übung prüft `workshop-playground/access_control.py`."),
    ("s3-06-devils-advocate.md", "In der Demo (optionaler Schritt) und im CTF unten sucht der Schwarm",
     "Im CTF unten sucht der Schwarm"),
    ("s3-07-eingebaute-reviews.md",
     " Wie Claude eine CVE in einer Abhängigkeit bis zum PR behebt, zeigt die CVE-Demo in [S3.6](s3-06-devils-advocate.md).",
     ""),
    ("s4-01-modell-pro-phase.md", "zeigt die Demo in [S4.2](s4-02-codex-schwarm.md);", "beschreibt [S4.2](s4-02-codex-schwarm.md);"),
    ("s4-09-fehlersuche-werkzeuge.md",
     "In der Demo in [S4.10](s4-10-diagnose-schritt-fuer-schritt.md) siehst du `/debug` in Schritt 4 live.",
     "Wie `/debug` in einer ganzen Diagnose sitzt, zeigt Schritt 4 der Abläufe in [S4.10](s4-10-diagnose-schritt-fuer-schritt.md)."),
    ("s4-02-codex-schwarm.md",
     "**Format:** Du siehst die Demo oben (live, als Aufzeichnung oder selbst ausgeführt).",
     "**Format:** Grundlage ist der Ablauf des Codex-Schwarms aus der Moderationsschicht ([Vorführen: S4.2](../moderation/vorfuehren/s4-02-codex-schwarm.md)): live gesehen, als Aufzeichnung oder selbst ausgeführt."),
]


CROSSREF_WORDS = ("Demo", "Schritt", "Sprechpunkt", "Vorführung", "Fortsetzung")
CROSSREF_SKIP = {("s3-06-devils-advocate.md", "s1-14-plan-modus.md"), ("s3-06-devils-advocate.md", "s4-05-ci-pipelines.md")}


def demo_crossrefs():
    """In demo files: a link to a chapter on a line about demo steps becomes a link to that chapter's demo file."""
    import re
    names = {p.name for p in DEMOS.glob("*.md")}
    changed = 0
    for path in sorted(DEMOS.glob("*.md")):
        lines = path.read_text(encoding="utf-8").split(chr(10))
        for i, line in enumerate(lines):
            if i < 3 or not any(word in line for word in CROSSREF_WORDS):
                continue

            def fix(match, own=path.name):
                target = match.group(1)
                if target in names and target != own and (own, target) not in CROSSREF_SKIP:
                    return f"]({target})"
                return match.group(0)

            new = re.sub(r"\]\(\.\./\.\./library/([a-z0-9-]+\.md)\)", fix, line)
            if new != line:
                lines[i] = new
                changed += 1
        path.write_text(chr(10).join(lines), encoding="utf-8", newline=chr(10))
    print(f"{changed} Zeilen in Demo-Dateien auf Demo-Dateien umgelenkt")
    return 0


def main():
    if "--demo-crossrefs" in sys.argv:
        return demo_crossrefs()
    move_moderator_block("s1-20-praxis-station-1.md")
    for name, block in EXAMPLES.items():
        add_try_it(name, block)
    for name, old, new in REWORD:
        replace_once(name, old, new)
    print(f"{len(REWORD)} Verweise angepasst")
    return 0


if __name__ == "__main__":
    sys.exit(main())
