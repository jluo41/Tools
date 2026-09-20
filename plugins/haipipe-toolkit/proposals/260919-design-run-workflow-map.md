# Proposal: Design Run workflow map — evidence use and reliable delivery

Date: 2026-09-19

Status: discussion draft. This is a proposed map, not a frozen executable
workflow. No live skills, Tickets, Results, source insights, UI, or versions
are changed. Proposed gates and routes below are **not implemented**.

Companion: [Design theories and method skills](260918-design-theory-and-method-skills.md).

## 1. Workflow Table

Keep three independently closable Run Specs. Strengthen their inputs, gates,
and recovery routes before adding more types. Design methods are internal
capabilities, not mandatory new Runs. Delivery is a projection, not a Run.

The existing Plugin roster remains **Goal Space, Design Space, Insight Space,
Run Space, Delivery Space**. Internal ids are `goal`, `design`, `insight`,
`runtime`, `delivery`; Space is the user-facing name.

| Run Spec | Goal Space | Design Space | Insight Space | Run Space | Delivery Space |
|---|---|---|---|---|---|
| **Commission** — release one bounded design request | READ: exact goal, audience, constraints | DECISION: release/hold the Item's frozen request | READ: decision-specific evidence assessment and gaps | READ: decision, actor, pins, route | — |
| **Generate** — produce the requested design | READ: released scope | ACTION: artifact(s), choices, assumptions, self-checks | READ: which insights influenced which choices; justified non-use | READ: method, inputs, outcome, next step | READ: exact artifact(s), only when Verify permits delivery |
| **Verify** — judge the exact design independently | READ: unchanged criteria and scope | REVIEW: artifact-level checks and substantive findings | READ: source-to-claim checks, applicability and remaining gaps | READ: verdict, findings, route, receipt | READ: exact passing review and remaining non-blocking limitations |

Rows are Run Specs, columns are Spaces, and cells present the same underlying
records. They do not create duplicate work or independent approval rules.
Commission's decision is collected in Design Space beside its Item. Goal and
Insight Spaces provide context; Run Space is always read-only.

```text
Prepare the Item: question + constraints + insight assessment + selected methods
(planning; no Run allocated merely for choosing a method)
                                |
                                v
Commission -- release --> Generate -- valid draft --> Verify -- pass --> CLOSE
    |                         ^                         |                 |
    | hold                    | design defect           |                 v
    v                         +-------------------------+         Delivery Space
   HOLD                                                 |       (same exact bytes)
                                                        |
                         incomplete review, unchanged inputs --> Verify

Generate or Verify discovers a necessary missing fact / changed authority:
  HOLD + named gap -> caller / Insight owner -> authorized new commission
  (external work is not silently dispatched; old Runs remain historical)
```

The agent-side HOLD and targeted recovery routes are proposed changes to the
current graph. Today it routes failed generation back to Generate and invalid
verification, including unresolved checks, back to Verify. That is inadequate
when the missing information cannot be produced by repeating either worker.

### Run Specs: bounded work and closure

All paths in this section are relative to the owning Design Folder. Every
allocated Run retains its own `runs/<rdNN_...>.yaml` Ticket and paired
`results/<same-stem>/runtime.yaml` receipt. A proposed assessment or decision
record is a deliverable inside that Run, not another Run identity.

| Spec / Type | Actor and target | Inputs / dependency | Gate and independently closable output | Planned cardinality |
|---|---|---|---|---|
| `commission` / `Design.commission` | Named human; one Item's exact request | Prepared Item, relevant Brief constraints, source manifest, assessment, selected method plan | **C:** durably record release or hold for the exact fingerprint; `decision.yaml` plus receipt | 1 released Commission per Item under the current identity policy |
| `generate` / `Design.generate` | Designer agent; one released single, sequence, or set | Released Commission; identical source versions; revision additionally pins base and feedback | **G:** required artifacts and all commissioned self-checks complete; immutable `result.yaml`, artifacts, checks, concise choice record, receipt; truthful non-success is preserved | N; allocate only justified attempts |
| `verify` / `Design.verify` | Fresh reviewer context; named immutable generation Result(s) | Exact Results/artifact hashes, released criteria, same source versions; depends on Generate | **V:** complete artifact × criterion review, source-use review and disposition of material findings; separate Result, checks, receipt; pass and fail are both legitimate completed reviews | J; allocate only required reviews/recoveries |

