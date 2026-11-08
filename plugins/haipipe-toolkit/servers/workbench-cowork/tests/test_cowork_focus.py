"""A cowork page's own parts on the shared work page (cowork_focus, b13 plan of 261106): Findings' People, Messages
and Next move; Status by who has the move (a Block), a Job's move, timeline and steps, a Task's rounds; Delivery as the
messages sent. A small Block of placeholders, then the theme's prototype Block in the blueprints."""
import re
from pathlib import Path

import pytest

from live import cowork_focus as CF
from live import focus_page as F


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def face(nn, title, state, waiting, since, nxt=""):
    return (f"# {nn} · {title}\njob-kind: cowork-job\nstate: {state}\nwaiting-on: {waiting}\nsince: {since}\n"
            + (f"next: {nxt}\n" if nxt else "") + "\n## Content\n\nWhat we asked for.\n")


@pytest.fixture
def demo(tmp_path):
    """A Project with one cowork Block: people by role, a Job waiting on them, one waiting on us (a draft email and a
    Task written in rounds), a done Job, one send."""
    root = tmp_path
    write(root / "Project" / "project.md", "# Project\n")
    block = root / "Project" / "cowork" / "b01_demo"
    write(block / "board.md", "# b01 · Demo\nboard-kind: cowork-block\nstate: 🟡 ACTIVE\nspine: one request.\n")
    write(block / "j00_people/j00_people.md",
          "# j00 · People\njob-kind: cowork-job\nstate: 📇 REFERENCE\n\n| Who | Side | Owns |\n|---|---|---|\n"
          "| ROLE_A | Office A | the extract |\n| ROLE_B | Our team | every send |\n| (to add) | … | … |\n")
    a = block / "j01_ask"
    write(a / "j01_ask.md", face("j01", "Ask OFFICE_A", "🟡 ACTIVE", "ROLE_A", "2026-10-01", "chase them"))
    write(a / "Timeline.md", "- 2026-09-25 agreed the fields\n- 2026-09-28 asked\n- 2026-10-01 they replied\n")
    write(a / "CHECKLIST.md", "- [x] 1. Ask\n- [ ] 2. Get the date\n")
    write(a / "emails/2026-10-01-reply.md", "# Reply from ROLE_A\n")
    write(a / "meetings/2026-09-30-call.md", "# Call with ROLE_A\n")
    b = block / "j02_amend"
    write(b / "j02_amend.md", face("j02", "Amendment", "🟡 ACTIVE", "us", "2026-10-05", "send the draft"))
    write(b / "emails/2026-10-06-amendment-draft.md", "# Amendment\nstatus: draft\n")
    t = b / "t01_plan"
    write(t / "t01_plan.md", "# t01 · Plan\nwaiting-on: us\nsince: 2026-10-05\nnext: write v3\n")
    run = t / "runs" / "run-write-plan"
    write(run / "run.yaml", "run: run-write-plan\nkind: soft\nstatus: waiting\n")
    write(run / "result/plan_v1.md", "# v1\n")
    write(run / "passes/p01-1001/pass.md", "# v1 to ROLE_A\n\n## Summary\n\nFour sections.\n\n## Changed\n\n- `result/plan_v1.md`\n")
    write(run / "passes/p02-1004/pass.md", "# v2 answers the comments\n\n## Summary\n\nAll answered.\n\n## Changed\n\n<nothing>\n")
    write(block / "j03_done/j03_done.md", face("j03", "Kickoff", "✅ DONE", "nobody", "2026-09-20"))
    send = block / "delivery" / "j01_ask" / "2026-09-28-ask"
    write(send / "2026-09-28-ask.md", "# Ask OFFICE_A\nstatus: sent\nTo: ROLE_A\nSubject: The ask\nAttach: fields.csv\n---\nHello\n")
    write(send / "fields.csv", "field\nfield_a\n")
    return root, block


def titles(rows):
    return [r[0] for r in rows]


