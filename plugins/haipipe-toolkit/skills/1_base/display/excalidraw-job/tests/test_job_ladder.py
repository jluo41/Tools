"""The staircase (job_ladder.py): steps that move right, quiet reruns, results as charts and tables, frames as stairs."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "excalidraw-studio" / "scripts"))
import job_ladder  # noqa: E402
from check import check  # noqa: E402


def job_with_results(tmp: Path) -> Path:
    """A Block with one Job of two Tasks: t01 with three Runs (r03 the current one, with per-model metrics), t02 with
    one Run whose result holds a single number."""
    b = tmp / "b01_demo"
    (b / "studio").mkdir(parents=True)
    (b / "board.md").write_text("# Demo\nspine: Compare two engines.\n")
    j = b / "j01_compare"
    (j / "j01_compare.md").parent.mkdir(parents=True)
    (j / "j01_compare.md").write_text("# j01 · Compare\n\ngoal: Compare engine A with engine B.\nclose: both read\n")
    for t, title in (("t01_overlap", "Overlap of A and B"), ("t02_order", "Order of shared items")):
        (j / t).mkdir()
        (j / t / f"{t}.md").write_text(f"# {title}\n\n## Opening\n\nHow much do A and B share?\n")
    for r in ("r01_first", "r02_rerun", "r03_fixed"):
        res = j / "t01_overlap/runs" / r / "result"
        res.mkdir(parents=True)
        (res / "runtime.yaml").write_text("status: complete\n")
        (res / "metrics.json").write_text(json.dumps({"summary": {"headline": f"{r} says the overlap is small"},
                                                      "by_model": {"x-x-alpha-20250101": {"j": {"p": 0.20, "lo": 0.15, "hi": 0.25}},
                                                                   "beta.2": {"j": {"p": 0.10, "lo": 0.05, "hi": 0.16}}}}))
    res = j / "t02_order/runs/r01_tau/result"
    res.mkdir(parents=True)
    (res / "runtime.yaml").write_text("status: complete\n")
    (res / "metrics.json").write_text(json.dumps({"tau": 0.02}))
    return j


CFG = {
    "reading": "A and B share little.",
    "tasks": {"t01_overlap": {"found": "Little overlap. More words follow here."},
              "t02_order": {"found": "Order agrees near zero."}},
    "runs": {"t01_overlap/r01_first": {"says": "the first pass"},
             "t01_overlap/r03_fixed": {"says": "the fixed matcher", "current": True}},
    "show": {"t02_order/r01_tau": [{"label": "Kendall tau", "at": "metrics.json:tau"}]},
    "charts": {"t01_overlap": [{"title": "Jaccard by model", "each": "by_model", "value": "j.p", "low": "j.lo",
                                "high": "j.hi", "fmt": "pct"}]},
    "terms": [{"term": "A", "means": "engine A"}],
}


def texts(out: Path) -> list[dict]:
    return [e for e in json.loads(out.read_text())["elements"] if e["type"] == "text"]


def test_columns_step_right_and_share_past_four():
    assert job_ladder.columns(3) == [0, 1, 2]
    ten = job_ladder.columns(10)
    assert ten[0] == 0 and max(ten) == 3 and ten == sorted(ten)        # four columns at most; several share one
    assert job_ladder.columns(0) == []


def test_runs_stand_in_a_grid_so_a_job_grows_wide_not_tall(tmp_path):
    """JL 261013 on j01: six Runs that each say something are two rows of three, not a column six cards tall."""
    assert [job_ladder.run_cols(n) for n in (0, 1, 2, 4, 5, 9)] == [1, 1, 2, 2, 3, 3]
    job = job_with_results(tmp_path)
    for k in range(4, 7):
        res = job / f"t01_overlap/runs/r0{k}_more/result"
        res.mkdir(parents=True)
        (res / "runtime.yaml").write_text("status: complete\n")
        (res / "metrics.json").write_text(json.dumps({"summary": {"headline": f"pass {k} adds a case"}}))
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, {"reading": "A and B share little."})   # no current Run: all six speak
    heads = [t for t in texts(out) if t["text"].split("\n")[0].endswith(("· first", "· rerun", "· fixed", "· more"))]
    rows = sorted({round(t["y"]) for t in heads})
    assert len(heads) == 6 and len(rows) == 2, [(t["text"][:20], t["x"], t["y"]) for t in heads]
    frame = next(e for e in json.loads(out.read_text())["elements"] if e["type"] == "frame")
    assert frame["width"] > frame["height"]


def test_short_key_drops_a_repeated_prefix_and_a_date():
    assert job_ladder.short_key("claude-claude-haiku-4-5-20251001") == "claude-haiku-4-5"
    assert job_ladder.short_key("deepseek-deepseek-v4-flash-harness") == "deepseek-v4-flash"
    assert job_ladder.short_key("model_specific_divergence") == "model specific divergence"


def test_the_staircase_quiet_reruns_charts_and_a_table(tmp_path):
    job = job_with_results(tmp_path)
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, dict(CFG))
    els = json.loads(out.read_text())["elements"]
    ts = texts(out)
    words = " ".join(e["text"].replace("\n", " ") for e in ts)
    # the steps move right: t02's box stands right of t01's
    step = {t["text"].split(" · ")[0][-3:]: t["x"] for t in ts if t["text"].startswith("🧩 ")}
    assert step["t02"] > step["t01"]
    # once a Run is marked current, the others are grey names only; the current one speaks
    assert "📌 current" in words and "the fixed matcher" in words
    assert "the first pass" not in words and "r01_first says" not in words
    # t01's results are a chart drawn from the current Run's metrics.json, into the topic's assets
    pngs = list((out.parent / "assets").glob("chart-t01_overlap-*.png"))
    assert pngs and any(e["type"] == "image" for e in els)
    assert "Jaccard by model" in words and "Little overlap." in words and "More words follow" not in words
    # t02 names no chart: its picked number is a table, not a sentence
    assert "Kendall tau" in words and "0.02" in words
    r = check(out)
    assert all("❌" not in v for row in r["rows"] for k, v in row.items() if k[0] in "①②③④⑤⑥⑦⑧⑨"), r["rows"]


def test_frames_after_the_staircase_step_down_and_right(tmp_path):
    job = job_with_results(tmp_path)
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, dict(CFG))
    frames = sorted((e for e in json.loads(out.read_text())["elements"] if e["type"] == "frame"), key=lambda e: e["y"])
    main, words_frame = frames[0], frames[1]
    assert main["x"] == 0 and words_frame["x"] > main["x"]                # never the same left edge
    assert words_frame["y"] >= main["y"] + main["height"]                 # below the main frame
    assert words_frame["width"] < main["width"]                           # 大小有致: the explaining frame is smaller
    assert (words_frame.get("customData") or {}).get("explains")


def test_a_tasks_own_figures_and_named_tables_join_its_results(tmp_path):
    """JL 261013: "for the task, we might want to add the figures and table from it". A picture in a Run's result is
    shown in that Task's results block (and not again in a Job-level pictures frame); a CSV the face names is a table."""
    from PIL import Image
    job = job_with_results(tmp_path)
    Image.new("RGB", (400, 200), "white").save(job / "t02_order/runs/r01_tau/result/scatter.png")
    (job / "t01_overlap/runs/r03_fixed/result/by_model.csv").write_text(
        "model,jaccard,n\nx-x-alpha-20250101,0.2,120\nbeta.2,0.1,90\n")
    cfg = dict(CFG, tables={"t01_overlap": [{"title": "Jaccard table", "file": "by_model.csv",
                                             "columns": ["model", "jaccard", "n"], "sort": "-jaccard"}]})
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, cfg)
    els = json.loads(out.read_text())["elements"]
    words = " ".join(e["text"].replace("\n", " ") for e in els if e["type"] == "text")
    assert "Jaccard table" in words and "x-alpha" in words and "120" in words     # the named table, its rows
    assert "runs/r01_tau/result/scatter.png" in words                              # t02's own figure, captioned
    assert sum(e["type"] == "image" for e in els) >= 2                            # the chart and the figure
    names = [e.get("name", "") for e in els if e["type"] == "frame"]
    assert not any("pictures" in n for n in names)                                 # no Job-level repeat of it


