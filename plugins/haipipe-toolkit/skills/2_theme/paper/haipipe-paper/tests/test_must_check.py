"""must_check.py on a tiny made-up paper Board: auto findings mapped to must-check ids, the reading agents it names
for dispatch, the person's list, and the exit code. The sub-scripts are stubbed, except in the last test."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import must_check as mc  # noqa: E402
from test_scope_guard import board, write  # noqa: E402

SENTS = {"C1.P1": [(1, "We trained 364 models on 2,660 patients (Fig. \\ref{fig:q00})."),
                   (2, "Scaling laws guide builders \\citep{kaplan2020,TOADD}.")],
         "C1.P2": [(3, "Error fell by 8.2% at 5 minutes."), (4, "The gain fades with the horizon.")]}
ITEMS = """# t02_results · evidence items

### E01-VALUE-study · C1.P1.B1 · Patients and models
- **Target**: C1.P1.B1
- **Expected**: VALUE · j02_evidence_value/t01_values/runs/r01/result/values.md
- **Verified**: ✅ checked by script

### E02-DISPLAY-fig1 · C1.P1.B1 · Figure 1
- **Target**: C1.P1.s1
- **Expected**: DISPLAY · j01_evidence_display/t01_fig/runs/r01/result
- **Verified**: ⬜ a person checks
"""
REVISE = """# revise

### Section question · 1 · causal verbs in the Results
Why: two verbs claim a cause.
State: proposed

