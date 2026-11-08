"""The discovery theme's own parts on the shared work page (discovery_focus.py): a small Discovery Block, placeholders
only, with one Task of two Paper Runs (one whose Card says NEEDS), a collection Run, a built Evidence Bib handed over to
the Block's delivery/, a synthesis, and a second, planned Task."""
from pathlib import Path

import pytest

from live import discovery_focus as D
from live import focus_page as F


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


ENTRY = "@article{{{key},\n  title = {{{title}}},\n  author = {{Example, Ann}},\n  journal = {{Example Journal}},\n  year = {{{year}}}\n}}\n"


def paper(task: Path, run: str, key: str, title: str, year: str, verification: str, depth: str = "abstract"):
    res = task / "runs" / run / "result"
    write(task / "runs" / run / f"{run}.sh", "#!/usr/bin/env bash\n")
    write(res / f"{run}.md", f"# {title}\n\n- run: {run}\n- cite: @{key}\n- subject: [Example Journal](https://example.org/{key})\n"
                             f"- venue: Example Journal ({year})\n- verification: {verification}\n\n## Readout\n\n"
                             f"A placeholder readout of {key}. Second sentence.\n\n## Reuse\n\nThe introduction cites it.\n")
    write(res / "runtime.yaml", f"run: {run}\nfamily: discovery\nstatus: complete\nplaceholder: true\nsubject:\n  kind: paper\n"
                                f"  title: \"{title}\"\n  authors: \"Ann Example\"\nanalysis:\n  reading_depth: {depth}\n"
                                f"  claim_support: supported\nbib:\n  source: \"scripts/placeholder.bib\"\n  mode: verbatim_copy\n"
                                f"  verification:\n    status: pending\n")
    write(res / f"{run}.bib", ENTRY.format(key=key, title=title, year=year))


@pytest.fixture
def demo(tmp_path):
    block = tmp_path / "examples-t/Project-Test/discovery/b01_example_topic"
    write(block / "board.md", "# b01 · A topic\n\nboard-kind: discovery-block\nspine: Papers on a topic.\nclose: Each Task closes.\n")
    task = block / "j01_example_inquiry/t01_example_survey"
    write(block / "j01_example_inquiry/j01_example_inquiry.md", "# j01 · an inquiry\n\n## Tasks\n\n1. t01_example_survey · a survey\n")
    write(task / "t01_example_survey.md", "# t01 · a survey\n\nstate: 🟡 waiting on you · r02 to check\nfolder-kind: discovery\n")
    write(task / "discovery.yaml", "version: 6\nkind: discovery\ndiscovery_type: topic-summary\npage: t01_example_survey.md\n")
    paper(task, "r01_example2024_policy", "example2024policy", "<A policy>: a placeholder", "2024",
          "checked against its placeholder entry")
    paper(task, "r02_example2022_two", "example2022two", "<An outcome>: a placeholder", "2022",
          "NEEDS a person: its year is not checked", depth="metadata-only")
    write(task / "runs/r03_collect_example_order/result/answer_collection.md", "# Answers\n")   # never a paper
    bib = "".join(ENTRY.format(key=k, title=t, year=y) + "\n" for k, t, y in
                  (("example2022two", "<An outcome>: a placeholder", "2022"), ("example2024policy", "<A policy>: a placeholder", "2024")))
    write(task / "draft/evidence/bibex/t01_example_survey.bib", bib)
    write(task / "summary.md", "# Summary\n\nThe placeholder synthesis.\n")
    sent = write(block / "delivery/j01_example_inquiry/t01_example_survey/bib/t01_example_survey-v1.bib", bib)
    write(block / "delivery/delivery.md", "| date | for | from | status |\n|---|---|---|---|\n| 261108 | a reader | "
                                          "`j01_example_inquiry/t01_example_survey/bib/t01_example_survey-v1.bib` (v1, from "
                                          "j01_example_inquiry/t01_example_survey) | draft |\n")
    planned = block / "j02_example_subgroup/t01_example_plan"
    write(block / "j02_example_subgroup/j02_example_subgroup.md", "# j02 · a subgroup\n")
    write(planned / "t01_example_plan.md", "# t01 · a plan\n\nstate: 🔴 planned\nfolder-kind: discovery\n")
    write(planned / "discovery.yaml", "version: 6\nkind: discovery\ndiscovery_type: source-map\nstatus: planned\n")
    return tmp_path, block, task, sent


def titles(parts):
    return [p[0] for p in parts]


