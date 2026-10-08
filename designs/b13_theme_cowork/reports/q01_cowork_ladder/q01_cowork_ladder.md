# How does a cowork topic climb the ladder?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

Proposed 261007, waiting for JL: a cowork topic climbs Block → Job → Run; an email, a meeting
or a checklist step is a row of its Job, not a Task.

**Where this Page sits:** [Q01](../../board.md) · What do the CoWork Block and a line-of-work Job
each hold and show on screen, and does a cowork Job have Tasks (an email thread, a meeting, a draft)
or stop at the Job?


## Content

### Answer

**A cowork topic climbs Block → Job → Run. An email, a meeting or a checklist step is a row of its
Job, not a Task.** A Task appears only when a Job writes a document with others over several rounds
(a protocol, an SOP). That Task is then a Page Task, shown on the shared Task tab.

```text
Block   cowork/bNN_<topic>/                      one coordination topic       the Block tab
Job     jNN_<job>/                               one line of work             the Job tab, six Spaces
item    Timeline · CHECKLIST · emails/ · meetings/   rows of Job › Work Details, by date
Task ?  tNN_<doc>/                               only a document written in rounds: a Page Task
Run     runs/run-<type>-<target>/                soft only, at Block and Job; a pass per round
```

**Why a row and not a Task.** There are five reasons:

1. An email or a meeting is one file. A Task is a folder with its own face, `runs/` and `delivery/`.
2. Its work fits a soft Run of the Job (b03 s01-D15, D17). For example, `run-email-<thread>`
   writes `emails/<thread>.md`, with one pass per round.
3. Cowork makes no facts, so it has no hard Runs and no work Task. Work that runs code is a work
   Task in another Block, and a cowork Question cites it. The skill already says this.
4. One Job screen answers who has the next move. Work Details › Timeline lists every email,
   meeting and step by date.
5. The hypothesis holds: an item becomes a Task only "if it needs Runs of its own". Only a
   document written over several rounds does.

**Each level's six Spaces.** Each level uses the Description · Idea Studio · Audience Report |
Work Details | Runs · Delivery order (b03 s01-D20, D22):

```text
Space            Block tab                                        Job tab
Description      bNN_<topic>.md · Scope · People · Resources ·    jNN_<job>.md header and text
                 Related                                          · Job · Files (materials/)
Idea Studio      studio/sNN-<topic>/ (was Scope › RoadMap Draw)   optional studio/
Audience Report  reports/qNN_*: Question │ Work │ Report          optional: the Block's Questions
                 (was Work › Questions)                           that cite this Job
Work Details     its Jobs: All · open · waiting · done            its rows: Timeline · Checklist ·
                 (was Work › Jobs)                                Emails · Meetings
Runs             run-status- · run-draw- · run-report- ·          run-email- · run-notes- ·
                 run-check-                                       run-update-job · run-check-
Delivery         optional: answered reports · done Jobs (Q03)     optional: sent and decided (Q03)
```

The Job tab now has the Block's six Spaces, as the DIKW level and the design Job already do. It
replaces the older Overview · Studio · Reports | Timeline · Emails · Meetings | Runs · Delivery.
The cowork Job's header (`state · waiting-on · since · next · ticket · url`) remains the only place
the Job's state is written.

**Today's Check Space.** Check is removed (b03 s01-D18):

- Waiting on becomes a chip on each Job row.
- Drafts become open `run-email-<thread>` Runs.
- Reports becomes `run-check-<qNN>`, with the release in Delivery.

Q02 settles the details.


### Evidence

- [cowork ladder](../../studio/s01-cowork-ladder/s01-cowork-ladder.excalidraw) (preview
  `s01-cowork-ladder.png`). The overview frame holds this answer. The Block and Job frames show
  the proposed screens above today's.
- The cowork rows are defined once in b03's shared definitions:
  `Tools/designs/b03_project_workbench/studio/s01-overall-tree-structure/build_ladder_v4.py`
  (`BLOCK_TREES` "cowork Block", `JOB_TREES` "cowork Job", `JOB_SPACES_COWORK`, `level_subs`) and
  `level_views.py` (`JOB_FAMILY_VIEWS["cowork"]`, `COWORK_ROWS`, `COWORK_NOTES`).
- The contract today: `Tools/plugins/haipipe-toolkit/skills/2_theme/cowork/haipipe-cowork/SKILL.md`
  ("There is no `tNN` level") and `workbench-cowork/ref/workbench-table.md`.


### Limits

- No real cowork Block was found in this SPACE, so the rows come from the skill's contract with
  placeholders only.
- Still a proposal. The workbench follows it: `Tools/plugins/haipipe-toolkit/servers/workbench-cowork/cowork_theme.py`
  draws the Block and Job levels on the base frame (`/_board/workbench?path=<Block or Job>`), tested on a
  placeholder Block (`tests/test_cowork_theme.py`, 4 tests). Today's four-Space page is unchanged. The
  haipipe-cowork contract and its scaffold are not changed yet.


### Next

Open, marked red in the drawing:

1. `j00_people/` is not a line of work. Should People move to `people.md` at the Block (shown as
   Description › People)? This changes real Blocks, so JL decides.
2. A Job's `design/` folder: should its drawings move to `studio/` and its notes to `materials/`?
   This changes real Jobs, so JL decides.
3. The Task ▾ tab on a cowork Block: should it stay greyed unless the open Job has a `tNN_<doc>/`?
4. `board.md` → `bNN_<topic>.md` (b03 s01-D12): rename it together with every other Theme.
5. Q02: where waiting-on, drafts and a stale Job show. Q03: what a Block and a Job deliver.

Once JL settles these, the haipipe-cowork contract and scaffold follow (new Block · Job · Run,
plus Page Task by reference); the workbench theme changes with any answer that moves a Space.
