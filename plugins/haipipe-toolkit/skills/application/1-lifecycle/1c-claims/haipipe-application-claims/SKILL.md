---
name: haipipe-application-claims
description: "Stage orchestrator for rung 1c of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice): the claim ledger + evidence campaign brain — what generalizes, with status + anchor. THE ONLY home of a claim's status (supported | weak | GAP). Three sections: Claims (theme-tagged, status + PP reference), Q-consumer (the evidence questions raised, one `## Q` per Q), Evidence Campaign (dispatch order + dependencies). The pinned venue sets how much of the campaign must SETTLE (light/medium/full). Markdown only. Trigger: claims, claim ledger, what must be true, what generalizes, evidence plan, probes, supported, GAP, /haipipe-application claims."
argument-hint: "[intervention-path] [--backfill <PPNN>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "7.2.0"
  last_updated: "2026-07-17"
  summary: "Claims stage (rung 1c of the venue-FREE 1a–1d evidence ladder; the K rung) — the ONLY home of a claim's status (supported | weak | GAP, from a judged artifact, never intuition; no verdict block). Consumes 1b theme hooks into a claim ledger + evidence campaign, gives each primary a Rival + refute-capable probe, and reaches for evidence via the PROBE phase (questions raised as sections in 1-probes/). The pinned venue sets how much of the campaign must SETTLE (light/medium/full). History: ./CHANGELOG.md."
---

Skill: haipipe-application-claims
==================================

Rung **1c** of the venue-FREE evidence ladder, and the rung that reaches hardest for evidence.
It answers: which claims generalize — supported, weak, or GAP — and what evidence settles each?

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)   <- THIS RUNG
1d-advice         what the evidence advises (the deliverable)
```

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/03-intervention-lifecycle.md`, `../../../wiki/11-delivery-need.md`.


## What's special: three things make claims claims

**1. It is the ONLY home of a claim's status.**
`supported | weak | GAP` lives HERE, per-claim, private to this intervention — never in a probe file (there is no `## Verdict`, no `verdicted` state).
A probe section carries the evidence's MEANING (its `a-consumer:`); the judgment is ours to write.
A claim is `supported` only when it traces to a JUDGED artifact (a full-mode probe answer, or an equivalently reviewed result) — never from intuition, never from a raw unjudged number.

**2. The venue sets the settlement bar, read at the gate.**
Venue-FREE: retargeting changes the required settlement, never the ledger's truth.
CHECK reads `STATUS.md | claims_settlement |` and evaluates the Evidence Campaign table against it (light | medium | full — table below).
The same bar reaches 1d: an advice entry may only cite claims at/above it.

**3. It consumes 1b's theme hooks, and it tests its primaries to destruction.**
Every 1b theme hook becomes a `C<n>` entry or a Declined-hooks line with a why — the Declined section is the reservoir the next round re-mines.
Every primary claim carries a `Rival:` (the strongest alternative explanation) and a refute-capable probe (`Refutes-if:` — the result that would FLIP it, not only confirm it).
There is NO Hypotheses section (application delta vs paper): the mechanism lives in seed/pitch, the theme space in 1b, and alignment is in the tags (`C1 (T1)`, `PP03 (C1/C3)`).


## The four phases, in claims

```text
DRAFT   re-mine last round's Declined reservoir, read 1b-themes.md (hooks = claim candidates)
        and 1a-descriptions.md (the grounding floor); CONSUME every hook; give every primary a
        Rival; write Claims (short, theme-tagged), Q-consumer (the evidence questions), Evidence Campaign
PROBE   one worker call; the five-step loop raises each GAP/weak claim as a SECTION in 1-probes/
        and COLLECTS — the claim status FLIPS at INTERPRET, numbers land in _VALUES_. Mode FULL is
        the norm here. Routing mechanics are the probe layer's: ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  refine claim statements, probe-plan clarity, campaign ordering
CHECK   settlement bar vs the campaign table; every hook consumed; every primary has a Rival +
        Refutes-if; every settled claim traced to a RESOLVING QA file; no aspirational anchors; no STALE tags
```

Claims RECEIVES evidence, never PRODUCES it inline (LAW 1): it raises questions; `haipipe-application-probe` binds them.
`--backfill <PPNN>` flips a claim from a landed answer: `supported` -> supported · `refuted` -> drop or reword · `inconclusive` -> stays weak/GAP with the caveat recorded.
Rounds + back-routing (loop-until-dry for medium+ venues, `[ROUND n]` / `[ROUTE -> themes|descriptions]` in `_LOG`) follow `../../../wiki/08-stage-gate.md`.
Seed's `[FORWARD -> CLAIMS]` pointers are consumed by rung 1a, which seeds this doc's questions; this rung no longer greps seed's `_LOG` itself.


## The artifact

`0-lifecycle/1c-claims/1c-claims.md` — full skeleton in `ref/claims-template.md`:

```text
Claims             one C<n>: statement + theme tag (T<n>) + role (primary|enabling|assumption)
                   + status + -> PP reference; primaries carry a Rival line (short; the question is in Q-consumer)
Declined hooks     theme hooks considered and not committed, one line + why (the reservoir)
Q-consumer         one `## Q` per evidence question this stage raises; the mode, route,
                   approver, and Refutes-if organize into 1-probes/ at APPROVE, not here
Evidence Campaign  dispatch order + a compact summary table (the gate reads this)
```

Sidecars: `_LOG_1c-claims.md` (phase journal) · `_VALUES_1c-claims.md` (verified numbers with anchors) · `_CITATION_1c-claims.md` (sectioned venues only).
A claim with no plausible theme parent signals a 1b gap: loop back to themes rather than orphan-tagging.


## Settlement Gate (venue-scaled, read at CHECK against the campaign)

```text
light    (sms, push, reminder)      every claim the artifact leans on is at least tied to a named
                                    anchor or "common knowledge"; GAPs allowed if not load-bearing
medium   (checklist, email)         primary claims supported or weak-with-caveat;
                                    load-bearing GAPs have campaign rows (dispatch optional)
full     (dashboard, ui-card,       primary claims supported (judged); every GAP in the campaign,
          report)                   load-bearing ones settled
```

Absent `claims_settlement` (venue unpinned) → apply `light` provisionally.


## Exits

```text
promote -> /haipipe-application advice   derive the advice (the ladder's deliverable)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
