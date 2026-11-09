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
    proto, board = p / "insight" / "Prototype-Demo", p / "insight" / "Insight-Demo"
    L("prototype", proto, "--serves", "insight/Insight-Demo")
    L("version", proto)
    L("question", proto / "j01_code-v1", "D01", "extract-shape")
    L("question", proto / "j01_code-v1", "I01", "rates-by-cut")
    return p, proto, board


def test_a_release_folder_says_what_it_is(tmp_path):
    """jNN_pN_<slug> (JL 261008); the release id stays pN, and a Board Job pins it by that id."""
    p = tmp_path / "Project-Demo"
    proto, board = p / "insight" / "Prototype-Demo", p / "insight" / "Insight-Demo"
    L("prototype", proto, "--serves", "insight/Insight-Demo")
    L("version", proto, "--slug", "first-questions")
    v = proto / "j01_code-v1_first-questions"
    assert _front(v / "j01_code-v1_first-questions.md")["release"] == "code-v1"
    L("question", v, "D01", "extract-shape")
    _agree_and_need(v)
    _cuts(v)
    L("sign", v, "--date", "261008")
    L("board", board, "--dataset", "Demo", "--prototype", "insight/Prototype-Demo")
    L("data", board, "data-v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    L("job", board, "--release", "code-v1", "--data", "data-v1")
    job = "j01_code-v1-first-questions_data-v1"                         # read left to right (JL 261012)
    face = _front(board / job / f"{job}.md")
    assert face["prototype"] == "insight/Prototype-Demo/j01_code-v1_first-questions"
    L("run", v / "t01_D01_extract-shape", "plan-evidence")
    assert (v / "t01_D01_extract-shape" / "runs" / "run-plan-evidence-d01" / "run.yaml").is_file()
    L("run", v, "set-cuts")
    assert (v / "runs" / "run-set-cuts-code-v1").is_dir()


def test_prototype_and_first_release(project):
    p, proto, _ = project
    assert _front(proto / "board.md") == {"board-kind": "prototype", "serves": "insight/Insight-Demo",
                                          "goal": "The questions and their scripts, one signed code version at a time"}
    v = proto / "j01_code-v1"
    assert _front(v / "j01_code-v1.md")["state"] == "open"
    rel = yaml.safe_load((v / "release.yaml").read_text())
    assert rel["questions"] == {"D01": {"task": "t01_D01_extract-shape", "change": "new"},
                                "I01": {"task": "t02_I01_rates-by-cut", "change": "new"}}
    q = _front(v / "t02_I01_rates-by-cut" / "question.md")
    assert (q["id"], q["level"], q["agreed"]) == ("I01", "information", "⬜")
    assert (proto / "proposals" / "README.md").is_file()


def test_sign_needs_agreed_questions_and_cuts(project):
    _, proto, _ = project
    v = proto / "j01_code-v1"
    with pytest.raises(SystemExit, match="not agreed"):
        L("sign", v, "--date", "261008")
    _agree_and_need(v)
    with pytest.raises(SystemExit, match="set the cuts"):
        L("sign", v, "--date", "261008")
    _cuts(v)
    L("sign", v, "--date", "261008")
    assert _front(v / "j01_code-v1.md")["signed"] == "✅ 261008"
    with pytest.raises(SystemExit, match="frozen"):
        L("question", v, "K01", "late")


def test_an_id_is_never_reused_and_a_question_keeps_its_task_number(project):
    _, proto, _ = project
    v1 = proto / "j01_code-v1"
    _agree_and_need(v1)
    _cuts(v1)
    L("sign", v1, "--date", "261008")
    L("version", proto)
    v2 = proto / "j02_code-v2"
    rel = yaml.safe_load((v2 / "release.yaml").read_text())
    assert rel["questions"]["D01"] == {"task": "../j01_code-v1/t01_D01_extract-shape", "change": "kept"}
    with pytest.raises(SystemExit, match="already in"):
        L("question", v2, "D01", "again")
    L("change", v2, "I01", "--why", "its script fixed")
    assert (v2 / "t02_I01_rates-by-cut" / "question.md").is_file()             # the same tNN, carried forward
    L("question", v2, "I02", "drop-off")
    assert (v2 / "t03_I02_drop-off").is_dir()
    L("retire", v2, "D01", "--why", "answered by I02")
    rel = yaml.safe_load((v2 / "release.yaml").read_text())
    assert "D01" not in rel["questions"] and rel["retired"] == {"D01": "answered by I02"}
    L("question", proto / "j02_code-v2", "D02", "new-shape")
    assert (v2 / "t04_D02_new-shape").is_dir()


def test_board_jobs_one_clock_and_the_reader(project):
    p, proto, board = project
    v1 = proto / "j01_code-v1"
    with pytest.raises(SystemExit, match="Insight-<name>"):
        L("board", p / "insights" / "topic", "--dataset", "Demo", "--prototype", "insight/Prototype-Demo")
    with pytest.raises(SystemExit, match="carrying no version"):
        L("board", board, "--dataset", "Demov1", "--prototype", "insight/Prototype-Demo")
    L("board", board, "--dataset", "Demo", "--prototype", "insight/Prototype-Demo")
    L("data", board, "data-v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    with pytest.raises(SystemExit, match="not signed"):
        L("job", board, "--release", "code-v1", "--data", "data-v1")
    _agree_and_need(v1)
    _cuts(v1)
    L("sign", v1, "--date", "261008")
    with pytest.raises(SystemExit, match="not a data version"):
        L("job", board, "--release", "code-v1", "--data", "data-v2")
    L("job", board, "--release", "code-v1", "--data", "data-v1")
    j1 = board / "j01_code-v1_data-v1"
    face = _front(j1 / "j01_code-v1_data-v1.md")
    assert (face["release"], face["data"], face["moved"], face["state"]) == ("code-v1", "data-v1", "start", "open")
    assert re.fullmatch(r"[0-9a-f]{12}", face["hash"])
    runs = sorted(r.name for r in (j1 / "t02_I01_rates-by-cut" / "runs").iterdir())
    assert runs == ["r01_full", "r02_part-a"]                                    # rNN = the cut's place
    assert (j1 / "t02_I01_rates-by-cut" / "runs" / "r01_full" / "run.sh").is_file()
    with pytest.raises(SystemExit, match="one Job per pair"):
        L("job", board, "--release", "code-v1", "--data", "data-v1")
    L("data", board, "data-v2", "--extract", "_WorkSpace/<store>/demo_v2.parquet")
    L("job", board, "--release", "code-v1", "--data", "data-v2")
    assert _front(board / "j02_code-v1_data-v2" / "j02_code-v1_data-v2.md")["moved"] == "data"
    L("version", proto)
    _agree_and_need(proto / "j02_code-v2")
    L("sign", proto / "j02_code-v2", "--date", "261008")
    with pytest.raises(SystemExit, match="one clock per Job"):
        L("job", board, "--release", "code-v2", "--data", "data-v1")
    L("job", board, "--release", "code-v2", "--data", "data-v2")
    assert _front(board / "j03_code-v2_data-v2" / "j03_code-v2_data-v2.md")["moved"] == "code"

    L("propose", proto, "a-cut", "--kind", "cut", "--from", "j02", "--why", "<why>")
    L("run", board, "coverage")
    L("run", board / "j03_code-v2_data-v2", "compare", "j02")
    L("run", board / "j03_code-v2_data-v2" / "t02_I01_rates-by-cut", "write")
    card = yaml.safe_load((board / "j03_code-v2_data-v2" / "t02_I01_rates-by-cut" / "runs" / "run-write-t02" /
                           "run.yaml").read_text())
    assert card["skill"] == "haipipe-insight-information"
    with pytest.raises(SystemExit, match="does not run at the board level"):
        L("run", board, "launch")

    sys.path.insert(0, str(READER))
    import insight_plan_c as C
    assert C.is_plan_c(board)
    b = C.board(board)
    assert [(j["name"], j["moved"]) for j in b["jobs"]] == [("j01_code-v1_data-v1", "start"), ("j02_code-v1_data-v2", "data"),
                                                           ("j03_code-v2_data-v2", "code")]
    assert [r["name"] for r in b["prototype"]["releases"]] == ["code-v1", "code-v2"]
    assert "a-cut" in [x["title"] for x in b["prototype"]["proposals"]]


def test_a_lower_case_dataset_job_is_still_a_job(project):
    """A Job on a lower-case dataset is a Job (its name carries no dataset since JL 261109), and so is one under either
    older name, j01_prototype-p1_data-demov1 (JL 261012) or j01_p1_demov1, which also fits a release's name; a Task
    under any of them is a Board Task."""
    p, proto, board = project
    v1 = proto / "j01_code-v1"
    L("board", board, "--dataset", "demo", "--prototype", "insight/Prototype-Demo")
    L("data", board, "data-v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet")
    _agree_and_need(v1)
    _cuts(v1)
    L("sign", v1, "--date", "261011")
    L("job", board, "--release", "code-v1", "--data", "data-v1")
    task = board / "j01_code-v1_data-v1" / "t02_I01_rates-by-cut"
    assert IL.level_of(task) == "task"
    assert IL.level_of(v1 / "t02_I01_rates-by-cut") == "question"
    L("run", task, "write", "t02")
    assert (task / "runs" / "run-write-t02" / "run.yaml").is_file()
    now = board / "j01_code-v1_data-v1"
    for older in ("j01_prototype-p1_data-demov1", "j01_p1_demov1"):            # the names before JL 261109
        (now / f"{now.name}.md").rename(now / f"{older}.md")
        now = now.rename(board / older)
        assert IL.level_of(now / "t02_I01_rates-by-cut") == "task"
        assert [j.name for j in IL.jobs(board)] == [older]


def test_a_need_draws_its_declared_figures(tmp_path):
    """A need's figures: list draws each figure from its table; a declared table gets no shape-based figure too."""
    import pandas as pd
    spec_f = importlib.util.spec_from_file_location("figures", HERE.parent / "ref" / "figures.py")
    F = importlib.util.module_from_spec(spec_f)
    spec_f.loader.exec_module(F)
    pd.DataFrame({"hour": range(24), "mean": [120 + h for h in range(24)], "code-v25": [110] * 24, "code-v75": [140] * 24}) \
        .to_csv(tmp_path / "by_hour.csv", index=False)
    pd.DataFrame({"event": ["a", "b"], "est": [1.0, -2.0], "est_lo": [0.0, -3.0], "est_hi": [2.0, -1.0]}) \
        .to_csv(tmp_path / "effects.csv", index=False)
    needs = {"E1": {"kind": "compute", "output": {"by_hour.csv": [], "effects.csv": []}, "figures": [
        {"table": "by_hour.csv", "kind": "line", "x": "hour", "y": "mean", "band": ["code-v25", "code-v75"], "hline": [180]},
        {"table": "effects.csv", "kind": "forest", "label": "event", "x": "est", "lo": "est_lo", "hi": "est_hi"},
        {"table": "missing.csv", "kind": "bar", "x": "a", "y": "b"}]}}
    made = F.draw(tmp_path, needs)
    files = sorted(m["file"] for m in made if m["file"])
    assert files == ["fig_E1_by_hour_1.png", "fig_E1_effects_2.png"]          # the estimate shape is not drawn again
    assert [m["problem"] for m in made if not m["file"]] == ["declared table not written"]
    assert all((tmp_path / f).stat().st_size > 1000 for f in files)


def test_dry_run_changes_nothing(tmp_path):
    p = tmp_path / "Project-Demo"
    made = L("prototype", p / "insight" / "Prototype-Demo", "--serves", "insight/Insight-Demo", "--dry-run")
    assert made and not (p / "tasks").exists()


def test_every_page_has_a_goal_line_and_goals_backfills_only_a_missing_one(tmp_path):
    """Each generator writes a face's `goal:` (the line a page's header shows, 261106); `goals` writes it into a face
    made before that line, from the same source, and never twice."""
    p = tmp_path / "Project-Demo"
    proto, board = p / "insight" / "Prototype-Demo", p / "insight" / "Insight-Demo"
    L("prototype", proto, "--serves", "insight/Insight-Demo", "--title", "the demo questions")
    L("version", proto, "--slug", "first-questions")
    v = proto / "j01_code-v1_first-questions"
    L("question", v, "D01", "extract-shape", "--ask", "How many rows does the demo extract hold?")
    t = v / "t01_D01_extract-shape"
    assert _front(t / f"{t.name}.md")["goal"] == "How many rows does the demo extract hold?"
    assert _front(v / f"{v.name}.md")["goal"].startswith("code-v1, first questions")
    _agree_and_need(v)
    _cuts(v)
    before = IL.release_hash(v)
    (t / f"{t.name}.md").unlink()                                   # a question made before its face
    L("goals", proto)
    assert _front(t / f"{t.name}.md")["goal"] == "How many rows does the demo extract hold?"
    assert IL.release_hash(v) == before                             # a face is the page's, never the plan's
    L("sign", v, "--date", "261008")
    L("board", board, "--dataset", "Demo", "--prototype", "insight/Prototype-Demo", "--title", "Insight · Demo: what it says")
    assert _front(board / "board.md")["goal"] == "What it says"
    L("data", board, "data-v1", "--extract", "_WorkSpace/<store>/demo_v1.parquet", "--label", "first days")
    L("job", board, "--release", "code-v1", "--data", "data-v1")
    job = board / "j01_code-v1-first-questions_data-v1"
    assert _front(job / f"{job.name}.md")["goal"] == "What the first questions (code-v1) find on data-v1, first days"
    task = job / "t01_D01_extract-shape"
    assert _front(task / f"{task.name}.md")["goal"] == "How many rows does the demo extract hold?"
    face = job / f"{job.name}.md"
    face.write_text(face.read_text().replace("goal: What the first", "goal: My own words for the first"))
    L("goals", board)
    assert _front(face)["goal"].startswith("My own words")          # a person's goal stays
    assert face.read_text().count("goal:") == 1


def test_update_carries_an_older_board_and_keeps_what_names_another_thing(tmp_path, capsys):
    """`update` (JL 261109) carries a Board and its Prototype from pN/vM and work/Prototype-bNN-<T>/ onto code-vN ×
    data-vM beside the Board: a dry run first, nothing written; then --apply. It never rewrites the data version's
    folder outside the Board, the Board's own name, a register board's name, a `renamed-from:` line, or a script's
    p1 variable, and it re-pins each Job's hash to its release."""
    p = tmp_path / "Project-Demo"
    proto, board = p / "work" / "Prototype-b01-Demo", p / "insight" / "Insight-Demov1"
    rel = proto / "j01_p1_extract"
    (rel / "t01_D01_shape" / "scripts").mkdir(parents=True)
    (proto / "board.md").write_text("---\nboard-kind: prototype\nserves: insight/Insight-Demov1\n"
                                    "renamed-from: Prototype-b01-Demoo   # old links still open\n---\n\n# Demo\n")
    (rel / "j01_p1_extract.md").write_text("---\nrelease: p1\nstate: closed\n---\n\n# p1 · the extract\n")
    (rel / "t01_D01_shape" / "question.md").write_text("---\nid: D01\n---\n\n# D01\n")
    (rel / "t01_D01_shape" / "scripts" / "shape.py").write_text("p1, p2 = 0.5, 0.4\nd = p1 - p2\n")
    (board).mkdir(parents=True)
    (board / "board.md").write_text(
        "---\nboard-kind: insight-board\nworkbench: insight\ndataset: Demo\nprototype: work/Prototype-b01-Demo\n"
        "versions:\n- version: v1\n  folder: _WorkSpace/store/20250101_Demov1/\n---\n\n# Insight · Demo\n\n"
        "Carried from Demo-InsightBoard. Data version v1 is at _WorkSpace/store/20250101_Demov1/.\n")
    job = board / "j01_prototype-p1-extract_data-Demov1"
    job.mkdir()
    (job / f"{job.name}.md").write_text("---\nrelease: p1\nprototype: work/Prototype-b01-Demo/j01_p1_extract\n"
                                        "data: v1\n---\n\n# p1 × v1\n")
    before = {f: f.read_bytes() for f in p.rglob("*") if f.is_file()}

    rows = IL.audit(p, quiet=True)
    assert [(r[1], r[2] > 0) for r in rows][0] == ("names", True)
    L("update", p)                                                                  # a dry run
    assert {f: f.read_bytes() for f in p.rglob("*") if f.is_file()} == before

    L("update", p, "--apply")
    new_proto = p / "insight" / "Prototype-Demo"
    new_rel, new_job = new_proto / "j01_code-v1_extract", board / "j01_code-v1-extract_data-v1"
    assert not proto.exists() and new_rel.is_dir() and new_job.is_dir() and board.is_dir()
    bf = _front(board / "board.md")
    assert bf["prototype"] == "insight/Prototype-Demo" and bf["versions"][0]["version"] == "data-v1"
    assert bf["versions"][0]["folder"] == "_WorkSpace/store/20250101_Demov1/"       # data outside the Board, kept
    body = (board / "board.md").read_text()
    assert "Demo-InsightBoard" in body and "data-v1 is at _WorkSpace/store/20250101_Demov1/" in body
    assert "renamed-from: Prototype-b01-Demoo" in (new_proto / "board.md").read_text()
    assert (new_rel / "t01_D01_shape" / "scripts" / "shape.py").read_text() == "p1, p2 = 0.5, 0.4\nd = p1 - p2\n"
    jf = _front(new_job / f"{new_job.name}.md")
    assert (jf["release"], jf["data"], jf["prototype"]) == ("code-v1", "data-v1",
                                                            "insight/Prototype-Demo/j01_code-v1_extract")
    assert jf["hash"] == IL.release_hash(new_rel) and jf.get("goal")
    assert all(n == 0 for _, check, n, _ in IL.audit(p, quiet=True) if check != "receipts")
