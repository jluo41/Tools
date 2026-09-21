# Ideation Workflow: Run Specs and owner bindings

A Workflow is a list of Runs; directed dependencies and routes form its graph.
I1/I2/I3 name capability groups. They are neither Run identities nor graph
nodes. Read `../../../run/haipipe-run/SKILL.md` before commissioning a
durable episode, and load each selected Folder owner.

## Run Spec list

This definition reuses Discovery and Task Run families. It creates no local
Ideation execution bank. Before allocation, replace the symbolic targets and
counts below with the bounded questions, frozen inputs, owner folders, actors,
and acceptance rules for this commission.

| Run Spec | Run Type / owner | Bounded target and actor | Inputs / dependencies | Action and internal Steps | Exit gate / Result | Directed route / cardinality |
|---|---|---|---|---|---|---|
| source(subject) | Discovery / owning Discovery Folder | Agent analyzes one canonical source needed for a named claim or official venue fact | Frozen search question; source identity; existing Results first | Search/admit/read/verify using Discovery workers; individual queries and model calls are Steps | Agent gate: verified same-stem Result/Bib/runtime, or truthful inaccessible/insufficient outcome | Accepted Result → portfolio; unavailable → portfolio with HOLD; N missing independently reusable Subjects |
| pilot(question) | Execution / owning Task Folder | Agent answers one bounded minimum-experiment question | Frozen design, data and acceptance rule; relevant source Results | Execute the pilot and classify its outcome; tools/retries are Steps | Agent gate: Task Result/runtime answering the question as positive/negative, or truthful non-success | Result → portfolio; blocked → portfolio with HOLD; K authorized missing pilot questions |
| portfolio(snapshot) | Execution / owning Task Folder | Agent reconciles one direction/evidence snapshot to the requested Ideation deliverable; the named person owns any selection interaction | Direction and admitted card ids; exact existing/new source and pilot Results; current Venue contracts as needed | I1 generation/admission, I2 specialist readings/reconciliation, and requested I3 comparison/decision recording are internal Steps. Stage-specific commissions use only their requested Steps | Hybrid gate for selection: explicit per-card human answer plus mechanical gates, or a durable defer/HOLD outcome. Agent gate for generation/testing only: requested artifact gate or truthful non-success. Task Result indexes semantic artifacts, frozen input hashes and receipts; it does not copy source evidence | CLOSE on the commissioned deliverable or truthful non-success; missing evidence routes to the named source/pilot Specs and resumes under owner rules; one per independently closable direction/snapshot commission |

The portfolio Run uses the existing Execution family (model/tool work), the
Task owner's authored Ticket and same-stem Result/runtime grammar. The Task
Folder is the execution owner; the Ideation direction folder keeps semantic
cards and decision receipts. They may be sibling folders. A Task Run never
acquires authority to choose on the person's behalf.

`N` and `K` count independently commissioned missing targets, not queries,
papers mentioned, or candidate count. Reuse exact owner Results whenever
possible. The portfolio Spec may consume only existing Results, so N=K=0 is
valid. A semantic snapshot already produced by another commissioned Run is
reused rather than wrapped in another Run.

## Entry, closure, and recovery

- Entry: freeze the requested output (generate, test, compare/select), direction,
  scope, evidence revision, Folder owner, actor and close rule. Merely opening
  this skill allocates no Run. An inline answer, audit, or projection-only
  invocation can commission zero Runs and return a workflow/adapter receipt.
- Bind each Spec to its owner-native full Run address and Ticket after explicit
  commission. The Ticket freezes `run_type`, target, inputs, worker skills,
  `gate.mode`, `route.mode`, close rule and Result location. Use only
  `human | automatic | agent | hybrid` for gate/route modes.
- For every novelty, pressure, or Fit assessment Step, the Task Ticket freezes
  an `assessment_id`, evaluator (person/agent and exact model/build), criterion
  owner plus rubric id/version, subject Card hash, and sorted input-manifest
  hash. The Task Result indexes those exact values and its assessment receipt
  path/hash. A durable specialist receipt records the full owning Run address
  and `assessment_id`, then inherits the rest from that Result as specified in
  `receipts.md`; it does not create a child Run. A direct/one-off specialist
  call has no owning Run and carries the complete binding inline or in its own
  retained receipt.
- If multiple reviewers assess the same frozen input, preserve each raw
  receipt and add a resolution receipt. Agreement, a named evidence-based
  resolution, or an `undetermined`/HOLD route must be explicit. Do not resolve
  by overwriting, averaging, or creating another Run for the arbitration.
- A missing evidence target routes to source/pilot work only within the
  authorized request. Otherwise preserve HOLD and the named missing input.
  No response to a selection question remains open; it is not a human defer.
  A bounded comparison-only commission can close with advice and no selection.
- Changes to the goal, evidence snapshot or acceptance rule follow the shared
  new-Run/supersedes rule. A retry on unchanged frozen inputs appends an attempt.
  Pending human interaction resumes the matching open commission; do not mint
  a Run for each reply.
- The Task Result links the Ideation artifact versions and human receipt, when
  present. It reports success or truthful non-success independently of the P0
  Page. Human selection and the Task runtime receipt have different purposes:
  only the former authorizes selected Idea-target-Story pairs.
- The owning Workflow Runtime, when needed, indexes these Runs and their routes;
  it is not another Run. Workspace Cells bind the appropriate Ideation worker
  and artifact view to the same Run identity.

## Capability and adapter mapping

| Activity | Placement |
|---|---|
| Generate lenses, dedupe, card edits, comparison order | Internal portfolio Steps; provisional inline preparation can precede commission |
| Novelty comparisons, pressure assessment, broad/deep venue fit, Nature lenses | Internal portfolio Steps using owner evidence; each remains directly callable |
| New source analysis / new computation | Independently closable source / pilot Run in the owning Folder |
| Human candidate/target decision | Internal human interaction/gate of the commissioned portfolio Run; the I3 receipt persists the answer |
| Matrix aggregation, source-pointer maintenance, semantic sync | Internal Steps or router bookkeeping; no separate Run |
| P0 working projection, Page dispatch receipt | Paper/Page adapter operation; no new Run solely for sync |
| Separately requested bounded Page writing/feedback | Page-owned Run only under its own Ticket/Result/closure contract |

Do not count both the portfolio episode and its independently commissioned
source/pilot children for the same Result: each of the three Spec families
above has a different bounded output. The portfolio Result is the semantic
reconciliation/decision outcome, not another copy of any source/pilot Result.
Existing `stage` fields remain capability metadata; Page serialized `phase`
fields remain dispatch metadata. They never supply a missing Run identity.
