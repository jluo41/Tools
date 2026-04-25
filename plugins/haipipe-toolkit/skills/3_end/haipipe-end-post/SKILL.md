---
name: haipipe-end-post
description: "PostFn specialist — design and review of the response-formatting function in an Endpoint_Set. One of 5 inference Fn-types. Called by /haipipe-end orchestrator when intent references PostFn, response formatting, post-processing, or `post` keyword. Reads own ref/concepts.md plus umbrella's fn/fn-design.md and endpointset's fn/fn-review.md."
argument-hint: [verb] [use_case] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-post
========================

Per-Fn-type specialist for **PostFn** — the inference function that
formats the model's raw prediction into the wire response shape
returned to the caller. One of the 5 inference Fn-types inside an
Endpoint_Set. See `ref/concepts.md` for PostFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each PostFn impl is scoped to ONE response shape (CGM forecast, optimal-
                message bandit / holistic, R3 SMS lineups, weight-loss multi-label,
                xgboost multi-models). `design` and `review` take a use_case argument.

---

Commands
--------

```
/haipipe-end-post                                       -> show PostFn ref (concepts mode)
/haipipe-end-post concepts                              -> same
/haipipe-end-post list                                  -> list known use-case impls in fn_post/
/haipipe-end-post design <use_case> [endpoint_set]      -> scaffold a new PostFn for <use_case>
/haipipe-end-post review <use_case> [endpoint_set]      -> structural audit of one use-case impl
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_post/, as of 2026-04-25)
--------------------------------------------------------------------------------

```
CGMForecast_v260101                              CGM forecast response
OptimalMessage_Bandit_v250620                    bandit-driven optimal message
OptimalMessage_Bandit_Greedy_v250620             bandit (greedy variant)
OptimalMessage_Bandit_ABCTest_v250620            bandit (ABC test variant)
OptimalMessage_Holistic_Greedy_v250721           holistic (greedy variant)
OptimalMessage_Holistic_ABTest_v250721           holistic (AB test variant)
OptimalMessage_Holistic_ABCTest_v250721          holistic (ABC test variant)
R3sms_9o20_ArmGreedy_v250922                     R3 SMS 9-of-20 greedy
R3sms_9o20_ArmGreedyRandom_v250922               R3 SMS 9-of-20 greedy + random
R3sms_9o20_ABTest_v250922                        R3 SMS 9-of-20 AB test
WeightLossMultiLabel_PostFn_v260305              weight-loss multi-label
WeightLossMultiLabel_Af1M_PostFn_v260310         weight-loss (Af1M variant)
WeightLossMultiLabel_v3_PostFn_v260316           weight-loss v3
XgboostMultiModels_PostFn_v0610                  xgboost multi-model ensemble
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_post/")`
and ask the user to pick.

---

Dispatch Table
---------------

```
Verb       Reads
---------- ------------------------------------------------------------------
design     ref/concepts.md
           ../haipipe-end/fn/fn-design.md
           ../haipipe-end/ref/0-overview.md
review     ref/concepts.md
           ../haipipe-end-endpointset/fn/fn-review.md
concepts   ref/concepts.md  (only)
```

---

Step-by-Step Protocol
----------------------

Step 0:  Read `ref/concepts.md` — PostFn semantics, response schema, formatting rules.
Step 1:  For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2:  Execute the procedure scoped to PostFn.
Step 3:  Emit the structured tail.

---

Scope
------

Owns:
  - PostFn concept ref (`ref/concepts.md`)
  - PostFn design + review scoped to ONE Fn-type

Does NOT own:
  - Other 4 Fn-types — sibling skills `-meta`, `-trig`, `-src2input`, `-input2src`
  - Whole-artifact verbs — `/haipipe-end-endpointset`
  - Deployment — `/haipipe-end-deploy-*`
