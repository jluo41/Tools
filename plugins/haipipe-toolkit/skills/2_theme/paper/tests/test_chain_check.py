"""haipipe-paper-evidence chain_check.py on tiny made-up paper Boards of both value-Job shapes (JL 261110):
a clean Board passes; each break gives its own FAIL line."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "haipipe-paper-evidence" / "scripts"))
import chain_check  # noqa: E402

DONE = "run: {}\nstatus: completed\nexit_code: 0\n"
WORK_RUN = "work/b01_example/j01_estimates/t01_main/runs/r01_main"


def write(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def done(run: Path) -> None:
    write(run / "result" / "runtime.yaml", DONE.format(run.name))


def project(tmp: Path) -> Path:
    proj = tmp / "Project-X"
    write(proj / "project.yaml", "name: Project-X\n")
    w = proj / WORK_RUN
    write(w / "result" / "values.csv", "key,value\nmain.b,2.3461\nmain.n,120\nmain.s,0.1\n")
    write(w / "result" / "metrics.json", json.dumps({"n": 120, "by": {"num": 60}}))
    done(w)
    board = proj / "paper" / "Paper-X"
    write(board / "board.md", "# Paper-X\n\nspine: one question\n")
    return board


def fails(board: Path, rule=None) -> list:
    got = chain_check.chain(board).fails
    return [f"FAIL {f['rule']} {f['where']}: {f['what']}" for f in got if rule is None or f["rule"] == rule]


# ── the copying shape ────────────────────────────────────────────────────────────────────────────────────────────────
VALUES = [{"id": "V_b", "says": "the difference", "from": "est/values.csv", "where": {"key": "main.b"}, "column": "value", "fmt": "{:.2f}"},
          {"id": "V_n", "says": "units", "from": "est/metrics.json", "key": "n", "fmt": "{:,.0f}"},
          {"id": "V_s", "says": "change per 10x", "from": "est/values.csv", "where": {"key": "main.s"}, "column": "value",
           "transform": "pct10", "fmt": "{:+.1f}%"}]


def value_run(task: Path, run: str, values=VALUES) -> Path:
    r = task / "runs" / run
    src = task.parents[3] / WORK_RUN / "result"           # task -> j02 -> Board -> paper -> Project
    for f in ("values.csv", "metrics.json"):
        write(r / "result" / "est" / f, (src / f).read_text(encoding="utf-8"))
    write(r / "result" / "est" / "SOURCE.txt", f"copied from Project-X/{WORK_RUN}/result\n")
    out = {}
    for v in values:
        x = chain_check.reread(v, src / v["from"].split("/", 1)[1])
        x = chain_check.TRANSFORM[v.get("transform")](x)
        out[v["id"]] = {"value": x, "text": v["fmt"].format(x), "says": v["says"], "source": "b01 ..."}
    write(r / "result" / "values.json", json.dumps(out))
    write(r / "run.yaml", yaml.safe_dump({"run": run, "reads": ["b01_example/j01_estimates/t01_main/runs/r01_main"]}))
    done(r)
    return r


def copying_board(tmp: Path) -> Path:
    board = project(tmp)
    j02 = board / "j02_evidence_value"
    write(j02 / "src" / "gen_runs.py", 'RUN = "r02_collect_values"\n')
    task = j02 / "t01_values-main"
    write(task / "scripts" / "values.yaml", yaml.safe_dump(
        {"sources": [{"key": "est", "run": "j01_estimates/t01_main/runs/r01_main", "files": ["values.csv", "metrics.json"]}],
         "values": VALUES}, sort_keys=False))
    value_run(task, "r01_collect_values")
    value_run(task, "r02_collect_values")
    disp = board / "j01_evidence_display" / "t01_figure1"
    write(disp / "t01_figure1.md", "# t01_figure1\n\nprinted: r01_draw\n")
    r = disp / "runs" / "r01_draw"
    write(r / "run.yaml", yaml.safe_dump({"run": "r01_draw", "reads": [
        "j02_evidence_value/t01_values-main/runs/r02_collect_values/result/est"]}))
    write(r / "result" / "display.yaml", "value_run: r02_collect_values\n")
    write(r / "result" / "values_used.csv", "id,text,says,value_task\nV_b,2.35,the difference,t01_values-main\n")
    done(r)
    sec = board / "j11_writing_v1130_venue" / "t01_results"
    write(sec / "t01_results.md", "# t01_results\n\nquotes j02_evidence_value/t01_values-main/runs/r02_collect_values/result/values.json\n")
    return board


@pytest.fixture
def cboard():
    with tempfile.TemporaryDirectory() as tmp:
        yield copying_board(Path(tmp))


def test_a_clean_copying_board_passes(cboard, capsys):
    assert fails(cboard) == []
    assert chain_check.main([str(cboard)]) == 0
    assert "the chain holds" in capsys.readouterr().out.strip().splitlines()[-1]


def test_a_changed_copy(cboard):
    write(cboard / "j02_evidence_value/t01_values-main/runs/r02_collect_values/result/est/metrics.json", '{"n": 121}')
    assert any("est/metrics.json: the copy differs" in f for f in fails(cboard, 1))


def test_a_drifted_id(cboard):
    f = cboard / "j02_evidence_value/t01_values-main/runs/r02_collect_values/result/values.json"
    d = json.loads(f.read_text())
    d["V_b"].update(value=2.4, text="2.40")
    f.write_text(json.dumps(d))
    got = fails(cboard, 1)
    assert any("V_b: the work Run's file gives 2.35" in f for f in got), got


def test_a_stale_source_run(cboard):
    done(cboard.parents[1] / WORK_RUN.replace("r01_main", "r02_main"))
    assert any("stale: reads r01_main" in f and "r02_main" in f for f in fails(cboard, 6))


def test_an_incomplete_source_run(cboard):
    write(cboard.parents[1] / WORK_RUN / "result" / "runtime.yaml", "status: failed\n")
    assert any("not complete (status failed)" in f for f in fails(cboard, 1))


def test_a_display_reading_work(cboard):
    card = cboard / "j01_evidence_display/t01_figure1/runs/r01_draw/run.yaml"
    d = yaml.safe_load(card.read_text())
    d["reads"].append(WORK_RUN + "/result/values.csv")
    card.write_text(yaml.safe_dump(d))
    assert any("reads work/ directly" in f for f in fails(cboard, 1))


def test_a_display_on_an_old_value_run(cboard):
    card = cboard / "j01_evidence_display/t01_figure1/runs/r01_draw/run.yaml"
    card.write_text(card.read_text().replace("r02_collect_values", "r01_collect_values"))
    got = fails(cboard, 6)
    assert any("stale: reads t01_values-main/r01_collect_values; the current value Run is r02_collect_values" in f for f in got)


def test_a_display_printing_a_drifted_number(cboard):
    write(cboard / "j01_evidence_display/t01_figure1/runs/r01_draw/result/values_used.csv",
          "id,text,says,value_task\nV_b,2.30,the difference,t01_values-main\nV_gone,1,x,t01_values-main\n")
    got = fails(cboard, 2)
    assert any("V_b: prints 2.30, the current value is 2.35" in f for f in got)
    assert any("V_gone: not an id of the current value Run" in f for f in got)


def test_a_flagged_id(cboard):
    f = cboard / "j02_evidence_value/t01_values-main/runs/r02_collect_values/result/values.json"
    d = json.loads(f.read_text())
    d["V_n"]["flag"] = "An older setup: check before quoting."
    f.write_text(json.dumps(d))
    assert any("V_n: marked to check before quoting" in f for f in fails(cboard, 5))


def test_a_section_naming_an_old_value_run(cboard):
    f = cboard / "j11_writing_v1130_venue/t01_results/t01_results.md"
    f.write_text(f.read_text().replace("r02_collect_values", "r01_collect_values"))
    assert any("t01_results.md: stale: names t01_values-main/r01_collect_values" in f for f in fails(cboard, 6))


def test_an_id_in_two_value_tasks(cboard):
    j02 = cboard / "j02_evidence_value"
    shutil.copytree(j02 / "t01_values-main", j02 / "t02_values-again")
    assert any("V_b is in two value Tasks" in f for f in fails(cboard, 2))


def test_the_recompute_hook(cboard, capsys):
    hook = write(cboard / "scripts" / "recompute_check.py", "print('recomputed 3 numbers, 1 differs'); raise SystemExit(1)\n")
    assert any("the recompute check exited 1" in f for f in fails(cboard, 7))
    assert chain_check.main([str(cboard)]) == 1
    assert "  | recomputed 3 numbers, 1 differs" in capsys.readouterr().out
    hook.write_text("print('recomputed 3 numbers, all agree')\n")
    assert fails(cboard) == []


def test_json_output(cboard, capsys):
    write(cboard / "j01_evidence_display/t01_figure1/runs/r01_draw/run.yaml", "run: r01_draw\nreads: [" + WORK_RUN + "]\n")
    assert chain_check.main([str(cboard), "--json"]) == 1
    doc = json.loads(capsys.readouterr().out)
    assert [f["rule"] for f in doc["failures"]] == [1] and doc["summary"].startswith("chain_check Paper-X: 1 failure ")


# ── the value-map shape (values_ledger.py's own) ─────────────────────────────────────────────────────────────────────
def map_board(tmp: Path) -> Path:
    import values_ledger
    board = project(tmp)
    task = board / "j02_evidence_value" / "t01_values-main"
    write(task / "scripts" / "value_map.yaml", yaml.safe_dump(
        {"rq": "RQ1", "group": "the main association", "defaults": {"file": "values.csv", "column": "value"},
         "runs": {"main": WORK_RUN},
         "values": {"main.b": {"what": "difference", "run": "main", "where": {"key": "main.b"}, "digits": 2},
                    "main.n": {"what": "units", "run": "main", "where": {"key": "main.n"}}}}, sort_keys=False))
    run = task / "runs" / "r01_read_values"
    (run / "result").mkdir(parents=True)
    values_ledger.run(task, run / "result")
    done(run)
    sec = board / "j11_writing_v1130_venue" / "t01_results"
    write(sec / "t01_results.md", "# t01_results\n")
    write(sec / "evidence" / "cards.yaml", yaml.safe_dump({"evidence": [{"kind": "value", "source": "j02.t01", "items": [
        {"run": "r01", "for": ["1"], "value": "RQ1-t01-001", "anchor": ["2.35"]}]}]}))
    return board


@pytest.fixture
def mboard():
    with tempfile.TemporaryDirectory() as tmp:
        yield map_board(Path(tmp))


def test_a_clean_value_map_board_passes(mboard):
    assert fails(mboard) == []


def test_a_value_map_value_drifted_from_its_work_run(mboard):
    f = mboard.parents[1] / WORK_RUN / "result" / "values.csv"
    f.write_text(f.read_text().replace("2.3461", "2.5"))
    assert any("RQ1-t01-001: the work Run gives 2.5, the value Run says 2.3461" in f for f in fails(mboard, 1))


def test_a_binding_on_an_old_value_run(mboard):
    task = mboard / "j02_evidence_value" / "t01_values-main"
    shutil.copytree(task / "runs" / "r01_read_values", task / "runs" / "r02_read_values")
    assert any("stale: RQ1-t01-001 reads t01_values-main/r01" in f for f in fails(mboard, 6))


def test_a_flag_in_the_value_map(mboard):
    f = mboard / "j02_evidence_value" / "t01_values-main" / "scripts" / "value_map.yaml"
    d = yaml.safe_load(f.read_text())
    d["values"]["main.n"]["flag"] = "An older setup."
    f.write_text(yaml.safe_dump(d))
    assert any("marked to check before quoting" in f for f in fails(mboard, 5))


def test_paper_check_row_v11(cboard):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "haipipe-paper" / "scripts"))
    import paper_check
    row = lambda: next(r for r in paper_check.check(cboard) if r[1] == "V11")
    assert row()[3] == "✅"
    write(cboard / "j01_evidence_display/t01_figure1/runs/r01_draw/run.yaml", "run: r01_draw\nreads: [" + WORK_RUN + "]\n")
    assert row()[3:] == ("❗", "1 failure, rule 1 (chain_check.py)")
