"""A letter that says "on behalf of my co-authors" in its own words prints it once (Pp-AgreeableRx 261122)."""
from test_build_delivery import _cover_module


def _build(tmp_path, monkeypatch, words):
    cl = _cover_module()
    root = tmp_path / "Paper-T"; here = root / "delivery"; here.mkdir(parents=True)
    page_dir = root / "Bc-T-Round" / "RD02-T-submission-20260929"; page_dir.mkdir(parents=True)
    (page_dir / "RD02-T-submission-20260929.md").write_text("# RD02\n\n## Content\n\n### Cover letter\n\n" + words)
    monkeypatch.setattr(cl, "pdf_text", lambda p: "")
    monkeypatch.setattr(cl, "pdf_pages", lambda p: None)
    cfg = {"coverletter": {"round": "RD02", "journal": "MIS Quarterly", "signatory": "A Author",
                           "authors": ["A Author", "B Author", "C Author"], "affiliation": "", "email": ""}}
    out = {"cover_letter_pdf": "cover-letter/c.pdf", "cover_letter_docx": "cover-letter/c.docx"}
    cl.build_cover_letter(cfg, {}, root, here, out, title="T", main_pdf=here / "m.pdf", tables=1, figures=1,
                          run=lambda cmd, **kw: type("R", (), {"returncode": 0})())
    from docx import Document
    docx = "\n".join(p.text for p in Document(here / "cover-letter" / "c.docx").paragraphs)
    return docx, (here / "cover-letter" / "c.tex").read_text()


def test_the_letters_own_sentence_is_printed_once(tmp_path, monkeypatch):
    words = ("We submit our paper.\n\nI submit this manuscript on behalf of my co-authors B Author and C Author. "
             "It is not under review elsewhere.\n")
    docx, tex = _build(tmp_path, monkeypatch, words)
    assert docx.lower().count("on behalf of") == 1 and tex.lower().count("on behalf of") == 1


def test_without_it_the_engine_adds_it(tmp_path, monkeypatch):
    docx, tex = _build(tmp_path, monkeypatch, "We submit our paper.\n")
    assert "on behalf of my co-authors, B Author and C Author." in docx and "on behalf of" in tex
