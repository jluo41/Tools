# Idea Block, Idea Job, evaluation Task

Read this before keeping new ideas or opening an idea's evaluation work.
The public entrypoint remains `hai-ideation` in `1_base/ideation/`.

## Ownership and storage

| Level | Owns | Does not imply |
|---|---|---|
| Block | One bounded direction and the index of admitted Idea Jobs | A paper already exists |
| Job | One candidate question, claim, identity, assessments and decisions | The idea will necessarily become a paper |
| Task | A bounded question or deliverable that develops/evaluates the idea | One Task for each skill invocation |
| Run | One commissioned assessment, with frozen inputs and a close rule | One Run for each tool call or human reply |

```text
<project>/paper/Idea-<Slug>/          an Idea Block sits in paper/, beside Paper- and Grant-
├── board.md                         board-kind: ideation-block
├── ideation.yaml                    pointer-only portfolio index
├── sNN-<topic>/                     shared reasoning/drawings when needed
├── trace/                           the work done on the Block (hai-trace)
└── j01_<idea>/
    ├── j01_<idea>.md                question, goal, Tasks, decision links
    ├── ideation.yaml                kind: ideation-unit; layout: idea-job
    ├── bundle/evidence-bundle.yaml  pointers to original evidence
    ├── cards/direction.yaml         this idea's bounded question and context
    ├── cards/iNN_<idea>.yaml         exactly one canonical Idea Card
    ├── cards/test-matrix.yaml       this idea's assessments
    ├── cards/venue-fit/             candidate target readings
    ├── workflow/                    semantic receipts, immutable decisions
    ├── projection/paper-ideation-sync.yaml
    ├── handoff/paper-ideation.yaml   after explicit selection
    └── t01_<assessment-question>/
        ├── t01_<assessment-question>.md
        ├── assessments/             authored review receipts, when produced
        └── runs/run-assess-<target>/ soft Run, when commissioned
            ├── run.yaml
            ├── run-assess-<target>.md
            └── passes/pNN-<MMDD>/
```

Create faces with `hai-block` and `hai-job`; load `hai-task` for a
Task's type and workflow, and `hai-run` before allocating a Run. Authored
idea assessments use `task-type: ideation`; read
[assessment-task.md](assessment-task.md). Use `new_board.py` with explicit
`--kind ideation-block`; the Block is `paper/Idea-<Slug>/` (JL 261124: "No more ideation theme"; an older
`ideation/bNN_<direction>/` Block still reads, its address `bNN.jNN`). Make folders only when
their first content exists. A newly admitted Job can have no Tasks yet.

Soft assessment Runs write reviews/receipts into their scope and reference
them from the Idea Card. A novelty or feasibility reading is an assessment,
not new scientific evidence. Actual computation uses a Work Task's hard Run;
source acquisition uses Discovery. Link the full owner Run/Result address.
An LLM experiment producing new measurements also belongs to Work. A local
assessment can use several skills as internal Steps. Changed inputs or close
rules follow the shared new-Run rule; retries on the same inputs are passes.

## Index and identity

The Block's `ideation.yaml` is an index, not a second semantic portfolio:

```yaml
version: 1
kind: ideation-block
direction: Robustness under distribution change
question: When do apparent gains survive a change in population?
scope: A bounded population, outcome and evidence window
ideas:
  - idea_id: i01
    job: j01_calibration
  - idea_id: i02
    job: j02_missingness
```

Each Job reuses the existing unit, Card, bundle, sync and receipt schemas.
Add these fields to its `ideation.yaml` (all the ordinary manifest fields
from [manifest-and-sync.md](manifest-and-sync.md) still apply):

```yaml
layout: idea-job
block: ../ideation.yaml
idea_id: i01
address: b01.j01
```

The Job's `direction`, `question`, `scope` and Direction Card describe that
idea's bounded context within the Block. They do not repeat the whole
candidate portfolio. Its sync source uses `ideation_job: b01.j01`; the legacy
`ideation_task` field is only for an existing Task portfolio. Each Job sync
contains its one Card. A Block comparison reads the Jobs' packets by pointer.

`iNN` is stable within its Block; `jNN` is an address. They need not match.
Allocate the next unused identity, including retained/eliminated candidates;
never renumber for ranking. The index has exactly one entry per Idea Job and
each Job has exactly one canonical Card. An alias is a Card field, not another
Card file. Job names and Task numbers do not encode skill or revision counts.

## Evaluation Tasks

Choose only questions needed for this idea; this is a menu, not a required
six-Task pipeline. Each Task face records its question, expected output,
input pointers, acceptance rule and applicable skills.

When only hypotheses exist, keep the Direction's observed signals and the
sync's opportunity map empty. Record the evidence gaps in `open_gaps` and
keep novelty/feasibility pending. Retaining a candidate does not establish an
evidence-backed opportunity or pass Test/Select.

