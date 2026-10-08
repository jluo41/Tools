# b13 · Theme: cowork

board-kind: task-block
spine: Design questions about the cowork Theme as one ladder: what a CoWork Block, a line-of-work Job and its pieces (emails, meetings, checklist) each hold and show, whether a cowork Job has Tasks at all, where waiting-on and drafts go once there is no Check Space, and what a cowork Block delivers.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The cowork Theme coordinates one topic with people: who has the next move, what was sent,
what was decided. Its Block is `cowork/bNN_<topic>/` (`board-kind: cowork-block`) with a people
Job `j00_people/` and one Job per line of work (`jNN_<job>/`: its state in the page header,
`Timeline.md`, `CHECKLIST.md`, `emails/`, `meetings/` when it has them). It has no Task level today.

Today the CoWork workbench shows it at Block level in four Spaces (Scope · Work · Check ·
Delivery): Jobs, Questions, Emails and Meetings are Views of Work; Waiting on and Drafts are
Views of Check.

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how cowork fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the cowork skills (`2_theme/cowork/haipipe-cowork`, `workbench-cowork`), the CoWork workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); writing a report Page
(haipipe-page).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. The studio topics:

- `studio/s01-cowork-ladder/`: every cowork row, Block to Run, proposed and today, with Q01's
  proposed answer in its overview frame. Drawn from b03's shared definitions
  (`b03_project_workbench/studio/s01-overall-tree-structure/`) by its own `build_s01_cowork_ladder.py`, and
  rebuilt by b03's `studio/_build/make.sh`.
- `studio/s02-cowork-workbench/`: today's CoWork workbench design drawing, moved from
  `servers/workbench-cowork/studio/` (261007); the Guide's RoadMap Draw opens it.
- `studio/s32-cowork-element-ui/`: every element the cowork theme draws (frame and old page, shot live
  from a placeholder Block), the planned screen from b03's s11 · s12 cowork rows, and the proposed
  unified look beside each; its Theme elements list feeds b03's s32 (261008).

The workbench on the base frame is `servers/workbench-cowork/cowork_theme.py` (Q01).

## Questions

```yaml
questions:
- id: Q01
  title: How does a cowork topic climb the ladder?
  question: What do the CoWork Block and a line-of-work Job each hold and show on screen, and does
    a cowork Job have Tasks (an email thread, a meeting, a draft) or stop at the Job?
  hypothesis: The Block keeps people and the Questions; a Job is one line of work with the six Spaces,
    Work Details = its Timeline, emails and meetings as groups; an email or meeting is a row, not
    a Task, unless it needs Runs of its own.
  acceptance: Answered when each level names its folder and its six Spaces' content, and the Task
    question is decided, drawn in studio/.
  work: []
  report: reports/q01_cowork_ladder/q01_cowork_ladder.md
- id: Q02
  title: Where do waiting-on and drafts go?
  question: Today's Check Space shows Waiting on, Drafts and Reports; the six Spaces have no Check.
    Where does who-we-wait-on, an unsent draft and a stale Job show?
  hypothesis: Waiting-on is a chip on each Job row in Block › Work Details (and the Job's own header);
    a draft is a soft Run (run-email-<thread>) under Runs until sent; a stale Job is a row state,
    not a Space.
  acceptance: Answered when every one of today's Check Views has a place in the six Spaces, or a stated
    reason to keep one.
  work: []
  report: reports/q02_waiting_and_drafts/q02_waiting_and_drafts.md
- id: Q03
  title: What does a cowork Block deliver?
  question: What does a cowork Job or Block release (a sent email, a signed decision, a done Job),
    and where do done Jobs go?
  hypothesis: A Job delivers what it sent and what was decided; Block › Delivery lists done Jobs and
    released reports; nothing is built.
  acceptance: Answered when Delivery at each level is either empty with a reason or names what it
    holds.
  work: []
  report: reports/q03_cowork_delivery/q03_cowork_delivery.md
```

## Related resources

```yaml
resources:
- title: haipipe-cowork skill (the CoWork Block contract)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/cowork/haipipe-cowork
  questions:
  - Q01
  - Q02
  - Q03
- title: workbench-cowork skill (the CoWork workbench)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/cowork/workbench-cowork
  questions:
  - Q01
  - Q02
  - Q03
```
