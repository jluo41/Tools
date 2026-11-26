"""The Word copy cites with the labels LaTeX printed in master.bbl (Pp-AgreeableRx 261122)."""
import re
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

APACITE = r"""\begin{thebibliography}{}
\bibitem [\protect \citeauthoryear {%
Lu%
\ \BBA {} Rui%
}{%
Lu%
\ \BBA {} Rui%
}{%
{\protect \APACyear {2018}}%
}]{%
Lu_2018}
\bibitem [\protect \citeauthoryear {%
{Centers for Medicare \& Medicaid Services}%
}{%
{Centers for Medicare \& Medicaid Services}%
}{%
{\protect \APACyear {2026}}%
{\protect \APACexlab {{\protect \BCnt {2}}}}}]{%
cms_b}
\bibitem [\protect \citeauthoryear {%
{Centers for Medicare \& Medicaid Services}%
}{%
{Centers for Medicare \& Medicaid Services}%
}{%
{\protect \APACyear {2026}}%
{\protect \APACexlab {{\protect \BCnt {1}}}}}]{%
cms_a}
\end{thebibliography}
"""


def _ns(tmp_path, bbl):
    (tmp_path / "master.bbl").write_text(bbl, encoding="utf-8")
    ns = {"MASTER": tmp_path / "master.tex", "LATEX_ROOM": tmp_path, "BIB": {},
          "latex_to_text": lambda s: re.sub(r"[{}\\]", "", s), "author_date_label": lambda k: "Someone, 1999"}
    exec(compile((SCRIPTS / "bbl_labels.py").read_text(encoding="utf-8"), "bbl_labels.py", "exec"), ns)
    return ns


def test_apacite_labels_and_year_letters(tmp_path):
    ns = _ns(tmp_path, APACITE)
    assert ns["cite_label"]("Lu_2018") == ("Lu & Rui", "2018")
    assert ns["cite_label"]("Lu_2018", narrative=True) == ("Lu and Rui", "2018")
    assert ns["author_date_group"](["cms_b", "cms_a", "Lu_2018"]) == \
        "Centers for Medicare & Medicaid Services, 2026a, 2026b; Lu & Rui, 2018"


def test_natbib_label_and_fallback(tmp_path):
    ns = _ns(tmp_path, "\\begin{thebibliography}{1}\n\\bibitem[{Soto}(2017)]{soto}\nx\n\\end{thebibliography}\n")
    assert ns["cite_label"]("soto") == ("Soto", "2017")
    assert ns["cite_label"]("missing") == ("Someone", "1999")


def test_informs_and_between_two_authors(tmp_path):
    """INFORMS's bst writes "and" as \\protect\\BIBand{}; the Word copy printed "(Chen Chan, 2024)" (TestToLearn 261123)."""
    bbl = ("\\begin{thebibliography}{2}\n\\bibitem[{Chen \\protect\\BIBand{} Chan(2024)}]{chen2024large}\nx\n"
           "\\bibitem[{Paley \\protect\\BIBand{} van~de Ven(2023)}]{paley}\ny\n\\end{thebibliography}\n")
    ns = _ns(tmp_path, bbl)
    assert ns["cite_label"]("chen2024large") == ("Chen and Chan", "2024")
    assert ns["cite_label"]("paley")[0].startswith("Paley and van")


def test_a_build_leaves_a_word_in_use_alone(monkeypatch):
    import sys
    sys.path.insert(0, str(SCRIPTS))
    import word_lock
    monkeypatch.setenv("HAIPIPE_WORD_PREVIEW", "word")
    assert word_lock.word_in_use() is False          # asked for: Word is used even with documents open
    monkeypatch.delenv("HAIPIPE_WORD_PREVIEW")
    calls = []
    monkeypatch.setattr(word_lock, "OWN_FOLDERS", ("haipipe-preview",))
    import subprocess
    def fake(cmd, **kw):
        calls.append(cmd[0])
        out = "Macintosh HD:Users:x:OneDrive:cover-letter.docx" if cmd[0] == "osascript" else ""
        return subprocess.CompletedProcess(cmd, 0, stdout=out, stderr="")
    monkeypatch.setattr(subprocess, "run", fake)
    assert word_lock.word_in_use() is True and calls == ["pgrep", "osascript"]
