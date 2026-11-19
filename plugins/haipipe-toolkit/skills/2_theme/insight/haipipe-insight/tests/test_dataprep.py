"""The DataPrep Block makes a Set's data versions (ref/dataprep.md; workbench-insight topic T10).

A placeholder Project is built in a temp folder through scripts/insight_ladder.py: a DataPrep Block, its first prep
version carried from a work Task, a step and its dataset Runs, the signature, the next prep version, and a Board whose
data version names the signed prep version that made it. No real names and no data: every value is a placeholder.
"""
import importlib.util
import re
import subprocess
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("insight_ladder", HERE.parent / "scripts" / "insight_ladder.py")
IL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IL)


def L(*args):
    return IL.main([str(a) for a in args])


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) if m else {}


def _agree(step: Path) -> None:
    md = step / f"{step.name}.md"
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", md.read_text(encoding="utf-8"))
    f = yaml.safe_load(m.group(1))
    f["agreed"] = "✅ 261116"
    md.write_text("---\n" + yaml.safe_dump(f, sort_keys=False, allow_unicode=True) + "---\n" + m.group(2), encoding="utf-8")


def _card(run: Path) -> None:
    """What a first step's Run writes in its Result (rule 7): the experiment card, aggregates only."""
    (run / "result").mkdir(parents=True, exist_ok=True)
    (run / "result" / "experiment_card.json").write_text('{"settings": {}, "time": {}}')
    (run / "result" / "experiment_card.md").write_text("# experiment card\n")


@pytest.fixture()
def space(tmp_path):
    p = tmp_path / "examples" / "Project-Demo"
    prep = p / "insight" / "InsightDataPrep-DemoSet"
    L("dataprep", prep, "--set", "DemoSet", "--serves", "insight/Insight-Demo", "--store", "_WorkSpace/<store>")
    return tmp_path, p, prep


