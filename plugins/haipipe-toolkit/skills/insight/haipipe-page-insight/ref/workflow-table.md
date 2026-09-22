# Insight item workflow and tables

This task-side item workflow is owned by `haipipe-page-insight`.
`haipipe-insight-workflow` continues to own the InsightBoard Run workflow.
All steps operate inside one fixed Insight Page Folder. Page authoring uses
the shared Page workflow; execution uses `haipipe-run`.

## Activities and checkpoints

| Step | Unit / question | Reads | Produces | Checkpoint / next |
|---|---|---|---|---|
| Scope | Instance: what topic and data context? | Topic, dataset manifests | `workflow/insight.yaml`, Page scope | Scope resolves; plan items |
| Plan | Item: what independently answerable work? | Instance, prior items/Results | Question, target, expected Result, acceptance, dependencies | Reuse exact Result, resume, or commission a version |
| Bind | RI: which R and new dataset? | Item, normal R ticket, snapshots, recipe contracts | `riNN` YAML Ticket, immutable `v001/binding.yaml`, planned runtime; explicit upstream calls | Missing R, parameter support, or snapshot: hold this item |
| Evidence | Execution: are sources ready? | Supporting/local Evidence Runs | `freeze` seals `input.yaml` from ready supporting/local Results | `frozen` then `evidence` receipts |
| Reason | Item: what does evidence establish? | Frozen input and evidence | D/I/K/W/RF candidate, contradictions, limits | Independent CHECK receipt, `reasoned` |
| Publish | Item: what may others reuse? | Candidate and CHECK | Immutable Result/hash; accepted or reasoned non-answer | Accepted RF gets `published`; non-answer closes without RF |
| Synthesize | Page: what do completed items collectively say? | Exact accepted item Results | Current Page synthesis and RF index | Shared Page CHECK; open siblings visible |

“Breakpoint” means a resumable checkpoint receipt, not a debugger stop, new
Run, Page, or person-signature gate. Resume from the earliest unsatisfied
checkpoint after checking frozen inputs. Existing Page/Evidence human
decisions remain in force and are not replaced by these receipts.

## Workflow activities × Run ownership

Rows describe operations/checkpoints. Actual workflow nodes are the declared
owner-native Runs; a row or checkpoint alone never allocates one.

| Activity | Folder / scope | Purpose | Allowed Run operations | Cardinality | Gate / authority | Close |
|---|---|---|---|---|---|---|
| Scope / Plan | Insight instance | Declare context and intent | none | 0 | Owner resolves input and question | Planned items only |
| Bind / Evidence | Item dependencies | Obtain computations and typed evidence | Execution / Discovery / accepted Insight supports; local Page Evidence Item Runs | 0..N supports; one local Run per typed make-item | Producing Task and Page EVIDENCE contracts | Ready evidence |
| Reason / Publish | Insight Item | Produce its own DIKW Result | Insight · Item (`riNN`) | one RI per R+dataset binding; versioned immutable Results | Independent CHECK; accepted or truthful non-answer | Versioned Result |
| Synthesize | Same Page | Read settled items together | Page writing/display only when independently commissioned | 0..N as Page workflow requires | Page CHECK | Current synthesis |

Item tickets can orchestrate dependencies, which retain their own identities.
Count declared RI bindings and their execution versions separately. The base
R is referenced, not recounted or overwritten. Do not
add an episode Run whose only Result duplicates its children. A checkpoint,
LLM call, or rendering pass is not an additional item.

Item CHECK here is independent review of a frozen Result candidate, recorded
in its typed `review.yaml`. It is not the shared Page CHECK control, which still
checks the whole Page. Neither review creates a new Run unless independently
commissioned under an existing owner contract.

## Item table

One row per item, generated from intent + tickets + receipts:

| Insight Run | Base R | Question | Target | Dataset versions | Current execution | Checkpoint | Outcome | Last accepted / exact RF |
|---|---|---|---|---|---|---|---|---|
| ri01_description | r01_description | What patterns exist? | wisdom | patient-a@snapshot-01 | instance#ri01_description@v002 | evidence | running | v001 / RF1 |
| ri02_temporal-pattern | r02_temporal-pattern | What changes over time? | knowledge | patient-a@snapshot-01 | none | planned | not run | none |

This row grain is work, not a finding. Several RFs can come from one item
execution. The evidence table remains Evidence-Item-grained; the Board table
remains Page-Folder-grained. These three grains stay distinct.

## Closure and reopening

- New dataset or changed base R/question/target/acceptance: allocate a new RI;
  preserve the base R, old RI Results, and citations.
- Same RI binding, corrected or newly reviewed publication: allocate a new
  execution version; preserve the earlier publication.
- Same frozen contract failed: append retry history to that execution.
- New question in the topic: add an item; existing items do not reopen.
- New independent patient/context: new instance and RI, reused normal R/Task
  recipes, independent executions. No patient roster in the shared Task.
- Source used by several items changed: reopen their explicit bindings, then
  affected synthesis and consumers. Unrelated siblings remain current.
- Insufficient evidence: terminate with reason; do not manufacture a finding
  to reach the target. Closed work is not automatically accepted support.

Return instance, current item table, new exact Result references, held items
and reasons, and next runnable work. Page-changing responses additionally
follow the shared Page user-check packet.
