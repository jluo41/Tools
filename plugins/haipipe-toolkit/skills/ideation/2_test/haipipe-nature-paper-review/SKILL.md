---
name: haipipe-nature-paper-review
description: >-
  Apply a Nature-family editorial lens to a tested research Idea: broad
  significance, conceptual advance, evidence decisiveness, cross-field
  accessibility, figure-led claim structure, robustness, and specialist
  journal rerouting. Use when asking whether an Idea is Nature-shaped or which
  Nature Portfolio target fits; current submission rules still require a
  verified Venue contract.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-08"
  capability_family: "2_test"
---

# /haipipe-nature-paper-review · Nature editorial-shape overlay

Load `haipipe-journal-fit`, the Idea Card, its novelty and pressure receipts,
and the candidate Venue Fit Card. This is a specialized editorial overlay,
not a static database of Nature rules. Load `haipipe-paper-venue` and current
official-source Discovery Results for binding scope, category, format, data,
code, ethics, fee, or submission claims.

## First resolve the target

"Nature paper" is ambiguous. Distinguish:

```text
Nature                         broad flagship editorial claim
Nature <discipline>            specialist scientific community and evidence floor
Nature Reviews <discipline>    synthesis/review promise rather than original study
Nature Communications         broad multidisciplinary research route
npj <discipline>               specialist application/community route
```

Do not assess a generic brand when the Idea actually belongs to a specific
journal and category. If target identity remains open, compare plausible
families provisionally and route final candidates to Venue contracts.

## Editorial lenses

Assess each lens independently:

| Lens | Question |
|---|---|
| broad significance | Why should readers outside the narrow dataset or subfield care? |
| conceptual advance | What changes in explanation, capability, or decision—not merely scale? |
| verified novelty | Which Core Claim survives the closest-work rejection? |
| evidence decisiveness | Does the design support the headline claim without a major inferential leap? |
| generality | Is the result likely to travel across populations, systems, or disciplines? |
| figure-led story | Can each central claim map to a decisive display, with one main claim per figure unless justified? |
| accessibility | Can the question, mechanism, and consequence be understood across fields without losing precision? |
| robustness/reproducibility | Are validation, negative results, source data, code, and availability expectations realistically supportable? |
| societal/clinical relevance | Is importance demonstrated rather than asserted, with harms and limits visible? |
| specialist reroute | Would a narrower Nature-family desk serve the actual audience better? |

The figure-led lens evaluates claim architecture at Ideation; it does not
write figures or manuscript prose.

## Verdict classes

- `plausible`: the Idea has a defensible Nature-family editorial shape and no
  currently visible fatal evidence gap;
- `upgrade-required`: the core shape is plausible but named scientific work
  must land before the target is credible;
- `specialist-reroute`: the contribution is strong but its natural audience is
  a narrower Nature-family or field journal;
- `not-nature-shaped`: the Idea may be publishable, but breadth, conceptual
  advance, or evidence decisiveness does not support this route;
- `hold`: target identity, closest work, evidence, or current rules are too
  incomplete for judgment.

These are editorial-shape readings, never acceptance predictions.

## Output receipt

Write `workflow/nature/<idea>_<timestamp>.yaml` with target/category, Venue
contract path/version, lens-by-lens status and evidence, strongest EIC
rejection, required scientific upgrades, specialist reroutes, rule gaps, and
verdict. An exact target/category is required for `plausible`,
`upgrade-required`, `specialist-reroute`, or `not-nature-shaped`. A route
assessment may use `target: unresolved` and `category: unresolved` only with
`verdict: hold`, explicit prerequisites, and no desk-rule claims. Link the
receipt from the Idea Card and Venue Fit Card.

Current official requirements remain `DESK RULE`; measured exemplars are
`PACK OBSERVATION`; this overlay's recommendation is `LOCAL DECISION` unless
supported by one of those sources.

## One-off mode

Return the lens table, verdict, strongest editorial objection, required
upgrades, and plausible specialist reroutes. Browse current official pages
before stating volatile submission rules and cite them directly.
