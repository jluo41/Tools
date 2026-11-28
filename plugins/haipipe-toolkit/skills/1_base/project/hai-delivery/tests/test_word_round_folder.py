"""The co-author round folder: open-round, settle and submit (Pp-AgreeableRx-Discrention, JL 261122)."""
import re
import sys
import time
import zipfile
from pathlib import Path

import docx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import word_round_folder as wrf  # noqa: E402
import word_marks  # noqa: E402

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NAME = "Paper-X"


def make(path, paras):
    d = docx.Document()
    for t in paras:
        d.add_paragraph(t)
    d.save(path)
    return path


def add_ins(path, words, author="Coauthor"):
    """A tracked insertion of `words` at the end of the first paragraph."""
    with zipfile.ZipFile(path) as z:
        items = {i.filename: z.read(i.filename) for i in z.infolist()}
    s = items["word/document.xml"].decode()
    ins = (f'<w:ins w:id="91" w:author="{author}" w:date="2026-11-22T00:00:00Z"><w:r><w:t xml:space="preserve">'
           f' {words}</w:t></w:r></w:ins>')
    s = s.replace("</w:p>", ins + "</w:p>", 1)
    items["word/document.xml"] = s.encode()
    with zipfile.ZipFile(path, "w") as z:
        for k, v in items.items():
            z.writestr(k, v)


@pytest.fixture
def rounds(tmp_path):
    r1 = tmp_path / "Round1-v1101"
    (r1).mkdir()
    make(r1 / f"1-{NAME}-v1101-manuscript.docx", ["Alpha sentence.", "Beta sentence."])
    make(r1 / f"2-{NAME}-v1101-cover-letter.docx", ["Dear editor."])
    return tmp_path


def test_marker_name_and_listing(tmp_path):
    (tmp_path / "Round1-v1101" / "clean").mkdir(parents=True)
    f = tmp_path / "Round1-v1101" / "clean" / "a.docx"
    f.write_bytes(b"x")
    (f.parent / "last-update-2020-01-01 00.00.txt").write_text("old")
    m = wrf.marker(f.parent)
    assert re.fullmatch(r"last-update-\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.txt", m.name) and ":" not in m.name
    assert [p.name for p in f.parent.glob("last-update-*")] == [m.name]
    assert "a.docx" in m.read_text() and m.read_text().startswith("Round1-v1101/clean: last updated")


def test_open_round_copies_previous_and_turns_tracking_on(rounds):
    new = wrf.open_round(rounds, "1122", {})
    assert new.name == "Round2-v1122"
    assert sorted(p.name for p in (new / "previous").glob("*.docx")) == [
        f"1-{NAME}-v1101-manuscript.docx", f"2-{NAME}-v1101-cover-letter.docx"]
    tops = sorted(p.name for p in new.glob("*"))
    assert f"1-{NAME}-v1122-manuscript.docx" in tops and not any(t.endswith(".pdf") for t in tops)
    assert all(wrf.tracking(p) for p in new.glob("*.docx"))
    assert list((new / "previous").glob("last-update-*.txt"))


def test_track_on_is_where_word_reads_it(tmp_path):
    f = make(tmp_path / "a.docx", ["x"])
    assert wrf.track_on(f) and not wrf.track_on(f)
    s = zipfile.ZipFile(f).read("word/settings.xml").decode()
    assert s.count("<w:trackRevisions/>") == 1
    assert s.index("<w:trackRevisions/>") < s.index("<w:defaultTabStop")


def test_settle_refuses_while_word_holds_the_lock(rounds):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    (r / ("~$" + top.name[2:])).write_text("lock")
    with pytest.raises(SystemExit, match="lock file"):
        wrf.settle_one(r, top, how="keep")
    assert not (r / "track").exists()


def test_settle_with_no_answer_asks_and_leaves_the_file(rounds):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    add_ins(top, "Gamma added.")
    before = top.read_bytes()
    lines = wrf.settle_one(r, top)
    assert any("How should the working file" in l for l in lines)
    assert top.read_bytes() == before
    copies = list((r / "track").glob("1-*-tracked-*.docx"))
    assert len(copies) == 1 and copies[0].read_bytes() == before
    assert any("ins [Coauthor]" in l and "Gamma added." in l for l in lines)


