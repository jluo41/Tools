---
name: haipipe-norm
description: "The contract every describe-* normalizer obeys: free text in a cohort's own dialect, resolved against a reference bank, into numbers that carry their own provenance. Owns the five rules and the door signature; ships no code. Load before building or changing a normalizer. Trigger: normalizer contract, new normalizer, describe-food, describe-exercise, normalize door, provenance columns, basis column, haipipe-utils."
metadata:
  version: "0.4.0"
  last_updated: "2026-08-22"
  members: "describe-food (0.4.0) · describe-exercise (0.1.0) · describe-medication (0.1.0) · describe-insulin (0.1.0)"
---

Skill: haipipe-norm
================================================================================

The head of the `haipipe-utils` normalizer family. It owns the CONTRACT and no
code; each member ships its own implementation.

    free text in a cohort's own dialect
        -> typed components
        -> a reference bank
        -> numbers that carry their own provenance

    🍎 describe-food       FoodName      -> USDA FDC
                                               -> Calories Carbs Protein Fat Fiber
    🏃 describe-exercise   ExerciseType  -> PA Compendium 2024
                                               -> MET, and kcal when the log
                                                  stated minutes and the mass
                                                  is known
    💊 describe-medication MedicationID  -> FDA NDC Directory
                                               -> ingredient, class, and a dose
                                                  that states its own unit
    💉 describe-insulin    DrugKey       -> insulin PK table
                                               -> class, onset, peak, duration


WHY A CONTRACT AND NOT A BASE PACKAGE
--------------------------------------------------------------------------------

The nouns differ in every particular that matters. A food bank is keyed on a
description and an exercise bank on an activity code. A meal has components; a
session has intervals. The quantity a food log omits is grams, and the one an
exercise log omits is minutes.

What they share is the SHAPE of the problem, not its solution. A base class
written while only one member exists would fit neither, so this file holds the
rules and each member holds its own code.


THE DOOR
--------------------------------------------------------------------------------

Every member exposes exactly one entry point, with this signature:

    normalize(items: list[str]) -> list[dict]

Batch, order-preserving, one result per input, duplicates resolved once. It is
deliberately shaped like a third-party API call: a caller knows the signature and
nothing about the dialect layer, the bank, or the stage sequence, so all of those
can move or be rewritten without a caller changing.

A member picks its transport from `<MEMBER>_TRANSPORT`: `local` in process by
default, `http` against a running service. `local` is the default because a
pipeline cook must not fail because a daemon was down.

A workspace declares where the members live. That is what `env.sh` is for: a
space is the unit of work, and each space puts the normalizer skill dirs it wants
on `PYTHONPATH`, so the package imports as a bare top-level name.


THE FIVE RULES
--------------------------------------------------------------------------------

Each was earned by a real defect in `describe-food`; a new member gets them
for free.

1. ONE DOOR
   `normalize()` and nothing else is public. Anything a caller must know about
   the internals is a leak -- including a stage number in a keyword argument.

2. TYPE, DO NOT DELETE
   A placeholder is CLASSIFIED, never dropped: 'Just Carbs' is a declaration,
   'dinner' a meal slot, 'Unknown' unnamed. So it never reaches the bank, and it
   never sits in the denominator as a failed match. Deleting placeholders made a
   cohort read as 100% miss while its items were matching.

3. TRUSTED ONLY
   Only GOOD / OK / ALIAS may be written into value columns. WEAK and MISS stay
   NULL. A confidently wrong value is worse than a missing one, because nothing
   downstream can tell it apart from a measurement.

4. BASIS IS A COLUMN, NOT A FOOTNOTE
   Never invent the quantity the log did not state. When it is absent, say so in
   a `<X>Basis` column and report on the reference scale instead:
       food      per_meal | per_100g | None
       exercise  per_session | per_minute | None
   Basis is a SCALE, so it is a property of the whole record: mixing one scaled
   component with one unscaled yields a number that is neither.

5. PROVENANCE NEVER FOLDS
   `<X>Source`, `<X>Conf`, `<X>Basis`, and each answers ONE question. When a
   member derives its own input -- food's stage 0 reads a photo into a name --
   that derivation gets its OWN pair (`NameSource`, `NameConf`) and tags the
   source column, so a model's guess can never be mistaken for a report.
   Collapsing two independent failures into one column is the bug this rule
   exists for: 'the bank did not know it' and 'the log stated no portion' once
   shared a single code path.

   describe-exercise needed FOUR: 'this row is not a bout', 'nothing was
   named', 'the vendor's codebook is not on this machine', and 'the bank does
   not list it'. The count is not the point; the point is that each has a
   different fix, so each needs its own value.


WHAT THE SECOND MEMBER ADDED
--------------------------------------------------------------------------------

Two rules that were latent in describe-food and became explicit in
describe-exercise. A third member gets them for free.

6. AN IDENTIFIER IS A NAMESPACE PLUS A CODE
   A cohort's code means nothing without the key that says whose code it is.
   `EntrySourceID` partitions 129 WellDoc exercise codes into four disjoint
   vendor spaces; a SourceFn whitelist had been dropping it, so no codebook
   could ever be applied. And the BANK has its own code space, which overlaps
   the cohort's by coincidence: PA Compendium 20050 is 'Eating at church',
   MET 1.5, while WellDoc 20050 is a 42-minute, 242 kcal workout. Never join on
   a bare integer, and make the wrong join RAISE rather than warn.

   `_FoodInfo/README.md` records the same shape from the other direction:
   `fdc_id`, a food's identity, is computed and then discarded. An identity is
   a column, not a temporary.

