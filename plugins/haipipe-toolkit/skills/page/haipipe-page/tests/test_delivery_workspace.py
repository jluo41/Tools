import hashlib
import json

from live.delivery import check_delivery, render_workspace


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_delivery_workspace_passes_matching_lanes_and_flags_source_drift(tmp_path):
    page = tmp_path / "guide.md"
    page.write_text("# Guide\n\n## Opening\nA page.\n", encoding="utf-8")
    delivery = tmp_path / "delivery"
    web = delivery / "web"
    latex = delivery / "latex"
    word = delivery / "word"
    for lane in (web, latex, word):
        lane.mkdir(parents=True)
    (web / "index.html").write_text("<main>Guide</main>\n", encoding="utf-8")
    (web / page.name).write_bytes(page.read_bytes())
    (web / ".haipipe-page-export").write_text(
        json.dumps({
            "schema": "haipipe-page-export/v2",
            "source": page.name,
            "source_sha256": _sha256(page),
        }),
        encoding="utf-8",
    )
    tex = latex / "guide.tex"
    pdf = latex / "guide.pdf"
    docx = word / "guide.docx"
    tex.write_text("% Guide\n", encoding="utf-8")
    pdf.write_bytes(b"PDF")
    docx.write_bytes(b"DOCX")
    manifest = {
        "source": {"path": page.name, "sha256": _sha256(page)},
        "outputs": {
            "web": {"path": "delivery/web/index.html", "sha256": _sha256(web / "index.html")},
            "latex": {
                "tex": "delivery/latex/guide.tex", "tex_sha256": _sha256(tex),
                "pdf": "delivery/latex/guide.pdf", "pdf_sha256": _sha256(pdf),
            },
            "word": {"docx": "delivery/word/guide.docx", "docx_sha256": _sha256(docx)},
        },
    }
    (delivery / "build-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    receipt = check_delivery(page)
    assert receipt["overall"] == "pass", receipt
    assert receipt["counts"] == {"pass": 3, "stale": 0, "unverified": 0, "not-built": 2}
    body = render_workspace(page, "", page.name)
    assert "Delivery Workspace" in body
    assert "source fingerprint" in body
    assert "content mirror" in body

    page.write_text("# Guide\n\n## Opening\nA changed page.\n", encoding="utf-8")
    drifted = check_delivery(page)
    assert drifted["overall"] == "stale"
    assert drifted["counts"]["stale"] == 3
