Interrogation Battery -- rung 1a's GROW-loop engine
====================================================

Why this file: "loop until you really know the data" is enforceable only if (a) each round generates questions a DIFFERENT way (the lenses), and (b) "really know" has a test (the blind battery + the dry rule). The 1a skill runs this engine every round; sessions must not improvise a weaker version.

The round engine
-----------------

1. GENERATE   run this round's lens (schedule below) as a question storm: >=10 questions about the data. Fresh-eyes option: spawn a cheap read-only subagent that sees ONLY the schema + the current 1a doc -- it asks what the incumbent stopped asking.
2. FILTER     each question -> answerable from existing D entries (cite the id)? discard. Not answerable -> a new D slot + a planned probe skeleton.
3. RELEASE    end the lap with the release menu (draft worker step 5); the user picks; only picks dispatch (probe worker STEP 1.5).
4. LAND       released probes return; TRANSLATE writes D entries + the `_DESCRIPTIONS/DS<n>` sheet (values-lane redirect).
5. SELF-TEST  answer the blind battery (below) from D entries ONLY, one resolving D id per answer. Any stumble = a new topic; the loop continues.
6. DRY RULE   a full round whose storm + self-test add ZERO new topics = saturated. Venue-scaled (wiki/08): light = one clean round; medium = one dry round; full = two consecutive. Log every lap as `[ROUND n]` in `_LOG`.
7. GATE LENS  at CHECK the user is asked "which data topics are still missing?" (JL: "after the check, they can think about adding more probes in the draft"). A `grow` verdict converts the answers to new slots + probes and re-opens DRAFT as `[ROUND n+1]`. Approve = saturated AND the user added nothing.

Lens schedule (rotate; wrap around if rounds outlast lenses)
--------------------------------------------------------------

- round 1  SCHEMA lens        which fields/groups have no D entry and no waiver? (drives Field Disposition to 100%)
- round 2  DISTRIBUTION lens  for every profiled stat: spread, extremes, missingness, concentration -- not just the mean
- round 3  CROSSING lens      outcome x time, outcome x geography, arm x demographic, outcome x clinical context
- round 4  SURPRISE lens      what result would surprise us? check it; what would fire the seed's kill criteria early?
- round 5  FIELD lens         what do comparable studies profile that we have not? (discovery route)
- at gate  USER lens          the CHECK ask above -- the user's questions outrank every automated lens

Blind battery (the "really know the data" test)
------------------------------------------------

Answerable from D entries only, one resolving D id each:

- WHO is in the data (cohort N, demographics) and who was excluded?
- WHAT treatments/arms exist and how are units distributed across them?
- WHAT outcomes exist and what are their base rates -- all of them, not just the primary?
- WHEN does the data cover (window, waves, seasonality) -- or which waiver says why not?
- HOW CLEAN is it (missingness of load-bearing fields, filter survivorship)?
- HOW does the segment compare to its benchmark (population / external)?
- WHAT is deliberately not profiled (waivers + exclusions), and why?

Rails
------

- Question storms and self-tests are DRAFTING FUEL: no numbers land from them; released probes are the only door for data (draft worker step 5, probe worker STEP 1.5).
- Schema sweeps read column names ONLY -- never data values (PHI rail).
- Saturation earns promotion to 1b; impatience does not. CHECK still gates.
- GROW grows PROBES, not folders: new topics on the same dataset usually land as new CONFIGS (or added outputs) of the existing profiling task -- the granularity ladder (config > task > group) rides in every dispatch (probe worker task_landing). Same for new SEGMENTS or same-shape datasets (young_female after young_male): tasks stay segment-agnostic, the slice is a config key -- the whole battery re-runs on a new cohort by adding configs/<variant>.yaml + runs/run_<variant>.sh, never by re-scaffolding.
