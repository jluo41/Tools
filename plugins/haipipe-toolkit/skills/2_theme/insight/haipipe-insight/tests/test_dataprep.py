"""The DataPrep Block holds code; a Board runs it and makes its own data version (ref/dataprep.md; JL 261120).

A placeholder SPACE is built in a temp folder through scripts/insight_ladder.py: a DataPrep Block whose prep version is
a chain of three steps (experiment, source, prepare), a Board whose raw export they read, and a data Job whose Runs
ref/run_prep.py runs in order, the last step's folder becoming the Board's data-v1. No real names and no data.
"""
import importlib.util
import re
import shutil
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("insight_ladder", HERE.parent / "scripts" / "insight_ladder.py")
IL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IL)
_rspec = importlib.util.spec_from_file_location("run_prep", HERE.parent / "ref" / "run_prep.py")
RP = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(RP)

EXPERIMENT = '''import json
def run(ctx):
    (ctx.out / "experiment_card.json").write_text(json.dumps({"settings": {}, "time": {}, "stated": "nothing stated"}))
    (ctx.out / "experiment_card.md").write_text("# experiment card\\n")
'''
SOURCE = '''def run(ctx):
    rows = (ctx.raw / "rows.csv").read_text()
    (ctx.out / "rows.csv").write_text(rows)
'''
PREPARE = '''def run(ctx):
    rows = (ctx.prev / "rows.csv").read_text().splitlines()
    (ctx.out / "data.csv").write_text("\\n".join(rows) + "\\n")
    (ctx.out / "data_dictionary.csv").write_text("name,dtype,null_pct\\narm,str,0\\n")
    (ctx.out / "cut.txt").write_text(str(sorted(ctx.cut.items())) + str(sorted(ctx.refs)))
    (ctx.out / "params.txt").write_text(str(sorted(ctx.params.items())))
'''


def L(*args):
    return IL.main([str(a) for a in args])


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) if m else {}


def _agree(step: Path) -> None:
    md = step / "step.md"
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", md.read_text(encoding="utf-8"))
    f = yaml.safe_load(m.group(1))
    f["agreed"] = "✅ 261120"
    md.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2), encoding="utf-8")


def _signed_prep(prep: Path, scripts=(("experiment", EXPERIMENT), ("source", SOURCE), ("prepare", PREPARE))) -> Path:
    L("prep", prep, "--slug", "first")
    ver = prep / "j01_prep-v1_first"
    for name, code in scripts:
        L("step", ver, name)
        step = next(s for s in IL.PR.steps(ver) if s.name.endswith("_" + name))
        (step / "scripts" / f"{name}.py").write_text(code)
        _agree(step)
    L("sign", ver, "--date", "261120")
    return ver


