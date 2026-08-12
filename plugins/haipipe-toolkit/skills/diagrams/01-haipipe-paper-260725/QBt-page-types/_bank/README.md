# _bank — a simulated EXECUTOR tree

The QA-bank half of the twin naming law. The contract puts it plainly: one
conversation, two QAs. The QA-bank is the ORIGINAL and lives in the executor's
own tree at `tasks|discoveries/…/QA/<n>-<slug>.md`; the QA-probe is the
consumer's stub that points at it by `**target**:`.

Until 260807 this specimen had no bank at all. Both records carried
`route: task` while their `target` named a script sitting inside the probe's own
`.data/`, so the probe WAS the original and the twin law was stated on the page
and broken on disk. JL caught it by reading the binding.

## The shape, copied from a real one

```text
 🏦 _bank/                                the executor's tree · OUTSIDE the paper
    tasks/A01_page-type-contracts/        the task-GROUP
      A01_measure_paths/                  a task-FOLDER
        measure_artifact_paths.py         🏃 the run · scripts sit at its root
        configs/  runs/  results/         the shape /haipipe-task declares
      A02_measure_estate/
        measure_typed_pages.py
        configs/  runs/  results/
      QA/<n>-<slug>.md                    the QA-bank, at GROUP level
                                          `# Q —` is the Q-executor
                                          `## Answer` is the A-executor

 📥 QA-probe/QBt5-for-value/              the consumer's stubs · INSIDE the stage
      <n>-<slug>.md                       binding + digest only, target points up
      <n>-<slug>.data/counts.csv          the ONE extract, parsed FROM the bank
```

**THE SHAPE IS COPIED, NOT INVENTED.** A first cut put both runs in a made-up
`src/` directly under a folder named `T01_…`, which is neither level of the real
hierarchy. `/haipipe-task` declares `tasks/{G}{NN}_{name}/` for the task-GROUP
and `<name>/` holding `*.py`, `configs/`, `runs/`, `results/` for the
task-FOLDER below it, with `QA/` appearing only when `qa` is called.
`examples/Project-Personality-OpioidRx/tasks/A01_external-ndc/` is a real one on
disk: three task-folders and one group-level `QA/`, whose file opens
`# Q — <question>` with `state`, `started` and `by` lines and a `## Answer`.
Both the folder shape and the file shape were reproduced from it rather than
described from memory, which is the mistake the first cut made.

Why the tree is simulated rather than borrowed: an executor tree belongs to a
project, and this specimen has no project. `_fixture/` stands in for the paper
root the same way, and both carry a leading `_` so the board's page sweep never
walks them.

## What is NOT here yet

A `discoveries/` half. `/haipipe-discovery` is the other executor and its
folders answer OUTWARD questions, which is what `QBt4-for-literature` routes.
That page's two records still carry no bank, so the discovery side of this
simulation is owed rather than done.

**The bank is never copied into the paper.** Many QA-probes across many papers
may point at one QA-bank; that sharing lives here, at the bank, and never on a
page.
