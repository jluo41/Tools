---
name: hai-labeling
description: "The one door for subjective labeling: Building teaches and freezes what one human means by a vague trait; Scanning qualifies executors on a sealed test, scans and audits the corpus. Use to start, resume or check a labeling job. Trigger: subjective labeling, annotation job, /hai-labeling."
metadata:
  version: "0.13.0"
  last_updated: "2026-11-27"
---

# /hai-labeling · build the label, then scan under it

Resolve the owning Block and inspect the Job's records before routing work. The Block owns the page;
Jobs, Tasks and Runs are internal selections. Read `workbench` for the Block route and host rules.

## Block boundaries

| Block type | One Job binds | Task types | Output |
|---|---|---|---|
| Itemization | source snapshot and accepted recipe | `items` | immutable Items |
| Guideline Generation | Items, construct and human authority | `labeling-meaning`, `labeling-expression` | signed guideline and reference labels |
| Labeling at Scale | Items, signed release and executor configuration | `labeling-scanning`; independently authorized `eval` when needed | audited labels |

These are the approved work boundaries. Independent Job Type identifiers, Block writers and full shared-page
integration require implementation. Do not invent a `job-type` value or a completed execution from a design preview.
Task types are read from faces, not inferred from directory names. A `labeling-building` Task routes to Building;
a `labeling` record requires inspecting its bound artifacts to determine the responsible side. `data` is an accepted
Items alias. Ground-truth and external-score records keep their separately authorized custody.

Items describe/build/check/embed are operations within one Items Task. Guideline methods and rounds stay inside
Meaning/Expression. Test/Scan/Audit stay inside Scanning. Job topics group work; they are not Job types. No separate
Task topic layer is declared. Studio topics do not create Block or Task types.

## Start or resume

Resolve `TOOLS_ROOT` to the checkout containing `plugins/haipipe-toolkit`, and `PYTHON_BIN` to a supported workspace
interpreter. Keep work paths relative to the consuming SPACE, or use absolute paths.

1. Read the requested Job and its Task faces, accepted inputs, Run Tickets, results and human decisions.
2. Resolve the owning Block through real ancestry. Open that Block through `workbench`; choose the requested Job
   and Task inside it. Deliver only a verified Block URL. If the selector is missing, report the implementation
   gap and preserve the requested record identity; do not manufacture a child-page URL.
3. Derive the next operation from canonical records: `engine/items_task.py next` for Items,
   `engine/two_loops.py`'s `next_step` for Meaning/Expression, or the Building/Scanning order contract for those
   records. Open a waiting human decision before progressing to another operation.
4. Route Items to preparation, Meaning to interaction, Expression to expression, and execution to scanning.
   Read the sibling skill by path and follow its gates. Run only commissioned operations with their bound inputs.
5. Report what was produced or the exact required human action in the Block. Never sign for the person.

The requested selection and its data are read again for each prompt. User feedback belongs in the operation's
configuration or canonical interaction record; it is not a second source of approval.

## Architecture

```text
one human semantic authority
          │
          ▼
🏗 Label Building                                    🔍 Label Scanning
Contract → Round × N → Freeze ── Label Handoff ──▶ Test → Scan → Audit
  scope     calibrate   sign       G* + D_cal*      T*     D*     claim
```

The two sides answer different questions and therefore keep different write
authority:

```text
Building   "Is this what the human means?"        ends at a signed Label Handoff
Scanning   "Was that frozen meaning executed?"    ends at audited D*
```

Five layers, never mixed:

```text
LAW      hai-labeling-building · hai-labeling-scanning          who may decide, human gates, verbs, forbidden acts
ORDER    hai-labeling-building · hai-labeling-scanning   which Run comes next, allocation, receipts
VIEW     hai-labeling-<view> × 11                 one context skill per workbench view; a Run's own steps
CROSSING hai-labeling-workflow               Run Specs, dependencies, gates, Routes, handoff validity, invalidation
RUN      hai-run + ref-run.md                 Level-4 identity, Ticket/Result pairing, receipt, presentation
```

The Data views use `hai-labeling-preparation` for upstream raw-corpus work,
then `hai-labeling-contract` and `-embedding` for the Page-local job.
The eleven job view skills are `hai-labeling-contract` and `-embedding` (Data),
`-definition`, `-rounds` and `-guideline` (Labeling), `-test`, `-evaluation` and
`-audit` (Quality), and `-handoff`, `-scan` and `-final-labels` (Delivery). Route a
request about one Run to its view skill; no view skill is used by another view.
That Skill is one member of the Run Type's declared set, which
also includes shared workflow, domain, and procedure Skills; see
`../hai-labeling-building/ref/ref-space-mapping.md` §Run Type skills. The set describes
guidance, not proof that a Run loaded each Skill. A rule that fits
two layers goes in the door. P0-P5 and G0-G6 are stable
compatibility labels declared in `hai-labeling-workflow`; they are not
independent Workflow units, owners, or route authority.

## The crossing

The only legal crossing is one immutable Label Handoff. It binds:

- the corpus snapshot and target population;
- label, region, and uncertainty schemas;
- frozen policy `G*` and calibration gold `D_cal*` versions;
- the sealed-test manifest, its item count, and custody status, never protected ids;
- the human semantic authority and freeze signature;
- lineage, invalidation status, and creation receipt.

Scanning reads the handoff by version (for example `label-v1` and its date).
It never reads policy drafts as authority and never edits `G*` or `D_cal*`. A
semantic change returns to Building, mints a new lineage, and invalidates
affected scorecards, Runs, and claims.

