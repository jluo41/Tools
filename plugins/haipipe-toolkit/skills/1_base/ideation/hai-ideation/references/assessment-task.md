# An authored Idea assessment Task

`task-type: ideation` routes to `hai-ideation`. Use it for an authored
evaluation or development question in an Idea Job: framing, novelty,
falsifiability, feasibility interpretation, contribution/target comparison or
decision preparation. This type uses shared soft Runs and assessment receipts.
It needs no model-training worker, generated LLM campaign or manuscript Page.

## Plan and build

Read the source Job's Card, bundle and current semantic revision. Choose one
bounded question and the methods it needs. Use `hai-job/scripts/new_job.py`
to create its Task slot:

```text
new_job.py task <idea-job> --slug prior_work --title "What distinguishes this claim?" --type ideation
```

Complete its face with the question as `goal`, an observable `close` rule,
source Card/revision, evidence pointers, applicable skills and planned output.
Link the face from the Job's Task list. No empty scripts/config tree is needed.
Create `assessments/` only with the first authored assessment. A formal Page
report, if separately requested, follows `hai-draft`; it is not required
just to retain the assessment.

## Assess and record

1. When a durable assessment is commissioned, use
   `hai-run/scripts/soft_run.py new <task> --type assess --target <target>
   --skill hai-ideation --agent <actor>`. The shared writer owns run.yaml.
2. Complete its Markdown Ticket with the exact Card revision, input pointers,
   bounded target, skills, evaluator/model build, criterion version and close
   rule. Multiple methods are Steps in this commission. Use the shared
   pass/receipt mechanism to record actual execution; do not claim a planned
   assessment complete.
3. Apply only the requested methods. Keep raw reviews and any disagreement.
   Write the appropriate specialist schema under `assessments/`; retain the
   full `assessment` binding with `mode: direct`, `owning_run: null`, plus
   `assessment_run` pointing to the soft Run. See [receipts.md](receipts.md).
4. Update the Job's Card and test-matrix pointers from the completed reading.
   New evidence/claims/assessments advance its semantic revision. A negative
   or unresolved assessment is an honest outcome, not a failed execution.
5. Request external evidence through Discovery or a scientific pilot through
   Work. Keep missing checks explicit. A model's confidence is not evidence.

Use the existing Run's next pass for a retry on the same frozen inputs; a
changed target/input/close rule follows `hai-run`'s new-Run rule. Every
Task retains its identity when methods or reviewers change. A human selection
remains the Job's immutable I3 receipt, not an automatic assessment label.

Return status, Job, Task, actual Run (or null), authored assessment paths,
missing evidence and next action. `result` here means authored outcome paths,
never a fabricated scientific `result/runtime.yaml`. A declared workflow must
use an existing applicable Run catalogue profile; if none fits, leave the
formal workflow unbound instead of inventing a registered profile.
