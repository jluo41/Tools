"""`build.py send <target>` on the ladder: the target may be the review Job on the Board (jNN_review_<kind>_v<MMDD>/)
whose face says `for:` this version; one for another version is refused. Placeholders only, in a temp folder."""
import pytest

from test_build_delivery import _ladder_paper


def _built(m):
    for configured in m.OUT.values():
        path = m.rel(configured)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"%PDF" if path.suffix == ".pdf" else b"artifact")
    (m.HERE / "display-register.md").write_text("# display register\n")


def _review_job(m, name, serves):
    job = m.ROOT / name
    job.mkdir()
    (job / f"{name}.md").write_text(f"# {name}\npage-type: comments\nfor: {serves}\n")
    return job


def test_send_freezes_into_the_review_job_of_this_version(tmp_path, monkeypatch):
    m = _ladder_paper(tmp_path, monkeypatch)
    _built(m)
    job = _review_job(m, "j31_review_coauthor_v1110", m.VERSION.name)
    m.freeze("sent", "j31")                                  # the short name finds it
    sent = job / "sent"
    assert (sent / "L.pdf").exists() and (sent / "L.docx").exists()
    assert (sent / "build-manifest.json").exists() and (sent / "display-register.md").exists()
    with pytest.raises(SystemExit, match="immutable"):
        m.freeze("sent", "j31_review_coauthor_v1110")        # the full name finds the same Job, now frozen


def test_send_refuses_a_review_job_of_another_version(tmp_path, monkeypatch):
    m = _ladder_paper(tmp_path, monkeypatch)
    _built(m)
    job = _review_job(m, "j32_review_internal_v1112", "j02_v2_other")
    with pytest.raises(SystemExit, match="another version"):
        m.freeze("sent", "j32")
    assert not (job / "sent").exists()
