Method
======

1 · The six steps
-----------------

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| Name the Block | one coordination topic: its spine, its close condition and the gate it waits for, such as an ethics approval | Scope | Scope › Block · run Update the Block status | the spine |
| Open the Job | one Job folder `jNN_<job>/` for each line of work, usually one request to one office; its page header says who has the next move, since when, the next step | Job | Work › Jobs · run Open a job | the request |
| Draft the message | the message is drafted inside its checklist step or in the Job's `emails/`; a different agent reviews it; only the person sends it | Job, Report | Work › Emails · Check › Drafts · runs Draft an email, Review a draft | the send |
| Track the wait | when the next move changes hands, the job page header changes (waiting-on, since, next) and the Job's Timeline.md gets the date | Job | Check › Waiting on · Work › Jobs · runs Update a job, Draft a follow-up | none |
| Meet and record | a dated note for each meeting; its decisions move into the Job's `design/` | Record | Work › Meetings · run Write meeting notes | none |
| Answer the Question | a report Page written from the Block's own files; a different agent checks it; the person releases it | Report | Work › Questions · Check › Reports · Delivery › Reports · runs Write the report, Check a report | the release |

A failed check goes back to the step that owns the fault: a vague topic to Name, a missing
Job to Open, a wrong message to Draft, a stale wait to Track, a lost decision to Meet,
an unsupported sentence to Answer. Nothing is fixed in a generated file: a built report or a
drawing changes only by rerunning what made it. No agent sends a message; the person does.
Every run is in the Runs panel beside its Space, with the prompt to copy.