| Question/deliverable | Methods | Durable outcome |
|---|---|---|
| What claim would distinguish this idea? | Generate, framing research questions | Falsifiable question, hypothesis, alternatives |
| What is already known? | Novelty check; Discovery for missing sources | Closest-work comparisons and bounded novelty delta |
| What could refute the claim? | Pressure test; optional adversarial review | Fatal assumptions, counterevidence and repair paths |
| What is the minimum informative experiment? | Pressure test; Work for actual pilot | Experiment design and linked pilot Result or reasoned waiver |
| What contribution and target fit the evidence? | Journal fit; Venue owner | Contribution, target options and current contract pointers |
| Is this ready to develop into a paper? | Test reconciliation, Select | Recommendation followed by the person's decision |

Generating more ideas at Block level creates more Jobs, not more Cards inside
one Job. Refining the same question updates that Job and its semantic revision.
A materially independent question becomes another Job with lineage links.

## Paper handoff

Keep the existing per-card scientific gates, exact target/category, accepted
risks and immutable human selection receipt. Advance `sync_revision` when the
scientific inputs or assessments change. Pin that revision in the selection
and handoff; a stale receipt cannot authorize a new handoff.

A new Idea Job can select while `paper_page.state: missing`, every Page
surface is `not-requested`, and `sync_status: stale` means no Paper projection
has consumed the packet. Scientific readiness comes from the Job's I2
artifacts. Do not claim any Paper surface current or create a dummy Page to
pass a gate. Legacy Task portfolios retain their existing projection gate.

By default each selected Idea Job routes to its own `Paper-<slug>` Block. The
selection's `story_route` includes `paper_block` and the future `story_path`
inside it; paths resolve from the Idea Job. The handoff's selected row carries
the same `paper_block`. Those paths are destinations, not evidence that they
have already been created. `hai-paper` creates/binds the Paper using its
scaffold, then `hai-paper-ideation` projects the source into `s01-ideation/`.

The Paper owner writes `ideation-origin.yaml` at the Paper root:

```yaml
version: 1
kind: paper-ideation-origin
sources:
  - idea_job: <SPACE-relative Job path>
    idea_id: i01
    selection: <SPACE-relative immutable selection snapshot>
    handoff: <SPACE-relative immutable handoff snapshot>
    sync_revision: 3
```

These pointers and the selected route are reciprocal. They confer no new
selection authority. On a repeated handoff, resolve them before allocating a
destination; reuse the bound Paper. Changed scientific inputs require another
assessment/decision, preserving the old snapshots. Paper versions remain Jobs
inside that Paper. Existing target-rebind rules stay with Story/Venue.

For a split, create child Idea Jobs, record `derived_from` pointers and obtain
their own decisions. For a merge, record all contributing Job/decision pointers
and the explicit decision to share one Paper; do not silently coalesce ideas.
Record lineage on the affected Card(s); keep old Jobs and decisions accessible.
The ordinary gate covers one Job's selection; a split/merge also needs review
of all affected sources and reciprocal links. Do not claim automation for it.

## Workbench map

| Surface | Reads |
|---|---|
| Block | `board.md`, Idea Job faces, index pointers |
| Job | Its question/Card, Task faces, evidence links, assessment/decision links |
| Task | Question, expected output, authored assessments and its Runs |
| Paper Idea | Source Job + selected revision; paper-specific framing |
| Trace | Prompts, plan and files of one piece of work (hai-trace); no replacement for a Job |

The existing generic workbench reads the normal faces, Jobs, Tasks and links.
This contract does not register a dedicated Ideation renderer or promise
YAML-specific controls. Put useful links on the faces, not only in YAML.
Future Idea screens follow `hai-ui/CONSTITUTION.md`: marks beside items,
decisions where they apply, no progress tallies or empty sections. Related
remains shared by Paper Idea and Story; Story by Section remains shared by
Story and Displays.

## Legacy portfolios and checks

Existing `bNN/jNN/tNN/ideation.yaml` units with several Cards remain readable
under their original contracts. Do not add `layout: idea-job` to bypass their
gates. Migration, when requested, starts with a path/identity map, preserves
the original immutable receipts, rewrites only current pointers with correct
relative bases, and verifies all destinations before adoption. Never silently
move folders, renumber Cards, or rewrite historical decisions.

For a new Block, run `scripts/check_idea_block.py <block>` for structure.
Add `--gate generate|sync|test|select|handoff` to run the existing scientific
gate for its Jobs, or `--job <jNN_slug>` for a particular Job. Other candidates
can remain provisional when one is selected. Run shared face/Task/Run checks
as appropriate. A structural pass alone is never a scientific gate.
