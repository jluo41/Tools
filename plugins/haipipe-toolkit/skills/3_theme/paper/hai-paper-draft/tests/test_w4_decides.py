"""W4 (CONSTITUTION A01, JL 261118): a sentence under 8 is open until the AI settles it (`AI decided:` on its Pass line)
or an AI comment asks the person; a card left `State: proposed` keeps W4 open."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cli"))
from section_workflow import w4_counts  # noqa: E402

PASS = """### Revise review report
Sentences:
- C1.P1.s1 · logic 9/10 · read 9/10 · ai 9/10 · link: x · ok · Fix: none
- C1.P1.s2 · logic 7/10 · read 8/10 · ai 8/10 · link: x · weak · Fix: none
- C1.P1.s3 · logic 8/10 · read 7/10 · ai 8/10 · link: x · stiff · Fix: none · AI decided: keep, two rounds no easier
- C1.P1.s4 · logic 6/10 · read 8/10 · ai 8/10 · link: x · claim · Fix: none · asked in Comment 3
"""


def test_counts():
    assert w4_counts(PASS) == (1, 2, 0)


def test_proposed_card_waits():
    assert w4_counts(PASS + "\n### Edit · s2 · x\nState: proposed\n")[2] == 1


def test_titles():
    from section_workflow import title_counts, titles_in
    draft = "### Structure Overview\n- C1 · Part one\n- C1.P1 · Para\n  → s1 to s2\n\n## 3 · Draft\n### C1.P1 · Para · s1 to s2\n"
    assert titles_in(draft) == {"C1", "C1.P1"}
    rated, open_, settled = title_counts("Titles:\n- C1 · title 9/10 · x · Fix: none\n"
                                         "- C1.P1 · title 7/10 · x · AI decided: keep · Fix: none\n")
    assert rated == {"C1", "C1.P1"} and (open_, settled) == (0, 1)


def test_card_with_comment_may_wait():
    p = PASS + "\n### Edit · s2 · x\nAnswers: Comment 3\nState: proposed\n"
    assert w4_counts(p)[2] == 0


def test_paragraphs_counted():
    from section_workflow import paragraph_counts
    rated, open_, settled = paragraph_counts("Paragraphs:\n- C1.P1 · 7/10 · x\n- C1.P2 · 9/10 · y\n")
    assert rated == {"C1.P1", "C1.P2"} and (open_, settled) == (1, 0)


def test_newest_pass_by_number(tmp_path):
    """A record listing Pass 7 above Pass 6 still gives Pass 7, as the page does (t00_abstract 261118)."""
    from section_workflow import newest_pass
    rec = tmp_path / "draft" / "records"
    rec.mkdir(parents=True)
    body = "### Revise review report\nSentences:\n- C1.P1.s1 · logic 9/10 · read 9/10 · ai 9/10 · ok\n"
    (rec / "x-revise.md").write_text(f"## Pass 7 · 2026-11-18 · on draft v1.6\n{body}\n## Pass 6 · 2026-11-17 · on draft v1.5\n{body}")
    assert newest_pass(tmp_path)[:2] == (7, "1.6")
