---
name: haipipe-end-meta
description: "MetaFn specialist — design and review of the model-metadata-lookup function in an Endpoint_Set. One of 5 inference Fn-types. Called by /haipipe-end orchestrator when intent references MetaFn, model metadata, model card, or `meta` keyword. Reads own ref/concepts.md plus umbrella's fn/fn-design.md and endpointset's fn/fn-review.md."
argument-hint: [verb] [use_case] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-meta
========================

Per-Fn-type specialist for **MetaFn** — the inference function that
returns model metadata (model name, version, description, signature)
without running prediction. One of the 5 inference Fn-types inside an
Endpoint_Set. See `ref/concepts.md` for MetaFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each MetaFn impl is scoped to ONE product use case (CGMDecoder, SMS,
                Bandit, WeightLoss, …). `design` and `review` take a use_case argument.

---

Commands
--------

```
/haipipe-end-meta                                       -> show MetaFn ref (concepts mode)
/haipipe-end-meta concepts                              -> same
/haipipe-end-meta list                                  -> list known use-case impls in fn_meta/
/haipipe-end-meta design <use_case> [endpoint_set]      -> scaffold a new MetaFn for <use_case>
/haipipe-end-meta review <use_case> [endpoint_set]      -> structural audit of one use-case impl
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_meta/, as of 2026-04-25)
--------------------------------------------------------------------------------

```
AutoMetaFn                                  generic auto-built MetaFn
BanditSMS_v250225                           SMS bandit
BanditSMSnNudge_v0620                       SMS+Nudge bandit
CGMDecoder_v260101                          CGM decoder (SageMaker)
CGMDecoder_DBR_v260101                  🚩  CGM decoder (Databricks variant)
SMSnNudge_v0620                             SMS+Nudge
SMSR2_13Messages                            R2: 13-message lineup
SMSR3_20Messages_SMSPersonalizeContent      R3: 20-message lineup with personalization
WeightLossMultiLabel_v260305                weight-loss multi-label
WeightLossMultiLabel_Af1M_v260310           weight-loss (Af1M variant)
WeightLossMultiLabel_OldFormat_v260318      weight-loss (legacy format)

🚩 = target-specific variant (Databricks)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_meta/")`
and ask the user to pick.

---

Dispatch Table
---------------

```
Verb       Reads
---------- ------------------------------------------------------------------
design     ref/concepts.md
           ../haipipe-end/fn/fn-design.md
           ../haipipe-end/ref/0-overview.md   (Endpoint_Set + pipeline context)
review     ref/concepts.md
           ../haipipe-end-endpointset/fn/fn-review.md
concepts   ref/concepts.md  (only)
```

---

Step-by-Step Protocol
----------------------

Step 0:  Read `ref/concepts.md` — MetaFn semantics, expected I/O, registry pointers.
Step 1:  For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2:  Execute the procedure scoped to MetaFn (do NOT touch other Fn-types).
Step 3:  Emit the structured tail (umbrella parses this):

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was designed/reviewed for MetaFn
artifacts: [paths to MetaFn files created or modified]
next:      suggested next command (typically: review, then sibling Fn-type)
```

---

Scope
------

Owns:
  - MetaFn concept ref (`ref/concepts.md`)
  - MetaFn design + review behavior scoped to ONE Fn-type
  - MetaFn-specific files inside `code/haifn/fn_endpoint/` and the Endpoint_Set

Does NOT own:
  - Other 4 Fn-types — sibling skills `-trig`, `-post`, `-src2input`, `-input2src`
  - Whole-artifact verbs (package / test / dashboard) — `/haipipe-end-endpointset`
  - Deployment to any target — `/haipipe-end-deploy-*`

If a design fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review` rather than patching here.
