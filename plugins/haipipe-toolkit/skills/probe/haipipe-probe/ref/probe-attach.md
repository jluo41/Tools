probe-attach - file scattered work into the evidence base
==========================================================

What this is
------------

A user has a scattered thought, a one-off task, or a quick search. They are NOT
thinking about probes. This judge runs at the moment that work is created and
FILES it, so nothing falls on the floor unfiled:

```
scattered work (task | discovery | loose idea)
        │
        ▼
   probe-attach judge
        │
        ├─▶ FILE under an existing probe        (attach: wire as evidence)
        ├─▶ OPEN a new drawer                   (new probe: ask one confirm)
        └─▶ SHELF as standalone                 (no probe: infra/prep/display - still logged)
```

The point is filing, not gatekeeping. Even "no probe" work is recorded, so the
evidence base stays organized instead of accumulating orphan tasks (which is the
default failure: ProjB had 15 tasks, 1 broken probe, nothing filed).

Front door: `/haipipe-probe file "<thought-or-work>"`. Also auto-invoked by
`haipipe-data` (on task create) and `haipipe-discover` (on discovery create).


Disposition rules
-----------------

Three dispositions. The first two wire a ref; the third only logs.

```
ATTACH      work shares an existing probe's claim topic → add it as that probe's evidence
NEW         work is claim-bearing but no probe fits      → propose a ready probe.yaml stub, ASK
STANDALONE  work is not claim-bearing                     → no probe; log reason; shows in dashboard UNLINKED
```

Auto-apply ATTACH and STANDALONE (low stakes) and report them. NEW is a
commitment - propose a filled stub and take one confirm; never auto-create a probe.


Step 1 - classify modality
--------------------------

From the work's words (slug + description):

```
search · lit · literature · prior art · "what's known" · web · benchmark · landscape
                                                              → DISCOVERY
run · regress · train · compute · build · pipeline · extract · case · display · load
                                                              → TASK
"does X affect Y" · "is X better" · "test whether" · "effect of" · a bare hypothesis
                                                              → IDEA (already claim-shaped)
```


Step 2 - claim-bearing gate
---------------------------

Decides ATTACH/NEW vs STANDALONE. A piece of work is claim-bearing if it
tests or supports a falsifiable comparison or effect.

```
claim-bearing TASK signals:    reg/regression · vs/versus · effect · ablation ·
                               compare · treatment/control · trait-on-outcome estimate
NOT claim-bearing TASK signals: pipeline · build · extract · external/dimension/lookup ·
                               case/casedata construction · display/figure/table/report ·
                               setup · load   → STANDALONE (it FEEDS claims, is not one)
DISCOVERY:  usually claim-bearing (it informs or settles a claim)
IDEA:       always claim-bearing
```


Step 3 - match against existing probes (executable)
---------------------------------------------------

```
1. salient keywords: pull 3–6 from the work (trait/entity names, outcomes,
   cohorts, methods, domain terms). e.g. "regress agreeableness on MME in cancer"
   → {agreeableness, MME, opioid, cancer, regression}
2. candidate probes: find probes -name probe.yaml, exclude */_archive/* and
   */<YYYY>-archive/*
3. grep is only a CANDIDATE FILTER, never the decision: `grep -ic` each keyword
   in the probe.yaml just to find probes worth inspecting. Do NOT pick by score.
4. STRONG match has a hard rule for a RELATIONAL claim (X affects Y): BOTH halves
   must appear in a claim-level field (claim.target_sentence / claim.hypothesis / claim.scope):
     - the driver/entity (e.g. trait = agreeableness), AND
     - the OUTCOME (e.g. opioid/MME).
   One half alone is NOT strong. This is the load-bearing rule - without it,
   "trait" matches everything (every cohort task has "Trait" in its name and the
   opioid probe greps 8 hits on "trait"), so trait→diabetes would wrongly attach
   to the trait→opioid probe. The outcome half (diabetes/NDC = 0 hits anywhere)
   is what correctly routes it to NEW.
```


Step 4 - decide
---------------

```
STRONG (entity AND outcome at claim level)  → ATTACH to that probe
no STRONG + claim-bearing                   → NEW probe (but dedup first, below)
not claim-bearing                           → STANDALONE
ambiguous (2+ probes tie STRONG)            → ASK which probe, don't guess
```

