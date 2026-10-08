"""The insight ladder's scaffold makes each level and keeps its gates (ref/insight-ladder.md, b11 s21 phase 1).

A placeholder Project is built in a temp folder through scripts/insight_ladder.py, from a Prototype's first
release to a Board's third Job; the insight workbench's own reader (servers/workbench-insight/insight_plan_c.py)
must read it back. No real names and no data: every value is a placeholder.
"""
import importlib.util
import re
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("insight_ladder", HERE.parent / "scripts" / "insight_ladder.py")
IL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IL)
READER = HERE.parents[4] / "servers" / "workbench-insight"


def L(*args):
    return IL.main([str(a) for a in args])


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) if m else {}


def _agree_and_need(version: Path) -> None:
    """What another agent and the plan write before a release is signed: agreed needs, one compute need."""
    for q in version.glob("t*/question.md"):
        text = q.read_text(encoding="utf-8")
        m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", text)
        f = yaml.safe_load(m.group(1))
        f["agreed"] = "✅ 261008"
        f["needs"] = {"E1": {"kind": "compute", "what": "<what>", "pass": "<pass>", "cut": "the cell's partition",
                             "unit": "<unit>", "measure": "<measure>", "by": "<by>", "uncertainty": "<interval>",
                             "rivals": "none", "output": {"table.csv": ["<col>"]}}}
        q.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2),
                     encoding="utf-8")


def _cuts(version: Path) -> None:
    (version / "partitions.md").write_text(
        "---\npartitions:\n- {name: full, where: []}\n- name: part-a\n  where: [{column: <col>, lte: 1}]\n"
        "- {name: cross, of: [full, part-a]}\n---\n\n# The cuts\n", encoding="utf-8")


@pytest.fixture()
def project(tmp_path):
    p = tmp_path / "Project-Demo"
    proto, board = p / "tasks" / "Prototype-b01-Demo", p / "insights" / "Insight-Demo"
    L("prototype", proto, "--serves", "insights/Insight-Demo")
    L("version", proto)
    L("question", proto / "j01_p1", "D01", "extract-shape")
    L("question", proto / "j01_p1", "I01", "rates-by-cut")
    return p, proto, board


