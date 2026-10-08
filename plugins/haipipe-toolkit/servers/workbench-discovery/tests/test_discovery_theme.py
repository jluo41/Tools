"""The discovery theme on the base frame (discovery_theme.py): a small Discovery Block, placeholders only,
opened at the Block, Job and Task levels; each Space's subspaces and run types come from the old page's
data and the family's Workbench Table, drawn with the base's classes only."""
import json
from pathlib import Path

import pytest

from live import frame
from live.discovery_theme import THEME


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def paper(task: Path, name: str, title: str, status: str, verification: str, bib: bool):
    write(task / "runs" / f"{name}.sh", "#!/usr/bin/env bash\necho read\n")
    result = task / "results" / name
    write(result / f"{name}.md", f"# {title}\n\n- run: {name}\n- cite: @{name}\n- subject: https://example.org/{name}\n"
                                 f"- venue: Test venue\n- verification: {verification}\n\n## Readout\n\nOne clear thing.\n")
    write(result / "runtime.yaml", f"run: {name}\nfamily: discovery\nstatus: {status}\nsubject:\n  kind: paper\n"
                                   f"  title: \"{title}\"\nanalysis:\n  reading_depth: full-text\n  claim_support: supported\n")
    if bib:
        write(result / f"{name}.bib", f"@article{{{name},\n  title = {{{title}}}\n}}\n")


@pytest.fixture
def demo(tmp_path):
    block = tmp_path / "examples-t/Project-Test/discoveries/b01_topic"
    write(block / "board.md", "# A topic\nboard-kind: discovery-block\nstate: 🟡 OPEN\nspine: Papers on a topic.\n"
          "close: Each Task has a synthesis.\n\n## Questions\n\n```yaml\nquestions:\n- id: Q01\n  title: Which method\n"
          "  question: Which method works best?\n  work:\n  - j01_methods/t01_survey\n```\n")
    task = block / "j01_methods/t01_survey"
    write(task / "t01_survey.md", "---\nfolder-kind: discovery\n---\n# A survey\n\n## Opening\n\nWhy.\n")
    write(task / "discovery.yaml", "version: 6\nkind: discovery\ndiscovery_type: topic-summary\njob:\n  title: \"Methods\"\n")
    write(task / "summary.md", "# Summary\n\nThe placeholder synthesis.\n")
    write(task / "notes.md", "# Notes\n")
    paper(task, "r01_one2024_a", "Paper One", "complete", "VERIFIED", True)
    paper(task, "r02_two2025_b", "Paper Two", "blocked", "NEEDS-VERIFICATION", False)
    return tmp_path, block


def spaces(root, folder, sub=""):
    return {s["name"]: s for s in json.loads(frame.frame_json(THEME, root, folder, sub))["spaces"]}


def test_the_frame_finds_the_discovery_theme(demo):
    root, block = demo
    assert frame.theme_of(block, root) == "discovery"
    assert frame.themes()["discovery"] is THEME


def test_the_block_carries_the_old_pages_views(demo):
    root, block = demo
    s = spaces(root, block)
    assert s["Description"]["subspaces"] == ["Block", "Resources"]
    assert s["Audience Report"]["subspaces"] == ["Questions", "Reports"]
    assert s["Work Details"]["subspaces"] == ["Papers", "Tasks", "Citations"]
    assert s["Runs"]["subspaces"] == ["All", "Blocked"]
    assert s["Delivery"]["subspaces"] == ["Reports", "BibTeX"]
    assert "Ask a Question" in s["Audience Report"]["run_doing"]
    assert {"Find papers", "Read a paper", "Synthesize a Task", "Verify a citation"} <= set(s["Work Details"]["run_doing"])
    assert all(r.startswith(("run-", "rNN_")) for r in s["Work Details"]["run_types"])   # named by their Runs
    assert s["Runs"]["run_types"] == ["run-review-<run>"] and s["Runs"]["run_doing"] == ["Review a Run"]
    views = frame.spaces_for(THEME, "Block", block, root, "Papers")
    assert "Paper One" in views["Work Details"].html and "st-warn" in views["Work Details"].html
    assert "Which method" in frame.spaces_for(THEME, "Block", block, root)["Audience Report"].html
    assert "@article" in frame.spaces_for(THEME, "Block", block, root, "BibTeX")["Delivery"].html
    assert "r02_two2025_b" in frame.spaces_for(THEME, "Block", block, root, "Blocked")["Runs"].html


def test_a_job_and_a_task_read_their_own_part(demo):
    root, block = demo
    job, task = block / "j01_methods", block / "j01_methods/t01_survey"
    jv = frame.spaces_for(THEME, "Job", job, root)
    assert "t01_survey" in jv["Work Details"].html and "Which method" in jv["Audience Report"].html
    tv = frame.spaces_for(THEME, "Task", task, root)
    assert "placeholder synthesis" in tv["Audience Report"].html
    assert "Paper One" in tv["Work Details"].html
    assert "notes.md" in frame.spaces_for(THEME, "Task", task, root, "Notes")["Work Details"].html


def test_every_level_renders_in_base_classes_only(demo):
    root, block = demo
    for folder in (block, block / "j01_methods", block / "j01_methods/t01_survey"):
        for space in frame.SPACE_NAMES:
            page = frame.render(THEME, root, folder, space)
            assert "Discovery" in page
            body = page.split("<div class=space-main>", 1)[1]
            assert "<style" not in body.split("</main>", 1)[0].split("<dialog", 1)[0]   # no theme stylesheet
            for old in ('class="pill', 'class="idtag', 'class="hl-row'):                 # the old page's classes
                assert old not in body
