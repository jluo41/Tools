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


def fake_tasks(names: list[str], tmp: Path) -> list[dict]:
    """Task dicts as task_info makes them, enough for the steps: an id, a folder name, a title, Runs, a row."""
    out = []
    for n in names:
        folder = tmp / "j51_raw" / n
        out.append({"id": n[:3], "name": n, "title": f"B00/J51/T{n[1:3]} · {n[4:].replace('_', ' ')}",
                    "question": "What does this table hold?", "lab": {},
                    "runs": [{"name": "r01_profile", "mark": "✅", "state": "ok", "values": [], "result": folder}],
                    "row": {"task": folder}})
    return out


def test_a_family_of_tasks_is_one_step(tmp_path):
    """Past eight Tasks, three or more of one kind in a row stand as one step; others stay their own (261014)."""
    tasks = fake_tasks(["t01_intake", "t02_catalog"] + [f"t{n}_profile_x{n}" for n in range(11, 21)] + ["t91_route"],
                       tmp_path)
    steps = job_ladder.step_groups(tasks, {})
    assert [s["id"] for s in steps] == ["t01", "t02", "t11–t20", "t91"]
    fam = steps[2]
    assert len(fam["members"]) == 10 and len(fam["runs"]) == 10 and fam["question"] == "What does this table hold?"
    assert job_ladder.bare(tasks[0]["title"]) == "intake"                 # the page's address is not said twice


def test_the_face_names_steps_and_two_staircases(tmp_path):
    """The face's steps group Tasks by range; past six steps, or where parts says, the Job is two staircases."""
    tasks = fake_tasks(["t01_intake"] + [f"t{n}_profile_x{n}" for n in range(11, 17)] + ["t91_route", "t92_time",
                                                                                         "t93_handoff"], tmp_path)
    cfg = {"steps": [{"title": "cohort", "tasks": "t11-t13"}, {"title": "signals", "tasks": ["t14", "t15", "t16"]}]}
    steps = job_ladder.step_groups(tasks, cfg)
    assert [s["id"] for s in steps] == ["t01", "t11–t13", "t14–t16", "t91", "t92", "t93"]
    assert job_ladder.split_steps(steps, cfg) == [("", steps)]           # six steps: one staircase
    parts = job_ladder.split_steps(steps, {"parts": [{"title": "in"}, {"title": "out", "from": "t91"}]})
    assert [(t, [s["id"] for s in ss]) for t, ss in parts] == [("in", ["t01", "t11–t13", "t14–t16"]),
                                                               ("out", ["t91", "t92", "t93"])]
    seven = steps + job_ladder.step_groups(fake_tasks(["t94_more"], tmp_path), {})
    assert len(job_ladder.split_steps(seven, {})) == 2                    # past six: halves, named by their Tasks


def test_a_row_per_run_and_later_drawn_plain(tmp_path):
    """LLMRec 261014: "make the report of the task to be shown as the table, then make it to the level 3 of the
    agreed". A Task of one subject per Run is a table, a row per Run, its cells read from each Run's result; an agreed
    topic's open points move to `later:`, drawn plain in ②, so no red ❓ is left."""
    job = job_with_results(tmp_path)
    for r in ("r01_first", "r02_rerun", "r03_fixed"):
        (job / "t01_overlap/runs" / r / "result/runtime.yaml").write_text(
            f"status: complete\nsubject:\n  title: Paper of {r}\n")
    cfg = dict(CFG, tables={"t01_overlap": [{"title": "Its papers", "runs": True, "rows": 2, "columns": [
        {"label": "paper", "at": "runtime.yaml:subject.title"}, {"label": "says", "at": "says"}]}]},
        later=[{"item": "A third engine", "closer": "when one is licensed"}])
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, cfg)
    els = json.loads(out.read_text())["elements"]
    words = " ".join(e["text"].replace("\n", " ") for e in els if e["type"] == "text")
    assert "Its papers" in words and "Paper of r01_first" in words and "the first pass" in words
    assert "1 more Run, not shown" in words                                      # capped, counted, never dropped
    assert "⏳ A third engine" in words and "when one is licensed" in words
    red = [e["text"] for e in els if e["type"] == "text" and e.get("strokeColor") == job_ladder.RED]
    assert not any("A third engine" in t or "Later" in t for t in red)            # later is plain, never red


