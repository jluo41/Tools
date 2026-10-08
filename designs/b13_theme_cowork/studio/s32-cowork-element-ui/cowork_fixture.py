"""A placeholder cowork Project for the s32 shoot (no real cowork Block is on disk in this SPACE, 261008).

    python cowork_fixture.py <dir>     writes <dir>/Project-CoworkDemo/cowork/b01_demo/

It is the cowork theme's test Block (servers/workbench-cowork/tests/test_cowork_theme.py, `demo`), with a
little more so every element has something to draw: a second waiting Job, soft Runs at the Block and the
Job, a delivery/ and a Page Task (`t01_protocol/`, a document written in rounds). Placeholders only.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT, BLOCK = "Project-CoworkDemo", "cowork/b01_demo"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def job_page(title, state, waiting, since, nxt, ticket=""):
    return (f"# {title}\njob-kind: cowork-job\nstate: {state}\nwaiting-on: {waiting}\nsince: {since}\n"
            f"next: {nxt}\n" + (f"ticket: {ticket}\n" if ticket else "") + "\nWhat we asked for, and why.\n")


def face(title, state, qid, status, answer):
    """A report Page Face: its header, Opening and Content (the Page reader refuses a bare .md)."""
    return (f"# {title}\nstate: {state}\nanswers: {qid}\nanswer-status: {status}\n\n## Opening\n\n{answer}\n\n"
            f"**Where this Page sits:** [{qid}](../../board.md).\n\n## Content\n\n### Answer\n\n{answer}\n")


def run_card(folder: Path, name: str, rtype: str, status: str) -> None:
    write(folder / "runs" / name / "run.yaml", f"run: {name}\ntype: {rtype}\nstatus: {status}\n")
    write(folder / "runs" / name / f"{name}.md", f"# {name}\n\nOne pass: p01.\n")


def make(root: Path) -> Path:
    block = Path(root) / PROJECT / BLOCK
    write(Path(root) / PROJECT / "README.md", "# Project-CoworkDemo\n\nPlaceholders for the s32 shoot.\n")
    write(block / "board.md",
          "# b01 · Demo\nboard-kind: cowork-block\nstate: 🟡 ACTIVE\nspine: one request to OFFICE_A, and its review.\n"
          "close: it is done.\n\n## Questions\n\n```yaml\nquestions:\n"
          "- id: Q01\n  title: Is it ready?\n  slug: ready\n  question: Is the request ready to send? What is still missing.\n"
          "  hypothesis: One form is missing.\n  work:\n  - j01_request/Timeline.md\n"
          "  report: reports/q01_ready/q01_ready.md\n"
          "- id: Q02\n  title: Who signs?\n  question: Who signs the request on our side?\n  work: []\n"
          "  report: reports/q02_signs/q02_signs.md\n```\n\n"
          "## Related resources\n\n```yaml\nresources:\n- title: The form\n  url: https://example.test/form\n"
          "  questions: [Q01]\n```\n")
    write(block / "reports/q01_ready/q01_ready.md", face("Is it ready?", "🟢 ANSWERED", "Q01", "answered",
                                                         "Yes, once the form is in."))
    write(block / "reports/q01_ready/page.toml", 'version = 1\nsource = "q01_ready.md"\ntitle = "Is it ready?"\n')
    write(block / "reports/q02_signs/q02_signs.md", face("Who signs?", "🔴 OPEN", "Q02", "open", "No answer yet."))
    write(block / "reports/q02_signs/page.toml", 'version = 1\nsource = "q02_signs.md"\ntitle = "Who signs?"\n')
    write(block / "studio/s01-flow/s01-flow.md", "s01 · flow\n=========\n\n**Topic:** the request, step by step.\n")
    write(block / "studio/s01-flow/s01-flow.excalidraw", '{"type":"excalidraw","elements":[]}')
    write(block / "studio/s02-roadmap.excalidraw", '{"type":"excalidraw","elements":[]}')   # the old page reads flat ones
    write(block / "j00_people/j00_people.md",
          "# People\njob-kind: cowork-job\nstate: 📇 REFERENCE\n\nPERSON_001 · owner\nPERSON_002 · OFFICE_A contact\n")
    run_card(block, "run-draw-s01", "draw", "open")
    run_card(block, "run-report-q01", "report", "closed")
    write(block / "delivery/q01_ready.md", "# Is it ready? (released)\n")

    job = block / "j01_request"
    write(job / "j01_request.md", job_page("Request to OFFICE_A", "🟡 ACTIVE", "PERSON_002", "2026-10-01", "send v2",
                                           "TICKET_001"))
    write(job / "Timeline.md", "- 2026-09-28 asked OFFICE_A\n- 2026-10-01 they replied\n")
    write(job / "CHECKLIST.md", "- [x] 1. Ask\n- [ ] 2. Send v2\n- [ ] 3. File the answer\n")
    write(job / "emails/2026-09-28-ask.md", "# Ask\n")
    write(job / "emails/2026-10-03-v2-draft.md", "# Version 2\nstatus: draft\n")
    write(job / "meetings/2026-10-02-call.md", "# Call\n")
    write(job / "materials/form.md", "# Form\n")
    run_card(job, "run-email-v2", "email", "draft")
    run_card(job, "run-meeting-call", "meeting", "closed")
    write(job / "t01_protocol/t01_protocol.md",
          "# t01 · Protocol\npage-kind: page\nstate: 🟡 DRAFT\n\n## Opening\n\nThe protocol, written with OFFICE_A in rounds.\n")
    write(job / "t01_protocol/page.toml", 'version = 1\nsource = "t01_protocol.md"\ntitle = "t01 · Protocol"\n')

    write(block / "j02_review/j02_review.md", job_page("Review by OFFICE_B", "🟡 ACTIVE", "us", "2026-10-05", "read the notes"))
    write(block / "j02_review/Timeline.md", "- 2026-10-05 notes in\n")
    write(block / "j03_done/j03_done.md", job_page("Done line", "✅ DONE", "nobody", "2026-09-01", "—"))
    return block


if __name__ == "__main__":
    print(make(Path(sys.argv[1])))
