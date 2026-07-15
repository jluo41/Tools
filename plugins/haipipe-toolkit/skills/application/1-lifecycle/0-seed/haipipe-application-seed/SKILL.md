---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle (venue-FREE). Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel hunch, mechanism hypothesis, and kill criteria. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md; context needs are raised as question SECTIONS in 1-probes/ (serves: 0-seed). Markdown only. Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, kill criteria, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.3.1"
  last_updated: "2026-07-14"
  summary: "Stage 0 on the paper-aligned contract: stage FOLDER (0-seed.md + _LOG), venue-FREE marker, DPRC phases via 2-phase/ workers, scaffold via enter get-or-create (dead ref pointer removed). v3.2: DRAFT may WebSearch to orient (fuel -> prose + planned question sections), PROBE must ALWAYS run the real worker; seed probes are FEASIBILITY only (novelty + external-data-obtainable), internal-data profiling forward-points to CLAIMS via a _LOG pointer. v3.3.0 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): seed-level questions are SECTIONS in 1-probes/ (serves: 0-seed); the per-stage _PROBE/ folder is RETIRED. v3.3.1: BODY caught up with the frontmatter — the Phases block, the probe-scope rules and the done-criteria still told DRAFT to buffer `status: planned` PP CARDS and to backfill `refs` (both DELETED fields; the checker reads `state:`), so an agent obeying the body wrote a probe file the checker could not see. Now: question SECTIONS at `state: planned` with an EMPTY `target:`, the worker's five-step loop named, and the DRAFT/PROBE line drawn on SECTION STATE (`planned` + empty target vs `read` + a target: resolving to a QA file). 'takeaway'/'verdict' -> `a-consumer:`."
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
- The existing project bank (discoveries/ + tasks/) — read at the PROBE phase's
  MATCH step by grepping the bank's QA corpus ({tasks,discoveries}/**/QA/*.md).
  There is no gateway agent doing this sweep any more (retired 2026-07-14).
- Domain knowledge about the audience and channel

Output
=======

```
<intervention-root>/0-lifecycle/0-seed/0-seed.md
<intervention-root>/0-lifecycle/0-seed/_LOG_0-seed.md
<intervention-root>/1-probes/PPNN_<topic>.md            (feasibility questions, serves: 0-seed: novelty + external-data obtainability)
```

Seed artifact schema
=====================

```markdown
# Intervention Seed: <name>

## Opportunity
<2-3 sentences: what gap exists, what behavior we want to change>

## Expected impact
<directional estimate: "increase refill adherence by 5-15pp">

## Audience
<who receives this intervention: patient subset, clinician type>

## Channel hunch
<SMS, push, in-app UI, provider dashboard, email — a HUNCH, not a pin;
the venue decision happens after claims via /haipipe-application venue>

## Mechanism hypothesis
<one sentence: why this audience + this content might respond>

## Kill criteria
<conditions under which we abandon this intervention>
- <criterion 1: e.g., "no HTE detected in cohort data">
- <criterion 2: e.g., "click rate < 2% in pilot">
- <criterion 3: e.g., "clinician review rejects tone/content">

## Probes
<seed-level FEASIBILITY probes, INLINE and visible: novelty landscape, prior
interventions, external-data obtainability — one line per PP with status;
the questions live as SECTIONS in 1-probes/ (serves: 0-seed); internal-data
needs are [FORWARD -> CLAIMS] pointer lines in _LOG_0-seed.md, NOT questions>
```

Artifact formatting: `=====` title / `-----` sections (no `#` headings); one sentence per line. Venue-FREE: the seed survives retargeting; the channel hunch is context, not a commitment.

Phases
=======

