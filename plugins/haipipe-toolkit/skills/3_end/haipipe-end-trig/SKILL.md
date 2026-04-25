---
name: haipipe-end-trig
description: "TrigFn specialist — design and review of the trigger-detection function in an Endpoint_Set. One of 5 inference Fn-types. Called by /haipipe-end orchestrator when intent references TrigFn, trigger detection, or `trig` keyword. Reads own ref/concepts.md plus umbrella's fn/fn-design.md and endpointset's fn/fn-review.md."
argument-hint: [verb] [use_case] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-trig
========================

Per-Fn-type specialist for **TrigFn** — the inference function that
decides whether (and when) to run prediction based on incoming data.
One of the 5 inference Fn-types inside an Endpoint_Set. See
`ref/concepts.md` for TrigFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each TrigFn impl is scoped to ONE input cadence (e.g., CGM 5-minute
                stream, weight day entry, generic any-invocation). `design` and `review`
                take a use_case argument.

---

Commands
--------

```
/haipipe-end-trig                                       -> show TrigFn ref (concepts mode)
/haipipe-end-trig concepts                              -> same
/haipipe-end-trig list                                  -> list known use-case impls in fn_trig/
/haipipe-end-trig design <use_case> [endpoint_set]      -> scaffold a new TrigFn for <use_case>
/haipipe-end-trig review <use_case> [endpoint_set]      -> structural audit of one use-case impl
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_trig/, as of 2026-04-25)
--------------------------------------------------------------------------------

```
AnyInv_v250205         generic any-invocation trigger (always fires)
CGM5Min_v260101        CGM 5-minute stream trigger
WeightDayEntry_v260305 weight day-entry trigger
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_trig/")`
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

Step 0:  Read `ref/concepts.md` — TrigFn semantics, condition evaluation, gate logic.
Step 1:  For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2:  Execute the procedure scoped to TrigFn.
Step 3:  Emit the structured tail.

---

Scope
------

Owns:
  - TrigFn concept ref (`ref/concepts.md`)
  - TrigFn design + review scoped to ONE Fn-type

Does NOT own:
  - Other 4 Fn-types — sibling skills `-meta`, `-post`, `-src2input`, `-input2src`
  - Whole-artifact verbs — `/haipipe-end-endpointset`
  - Deployment — `/haipipe-end-deploy-*`