def test_keep_leaves_the_file_and_the_next_settle_starts_from_track(rounds):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    add_ins(top, "Gamma added.")
    before = top.read_bytes()
    first = wrf.settle_one(r, top, how="keep")
    assert top.read_bytes() == before and any("kept as it is" in l for l in first)
    time.sleep(1.1)
    assert wrf.last_seen(r, 1).parent.name == "track"
    second = wrf.settle_one(r, top, how="keep")
    assert any("no changes since then" in l for l in second)
    assert any(l.startswith("since: track/") for l in second)


def test_accept_replaces_with_clean_only_when_the_words_are_in_the_drafts(rounds, tmp_path):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    add_ins(top, "Gamma added.")
    stale = make(tmp_path / "stale.docx", ["Alpha sentence.", "Beta sentence."])
    refused = wrf.settle_one(r, top, clean=[stale], how="accept")
    assert any(l.startswith("refused") for l in refused) and top.is_file()
    time.sleep(1.1)
    synced = make(tmp_path / "synced.docx", ["Alpha sentence. Gamma added.", "Beta sentence."])
    done = wrf.settle_one(r, top, clean=[synced], draft=synced, how="accept")
    assert any("is the clean Word now" in l and "✅" in l for l in done)
    assert wrf.tracking(top) and not word_marks.listing(top)
    # the refused accept changed nothing, so the second settle's marked copy is the same file, not a second one
    copies = list((r / "track").glob("1-*-tracked-*.docx"))
    assert len(copies) == 1 and "Gamma added." in " ".join(wrf.accepted_text(copies[0]))


def test_each_lists_then_accepts_the_picked(rounds):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    add_ins(top, "Gamma added.")
    listed = wrf.settle_one(r, top, how="each")
    assert any(re.match(r"\s+1\. ins \[Coauthor\] .*Gamma", l) for l in listed)
    time.sleep(1.1)
    wrf.settle_one(r, top, how="each", pick={1})
    assert not word_marks.listing(top) and "Gamma added." in " ".join(wrf.accepted_text(top))


def test_settle_never_writes_previous_or_submission(rounds):
    r = wrf.open_round(rounds, "1122", {})
    with pytest.raises(SystemExit, match="never writes"):
        wrf.guard(r / "previous" / "x.docx", r)
    with pytest.raises(SystemExit, match="never writes"):
        wrf.guard(r / "submission" / "x.pdf", r)


def test_submit_numbers_by_slot_follows_the_build_and_freezes_on_submitted(rounds, tmp_path):
    r = wrf.open_round(rounds, "1122", {})
    paper = tmp_path / "delivery"
    paper.mkdir()
    for f in ("m.pdf", "c.pdf", "t.pdf"):
        (paper / f).write_bytes(b"%PDF")
    (paper / "paper-build.toml").write_text(
        '[paper]\nid = "Paper-X"\n[[portal.upload]]\nslot = "Manuscript (PDF)"\nfrom = "m.pdf"\n'
        '[[portal.upload]]\nslot = "Cover letter"\nfrom = "c.pdf"\n'
        '[[portal.upload]]\nslot = "Research Transparency Commitment"\nfrom = "t.pdf"\n')
    sub = wrf.submit(r, paper / "paper-build.toml", "1122")
    assert sorted(p.name for p in sub.glob("*.pdf")) == [
        f"1-{NAME}-v1122-manuscript.pdf", f"2-{NAME}-v1122-cover-letter.pdf", f"3-{NAME}-v1122-research-transparency.pdf"]
    (paper / "m.pdf").write_bytes(b"%PDF new")              # a later build: submission/ follows it until Submit
    wrf.submit(r, paper / "paper-build.toml", "1122")
    assert (sub / f"1-{NAME}-v1122-manuscript.pdf").read_bytes() == b"%PDF new"
    wrf.submitted(r)                                          # the person pressed Submit
    with pytest.raises(SystemExit, match="frozen"):
        wrf.submit(r, paper / "paper-build.toml", "1122")


