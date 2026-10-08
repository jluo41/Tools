"""Proposals reach a release only through triage, one batch per release (haipipe-insight ref/release.md, b11 s21 phase 3)."""
import importlib.util
import re
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
INSIGHT = HERE.parents[2]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PR = _load("proposals", HERE.parent / "scripts" / "proposals.py")
NR = _load("next_run", INSIGHT / "haipipe-insight-workflow" / "scripts" / "next_run.py")
IL = PR.IL


def _front(md):
    return yaml.safe_load(re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8")).group(1))


def _signed_release(proto):
    IL.main(["version", str(proto), "--slug", "first"])
    v = proto / "j01_p1_first"
    IL.main(["question", str(v), "D01", "shape"])
    q = v / "t01_D01_shape" / "question.md"
    text = q.read_text(encoding="utf-8").replace("agreed: ⬜", "agreed: ✅ 261008")
    q.write_text(text, encoding="utf-8")
    (v / "partitions.md").write_text("---\npartitions:\n- {name: full, where: []}\n---\n", encoding="utf-8")
    IL.main(["sign", str(v), "--date", "261008"])


def test_a_batch_goes_into_the_next_release_and_next_run_follows(tmp_path):
    proto = tmp_path / "Project-Demo" / "tasks" / "Prototype-b01-Demo"
    IL.main(["prototype", str(proto), "--serves", "insights/Insight-Demo"])
    _signed_release(proto)
    for slug, kind in (("a-gap", "new question"), ("a-cut", "cut"), ("too-broad", "new question")):
        IL.main(["propose", str(proto), slug, "--kind", kind, "--from", "j01", "--why", "<why>"])
    assert NR.state(proto)[1].startswith("run-triage-proposals-p2")
    with pytest.raises(SystemExit, match="next one, p2"):
        PR.main(["take", str(proto), "a-gap", "--into", "p1"])
    PR.main(["take", str(proto), "a-gap", "a-cut", "--into", "p2"])
    PR.main(["decline", str(proto), "too-broad", "--why", "two questions in one"])
    assert _front(proto / "proposals" / "a-gap.md")["taken-in"] == "p2"
    assert _front(proto / "proposals" / "too-broad.md")["state"] == "declined"
    assert NR.state(proto)[1].startswith("run-open-version-p2")
    with pytest.raises(SystemExit, match="already taken"):
        PR.main(["take", str(proto), "a-gap", "--into", "p2"])
    IL.main(["version", str(proto), "--slug", "the-gaps"])
    IL.main(["propose", str(proto), "late", "--kind", "fix", "--from", "j01", "--why", "<why>"])
    with pytest.raises(SystemExit, match="still open: a batch goes into p2"):
        PR.main(["take", str(proto), "late", "--into", "p3"])
    PR.main(["take", str(proto), "late", "--into", "p2"])
