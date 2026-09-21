> Retained independent validation record. The evaluator used an isolated fixture at `/tmp/insight-forward-kmDMy9` while the source patch was being finalized. Earlier observations below are historical; the final compatibility retest records their resolution. Relative artifact names refer to that fixture directory.

# Fresh-context Insight behavior validation

Skill selected: `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/insight/haipipe-insight/SKILL.md` (observed metadata v1.6.0). I independently followed its Task and InsightBoard owner/reference routes. No evaluation report was consulted. All authored artifacts live beneath this fresh temporary directory; no repository or live-board files were changed.

## Result

The three requested workflows can be followed with the current skill. The Task CLI sequence completed allocation, delayed evidence freeze, immutable retry rejection and successor-version allocation. The board drafts preserve fixed question-rung identity and distinguish a historical signature from current Design eligibility. The extra static-codebook scenario is explicitly permitted by current GI2 rules. See routing-status-notes.md for the final three bounded Board requests.

## Executed evidence

- A and B are independent topic/data contexts on one Task-side board, represented by two Insight Pages. Both RI tickets point to the same unchanged reusable r01 ticket. No InsightBoard was created for the datasets.
- A's producer was actually executed during fixture setup, before Insight work, returning count=3 and sum=6. Its exact completed b01j01t01r01 Result was reused with zero new recipe calls.
- Both bind calls returned input:null; planned check succeeded. B remained allocated without a final input while its producer was absent.
- B's distinct native b01j01t01r02 Ticket invoked the same worker/recipe against its own frozen data/output, returning count=2 and sum=30. A supplied unknown flag was rejected (exit 2) before B created output.
- freeze created B's v001 input only after its native receipt completed, with explicit producer and consumer identities and exact hashes. The producer recipe, config and A Result/receipt hashes remained unchanged.
- Repeating A v001 freeze returned exit 1: `input is already frozen; use the next explicit version without rewriting it`.
- Later governed non-numeric context was frozen as A ri01@v002. Dataset A snapshot-02 allocated new ri02@v001 instead of retargeting ri01. Both saved v001 input hashes remained identical.
- Final checks: A `2 items; 3 executions; 0 findings`; B `1 items; 1 executions; 0 findings`.
- The actual handoff eligibility function returned `bindable: false`, `eligibility: unverified`, reason `no current handoff binding record` for a clearly fictional legacy-signature fixture. The actual pin validator rejected a changed current-source record. Passed owner receipts and real approvals were not manufactured.

Exact commands, exit codes, stdout and stderr are in command-transcript.md and commands.json. exercise_task.py and exercise_boards.py are the self-contained fixture drivers (rerunning them in this same directory is intentionally unsafe because immutable paths already exist).

## Drafts and remaining authority

`board-drafts/Synthetic-InsightBoard/0-MT-meta/MT02-question-information/MT02-question-information.md` preserves QI3 and its historical settled F cell, retires open B and non-final partial C with explicit reasons, and links `superseded-by: QK2`. MT03 allocates its next free QK2 with reciprocal `supersedes: QI3` and fresh open cells. The draft request does not answer the new question or transfer completion.

`handoff-explanation.md`, the Wisdom GI5 draft, Question GI6 draft, `workflow/handoff-draft.yaml` and `design-binding-draft.yaml` show the exact Page/dependency/receipt fields and owner sequence. The only current-eligibility execution is negative: a signature line is insufficient. No real person signature, passed Page CHECK, GI5/GI6, scientific finding or Design binding is asserted.

`local-codebook/gi2-explanation.md` and its pinned static-source input draft show GI2's zero-Supporting-Run branch. Local typed Evidence Result/verification and Page CHECK/CLOSE remain required; a raw hash alone does not satisfy GI2.

No DIKW Result/RF was published for either Task Page. Interpretation requires ready Page Evidence as owed by its make-items and independent review; those approvals/results were outside the setup-and-input-freeze exercise and were not fabricated. The item tables truthfully stop at frozen/planned.

## Observations found in the first pass (follow-up below)

1. **Executable validation gap:** `negative-reused-support/result.yaml` reproduces a successful freeze of a reused native `b01j01t01r03` support file whose own payload says `status: running`, with no completed native receipt, when `recipe_calls: []`. The current validator checks native reused Supporting Results only for qualified identity and path/hash; terminal receipt checking occurs in the recipe-call branch. This is narrower than the skill's claim that freeze validates completed supporting/local evidence. The workflow's owner acceptance rules remain correct, but callers must manually enforce readiness or strengthen this CLI contract.
2. **Wording ambiguity:** Data's introduction and Task Face still describe every observation through a producing Run. Its explicit Input and Gate/Closure sections, and workflow GI2, correctly allow governed static local sources with zero Supporting Runs. Following the more specific GI2 branch resolves the scenario, but introductory wording could be harmonized.
3. **Migration ambiguity:** page-v2-adapter.md says a human signature remains 'immediately binding'; the adjacent exact-current-eligibility section and handoff-record.md clearly require current dependencies, exact payload and owner GI5/GI6. Read the migration bullet as preserving the person-signature requirement, not waiving the newer current-use checks. Rephrasing would remove that ambiguity.

No additional contradiction was encountered in the successor-question, late-partition or bounded registration rules.