def test_a_dataprep_block_is_named_placed_and_unversioned(tmp_path):
    p = tmp_path / "Project-Demo"
    with pytest.raises(SystemExit, match="lives in <Project>/insight/"):
        L("dataprep", p / "work" / "InsightDataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="InsightDataPrep-<Set>"):
        L("dataprep", p / "insight" / "DataPrep-DemoSet", "--set", "DemoSet")
    with pytest.raises(SystemExit, match="carrying no version"):
        L("dataprep", p / "insight" / "InsightDataPrep-DemoSet", "--set", "DemoSetv1")
    with pytest.raises(SystemExit, match="never absolute"):
        L("dataprep", p / "insight" / "InsightDataPrep-DemoSet", "--set", "DemoSet", "--store", "/abs/store")


def test_prep_versions_steps_runs_and_the_signature(space):
    _, p, prep = space
    fm = _front(prep / "board.md")
    assert (fm["board-kind"], fm["set"], fm["serves"], fm["store"]) == (
        "insight-dataprep", "DemoSet", ["insight/Insight-Demo"], "_WorkSpace/<store>")
    assert fm["goal"] and (prep / "background" / "README.md").is_file()
    L("dataset", prep, "DemoA", "--raw", "_WorkSpace/<raw>/demo_a", "--why", "<why>")
    with pytest.raises(SystemExit, match="already a dataset"):
        L("dataset", prep, "DemoA", "--raw", "_WorkSpace/<raw>/demo_a")
    assert [d["name"] for d in _front(prep / "board.md")["datasets"]] == ["DemoA"]

    L("prep", prep, "--slug", "carried", "--from", "work/b01_demo/j01_prep/t01_prepare")
    v1 = prep / "j01_prep-v1_carried"
    face = _front(v1 / f"{v1.name}.md")
    assert (face["prep"], face["state"], face["carried-from"]) == ("prep-v1", "open", "work/b01_demo/j01_prep/t01_prepare")
    with pytest.raises(SystemExit, match="still open"):
        L("prep", prep, "--slug", "next")
    with pytest.raises(SystemExit, match="no step yet"):
        L("sign", v1, "--date", "261116")

    L("step", v1, "join", "--ask", "Join each dataset's raw tables into one row per message")
    step = v1 / "t01_join"
    assert IL.level_of(prep) == "dataprep" and IL.level_of(v1) == "prep" and IL.level_of(step) == "step"
    assert _front(step / "t01_join.md")["goal"] == "Join each dataset's raw tables into one row per message"
    L("run", step, "dataset", "demoa")
    L("run", step, "dataset", "demoa")                                          # the same dataset: the same Run
    run = step / "runs" / "r01_demoa"
    assert sorted(x.name for x in (step / "runs").iterdir() if x.is_dir()) == ["r01_demoa"]
    ticket = (run / "r01_demoa.sh").read_text(encoding="utf-8")
    assert 'TASK_NAME="join"' in ticket and "InsightDataPrep-*" in ticket
    card = yaml.safe_load((run / "run.yaml").read_text())
    assert (card["kind"], card["type"], card["prep"], card["status"]) == ("hard", "dataset", "prep-v1", "planned")
    cfg = yaml.safe_load((step / "scripts" / "config" / "r01_demoa.yaml").read_text())
    assert "env" not in cfg and "dataset" in cfg                          # the worker reads the file; no env: is exported
    assert cfg["output"]["prepare_dir"].startswith("_WorkSpace/<store>/") and cfg["output"]["prepare_dir"].endswith("@prep-v1")
    L("run", v1, "review-steps")
    review = yaml.safe_load((v1 / "runs" / "run-review-steps-prep-v1" / "run.yaml").read_text())
    assert review["agent"] == "haipipe-insight-reviewer-agent"           # the reviewer that may write agreed:

    with pytest.raises(SystemExit, match="not agreed yet"):
        L("sign", v1, "--date", "261116")
    _agree(step)
    L("sign", v1, "--date", "261116")
    face = _front(v1 / f"{v1.name}.md")
    assert (face["state"], face["signed"]) == ("closed", "✅ 261116") and re.fullmatch(r"[0-9a-f]{12}", face["hash"])
    with pytest.raises(SystemExit, match="signed and frozen"):
        L("step", v1, "cut")

    L("prep", prep, "--slug", "derive-fields")
    v2 = prep / "j02_prep-v2_derive-fields"
    assert _front(v2 / f"{v2.name}.md")["from"] == "prep-v1"
    assert (v2 / "t01_join" / "t01_join.md").is_file() and not (v2 / "t01_join" / "runs").exists()
    assert _front(v2 / "t01_join" / "t01_join.md")["agreed"] == ""          # a carried step is reviewed again
    assert yaml.safe_load((v2 / "t01_join" / "scripts" / "config" / "r01_demoa.yaml").read_text())[
        "output"]["prepare_dir"].endswith("@prep-v2")                        # re-aimed at the new version's folder


def test_a_board_data_version_names_the_signed_prep_that_made_it(space):
    _, p, prep = space
    L("prototype", p / "insight" / "InsightQuestionBook-Demo", "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    L("prep", prep, "--slug", "first")
    v1 = prep / "j01_prep-v1_first"
    L("step", v1, "join")
    L("run", v1 / "t01_join", "dataset", "demoa")
    _card(v1 / "t01_join" / "runs" / "r01_demoa")
    with pytest.raises(SystemExit, match="not signed"):
        L("data", board, "data-v1", "--data-folder", "_WorkSpace/<store>/demo_a_v1/", "--prep",
          "insight/InsightDataPrep-DemoSet/j01_prep-v1_first")
    _agree(v1 / "t01_join")
    L("sign", v1, "--date", "261116")
    L("run", v1 / "t01_join", "dataset", "demoa")
    L("data", board, "data-v1", "--data-folder", "_WorkSpace/<store>/demo_a_v1/", "--prep",
      "insight/InsightDataPrep-DemoSet/j01_prep-v1_first/t01_join/runs/r01_demoa")
    row = _front(board / "board.md")["versions"][0]
    assert row["prep"] == "insight/InsightDataPrep-DemoSet/j01_prep-v1_first/t01_join/runs/r01_demoa"
    rows = {r[1]: r[2] for r in IL.audit(board, quiet=True)}
    assert rows["prep"] == 0
    L("data", board, "data-v2", "--data-folder", "_WorkSpace/<store>/demo_a_v2/")      # made by hand: the audit names it
    rows = {r[1]: r[2] for r in IL.audit(board, quiet=True)}
    assert rows["prep"] == 1


def test_a_board_no_dataprep_serves_owes_no_prep_line(tmp_path):
    p = tmp_path / "Project-Demo"
    L("prototype", p / "insight" / "InsightQuestionBook-Demo", "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    L("data", board, "data-v1", "--data-folder", "_WorkSpace/<store>/demo_a_v1/")
    assert {r[1]: r[2] for r in IL.audit(board, quiet=True)}["prep"] == 0


def test_a_dataprep_in_another_project_serves_a_board_by_its_space_path(space):
    root, p, prep = space
    other = root / "examples-2" / "Project-Other"
    L("prototype", other / "insight" / "InsightQuestionBook-Other", "--serves", "insight/Insight-Other")
    board = other / "insight" / "Insight-Other"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Other")
    md = prep / "board.md"
    md.write_text(md.read_text(encoding="utf-8").replace(
        "- insight/Insight-Demo", "- insight/Insight-Demo\n- examples-2/Project-Other/insight/Insight-Other"), encoding="utf-8")
    assert IL.PR.serving(board) == [prep.resolve()]


def test_the_ticket_admits_a_dataprep_block_and_only_it_in_insight(space, tmp_path):
    _, p, prep = space
    L("prep", prep)
    step = prep / "j01_prep-v1"
    L("step", step, "join")
    L("run", step / "t01_join", "dataset", "demoa")
    (tmp_path / "env.sh").write_text("")                               # the SPACE marker the ticket walks up to
    out = subprocess.run(["bash", str(step / "t01_join" / "runs" / "r01_demoa" / "r01_demoa.sh")],
                         capture_output=True, text=True, timeout=60)
    assert "BLOCKED: Task worker missing" in out.stderr                # its shape passes; it stops at the absent script
    assert "join.py" in out.stderr                                     # the step's worker, named on its face
    bad = p / "insight" / "b01_other" / "j01_x" / "t01_y" / "runs" / "r01_z"
    bad.mkdir(parents=True)
    (bad.parent.parent / "t01_y.md").write_text("# t01_y\n")
    (bad / "r01_z.sh").write_text((step / "t01_join" / "runs" / "r01_demoa" / "r01_demoa.sh").read_text())
    out = subprocess.run(["bash", str(bad / "r01_z.sh")], capture_output=True, text=True, timeout=60)
    assert "Only a DataPrep Block runs Task tickets in insight/" in out.stderr


def test_a_run_never_writes_a_folder_made_before_and_audit_reads_the_block(space):
    _, p, prep = space
    L("prototype", p / "insight" / "InsightQuestionBook-Demo", "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    L("data", board, "data-v1", "--data-folder", "_WorkSpace/<store>/demo_a_v1/")      # a frozen folder, made by hand
    L("prep", prep, "--slug", "carried", "--from", "work/b01_demo/j01_prep")
    v1 = prep / "j01_prep-v1_carried"
    L("step", v1, "prepare")
    (v1 / "t01_prepare" / "scripts" / "prepare.py").write_text("# the carried worker\n")
    L("run", v1 / "t01_prepare", "dataset", "demoa")
    cfg = v1 / "t01_prepare" / "scripts" / "config" / "r01_demoa.yaml"
    cfg.write_text("env:\n  OUT_NAME: demo_a_v1\noutput:\n  prepare_dir: _WorkSpace/<store>/demo_a_v1\n")   # as carried
    _agree(v1 / "t01_prepare")
    rows = {r[1]: r[2] for r in IL.audit(prep, quiet=True)}
    assert rows == {"serves": 0, "raw": 0, "references": 0, "workers": 0, "configs": 0, "outputs": 2, "inputs": 0,
                    "records": 0, "card": 0, "notebooks": 0, "agreed": 0, "hash": 0}
    assert ("t01_prepare/r01_demoa", "_WorkSpace/<store>/demo_a_v1") in IL.PR.outputs(v1)
    with pytest.raises(SystemExit, match="a folder made before, or one a Board's data version names"):
        L("sign", v1, "--date", "261116")
    cfg.write_text("env:\n  OUT_NAME: demo_a_v1@prep-v1\noutput:\n  prepare_dir: _WorkSpace/<store>/demo_a_v1@prep-v1\n")
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["outputs"] == 0
    L("sign", v1, "--date", "261116")
    (v1 / "t01_prepare" / "scripts" / "prepare.py").write_text("# changed after the signature\n")
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["hash"] == 1
    md = prep / "board.md"
    md.write_text(md.read_text(encoding="utf-8").replace("- insight/Insight-Demo", "- insight/Insight-Gone"), encoding="utf-8")
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["serves"] == 1


def test_a_step_reads_only_its_raw_export_and_shows_no_record_value(space, tmp_path):
    root, p, prep = space
    (root / "_WorkSpace" / "raw" / "demo_a").mkdir(parents=True)
    L("dataset", prep, "DemoA", "--raw", "_WorkSpace/raw/demo_a")
    L("dataset", prep, "DemoGone", "--raw", "_WorkSpace/raw/gone")
    assert IL.PR.raw_gone(prep) == ["DemoGone"]                                 # an export that is not there
    L("prep", prep, "--slug", "raw-only")
    v1 = prep / "j01_prep-v1_raw-only"
    L("step", v1, "prepare")
    L("run", v1 / "t01_prepare", "dataset", "demoa")
    cfgdir = v1 / "t01_prepare" / "scripts" / "config"
    (cfgdir / "r02_other.yaml").write_text("dataset: DemoA\n")                 # names no folder of its own
    assert ("t01_prepare/r02_other", "names no output folder of its own") in IL.PR.outputs(v1)
    (cfgdir / "1_source_demo.yaml").write_text(                                # a shared source stage, as carried
        "SourceArgs:\n  raw_data_path: _WorkSpace/raw/demo_a\n  use_cache: true\n  save_cache: true\n")
    found = {why.split(":")[0] for _, why in IL.PR.inputs(v1)}
    assert found == {"SourceArgs.raw_data_path", "SourceArgs.use_cache", "SourceArgs.save_cache"}
    (v1 / "t01_prepare" / "scripts" / "prepare.py").write_text(
        "top = df['state'].value_counts().head(10)\n"                         # an aggregate: fine
        "first = df['x'].dropna().head(1).tolist()\n"                         # a record's value
        "row = {'name': c, 'sample_value': first}\n")
    result = v1 / "t01_prepare" / "runs" / "r01_demoa" / "result"
    result.mkdir(parents=True)
    (result / "data_dictionary.csv").write_text("column,dtype,sample_value\nx,int,3\n")
    where = sorted(w for w, _ in IL.PR.records(v1))
    assert where == ["t01_prepare/runs/r01_demoa/result/data_dictionary.csv", "t01_prepare/scripts/prepare.py:2",
                     "t01_prepare/scripts/prepare.py:3"]
    rows = {r[1]: r[2] for r in IL.audit(prep, quiet=True)}
    assert (rows["raw"], rows["outputs"], rows["inputs"], rows["records"]) == (1, 1, 3, 3)


def test_a_second_run_supersedes_the_newest_and_keeps_its_ticket_and_config(space):
    _, p, prep = space
    L("prep", prep, "--slug", "carried")
    v1 = prep / "j01_prep-v1_carried"
    L("step", v1, "prepare")
    step = v1 / "t01_prepare"
    L("run", step, "dataset", "demoa")
    first = step / "runs" / "r01_demoa"
    (first / "r01_demoa.sh").write_text((first / "r01_demoa.sh").read_text() + "# a carried line\n")
    (step / "scripts" / "config" / "r01_demoa.yaml").write_text("dataset: DemoA\noutput:\n  prepare_dir: s/a@prep-v1\n")
    L("run", step, "dataset", "demoa")                                         # no --again: the same Run back
    assert not (step / "runs" / "r02_demoa").exists()
    L("run", step, "dataset", "demoa", "--again")
    second = step / "runs" / "r02_demoa"
    card = yaml.safe_load((second / "run.yaml").read_text())
    assert (card["supersedes"], card["status"], card["prep"]) == ("r01_demoa", "planned", "prep-v1")
    assert (second / "r02_demoa.sh").read_text().endswith("# a carried line\n")      # the carried ticket, kept
    assert (step / "scripts" / "config" / "r02_demoa.yaml").read_text() == (
        step / "scripts" / "config" / "r01_demoa.yaml").read_text()
    L("run", step, "dataset", "demoa", "--again")
    assert yaml.safe_load((step / "runs" / "r03_demoa" / "run.yaml").read_text())["supersedes"] == "r02_demoa"


def test_a_reference_names_its_version_and_is_there(space):
    root, p, prep = space
    (root / "_WorkSpace" / "ext").mkdir(parents=True)
    (root / "_WorkSpace" / "ext" / "area.csv").write_text("code,area\n")
    L("reference", prep, "area", "--path", "_WorkSpace/ext/area.csv", "--version", "v1", "--why", "<why>")
    with pytest.raises(SystemExit, match="already a reference"):
        L("reference", prep, "area", "--path", "_WorkSpace/ext/area.csv", "--version", "v1")
    with pytest.raises(SystemExit, match="--version"):
        L("reference", prep, "prescriber", "--path", "_WorkSpace/ext/p.csv")
    L("reference", prep, "prescriber", "--path", "_WorkSpace/ext/gone.csv", "--version", "v2")
    assert [r["name"] for r in _front(prep / "board.md")["references"]] == ["area", "prescriber"]
    assert IL.PR.references_off(prep) == ["prescriber"]
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["references"] == 1


def test_a_data_version_whose_dictionary_holds_record_values_is_named(tmp_path):
    p = tmp_path / "Project-Demo"
    L("prototype", p / "insight" / "InsightQuestionBook-Demo", "--serves", "insight/Insight-Demo")
    board = p / "insight" / "Insight-Demo"
    L("board", board, "--dataset", "DemoA", "--prototype", "insight/InsightQuestionBook-Demo")
    for ver, header in (("v1", "name,dtype,sample_value"), ("v2", "name,dtype,n_unique")):
        folder = tmp_path / "_WorkSpace" / "store" / ver
        folder.mkdir(parents=True)
        (folder / "data_dictionary.csv").write_text(header + "\n", encoding="utf-8")
        L("data", board, f"data-{ver}", "--data-folder", f"_WorkSpace/store/{ver}/")
    assert IL.version_records(board) == ["data-v1"]                            # frozen, so named, never edited
    assert {r[1]: r[2] for r in IL.audit(board, quiet=True)}["records"] == 1


def test_a_new_prep_version_names_its_step_order(space):
    _, p, prep = space
    L("prep", prep, "--slug", "carried", "--from", "work/b01_demo/j01_prep")
    v1 = prep / "j01_prep-v1_carried"
    L("step", v1, "prepare-cohort")
    L("step", v1, "compare-cohorts")
    L("step", v1, "old-extra")
    L("run", v1 / "t01_prepare-cohort", "dataset", "demoa")
    L("run", v1 / "t01_prepare-cohort", "dataset", "demoa", "--again")      # its config is r02_demoa.yaml
    (v1 / "t01_prepare-cohort" / "scripts" / "config" / "r02_demoa.yaml").write_text(
        "dataset: DemoA\noutput:\n  prepare_dir: s/demo_a@prep-v1\n")
    for s_ in (v1 / "t01_prepare-cohort", v1 / "t02_compare-cohorts", v1 / "t03_old-extra"):
        _agree(s_)
    L("sign", v1, "--date", "261119")
    with pytest.raises(SystemExit, match="names each step once"):
        L("prep", prep, "--steps", "experiment,experiment")
    L("prep", prep, "--slug", "raw-only", "--steps", "experiment,source,prepare-cohort,compare-cohorts")
    v2 = prep / "j02_prep-v2_raw-only"
    assert [s_.name for s_ in IL.PR.steps(v2)] == ["t01_experiment", "t02_source", "t03_prepare-cohort",
                                                    "t04_compare-cohorts"]       # old-extra left out
    moved = v2 / "t03_prepare-cohort"
    assert (moved / "t03_prepare-cohort.md").is_file() and not (moved / "t01_prepare-cohort.md").exists()
    assert _front(moved / "t03_prepare-cohort.md")["step"] == "prepare-cohort"
    assert "# t03_prepare-cohort" in (moved / "t03_prepare-cohort.md").read_text()
    assert _front(moved / "t03_prepare-cohort.md")["agreed"] == "" and not (moved / "runs" / "r02_demoa").exists()
    assert _front(v2 / "t01_experiment" / "t01_experiment.md")["step"] == "experiment"   # a new step, empty
    L("run", moved, "dataset", "demoa")                                           # the carried config becomes r01's
    cfg = moved / "scripts" / "config"
    assert sorted(c.name for c in cfg.glob("r*.yaml")) == ["r01_demoa.yaml"]
    assert yaml.safe_load((cfg / "r01_demoa.yaml").read_text())["output"]["prepare_dir"] == "s/demo_a@prep-v2"


def test_a_new_version_signs_on_its_experiment_cards_and_leaves_notebooks_behind(space):
    _, p, prep = space
    L("prep", prep, "--slug", "carried", "--from", "work/b01_demo/j01_prep")
    v1 = prep / "j01_prep-v1_carried"
    L("step", v1, "prepare")
    L("run", v1 / "t01_prepare", "dataset", "demoa")
    nb = v1 / "t01_prepare" / "notebooks"
    nb.mkdir()
    for name in ("_source.ipynb", "r01_demoa.ipynb", "r07_pruned.ipynb"):            # r07's Run is gone
        (nb / name).write_text("{}")
    assert IL.PR.notebooks_orphan(v1) == ["t01_prepare/notebooks/r07_pruned.ipynb"]
    assert IL.PR.cards_missing(v1) == []                                             # carried: no card owed
    _agree(v1 / "t01_prepare")
    L("sign", v1, "--date", "261119")
    L("prep", prep, "--slug", "raw-only", "--steps", "experiment,prepare")
    v2 = prep / "j02_prep-v2_raw-only"
    assert not (v2 / "t02_prepare" / "notebooks").exists()                           # the Runs' notebooks stay behind
    assert IL.PR.cards_missing(v2) == ["t01_experiment: no Run yet"]
    L("run", v2 / "t01_experiment", "dataset", "demoa")
    for s_ in IL.PR.steps(v2):
        _agree(s_)
    with pytest.raises(SystemExit, match="experiment card"):
        L("sign", v2, "--date", "261120")
    _card(v2 / "t01_experiment" / "runs" / "r01_demoa")
    assert {r[1]: r[2] for r in IL.audit(prep, quiet=True)}["card"] == 0
    L("sign", v2, "--date", "261120")
    assert _front(v2 / f"{v2.name}.md")["state"] == "closed"