Entry is `commission`; terminal routes are `CLOSE` and `HOLD`. The evidence
assessment informs release but cannot impersonate the human decision. A release
authorizes generation; it does not certify insight truth or design success.

Expected allocated Run count for a released Item follows `1 + N + J`, not
three fixed executions. Before release it may be smaller. Methods, renders,
files, internal iterations, projections, and workflow episodes add no Runs.

### Gate C — what is being commissioned, on what grounds?

Before release, make the following inspectable:

- Bounded question, audience, context, required artifact shape/count, and
  acceptance rules. Resolve compound rules without dropping any clause.
- Exact relevant Brief/constraint versions and source versions. Record source
  authorization separately from relevance, scope, and strength of support.
- A decision-specific insight assessment: the finding, what it covers, what it
  does not cover, conflicts, material unknowns, and resulting recommendation.
- Selected design methods, evidence-access timing, permitted scope, and budget.
  Freeze required outputs/checks before seeing the candidate.
- Allowed claims: distinguish observations, interpretations, design hypotheses,
  craft choices, and anything requiring downstream testing.

Assessment recommendations, **not new runtime states or quality scores**:

| Assessment | Consequence before release |
|---|---|
| Sufficient for this use | Design within the finding's actual scope; record the inference from finding to choice |
| Enough for bounded exploration | Allow speculative alternatives with known facts/constraints intact; do not claim demonstrated benefit |
| Irrelevant to this decision | Explain non-use; proceed on an explicitly brief-only basis if appropriate |
| Missing, contradictory, or inapplicable on a necessary premise | Narrow the request or ask a specific question of the source owner; hold if the premise cannot safely remain unknown |

An insight can constrain, inspire, support, or challenge a choice. Merely
linking a signed page is insufficient. Equally, lack of measured evidence
does not prohibit all creative work. Sufficiency depends on the proposed use
and consequences of being wrong, not the number of citations.

### Gate G — produce both a design and a reviewable account of its choices

The Generate Result contains every commissioned artifact, not just the first
member of a set. For material choices, preserve a concise record:

`choice -> source finding/version OR craft/hypothesis -> relationship ->
applicability/inference -> uncertainty -> check or question`

This is an inspectable rationale, not a private reasoning transcript. An
unused insight may be irrelevant or deliberately challenged; give the reason
when it matters. Do not invent evidence after producing a preferred answer.

Generate must evaluate every commissioned criterion on the actual artifacts.
Deterministic checks support, but do not replace, semantic or visual checks.
An incomplete or failed self-check cannot be relabeled as independent review.

Delayed-exposure exploration is optional. Essential facts and constraints
remain visible. Use a genuinely unexposed context, preserve its first concept,
then reconcile with the authorized insights before verification. A model that
already read an insight cannot establish blindness by being told to forget it.
Reconciliation stays inside the same bounded Generate Run; changing its scope
or evidence authority does not.

### Gate V — check the design, not just the files

Use an actual fresh reviewer context and inspect exact generated bytes. Check:

1. Every artifact against every commissioned criterion, including all clauses
   of raw acceptance rules. Missing coverage never counts as pass.
2. Factual claims and source use: does the cited finding support this use, for
   this audience/context, with these changes? Mark unsupported extrapolation.
3. Design reasoning: does the artifact plausibly serve the stated purpose?
   Distinguish a reviewer's judgment from observed user behavior.
4. Material contradictions and adverse findings. A serious issue in review
   prose cannot coexist with an unqualified structured pass. Resolve it into
   a failed criterion, a named blocking gap, or a documented non-blocking issue.

