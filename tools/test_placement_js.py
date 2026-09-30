"""The JavaScript placement engine in the cockpit must equal the Python reference on every persona."""
from pathlib import Path
import json
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tools" / "fixtures"
TEMPLATE = ROOT / "tools" / "cockpit" / "template.html"
ARTEFACT = ROOT / "resources" / "claude-code-workshop-ui.html"
NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(NODE is None, reason="node nicht installiert — JS-Parität nicht prüfbar")


def engine_source(html: str) -> str:
    start, end = html.index("/*@@ENGINE_START@@*/"), html.index("/*@@ENGINE_END@@*/")
    return html[start:end]


def run_js(source: str, tmp_path: Path):
    catalog = json.loads((FIX / "placement-catalog.json").read_text(encoding="utf-8"))
    personas = json.loads((FIX / "placement-vectors.json").read_text(encoding="utf-8"))["personas"]
    script = tmp_path / "run.js"
    script.write_text(
        source + "\nconst catalog = " + json.dumps(catalog) + ";\nconst personas = " + json.dumps(personas) + ";\n"
        "const out = {};\nfor (const p of personas) out[p.id] = place(catalog, p.answers);\n"
        "process.stdout.write(JSON.stringify(out));\n", encoding="utf-8")
    result = subprocess.run([NODE, str(script)], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(result.stdout)


def test_template_engine_equals_python_golden(tmp_path):
    golden = json.loads((FIX / "placement-golden.json").read_text(encoding="utf-8"))
    js = run_js(engine_source(TEMPLATE.read_text(encoding="utf-8")), tmp_path)
    for pid in golden:
        assert js[pid] == golden[pid], pid


def test_js_engine_rejects_unknown_ids(tmp_path):
    catalog = json.loads((FIX / "placement-catalog.json").read_text(encoding="utf-8"))
    script = tmp_path / "bad.js"
    script.write_text(engine_source(TEMPLATE.read_text(encoding="utf-8")) + "\nconst catalog = " + json.dumps(catalog)
                      + ";\ntry { place(catalog, {goals: ['nope']}); console.log('no'); } catch (e) { console.log('raised'); }\n",
                      encoding="utf-8")
    out = subprocess.run([NODE, str(script)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert out.strip() == "raised"


@pytest.mark.skipif(not ARTEFACT.exists() or "@@ENGINE_START@@" not in ARTEFACT.read_text(encoding="utf-8"),
                    reason="Cockpit-Artefakt noch nicht aus der Bibliothek gebaut")
def test_artefact_engine_equals_template_engine():
    assert engine_source(ARTEFACT.read_text(encoding="utf-8")) == engine_source(TEMPLATE.read_text(encoding="utf-8"))
