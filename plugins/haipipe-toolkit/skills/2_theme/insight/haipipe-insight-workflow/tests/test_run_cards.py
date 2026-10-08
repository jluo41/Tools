"""The insight run cards hold, the table follows them, and next_run names the owed Run (b11 s21 phase 2)."""
import importlib.util
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
INSIGHT = HERE.parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RC = _load("run_cards", INSIGHT / "haipipe-insight-workflow" / "scripts" / "run_cards.py")
NR = _load("next_run", INSIGHT / "haipipe-insight-workflow" / "scripts" / "next_run.py")
CT = _load("cards_table", INSIGHT / "workbench-insight" / "scripts" / "cards_table.py")
IL = NR.IL


def test_every_card_is_whole_and_the_scaffold_agrees():
    assert RC.check() == []
    assert RC.against_scaffold() == []


def test_no_card_names_the_workflow_skill_and_judges_are_other_agents():
    cards = RC.cards()
    assert not [c for c in cards if c["skill"].endswith("-workflow")]
    judging = [c for c in cards if re.search(r"\b(review|check)\b", c["label"], re.I)]
    assert judging and all(c["agent"] != "haipipe-insight-agent" for c in judging)


def test_the_table_is_generated_from_the_cards():
    table = (INSIGHT / "workbench-insight" / "ref" / "workbench-table.md").read_text(encoding="utf-8")
    rows = [line for line in table.splitlines() if line.startswith("| ") and not line.startswith("| Level")]
    assert len(rows) == len(RC.cards())
    assert [r.split(" | ")[3] for r in rows] == [c["label"] for c in RC.cards()]


def test_card_for_finds_a_run_by_its_folder_name():
    assert RC.card_for("run-add-j03", "Block")["label"] == "Add a Job"
    assert RC.card_for("r02_part-a", "Task")["label"] == "Run a partition"
    assert RC.card_for("run-compare-j02", "Job")["skill"] == "haipipe-insight-knowledge"


def _front_set(md: Path, **kv):
    text = md.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", text)
    f = yaml.safe_load(m.group(1))
    f.update(kv)
    md.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2),
                  encoding="utf-8")


def test_next_run_walks_the_gates(tmp_path):
    p = tmp_path / "Project-Demo"
    proto, board = p / "tasks" / "Prototype-b01-Demo", p / "insights" / "Insight-Demo"
    L = lambda *a: IL.main([str(x) for x in a])  # noqa: E731
    L("prototype", proto, "--serves", "insights/Insight-Demo")
    assert NR.state(proto)[1] == "run-open-version-p1"
    L("version", proto, "--slug", "first")
    v = proto / "j01_p1_first"
    assert NR.state(v)[1].startswith("run-ask-")
    L("question", v, "D01", "shape")
    assert NR.state(v)[1] == "run-plan-evidence-d01"
    q = v / "t01_D01_shape" / "question.md"
    _front_set(q, needs={"E1": {"kind": "compute"}})
    assert NR.state(v)[1] == "run-review-plan-d01"
    _front_set(q, agreed="✅ 261008")
    assert NR.state(v)[1] == "run-write-script-d01"
    (q.parent / "scripts").mkdir()
    (q.parent / "scripts" / "shape.py").write_text('SPEC = "D01"\n', encoding="utf-8")
    assert NR.state(v)[1] == "run-set-cuts-p1"
    (v / "partitions.md").write_text("---\npartitions:\n- {name: full, where: []}\n---\n", encoding="utf-8")
    assert NR.state(v)[1].startswith("run-sign-release-p1")
    L("sign", v, "--date", "261008")
    L("board", board, "--dataset", "Demo", "--prototype", "tasks/Prototype-b01-Demo")
    assert NR.state(board)[1] == "run-add-version-v1"
    L("data", board, "v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    assert NR.state(board)[1] == "run-add-j01"
    L("job", board, "--release", "p1", "--data", "v1")
    job = board / "j01_p1_Demov1"
    assert NR.state(job)[1] == "run-launch-j01"
    (job / "runs" / "run-launch-j01").mkdir(parents=True)
    run = job / "t01_D01_shape" / "runs" / "r01_full"
    assert NR.state(job)[1].startswith("r01_full")
    _front_set_yaml = yaml.safe_load((run / "run.yaml").read_text())
    _front_set_yaml["status"] = "ok"
    (run / "run.yaml").write_text(yaml.safe_dump(_front_set_yaml), encoding="utf-8")
    assert NR.state(job)[1] == "run-write-t01"
    page = job / "t01_D01_shape" / "t01_D01_shape.md"
    _front_set(page, **{"answer-status": "answered"})
    assert NR.state(job)[1].startswith("run-check-t01")
    _front_set(page, check="✅ 261008")
    assert NR.state(job)[1].startswith("run-close-j01")
    _front_set(job / "j01_p1_Demov1.md", state="closed")
    L("data", board, "v2", "--extract", "_WorkSpace/<store>/demo_v2.parquet")
    assert NR.state(board)[1].startswith("run-add-j02 (p1 on v2: data moved)")