def test_a_release_folder_says_what_it_is(tmp_path):
    """jNN_pN_<slug> (JL 261008); the release id stays pN, and a Board Job pins it by that id."""
    p = tmp_path / "Project-Demo"
    proto, board = p / "tasks" / "Prototype-b01-Demo", p / "insights" / "Insight-Demo"
    L("prototype", proto, "--serves", "insights/Insight-Demo")
    L("version", proto, "--slug", "first-questions")
    v = proto / "j01_p1_first-questions"
    assert _front(v / "j01_p1_first-questions.md")["release"] == "p1"
    L("question", v, "D01", "extract-shape")
    _agree_and_need(v)
    _cuts(v)
    L("sign", v, "--date", "261008")
    L("board", board, "--dataset", "Demo", "--prototype", "tasks/Prototype-b01-Demo")
    L("data", board, "v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    L("job", board, "--release", "p1", "--data", "v1")
    face = _front(board / "j01_p1_Demov1" / "j01_p1_Demov1.md")
    assert face["prototype"] == "tasks/Prototype-b01-Demo/j01_p1_first-questions"
    L("run", v / "t01_D01_extract-shape", "plan-evidence")
    assert (v / "t01_D01_extract-shape" / "runs" / "run-plan-evidence-d01" / "run.yaml").is_file()
    L("run", v, "set-cuts")
    assert (v / "runs" / "run-set-cuts-p1").is_dir()


def test_prototype_and_first_release(project):
    p, proto, _ = project
    assert _front(proto / "board.md") == {"board-kind": "prototype", "serves": "insights/Insight-Demo"}
    v = proto / "j01_p1"
    assert _front(v / "j01_p1.md")["state"] == "open"
    rel = yaml.safe_load((v / "release.yaml").read_text())
    assert rel["questions"] == {"D01": {"task": "t01_D01_extract-shape", "change": "new"},
                                "I01": {"task": "t02_I01_rates-by-cut", "change": "new"}}
    q = _front(v / "t02_I01_rates-by-cut" / "question.md")
    assert (q["id"], q["level"], q["agreed"]) == ("I01", "information", "⬜")
    assert (proto / "proposals" / "README.md").is_file()


def test_sign_needs_agreed_questions_and_cuts(project):
    _, proto, _ = project
    v = proto / "j01_p1"
    with pytest.raises(SystemExit, match="not agreed"):
        L("sign", v, "--date", "261008")
    _agree_and_need(v)
    with pytest.raises(SystemExit, match="set the cuts"):
        L("sign", v, "--date", "261008")
    _cuts(v)
    L("sign", v, "--date", "261008")
    assert _front(v / "j01_p1.md")["signed"] == "✅ 261008"
    with pytest.raises(SystemExit, match="frozen"):
        L("question", v, "K01", "late")


def test_an_id_is_never_reused_and_a_question_keeps_its_task_number(project):
    _, proto, _ = project
    v1 = proto / "j01_p1"
    _agree_and_need(v1)
    _cuts(v1)
    L("sign", v1, "--date", "261008")
    L("version", proto)
    v2 = proto / "j02_p2"
    rel = yaml.safe_load((v2 / "release.yaml").read_text())
    assert rel["questions"]["D01"] == {"task": "../j01_p1/t01_D01_extract-shape", "change": "kept"}
    with pytest.raises(SystemExit, match="already in"):
        L("question", v2, "D01", "again")
    L("change", v2, "I01", "--why", "its script fixed")
    assert (v2 / "t02_I01_rates-by-cut" / "question.md").is_file()             # the same tNN, carried forward
    L("question", v2, "I02", "drop-off")
    assert (v2 / "t03_I02_drop-off").is_dir()
    L("retire", v2, "D01", "--why", "answered by I02")
    rel = yaml.safe_load((v2 / "release.yaml").read_text())
    assert "D01" not in rel["questions"] and rel["retired"] == {"D01": "answered by I02"}
    L("question", proto / "j02_p2", "D02", "new-shape")
    assert (v2 / "t04_D02_new-shape").is_dir()


def test_board_jobs_one_clock_and_the_reader(project):
    p, proto, board = project
    v1 = proto / "j01_p1"
    with pytest.raises(SystemExit, match="Insight-<name>"):
        L("board", p / "insights" / "topic", "--dataset", "Demo", "--prototype", "tasks/Prototype-b01-Demo")
    with pytest.raises(SystemExit, match="carrying no version"):
        L("board", board, "--dataset", "Demov1", "--prototype", "tasks/Prototype-b01-Demo")
    L("board", board, "--dataset", "Demo", "--prototype", "tasks/Prototype-b01-Demo")
    L("data", board, "v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    with pytest.raises(SystemExit, match="not signed"):
        L("job", board, "--release", "p1", "--data", "v1")
    _agree_and_need(v1)
    _cuts(v1)
    L("sign", v1, "--date", "261008")
    with pytest.raises(SystemExit, match="not a data version"):
        L("job", board, "--release", "p1", "--data", "v2")
    L("job", board, "--release", "p1", "--data", "v1")
    j1 = board / "j01_p1_Demov1"
    face = _front(j1 / "j01_p1_Demov1.md")
    assert (face["release"], face["data"], face["moved"], face["state"]) == ("p1", "v1", "start", "open")
    assert re.fullmatch(r"[0-9a-f]{12}", face["hash"])
    runs = sorted(r.name for r in (j1 / "t02_I01_rates-by-cut" / "runs").iterdir())
    assert runs == ["r01_full", "r02_part-a"]                                    # rNN = the cut's place
    assert (j1 / "t02_I01_rates-by-cut" / "runs" / "r01_full" / "run.sh").is_file()
    with pytest.raises(SystemExit, match="one Job per pair"):
        L("job", board, "--release", "p1", "--data", "v1")
    L("data", board, "v2", "--extract", "_WorkSpace/<store>/demo_v2.parquet")
    L("job", board, "--release", "p1", "--data", "v2")
    assert _front(board / "j02_p1_Demov2" / "j02_p1_Demov2.md")["moved"] == "data"
    L("version", proto)
    _agree_and_need(proto / "j02_p2")
    L("sign", proto / "j02_p2", "--date", "261008")
    with pytest.raises(SystemExit, match="one clock per Job"):
        L("job", board, "--release", "p2", "--data", "v1")
    L("job", board, "--release", "p2", "--data", "v2")
    assert _front(board / "j03_p2_Demov2" / "j03_p2_Demov2.md")["moved"] == "code"

    L("propose", proto, "a-cut", "--kind", "cut", "--from", "j02", "--why", "<why>")
    L("run", board, "coverage")
    L("run", board / "j03_p2_Demov2", "compare", "j02")
    L("run", board / "j03_p2_Demov2" / "t02_I01_rates-by-cut", "write")
    card = yaml.safe_load((board / "j03_p2_Demov2" / "t02_I01_rates-by-cut" / "runs" / "run-write-t02" /
                           "run.yaml").read_text())
    assert card["skill"] == "haipipe-insight-information"
    with pytest.raises(SystemExit, match="does not run at the board level"):
        L("run", board, "launch")

    sys.path.insert(0, str(READER))
    import insight_plan_c as C
    assert C.is_plan_c(board)
    b = C.board(board)
    assert [(j["name"], j["moved"]) for j in b["jobs"]] == [("j01_p1_Demov1", "start"), ("j02_p1_Demov2", "data"),
                                                           ("j03_p2_Demov2", "code")]
    assert [r["name"] for r in b["prototype"]["releases"]] == ["p1", "p2"]
    assert "a-cut" in [x["title"] for x in b["prototype"]["proposals"]]


def test_dry_run_changes_nothing(tmp_path):
    p = tmp_path / "Project-Demo"
    made = L("prototype", p / "tasks" / "Prototype-b01-Demo", "--serves", "insights/Insight-Demo", "--dry-run")
    assert made and not (p / "tasks").exists()
