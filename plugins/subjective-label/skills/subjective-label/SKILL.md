---
name: subjective-label
description: >-
  The one user-facing door for a human-grounded subjective-label family with
  two sides: Label Building teaches and freezes what one identified human means
  by a vague trait; Label Scanning qualifies executors against a sealed
  human-gold test, scans the corpus under the frozen meaning, and audits the
  completed labels. Use for starting, resuming, routing, or checking a
  subjective annotation job; defining H/L/N and boundary regions; calibration
  rounds; guideline freeze; executor evaluation; corpus scanning; final audit;
  or /subjective-label.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-30"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label · build the label, then scan under it

This is the only user-facing door. Resolve one job as one corpus snapshot plus
one target trait, inspect its artifacts, and route to the owning sibling door.
Do not expose internal round actions as a menu of lifecycle phases.

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

Three layers, never mixed:

```text
LAW      label-building · label-scanning          who may decide, human gates, verbs, forbidden acts
ORDER    label-building-workflow · label-scanning-workflow   step order, resume, run receipts
CROSSING subjective-label-workflow               phase numbers P0-P5, gates G0-G6, handoff validity, invalidation
```

A rule that fits two layers goes in the door. Phase and gate numbers are
declared in `subjective-label-workflow` only.

## The crossing

The only legal crossing is one immutable Label Handoff. It binds:

- the corpus snapshot and target population;
- label, region, and uncertainty schemas;
- frozen policy `G*` and calibration gold `D_cal*` checksums;
- the sealed-test manifest checksum and custody status, never protected ids;
- the human semantic authority and freeze signature;
- lineage, invalidation status, and creation receipt.

Scanning reads the handoff by checksum. It never reads policy drafts as
authority and never edits `G*` or `D_cal*`. A semantic change returns to
Building, mints a new lineage, and invalidates affected scorecards, runs, and
claims.

Read `../../ref/ref-label-handoff.md` whenever creating, validating, or
consuming the crossing.

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
building | build | teach  forward to /label-building (law), which hands execution
                          to /label-building-workflow (order)
scanning | scan           forward to /label-scanning (law), which hands execution
                          to /label-scanning-workflow (order)
workflow | run | drive    forward to /subjective-label-workflow, which hands the
                          runnable side to its ORDER machine
feedback | digest         use the existing family feedback procedures
```

No-argument behavior:

1. resolve the job;
2. load `subjective-label-workflow` (it defines gates G0-G6) and derive the
   highest valid gate from canonical artifacts;
3. dispatch the single next runnable action;
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
/label-init · /label-round      → /label-building
/label-evaluate · /label-complete → /label-scanning
/label-status                   → /subjective-label status
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

Read `../../ref/ref-contract.md` for authority and claim rules and
`../../ref/ref-assets.md` for canonical artifact locations. Every `../../ref/`
path is relative to this skill's REAL folder inside the plugin; when the skill
was loaded through a symlink (`~/.claude/skills/...`), resolve it first.

## Implementation truth

Inspect actual engine capability before writing. A conceptual contract is not
evidence that sealing, checkpointing, evaluation, production, or auditing ran.
When a required keeper, writer, runner, or verifier is absent, return `HOLD`
with the missing capability, preserved artifact frontier, responsible owner,
and next implementation action. Never emulate a missing phase with majority
vote, inferred provenance, or placeholder receipts.
