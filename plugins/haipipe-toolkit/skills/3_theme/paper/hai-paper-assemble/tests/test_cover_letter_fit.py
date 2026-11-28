"""A cover letter prints on one page: space shrinks first, then 11 pt; the closing never breaks (Pp-AgreeableRx 261122)."""
from test_build_delivery import _cover_module


def _build(tmp_path, monkeypatch, pages_at):
    cl = _cover_module()
    root = tmp_path / "Paper-T"; here = root / "delivery"; here.mkdir(parents=True)
    page_dir = root / "Bc-T-Round" / "RD02-T-submission-20260929"; page_dir.mkdir(parents=True)
    (page_dir / "RD02-T-submission-20260929.md").write_text("# RD02\n\n## Content\n\n### Cover letter\n\nWe submit it.\n")
    sizes = []
    def fake(cmd, **kw):
        sizes.append((kw["cwd"] / "c.tex").read_text().split("documentclass[", 1)[1][:4])
        return type("R", (), {"returncode": 0})()
    monkeypatch.setattr(cl, "pdf_text", lambda p: "")
    monkeypatch.setattr(cl, "pdf_pages", lambda p: pages_at(len(sizes)) if p.name == "c.pdf" else None)
    cfg = {"coverletter": {"round": "RD02", "journal": "J", "signatory": "A", "authors": ["A"], "affiliation": "x", "email": "y"}}
    out = {"cover_letter_pdf": "cover-letter/c.pdf", "cover_letter_docx": "cover-letter/c.docx"}
    rep = cl.build_cover_letter(cfg, {}, root, here, out, title="T", main_pdf=here / "m.pdf", tables=1, figures=1, run=fake)
    return {c["check"]: c for c in rep["checks"]}, sizes, here


def test_a_spill_shrinks_space_then_type_and_word_follows(tmp_path, monkeypatch):
    checks, sizes, here = _build(tmp_path, monkeypatch, lambda tries: 1 if tries >= 4 else 2)
    assert sizes == ["12pt", "12pt", "12pt", "11pt"] and checks["letter fits one page"]["ok"]
    tex = (here / "cover-letter" / "c.tex").read_text()
    assert "\\begin{minipage}{\\linewidth}Sincerely," in tex
    from docx import Document
    d = Document(here / "cover-letter" / "c.docx")
    assert d.styles["Normal"].font.size.pt == 11
    assert [p.paragraph_format.keep_with_next for p in d.paragraphs if p.text == "Sincerely,"] == [True]


def test_a_letter_that_never_fits_fails_loudly(tmp_path, monkeypatch):
    checks, sizes, _ = _build(tmp_path, monkeypatch, lambda tries: 2)
    assert len(sizes) == 4 and not checks["letter fits one page"]["ok"]
    assert "shorten the letter" in checks["letter fits one page"]["detail"]


def test_a_one_page_letter_is_built_once(tmp_path, monkeypatch):
    checks, sizes, _ = _build(tmp_path, monkeypatch, lambda tries: 1)
    assert sizes == ["12pt"] and checks["letter fits one page"]["detail"] == "1 page(s)"