Commission must explicitly require source-use and material-issue checks so
Verify does not invent a hidden rubric. If a genuinely new essential constraint
is discovered, record a scope/authority gap and return to the caller; do not
quietly alter the criteria to rescue or reject the output.

Passing means **ready for handoff under the stated criteria**, not proven
effective, clinically approved, shipped, or accepted by the downstream team.
No Adopt Run or extra adoption decision is introduced.

### Routes and bounded recovery

Each route belongs to its Run Spec; Space cells only project it. Route selection
must record the cause and exact evidence on the owning Run receipt.

| From / outcome | Destination | Required next action |
|---|---|---|
| Commission / released | `generate` | Allocate a Ticket with the released input versions |
| Commission / held | `HOLD` | Name the person/question needed; do not generate |
| Generate / valid draft and complete passing self-checks | `verify` | Allocate independent review of exact Results |
| Generate / repairable artifact defect | `generate` | New Generate with frozen base and actionable feedback, within authorized budget |
| Verify / complete pass, no blocking findings | `CLOSE` | Project exact artifacts plus review in Delivery Space |
| Verify / complete fail caused by artifact defect | `generate` | Revise artifact; preserve failed review and old artifact |
| Verify / recoverable incomplete review | `verify` | Reattempt only when reviewer/coverage can be repaired with unchanged authorized inputs |
| Generate or Verify / necessary evidence gap, source drift, changed scope, unrecoverable reviewer problem, or exhausted budget | `HOLD` | Preserve diagnostic receipt; name responsible owner and recovery condition |

Retry only with an actionable recovery and a bounded budget; repeated unresolved
review is not progress. The proposal requires a finite workflow-level recovery
budget agreed at release. The existing `max_iterations: 2` is an **internal
Generate budget**, not permission for unlimited Generate/Verify Runs. No new
global retry number is silently imposed by this draft.

Unchanged-input infrastructure retries preserve identity and append attempt
history. Changed artifacts require a new Generate and new Verify. Changed
scope, criteria, or evidence authority require renewed release, never in-place
re-pinning. Under today's one-release-per-Item rule, this means a new Item and
Commission; retaining one Item across multiple commissions would be a separate
identity-policy change, not a hidden behavior of this map.

A source owner request states the decision, exact unresolved premise, known
sources/conflict, and minimum evidence needed. It is not permission to run
analytics, edit/groom a board, sign a handoff, or recruit users. Authorized
upstream work retains its own native workflow and Run ids. Its returned source
version goes through the release boundary before Design consumes it.

## 2. Runs Overview

This proposal allocated no Runs and did not inventory the live board. Its
existing counts/statuses are **not assessed here**, not assumed to be zero.

The proposed Run Space lists receipt-backed instances with:

`Item | Run id | Run Spec/type | target | actor/context | method | status |
gate outcome | route + reason | exact Result | receipt`

Expand a row to see frozen inputs, criteria coverage, material findings, and
the specific next action. Link the same identities from Design and Insight
Spaces. Show history distinctly from the latest eligible handoff; never infer
that a later draft silently replaces a previously verified version.

Delivery Space shows all eligible Items and all commissioned members of each
Result, their Generate/Verify pointers and limitations. Failed or unverified
work stays inspectable in Design/Run Spaces but is not labeled delivery-ready.

## 3. Human Queue

No new human decision Run is allocated by this draft. In the future UI, derive
pending questions from actual owning Run receipts:

| Owning Run | Question shown | Authority boundary |
|---|---|---|
| Commission | Release this exact bounded request, or hold for this named gap? | Named human's version-bound decision |
| Blocked Generate/Verify | This premise/source/reviewer/budget prevents completion; who can resolve it? | Recovery request attached to the same Run, not an adoption step |

A change to the commission takes the renewed-release route above. A missing
insight can generate a request to its owner, but does not auto-authorize that
owner's work. Agent diagnostic HOLD and human Commission hold remain distinct
causes on their receipts even if the presentation groups both as waiting.

