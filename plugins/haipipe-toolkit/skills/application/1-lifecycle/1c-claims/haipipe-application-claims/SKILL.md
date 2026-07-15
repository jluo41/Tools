---
name: haipipe-application-claims
description: "Stage orchestrator for the intervention's 0-lifecycle/1c-claims/1c-claims.md: rung 1c of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice). The claim ledger and evidence campaign brain: what generalizes, with status + anchor. Three sections: Claims (short, theme-tagged, status + PP reference), Probes (the evidence plan, one per PP), Evidence Campaign (dispatch order + dependencies). The pinned venue later sets how much of the campaign must SETTLE (light/medium/full). Markdown only. Trigger: claims, claim ledger, what must be true, what generalizes, evidence plan, probes, supported, GAP, /haipipe-application claims."
argument-hint: "[intervention-path] [--backfill <PPNN>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "6.1.0"
  last_updated: "2026-07-09"
  summary: "6.1.0 (breadth round, JL 2026-07-09): full hook consumption (Declined-hooks section = reservoir), Rival line + refute-capable probe per primary claim, multi-round DPRC + mid-phase back-routing. 6.0.0 ladder restage (SOP-ladder-restage.md): stage 1 split into the 1a-1d evidence ladder; this skill is now rung 1c, the K rung. Slimmed to pure claim work: claims cite T/D ids from 1b/1a; FORWARD reader moved to 1a; keeps statuses, settlement, campaign, _VALUES_; staleness tags honored at CHECK. Prior history: 5.x = paper claims port (evidence campaign brain)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-claims
==================================

Stage orchestrator for **rung 1c** of the evidence ladder (venue-FREE). The user invokes this skill (or the `ladder` sweep); it drives the phases internally.

It answers one question:

```text
Which claims generalize -- supported, weak, or GAP -- and what evidence settles each?
```

The evidence ladder (stage-1 family, all venue-FREE):

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)   <- THIS RUNG
1d-advice         what the evidence advises (the deliverable)
```

Claims is the **evidence campaign brain** -- the rung that reaches out hardest for evidence. It does three jobs in sequence:

```text
1. PLAN        what must be true? (claims, extracted from 1b theme hooks)
               what evidence would settle each? (probe plan per claim)

2. OUTSOURCE   dispatch through the probe gateway to tasks/ and discoveries/
               each GAP claim -> a probe that routes to task or discovery
               claims writes the NEED, not the execution spec

3. COLLECT     results come back via TRANSLATE
               backfill status: GAP -> weak -> supported
               verified numbers go to _VALUES_
               claims RECEIVES evidence, never PRODUCES it
```

**Venue-FREE.** Written before the venue is pinned and unchanged on retarget: the truth of a claim does not change when the channel changes. No slot-mapping, no channel framing here. What the venue DOES control is the required **settlement depth**, read at the gate against the Evidence Campaign (below) and applied through 1d's derivations.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1c-claims/1c-claims.md` -- claim/evidence inventory + probe plans + campaign
- `0-lifecycle/1c-claims/_LOG_1c-claims.md` -- phase progress journal
- `0-lifecycle/1c-claims/_VALUES_1c-claims.md` -- verified numbers backing each supported claim
- `0-lifecycle/1c-claims/_CITATION_1c-claims.md` -- citation candidates (SECTIONED VENUES ONLY, e.g. report)
- `0-lifecycle/1c-claims/_PROBE/PPNN_*.md` -- probe card files (execution detail per PP; + index row in `1-probe-plans/README.md`)

**Canonical template (source of truth for section order + placeholders):** `ref/claims-template.md`

**Content structure (1c-claims.md) -- three sections + summary:**

```text
Claims                what generalizes: one **C<n>** per claim -- statement,
                      theme tag (T<n>), role (primary|enabling|assumption),
                      status, -> PP reference; primaries carry a Rival line
Declined hooks        theme hooks considered and not committed, one line + why
Probes                the evidence plan: one **PP<nn>** per probe -- mode,
                      which claims it settles, dependencies, what work, route
Evidence Campaign     dispatch order + summary table (probe, status, deps,
                      settles) -- the compact overview the gate reads
```

- **Claims** are short: the testable statement, theme tag, role, current status (supported/weak/GAP), and which probe settles it. No inline study design. Tag form: `**C1 (T1, primary) - <title> - supported**`. Primary claims also carry a one-line `Rival:` -- the strongest alternative explanation the probe must rule out.
- **Declined hooks** close the consumption loop with 1b: every theme hook either becomes a C entry or gets a one-line declined-with-why; the section is the reservoir the next round's DRAFT re-mines.
- **Probes** carry the full evidence plan per PP number: mode (light/full), route (task/discovery), which claims it settles, dependencies. This is where the brain thinks; the `_PROBE/` card mirrors it as the dispatch contract. A primary claim's probe must be refute-capable: the plan states what result would FLIP the claim (`Refutes-if:`), not only what would confirm it.
- **Evidence Campaign** shows all probes with status and dependencies -- the settlement gate evaluates the venue bar against THIS table.
- No Hypotheses section (application delta vs paper): the mechanism lives in seed/pitch, and the theme space lives in 1b. Alignment is in the tags: `C1 (T1)`, `PP03 (C1/C3)`.
- A claim with no plausible theme parent signals a 1b gap: loop back to themes rather than orphan-tagging.

**Formatting (artifact, not this spec):**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- Sub-items within sections: `**bold**` text (e.g. `**C1 (T1, primary) - title - status**`, `**PP01 - title - status**`).
- One sentence per line (semantic line breaks). Probes separated by `---` rules.