def test_the_block_findings_add_people_messages_and_the_next_move(demo):
    root, block = demo
    got = {r[0]: r for r in CF.parts(block, root, "Block")}
    assert list(got) == ["👥 People", "✉️ Messages", "⏳ Next move"]
    people = got["👥 People"][2]
    assert "ROLE_A" in people and "ROLE_B" in people and "(to add)" not in people   # a row still to fill is left out
    assert "has the move" in people and got["👥 People"][1] == "1 has the move"        # ROLE_A has j01's move
    title, word, html, waits = got["✉️ Messages"]
    assert word == "1 draft waits for you" and waits.startswith("🙋 a draft waits for you to send")
    assert all(t in html for t in (">Emails<", ">Meetings<", ">Drafts<", "Reply from ROLE_A", "Call with ROLE_A"))
    title, word, html, waits = got["⏳ Next move"]
    assert word == "1 waits for you · 1 on them"
    assert waits == ""                                     # its draft already waits under Messages: once per page
    assert html.index("Amendment") < html.index("Ask OFFICE_A")                        # ours first
    assert "Kickoff" not in html and "People" not in html                              # done and reference Jobs: no move


def test_a_job_findings_name_only_its_people_and_have_no_next_move(demo):
    root, block = demo
    got = {r[0]: r for r in CF.parts(block / "j01_ask", root, "Job")}
    assert list(got) == ["👥 People", "✉️ Messages"]                                 # its move is its Status
    assert "ROLE_A" in got["👥 People"][2] and "ROLE_B" not in got["👥 People"][2]
    assert got["✉️ Messages"][3] == ""                                                 # no draft here
    assert CF.parts(block / "j03_done", root, "Job") == []                             # nothing in it: no part


def test_the_block_status_groups_its_jobs_by_who_has_the_move(demo):
    root, block = demo
    got = CF.status(block, root, "Block")
    assert titles(got) == ["🙋 Waiting on us", "⏳ Waiting on them", "✅ Done"]           # a reference Job is no line
    assert got[0][1] == "1 waits for you" and got[0][3] == "🙋 Amendment: send the draft"
    assert got[1][1].startswith("longest ") and "Ask OFFICE_A" in got[1][2] and "agreed the fields" in got[1][2]
    assert "they replied" not in got[1][2] and "Reply from ROLE_A" in got[1][2]     # a note twin of an email goes
    assert ">note<" in got[1][2] and ">entry<" not in got[1][2]
    assert got[2][1] == "done" and "Kickoff" in got[2][2]


def test_a_job_status_is_its_move_its_timeline_and_its_steps(demo):
    root, block = demo
    got = CF.status(block / "j01_ask", root, "Job")
    assert titles(got) == ["⏳ Waiting on them", "🗓️ Timeline", "☑️ Steps"]
    assert got[0][1].startswith("ROLE_A · ") and "chase them" in got[0][2]
    timeline = got[1][2]
    assert got[1][1] == "newest 2026-10-01"
    assert [timeline.index(x) for x in ("2026-10-01", "2026-09-30", "2026-09-28")] == sorted(
        timeline.index(x) for x in ("2026-10-01", "2026-09-30", "2026-09-28"))                # newest first, every kind
    assert "Ask OFFICE_A" in timeline                                                         # its send, dated
    assert got[2][1] == "1 of 2 done"
    ours = CF.status(block / "j02_amend", root, "Job")
    assert ours[0][0] == "🙋 Waiting on us" and ours[0][3] == "🙋 the next move is ours"     # its sentence: the lead
    assert ">State<" not in ours[0][2]
    assert titles(CF.status(block / "j03_done", root, "Job"))[:1] != ["✅ Done"]          # the lead says done
    assert "🧱 Tasks" in titles(ours)                                                       # its Task, the shared row


def test_a_task_written_in_rounds_shows_each_round(demo):
    root, block = demo
    got = CF.status(block / "j02_amend" / "t01_plan", root, "Task")
    assert titles(got)[0] == "📌 v2 answers the comments" and got[0][1] == "waits for you"   # the newest round first
    assert titles(got)[1] == "📝 Rounds" and got[1][1] == "newest 10-04"
    rounds = got[1][2]
    assert "cw-chain" in rounds and rounds.index("v1 to ROLE_A") < rounds.index(">write v3<")   # the chain, v1 to v3
    tabs = rounds[rounds.index("pb-list"):]
    assert tabs.index("v2 answers the comments") < tabs.index("v1 to ROLE_A")                 # the tabs newest first
    plain = block / "j01_ask" / "t01_note"
    write(plain / "t01_note.md", "# t01 · Note\n")
    assert CF.status(plain, root, "Task") == []                                              # no rounds: the shared bars


