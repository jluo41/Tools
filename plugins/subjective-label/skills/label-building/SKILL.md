---
name: label-building
description: >-
  The Building-side door of the subjective-label family, and its LAW: who is
  the semantic authority, what each of Contract, Round and Freeze may and may
  not create, which decisions are human gates, which verbs exist, and what is
  forbidden. It ends at a signed Label Handoff and never evaluates executors or
  scans the corpus. The order of steps lives in label-building-workflow. Use for
  new labeling jobs, calibration rounds, human annotation sessions, boundary
  discovery, guideline revision, stopping decisions, freeze, or /label-building.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-building · the law of building one meaning

`subjective-label` is the family umbrella; `subjective-label-workflow` declares
the phase numbers and gates; `label-building-workflow` orders the steps. This
door owns the LAW of the Building side, symmetric to `/label-scanning`. Nothing
here says in what order a step runs.

## Authority

One identified human decides class, region, semantic rules, concept revisions,
stopping signoff, and accepted risk. The strong calibration agent controls the
interaction and records inspectable human input; it cannot create gold, accept
its own rule proposal, or hint at a sealed prediction before the lock.

Weak executors are independent diagnostic readers. Their sealed predictions may
select challenge cases and expose guideline failures after the human-first
lock. Agreement among them is a sampling stratum, never gold.

## The three phases and what each may create

```text
P0 Contract   one valid job: corpus, target, authority, schemas, sealed reservation
              creates NO label, NO claim that the guideline is mature
P1 Round      one closed checkpoint: D_t (human-confirmed gold) + G_t (closed policy)
              creates gold ONLY through a human event inside a closed checkpoint
P2 Freeze     one signed Label Handoff binding exact G* and D_cal*
              creates NO new content; it packages what is already closed
```

Each phase is a phase because it has an authority artifact of its own; the
artifacts are named in `subjective-label-workflow`.

## Building Run boundary

Building uses the operation catalog in `../../ref/ref-run.md`:

```text
P0  corpus-contract · discovery-search* · guideline-seed · test-reserve · embedding-build
P1  round-prepare · weak-prelabel* · human-calibration · guideline-learn
    · round-measure · round-close
P2  handoff-freeze
```

A round folder, `rounds/round_<t>/`, is an episode grouped by one Card and one
checkpoint (`../../ref/ref-assets.md` §3). It is not an extra umbrella Run.
While the Card is proposed it is planning. Human release makes it the frozen
commission for `round-prepare`; later operations allocate only when their own
inputs freeze. P0 human meaning confirmation, Card release, STOP, and the
freeze signature are gate events rather than additional Runs.

Laws across the round's Runs:

1. **Card before work.** The card states the register cell it targets, its two
   arms, its seed, and its expected finding. A person releases it; a machine
   never does. Round 1's card names no cell and draws at random.
2. **Seal before sight.** Every weak prediction is sealed before the human's
   first record for that item exists; a seal that follows a first record
   voids the affected operation and blocks `round-close`.
3. **Forecast before judgment.** `prospect.md` is written before the first
   item is shown, so the checkpoint can score the round against it.
4. **Views are not authority.** `view/` and `README.md` are rendered from the
   canonical files; `checkpoint.json` is the only artifact that promotes gold
   and policy.
5. **A locked event is never replayed.** A dead chat resumes at the open item;
   it does not reopen a seal or a lock.

## The register

`register.md` holds the seven diagnostic regions (H, L, N, HL, LN, HN, HLN)
as cells, each `open`, `covered`, or `risky`. A round card names the cell(s)
it targets; CLOSE settles them. The Building side may route to Freeze only
when no cell is `open`, or the human has explicitly accepted a named open cell
as a limitation carried into the handoff.

## Human gates

```text
meaning    the human confirms the target and the schema, including what LOW means  (P0)
release    the human releases each round card                                       (P1)
item       the human creates every first and final judgment                         (P1)
rule       the human accepts, rejects, or narrows every substantive semantic patch  (P1)
stop       the human signs off stopping on the checkpoint's evidence                (P1 CLOSE)
freeze     the human signs the exact G* and D_cal* checksums and the lineage        (P2)
```

`stop` and `freeze` are two ticks: stopping approves that no round is owed;
freeze signs the handoff. A batch-selection charter may pre-authorize
mechanical sampling classes for one bounded Run; it cannot pre-authorize a
release, a label, a rule, a stop, or a freeze.

## Verbs

```text
enter | status      resolve the Building frontier from closed artifacts
start | contract    establish or resume P0 without creating gold
round               run or resume exactly one operation in the active P1 episode
card                propose a round card for a person to release
prepare · judge · learn · checkpoint   the round steps, ordered by label-building-workflow
freeze              run P2 and record the human-signed Label Handoff
reopen              open a new policy lineage and invalidate downstream claims
workflow | run      hand the frontier to label-building-workflow
```

## Forbidden

- a label, region, or rule created by model majority, unanimity, nearest
  neighbor, classifier confidence, or a persona panel;
- `NONE` used for an unresolved item;
- a sealed-test id or text inside any round file;
- a round closed with a failing Keeper check;
- a checkpoint, `D_t`, `G_t`, or handoff edited after close;
- this door writing `T*` gold, a scorecard, a production label, or an audit
  claim.

## Ends at the handoff

When a selector, sealed runner, Session recorder, Checkpoint Keeper, Test
Custodian, or Label Handoff Keeper is absent, the Building side stops at its
last closed artifact and returns a structured `HOLD`; it never emulates the
missing role.
