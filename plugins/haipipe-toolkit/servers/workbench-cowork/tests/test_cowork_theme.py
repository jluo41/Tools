"""The cowork theme on the base frame (b13 Q01): a demo Block of placeholders, its Block and Job
levels in the six Spaces, emails and meetings as rows of a Job, and a greyed Task tab until a Job writes a
document in rounds."""
import json
from pathlib import Path

from live import frame
from live.cowork_theme import THEME


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def job_page(title, state, waiting, since, nxt):
    return (f"# {title}\njob-kind: cowork-job\nstate: {state}\nwaiting-on: {waiting}\nsince: {since}\n"
            f"next: {nxt}\n\nWhat we asked for.\n")


def demo(tmp_path) -> tuple[Path, Path]:
    """A Project with one cowork Block: people, a waiting Job with emails, a meeting and a checklist,
    a done Job, a Question citing the waiting Job, a drawing."""
    root = tmp_path
    block = root / "Project" / "cowork" / "b01_demo"
    write(block / "board.md", "# b01 · Demo\nboard-kind: cowork-block\nstate: 🟡 ACTIVE\nspine: one request.\n"
          "close: it is done.\n\n## Questions\n\n```yaml\nquestions:\n- id: Q01\n  title: Is it ready?\n"
          "  question: Is the request ready?\n  work:\n  - j01_request/Timeline.md\n"
          "  report: reports/q01_ready/q01_ready.md\n```\n\n## Related resources\n\n```yaml\nresources:\n"
          "- title: The form\n  url: https://example.test/form\n  questions: [Q01]\n```\n")
    write(block / "reports/q01_ready/q01_ready.md", "# Is it ready?\nanswers: Q01\nanswer-status: answered\n")
    write(block / "studio/s01-flow/s01-flow.excalidraw", "{}")
    write(block / "j00_people/j00_people.md", "# People\njob-kind: cowork-job\nstate: 📇 REFERENCE\n\nPERSON_001 · owner\n")
    job = block / "j01_request"
    write(job / "j01_request.md", job_page("Request to OFFICE_A", "🟡 ACTIVE", "PERSON_002", "2026-10-01", "send v2"))
    write(job / "Timeline.md", "- 2026-09-28 asked OFFICE_A\n- 2026-10-01 they replied\n")
    write(job / "CHECKLIST.md", "- [x] 1. Ask\n- [ ] 2. Send v2\n")
    write(job / "emails/2026-09-28-ask.md", "# Ask\n")
    write(job / "emails/2026-10-03-v2-draft.md", "# Version 2\nstatus: draft\n")
    write(job / "meetings/2026-10-02-call.md", "# Call\n")
    write(job / "materials/form.md", "# Form\n")
    write(block / "j02_done/j02_done.md", job_page("Done line", "✅ DONE", "nobody", "2026-09-01", "—"))
    return root, block


def data(root, folder, space="", sub=""):
    return json.loads(frame.frame_json(THEME, root, folder, sub))


def test_a_cowork_folder_reads_as_the_cowork_theme(tmp_path):
    root, block = demo(tmp_path)
    assert frame.theme_of(block / "j01_request", root) == "cowork"
    assert frame.themes()["cowork"].name == "cowork"


def test_the_block_fills_its_spaces_with_cowork_rows(tmp_path):
    root, block = demo(tmp_path)
    got = {s["name"]: s for s in data(root, block)["spaces"]}
    assert [s for s in got] == list(frame.SPACE_NAMES)
    assert got["Description"]["subspaces"] == ["Scope", "People", "Resources", "Related"]
    assert got["Work Details"]["subspaces"] == ["All", "open", "waiting", "done"]
    assert "Open a job" in got["Work Details"]["run_doing"] and "run-add-<jNN>" in got["Work Details"]["run_types"]
    views = frame.spaces_for(THEME, "Block", block, root, "waiting")
    assert "j01_request" in views["Work Details"].html and "j02_done" not in views["Work Details"].html
    assert "j00_people" not in views["Work Details"].html                 # a reference Job is not waiting
    done = frame.spaces_for(THEME, "Block", block, root, "done")["Work Details"].html
    assert "j02_done" in done and "j01_request" not in done
    report = frame.spaces_for(THEME, "Block", block, root)["Audience Report"].html
    assert "Q01 Is it ready?" in report and "j01_request/Timeline.md" in report and "answered" in report
    people = frame.spaces_for(THEME, "Block", block, root, "People")["Description"].html
    assert "PERSON_001" in people
    resources = frame.spaces_for(THEME, "Block", block, root, "Resources")["Description"].html
    assert "https://example.test/form" in resources and "materials/form.md" in resources


def test_a_job_shows_its_emails_and_meetings_as_rows_not_tasks(tmp_path):
    root, block = demo(tmp_path)
    job = block / "j01_request"
    got = {s["name"]: s for s in data(root, job)["spaces"]}
    assert data(root, job)["level"] == "Job"
    assert got["Work Details"]["subspaces"] == ["Timeline", "Checklist", "Emails", "Meetings"]
    assert "Draft an email" in got["Runs"]["run_doing"] and "run-email-<slug>" in got["Runs"]["run_types"]
    timeline = frame.spaces_for(THEME, "Job", job, root)["Work Details"].html
    order = [timeline.index(x) for x in ("2026-10-03", "2026-10-02", "2026-10-01", "2026-09-28")]
    assert order == sorted(order)                                         # newest first, all kinds together
    assert "draft ✎" in timeline and "1 checklist steps open" in timeline
    steps = frame.spaces_for(THEME, "Job", job, root, "Checklist")["Work Details"].html
    assert "☑" in steps and "☐" in steps and "Send v2" in steps
    head = frame.spaces_for(THEME, "Job", job, root)["Description"].html
    assert "PERSON_002" in head and "send v2" in head
    cites = frame.spaces_for(THEME, "Job", job, root)["Audience Report"].html
    assert "Q01 Is it ready?" in cites
    assert "Q01" not in frame.spaces_for(THEME, "Job", block / "j02_done", root)["Audience Report"].html


def test_the_task_tab_opens_only_for_a_document_written_in_rounds(tmp_path):
    root, block = demo(tmp_path)
    job = block / "j01_request"
    assert '<select disabled aria-label="Task">' in frame.render(THEME, root, job)   # greyed: no Task here
    write(job / "t01_protocol" / "t01_protocol.md", "# t01 · Protocol\n")
    page = frame.render(THEME, root, job)
    assert '<select disabled aria-label="Task">' not in page and "t01_protocol" in page
    assert frame.spaces_for(THEME, "Task", job / "t01_protocol", root)["Description"].html   # the base's own
