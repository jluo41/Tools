---
name: haipipe-application-claims
description: "Stage orchestrator for the intervention's 0-lifecycle/1-claims/1-claims.md: the venue-FREE claim/evidence inventory and evidence campaign brain. Three sections: Claims (what must be true, short, with status + → PP reference), Probes (the evidence plan, one per PP, full detail), Evidence Campaign (dispatch order + dependencies + summary). Plans what evidence to collect, commissions the work via the probe gateway (tasks/discoveries), and tracks results as they return. The pinned venue later sets how much of the campaign must SETTLE before artifact work (light/medium/full). Markdown only. Trigger: claims, claim ledger, what must be true, evidence plan, probes, supported, GAP, /haipipe-application claims."
argument-hint: "[intervention-path] [--backfill <PPNN>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.1.0"
  last_updated: "2026-07-07"
  summary: "Port of paper claims 4.0.0 (765696f): claims = evidence campaign brain. Three sections (Claims / Probes / Evidence Campaign; no Hypotheses app-side — mechanism lives in seed/pitch); _EVIDENCE_ → _VALUES_; settlement gate reads the campaign; ascii heading + one-sentence-per-line artifact formatting. v5.1 (paper claims 4.1.0 port): DRAFT opens by consuming seed's [FORWARD -> CLAIMS] pointers; any unconsumed pointer fails CHECK."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-claims
==================================

