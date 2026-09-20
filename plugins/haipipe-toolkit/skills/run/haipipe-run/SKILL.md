---
name: haipipe-run
description: >-
  The neutral Level-4 Run contract shared by Execution, Discovery, Page, and Labeling
  work. Define, name, scaffold, execute, resume, count, or audit one logical Run as an
  authored Ticket paired with one generated Result and runtime receipt. Use
  when designing a workflow's Run Spec graph or one Run Type/Profile, deciding
  whether work is a Run or an internal Step, pairing runs/ with results/, resolving
  Folder-local versus Job-backed storage, or routing Execution, Discovery,
  Page Evidence Item, Page Paragraph Writing, Page Display, and domain-specific Labeling operations. Trigger: Run contract,
  Level 4 Run, run profile, run ticket, run result, runtime receipt, orphaned
  result, calibration run, qualification run, production scan, final audit,
  /haipipe-run.
metadata:
  version: "0.26.1"
  last_updated: "2026-09-15"
---

# /haipipe-run · one attempt, two projections, one receipt

A Run is one durable, addressable attempt to satisfy one bounded target. It is
Level 4 beneath a Folder/Task, but it is not another folder level:

```text
Run address = authored Ticket identity = generated Result identity
```

The Insight instance dialect adds one explicit relation: `riNN` is an Insight
Run that points to a normal R ticket and freezes a new dataset binding. In that
dialect the equation is `full RI address = instance + riNN + execution
version`; the RI Ticket also carries the base R id/hash and dataset snapshot.
An unqualified R names only the reusable method, never the rebound dataset
execution. All other dialects retain their existing resolver.

Load the Folder owner and the Workflow that declares the Run Spec first. The
Folder owner owns kind, dialect, and cross-face closure. The Workflow owns the
directed graph, entry points, and terminal rules. The Run Spec owns why one
instance is commissioned, its target, actor, gates, routes, and cardinality.
Each Run Spec × Workspace Cell binds Skills, interaction, authority, and
projection behavior. Load the selected worker/dialect after this contract.
Load `haipipe-plugin-runs` only to present the same Run identity inside a
Runtime Workspace; the presenter owns no Run semantics.

The ontology is explicit: a Run Type is reusable vocabulary and owns inherited
defaults; a Run Spec is one bounded graph node; and a Run Instance is the
materialized execution. A Run Spec records its goal/target, actor,
action/interaction, optional inputs and dependencies, gates, optional route,
cardinality, Cell references, and internal Steps. Its entry gate may be omitted
and defaults open. Its exit gate may be inherited from the Run Type or declared
explicitly, but close semantics are mandatory. A route may be omitted only for
a terminal node, where it defaults to `CLOSE`; nonterminal routes are explicit.
The Run Instance owns the stable id, immutable `run_type` reference,
state/lifecycle, Result and receipt, and append-only attempt history.

Gate and Route modes are exactly `human | automatic | agent | hybrid`.
Workflow Definition owns the complete graph, entry rules, and terminal rules;
Workflow Execution materializes Run Instances from it. Workspace owns
presentation and interaction, not Run execution or ontology.

## Ownership

Keep these authorities separate:

```text
Workflow Definition  Run Spec graph · entry rules · terminal rules
Workflow Execution   materialized Run Instances · lifecycle projection
Plugin               member Workspace roster · stable Workspace ids
Run Type             reusable defaults · allowed action/result · close default
Run Spec             bounded node · goal/target · actor · action/interaction
                     · inputs/dependencies · gates/routes · cardinality · Steps
Cell                 Run Spec × Workspace · Skill/interaction/authority/projection
Run Instance         stable id · frozen run_type reference · state/lifecycle
                     · Result/receipt · attempt history
worker/dialect       execution method · kind-specific Result grammar
Workspace             presentation/interaction surface for the Run Instance
```

Do not create a horizontal `run-for-<folder-kind>` owner. Reusable Execution,
Discovery, writing, display, or Labeling skills are workers. A Workspace is a
presentation/interaction surface and never becomes the execution owner.