### Edit · C1.P1.B1 · a small edit
State: proposed
"""
HEALTH = [{"page": "t02_results", "verdict": "FAIL", "findings": [
    {"level": "FAIL", "check": "paragraphs", "message": "C1.P1 has 2 sentences", "where": ""},
    {"level": "WARN", "check": "steps", "message": "the person signs the plan", "where": ""},
    {"level": "OK", "check": "sync", "message": "all equal", "where": ""}]}]


def stub(health=HEALTH, chain=None, captions="", mark=" ⚠"):
    def run(*cmd):
        name, args = Path(str(cmd[0])).name, [str(c) for c in cmd[1:]]
        if name == "page.py" and args[0] == "health":
            return (1, json.dumps(health))
        if name == "page.py":
            return (0, "t02_results · Draft v1.2\nC1  claim\n  P1   Design   s1-s2   2 sent  20 w" + mark + "\n")
        if name == "chain_check.py":
            return (0, json.dumps({"failures": chain or []}))
        if name == "caption_check.py":
            return (0, captions)
        return (0, "")
    return run


def paper(tmp: Path) -> Path:
    t = board(tmp, "t02_results", SENTS)
    write(t / "draft" / "t02_results-evidence-items.md", ITEMS)
    write(t / "draft" / "records" / "t02_results-revise.md", REVISE)
    b = t.parent.parent
    write(b / "j03_evidence_cite" / "t99_paper_citation_check" / "runs" / "r01_check" / "result" / "citations.csv",
          "key,status\nkaplan2020,card-only\n")
    (b / "j01_evidence_display").mkdir()
    return t


def test_section_gate(tmp_path, monkeypatch):
    t = paper(tmp_path)
    monkeypatch.setattr(mc, "run", stub(captions="✅ t01 · r01: fine\n❗ t02 · r01: the caption names Figure 9, "
                                                 "which the current numbering does not have\n"))
    rep = mc.gate(t)
    ids = {(a["id"], a["where"]) for a in rep["auto"] if a["level"] == "FAIL"}
    assert ("M-A02", "t02_results") in ids                       # health paragraphs and the structure ⚠ line
    assert ("M-B07", "t02_results") in ids                       # \citep{TOADD}
    assert ("M-E04", "t02_results") in ids                       # no review Run at v1.2
    assert ("M-D12", "j01_evidence_display") in ids              # caption names a display that is not there
    assert rep["failed"] >= 4 and rep["versions"] == {"t02_results": "v1.2"}
    agents = [d["agent"] for d in rep["dispatch"]]
    assert agents[:4] == ["haipipe-draft-eval-structure-agent", "haipipe-draft-eval-paragraph-agent",
                          "haipipe-draft-eval-sentence-agent", "haipipe-draft-ab-reader-agent"]
    assert "haipipe-draft-evidence-value-agent" in agents       # s3 prints 8.2 with no VALUE item
    assert "haipipe-draft-evidence-cite-agent" in agents        # kaplan2020 is card-only
    assert "haipipe-draft-evidence-display-agent" in agents     # s1 calls a figure
    assert agents[-1] == "haipipe-draft-consistency-agent"
    person = {(p["kind"], p["where"]) for p in rep["person"]}
    assert ("number", "t02_results C1.P2.s3") in person
    assert ("number", "t02_results C1.P1.s1") not in person     # covered by E01 (bullet B1)
    assert ("cite", "t02_results") in person and ("fact", "t02_results") in person
    assert ("sign", "t02_results") in person
    claims = [p["what"] for p in rep["person"] if p["kind"] == "claim"]
    assert claims == ["M-E06 Section question · 1 · causal verbs in the Results: proposed"]
    text = mc.render(rep)
    assert "## Dispatch" in text and "## For the person" in text and "C1.P2.s3" in text


def test_review_runs_at_the_version_clear_d1(tmp_path, monkeypatch):
    t = paper(tmp_path)
    b = t.parent.parent
    for task, run in (("t01_sentence_review", "r02_t02_review_v1.2"), ("t03_paragraph_logic", "r01_t02_review_v1.2"),
                      ("t04_structure", "r01_t02_structure_v1.2"), ("t01_sentence_review", "r03_t01_review_v1.2")):
        (b / "j31_review_x_v0101" / task / "runs" / run / "result").mkdir(parents=True)
    monkeypatch.setattr(mc, "run", stub(health=[{"findings": []}]))
    rep = mc.gate(t)
    assert not [a for a in rep["auto"] if a["id"] == "M-E04"]
    agents = [d["agent"] for d in rep["dispatch"]]
    assert "haipipe-draft-eval-sentence-agent" not in agents and "haipipe-draft-eval-structure-agent" not in agents
    assert any("already ran at v1.2" in n for n in rep["notes"])


def test_version_job_scopes_and_exit(tmp_path, monkeypatch):
    t = paper(tmp_path)
    job = t.parent
    other = board(tmp_path, "t01_introduction", {"C1.P1": [(1, "Builders follow laws.")]})
    assert other.parent == job
    chain = [{"rule": 6, "where": f"{job.name}/t01_introduction/draft/x.md", "what": "stale"},
             {"rule": 7, "where": "j02_evidence_value/scripts/recompute_check.py", "what": "exited 1"}]
    monkeypatch.setattr(mc, "run", stub(health=[{"findings": []}], chain=chain))
    sec = mc.gate(t)
    assert [a["where"] for a in sec["auto"] if a["id"] == "M-B01"] == ["j02_evidence_value/scripts/recompute_check.py"]
    ver = mc.gate(job)
    assert ver["mode"] == "version" and set(ver["versions"]) == {"t01_introduction", "t02_results"}
    assert len([a for a in ver["auto"] if a["id"] == "M-B01"]) == 2
    assert mc.main([str(t)]) == 1
    clean = board(tmp_path / "clean", "t02_results", {"C1.P1": [(1, "The gain fades with the horizon.")]})
    for task in ("t01_sentence_review", "t03_paragraph_logic"):
        (clean.parent.parent / "j31_review_x" / task / "runs" / "r01_t02_review_v1.2").mkdir(parents=True)
    monkeypatch.setattr(mc, "run", stub(health=[{"findings": []}], mark=""))
    assert mc.main([str(clean), "--json"]) == 0


def test_real_scripts_run_read_only(tmp_path):
    t = paper(tmp_path)
    before = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    rep = mc.gate(t)
    assert rep["mode"] == "section" and rep["dispatch"] and isinstance(rep["auto"], list)
    after = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    assert before == after
