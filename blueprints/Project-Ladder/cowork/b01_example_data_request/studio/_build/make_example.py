"""The cowork prototype Block, written by this generator: every file of b01_example_data_request but the Studio topic's
face and builder (its own source, in j02_review_board_amendment/t01_data_use_plan/s01-data-use-plan-rounds/).

Placeholders only: every role, date, ticket and number is made up; no person's name, no organization, no address.
It shows each part of a cowork page once (b13, the plan of 261106): the people Job by role; a Job waiting on them, a
Job waiting on us, a done Job, each with its Timeline, CHECKLIST, an email and a meeting note; an email draft not sent
yet; two sends in delivery/; one Task, a document written in rounds; Questions in two groups (one answer agreed, one
proposed, one none); a waiting form and a decided record (collect.py); the Studio topic redrawn (its builder, then
render_png.py).

    python make_example.py          rewrites the example in place; run it again after any change here

The tools it calls write their own files: new_board.py and new_job.py scaffold a missing Block, Job or Task;
soft_run.py writes each soft Run's card and passes; collect.py the form and the record; email_page.py each send's copy
page; the topic's builder its drawing; render_png.py the preview. Nothing it makes is edited by hand.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BLOCK = Path(__file__).resolve().parents[2]
TOOLS = next(p for p in BLOCK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
SKILLS = TOOLS / "plugins" / "haipipe-toolkit" / "skills"
PROJECT = SKILLS / "1_base" / "project"
SOFT_RUN = PROJECT / "haipipe-run" / "scripts" / "soft_run.py"
COLLECT = SKILLS / "1_base" / "workbench" / "haipipe-interaction" / "scripts" / "collect.py"
EMAIL_PAGE = SKILLS / "2_theme" / "cowork" / "haipipe-cowork" / "scripts" / "email_page.py"
RENDER_PNG = PROJECT / "haipipe-studio" / "scripts" / "render_png.py"
sys.path.insert(0, str(PROJECT / "haipipe-job" / "scripts"))
from new_job import add_task, new_job  # noqa: E402  (haipipe-job: a missing Job or Task is scaffolded the one way)

J00, J01, J02, J03 = "j00_people", "j01_data_access_request", "j02_review_board_amendment", "j03_kickoff_meeting"
T01 = "t01_data_use_plan"
TOPIC = "s01-data-use-plan-rounds"
FOR = "b01.j02.t01-s01:example_data_request"          # the Studio topic every interaction here is about
NOTE = "a placeholder decision on the example; no person decided this"


def write(rel: str, text: str) -> Path:
    path = BLOCK / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.lstrip("\n"), encoding="utf-8")
    return path


def run(*args) -> str:
    out = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"{Path(str(args[0])).name} {' '.join(map(str, args[1:3]))}: {out.stderr or out.stdout}")
    return out.stdout.strip()


def fresh(rel: str) -> Path:
    """A folder this generator (or a tool it calls) fills: emptied first, so a rerun leaves nothing stale."""
    path = BLOCK / rel
    if path.exists():
        shutil.rmtree(path)
    return path


# ── the Block ────────────────────────────────────────────────────────────────────────────────────────────────────
BOARD = """
# b01 · Example data request (placeholder)

board-kind: cowork-block
state: 🟡 ACTIVE
owner: Project lead
spine: A placeholder request for a data extract from a partner office, and the review board amendment it needs; every role, date and number is made up.
close: The extract arrives under an approved amendment, and the data-use plan is filed.
status: 2026-11-06 the data owner holds the extract until the amendment is approved; our amendment draft waits to be sent.

## Topic

The cowork prototype: one coordination topic with people, as a cowork Block holds it. Every role, date, ticket and
number is a placeholder; no person or organization is named. It shows each part of a cowork page once.

- `j00_people/` who to ask, by role (📇 reference).
- `j01_data_access_request/` the request to the partner office; the next move is the data owner's.
- `j02_review_board_amendment/` the amendment the extract waits for; the next move is ours. Its Task
  `t01_data_use_plan/` is the data-use plan, written with the review board contact in rounds.
- `j03_kickoff_meeting/` the first meeting with the partner office (✅ done).

Everything sent is in `delivery/`, one folder per message with its attachments. This file and every file of the
example are written by `studio/_build/make_example.py`.

Excluded: running anything on the extract (a work Block's Task); a real request (a Project's own cowork Block).

## Questions