## What earns a Run

Mint a Run only when all six are true:

1. one bounded goal or target can be named;
2. a stable Run Type and independently addressable instance id exist;
3. an actor and one action or interaction are commissioned by a Ticket/Spec;
4. a close rule can settle success or truthful non-success;
5. the terminal outcome can be preserved in a durable receipt;
6. the Run can close independently of its caller's presentation surface.

Keep planning in `outline/`. A proposed section or unresolved item row is not
an allocated Run. A human decision is a decision Run only when it is bounded,
explicitly commissioned, durable through a decision Result/receipt, and
independently closable; it must also satisfy the six tests above. A click,
comment, approval tick, or feedback turn that does not satisfy those conditions
is an internal Gate or Step inside another Run.
A bounded human-feedback writing commission satisfies the tests through saved
feedback, candidate text, explicit human acceptance, and a close receipt; it
follows the interactive Page dialect below. For evidence
work, a Paper workflow may reserve a proposed P/J/T/R
address during SURVEY so the future Run is indexable; the `new` action records
that no Ticket exists. Open and count the Run only when LAND commissions the
attempt and creates its authored Ticket.

A Page-owned `fn/Runs` candidate is also planning, not an allocated Run. It has
no identity, Ticket, Result, runtime receipt, or inventory row until the person
selects or directly commissions it. Do not mint a typed RP identity before
selection; resume
an existing matching open Page Run instead of allocating a duplicate.

Do not confuse a workflow's `RUN` or `Execute` verb with this Level-4 identity.
A router invocation may plan, dispatch zero or many Runs, or only write a
workflow receipt. It earns a Level-4 Run address only when the Ticket, Result,
and runtime-receipt contract exists.

Treat scripts, tool calls, model calls, API requests, agent turns, retries, and
internal rounds as implementation details of one Run when they serve the same
target and Result contract. Split them into separate Runs only when their
targets or Results are independently reusable and independently closable.

A workflow episode may group several dependent Runs without becoming another
Run. Never count both an episode and its independently closable children.

## 📚 Page-facing projection

The neutral registry keeps native Run identities. Plugin Outline presents them
through three reader-facing lanes without renaming or copying the underlying
objects:

```text
Run P      family=page + operation=interactive-writing
           local identity rp-struct-NN, rp-sec-NN, or rp-para-NN_Pxx[-Pyy]
           rp-struct-01 is one whole-Page Structure Run for SHAPE + SURVEY;
           later Page Runs cover sections or numbered paragraph groups;
           Page owns human feedback, Version/Step history, working state,
           and explicit closure
Run E      Page-owned Evidence production
           one value, display, or citation Evidence Item; IDs are
           re-value-NN_<slug>, re-display-NN_<slug>, or re-cite-NN_<slug>;
           one Result/Card may expose zero-to-many `$V_xxx$`,
           `\\figure{D_xxx}` / `\\table{D_xxx}` / `\\algorithm{D_xxx}`, and
           `\\cite{C_xxx}` labels; labels are not Runs;
           Ticket in runs/, Result in results/
Supporting Run
           external/upstream native family, including Discovery
           keeps its rNN / rlNN / bNNjNNtNNrNN / family-specific identity;
           the Page stores only a reference and consumes the Result contract
```

Page Evidence Items appear as Run E. External Execution, Discovery, Insight,
Design, Labeling, and other independently commissioned work appear as
Supporting Runs when an Evidence Result references them. Labeling uses `rlNN`;
ordinary local Task work may use `rNN`. New Run P records use only typed
`rp-*` identities, meaning Run of Page.
A human review or acceptance gate on code, search, data, build, or another Task
Result does not reclassify the producing work as a Page Run.
A Page workflow pass has no Level-4 Run identity merely because its controller
command uses the verb `run`.