Read `../hai-labeling-building/ref/ref-label-handoff.md` whenever creating, validating, or
consuming the crossing.

Read `../hai-labeling-building/ref/ref-run.md` whenever allocating, resuming, presenting, or
auditing a Labeling Run. It defines 26 independently closable operation kinds
across P0-P5. Round, Test, Scan, and Audit are grouping episodes, not extra
Runs. A human gate event is not a Run by itself; a bounded human-work operation
such as `human-calibration` or `audit-human-gold` may be one.

## Ownership

| owner | canonical artifacts | forbidden |
|---|---|---|
| shared job | corpus manifest/items, config, cache | assigning semantic gold |
| Building | policy versions, round units, Sessions, cumulative human gold, register, sealed-test reservation, Label Handoff | opening test text; production labeling |
| Scanning | released test gold, evaluation registry/predictions/scorecards, production runs, terminal labels, final audits, `D*` | revising human meaning silently |

Rendered `REPORT.md` and `.state.json` are views or caches. Closed artifacts and
their gate receipts win whenever a rendered view disagrees.

## Verbs and routing

```text
enter | status            resolve the job and derive both frontiers from disk
building | build | teach  forward to /hai-labeling building (law), which hands execution
                          to its ref/step-order.md (order)
scanning | scan           forward to /hai-labeling scanning (law), which hands execution
                          to its ref/step-order.md (order)
workflow | run | drive    forward to /hai-labeling workflow, which hands the
                          runnable side to its ORDER machine
one Run | one view        forward to that view's skill (/hai-labeling-<view>),
                          which holds the Run's own steps
raw corpus | preparation forward to /hai-labeling preparation before Contract
meaning | frame | report  forward to /hai-labeling interaction: a meaning Task's Frame, a loop's
| answers | update        Report, Preferences (save the answers) and Update
expression | round       forward to /hai-labeling expression: a round under a signed meaning
| rewrite | release       (Rewrite → Run → Evaluate), and Release
feedback | digest         use the existing family feedback procedures
```

`/hai-labeling <kind>` (and "forward to" above) means: read that kind's SKILL.md and follow it
with the remaining args. The kind skills are hidden from the skill listing
(`disable-model-invocation: true`), so this door reads them by path; a person can still
type `/hai-labeling-<kind>`.

```text
kind           read
workflow       ../hai-labeling-workflow/SKILL.md      gates G0-G6, the ORDER machine
building       ../hai-labeling-building/SKILL.md      the building law
scanning       ../hai-labeling-scanning/SKILL.md      the scanning law
preparation    ../1_data/hai-labeling-preparation/SKILL.md
contract       ../1_data/hai-labeling-contract/SKILL.md
embedding      ../1_data/hai-labeling-embedding/SKILL.md
definition     ../2_labeling/hai-labeling-definition/SKILL.md
guideline      ../2_labeling/hai-labeling-guideline/SKILL.md
rounds         ../2_labeling/hai-labeling-rounds/SKILL.md
interaction    ../2_labeling/hai-labeling-interaction/SKILL.md   the 🧭 meaning Task, step by step
expression     ../2_labeling/hai-labeling-expression/SKILL.md    the 🛠 expression Task, round by round
audit          ../3_quality/hai-labeling-audit/SKILL.md
evaluation     ../3_quality/hai-labeling-evaluation/SKILL.md
test           ../3_quality/hai-labeling-test/SKILL.md
final-labels   ../4_delivery/hai-labeling-final-labels/SKILL.md
handoff        ../4_delivery/hai-labeling-handoff/SKILL.md
scan           ../4_delivery/hai-labeling-scan/SKILL.md
```

No-argument behavior:

1. resolve the job;
2. read `../hai-labeling-workflow/SKILL.md` and derive the eligible Run frontier from canonical dependencies, routes and gate evidence;
3. dispatch the single next runnable action, allocating or resuming its exact
   Level-4 Run only when its Ticket contract is ready;
4. stop at a human gate or explicit `HOLD`.

Do not ask the user to choose among `pick`, `seal`, `judge`, `rules`, `measure`,
or `next`. Those are verbs inside one calibration round, not top-level phases.

## Core contract

One identified human is the semantic authority. Models may retrieve, prelabel,
diagnose, draft, and execute a frozen policy; they never create human gold by
consensus. Maintain:

- H/L/N terminal classes, with `NONE` meaning absence of evidence;
- H, L, N, HL, LN, HN, and HLN diagnostic regions;
- uncertainty and unresolved disposition separate from `NONE`;
- `D_cal*`, `G*`, sealed `T*`, executor scorecards, completed `D*`, and full
  provenance.

Read `../hai-labeling-building/ref/ref-contract.md` for authority and claim rules,
`../hai-labeling-building/ref/ref-assets.md` for canonical artifact locations, and
`../hai-labeling-building/ref/ref-run.md` for the Labeling Run dialect. Every `../hai-labeling-building/ref/`
path is relative to this skill's REAL folder inside the plugin; when the skill
was loaded through a symlink (`~/.claude/skills/...`), resolve it first.

## Implementation truth

Inspect actual engine capability before writing. A conceptual contract is not
evidence that sealing, checkpointing, evaluation, production, or auditing ran.
When a required keeper, writer, runner, or verifier is absent, return `HOLD`
with the missing capability, preserved Run frontier, responsible owner, and
next implementation action. Never emulate a missing Run, owner, or gate with
majority vote, inferred provenance, or placeholder receipts.
