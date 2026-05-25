---
name: haipipe-insight-wisdom
description: "W-level wisdom specialist of the haipipe-insight family. Reads K_knowledge entries (validated beliefs) and writes strategic recommendation entries to insights/W_wisdom/ — 'what we should DO next'. Each W entry is actionable: a proposed next experiment, a strategic re-direction, or a stop-doing-X. NO code. Use when running W-phase via /haipipe-insight-session, or directly /haipipe-insight-wisdom. Trigger: W-level, wisdom, recommendations, what next, strategic direction, action items."
argument-hint: [--project <path>] [--scope <knowledge-ids>] [--slug <slug>]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-wisdom
==============================

W-level of the Insight base (D → I → K → W). Reads validated knowledge
(K entries) and writes **actionable strategic recommendations**.

```
D — Observations:  "what we observed"
I — Patterns:      "what patterns emerged"
K — Knowledge:     "what we now believe is true"     (input)
W — Wisdom:        "what we should do next"           ← THIS SKILL
```

W is the bridge **from understanding to action**. Each W entry should
be actionable — translatable into either a new experiment (via
/haipipe-experiment), a research pivot, or a stop-doing-X decision.


Input
-----

```
examples/<project>/insights/K_knowledge/K*.md      (REQUIRED, ≥ 1)
examples/<project>/insights/I_patterns/P*.md       (optional context)
```


Output
------

```
examples/<project>/insights/W_wisdom/W{NN}_<slug>.md
```


Hard rules
----------

- W entries must be ACTIONABLE. "Should think about X" is too vague —
  prefer "Run experiment to test X under param-matched conditions",
  "Stop chasing the +1mg val improvement; it doesn't transfer to test-od",
  "Pivot main figure 3 to focus on FiLM generalization gap".
- Each W must cite ≥ 1 K it derives from.
- W entries decay — they're "what we should do now given what we know
  now". As K updates, W entries may become stale; mark them `status:
  stale` rather than delete.
- W never executes anything. To act on a W's recommendation, the user
  invokes /haipipe-experiment design new (or /haipipe-task task-folder)
  manually. /haipipe-insight-session can chain this.


Workflow
--------

```
Step 1: Parse args (--scope picks which K entries to derive from)
Step 2: Read scoped K entries (and their counter-evidence sections)
Step 3: Propose ≥ 1 candidate recommendation per K
Step 4: Triage (interactive; --auto picks top)
Step 5: Compose entry; atomic write
Step 6: Update INDEX.md and back-links
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "W layer" section).

Quick reminder for W entries:

```
frontmatter (≤ 13 lines):
  id, layer=W, tags, status, created, updated,
  rec, type, cost,
  sources, ref_by

body sections (in order):
  ## Recommendation    (1-2 paragraphs, sufficient detail to execute)
  ## How to act        (exact command / decision / next step)
  ## Why now           (timeliness; which K entries trigger this)
  ## Decay condition   (what would change our mind)

length: ≤ 120 lines total
```

The `rec` field in frontmatter is THE action in ONE sentence.
`type` enum: `next_experiment | research_pivot | stop_doing |
paper_direction`. `cost` qualitative: `cheap | medium | expensive`.
`status` flips to `acted_on` once user has executed the recommendation
(or to `stale` if it decayed without action).


Definition of done
-------------------

- [ ] `insights/W_wisdom/W{NN}_<slug>.md` written
- [ ] Recommendation is actionable (passes "could I write the command?" test)
- [ ] At least 1 K cited; counter-arguments engaged in "What would change..."
- [ ] NO Python written, NO command auto-executed (user must act)
- [ ] Back-links added to cited K entries


Risk profile
-------------

WRITES new file under `insights/W_wisdom/`. APPENDS to INDEX.md and
back-links. Suggests but does NOT execute /haipipe-experiment or
/haipipe-task commands — those are user actions.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "W02_<slug> written: 'Run param-matched LHM re-test'"
artifacts: [insights/W_wisdom/W02_<slug>.md, INDEX.md, back-links]
next:      Suggest user runs the recommended command
           (or /haipipe-insight-session can chain it directly)
```
