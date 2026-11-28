"""A co-author edited clean/'s Word, not the working file (AgreeableJama-Board 261123, Round2-v1120)."""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_round  # noqa: E402
import round_clean  # noqa: E402
import word_round_folder as wrf  # noqa: E402
from test_word_round_folder import NAME, add_ins, make  # noqa: E402


@pytest.fixture
def rnd(tmp_path):
    """Round1-v1101: working file 1 refreshed from the build, so top and clean/ hold the same words."""
    r = tmp_path / "Round1-v1101"
    r.mkdir()
    top = make(r / f"1-{NAME}-v1101-manuscript.docx", ["Alpha sentence.", "Beta sentence."])
    pdf = tmp_path / "b.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    wrf.refresh_one(r, top, clean=[make(tmp_path / "b.docx", ["Alpha sentence.", "Beta sentence."]), pdf])
    for sub in ("previous", "submission"):
        (r / sub).mkdir(exist_ok=True)
    return r


def test_clean_copies_never_carry_the_working_name(rnd):
    assert sorted(p.name for p in (rnd / "clean").glob("1-*")) == [
        f"1-{NAME}-v1101-manuscript-clean.docx", f"1-{NAME}-v1101-manuscript-clean.pdf"]
    assert wrf.working(rnd)[1].name == f"1-{NAME}-v1101-manuscript.docx"
    assert wrf.top_name(rnd / "clean" / f"1-{NAME}-v1101-manuscript-clean.docx") == f"1-{NAME}-v1101-manuscript.docx"


def test_the_check_flags_marks_in_clean_and_an_old_clean_name(rnd):
    assert dict((t.split()[0], ok) for ok, t in check_round.check(rnd))["7"]
    add_ins(rnd / "clean" / f"1-{NAME}-v1101-manuscript-clean.docx", "Gamma added.", author="Gordon")
    line = next(t for ok, t in check_round.check(rnd) if t.startswith("7") and not ok)
    assert "a co-author edited the clean copy" in line and "1 insertions" in line and "take-clean 1" in line
    shutil.copy2(rnd / "clean" / f"1-{NAME}-v1101-manuscript-clean.pdf", rnd / "clean" / f"1-{NAME}-v1101-manuscript.pdf")
    assert "rename:" in next(t for ok, t in check_round.check(rnd) if t.startswith("7"))


def test_take_clean_makes_their_marked_copy_the_working_file(rnd, tmp_path):
    clean = rnd / "clean" / f"1-{NAME}-v1101-manuscript-clean.docx"
    add_ins(clean, "Gamma added.", author="Gordon")
    with pytest.raises(SystemExit):
        round_clean.take_clean(rnd, 1)                                  # no build to refill clean/ with
    lines = round_clean.take_clean(rnd, 1, [make(tmp_path / "b2.docx", ["Alpha sentence.", "Beta sentence."])])
    top = wrf.working(rnd)[1]
    assert sum(wrf.marks(top)["ins"].values()) == 1 and wrf.tracking(top)
    assert not round_clean.edited(rnd) and clean.is_file()             # clean/ is the build again
    assert len(list((rnd / "track").glob("1-*-tracked-*.docx"))) == 2 and any("Gordon" in l for l in lines)
    listed = wrf.changes(top, wrf.last_seen(rnd, 1))                    # settle lists exactly their mark
    assert [(k, a) for k, a, _ in listed] == [("ins", "Gordon")]


def test_take_clean_stops_when_the_working_file_was_edited_too(rnd):
    add_ins(rnd / "clean" / f"1-{NAME}-v1101-manuscript-clean.docx", "Gamma added.", author="Gordon")
    add_ins(wrf.working(rnd)[1], "Delta added.", author="JL")
    lines = round_clean.take_clean(rnd, 1, [rnd / "nothing.docx"])
    assert lines[-1].startswith("refused: both files hold edits")


