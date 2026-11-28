"""caption_check cross-references (hai-paper ref/must-check.md M-D12): a caption names only displays that exist."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import caption_check as C  # noqa: E402


def display(job: Path, name: str, label: str, caption: str, run: str = "r01_draw") -> None:
    task = job / name
    res = task / "runs" / run / "result"
    res.mkdir(parents=True)
    (task / f"{name}.md").write_text(f"# {name}\nlabel: {label}\nprinted: {run}\n", encoding="utf-8")
    (res / "float.tex").write_text(f"\\begin{{figure}}\n\\caption{{\\textbf{{T.}} {caption}}}\n\\end{{figure}}\n",
                                   encoding="utf-8")


def test_refs_reads_every_way_a_caption_names_a_display():
    got = C.refs("as in Figure 2 and Table 1; Extended~Data Fig. 3's corner; Figs. 4 to 6; Supplementary Table 9")
    assert got == ["Figure 2", "Table 1", "Extended Data Figure 3", "Figure 4", "Figure 5", "Figure 6"]


def test_a_caption_naming_a_display_the_numbering_lacks_is_reported(tmp_path):
    job = tmp_path / "j01_evidence_display"
    display(job, "t01_overview", "Figure 1 · Q00", "Points, models.")
    display(job, "t02_forecast", "Figure 2 · Q01", "As in Figure 1 and Extended Data Fig. 1.")
    display(job, "t54_edtable1", "Extended Data Table 1", "Values of Figure 2 and Table 1.")
    display(job, "t04_ed1", "Extended Data Figure 1 · Q04", "Each pair as in Figure 2.")
    assert set(C.numbering(job)) == {"Figure 1", "Figure 2", "Extended Data Table 1", "Extended Data Figure 1"}
    assert C.cross_refs(job) == [("t54_edtable1", "r01_draw", "Table 1")]
