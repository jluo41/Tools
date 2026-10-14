"""A Job made on a small Block, drawn, then checked against excalidraw-studio's principles."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "excalidraw-studio" / "scripts"))
import job_drawing  # noqa: E402
from check import check  # noqa: E402

PAGE = """# Entropy and KL

## Opening

How are entropy and KL related, and why does a loss use them?

## Content

### 1 · Concept · Entropy and KL

Sources   → 2 filed videos from a channel (Bilibili)

**What it is**: Entropy is the average surprise of a distribution. KL is the extra surprise of a wrong model.

**How it works**: Cross-entropy is `H(P, Q) = H(P) + KL(P || Q)`. With one-hot labels the two are equal.

**Why it matters**: Cross-entropy is the next-token loss of every LLM.

**The videos on this page**:

| # | Run | Video | State |
|---|---|---|---|
| 1 | r01 | 熵与交叉熵 | drafted |

**How the videos fit**: r01 tells the whole story.

**Interview questions**:
- **Is KL a distance?** No. It is not symmetric.

### 2 · r01 · a video

**Key points**: a video's own point, not the Task's conclusion.

## Aims

- 🔨 A1.1 · Division 1 explains the concept.
  **Done when:** the explanation answers the Opening question.
  **Now:** drafted from transcripts.
