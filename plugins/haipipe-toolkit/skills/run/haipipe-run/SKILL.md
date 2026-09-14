---
name: haipipe-run
description: >-
  The neutral Level-4 Run contract shared by Execution, Discovery, Page, and Labeling
  work. Define, name, scaffold, execute, resume, count, or audit one logical Run as an
  authored Ticket paired with one generated Result and runtime receipt. Use
  when designing a workflow's Phase × Run Map or one phase's Run Profile, deciding whether work is a
  Run or an internal worker call, pairing runs/ with results/, resolving
  Folder-local versus Job-backed storage, or routing Execution, Discovery,
  Page Evidence Item, Page Paragraph Writing, Page Display, and domain-specific Labeling operations. Trigger: Run contract,
  Level 4 Run, run profile, run ticket, run result, runtime receipt, orphaned
  result, calibration run, qualification run, production scan, final audit,
  /haipipe-run.
metadata:
  version: "0.24.0"
  last_updated: "2026-09-13"
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

Load the Folder owner first: normally a workflow phase, or a declared canonical
family skill for a stable base Folder such as Task. Then load the current phase
that commissions the Run. The Folder owner owns kind, dialect, and cross-face
closure; the current phase owns why this attempt is needed, which Run kinds it
permits, and its acceptance/promotion rule. Load the selected worker/dialect
after this contract. Load `haipipe-plugin-runs` only to present the completed
structure inside Plugin Outline's Run Workspace; the presenter owns no Run
semantics.

## Ownership

Keep the four authorities separate:

```text
workflow phase       why to run · allowed kinds · target · acceptance · promotion
haipipe-run          identity · pairing · receipt · lifecycle · audit invariants
worker/dialect       how to perform the work · kind-specific Result grammar
haipipe-plugin-runs  read-only Run Workspace inside Plugin Outline
```

Do not create a horizontal `run-for-<folder-kind>` owner. Put the Run Profile
inside the workflow phase that owns that Folder kind. Reusable Execution,
Discovery, writing, display, or Labeling skills are workers, not Folder owners.

## What earns a Run

Mint a Run only when all four are true:

1. one bounded target can be named;
2. an authored Ticket can commission the work;
3. a generated Result can return a durable readout;
4. success or truthful non-success can be tested from disk.

Keep planning in `outline/`. A proposed section, unresolved item row, or human
decision alone is not a Run. A bounded human-feedback writing commission may
satisfy all four tests through saved feedback, candidate text and explicit
human acceptance; it follows the interactive Page dialect below. For evidence
work, a Paper workflow may reserve a proposed P/J/T/R
address during SURVEY so the future Run is indexable; the `new` action records
that no Ticket exists. Open and count the Run only when LAND commissions the
attempt and creates its authored Ticket.

A Page-owned `fn/Runs` candidate is also planning, not an allocated Run. It has
no identity, Ticket, Result, runtime receipt, or inventory row until the person
selects or directly commissions it. Do not mint `rpNN` before selection; resume
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
           local identity rp00_mermaid-structure or rpNN_pNN[-pNN]
           mandatory whole-Page Mermaid Structure, then one numbered paragraph group;
           Page owns human feedback, Version/Step history, working state,
           and explicit closure
Run E      Page-owned Evidence production
           one VALUE/TABLE/DISPLAY/CITE target; Ticket in runs/, Result in results/
Supporting Run
           external/upstream native family, including Discovery
           keeps its rNN / rlNN / bNNjNNtNNrNN / family-specific identity;
           the Page stores only a reference and consumes the Result contract
