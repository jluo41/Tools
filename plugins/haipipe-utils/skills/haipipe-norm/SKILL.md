---
name: haipipe-norm
description: "The contract every describe-* normalizer obeys: free text in a cohort's own dialect, resolved against a reference bank, into numbers that carry their own provenance. Owns the five rules, the door signature and the event JSON checklist (raw, input, output); ships no code. Load before building or changing a normalizer. Trigger: normalizer contract, new normalizer, event JSON, raw input output, event checklist, describe-food, describe-exercise, normalize door, provenance columns, basis column, haipipe-utils."
metadata:
  version: "0.5.0"
  last_updated: "2026-11-02"
  members: "describe-food (0.8.0) · describe-exercise (0.5.1) · describe-medication (0.1.2) · describe-insulin (0.1.2)"
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
pipeline cook must not fail because a daemon was down. The service is the
member's api lane, `servers/api-<noun>/server.py`, which the plugin host
`servers/_host/serve.py` mounts at `http://127.0.0.1:8070/<noun>`; `<MEMBER>_URL`
names that address and `client.py` appends `/normalize/batch`.

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

    eventnorm  the event layer (2026-10-21, food first): raw as it arrives ->
             preprocess/ (a file a raw type) -> the input JSON -> the noun's
             enrich(items) -> the output by local hour (hours.py by_hour, the
             one every event type shares). Served as POST /meal/event; its
             test sends b51 s01 ③'s eight real meals, read in place, and wants
             them back byte for byte but for one named difference. A member
             still answers only its items: time and the meal's own numbers
             pass by it. What the JSON must hold: THE EVENT JSON, below.


THE EVENT JSON: RAW, INPUT, OUTPUT
--------------------------------------------------------------------------------