def test_each_step_names_its_page_and_run_tables_filter(tmp_path):
    """Reader review 261014 (LLMRec): "no Task page is named". Each step says where its page is, linked; a row per Run
    keeps only the Runs `only:` names, and a Run with nothing in the columns takes no row; the picked numbers' table
    says which Run it reads."""
    job = job_with_results(tmp_path)
    for r in ("r01_first", "r02_rerun"):
        (job / "t01_overlap/runs" / r / "result/runtime.yaml").write_text(f"status: complete\nn: {len(r)}\n")
    cfg = dict(CFG, tables={"t01_overlap": [{"title": "Only r0[12]", "runs": True, "only": "r0[12]_*",
                                             "columns": [{"label": "n", "at": "runtime.yaml:n"}]}]})
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, cfg)
    els = json.loads(out.read_text())["elements"]
    page = [e for e in els if e["type"] == "text" and e["text"].startswith("📄 page: t01_overlap/t01_overlap.md")]
    assert page and page[0].get("link", "").endswith("t01_overlap/t01_overlap.md")
    words = " ".join(e["text"].replace("\n", " ") for e in els if e["type"] == "text")
    assert "Only r0[12]" in words and "r03" not in [e["text"] for e in els if e["type"] == "text"]
    assert "measure (r01 · tau)" in words                                       # t02's picks name their Run


def test_a_unit_stays_with_its_number_and_a_block_path_table(tmp_path):
    """Reader review 261014 (LLMRec b02 s23): "Claude transport response 1,326 | chars", the unit split off as a
    second cell. A pick's own label splits it. A table may read a file anywhere in the Block (`path:`)."""
    job = job_with_results(tmp_path)
    (job.parent / "shared.csv").write_text("pair,rate\na-b,0.6\na-c,0.7\n")
    cfg = dict(CFG, show={"t02_order/r01_tau": [{"label": "Kendall tau", "at": "metrics.json:tau", "unit": "units"}]},
               tables={"t01_overlap": [{"title": "From the Block", "path": "shared.csv", "columns": ["pair", "rate"]}]})
    out = tmp_path / "out" / "j01.excalidraw"
    out.parent.mkdir()
    job_ladder.draw_job(job, out, cfg)
    cells = [e["text"] for e in json.loads(out.read_text())["elements"] if e["type"] == "text"]
    assert "Kendall tau" in cells and "0.02 units" in cells
    assert "From the Block" in cells and "a-c" in cells


def test_results_stay_inside_the_frame_or_overflow_it_evenly():
    """JL 261014: the results may pass the frame's top and bottom, but by the same amount; shorter, they stay inside
    it, each as near its own step as it can be, and never overlap."""
    tall = job_ladder.results_layout([0, 0], [900, 900], 100, 1100, 90)            # 1,890 tall for 1,000 of frame
    assert abs((100 - tall[0]) - (tall[1] + 900 - 1100)) < 1                      # as far above as below
    short = job_ladder.results_layout([150, 600, 1000], [200, 200, 200], 100, 1100, 90)
    assert short[0] == 150 and short[1] == 600                                    # level with their steps
    assert short[2] + 200 <= 1100                                                 # pulled up inside the bottom
    assert all(b >= a + 200 + 90 for a, b in zip(short, short[1:]))              # never overlapping


def test_bent_links_take_lanes_that_never_cross():
    """Links that turn up take lanes left to right in step order; links that both turn down, right to left; a
    straight one takes none."""
    lanes = job_ladder.results_lanes([(500, 100), (900, 400), (1300, 1300), (1700, 2100), (2100, 2600)])
    assert lanes[0] < lanes[1] < lanes[4] < lanes[3] and 2 not in lanes


