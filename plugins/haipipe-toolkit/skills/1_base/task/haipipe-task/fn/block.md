fn-block: Scaffold a New Task Block Board
==========================================

A Block is the Board over one large task topic. It contains related Jobs;
their Tasks are the Board Pages and their Runs remain execution records.

Output: `examples/{PROJECT_ID}/work/bNN_{block_name}/`.


Step 1 - Identify the project
-----------------------------

Resolve the parent project:

- explicit `--project-id <PROJECT_ID>` -> use it;
- cwd inside `examples/Proj*/` -> use it;
- project id present but folder missing in AUTO mode -> scaffold it through
  `haipipe-project`, then continue;
- no project can be resolved -> block and request the project id.


Step 2 - Name and index the Block
---------------------------------

Use the next free two-digit pipeline index, starting at 01 with no gap at
scaffold time. The name is snake_case `<noun>_<qualifier>` and passes the
stranger test: a reader can tell what thing and which one from the folder name.

Compose `bNN_{block_name}`, for example:

- `b01_physician_ground_truth`
- `b02_llm_recommendation_runs`
- `b05_paper_display`

The `b` prefix carries level only. Never infer a Task type from the Block
index or introduce a second type-letter scheme.


Step 3 - Create the Board skeleton
----------------------------------

Make the folder and its face with haipipe-block's scaffold, then fill the face from this skill's
work template:

```bash
python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-block/scripts/new_board.py <work/> --slug <block_name> --title '<title>'
```

```
work/bNN_{block_name}/
├── board.md                 from ref/block-board-template.md
└── studio/                  made when its first topic is drawn (haipipe-studio)
```

The face carries `board-kind: task-block` and `workbench-layout: workflow`, so the workbench opens on
Goal · Plan · Execution · Results; its own `## Deliverables` holds only what no Job owns. The Task
tree is the membership and default-order authority:

```
Block Board -> Job Group -> Task Page -> Run execution record
```

`## Pages` may contain Job headings and introductions without restating Task rows. If an explicit
Task order is needed, list the full relative Page path (`j01_job_name/t01_task_name/t01_task_name.md`);
never a bare Task filename, since two Jobs may hold the same Task name.

For a question-driven Block, follow `haipipe-report` (`ref/block-questions.md`): register the
Questions in `board.md`, place their Report Pages in `reports/`, and draw in `studio/` topics
(`haipipe-studio`). Create these when the Block's questions are known; never prefill invented
questions or answers. Report Page Folders are documentation, never executable Tasks or Job groups.


Step 4 - Optionally create the first Job
----------------------------------------

Make the Job with haipipe-job (`new_job.py job <block> --slug … --title … --goal … --close …`), then
its Tasks (`new_job.py task`); the Job, not the Block, owns `sbatch/`, shared `src/` and its Tasks,
and each Task's Runs write their own `runs/<run>/result/`. Then `/wb update <block>` checks today's rules.


Step 5 - Check the new Board
----------------------------

Run both contracts before reporting the scaffold complete:

```bash
python3 Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft/cli/check.py <block>
python3 Tools/plugins/haipipe-toolkit/skills/1_base/task/haipipe-task/scripts/check_task_tree.py <block>
```

The Board check must be clean immediately. A container-only Block may also be
clean in the Task-tree checker; run the checker again after the first Job and
Task are scaffolded so S18 and the execution-shape rows are exercised.


MUST NOT
--------

- Create `README.md` in the Block.
- Create Block-level `sbatch/`, `scripts/`, `results/`, or workflow code. Runnable material belongs to
  a Job or Task; a Block's `src/` holds only code its Jobs share (haipipe-project ref/ladder.md).
- Copy the Task tree into `board.md` merely to make Tasks visible.
- Turn a Run into a Board Page.
