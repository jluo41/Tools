# Types of a Work Block

The four lists a Work Block's Jobs and Tasks are sorted by, pinned here and nowhere else (s71 · Studio Type: Block
Structure, Structure › Job-Task). `## ` is a level, `### ` one type of it: `for:` what it is for, `holds:` what a Job
or Task of that type must hold. A Job names its type on its face (`job-type:`), a Task on its own (`task-type:`); a
group is the decade of a number, named on a `bands:` line. Read by the Job types and Task types views of the Block
Job UI Preview (s11), the Jobs page rows, and `block_types_check.py`.

These names are read from one example, b01_example_work (a CSV checker). None is agreed yet as a type every Work Block
uses: each carries `agreed: no` and shows as 〈name〉 until JL agrees it (then `agreed: yes`, and the brackets go).

example: examples/Project-Ladder/work/b01_example_work

## Job group type
named: by each Block, on its `board.md` `bands:` line (`j0N First version · j1N Second version · j2N Ideas`)

### Version
agreed: no
for: one stretch of the work that ends in something a user can run.
holds: the Jobs that build, check and write that version; closed together.

### Ideas
agreed: no
for: candidates not yet agreed to build.
holds: Jobs that stay open questions until one is moved into a Version.

## Job type
field: `job-type:` on the Job face

### code
agreed: no
for: build a part of the tool.
holds: Tasks whose Runs produce code that runs; a result a user can call.

### check
agreed: no
for: prove a part of the tool is right.
holds: Tasks whose Runs test or measure; a pass or fail per case.

### doc
agreed: no
for: write what a person reads to use or release the tool.
holds: Tasks whose Runs produce a document; a reader can follow it without the author.

## Task group type
named: by each Job, on its face's `bands:` line (`t0N ... · t1N ...`)

### Make
agreed: no
for: the Tasks that produce the Job's thing.
holds: Tasks run in order; each one's output feeds the next.

### Show
agreed: no
for: the Tasks that present what was made.
holds: Tasks that read the Make Tasks' results and produce a report, a table or a figure.

## Task type
field: `task-type:` on the Task face (a kind of hai-task)

### code
agreed: no
for: write and run code.
holds: `scripts/`, hard Runs under `runs/`, each with its result.

### display
agreed: no
for: produce one display, a figure or a table.
holds: a display unit: its recipe, its assets and its preview.
