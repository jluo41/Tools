"""Readable run names, records at the two ends, and the one-time rename (JL 260928)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import run_names
from src.run_lifecycle import close_run, find_open, open_run
from src.run_rename import apply as rename, plan as rename_plan


def test_names_read_both_forms_and_mint_readable_ones():
    assert run_names.kind_of("run-section-0927-readability-cleanup") == "section"
    assert run_names.kind_of("rp-sec-07") == "section"
    assert run_names.kind_of("re-cite-01_score") == "citation"
    assert run_names.kind_of("run-delivery-latex") == run_names.kind_of("rd01_latex") == "delivery"
    assert run_names.is_run_name("run-auto-write-0928-c1") and not run_names.is_run_name("rp-auto-01_C1")
    assert run_names.is_run_name("run-section-readability-cleanup")       # undated: the grammar (JL 261007)
    assert run_names.is_dated("run-section-0927-readability-cleanup") and not run_names.is_dated("run-section-c1")
    assert run_names.undated("run-display-0930-main-effects") == "run-display-main-effects"
    assert run_names.mint("section", "whole-Section readability cleanup after the delivery",
                          day="2026-09-14T10:00") == "run-section-whole-section-readability-cleanup"
    assert run_names.mint("revise", "c1-p2", day="2026-09-28",
                          taken={"run-revise-c1-p2"}) == "run-revise-c1-p2-2"
    assert run_names.item_slug("E11-VALUE-score-validation") == "score-validation"
    assert run_names.delivery_name("web") == "run-delivery-webpage"


def page(tmp_path):
    folder = tmp_path / "Page"
    (folder / "draft").mkdir(parents=True)
    (folder / "Page.md").write_text("# Page\n\n## Opening\nQ.\n\n## Content\nText.\n")
    (folder / "draft" / "Page-draft-v1.0.md").write_text(
        "# Page · draft v1.0\ndraft-version: v1.0\n\n## 1 · Structure · Bullet Point Table\n\n"
        "### C1.P1 · First\n- B1 · [Point] One\n\n## 2 · Scratch · What to write here\n\n### C1.P1 · First\n\n"
        "## 3 · Draft · Reading and Revise\n\n### C1.P1 · First\n- B1 · The first sentence.\n")
    return folder


def test_a_run_writes_its_ticket_at_open_and_its_results_only_at_close(tmp_path):
    folder = page(tmp_path)
    opened = open_run(folder, "section", target="C1", goal="Tighten the section", by="JL", day="2026-09-29")
    run = opened["run"]
    # one folder per Run (0.125): runs/<name>/<name>.md and its card at open, its pass at close
    assert run == "run-section-c1" and opened["ticket"] == "runs/%s/%s.md" % (run, run)
    assert "status: open" in (folder / "runs" / run / (run + ".md")).read_text()
    assert "status: running" in (folder / "runs" / run / "run.yaml").read_text()
    assert not (folder / "results").exists() and not (folder / "runs" / run / "passes").exists()
    assert find_open(folder, "section", "C1") == run
    closed = close_run(folder, run, summary="tightened three sentences")
    assert re.fullmatch(r"runs/%s/passes/p01-\d{4}/" % run, closed["result"])
    runtime = (folder / closed["result"] / "runtime.yaml").read_text()
    assert "status: complete" in runtime and "skills: haipipe-page-writing · haipipe-writing" in runtime
    assert "status: closed" in (folder / "runs" / run / (run + ".md")).read_text()
    card = (folder / "runs" / run / "run.yaml").read_text()
    assert "kind: soft" in card and "status: done" in card and closed["result"].split("/")[3] in card
    assert not (folder / "results").exists()
    assert run + " closed: tightened three sentences" in (folder / "draft" / "records" / "Page-log.md").read_text()
    assert find_open(folder, "section", "C1") is None


def test_rename_flattens_renames_rewrites_and_pairs_every_result(tmp_path):
    folder = page(tmp_path)
    (folder / "draft" / "Page-evidence-items.md").write_text(
        "# Page · evidence items\n\n## Values\n\n### E03-VALUE-headline-estimate · C1.P1.B1\n"
        "- **Local Run**: Page · Evidence Item · pj02t03r01 → results/pj02t03r01_headline/result.yaml\n")
    for rel, text in {"runs/draft-manual-run/rp-sec-01.md": "- Goal: whole section readability cleanup\n",
                      "runs/evidence-run/re-value-01_headline.md": "---\nitem: E03-VALUE-headline-estimate\n---\n"}.items():
        (folder / rel).parent.mkdir(parents=True, exist_ok=True)
        (folder / rel).write_text(text)
    for name, day in {"rp-sec-01": "2026-09-14", "re-value-01_headline": "2026-09-28",
                      "pj02t03r01_headline": "2026-09-06"}.items():
        (folder / "results" / name).mkdir(parents=True)
        (folder / "results" / name / "runtime.yaml").write_text("started_at: '%sT10:00:00'\n" % day)
    (folder / "runs" / "evidence-run" / "re-value-01_headline.md").write_text(
        "---\nitem: E03-VALUE-headline-estimate\nlegacy_run: pj02t03r01\n---\nsee results/re-value-01_headline/\n")
    names = {row["old"]: row["new"] for row in rename_plan(folder)["moves"]}
    assert names == {"rp-sec-01": "run-section-whole-section-readability-cleanup",
                     "pj02t03r01_headline": "run-value-headline-estimate",
                     "re-value-01_headline": "run-value-headline-estimate-2"}
    rename(folder)
    # one folder per Run (0.125): each run is runs/<name>/ with its ticket, card and first pass
    runs = sorted(p.name for p in (folder / "runs").iterdir())
    assert runs == sorted(names.values()) and not (folder / "results").exists()
    for name in runs:
        assert (folder / "runs" / name / (name + ".md")).is_file() and (folder / "runs" / name / "run.yaml").is_file()
    assert [p.name for p in (folder / "runs" / "run-value-headline-estimate" / "passes").iterdir()] == ["p01-0906"]
    assert [p.name for p in (folder / "runs" / "run-value-headline-estimate-2" / "passes").iterdir()] == ["p01-0928"]
    evidence = (folder / "draft" / "Page-evidence-items.md").read_text()
    assert "run-value-headline-estimate → runs/run-value-headline-estimate/passes/p01-0906/result.yaml" in evidence
    assert "pj02t03r01" not in evidence and "results/" not in evidence
    two = folder / "runs" / "run-value-headline-estimate-2" / "run-value-headline-estimate-2.md"
    assert "runs/run-value-headline-estimate-2/passes/p01-0928/" in two.read_text()
    one = folder / "runs" / "run-value-headline-estimate" / "run-value-headline-estimate.md"
    assert "had no ticket" in one.read_text() and re.search(r"kind: value", one.read_text())


def test_rename_drops_the_day_from_a_dated_name(tmp_path):
    """JL 261007: a run carries no day; run-names renames run-<kind>-<MMDD>-<slug>, the older first."""
    folder = page(tmp_path)
    for name in ("run-display-0930-main-effects", "run-display-1002-main-effects", "run-section-c1"):
        (folder / "runs").mkdir(exist_ok=True)
        (folder / "runs" / (name + ".md")).write_text("see results/%s/\n" % name)
        (folder / "results" / name).mkdir(parents=True)
        (folder / "results" / name / "runtime.yaml").write_text("run: %s\n" % name)
    (folder / "draft" / "Page-evidence-items.md").write_text("- run-display-0930-main-effects → results/run-display-0930-main-effects/\n")
    names = {row["old"]: row["new"] for row in rename_plan(folder)["moves"]}
    assert names == {"run-display-0930-main-effects": "run-display-main-effects",
                     "run-display-1002-main-effects": "run-display-main-effects-2"}
    rename(folder)
    assert sorted(p.name for p in (folder / "runs").iterdir()) \
        == ["run-display-main-effects", "run-display-main-effects-2", "run-section-c1"]
    # the dropped day becomes the first pass's day (0.125): the name has none, its pass does
    first = folder / "runs" / "run-display-main-effects" / "passes" / "p01-0930"
    assert "run: run-display-main-effects\n" == (first / "runtime.yaml").read_text()
    assert (folder / "runs" / "run-display-main-effects-2" / "passes" / "p01-1002").is_dir()
    evidence = (folder / "draft" / "Page-evidence-items.md").read_text()
    assert "run-display-0930" not in evidence and "runs/run-display-main-effects/passes/p01-0930/" in evidence
