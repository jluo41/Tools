"""`page.py export`: the LaTeX and Word doors run from the terminal as the Board server runs them."""
from src import page_export


def _space(tmp_path):
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    (tmp_path / "code").mkdir()
    board = tmp_path / "examples" / "P" / "papers" / "Paper-X"
    page = board / "Ba-X-Main" / "S-X-Main-1-Intro"
    page.mkdir(parents=True)
    (board / "board.md").write_text("# Paper-X\n", encoding="utf-8")
    (page / "S-X-Main-1-Intro.md").write_text("# S-X-Main-1-Intro\n\n## Opening\nA page.\n", encoding="utf-8")
    return board, page


def test_the_root_is_the_folder_the_board_server_serves(tmp_path):
    board, page = _space(tmp_path)
    assert page_export.repo_root(page) == tmp_path.resolve()


def test_export_resolves_the_page_exactly_as_the_board_server(tmp_path, monkeypatch):
    board, page = _space(tmp_path)
    page_export._exporter(tmp_path)                    # bootstraps the servers' `live` namespace
    import live.export

    def door(self, payload):                           # stands in for LuaLaTeX / md2docx
        source, found = self.target(payload)
        return {"source": str(source), "board": str(found), "author": payload.get("author")}, None

    monkeypatch.setattr(live.export.ExportMixin, "export_latex", door)
    monkeypatch.setattr(live.export.ExportMixin, "export_word", door)
    results = page_export.export(page, ["latex", "word"], author="Junjie Luo")
    face = (page / "S-X-Main-1-Intro.md").resolve()
    assert results["latex"] == {"ok": True, "source": str(face), "board": str(board.resolve()), "author": None}
    assert results["word"]["author"] == "Junjie Luo" and results["word"]["source"] == str(face)


def test_a_folder_that_is_not_a_page_is_refused_by_name(tmp_path):
    board, page = _space(tmp_path)
    stray = board / "notes"
    stray.mkdir()
    results = page_export.export(stray, ["latex"])
    assert results["latex"]["ok"] is False and results["latex"]["err"]


def test_each_lane_has_one_fixed_run_whose_ticket_code_writes(tmp_path):
    """JL 260928: one Run per lane (`run-delivery-webpage`), rerun in place, never rd01_web, rd02_web."""
    board, page = _space(tmp_path)
    (page / "runs" / "delivery-run").mkdir(parents=True)        # an older Page with Space folders
    first = page_export.write_ticket(page, "word", "Junjie Luo")
    again = page_export.write_ticket(page, "word", "Junjie Luo")
    # one folder per Run (0.125): the lane's Run is runs/run-delivery-word/ with its command and card
    assert first == again == page / "runs" / "run-delivery-word" / "run-delivery-word.sh"
    text = first.read_text(encoding="utf-8")
    assert 'page="$(cd "$(dirname "$0")/../.." && pwd)"' in text
    assert 'export "$page" --lane word --author "Junjie Luo"' in text
    assert sorted(p.name for p in first.parent.iterdir()) == ["run-delivery-word.sh", "run.yaml"]
    assert sorted(p.name for p in (page / "runs").iterdir()) == ["delivery-run", "run-delivery-word"]
    (page / "runs" / "run-delivery-latex.sh").write_text("old flat ticket\n", encoding="utf-8")
    page_export.write_ticket(page, "latex")                     # an older flat ticket is the same Run
    assert not (page / "runs" / "run-delivery-latex.sh").exists()
    assert (page / "runs" / "run-delivery-latex" / "run-delivery-latex.sh").is_file()


def test_run_names_keeps_old_builds_and_adds_each_built_lanes_run(tmp_path):
    """An older numbered build (rd01_latex) stays as history; each lane with built files gets its one Run."""
    from src import run_rename
    board, page = _space(tmp_path)
    (page / "runs").mkdir()
    (page / "runs" / "rd01_latex.md").write_text("# rd01_latex\n", encoding="utf-8")
    (page / "delivery" / "latex").mkdir(parents=True)
    (page / "delivery" / "latex" / "S-X-Main-1-Intro.pdf").write_bytes(b"PDF")
    report = run_rename.apply(page)
    assert [k["old"] for k in report["kept"]] == ["rd01_latex"] and report["fixed"] == ["latex"]
    assert (page / "runs" / "rd01_latex.md").is_file()
    assert (page / "runs" / "run-delivery-latex" / "run-delivery-latex.sh").is_file()
    assert run_rename.plan(page)["fixed"] == []                 # a second pass adds nothing


def test_a_fixed_delivery_run_is_done_while_its_lane_is_current(tmp_path):
    import os
    import time
    board, page = _space(tmp_path)
    page_export._exporter(tmp_path)
    from live.runs import local_runs
    face = page / "S-X-Main-1-Intro.md"
    past = time.time() - 60
    os.utime(face, (past, past))
    for lane in ("web", "latex"):
        page_export.write_ticket(page, lane)
    (page / "delivery" / "web").mkdir(parents=True)
    (page / "delivery" / "web" / "index.html").write_text("<main>x</main>", encoding="utf-8")
    (page / "delivery" / "web" / face.name).write_bytes(face.read_bytes())
    rows = {r["run_id"]: r for r in local_runs(face) if r.get("operation") == "delivery"}
    assert {k: v["status"] for k, v in rows.items()} == {"run-delivery-webpage": "Done", "run-delivery-latex": "Ready"}
    assert rows["run-delivery-webpage"]["audit"] == [] and rows["run-delivery-webpage"]["runtime"] is None