One Page may therefore own many sibling Page Runs. The first is always
`rp-struct-01`; its SHAPE and SURVEY cycles share one Ticket, one paired Result,
and may have several human participants. Record `participants` on the Run and
`contributors` on each Step; a new participant does not create a child Run.
Later structural passes use `rp-struct-02`, `rp-struct-03`, … only for a
genuinely independent post-closure goal. `rp-struct-01` must explicitly close
the whole-Page Mermaid map
and `P01..PN` index before any paragraph Page Run exists. The Page then
partitions `N` numbered paragraphs into `K` independently closable groups,
where `1 <= K <= N`; ten paragraphs may yield 10, 8, or 6 paragraph Page Runs.
Every group has its own closure boundary and short `rp-para-NN_Pxx[-Pyy]`
identity. Section-level writing uses the sibling `rp-sec-NN` sequence.

### Cross-face handoff

For a Task Folder, the Run boundary is a four-step transfer rather than shared
ownership:

```text
Page candidate (no Task identity)
  → Task owner allocates and executes native rNN
  → Task returns Result + runtime receipt
  → Page binds full Run id + Result path + fingerprint
```

The candidate never reserves an `rNN`. A ready Task Result does not close the
dependent Page Run or release the Page, and a closed Page Run does not prove
the Task Result current. Use
`../../task/haipipe-task/ref/task-page.md` for the Task-Folder closure equation
and staleness rules.

## Workflow Definition = directed Run Spec graph

There is no separate Phase authority layer:

```text
Workflow Definition = bounded Run Spec nodes + graph entry/terminal rules
                      + graph compiled from the Specs' directed Routes
Workflow Execution  = Run Instances materialized from those Specs

Run Spec = Run Type + bounded Goal/Target + actor + Action/Interaction
           + optional Inputs/Dependencies + Gate + optional Route
           + internal Steps + Cell references
Run Instance = stable id + frozen run_type reference + lifecycle + Result/Receipt
               + attempt history
```

A `phase()` or `controller` label is descriptive routing metadata only. It is
not a semantic owner, graph node, Run Type, Run Spec, Run Instance, Gate, Route,
or Workspace.

## Workflow Runtime boundary

One Workflow invocation may have one `workflow_runtime_id` when multiple Runs,
branching, resume, human HOLD, or aggregate audit needs a shared frontier. One
straightforward Run may rely on its own receipt. When present, the Runtime is
the aggregate record for status, frontier, and an index of Run-owned control
decisions; each child Run keeps its owner-native
Ticket, Result, gate/route record, and receipt. `workflow_runtime_id` is not an
`rNN`, `riNN`, `rp-*`, or
other Level-4 Run id. Load
`../../task/haipipe-workflow/ref/workflow-runtime.md` for the shared envelope
and adapter aliases.

Every executable Workflow publishes one Run Spec graph:

| Run Spec | Run Type | Goal / target | Actor | Action / interaction | Inputs / dependencies | Entry / exit gate | Optional route | Cardinality | Internal Steps | Cells |
|---|---|---|---|---|---|---|---|---:|---|---|
| `<spec-id>` | `<type>` | `<bounded goal/target>` | `<actor>` | `<work>` | `<optional>` | `<open/default + inherited/explicit exit>` | `<terminal only; default CLOSE>` | `<formula>` | `<internal>` | `<bindings>` |

Apply these laws:

1. One row is one independently closable Run Spec, never a Phase, Step, call,
   script, Result file, or display projection.
2. A Step is an internal action inside one Run. A Version is an immutable
   reopen episode for the same goal/target. Neither gets a Run identity.
3. Keep symbolic cardinality (`N`, `K`, `S`, `sum(W_r)`) in the definition.
   Count actual work only from allocated Run Instances and valid receipts.
4. Do not mint an umbrella Run when independently closable child Runs are the
   Workflow. Keep calls inside one Run when they share target and close rule.
5. Gate and Route are fields of the Run Spec/Instance. Their modes are exactly
   `human | automatic | agent | hybrid`; no other mode label is valid.
