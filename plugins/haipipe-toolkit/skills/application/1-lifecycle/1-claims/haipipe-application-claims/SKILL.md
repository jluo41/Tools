---
name: haipipe-application-claims
description: "Stage orchestrator for the intervention's 0-lifecycle/1-claims/1-claims.md: the venue-FREE claim/evidence inventory and evidence campaign brain, and THE HOME OF EVERY CLAIM'S STATUS (supported | refuted | inconclusive, with confidence, claim_type and the G1/G2/G3 gates). Three sections: Claims (what must be true, short, with status + → PP reference), Probes (the evidence plan, one per PP), Evidence Campaign (dispatch order + dependencies + summary). Plans what evidence to collect, raises the questions the PROBE phase commissions to the task/discovery bank, and receives each answer as a probe section's `reading`. The pinned venue later sets how much of the campaign must SETTLE before artifact work (light/medium/full). Markdown only. Trigger: claims, claim ledger, what must be true, evidence plan, probes, supported, refuted, inconclusive, GAP, /haipipe-application claims."
argument-hint: "[intervention-path] [--backfill <PPNN>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.2.1"
  last_updated: "2026-07-14"
  summary: "Port of paper claims 4.0.0 (765696f): claims = evidence campaign brain. Three sections (Claims / Probes / Evidence Campaign; no Hypotheses app-side — mechanism lives in seed/pitch); _EVIDENCE_ → _VALUES_; settlement gate reads the campaign; ascii heading + one-sentence-per-line artifact formatting. v5.1 (paper claims 4.1.0 port): DRAFT opens by consuming seed's [FORWARD -> CLAIMS] pointers; any unconsumed pointer fails CHECK. v5.2 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): THE CLAIM LEDGER IS NOW THE ONLY HOME OF A CLAIM'S STATUS. R7 killed the probe 'Verdict' block and the 'verdicted' state, so `supported | refuted | inconclusive` + confidence + claim_type + G1/G2/G3 land HERE, per-claim, per-consumer, private — a probe section's `reading` FEEDS this ledger and no longer carries a judgment of its own. Probe files live at 1-probes/PPNN_<topic>.md (one file per topic, one SECTION per question); the per-stage _PROBE/ folder and the 1-probe-plans/ index are RETIRED. Evidence is COMMISSIONED to the task/discovery orchestrators (the probe gateway is retired) and returns as a QA file the section's target: points at. --backfill reads the section's reading, not a verdict block. Convention pointer repointed: `haipipe-application/fn/probe-plans.md` was RENAMED to `fn/probes.md` (matching the paper twin; 'plans' is retired vocabulary per skills/STRUCTURE.md)."
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

2. OUTSOURCE   each GAP claim raises a QUESTION; the PROBE phase collects it into
               1-probes/PPNN_<topic>.md as a SECTION, matches it against the bank's
               QA corpus, and commissions only what is missing to tasks/ or discoveries/
               claims writes the NEED, never the execution spec

3. COLLECT     answers come back as a section's `reading` at INTERPRET
               THE STATUS LANDS HERE: supported | refuted | inconclusive
               verified numbers go to _VALUES_
               claims RECEIVES evidence, never PRODUCES it
```

**THE CLAIM'S STATUS LIVES IN THIS LEDGER, AND NOWHERE ELSE** (R7, 2026-07-14). A probe file
does not judge — it carries the evidence's MEANING for this intervention (its `reading`), and
that is all. The judgment — `supported | refuted | inconclusive`, plus `confidence`,
`claim_type`, and the G1/G2/G3 gates — is written HERE, per-claim, private to this intervention.
Two consumers reading the SAME bank fact may reach different judgments about their own claims,
and that is correct: the fact is shared, the judgment is not.
💀 The probe `## Verdict` block and the `verdicted` state are DELETED. Do not write either.

**Venue-FREE.** Written before the venue is pinned and unchanged on retarget: the ledger's truth does not change when the channel changes. No slot-mapping, no channel framing here. What the venue DOES control is the required **settlement depth**, read at the gate against the Evidence Campaign (below).

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory + probe plans + campaign
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal
- `0-lifecycle/1-claims/_VALUES_1-claims.md` -- verified numbers backing each supported claim
- `0-lifecycle/1-claims/_CITATION_1-claims.md` -- citation candidates (SECTIONED VENUES ONLY, e.g. report)
- `1-probes/PPNN_<topic>.md` -- the probe FILES (intervention-root, one per topic, one SECTION per question). NOT a per-stage `_PROBE/` folder, NOT a `1-probe-plans/` index: both are RETIRED.

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
- **Probes** carry the evidence plan per PP number: which claims it settles, dependencies, and what would answer it. This is where the brain thinks; the probe file at `1-probes/PPNN_<topic>.md` is where the QUESTION is actually posed (as a SECTION) and bound to an answer.
- **Evidence Campaign** shows all probes with status and dependencies -- the settlement gate evaluates the venue bar against THIS table.
- No Hypotheses section (application delta vs paper): the intervention's mechanism lives in seed/pitch. Alignment is in the tags: `C1`, `PP03 (C1/C3)`.

