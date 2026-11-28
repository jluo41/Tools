"""A Section bound by hai-paper-evidence `cite_tasks.py bind` still exports (must-check M-D20): bind writes a
Local Run whose Result path is relative to the paper Board, and the LaTeX and Word writers, health and Draft Lab
read it through the one resolver (src/result_paths.py), so the export's evidence selection passes and reaches its
converter. ScalingGlucose t01 (261115) stopped on "E01-CITE-lutsker-2026: selected Result is missing" before."""
import importlib.util
from pathlib import Path

import pytest
from live.export import ExportMixin
from src.evidence_selection import selected_results
from src.result_paths import resolve

BIND = Path(__file__).resolve().parents[4] / "3_theme/paper/hai-paper-evidence/scripts/cite_bind.py"
CSV = "key,group,status,title,year,verified,discovery_runs\nLutsker_2026,t02_glucose,card-only,T,2026,nobody yet,\n"
ITEMS = ("# t01_note · evidence items\n\n### E01-CITE-lutsker-2026 · C1.P1.B1 · Lutsker_2026\n- **Target**: C1.P1.B1\n"
         "- **Label**: Lutsker_2026\n- **Need**: the sentence states this\n- **Expected**: CITE · @article{Lutsker_2026,\n"
         "- **Acceptance**: the source says it\n- **Verified**: \u2b1c a person checks\n"
         "- **Local Input**: @article{Lutsker_2026,\n")


class Reached(Exception):
    pass


def bound_section(tmp_path: Path) -> Path:
    board = tmp_path / "paper" / "Paper-Demo"
    task = board / "j11_writing_v1" / "t01_note"
    (task / "draft").mkdir(parents=True)
    (board / "board.md").write_text("# Paper\n")
    page = task / "t01_note.md"
    page.write_text("# t01_note\n\n## Opening\nQuestion?\n\n## Content\n\nA sentence \\citep{Lutsker_2026}.\n")
    (task / "draft" / "t01_note-evidence-items.md").write_text(ITEMS)
    res = board / "j03_evidence_cite/t02_glucose/runs/r01_check_citations/result"
    res.mkdir(parents=True)
    (res / "citations.csv").write_text(CSV)
    (res / "runtime.yaml").write_text("run: r01_check_citations\nstatus: completed\nexit_code: 0\n")
    spec = importlib.util.spec_from_file_location("cite_bind", BIND)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.bind(task, apply=True)
    assert "reuse · P.j03.t02.r01 → j03_evidence_cite/" in (task / "draft/t01_note-evidence-items.md").read_text()
    return page


def test_a_board_relative_binding_resolves_from_the_section(tmp_path):
    page = bound_section(tmp_path)
    rel = "j03_evidence_cite/t02_glucose/runs/r01_check_citations/result/citations.csv"
    assert resolve(rel, tmp_path / "elsewhere", page.parent) == page.parents[2] / rel
    assert resolve("j03_evidence_cite/nope.csv", tmp_path, page.parent) is None
    assert selected_results(page) == []          # receipt-bound: nothing to select, and nothing missing


@pytest.mark.parametrize("method", ["export_latex", "export_word"])
def test_latex_and_word_reach_their_converter_after_bind(tmp_path, method):
    page = bound_section(tmp_path)
    out = tmp_path / "out"
    out.mkdir()

    class Fake(ExportMixin):
        root = tmp_path
        def _export_target(self, payload, workbench): return page, out, tmp_path, None
        def _canon_ctx(self, board, payload): return {}
        def _rebuild_ui(self, route, payload): return "", ""
        def _run(self, *args, **kwargs): raise Reached()

    try:
        result, error = getattr(Fake(), method)({})
    except Reached:
        return
    assert "selected Result is missing" not in str(error)