## Independent post-fix follow-up

Fresh allocation under `post-fix-reused-support/I01-reused-a` independently confirmed the receipt-readiness fix. With `recipe_calls: []`, missing Ticket/receipt pins now fail (exit 1), and a hash-valid receipt with status running fails (exit 1). Both failures leave input.yaml absent. The exact completed A Ticket/receipt passes freeze and check reports `1 items; 1 executions; 0 findings`. No producer was reexecuted; original saved inputs and producer artifacts retain their hashes. Exact additional commands/results are in `post-fix-reused-support/commands.json`; preservation/outcome assertions are in that directory's `outcome.yaml`.

The maintainer also corrected the identified Data introduction and signature-migration wording; those original wording observations are resolved by inspection.

A further read-only compatibility check found that the earlier valid, already-frozen v2 A inputs now report `2 items; 3 executions; 12 findings`: receipt checks are enabled by runtime.binding_sha256, which those pre-fix inputs already contain. They were not changed. This is a schema-contract compatibility concern if those saved v2 inputs are considered historical; an explicit receipt-contract marker/version can distinguish newly sealed envelopes from the old dialect. The maintainer has been notified.

## Final compatibility retest — all requested checks pass

The final frozen input now declares `evidence_contract: haipipe.insight-evidence/v1`; new freezes enforce producer Ticket/receipt pins, matching producer identity and completed status. Historical inputs without the marker retain their recorded dialect even when they contain binding_sha256.

Independent final commands confirmed original A `2 items; 3 executions; 0 findings`, original B `1 items; 1 executions; 0 findings`, earlier post-fix reuse `1 items; 1 executions; 0 findings`, and a fresh marked allocation `1 items; 1 executions; 0 findings`. The fresh allocation still rejects both missing and running receipts with exit 1 and no input file; the completed reuse then succeeds with the exact marker. All earlier frozen YAML and producer artifact hashes remain unchanged. Commands, exact outputs and final preservation results are in `post-contract-marker/command-transcript.md`, `commands.json`, and `outcome.yaml`.

The previously reported reused-readiness gap, backward-compatibility concern and two wording ambiguities are resolved for the exercised cases. No remaining blocking contradiction was observed. This validates structure/provenance and workflow behavior over synthetic data; it does not substitute for independent scientific interpretation review, Page Evidence acceptance or a person's handoff signature.

## Retained final outcome

```yaml
historical_A: 2 items; 3 executions; 0 findings
historical_B: 1 items; 1 executions; 0 findings
earlier_post_fix: 1 items; 1 executions; 0 findings
fresh_marked_reuse: 1 items; 1 executions; 0 findings
marker: haipipe.insight-evidence/v1
missing_receipt_fails_without_input: true
running_receipt_fails_without_input: true
all_prior_frozen_yaml_and_producer_files_unchanged: true
```

## Final routing notes

# Three bounded Board requests

| Request | Owners and countable work from supplied facts | Next action or missing record |
|---|---|---|
| Resume an existing paragraph-writing goal whose Evidence Result is accepted | Insight workflow resolves the existing cell and runtime; the rung owner owns semantics; Page workflow resumes the compatible native rp-para-NN_Pxx goal. The accepted Evidence Result is a reused native dependency. These facts establish no new Run count; resolve the existing Writing Ticket/runtime and accepted Evidence Run identity/receipt before inventorying each once. Controller pass and Page/GI checks add no Run. | Pin exact Evidence Result/version/hash and its acceptance receipt, then read the existing Writing Run's frozen goal, target, latest Version/Step and acceptance state. Resume the same Run for feedback within that goal; reopen its Version if its native closure rules require it. If the existing Ticket/receipt is missing, hold with that named gap. Do not allocate a wrapper Run or redo accepted evidence. |
| Register one neutral question only | Question owns neutral ask, next legal rung-prefixed id, eligible Queue cells and Outline registration receipt; Insight workflow indexes a control-only definition/runtime. Zero answer Runs and zero new native Runs follow from registration alone. | Resolve board/rung, origin/raiser, why-now, answerability, partition scope and blocked Aim; search for an existing equivalent question; write/reuse exactly one row and its open cells. requested_answer_targets: [], runs: []. Complete against registration acceptance, without requiring an answer or GI6. |
| Add an audience partition after sibling D/I/K are settled | Meta validates the audience and owns MT00 registration/config/group; Question adds eligible cells; each D/I/K/W owner keeps its evidence and findings; Insight workflow updates bounded definitions, dependencies and controls. Registration itself adds zero Runs. Existing D/I/K may be reused only by exact current Result/receipt, counted once if indexed. No number of new computation, evidence or writing Runs can be inferred until actual owners allocate Tickets/receipts for missing work. | Verify disjoint/stable, exogenous and addressable audience membership, same-extract scope and shared config/thresholds. Add the mirror group before X without renaming history. New eligible cells start open; refusals are not copied. Preserve sibling D/I/K. Reopen X contrast/heterogeneity/pooling verdict for the expanded partition set; hold every verdict-conditioned W including template F. Plan missing work and honor each owner release; changed handoff pins require a new person signature and new GI5/GI6. Missing audience filter/config/current membership evidence is a named blocker. |

These are routing/status notes, not fabricated runtime inventories or executed board changes.