def test_previous_keeps_its_one_marker(tmp_path):
    prev = tmp_path / "Round2-v1120" / "previous"
    prev.mkdir(parents=True)
    wrf.marker(prev, "Where this round started.")
    with pytest.raises(SystemExit, match="never rewritten"):
        wrf.marker(prev)


def test_clean_names_moves_an_older_clean_folder(rnd):
    for p in (rnd / "clean").glob("1-*-clean.*"):
        p.rename(p.with_name(p.name.replace("-clean", "")))
    assert "rename:" in next(t for ok, t in check_round.check(rnd) if t.startswith("7"))
    assert round_clean.clean_names(rnd, dry=True)[-1] == "(dry run: nothing moved)"
    round_clean.clean_names(rnd)
    assert next(ok for ok, t in check_round.check(rnd) if t.startswith("7"))
    assert len(list((rnd / "clean").glob("last-update-*.txt"))) == 1


def test_adopt_round_into_a_paper_folder_keeps_the_paper_folder(tmp_path):
    """Paper-FairGlucose-preprint 261123: adopt-round renamed the new paper folder itself to Round1-v1123."""
    from round_adopt import adopt_round
    paper = tmp_path / "Paper-FairGlucose"; paper.mkdir()
    make(paper / "P.docx", ["Alpha."]); (paper / "P.pdf").write_bytes(b"%PDF")
    with pytest.raises(SystemExit, match="--into"):
        adopt_round(paper, NAME, "1123", {1: ("P.docx", "manuscript")})          # never renames a paper folder
    _, lines = adopt_round(paper, NAME, "1123", {1: ("P.docx", "manuscript")}, dry=True, into=paper)
    assert str(paper / "Round1-v1123") in lines[0] and (paper / "P.docx").is_file()
    r, _ = adopt_round(paper, NAME, "1123", {1: ("P.docx", "manuscript")}, into=paper)
    assert r == (paper / "Round1-v1123").resolve() and paper.is_dir()
    assert sorted(p.name for p in paper.iterdir()) == ["Round1-v1123"]
    assert all(ok for ok, _ in check_round.check(r))
    make(paper / "Q.docx", ["Beta."])                                           # round 2 beside round 1
    r2, _ = adopt_round(paper, NAME, "1201", {1: ("Q.docx", "manuscript")}, round_n=2, into=paper)
    assert sorted(p.name for p in paper.iterdir()) == ["Round1-v1123", "Round2-v1201"]
    assert not (r2 / "previous" / "Round1-v1123").exists()


def test_round_status_is_a_verb_of_the_folder_script(rnd, capsys):
    wrf.main(["round-status", str(rnd)])
    assert "clean/  2 files" in capsys.readouterr().out


def test_submit_reads_a_portal_glob_as_the_portal_does(rnd, tmp_path):
    """Paper-FairGlucose-preprint 261123: from = "npj/npjDM-X-*-source.zip" stopped submit with "not built"."""
    import os
    npj = tmp_path / "npj"; npj.mkdir()
    old, new = npj / "npjDM-X-261120-source.zip", npj / "npjDM-X-261123-source.zip"
    old.write_bytes(b"old"); new.write_bytes(b"new")
    os.utime(old, (1, 1))
    cfg = tmp_path / "paper-build.toml"
    cfg.write_text('[[portal.upload]]\nslot = "LaTeX source"\nkind = "source"\nfrom = "npj/npjDM-X-*-source.zip"\n')
    wrf.submit(rnd, cfg, "1123")
    got = sorted((rnd / "submission").glob("1-*"))
    assert [p.name for p in got] == [f"1-{NAME}-v1123-source.zip"] and got[0].read_bytes() == b"new"
    cfg.write_text(cfg.read_text() + "all = true\n")
    wrf.submit(rnd, cfg, "1123")
    assert [p.name for p in sorted((rnd / "submission").glob("1-*"))] == [
        f"1-{NAME}-v1123-source-1.zip", f"1-{NAME}-v1123-source-2.zip"]
