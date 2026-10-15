---
name: haipipe-labeling
description: >-
  The one user-facing door for a human-grounded subjective-labeling theme with
  two sides: Label Building teaches and freezes what one identified human means
  by a vague trait; Label Scanning qualifies executors against a sealed
  human-gold test, scans the corpus under the frozen meaning, and audits the
  completed labels. Use for starting, resuming, routing, or checking a
  subjective annotation job; defining H/L/N and boundary regions; calibration
  rounds; guideline freeze; executor evaluation; corpus scanning; final audit;
  or /haipipe-labeling (named subjective-label until 2026-10-07). Called with
  a labeling Job folder, it opens the workbench on the step the Job is at and
  guides the person through it, one step at a time, from the items Task on.
metadata:
  version: "0.11.1"
  last_updated: "2026-10-14"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-labeling · build the label, then scan under it

This is the only user-facing door. Resolve one Level-3 job as one corpus
snapshot plus one target trait and one identified human semantic authority,
inspect its artifacts, and route to the owning sibling door.
Do not expose internal round actions as a menu of lifecycle phases.

Before running an engine command, resolve the tools checkout that contains
`plugins/haipipe-toolkit/skills/2_theme/labeling` and set `TOOLS_ROOT` to that directory. Use `.` when
working in the tools checkout, or the consuming workspace's `Tools` link when
it has one. A Page path and a source path remain relative to the current
workspace (or may be absolute); do not assume the tools checkout is the
current directory. Set `PYTHON_BIN` to that workspace's Python interpreter
(for example `.venv/bin/python`, or `python3` when no project venv is used).

## Start from a Job: `/haipipe-labeling <Job folder>`

The person's one start message (JL 261014: "from /haipipe-labeling <path to job> and it will open the UI for me,
and guide me step by step"). A labeling Job is one dataset × one label; its Tasks are typed by their faces'
`task-type:` lines (items · ground truth · building · scanning · score), and the work goes items → building → scanning.