## 4. Skill Coverage

### Existing ownership skills

Paths below are relative to this proposal. Versions/line counts were read on
2026-09-19; they are inventory facts, not behavioral validation. Existing files
already have unrelated working-tree edits, which this proposal leaves intact.

| Skill / source | Role; cells | Observed version / lines | Static finding / proposed repair | Field-test for this map |
|---|---|---|---|---|
| [haipipe-design](../skills/design/haipipe-design/SKILL.md) | Contract; `commission@goal`, `generate@goal`, `verify@goal`, `generate@delivery`, `verify@delivery` | 0.4.0 / 301 | Owns Item and five Spaces; proposed expanded input freeze/assessment needs contract alignment | ? Not run |
| [haipipe-design-workflow](../skills/design/haipipe-design-workflow/SKILL.md) | Machine; `commission@design`, `commission@insight` | 0.4.0 / 190 | Three current Run types; agent HOLD and cause-specific recovery are missing from current routes | ? Not run |
| [haipipe-design-unit](../skills/design/haipipe-design-unit/SKILL.md) | Craft; `generate@design`, `generate@insight`, `verify@design`, `verify@insight` | 0.4.0 / 137 | Existing production/review worker; add explicit choice/source-use deliverables and remove stale adoption language | ? Not run |
| [haipipe-run](../skills/run/haipipe-run/SKILL.md) | Contract; `commission@runtime`, `generate@runtime`, `verify@runtime` | 0.26.1 / 689 | Preserves identity/receipt invariants; generic Design examples still mention retired Adopt | ? Not run |

These are semantic owner bindings, not new browser presenters. The existing
Design Plugin remains the presenter. The map is authored using
[workflow-table](../skills/0_utils/workflow-table/SKILL.md) (0.4.4) and
[haipipe-workflow](../skills/task/haipipe-workflow/SKILL.md) (0.3.1).
Their generic examples do not override the newer Design no-Adopt ruling.

### Proposed methods, not installed skills

| Proposed skill | Where used | Reviewable contribution |
|---|---|---|
| `haipipe-design-inquire` | Commission preparation; bounded source reading inside Generate | Decision-specific sufficiency, conflicts, missing questions |
| `haipipe-design-translate` | Generate | Finding-to-feature translation with limits and assumptions |
| `haipipe-design-reframe` | Preparation; Generate only within released scope | Alternative problem frames and implications; changed goals return to caller |
| `haipipe-design-explore` | Generate | Distinct concepts, their origins, unknowns, reconciliation with evidence |
| `haipipe-design-challenge` | Generate | Named assumption, coherent alternative, trade-off, distinguishing observation |
| `haipipe-design-prototype` | Generate | Inspectable prototype and actual observations; no implied user testing |

Start with the **inquire capability and Verify source-use checks** for reliability,
then pilot Translate/Explore/Challenge for different creative approaches. This
refines the companion proposal's creative-method-first pilot: method diversity
cannot repair an evidence boundary that nobody checks. Prototype and Reframe
can begin as procedures rather than separate installed skills if that is enough.

Verify remains the independent operation of `haipipe-design-unit`, not a seventh
persona. It must check the producer's work rather than inherit its conclusions.
All six method names remain proposals; none is a callable dependency of the
current runtime. Their eventual integration is unresolved, not declared valid.

## 5. Cell contract for implementation

This appendix makes all 15 cells explicit. It is a compact design specification,
not the normalized YAML declaration required before executable integration.

Conventions applying to every cell:

- Cell id is `<spec>@<space>`. Skill bindings are exactly those in Skill Coverage.
- Source cells bind that skill as owner and worker; projections bind the owner
  only, with an empty worker chain. Commission uses its human actor; its bound
  workflow skill records the decision, never substitutes for the human.
- Inputs/outputs are the subset named in the table, with full provenance to
  the owning Ticket or Result. No projection copies or edits authoritative bytes.
