"""cite_support.py and send_check.py: a citing sentence read against its source, and the one check before a send
that keeps "prints wrong" apart from "not recorded" (AgreeableJama-Board 261123)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cite_support as cs  # noqa: E402
import send_check as sc  # noqa: E402

GRAY = r"an opioid prescription was filled after 21.6\% of visits from 2009 to 2017 \citep{Gray2021}."


def row(reading="", passage="", note="", sentence="s3", key="Gray2021", text=GRAY):
    return {"section": "t01_introduction", "sentence": sentence, "key": key, "text": cs.plain(text),
            "hash": cs.digest(text), "reading": reading, "passage": passage, "note": note}


def test_a_quoted_number_is_a_percent_or_a_decimal_not_a_year():
    assert cs.numbers(GRAY) == ["21.6"]
    assert cs.plain(GRAY).endswith("21.6% of visits from 2009 to 2017.")


def test_supports_needs_the_number_in_its_passage(tmp_path):
    J = cs.judge([row("supports", "opioid prescribing rates fell")], tmp_path)
    assert [w for _, w in J["wrong"]] == ["quotes 21.6, which no supporting passage holds"]
    J = cs.judge([row("supports", "the rate of opioid prescribing was 21.6% (11 978)")], tmp_path)
    assert len(J["ok"]) == 1 and not J["wrong"]


def test_the_cite_agents_words_read_the_same(tmp_path):
    J = cs.judge([row("partly: prescribing, not filling", "x", sentence="s1"), row("does not", sentence="s2"),
                  row("unclear: abstract only", sentence="s3")], tmp_path)
    assert [r["sentence"] for r, _ in J["wrong"]] == ["s1", "s2"] and len(J["person"]) == 1


def test_each_reading_lands_in_its_group(tmp_path):
    J = cs.judge([row("looser", "x", "prescribing, not filling", sentence="s1"), row(sentence="s2"),
                  row("not checkable", sentence="s4"), row("supports", sentence="s5"), row("maybe", sentence="s6")],
                 tmp_path)
    assert [r["sentence"] for r, _ in J["wrong"]] == ["s1"]
    assert [r["sentence"] for r, _ in J["missing"]] == ["s2", "s5", "s6"]
    assert [r["sentence"] for r, _ in J["person"]] == ["s4"]


BBL = r"""\begin{thebibliography}{3}
\bibitem{Gray2021}
Gray BM. Clinical knowledge. \newblock JAMA Network Open. 2021;4(7):e2115328.
\bibitem{web}
{CMS}. Condition categories; 2024. \newblock Accessed: 2026-10-22. \newblock \url{https://example.test/c}.
\bibitem{book}
Rothman KJ. Modern Epidemiology. Lippincott; 2008.
\end{thebibliography}
"""


def test_a_reference_without_doi_or_url_and_an_access_date_as_data(tmp_path):
    f = tmp_path / "master.bbl"
    f.write_text(BBL, encoding="utf-8")
    assert list(sc.bbl_items(BBL)) == ["Gray2021", "web", "book"]
    lines = sc.web_lines(f, {"Gray2021": "10.1001/jamanetworkopen.2021.15328"})
    assert lines[0].startswith("Gray2021: the bib holds doi 10.1001/jamanetworkopen.2021.15328, the reference prints none")
    assert lines[1].startswith("web: the access date prints as 'Accessed: 2026-10-22'")
    assert lines[2] == "book: no DOI and no URL printed"


def test_the_report_keeps_the_groups_apart():
    text = sc.render(Path("Paper-X"), "j11", [("citations · web", "a")], [("values · chain", "b")], [])
    assert text.index("prints something wrong") < text.index("A record is missing")
    assert "Waits on a person" not in text and "nothing printed wrong" not in text
    assert "✅ nothing printed wrong was found" in sc.render(Path("P"), "j11", [], [], [])
