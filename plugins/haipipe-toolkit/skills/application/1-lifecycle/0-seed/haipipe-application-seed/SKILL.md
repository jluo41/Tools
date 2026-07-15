---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle (venue-FREE). Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel hunch, mechanism hypothesis, and kill criteria. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md (+ _PROBE/ for context needs). Markdown only. Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, kill criteria, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.2.0"
  last_updated: "2026-07-07"
  summary: "Stage 0 on the paper-aligned contract: stage FOLDER (0-seed.md + _LOG + _PROBE/), venue-FREE marker, DPRC phases via 2-phase/ workers, scaffold via enter get-or-create (dead ref pointer removed). v3.2: DRAFT may WebSearch to orient (fuel -> prose + buffered planned skeletons), PROBE must ALWAYS run the real worker; seed probes are FEASIBILITY only (novelty + external-data-obtainable), internal-data profiling forward-points to CLAIMS via a _LOG pointer."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-seed
================================

Stage 0 of the intervention lifecycle (venue-FREE). Documents why this intervention might work before investing in evidence gathering. The user invokes this skill; it drives DRAFT → PROBE → REVISE → CHECK internally via the `2-phase/` workers.

Question answered
==================

"Why might this intervention work? What is the opportunity?"

Input
======

- User intent / problem statement
- Existing project KB (insights/INDEX.md if available)
- Domain knowledge about the audience and channel

Output
=======

```
<intervention-root>/0-lifecycle/0-seed/0-seed.md
<intervention-root>/0-lifecycle/0-seed/_LOG_0-seed.md
<intervention-root>/0-lifecycle/0-seed/_PROBE/          (feasibility probes: novelty + external-data obtainability)
```

Seed artifact schema
=====================

Canonical template (source of truth for section order + placeholders): `ref/seed-template.md`.

```markdown
0-seed: <intervention name>
===========================

Opportunity
-----------
<2-3 sentences: what gap exists, what behavior we want to change>

Expected impact
---------------
<directional estimate: "increase refill adherence by 5-15pp">

Audience
--------
<who receives this intervention: patient subset, clinician type>

Channel hunch
-------------
<SMS, push, in-app UI, provider dashboard, email — a HUNCH, not a pin;
the venue decision happens after the evidence ladder (1a-1d) via
/haipipe-application venue>

Mechanism hypothesis
--------------------
<one sentence: why this audience + this content might respond>

Kill criteria
-------------
<conditions under which we abandon this intervention>
- <criterion 1: e.g., "no HTE detected in cohort data">
- <criterion 2: e.g., "click rate < 2% in pilot">
- <criterion 3: e.g., "clinician review rejects tone/content">

Probes
------
<seed-level FEASIBILITY probes, INLINE and visible: novelty landscape, prior
interventions, external-data obtainability — one line per PP with status;
cards in _PROBE/; internal-data needs are [FORWARD -> CLAIMS] pointer lines
in _LOG_0-seed.md, NOT probes>
```

Artifact formatting: `=====` title / `-----` sections (no `#` headings); one sentence per line. Venue-FREE: the seed survives retargeting; the channel hunch is context, not a commitment.

Phases
=======

```
DRAFT   settle the six sections with the user (haipipe-application-draft).
        MAY WebSearch inline to ORIENT (crowded space? prior interventions?
        benchmark rates?) — the result is drafting fuel: weave it into the
        prose as orientation AND buffer the feasibility probes as
        `status: planned` PP skeletons (empty refs). NEVER write
        findings/refs into a PP card here — that is PROBE's job. When the
        draft surfaces an INTERNAL-data question (our own cohort /
        engagement data), register a `[FORWARD -> CLAIMS] PPNN_<slug>`
        pointer line in _LOG_0-seed.md (need + why; no card, no dispatch).
PROBE   FEASIBILITY probes only, mode light — they answer "can this
        intervention exist at all?": is it NOVEL (landscape / prior
        interventions / 查新) and is the EXTERNAL data OBTAINABLE
        (benchmarks, field norms, outside labeled data). ALWAYS run the
        real worker — this stage does EXACTLY ONE thing here:
            Skill("haipipe-application-probe", args="from-buffer <intervention_root>")
        The worker owns everything downstream: PP card creation, index
        bookkeeping, project-root resolution, dispatch, refs backfill.
        THIS STAGE NEVER does evidence work itself — inline WebSearch was
        fine in DRAFT as orientation fuel; here in PROBE it is FORBIDDEN
        (durability is the whole point). Evidence produced any other way
        has no project-side ledger and is void: the PROBE phase did not
        happen. Skip only by an explicit logged verdict.
REVISE  tighten wording; weave probe takeaways into the Probes section
        (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

If the intervention folder does not exist, route to `/haipipe-application enter <path>` (get-or-create owns scaffolding).

Probe scope and FORWARD handoff
================================

**Seed probes are FEASIBILITY only.** A seed probe answers "can this intervention exist at all?" -- novelty (is the angle new, or did a prior intervention already try it?) and external-data obtainability (do the outside benchmarks / field norms / labeled data the intervention needs exist and are they accessible?). Both are `discover` (lit/landscape) work.
Profiling OUR OWN data (the intervention's cohort size, engagement rates, field coverage) is `task` work that belongs in the evidence LADDER (rung 1a-descriptions). When DRAFT surfaces an internal-data question, DO NOT open a seed probe for it -- record a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in `_LOG_0-seed.md` (token unchanged for grep-stability; need + why; a pointer, NOT a probe card, no dispatch); it fires when the ladder opens. Rung 1a CONSUMES these pointers at its DRAFT open (data-profile needs -> 1a probe plans; verdict-shaped needs -> planned PP skeletons in 1c's Probes section) -- an unconsumed pointer fails the 1a CHECK. This keeps the seed's cost bounded to the feasibility question and stops the seed from doing ladder evidence work early.
**DRAFT may search; PROBE must dispatch.** Inline WebSearch is legitimate DRAFT fuel (orientation -> prose + buffered `status: planned` PP skeletons), but it is NEVER evidence. The PROBE phase must ALWAYS run the real worker (`Skill(haipipe-application-probe, from-buffer ...)`); inline results with no project-side ledger mean the PROBE phase did not happen. The invariant that separates the two is card state: planned skeleton (DRAFT) vs `read` + resolving refs (PROBE), mechanically enforced by `check-probe-cards.sh` at the probe worker's VERIFY step and the CHECK gate.

Definition of done
===================

```
[ ] 0-lifecycle/0-seed/0-seed.md exists and has all 6 sections
[ ] Kill criteria has at least 2 concrete conditions
[ ] Audience and channel hunch are specific (not "everyone" / "any channel")
[ ] Probes section carries at least the novelty/landscape takeaway; internal-data
    needs appear only as [FORWARD -> CLAIMS] pointer lines in _LOG_0-seed.md,
    never as seed probe cards
[ ] Probe cards verify clean: locate the checker layout-agnostically (installed
    skills flatten the tree, so a relative path is NOT reliable) --
    CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -path "*haipipe-application-probe/check-probe-cards.sh" 2>/dev/null | head -1)
    then sh "$CHK" <intervention_root> exits 0 (refs resolve project-side --
    the gate RUNS the checker and shows its output; it never eyeballs cards)
```

Handoff: `promote -> /haipipe-application ladder` (the 1a-1d sweep; or `descriptions` to start rung-by-rung). End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 0-seed/ stage folder only.
