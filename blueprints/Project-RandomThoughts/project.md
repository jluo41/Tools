# Project-RandomThoughts

The one inbox of Tools: a loose thought or a meeting note lands here first, kept by topic and by date, and points to
the Block it feeds. Look-backs on finished work (the replays) sit beside them.

One Project of `Tools/blueprints/`; each Project keeps its Blocks in `work/`. Block numbers are unique across all of
Tools. The other Projects keep no `note/` of their own: a thought about their work lands here, and its `next:` names
their Block.

## Thoughts

One thought, one file: `note/YYMMDD-<slug>.md`, written fast. It is the Project inbox of `haipipe-project`
(`ref/project-structure.md` § note/) with one more field, `topic:`, a short lowercase name the thoughts on one
subject share.

```markdown
# <the thought in one line>

date: YYMMDD
from: <the session or the person, by role>
kind: thought             # thought · finding · gap
topic: <topic>
status: open              # open · moved · dropped
next: <Project>/work/bNN_<block>/ · jNN or sNN     # the one place it feeds; end with ? when it is a guess
first-step: <the Run, Job or topic edit that would use it>

<the thought>
```

A person's thought stays in their own words; a session adds the fields and the links, never a rewrite. When a thought
becomes work, `status:` turns `moved` and `next:` keeps where it went; a dropped one keeps one line on why. The file
stays where it is.

## Meetings

One meeting, one file: `cowork/meetings/YYYY-MM-DD-<slug>.md`, in the cowork meeting shape (`haipipe-cowork`).

```markdown
# <what the meeting was about>
Date: YYYY-MM-DD
With: <roles, never names>
Topics: <topic>, <topic>

- <one point a line>

Decided: <what was settled>
Next: <role> <does what>
```

A point that should shape later work is also written as a thought in `note/`, linking back to the meeting. Nothing
that belongs to an employer's or a client's work goes here (internal plans, customer or patient data): this
repository is not an employer's system.

## Topics

One line per topic: its name, what it covers, then its thoughts and meetings, newest first. A new topic gets its line
when its first thought or meeting is written.

- `tools-layout`: how Tools is organized and where things go.
  [261121 One place for loose thoughts and meetings](note/261121-one-inbox.md)

## Blocks

- `work/b41_agreeablerx_replay`: The AgreeableRx MISQ paper and its workbench, 2026-11-08 to 2026-11-14: eleven sessions, one Studio topic per day, and the replay page in `delivery/website/replay.html`.
- `work/b42_paper_workbench_review`: The paper workbench and its skills, 2026-11-08 to 11-15: what changed by area, what went wrong, and JL's decisions on what to change next.

## Design drafts

- [File System, UI System and Mapping](docs/figma/architecture-explorer/README.md): Figma screens and a clickable preview following one Chat from its files to its page.
