<!-- Folded from the haipipe-labeling-building skill on 2026-10-07 (JL): the Building step order,
     its text kept, with its own name updated. Its law is ../SKILL.md. -->

# /haipipe-labeling-building · the Building step order

When a request says “two labels,” ask whether that means two class values for
one construct (one job, with both values in its schema) or two separate
constructs (one job per construct). Do not infer which they mean. Before using
a real corpus, do a scratch-workspace check with synthetic rows. There is no
non-writing `--dry-run` command: `corpus_preparation.py`, `fence_source.py`, and `job.py create` write
artifacts, while `job.py status` is read-only. For the scratch check, create a
temporary Page Markdown file in the temporary workspace because `create`
requires an existing Page file and writes `<page-folder>/labeling/` plus a
Run/Result. Remove the whole scratch workspace, including that Page and the
Run/Result, after checking `status`; do not put scratch artifacts in a real
Page folder.

Load `haipipe-labeling` (family), `haipipe-labeling-workflow` (the Run Spec
graph and Routes), and `haipipe-labeling-building` (semantic authority and restrictions)
first. **A Workflow is a list of Runs.** The operation names below are Run
Types used by the shared Workflow's Run Specs. This file gives their
Building-side order; each Run's internal Steps are in its view skill; the source Run Spec owns its
commission, actor, entry/exit gates, Route, and completion rule. P0-P2 are
compatibility capability tags only and do not create an independent frontier.

## Run allocation

Read `ref-run.md` before allocating. This machine may allocate:

```text
P0 (compat tag)  corpus-contract · definition-discussion · discovery-search* · guideline-seed
                 · test-reserve · embedding-build
P1 (compat tag)  round-prepare · weak-prelabel* · human-calibration · guideline-learn
    · round-measure · round-close
P2 (compat tag)  handoff-freeze
```

Write each Ticket to `<Page>/runs/<RUNNAME>.yaml` and its runtime/Result envelope to
`<Page>/results/<RUNNAME>/`, beside `labeling/`. Point the Result at the canonical domain files named
below; never copy them. One round folder is an episode, not a Run. While its
Card is merely proposed, it has no allocated `round-prepare` Run. Card release
commissions that operation; subsequent operations allocate only when their own
inputs freeze. Work exactly one non-parallel operation per dispatch.

## Steps and their view skills

Each Run's own steps live in the one skill of the workbench view that shows it
(JL 260929: one skill per view, never shared). This file keeps only the order.

```text
step  Run Type                     view                    skill
 1    corpus-contract          Data › Contract         haipipe-labeling-contract
 2    test-reserve*            Quality › Test          haipipe-labeling-test
 3    embedding-build*         Data › Embedding        haipipe-labeling-embedding
 4    discovery-search*        Labeling › Definition   haipipe-labeling-definition
 5    definition-discussion    Labeling › Definition   haipipe-labeling-definition
G0    Confirm meaning (a gate)     Labeling › Definition   haipipe-labeling-definition
 6    guideline-seed*          Labeling › Guideline    haipipe-labeling-guideline
 7    round-prepare            Labeling › Rounds       haipipe-labeling-rounds
 8    weak-prelabel*           Labeling › Rounds       haipipe-labeling-rounds
 9    human-calibration        Labeling › Rounds       haipipe-labeling-rounds
10    guideline-learn          Labeling › Guideline    haipipe-labeling-guideline
11    round-measure            Labeling › Rounds       haipipe-labeling-rounds
12    round-close              Labeling › Rounds       haipipe-labeling-rounds
13    handoff-freeze           Delivery › Handoff      haipipe-labeling-handoff
```

`*` optional. Steps 7 to 12 repeat for each round.

## Contract order · P0 compatibility tag

```text
pre-job      normalize, unitize, check, and reserve groups       → source-owned Corpus Preparation Runs
legacy      fence an already-unitized single-unit source        → engine/fence_source.py, no Run
first Run    import fenced corpus, initial policy, reservation  → corpus-contract
optional    the human settles each label's wording, in chat     → definition-discussion
optional    bounded external-evidence query, if commissioned   → discovery-search*
optional    revise the inspectable policy, if commissioned     → guideline-seed
optional    supersede the sealed frame under custody           → test-reserve
optional    embed one corpus × embedder, when commissioned      → embedding-build
entry gate  configured semantic authority explicitly attests → G0 evidence; no gate Run
```

At the Workflow Runtime level, record the human's G0 control in
`resource_controls`, referencing the completed `corpus-contract` Result and
the five authority files. The current engine persists the attestation and G0
receipt in `config.yaml` and `gates/g0/receipt.json`; these are storage details,
not a new Run or a reason to rewrite the closed Result. Optional discovery,
policy revision, and frame-supersession Specs may run only when separately
commissioned; they are not prerequisites when the contract Result already
contains valid initial policy and reservation artifacts. `embedding-build` is
also separately commissioned and may run once the P0 files pass integrity and
the job is not on HOLD; it does not depend on G0. Skip every uncommissioned
Spec. Discovery and embeddings are provenance, not gate inputs. A changed
corpus creates a new job; a materially changed query, seed,
reservation frame, or embedder receives a new Run only under the owner
contract.

## Round order · P1 compatibility tag

```text
CARD      round card proposed → a person releases it            card.md
PREPARE   pool → batch → evidence → prospect                     round-prepare
                                                                manifest.yaml · candidate_pool.jsonl
                                                                human_batch.jsonl · prelabels/<executor>.jsonl
PRELABEL  each weak executor, independently and sealed          weak-prelabel*
JUDGE     per item: show → first record → lock → reveal → final human-calibration
                                                                sessions/ (append-only events)
                                                                human_final.jsonl
LEARN     propose patches → backward impact → human ruling      guideline-learn · policy_draft/
MEASURE   metrics → coverage → risk                              round-measure
                                                                metrics.json · coverage.json · risk_ledger.jsonl
CLOSE     Checkpoint Keeper verifies → promotes → routes        round-close
                                                                checkpoint.json · README.md closed:
                                                                policy/versions/G_<t>/ · gold/cumulative.jsonl
                                                                register.md cells settled · view/
```

## Receipts this machine writes

```text
card.md released:        the person's release of the batch (before round-prepare)
<Page>/runs/<RUNNAME>.yaml   one authored operation Ticket, beside labeling/
<Page>/results/<RUNNAME>/    runtime.yaml + safe result.yaml for that operation
sessions/events.jsonl    item-level, append-only, numbered in sequence, the resume source
human_final.jsonl        one row per batch item, written when the last final lands
checkpoint.json          the round receipt; the only artifact that promotes gold and policy
README.md closed:        keeper · date · route
handoff/label-v1.yaml    the handoff-freeze Result, written once by the Label Handoff Keeper;
                         its Run exit predicate carries the G3 compatibility label
```

## Return

Return the current Run address or `none`, Run Spec/operation, round episode and its
`state:`, the open item if any, the files written this Run, actual allocated
Run count, register cells still open, checkpoint route, and exactly one next
runnable Run Spec or named human gate.