```
DRAFT   settle the six sections with the user (haipipe-application-draft).
        MAY WebSearch inline to ORIENT (crowded space? prior interventions?
        benchmark rates?) — the result is drafting fuel: weave it into the
        prose as orientation AND raise each feasibility question as a
        question SECTION (`state: planned`, EMPTY `target:`) in the right
        topic's `1-probes/PPNN_<topic>.md`. NEVER write a finding or a
        `a-consumer:` into a section here — that is PROBE's job. When the
        draft surfaces an INTERNAL-data question (our own cohort /
        engagement data), register a `[FORWARD -> CLAIMS] PPNN_<slug>`
        pointer line in _LOG_0-seed.md (need + why; no section, no dispatch).
PROBE   FEASIBILITY probes only, mode light — they answer "can this
        intervention exist at all?": is it NOVEL (landscape / prior
        interventions / 查新) and is the EXTERNAL data OBTAINABLE
        (benchmarks, field norms, outside labeled data). ALWAYS run the
        real worker — this stage does EXACTLY ONE thing here:
            Skill("haipipe-application-probe", args="from-buffer <intervention_root>")
        The worker owns the whole five-step loop downstream: ORGANIZE the
        sections → MATCH the bank's QA corpus → DISPATCH the commission →
        POINT target: at the answering QA file → INTERPRET into a-consumer:.
        THIS STAGE NEVER does evidence work itself — inline WebSearch was
        fine in DRAFT as orientation fuel; here in PROBE it is FORBIDDEN
        (durability is the whole point). Evidence produced any other way
        has no project-side ledger and is void: the PROBE phase did not
        happen. Skip only by an explicit logged decision.
REVISE  tighten wording; weave each section's `a-consumer:` into the Probes
        section (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

If the intervention folder does not exist, route to `/haipipe-application enter <path>` (get-or-create owns scaffolding).

Probe scope and FORWARD handoff
================================

**Seed probes are FEASIBILITY only.** A seed probe answers "can this intervention exist at all?" -- novelty (is the angle new, or did a prior intervention already try it?) and external-data obtainability (do the outside benchmarks / field norms / labeled data the intervention needs exist and are they accessible?). Both are `discover` (lit/landscape) work.
Profiling OUR OWN data (the intervention's cohort size, engagement rates, field coverage) is `task` work that belongs in the CLAIMS stage. When DRAFT surfaces an internal-data question, DO NOT open a seed probe for it -- record a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in `_LOG_0-seed.md` (need + why; a pointer, NOT a probe section, no dispatch); it fires when claims opens. The claims stage CONSUMES these pointers at its DRAFT open -- an unconsumed pointer fails the claims CHECK. This keeps the seed's cost bounded to the feasibility question and stops the seed from doing claims-stage evidence work early.
**DRAFT may search; PROBE must dispatch.** Inline WebSearch is legitimate DRAFT fuel (orientation -> prose + question SECTIONS left at `state: planned`), but it is NEVER evidence. The PROBE phase must ALWAYS run the real worker (`Skill(haipipe-application-probe, from-buffer ...)`); inline results with no project-side ledger mean the PROBE phase did not happen. The invariant that separates the two is SECTION STATE: `planned` with an empty `target:` (DRAFT) vs `read` with a `target:` that resolves to a QA file in the bank (PROBE) -- mechanically enforced by `check-probe-cards.sh` at the probe worker's VERIFY step and the CHECK gate.

Definition of done
===================

```
[ ] 0-lifecycle/0-seed/0-seed.md exists and has all 6 sections
[ ] Kill criteria has at least 2 concrete conditions
[ ] Audience and channel hunch are specific (not "everyone" / "any channel")
[ ] Probes section carries at least the novelty/landscape reading; internal-data
    needs appear only as [FORWARD -> CLAIMS] pointer lines in _LOG_0-seed.md,
    never as seed probe sections
[ ] Probe files verify clean: locate the checker layout-agnostically (installed
    skills flatten the tree, so a relative path is NOT reliable) --
    CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -path "*haipipe-application-probe/check-probe-cards.sh" 2>/dev/null | head -1)
    then sh "$CHK" <intervention_root> exits 0 (every section's target: resolves
    project-side -- the gate RUNS the checker and shows its output; it never
    eyeballs the probe files)
```

Handoff: `promote -> /haipipe-application claims`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 0-seed/ stage folder only.
