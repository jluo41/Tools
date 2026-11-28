"""Health row `comments` (CONSTITUTION A01, JL 261118): a person's page comment with no reply after it is named, an AI
note is not, a reply clears it, and a closed or done comment is skipped."""
from pathlib import Path

from src.comment_health import unanswered

TEXT = """# t · comments

### Comment 1 · C1.P1.s1
State: open
- Note · 2026-11-18 16:52: very hard to read?

### Comment 2 · C1.P1.s2
State: open
- Note · 2026-11-16 02:35 · AI: should s2 say X?

### Comment 3 · C1.P1.s3
State: answered
- Note · 2026-11-18 10:00: rewrite it
- Reply · 2026-11-18 10:05: Done, it reads now ...

### Comment 4 · C1.P1.s4
State: answered
- Note · 2026-11-18 10:00: rewrite it
- Reply · 2026-11-18 10:05: Done.
- Note · 2026-11-18 11:00: still long

### Comment 5 · C1.P1.s5
State: closed
- Note · 2026-11-18 10:00: old

### Comment 6 · C1.P1.s6
State: done · 2026-11-14 02:28
- Note · 2026-11-14 01:00: Looks good, I accept it.
"""


def test_unanswered(tmp_path: Path):
    f = tmp_path / "t-comments.md"
    f.write_text(TEXT, encoding="utf-8")
    got = [(n, a) for n, a, _ in unanswered(f)]
    assert got == [("1", "C1.P1.s1"), ("4", "C1.P1.s4")]


def test_missing_file(tmp_path: Path):
    assert unanswered(tmp_path / "none.md") == []
