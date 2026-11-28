# Types of a Work Block (CoWork)

The four lists a Work Block (CoWork)'s Jobs and Tasks are sorted by (s71 · Studio Type: Block Structure, Structure › Job-Task).
`## ` is a level, `### ` one type of it: `for:` what it is for, `holds:` what a Job or Task of that type must hold. A
level this Block type does not use says so with a `none:` line. Read by `block_types_pages.py` and
`block_types_check.py`.

None of these names is agreed yet: each was read from the example Block, carries `agreed: no`, and shows as 〈name〉
until JL agrees it (then `agreed: yes`, and the brackets go).

example: examples/Project-Ladder/cowork/b01_example_cowork

## Job group type
named: by each Block, on its `board.md` `bands:` line; optional

### Job group type 1
agreed: no
for: not pinned yet: the example Block names no group.
holds: to be agreed from the first Block that groups its Jobs.

## Job type
field: `job-type:` on the Job face; no Job of the example Block names one yet

### People
agreed: no
for: say who is involved and how to reach them; always `j00_people`.
holds: one line per person: role, contact, what they decide.

### Request
agreed: no
for: ask someone outside for something and follow it until it is answered.
holds: the request as sent, a `CHECKLIST.md` of what it still needs, a `Timeline.md` of what happened.

### Meeting
agreed: no
for: hold one meeting and keep what it decided.
holds: the notes and the decisions, each with who has the next move.

## Task group type
none: a CoWork Job has no Task level (hai-cowork: there is no `tNN` level)

## Task type
none: a CoWork Job has no Task level (hai-cowork: there is no `tNN` level)
