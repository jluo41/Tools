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
    assert run_names.mint("section", "whole-Section readability cleanup after the delivery",
                          day="2026-09-14T10:00") == "run-section-0914-whole-section-readability-cleanup"
    assert run_names.mint("revise", "c1-p2", day="2026-09-28",
                          taken={"run-revise-0928-c1-p2"}) == "run-revise-0928-c1-p2-2"
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
    assert run == "run-section-0929-c1" and opened["ticket"] == "runs/%s.md" % run
    assert "status: open" in (folder / "runs" / (run + ".md")).read_text()
    assert not (folder / "results").exists()
    assert find_open(folder, "section", "C1") == run
    closed = close_run(folder, run, summary="tightened three sentences")
    assert closed["result"] == "results/%s/" % run
    runtime = (folder / "results" / run / "runtime.yaml").read_text()
    assert "status: complete" in runtime and "skills: haipipe-page-writing · haipipe-writing" in runtime
    assert "status: closed" in (folder / "runs" / (run + ".md")).read_text()
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
    assert names == {"rp-sec-01": "run-section-0914-whole-section-readability-cleanup",
                     "pj02t03r01_headline": "run-value-0906-headline-estimate",
                     "re-value-01_headline": "run-value-0928-headline-estimate"}
    rename(folder)
    tickets = sorted(p.stem for p in (folder / "runs").iterdir() if p.is_file())
    results = sorted(p.name for p in (folder / "results").iterdir())
    assert tickets == results == sorted(names.values())          # one ticket ↔ one result, flat
    assert not any(p.is_dir() for p in (folder / "runs").iterdir())
    evidence = (folder / "draft" / "Page-evidence-items.md").read_text()
    assert "run-value-0906-headline-estimate → results/run-value-0906-headline-estimate/result.yaml" in evidence
    assert "pj02t03r01" not in evidence
    assert "results/run-value-0928-headline-estimate/" in (folder / "runs" / "run-value-0928-headline-estimate.md").read_text()
    assert "had no ticket" in (folder / "runs" / "run-value-0906-headline-estimate.md").read_text()
    assert re.search(r"kind: value", (folder / "runs" / "run-value-0906-headline-estimate.md").read_text())