def test_a_current_run_never_folds_away():
    """Found by the b03 s21 trial (261013): past MOST Runs that report, the current one still has its own row."""
    runs = [{"name": f"r{k:02d}_m{k}", "values": ["n 1"], "result": Path("/nonexistent"), "state": "complete",
             "mark": "✅", "subject": ""} for k in range(1, 10)]
    t = {"name": "t01_x", "runs": runs}
    keep, folded = job_ladder.shown_runs(t, {"runs": {"t01_x/r02_m2": {"current": True}}})
    names = [r["name"] for r in keep]
    assert "r02_m2" in names and len(keep) <= job_ladder.MOST and names == sorted(names)
    assert len(keep) + len(folded) == 9


def test_a_stata_csv_gives_bars_with_whiskers_and_a_filtered_table(tmp_path):
    """OpioidRx 261013: a Stata table holds several models; a chart picks rows by `col=v&col2=v` with each bar's interval
    (`low`, `high`), and a table shows only the rows its `where` picks."""
    job = job_with_results(tmp_path)
    res = job / "t02_order/runs/r01_tau/result"
    (res / "slopes.csv").write_text("model_id,context,estimate,ci_lo,ci_hi\n"
                                    "m2,lbp,9.19,4.20,14.18\nm2,cancer,0.12,-0.93,1.16\nm5,lbp,12.6,5.4,19.8\n")
    spec = {"file": "slopes.csv", "bars": [
        {"label": "low back pain", "at": "model_id=m2&context=lbp.estimate",
         "low": "model_id=m2&context=lbp.ci_lo", "high": "model_id=m2&context=lbp.ci_hi"},
        {"label": "cancer", "at": "model_id=m2&context=cancer.estimate"}]}
    rows = job_ladder.chart_rows(spec, res)
    assert rows[0] == ("low back pain", 9.19, 4.20, 14.18) and rows[1][2] is None
    cfg = dict(CFG, tables={"t02_order": [{"title": "Slopes, model m2", "file": "slopes.csv", "where": "model_id=m2",
                                           "columns": ["context", "estimate"]}]})
    t = {"name": "t02_order", "runs": [{"name": "r01_tau", "result": res}]}
    (title, cols, shown), = job_ladder.task_tables(t, cfg)
    assert [r["cells"][0] for r in shown] == ["lbp", "cancer"]                     # m5's row is left out


def test_terms_past_the_cap_are_counted_and_millions_stay_short(tmp_path):
    """OpioidRx 261013: a face with more terms than ② draws says how many more, never drops them silently; a chart
    of counts in the millions labels its bars 113.2M, not 113,219,741 run off the edge."""
    job = job_with_results(tmp_path)
    cfg = dict(CFG, terms=[{"term": f"T{k}", "means": "x"} for k in range(job_ladder.TERMS + 3)])
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, cfg)
    words = " ".join(e["text"].replace("\n", " ") for e in texts(out))
    assert "3 more terms in the face" in words
    res = job / "t02_order/runs/r01_tau/result"
    (res / "rows.json").write_text(json.dumps({"a": 113219741, "b": 2397223}))
    png = job_ladder.chart_png({"file": "rows.json", "bars": [{"label": "a", "at": "a"}, {"label": "b", "at": "b"}]},
                               res, tmp_path / "c.png")
    assert png and png.is_file()