6. Entry gate is optional and defaults to `open`. Exit gate semantics are
   mandatory and may be inherited from the Run Type or declared explicitly. A
   route is optional only for a terminal node and then defaults to `CLOSE`; a
   nonterminal route must be an explicit graph edge.
7. Inputs, dependencies, and Result payload may be empty. Stable identity,
   Run Type, bounded target, actor, action/interaction, lifecycle state, close
   rule, terminal outcome, and durable receipt are not optional.

The graph is the Workflow authority. Run Types are reusable vocabulary; Run
Specs are planned nodes; Run Instances are runtime truth. If these disagree,
stop with a contract mismatch rather than inventing a Phase or controller to
reconcile them.

## Run family and target

Use one family classification for routing and presentation:

```text
Execution                computation · data · model · tool execution
Discovery                paper/source search and external-evidence analysis
Page · Evidence Item     one focal VALUE/TABLE/CITE/DISPLAY Result ready for EMBED
Page · Paragraph Writing  one addressed paragraph candidate
Page · Display           one display unit candidate
Labeling                 a domain operation declared by subjective-label/ref/ref-run.md
Insight · Item           one `riNN` binding from a normal R to new frozen data,
                         producing its own checked DIKW/RF Result
Design                   one Commission decision, one Generate Result, one
                         independent Verify, or one Adopt decision
```

Inside EVIDENCE/LAND, a DISPLAY-typed Evidence Item is still exactly one
`Page · Evidence Item` Run. Rendering calls are internal worker steps because
they share that item's target and Result contract. Use `Page · Display` only
when a display unit is commissioned as an independently closable target outside
an Evidence Item Run; never count both families for one unit.

The base classifies these families but does not define their semantic outputs.
For Page Paragraph Writing, load
`../../page/page-workflows/haipipe-page-content/ref/paragraph-run.md` for the
Markdown Ticket with embedded prompt, one-paragraph Result, and promotion
boundary. Historical `division-writing` Runs remain readable history; new
Content commissions use paragraph targets without renaming old artifacts.
Design's caller-owned YAML Ticket dialect and commission/generate/verify/adopt
gates are in
`../../application/haipipe-design-workflow/references/run-profile.md`;
the worker is `haipipe-design-unit`, not another Folder owner.
The Run Spec supplies the target grammar and the worker/dialect supplies the
kind-specific Result gate. A Workflow may extend the vocabulary only when the
new family has an independently testable target and Result contract.

Name new Task Runs with the owning family's monotonic address and a
family-bearing stem. Name interactive Page Runs with explicit typed local
identities (`rp` means Run of Page):

```text
r01_execution_fit-model
r02_discovery_chen2025_trace
r03_page-evidence-item_e01-value-adjusted-effect
r04_page-writing_c02-p01
r05_page-display_c02-f01
rl06_guideline-learn_round-03
rl07_executor-predict_test-v1-executor-a
rp-struct-01
rp-struct-02
rp-sec-01
rp-para-01_P01
rp-para-02_P02-P03
```

Use lowercase ASCII, digits, underscores, and hyphens. Never renumber. When
intent, target, frozen inputs, or acceptance semantics change materially,
allocate a new Run and record `supersedes:` rather than overwriting history.
The declared interactive Page dialect allocates independent monotonic
sequences for `rp-struct-NN`, `rp-sec-NN`, and `rp-para-NN_Pxx[-Pyy]`.
Evolving feedback advances Steps/Versions rather than Run ids. These typed
RP sequences neither consume nor renumber the Task Run `rNN` counter; an RP
identity and `r01` may coexist.

For Insight instance work, a new dataset allocates a new `riNN`; it never
becomes a rerun or later version of the old dataset. The RI points to the
unchanged normal R Ticket and owns an independent Result history. A retry of
the exact frozen RI contract appends an attempt; a corrected publication over
the unchanged binding may allocate the next execution version. A changed base
R, question, target, or acceptance allocates a new RI. `supersedes` never
relates independent patient datasets.

