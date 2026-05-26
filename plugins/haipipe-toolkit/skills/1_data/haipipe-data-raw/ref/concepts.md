Layer 0': Raw Cohort
====================

Architecture Position
---------------------

```
                                ExternalStore (sideways pantry of dimensions)
                                         │
                                         ▼
  Layer 0': Raw  ───►  Layer 1: Source  ───►  Layer 2: Record  ───►  ...  ───►  Layer 6: Endpoint
  (this skill)
```

A raw cohort lives at `_WorkSpace/0-RawStore/<cohort_name>/` as a single
extract from upstream — vendor delivery, internal ETL run, partner
data drop, device export, registry pull, etc. The skill is
domain-agnostic: a cohort can be a CGM stream, an EHR encounter table,
a claims line file, a sensor / wearable session log, a messaging or
engagement extract, a survey panel, etc. Typical contents:

```
_WorkSpace/0-RawStore/<cohort>/
├── *.parquet              ← actual rows (or .csv, multi-parquet)
├── data_description*.txt  ← what was extracted, by whom, with what
├── protocol_*.txt         ← study/extraction protocol, design notes
└── (other domain docs)
```

Distinct from neighbours:
  - `haipipe-data-external` owns ExternalStore — sideways pantry of
    dimension lookups (e.g. NPI / NDC / zip3 in US-healthcare contexts,
    device-model / station / SKU lookups in IoT or commerce contexts)
    joined into Stage 1+ assets.
  - `haipipe-data-source` owns Stage 1 — wraps the raw parquet into
    a HumanSet and lifts it into the pipeline.
  - `haipipe-data-raw` (this skill) owns the *upstream* of all that:
    the cohort-specific event extract itself, and the discipline of
    understanding it before it ever touches SourceFn.


Why Draw a Single-Data-Point Timeline
--------------------------------------

A column-level data dictionary doesn't tell you:

  - what real-world process generated each row
  - which events are observable vs invisible (fog of war)
  - where eligibility is mixed with engagement drop-off
  - which "treatment" knobs are pure vs joint experiments
  - what derived fields you must compute (because the upstream
    extract surfaces a *concept* without storing it as a column)

Without this, downstream analyses confuse content for timing, treat
eligibility cohort selection as engagement effect, etc.

The timeline forces a writer-reader to reason at the **business**
level (one patient, one event, one row), not at the **engineering**
level (which column writes what). Two distinct deliverables. This
skill produces the business one.


The 5-Zone Timeline Shape
--------------------------

Canonical zones (most cohorts have most of these):

```
┌── ⓪ PRE-T₀ ──┬── ① IN-DATA STAGE(s) ──┬── 🌫️ FOG ──┬── ② LATE-VISIBLE ──┐
│ background    │ events that stamp        │ events     │ signals that loop  │
│ events; not   │ visible columns          │ we don't   │ back into the      │
│ in parquet    │                          │ observe    │ data days/weeks    │
│               │                          │            │ later              │
└──────────────┴──────────────────────────┴────────────┴───────────────────┘

  🚫 CROSS-CUTTING:  events that fire any time after T₀ (opt-out, withdrawal),
                     orthogonal to the main flow.
```

For each zone capture:

```
  📋 events            what happens (in real-world / business terms)
  📋 columns stamped   which parquet columns get values (if any)
  📋 time scale        seconds / minutes / hours / days / weeks
  📋 visibility        ✅ observed   |   🌫️ inferred   |   ❌ unobserved
  📋 caveats           eligibility, drift, drop-off mixing, treatment confounders
```


The understand Procedure (iterative dialogue)
----------------------------------------------

This is the centerpiece function. The user is not just asking for a doc;
they are working out a mental model. Don't rush to produce the timeline.
Mistake the agent must avoid: writing a comprehensive draft on round 1,
then defending it. Each round, the user reveals nuance — restate, confirm,
THEN draft.

```
Step 4a: List cohort folder. Read every descriptive .txt.

Step 4b: Inspect parquet for grounding. Only what's needed:
         - row count, column list
         - key column value_counts (e.g. event_type, encounter_class,
           sensor_state — whatever the cohort's branch-deciding columns are)
         - null rates for branch-deciding columns (e.g. follow_up_*)
         Do NOT do exploratory analysis here — that's a different task.

Step 4c: First-round restate. Ask: "what is one row?" — confirm with
         user. Don't assume. Real possibilities span domains:
         - 1 CGM reading-window (e.g. 5-min sample / hourly aggregate)
         - 1 EHR encounter / 1 lab result / 1 medication order
         - 1 claims line / 1 visit / 1 evaluation
         - 1 sensor or wearable session
         - 1 messaging invitation / engagement event
         - 1 patient-day / 1 device-day / 1 user-session.

Step 4d: Sketch zones inline (chat, not file). Use placeholder events.
         Ask: "did I miss anything before T₀? after the last visible
         signal? any cross-cutting?"

Step 4e: For each zone, walk through 1-by-1. User often surfaces
         caveats only when looking at one zone at a time. Capture
         each caveat with WHY (the concrete reason it matters).

Step 4f: Validate every numerical claim against the parquet
         (uniqueness, prevalence rate, null rate) before committing.

Step 4g: ONLY when user signals alignment ("this is good", "save it"),
         write to <cohort>/datapoint-timeline.txt using
         templates/datapoint-timeline.txt as starting skeleton.
```

