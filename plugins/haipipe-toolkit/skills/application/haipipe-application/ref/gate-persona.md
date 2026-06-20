Gate Persona — Reviewer Voice for SOFT Gates
==============================================

Controls how strict each SOFT gate is about approving forward motion.
Set once at session creation, locked for the session by default.

Stored in `SESSION_STATE.gate_persona`. Read by
`haipipe-application-gate` at every firing to compose the reviewer
voice.

ONLY applies to SOFT gates inside application (G-plan / G-observe
/ G-claim / G-draft / G-review / etc.). HARSH gates upstream
(task CODE_REVIEW, probe review/integrity/claim) ignore
persona — they enforce minimum bars regardless.


Three composition layers
=========================

```
preset (Tier 1)  +  axes (Tier 3)  +  notes (Tier 2)  →  persona block
```

Tier 1 — preset (required):

| Preset      | strictness | ambition | Default route when in doubt |
|-------------|-----------:|---------:|-----------------------------|
| `strict`    |          8 |        4 | `revise plan`               |
| `balanced`  |          5 |        5 | `revise plan`               |
| `creative`  |          3 |        8 | `approve`                   |
| `lenient`   |          2 |        3 | `approve`                   |

`balanced` is the default for new sessions.

Tier 3 — axes (optional 0-10 integer overrides):

```
strictness    evidence bar; concrete thresholds below
ambition      richness bar; tone-only (the gate LLM interprets)
```

Tier 2 — notes (optional free text):

```
Short string prepended verbatim to the persona block.
e.g. "Act as Reviewer 2 at a top clinical journal"
     "Trust the user's intuition more than the numbers"
```


Concrete strictness thresholds
================================

Applied at the gate's sufficiency check:

| strictness | Evidence bar for categorical claims                               |
|-----------:|-------------------------------------------------------------------|
|        0-3 | Directional language is fine; narrative judgment allowed.         |
|        4-6 | Point estimates + n required; CI encouraged.                      |
|        7-8 | CI must exclude the target to make a categorical claim;           |
|            | otherwise mark as "directional / CI-limited".                     |
|       9-10 | CI must exclude target AND n must meet a stated minimum;          |
|            | otherwise `revise plan`.                                          |

`ambition` is tone-only — higher values mean the gate pushes the
session toward richer claims, named hypotheses, and follow-up
questions, and is less willing to approve minimal "contract-met"
artifacts.


How to compose the persona block
=================================

At Step 1 of `haipipe-application-gate`, read `SESSION_STATE.gate_persona`
and compose a block like:

```
You are reviewing as persona: balanced
  strictness = 5/10 — point estimates + n required; CI encouraged
  ambition   = 5/10
  
Notes: Trust the user's intuition more than the numbers.
```

This block is prepended to the LLM-call that generates the gate's
proposal (approve / revise / done).


User overrides
===============

```
At session creation (CLI flags):
  --persona strict
  --persona balanced
  --strictness 7 --ambition 6
  --persona-notes "Act as Reviewer 2"

Persisted in SESSION_STATE.gate_persona; locked thereafter.

One-off gate override (advanced):
  User reply at a specific gate may include "--persona-override strict"
  to apply a stricter persona just for that gate firing. The
  SESSION_STATE.gate_persona itself is NOT modified.
```


Legacy default
===============

If `gate_persona` is missing from SESSION_STATE (pre-persona session),
default to:

```json
{ "preset": "balanced", "strictness": 5, "ambition": 5, "notes": "" }
```

Log the default in `tmp/migration-<ISO>.log`.