Use the owner-native stem for files and a full global reference when one Folder
refers to another Run:

```text
Task local identity   r04_execution_fit-model
Task global identity  b01j02t03r04
Page local identity   rp-struct-01 or rp-para-01_P01
```

A Paper Board has a separate local namespace because the Paper itself is the
fixed block. The current Paper-specific grammar is owned by
`../../paper/haipipe-paper/ref/run-naming.md`:

```text
Paper Main      pm-introduction-e01-cite-prescribing-variation-r01
Paper Appendix  pa-robustness-e01-value-sensitivity-r01
Paper Round     pr-rd01-misq-feedback-20260825-e01-cite-response-r01
```

The `p` namespace must never be rewritten as `b01`; doing so can collide with
an Execution or Discovery Run. A reserved Paper address is not counted as a
Run until its Ticket exists. The former `pjNNtNNrNN` form is a read-only
historical Paper dialect; new Paper work must not mint it.

`reuse` and `rerun` references require the full owner-native identity:
`bNNjNNtNNrNN` for a Job-backed Task or global Supporting Run, a
`pm-/pa-/pr-` id for a current Paper-local Run, and the local `rNN_…` Task stem
or `rp-struct-NN` / `rp-sec-NN` / `rp-para-NN_Pxx[-Pyy]` Page stem only when
the owning Folder's path is carried with it.
`rerun` adds an attempt under the same Run identity because target, frozen
inputs, and acceptance are unchanged. If any changes materially, mint a new
Run and set `supersedes: bNNjNNtNNrNN` in its receipt.

### Interactive Page writing dialect

Canonical profile:
`../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md`.
Load it before executing human-feedback Page writing.

```text
family / operation   page / interactive-writing
interaction          human-feedback
Run target           whole-Page SHAPE + SURVEY Structure, or one independently reviewable numbered paragraph group
authored Run         runs/rp-struct-NN.md, runs/rp-sec-NN.md, or
                     runs/rp-para-NN_Pxx[-Pyy].md
paired Result        results/<run>/working.md + runtime.yaml + vNNN.md
human Step           one ## Step sNNN section in vNNN.md, with feedback + result
accepted episode     ## Version closure in vNNN.md with explicit human decision
```

For RP, each fixed-scope Page-writing target is one persistent Run across its
interaction; feedback is a Step, never a new Run per turn. Reopening the same
goal/target creates a new Version inside that Run. A changed goal or target is
`NEW_RUN`. Acceptance is the Run's exit gate. The RP route vocabulary is:

```text
SELF          next Step in the same Run
NEW_VERSION   reopen the same goal/target in a new Version
CLOSE         close this Run / next Run in the Workflow
NEW_RUN       commission a new Run for a changed goal/target
```

The Folder's dialect may place that Result elsewhere; record the resolved path.
A Version and Step are inner history, not extra L4 Runs or hierarchy levels.
Waiting for feedback is ordinary `waiting-for-feedback`, not a failed worker.
A human-accepted writing Version is not Page CHECK closure or evidence readiness.
The invariant tested on disk is scoped human agreement plus preserved history,
not a machine score that declares prose good.

Across the Page, `rp-struct-01` must close before independently closable
paragraph groups receive sibling Page Run identities. Each identity shows its
exact serial or range, such as `rp-para-01_P01` or `rp-para-02_P02-P03`;
section-level writing uses `rp-sec-NN`; semantic wording
belongs in Goal. Inside one Page Run, sentences, Steps, Versions, and internal
agent calls do not receive child Run identities. Adjacent paragraphs share one
Run only when the human must judge them together under one acceptance decision.
These two forms are exhaustive. A differently named `interactive-writing` Run
is invalid, is not aliased, and cannot satisfy the structure prerequisite.