The questions this example Block answers, in two groups.

```yaml
questions:
- id: Q01
  title: What the partner office needs
  group: Needs
  question: What does the partner office need from us before it sends the extract?
  report: reports/q01_partner_needs/q01_partner_needs.md
  work:
  - path: j01_data_access_request
    role: The request and the data owner's reply.
- id: Q02
  title: The retention period
  group: Needs
  question: Which retention period does the data-use plan ask for?
  report: reports/q02_retention_period/q02_retention_period.md
  work:
  - path: j02_review_board_amendment/t01_data_use_plan
    role: The plan, written in rounds.
- id: Q03
  title: What could hold up the extract
  group: Blockers
  question: What could still hold up the extract once the amendment is approved?
  work:
  - path: j01_data_access_request
    role: The data owner's conditions.
```

## Related resources

```yaml
resources:
- title: Request form (placeholder)
  url: https://example.test/request-form
  questions: [Q01]
  contribution: The form the partner office asks every request to use.
```
"""

REPORTS = {
    "q01_partner_needs": ("Q01", "What the partner office needs", "answered", """
Agreed (261104): a signed data-use plan and the request form with its field list; the extract follows once the
review board approves the amendment.

## Content

- The request form went out with the field list on 2026-10-20 (`delivery/j01_data_access_request/`).
- The data owner's reply of 2026-10-28 names the approved amendment as the one condition left.
"""),
    "q02_retention_period": ("Q02", "The retention period", "proposed", """
Proposed (261106), waiting for you: two years after the study closes, the shorter of the two periods the review
board contact named in the comments on v1.

## Content

- The comments on v1 (2026-10-30) ask for a retention period in the plan.
- v2 leaves it open; the waiting form under `t01_data_use_plan` asks for the pick.
"""),
}

PEOPLE = """
# j00 · People
job-kind: cowork-job
state: 📇 REFERENCE
waiting-on: nobody
since: 2026-10-07
next: keep current as a role joins a Job
goal: Who to ask for help in this Block, by role; every role is a placeholder and names no person.

| Who | Side | Role here | Owns | Reach | Ask them about |
|---|---|---|---|---|---|
| Project lead | Our team | leads the request and signs each send | the Block, the request and every send | the project channel | priorities, a send to sign |
| Data owner | Partner office | holds the source data | the extract and its date | the partner office's request queue (ticket REQ-0001) | the fields, the extract date |
| Review board contact | Review board | reads the amendment and the data-use plan | the amendment's review | the review board's submission portal (ticket RB-0001) | the plan's wording, the retention period |
| Data analyst | Our team | checks the extract when it comes | the field check | the project channel | whether every field arrived |
| Partner coordinator | Partner office | books the meetings | the partner office's calendar | the partner office's front desk | a meeting time |
"""


def job_face(nn: str, title: str, head: dict, content: str, tasks: str = "") -> str:
    lines = [f"# {nn} · {title}", "job-kind: cowork-job"] + [f"{k}: {v}" for k, v in head.items() if v]
    one = "\n\n".join(" ".join(p.split()) for p in content.strip().split("\n\n"))   # a paragraph on one line: the
    return "\n".join(lines) + "\n\n## Content\n\n" + one + "\n"                     # page reads its first line + (f"\n## Tasks\n\n{tasks.strip()}\n" if tasks else "")


JOBS = {
    J01: dict(nn="j01", title="Data access request to the partner office",
              head={"state": "🟡 ACTIVE", "waiting-on": "Data owner", "since": "2026-10-28",
                    "next": "chase the extract date if there is no word by 2026-11-12", "ticket": "REQ-0001",
                    "goal": "The partner office sends the extract with every field on the request's list.",
                    "close": "The extract is in and the data analyst has checked its fields."},
              content="""
We asked the partner office for a placeholder extract: twelve fields, counted by month, no row-level data. The data
owner answered that the extract follows the approved amendment (j02); its date is theirs to give.
""",
              timeline="""
- 2026-10-14 the kickoff agreed what the request asks for (j03)
- 2026-10-20 sent the request with the field list
- 2026-10-24 intro call with the data owner
- 2026-10-28 the data owner: the extract follows the approved amendment; waiting on them since
""",
              checklist="""
- [x] 1. Fill in the request form
- [x] 2. Send the request with the field list
- [x] 3. Walk the fields with the data owner
- [ ] 4. Get the extract date
- [ ] 5. Receive the extract and check every field
""",
              emails={"2026-10-28-reply-from-the-data-owner.md": """