**Status vocabulary:** `supported` · `weak` · `GAP`. A claim is `supported` only when it traces to a judged artifact (a full-mode probe verdict `supported`, or an equivalently reviewed result) -- never from intuition and never from a raw, unjudged number. Verdict words follow the PPNN enum: `supported | refuted | inconclusive`. Insight K/W cards remain valid anchors when they exist, but are optional context, not a required source (ladder restage R7).

## Phase Orchestration

```
claims invoked
  |
  v
DRAFT --> re-mine the reservoir (last round's Declined hooks -- did new
          grounding land or the campaign free up?); read 1b-themes.md (the
          hooks are the claim candidates) and 1a-descriptions.md (the
          grounding floor); CONSUME every hook -- each becomes a C entry or
          a Declined-hooks line with a why; give every primary claim a Rival
          line; illuminate existing claims, elicit taste; write Claims
          (short, theme-tagged), Probes (full plans, refute-capable for
          primaries), Evidence Campaign
          (internally calls haipipe-application-draft with this artifact spec)
  |
  v
PROBE --> mirror each planned PP into a _PROBE/ card (+ index row);
          dispatch on `probe run` via haipipe-application-probe (mode FULL
          for committed verdicts -- this rung's normal case);
          COLLECT: backfill statuses, land numbers in _VALUES_
  |
  v
REVISE -> refine claim statements, probe plan clarity, campaign ordering
          (internally calls haipipe-application-revise)
  |
  v
CHECK --> exit gate (batched into the ladder gate for light venues; own gate
          for medium/full per wiki/08-stage-gate.md): settlement bar vs the
          campaign table; no unresolved STALE tags
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict; CHECK is never implicit.

Rounds + routing (breadth contract, wiki/08-stage-gate.md): REVISE ends with a self-assessment -- did this round surface new claims, rivals, or evidence gaps? If yes, run another DRAFT->PROBE->REVISE lap (`[ROUND n]` in `_LOG`); CHECK fires only when a round comes up dry (venue-scaled: medium+ loops-until-dry on THIS rung). Mid-phase back-routing is legal: an ungrounded hook logs `[ROUTE -> themes]`, a missing number files the 1a D slot and logs `[ROUTE -> descriptions]` -- never wait for a gate to report a discovery.

Note: seed's `[FORWARD -> CLAIMS]` pointers are consumed by rung 1a (the ladder's first rung), which materializes verdict-shaped needs as planned PP skeletons in THIS doc's Probes section. This rung inherits those skeletons at DRAFT; it no longer greps seed's _LOG itself.

## Probe dispatch (unchanged folderless contract)

Cards live in `_PROBE/`, numbering authority = `1-probe-plans/README.md`, statuses `planned | dispatched | read | verdicted`. Dispatch ONLY through `haipipe-application-probe` (`/haipipe-application probe run [PPNN]`) -- never `/haipipe-probe` from here. Claims-rung probes default to **mode: full** (committed verdicts); orientation questions run light. On verdict return, `--backfill <PPNN>` flips the claim from the verdict: `supported` -> supported; `refuted` -> drop or reword; `inconclusive` -> stays weak/GAP with the caveat recorded. Buffer convention: `../../../haipipe-application/fn/probe-plans.md`.

## Settlement Gate (venue-scaled, read at CHECK against the campaign)

CHECK reads `STATUS.md | claims_settlement |` (absent = venue unpinned, apply `light` provisionally) and evaluates the Evidence Campaign table:

```
light    (sms, push, reminder)      every claim the artifact leans on is at least
                                    tied to a named anchor or "common knowledge";
                                    GAPs allowed if not load-bearing
medium   (checklist, email)         primary claims supported or weak-with-caveat;
                                    load-bearing GAPs have campaign rows (dispatch optional)
full     (dashboard, ui-card,       primary claims supported (judged verdicts);
          report)                   every GAP in the campaign, load-bearing ones verdicted
```

The same bar reaches 1d through derivations: an advice entry may only cite claims at/above the bar (see `haipipe-application-advice`).

**Done-criteria:**
- [ ] Every claim has its own `**C<n>**` sub-item with theme tag, role, status, and -> PP reference
- [ ] Every 1b hook is consumed: a C entry or a Declined-hooks line with a why
- [ ] Every primary claim carries a Rival line; its probe plan states the refuting result (`Refutes-if:`)
- [ ] Every theme tag resolves to a `T<n>` in 1b-themes.md
- [ ] Every probe has its own `**PP<nn>**` sub-item with full evidence plan; `_PROBE/` cards mirror them
- [ ] Evidence Campaign shows dispatch order and dependencies; no load-bearing GAP without a campaign row
- [ ] Verified numbers recorded in _VALUES_ (with anchors); no aspirational anchors anywhere
- [ ] No unresolved `[STALE ...]` tags in this doc
- [ ] Settlement bar met for the pinned (or provisional) depth

## Principles

1. Claims short, probes full, campaign compact -- one thought, one home; no matrix tables.
2. Never mark `supported` from intuition; cite the judged artifact and its anchor.
3. No aspirational anchors: "the dashboard will show X" is not evidence.
4. Overclaim guard: pattern-level evidence (a 1b theme, an in-sample number) for a generalization claim stays `weak`; route a probe for the verdict.
5. Venue-FREE: retargeting changes the required settlement, never the ledger's truth.
6. The ledger reads the project KB when present but never writes insight cards from here -- deposits belong to the probe/insight side, and 1d owns on-request W deposits.

## Handoff

On CHECK confirm (or ladder-gate batch): `promote -> /haipipe-application advice` (derive the advice). End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
