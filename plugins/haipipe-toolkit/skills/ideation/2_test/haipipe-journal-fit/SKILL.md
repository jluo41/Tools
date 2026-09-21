---
name: haipipe-journal-fit
description: >-
  Compare a research Idea with plausible journals or conferences using a
  broad screen for every candidate and evidence-bound deep fit for live
  finalists. Use for journal targeting, article-type choice, desk-rejection
  risk, ambitious/realistic/fallback portfolios, or deciding where an Idea
  belongs; it never predicts acceptance or chooses the target for the user.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.2"
  last_updated: "2026-09-20"
  capability_family: "2_test"
---

# /haipipe-journal-fit · Idea × publication desk

Load `haipipe-ideation`, the target Idea Card, and its shared
`references/venue-fit.md`. Load `haipipe-paper-venue` for any named finalist
that needs deep fit. Discovery owns current official-source retrieval; a
remembered policy, ranking, skill pack, or search snippet is never a binding
desk rule.

For a durable commission, use the owner-bound Run Specs in
`../../haipipe-ideation/references/workflow-runs.md`. This capability's checks
are internal Steps unless separately commissioned under that contract.

## Pass 1 · broad screen

Every admitted Idea receives a retained screen:

```text
field and conversation
target readership and decision-maker
contribution type
method and evidence shape
likely article/category type
submission goal
obvious desk mismatch
candidate families and excluded families
```

The screen may end at a journal family when evidence is weak. Keep eliminated
screens so the same mismatch is not rediscovered later.

## Pass 2 · deep fit

For live candidates, compare a small defensible set of named targets. Each
finalist requires a current versioned Venue contract matching its exact
target and category. Evaluate:

1. scope and audience;
2. contribution significance;
3. verified novelty delta;
4. method and design fit;
5. evidence floor;
6. article or submission category;
7. generality and likely impact on the target readership; and
8. compliance, openness, data/code, and disclosure expectations.

For every dimension record `strong`, `conditional`, `weak`, `off-fit`, or
`unknown`, plus reason, authority class, and evidence ids. A single unknown
binding requirement keeps that part open; do not average it away.

## EIC challenge

Before recommending a target, write the strongest plausible desk-rejection
case:

- wrong reader or conversation;
- contribution too local, incremental, or technically narrow;
- evidence below the journal's expected floor;
- article type or manuscript container mismatch;
- claim too broad for the design;
- required openness, ethics, or reporting obligations cannot be met.

Then state which change, if any, repairs the mismatch. Distinguish a scientific
upgrade from a cosmetic reframing.

## Portfolio result

When supported, label targets `ambitious`, `realistic`, `fallback`, or
`reroute`. These are strategic roles, not rankings or acceptance
probabilities. The recommendation names one proposed target/category, its
conditions, and alternatives, while `human_target.status` remains `open`.

Write an immutable assessment snapshot to
`workflow/venue-fit/<idea>_<timestamp>.yaml` using the shared schema and its
`assessment_binding`, then project the current assessment to
`cards/venue-fit/<idea>_venue-fit.yaml`. Every deep-fit desk fact must resolve
through the named Venue contract; every local interpretation stays
`LOCAL DECISION`.

Each independent assessor gets a distinct snapshot and binding. For a durable
Run, inherit evaluator, rubric and frozen-input hashes through the Run's
`assessment_id`; for direct or one-off work, include the full binding inline
as described in `../../haipipe-ideation/references/receipts.md`. Preserve every
snapshot and list its `assessment_id`, receipt path and exact-byte SHA-256 in
the current Venue Fit Card's `assessment_receipts`. With one judgment, its
binding may be projected in `assessment_binding`; with multiple judgments,
leave that singular field null and point `review_resolution` to the resolution
receipt with its SHA-256. Unresolved dimensions and overall status remain
`unknown`, with `human_target.status: open` and a HOLD route. Do not average
fit labels or overwrite a review.

## Exit gate

Broad fit is complete when every admitted Idea has a retained family-level
screen. Deep fit is complete only when every named finalist has a matching
current Venue contract, all dimensions and desk risks are explicit, and every
unknown has a route. Target selection still belongs to a person in Stage 3.

## One-off mode

Follow the umbrella skill's one-off source route: reuse verified inputs,
otherwise use Discovery one-off search/read within the request; return links,
access dates and reading depth inline. Keep no-search/read-only restrictions.
Unavailable evidence means provisional/HOLD. Inline work creates no durable
portfolio or source bank unless the user asks to retain it.

Return the broad screen or comparison inline with official-source links,
access dates, article categories, desk risks, and uncertainty. If current
rules were not verified, label the result provisional rather than presenting
memory as policy.
Include the complete direct-mode `assessment_binding` inline. If multiple
reviewers are used, preserve their raw judgments and return the shared
`review_resolution` block; unresolved conflict remains HOLD.