```

Page Evidence Items appear as Run E. External Execution, Discovery, Insight,
Design, Labeling, and other independently commissioned work appear as
Supporting Runs when an Evidence Result references them. Labeling uses `rlNN`;
ordinary local Task work may use `rNN`. New Run P records use only `rpNN`,
meaning Run of Page.
A human review or acceptance gate on code, search, data, build, or another Task
Result does not reclassify the producing work as a Page Run.
A Page workflow pass has no Level-4 Run identity merely because its
compatibility command uses the verb `run`.

One Page may therefore own many sibling Page Runs. The first is always
`rp00_mermaid-structure`; it must explicitly close the whole-Page Mermaid map
and `P01..PN` index before any paragraph Page Run exists. The Page then
partitions `N` numbered paragraphs into `K` independently closable groups,
where `1 <= K <= N`; ten paragraphs may yield 10, 8, or 6 paragraph Page Runs.
Every group has its own closure boundary and short `rpNN_pNN[-pNN]` identity.

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

## Phase × Run design law

Use one workflow-level table to join the semantic/control plane to the work
plane without collapsing them:

```text
Phase    owns why · order · authority · gate · promotion · handoff
Episode  groups related Runs inside a phase; has no extra Run identity
Run      owns one independently closable Ticket → Result attempt
Gate     authorizes or blocks a transition; is not a Run by itself
```

Every workflow that permits Runs must publish one **Phase × Run Map**. Use this
minimum schema and let each phase-owning skill supply the concrete cells:

| Phase | Folder / Episode | Phase purpose | Allowed Run operations | Cardinality | Gate / authority | Close / handoff |
|---|---|---|---|---:|---|---|
| `<P>` | `<kind or episode>` | `<why this phase exists>` | `<operation × multiplier>` | `<formula or none>` | `<named assertion/person>` | `<named receipt/output>` |

Apply these rules:

1. Write one row per workflow phase; split only when one phase truly owns
   distinct Folder kinds with different closure boundaries.
2. List independently closable operation kinds, not steps, calls, scripts,
   human ticks, or Result files.
3. Write `none` when a phase has no addressable Runs and do not scaffold empty
   Run lanes.
4. Keep symbolic cardinality (`N`, `K`, `S`, `sum(W_r)`) until the workflow
   freezes its actual scope. State the expected total formula below the table.
5. Derive actual inventory only from allocated Tickets plus valid runtime
   receipts. Never present the planned formula as work that already happened.
6. Do not mint an umbrella Run for a Phase or Episode when independently
   closable children are listed. Conversely, keep calls inside one Run when
   they share one target and one Result gate.
7. Treat a bare human approval/signature as a Gate. A bounded human-work
   commission may be a Run when it independently satisfies the four Run tests.

The map is an index, not a second authority. The workflow owns the complete
table; each phase's Task Face owns the matching detailed Run Profile; this
contract owns Run identity and counting. If those three disagree, stop with a
contract mismatch instead of guessing.

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
Design                   one generated DU or independently commissioned verification
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
Design's caller-owned YAML Ticket dialect and generate/verify gates are in
`../../application/haipipe-design-workflow/references/run-profile.md`;
the worker is `haipipe-design-unit`, not another Folder owner.
The owning phase supplies the target grammar and the worker/dialect supplies the
kind-specific Result gate. A phase may extend the vocabulary only when the new
family has an independently testable target and Result contract.

Name new Task Runs with the owning family's monotonic address and a
family-bearing stem. Name interactive Page Runs with the separate `rpNN`
counter (`rp` means Run of Page):

```text
r01_execution_fit-model
r02_discovery_chen2025_trace
r03_page-evidence-item_e01-value-adjusted-effect
r04_page-writing_c02-p01
r05_page-display_c02-f01
rl06_guideline-learn_round-03
rl07_executor-predict_test-v1-executor-a
rp00_mermaid-structure
rp01_p01
rp02_p02-p03
```

Use lowercase ASCII, digits, underscores, and hyphens. Never renumber. When
intent, target, frozen inputs, or acceptance semantics change materially,
allocate a new Run and record `supersedes:` rather than overwriting history.
The declared interactive Page dialect is the scoped exception: it allocates
from the Page Folder's own `rpNN` sequence, and evolving feedback advances
Steps/Versions rather than Run ids. The `rpNN` counter neither consumes nor
renumbers the Task Run `rNN` counter; `rp01` and `r01` may coexist.

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
Page local identity   rp00_mermaid-structure or rp01_p01
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
or `rpNN_…` Page stem only when the owning Folder's path is carried with it.
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
Run target           whole-Page Mermaid Structure, or one independently reviewable numbered paragraph group
authored Run         runs/rp00_mermaid-structure.md or runs/rpNN_pNN[-pNN].md
paired Result        results/<run>/working.md + runtime.yaml + vNNN.md
human Step           one ## Step sNNN section in vNNN.md, with feedback + result
accepted episode     ## Version closure in vNNN.md with explicit human decision
```