STRONG is restated inline on purpose: never read it off the grep score from Step 3.
Both halves of the pair must sit in a claim-level field, or it is not STRONG.

Dedup before NEW: a probe may not exist yet but may already be PROPOSED. Before
proposing NEW, grep `probes/FILING.md` for a prior NEW with the same claim topic
(same entity+outcome pair).

If the prior row points to a real `probes/<MMDD>_<slug>/probe.yaml`, ATTACH to
that existing probe.

If the prior row points to a placeholder such as `P.06xx_trait-diabetes`, do
NOT treat it as an existing probe and do NOT write `evidence_refs` to any active
probe. Instead:

```
DEDUP-PROPOSAL → ask whether to materialize/select the real probe folder
              → only after confirmation, create/select the probe
              → then attach the evidence to that real probe
```

This avoids silently attaching evidence to a non-existent proposal while still
preventing duplicate trait→diabetes proposals.


Step 5 - file it (the well-filed part)
-----------------------------------

The writes per disposition. ALWAYS also append one line to `probes/FILING.md`.

```
ATTACH task       → probe.yaml: add path to evidence_refs.tasks[].
                    Wire the path that RESOLVES on disk - if the probe's existing
                    ref is stale (renamed away), attaching the live path repairs
                    the drift the dashboard flagged.
ATTACH discovery  → probe.yaml: add to evidence_plan.discoveries[] (role) +
                    evidence_refs.discoveries[].
NEW probe         → after user confirmation, scaffold
                    probes/<MMDD>_<slug>/probe.yaml via Plan, with
                    claim.target_sentence seeded from the work and the work as
                    first evidence_ref.
DEDUP-PROPOSAL    → no probe write yet. Ask to materialize/select the proposed
                    probe before attaching evidence.
STANDALONE        → no probe write. Record disposition so the dashboard's un-probed
                    scan classes it as "standalone (reason)" not "gap".
```

If an ATTACH has no NEW on-disk artifact (e.g. a loose idea that just restates an
already-wired arm), the `FILING.md` row is the only write - do not add empty
`evidence_refs:` blocks. The row records the thought; the wiring already exists.

Idempotent scaffolding - create what is absent, do not assume it exists:
  - `probes/FILING.md` may not exist → create on first filing.
  - `discoveries/` may not exist → scaffold before an ATTACH-discovery.
  - a probe may lack `evidence_refs:` / `evidence_plan:` blocks → ADD the key,
    do not just append to a missing list.

`probes/FILING.md` - append-only archive of every scattered-work decision (this
IS the user's idea archive):

```
## YYYY-MM-DD
- tasks/R01_Reg_TraitOpioid           → ATTACH P.0605 (trait→opioid, claim-level match)
- tasks/R02_Reg_TraitDiabetesNDC      → NEW P.06xx_trait-diabetes (claim-bearing, no probe fit)
- tasks/R02_Reg_TraitDiabetesNDC      → DEDUP-PROPOSAL P.06xx_trait-diabetes (confirm materialize before attach)
- tasks/A11_CMS-pipeline              → STANDALONE (data prep; feeds claims, is not one)
- discoveries/L0x_personality-rx-lit  → ATTACH P.0605 (prior_art_check)
```

(STANDALONE rows are intentional, not gaps. The dashboard reads FILING.md so it
nags only about claim-bearing work that is still un-probed.)


Report format
-------------

```
🗂  probe-attach: <one-line work description>
   modality:    task | discovery | idea
   claim-bearing: yes | no
   match:       <P.id> (STRONG: claim shares <topic>)  |  none
   → disposition: ATTACH P.0605   |   NEW P.06xx (confirm?)   |   DEDUP-PROPOSAL P.06xx (materialize?)   |   STANDALONE (reason)
   filed:       probes/FILING.md  (+ probe.yaml ref, if attach/new)
```


Hook points
-----------

```
/haipipe-probe file "<nl>"     front door: classify + file a loose thought/work
haipipe-data   (task create)   auto-call after scaffolding a task folder
haipipe-discover (disc create) auto-call after scaffolding a discovery
```

Run it at creation time, not later - filing a thought while it is fresh is the
whole point. The no-arg dashboard (UNLINKED EVIDENCE) still surfaces anything that slipped.
