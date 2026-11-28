---
name: hai-design
description: "The one door for the design theme: a design Block, its Jobs, Tasks and Runs; owns the ladder contract and scaffold. Use to set up a Block, launch a Job or audit or update a Block. Trigger: design Block, launch a design Job, design ladder, update design block, /hai-design, /hai-design update."
metadata:
  version: "0.4.2"
  last_updated: "2026-11-27"
  folder_owner: canonical
  folder_kind: design
  primary_face: board
  page_ruling: domain-gate
  outline:
    mode: grammar
    source: "ref/design-ladder.md"
    shape: "goal signed → Job pinned → ② ideas → ③ ④ each design → ⑤ rank → release"
---

# /hai-design · the Design folder owner

Use Python 3.10+ with PyYAML. Run the commands from this skill's folder using the SPACE environment or
`uv run --python 3.13 --with pyyaml python`. Keep the version declared in metadata; a version change needs explicit user approval.

Read [ref/design-ladder.md](ref/design-ladder.md) before creating, naming or auditing a folder.
Read a routed helper's `SKILL.md` by path when it has `disable-model-invocation: true`.

## Blocks, Jobs and Tasks

```text
design/DesignMethodBook-〈topic〉/                 one channel's method collection
└── jNN_M0x-〈method〉/                           one method identity and its signed mK.md versions

design/Design-〈application〉/                    one application in one channel
└── jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM/        one signed goal × method version × inputs version
    ├── inputs/                                the Job's frozen reading fence
    ├── t00_reason-ideas/                       task-type: design-reason
    ├── tNN_dNN_〈design〉/                      task-type: design-item; one per idea
    └── t99_review-whole/                       task-type: design-whole
```

A Design Board execution Job and a Method Book method Job have different contracts. M01 and M02 are method
identities; mK is a version inside its method Job. The Method Book has no execution Task layer. A recipe's five
steps describe Board execution, not five Book Tasks. A new draft is another Run of the same design Task.

A Board names its Book with `method-book:`. Each execution Job pins one goal, method version and inputs version.
The method registry owns recipes; the Board owns application rules and inputs; a channel's venue pack owns its
channel rules. New inputs do not change a method. Move one clock per Job (`moved: start | method | inputs`).
Job groups use method family; Ideas, Designs and Review are Task groups. Groups do not define new Job or Task types.
See the ladder reference for the grouping fallback and exact naming fields.

## Route to the owner

| Request | Owner |
|---|---|
| Create or audit Block, Job or Task folders; allocate a Run; open designs | this skill, `scripts/design_ladder.py` |
| Signed goals, shared rules, inputs versions and the Job's fence | [hai-design-goal](../hai-design-goal/SKILL.md) |
| Register or pin a method, propose a version, record observed totals, score an experiment | [hai-design-method](../hai-design-method/SKILL.md) |
| Reason, generate, revise, verify or rank within the fence | [hai-design-unit](../hai-design-unit/SKILL.md) |
| Decide the next Run, enforce gates, project closed Results, close the Job | [hai-design-workflow](../hai-design-workflow/SKILL.md) |
| Freeze predictions and release signed designs into Block Delivery | [hai-design-delivery](../hai-design-delivery/SKILL.md) |
| Read the Block UI, embedded Main and selected Tasks | [workbench-design](../workbench-design/SKILL.md) |
| Block question and report | `hai-report` |
| Run card, passes, receipts and hard/soft lifecycle | `hai-run` |

The designer agent sets up and makes designs. The reviewer agent checks the fence, verifies, ranks and scores in
an independent context. A person signs goals, shared rules, method versions, release predictions and Job closure.
Routing or opening a page does not perform those signatures.

## Scaffold

Arguments in 〈brackets〉 are slots to fill before running a command.

```bash
python scripts/design_ladder.py block "design/Design-〈application〉" --title "〈application〉" --channel "〈channel〉"
python scripts/design_ladder.py book "design/DesignMethodBook-〈topic〉" --serves "design/Design-〈application〉"
python scripts/design_ladder.py method "design/DesignMethodBook-〈topic〉/j01_M01-goal-only" --version m2
python scripts/design_ladder.py job "design/Design-〈application〉/j03_〈goal〉_M02-overall-performance-m1_inputs-v2" --goal G01 --moved method
python scripts/design_ladder.py run "〈Block〉" add-job j03
```

The method version must exist in the registry; a person signs the Book's version before a Board Job can pin it.
`run-add-job-jNN` is a Block soft Run. It needs a signed goal, signed shared rules, a registered and signed method
version, frozen inputs, and a name matching those pins. The goal's `n` determines how many designs to keep;
`--n` may only confirm it. Job setup comprises `run-setup-goal`, `run-setup-method` and `run-setup-inputs`, all closed.
Before invoking the scaffold, the caller verifies the frozen manifest and hashes; an existing inputs directory
alone is insufficient. The goal's `name` must match the goal slug in the Job folder.

`run-open-designs-jNN` is a Job soft Run. Its first pass is the independent reviewer's fence check: every `from`
in t00's `chains.yaml` names a manifest file or exactly `own knowledge`. The pass's `fence-check.md` must say pass.
Then open one Task for every idea in `run-reason-t00/result/ideas.yaml`, using the idea's short name, and open t99.
Selection happens at ranking, not while opening ideas.

```bash
python scripts/design_ladder.py task "〈Job〉" d04 "〈idea-name〉"
python scripts/design_ladder.py task "〈Job〉" t99
python scripts/design_ladder.py run "〈owner folder〉" "〈run type〉" "〈target〉"
```

Run allocation checks the owner's level. Reason, generate, verify and rank are hard and own `result/`; revise is
soft and keeps passes. Verify names the draft it reads, `run-verify-dNN-vK`. The scaffold only writes missing files.
Freezing a Book method uses `method --version`; releasing designs belongs to `hai-design-delivery`.

## Audit and update

For `/hai-design update 〈Block〉`, inspect the actual Board, repository guidance, working tree and pins first.
`--check` in the conversational request means stop after audit and dry run:

```bash
python scripts/design_ladder.py audit "〈Block〉"
python scripts/design_ladder.py update "〈Block〉"
```

Review every proposed rename, text edit, link and Book addition. Stop on a held mapping or mismatching recorded
hash; do not guess a new pin. Preserve dirty work. Rehearse on a copy when the Block is untracked or otherwise
not recoverable. Apply only a confirmed concrete file plan:

```bash
python scripts/design_ladder.py update "〈Block〉" --apply
```

Re-run audit, verify recorded hashes and links, and open both owning Blocks. Report unsigned Book versions to the
person; an update never signs them. `scripts/design_update.py` is the implementation. Do not replace records by
hand or claim a clean audit when a check remains unresolved.

## Boundaries

- End at the person's release and close. Sending, allocation, experimentation and measurement belong downstream.
- Observed results return once per experiment at the Block as per-arm totals; no raw rows enter the fence.
- Do not edit closed hard Results, frozen inputs or released Jobs. A changed method or input version makes a new Job.
- Generated delivery comes from its owning writer. Preserve recorded hashes, manual drawings and source identity.
- User-facing entries open a Block; Jobs, Tasks and Runs remain selections inside it.
