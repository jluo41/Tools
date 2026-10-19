import os
import time

from live.delivery import check_delivery, render_workspace


def test_delivery_workspace_reads_file_times_not_hashes(tmp_path):
    """JL 260928: no content hashes and no build record. A lane is current when its built
    files are at least as new as the Page, stale when one is older, not built when it has none."""
    page = tmp_path / "guide.md"
    page.write_text("# Guide\n\n## Opening\nA page.\n", encoding="utf-8")
    past = time.time() - 60
    os.utime(page, (past, past))
    delivery = tmp_path / "delivery"
    web, latex, word = delivery / "web", delivery / "latex", delivery / "word"
    for lane in (web, latex, word):
        lane.mkdir(parents=True)
    (web / "index.html").write_text("<main>Guide</main>\n", encoding="utf-8")
    (web / page.name).write_bytes(page.read_bytes())
    (latex / "guide.tex").write_text("% Guide\n", encoding="utf-8")
    (latex / "guide.pdf").write_bytes(b"PDF")
    (word / "guide.docx").write_bytes(b"DOCX")

    receipt = check_delivery(page)
    assert receipt["overall"] == "pass", receipt
    assert receipt["counts"] == {"pass": 3, "stale": 0, "not-built": 2}
    body = render_workspace(page, "", page.name)
    assert "Delivery Space" in body and "Page copy" in body and "Page saved" in body
    assert "SHA" not in body and "sha256" not in body and "manifest" not in body
    assert "grid-template-columns:1fr" in body

    page.write_text("# Guide\n\n## Opening\nA changed page.\n", encoding="utf-8")   # now newer than every build
    drifted = check_delivery(page)
    assert drifted["overall"] == "stale"
    assert drifted["counts"]["stale"] == 3
    web_rows = {row["label"]: row["state"] for row in drifted["lanes"][0]["rows"]}
    assert web_rows == {"index.html": "stale", "Page copy": "stale"}


def test_block_delivery_keeps_job_task_and_report_sources_distinct(tmp_path):
    from src.common import delivery_dir, delivery_lane_dir, delivery_source
    from src.page_workspace import load_page, build_page
    block = tmp_path / "b01_paper"
    block.mkdir()
    (block / "board.md").write_text("# Paper\n")
    for relative in ("j01_v1/t01_intro", "j02_v2/t01_intro", "reports/q01_audience"):
        folder = block / relative
        folder.mkdir(parents=True)
        (folder / (folder.name + ".md")).write_text("# " + relative + "\n\n## Opening\nA test page.\n\n## Content\nWords.\n")
        target = delivery_dir(folder)
        assert target == block / "delivery" / relative
        assert delivery_source(target) == folder
        index = build_page(load_page(folder))
        assert index == delivery_lane_dir(folder, "web") / "index.html"
        assert not (folder / "delivery").exists()
        assert check_delivery(folder / (folder.name + ".md"))["lanes"][0]["state"] == "pass"
    assert delivery_dir(block) == block / "delivery"


def test_delivery_writer_rejects_a_symlink_escape(tmp_path):
    import pytest
    from src.common import delivery_dir
    block = tmp_path / "b01_demo"
    task = block / "j01_job/t01_task"
    task.mkdir(parents=True)
    (block / "delivery").symlink_to(tmp_path / "outside", target_is_directory=True)
    with pytest.raises(ValueError, match="escapes|symlink"):
        delivery_dir(task)


def test_child_delivery_preview_links_use_block_storage(tmp_path):
    from live.space_views import delivery_space_html
    from live.delivery import render
    block = tmp_path / "b01_demo"
    folder = block / "j01_job/t01_task"
    folder.mkdir(parents=True)
    page = folder / "t01_task.md"
    page.write_text("# Task\n")
    output = block / "delivery/j01_job/t01_task/latex"
    output.mkdir(parents=True)
    (output / "t01_task.pdf").write_bytes(b"PDF")
    markup = delivery_space_html(page, checks_url="/checks", path_q="/b01_demo/board.md",
                                 file_q="j01_job/t01_task/t01_task.md",
                                 asset_base="/b01_demo/j01_job/t01_task")
    assert '/b01_demo/delivery/j01_job/t01_task/latex/t01_task.pdf' in markup
    assert '"delivery_relative": "../../delivery/j01_job/t01_task"' in render(
        page, '/b01_demo/board.md', 'j01_job/t01_task/t01_task.md',
        asset_base='/b01_demo/j01_job/t01_task')


def test_cowork_draft_export_never_writes_job_local_output(tmp_path):
    import importlib.util
    from pathlib import Path
    scripts = Path(__file__).resolve().parents[4] / "2_theme/cowork/haipipe-cowork/scripts"
    spec = importlib.util.spec_from_file_location("cowork_email_delivery_test", scripts / "email_page.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    folder = tmp_path / "b01_request/j01_office/delivery/2026-10-10-reply"
    folder.mkdir(parents=True)
    draft = folder / "reply-draft.md"
    draft.write_text("# Reply\nstatus: draft\nTo: Example\nSubject: Reply\nAttach: diagram.png\n---\nHello.\n")
    (folder / "diagram.png").write_bytes(b"SOURCE")
    out = mod.write(draft)
    assert out == tmp_path / "b01_request/delivery/j01_office/2026-10-10-reply/reply-draft.html"
    assert not (folder / "reply-draft.html").exists()
    assert out.with_name("diagram.png").read_bytes() == b"SOURCE"
    assert "Hello." in out.read_text()


def test_explicit_output_cannot_restore_task_local_delivery(tmp_path):
    import pytest
    from src.page_workspace import load_page, build_page
    folder = tmp_path / "b01_demo/j01_job/t01_task"
    folder.mkdir(parents=True)
    (folder / "t01_task.md").write_text("# Task\n\n## Opening\nWords.\n")
    with pytest.raises(ValueError, match="belong to the Block"):
        build_page(load_page(folder), folder / "delivery/web")
    assert not (folder / "delivery").exists()


def test_nested_orphan_job_report_has_no_delivery_owner(tmp_path):
    import pytest
    from src.common import delivery_dir
    folder = tmp_path / "j01_orphan/reports/q01_audience"
    folder.mkdir(parents=True)
    with pytest.raises(ValueError, match="containing Block"):
        delivery_dir(folder)