def test_a_results_block_lays_its_panels_side_by_side(tmp_path):
    """Asked 261014 ("这个 result 右边有这么多的空位你都不用"): given two columns, a block's two charts stand side by
    side, and the block is shorter than with one; a small Job's results, which fit beside its frame, keep one."""
    job = job_with_results(tmp_path)
    cfg = {"charts": {"t01_overlap": [
        {"title": "J by model", "file": "metrics.json", "each": "by_model", "value": "j.p"},
        {"title": "J by model, again", "file": "metrics.json", "each": "by_model", "value": "j.p"}]}}
    jd = job_ladder.jd
    t = jd.task_info(jd.jr.job_rows(job.parent, job, {"show": {}})[0], {"show": {}})
    one, two = job_ladder.Drawing(), job_ladder.Drawing()
    w1, h1, _ = job_ladder.results_block(one, 0, 0, t, cfg, "", tmp_path / "assets", cols=1)
    w2, h2, _ = job_ladder.results_block(two, 0, 0, t, cfg, "", tmp_path / "assets", cols=2)
    charts = [e for e in two.els if e["type"] == "image"]
    assert abs(charts[0]["y"] - charts[1]["y"]) < 1 and charts[0]["x"] < charts[1]["x"]
    assert w2 > w1 and h2 < h1
    _, h3, _ = job_ladder.results_block(job_ladder.Drawing(), 0, 0, t, cfg, "", tmp_path / "assets", cols=3)
    assert h3 == h2                                                               # never a column with nothing in it


def test_results_too_tall_stand_in_columns_centred_and_uncrossed(monkeypatch):
    """Past twice ①'s height the blocks stand in side-by-side columns (JL 261014), each centred on ①, so what rises
    above it equals what hangs below; no two blocks overlap and no two links cross."""
    groups = job_ladder.results_columns([1900] * 5, 2 * 3000, 90)
    assert len(groups) == 2 and [k for g in groups for k in g] == list(range(5))
    assert all(sum(1900 for _ in g) + 90 * (len(g) - 1) <= 6000 for g in groups)

    blocks = []

    def fake(d, x, y, t, cfg, found, assets, thumb=None, cols=1):
        blocks.append((x, y, 1500, t["h"]))
        return 1500, t["h"], False
    monkeypatch.setattr(job_ladder, "results_block", fake)
    d = job_ladder.Drawing()
    f = {"x": 0, "y": 0, "width": 4000, "height": 3000}
    steps = [{"task": {"h": h}, "found": "", "thumb": None, "y": 300 + 500 * k, "mid": 340 + 500 * k,
              "right": 3000} for k, h in enumerate([2200, 1900, 2100, 2000, 2300])]
    sizes = [(1500, s["task"]["h"]) for s in steps]
    job_ladder.results_in_columns(d, f, 4000, steps, {}, None, 1, sizes, job_ladder.results_columns(
        [h for _, h in sizes], 6000, 90))
    top = min(y for _, y, _, _ in blocks)
    bottom = max(y + h for _, y, _, h in blocks)
    assert abs((0 - top) - (bottom - 3000)) < 1                         # equal above and below
    for i, a in enumerate(blocks):
        for b in blocks[i + 1:]:
            assert a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1]
    segs = []
    for k, e in enumerate(e for e in d.els if e["type"] in ("arrow", "line")):
        pts = [(e["x"] + px, e["y"] + py) for px, py in e["points"]]
        segs += [(k, p, q) for p, q in zip(pts, pts[1:])]

    def cross(p, q, r, s):                                              # an H and a V segment that properly meet
        (h1, h2), (v1, v2) = ((p, q), (r, s)) if p[1] == q[1] else ((r, s), (p, q))
        if h1[1] != h2[1] or v1[0] != v2[0]:
            return False
        return min(h1[0], h2[0]) < v1[0] < max(h1[0], h2[0]) and min(v1[1], v2[1]) < h1[1] < max(v1[1], v2[1])
    assert not [(a, b) for a, p, q in segs for b, r, s in segs if a < b and cross(p, q, r, s)]