def test_settle_refreshes_every_rebuilt_clean_file_and_submission(rounds, tmp_path):
    r = wrf.open_round(rounds, "1122", {})
    files = wrf.working(r)
    paper = tmp_path / "delivery"; paper.mkdir()
    built = {n: make(paper / f"b{n}.docx", [f"rebuilt {n}"]) for n in files}
    for f in ("m.pdf", "c.pdf"):
        (paper / f).write_bytes(b"%PDF")
    (paper / "paper-build.toml").write_text('[paper]\nid = "Paper-X"\n[[portal.upload]]\nslot = "Manuscript"\n'
                                            'from = "m.pdf"\n[[portal.upload]]\nslot = "Cover letter"\nfrom = "c.pdf"\n')
    args = ["settle", str(r), "2", "--working", "keep", "--config", str(paper / "paper-build.toml")]
    for n, b in built.items():
        args += ["--clean", f"{n}={b}"]
    wrf.main(args)
    cleaned = sorted(p.name.split("-", 1)[0] for p in (r / "clean").glob("*.docx"))
    assert cleaned == sorted(str(n) for n in files)           # file 1 and 3 too, not only the settled 2
    assert len(list((r / "submission").glob("*.pdf"))) == 2 and not wrf.is_frozen(r)


def test_newest_marked_copy_is_by_its_name_not_its_file_time(tmp_path):
    r = tmp_path / "Round4-v1121"
    (r / "track").mkdir(parents=True)
    old = make(r / "track" / f"1-{NAME}-v1114-manuscript-tracked-2026-11-22 02.12.docx", ["a"])
    new = make(r / "track" / f"1-{NAME}-v1121-manuscript-tracked-2026-11-22 20.51.docx", ["b"])
    import os
    os.utime(new, (1, 1))   # copy2 kept an older file time
    assert wrf.last_seen(r, 1) == new and old.is_file()


def test_refresh_makes_an_unedited_working_file_the_clean_build(rounds, tmp_path):
    """Pp-AgreeableRx 261122: the portal file kept old values after a portal rebuild; refresh is one command."""
    r = wrf.open_round(rounds, "1122", {})
    paper = tmp_path / "delivery"; paper.mkdir()
    new = make(paper / "portal.docx", ["Alpha sentence.", "Beta sentence, new values."])
    (paper / "m.pdf").write_bytes(b"%PDF")
    (paper / "paper-build.toml").write_text('[paper]\nid = "Paper-X"\n[[portal.upload]]\nslot = "Manuscript"\nfrom = "m.pdf"\n')
    wrf.main(["refresh", str(r), "1", "--clean", f"1={new}", "--version", "1123", "--config", str(paper / "paper-build.toml")])
    top = wrf.working(r)[1]
    assert top.name == f"1-{NAME}-v1123-manuscript.docx" and wrf.tracking(top)
    assert "new values" in " ".join(wrf.accepted_text(top))
    assert list((r / "track").glob("1-*-v1122-manuscript-tracked-*.docx"))      # the old copy, saved first
    for sub in ("track", "clean", "submission"):
        assert len(list((r / sub).glob("last-update-*.txt"))) == 1             # markers by the tool, never by hand
    # settle's baseline is the clean Word that was placed: the replacement is not listed as untracked changes
    assert any("no changes since then" in l for l in wrf.settle_one(r, top, dry=True))


def test_refresh_refuses_a_working_file_with_marks(rounds, tmp_path):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    add_ins(top, "Gamma added.")
    lines = wrf.refresh_one(r, top, clean=[make(tmp_path / "c.docx", ["x"])])
    assert any(l.startswith("refused") for l in lines) and "Gamma added." in " ".join(wrf.accepted_text(top))


