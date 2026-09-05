fn-block: Scaffold a New Task Block Board
==========================================

A Block is the Board over one large task topic. It contains related Jobs;
their Tasks are the Board Pages and their Runs remain execution records.

Output: `examples/{PROJECT_ID}/tasks/bNN_{block_name}/`.


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
index or resurrect the retired A/B/C/D type-letter scheme.


Step 3 - Create the Board skeleton
----------------------------------

Create exactly:

```
tasks/bNN_{block_name}/
├── board.md
└── diagram/                 optional until a shared narrative is authored
```

Start `board.md` from `ref/block-board-template.md` and set:

```yaml
board-kind: task-block
```

The Task tree is the membership and default-order authority:

```
Block Board -> Job Group -> Task Page -> Run execution record
```

`## Pages` may contain Job headings and introductions without restating Task
rows. If an explicit Task order is needed, list the full relative Page path:

```
j01_job_name/t01_task_name/t01_task_name.md
```

Do not use a bare Task filename: two Jobs may legitimately contain the same
Task name.

When the Block is cohesive and its shared narrative is ready, create
`diagram/` through `diagram-ascii` with the canonical overview, task map,
progress, and design records, then bundle the canvas. Do not invent diagram
content merely to fill the folder.


Step 4 - Optionally create the first Job
----------------------------------------

Proceed through the Task orchestrator's Job scaffold. The Job, not the Block,
owns `sbatch/`, shared `src/`, generated `results/`, and its Tasks.


Step 5 - Check the new Board
----------------------------

Run both contracts before reporting the scaffold complete:

```bash
python3 Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/check.py <block>
python3 Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/check_task_tree.py <block>
```

The Board check must be clean immediately. A container-only Block may also be
clean in the Task-tree checker; run the checker again after the first Job and
Task are scaffolded so S18 and the execution-shape rows are exercised.


MUST NOT
--------

- Create `README.md` in the Block.
- Create Block-level `sbatch/`, `src/`, `scripts/`, `results/`, or workflow
  code. Runnable material belongs to a Job or Task.
- Copy the Task tree into `board.md` merely to make Tasks visible.
- Turn a Run into a Board Page.