Common pitfalls to flag during the dialogue:

  - Treating dataset-level funnel rates as a single-individual story.
    A 100% → 60% → 40% → 1% drop-off chart describes a population,
    not one individual. (Applies equally to CGM wear funnels, EHR
    follow-up retention, clinical trial enrolment, app onboarding.)
  - Mixing eligibility (system / cohort gating decision) with
    operational drop-off (individual behaviour, device dropout, response
    refusal). These look identical in a binary 0/1 column but are
    causally different. Examples: "CGM not worn" can mean "device
    failed" vs "patient removed it"; "no follow-up encounter" can
    mean "patient ineligible for the program" vs "patient declined".
  - Forgetting joint experiments / multi-knob designs. A cohort
    branded as varying ONE dimension often actually varies several
    (e.g. timing × content in messaging, device firmware × wear
    protocol in CGM, clinic site × care pathway in EHR cohorts).
    Single-dimension analyses are confounded unless the other knobs
    are held fixed or stratified.
  - Confusing scheduled vs actual times. Schedulers jitter; what
    the system *intended* and what it *did* are different columns
    (or one column is missing entirely and must be derived). Common
    in messaging dispatch, CGM sensor session boundaries, EHR
    appointment scheduling, lab order vs result timestamps.


The review Checklist
---------------------

When auditing an existing `<cohort>/datapoint-timeline.txt`:

```
☐ Stage banner present at top with all zones, time scales, visibility marks
☐ Each zone has at least one event AND a caveat line (or explicit "none")
☐ Every column name in the doc actually exists in the parquet
☐ Every prevalence claim ("~50% of cohort") matches the parquet within ±2pp
☐ Eligibility flags marked distinctly from drop-off events
☐ Joint-treatment dimensions disclosed (if any)
☐ Derived concepts (column not stored, must compute) called out explicitly
☐ Source attribution at the bottom: which raw .txt each fact comes from
☐ Cross-cutting events (opt-out, withdrawal) on a separate axis, not
  jammed into one zone
☐ Time scales sanity-checked (event scale vs parquet date span)
```


The hand-off Procedure (Stage 0' → Stage 1)
--------------------------------------------

After the timeline is written and reviewed, derive what SourceFn must do:

```
Step 4a: Read <cohort>/datapoint-timeline.txt.

Step 4b: Extract from the timeline:
  - column names mentioned (these become candidate SourceFn outputs)
  - derived concepts (column not stored — SourceFn must compute or
    leave as TODO with upstream attribution)
  - eligibility flags (must be retained as separate columns, not
    collapsed into a single binary outcome flag)
  - fog boundaries (the SourceFn schema can include the LAST visible
    signal but should annotate it as "post-fog observation")
  - joint-treatment / multi-knob dimensions (cohorts that vary 2+
    factors; document so downstream stratifies correctly)

Step 4c: Match against ../haipipe-data-source/ref/concepts.md schema
         expectations.

Step 4d: Emit a checklist:
  • Columns SourceFn keeps verbatim
  • Columns SourceFn derives (with derivation rule from timeline)
  • Flags SourceFn must NOT collapse
  • Upstream asks (columns that should be added by the data team)
  • Notes for downstream Record / Case design
```

The output is a checklist file or chat report — NOT actual SourceFn
code. Hand off to `haipipe-data-source design-chef` for the code.


Three Classic Traps (worth concrete illustration)
--------------------------------------------------

These three traps motivated formalising this skill — each silently
corrupts downstream analysis if the timeline isn't drawn first. They
recur across domains; the patterns matter more than any one example.

  1. **Eligibility-vs-drop-off mixing**:
     A binary 0/1 column that conflates "individual was never eligible"
     with "individual was eligible but did not engage / data was lost".
     Causally different, statistically indistinguishable from the
     column alone.
     - CGM example: `wore_sensor=0` could mean "no prescription / not
       enrolled" OR "enrolled but removed device early".
     - EHR example: `had_followup=0` could mean "patient ineligible
       for the program" OR "eligible but did not return".
     - Messaging example: a "card shown" flag may be off because the
       patient/Rx was never eligible OR because the patient dropped
       off the funnel after auth.

  2. **Joint / multi-knob experiments**:
     A cohort branded as varying ONE treatment dimension actually
     varies several. Single-dimension analyses are confounded unless
     other knobs are held fixed or stratified.
     - Messaging example: a "timing" experiment that also varies
       message content via a separate model — the same dataset is
       effectively two experiments.
     - CGM / device example: device firmware version × wear protocol
       co-vary across study arms.
     - EHR example: care-pathway changes coincide with site or
       provider changes.

  3. **Scheduled vs actual time**:
     What the system *intended* and what it *did* live in different
     columns — or the scheduled timestamp is missing entirely and
     must be derived from a template + an offset rule. Actual delivery
     jitters from scheduled.
     - Messaging example: scheduled dispatch slot is a template;
       actual delivery time can drift by hours.
     - CGM example: sensor session "start" can be insertion time vs
       first valid reading; "end" can be last reading vs explicit
       removal event.
     - EHR example: appointment scheduled time vs check-in time vs
       provider-seen time; lab order vs collection vs result.

Reference Cohorts
------------------

Cohorts already living under `_WorkSpace/0-RawStore/` with a complete
`datapoint-timeline.txt` are the best worked examples — read whichever
matches your domain (CGM, EHR, claims, messaging, sensor, etc.). Each
one will illustrate the 5 zones plus a subset of the three traps above
in concrete column terms for that domain.
