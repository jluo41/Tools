"""The answering page of a Board Task and a Prototype's question map are generated, never typed (ref/insight-ladder.md):
write_answer_page.py writes a Board Task's face and sections from a spec, citing only tables its Runs wrote, and
question_map.py draws a release's questions, Executive included. Placeholders only: a made-up extract in a temp folder.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "ref"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


IL = _load("insight_ladder", HERE.parent / "scripts" / "insight_ladder.py")
sys.path.insert(0, str(REF))
WAP = _load("write_answer_page", REF / "write_answer_page.py")
QM = _load("question_map", REF / "question_map.py")
RJ = _load("run_job", REF / "run_job.py")


def L(*args):
    return IL.main([str(a) for a in args])


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) if m else {}


def _set(q: Path, **fields):
    text = q.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", text)
    f = yaml.safe_load(m.group(1))
    f.update(fields)
    q.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2), encoding="utf-8")


COMPUTE = {"kind": "compute", "what": "<what>", "pass": "<pass>", "cut": "the cell's partition", "unit": "<unit>",
           "measure": "<measure>", "by": "<by>", "uncertainty": "none", "rivals": "none",
           "output": {"counts.csv": ["level", "n"]}}


@pytest.fixture()
def board(tmp_path):
    (tmp_path / "env.sh").write_text("# the SPACE root of the test\n")
    p = tmp_path / "Project-Demo"
    proto, board = p / "work" / "Prototype-b01-Demo", p / "insight" / "Insight-Demo"
    L("prototype", proto, "--serves", "insight/Insight-Demo")
    L("version", proto, "--slug", "first")
    v = proto / "j01_p1_first"
    L("question", v, "D01", "counts")
    L("question", v, "X01", "the-line")
    d01, x01 = v / "t01_D01_counts", v / "t02_X01_the-line"
    _set(d01 / "question.md", agreed="✅ 261106", partitions={"asked": ["full"], "not_elsewhere": "<why>", "power": "none"},
         needs={"E1": COMPUTE})
    _set(x01 / "question.md", agreed="✅ 261106", partitions={"asked": ["full"], "not_elsewhere": "<why>", "power": "none"},
         needs={"E1": {"kind": "cite", "what": "<the counts>", "from": "D01.E1"},
                "E2": {"kind": "judge", "what": "<the line>", "from": ["E1"]}})
    (d01 / "scripts").mkdir()
    (d01 / "scripts" / "counts.py").write_text(
        'import pandas as pd\nSPEC = "D01"\nCOLUMNS = ["arm"]\n\n\ndef run(df, ctx):\n'
        '    c = df["arm"].value_counts().sort_index()\n'
        '    return {"counts.csv": pd.DataFrame({"level": list(c.index), "n": list(c.values)})}\n')
    (v / "partitions.md").write_text("---\npartitions:\n- {name: full, where: [], why: every row}\n"
                                     "- {name: small, where: [{column: arm, eq: A}], why: <why>}\n---\n")
    L("sign", v, "--date", "261106")
    data = p / "insight" / "Insight-Demo-data" / "v1"
    data.mkdir(parents=True)
    pd.DataFrame({"arm": ["A", "B"] * 30}).to_parquet(data / "demo.parquet", index=False)
    L("board", board, "--dataset", "Demo", "--prototype", "work/Prototype-b01-Demo")
    L("data", board, "v1", "--data-folder", data.relative_to(tmp_path).as_posix() + "/")
    L("job", board, "--release", "p1", "--data", "v1")
    job = board / "j01_prototype-p1-first_data-Demov1"
    assert RJ.run(job / "t01_D01_counts", "r01_full")["status"] == "ok"
    return proto, board, job


def _spec(**over):
    spec = {"answer-status": "answered", "answer": "Both arms hold thirty rows.", "how-sure": "exact counts",
            "opening": ["The two arms are the same size."],
            "divisions": [{"partition": "full", "takeaway": "Thirty rows in each arm.",
                           "bullets": [{"draft": "Arm A and arm B each hold 30 rows", "file": "counts.csv"}]}]}
    spec.update(over)
    return spec


def test_a_board_task_page_is_written_from_its_spec(board):
    _, _, job = board
    task = job / "t01_D01_counts"
    assert WAP._board_task(task)
    WAP.build_task_page(task, _spec())
    face = _front(task / f"{task.name}.md")
    assert face["question"] == "D01" and face["answer-status"] == "answered" and face["check"] == ""
    assert face["takeaways"] == {"full": "Thirty rows in each arm."}
    body = (task / f"{task.name}.md").read_text(encoding="utf-8")
    assert "## Full" in body and "(r01_full · counts.csv)." in body and "**The ask**" in body


def test_a_page_cites_only_what_its_runs_wrote(board):
    _, _, job = board
    task = job / "t01_D01_counts"
    bad = _spec(divisions=[{"partition": "full", "takeaway": "x", "bullets": [{"draft": "y", "file": "nope.csv"}]}])
    with pytest.raises(SystemExit, match="no such table"):
        WAP.build_task_page(task, bad)
    with pytest.raises(SystemExit, match="one division per hard Run"):
        WAP.build_task_page(task, _spec(divisions=[]))


def test_an_executive_page_cites_a_question_of_its_job(board):
    _, _, job = board
    task = job / "t02_X01_the-line"
    spec = _spec(figures=[{"name": "counts", "title": "<outcome>", "kind": "bars",
                           "table": "t01_D01_counts/runs/r01_full/result/counts.csv", "label": "level", "value": "n"}],
                 divisions=[{"title": "What it rests on", "bullets": [{"draft": "The counts per arm", "cite": "D01"}]}])
    WAP.build_task_page(task, spec)
    face = _front(task / f"{task.name}.md")
    assert face["figures"][0]["name"] == "counts" and "takeaways" not in face
    assert "(D01 · t01)." in (task / f"{task.name}.md").read_text(encoding="utf-8")
    with pytest.raises(SystemExit, match="is not a question"):
        WAP.build_task_page(task, _spec(divisions=[{"title": "x", "bullets": [{"draft": "y", "cite": "K09"}]}]))


def test_the_question_map_draws_a_release_with_its_executive_level(board, tmp_path):
    proto, _, _ = board
    out = tmp_path / "s01-question-map" / "s01-question-map.excalidraw"
    assert QM.main(["question_map.py", str(proto), "--out", str(out)]) == 0
    scene = json.loads(out.read_text(encoding="utf-8"))
    frames = [e["name"] for e in scene["elements"] if e["type"] == "frame"]
    assert any(f.startswith("Executive") for f in frames) and any(f.startswith("Data") for f in frames)
    assert any(e["type"] == "arrow" and e["id"] == "use-D01-X01" for e in scene["elements"])


def test_an_executive_figure_lands_under_its_task(board):
    """overall_report.py draws each Executive figure into its Task's part of the Job's delivery (haipipe-delivery: a
    Task's output sits under its address), and removes an older figures/ folder."""
    _, board_dir, job = board
    task = job / "t02_X01_the-line"
    WAP.build_task_page(task, _spec(figures=[{"name": "counts", "title": "<outcome>", "kind": "bars",
                                              "table": "t01_D01_counts/runs/r01_full/result/counts.csv",
                                              "label": "level", "value": "n"}],
                                    divisions=[{"title": "Answer", "bullets": [{"draft": "The counts", "cite": "D01"}]}]))
    OR = _load("overall_report", REF / "overall_report.py")
    out = board_dir / "delivery" / job.name
    (out / "figures").mkdir(parents=True)
    got = OR.figures(job, out)
    assert [p.relative_to(out).as_posix() for _, p in got["X01"]] == ["t02_X01_the-line/X01-counts.png"]
    assert not (out / "figures").exists()
