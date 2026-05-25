Application Input Contract — reading K/W from E_insight
========================================================

How kind-specialists locate, load, and cite knowledge entries.


Where to read
==============

```
examples/<project>/insights/INDEX.md                gateway (always read first)
examples/<project>/insights/K_knowledge/INDEX.md    K-layer sub-index
examples/<project>/insights/W_wisdom/INDEX.md       W-layer sub-index
examples/<project>/insights/K_knowledge/K*.md       individual K entries
examples/<project>/insights/W_wisdom/W*.md          individual W entries
```

I/D entries are accessible but NOT primary citations for applications
— if you need them, descend through a K entry's `sources:` field.


Loading sequence (Phase 1)
===========================

```
1. Read insights/INDEX.md
   → identify topics matching intent (frontmatter tags)
2. Read K_knowledge/INDEX.md
   → enumerate K entries under matching topics
   → filter by status: active (skip superseded / contested unless explicit)
3. Read W_wisdom/INDEX.md
   → enumerate active W entries deriving from those K ids
4. Read full K*.md and W*.md for the shortlisted ids
   → ≤ 5 K + ≤ 3 W typical; if more relevant, ASK user to narrow
5. (Optional descent)
   If a K's claim needs evidence detail, follow its sources: → I/D entries.
   Otherwise skip — applications cite K/W, not raw observations.
```


Gap detection (Phase 2)
========================

After loading, run the gap check:

```
Gap signals → trigger Phase 3 (call /haipipe-insight ask):

(a) No active K covers a load-bearing claim the artifact needs.
(b) Active K exists but status=contested with conflicting sources.
(c) Active K covers it but for a different audience/subgroup than
    the artifact's audience (e.g., K validated on val but artifact
    targets test-od deployment).
(d) Multiple K conflict on the same claim with no superseding chain.

No-gap signals → proceed to Phase 5:

(a) ≥ 1 active K per load-bearing claim, status=active.
(b) Optional W gives an "act on this" recommendation matching intent.
```


Citation contract (Phase 5-6)
==============================

When citing in the artifact body:

```
audience=patient    plain language, no K-id in body
                    BUT frontmatter cited_K MUST list ids
audience=clinician  inline K-id: "Patients with high variability show
                    larger post-meal swings (K03)."
audience=regulator  footnote: "...post-meal swings.¹"
                    "¹ K03_lhm_film_overfit (high confidence)"
audience=designer   caption under sketch: "(motivated by K03, W02)"
audience=dev        code comment or doc block:
                    "# implements W02 (cites K03)"
audience=executive  endnote at bottom; minimize in-body marks
audience=partner    inline parenthetical: "(see K03)"
```


What NOT to do
===============

- DO NOT modify K/W entries during application drafting. If you think
  a K entry is wrong, raise it via `/haipipe-insight ask` — never edit
  insights/ directly from this skill family.
- DO NOT cite I or D entries directly in audience-facing copy. They are
  layer-internal; use K/W as the audience-facing layer.
- DO NOT cite a K with status=superseded as if active. If the user
  insists, mark the artifact `status: draft` + explain in "Open questions".
- DO NOT cite an exp_id directly. Experiments are the substrate of K;
  if you need to cite a specific experiment, cite the K that derives
  from it.


Triggering insight-session (Phase 3)
=====================================

When gap detected:

```
Skill("haipipe-application-ask", args="<Q>")

Q should be:
  - specific:    "Does K03 (FiLM overfit) hold for elderly patient subset?"
                 NOT "What about FiLM?"
  - load-bearing: tied to a concrete claim the artifact needs
  - bounded:     answerable by ≤ MAX_EXPERIMENTS (3) new experiments

Return contract: the session completes with status=answered (or
budget/blocked). Phase 4 re-reads INDEX to pick up new K/W.
```


Re-evaluation loop (Phase 4)
=============================

```
loop:
  re-read insights/INDEX.md (frontmatter updated_at > last_check)
  re-load relevant K/W
  if gap_resolved → Phase 5
  if gap_unresolved + budget_remaining → another insight-session OR
                                          mark draft + write Open Questions
  if gap_unresolved + budget_exhausted → return status=gap_unresolved
                                          with explicit list of unanswered Qs
```


Frontmatter trail
==================

After Phase 7 write, the artifact's frontmatter records the full trail:

```yaml
cited_K:      [K03, K07]
cited_W:      [W02]
triggered:    [insight_session_2026-05-25_film_elderly,
               experiment_15_film_age_stratified]
```

This makes the artifact reproducible: future readers can follow
`triggered` → experiment → K → I → D back to raw observations.
