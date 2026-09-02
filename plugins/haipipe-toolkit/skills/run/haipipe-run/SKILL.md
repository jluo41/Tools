---
name: haipipe-run
description: >-
  The neutral Level-4 Run contract shared by Execution, Discovery, Page, and Labeling
  work. Define, name, scaffold, execute, resume, count, or audit one logical Run as an
  authored Ticket paired with one generated Result and runtime receipt. Use
  when designing a workflow's Phase × Run Map or one phase's Run Profile, deciding whether work is a
  Run or an internal worker call, pairing runs/ with results/, resolving
  Folder-local versus Job-backed storage, or routing Execution, Discovery,
  Page Evidence Item, Page Division Writing, Page Display, and domain-specific Labeling operations. Trigger: Run contract,
  Level 4 Run, run profile, run ticket, run result, runtime receipt, orphaned
  result, calibration run, qualification run, production scan, final audit,
  /haipipe-run.
metadata:
  version: "0.5.0"
  last_updated: "2026-09-01"
---

# /haipipe-run · one attempt, two projections, one receipt

A Run is one durable, addressable attempt to satisfy one bounded target. It is
Level 4 beneath a Folder/Task, but it is not another folder level:

```text
Run address = authored Ticket identity = generated Result identity
```

Load the Folder's owning workflow phase first. The phase owns why this work is
needed, which Run kinds it permits, and what closes the Folder. Load the
selected worker/dialect after this contract. Load `haipipe-plugin-runs` only to
present the completed structure; the presenter owns no Run semantics.

## Ownership

Keep the four authorities separate:

```text
workflow phase       why to run · allowed kinds · target · acceptance · promotion
haipipe-run          identity · pairing · receipt · lifecycle · audit invariants
worker/dialect       how to perform the work · kind-specific Result grammar
haipipe-plugin-runs  read-only overview and Ticket/Result detail
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
decision is not yet a Run. Open the Run when the phase commissions an attempt
and allocates its address.

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
Page · Evidence Item     one focal VALUE/CITE/DISPLAY Result ready for EMBED
Page · Division Writing  one Content division candidate
Page · Display           one display unit candidate
Labeling                 a domain operation declared by subjective-label/ref/ref-run.md
```

The base classifies these families but does not define their semantic outputs.
The owning phase supplies the target grammar and the worker/dialect supplies the
kind-specific Result gate. A phase may extend the vocabulary only when the new
family has an independently testable target and Result contract.

Name new Runs with a monotonic two-digit address and a family-bearing stem:

```text
r01_execution_fit-model
r02_discovery_chen2025_trace
r03_page-evidence-item_e01-value-adjusted-effect
r04_page-division-writing_c02
r05_page-display_c02-f01
r06_labeling-guideline-learn_round-03
r07_labeling-executor-predict_test-v1-executor-a
```

Use lowercase ASCII, digits, underscores, and hyphens. Never renumber. When
intent, target, frozen inputs, or acceptance semantics change materially,
allocate a new Run and record `supersedes:` rather than overwriting history.

Use the local `rNN` stem for files and a full global reference when one Folder
refers to another Run:

```text
local identity   r04_execution_fit-model
global identity  b01j02t03r04
```

`reuse` and `rerun` references require the full `bNNjNNtNNrNN` identity.
`rerun` adds an attempt under the same Run identity because target, frozen
inputs, and acceptance are unchanged. If any changes materially, mint a new
Run and set `supersedes: bNNjNNtNNrNN` in its receipt.

## Two mandatory projections

Every Run has exactly one authored Ticket and one generated Result address.
Resolve their physical locations from the Folder dialect:

```text
FOLDER-LOCAL
  <folder>/runs/<RUNNAME>.sh
  <folder>/results/<RUNNAME>/

JOB-BACKED TASK
  <job>/<task>/runs/<RUNNAME>.sh
  <job>/results/<task>/<RUNNAME>/

LABELING JOB
  <job>/runs/<RUNNAME>.yaml
  <job>/results/<RUNNAME>/
  Result envelopes point to authority-owning domain artifacts resolved by
  subjective-label/ref/ref-run.md; they never copy protected artifacts.
```

The Result folder is the generated projection of the Run, never Level 5. Do not
copy or symlink a Job-owned Result into its Task Folder to imitate the local
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
REOPEN       which changed input invalidates the binding and requires a new Run
```

Select `haipipe-plugin-runs` when the Folder exposes these Runs. The plugin is a
surface, never a substitute for this phase-owned profile.

## Lifecycle

Work one Run in this order:

```text
PLAN          outline declares the owed target; no Run yet
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
replace it. Any material change mints a new RUNNAME.

## Runtime receipt

Every dialect keeps one machine-readable lifecycle receipt at the deterministic
path declared by its Run Profile, conventionally `runtime.yaml` in or beside
the paired Result projection. New Runs record at least:

```yaml
run: r03_page-division-writing_c02
family: page
operation: division-writing
target: C02
status: complete
ticket: runs/r03_page-division-writing_c02.sh
result: results/r03_page-division-writing_c02/
inputs:
  - path: outline/example-outline-v3.md
    sha256: <lowercase-hex>
worker:
  kind: skill
  name: haipipe-page-draft
started_at: "2026-09-01T12:00:00-04:00"
finished_at: "2026-09-01T12:08:00-04:00"
supersedes: null
failure: null
```

For `operation: evidence-item`, `inputs` is one frozen envelope. It may contain
zero-to-many Execution/Discovery Supporting Result pointers and hashes but
remains one local Run input. The local Run produces exactly one typed focal
Result; Page interpretation belongs to EMBED and is not part of this Run.

Add dialect-specific provenance such as subject identity, git SHA, config hash,
host, model, calls, or artifact pointers. Never store credentials, private
tokens, PHI, or raw sensitive rows.

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
interprets it. Division Writing may be promoted into one Content division;
Display may be promoted into the selected display lane. A Labeling Result may promote
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
- `../../board/page-plugins/haipipe-plugin-runs/SKILL.md`
- `../../../../subjective-label/ref/ref-run.md`