def test_a_block_shows_papers_bib_and_synthesis(demo):
    root, block, task, _ = demo
    parts = D.parts(block, root, "Block")
    assert titles(parts) == ["📚 Papers", "📖 Evidence Bib", "🧾 Synthesis"]
    papers = parts[0]
    assert papers[1] == "1 waits for you"                                     # the NEEDS Card, counted
    assert papers[3] == "🙋 Example 2022 · two: its verification waits for you"   # the one waiting line
    assert papers[2].count("data-pbtab=") == 2                                # a side tab per Paper Run; no collect Run
    assert "r03_collect" not in papers[2]
    assert "&lt;A policy&gt;: a placeholder" in papers[2] and "<A policy>" not in papers[2]   # escaped
    assert "placeholder</span>" in papers[2]
    assert "prior work" not in papers[2] and "a survey" in papers[2]          # a Block's tab names its Task
    assert parts[1][1] == "built" and "@example2024policy" in parts[1][2] and "draft" in parts[1][2]
    assert parts[2][1] == "1 of 2 written" and "placeholder synthesis" in parts[2][2]


def test_a_job_and_a_task_show_their_own(demo):
    root, block, task, _ = demo
    assert titles(D.parts(block / "j01_example_inquiry", root, "Job")) == ["📚 Papers", "📖 Evidence Bib", "🧾 Synthesis"]
    assert D.parts(block / "j02_example_subgroup", root, "Job") == []        # a planned Job: nothing to show yet
    mine = D.parts(task, root, "Task")
    assert mine[2][1] == "written"


def test_the_paper_words(demo):
    root, block, task, _ = demo
    words = [D.paper_word(p) for p in D.papers_of(task)]
    assert words == ["abstract read", "waits for you"]
    assert D.label_of("r01_example2024_policy") == "Example 2024 · policy"
    assert D.paper_word({"status": "blocked", "needs": False, "verified": "pending", "depth": ""}) == "blocked"
    assert D.paper_word({"status": "complete", "needs": False, "verified": "verified", "depth": "abstract"}) == "verified"


def test_the_bib_says_when_it_is_out_of_date_or_not_built(demo):
    root, block, task, _ = demo
    built = task / "draft/evidence/bibex/t01_example_survey.bib"
    built.write_text(ENTRY.format(key="example2024policy", title="x", year="2024"), encoding="utf-8")
    assert D.bib_panel(task, root)[0] == "out of date"
    built.unlink()
    word, panel = D.bib_panel(task, root)
    assert word == "not built" and "Not built yet" in panel


def test_status_is_the_tasks_own_and_leaves_block_and_job_alone(demo):
    root, block, task, _ = demo
    assert D.status(block, root, "Block") == [] and D.status(block / "j01_example_inquiry", root, "Job") == []
    bars = D.status(task, root, "Task")
    assert [b[0] for b in bars] == ["📚 Papers", "📖 Evidence Bib", "🧾 Synthesis", "🧪 Runs"]
    assert bars[0][3].startswith("🙋 ")


def test_delivery_hands_over_the_bib(demo):
    root, block, task, sent = demo
    for folder, level in ((block, "Block"), (block / "j01_example_inquiry", "Job"), (task, "Task")):
        tabs = D.delivery_tabs(folder, root, level)
        assert tabs[0][0] == "Evidence Bib" and tabs[0][1] == "ready", level
        assert sent.name in tabs[0][2] and "draft" in tabs[0][2]
        assert all(t[1] != "nothing yet" for t in tabs[1:])                   # an empty shared lane is left out
    empty = D.delivery_tabs(block / "j02_example_subgroup", root, "Job")
    assert empty[0][1] == "nothing yet" and "Nothing handed over yet." in empty[0][2]


def test_the_shared_page_finds_the_parts(demo):
    root, block, task, _ = demo
    assert F.page_module("discovery", block, root)[0] is D
    assert titles(F.theme_parts("discovery", block, root, "Block")) == ["📚 Papers", "📖 Evidence Bib", "🧾 Synthesis"]
    html = F.findings_board([], block, root, "", F.theme_parts("discovery", block, root, "Block"))
    assert "1 · 📚 Papers" in html and "4 · 📦 Delivery" in html and "Traceback" not in html
    assert "<p class=band-wait>🙋 Example 2022 · two: its verification waits for you</p>" in html
    job = F.job_findings(block / "j01_example_inquiry", root, F.theme_parts("discovery", block / "j01_example_inquiry", root, "Job"))
    assert "📚 Papers" in job and "📦 Delivery" in job
    assert set(D.VIEW_SKILLS) <= {"mindmap", "standing", "findings"}


def test_a_tasks_headline_is_its_synthesis_then_its_newest_paper(demo):
    root, block, task, _ = demo
    assert D.headline(task, root) == "The placeholder synthesis."
    (task / "summary.md").unlink()
    write(task / "runs/r02_example2022_two/result/runtime.yaml",
          (task / "runs/r02_example2022_two/result/runtime.yaml").read_text(encoding="utf-8") + 'headline: "Newest paper line."\n')
    assert D.headline(task, root) == "Newest paper line."
    assert D.headline(block / "j02_example_subgroup/t01_example_plan", root) == ""
