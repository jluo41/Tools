---
name: haipipe-end-post
description: "PostFn specialist -- designs/reviews the response-formatting function in an Endpoint_Set. One of 5 inference Fn-types. Called by /haipipe-end when intent references PostFn, response formatting, post-processing, or `post`."
argument-hint: "[verb] [use_case] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.1.1"
  last_updated: "2026-07-08"
  summary: "PostFn specialist — design and review of the response-formatting function in an Endpoint_Set."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-post
========================

Per-Fn-type specialist for **PostFn** — the inference function that formats the model's raw prediction into the wire response shape returned to the caller.
One of the 5 inference Fn-types inside an Endpoint_Set.
See `ref/concepts.md` for PostFn semantics.

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

Use cases (concrete impls in code/haifn/fn_endpoint/fn_post/, as of 2026-04-25 — discover current impls with ls code/haifn/fn_endpoint/)
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
R4sms_10o40_ArmGreedy_v260807                    R4 SMS 10-of-40 greedy (top-9 + default)
WeightLossMultiLabel_PostFn_v260305              weight-loss multi-label
WeightLossMultiLabel_Af1M_PostFn_v260310         weight-loss (Af1M variant)
WeightLossMultiLabel_v3_PostFn_v260316           weight-loss v3
XgboostMultiModels_PostFn_v0610                  xgboost multi-model ensemble
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_post/")` and ask the user to pick.

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

Step 0: Read `ref/concepts.md` — PostFn semantics, response schema, formatting rules.
Step 1: For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2: Execute the procedure scoped to PostFn.
Step 3: Emit the structured tail.

---

Guardrails (learned the hard way — do NOT skip)
------------------------------------------------

```
POST-1  An ARM-RESTRICTING PostFn must RAISE on a candidate that does not resolve.
        The `action_list_candidates` pattern filters a hardcoded name list by
        membership in the model's arm set:

            action_list = [i for i in action_list_candidates if i in action_list_full]

        A name that is absent is dropped SILENTLY. When SMSR4 expanded 20 arms ->
        40 and renamed one, a 3-name list became a 2-name list and the endpoint
        served `salience` on 6,513/6,513 live requests for months. The list was
        never wrong for the round it was written for; it was wrong for the round
        it was INHERITED into, and nothing in the code could tell the difference.
        Always assert first:

            _unresolved = [i for i in action_list_candidates if i not in action_list_full]
            assert not _unresolved, f'candidate arms absent from model output: {_unresolved}'

POST-2  One PostFn per (round, candidate set, policy). NEVER edit a shared impl
        in place. Count the manifests first:

            find . -name manifest.json | xargs grep -l '"PostFn": "<name>"'

        Nine manifests shared OptimalMessage_Holistic_Greedy_v250721, and its
        list was still CORRECT for SMSR3. Editing it to fix SMSR4 would have
        broken SMSR3. Fork with a dated name following the existing convention:
        `<Round>_<N>o<M>_<Policy>_v<YYMMDD>` (R3sms_9o20_ArmGreedy_v250922).

POST-3  A restricted candidate list constrains ONLY `action.name`. The response
        still carries every arm in `predictions[]`. So a broken candidate list
        leaves all scores correct and serves the wrong message: any check that
        compares only the returned SCORES cannot see it. Assert on the SERVED arm.
        (See haipipe-task guardrail GATE-1.)

POST-4  Derive the candidate list from an eval artifact at build time and assert
        it against a frozen expected list, rather than typing names in. A hand-
        typed list is what goes stale; a derived one regenerates and a drifted
        eval table then FAILS the build instead of shipping quietly.
```

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

Builder templates (code/scripts/haibuilder/)
---------------------------------------------

Copy-and-customize starting point for new PostFn builders:

```
code/scripts/haibuilder/6-endpoint/c1_build_postfn_weight_multilabel.py  ← WellDoc weight PostFn
```

Project-specific builders live in the task folder:
```
examples/<project>/tasks/C01_*/00_endpoint_set_fn_develop/c1_build_postfn.py
```