The Folder's dialect may place that Result elsewhere; record the resolved path.
A Version and Step are inner history, not extra L4 Runs or hierarchy levels.
Waiting for feedback is ordinary `waiting-for-feedback`, not a failed worker.
A human-accepted writing Version is not Page CHECK closure or evidence readiness.
The invariant tested on disk is scoped human agreement plus preserved history,
not a machine score that declares prose good.

Across the Page, `rp00_mermaid-structure` must close before independently closable
paragraph groups receive sibling Page Run identities. Each identity shows its
exact serial or range, such as `rp01_p01` or `rp02_p02-p03`; semantic wording
belongs in Goal. Inside one Page Run, sentences, Steps, Versions, and internal
agent calls do not receive child Run identities. Adjacent paragraphs share one
Run only when the human must judge them together under one acceptance decision.
These two forms are exhaustive. A differently named `interactive-writing` Run
is invalid, is not aliased, and cannot satisfy the structure prerequisite.

Feedback evolves the input on purpose. One Version is one append-only Markdown
journal containing every Step in order. Each Step freezes its reviewed source;
ordinary edits append a Step, reopening a closed episode adds a Version file, and a
new session resumes the same Run. New independent goals still require new Runs.
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
dialect. A phase may declare another Ticket extension or storage dialect only
when its Run Profile gives a deterministic Ticket-to-Result resolver.

Supporting projections are conditional:

```text
scripts/ · scripts/config/   reusable or per-Run implementation inputs
notebooks/                   generated execution record in dialects that own one
heavy external stores       declared artifacts represented by safe pointers
```

None of them creates another Run identity. Pair by logical RUNNAME, not by
assuming every projection exists.

## Phase-owned Run Profile

When a phase permits addressable Runs, add `### Run Profile` inside its Task
Face and state:

```text
ALLOWED      permitted family/operation values
TARGET       one target grammar and cardinality per operation
TICKET       physical dialect and who may author it
INPUTS       authoritative paths plus required versions/hashes
WORKER       skill, agent, CLI, API, or script allowed to execute
RESULT       required generated files and safe external pointers
ACCEPT       kind-specific test for status=complete
PROMOTION    how an accepted Result binds to evidence, Page, or handoff
REOPEN       which change requires a new Run, or a declared dialect's new Version
```

Select `haipipe-plugin-runs` when the Folder exposes these Runs. The plugin is a
surface, never a substitute for this phase-owned profile.

## Lifecycle

The delegated baseline is below. Interactive Page writing uses its declared
feedback wait/Step/Version loop instead of treating every turn as a new attempt.

Work one delegated Run in this order:

```text
PLAN          outline declares the owed target; Paper may reserve P/J/T/R; no Ticket or Run yet
ALLOCATE      choose the next RUNNAME; never reuse or renumber
SCAFFOLD      create the Ticket and runtime receipt; reserve the Result address
FREEZE        record authoritative inputs and versions before work starts
EXECUTE       invoke the declared worker only through the Ticket
MATERIALIZE   write only the declared Result and safe external pointers
VALIDATE      apply the worker/dialect Result gate
TERMINATE     complete · failed · blocked · superseded
BIND/PROMOTE  separate phase authority admits the Result into evidence/Page/handoff
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
family: page
operation: paragraph-writing
target: C2.P1
status: complete
ticket: runs/r03_page-writing_c02-p01.md
result: results/r03_page-writing_c02-p01/
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
Evidence   a Page/phase binding that admits a Result as support
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
only through its owning phase gate. Record the source RUNNAME at the binding or
promotion boundary.

The Run remains historical and immutable when an upstream input changes. Mark
the downstream binding stale, revise the Outline if necessary, and mint a new
Run. Never rewrite a completed Result to make the current Page look consistent.

## Audit one Run inventory

Audit in this order:

1. Resolve the Folder kind, owning phase, and its Run Profile.
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

- Let the workflow phase decide whether to commission, retry, bind, promote,
  reopen, or close; this skill owns none of those semantic decisions.
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