@pytest.fixture()
def space(tmp_path):
    (tmp_path / "env.sh").write_text("")                                      # the SPACE marker
    raw = tmp_path / "_WorkSpace" / "raw" / "demo_a"
    raw.mkdir(parents=True)
    (raw / "rows.csv").write_text("arm,clicked\nA,1\nB,0\n")
    p = tmp_path / "examples" / "Project-Demo"
    prep = p / "insight" / "InsightDataPrep-DemoSet"
    L("dataprep", prep, "--set", "DemoSet", "--serves", "insight/Insight-Demo", "--store", "_WorkSpace/stage")
    L("prototype", p / "insight" / "InsightQuestionBook-Demo", "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    return tmp_path, p, prep, board


def test_a_dataprep_block_is_named_placed_and_unversioned(tmp_path):
    p = tmp_path / "Project-Demo"
    with pytest.raises(SystemExit, match="lives in <Project>/insight/"):
        L("dataprep", p / "work" / "InsightDataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="InsightDataPrep-<Set>"):
        L("dataprep", p / "insight" / "DataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="carrying no version"):
        L("dataprep", p / "insight" / "InsightDataPrep-DemoSet", "--set", "DemoSetv1")


def test_a_prep_version_is_code_only_and_signed_when_agreed(space):
    _, p, prep, _ = space
    assert "datasets" not in _front(prep / "board.md")
    with pytest.raises(SystemExit, match="its Board's raw"):
        L("dataset", prep, "DemoA", "--raw", "_WorkSpace/raw/demo_a")
    L("prep", prep, "--slug", "first")
    ver = prep / "j01_prep-v1_first"
    L("step", ver, "experiment", "--ask", "Write the experiment card from the raw export")
    step = ver / "t01_experiment"
    assert _front(step / "t01_experiment.md")["goal"] == "Write the experiment card from the raw export"
    assert _front(step / "step.md")["script"] == "experiment"
    assert "def run(ctx)" in (step / "scripts" / "experiment.py").read_text()
    assert not [r for r in (step / "runs").iterdir() if r.is_dir()]          # a step holds no Run
    with pytest.raises(SystemExit, match="not agreed yet"):
        L("sign", ver, "--date", "261120")
    rows = {r[1]: r[2] for r in IL.audit(prep, quiet=True)}
    assert rows == {"serves": 0, "references": 0, "scripts": 0, "records": 0, "agreed": 1, "hash": 0}
    _agree(step)
    L("sign", ver, "--date", "261120")
    face = _front(ver / f"{ver.name}.md")
    assert (face["state"], face["signed"]) == ("closed", "✅ 261120") and re.fullmatch(r"[0-9a-f]{12}", face["hash"])
    (step / "scripts" / "experiment.py").write_text("def run(ctx):\n    pass\n")    # changed after the signature
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["hash"] == 1


def test_a_new_prep_version_orders_its_steps_and_copies_code_only(space):
    _, p, prep, _ = space
    v1 = _signed_prep(prep)
    (v1 / "t03_prepare" / "notebooks").mkdir()
    (v1 / "t03_prepare" / "notebooks" / "r01_x.ipynb").write_text("{}")
    with pytest.raises(SystemExit, match="names each step once"):
        L("prep", prep, "--steps", "experiment,experiment")
    L("prep", prep, "--slug", "raw-only", "--steps", "experiment,source,clean,prepare")
    v2 = prep / "j02_prep-v2_raw-only"
    assert [s.name for s in IL.PR.steps(v2)] == ["t01_experiment", "t02_source", "t03_clean", "t04_prepare"]
    moved = v2 / "t04_prepare"
    assert (moved / "t04_prepare.md").is_file() and not (moved / "t03_prepare.md").exists()
    assert (moved / "scripts" / "prepare.py").read_text() == PREPARE and not (moved / "notebooks").exists()
    assert _front(moved / "step.md")["agreed"] == ""                           # a carried step is reviewed again


def test_a_board_runs_a_signed_prep_version_and_adds_its_data_version(space):
    root, p, prep, board = space
    with pytest.raises(SystemExit, match="not there"):
        L("datasource", board, "--raw", "_WorkSpace/raw/gone", "--dataprep", "insight/InsightDataPrep-DemoSet")
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet",
      "--cut", "end_date=2025-07-03", "--param", "source_fn=FnA")
    fm = _front(board / "board.md")
    assert (fm["raw"], fm["cut"], fm["params"]) == ("_WorkSpace/raw/demo_a", {"end_date": "2025-07-03"}, {"source_fn": "FnA"})
    L("prep", prep, "--slug", "first")
    with pytest.raises(SystemExit, match="not signed"):
        L("datajob", board, "--prep", "prep-v1")
    shutil.rmtree(prep / "j01_prep-v1_first")
    L("reference", prep, "area", "--path", "_WorkSpace/raw/demo_a/rows.csv", "--version", "v1")
    _signed_prep(prep)
    L("datajob", board, "--prep", "prep-v1")
    job = board / "j01_prep-v1-first_data-v1"
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet",
      "--param", "source_fn=FnB")                                             # after the Job opened: it keeps FnA
    assert _front(job / f"{job.name}.md")["params"] == {"source_fn": "FnA"}
    assert [t.name for t in sorted(job.iterdir()) if t.is_dir() and t.name.startswith("t")] == [
        "t01_experiment", "t02_source", "t03_prepare"]
    for t in ("t01_experiment", "t02_source", "t03_prepare"):
        assert (job / t / "runs" / "r01_demoa" / "run.sh").is_file()
    assert IL.level_of(job) == "datajob" and IL.level_of(job / "t02_source") == "datatask"
    assert RP.main([str(job)]) == 0
    for t in ("t01_experiment", "t02_source", "t03_prepare"):
        rt = yaml.safe_load((job / t / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
        assert rt["status"] == "done" and rt["prep"] == "prep-v1" and re.fullmatch(r"[0-9a-f]{64}", rt["script_sha256"])
        assert (job / t / "runs" / "r01_demoa" / "result" / "provenance" / "sha256.txt").is_file()
    assert (job / "t01_experiment" / "runs" / "r01_demoa" / "result" / "experiment_card.json").is_file()
    heavy = yaml.safe_load((job / "t02_source" / "runs" / "r01_demoa" / "result" / "heavy.yaml").read_text())
    assert heavy["heavy_dir"].startswith("_WorkSpace/ProjectResult/Project-Demo/insight/Insight-Demo/")
    ready = root / "_WorkSpace" / "stage" / "DemoA@prep-v1"
    assert (ready / "data.csv").is_file() and (ready / "experiment_card.json").is_file()
    assert (ready / "cut.txt").read_text() == "[('end_date', '2025-07-03')]['area']"
    assert (ready / "params.txt").read_text() == "[('source_fn', 'FnA')]"
    row = _front(board / "board.md")["versions"][0]
    assert (row["version"], row["folder"], row["prep"], row["made-by"]) == (
        "data-v1", "_WorkSpace/stage/DemoA@prep-v1/", "prep-v1", job.name)
    assert _front(job / f"{job.name}.md")["state"] == "closed"
    assert IL.DJ.next_number(board) == 2 and IL.DJ.next_data(board) == 2      # one count for every Job


def test_a_data_job_refuses_out_of_order_without_a_card_or_on_changed_code(space):
    root, p, prep, board = space
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet")
    ver = _signed_prep(prep, scripts=(("experiment", "def run(ctx):\n    pass\n"), ("source", SOURCE), ("prepare", PREPARE)))
    L("datajob", board, "--prep", "prep-v1")
    job = board / "j01_prep-v1-first_data-v1"
    assert RP.main([str(job / "t02_source"), "r01_demoa"]) == 0                  # refused: a refusal is an answer
    rt = yaml.safe_load((job / "t02_source" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert (rt["status"], rt["reason"]) == ("refused", "the earlier step, t01_experiment, has not finished")
    assert RP.main([str(job / "t01_experiment"), "r01_demoa"]) == 1              # failed: no experiment card
    rt = yaml.safe_load((job / "t01_experiment" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert rt["status"] == "failed" and "experiment card" in rt["reason"]
    (ver / "t01_experiment" / "scripts" / "experiment.py").write_text(EXPERIMENT)   # the signed code, edited
    RP.main([str(job / "t01_experiment"), "r01_demoa"])
    rt = yaml.safe_load((job / "t01_experiment" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert rt["status"] == "refused" and "not what this Job pinned" in rt["reason"]
    assert not _front(board / "board.md").get("versions")


def test_a_step_refuses_in_its_own_words_and_the_chain_stops(space):
    root, p, prep, board = space
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet")
    _signed_prep(prep, scripts=(("experiment", EXPERIMENT), ("source", 'def run(ctx):\n    ctx.refuse("thin: 2 rows")\n'),
                                ("prepare", PREPARE)))
    L("datajob", board, "--prep", "prep-v1")
    job = board / "j01_prep-v1-first_data-v1"
    assert RP.main([str(job)]) == 0
    rt = yaml.safe_load((job / "t02_source" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert (rt["status"], rt["reason"]) == ("refused", "thin: 2 rows")
    assert not (job / "t03_prepare" / "runs" / "r01_demoa" / "result" / "runtime.yaml").exists()   # the chain stopped


def test_a_ready_folder_dictionary_carries_no_record_value(space):
    root, p, prep, board = space
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet")
    leaky = PREPARE.replace("name,dtype,null_pct\\narm,str,0", "name,dtype,sample_value\\narm,str,A")
    assert leaky != PREPARE
    _signed_prep(prep, scripts=(("experiment", EXPERIMENT), ("source", SOURCE), ("prepare", leaky)))
    L("datajob", board, "--prep", "prep-v1")
    job = board / "j01_prep-v1-first_data-v1"
    assert RP.main([str(job)]) == 1
    rt = yaml.safe_load((job / "t03_prepare" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert rt["status"] == "failed" and "sample column" in rt["reason"]
    assert not _front(board / "board.md").get("versions")


def test_a_hand_named_data_version_names_a_signed_prep_version(space):
    root, p, prep, board = space
    L("datasource", board, "--raw", "_WorkSpace/raw/demo_a", "--dataprep", "insight/InsightDataPrep-DemoSet")
    (root / "_WorkSpace" / "stage" / "old_v1").mkdir(parents=True)
    with pytest.raises(SystemExit, match="not a signed prep version"):
        L("data", board, "data-v1", "--data-folder", "_WorkSpace/stage/old_v1/", "--prep", "prep-v1")
    _signed_prep(prep)
    L("data", board, "data-v1", "--data-folder", "_WorkSpace/stage/old_v1/", "--prep", "prep-v1")
    assert _front(board / "board.md")["versions"][0]["prep"] == "prep-v1"


def test_references_and_record_lines_are_audited(space):
    root, p, prep, _ = space
    L("reference", prep, "area", "--path", "_WorkSpace/raw/demo_a/rows.csv", "--version", "v1")
    L("reference", prep, "gone", "--path", "_WorkSpace/raw/none.csv", "--version", "v2")
    with pytest.raises(SystemExit, match="already a reference"):
        L("reference", prep, "area", "--path", "x", "--version", "v1")
    L("prep", prep)
    ver = prep / "j01_prep-v1"
    L("step", ver, "prepare")
    (ver / "t01_prepare" / "scripts" / "prepare.py").write_text(
        "def run(ctx):\n    top = df['s'].value_counts().head(5)\n    first = df['x'].head(1)\n    d = {'sample_value': 1}\n")
    assert [w for w, _ in IL.PR.records(ver)] == ["t01_prepare/scripts/prepare.py:3", "t01_prepare/scripts/prepare.py:4"]
    rows = {r[1]: r[2] for r in IL.audit(prep, quiet=True)}
    assert (rows["references"], rows["records"]) == (1, 2)
