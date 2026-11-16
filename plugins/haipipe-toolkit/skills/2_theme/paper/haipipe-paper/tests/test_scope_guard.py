"""scope_guard.py on a tiny made-up paper Board: the fixed rules, § 8.6's "never" phrases, the Section's must-refuse
cell and the venue's Abstract cap, each hit keyed by the sentence's full address."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scope_guard as sg  # noqa: E402

FACE = """# j11_writing_v0101_x · version 1

venue: Example Journal

## Narrative

#### 8.3 · Per-section narrative

| Section | reader question | entry | ordered moves | must refuse | displays | exit |
|---|---|---|---|---|---|---|
| t02_results | What changed? | Has the gap. | a → b | "first", "no effect" without an interval | Figure 1 | has the numbers |

#### 8.6 · What every Section receives unchanged
Say "to our knowledge the most readings", never "the largest dataset". The word is "fades", never "vanishes".

#### 8.7 · What a Section row may add
Nothing.
"""
CALL = """# Example Journal

| what | limit | counts |
|---|---|---|
| abstract | up to 12 words, unreferenced | one paragraph |
| main limit | 2 (figures and tables together) | |
"""


def write(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def draft(lines: dict) -> str:
    out = ["# draft", "", "## 1 · Structure", "", "## 3 · Draft · Reading and Revise", ""]
    for pid, sents in lines.items():
        out.append(f"### {pid} · a paragraph")
        out += [f"- B{i} · s{n} · {t}" for i, (n, t) in enumerate(sents, 1)]
        out.append("")
    return "\n".join(out) + "\n## 4 · Notes\n"


def board(tmp: Path, task: str, sents: dict, version: str = "v1.2") -> Path:
    b = tmp / "Paper-X"
    write(b / "board.md", "# Paper-X\n")
    write(b / "venues" / "example-journal" / "call.md", CALL)
    job = b / "j11_writing_v0101_x"
    write(job / f"{job.name}.md", FACE)
    t = job / task
    write(t / f"{task}.md", f"# {task}\n")
    write(t / "draft" / f"{task}-draft-v1.1.md", draft({"C1.P1": [(1, "An older draft; with a semicolon.")]}))
    write(t / "draft" / f"{task}-draft-{version}.md", draft(sents))
    return t


def test_clean_section_passes(tmp_path):
    t = board(tmp_path, "t02_results", {"C1.P1": [(1, "Error fell by 8.2% (patient interval -9.6 to -6.9)."),
                                                  (2, "The gain fades with the horizon.")]})
    rep = sg.guard(t)
    assert rep["version"] == "v1.2" and rep["sentences"] == 2
    assert rep["hits"] == [] and rep["failed"] == 0
    assert sg.main([str(t)]) == 0


def test_rules_hit_with_full_addresses(tmp_path):
    t = board(tmp_path, "t02_results", {
        "C1.P1": [(1, "Error fell; the gain held."), (2, "The gain vanishes at 2 hours \u2014 as expected.")],
        "C2.P2": [(3, "This is the first study of its kind."), (4, "Scale had no effect on the next day."),
                  (5, "At first the gain is large (a; b), as Figure 1 shows.")]})
    rep = sg.guard(t)
    got = {(h["where"], h["rule"], h["kind"]) for h in rep["hits"]}
    assert ("C1.P1.s1", "M-A13", "rule") in got                 # semicolon
    assert ("C1.P1.s2", "M-A18", "rule") in got                 # em-dash
    assert ("C1.P1.s2", "M-D08", "rule") in got                 # § 8.6: never "vanishes"
    assert ("C2.P2.s3", "M-A08", "refuse") in got               # must refuse "first"
    assert ("C2.P2.s4", "M-A08", "read") in got                 # conditional: for the reading agent
    assert not any(w == "C2.P2.s5" for w, _, _ in got)          # "At first" and a semicolon in a parenthesis
    assert rep["failed"] == 4
    assert sg.main([str(t)]) == 1


def test_never_phrases_and_refuse_cell_are_read(tmp_path):
    t = board(tmp_path, "t02_results", {"C1.P1": [(1, "Fine.")]})
    texts = sg.narrative_texts(t)
    assert [p for p, _ in sg.forbidden(texts)] == ["the largest dataset", "vanishes"]
    cell = sg.must_refuse(texts, "t02_results")
    assert [(p, c) for p, c, _ in sg.refuse_phrases(cell)] == [("first", False), ("no effect", True)]


def test_abstract_cap_and_display_count(tmp_path):
    long = "We trained many glucose models and found that scale helps in some tasks only."
    t = board(tmp_path, "t00_abstract", {"C1.P0": [(0, "A title that is not counted at all here")],
                                         "C1.P1": [(1, long), (2, "See Figure 1, Figure 2 and Figure 3.")]})
    rep = sg.guard(t)
    venue = [h["what"] for h in rep["hits"] if h["kind"] == "venue"]
    assert any(v.startswith("Abstract 22 words, the venue allows 12") for v in venue)
    assert any(v.startswith("3 main displays called, the venue allows 2") for v in venue)


def test_not_a_section(tmp_path):
    assert sg.main([str(tmp_path)]) == 2
