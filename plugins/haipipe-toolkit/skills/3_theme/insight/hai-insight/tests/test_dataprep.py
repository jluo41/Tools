"""DataPrep holds code; a Board Job pins three versions, data × prep × question (ref/dataprep.md; JL 261120).

A placeholder SPACE is built in a temp folder through scripts/insight_ladder.py: a DataPrep Block whose prep version is
a chain of three steps (experiment, source, prepare), a Question Book with one signed question, a Board whose data
version is a raw export with its cut and params, and a Job whose t01 runs the whole prep version in one Run
(ref/run_prep.py) and whose question Tasks read t01's ready folder (ref/run_job.py). No real names and no data.
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
    (ctx.result / "metrics.json").write_text('{"rows": 2}')
'''
PREPARE = '''def run(ctx):
    rows = (ctx.prev / "rows.csv").read_text().splitlines()
    (ctx.out / "demo.parquet").write_bytes(b"PAR1 placeholder")
    (ctx.out / "data_dictionary.csv").write_text("name,dtype,null_pct\\narm,str,0\\n")
    (ctx.out / "seen.txt").write_text(str(sorted(ctx.cut.items())) + str(sorted(ctx.params.items())) + str(sorted(ctx.refs)))
'''
DEFAULT = (("experiment", EXPERIMENT, (), ()), ("source", SOURCE, (), ("source_fn",)), ("prepare", PREPARE, ("end_date",), ()))


def L(*args):
    return IL.main([str(a) for a in args])


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) if m else {}


def _set(md: Path, **fields) -> None:
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", md.read_text(encoding="utf-8"))
    f = yaml.safe_load(m.group(1))
    f.update(fields)
    md.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2), encoding="utf-8")


def _signed_prep(prep: Path, steps=DEFAULT, slug="first") -> Path:
    L("prep", prep, "--slug", slug)
    ver = sorted(prep.glob("j*_prep-v*"))[-1]
    for name, code, cut, params in steps:
        L("step", ver, name)
        step = next(s for s in IL.PR.steps(ver) if s.name.endswith("_" + name))
        (step / "scripts" / f"{name}.py").write_text(code)
        _set(step / "step.md", cut=list(cut), params=list(params), agreed="✅ 261120")
    L("sign", ver, "--date", "261120")
    return ver


def _signed_release(proto: Path, n: int) -> None:
    """question-v<n> with one question, D01, agreed, its segments set, signed."""
    L("version", proto)
    ver = sorted(proto.glob("j*_question-v*"))[-1]
    if n == 1:
        L("question", ver, "D01", "extract-shape")
    for q in ver.glob("t*/question.md"):
        (q.parent / "scripts").mkdir(exist_ok=True)
        (q.parent / "scripts" / "extract_shape.py").write_text('SPEC = "D01"\n')      # its one entry script
        _set(q, agreed="✅ 261120", needs={"E1": {"kind": "compute", "what": "<what>", "pass": "<pass>",
             "cut": "the cell's partition", "unit": "<unit>", "measure": "<measure>", "by": "<by>",
             "uncertainty": "<interval>", "rivals": "none", "output": {"table.csv": ["<col>"]}}})
    (ver / "partitions.md").write_text("---\npartitions:\n- {name: full, where: []}\n---\n\n# The segments\n", encoding="utf-8")
    L("sign", ver, "--date", "261120")


@pytest.fixture()
def space(tmp_path):
    (tmp_path / "env.sh").write_text("")                                      # the SPACE marker
    raw = tmp_path / "_WorkSpace" / "raw" / "demo_a"
    raw.mkdir(parents=True)
    (raw / "rows.csv").write_text("arm,clicked\nA,1\nB,0\n")
    p = tmp_path / "examples" / "Project-Demo"
    prep = p / "insight" / "InsightDataPrep-DemoSet"
    L("dataprep", prep, "--set", "DemoSet", "--serves", "insight/Insight-Demo", "--store", "_WorkSpace/stage")
    proto = p / "insight" / "InsightQuestionBook-Demo"
    L("prototype", proto, "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    return tmp_path, p, prep, board, proto


def _ready_board(space, steps=DEFAULT):
    root, p, prep, board, proto = space
    L("datasource", board, "--dataprep", "insight/InsightDataPrep-DemoSet")
    L("data", board, "data-v1", "--raw", "_WorkSpace/raw/demo_a", "--cut", "end_date=2025-07-03", "--param", "source_fn=FnA")
    _signed_prep(prep, steps)
    _signed_release(proto, 1)
    L("job", board, "--data", "data-v1", "--prep", "prep-v1", "--release", "question-v1")
    return board / "j01_data-v1_prep-v1_question-v1"


def test_a_dataprep_block_is_named_placed_and_unversioned(tmp_path):
    p = tmp_path / "Project-Demo"
    with pytest.raises(SystemExit, match="lives in <Project>/insight/"):
        L("dataprep", p / "work" / "InsightDataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="InsightDataPrep-<Set>"):
        L("dataprep", p / "insight" / "DataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="carrying no version"):
        L("dataprep", p / "insight" / "InsightDataPrep-DemoSet", "--set", "DemoSetv1")


def test_a_step_is_its_spec_and_its_script_and_a_version_signs_when_agreed(space):
    _, p, prep, _, _ = space
    with pytest.raises(SystemExit, match="its Board's raw"):
        L("dataset", prep, "DemoA", "--raw", "_WorkSpace/raw/demo_a")
    L("prep", prep, "--slug", "first")
    ver = prep / "j01_prep-v1_first"
    L("step", ver, "experiment", "--ask", "Write the experiment card from the raw export")
    step = ver / "t01_experiment"
    assert sorted(x.name for x in step.iterdir()) == ["scripts", "step.md"]   # as a question: its spec and its script
    assert _front(step / "step.md")["goal"] == "Write the experiment card from the raw export"
    assert "def run(ctx)" in (step / "scripts" / "experiment.py").read_text()
    with pytest.raises(SystemExit, match="not agreed yet"):
        L("sign", ver, "--date", "261120")
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)} == {
        "serves": 0, "references": 0, "scripts": 0, "records": 0, "agreed": 1, "hash": 0}
    _set(step / "step.md", agreed="✅ 261120")
    L("sign", ver, "--date", "261120")
    face = _front(ver / f"{ver.name}.md")
    assert (face["state"], face["signed"]) == ("closed", "✅ 261120") and re.fullmatch(r"[0-9a-f]{12}", face["hash"])
    (step / "scripts" / "experiment.py").write_text("def run(ctx):\n    pass\n")    # changed after the signature
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["hash"] == 1


def test_a_new_prep_version_orders_its_steps_and_copies_code_only(space):
    _, p, prep, _, _ = space
    v1 = _signed_prep(prep)
    (v1 / "t03_prepare" / "t03_prepare.md").write_text("---\ngoal: an older face's goal\n---\n")   # an older step's face
    (v1 / "t03_prepare" / "notebooks").mkdir()
    (v1 / "t03_prepare" / "notebooks" / "r01_x.ipynb").write_text("{}")
    _set(v1 / "t03_prepare" / "step.md", goal="")
    _set(v1 / f"{v1.name}.md", hash=IL.PR.prep_hash(v1))
    with pytest.raises(SystemExit, match="names each step once"):
        L("prep", prep, "--steps", "experiment,experiment")
    L("prep", prep, "--slug", "raw-only", "--steps", "experiment,source,clean,prepare")
    v2 = prep / "j02_prep-v2_raw-only"
    assert [s.name for s in IL.PR.steps(v2)] == ["t01_experiment", "t02_source", "t03_clean", "t04_prepare"]
    moved = v2 / "t04_prepare"
    assert sorted(x.name for x in moved.iterdir()) == ["scripts", "step.md"]  # no face, no notebooks
    assert _front(moved / "step.md")["goal"] == "an older face's goal" and _front(moved / "step.md")["agreed"] == ""


def test_a_job_of_three_versions_runs_its_prep_then_its_questions_read_the_ready_folder(space):
    root, p, prep, board, proto = space
    L("reference", prep, "area", "--path", "_WorkSpace/raw/demo_a/rows.csv", "--version", "v1")
    job = _ready_board(space)
    row = _front(board / "board.md")["versions"][0]
    assert (row["raw"], row["cut"], row["params"]) == ("_WorkSpace/raw/demo_a", {"end_date": "2025-07-03"}, {"source_fn": "FnA"})
    assert [t.name for t in sorted(job.iterdir()) if t.is_dir() and t.name.startswith("t")] == [
        "t01_prep-v1_first", "t02_D01_extract-shape"]                         # D01 is t01 in the release
    face = _front(job / f"{job.name}.md")
    assert (face["data"], face["prep"], face["release"], face["moved"]) == ("data-v1", "prep-v1", "question-v1", "start")
    assert IL.level_of(job / "t01_prep-v1_first") == "preptask" and IL.level_of(job / "t02_D01_extract-shape") == "task"
    assert (job / "t02_D01_extract-shape" / "runs" / "r01_full" / "run.sh").is_file()
    sys_path = str(HERE.parent / "ref")
    import sys
    sys.path.insert(0, sys_path)
    import run_job as RJ
    with pytest.raises(Exception, match="ready folder is not made yet"):
        RJ.resolve(job / "t02_D01_extract-shape", "r01_full")
    assert RP.main([str(job)]) == 0
    result = job / "t01_prep-v1_first" / "runs" / "r01_demoa" / "result"
    rt = yaml.safe_load((result / "runtime.yaml").read_text())
    assert rt["status"] == "done" and [s["status"] for s in rt["steps"]] == ["done", "done", "done"]
    assert set(rt["scripts_sha256"]) == {"t01_experiment", "t02_source", "t03_prepare"}
    assert (result / "experiment_card.json").is_file() and (result / "provenance" / "sha256.txt").is_file()
    assert (result / "steps" / "t02_source" / "metrics.json").read_text() == '{"rows": 2}'
    heavy = yaml.safe_load((result / "heavy.yaml").read_text())["heavy"][0]["dir"]
    assert heavy.startswith("_WorkSpace/ProjectResult/Project-Demo/insight/Insight-Demo/") and heavy.endswith("t02_source")
    ready = root / "_WorkSpace" / "stage" / "DemoA_data-v1@prep-v1"
    assert (ready / "experiment_card.json").is_file()
    assert (ready / "seen.txt").read_text() == "[('end_date', '2025-07-03')][('source_fn', 'FnA')]['area']"
    assert _front(job / f"{job.name}.md")["ready"] == "_WorkSpace/stage/DemoA_data-v1@prep-v1/"
    r = RJ.resolve(job / "t02_D01_extract-shape", "r01_full")
    assert r["extract"] == "_WorkSpace/stage/DemoA_data-v1@prep-v1/demo.parquet"
    assert RP.main([str(job)]) == 0                                           # done already: never rerun
    _signed_release(proto, 2)
    L("job", board, "--data", "data-v1", "--prep", "prep-v1", "--release", "question-v2")
    j2 = board / "j02_data-v1_prep-v1_question-v2"
    f2 = _front(j2 / f"{j2.name}.md")
    assert (f2["moved"], f2["ready"]) == ("code", "_WorkSpace/stage/DemoA_data-v1@prep-v1/")   # the same ready folder
    assert yaml.safe_load((j2 / "t01_prep-v1_first" / "runs" / "r01_demoa" / "run.yaml").read_text())["status"] == "done"
    (root / "_WorkSpace" / "raw" / "demo_b").mkdir()
    L("data", board, "data-v2", "--raw", "_WorkSpace/raw/demo_b")
    with pytest.raises(SystemExit, match="one version per Job"):
        L("job", board, "--data", "data-v2", "--prep", "prep-v1", "--release", "question-v1")
    with pytest.raises(SystemExit, match="names its raw export already"):
        L("data", board, "data-v1", "--raw", "_WorkSpace/raw/demo_b")


def test_the_prep_run_stops_at_a_refusal_a_missing_card_or_changed_code(space):
    root, p, prep, board, proto = space
    refusing = (("experiment", EXPERIMENT, (), ()), ("source", 'def run(ctx):\n    ctx.refuse("thin: 2 rows")\n', (), ("source_fn",)),
                ("prepare", PREPARE, ("end_date",), ()))
    job = _ready_board(space, refusing)
    assert RP.main([str(job)]) == 0
    rt = yaml.safe_load((job / "t01_prep-v1_first" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert (rt["status"], rt["reason"]) == ("refused", "t02_source: thin: 2 rows") and len(rt["steps"]) == 2
    assert "ready" not in _front(job / f"{job.name}.md")
    ver = prep / "j01_prep-v1_first"
    (ver / "t01_experiment" / "scripts" / "experiment.py").write_text("def run(ctx):\n    pass\n")   # signed code, edited
    RP.main([str(job)])
    rt = yaml.safe_load((job / "t01_prep-v1_first" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert rt["status"] == "refused" and "not what this Job pinned" in rt["reason"]


def test_a_first_step_without_a_card_and_a_leaky_dictionary_fail(space):
    root, p, prep, board, proto = space
    leaky = PREPARE.replace("name,dtype,null_pct\\narm,str,0", "name,dtype,sample_value\\narm,str,A")
    assert leaky != PREPARE
    job = _ready_board(space, (("experiment", EXPERIMENT, (), ()), ("source", SOURCE, (), ("source_fn",)),
                               ("prepare", leaky, ("end_date",), ())))
    assert RP.main([str(job)]) == 1
    rt = yaml.safe_load((job / "t01_prep-v1_first" / "runs" / "r01_demoa" / "result" / "runtime.yaml").read_text())
    assert rt["status"] == "failed" and "sample column" in rt["reason"]
    assert "ready" not in _front(job / f"{job.name}.md")


def test_a_data_version_key_no_step_reads_is_refused(space):
    root, p, prep, board, proto = space
    L("datasource", board, "--dataprep", "insight/InsightDataPrep-DemoSet")
    L("data", board, "data-v1", "--raw", "_WorkSpace/raw/demo_a", "--cut", "end=2025-07-03")   # the step reads end_date
    _signed_prep(prep)
    _signed_release(proto, 1)
    with pytest.raises(SystemExit, match="no step of prep-v1 reads data-v1's cut end"):
        L("job", board, "--data", "data-v1", "--prep", "prep-v1", "--release", "question-v1")


def test_drop_datajob_undoes_a_job_of_the_withdrawn_shape(space):
    root, p, prep, board, proto = space
    old = board / "j02_prep-v1-raw-chain_data-v2"
    (old / "t01_experiment").mkdir(parents=True)
    (old / f"{old.name}.md").write_text("---\nprep: prep-v1\ndata: data-v2\n---\n")
    folder = root / "_WorkSpace" / "stage" / "DemoA@prep-v1"
    folder.mkdir(parents=True)
    (folder / "made-by.yaml").write_text(f"job: {old.name}\nprep: prep-v1\n")
    md = board / "board.md"
    fm = _front(md)
    fm["versions"] = [{"version": "data-v1", "folder": "_WorkSpace/b01/"},
                      {"version": "data-v2", "folder": "_WorkSpace/stage/DemoA@prep-v1/", "made-by": old.name}]
    md.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="withdrawn"):
        L("datajob", board, "--prep", "prep-v1")
    L("drop-datajob", old, "--dry-run")
    assert old.exists() and folder.exists() and len(_front(md)["versions"]) == 2      # a dry run removes nothing
    shutil.rmtree(old)                                                        # the Job folder already gone: its leftovers
    L("drop-datajob", old)
    assert not folder.exists()
    assert [v["version"] for v in _front(md)["versions"]] == ["data-v1"]


def test_a_hand_named_data_version_names_a_signed_prep_version(space):
    root, p, prep, board, proto = space
    L("datasource", board, "--dataprep", "insight/InsightDataPrep-DemoSet")
    (root / "_WorkSpace" / "stage" / "old_v1").mkdir(parents=True)
    with pytest.raises(SystemExit, match="not a signed prep version"):
        L("data", board, "data-v1", "--data-folder", "_WorkSpace/stage/old_v1/", "--prep", "prep-v1")
    _signed_prep(prep)
    L("data", board, "data-v1", "--data-folder", "_WorkSpace/stage/old_v1/", "--prep", "prep-v1")
    assert _front(board / "board.md")["versions"][0]["prep"] == "prep-v1"
    L("data", board, "data-v1", "--raw", "_WorkSpace/raw/demo_a")              # an older row gains its raw once
    assert _front(board / "board.md")["versions"][0]["raw"] == "_WorkSpace/raw/demo_a"


def test_references_and_record_lines_are_audited(space):
    root, p, prep, _, _ = space
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