Feedback evolves the input on purpose. One Version is one append-only Markdown
journal containing every Step in order. Each Step freezes its reviewed source;
ordinary edits append a Step, reopening the same goal/target adds a Version
file, and a new session resumes the same Run. A changed goal or target is
`NEW_RUN`; new independent goals still require new Runs.
Closed records are immutable. Changes to accepted targets require explicit
scoped reopening. Never apply this exception to Execution/Discovery retries.

### Insight instance dialect

The task-side Insight contract owns this scoped dialect and its schemas at
`task/page-types/haipipe-page-insight/ref/instance-items.md`:

```text
base normal R          r01_description / runs/r01_description.sh
Insight Run Ticket     ri01_description / runs/ri01_description.yaml
full execution         sms/patient-a-study#ri01_description@v001
local Result           results/ri01_description/v001/result.yaml
runtime receipt        results/ri01_description/v001/runtime.yaml
frozen input           results/ri01_description/v001/input.yaml
```

One authored RI Ticket points to exactly one base R Ticket/hash and one frozen
dataset/question/target/acceptance binding. A different dataset or base R
allocates a sibling RI. Each RI version has exactly one frozen input envelope,
runtime receipt, and Result address; retrying unchanged inputs appends attempts
to that version. Cross-Folder references carry the full RI execution id,
base-R pointer, Result path, and hash. An `rNN` or BJTR address alone identifies
the method but cannot identify the rebound dataset. RI has its own monotonic
counter and does not consume or renumber the R, RP, RL, RD, or Paper counters.
Historical `instance#rNN@vNNN` Insight items remain readable but new bindings
use RI.

Instance-local supporting Execution tickets may call a shared Task recipe
under the same qualified identity scheme. Recipe definitions are not counted
as completed Runs. Their actual call owns one producing receipt; the Insight
Item owns a different DIKW Result. See the Insight `ref/task-calls.md` for
parameter binding, isolation, and legacy adapter checks. This does not grant
all existing launchers an unimplemented input override.

## Two mandatory projections

Every Run has exactly one authored Ticket and one generated Result address.
In the Insight dialect this statement is per full RI execution version: the RI
Ticket is reusable only within its immutable R+dataset binding, while each
qualified execution has one Result address. The referenced base R Ticket is
not a second projection of RI and is not recounted.
Resolve their physical locations from the Folder dialect:

```text
FOLDER-LOCAL
  <folder>/runs/<RUNNAME>.sh
  <folder>/results/<RUNNAME>/

JOB-BACKED TASK
  <job>/<task>/runs/<RUNNAME>.sh
  $OUTPUT_ROOT/results/<task>/<RUNNAME>/
  where $OUTPUT_ROOT is the Job in self-serving mode or the consumer-owned
  mirrored Job root selected by the Task's `store:`/launcher contract

LABELING JOB
  <job>/runs/<RUNNAME>.yaml
  <job>/results/<RUNNAME>/
  Result envelopes point to authority-owning domain artifacts resolved by
  subjective-label/ref/ref-run.md; they never copy protected artifacts.
```

The Result folder is the generated projection of the Run, never Level 5. Do not
copy or symlink a resolved Task Result into its Task Folder to imitate the local
dialect. A Run Spec may declare another Ticket extension or storage dialect only
when its Run Profile gives a deterministic Ticket-to-Result resolver.

Supporting projections are conditional:

```text
scripts/ · scripts/config/   reusable or per-Run implementation inputs
notebooks/                   generated execution record in dialects that own one
heavy external stores       declared artifacts represented by safe pointers
```

None of them creates another Run identity. Pair by logical RUNNAME, not by
assuming every projection exists.

## Run Type and Run Spec profile

Every Workflow node references a Run Type and materializes one or more Run
Instances. State:

