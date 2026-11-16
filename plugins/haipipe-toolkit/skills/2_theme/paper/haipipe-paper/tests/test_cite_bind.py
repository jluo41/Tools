"""haipipe-paper-evidence cite_tasks.py bind (cite_bind.py, must-check M-D20) on a tiny made-up paper Board: a dry run
prints the diff and writes nothing; --apply writes each CITE item's Local Run (and its discovery Run as Supporting
Runs) by BibTeX key; a second run binds nothing; a kept Local Run, a retired item and an unchecked key are left."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "haipipe-paper-evidence" / "scripts"))
import cite_tasks  # noqa: E402

CSV = ("key,group,status,cited_in,title,year,verified,discovery_runs\n"
       "kaplan2020,t01_scaling_laws,card-only,,T,2020,nobody yet,b01.j03.t01.r01\n"
       "Lutsker_2026,t02_glucose,card-only,,T,2026,nobody yet,\n")
ITEMS = """# t01_note · evidence items

### E01-CITE-kaplan · C1.P1.B1 · kaplan2020
- **Target**: C1.P1.B1
- **Label**: kaplan2020
- **Local Input**: @misc{kaplan2020,

### E02-CITE-lutsker · C1.P1.B2 · Lutsker
- **Target**: C1.P1.B2
- **Label**: Lutsker
- **Expected**: CITE · @article{Lutsker_2026, title={A model}, year={2026} }
- **Local Run**: \u2014

### E03-CITE-kept · C1.P1.B3 · kaplan2020
- **Target**: C1.P1.B3
- **Label**: kaplan2020
- **Local Run**: Page · Evidence Item · reuse · run-citation-x → runs/run-citation-x/passes/p01/result.yaml

### E04-CITE-unknown · C1.P1.B4 · nobody2020
- **Target**: C1.P1.B4
- **Label**: nobody2020

#### E05-CITE-old · retired · was C1.P1.B5
- **Label**: kaplan2020
"""


def board(tmp: Path) -> Path:
    b = tmp / "Project-X/paper/Paper-Demo"
    task = b / "j11_writing_v1/t01_note"
    (task / "draft").mkdir(parents=True)
    (task / "draft/t01_note-evidence-items.md").write_text(ITEMS, encoding="utf-8")
    for group, rows in (("t01_scaling_laws", CSV.rsplit("Lutsker", 1)[0]), ("t99_paper_citation_check", CSV)):
        r = b / "j03_evidence_cite" / group / "runs/r01_check_citations/result"
        r.mkdir(parents=True)
        (r / "citations.csv").write_text(rows, encoding="utf-8")
    return task


def test_dry_run_prints_the_diff_and_writes_nothing(tmp_path, capsys):
    task = board(tmp_path)
    before = (task / "draft/t01_note-evidence-items.md").read_text(encoding="utf-8")
    cite_tasks.main(["bind", str(task)])
    out = capsys.readouterr().out
    assert (task / "draft/t01_note-evidence-items.md").read_text(encoding="utf-8") == before
    assert "+- **Local Run**: Page · Evidence Item · reuse · P.j03.t01.r01 → " \
           "j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result/citations.csv" in out
    assert "dry run" in out


def test_apply_binds_by_bibtex_key_and_keeps_the_rest(tmp_path, capsys):
    task = board(tmp_path)
    cite_tasks.main(["bind", str(task), "--apply"])
    out = capsys.readouterr().out
    text = (task / "draft/t01_note-evidence-items.md").read_text(encoding="utf-8")
    e1, e2, e3, e4, e5 = text.split("\n### ")[1:4] + text.split("\n### ")[4].split("\n#### ")
    assert "- **Supporting Runs**: Discovery · reuse · b01.j03.t01.r01\n- **Local Run**: Page · Evidence Item · " \
           "reuse · P.j03.t01.r01 → j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result/citations.csv" in e1
    # E02's key is its BibTeX's, not its Label; only the t99 check holds it; its empty dash line is replaced
    assert "reuse · P.j03.t99.r01 → j03_evidence_cite/t99_paper_citation_check/" in e2
    assert "Local Run**: \u2014" not in e2 and "Supporting Runs" not in e2
    assert e3.count("Local Run") == 1 and "run-citation-x" in e3
    assert "Local Run" not in e4 and "no citation Run checked this key" in out
    assert "Local Run" not in e5
    cite_tasks.main(["bind", str(task)])
    assert "nothing to bind" in capsys.readouterr().out