**The judgment fields (written HERE, at INTERPRET, when a probe section's `reading` lands):**

```text
status       supported | refuted | inconclusive      (the enum; nothing else is a status)
confidence   how strongly the evidence carries the claim
claim_type   associational | causal | in-sample | generalizing   (never upgraded by confidence)
gates        G1 / G2 / G3   (judgment CONTENT is governed by the probe-review skill:
             ../../../../probe/haipipe-probe-review/SKILL.md — only its LANDING SITE is here)
```

**Formatting (artifact, not this spec):**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- Sub-items within sections: `**bold**` text (e.g. `**C1 - title (role) - status**`, `**PP01 - title - status**`).
- One sentence per line (semantic line breaks). Probes separated by `---` rules.

**Status vocabulary:** `supported` · `weak` · `GAP` (the ledger's own progress vocabulary), settled by the judgment enum `supported | refuted | inconclusive`. A claim is `supported` only when it traces to a QA file in the bank, through a probe section's `target:` and `reading:` -- never from intuition, and never from a probe file's own say-so (probe files no longer judge).

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
          claims from the seed, scan already-`read` probe sections for settled
          evidence; write Claims (short), Probes (full plans), Evidence Campaign
          (internally calls haipipe-application-draft with this artifact spec)
          DRAFT RAISES THE QUESTIONS. It does not answer them, and it does not
          dispatch: every GAP/weak claim leaves here as an open question.
  │
  ▼
PROBE ──→ haipipe-application-probe runs the five-step loop over those questions:
          ①ORGANIZE into 1-probes/ ②MATCH the bank's QA corpus ③DISPATCH only what
          is missing ④POINT target: at the answering QA file ⑤INTERPRET
          COLLECT: the reading lands, THE CLAIM'S STATUS FLIPS HERE, numbers to _VALUES_
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

## Probe dispatch

Probe FILES live at `1-probes/PPNN_<topic>.md` (intervention root, one file per topic, one
SECTION per question); `ls 1-probes/` is the numbering authority. Section states:
`planned | commissioned | answered | read | answered-local | failed`.

Dispatch ONLY through `haipipe-application-probe` (`/haipipe-application probe run [PPNN]`).
**This stage never dispatches an evidence agent itself, and never reads or writes anything under
`tasks/` or `discoveries/`** — that is LAW 1, and breaking it is exactly how a bank file ends up
carrying this ledger's claim ids.

Most questions should never reach an agent at all: the PROBE phase MATCHes the bank's QA corpus
first (T2 REUSE), and in a healthy project most answers already exist. A commission is the
EXCEPTION.

On return, `--backfill <PPNN>` flips the claim from the section's `reading`:
`supported` → supported; `refuted` → drop or reword; `inconclusive` → stays weak/GAP with the
caveat recorded. The status is WRITTEN HERE — there is no verdict block to copy it from.
Convention: `../../../haipipe-application/fn/probes.md`.

## Settlement Gate (venue-scaled, read at CHECK against the campaign)

CHECK reads `STATUS.md | claims_settlement |` (absent = venue unpinned, apply `light` provisionally) and evaluates the Evidence Campaign table:

```
light    (sms, push, reminder)      every claim the artifact leans on is at least
                                    tied to a named ledger claim (C##) or "common knowledge";
                                    GAPs allowed if not load-bearing
medium   (checklist, email)         primary claims supported or weak-with-caveat;
                                    load-bearing GAPs have campaign rows (dispatch optional)
full     (dashboard, ui-card,       primary claims supported (judged HERE, from a landed
          report)                   QA file); every GAP in the campaign, load-bearing ones settled
```

**Done-criteria:**
- [ ] Every claim has its own `**C<n>**` sub-item with role, status, and → PP reference
- [ ] Every probe has its own `**PP<nn>**` sub-item with its evidence plan; a probe FILE exists for it under `1-probes/`, with one SECTION per question
- [ ] No unconsumed `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md` -- each is either a PP entry in Probes (with its Evidence Campaign row) or explicitly declined in `_LOG`
- [ ] Evidence Campaign shows dispatch order and dependencies; no load-bearing GAP without a campaign row
- [ ] Every settled claim traces to a section whose `target:` RESOLVES to a QA file on disk -- a status with no resolving target is the exact shortcut this ledger exists to prevent
- [ ] No section is still `planned`, and no `commissioned` section is OVERDUE (`check-probe-cards.sh --stage 1-claims`)
- [ ] Verified numbers recorded in _VALUES_ (with anchors); no aspirational anchors anywhere
- [ ] Settlement bar met for the pinned (or provisional) depth

## Principles

1. Claims short, probes full, campaign compact -- one thought, one home; no matrix tables.
2. Never mark `supported` from intuition; cite the QA file the section's `target:` resolves to.
3. No aspirational anchors: "the dashboard will show X" is not evidence.
4. Overclaim guard: if the evidence is in-sample only (a pattern inside one dataset, with no generalization basis) while the claim asserts it holds beyond that sample, the claim stays `weak` and a question is raised. Same for a causal claim resting on associational evidence — `claim_type` decides, and it is never upgraded just because `confidence` is high.
5. Venue-FREE: retargeting changes the required settlement, never the ledger's truth.
6. **The judgment is OURS; the fact is not.** The bank's QA files speak general language and belong to every consumer. This ledger interprets them for THIS intervention. Never push our claim ids back into the bank, and never expect a QA file to tell us whether a claim survives -- that is this file's job, and only this file's.
7. **This stage never executes bank work inline** (LAW 1). It raises questions; `haipipe-application-probe` binds them. A claims session that opens `tasks/.../results/` and starts writing has already broken the wall, whatever it ends up writing.

## Handoff

On CHECK confirm: `promote -> /haipipe-application venue` (pin modality + Artifact Principles), or `-> /haipipe-application pitch` if venue already pinned. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
