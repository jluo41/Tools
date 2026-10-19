# Proposing a Job's tree: Tasks, Runs, their types, order and states

A Job drawing is only as good as the tree under it. Before a Job is drawn, or when it is redrawn, propose the
Tasks and Runs it is missing, so a reader sees what is done, what failed, what is ready and what is only an idea,
in the order it should happen. Asked 261019: "一定要把这些 run 也 propose 好，然后每一个 run 都要排序排好" (propose
the Runs too, and put every Run in order), and "the /excalidraw-job should add a fn about how to propose and group
the tree of job-task-runs".

```text
Job   one setup        jNN_M-<model>_D-<data>_E-<engine>     what is fixed: model, data, engine
Task  one algorithm    tNN_A-<algorithm>[_<what>]            what is done on that setup: sft, grpo, …
Run   one setting      rNN_<type>_<slug>                     what is varied, numbered by its type's band
```

## 1. Group: which level a thing belongs to

1. **Job**: whatever every Task shares and a reader compares across Jobs: the model, the dataset, the engine.
2. **Task**: one algorithm, or one question with its own worker (`scripts/`). Two algorithms, two Tasks.
3. **Run**: one setting of a Task's worker. A knob the worker already takes is a Run, never a new Task.
4. **Not a Task**: a learning rate, a token budget, a seed, a thinking switch. Those are Runs (sweeps, repeats).

## 2. Run types, their bands and their order

A Run's number says its type, so a Task's Runs sort into the order they should run.

| band | type     | what it is                                                          | runs after   |
|------|----------|---------------------------------------------------------------------|--------------|
| r0x  | smoke    | a few steps end to end: proves venv, data, worker, result path       | nothing      |
| r1x  | main     | the full setting the Task exists for                                | its smoke    |
| r2x  | sweep    | one knob changed from the main Run (lr, budget, group size, thinking) | the main Run |
| r3x  | repeat   | the main Run again with a new seed: the spread a claim needs        | the main Run |
| r4x  | score    | a finished checkpoint scored again (another budget, the shared harness) | its training Run |
| r5x  | ablation | the main Run with one part removed (format reward, KL, critic)      | the main Run |

Older Runs keep their names (receipts use them); the bands apply to every new Run. A Task whose older Runs already
fill a band (LLMRec b01 j02 t02: r01-r57) numbers a new Run after its last one (r58), its type kept in `run_type`.

## 3. States, and how a card looks

| state       | mark | card                    | means                                              |
|-------------|------|-------------------------|----------------------------------------------------|
| completed   | ✅   | solid                   | ran and left a result                              |
| failed      | ❌   | solid, its cause shown  | ran and did not finish; `failure:` says why        |
| running     | 🔶   | solid                   | started, no final result yet                       |
| ready       | ⬜   | dashed                  | its ticket can run; nothing ran yet                |
| proposed    | ◌    | dashed, its purpose shown | an idea with a stub ticket that refuses to run   |

A proposed Task (its face says `state: ◌ proposed`) draws its step dashed too. A proposal never has a `result/`.

## 4. What a yes rests on: every proposal carries its plan

Asked 261019: "每次给我 propose，我得同意 … 但你得让我知道这每个 run 它都代表什么", and "你想在哪里 run？".

1. **aim**: what this Run produces, one line.
2. **why**: what decision or comparison needs it; why now and not later.
3. **settings**: the data and how much of it (rows, steps, epochs), the knobs that differ (lr, batch, budget, seed).
4. **host** and **time**: where it would run and how long; a measured time when a past Run gives one, else "about".
5. **after**: the Run it waits for, so the order is visible.
6. **Tasks in reading order**: number a Job's Tasks by what ran first, then cheapest to costliest, a Task after
   the one it depends on; renumber (with `renamed-from:`) rather than leave a proposal ahead of what ran.

A Task whose Runs carry a plan draws one wide card a row, so each Run reads whole.

## 5. The function

```bash
python scripts/propose_tree.py <job folder> --plan <plan.yaml>            # dry run: what it would make
python scripts/propose_tree.py <job folder> --plan <plan.yaml> --apply    # make the proposed Tasks and Runs
```

```yaml
tasks:
- name: t01_A-sft                    # an existing Task adds Runs; a new one gets a face marked ◌ proposed
  asks: "Does SFT on worked solutions lift strict accuracy?"
  develops: "a verl SFT checkpoint"
  reuse: "path/to/a worker to copy before it can run"     # optional; written into the stubs
  runs:
  - {type: smoke, slug: 20steps, says: "20 steps end to end", aim: "prove the pipeline", why: "find a crash in minutes",
     settings: {data: "first 320 rows", steps: 20, lr: 1e-5}, host: "a 24 GB card", time: "about 5 min"}
  - {type: main, slug: 1epoch, says: "one epoch, lr 1e-5"}
  - {type: sweep, slug: lr5e6, says: "lr 5e-6"}
```

It numbers each Run by its type's band (the next free number), sets `after:` to the Run it waits for, and writes
`run.yaml` (`status: proposed`, `run_type`, `says`, `after`) with a stub ticket that exits with what it still needs.
It never touches a Run that exists. Turning a proposal into a ready Run is writing its real ticket and config and
clearing `status:`; that is the Task owner's work (haipipe-task), not this drawing's.
