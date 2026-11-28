# Types of a Work Block (Blueprint)

The four lists a Work Block (Blueprint)'s Jobs and Tasks are sorted by (s71 · Studio Type: Block Structure, Structure › Job-Task).
`## ` is a level, `### ` one type of it: `for:` what it is for, `holds:` what a Job or Task of that type must hold. A
level this Block type does not use says so with a `none:` line. Read by `block_types_pages.py` and
`block_types_check.py`.

None of these names is agreed yet: each was read from the example Block, carries `agreed: no`, and shows as 〈name〉
until JL agrees it (then `agreed: yes`, and the brackets go).

example: examples/Project-Ladder/blueprint/b17_theme_work

## Job group type
named: by each Block, on its `board.md` `bands:` line (`j0N Earlier design · j1N Workbench`)

### Tool area
agreed: no
for: the Jobs that plan one area of the tool.
holds: Jobs whose parts ship together; an area that is replaced stays as a closed group.

## Job type
field: `job-type:` on the Job face; no Job of the example Block names one yet

### Job type 1
agreed: no
for: not pinned yet: the example Block's Jobs carry no `job-type:` line.
holds: to be agreed from the first Jobs that name their type.

## Task group type
named: by each Job, on its face's `bands:` line (`t0N Page components`)

### Parts of one page
agreed: no
for: the Tasks that design the pieces of one page or one tool.
holds: Tasks that can be designed and shown one by one.

## Task type
field: `task-type:` on the Task face

### ui
agreed: no
for: design a piece a person sees on a page.
holds: a preview a person can open, and the page part it changes.

### tool
agreed: no
for: design a script, a check or a skill step a page relies on.
holds: the command, what it reads and writes, and a check that it holds.