def test_delivery_is_the_messages_sent(demo):
    root, block = demo
    tabs = CF.delivery_tabs(block, root, "Block")
    assert [t[:2] for t in tabs] == [("Ask OFFICE_A", "sent")]
    assert "fields.csv" in tabs[0][2] and "The ask" in tabs[0][2] and "j01_ask" in tabs[0][2]
    assert CF.delivery_tabs(block / "j03_done", root, "Job") == [
        ("Messages", "nothing yet", '<p class=mut>Nothing sent from here yet.</p>')]


def test_the_shared_page_finds_these_parts(demo):
    """focus_page.page_module finds live.cowork_focus for a cowork page: its parts, its Status, its Delivery tabs."""
    root, block = demo
    assert titles(F.theme_parts("cowork", block, root, "Block")) == ["👥 People", "✉️ Messages", "⏳ Next move"]
    assert titles(F.theme_status("cowork", block / "j01_ask", root, "Job"))[0] == "⏳ Waiting on them"
    findings = F.findings_board([], block, root, "", F.theme_parts("cowork", block, root, "Block"))
    assert "⏳ Next move" in findings and "📦 Delivery" in findings and "Ask OFFICE_A" in findings
    assert "Traceback" not in F.status_now_html(block, root, "Block", [])


EXAMPLE = Path(__file__).resolve().parents[5] / "blueprints" / "Project-Ladder" / "cowork" / "b01_example_data_request"


@pytest.mark.skipif(not EXAMPLE.is_dir(), reason="the prototype Block is not in this checkout")
def test_the_prototype_block_shows_every_cowork_part():
    """The theme's placeholder Block (made by its studio/_build/make_example.py): each part has something in it."""
    root = EXAMPLE.parents[3]                          # the Tools root
    assert titles(CF.parts(EXAMPLE, root, "Block")) == ["👥 People", "✉️ Messages", "⏳ Next move"]
    assert titles(CF.status(EXAMPLE, root, "Block")) == ["🙋 Waiting on us", "⏳ Waiting on them", "✅ Done"]
    task = EXAMPLE / "j02_review_board_amendment" / "t01_data_use_plan"
    assert [x[:1] for x in titles(CF.status(task, root, "Task"))[:2]] == ["📌", "📝"]
    assert len(CF.delivery_tabs(EXAMPLE, root, "Block")) == 3
    assert titles(CF.parts(EXAMPLE / "j03_kickoff_meeting", root, "Job"))[0] == "📌 Headlines"
    for path in EXAMPLE.rglob("*"):                     # public placeholders: no machine path, no address
        if path.is_file() and path.suffix in (".md", ".yaml", ".csv", ".txt", ".html", ".py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            assert not re.search(r"/(Users|home)/\w", text) and not re.search(r"\w@\w+\.\w", text), path


def test_a_job_with_no_tasks_maps_what_happened_who_has_the_move_and_what_is_left(demo):
    """focus_page.parts_mindmap asks map_branches when its own map is empty (a cowork Job has no Tasks, 261108)."""
    root, block = demo
    got = dict(CF.map_branches(block / "j01_ask", root, "Job"))
    assert list(got) == ["🗓️ What happened", "⏳ Who has the move", "➡️ Next", "☐ Steps still open"]
    assert got["🗓️ What happened"][0].startswith("2026-10-01 · ") and any("(meeting)" in x for x in got["🗓️ What happened"])
    assert all("<" not in x for x in got["🗓️ What happened"])                       # words, no markup
    assert got["⏳ Who has the move"][0].startswith("ROLE_A · since 2026-10-01")
    assert got["➡️ Next"] == ["chase them"] and got["☐ Steps still open"] == ["Get the date"]
    assert list(dict(CF.map_branches(block / "j03_done", root, "Job"))) == ["✅ Done"]
    assert CF.map_branches(block / "j00_people", root, "Job") == [("👥 Who to ask", ["ROLE_A · Office A", "ROLE_B · Our team"])]
    assert CF.map_branches(block, root, "Block") == []
    page = F.parts_mindmap(block / "j01_ask", root)
    assert "Nothing to map yet" not in page and "Who has the move" in page and "chase them" in page


def test_a_cowork_status_reads_in_its_own_words(demo):
    """CAPTIONS: the shared "Where its Tasks stand" reads wrong on a Job with no Tasks."""
    root, block = demo
    assert CF.CAPTIONS[("Job", "standing")] == "Who has the move, since when, and what happened so far."
    page = F.render(F.frame.themes()["cowork"], root, block / "j01_ask", "report", "standing")
    assert "Who has the move, since when, and what happened so far." in page and "Where its Tasks stand" not in page