Every event door (eventnorm: POST /meal/event, /exercise/event, /medication/event,
/insulin/event) answers one JSON of three parts. Each rule below came from a real
row someone questioned in b51's API topics (s01 food, s02 exercise, s03
medication, s04 insulin; the s01-Dnn numbers are decisions in s01-food-api.md).
Check a new event type, or a change to one, against this list. A noun's own rules
(food's items, nutrients, GI and checks) are in its member's SKILL.md.

    raw     what arrived, as it arrived            never cleaned, never added to
    input   what the preprocess step makes of it   one shape, whatever the source
    output  the input, enriched from the tables    keyed by local hour

**The whole**

    [ ] E1  Three parts and nothing else: {"raw", "input", "output"}. A field that
            is a column of the raw row stays in raw (s01-D20). A saved example may
            add "example" and "note" around them.
    [ ] E2  Nothing named is no output, never a guessed one: input.items is null;
            a raw that names no event at all has input and output null and a
            "note" saying why.

**Raw**

    [ ] R1  {"type", "file"?, "rows": [{column: text}]}: every column of every row,
            as text, in the source's order (s01-D36).
    [ ] R2  Only the columns saying whose row it is are dropped (schema.py
            RAW_DROP: PatientID, id, ObservationCreatedBy).
    [ ] R3  raw.type is one of the type's RAW_TYPES, and it alone picks the
            preprocess step.

**Input**

    [ ] I1  Its keys are the type's INPUT_KEYS, in that order, coarse to fine:
            the times, the kind (meal_type), total, items, timeline, source.
    [ ] I2  Times are local with their offset, "2021-04-14 07:17 -04:00"; bare
            only when the raw names no zone. start is when it happened, logged_at
            when it was typed (s01-D36); end is null unless the raw gives one.
    [ ] I3  Every number says its unit: in its text ("32.45 g", food), in its key
            ("minutes", exercise) or in a "unit" field beside it (medication).
    [ ] I4  total is the event's own numbers as the raw states them, kept even
            when there are no items (s01-D23). A number the raw does not give is
            LEFT OUT, never 0 and never null (s01-D28); an app's 0 or sentinel that
            means "not given" counts as not given (s01-D45; medication SENTINELS).
    [ ] I5  items: one thing each, ids i1..iN; null when nothing is named. A
            placeholder ('Just Carbs', "data not available") makes no item (rule
            2; s01-D48).
    [ ] I6  timeline is null unless the raw logs points (a bite, a minute, a
            delivery); one name for every type (s01-D24).
    [ ] I7  source comes last: {"kind": "logged"}, or {"kind": "detected", "rule",
            ...} for an event a rule found in a stream, which has no items and no
            total and must never read as a logged one (s01-D47).

**Output**

    [ ] O1  Keyed by local hour, "2021-04-14 07:00 -04:00"; each hour holds the
            input's keys in the input's order.
    [ ] O2  A moment (a meal, a dose) has a "share" first, the shares sum to 1,
            and with no end the start's hour holds it all. A stretch (exercise)
            gives each hour its own numbers instead (s02-D23); a dose that acts
            for hours is spread by its curve (insulin).
    [ ] O3  Each output item repeats its input item's fields, in the same order,
            then what the tables add, so every item names itself (s01-D50).
    [ ] O4  Only a trusted match gives numbers (rule 3). In the output a null says
            "the tables have none"; in the input a missing field says "the raw
            gave none". The two are never mixed.
    [ ] O5  The logged numbers are never overwritten. Where the input has a total,
            the output sets its own beside it and says whether they agree
            (food: total.check, s01-D51).

**Where each type stands** (2026-11-02, read from each topic's saved examples
and a live call; 23 examples):

    rule                        food   exercise   medication   insulin
    E1-R3 parts, raw            ✅     ✅          ✅            ✅
    I1 keys in order            ✅     ✅          ✅            ✅
    I2 logged_at                ✅     ❗ none      ✅            ✅
    I3, I4 units, left out      ✅     ✅          ✅            ✅
    I7 source last              ✅     ❗ none      ✅            ❗ before timeline
    O1, O2 by hour              ✅     ✅          ✅            ✅
    O3 item repeats its input   ✅     ✅          ❗ drug words  🔶 drug, not dose
    O5 checks the log           ✅     ⬜          ⬜            ⬜

Exercise kept its own schema when "source" came in (s01-D47). s03's saved
medication example predates "source"; the live door gives it.


THE EVENT RELEASE: WHERE A MEMBER'S TABLES COME FROM
--------------------------------------------------------------------------------

Every table a member reads is a versioned ext_ asset in the workspace ExternalStore,
built, validated and pinned in `examples-1-data/Proj01-CGM-RawData/tasks/b51_externalstore`
(the diabetes event external store). A member finds a table through the release, not a
hard-coded folder:

    paths.py release_file(asset, filename=None)   the pinned file, sha256 checked
    <noun>norm/_release.py                        loads paths.py beside the skill; no PYTHONPATH

The release is `$EVENTNORM_RELEASE` (default `EventNormV6`, the release the newest WellDoc SourceFn, `WellDocDataExtV260930`, reads); `EVENTNORM_RELEASE=none`, or a
release that does not pin the asset, falls back to the old flat folder. Each member's
answers are also frozen there as `ext_<noun>_resolved`, one row per distinct request
in the WellDoc Source tables, so a SourceFn looks an answer up and never calls a
member during a build. After changing a member or its tables, freeze a new version
and write a new release; that Block's parity Runs say whether anything moved.


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

    servers/api-<noun>/         the same normalize() on the wire (servers/README.md)
        server.py           FastAPI: /healthz /normalize /normalize/batch
        tests/test_server.py the black-box service suite, run against <MEMBER>_URL
        examples/           recorded request/response cases, generated

Then add one line to the workspace `env.sh` putting that skill dir on
`PYTHONPATH`, and register nothing else: the plugin manifest already covers the
folder, and the host mounts `servers/api-<noun>/server.py` by folder name.