- Only source cells may create/release authority, at the paths below. All
  projections have `authority_change: none`. Gates C/G/V are owned by the Specs;
  cells collect, evaluate, or present them, never define a new Gate/Route.

| Cell id | Mode | Source/projection and shown object | Gate binding | Authority change |
|---|---|---|---|---|
| `commission@goal` | read-only | From `commission@design`: frozen goal/Brief constraints | present C | none |
| `commission@design` | decision | Source: request, assessment, human decision | collect C | release exact request; `results/<commission>/decision.yaml` |
| `commission@insight` | read-only | From `commission@design`: source pins, fit/gap assessment | present C | none |
| `commission@runtime` | read-only | From `commission@design`: same Ticket/decision/receipt | present C | none |
| `commission@delivery` | empty | none; no owner/worker, no inputs/outputs | none | none |
| `generate@goal` | read-only | From `generate@design`: released target/constraints | present G | none |
| `generate@design` | action | Source: frozen inputs -> artifacts/choice record/self-checks | evaluate G | create only paired `results/<generate>/` worker outputs |
| `generate@insight` | read-only | From `generate@design`: source use/non-use and questions | present G | none |
| `generate@runtime` | read-only | From `generate@design`: same Ticket/Result/receipt | present G | none |
| `generate@delivery` | read-only | From `generate@design`: exact artifacts, eligible only via V pass | present G; V controls eligibility | none |
| `verify@goal` | read-only | From `verify@design`: unchanged scope/rules | present V | none |
| `verify@design` | review | Source: pinned artifacts/inputs -> independent checks/findings | evaluate V | create only paired `results/<verify>/` worker outputs |
| `verify@insight` | read-only | From `verify@design`: applicability/claim checks and gaps | present V | none |
| `verify@runtime` | read-only | From `verify@design`: same Ticket/verdict/receipt | present V | none |
| `verify@delivery` | read-only | From `verify@design`: passing verdict bound to exact draft | present V | none |

The workflow caller alone allocates Tickets, records lifecycle/route receipts,
and binds Delivery eligibility. A worker's source cell owning its output does
not grant it control of `runtime.yaml` or the delivery state.

## 6. Validation cases before calling the workflow reliable

These are proposed tests, not passing test reports:

| Case | Expected behavior |
|---|---|
| Strong finding, matching population/context | Translate within scope; trace the design choices; verify the actual source claims |
| No relevant insight, bounded creative brief | Explicit brief-only/exploratory release allowed; no invented source or effect claim |
| Necessary premise missing or two sources conflict | Named question to owner and HOLD; no endless Verify loop |
| Source permits unchanged message, designer changes it | Changed design cannot inherit the measured effect; narrow its claims or renew its commission |
| Draft adds a visit-specific claim to an all-recipient message | Claim must be supported for the target audience or removed; a prose-only warning cannot coexist with clean pass |
| One acceptance rule has a length clause and a forbidden phrase | Both checks survive compilation and can independently fail |
| Source or Brief constraint changes after release | No silently refreshed hash; preserve history, stop current dispatch, seek renewed release |
| Generation Result is a set/sequence | Check and display every member; do not inspect or deliver only member one |
| Self-check passes, independent review finds substantive failure | Revise; never treat self-check or file validity as final authority |
| Review unavailable, repeatedly incomplete, or budget exhausted | Bounded recovery then explicit HOLD with owner/action |
| Method experiment uses delayed exposure | Fresh context and saved pre-exposure artifact; essential constraints remain visible |

### Next implementation boundary

First agree this map and its failure routes. Then align the existing contracts,
source freezing, criterion compilation, structured review findings, dispatcher,
and Space projections. Add only the methods needed for a bounded pilot.
Freeze a normalized declaration only after every binding, payload, budget,
route and recovery condition resolves and the behavior is field-tested.

Do not rename Spaces, move the skill family, add adoption, change Run ids,
rewrite historical Results, or start an Insight workflow as a side effect.