# Reply from the data owner
From: Data owner (partner office)
To: Project lead
Date: 2026-10-28
Subject: Re: Data access request (placeholder extract)

Thank you for the request and the field list. The twelve fields are all available, counted by month.

We send the extract once the review board approves your amendment; please forward the approval when you have it,
and we will give you a date then.
"""},
              meetings={"2026-10-24-intro-call-with-the-data-owner.md": """
# Intro call with the data owner
Date: 2026-10-24
With: Data owner, Project lead, Data analyst

- The data owner walked through the twelve fields; all are kept by month.
- No row-level data leaves the partner office: the extract is counts only.

Decided: the field list stays as sent.
Next: the data owner confirms the conditions by email (they did, 2026-10-28).
"""},
              materials={"request-form.md": """
# Request form (placeholder)

The partner office's form, as we filled it in: who asks, what for, which fields, for how long. Every answer here is
a placeholder.
"""}),
    J02: dict(nn="j02", title="Review board amendment",
              head={"state": "🟡 ACTIVE", "waiting-on": "us", "since": "2026-11-05",
                    "next": "pick the retention period, then send the amendment draft", "ticket": "RB-0001",
                    "goal": "The review board approves the amendment that lets the partner office send the extract.",
                    "close": "The amendment is approved and filed with the data-use plan."},
              content="""
The extract needs an amendment to the study's review board approval. The amendment carries the data-use plan, which
we write with the review board contact in rounds (Task t01). v2 answered every comment on v1; the retention period is
the one point left, and the amendment email waits as a draft until it is set.
""",
              tasks="1. t01_data_use_plan · Data-use plan, written in rounds",
              timeline="""
- 2026-10-27 sent v1 of the data-use plan to the review board contact
- 2026-10-30 six comments came back on v1
- 2026-11-02 call with the review board contact on the comments
- 2026-11-04 sent v2, every comment answered
- 2026-11-05 the review board contact: submit once the retention period is set; the move is ours
- 2026-11-06 drafted the amendment email (not sent)
""",
              checklist="""
- [x] 1. Write the data-use plan v1
- [x] 2. Answer the comments in v2
- [ ] 3. Pick the retention period
- [ ] 4. Send the amendment with the plan
- [ ] 5. Forward the approval to the data owner
""",
              emails={"2026-10-30-comments-on-v1.md": """
# Comments on v1
From: Review board contact
To: Project lead
Date: 2026-10-30
Subject: Re: Data-use plan v1

Six comments, numbered in the plan's margin. Two are about retention: the plan must name how long the extract is
kept, either one year or two years after the study closes.
""",
                      "2026-11-06-amendment-draft.md": """
# Amendment to the review board
status: draft
To: Review board contact
Cc: Data owner
Subject: Amendment: placeholder extract from the partner office
---
Hello,

Please find the amendment and the data-use plan for the placeholder extract. The plan answers each comment on v1.

1. The extract: twelve fields, counted by month.
2. The retention period: <set it before sending>.

Best regards,
Project lead
"""},
              meetings={"2026-11-02-call-with-the-review-board-contact.md": """
# Call with the review board contact
Date: 2026-11-02
With: Review board contact, Project lead

- Went through the six comments on v1; four were wording.
- Retention: one year or two years after the study closes are both accepted.

Decided: v2 answers the wording; the retention period is ours to pick.
Next: send v2 (sent 2026-11-04).
"""}),
    J03: dict(nn="j03", title="Kickoff meeting with the partner office",
              head={"state": "✅ DONE", "waiting-on": "nobody", "since": "2026-10-15",
                    "goal": "The partner office and our team agree what the request asks for.",
                    "close": "The kickoff notes are sent."},
              content="""
The first meeting with the partner office: what the study needs, which fields, who signs what. Its notes went to
everyone the next day.
""",
              timeline="""
- 2026-10-07 sent the invite through the partner coordinator
- 2026-10-14 the kickoff
- 2026-10-15 sent the notes
""",
              checklist="""
- [x] 1. Book a time with the partner coordinator
- [x] 2. Hold the kickoff
- [x] 3. Send the notes
""",
              emails={"2026-10-15-kickoff-notes.md": """
# Kickoff notes
From: Project lead
To: Data owner, Partner coordinator
Date: 2026-10-15
Subject: Kickoff notes (placeholder)