```text
TYPE         stable Run Type key and inherited defaults
TARGET       bounded goal/target grammar and symbolic cardinality
ACTOR        human | automatic | agent | hybrid; named decision/execution owner
ACTION       one action or interaction boundary; Steps remain internal
INPUTS       optional authoritative paths plus required versions/hashes
DEPENDENCIES optional upstream Run Specs/Instances or governed prerequisites
STEPS        internal ordered actions; never child Run identities
TICKET       physical dialect and who may author it
WORKER       skill, agent, CLI, API, or script allowed to execute
CELLS        one coordinate per Plugin Workspace; each Cell binds Skill,
             interaction, authority, and projection behavior
RESULT       required terminal Result record; domain payload may be empty
GATE         optional/default-open entry; inherited or explicit exit; mandatory close semantics; mode: human | automatic | agent | hybrid
ROUTE        optional only for terminal/default CLOSE; otherwise explicit graph edge; mode: human | automatic | agent | hybrid
ACCEPT       kind-specific test for status=complete
PROMOTION    how an accepted Result binds to evidence, Page, or handoff
REOPEN       which change requires a new Run, or a declared dialect's new Version
RECEIPT      deterministic durable terminal outcome and append-only attempt history
```

Select `haipipe-plugin-runs` when the Folder exposes these Runs. The plugin is a
surface, never a substitute for this Run Spec profile.

## Lifecycle

The delegated baseline is below. Interactive Page writing uses its declared
feedback wait/Step/Version loop instead of treating every turn as a new attempt.

Work one delegated Run in this order:

```text
PLAN          Workflow declares the Run Spec; no instance exists yet
ALLOCATE      choose the next RUNNAME; never reuse or renumber
SCAFFOLD      create the Ticket and runtime receipt; reserve the Result address
FREEZE        record authoritative inputs and versions before work starts
EXECUTE       invoke the declared worker only through the Ticket
MATERIALIZE   write only the declared Result and safe external pointers
VALIDATE      apply the worker/dialect Result gate
TERMINATE     complete · failed · blocked · superseded
BIND/PROMOTE  a downstream Run or owning Folder authority admits the Result
```

Create the runtime receipt at SCAFFOLD with a planned state. Write identifying
facts before expensive work begins; a crashed Run is precisely the one that
must remain identifiable. Preserve failed and blocked Results as truthful
receipts.

Retry the same Run only when target, intent, frozen inputs, and acceptance
contract are unchanged. Append the attempt and failure trail; never silently
replace it. Any material change mints a new RUNNAME in this delegated baseline;
the interactive Page dialect explicitly permits feedback-driven Steps/Versions.

## Runtime receipt

Every dialect keeps one machine-readable lifecycle receipt at the deterministic
path declared by its Run Profile, conventionally `runtime.yaml` in or beside
the paired Result projection. New Runs record at least:

```yaml
run: r03_page-writing_c02-p01
run_type: Page.paragraph-writing
family: page
operation: paragraph-writing
target: C2.P1
actor: {mode: hybrid, name: page-writer-with-human-reviewer}
action: interactive-writing
status: complete
ticket: runs/r03_page-writing_c02-p01.md
result: results/r03_page-writing_c02-p01/
receipt: results/r03_page-writing_c02-p01/runtime.yaml
entry_gate: {mode: automatic, status: passed, rule: inputs-frozen}
exit_gate: {mode: human, status: passed, rule: scoped-text-accepted}
route: {mode: automatic, destination: CLOSE}
close_rule: scoped target accepted and every evidence obligation settled
terminal_outcome: accepted
attempt_history:
  - attempt: 1
    status: complete
inputs:
  - path: outline/example-outline-v3.md
    sha256: <lowercase-hex>
worker:
  kind: skill
  name: haipipe-page-content
started_at: "2026-09-01T12:00:00-04:00"
finished_at: "2026-09-01T12:08:00-04:00"
supersedes: null
failure: null
```

For `operation: evidence-item`, `inputs` is one frozen envelope. It may contain
zero-to-many Execution/Discovery/Insight Supporting Result pointers and hashes but
remains one local Run input. The local Run produces exactly one typed focal
Result; Page interpretation belongs to EMBED and is not part of this Run.

Add dialect-specific provenance such as subject identity, git SHA, config hash,
host, model, calls, or artifact pointers. Never store credentials, private
tokens, PHI, or raw sensitive rows.