Stage orchestrator for the **claims** stage (stage 1, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
What must be true for this intervention to work, and what evidence settles each claim?
```

Claims is the **evidence campaign brain**. It does three jobs in sequence:

```text
1. PLAN        what must be true? (claims)
               what evidence would settle each? (probe plan per claim)

2. OUTSOURCE   dispatch through the probe gateway to tasks/ and discoveries/
               each GAP claim → a probe that routes to task or discovery
               claims writes the NEED, not the execution spec

3. COLLECT     results come back via TRANSLATE
               backfill status: GAP → weak → supported
               verified numbers go to _VALUES_
               claims RECEIVES evidence, never PRODUCES it
```

**Venue-FREE.** Written before the venue is pinned and unchanged on retarget: the K/W truth does not change when the channel changes. No slot-mapping, no channel framing here. What the venue DOES control is the required **settlement depth**, read at the gate against the Evidence Campaign (below).

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory + probe plans + campaign
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal
- `0-lifecycle/1-claims/_VALUES_1-claims.md` -- verified numbers backing each supported claim
- `0-lifecycle/1-claims/_CITATION_1-claims.md` -- citation candidates (SECTIONED VENUES ONLY, e.g. report)
- `0-lifecycle/1-claims/_PROBE/PPNN_*.md` -- probe card files (execution detail per PP; + index row in `1-probe-plans/README.md`)

**Content structure (1-claims.md) -- three sections + summary:**

```text
Claims                what must be true: one **C<n>** per claim — statement,
                      role (primary|enabling|assumption), status, → PP reference
Probes                the evidence plan: one **PP<nn>** per probe — mode,
                      which claims it settles, dependencies, what work, route
Evidence Campaign     dispatch order + summary table (probe, status, deps,
                      settles) — the compact overview the gate reads
```

- **Claims** are short: the testable statement, role, current status (supported/weak/GAP), and which probe settles it. No inline study design.
- **Probes** carry the full evidence plan per PP number: mode (light/full), route (task/discovery), which claims it settles, dependencies. This is where the brain thinks; the `_PROBE/` card mirrors it as the dispatch contract.
- **Evidence Campaign** shows all probes with status and dependencies -- the settlement gate evaluates the venue bar against THIS table.
- No Hypotheses section (application delta vs paper): the intervention's mechanism lives in seed/pitch. Alignment is in the tags: `C1`, `PP03 (C1/C3)`.

**Formatting (artifact, not this spec):**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- Sub-items within sections: `**bold**` text (e.g. `**C1 - title (role) - status**`, `**PP01 - title - status**`).
- One sentence per line (semantic line breaks). Probes separated by `---` rules.

**Status vocabulary:** `supported` · `weak` · `GAP`. A claim is `supported` only when it traces to a judged artifact (insight K/W card, probe verdict `supported`, or an equivalently reviewed result) -- never from intuition. Verdict words follow the PPNN enum: `supported | refuted | inconclusive`.

## Phase Orchestration

```
claims invoked
  │
  ▼
DRAFT ──→ FIRST: consume seed's forward pointers — grep seed's
          `_LOG_0-seed.md` for `[FORWARD -> CLAIMS]` lines; each becomes a
          PP entry in the Probes section + an Evidence Campaign row (or is
          explicitly declined with a `_LOG` note). An unconsumed pointer
          fails the CHECK done-criteria below.
          Then: illuminate existing claims, elicit taste, extract testable
          claims from the seed, scan insights/INDEX.md for candidate K/W;
          write Claims (short), Probes (full plans), Evidence Campaign
          (internally calls haipipe-application-draft with this artifact spec)
  │
  ▼
PROBE ──→ mirror each planned PP into a _PROBE/ card (+ index row);
          dispatch on `probe run` via haipipe-application-probe;
          COLLECT: backfill statuses, land numbers in _VALUES_
  │
  ▼
REVISE ─→ refine claim statements, probe plan clarity, campaign ordering
          (internally calls haipipe-application-revise)
  │
  ▼
CHECK ──→ present exit gate (settlement bar vs the campaign table);
          user confirms → Gate Ledger row → advance to venue
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict; CHECK is never implicit.

## Probe dispatch (unchanged folderless contract)

Cards live in `_PROBE/`, numbering authority = `1-probe-plans/README.md`, statuses `planned | dispatched | read | verdicted`. Dispatch ONLY through `haipipe-application-probe` (`/haipipe-application probe run [PPNN]`) -- never `/haipipe-probe` from here. Claims-stage probes default to **mode: full** (committed verdicts); orientation questions run light. On verdict return, `--backfill <PPNN>` flips the claim from the verdict: `supported` → supported; `refuted` → drop or reword; `inconclusive` → stays weak/GAP with the caveat recorded. Buffer convention: `../../../haipipe-application/fn/probe-plans.md`.

## Settlement Gate (venue-scaled, read at CHECK against the campaign)

CHECK reads `STATUS.md | claims_settlement |` (absent = venue unpinned, apply `light` provisionally) and evaluates the Evidence Campaign table:

```
light    (sms, push, reminder)      every claim the artifact leans on is at least
                                    tied to a named K/W or "common knowledge";
                                    GAPs allowed if not load-bearing
medium   (checklist, email)         primary claims supported or weak-with-caveat;
                                    load-bearing GAPs have campaign rows (dispatch optional)
full     (dashboard, ui-card,       primary claims supported (judged verdicts);
          report)                   every GAP in the campaign, load-bearing ones verdicted
```

**Done-criteria:**
- [ ] Every claim has its own `**C<n>**` sub-item with role, status, and → PP reference
- [ ] Every probe has its own `**PP<nn>**` sub-item with full evidence plan; `_PROBE/` cards mirror them
- [ ] No unconsumed `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md` -- each is either a PP entry in Probes (with its Evidence Campaign row) or explicitly declined in `_LOG`
- [ ] Evidence Campaign shows dispatch order and dependencies; no load-bearing GAP without a campaign row
- [ ] Verified numbers recorded in _VALUES_ (with anchors); no aspirational anchors anywhere
- [ ] Settlement bar met for the pinned (or provisional) depth

## Principles

1. Claims short, probes full, campaign compact -- one thought, one home; no matrix tables.
2. Never mark `supported` from intuition; cite the judged artifact and its anchor.
3. No aspirational anchors: "the dashboard will show X" is not evidence.
4. Overclaim guard: I-level evidence for a K-level claim stays `weak`, route a probe.
5. Venue-FREE: retargeting changes the required settlement, never the ledger's truth.
6. The application reads the project KB (insights/INDEX.md first) but never writes insight cards from here -- deposits belong to the probe/insight side.

## Handoff

On CHECK confirm: `promote -> /haipipe-application venue` (pin modality + Artifact Principles), or `-> /haipipe-application pitch` if venue already pinned. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