One example runs through this page, and it is made up: a study asks a hospital IT office
for a cloud storage group to hold its wearable data. The Block is `b11_cloud_storage`; the
request is Job `j02_cloud_group` (the office's number is `IT-1042`); the gate is the ethics approval, Block `b01_irb`.


2 · Step 1 in depth: naming the Block
-------------------------------------

A Block is one coordination topic of a research Project (`cowork/bNN_<topic>/`), and its
`board.md` header says what it is. In the example: the spine is "get a cloud storage group
for the wearable data and say how the study uses it", the close condition is "the group
exists, its access list is agreed and the IRB (Institutional Review Board, the ethics
committee) has approved the storage plan", and it waits for Block `b01_irb`. A gate is
something every later step waits for; naming it keeps the Block from being worked on in
the wrong order.

| family | method | card |
|---|---|---|
| Scope: How is one coordination topic bounded? | By one topic | methods/cowork/01-by-one-topic.md |

| test | asks | when | source |
|---|---|---|---|
| T0 Bounded | the spine, the close condition and the gate are written before any Job is opened | step 1 | coordination as managing dependencies (Malone & Crowston 1994) |

In the example, T0 fails if the Block says "storage" and nothing about when it is done.


3 · Steps 2 to 4 in depth: the request, the message and the wait
----------------------------------------------------------------

A line of work is a Job: a folder `jNN_<job>/`, usually one request to one office. Its
page `jNN_<job>/jNN_<job>.md` starts with header lines:

```
# <title>
job-kind: cowork-job
state: 🔴 OPEN | 🟡 ACTIVE | ⏸️ ON HOLD | ✅ DONE | 📇 REFERENCE
waiting-on: us | <person> | nobody
since: YYYY-MM-DD
next: <the next step>
ticket: <office number, optional>
url: <link, optional>
```

and then what we asked for and why. Inside the Job, `Timeline.md` holds the dates and
`CHECKLIST.md` holds the numbered steps (`- [ ]` open, `- [x]` done), each with its draft
message inside it; `emails/`, `meetings/`, `design/` and `materials/` exist only when
needed. Every Block also has `j00_people/` (state 📇 REFERENCE): who to ask for help. Each
message is drafted inside its step, or in `emails/`, marked `status: draft`. In the example, step 3 of the checklist in
`j02_cloud_group` is "send the diagram and the IRB wording to the IT office"; the draft sits
under it; a reviewer finds the IRB number missing; the person fixes it and sends. Then
`waiting-on` in the job page header changes from `us` to `IT office`, `since` becomes the
send date, and Timeline.md gets the date.

| family | method | card |
|---|---|---|
| Job: How does a request to another office stay one thing, and keep moving? | By one job per request | methods/cowork/02-by-one-job-per-request.md |
| Job: How does a request to another office stay one thing, and keep moving? | By checklist draft | methods/cowork/03-by-checklist-draft.md |
| Job: How does a request to another office stay one thing, and keep moving? | By named wait | methods/cowork/05-by-named-wait.md |
| Report: How does the answer reach the reader, checked? | By independent review | methods/cowork/04-by-independent-review.md |

| test | asks | when | source |
|---|---|---|---|
| T1 One Job | each request has one Job folder whose page header has its state, waiting-on, since and next step | step 2 | coordination as managing dependencies (Malone & Crowston 1994) |
| T2 Reviewed draft | an agent other than the writer reviewed the draft before it was sent | step 3 | self-preference of model evaluators (Panickssery et al. 2024) |
| T3 Person sends | the message is marked draft until the person sends it, and no agent sends | step 3 | a checklist for team communication (Haynes et al. 2009) |
| T4 Wait named | waiting-on and since match the last move in Timeline.md | step 4 | delay in work across sites (Herbsleb & Mockus 2003) |

In the example, T2 fails if the agent that wrote the draft also reviewed it, and T4 fails
if the job page header says we have waited since 2026-10-02 while Timeline.md shows a reply on
2026-10-09.


4 · Step 5 in depth: meeting and recording
------------------------------------------

A meeting with the IT office or the IRB is written down the same day as
`<job>/meetings/YYYY-MM-DD-<topic>.md`: who was there, what was said, what was decided. The note
is a record; the decision's home is the Job's `design/`. In the example, "the group will hold
de-identified files only" is a decision, so it moves into `j02_cloud_group/design/storage-plan.md`, and
the Job's `next:` line changes.

| family | method | card |
|---|---|---|
| Record: How do meetings and decisions stay findable? | By dated record | methods/cowork/06-by-dated-record.md |

| test | asks | when | source |
|---|---|---|---|
| T5 Dated | each meeting note carries its date, and each decision in it appears in the Job's design/ | step 5 | team science needs shared structures (Hall et al. 2018) |

In the example, T5 fails if the note says "decided: de-identified only" and the Job's `design/` still
says "identified files allowed".


5 · Step 6 in depth: answering the Question
-------------------------------------------

A Question of the Block, for example "Can the study store wearable data in the cloud?", is
answered by a report Page in `reports/qNN_<topic>/`: Answer, Evidence, Limits, Next. Its
`work:` names files in the Block (the job page, a design note, a meeting note), not code.
Each claim names the file it came from. An agent that wrote nothing in the report checks
it, and the person releases it.

| family | method | card |
|---|---|---|
| Report: How does the answer reach the reader, checked? | By report from block files | methods/cowork/07-by-report-from-block-files.md |
| Report: How does the answer reach the reader, checked? | By independent review | methods/cowork/04-by-independent-review.md |

| test | asks | when | source |
|---|---|---|---|
| T6 Cited | every claim in the report names a Block file that exists | step 6 | good enough practices (Wilson et al. 2017) |
| T7 Independent | an agent that did not write the report checks it | step 6 | self-preference of model evaluators (Panickssery et al. 2024) |

In the example, T6 fails if the report says "access is approved" with no job page or
meeting note behind it.


6 · Why it works
----------------

One topic, one home
~~~~~~~~~~~~~~~~~~~

Coordination is managing dependencies between activities (Malone & Crowston 1994). A Block
names its one topic and its gate, so the dependencies of a request are written where the
request is.

```
Block        b11_cloud_storage          spine · close · waits-for b01_irb
   ↓ holds
Jobs         j02_cloud_group            page header · Timeline · CHECKLIST
   ↓ moved by
Messages     drafts, meetings           reviewed, then sent by the person
   ↓ feed
Report       Answer · Evidence · Limits · Next      checked, then released
```

What the evidence says
~~~~~~~~~~~~~~~~~~~~~~

- Work that spans sites took about two and one half times as long, and the number of
  people involved was strongly related to the delay (Herbsleb & Mockus 2003), so each
  wait is named with its date.
- A checklist built to improve team communication reduced complications and deaths in
  eight hospitals (Haynes et al. 2009), so a request keeps its steps in order.
- A model judging text tends to score its own output higher (Panickssery et al. 2024), so
  the writer of a draft or a report never reviews it.
- No study tests this whole loop on agent-assisted coordination; its order is our own
  judgment.


Reference
---------

Terms
~~~~~

| term | means here |
|---|---|
| Block | one `cowork/bNN_<topic>/` folder: one coordination topic and its workbench |
| Job | one line of work, usually one request to one office: a folder `jNN_<job>/` with its page, Timeline.md and CHECKLIST.md |
| Job page header | the lines `state`, `waiting-on`, `since`, `next` (and `ticket`, `url`) at the top of `jNN_<job>/jNN_<job>.md` |
| Register | a YAML list under a `##` heading in `board.md` (Questions, Related resources) |
| `j00_people/` | the Block's people Job (📇 REFERENCE): who to ask for help |
| Gate | an approval that other work waits for, such as an ethics approval |
| Waiting-on, since | header lines of the job page: who the next move belongs to, and the date that wait began |
| Draft | a message marked `status: draft` until the person sends it |
| Question, report | a register entry in `board.md` and its Page `reports/qNN_<topic>/` |

| term | 中文 | read more |
|---|---|---|
| Science of team science | 团队科学 * | [Wikipedia](https://en.wikipedia.org/wiki/Science_of_team_science) |
| Institutional review board | 伦理审查委员会 | [Wikipedia](https://en.wikipedia.org/wiki/Institutional_review_board) · [中文维基](https://zh.wikipedia.org/wiki/伦理审查委员会) |
| Checklist | 检查清单 * | [Wikipedia](https://en.wikipedia.org/wiki/Checklist) |
| Issue tracking system | 问题跟踪系统 * | [Wikipedia](https://en.wikipedia.org/wiki/Issue_tracking_system) |
| Research data management | 研究数据管理 * | [Wikipedia](https://en.wikipedia.org/wiki/Research_data_management) |

Rules
~~~~~

1. One Block is one coordination topic; it names its close condition and its gate.
2. One line of work is one Job: one folder, one page with its header.
3. A message is drafted inside its step or in `emails/`, reviewed by a different agent, and
   sent only by the person.
4. When the next move changes hands, the job page header changes and the Job's Timeline.md gets the date.
5. A meeting is a dated note; its decisions move into the Job's `design/`.
6. A report cites Block files; a different agent checks it; the person releases it.