7. A CATEGORY WORD IS NOT EVIDENCE FOR A MEMBER
   'Sports' scored a perfect match against 'Judo'. A matcher that folds a
   grouping label into its searchable text will confidently return an arbitrary
   member of the group. Score the thing, not the shelf it sits on -- and when a
   query genuinely does not identify one item, the answer is a candidate for a
   person to curate, never a value.


WHAT THE THIRD AND FOURTH MEMBERS ADDED
--------------------------------------------------------------------------------

describe-medication and describe-insulin arrived as a PAIR, and the pair is the
lesson.

8. A MEMBER MAY CONSUME ANOTHER MEMBER, AND THE SEAM IS A STRING
   Two nouns that need different banks are two members, even when one only ever
   sees rows the other produced. describe-medication resolves a logged row to
   an ingredient; describe-insulin turns that ingredient into onset, peak and
   duration. They CHAIN.

   They are not siblings a caller chooses between, because nothing can tell
   whether MedicationID 612997 is insulin until it has been resolved. The order
   is fixed, and the seam between them is one string field.

   The test for splitting is not 'are they different enough'. It is DO THEY
   REACH DIFFERENT ROWS. 5,445 insulin administrations resolve in
   describe-insulin and in no product directory on earth, because their cohorts
   log a therapeutic class or a product the FDA does not currently list. One
   skill holding both would have to emit records whose identity failed while
   their class was known -- a row that contradicts itself.

   AND A SPLIT MUST BE COUNTED, NOT ASSERTED. That figure read 8,364 until
   describe-insulin got its own `_InsInfo` and the number could be measured per
   cohort; the old one had added ALL of Shanghai's insulin rows to OhioT1DM's,
   as if none of Shanghai's resolved in the first half. 779 do. A chain whose
   members share a folder has nowhere to put the seam table that would have
   caught it, which is the practical argument for one _XInfo per member.

9. THE SEAM FIELD MUST SURVIVE A BANK MISS
   Corollary, and it was a real defect for one measurement cycle. The obvious
   thing to route on is the bank's answer, and the bank's answer is null exactly
   where the second member is most needed. Routing on the FDA ingredient sent
   ZERO of OhioT1DM and 42% of Shanghai's insulin nowhere.

   So the seam carries the best string available -- the bank's word when there
   is one, the log's own words when there is not -- and it is a DIFFERENT field
   from the bank's answer. `DrugKey` is non-null on 100% of insulin rows;
   `Ingredient` on 58% of them. A bank miss is not evidence about the thing.

10. WHERE A BANK LIVES DECIDES WHAT IT CAN SEE
   Resolution was first built into the SourceFn, and the measurement killed it:
   a SourceFn cooks ONE cohort and can only read that cohort's files, so
   WellDoc2025ALS resolved 46.0% of its rows against its own 124-entry export
   while the same rows resolve at 85.2% against the 871 entries pooled from all
   cohorts.

   A bank belongs in `ExternalStore`, and a normalizer reads it. What a SourceFn
   owns is what only a SourceFn can do: read raw files, and lose nothing.


WHAT THE BENCHMARK ADDED
--------------------------------------------------------------------------------

11. A BANK BUILT FROM THE BOARD IS A SECOND PATH TO THE LABEL
   Splitting on PatientID protects the MATCHER. It does not protect the BANK.
   describe-food's T0 tier resolves against a table harvested from the food
   strings patients logged on this very board, so a held-out row is answered
   with the number it is about to be graded against: 98.3% of gold_macros names
   the train split had never seen came back MEASURED, and one cell read r 0.988
   against a frozen baseline of 0.821.

   Two circularity rules, not one. Rule 2's `derived` catches the FRAME case --
   the normalizer wrote this row. This catches the BANK case -- the reference
   contains the row. A member that harvests any part of its bank from cohort
   data must declare `circular_conf`, build a split-aware bank for grading, and
   report both halves. Neither half is dropped; rule 2 forbids that.

12. A BASELINE IS ONLY A BASELINE OVER THE SAME POPULATION
   The same run flagged three apparent regressions against a frozen baseline
   and none was one: the baseline scored every row, the new run scores the
   residual after the bank absorbs the easy ones. When a tier changes WHICH
   rows reach the metric, the old numbers are retired, not compared.


THE SHARED PACKAGES
--------------------------------------------------------------------------------

haipipe-norm ships no resolver and two packages every member imports:

    xinfo    the `_stats.json` record shape. One schema, so a reader of
             _FoodInfo and a reader of _ExerciseInfo learn one layout.
    xbench   the benchmark harness. The split rule, the circularity bans, the
             row/dedup double run and the regression comparator are written
             once; a member supplies a NounSpec -- its cells, its columns, its
             metric -- and nothing else.

A member's benchmark is therefore small, and lives at
`describe-<noun>/benchmark/`, with its DATA under
`_WorkSpace/0-RawDataStore/0-EventNorm/_<Noun>Info/6-benchmark/` and a `code`
symlink pointing back. Code in git, data in the store, one copy of each.


ADDING A MEMBER
--------------------------------------------------------------------------------

A member is named `describe-<noun>`: the verb first, because the folder names what
the skill DOES to that noun, and a reader scanning the skill list groups the family
on sight instead of on a suffix they have to read to the end of.

    skills/describe-<noun>/
        SKILL.md            its dialect, its bank, its measured coverage
        <noun>norm/
            client.py       normalize() + the transport switch
            dialect.py      text -> typed components
            retrieve.py     component -> bank candidates + a confidence ladder
            aggregate.py    components -> one record, with its basis
        pipeline.py         CLI
        test_<noun>norm.py  regression suite
        benchmark/          cells, spec, metric. The harness is xbench's.

Then add one line to the workspace `env.sh` putting that skill dir on
`PYTHONPATH`, and register nothing else: the plugin manifest already covers the
folder.
