"""caption_check: words of a caption's title and legend, the newest Run, the limits."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import caption_check as C  # noqa: E402


def fl(title, legend, env="figure"):
    return f"\\begin{{{env}}}\n\\caption{{\\textbf{{{title}}} {legend}}}\n\\label{{x}}\n\\end{{{env}}}\n"


def test_counts_title_and_legend_apart():
    assert C.caption_words(fl("Data, Not Size", "Circles, each \\emph{one} model; lines, medians.")) == (3, 6, False)


def test_a_table_is_known_and_no_caption_is_none():
    assert C.caption_words(fl("T", "note", "table"))[2] is True
    assert C.caption_words("\\begin{figure}\\end{figure}") is None


def _run(job, task, run, legend_words):
    r = job / task / "runs" / run / "result"
    r.mkdir(parents=True)
    (r / "float.tex").write_text(fl("A Title", " ".join(["word"] * legend_words)))


def test_reads_the_newest_run_and_flags_a_long_legend(tmp_path):
    _run(tmp_path, "t01_a", "r01_old", 200)
    _run(tmp_path, "t01_a", "r02_new", 40)
    _run(tmp_path, "t02_b", "r01_long", 76)
    rows = C.check(tmp_path)
    assert [(r[0], r[1], r[3], r[-1]) for r in rows] == [("t01_a", "r02_new", 40, False), ("t02_b", "r01_long", 76, True)]


def test_a_table_legend_may_run_longer(tmp_path):
    r = tmp_path / "t51_t" / "runs" / "r01" / "result"
    r.mkdir(parents=True)
    (r / "float.tex").write_text(fl("T", " ".join(["word"] * 100), "table"))
    assert C.check(tmp_path)[0][-1] is False


def test_message_sentences():
    assert C.message_sentences("# M\n\n## Question\nWhy?\n") == 0
    assert C.message_sentences("## Message\nOne thing. Another thing.\n\n## Data\nA. B. C. D.\n") == 2
    assert C.message_sentences("## Message\nNo full stop\n") == 1


def test_messages_name_a_display_with_none_or_too_many(tmp_path):
    for task, text in (("t01_a", "## Message\nIt holds.\n"), ("t02_b", "## Data\nx\n"), ("t03_c", "## Message\nA. B. C. D.\n")):
        _run(tmp_path, task, "r01_x", 10)
        (tmp_path / task / "runs" / "r01_x" / "result" / "method.md").write_text(text)
    got = {r[0]: r[-1] for r in C.messages(tmp_path)}
    assert got["t01_a"] == "" and got["t02_b"] == "no ## Message" and "at most 3" in got["t03_c"]


def test_the_venue_limit_wins(tmp_path):
    job = tmp_path / "j01_evidence_display"
    _run(job, "t01_a", "r01_x", 90)
    assert C.check(job)[0][-1] is True
    call = tmp_path / "venues" / "v" / "call.md"
    call.parent.mkdir(parents=True)
    call.write_text("| caption | our limit at most 100 words | x |\n")
    assert C.check(job)[0][-1] is False
