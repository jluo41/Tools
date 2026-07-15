1-resource: <paper title> (what must EXIST for this paper to be testable)
=========================================================================

Date: YYYY-MM-DD
Status: DRAFT.
Venue-FREE. Exactly two sections: Demand and Questions. No sidecars.


Demand
------

What we MIGHT NEED. One `N<n>` per prerequisite the seed's Tentative Claim Shape implies.
Keyed on `H<n>`, never `C<n>` -- C-ids do not exist yet at resource time.
Scope is DATA + MODELS + PRODUCING-CODE alike: a corpus, a checkpoint, and "does code that emits metric X exist?" are the same kind of demand.

**N1 (H1)** <the resource, and the property that makes it usable for H1.>

**N2 (H1)** <a second prerequisite the same hypothesis needs.>

**N3 (H2)** <one per hypothesis; a demand with no obtainable resource is a SCOPE CUT, said out loud at the gate and logged in `_LOG`.>


Questions
---------

What we need to KNOW. One `Q<n>`, keyed to the N it serves.
Paper-space questions ONLY: no PP ids minted here, no probe topic -- the PROBE WORKER opens the section after the human approves the Q at GATE 1.
`-> PP<NN>` is a BACKLINK: it is written back into the Q once the PROBE WORKER has opened the question's SECTION, never invented by this stage.
The `A:` is BOTH the existence answer and the fitness answer, and it says what it KILLS.

**Q1 (N1)** <question -- does it exist, and can it carry N1?>

-> PP<NN>
A: <the answer -- existence AND fitness, and what it KILLS. A woolly A ("probably fine") is a DEFECT, not an answer.>

**Q2 (N1)** <question>

-> PP<NN>
A: <pending -- left blank until the answer lands.>

**Q3 (N2)** <a BUILD question -- can we build what we do not have?>

-> PP<NN>
A: COMMISSIONED · owner <name> · eta YYYY-MM-DD · blocks N<n> · cross-project: <sibling-project path | none-found>
   <what the build yields, and what it does NOT fix.>


```text
REFERENCE -- worked example, NOT part of the artifact. Delete on copy.
Paper-CGMtoAge, as of the morning of 2026-07-07 (PP02/PP03 had landed; PP04 had NOT
yet dispatched). This is what the stage would have said, and PP04 would not have run.

    Demand
    ------

    **N1 (H1)** A CGM corpus with age -- at a LIFESPAN range. A clock needs age VARIANCE.
    **N2 (H1)** A CGM foundation-model rep to freeze, plus a non-deep baseline to beat.
    **N3 (H2)** Age-related OUTCOMES co-measured with CGM.
    **N4 (H3)** A cohort co-measuring CGM with an established clock (PhenoAge / Horvath).


    Questions
    ---------

    **Q1 (N1)** Do we have a CGM corpus with age labels? What age range?

    -> PP02
    A: AIREADI @v0 · N=2021 · age 60.9±11.2 · range 40-94 · ZERO under-40s.
       CANNOT CARRY N1 -- range-restricted, so this is a mid-to-late-life clock, not a
       lifespan clock. A fit here returns a null BY CONSTRUCTION.
       DO NOT DISPATCH A FIT ON THIS ALONE.

    **Q2 (N1)** What else has CGM + age? Any young/healthy tail?

    -> PP03
    A: CGMacros · N=45 · age 18-69 · 10 under-40. Too small to train.
       -> HELD-OUT EXTERNAL TEST, nothing more.

    **Q3 (N1)** Can we BUILD a wide-age corpus?

    -> PP05
    A: COMMISSIONED · owner JL · eta 2026-07-21 · blocks N1 · cross-project: none-found
       WellDoc N=2,576 · age 6-93 · +811 under-40 -> pooled ~4,642 · age 6-94.
       Widens N and AGE. Does NOT widen HEALTH (~0% healthy).
       New confound (T1D + paediatric).

    **Q4 (N2)** Does a masked-LM CGM backbone exist ANYWHERE?

    -> PP06
    A: Checkpoint NO. Pipeline YES --
       cross-project: ProjC-Model-1-ScalingLaw/tasks/A02_pretraining_mlm (9 subtasks)
       DECISION AT GATE 1b: (a) authorize reuse -> a RUN
                            (b) build -> GPU-WEEKS
                            (c) cut the MLM arm -> ONE SENTENCE

    **Q5 (N3,N4)** Does anything co-measure CGM with aging outcomes?

    -> PP07
    A: HPP / Pheno.AI · ~10,812 · CGM + ~2yr revisits.
       rung: APPLICATION -> DUA -> secure enclave. MONTHS OF CALENDAR.
       H2 and H3 are UNFALSIFIABLE until this lands.
       owner: UNASSIGNED · application: UNFILED

Read Q1's A again. That is the line that would have stopped PP04.
```