Thank you for the meeting. The notes are below; the request follows next week with the field list.
"""},
              meetings={"2026-10-14-kickoff.md": """
# Kickoff with the partner office
Date: 2026-10-14
With: Data owner, Partner coordinator, Project lead, Data analyst

- What the study needs: counts by month, twelve fields.
- Who signs: the project lead signs each send.

Decided: the request goes through the partner office's form.
Next: send the request with the field list (j01).
"""}),
}

TASK_FACE = """
# t01 · Data-use plan, written in rounds

task-kind: page
state: 🟡 IN PROGRESS · v2 sent; v3 waits on the retention pick
goal: The data-use plan the review board reads with the amendment, written with the review board contact in rounds.
waiting-on: us
since: 2026-11-05
next: pick the retention period (the waiting form), then write v3

## Content

v2 answers all six comments on v1; the retention period is the one point still open.

Each round is a pass of `runs/run-write-data_use_plan/`, and each version sent is a file of its `result/`. What came back is in the Job's `emails/`.
"""

PLAN = {"data_use_plan_v1.md": """
# Data-use plan v1 (placeholder)

1. Purpose: a placeholder study of monthly counts.
2. Fields: twelve, counted by month; no row-level data.
3. Storage: the project's approved storage only.
4. Retention: to be set.
""", "data_use_plan_v2.md": """
# Data-use plan v2 (placeholder)

1. Purpose: a placeholder study of monthly counts, as the review board contact worded it.
2. Fields: twelve, counted by month, listed by name; no row-level data.
3. Storage: the project's approved storage only; who can open it, by role.
4. Retention: one year or two years after the study closes (to pick before v3).
"""}

SENDS = {
    f"{J01}/2026-10-20-access-request": ("2026-10-20-access-request.md", """
# Data access request
status: sent
How: paste into a new email to the data owner and attach the field list.
To: Data owner (partner office)
Cc: Project lead
Subject: Data access request (placeholder extract)
Attach: requested-fields.csv
---
Hello,

We would like to request a placeholder extract for the example study. The attached list names the twelve fields.

1. Twelve fields, counted by month.
2. No row-level data.

Best regards,
Project lead
""", {"requested-fields.csv": "field,kind\n" + "".join(f"field_{c},count by month\n" for c in "abcdefghijkl")}),
    f"{J02}/{T01}/2026-11-04-plan-v2": ("2026-11-04-plan-v2.md", """
# Data-use plan v2
status: sent
How: paste into a reply to the comments on v1 and attach v2.
To: Review board contact
Cc: Project lead
Subject: Re: Data-use plan v1, now v2
Attach: data-use-plan-v2.txt
---
Hello,

Thank you for the six comments. v2, attached, answers each one; the retention period is the one point we still set.

Best regards,
Project lead
""", {"data-use-plan-v2.txt": PLAN["data_use_plan_v2.md"].lstrip("\n")}),
}

DELIVERY_MD = f"""
# Delivery

What this Block has sent, one row per send; a person marks a row sent.

| Send | From | State |
|---|---|---|
| `{J01}/2026-10-20-access-request/` | from {J01} | sent |
| `{J02}/{T01}/2026-11-04-plan-v2/` | from {J02} | sent |
"""

QUESTIONS = f"""
# Retention period

for: {FOR} @ retention-period

Placeholder questions on the example; every choice here is made up.

## Q1 · Retention period

The review board contact accepts one year or two years after the study closes.

**Which retention period goes into v3?**

- [x] A · Two years after the study closes.
- [ ] B · One year after the study closes.

Why A: The data analyst's checks may need a second year.

## Q2 · Who signs

The amendment goes out under one role's name.

**Who signs the amendment email?**

- [x] A · The project lead, as for every send.
- [ ] B · The data analyst.

Why A: One role signs every send.
"""


def main() -> None:
    write("board.md", BOARD)
    fresh("reports")
    for slug, (qid, title, status, body) in REPORTS.items():
        write(f"reports/{slug}/{slug}.md", f"""
# {qid} · {title}
answers: {qid}
answer-status: {status}

## Opening

