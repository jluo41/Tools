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