1. **Open and read.** Run `"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling/scripts/start.py" <Job>`.
   It reads the Job from disk (writes nothing), opens the workbench on the tab of the step the Job is at
   (starting the SPACE's host through /wb when none runs) and prints the Job's Tasks, the one step now, `who`
   does it and what. `--no-open` only prints; `--json` for the fields.
2. **Say where it stands**, in a few lines: the Job's Tasks with ▶ on the current one, the data it reads, the step
   now, any `note` as it is, and the tab now open by its full `open` link (never a bare `/_board/...` path).
3. **Guide that one step**, then stop:
   - `who: agent` on the items Task: do it now through `/haipipe-labeling-preparation` (its "The items Task"):
     describe runs to the end; items and embed stop once their recipe or build is proposed. Then tell the person
     what to look at in the open tab, and what to press.
   - `who: person`: say exactly what to press in which tab (Sign the recipe, Agree the build), and that the next
     message is this same start message, or the tab's own Copy prompt.
   - the building Task: the items are ready; continue with the no-argument behaviour below on that Task.
4. **Every message after** is the same start message (or a tab's prompt, with its `user feedback:` line). The
   script reads the Job again, so the guide moves on by itself; nothing is remembered between messages.

A person's feedback rides on the message as a `user feedback:` line; on the items Task it goes into the step's
config as its notes (and a revision's reason).

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
LAW      haipipe-labeling-building · haipipe-labeling-scanning          who may decide, human gates, verbs, forbidden acts
ORDER    haipipe-labeling-building · haipipe-labeling-scanning   which Run comes next, allocation, receipts
VIEW     haipipe-labeling-<view> × 11                 one context skill per workbench view; a Run's own steps
CROSSING haipipe-labeling-workflow               Run Specs, dependencies, gates, Routes, handoff validity, invalidation
RUN      haipipe-run + ref-run.md                 Level-4 identity, Ticket/Result pairing, receipt, presentation
```

The Data views use `haipipe-labeling-preparation` for upstream raw-corpus work,
then `haipipe-labeling-contract` and `-embedding` for the Page-local job.
The eleven job view skills are `haipipe-labeling-contract` and `-embedding` (Data),
`-definition`, `-rounds` and `-guideline` (Labeling), `-test`, `-evaluation` and
`-audit` (Quality), and `-handoff`, `-scan` and `-final-labels` (Delivery). Route a
request about one Run to its view skill; no view skill is used by another view
(JL 260929). That Skill is one member of the Run Type's declared set, which
also includes shared workflow, domain, and procedure Skills; see
`../haipipe-labeling-building/ref/ref-space-mapping.md` §Run Type skills. The set describes
guidance, not proof that a historical Run loaded each Skill. A rule that fits
two layers goes in the door. P0-P5 and G0-G6 are stable
compatibility labels declared in `haipipe-labeling-workflow`; they are not
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

Read `../haipipe-labeling-building/ref/ref-label-handoff.md` whenever creating, validating, or
consuming the crossing.

Read `../haipipe-labeling-building/ref/ref-run.md` whenever allocating, resuming, presenting, or
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
building | build | teach  forward to /haipipe-labeling-building (law), which hands execution
                          to /haipipe-labeling-building (order)
scanning | scan           forward to /haipipe-labeling-scanning (law), which hands execution
                          to /haipipe-labeling-scanning (order)
workflow | run | drive    forward to /haipipe-labeling-workflow, which hands the
                          runnable side to its ORDER machine
one Run | one view        forward to that view's skill (/haipipe-labeling-<view>),
                          which holds the Run's own steps
raw corpus | preparation forward to /haipipe-labeling-preparation before Contract
feedback | digest         use the existing family feedback procedures
```

No-argument behavior:

1. resolve the job;
2. load `haipipe-labeling-workflow` (it defines gates G0-G6) and derive the
   highest valid gate from canonical artifacts;
3. dispatch the single next runnable action, allocating or resuming its exact
   Level-4 Run only when its Ticket contract is ready;
4. stop at a human gate or explicit `HOLD`.

Do not ask the user to choose among `pick`, `seal`, `judge`, `rules`, `measure`,
or `next`. Those are verbs inside one calibration round, not top-level phases.

## Retired names

The pre-0.4.0 commands `/label-init`, `/label-round`, `/label-evaluate`,
`/label-complete`, `/label-status` and the `/sl-*` names are retired, and so are
the draft door names `subjective-labeling` and `subjective-scanning` that
preceded this rename. When
a person types one, announce the canonical route and continue there:

```text
/label-init · /label-round      → /haipipe-labeling-building
/label-evaluate · /label-complete → /haipipe-labeling-scanning
/label-status                   → /haipipe-labeling status
```

Never preserve panel-majority gold, public-dataset convergence, or unvalidated
k-NN inheritance semantics.

## Core contract

One identified human is the semantic authority. Models may retrieve, prelabel,
diagnose, draft, and execute a frozen policy; they never create human gold by
consensus. Maintain:

- H/L/N terminal classes, with `NONE` meaning absence of evidence;
- H, L, N, HL, LN, HN, and HLN diagnostic regions;
- uncertainty and unresolved disposition separate from `NONE`;
- `D_cal*`, `G*`, sealed `T*`, executor scorecards, completed `D*`, and full
  provenance.

Read `../haipipe-labeling-building/ref/ref-contract.md` for authority and claim rules,
`../haipipe-labeling-building/ref/ref-assets.md` for canonical artifact locations, and
`../haipipe-labeling-building/ref/ref-run.md` for the Labeling Run dialect. Every `../haipipe-labeling-building/ref/`
path is relative to this skill's REAL folder inside the plugin; when the skill
was loaded through a symlink (`~/.claude/skills/...`), resolve it first.

## Implementation truth

Inspect actual engine capability before writing. A conceptual contract is not
evidence that sealing, checkpointing, evaluation, production, or auditing ran.
When a required keeper, writer, runner, or verifier is absent, return `HOLD`
with the missing capability, preserved Run frontier, responsible owner, and
next implementation action. Never emulate a missing Run, owner, or gate with
majority vote, inferred provenance, or placeholder receipts.