{body.strip()}
""")
        write(f"reports/{slug}/page.toml", f'version = 1\nsource = "{slug}.md"\ntitle = "{qid} · {title}"\n')

    for name in (J00, J01, J02, J03):                        # a missing Job is scaffolded by haipipe-job first
        if not (BLOCK / name / f"{name}.md").is_file():
            new_job(BLOCK, name.split("_", 1)[1], name, nn=int(name[1:3]))
    write(f"{J00}/{J00}.md", PEOPLE)
    for name, j in JOBS.items():
        write(f"{name}/{name}.md", job_face(j["nn"], j["title"], j["head"], j["content"], j.get("tasks", "")))
        write(f"{name}/Timeline.md", f"# Timeline\n\n{j['timeline'].strip()}\n")
        write(f"{name}/CHECKLIST.md", f"# Checklist\n\n{j['checklist'].strip()}\n")
        for sub in ("emails", "meetings", "materials"):
            fresh(f"{name}/{sub}")
            for file, text in j.get(sub, {}).items():
                write(f"{name}/{sub}/{file}", text)

    job2 = BLOCK / J02                                       # the draft email's soft Run, waiting on the person to send
    fresh(f"{J02}/runs")
    email_run = Path(run(SOFT_RUN, "new", job2, "--type", "email", "--target", "amendment", "--skill", "haipipe-cowork",
                         "--ask", "draft the amendment email for the person to send",
                         "--close", "the person sends it and marks it sent"))
    run(SOFT_RUN, "pass", email_run, "--title", "Amendment email drafted", "--date", "1106", "--status", "waiting",
        "--summary", "The draft is in emails/; it waits on the retention period and on the person to send it.",
        "--changed", "emails/2026-11-06-amendment-draft.md")

    task = BLOCK / J02 / T01                                 # the document written in rounds
    if not (task / f"{T01}.md").is_file():
        add_task(job2, "data_use_plan", "Data-use plan, written in rounds", nn=1)
    write(f"{J02}/{T01}/{T01}.md", TASK_FACE)
    fresh(f"{J02}/{T01}/runs")
    plan_run = Path(run(SOFT_RUN, "new", task, "--type", "write", "--target", "data_use_plan", "--skill", "haipipe-draft",
                        "--ask", "write the data-use plan with the review board contact, one version per round",
                        "--close", "the review board contact has no comment left and the plan goes with the amendment"))
    for file, text in PLAN.items():
        (plan_run / "result").mkdir(exist_ok=True)
        (plan_run / "result" / file).write_text(text.lstrip("\n"), encoding="utf-8")
    (plan_run / "result" / "headline.txt").write_text(
        "v2 answers all six comments on v1; the retention period waits on a person before v3.\n", encoding="utf-8")
    run(SOFT_RUN, "pass", plan_run, "--title", "v1 to the review board contact", "--date", "1027",
        "--summary", "Four sections; the retention period left to set. Six comments came back on 2026-10-30.",
        "--changed", "result/data_use_plan_v1.md")
    run(SOFT_RUN, "pass", plan_run, "--title", "v2 answers the six comments", "--date", "1104", "--status", "waiting",
        "--summary", "Every comment answered; the retention period is the one point open, asked in the waiting form.",
        "--changed", "result/data_use_plan_v2.md,result/headline.txt")

    form = Path(run(COLLECT, "new", task, "retention_period", "--title", "Retention period",
                    "--for", f"{FOR} @ retention-period"))
    (form / "question_collection.md").write_text(QUESTIONS.lstrip("\n"), encoding="utf-8")
    run(COLLECT, "check", form)
    run(COLLECT, "build", form)
    run(COLLECT, "record", task, "data_use_plan", "--title", "Plan decisions", "--for", f"{FOR} @ data-use-plan",
        "--decision", f"Four sections :: The plan keeps four sections: purpose, fields, storage, retention :: {NOTE}",
        "--applied-by", "v2 of the plan, run-write-data_use_plan p02")

    fresh("delivery")                                        # each message sent, its draft beside its attachments
    write("delivery/delivery.md", DELIVERY_MD)
    for where, (draft, text, attach) in SENDS.items():
        md = write(f"delivery/{where}/{draft}", text)
        for file, body in attach.items():
            write(f"delivery/{where}/{file}", body)
        run(EMAIL_PAGE, md)

    topic = task / TOPIC                                     # the Studio topic: its builder, then its preview
    run(topic / f"build_{TOPIC.replace('-', '_')}.py")
    run(RENDER_PNG, topic / f"{TOPIC}.excalidraw", topic / f"{TOPIC}.png")
    print(BLOCK.name, "written")


if __name__ == "__main__":
    main()