def test_after_accept_the_next_settle_starts_from_the_placed_clean_word(rounds, tmp_path):
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    synced = make(tmp_path / "s.docx", ["Alpha sentence, rebuilt.", "Beta sentence."])
    wrf.settle_one(r, top, clean=[synced], how="accept")
    top = wrf.working(r)[1]
    assert any("no changes since then" in l for l in wrf.settle_one(r, top, dry=True))


def test_refresh_records_a_clean_word_placed_by_hand(rounds, tmp_path):
    """Round4-v1121: the clean portal Word was copied over the working file by hand; settle listed it as untracked."""
    r = wrf.open_round(rounds, "1122", {})
    top = wrf.working(r)[1]
    wrf.settle_one(r, top, how="keep")                                    # a marked copy of the old file in track/
    built = make(tmp_path / "b.docx", ["Alpha sentence, new value.", "Beta sentence."])
    wrf.place_clean(r, top, [built])
    import shutil; shutil.copy2(r / "clean" / f"{top.stem}-clean.docx", top)             # the hand copy
    assert any("untracked" in l for l in wrf.settle_one(r, top, dry=True))
    assert any("settle starts from it now" in l for l in wrf.refresh_one(r, top))
    after = wrf.settle_one(r, top, dry=True)
    assert any("no changes since then" in l for l in after)
    assert any(l.startswith("marked copy: none needed") for l in after) and not any(".placed" in l for l in after)


def test_push_never_writes_into_a_round_folder(tmp_path):
    """Pp-AgreeableRx 261122: push wrote a flat Round3-v1122/ (no numbers, a PDF at the top, no subfolders)."""
    import word_round
    (tmp_path / "env.sh").write_text("")                              # the SPACE a lane sits in
    lane = tmp_path / "word"; lane.mkdir()
    make(lane / f"{NAME}-v1.docx", ["Alpha."])
    flat = tmp_path / "Round3-v1122"; flat.mkdir()
    r = word_round.Round(lane, NAME, flat / f"{NAME}.docx")
    with pytest.raises(SystemExit, match="refused: Round3-v1122/ is a round folder"):
        r.push(1, force=True)                                           # --force never opens a round to push
    assert not list(flat.iterdir())


def test_round_status_flags_a_flat_round(tmp_path, capsys):
    flat = tmp_path / "Round3-v1122"; flat.mkdir()
    make(flat / f"{NAME}.docx", ["Alpha."])
    wrf.status(flat)
    assert "❗ old layout" in capsys.readouterr().out


def test_adopt_round_moves_a_flat_folder_into_the_layout(tmp_path):
    """ScalingGlucose-Board-v2 261122: GlucoseScalingLaw/v1118 was flat and open-round could not make a first round."""
    import check_round
    from round_adopt import adopt_round
    flat = tmp_path / "v1118"; flat.mkdir()
    make(flat / "P-draft.docx", ["Alpha."]); (flat / "P-draft.pdf").write_bytes(b"%PDF")
    make(flat / "P-draft-tracked.docx", ["Alpha, marked."]); (flat / "notes.txt").write_text("kept")
    r, _ = adopt_round(flat, NAME, "1118", {1: ("P-draft.docx", "manuscript")})
    assert r.name == "Round1-v1118" and not flat.exists()
    assert wrf.tracking(r / f"1-{NAME}-v1118-manuscript.docx")
    assert (r / "clean" / f"1-{NAME}-v1118-manuscript-clean.pdf").is_file() and (r / "clean" / f"1-{NAME}-v1118-manuscript-clean.docx").is_file()
    assert (r / "track" / "P-draft-tracked.docx").is_file() and (r / "previous" / "notes.txt").read_text() == "kept"
    assert all(ok for ok, _ in check_round.check(r))


def test_check_round_flags_a_flat_round(tmp_path):
    import check_round
    flat = tmp_path / "Round3-v1122"; flat.mkdir()
    make(flat / f"{NAME}.docx", ["Alpha."]); (flat / f"{NAME}.pdf").write_bytes(b"%PDF")
    bad = [t for ok, t in check_round.check(flat) if not ok]
    assert bad[0].startswith("1 top") and f"{NAME}.pdf" in bad[0] and bad[1].startswith("2 subfolders: missing")