For every newly allocated Run, `started_at` and `finished_at` are RFC 3339
date-times with an explicit UTC offset. A date-only value is readable legacy
history but cannot support within-day order or duration and must not be emitted
by a new writer. An atomic scaffold may use the same full timestamp for both
fields; monotonic Run identity, not timestamp precision, remains the address.

Use the owning dialect's detailed states on disk and normalize them for the
Runs surface without minting another state file:

```text
planned                         -> Ready
running                         -> Running
complete                        -> Done
failed                          -> Failed
blocked · unresolved            -> Held
superseded                      -> historical, not current
```

Only the kind-specific Result gate may write `complete`. A process exit code
alone is not completion.

## Result, evidence, and promotion

Keep three facts distinct:

```text
Result     what this Run generated
Evidence   a governed binding that admits a Result as support
Promotion  an accepted candidate written into an authority or handoff
```

A Result does not become evidence merely because it exists. Execution and
Discovery Results may support a Page Evidence Item; its one local Page ·
Evidence Item Result becomes Page evidence only when LAND binds it and EMBED
interprets it. Interactive writing may be adopted into its explicitly accepted
paragraph targets; the delegated Paragraph Writing profile promotes one
addressed Content paragraph. Feedback and accepted writing history are not
regenerable caches, even though their Result directory also contains projections.
For DISPLAY, the Page-owned display unit may be the renderer's direct output
destination; the governed Result envelope points to that unit and records its
hashes instead of first creating and then copying a duplicate payload. In a
consumer-serving canonical Task this PHI-safe admitted unit is the narrow
Page-authority exception to `$OUTPUT_ROOT`; `result.yaml` and `runtime.yaml`
remain in the resolved Result store. A Labeling Result may promote
closed policy/gold, a qualified route, a production candidate, or audited D*
only through its owning Run/Folder gate. Record the source RUNNAME at the binding or
promotion boundary.

The Run remains historical and immutable when an upstream input changes. Mark
the downstream binding stale, revise the Outline if necessary, and mint a new
Run. Never rewrite a completed Result to make the current Page look consistent.

## Audit one Run inventory

Audit in this order:

1. Resolve the Folder kind, Workflow, Run Spec, Run Type, and Run Profile.
2. Enumerate Tickets and Results using the declared dialect.
3. Report orphan Tickets, orphan Results, duplicate logical addresses, and stem
   mismatches.
4. Require a runtime receipt for every allocated Run, including planned,
   failed, blocked, and superseded Runs.
5. Verify family, operation, target, paths, frozen inputs, worker, timestamps,
   and status continuity.
6. Apply the selected worker/dialect Result gate before accepting `complete`.
7. Inspect evidence bindings and promotions separately; do not downgrade a
   valid Result merely because it has not yet been selected by a Page.

Report one row per logical Run. Put active and recovery-needed work first. Do
not present Results as separate Runs or count worker calls as Runs.

## Boundaries

- Let the Workflow graph and Run Spec decide whether to commission, route,
  retry, bind, promote, reopen, or close; this skill owns the invariants.
- Launch work only through the authored Ticket. Do not add a second browser or
  ad hoc execution door.
- Let the worker/dialect own concrete output grammar. Do not centralize paper
  Bib rules, model artifacts, prose rubrics, or display rendering here.
- Let `haipipe-plugin-runs` present the inventory read-only. Do not put surface
  layout or UI state into the Run contract.
- Keep heavy artifacts and sensitive data in their governed stores; record safe
  pointers in Results.

## Files

This skill intentionally contains only this contract and its UI metadata.
Existing specializations remain authoritative for their dialect details:

- `../../discovery/haipipe-discovery/ref/paper-run-contract.md`
- `../../task/haipipe-task/ref/hierarchy.md`
- `../../page/page-plugins/haipipe-plugin-runs/SKILL.md`
- `../../../../subjective-label/ref/ref-run.md`