"""


def block(tmp: Path) -> Path:
    b = tmp / "b01_demo"
    (b / "studio").mkdir(parents=True)
    (b / "board.md").write_text("# Demo\nspine: Learn what losses mean.\nclose: Each page explains its concept.\n")
    j = b / "j01_losses"
    t1, t2 = j / "t01_entropy_kl", j / "t02_empty"
    run = t1 / "runs/r01_video/result"
    run.mkdir(parents=True)
    t2.mkdir(parents=True)
    (j / "j01_losses.md").write_text("# j01 · Losses\n\ngoal: Explain the losses LLMs use.\nclose: open\n\n"
                                     "## Tasks\n\n1. t01_entropy_kl\n2. t02_empty\n")
    (t1 / "t01_entropy_kl.md").write_text(PAGE)
    (t2 / "t02_empty.md").write_text("# Nothing yet\n")
    (run / "runtime.yaml").write_text("status: blocked\nsubject:\n  kind: webpage\n  title: 熵与交叉熵\n"
                                      "  creator: a channel\n  platform: Bilibili\n")
    (run / "r01_video.md").write_text("# 熵与交叉熵\n")
    return j


def test_make_draws_the_whole_job(tmp_path):
    job = block(tmp_path)
    out = job_drawing.make(job)
    topic = out.parent
    assert topic.name == "s21-j01-losses" and out.with_suffix(".png").is_file()
    face = (topic / f"{topic.name}.md").read_text()
    assert "job:\n  name: j01_losses" in face and "**Tags:** `Jobs`" in face
    els = json.loads(out.read_text())["elements"]
    frames = sorted(e["name"] for e in els if e["type"] == "frame")
    assert [f[0] for f in frames] == ["①"]                                # the ladder (no picture, no detail asked)
    words = " ".join(e.get("text", "").replace("\n", " ") for e in els if e["type"] == "text")
    assert "Explain the losses LLMs use." in words                       # the Job row: its aim, from the goal: line
    assert "How are entropy and KL related" in words                     # a Task row: its question
    assert "❓ close: not written on the Job face" in words               # the Job row: what is missing, in red
    assert "r01 · video" in words and "⬜ no Run yet" in words           # a Run row under its Task; an empty Task
    assert "Cross-entropy is the next-token loss of every LLM." in words  # right of the Task: its finding
    assert "a video's own point" not in words                             # division 1 only, not a Run's
    assert "Is KL a distance?" not in words                               # a Task's detail is its own topic's
    r = check(out)
    assert r["③"].startswith("✅")
    for f in r["rows"]:
        assert f["①"].startswith("✅") and "key point yes" in f["⑤"] and f["⑦"].startswith("✅"), f


def test_a_task_topic_is_named_in_the_workflow(tmp_path):
    """A face whose `task:` yaml names a Task (excalidraw-task's) is pointed to from that Task's row."""
    job = block(tmp_path)
    other = job.parent / "studio/s24-j01-t01-entropy-kl"
    other.mkdir(parents=True)
    (other / f"{other.name}.md").write_text("s24 · t01\n\n```yaml\ntask:\n  name: j01_losses/t01_entropy_kl\n```\n")
    out = job_drawing.make(job)
    words = " ".join(e.get("text", "") for e in json.loads(out.read_text())["elements"] if e["type"] == "text")
    assert "→ details: s24" in words


def test_adopt_keeps_the_results_words(tmp_path):
    job = block(tmp_path)
    topic = job.parent / "studio/s21-j01-losses-results"
    topic.mkdir()
    (topic / f"{topic.name}.md").write_text(
        "s21 · j01 · Losses: current results\n====================================\n\n**Topic:** old\n\n"
        "Results\n-------\n\nold words\n\n```yaml\nresults:\n  jobs: [j01_losses]\n  reading:\n"
        "    j01_losses: \"what is filed\"\n  show: {}\n  open:\n    - \"a check is missing\"\n```\n\n"
        "<!-- job-results:start -->\n<!-- job-results:end -->\n\nFiles\n-----\n\n```text\n"
        f"{topic.name}/\n└── x\n```\n\nDecided\n-------\n\ns21-D01 · kept\n")
    (topic / "build_s21_j01_losses_results.py").write_text("# old builder\n")
    out = job_drawing.adopt(topic, aim="Explain the losses.")
    face = (topic / f"{topic.name}.md").read_text()
    assert face.startswith("s21 · j01 · Losses: the whole Job")
    assert 'aim: "Explain the losses."' in face and 'reading: "what is filed"' in face
    assert "a check is missing" in face and "s21-D01 · kept" in face and "```yaml\nresults:" not in face
    assert "job_drawing.draw(HERE)" in (topic / "build_s21_j01_losses_results.py").read_text()
    assert out.is_file()


def test_one_topic_per_job(tmp_path):
    """make refuses a Job that already has a topic; job_results.py sees a whole-Job topic as covering its Job (its
    covered() reads `job: name`, so it makes no duplicate results topic after an adopt)."""
    import pytest
    import job_results as jr
    job = block(tmp_path)
    job_drawing.make(job)
    assert jr.covered(job.parent) == {"j01_losses"}
    with pytest.raises(SystemExit, match="already has a topic: s21-j01-losses"):
        job_drawing.make(job)


def test_explained_layout_makes_the_words_from_zero_the_main_frame(tmp_path):
    """layout: explained (JL 261013 on Proj11 b01's s21, with a sketch: a wide, low frame; JOB at its top left; each
    Task a step lower and further right; from each, one line out through the frame's edge to its result, level with
    it): each result a small table outside ① (JL: "like table, not this figure"), read from the Task's settings rows."""
    job = block(tmp_path)
    res = job / "t01_entropy_kl/runs/r01_video/result/m.json"
    res.write_text('{"rmse": 4.7, "mae": 3.1}')
    at = "j01_losses/t01_entropy_kl/runs/r01_video/result/m.json:"
    cfg = {"layout": "explained", "reading": "Entropy explains the loss.",
           "tasks": {"t01_entropy_kl": {"found": "KL is the extra surprise."}},
           "chart": {"title": "📈 RMSE", "key": "one bar", "legend": ["num", "tkn"],
                     "bars": [{"label": "a", "at": [at + "rmse", at + "mae"]}]},
           "settings": {"columns": ["Task", "Sweep", "Form", "Low", "High"],
                        "rows": [{"state": "done", "cells": ["t01", "size", "num", {"label": "1m", "at": at + "rmse"},
                                                            {"label": "1b", "at": at + "mae"}]}]}}
    out, _ = job_drawing.draw_job(job, tmp_path / "x.excalidraw", cfg)
    els = json.loads(out.read_text())["elements"]
    fs = [e for e in els if e["type"] == "frame"]
    assert len(fs) == 1 and fs[0]["name"].startswith("① 📚") and "explained from zero" in fs[0]["name"]
    f = fs[0]
    assert f["width"] <= 3600                                             # it ends at its widest step, no margin
    texts = {e["text"].split("\n")[0]: e for e in els if e["type"] == "text"}
    steps = [next(e for k_, e in texts.items() if k_.startswith(f"🧩 {k} ·")) for k in ("t01", "t02")]
    assert steps[1]["y"] > steps[0]["y"] and steps[1]["x"] > steps[0]["x"]  # a step lower and further right
    r1, r2 = (texts[f"📊 {t} result"] for t in ("t01", "t02"))
    assert r1["x"] > f["width"] and not r1.get("frameId")                 # outside ①, on its right
    assert abs(r1["y"] - steps[0]["y"]) < 40 and abs(r2["y"] - steps[1]["y"]) < 40   # level with its step
    words = " ".join(e["text"] for e in els if e["type"] == "text")
    assert "4.70 → 3.10" in words and "1m → 1b" in words                 # its result a table: low → high, from disk
    assert "4.70" in words and "3.10" in words and "num" in words          # the Job's chart as a table too
    assert "💡 KL is the extra surprise." in words and "never evaluated" in words   # t02 has no number: dashed
    assert "r01 · video" in words                                         # its Runs, a card each, beside its step
    assert "read from, under the Project's work/" in words and "→ rmse" in words   # each result names its files
    assert "b01_demo/j01_losses/t01_entropy_kl/runs/r01_video/result/m.json" in words
    assert check(out)["③"].startswith(("✅", "🔶"))


def test_labelled_reads_lists_after_a_blank_and_running_paragraphs():
    """Found by the Proj10 session: a label, a blank line, then its list; and a paragraph past the label's line."""
    page = ("**How it works**:\n\n- first step\n  wrapped on\n- second step\n\n"
            "**Why it matters**: one sentence\nthat runs on.\n\n**Interview questions**:\n\n- **Q?** A.\n")
    lab = job_drawing.labelled(page)
    assert lab["How it works"]["items"] == ["first step wrapped on", "second step"]
    assert lab["Why it matters"]["body"] == "one sentence that runs on."
    assert lab["Interview questions"]["items"] == ["**Q?** A."]


def test_one_file_read_for_many_keys_is_one_line(tmp_path):
    import job_drawing as jd
    ats = [f"j02/t06/tables/counts.csv:context={c}.n" for c in ("lbp", "osteo", "cancer", "headache")]
    lines = jd.file_lines(ats, tmp_path)
    assert len(lines) == 1 and lines[0][1].startswith("4 values: context=lbp.n")
